"""Portable synthetic regression checks. These do not certify semantic quality."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('reader',ROOT/'skills/markkiller/scripts/reader.py')
reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.base=ROOT/'docs/demo'
        self.data=json.loads((self.base/'reader.json').read_text(encoding='utf-8'))
    def test_self_contained_and_complete(self):
        output=reader.build(self.data,self.base)
        class Page(HTMLParser):
            def __init__(self):super().__init__();self.ids=[];self.links=[];self.src=[];self.text=[]
            def handle_starttag(self,tag,attrs):
                a=dict(attrs)
                if 'id' in a:self.ids.append(a['id'])
                if tag=='a':self.links.append(a['href'])
                if 'src' in a:self.src.append(a['src'])
            def handle_data(self,s):self.text.append(s)
        page=Page();page.feed(output)
        self.assertEqual(len(page.ids),len(set(page.ids)))
        self.assertTrue(all(x[1:] in page.ids for x in page.links if x.startswith('#')))
        self.assertTrue(all(x.startswith('data:') for x in page.src))
        text=''.join(page.text)
        for i in self.data['items']:
            for s in i['sections']:
                for p in s['paragraphs']:self.assertIn(p.replace('**',''),text)
    def test_html_in_source_stays_text(self):
        self.data['items'][0]['title']='<script>alert(1)</script>'
        output=reader.build(self.data,self.base)
        self.assertNotIn('<script>alert(1)</script>',output)
        self.assertIn('&lt;script&gt;',output)
    def test_unsafe_source_link_is_rejected(self):
        self.data['items'][0]['url']='javascript:alert(1)'
        with self.assertRaises(ValueError):reader.validate(self.data,self.base)
    def test_media_cannot_escape_workspace(self):
        self.data['items'][0]['cover']['path']='../../README.md'
        with self.assertRaises(ValueError):reader.validate(self.data,self.base)
    def test_pending_cannot_present_analysis(self):
        self.data['items'][0]['status']='pending'
        with self.assertRaises(ValueError):reader.validate(self.data,self.base)
    def test_duplicate_work_is_rejected(self):
        item=copy.deepcopy(self.data['items'][0]);item['id']='other';item['work_id']='same'
        self.data['items'][0]['work_id']='same';self.data['items'].append(item)
        with self.assertRaises(ValueError):reader.validate(self.data,self.base)
    def test_two_video_parts_count_one_work(self):
        a=self.data['items'][0];a.update(kind='video',work_id='course',part=1,parts_total=2)
        b=copy.deepcopy(a);b.update(id='part-2',part=2);self.data['items'].append(b)
        self.assertEqual(reader.validate(self.data,self.base)['video_works'],1)
    def test_missing_diagram_target_is_rejected(self):
        self.data['items'][0]['diagram']['nodes'][0]['section']=99
        with self.assertRaises(ValueError):reader.validate(self.data,self.base)
    def test_unknown_date_does_not_invent_a_date(self):
        self.assertEqual(reader.date_key('未知'),'')
        self.assertEqual(reader.date_key('2026-02-30'),'')
        self.assertEqual(reader.date_key('2026-11-02T08:00:00+08:00'),'2026-11-02')
    def test_generated_candidate_preserves_original(self):
        import subprocess,sys
        with tempfile.TemporaryDirectory() as tmp:
            output=Path(tmp)/'reading.html';output.write_text('user edits',encoding='utf-8')
            run=subprocess.run([sys.executable,str(ROOT/'skills/markkiller/scripts/reader.py'),'build','--input',str(self.base/'reader.json'),'--output',str(output)],capture_output=True)
            self.assertEqual(run.returncode,0)
            self.assertEqual(output.read_text(encoding='utf-8'),'user edits')
            self.assertTrue(output.with_name('reading.proposed.html').exists())

if __name__=='__main__':unittest.main()

import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('selection', ROOT/'skills/markkiller/scripts/check_selection.py')
selection = importlib.util.module_from_spec(spec)
spec.loader.exec_module(selection)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        self.row = dict(id='sample', platform='test', work_id='work', title='A lesson',
                        source_url='https://example.org/video', favorite_sources=['imported catalog'],
                        decision='selected', reason='Body explains model evaluation',
                        evidence=[dict(kind='transcript', text='Evaluation separates training and testing', locator='01:20')],
                        reader_ids=['reading'])
        self.data = dict(schema_version=1, criteria='AI', requested_count=1, count_unit='work',
                         catalog_boundary='One imported entry', entries=[self.row])
        self.reader = dict(items=[dict(id='reading', platform='test', work_id='work', status='deep')])
    def test_complete_mapping(self):
        self.assertEqual(selection.check(self.data,self.reader,True)['errors'], [])
    def test_titles_do_not_certify_selection(self):
        self.row['evidence'][0]['kind']='title'
        self.assertTrue(selection.check(self.data,self.reader)['errors'])
    def test_pending_not_completed(self):
        self.reader['items'][0]['status']='pending'
        r=selection.check(self.data,self.reader,True)
        self.assertEqual(r['completed'],0)
        self.assertTrue(r['errors'])
    def test_external_material_cannot_sneak_into_reader(self):
        self.reader['items'].append(dict(id='external', status='deep'))
        self.assertTrue(selection.check(self.data,self.reader)['errors'])
    def test_duplicate_favorite_does_not_double_count(self):
        other=copy.deepcopy(self.row);other.update(id='second',reader_ids=[])
        self.data['entries'].append(other)
        self.assertTrue(selection.check(self.data,self.reader)['errors'])
    def test_part_scope_requires_explicit_part(self):
        self.data['count_unit']='part'
        self.assertTrue(selection.check(self.data,self.reader)['errors'])
        self.row['part']=1;self.reader['items'][0]['part']=1
        self.assertFalse(selection.check(self.data,self.reader)['errors'])
    def test_shortfall_retained_until_exact_delivery(self):
        self.data['requested_count']=30
        r=selection.check(self.data,self.reader)
        self.assertEqual(r['shortfall'],29)
        self.assertFalse(r['errors'])
        self.assertTrue(selection.check(self.data,self.reader,True)['errors'])
    def test_wrong_source_mapping_rejected(self):
        self.reader['items'][0]['work_id']='other'
        self.assertTrue(selection.check(self.data,self.reader)['errors'])
    def test_missing_favorites_provenance_rejected(self):
        self.row['favorite_sources']=[]
        self.assertTrue(selection.check(self.data,self.reader)['errors'])

if __name__=='__main__':unittest.main()

"""Validate review bindings; does not judge semantic truth."""
import argparse
import hashlib
import json
from pathlib import Path

DIMENSIONS={'fidelity','explanation','examples_process','boundaries','traceability','readability'}

def verify(base, review, reader_path):
    base=base.resolve(); reader_path=reader_path.resolve()
    if not reader_path.is_relative_to(base): raise ValueError('阅读数据必须在任务目录内')
    d=json.loads(reader_path.read_text(encoding='utf-8-sig'))
    if review.get('review_contract')!=1 or not review.get('reviewer') or not review.get('reviewed_at'):
        raise ValueError('缺少审阅合同、审阅者或实际日期')
    deps=review.get('dependencies',{})
    if reader_path.relative_to(base).as_posix() not in deps: raise ValueError('未绑定当前阅读数据')
    if not any(k.startswith('raw/') for k in deps) or not any(k.startswith('output/') and k.endswith('.html') for k in deps):
        raise ValueError('须绑定原稿与实际交付HTML')
    for relative,expected in deps.items():
        p=(base/relative).resolve()
        if not p.is_relative_to(base) or not p.is_file(): raise ValueError('依赖不存在或越界: '+relative)
        if hashlib.sha256(p.read_bytes()).hexdigest()!=expected: raise ValueError('审阅已过期: '+relative)
    completed={i['id'] for i in d['items'] if i['status']!='pending'}
    items=review.get('items',[])
    if len({i['id'] for i in items})!=len(items): raise ValueError('审阅条目重复')
    if {i['id'] for i in items} != completed: raise ValueError('审阅范围不一致')
    content_by_id={i['id']:i for i in d['items']}
    for i in items:
        cover=content_by_id[i['id']].get('cover')
        if cover:
            path=(reader_path.parent/cover['path']).resolve()
            if not path.is_relative_to(base) or path.relative_to(base).as_posix() not in deps:
                raise ValueError('原视频封面未绑定审阅')
        sources=i.get('source_files')
        if not isinstance(sources,list) or not sources or any(not isinstance(s,str) or not s.startswith('raw/') or s not in deps for s in sources):
            raise ValueError('逐篇原稿必须明确绑定到已核依赖: '+i['id'])
        for section in content_by_id[i['id']].get('sections',[]):
            for im in section.get('images',[]):
                image_path=(reader_path.parent/im['path']).resolve()
                if not image_path.is_relative_to(base) or image_path.relative_to(base).as_posix() not in deps:
                    raise ValueError('展示图片未绑定审阅: '+im['path'])
        scores=i.get('scores',{})
        if set(scores)!=DIMENSIONS or any(type(v)!=int or not 0<=v<=3 for v in scores.values()): raise ValueError('六维评分无效')
        if min(scores.values())<2: raise ValueError('有未达可用标准的维度，应返工或简读重新审阅')
        if i.get('status') not in ('pass','pass_with_disclosed_limits') or not i.get('findings'): raise ValueError('缺少实际审阅依据')
    return {'bindings':'current','reviewed_items':len(items),'semantic_truth':'requires_actual_reading','checks':review.get('checks',{})}

def main():
    p=argparse.ArgumentParser();p.add_argument('--workspace',required=True);p.add_argument('--reader',default='reader.json');p.add_argument('--review',default='review.json');a=p.parse_args()
    base=Path(a.workspace); rp=(base/a.review).resolve()
    if not rp.is_relative_to(base.resolve()): raise ValueError('审阅文件必须在任务内')
    print(json.dumps(verify(base,json.loads(rp.read_text(encoding='utf-8-sig')),base/a.reader),ensure_ascii=False))

if __name__=='__main__': main()

"""Validate reading data and render a self-contained HTML. No network access."""
import argparse
import base64
import html
import json
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.gif':'image/gif'}

def esc(value):
    return html.escape(str(value), quote=True)

def url(value):
    p = urlsplit(value)
    if p.scheme not in ('http', 'https') or not p.hostname or p.username or p.password:
        raise ValueError('来源只允许无凭据的 HTTP/HTTPS 阅读链接')
    return value

def media(base, relative):
    p = (base / relative).resolve()
    if not p.is_relative_to(base.resolve()) or p.suffix.lower() not in TYPES or not p.is_file():
        raise ValueError('图片必须是任务目录内存在的 PNG/JPG/WebP/GIF')
    return p

def strings(values, name):
    if not isinstance(values,list) or any(not isinstance(s,str) or not s.strip() for s in values):
        raise ValueError(name+' 必须为非空文本组成的列表')

def validate(d, base):
    if d.get('schema_version') != 1 or not d.get('title') or not d.get('scope'):
        raise ValueError('需要 schema_version=1、title 与 scope')
    if not isinstance(d.get('items'),list) or not d['items']:
        raise ValueError('items 不可为空')
    ids = set(); versions=set(); videos=set(); articles=set()
    for i in d['items']:
        for k in ('id','title','platform','kind','author','url','date','topic','summary','status','coverage'):
            if not isinstance(i.get(k),str) or not i[k].strip():
                raise ValueError('缺少文本字段 '+k)
        if i['id'] in ids: raise ValueError('重复作品 ID: '+i['id'])
        ids.add(i['id']); url(i['url'])
        identity=(i['platform'],i.get('work_id',i['id']),i.get('version','original'))
        if 'part' in i or 'parts_total' in i:
            if not i.get('work_id') or type(i.get('part'))!=int or i['part']<1 or type(i.get('parts_total'))!=int or i['parts_total']<i['part']:
                raise ValueError('分P需要work_id、有效part和parts_total')
        unit_key=identity+(i.get('part'),)
        if unit_key in versions: raise ValueError('重复作品版本/分P')
        versions.add(unit_key)
        (videos if i['kind']=='video' else articles).add(identity)
        if i['kind'] not in ('video','article') or i['status'] not in ('deep','brief','pending'):
            raise ValueError('无效类型或状态')
        for key in ('reading_title','takeaway'):
            if key in i and (not isinstance(i[key],str) or not i[key].strip()):raise ValueError(key+' 必须是文本')
        if i['status']=='pending' and i.get('takeaway'): raise ValueError('待核索引不可提供结论摘要')
        strings(i.get('introduction',[]),'introduction')
        if i['status']=='pending' and i.get('introduction'): raise ValueError('待核索引不可提供整体讲解')
        if i.get('cover'):
            media(base,i['cover']['path']); url(i['cover']['source_url'])
            if not i['cover'].get('caption'):raise ValueError('封面需要说明')
        sections=i.get('sections',[])
        if not isinstance(sections,list): raise ValueError('sections 必须为列表')
        if i['status']=='pending' and sections: raise ValueError('待核索引不可含深读')
        if i['status']!='pending' and not sections: raise ValueError('已读项需要正文与依据')
        for s in sections:
            if not isinstance(s.get('heading'),str) or not s['heading'].strip(): raise ValueError('缺少小节标题')
            strings(s.get('paragraphs'),'paragraphs')
            if not s['paragraphs'] or not s.get('evidence'): raise ValueError('正文与证据不可为空')
            for e in s['evidence']:
                if not e.get('label'): raise ValueError('证据需要定位')
                if e.get('url'): url(e['url'])
            for im in s.get('images',[]):
                media(base,im['path'])
                if not im.get('caption'): raise ValueError('图片需要说明')
                if 'after' in im and (type(im['after'])!=int or not 1<=im['after']<=len(s['paragraphs'])):
                    raise ValueError('图片位置必须指向已有段落')
        diagram=i.get('diagram')
        if diagram:
            if i['status']=='pending' or diagram.get('kind') not in ('flow','map') or not diagram.get('title') or not diagram.get('caption'):
                raise ValueError('关系图需要类型、标题、归属说明和已核正文')
            if type(diagram.get('after_section'))!=int or not 0<=diagram['after_section']<=len(sections):
                raise ValueError('关系图插入位置无效')
            if not isinstance(diagram.get('nodes'),list) or len(diagram['nodes'])<2:
                raise ValueError('关系图至少需要两个有关系的节点')
            for node in diagram['nodes']:
                if not node.get('label') or not node.get('detail') or type(node.get('section'))!=int or not 1<=node['section']<=len(sections):
                    raise ValueError('关系图节点必须能回到已有章节')
        for key in ('practice','limitations'): strings(i.get(key,[]),key)
    for c in d.get('connections',[]):
        if not c.get('heading') or not c.get('item_ids') or not set(c['item_ids']) <= ids:
            raise ValueError('关联必须引用真实条目')
        strings(c.get('paragraphs'),'关联正文')
    return {'items':len(ids),'video_works':len(videos),'article_works':len(articles),'completed':sum(i['status']!='pending' for i in d['items']), 'semantic_review':'not_automated'}

def image_tag(base, im, zoom=False):
    p=media(base,im['path'])
    src='data:'+TYPES[p.suffix.lower()]+';base64,'+base64.b64encode(p.read_bytes()).decode()
    img=f'<img src="{src}" alt="{esc(im["caption"])}" loading="lazy">'
    if zoom: img=f'<button class="image-zoom" type="button" aria-label="放大原作画面：{esc(im["caption"])}">{img}</button>'
    return f'<figure>{img}<figcaption>{esc(im["caption"])}'+(' <span class="zoom-hint">点击画面放大</span>' if zoom else '')+'</figcaption></figure>'

def rich(value):
    # Only paired **emphasis** is interpreted. All other input stays escaped text.
    return re.sub(r'\*\*([^*\n]+)\*\*',r'<strong>\1</strong>',esc(value))

def paragraphs(values): return ''.join('<p>'+rich(v)+'</p>' for v in values)

def diagram_html(diagram,anchor):
    if not diagram: return ''
    nodes=''.join(f'<li><a href="#{anchor}-s{x["section"]}"><strong>{str(n).zfill(2)+" · " if diagram["kind"]=="flow" else ""}{esc(x["label"])}</strong><span>{esc(x["detail"])}</span></a></li>' for n,x in enumerate(diagram['nodes'],1))
    tag='ol' if diagram['kind']=='flow' else 'ul'
    stacked=' flow-stacked' if diagram['kind']=='flow' and len(diagram['nodes'])>5 else ''
    columns=f' style="--flow-columns:{len(diagram["nodes"])}"' if diagram['kind']=='flow' else ''
    return f'<figure class="diagram {diagram["kind"]}{stacked}" id="{anchor}-diagram"><h3>{esc(diagram["title"])}</h3><{tag}{columns}>{nodes}</{tag}><figcaption>{esc(diagram["caption"])}</figcaption></figure>'

def date_key(value):
    """Unknown dates remain visible and sort after verified publication dates."""
    try:
        return datetime.fromisoformat(value.replace('Z','+00:00')).strftime('%Y-%m-%d')
    except ValueError:
        return ''

def build(d, base, *, index_only=False, item_links=None):
    stats=validate(d,base)
    topics=list(dict.fromkeys(i['topic'] for i in d['items']))
    rows=[]; cards=[]
    labels={'deep':'深读','brief':'简读','pending':'待核'}
    for n,i in enumerate(d['items'],1):
        search_text=[i['title'],i['author'],i['summary'],i['topic'],i.get('reading_title',''),i.get('takeaway','')]
        for s in i.get('sections',[]):search_text.extend([s['heading'],*s['paragraphs'],*[im['caption'] for im in s.get('images',[])]])
        if i.get('diagram'):
            search_text.extend([i['diagram']['title'],i['diagram']['caption']])
            for node in i['diagram']['nodes']:search_text.extend([node['label'],node['detail']])
        search_text.extend(i.get('practice',[])+i.get('limitations',[])+i.get('introduction',[]))
        attrs=f'data-topic="{esc(i["topic"])}" data-search="{esc(" ".join(search_text).replace("**", "").lower())}"'
        anchor='item-'+str(n)
        target='#'+anchor
        if item_links:
            target=item_links[i['id']]
            if not re.fullmatch(r'[\w-]+\.html#item-\d+',target):
                raise ValueError('独立索引只允许本目录HTML阅读链接')
        tn=topics.index(i['topic'])+1
        date=date_key(i['date'])
        date_label=date or i['date']
        byline=' · '.join(esc(x) for x in [i['author'],i.get('duration','')] if x)
        metadata=' · '.join(esc(x) for x in [i['author'],date_label,i.get('duration','')] if x)
        citation_label='回看原片' if i['kind']=='video' else '查看原文'
        cover_link=''
        if i.get('cover'):
            cover_link=f'<a class="index-cover" href="{esc(target)}" aria-label="打开解读：{esc(i["title"])}">{image_tag(base,i["cover"])}</a>'
        else:
            cover_link='<span class="cover-missing">暂无已核封面</span>'
        rows.append(f'<tr class="index-entry" {attrs} data-date="{date}" data-order="{n}" data-topic-number="{tn}"><td class="index-date">{esc(date_label)}</td><td class="index-content"><div class="index-work">{cover_link}<div><span class="topic-tag topic-{tn%6}">{tn:02d} · {esc(i["topic"])}</span><a class="index-title" href="{esc(target)}">{esc(i["title"])} <span class="read-link">内容解读 →</span></a><p class="index-author">{byline}</p></div></div></td><td class="index-summary">{esc(i["summary"])}</td><td class="index-platform">{esc(i["platform"])}</td><td class="index-status">{labels[i["status"]]}</td></tr>')
        cover=image_tag(base,i['cover']) if i.get('cover') else ''
        body=''
        toc=[]
        for sn,s in enumerate(i.get('sections',[]),1):
            section_id=f'{anchor}-s{sn}'
            toc.append(f'<a href="#{section_id}">{esc(s.get("nav_title",s["heading"]))}</a>')
            evidence=' · '.join(f'<a href="{esc(url(e.get("url",i["url"])))}" target="_blank" rel="noopener noreferrer">{esc(e["label"])}</a>' for e in s['evidence'])
            prose=''
            for pn,p in enumerate(s['paragraphs'],1):
                prose+=paragraphs([p])+''.join(image_tag(base,im,True) for im in s.get('images',[]) if im.get('after')==pn)
            prose+=''.join(image_tag(base,im,True) for im in s.get('images',[]) if 'after' not in im)
            body+=f'<section id="{section_id}" class="reading-section"><h3><span class="section-number">{sn:02d}</span>{esc(s["heading"])}</h3>{prose}<p class="evidence">{citation_label}：{evidence}</p></section>'
            if i.get('diagram',{}).get('after_section')==sn: body+=diagram_html(i['diagram'],anchor)
        if i.get('limitations'): body+='<section class="note"><h3>理解边界</h3>'+paragraphs(i['limitations'])+'</section>'
        if i.get('practice'): body+='<section class="practice"><h3>可以试一试</h3>'+paragraphs(i['practice'])+'</section>'
        overview=f'<div class="takeaway"><span class="eyebrow">{"材料待核" if i["status"]=="pending" else "先抓住重点 · 解读提炼"}</span><p>{rich(i.get("takeaway",i["summary"]))}</p></div>'
        navigation='<nav class="section-nav" aria-label="本篇章节">'+''.join(toc)+'</nav>' if len(toc)>2 and i.get('diagram',{}).get('after_section')!=0 else ''
        source=f'<details class="source-details"><summary>原作信息与解读范围</summary><p>原作：{esc(i["title"])}</p><p>{esc(i["coverage"])}</p></details>'
        opening=''
        if i.get('introduction'):
            opening='<section class="opening"><span class="eyebrow">整体讲解</span><h3>'+esc(i.get('reading_title',i['title']))+'</h3>'+paragraphs(i['introduction'])+'</section>'
        if i.get('diagram',{}).get('after_section')==0:opening+=diagram_html(i['diagram'],anchor)
        cards.append(f'<article id="{anchor}" {attrs}><header class="video-header {'has-cover' if cover else ''}"><div class="video-cover">{cover}</div><div class="video-identity"><span class="eyebrow">第 {n:02d} 篇 · 主题 {tn:02d} / {esc(i["topic"])} · {labels[i["status"]]}</span><h2>{esc(i["title"])}</h2><p class="meta">{metadata} · 内容来源：<a href="{esc(url(i["url"]))}" target="_blank" rel="noopener noreferrer">{esc(i["platform"])}</a></p></div><button class="toggle" aria-expanded="true" aria-controls="body-{n}">收起 ↑</button></header>{overview}{source}<div id="body-{n}" class="body">{opening}{navigation}{body}</div></article>')
    connections=''
    for c in d.get('connections',[]):
        refs=' · '.join(f'<a href="#item-{j}">{esc(i["title"])}</a>' for j,i in enumerate(d['items'],1) if i['id'] in c['item_ids'])
        connections+=f'<section><h3>{esc(c["heading"])}</h3>{paragraphs(c["paragraphs"])}<p>{refs}</p></section>'
    if connections: connections='<article id="connections"><h2>放在一起理解</h2>'+connections+'</article>'
    developer=''
    devfile=ROOT/'assets/project-developer.json'
    if devfile.exists():
        dev=json.loads(devfile.read_text(encoding='utf-8-sig'))
        developer=image_tag(ROOT/'assets',{'path':dev['avatar']['path'],'caption':dev['avatar']['caption']})+f'<p>{esc(dev["role"])}<br><strong>{esc(dev["name"])}</strong></p>'+' · '.join(f'<a href="{esc(url(l["url"]))}">{esc(l["label"])}</a>' for l in dev['links'])
    css=(ROOT/'assets/reader.css').read_text(encoding='utf-8')
    js=(ROOT/'assets/reader.js').read_text(encoding='utf-8')
    options=''.join(f'<option value="{esc(t)}">{esc(t)}</option>' for t in topics)
    groups=[]
    for tn,t in enumerate(topics,1):
        members=sorted([j for j,i in enumerate(d['items']) if i['topic']==t],key=lambda j:date_key(d['items'][j]['date']),reverse=True)
        groups.append(f'<tbody class="index-group"><tr class="group-heading"><th colspan="5" scope="rowgroup"><span class="topic-tag topic-{tn%6}">主题 {tn:02d}</span> {esc(t)} <small>{len(members)} 项</small></th></tr>'+''.join(rows[j] for j in members)+'</tbody>')
    index='<table id="content-index"><thead><tr><th scope="col">发布日期</th><th scope="col">内容</th><th scope="col">内容简介</th><th scope="col">平台</th><th scope="col">阅读</th></tr></thead>'+''.join(groups)+'</table>'
    view_controls='<div class="index-toolbar"><div class="view-switch" role="group" aria-label="索引分类"><button type="button" data-view="topic" aria-pressed="true">按主题</button><button type="button" data-view="time" aria-pressed="false">按时间</button></div><p id="index-order-note">按主题分组，组内按发布时间从新到旧</p></div>'
    if index_only:
        cards=[];connections=''
    scope_parts=[f'{stats["items"]} 个阅读单元',f'{stats["completed"]} 个已解读']
    if stats['video_works']:scope_parts.append(f'{stats["video_works"]} 部视频')
    if stats['article_works']:scope_parts.append(f'{stats["article_works"]} 篇图文')
    scope_stats=' · '.join(scope_parts)
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; img-src data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'"><title>{esc(d['title'])}</title><style>{css}</style></head><body><aside><a class="brand" href="#home">MarkKiller</a><p>收藏夹杀手 · 让收藏不止于收藏。</p><nav><a href="#map">内容地图</a>{'<a href="#readings">深度解读</a>' if not index_only else ''}{'<a href="#connections">关联理解</a>' if connections else ''}</nav><div class="developer">{developer}</div></aside><main><header id="home" class="hero"><span class="eyebrow">COLLECTION → UNDERSTANDING</span><h1>{esc(d['title'])}</h1><p>{esc(d['scope'])}</p><p class="meta">{scope_stats}</p></header><section id="map"><h2>内容汇总</h2>{view_controls}<details class="filter-tools"><summary>搜索与展开选项</summary><div class="controls"><label>搜索<input id="search" type="search" aria-label="搜索" placeholder="标题、作者、内容"></label><label>主题<select id="topic" aria-label="主题"><option value="">全部主题</option>{options}</select></label><button id="reset">清除筛选</button>{'<button id="expand">展开当前结果</button><button id="collapse">收起当前结果</button>' if not index_only else ''}</div></details><p id="count" role="status"></p><p id="empty" hidden>没有匹配内容，清除筛选即可恢复。</p>{index}</section><div id="readings">{''.join(cards)}</div>{connections}<footer>来源可回查 · 解读不代表已掌握 · 阅读正文与图片可离线使用</footer></main><dialog id="image-dialog" aria-label="原作画面放大"><button id="close-image" autofocus>关闭 ×</button><img alt=""><p></p></dialog><script>{js}</script></body></html>'''

def main():
    p=argparse.ArgumentParser(); p.add_argument('command',choices=['validate','build']); p.add_argument('--input',required=True); p.add_argument('--output')
    args=p.parse_args(); source=Path(args.input).resolve(); d=json.loads(source.read_text(encoding='utf-8-sig'))
    stats=validate(d,source.parent)
    if args.command=='build':
        if not args.output: p.error('build requires --output')
        dest=Path(args.output)
        if dest.exists(): dest=dest.with_name(dest.stem+'.proposed'+dest.suffix)
        if dest.exists(): raise ValueError('候选也已存在，请指定新输出文件以保留已有修改')
        dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(build(d,source.parent),encoding='utf-8'); stats['output']=str(dest.resolve())
    print(json.dumps(stats,ensure_ascii=False))

if __name__=='__main__': main()

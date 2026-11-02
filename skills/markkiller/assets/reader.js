(()=>{'use strict';
const cards=[...document.querySelectorAll('#readings article')],rows=[...document.querySelectorAll('.index-entry')];
const search=document.querySelector('#search'),topic=document.querySelector('#topic');
const index=document.querySelector('#content-index'),viewButtons=[...document.querySelectorAll('[data-view]')];
let view='topic';
function arrange(){
 if(!index)return;
 const sorted=[...rows].sort((a,b)=>{
  if(view==='topic'&&a.dataset.topicNumber!==b.dataset.topicNumber)return Number(a.dataset.topicNumber)-Number(b.dataset.topicNumber);
  return b.dataset.date.localeCompare(a.dataset.date)||Number(a.dataset.order)-Number(b.dataset.order);
 });
 const groups=new Map();
 sorted.forEach(row=>{const key=view==='topic'?row.dataset.topic:(row.dataset.date.slice(0,7)||'日期待核');if(!groups.has(key))groups.set(key,[]);groups.get(key).push(row)});
 index.querySelectorAll('tbody').forEach(b=>b.remove());
 for(const [key,members] of groups){
  const body=document.createElement('tbody');body.className='index-group';
  const head=document.createElement('tr');head.className='group-heading';
  const cell=document.createElement('th');cell.colSpan=5;cell.scope='rowgroup';
  if(view==='topic'){const n=Number(members[0].dataset.topicNumber),badge=document.createElement('span');badge.className='topic-tag topic-'+n%6;badge.textContent='主题 '+String(n).padStart(2,'0');cell.append(badge,document.createTextNode(' '+key+' '));}
  else cell.append(document.createTextNode(key.replace(/^(\d{4})-(\d{2})$/,'$1 年 $2 月')+' '));
  const count=document.createElement('small');count.textContent=members.filter(r=>!r.hidden).length+' 项';cell.append(count);head.append(cell);body.append(head,...members);body.hidden=members.every(r=>r.hidden);index.append(body);
 }
 viewButtons.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===view)));
 document.querySelector('#index-order-note').textContent=view==='topic'?'按主题分组，组内按发布时间从新到旧':'按发布时间从新到旧 · 日期待核的内容置于末尾';
}
viewButtons.forEach(b=>b.addEventListener('click',()=>{view=b.dataset.view;arrange()}));
function toggle(card,open){const b=card.querySelector('.toggle');card.querySelector('.body').hidden=!open;b.setAttribute('aria-expanded',String(open));b.textContent=open?'收起 ↑':'展开 ↓';}
cards.forEach((c,n)=>{toggle(c,n===0);c.querySelector('.toggle').addEventListener('click',()=>toggle(c,c.querySelector('.body').hidden));});
function filter(){const q=search.value.trim().toLocaleLowerCase(),t=topic.value;[...cards,...rows].forEach(el=>el.hidden=!(el.dataset.search.includes(q)&&(!t||el.dataset.topic===t)));const items=cards.length?cards:rows,count=items.filter(c=>!c.hidden).length;document.querySelector('#count').textContent=`显示 ${count} / ${items.length} 项`;document.querySelector('#empty').hidden=count!==0;arrange();}
search.addEventListener('input',filter);topic.addEventListener('change',filter);document.querySelector('#reset').addEventListener('click',()=>{search.value='';topic.value='';filter();});
document.querySelector('#expand')?.addEventListener('click',()=>cards.filter(c=>!c.hidden).forEach(c=>toggle(c,true)));document.querySelector('#collapse')?.addEventListener('click',()=>cards.filter(c=>!c.hidden).forEach(c=>toggle(c,false)));
function openTarget(hash,scroll=false){const m=/^#item-(\d+)(?:-s\d+|-diagram)?$/.exec(hash);if(!m)return;const c=document.getElementById('item-'+m[1]);if(!c)return;if(c.hidden){search.value='';topic.value='';filter();}toggle(c,true);if(scroll)document.getElementById(hash.slice(1))?.scrollIntoView({block:'start',behavior:'instant'});}
document.querySelectorAll('a[href^="#item-"]').forEach(a=>a.addEventListener('click',()=>openTarget(a.getAttribute('href'))));
filter();openTarget(window.location.hash,true);window.addEventListener('hashchange',()=>openTarget(window.location.hash,true));
const dialog=document.querySelector('#image-dialog');
if(dialog){let trigger=null;document.querySelectorAll('.image-zoom').forEach(button=>button.addEventListener('click',()=>{trigger=button;const source=button.querySelector('img'),target=dialog.querySelector('img');target.src=source.src;target.alt=source.alt;dialog.querySelector('p').textContent=source.alt;dialog.showModal();}));document.querySelector('#close-image').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});dialog.addEventListener('close',()=>trigger?.focus());}
})();

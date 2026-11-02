# 阅读数据 v1

UTF-8 JSON，字段以scripts/reader.py校验为准。最小形状：

item.cover含path（任务内本地原生封面）、caption、source_url（对应原视频阅读链）；duration为展示用时长。封面须列入审阅依赖，原生元数据回执留raw。item.introduction为整体讲解段落数组；diagram.after_section=0表示放在整体讲解后、首个正文小节前。正文与整体讲解同受语义审阅，不能用字段存在证明连贯性。

可选阅读字段：item.reading_title为解读标题（原作title仍保留），takeaway为短总结；section.nav_title为章节短导航名。正文段落和takeaway只识别成对的 **加粗**，其他HTML/Markdown按普通文字转义。images[].after用1起始段落序号把图插到对应段后，不填则位于节末。

可选item.diagram含kind（flow或map）、title、caption（归纳归属及边界）、after_section（0为正文前，1起为对应章节后）、nodes。每个node含label、detail、section（1起始章节定位）。节点指向该章依据，不支持没有正文依据的漂浮观点。flow仅用于真实顺序，map表达并列关系。不要为了使用字段而给材料增加不存在的结构；待核索引不能有takeaway或diagram。

多分P条目另填work_id（平台内作品稳定ID）、part和parts_total；part须在1到parts_total之间。同一作品不同分P保留不同阅读id，作品数按platform/work_id/version去重，已解读数按阅读单元计，不表示全课已读。不同剪辑用version区分。不提供分P字段的普通单项沿id作为作品标识。收藏夹原始条目数另记catalog，不用阅读单元数冒充收藏数。

```json
{"schema_version":1,"title":"本批收藏解读","scope":"本次实际范围与重要缺口","items":[{"id":"stable-id-p1","title":"原作标题","platform":"B站","kind":"video","author":"作者","url":"https://example.org/video","date":"2026-10-30","topic":"内容创作","summary":"具体内容简介","status":"deep","coverage":"完整语音与所需关键画面已核","sections":[{"heading":"具体问题","paragraphs":["连贯解释"],"evidence":[{"label":"00:00—01:00","url":"https://example.org/video?t=0"}],"images":[{"path":"evidence/frame.jpg","caption":"原作画面，说明已核对象"}]}],"practice":["整理者建议，说明依据与检验方式"],"limitations":["实际边界"]}],"connections":[]}
```

status为deep、brief、pending；pending只表示索引，不能含无证据的深读。kind为video或article。sections的evidence至少有一条可读定位；其url可省略，默认继承作品原链。图片路径相对reader.json所在目录，必须落在任务目录内，支持PNG/JPG/WebP/GIF，不载入任意HTML或SVG。paragraphs是纯文本，不执行原始HTML。practice、limitations、images、connections可省略。connections用heading/paragraphs/item_ids表达跨项解释，引用必须存在。

任务其他记录由Agent按实际需要填写：request保留原话与范围解释，catalog保留条目ID、作品ID、分P、收藏时间和排序/分页证据，checkpoint保存完成/待办/下一动作，timing逐行记录真实起止。未知字段填null或明确未知，不倒算耗时。reader只含阅读必需信息，诊断留报告。

范围显示按实际深读/简读/待核统计，不把待核算完成。审阅按quality.md单独绑定输入与输出，校验程序不做语义判定。正文来源URL允许HTTPS/HTTP，拒绝脚本等协议；本地媒体不外传。授权全文可在独立原稿保留，出版展示full/excerpt/link_only及其原因另记录，不把文件存在当全文已展示。

<p align="center">
  <img src="docs/assets/markkiller-banner.png" alt="MarkKiller 收藏夹杀手：让收藏不止于收藏" width="100%">
</p>

# MarkKiller · 收藏夹杀手

**让收藏不止于收藏。**

先从混合收藏中识别你关心的内容，例如只看 AI 应用，再将选中视频蒸馏成有背景、过程、例子与来源的深度解读。支持指定视频和图文，交付图文并茂的 **单文件 HTML**；经授权也能发布为点击即读的网页。

*Turn bookmarks into understanding.*

[直接阅读 AI 收藏解读](https://passionyoungz.github.io/MarkKiller/ai-favorites/) · [项目主页](https://passionyoungz.github.io/MarkKiller/) · [下载安装包](https://github.com/PASSIONYOUNGZ/MarkKiller/releases/latest) · [使用指南](docs/usage.md) · [更新记录](CHANGELOG.md)

## 收藏之后，怎样真正读进去？

你可能收藏过一条很有启发的视频，过几天却只记得标题。重新打开要花时间，简单摘要又经常只留下几个术语，看不出它们之间的关系。

MarkKiller 从完整材料出发，把“作者在解决什么问题、怎么做、为什么这样选、结果能说明什么”接起来。你可以先看重点和总图，再沿着感兴趣的章节深入，必要时回到原视频核对。

## 你会得到什么

| 阅读环节 | 呈现方式 |
| --- | --- |
| 先认出内容 | 真实封面、原题、作者、发布日期、时长与来源 |
| 选择从哪篇开始 | 带封面的内容汇总，按主题或发布时间浏览，搜索与主题筛选联动 |
| 快速抓住重点 | 简短而具体的结论提炼，保留影响判断的条件 |
| 理解整篇关系 | 连贯的背景讲解；适合时配流程图、关系图或结构图 |
| 读懂过程与取舍 | 结合实例、关键步骤、原作画面和必要背景展开解释 |
| 回查与迁移 | 时间定位、来源链接、适用边界及可选择的实践建议 |
| 保存和复习 | 正文、图片、样式和交互内嵌在一个 HTML 中 |

关系图服务于理解，不强制每篇都画。原作没有提供的依据会明确留下缺口，整理者的分析也会与原作陈述区分。

## 按主题筛选，再深入理解

```text
用 $markkiller 检查我的 B 站收藏夹：[链接]。
只解读 AI 相关内容，最多 20 条独立收藏作品；不足就按实际数量交付。
```

Agent 先读实际目录，用标题、简介、章节与必要正文判断主题。文件夹叫“AI”不代表其他文件夹没有AI内容，标题出现AI也不代表正文值得纳入。跨收藏夹重复作品只计一次，模糊项留待核，选中项完成正文理解后才算已解读。

筛选账本保留纳入／排除原因、来源与覆盖边界；HTML里的搜索和主题按钮则用于浏览已经交付的结果。二者不是同一个功能。课程分P不会自动变成多条独立收藏，数量不足也不会拿外部视频补数。

## 其他用法

安装后，把链接和范围一起交给 Agent：

**一条视频，深入读懂**

```text
用 $markkiller 深度解读这个视频：[视频链接]。
```

**一个收藏夹，先消化一小批**

```text
用 $markkiller 处理这个 B 站收藏夹：[收藏夹链接]。
先做 3 条视频，生成一份 HTML 阅读版。
```

**几条材料，放在一起理解**

```text
用 $markkiller 解读下面这些视频和图文：[链接列表]。
有互补或冲突的地方，请结合各自依据解释清楚。
```

也可以提供已有字幕、文章或本地材料。多分 P 课程可以明确指定分集；只做了其中几集，就按实际范围交付。

## 安装

MarkKiller 是给 Agent 使用的 Skill，包含工作指引、阅读器与审阅校验脚本。它需要一个能读取文件、浏览材料和运行 Python 的宿主；生成器要求 **Python 3.12+**，仅使用标准库。

**交给 Codex 安装：**

```text
请从 https://github.com/PASSIONYOUNGZ/MarkKiller 安装 skills/markkiller 这个 Skill。
```

**手动安装：**从 [Releases](https://github.com/PASSIONYOUNGZ/MarkKiller/releases/latest) 下载 `markkiller-v0.2.0.zip`，解压后把其中的 `markkiller` 文件夹放进宿主的技能目录。Codex 的用户安装位置可使用 `$CODEX_HOME/skills/markkiller`，未设置 `CODEX_HOME` 时通常为 `~/.codex/skills/markkiller`。新开对话后检查是否能找到 `$markkiller`。[官方目录示例](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)

安装包只包含 Skill。宣传图、公开文档、开发测试和演示文件留在仓库中。使用其他支持 `SKILL.md` 的 Agent 时，按对应宿主的安装方式操作；目前没有做各宿主的完整兼容性测试。

## 当前验证到哪里

- **真实混合收藏筛选**：本轮检查12个收藏夹的可见目录，确认10条独立AI相关作品，交付9篇深读、1篇简读、43个小节。目标上限20条；2条正文以普通技术操作为主而排除，3套长课程未完整解读，其他收藏夹与不可见条目未穷尽。没有声称20条已完成或全账户仅有10条AI视频。
- **保留开发案例**：另有10条设计、协作、创作与AI实践案例，包含收藏样本和额外选取的公开视频，不能当成本轮AI收藏的数量。两组页面分开展示。
- **多平台按实际能力执行**：流程支持指定视频、图文与导入材料，其他平台尚未完成同规模验证。登录、字幕和媒体能否取得，取决于用户自己的环境与权限。
- **阅读体验已做浏览器检查**：桌面、笔记本与手机布局，以及主题／时间切换、搜索和解读跳转。HTML 资源自包含已检查；实际断网与 `file://` 打开尚未完成本轮自动验收。
- **研究与学习分开**：完整字幕不等于已理解所有画面，生成阅读版也不等于读者已经掌握。

“杀手”指消化收藏积压。Skill 不会自动取消收藏、移动收藏或公开你的收藏记录。材料获取需要联网，生成后的阅读文件内嵌阅读资源；主动访问原作链接仍需联网。

## 点击就能阅读

- [10篇 AI 收藏解读：封面与主题／时间索引](https://passionyoungz.github.io/MarkKiller/ai-favorites/)
- [整份 AI 收藏阅读版](https://passionyoungz.github.io/MarkKiller/ai-favorites/collection-v02.html)
- [此前10条开发案例](https://passionyoungz.github.io/MarkKiller/examples/)
- [阅读器功能演示](https://passionyoungz.github.io/MarkKiller/demo.html)

以上是 GitHub Pages 阅读地址，无需下载或打开 GitHub 源码视图。真实案例仅发布已授权的解读、原作公开信息和必要配图；研究原稿、私密目录、完整字幕、模型与认证信息留在本地。功能演示使用项目原创文章，不冒充平台采集。

若要发布自己的阅读版，可明确说明目标仓库和公开范围：

```text
将这批已完成的解读发布到我的 GitHub Pages：[仓库链接]。
只公开选中内容的阅读页，不上传收藏目录、原始字幕或登录材料。
给我可以直接打开的索引和单篇地址，并验证部署结果。
```

## 给开发者

```bash
python -X utf8 skills/markkiller/scripts/reader.py validate --input docs/demo/reader.json
python -X utf8 skills/markkiller/scripts/reader.py build --input docs/demo/reader.json --output demo-local.html
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tools/package.py --version 0.2.0
```

生成器只渲染已准备好的阅读数据；识别筛选、材料获取、理解、写作和语义审阅由宿主 Agent 按 Skill 执行。`check_selection.py` 校验收藏来源、正文依据、去重与阅读对应，不是关键词分类器。已有 HTML 默认另存 `.proposed.html`，避免覆盖手改内容。[筛选合同](skills/markkiller/references/selection.md) · [在线发布](skills/markkiller/references/publishing.md) · [数据结构](skills/markkiller/references/data.md) · [质量标准](skills/markkiller/references/quality.md)

项目开发者：[PassionYoungz](https://github.com/PASSIONYOUNGZ)。保留独立于使用者身份的项目署名。欢迎带上具体问题、相关公开链接和预期效果反馈；提交前请移除凭据及私密材料。

<p align="center">
  <img src="docs/assets/markkiller-banner.png" alt="MarkKiller 收藏夹杀手：让收藏不止于收藏" width="100%">
</p>

# MarkKiller · 收藏夹杀手

**让收藏不止于收藏。**

把收藏夹里的视频，或你指定的视频和图文，蒸馏成一份真正能读懂的深度解读：有背景、有过程、有例子、有来源，最终交付图文并茂的 **单文件 HTML**。

*Turn bookmarks into understanding.*

[下载安装包](https://github.com/PASSIONYOUNGZ/MarkKiller/releases/latest) · [使用指南](docs/usage.md) · [阅读版演示](docs/demo.html) · [更新记录](CHANGELOG.md) · [反馈问题](https://github.com/PASSIONYOUNGZ/MarkKiller/issues)

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

## 三种用法

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

**手动安装：**从 [Releases](https://github.com/PASSIONYOUNGZ/MarkKiller/releases/latest) 下载 `markkiller-v0.1.0.zip`，解压后把其中的 `markkiller` 文件夹放进宿主的技能目录。Codex 的用户安装位置可使用 `$CODEX_HOME/skills/markkiller`，未设置 `CODEX_HOME` 时通常为 `~/.codex/skills/markkiller`。新开对话后检查是否能找到 `$markkiller`。[官方目录示例](https://developers.openai.com/cookbook/examples/codex/iterating-development-workflows-with-codex)

安装包只包含 Skill。宣传图、公开文档、开发测试和演示文件留在仓库中。使用其他支持 `SKILL.md` 的 Agent 时，按对应宿主的安装方式操作；目前没有做各宿主的完整兼容性测试。

## 当前验证到哪里

- **B 站优先**：开发阶段完成了 10 条独立视频的解读与迭代，包含 10 张原生封面、33 张随文画面、50 个解读小节。样本偏向 AI、设计与产品实践，不代表所有题材或所有收藏夹都已验证。
- **多平台按实际能力执行**：流程支持指定视频、图文与导入材料，其他平台尚未完成同规模验证。登录、字幕和媒体能否取得，取决于用户自己的环境与权限。
- **阅读体验已做浏览器检查**：桌面、笔记本与手机布局，以及主题／时间切换、搜索和解读跳转。HTML 资源自包含已检查；实际断网与 `file://` 打开尚未完成本轮自动验收。
- **研究与学习分开**：完整字幕不等于已理解所有画面，生成阅读版也不等于读者已经掌握。

“杀手”指消化收藏积压。Skill 不会自动取消收藏、移动收藏或公开你的收藏记录。材料获取需要联网，生成后的阅读文件内嵌阅读资源；主动访问原作链接仍需联网。

## 看一份演示

[下载演示 HTML](https://github.com/PASSIONYOUNGZ/MarkKiller/releases/download/v0.1.0/markkiller-demo.html) 后用浏览器打开，也可以查看[演示原文](docs/reading-guide.md)和[演示说明](docs/demo/README.md)。

演示使用项目原创文章，展示封面、重点、整体讲解、关系图和来源结构，不冒充真实平台采集案例。真实研究原稿、私密收藏目录、字幕、模型和认证信息不随仓库发布。

## 给开发者

```bash
python -X utf8 skills/markkiller/scripts/reader.py validate --input docs/demo/reader.json
python -X utf8 skills/markkiller/scripts/reader.py build --input docs/demo/reader.json --output demo-local.html
python -X utf8 -m unittest discover -s tests -v
python -X utf8 tools/package.py --version 0.1.0
```

生成器只渲染已准备好的阅读数据；材料获取、理解、写作和语义审阅由宿主 Agent 按 Skill 执行。已有 HTML 默认另存 `.proposed.html`，避免覆盖手改内容。[数据结构](skills/markkiller/references/data.md) · [质量标准](skills/markkiller/references/quality.md)

项目开发者：[PassionYoungz](https://github.com/PASSIONYOUNGZ)。保留独立于使用者身份的项目署名。欢迎带上具体问题、相关公开链接和预期效果反馈；提交前请移除凭据及私密材料。

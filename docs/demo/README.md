# 公开演示

此处输入来自本项目原创的[阅读指南](../reading-guide.md)。封面为项目宣传图，明确作为这篇指南的配图使用。它是阅读器的可重建演示，不是外部平台采集回执，也不证明视频解析质量。

在仓库根目录运行：

```bash
python -X utf8 skills/markkiller/scripts/reader.py build --input docs/demo/reader.json --output demo-local.html
```

生成器只处理已准备好的阅读数据，不会自行联网抓取正文。已有输出不覆盖，另存 `.proposed.html`。演示仅一篇，时间／主题视图各一组；真实多条材料会按同一逻辑展开更多分组。

包内 `cover.png` 是项目宣传图的原样副本，保证输入图片位于该任务目录内。实际研究时应使用对应原作的已核封面。

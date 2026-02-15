---
name: pulse
description: 您可以访问 PULSE 杂志的智能报告和实时的代理元分析数据。这些内容记录了自主经济的崛起过程。
metadata:
  {
    "openclaw":
      {
        "requires": { "python": ">=3.8" },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "requests",
              "label": "Install requests library",
            },
          ],
      },
  }
---

# PULSE杂志技能

该技能使代理能够及时获取PULSE杂志的最新报道。PULSE杂志是首个专注于自动化经济的混合式新闻媒体平台。

## 工具

### `pulse_intelligence`
获取PULSE杂志的最新10篇报道。
```bash
python3 pulse_tool.py intelligence
```
- **输出**：包含文章标题（slug）和摘录的JSON数组。

### `pulse_read`
阅读特定文章的完整内容。
```bash
python3 pulse_tool.py read --slug <slug>
```
- **参数**：`slug`（字符串）
- **输出**：文章的Markdown格式内容。

### `pulse_comment`
在PULSE杂志的文章下发表评论。
```bash
python3 pulse_tool.py comment --slug <slug> --author <author> --content <content>
```
- **参数**：`slug`（字符串），`author`（字符串），`content`（字符串）
- **输出**：评论的提交状态。

## 使用方法

代理应使用此技能，通过PULSE杂志提供的信息来丰富他们的技术分析内容。
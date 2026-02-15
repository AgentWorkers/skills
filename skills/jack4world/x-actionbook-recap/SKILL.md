---
name: x-actionbook-recap
description: 使用 Actionbook Rust CLI（actionbook-rs）工作流程来收集、滚动浏览、提取并总结某个 Twitter 账号的最新帖子（可选通过关键词搜索进行过滤）：具体步骤包括：打开工具、创建快照、获取帖子的内容（`article` 部分）。该工具适用于需要分析某个账号在特定时间范围内的动态（例如过去 7 天内的帖子），生成中文的工作记录，并从指定账号发布中立的英文总结（可以是单条帖子或整个帖子串）。
---

# 通过 actionbook-rs 进行 X 内容回顾

## 该技能的用途

使用 **actionbook-rs** 方法，为 **任何 X 账号**（可选添加关键词）生成一个可重复的 “收集 → 提取 → 摘要 → 发布” 工作流程：

1) 使用 **actionbook browser** 打开个人资料/搜索页面。
2) 使用 **actionbook browser snapshot** 获取页面的访问结构（包括 `article` 节点）。
3) （可选）使用 **actionbook browser eval** 功能进行滚动浏览。
4) 从 `article` 节点中提取帖子内容。
5) 分析提取的内容并起草中文摘要；将英文摘要发布到 X 平台上。
6) （可选）添加图片。

## 注意事项

- 无限滚动可能无法覆盖所有内容，请明确说明覆盖范围的限制。
- 除非用户提供具体的链接或时间戳，否则不要引用 “最近的采访”。
- 发布内容属于外部操作：在发布前请确认目标账号和最终内容。

## 工作流程

### 1) 收集帖子（使用 Actionbook）

选择一个入口点：
- 个人资料：`https://x.com/<handle>`
- 搜索（包含关键词，可选设置时间范围）：`https://x.com/search?q=from%3A<handle>%20<keyword>&src=typed_query&f=live`

示例命令：

```bash
# open (profile)
actionbook browser open "https://x.com/<handle>"

# snapshot (repeat after each scroll)
actionbook browser snapshot --refs aria --depth 18 --max-chars 12000

# scroll a bit
actionbook browser eval "window.scrollBy(0, 2200)"
```

提取规则：
- 在页面快照中找到包含帖子内容的 `article` 节点。
- 记录每篇帖子的以下信息：
  - 原文内容
  - 显示的时间戳（相对或绝对时间）
  - 如果有的话，记录帖子的 URL
  - 是否为转载或引用（请注明）

停止条件：
- 收集到的帖子数量达到用户设定的时间范围（例如 7 天）；或者提取效率开始下降。

### 2) 撰写中文摘要

撰写简洁的中文工作摘要：
- 主要主题（3–6 个要点）
- 代表性帖子（附链接）
- 缺失的内容或存在的不确定性

### 3) 起草英文发布内容

选择发布形式：
- 单篇帖子（不超过 280 个字符）
- 如果需要，可以分成多部分发布（6–10 个部分）

使用中立的表达方式：
- “根据公开帖子观察到的内容……”
- 避免主观解读；区分 “原文内容” 和个人解读

使用 `references/templates.md` 中的模板。

### 4) 添加图片（可选，但推荐）

推荐的图片格式（无需使用 Python）：
- 相关帖子的清晰截图（分辨率 1280×720，可放大）
- 在浏览器中渲染的简单 HTML/SVG 卡片（参见 `references/image-card.md`）

### 5) 在 X 平台上发布内容

如果使用 OpenClaw 浏览器自动化工具：
- 打开发布界面
- 粘贴英文摘要
- 上传图片（如有）
- 发布内容

发布前请确认：
- 目标账号（例如 @gblwll）
- 最终发布的文本内容
- 选择的图片

## 配套参考资料

- `references/templates.md` — 摘要和多部分发布的模板（英文）
- `references/checklist.md` — 提取内容的检查清单及注意事项
- `references/image-card.md` — 使用 HTML/SVG 卡片的制作方法（无需安装 Pillow 库）
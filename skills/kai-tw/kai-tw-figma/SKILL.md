---
name: figma
description: 与 Figma 的 REST API 进行交互，以读取文件、将图层/组件导出为图像以及检索评论。当用户需要从 Figma 设计中获取信息或希望导出用于开发的资产时，可以使用此功能。触发事件包括 “read figma file”（读取 Figma 文件）、”export figma layer”（导出 Figma 图层）或 “check figma comments”（检查 Figma 评论）。
metadata:
  openclaw:
    emoji: 📐
    requires:
      env:
        - FIGMA_TOKEN
---

# Figma 技能

此技能允许代理通过 REST API 与 Figma 文件进行交互。

## 设置

需要一个 Figma 个人访问令牌（Personal Access Token，简称 PAT）。
环境变量：`FIGMA_TOKEN`

## 流程

### 1. 读取文件结构
要了解 Figma 文件的内容（页面、帧、图层）：
`python scripts/figma_tool.py get-file <file_key>`

### 2. 导出图片
要将特定的图层/组件导出为图片：
`python scripts/figma_tool.py export <file_key> --ids <id1>,<id2> --format <png|jpg|svg|pdf> --scale <1|2|3|4>`

### 3. 查看评论
要列出文件上的最新评论：
`python scripts/figma_tool.py get-comments <file_key>`

## 参考资料
- [Figma API 文档](https://www.figma.com/developers/api)
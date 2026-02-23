---
name: feed-to-md
title: Feed to Markdown
description: 使用 `feed2md` 将 RSS 或 Atom 源链接转换为 Markdown 格式。当用户请求将源链接转换为可读的 Markdown 格式时，可以使用此工具；同时还可以选择性地限制显示的条目数量或将转换结果保存到文件中。
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["feed2md","npm"]},"install":[{"id":"node","kind":"node","package":"feed2md-cli@0.1.0","bins":["feed2md"],"label":"Install feed2md-cli (npm)"}]}}
---
# 将 RSS/Atom 格式转换为 Markdown 格式

当需要将 RSS/Atom 源链接转换为 Markdown 格式时，可以使用此技能。

## 该技能的功能

- 通过 `feed2md` 工具将 RSS/Atom 源链接转换为 Markdown 格式
- 支持将转换结果输出到标准输出（stdout）或写入文件中
- 支持限制显示的文章数量和设置摘要内容

## 输入参数

- 必需参数：RSS/Atom 源链接
- 可选参数：
  - 输出路径（output path）
  - 最大显示文章数量（max item count）
  - 模板类型（template preset）：`short` 或 `full`

## 使用方法

建议先安装该工具：

```bash
npm install -g feed2md-cli@0.1.0
```

安装完成后，使用命令行工具进行转换：

```bash
feed2md "<feed_url>"
```

## 常见使用示例

- 基本转换：
  ```bash
feed2md "https://example.com/feed.xml"
```

- 将转换结果写入文件：
  ```bash
feed2md "https://example.com/feed.xml" --output feed.md
```

- 限制显示 10 条文章：
  ```bash
feed2md "https://example.com/feed.xml" --limit 10
```

## 命令行参数说明

- `-o, --output <file>`：将转换结果写入指定文件
- `--limit <number>`：限制显示的文章数量
- `--no-summary`：不显示文章摘要
- `--summary-max-length <number>`：限制摘要的最大长度
- `--template <preset>`：选择模板类型（`short` 或 `full`，默认为 `short`）

## 安装方法（可选）

```bash
npm install -g feed2md-cli@0.1.0
```

安装完成后，可以直接使用以下命令进行转换：

```bash
feed2md "https://example.com/feed.xml"
```
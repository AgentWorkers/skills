---
name: feed-to-md
title: feed-to-md
description: 使用 `feed2md` 将 RSS 或 Atom 源链接转换为 Markdown 格式。当用户请求将源链接转换为可读的 Markdown 格式时，可以使用此工具；同时，还可以选择性地限制显示的条目数量或将转换结果保存到文件中。
---
# 将 RSS/Atom 格式转换为 Markdown 格式

当需要将 RSS/Atom 源链接转换为 Markdown 格式时，可以使用此技能。

## 该技能的功能

- 通过 `feed2md` 工具将 RSS/Atom 源链接转换为 Markdown 格式
- 支持将转换结果输出到标准输出（stdout）或写入文件中
- 支持限制显示的文章数量以及自定义摘要内容

## 输入参数

- 必需参数：RSS/Atom 源链接
- 可选参数：
  - 输出路径（output path）
  - 最大显示文章数量（max item count）
  - 模板类型（template preset）：`short` 或 `full`
  - 自定义模板文件（custom template file）
  - 摘要显示选项（summary options）

## 命令使用方式

1. 如果已安装 `feed2md`，建议直接使用命令行工具：

```bash
feed2md "<feed_url>"
```

2. 如果 `feed2md` 未全局安装，可以使用 `npx` 命令来执行：

```bash
npx -y feed2md-cli "<feed_url>"
```

3. 为了实现重复执行，可以使用该技能的封装脚本：

```bash
./scripts/feed-to-markdown.sh "<feed_url>" [output_file]
```

## 常见使用示例

- 基本转换示例：

```bash
feed2md "https://example.com/feed.xml"
```

- 将转换结果写入文件示例：

```bash
feed2md "https://example.com/feed.xml" --output feed.md
```

- 仅显示前 10 条文章并使用完整模板示例：

```bash
feed2md "https://example.com/feed.xml" --limit 10 --template full
```

- 禁用摘要显示示例：

```bash
feed2md "https://example.com/feed.xml" --no-summary
```

- 使用自定义模板示例：

```bash
feed2md "https://example.com/feed.xml" --template-file ./template.eta
```

## 命令行参数说明

- `-o, --output <file>`：将转换结果写入指定文件
- `--limit <number>`：限制显示的文章数量
- `--no-summary`：不显示摘要
- `--summary-max-length <number>`：限制摘要的最大长度
- `--template <preset>`：模板类型（`short` 或 `full`）
- `--template-file <path>`：指定自定义模板文件的路径

## 错误处理

- 如果 `feed2md` 未安装，请通过以下命令进行安装或使用：

```bash
npm install -g feed2md-cli
# or
npx -y feed2md-cli "<feed_url>"
```

- 如果无法获取 RSS/Atom 数据，请确认链接是否可访问，并确保其指向有效的 RSS/Atom XML 文件。
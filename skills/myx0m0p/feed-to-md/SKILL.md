---
name: feed-to-md
title: Feed to Markdown
description: 使用内置的本地转换脚本将 RSS 或 Atom 源链接转换为 Markdown 格式。当用户请求将源链接转换为可读的 Markdown 格式时，可以使用此脚本；您还可以选择限制显示的条目数量或将转换结果保存到文件中。
metadata: {"clawdbot":{"emoji":"📰","requires":{"bins":["python3"]}}}
---
# 将 RSS/Atom 内容转换为 Markdown

当需要将 RSS/Atom 源链接转换为 Markdown 格式时，可以使用此技能。

## 该技能的功能

- 通过内置的本地脚本将 RSS/Atom 源链接转换为 Markdown 格式
- 支持将转换结果输出到标准输出（stdout）或写入 Markdown 文件
- 支持设置显示的文章数量和摘要长度

## 输入参数

- 必需参数：RSS/Atom 源链接
- 可选参数：
  - 输出路径
  - 最大显示文章数量
  - 模板类型（`short` 或 `full`）

## 使用方法

**运行本地脚本：**

```bash
python3 scripts/feed_to_md.py "<feed_url>"
```

**将转换结果写入文件：**

```bash
python3 scripts/feed_to_md.py "https://example.com/feed.xml" --output feed.md
```

**限制显示 10 篇文章：**

```bash
python3 scripts/feed_to_md.py "https://example.com/feed.xml" --limit 10
```

**使用包含摘要的完整模板：**

```bash
python3 scripts/feed_to_md.py "https://example.com/feed.xml" --template full
```

## 安全规则（必须遵守）

- 绝不要将用户的原始输入直接插入到 shell 字符串中。
- 必须将所有参数作为独立的 argv 参数传递给脚本。
- 源链接必须是 `http` 或 `https` 协议，且不能指向本地主机或私有地址。
- 输出路径必须是工作区相对路径，并以 `.md` 为扩展名。
- 不要使用 shell 重定向来输出结果；请使用 `--output` 选项。

**安全的命令格式：**

```bash
cmd=(python3 scripts/feed_to_md.py "$feed_url")
[[ -n "${output_path:-}" ]] && cmd+=(--output "$output_path")
[[ -n "${limit:-}" ]] && cmd+=(--limit "$limit")
[[ "${template:-short}" = "full" ]] && cmd+=(--template full)
"${cmd[@]}"
```

## 脚本选项**

- `-o, --output <文件路径>`：将转换结果写入指定文件
- `--limit <数量>`：限制显示的文章数量
- `--no-summary`：不显示文章摘要
- `--summary-max-length <长度>`：限制摘要的显示长度
- `--template <模板类型>`：选择 `short`（默认）或 `full` 模板
---
name: md-to-gdoc
version: 1.0.1
description: 将 Markdown 文件转换为格式正确的 Google 文档。适用于需要从 Markdown 创建 Google 文档、将 Markdown 文件上传到 Google 文档、将 `.md` 文件放入 Google 文档中，或把研究资料/笔记/文档转换为 Google 文档格式的场景。
---
# 将 Markdown 文件转换为 Google 文档

本工具可将 `.md` 文件转换为格式正确的 Google 文档，支持标题样式、粗体文本、代码块、列表、链接和块引用等功能。

## 所需工具

- **[gog](https://github.com/tychohq/gog)** — Google Workspace 命令行工具（需要先进行身份验证：`gog auth add <email>`）
- **python3** — 用于脚本中的 JSON 解析

## 快速入门

```bash
scripts/md-to-gdoc.sh <file.md> [--title "Title"] [--parent <folder-id>] [--account <email>]
```

请确保脚本位于当前技能目录的 `scripts/` 子目录中。

## 重要规则

1. **使用 `gog docs update --format=markdown`** 命令进行转换。切勿使用 `write --markdown` 或 `create --file` 命令。只有 `update` 命令才能通过 API 正确应用 Google 文档的标题样式。
2. Markdown 文件中的标题必须以 `#` 开头。如果源文件中存在没有 `#` 标记的标题文本，请在转换前手动添加它们。脚本会发出警告，但仍会继续执行转换。
3. 转换过程分为两步：首先创建一个空文档，然后使用 `update` 命令填充内容。此方法具有确定性和可靠性。
4. 在运行脚本之前，请务必检查 Markdown 文件中的标题语法。如果没有 `#` 标记，转换后的文档将不会显示标题格式。

## 支持的功能

- `#`–`######` 标题 → Google 文档中的一级至六级标题
- **粗体** → 粗体文本
- `` `inline code` `` → 行内代码（显示为 Courier New 字体）
- 带引号的代码块 → 以 Courier New 字体显示，并带有灰色背景
- `> blockquotes` → 嵌入式引用（显示为缩进段落）
- `- bullets` → 项目符号列表
- `1. numbered` → 编号列表
- `[text](url)` → 超链接
- Markdown 表格 → 可以直接转换为 Google 文档中的表格

## 已知的限制

- **斜体文字** 可能无法正确显示（这是 gog CLI 的一个已知问题，特别是在处理行内格式时）
- 项目符号/编号列表使用文本前缀（如 `•`、`1.`），而非 Google 文档中的原生列表格式
- 水平分隔线会显示为 40 个短横线

## 配置选项

- `--title` — 文档标题。默认值为文件名（使用连字符和空格分隔）。
- `--parent` — 文档要保存到的 Google Drive 文件夹 ID。
- `--account` — 使用的 Google 账户邮箱。默认值为首次登录时使用的账户。

## 常见问题解决方法

- **文档内容为空（无标题）**：可能是 Markdown 文件中缺少 `#` 标题标记。请添加相应的标题。
- **身份验证错误**：运行 `gog auth list` 命令检查身份验证状态。如有需要，可使用 `gog auth add <email>` 进行重新授权。
- **转换后文档为空**：可能是 `update` 命令执行失败。请查看 gog 的输出日志以获取 API 错误信息。
---
name: confcli
description:
  Interact with Confluence Cloud from the command line. Use when reading,
  creating, updating, or searching Confluence pages, managing attachments,
  labels, comments, or exporting content.
---

# confcli

Confluence Cloud 的命令行工具（CLI）。

## 安装

检查 confcli 是否已安装：

```bash
command -v confcli
```

如果未安装，请通过以下命令进行安装：

```bash
curl -fsSL https://raw.githubusercontent.com/hochej/confcli/main/install.sh | sh
```

若需要安装特定版本或将其安装到自定义目录，请使用以下命令：

```bash
curl -fsSL https://raw.githubusercontent.com/hochej/confcli/main/install.sh | VERSION=0.2.3 sh
curl -fsSL https://raw.githubusercontent.com/hochej/confcli/main/install.sh | INSTALL_DIR=~/.bin sh
```

## 认证

首先检查认证状态：

```bash
confcli auth status
```

如果未完成认证，请让用户配置认证信息。用户可以选择以下两种方式之一：
1. 在自己的终端中交互式地运行 `confcli auth login`；
2. 在开始会话之前设置环境变量：
   - `CONFLUENCE_DOMAIN` — 例如：`yourcompany.atlassian.net`
   - `CONFLUENCE_EMAIL`
   - `CONFLUENCE_TOKEN`（或 `CONFLUENCE_API_TOKEN`）

API 令牌可以在以下地址生成：
https://id.atlassian.com/manage-profile/security/api-tokens

> **切勿要求用户将令牌粘贴到对话中。** 令牌必须通过环境变量或 `confcli auth login` 来设置。

## 页面引用

页面可以通过以下方式引用：
- ID：`12345`
- URL：`https://company.atlassian.net/wiki/spaces/MFS/pages/12345/Title`
- Space:Title：`MFS:Overview`

## 重要提示

执行创建、更新、删除、清除、编辑、添加/删除标签、上传/删除附件、添加/删除评论、复制目录等操作时，必须明确用户的操作意图。切勿基于猜测来执行这些操作。

使用 `--dry-run` 选项可以预览这些操作，而不会实际执行它们。

## 常用命令

```bash
# Spaces
confcli space list
confcli space get MFS
confcli space pages MFS --tree
confcli space create --key PROJ --name "Project" -o json --compact-json
confcli space delete MFS --yes

# Pages
confcli page list --space MFS --title "Overview"
confcli page get MFS:Overview                  # metadata (table)
confcli page get MFS:Overview --show-body      # include body in table output
confcli page get MFS:Overview -o json          # full JSON
confcli page body MFS:Overview                 # markdown content
confcli page body MFS:Overview --format storage
confcli page children MFS:Overview
confcli page children MFS:Overview --recursive
confcli page history MFS:Overview
confcli page open MFS:Overview                 # open in browser
confcli page edit MFS:Overview                 # edit in $EDITOR

# Search
confcli search "query"
confcli search "type=page AND title ~ Template"
confcli search "confluence" --space MFS

# Write
confcli page create --space MFS --title "Title" --body "<p>content</p>"
confcli page update MFS:Overview --body-file content.html
confcli page delete 12345

# Attachments
confcli attachment list MFS:Overview
confcli attachment upload MFS:Overview ./file.png ./other.pdf
confcli attachment download att12345 --dest file.png

# Labels
confcli label add MFS:Overview tag1 tag2 tag3
confcli label remove MFS:Overview tag1 tag2
confcli label pages "tag"

# Comments
confcli comment list MFS:Overview
confcli comment add MFS:Overview --body "LGTM"
confcli comment delete 123456

# Export
confcli export MFS:Overview --dest ./exports --format md

# Copy Tree
confcli copy-tree MFS:Overview MFS:TargetParent
```

## 输出格式

使用 `-o` 标志指定输出格式：`json`、`table` 或 `md`：

```bash
confcli space list -o json
confcli page get MFS:Overview -o json
```

## 分页

使用 `--all` 选项获取所有结果，使用 `-n` 选项设置结果数量限制：

```bash
confcli space list --all
confcli search "query" --all -n 100
```
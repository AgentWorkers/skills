---
name: linearis
version: 1.0.0
description: **Linear.app CLI：用于问题跟踪的工具**  
该CLI可用于列出、创建、更新和搜索Linear平台上的问题、评论、文档、项目以及相关周期。专为基于大语言模型（LLM）的自动化系统优化设计，支持JSON格式的输出。
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["linearis"]},"install":[{"id":"npm","kind":"node","package":"linearis","bins":["linearis"],"label":"Install linearis (npm)"}]}}
---

# linearis

这是一个为 [Linear.app](https://linear.app) 设计的命令行工具（CLI），支持 JSON 格式的输出，专为大型语言模型（LLM）代理使用。

## 设置

```bash
npm install -g linearis
```

**身份验证：**
- 可以选择以下方式之一进行身份验证：
  - `echo "lin_api_..." > ~/.linear_api_token` （推荐）
  - `export LINEAR_API_TOKEN="lin_api_..."`
  - 或者使用 `--api-token <token>` 参数进行身份验证。

**获取 API 密钥：**
  - 登录 Linear 应用，进入 **设置** → **安全与访问** → **个人 API 密钥**。

## 命令

### 报告问题（Report Issues）

```bash
linearis issues list -l 20              # List recent issues
linearis issues list -l 10 --team WHO   # Filter by team
linearis issues search "bug"            # Full-text search
linearis issues read ABC-123            # Get issue details
linearis issues create --title "Fix bug" --team WHO --priority 2
linearis issues update ABC-123 --status "Done"
linearis issues update ABC-123 --title "New title" --assignee user123
linearis issues update ABC-123 --labels "Bug,Critical" --label-by adding
linearis issues update ABC-123 --parent-ticket EPIC-100  # Set parent
```

### 评论（Comments）

```bash
linearis comments create ABC-123 --body "Fixed in PR #456"
```

### 文档（Documents）

```bash
linearis documents list
linearis documents list --project "Backend"
linearis documents create --title "Spec" --content "# Overview..."
linearis documents read <doc-id>
linearis documents update <doc-id> --content "Updated"
linearis documents delete <doc-id>
```

### 文件上传/下载（File Uploads/Downloads）

```bash
linearis embeds upload ./screenshot.png
linearis embeds download "<url>" --output ./file.png
```

### 团队、用户、项目（Teams, Users, Projects）

```bash
linearis teams list
linearis users list --active
linearis projects list
linearis cycles list --team WHO --active
```

### 完整使用说明（Full Usage）

```bash
linearis usage  # Complete command reference (~1k tokens)
```

## 输出结果

所有命令默认返回 JSON 格式的数据。您可以将输出结果通过 `jq` 工具进行进一步处理：

```bash
linearis issues list -l 5 | jq '.[].identifier'
```

## 优先级（Priority Values）

- 0：无优先级
- 1：紧急
- 2：高
- 3：中等
- 4：低

## 链接（Links）

- 文档：https://github.com/czottmann/linearis
- 博文：https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html
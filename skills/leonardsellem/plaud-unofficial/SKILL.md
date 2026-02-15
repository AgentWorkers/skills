---
name: plaud-api
description: **使用说明：**  
本文档用于指导用户如何访问 Plaud 语音记录器的数据（包括录音文件、文字记录以及 AI 生成的摘要）。它详细介绍了凭证（credentials）的设置方法，并提供了 `plaud_client.py` 脚本的编写示例。
aliases:
  - plaud
  - plaud-recordings
---

# Plaud API 技能

该技能允许您访问 Plaud 语音记录器的数据，包括录音文件、文字记录以及人工智能生成的摘要。

## 概述

Plaud API 提供以下功能：
- **音频文件**：来自您的 Plaud 设备的 MP3 录音文件
- **文字记录**：包含说话人信息的完整文本转录
- **人工智能摘要**：自动生成的笔记和总结

**核心原则**：请使用 `plaud_client.py`（包含在该技能中）来调用 API，而非直接进行原始 API 调用。该客户端负责处理身份验证、错误处理和响应解析。

## 何时使用此技能

在以下情况下使用此技能：
- 用户提到 “Plaud”、“Plaud 录音” 或 “Plaud 的文字记录”
- 需要访问语音记录器的数据
- 需要处理来自 Plaud 设备的录音文件、文字记录或人工智能生成的摘要

## 交互式凭证教程

在使用 Plaud API 之前，您需要从 Web 应用程序中提取凭证。

### 第 1 步：访问 Plaud Web 应用程序

打开 Chrome 浏览器，并访问：https://web.plaud.ai
如果尚未登录，请使用您的 Plaud 账户登录。

### 第 2 步：打开 Chrome 开发工具

按 `F12`（或在 Mac 上按 `Cmd+Option+I`）打开开发工具。

### 第 3 步：查找 localStorage 的值

1. 在开发工具中点击 **应用程序** 标签
2. 在左侧边栏中展开 **本地存储**
3. 点击 `https://web.plaud.ai`

### 第 4 步：复制所需的值

找到并复制以下两个值：
- `tokenstr`：您的承载令牌（以 “bearer eyJ...” 开头）
- `plaud_user_api_domain`：API 端点（例如：“https://api-euc1.plaud.ai”）

### 第 5 步：创建 `.env` 文件

在技能目录（`~/.claude/skills/plaud-api/`）中创建或更新 `.env` 文件：

```bash
# In the skill directory
cd ~/.claude/skills/plaud-api
cp .env.example .env
# Edit .env with your actual credentials
```

或者直接创建文件：

```bash
cat > ~/.claude/skills/plaud-api/.env << 'EOF'
PLAUD_TOKEN=bearer eyJ...your_full_token_here...
PLAUD_API_DOMAIN=https://api-euc1.plaud.ai
EOF
```

**注意**：请确保令牌中包含 “bearer ” 前缀。

### 第 6 步：验证设置

测试凭证是否有效：

```bash
cd ~/.claude/skills/plaud-api
python3 plaud_client.py list
```

如果成功，您将看到包含文件 ID、时长和名称的录音列表。

**首次设置**：如有需要，请安装依赖项：
```bash
pip install -r ~/.claude/skills/plaud-api/requirements.txt
```

## `.env` 文件格式

```
PLAUD_TOKEN=bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
PLAUD_API_DOMAIN=https://api-euc1.plaud.ai
```

**注意事项**：
- 令牌中包含 “bearer ” 前缀
- API 域名因地区而异（欧盟用户：`api-euc1`，美国用户可能有所不同）

## 快速参考

所有命令都应在技能目录（`~/.claude/skills/plaud-api`）中执行：

| 任务 | 命令 |
|------|---------|
| 列出所有录音 | `python3 plaud_client.py list` |
| 以 JSON 格式列出 | `python3 plaud_client.py list --json` |
| 获取文件详细信息 | `python3 plaud_client.py details <file_id>` |
| 以 JSON 格式获取详细信息 | `python3 plaud_client.py details <file_id> --json` |
| 下载音频文件 | `python3 plaud_client.py download <file_id>` |
| 下载到指定路径 | `python3 plaud_client.py download <file_id> -o output.mp3` |
| 下载所有文件 | `python3 plaud_client.py download-all -o ./recordings` |
| 获取文件标签/文件夹信息 | `python3 plaud_client.py tags` |

## 常用操作模式

### 获取最近的文字记录

```bash
cd ~/.claude/skills/plaud-api

# List files to find IDs
python3 plaud_client.py list

# Get transcript for a specific file
python3 plaud_client.py details <file_id> --json | jq '.data.trans_result'
```

### 查找文件 ID

文件 ID 是 32 个字符的十六进制字符串。您可以通过以下方式获取它们：
- **URL**：`https://web.plaud.ai/file/{file_id}`
- **列表输出**：`python3 plaud_client.py list` 的第一列
- **JSON 输出**：`python3 plaud_client.py list --json | jq '.[].id'`

### 获取人工智能摘要

```bash
python3 plaud_client.py details <file_id> --json | jq '.data.ai_content'
```

### 批量操作

```bash
# Download all recordings to a folder
python3 plaud_client.py download-all -o ./all_recordings

# Get all file IDs
python3 plaud_client.py list --json | jq -r '.[].id'
```

### 仅提取文字记录

```bash
# Get plain transcript text (all segments concatenated)
python3 plaud_client.py details <file_id> --json | jq -r '.data.trans_result.segments[].text' | tr '\n' ' '
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|-----|
| `401 Unauthorized` | 令牌过期或无效 | 从 localStorage 中重新获取令牌 |
| 空响应 | 文件 ID 格式无效 | 确保文件 ID 是 32 个十六进制字符 |
| 连接错误 | API 域名错误 | 检查 `.env` 文件中的 `PLAUD_API_DOMAIN` |
| 需要令牌 | 缺少 `.env` 文件或 `PLAUD_TOKEN` | 按照上述凭证教程操作 |

## 令牌刷新

Plaud 令牌的有效期较长（约 10 个月），但当令牌过期时，请执行以下操作：
1. 登录 https://web.plaud.ai
2. 打开开发工具 > 应用程序 > 本地存储
3. 复制新的 `tokenstr` 值
4. 更新您的 `.env` 文件

## API 参考

有关详细的 API 文档，请参阅包含在该技能目录中的 `PLAUD_API.md` 文件。

`plaud_client.py` 使用的主要 API 端点：
- `GET /file/simple/web` - 列出所有文件
- `GET /file/detail/{file_id}` - 获取包含文字记录的文件详细信息
- `GET /file/download/{file_id}` - 下载 MP3 音频文件
- `GET /filetag/` - 获取文件标签/文件夹信息

## 包含的文件

| 文件 | 用途 |
|------|---------|
| `plaud_client.py` | 用于所有 Plaud API 操作的命令行工具 |
| `PLAUD_API.md` | 详细的 API 端点文档 |
| `requirements.txt` | Python 依赖项 |
| `.env.example` | 凭证模板 |
---
name: fireflies-ai
description: "Fireflies.ai 提供会议智能服务——通过 GraphQL API 搜索会议、获取会议记录、行动项、会议总结、参会者信息以及联系人信息。该服务不进行任何数据存储，而是直接查询 Fireflies 服务器。您可以使用该服务进行会议搜索、会议记录查询、行动项提取、会议总结查看、参会者信息查询以及生成智能会议笔记。"
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+ (stdlib only — no dependencies)
metadata: {"openclaw": {"emoji": "🔥", "requires": {"env": ["FIREFLIES_API_KEY"]}, "primaryEnv": "FIREFLIES_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---
# 🔥 Fireflies AI

您可以直接查询 Fireflies.ai 的会议数据——包括会议记录、会议总结、待办事项、联系人信息以及分析报告。所有数据都存储在 Fireflies 服务器上，无需本地存储。

## 主要功能

- **按关键词、日期范围、主持人或参与者搜索会议**  
- **获取包含发言者信息的完整会议记录**  
- **提取会议中的待办事项和会议总结**  
- **会议分析**：分析会议情绪氛围、发言者发言情况以及发言时长  
- **联系人查询**：查看您与哪些人进行过交流  
- **用户信息**：查看账户详情和团队成员信息  

## 所需参数

| 参数名 | 是否必填 | 说明 |
|----------|----------|-------------|
| `FIREFLIES_API_KEY` | ✅ | 来自 [app.fireflies.ai/integrations](https://app.fireflies.ai/integrations/custom/fireflies) 的 API 密钥 |

## 快速入门

```bash
# List recent meetings
python3 {baseDir}/scripts/fireflies.py meetings --limit 10

# Search meetings by keyword (searches titles and spoken words)
python3 {baseDir}/scripts/fireflies.py search "quarterly review"

# Search within specific date range
python3 {baseDir}/scripts/fireflies.py meetings --from 2026-01-01 --to 2026-02-01

# Filter by participant email
python3 {baseDir}/scripts/fireflies.py meetings --participant "john@example.com"

# Filter by host email
python3 {baseDir}/scripts/fireflies.py meetings --host "jane@example.com"

# Get full transcript for a meeting
python3 {baseDir}/scripts/fireflies.py transcript <meeting_id>

# Get summary only
python3 {baseDir}/scripts/fireflies.py summary <meeting_id>

# Get action items only
python3 {baseDir}/scripts/fireflies.py actions <meeting_id>

# Get meeting analytics (sentiment, speaker stats)
python3 {baseDir}/scripts/fireflies.py analytics <meeting_id>

# Get attendee info for a meeting
python3 {baseDir}/scripts/fireflies.py attendees <meeting_id>

# List all contacts
python3 {baseDir}/scripts/fireflies.py contacts

# Get current user info
python3 {baseDir}/scripts/fireflies.py user

# Get team members
python3 {baseDir}/scripts/fireflies.py users
```

## 输出格式

所有命令默认以 JSON 格式输出。若需可读的格式化输出，请添加 `--human` 参数。

```bash
# JSON (default, for programmatic use)
python3 {baseDir}/scripts/fireflies.py meetings --limit 5

# Human-readable
python3 {baseDir}/scripts/fireflies.py meetings --limit 5 --human
```

## 脚本参考

| 脚本名 | 说明 |
|--------|-------------|
| `{baseDir}/scripts/fireflies.py` | 主要的命令行工具，支持所有查询功能 |

## 数据政策

本工具 **绝不将会议数据存储在本地**。所有查询请求都会直接发送到 Fireflies 的 GraphQL API（`https://api.fireflies.aigraphql`），结果会直接输出到标准输出（stdout）。您的会议数据始终保存在 Fireflies 服务器上。

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发  
[YouTube 频道](https://youtube.com/@aiwithabidi) | [GitHub 仓库](https://github.com/aiwithabidi)  
该工具是 OpenClaw 代理的 **AgxntSix Skill Suite** 的一部分。

📅 **需要帮助为您的企业配置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
---
name: whatsapp-automation
description: "使用 OpenClaw 和 Claude 的定时任务（cron jobs）实现 WhatsApp 自动化功能：能够检测约会信息、重要消息，并自动建议将相关内容添加到日历中。"
---

⚠️ **已弃用 - 请使用新版本！**  
此技能已被更新、更完善的版本取代：  
🔗 **推荐的新技能：** https://www.clawhub.ai/Vincent-Labarthe/whatsapp-telegram-calendar-alert  

**新版本的改进之处：**  
- ✅ 更出色的约会检测功能  
- ✅ 与日历的集成更加便捷（支持添加约会记录）  
- ✅ 设置流程更加简洁  
- ✅ 文档更加清晰易懂  
- ✅ 保证没有重复记录  

**请使用新版本。** 旧版本仅保留供参考之用。  

---

# 📱 WhatsApp 自动化技能  
自动捕获 WhatsApp 消息，并通过 Claude 分析功能发送智能的 Telegram 通知。  

---

## 先决条件  
在开始设置之前，请确保您已具备以下条件：  
- ✅ 安装了 **OpenClaw**（并配置了 cron 任务和消息处理工具）  
- ✅ 配置了 AI 代理（如 Claude、Gemini、Anthropic 等）  
- ✅ 在 OpenClaw 配置中配置了 Telegram 机器人（用于接收通知）  
- （可选）配置了 Google 日历 API（用于添加日历事件）  

## 🚀 一键设置  
执行以下命令即可完成设置：  
```bash
bash ~/.openclaw/workspace/whatsapp-automation-skill/setup.sh
```  
该命令将：  
1. 启动用于捕获 WhatsApp 消息的 WAHA（基于 Docker 的服务）  
2. 创建两个 OpenClaw cron 任务（用于执行 Claude 分析）  
3. 设置消息存储路径  

设置完成！ ✅  

---

## 功能介绍  
| 功能        | 实现方式           |  
|------------|-----------------|  
| 🗓️ **约会检测**    | AI 代理会识别“会议/约会/聚会”等关键词，并询问是否需要将其添加到 Google 日历中 |  
| 📌 **重要消息**    | AI 会根据消息的语气和关键词判断其重要性，并发送 Telegram 通知 |  
| 💾 **消息存储**    | 所有 WhatsApp 消息会被保存在 `~/.openclaw/workspace/.whatsapp-messages/messages.jsonl` 文件中 |  
| ⏱️ **持续监控**    | 每 5 分钟通过 OpenClaw 的 cron 任务自动执行检测（非 Launchd 脚本） |  

---

## 工作原理  
```
WhatsApp → WAHA (Docker) → messages.jsonl
                              ↓
                        (every 5 min)
                              ↓
                    OpenClaw Cron Jobs
                              ↓
                    Claude AI Analysis
                              ↓
                    Telegram Alerts
                              ↓
                      Your Telegram
```  
### AI 分析的工作原理  
两个 cron 任务会分别运行 OpenClaw 的 `agentTurn` 任务，这些任务会启动独立的 AI 代理来处理消息：  
- **第一个任务：WhatsApp 智能分析器**：读取 WhatsApp 消息，检测约会信息，并提示是否需要添加到日历中。  
- **第二个任务：重要消息处理**：评估消息的重要性，仅在消息确实重要时发送通知。  
- **每个任务每 5 分钟执行一次**。  

您的 AI 代理会执行以下操作：  
- 检测约会信息（如“会议”、“约会”、“聚会”等关键词及上下文）  
- 评估消息的重要性（通过关键词和语气分析）  
- （可选）将结果同步到 Google 日历  

**注意：** 该技能支持您在 OpenClaw 中配置的任何 AI 代理或模型（Claude、Gemini 或自定义模型）。  

### 数据流  
```
WhatsApp → WAHA (Docker) → messages.jsonl
                              ↓
                        (every 5 min)
                              ↓
                    OpenClaw Cron Job
                              ↓
                    Your Configured AI Agent
                    (Claude, Gemini, etc)
                              ↓
                    Telegram Bot API
                              ↓
                      Your Telegram
```  

---

## 设置完成后  
### 验证系统是否正常运行  
```bash
# Check OpenClaw cron jobs
cron list

# Should show:
# ✅ WhatsApp Smart Analyzer
# ✅ Important Messages
```  
### 查看消息存储文件  
```bash
# View latest messages
tail ~/.openclaw/workspace/.whatsapp-messages/messages.jsonl | jq '.'

# Count total messages
wc -l ~/.openclaw/workspace/.whatsapp-messages/messages.jsonl
```  
### 查看通知日志  
```bash
# See sent alerts
tail ~/.openclaw/workspace/.whatsapp-messages/alerts.log
```  
### 测试功能  
**发送一条 WhatsApp 消息**：  
```
"meeting tomorrow at 3pm"
```  
**您会收到相应的 Telegram 通知**：  
```
🗓️ Meeting detected
Day: tomorrow
Time: 3:00 PM

Tu veux que j'ajoute ça à Google Calendar? (oui/non)
```  

---

## 配置选项  
### 自定义检测规则  
您可以在 OpenClaw 中修改 cron 任务的配置：  
```bash
cron list  # Get job IDs
cron update <job-id> --patch '{"payload":{"message":"YOUR NEW PROMPT"}}'
```  
### 为特定联系人设置个性化监控  
您可以为特定联系人创建额外的 cron 任务：  
```bash
cron add --job '{
  "name": "Monitor Contact",
  "schedule": {"kind": "every", "everyMs": 300000},
  "payload": {"kind": "agentTurn", "message": "Check messages from specific contact..."},
  "sessionTarget": "isolated"
}'
```  

---

## 常见问题及解决方法  
### 为什么没有收到通知？  
**可能原因及解决方法：**  
- **检查 cron 任务是否正确配置**  
- **更新 cron 任务的提示信息以提升准确性**  
- **确保微信消息被正确捕获**（可在 WAHA 控制面板中重新扫描 QR 码）  
- **查看相关文档（references/TROUBLESHOOTING.md）**  

---

## 相关文件  
- `setup.sh`：安装脚本  
- `scripts/`：辅助脚本（大部分功能已弃用，现使用 cron 任务）  
- `.whatsapp-messages/`：消息存储目录  
- `references/`：高级使用说明文档  
- `LICENSE.md`：许可证（CC BY-ND-NC 4.0）  

---

## 该技能的优势  
- ✅ Claude AI 智能分析消息  
- ✅ OpenClaw 的 cron 任务每 5 分钟自动执行一次  
- ✅ 提供详细的 Telegram 通知  
- ✅ 支持与 Google 日历的集成  
- ✅ 可为特定联系人设置个性化监控规则  

---

## 许可证  
**许可证：** CC BY-ND-NC 4.0  
- **用途限制**：仅限个人使用，禁止商业用途或修改源代码  
- **分享要求**：允许分享未经修改的版本  
- **商业使用及修改说明**：详见 `LICENSE.md`  

---

## 链接  
- WAHA：https://waha.devlike.pro/  
- OpenClaw：https://docs.openclaw.ai/  
- ClawhHub：https://clawhub.com/
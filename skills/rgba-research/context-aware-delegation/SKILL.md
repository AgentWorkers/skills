---
name: context-aware-delegation
description: 使用 `sessions_history` 为孤立的会话（如 Cron 作业、子代理、事件处理器）提供来自主会话的完整对话上下文。这样，您可以运行成本较低的背景任务（如 Haiku），同时仍能享受到高精度的数据处理能力（类似 Sonnet 级别的处理能力）——实现了两全其美的效果。
homepage: https://gitlab.com/rgba_research/context-aware-delegation
author: RGBA Research
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "requires": { "tools": ["sessions_list", "sessions_history"] },
      },
  }
---
# 上下文感知的委托机制  
## （又称“SmartBeat”）  

**问题：** 隔离会话（如定时任务、子代理）无法查看主会话的对话历史记录。虽然这些隔离会话的成本较低（使用 Haiku），但它们无法理解上下文信息。  

**解决方案：** 使用 `sessions_history` 功能，让隔离会话能够全面了解主会话中发生的事情——而且成本仅为在主会话中运行所有操作的几分之一。  

## 快速入门  

### 早晨报告示例  
你希望生成每日报告，内容包括“昨晚完成了什么”——但在主会话中使用 Sonnet 运行该报告的成本约为每份报告 $0.30。而使用 Haiku 在隔离会话中运行则只需约 $0.03，但无法查看对话历史记录。  

**解决方案：** 隔离会话首先查询主会话的历史记录。  

```javascript
// Inside your cron payload.message:
"1. Query main session history: sessions_history('agent:main:telegram:direct:{userId}', limit=50)
2. Read memory files: memory/YYYY-MM-DD.md
3. Fetch weather for Austin 78721
4. Generate report combining:
   - Recent conversation highlights
   - Memory file summaries
   - Current conditions
5. Send via Telegram + email"
```  

**成本：** 使用 Haiku 约 $0.03（比使用 Sonnet 在主会话中运行便宜 10 倍）  
**优势：** 全面了解夜间工作的内容  

## 模式概述  

### 1. 确定主会话的标识符  
```bash
# List sessions to find main
sessions_list(limit=10)
# Typical main session key format:
# agent:main:telegram:direct:{userId}
# agent:main:main
```  

### 2. 从隔离会话中查询历史记录  
```javascript
// In cron job, sub-agent, or event handler:
sessions_history({
  sessionKey: "agent:main:telegram:direct:8264585335",
  limit: 50  // Last 50 messages
})
```  
即使处于隔离会话中，也能获取对话历史记录。  

### 3. 结合上下文执行任务  
现在，你的隔离会话具备了以下功能：  
- ✅ 对话历史记录（讨论的内容）  
- ✅ 内存文件（持久化的笔记）  
- ✅ 低成本的工具（Haiku）  
- ✅ 完整的工具访问权限  

## 使用场景  

### 带有上下文的定时任务  
**早晨报告：**  
```bash
Schedule: 8 AM daily
Model: Haiku (~$0.03/run)
Task: Read overnight work, check email, send summary
Context: Last 50 messages from main session
```  

**每日总结：**  
```bash
Schedule: 9 PM daily
Model: Haiku
Task: What got done today? What's pending?
Context: Today's full conversation
```  

**定期检查：**  
```bash
Schedule: Every 2 hours (9 AM - 9 PM)
Model: Haiku
Task: Anything urgent in email/calendar?
Context: Recent discussion about priorities
```  

### 子代理的委托机制  
**后台构建任务：**  
```javascript
sessions_spawn({
  task: "Build the AREF product page based on our discussion",
  model: "haiku",
  // In the task prompt:
  // "First, query main session history to see our conversation about AREF requirements..."
})
```  

**研究任务：**  
```javascript
sessions_spawn({
  task: "Research Unreal Engine integration patterns. Reference our earlier discussion about AREF goals.",
  model: "haiku"
})
```  

### 基于事件的处理器  
**Webhook 到达 → 由隔离会话处理：**  
```javascript
// Webhook payload triggers isolated session
// Session logic:
"1. Query main session to see: what did J and I agree about this client?
2. Process webhook based on that context
3. Take action or notify"
```  

## 成本对比  
| 方法 | 工具 | 上下文支持 | 每次运行成本 | 适用场景 |  
|--------|--------|-----------|----------------|-------------|  
| 主会话 | Sonnet | 完全支持 | 约 $0.30 | 复杂的交互式任务 |  
| 隔离会话（无上下文支持） | Haiku | 无 | 约 $0.03 | 简单的定时任务 |  
| **上下文感知的委托机制** | Haiku | 完全支持 | 约 $0.03 | 需要上下文的后台任务 |  

**节省成本：** 比使用主会话便宜约 10 倍，同时仍能保持相同的上下文感知能力。  

## 实现技巧  

### 查找主会话的标识符  
```javascript
sessions_list({ kinds: ["main"], limit: 5 })
// Or:
sessions_list({ limit: 10 })
// Look for: agent:main:telegram:direct:{yourUserId}
```  

### 需要查询多少历史记录？  
- **10 条消息：** 只显示最近的上下文信息（约 2KB）  
- **50 条消息：** 最近几小时的工作内容（约 10KB）  
- **100 条消息：** 全天的或跨会话的上下文信息（约 20KB）  
根据需求调整查询量。  

### 结合历史记录和内存文件  
最佳效果来自：  
1. **会话历史记录**：最近的交互式操作  
2. **内存文件**：持久化的决策/笔记  

```javascript
"1. sessions_history(limit=30) → what we discussed today
2. read memory/2026-02-13.md → decisions logged
3. Combine both sources for complete picture"
```  

### 早晨报告的实现示例  
完整的每日早晨报告流程：  
**定时任务设置：**  
```javascript
{
  schedule: { kind: "cron", expr: "0 8 * * *", tz: "America/Chicago" },
  sessionTarget: "isolated",
  payload: {
    kind: "agentTurn",
    model: "haiku",
    message: `Generate morning report:

1. Query main session: sessions_history('agent:main:telegram:direct:8264585335', limit=50)
2. Read yesterday's memory: memory/YYYY-MM-DD.md
3. Get weather: Austin 78721
4. Check email (gog or himalaya)
5. Check calendar events for today

Report format:
📍 WEATHER: [conditions]
🌙 OVERNIGHT: [from session history - what we worked on]
📝 PERSISTENT NOTES: [from memory file]
📧 EMAIL: [urgent only]
📅 CALENDAR: [today's events]
🔗 DASHBOARD: [mission control link]

Send to Telegram using message tool.

Note: Email delivery from isolated sessions requires SMTP credentials or is better handled via main session heartbeats for reliability.`
  },
  delivery: { mode: "announce", to: "8264585335", channel: "telegram" }
}
```  

**成本：** 每份报告约 $0.03（每月约 $1）  
**优势：** 全面了解夜间工作的内容  
**时间安排：** 每天早上 8 点  

## 限制因素  

**历史记录的截断：**  
- `sessions_history` 只返回有限的内容（通常是最近 N 条消息）  
- 非常长的消息可能会被截断  
- 对于长期存档，需依赖内存文件  

**主会话必须存在：**  
- 如果主会话是新创建的（没有消息），历史记录为空  
- 隔离会话只能读取历史记录，无法创建新的历史记录  

**非实时性：**  
- 历史记录反映的是查询时的状态  
- 如果主会话正在运行中，最新的消息可能不会立即显示  

## 最佳实践：  
**1. 编写良好的内存摘要**  
即使可以访问会话历史记录，持久化的内存文件仍然非常重要。不要仅依赖对话历史记录。  
**2. 仅查询所需的内容**  
- `limit=10` 用于快速获取上下文信息  
- `limit=50` 用于处理大量数据  
- `limit=100` 用于深入分析  

**3. 有效组合工具**  
首先获取上下文信息，再执行相应操作。  
**4. 使用 Haiku 进行委托处理，使用 Sonnet 进行决策**  
- 后台任务：使用 Haiku  
- 交互式问题解决：使用 Sonnet  
- 早晨报告/总结：使用 Haiku  
- 架构讨论：使用 Sonnet  

## 故障排除：  
**“会话历史记录为空”**  
- 确认主会话的标识符是否正确（使用 `sessions_list()`）  
- 主会话可能是新创建的（尚未有任何消息）  
- 使用 `limit` 参数来控制查询范围  

**“内容被截断”**  
- 减小 `limit` 的值（查询更多消息可获取更完整的内容）  
- 对于长期存档数据，依赖内存文件  

**“隔离会话无法发送消息”**  
- 使用 `message` 工具，而非 `sessions_send`  
- 确保在定时任务配置中设置了 `delivery.mode`，或直接使用 `message` 工具发送消息  

**相关模式：**  
- **心跳机制（Heartbeats）**：主会话定期检查（提供完整上下文和模型支持）  
- **子代理**：长时间运行的后台任务  
- **定时任务**：计划好的隔离式工作  
- **内存文件**：用于跨会话的数据存储  

## 致谢  
该机制由 RGBA Research 在 OpenClaw 优化过程中发现，并作为开源模式发布在 ClawHub 上供社区使用。  

**联系方式：** https://rgbaresearch.com  
**许可证：** MIT 许可（免费使用、修改和分享）
---
name: secondmind
emoji: 🧠
version: 1.3.0
description: >
  Autonomous three-tier memory with proactive initiative and social intelligence.
  Ingests OpenClaw conversations, extracts knowledge + emotions,
  and proactively suggests automations, fixes, and project ideas.
  v1.3.0: Semantic dedup, bulk feedback, archive retrieval, gentle reminders.
  All models via OpenRouter Cloud. Cross-platform: Linux + Windows.
metadata:
  openclaw:
    requires:
      bins: ["node"]
    install:
      - id: npm
        kind: shell
        command: "cd {baseDir} && npm install --production"
        label: "Install SecondMind dependencies"
    config:
      stateDirs: ["data"]
---

# SecondMind – 自主AI记忆、主动建议与社交智能

## 使用场景
在以下情况下激活该功能：
- 用户请求设置、配置或查看SecondMind的状态；
- 用户希望搜索知识库或回忆过去的对话内容；
- 用户请求主动提出的建议或项目想法；
- 用户提及与过去会话相关的记忆、信息或上下文；
- 用户发送 `/new` 或 `/reset` 命令（触发预重置操作）；
- 用户询问自己的情绪状态或即将发生的事件；
- 用户发送任何与SecondMind相关的Telegram命令（详见下文）。

## 首次运行设置
如果数据库文件 `{baseDir}/data/secondmind.db` 不存在，请按照以下步骤操作：
```bash
node {baseDir}/setup.js
```
然后指导用户编辑 `{baseDir}/config.json` 文件：
1. 设置 `openrouter.apiKey`（必填项——请在 https://openrouter.ai/keys 获取API密钥）；
2. 确保 `openclaw.sessionsDir` 的路径与用户的代理会话目录匹配；
3. （可选）：启用Telegram通知功能。

## 重要提示：重置前的数据备份
当用户发送 `/new` 或 `/reset` 命令时：
1. 在重置生效之前，先运行以下代码：
   ```bash
   node {baseDir}/scripts/flush.js
   ```
2. 向用户回复脚本的输出结果（例如：“💾 会话已归档。”）
3. 然后允许重置操作正常进行。

## Telegram命令（集成模式）
当 `config.json` 中的 `telegramMode` 设置为 `"integrated"` 时，OpenClaw 代理会直接处理这些命令。执行相应的脚本并生成相应的回复。

### 命令说明：
- `/smstatus` 或 `/es`  
  ```bash
node {baseDir}/scripts/status.js
```

- `/proposals` 或 `/ep [filter]`  
  ```bash
node {baseDir}/scripts/proposals.js [proposed|accepted|rejected|all]
```

- `/accept <ID...> [comment]` 或 `/ea <ID...> [comment]`  
  ```bash
node {baseDir}/scripts/feedback.js accept <ID...> [comment]
```  
  支持多个ID：`/accept 1 3 5` 或 `/accept all`  
  接受建议后：
  1. 从数据库中读取该建议的 `follow_up` 字段：  
    `sqlite3 {baseDir}/data/secondmind.db "SELECT follow_up, description FROM proposals WHERE id=<ID>"`
  2. 如果有后续问题，向用户提出；
  3. 如果用户同意，立即开始处理该任务。  
  示例流程：
    - 用户：`/accept 5`
    - 代理：`✅ 已接受建议5。需要我为你整理相关指南吗？`
    - 用户：`是的，请帮忙。`
    - 代理：*开始处理任务*

- `/reject <ID...> [comment]` 或 `/er <ID...> [comment]`  
  ```bash
node {baseDir}/scripts/feedback.js reject <ID...> [comment]
```  
  支持多个ID：`/reject 2 4` 或 `/reject all`  
  简短回复确认即可，无需过度解释。

- `/defer <ID...> [comment]` 或 `/ed <ID...> [comment]`  
  ```bash
node {baseDir}/scripts/feedback.js defer <ID...> [comment]
```  
  用于暂时推迟处理某个建议。

- `/drop <ID...>` 或 `/drop all older_than <duration>`  
  ```bash
node {baseDir}/scripts/feedback.js drop <ID...>
node {baseDir}/scripts/feedback.js drop all older_than 14d
```  
  永久删除某个建议——该建议将不再被推荐。  
  支持的命令：`/drop 2 4`、`/drop all`、`/drop all older_than 14d`  

- `/mute <duration>` 或 `/unmute`  
  ```bash
node {baseDir}/scripts/feedback.js mute 1d
node {baseDir}/scripts/feedback.js mute 1w
node {baseDir}/scripts/feedback.js unmute
```  
  在指定时间内暂停所有通知和主动建议的发送。  
  可选时间范围：`1h`、`1d`、`1w`、`2w`  

### 自然语言反馈
该机器人能够理解用户对最近显示的建议的反馈：
- “先处理前两个建议，其余的忽略。”
- “1号和3号建议不错，其余的都删除。”
- “除了安全相关的建议外，全部删除。”

- `/smsearch <query>` 或 `/smsr <query>`  
  ```bash
node {baseDir}/scripts/search.js "<query>" --no-rerank
```  
  用于在数据库中搜索信息。

- `/mood` 或 `/em`  
  从 `{baseDir}/data/secondmind.db` 中查询用户的情绪状态：
  ```sql
SELECT mood, COUNT(*) as count FROM social_context
WHERE detected_at > datetime('now', '-7 days')
GROUP BY mood ORDER BY count DESC;
```  
  用表情符号表示情绪：😤（沮丧）🎉（兴奋）😰（担忧）🥳（庆祝）😫（压力）🤔（好奇）😴（无聊）🙏（感激）

- `/smrun` 或 `/smrun`  
  ```bash
cd {baseDir} && node scripts/ingest.js && node scripts/consolidate.js && node scripts/initiative.js
```  
  用于执行某些特定操作。

## 独立运行模式（可选）
当 `telegramMode` 设置为 `"standalone"` 时，用户会运行一个独立的Telegram机器人：
```bash
node {baseDir}/scripts/telegram-bot.js
```  
  此模式需要一个专用的Telegram机器人令牌（与OpenClaw代理的令牌不同）。独立机器人通过自己的轮询循环处理所有上述命令。

## 后台任务（由 `setup.js` 脚本执行）：
- **数据导入**：每30分钟一次，导入JSONL格式的会话记录；
- **数据整合**：每6小时一次，提取知识、情绪和事件信息；
- **数据归档**：每天凌晨3点，将成熟的知识内容导入长期存储的FTS5索引；
- **主动建议生成**：每6小时生成新的建议并通过Telegram发送通知。

## 配置文件说明：
编辑 `{baseDir}/config.json` 文件，设置以下参数：
- `openrouter.apiKey`：OpenRouter API密钥（必填）；
- `openclaw.sessionsDir`：代理会话目录的路径；
- `telegramMode`：`"integrated"`（通过OpenClaw集成）或 `"standalone"`（独立运行）；
- `notifications.enabled`：是否将建议发送到Telegram（默认值为 `true`）；
- `notifications.telegram_botToken`：你的Telegram机器人令牌；
- `notificationsTelegram.chatId`：你的Telegram聊天ID；
- `models.*`：指定的LLM模型（已预先优化，必要时可更改）；
- `initiative.reminderCooldownDays`：延迟提醒的建议间隔天数（默认值：7天）；
- `initiative.maxNudgesPerProposal`：每个建议的最大提醒次数（默认值：2次）；
- `initiative.dedupThreshold`：建议去重的语义相似度阈值（默认值：0.85）。

## 常见问题解决方法：
- “数据库被锁定”：可能是Cron任务正在运行，请等待30秒；
- “OpenRouter错误”：检查API密钥和余额信息（请访问 https://openrouter.ai/）；
- “没有新数据”：检查 `config.json` 中的 `openclawSessionsDir` 是否正确；
- Telegram冲突：两个机器人使用相同的令牌——请切换到集成模式或创建第二个机器人；
- 重置操作：运行 `node {baseDir}/setup.js --reset`。

## 成本
通过OpenRouter Cloud服务的费用约为每月0.60–1.65美元。具体价格请参考 https://openrouter.ai/models。
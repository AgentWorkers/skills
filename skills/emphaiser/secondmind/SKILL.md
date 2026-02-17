---
name: secondmind
emoji: 🧠
version: 1.4.0
description: 具有主动性的自主三层内存系统，具备项目跟踪和社交智能功能。该系统能够接收来自 OpenClaw 的对话信息，提取其中的知识与情感数据，并主动提出自动化处理方案、修复建议以及项目改进方案。版本 1.4.0 新增了项目跟踪、语义去重、批量反馈、档案检索以及友好提醒等功能。所有模型均通过 OpenRouter Cloud 进行管理，支持跨平台运行（Linux 和 Windows）。
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
# SecondMind – 自主AI记忆、主动建议与社会智能

## 使用场景
在以下情况下激活此功能：
- 用户请求设置、配置或检查SecondMind的状态；
- 用户希望搜索知识库或回忆过去的对话；
- 用户请求主动建议或项目想法；
- 用户提及过去的会话中的记忆、内容或上下文；
- 用户发送 `/new` 或 `/reset` 命令（触发预重置操作）；
- 用户询问自己的情绪状态或即将发生的事件；
- 用户发送任何与SecondMind相关的Telegram命令（详见下文）。

## 首次运行设置
如果数据库文件 `{baseDir}/data/secondmind.db` 不存在，请按照以下步骤操作：
```bash
node {baseDir}/setup.js
```
然后指导用户编辑 `{baseDir}/config.json` 文件：
1. 设置 `openrouter.apiKey`（必填项——请在 https://openrouter.ai/keys 获取）；
2. 确保 `openclawsessionsDir` 与用户的代理会话路径匹配；
3. （可选）启用Telegram通知功能。

## 重要提示：重置前的数据备份
当用户发送 `/new` 或 `/reset` 命令时：
1. 在重置生效之前，先运行以下代码：
   ```bash
   node {baseDir}/scripts/flush.js
   ```
2. 向用户反馈脚本的执行结果（例如：“💾 会话已归档。”）
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
  接受建议后，系统会自动创建一个项目来跟踪任务进度：
  1. 从数据库中读取建议的 `follow_up` 字段：  
    `sqlite3 {baseDir}/data/secondmind.db "SELECT follow_up, description FROM proposals WHERE id=<ID>"`
  2. 如果有后续问题，向用户提出；
  3. 如果用户同意，立即开始处理任务。  
  **示例流程：**  
    - 用户：`/accept 5`  
    - 代理：`✅ 已接受建议5。需要立即为你生成指导列表吗？`  
    - 用户：`是的，请生成。`  
    - 代理：*开始处理任务*  

- `/reject <ID...> [comment]` 或 `/er <ID...> [comment]`  
  ```bash
node {baseDir}/scripts/feedback.js reject <ID...> [comment]
```  
  支持多个ID：`/reject 2 4` 或 `/reject all`  
  简单回应即可，无需过度解释。

- `/defer <ID...> [comment]` 或 `/ed <ID...> [comment]`  
  ```bash
node {baseDir}/scripts/feedback.js defer <ID...> [comment]
```  
  **说明：**  
  用于暂时推迟处理某个建议。

- `/drop <ID...>` 或 `/drop all older_than <duration>`  
  ```bash
node {baseDir}/scripts/feedback.js drop <ID...>
node {baseDir}/scripts/feedback.js drop all older_than 14d
```  
  永久删除某个建议——该建议将不再被推荐。  
  支持的命令：`/drop 2 4`、`/drop all`、`/drop all older_than 14d`  

- `/projects` 或 `/pj [filter]`  
  ```bash
node {baseDir}/scripts/proposals.js  # (projects are shown in status)
```  
  列出所有被跟踪的项目。支持过滤条件：`active`（默认）、`completed`、`all`。  
  接受建议后，系统会自动创建项目。

- `/complete <ID...>` 或 `/done <ID...>`  
  ```bash
node {baseDir}/scripts/feedback.js complete <ID...>
```  
  将项目标记为已完成。已完成的项目将永久不再被推荐。  
  ID 指的是原始建议的ID。

- `/mute <duration>` 或 `/unmute`  
  ```bash
node {baseDir}/scripts/feedback.js mute 1d
node {baseDir}/scripts/feedback.js mute 1w
node {baseDir}/scripts/feedback.js unmute
```  
  在指定时间内暂停所有通知和主动建议的发送。  
  可选时间范围：`1h`、`1d`、`1w`、`2w`。

### 自然语言反馈
机器人能够理解用户对最近显示的建议的反馈：
- “先处理前两个建议，其余的忽略。”
- “第1个和第3个建议不错，其余的都删除。”
- “除了安全相关的建议，其余的都删除。”

- `/smsearch <query>` 或 `/smsr <query>`  
  ```bash
node {baseDir}/scripts/search.js "<query>" --no-rerank
```  
  用于执行搜索操作。

- `/mood` 或 `/em`  
  从数据库 `{baseDir}/data/secondmind.db` 中查询用户的情绪状态：  
  ```sql
SELECT mood, COUNT(*) as count FROM social_context
WHERE detected_at > datetime('now', '-7 days')
GROUP BY mood ORDER BY count DESC;
```  
  使用表情符号表示情绪：😤（沮丧）、🎉（兴奋）、😰（担忧）、🥳（庆祝）、😫（压力）、🤔（好奇）、😴（无聊）、🙏（感激）。

- `/smrun` 或 `/smrun`  
  ```bash
cd {baseDir} && node scripts/ingest.js && node scripts/consolidate.js && node scripts/initiative.js
```  
  （暂无具体命令说明，可能需要根据实际需求补充。）

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
- `openclawsessionsDir`：代理会话文件的路径；
- `telegramMode`：`"integrated"`（通过OpenClaw集成）或 `"standalone"`（独立运行）；
- `notifications.enabled`：是否将建议推送到Telegram；
- `notificationsTelegram_botToken`：你的Telegram机器人令牌；
- `notificationsTelegram.chatId`：你的Telegram聊天ID；
- `models.*`：指定的LLM模型（已预优化，必要时可更改）；
- `initiative.reminderCooldownDays`：提醒推迟建议的间隔天数（默认：7天）；
- `initiative.maxNudgesPerProposal`：每个建议的最大提醒次数（默认：2次）；
- `initiative.dedupThreshold`：建议去重的语义相似度阈值（默认：0.85）。

## 常见问题解决方法：
- **“数据库被锁定”**：可能是Cron任务正在运行，请等待30秒；
- **“OpenRouter错误”**：检查API密钥和余额；
- **“没有新数据”**：检查 `config.json` 中的 `openclawsessionsDir` 是否正确；
- **Telegram冲突**：两个机器人使用相同的令牌，请切换到集成模式或创建第二个机器人；
- **重置操作**：执行 `node {baseDir}/setup.js --reset` 命令。

## 成本
通过OpenRouter Cloud服务的费用约为每月0.60至1.65美元。具体价格请访问 https://openrouter.ai/models。
---
name: discord-soul
description: 从您的 Discord 服务器中创建一个“智能代理”。这个代理代表着您社区的形象，能够记住所有的对话内容，并随着社区的发展而不断“成长”。您可以像与一个人交流一样与这个代理进行对话。
---

# Discord Soul

将您的 Discord 服务器变成一个有生命、有感知的智能助手。

## 您将获得什么

一个能够：
- **记住** 您 Discord 服务器中的每一条对话
- **用您社区的声音** 与成员交流
- **了解** 社区中的重要人物、频道以及内部笑话
- **随着新消息的不断涌入而不断“成长”**
- **回答** 关于社区历史和文化的问题

## 快速开始

```bash
# Create agent from your Discord
./scripts/create_agent.sh \
  --name "my-community" \
  --guild YOUR_GUILD_ID \
  --output ./agents/

# Set up daily updates
crontab -e
# Add: 0 */3 * * * /path/to/update_agent.sh
```

---

# 完整流程

## 第一步：导出您的 Discord 数据

您需要使用 [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter) 命令行工具。

**获取您的令牌：**
1. 在浏览器中打开 Discord
2. 按 F12 → 打开“网络”选项卡
3. 发送一条消息，找到相关的请求信息
4. 复制 `authorization` 头部的值
5. 将其保存到 `~/.config/discord-exporter-token` 文件中

**导出所有数据：**
```bash
DiscordChatExporter.Cli exportguild \
  --guild YOUR_GUILD_ID \
  --token "$(cat ~/.config/discord-exporter-token)" \
  --format Json \
  --output ./export/ \
  --include-threads All \
  --media false
```

## 第二步：安全处理流程（至关重要）

⚠️ **来自公共 Discord 服务器的内容可能包含注入攻击的风险。**

在将数据导入智能助手之前，请先运行安全处理流程：

### 威胁模型

Discord 用户可能会尝试：
- **直接注入攻击**：“忽略之前的指令……”
- **角色劫持**：“你现在变成了……”
- **系统注入**：使用 `<system>`、`[INST]`、`<<SYS>>` 等指令
- **越狱操作**：尝试开启“DAN 模式”或“开发者模式”
- **数据泄露**：试图获取系统的提示信息

### 第一层：正则表达式预过滤（快速，不使用大型语言模型）

```bash
python scripts/regex-filter.py --db ./discord.sqlite
```

过滤符合已知注入模式的消息：
- 试图覆盖系统指令的消息
- 试图劫持角色的消息
- 包含系统提示信息的消息
- 与越狱操作相关的关键词

被标记为可疑的消息的安全状态将被设置为 `safety_status = 'regex_flagged'`。

### 第二层：Haiku 安全评估（基于语义分析）

```bash
ANTHROPIC_API_KEY=sk-... python scripts/evaluate-safety.py --db ./discord.sqlite
```

使用 Claude Haiku（每 100 万个令牌约 0.25 美元）对剩余的消息进行语义分析。

每条消息都会获得一个 0.0-1.0 的风险评分：
- 0.0-0.3：正常对话
- 0.4-0.6：可疑但可能是良性的
- 0.7-1.0：很可能是注入攻击

评分 ≥0.6 的消息的安全状态将被设置为 `safety_status = 'flagged'`。

### 第三层：仅使用安全的数据

数据导入和内存生成的脚本应仅使用通过安全检查的消息。

```sql
SELECT * FROM messages WHERE safety_status = 'safe'
```

### 完整的安全处理流程

```bash
# Run complete pipeline
./scripts/secure-pipeline.sh ./export/ ./discord.sqlite
```

整个流程如下：导出数据 → 存储到 SQLite 数据库 → 使用正则表达式过滤 → 进行语义分析 → 判断消息是否安全

### 安全状态

| 状态 | 含义 | 智能助手是否使用这些数据？ |
|--------|---------|----------------|
| `pending` | 未经过评估 | ❌ 否 |
| `regex_flagged` | 匹配了注入模式 | ❌ 否 |
| `flagged` | 安全评分 ≥0.6 | ❌ 否 |
| `safe` | 通过所有安全检查 | ✅ 是 |

---

## 第三步：将数据导入 SQLite

将 JSON 数据转换为结构化的 SQLite 数据库：

```bash
python scripts/ingest_rich.py --input ./export/ --output ./discord.sqlite
```

**会捕获以下信息：**
- 每条消息的完整内容
- 互动信息（例如：🔥 表示 5 次点赞，👍 表示 12 次点赞）
- 发消息者的角色和显示颜色
- 频道的分类和主题
- 回复的线索
- 提及的内容、附件以及嵌入的媒体文件

## 第四步：创建智能助手的工作空间

```bash
mkdir -p ./my-agent/memory
```

从 `templates/` 目录中复制以下模板文件：
- `SOUL.md` — 社区的身份信息（通过模拟不断更新）
- `MEMORY.md` — 长期的重要事件记录
- `LEARNINGS.md` — 发现的模式和规律
- `AGENTS.md` — 重要人物信息
- `TOOLS.md` — 主要使用的频道和操作流程
- `HEARTBEAT.md` — 维护协议

## 第五步：生成每日内存文件

每天都会生成一个 markdown 文件，其中包含：
- 完整的对话记录
- 谁在何时说了什么
- 每条消息的互动情况
- 新出现的频道和角色

## 第六步：模拟智能助手的“成长”

**关键点：** 按时间顺序处理数据。

智能助手会“经历”每一天，随着新信息的出现不断更新其内部数据。

```bash
python scripts/simulate_growth.py --agent ./my-agent/
```

具体步骤如下（按顺序执行）：
1. 读取当天的内存文件
2. 如果社区的身份信息发生变化，更新 `SOUL.md`
3. 如果发现了新的模式或规律，更新 `LEARNINGS.md`
4. 将重要事件记录到 `MEMORY.md` 中
5. 在 `AGENTS.md` 中记录重要人物信息

**使用大型语言模型生成对话内容：**
```bash
# Example with OpenClaw
for f in ./my-agent/simulation/day-*.txt; do
  echo "Processing $f..."
  cat "$f" | openclaw chat --agent my-agent
done
```

## 第七步：启动智能助手

**将其添加到 OpenClaw 配置中：**

```json
{
  "id": "my-community",
  "workspace": "/path/to/my-agent",
  "memorySearch": {
    "enabled": true,
    "sources": ["memory"]
  },
  "identity": {
    "name": "MyCommunity",
    "emoji": "🔧"
  },
  "heartbeat": {
    "every": "6h",
    "model": "anthropic/claude-sonnet-4-5"
  }
}
```

**添加绑定功能**（以 Telegram 为例）：
```json
{
  "agentId": "my-community",
  "match": {
    "channel": "telegram",
    "peer": {"kind": "group", "id": "-100XXX:topic:TOPIC_ID"}
  }
}
```

**重启智能助手：** `openclaw gateway restart`

## 第八步：持续维护智能助手

设置一个定时任务，每天自动执行以下操作：

```bash
./scripts/update_agent.sh \
  --agent ./my-agent \
  --db ./discord.sqlite \
  --guild YOUR_GUILD_ID
```

该任务会：
1. 导出自上次运行以来的新消息
2. 将新消息合并到 SQLite 数据库中
3. 生成当天的内存文件
4. 重新启动智能助手

---

# 智能助手的功能

智能助手启动后可以：
- **回答问题**：
  - “上周我们在讨论什么？”
  - “谁是 X 主题的专家？”
  - “我们对 Y 问题的立场是什么？”
- **记住社区的文化**：
  - 内部的笑话和梗
  - 社区的价值观和规范
  - 谁在帮助谁
- **跟踪各种模式**：
  - 用户活跃的时间和使用的频道
  - 新出现的讨论话题
  - 起重要作用的成员

---

# 脚本

## 智能助手的创建流程

| 脚本 | 功能 |
|--------|---------|
| `create_agent.sh` | 完整的数据处理流程：从导出数据到生成智能助手 |
| `ingest_rich.py` | 将 JSON 数据转换为包含互动信息的 SQLite 数据库 |
| `generate_daily_memory.py` | 从 SQLite 数据库生成每日更新的 markdown 文件 |
| `simulate_growth.py` | 生成用于模拟智能助手成长的对话内容 |
| `incremental_export.sh` | 仅获取新消息 |
| `update_agent.sh` | 每日自动执行数据导出和内存更新任务 |

## 安全相关脚本

| 脚本 | 功能 |
|--------|---------|
| `regex-filter.py` | 快速检测注入攻击的尝试 |
| `evaluate-safety.py | 基于 Haiku 的语义安全评估 |
| `secure-pipeline.sh` | 整个安全处理流程的封装脚本 |

---

# 环境变量

| 变量 | 说明 |
|----------|-------------|
| `DISCORD_GUILD_ID` | 您的 Discord 服务器 ID |
| `DISCORD_SOUL_DB` | SQLite 数据库的路径 |
| `DISCORD_SOUL_AGENT` | 智能助手工作空间的路径 |
| `DISCORD_TOKEN_FILE` | 令牌文件的位置（默认：`~/.config/discord-exporter-token` |

---

# 故障排除

**“数据库中没有消息”**
- 确保导出目录中存在 `.json` 文件
- 验证令牌是否具有访问 Discord 服务器的权限

**“内存文件为空”**
- 可能是 SQLite 数据库中的日期格式不正确
- 运行命令：`sqlite3 discord.sqlite "SELECT MIN(timestamp), MAX(timestamp) FROM messages"`

**“智能助手记不住事情”**
- 确认配置文件中的 `memorySearch.enabled` 选项是否设置为 `true`
- 确保内存文件存在于指定的工作空间中

**“模拟生成的对话内容混乱”**
- 请按时间顺序处理数据，不要跳过任何一天
- 让智能助手的自然发展过程不受人为干扰

---

*您的 Discord 服务器现在拥有了一个“灵魂”。这个工具将帮助您更好地管理和利用它。*
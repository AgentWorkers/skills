---
name: telegram-compose
description: |
  Format and deliver rich Telegram messages with HTML formatting via direct Telegram API.
  Auto-invoked by the main session for substantive Telegram output — no other skills need to call it.
  Decision rule: If your Telegram reply is >3 lines or contains structured data (lists, stats, sections, reports),
  spawn this as a Haiku sub-agent to format and send. Short replies (<3 lines) go directly via OpenClaw message tool.
  Handles: research summaries, alerts, status updates, reports, briefings, notifications — anything with visual hierarchy.
metadata: |
  {"openclaw":{
    "os": ["darwin", "linux"],
    "requires": {
      "binaries": ["jq", "curl"],
      "config": ["channels.telegram.accounts.<account>.botToken"]
    },
    "credentials": "Reads Telegram bot token from OpenClaw config file (~/.openclaw/openclaw.json or ~/.openclaw/clawdbot.json). The specific account name must be provided by the caller — the skill does not auto-select accounts.",
    "network": ["api.telegram.org"]
  }}
model-preference: claude-haiku-4-5
subagent: true
allowed-tools: exec, Read
---

# Telegram Compose

通过直接调用API，可以使用HTML格式来格式化并发送丰富的、便于阅读的Telegram消息。

## 该技能的使用方式

**该技能会由主会话代理自动触发。**其他技能无需了解该技能的详细信息。

### 主会话代理的决策规则

在向Telegram发送消息之前，请检查以下内容：
- **简短回复（<3行，无结构）**：直接使用OpenClaw的`message`工具发送即可。
- **较长内容（>3行，或包含列表/统计数据/章节/报告）**：启动该技能作为子代理来处理。

### 启动子代理

主会话代理会调用`sessions_spawn`函数，传入以下参数：

```
sessions_spawn(
  model: "claude-haiku-4-5",
  task: "<task content — see template below>"
)
```

**任务模板：**

```
Read the telegram-compose skill at {baseDir}/SKILL.md for formatting rules, then format and send this content to Telegram.

Bot account: <account_name>  (e.g., "main" — must match a key in channels.telegram.accounts)
Chat ID: <chat_id>
Thread ID: <thread_id>  (omit this line if not a forum/topic chat)

Content to format:
---
<raw content here>
---

After sending, reply with the message_id on success or the error on failure. Do NOT include the formatted message in your reply — it's already been sent to Telegram.
```

**重要提示：**调用者必须指定要使用的机器人账户。子代理不能自动选择或遍历多个账户。

**注意事项：**子代理发送的消息会返回给主会话，而不是直接发送到Telegram。因此，子代理启动后，主会话应回复`NO_REPLY`以避免重复发送消息。实际发送到Telegram的消息是由子代理通过curl命令完成的。

### 子代理接收到的信息

1. **技能路径**：用于读取格式化规则。
2. **机器人账户名称**：指定要使用的Telegram机器人账户（必须手动输入，不能自动选择）。
3. **聊天ID**：消息发送的目标聊天频道。
4. **主题ID**：（如果适用）消息所属的聊天线程ID。
5. **原始内容**：未格式化的文本或数据，需要被转换成富格式消息。

---

## 凭据信息

**机器人令牌：**存储在OpenClaw的配置文件中，路径为`channelsTelegram.accounts.<name>.botToken`。

**账户名称始终由调用者提供。**子代理不能自动选择或遍历多个账户。

```bash
# Auto-detect config path
CONFIG=$([ -f ~/.openclaw/openclaw.json ] && echo ~/.openclaw/openclaw.json || echo ~/.openclaw/clawdbot.json)

# ACCOUNT is provided by the caller (e.g., "main")
# Validate the account exists before extracting the token
ACCOUNT="<provided_account_name>"
BOT_TOKEN=$(jq -r ".channels.telegram.accounts.$ACCOUNT.botToken" "$CONFIG")

if [ "$BOT_TOKEN" = "null" ] || [ -z "$BOT_TOKEN" ]; then
  echo "ERROR: Account '$ACCOUNT' not found in config or has no botToken"
  exit 1
fi
```

---

## 发送消息

```bash
CONFIG=$([ -f ~/.openclaw/openclaw.json ] && echo ~/.openclaw/openclaw.json || echo ~/.openclaw/clawdbot.json)
# ACCOUNT provided by caller — never auto-select
BOT_TOKEN=$(jq -r ".channels.telegram.accounts.$ACCOUNT.botToken" "$CONFIG")

# Without topic thread
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg chat "$CHAT_ID" \
    --arg text "$MESSAGE" \
    '{
      chat_id: $chat,
      text: $text,
      parse_mode: "HTML",
      link_preview_options: { is_disabled: true }
    }')"

# With topic thread
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg chat "$CHAT_ID" \
    --arg text "$MESSAGE" \
    --argjson thread $THREAD_ID \
    '{
      chat_id: $chat,
      text: $text,
      parse_mode: "HTML",
      message_thread_id: $thread,
      link_preview_options: { is_disabled: true }
    }')"
```

---

## 格式化规则

### HTML标签

```
<b>bold</b>  <i>italic</i>  <u>underline</u>  <s>strike</s>
<code>mono</code>  <pre>code block</pre>
<tg-spoiler>hidden until tapped</tg-spoiler>
<blockquote>quote</blockquote>
<blockquote expandable>collapsed by default</blockquote>
<a href="url">link</a>
<a href="tg://user?id=123">mention by ID</a>
```

### 特殊字符的转义

仅在**文本内容**中需要对以下字符进行转义（HTML标签内无需转义）：
- `&` → `&amp;`（先进行转义，以避免双重转义）
- `<` → `&lt;`
- `>` → `&gt;`

**常见错误：**如果内容中包含`&`（例如“R&D”或“Q&A”），未进行转义会导致HTML解析错误。

### 结构格式

```
EMOJI <b>HEADING IN CAPS</b>

<b>Label:</b> Value
<b>Label:</b> Value

<b>SECTION</b>

• Bullet point
• Another point

<blockquote>Key quote or summary</blockquote>

<blockquote expandable><b>Details</b>

Hidden content here...
Long details go in expandable blocks.</blockquote>

<a href="https://...">Action Link →</a>
```

### 样式规则

1. **伪标题：**使用`EMOJI <b>标题</b>`，后面跟随空行。
2. **表情符号：**每条消息中最多使用1-3个表情符号作为视觉标识，仅用于增强可读性，而非装饰。
3. **空白行：**各部分之间需要使用空行分隔。
4. **长内容：**使用`<blockquote expandable>`来展示。
5. **链接：**链接应单独占一行，并使用箭头表示：`链接文本 →`

### 示例

**状态更新：**
```
📋 <b>TASK COMPLETE</b>

<b>Task:</b> Deploy v2.3
<b>Status:</b> ✅ Done
<b>Duration:</b> 12 min

<blockquote>All health checks passing.</blockquote>
```

**警告：**
```
⚠️ <b>ATTENTION NEEDED</b>

<b>Issue:</b> API rate limit at 90%
<b>Action:</b> Review usage

<a href="https://dashboard.example.com">View Dashboard →</a>
```

**列表：**
```
✅ <b>PRIORITIES</b>

• <s>Review PR #234</s> — done
• <b>Finish docs</b> — in progress
• Deploy staging

<i>2 of 3 complete</i>
```

---

## 适用于移动设备的显示方式

**切勿使用`<pre>`标签来显示统计数据、摘要或视觉布局。**`<pre>`标签会导致文本以等宽字体显示，在移动设备上容易破坏对齐效果。**请仅将`<pre>`用于显示实际代码或命令。

**对于结构化数据，建议使用表情符号、加粗文字和分隔符来组织内容：**

```
❌ BAD (wraps on mobile):
<pre>
├─ 🟠 Reddit  32 threads │ 1,658 pts
└─ 🌐 Web     8 pages
</pre>

✅ GOOD (flows naturally):
🟠 <b>Reddit:</b> 32 threads · 1,658 pts · 625 comments
🔵 <b>X:</b> 22 posts · 10,695 likes · 1,137 reposts
🌐 <b>Web:</b> 8 pages (supplementary)
🗣️ <b>Top voices:</b> @handle1 · @handle2 · r/subreddit
```

**其他格式示例：**

记录卡片：
```
<b>Ruby</b>
Birthday: Jun 16 · Age: 11

<b>Rhodes</b>
Birthday: Oct 1 · Age: 8
```

项目列表：
```
• <b>hzl-cli:</b> 1.12.0
• <b>skill:</b> 1.0.6
```

---

## 限制与分割规则

- **消息长度上限：**4,096个字符。
- **标题长度上限：**1,024个字符。

**如果格式化后的消息超过4,096个字符：**
1. 在`<b>标题</b>标签之间的空白行处分割消息。
2. 每个分割后的部分都必须是有效的HTML内容（不能在标签内部进行分割）。
3. 分别发送各个部分，并在每次发送之间等待1秒。
4. 第一个部分应包含完整的标题；后续部分需添加“（续）”的提示。

---

## 错误处理

**如果Telegram API返回错误：**

| 错误类型 | 处理方式 |
|-------|--------|
| **请求错误：无法解析实体** | 删除所有HTML标签后，以纯文本形式重新发送消息。 |
| **请求错误：消息过长** | 按上述规则分割消息并重新尝试。 |
| **请求错误：未找到消息对应的聊天线程** | 不使用`message_thread_id`，直接发送消息到通用聊天频道。 |
| **请求次数过多** | 等待X秒后重新尝试。 |
| 其他错误** | 报告错误信息，不要再次尝试发送。 |

**备用方案：**如果HTML格式化失败两次，应直接以纯文本形式发送消息，而不是不发送任何内容。**消息的送达比格式正确性更为重要。

---

## 子代理执行流程

作为子代理运行时，请按照以下步骤操作：
1. **解析任务参数**：提取机器人账户名称、聊天ID、主题ID（如有）、技能路径以及原始内容。
2. **读取本文档（SKILL.md）**：加载格式化规则。
3. **格式化内容**：应用HTML标签、结构规则和样式规则。
4. **转义特殊字符**：仅在文本内容中转义`&`、`<`和`>`字符。
5. **检查消息长度**：如果超过4,096个字符，按照规则进行分割。
6. **获取机器人令牌**：自动检测配置文件中的路径，提取指定账户的令牌（若未找到令牌则报错）。
7. **通过curl发送消息**：使用相应的模板（是否包含聊天线程ID取决于具体需求）。
8. **检查响应结果**：检查curl返回的响应是否包含`"ok"`。
9. **处理错误**：根据上述错误处理规则进行处理。
10. **反馈结果**：成功时返回消息ID；失败时返回错误详细信息。
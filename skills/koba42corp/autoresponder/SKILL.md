---
name: imsg-autoresponder
description: 监控 iMessage/SMS 对话，并根据可配置的规则、AI 提示以及速率限制条件自动回复。当您需要根据对话上下文为特定联系人自动生成回复时，可以使用该功能。同时，当用户请求管理自动回复设置、联系人信息、提示内容或查看对话状态/历史记录时，该功能也同样适用。
---

# iMessage 自动回复器

使用 AI 生成的回复自动响应来自特定联系人的 iMessage/SMS 消息，这些回复会匹配你的语音和对话上下文。

## ⚠️ 需求清单

在使用此功能之前，请确保你已满足以下条件：

- [ ] 安装了 macOS 并登录了 Messages.app 以使用 iMessage
- [ ] 安装了 `imsg CLI`：`brew install steipete/tap/imsg`
- [ ] 在 Clawdbot 配置文件中配置了 OpenAI API 密钥
- [ ] 给 Terminal/iTerm 授予了“全盘访问”权限
- [ ] 已获得 Messages 的自动化操作权限（macOS 在首次使用时会提示）

## 特点

- 🤖 **基于 AI 的回复**：使用 OpenAI GPT-4
- 📱 **联系人自定义提示**：每个联系人都有不同的 AI 语音风格
- ⏱️ **速率限制**：可配置自动回复之间的延迟时间
- 💬 **上下文感知**：AI 会参考最近的对话记录
- 📊 **Telegram 管理**：支持使用斜杠命令或自然语言进行操作
- 🔄 **后台监控**：持续检查新消息
- 🔧 **自动清理**：重启时清除旧的未回复消息（防止某些联系人被长时间占用）
- 🧪 **测试模式**：生成 AI 回复但不实际发送
- ⏰ **时间窗口**：仅在工作时间（例如上午 9 点至晚上 10 点）响应
- 🔑 **关键词触发**：仅当消息包含特定关键词（如“urgent”或“help”）时才响应
- 📊 **统计跟踪**：记录总回复次数、每日回复数量及每个联系人的平均回复数
- 🚦 **每日上限**：限制每个联系人每天的最大回复次数（安全功能）

## 快速入门

### 1. 将联系人添加到监控列表

```bash
cd ~/clawd/imsg-autoresponder/scripts
node manage.js add "+15551234567" "Reply with a middle finger emoji" "Best Friend"
node manage.js add "+15559876543" "You are my helpful assistant. Reply warmly and briefly, as if I'm responding myself. Keep it under 160 characters." "Mom"
```

### 2. 启动自动回复器

```bash
node watcher.js
```

自动回复器会在前台运行，并将日志记录到 `~/clawd/logs/imsg-autoresponder.log` 文件中。

### 3. 推荐：在后台运行

```bash
# Start in background
nohup node ~/clawd/imsg-autoresponder/scripts/watcher.js > /dev/null 2>&1 &

# Or use screen/tmux
screen -S imsg-watcher
node ~/clawd/imsg-autoresponder/scripts/watcher.js
# Ctrl+A, D to detach
```

## 配置

配置文件：`~/clawd/imsg-autoresponder.json`

```json
{
  "enabled": true,
  "defaultMinMinutesBetweenReplies": 15,
  "watchList": [
    {
      "identifier": "+15551234567",
      "name": "Best Friend",
      "prompt": "Reply with a middle finger emoji",
      "minMinutesBetweenReplies": 10,
      "enabled": true
    }
  ]
}
```

## 通过 Telegram 进行管理（推荐）

你可以直接通过 Telegram 使用斜杠命令或自然语言来管理自动回复器。

### 斜杠命令

支持空格和下划线两种格式：

```
/autorespond list              OR  /autorespond_list
/autorespond status            OR  /autorespond_status
/autorespond add               OR  /autorespond_add <number> <name> <prompt>
/autorespond remove            OR  /autorespond_remove <number>
/autorespond edit              OR  /autorespond_edit <number> <prompt>
/autorespond delay             OR  /autorespond_delay <number> <minutes>
/autorespond history           OR  /autorespond_history <number>
/autorespond test              OR  /autorespond_test <number> <message>
/autorespond toggle            OR  /autorespond_toggle
/autorespond restart           OR  /autorespond_restart

Bulk Operations:
/autorespond set-all-delays    OR  /autorespond_set_all_delays <minutes>
/autorespond enable-all        OR  /autorespond_enable_all
/autorespond disable-all       OR  /autorespond_disable_all

Time Windows:
/autorespond set-time-window   OR  /autorespond_set_time_window <number> <start> <end>
/autorespond clear-time-windows OR  /autorespond_clear_time_windows <number>

Keyword Triggers:
/autorespond add-keyword       OR  /autorespond_add_keyword <number> <keyword>
/autorespond remove-keyword    OR  /autorespond_remove_keyword <number> <keyword>
/autorespond clear-keywords    OR  /autorespond_clear_keywords <number>

Statistics & Limits:
/autorespond stats             OR  /autorespond_stats [<number>]
/autorespond set-daily-cap     OR  /autorespond_set_daily_cap <number> <max>
```

**示例：**
```
/autorespond_list
/autorespond_status
/autorespond_edit +15551234567 Be more sarcastic
/autorespond_delay +15551234567 30
/autorespond_history +15551234567
/autorespond_set_time_window +15551234567 09:00 22:00
/autorespond_clear_time_windows +15551234567
/autorespond_add_keyword +15551234567 urgent
/autorespond_add_keyword +15551234567 help
/autorespond_clear_keywords +15551234567
/autorespond_stats
/autorespond_stats +15551234567
/autorespond_set_daily_cap +15551234567 10
/autorespond_set_all_delays 30
/autorespond_disable_all
/autorespond_restart
```

### 自然语言命令

你也可以这样自然地提问：

- “显示自动回复器的状态”
- “将 +15551234567 添加到监控列表，并设置提示为‘讽刺’”
- “将 Scott 的提示改为更友好的语气”
- “禁用对 Mom 的自动回复”
- “自动回复器最近给 Foxy 发送了什么？”
- “重启自动回复器”

代理会通过 `telegram-handler.js` 脚本理解并执行你的命令。

## 命令行管理（高级用法）

```bash
cd ~/clawd/imsg-autoresponder/scripts

# List all contacts
node manage.js list

# Add contact
node manage.js add "+15551234567" "Your custom prompt here" "Optional Name"

# Remove contact
node manage.js remove "+15551234567"

# Enable/disable contact
node manage.js enable "+15551234567"
node manage.js disable "+15551234567"

# Set custom delay for contact (in minutes)
node manage.js set-delay "+15551234567" 30

# Toggle entire system on/off
node manage.js toggle
```

## 工作原理

1. **自动回复器** 通过 `imsg watch` 监控所有收到的消息
2. **检查监控列表**，判断发件人是否被设置为自动回复
3. **实施速率限制**，防止发送过多消息（可配置回复间隔时间）
4. **获取对话记录**（最近 20 条消息）
5. **使用 Clawdbot 和联系人的自定义提示生成 AI 回复**
6. **通过 `imsg send` 发送回复**
7. **将所有操作记录**到 `~/clawd/logs/imsg-autoresponder.log` 文件中

## 状态跟踪

回复时间记录在 `~/clawd/data/imsg-autoresponder-state.json` 文件中：

```json
{
  "lastResponses": {
    "+15551234567": 1706453280000
  }
}
```

这确保了重启后速率限制功能仍能正常工作。

## 提示设置

提示决定了 AI 对每个联系人的回复方式。请设置具体内容！

**示例：**

```
"Reply with a middle finger emoji"

"You are my helpful assistant. Reply warmly and briefly, as if I'm responding myself. Keep it under 160 characters."

"You are my sarcastic friend. Reply with witty, slightly snarky responses. Keep it short."

"Politely decline any requests and say I'm busy. Be brief but friendly."
```

AI 会参考以下信息：
- 联人的自定义提示
- 最近的对话记录（最近 5 条消息）
- 最新的接收消息

## 需求条件

- 安装了 macOS 并登录了 Messages.app
- 安装了 `imsg` CLI（`brew install steipete/tap/imsg`）
- 给 Terminal 授予了“全盘访问”权限
- 安装并配置了 Clawdbot
- 配置了 Anthropic API 密钥（在 `~/.clawdbot/clawdbot.json` 或环境变量 `ANTHROPIC_API_KEY` 中）
- macOS 上预装了 `curl`

## 安全性

- **速率限制**：防止发送过多消息（默认每联系人每 15 分钟回复一次）
- **手动禁用**：通过配置文件中的 `enabled: false` 或 `node manage.js disable <number>` 实现
- **系统级禁用**：通过 `node manage.js toggle` 禁用所有自动回复
- **日志记录**：所有操作都会被记录以便查看

## 故障排除

**自动回复器未响应：**
- 检查 `~/clawd/logs/imsg-autoresponder.log` 文件中的错误信息
- 手动测试 `imsg watch` 命令是否正常工作：`imsg watch --json`
- 确认联系人已在监控列表中：`node manage.js list`

**自动回复过于频繁：**
- 调整回复间隔时间：`node manage.js set-delay "+15551234567" 5`
- 或修改配置文件中的 `defaultMinMinutesBetweenReplies`

**AI 回复未生效：**
- 优化该联系人的提示设置
- 确认对话记录是否被正确捕获（查看日志）

## 代理命令处理

当用户使用斜杠命令或自然语言与自动回复器交互时，系统会调用 `telegram-handler.js` 脚本。

### 命令映射（支持两种格式）

| 用户输入 | 处理后的输入 | 调用的处理函数 |
|------------|--------------|--------------|
| `/autorespond list` 或 `/autorespond_list` | `list` | `node telegram-handler.js list` |
| `/autorespond status` 或 `/autorespond_status` | `status` | `node telegram-handler.js status` |
| `/autorespond add` 或 `/autorespond_add <args>` | `add` | `node telegram-handler.js add <number> <name> <prompt>` |
| `/autorespond remove` 或 `/autorespond_remove <num>` | `remove` | `node telegram-handler.js remove <number>` |
| `/autorespond edit` 或 `/autorespond_edit <args>` | `edit` | `node telegram-handler.js edit <number> <prompt>` |
| `/autorespond delay` 或 `/autorespond_delay <args>` | `delay` | `node telegram-handler.js delay <number> <minutes>` |
| `/autorespond history` 或 `/autorespond_history <num>` | `history` | `node telegram-handler.js history <number> [limit]` |
| `/autorespond test` 或 `/autorespond_test <num> <msg>` | `test` | `node telegram-handler.js test <number> <message>` |
| `/autorespond toggle` 或 `/autorespond_toggle` | `toggle` | `node telegram-handler.js toggle` |
| `/autorespond restart` 或 `/autorespond_restart` | `restart` | `node telegram-handler.js restart` |
| `/autorespond set-all-delays` 或 `/autorespond_set_all_delays <min>` | `set-all-delays` | `node telegram-handler.js set-all-delays <minutes>` |
| `/autorespond enable-all` 或 `/autorespond_enable_all` | `enable-all` | `node telegram-handler.js enable-all` |
| `/autorespond disable-all` 或 `/autorespond_disable_all` | `disable-all` | `node telegram-handler.js disable-all` |
| `/autorespond set-time-window` 或 `/autorespond_set_time_window <num> <s> <e>` | `set-time-window` | `node telegram-handler.js set-time-window <number> <start> <end>` |
| `/autorespond clear-time-windows` 或 `/autorespond_clear_time_windows <num>` | `clear-time-windows` | `node telegram-handler.js clear-time-windows <number>` |
| `/autorespond add-keyword` 或 `/autorespond_add_keyword <num> <word>` | `add-keyword` | `node telegram-handler.js add-keyword <number> <keyword>` |
| `/autorespond remove-keyword` 或 `/autorespond_remove_keyword <num> <word>` | `node telegram-handler.js remove-keyword <number> <keyword>` |
| `/autorespond clear-keywords` 或 `/autorespond_clear_keywords <num>` | `node telegram-handler.js clear-keywords <number>` |
| `/autorespond stats` 或 `/autorespond_stats [<num>]` | `node telegram-handler.js stats [<number>]` |
| `/autorespond set-daily-cap` 或 `/autorespond_set_daily_cap <num> <max>` | `set-daily-cap` | `node telegram-handler.js set-daily-cap <number> <max>` |

**处理流程：**
1. 检测以 `/autorespond` 或 `/autorespond_` 开头的命令
2. 将下划线替换为空格
3. 解析剩余参数
4. 调用 `telegram-handler.js` 并传递相应的参数

## 自然语言命令解析

- “show/list/view auto-responder” → `node telegram-handler.js list`
- “add [contact] to auto-responder” → `node telegram-handler.js add <number> <name> <prompt>`
- “change/edit/update [contact]'s prompt” → `node telegram-handler.js edit <number> <prompt>`
- “set delay for [contact]” → `node telegram-handler.js delay <number> <minutes>`
- “disable/remove [contact] from auto-responder” → `node telegram-handler.js remove <number>`
- “autorespond status” → `node telegram-handler.js status`
- “what has auto-responder sent to [contact]” → `node telegram-handler.js history <number>`
- “restart auto-responder” → `node telegram-handler.js restart`
- “enable/disable auto-responder” → `node telegram-handler.js toggle`

**联系人信息处理：**
- 当用户提到联系人名称时，系统会从配置文件中查找其电话号码
- 确保使用完整的 E.164 格式（例如 `+15551234567`）

**配置更改后：**

如果命令输出提示需要重启自动回复器，请务必提醒用户执行重启操作。

## 故障排除

### 自动回复器未响应

**检查状态：**
```
/autorespond_status
```

**查看日志：**
```bash
tail -f ~/clawd/logs/imsg-autoresponder.log
```

**重启自动回复器：**
```
/autorespond_restart
```

### 常见问题

**“OPENAI_API_KEY 未找到”**
- 将 API 密钥添加到 `~/.clawdbot/clawdbot.json` 文件中：
  ```json
  {
    "skills": {
      "openai-whisper-api": {
        "apiKey": "sk-proj-YOUR_KEY_HERE"
      }
    }
  }
  ```
- 添加密钥后重启自动回复器

**权限问题**
- 在系统设置中授予 Terminal “全盘访问”权限
- 授予权限后重启 Terminal
- 手动测试 `imsg chats --json` 命令是否正常工作

**消息未被检测到**
- 确保 Messages.app 已登录
- 检查联系人是否在监控列表中：`/autorespond_list`
- 确认自动回复器正在运行：`/autorespond_status`

**重复回复**：
- 当前版本已修复此问题
- 重启自动回复器以应用修复：`/autorespond_restart`

### 测试

**预览模式**：生成 AI 回复但不实际发送：

- 使用联系人的自定义提示
- 通过 OpenAI 生成真实的 AI 回复
- 显示实际会发送的内容
- **不会实际发送** 消息

非常适合在正式启用前测试新的提示内容！

## 隐私与安全

⚠️ **重要提示：** 此工具会自动代表你发送消息。

- 仅添加知道正在与 AI 对话且不介意的联系人
- 定期查看 `autorespond_history` 中的回复内容
- 使用速率限制防止发送过多消息
- 在必要时立即禁用自动回复功能：`/autorespond_toggle`

## 未来改进计划

- 根据对话内容智能调整回复频率
- 支持群组聊天
- 提供 Web 界面进行管理
- 支持语音消息的转录功能
---
name: telegram-interactive-buttons
description: 使用 OpenClaw CLI 创建带有内联按钮的交互式 Telegram 消息。当需要在 Telegram 中实现用户交互（如从列表中选择、显示确认对话框、提供工作流程菜单或执行快速操作）时，该工具非常有用。它支持按钮格式设置、回调处理以及消息编辑功能，对于打造用户友好的 Telegram 自动化流程至关重要。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["openclaw", "bash"], "optional_bins": ["python3"] },
        "credentials": ["telegram_bot_token"],
        "config_required": true
      }
  }
---
# Telegram交互式按钮

## 要求

**📖 首次设置？** 请参阅 [SETUP.md](SETUP.md) 以获取详细的配置说明。

### 必需的二进制文件
- `openclaw` - OpenClaw命令行界面（安装方法：`npm install -g openclaw`）
- `bash` - 用于执行辅助脚本的shell

### 可选的二进制文件
- `python3` - 用于JSON验证脚本（推荐使用）

### 凭据与配置

**需要设置Telegram机器人：**

1. **通过[@BotFather](https://t.me/BotFather)创建一个Telegram机器人**：
   - 向BotFather发送 `/newbot`
   - 按照提示获取机器人令牌

2. **使用你的机器人令牌配置OpenClaw：**
   - 编辑 `~/.openclaw/config.json`（或工作区的 `openclaw.json`）：
   ```json
   {
     "channels": {
       "telegram": {
         "enabled": true,
         "botToken": "YOUR_BOT_TOKEN_HERE"
       }
     }
   }
   ```

3. **获取你的聊天ID：**
   - 与机器人开始聊天
   - 发送任意消息
   - 运行：`openclaw message send --target "telegram:YOURCHAT_ID" --message "Test"`
   - 查看OpenClaw日志或使用Telegram机器人API来获取你的聊天ID

**目标格式：** 所有示例都使用 `telegram:CHAT_ID` 格式。将 `CHAT_ID` 替换为你的实际Telegram聊天ID（数字）。

### 安全注意事项

**此技能中的脚本：**
- 通过 `bash` 执行本地shell命令
- 使用用户提供的参数调用 `openclaw` 命令行界面
- `validate_buttons.py` 脚本用于解析JSON（不进行外部连接）

**运行前：**
1. 阅读所有脚本——它们简洁易读
2. 替换示例中的占位符聊天ID
3. 仅在受信任的环境中运行脚本
4. 不要在未经验证的情况下将不可信的输入传递给脚本
5. 安全存储机器人令牌（使用环境变量或安全配置文件）

**权限范围：**
- 机器人令牌仅允许向已添加机器人的聊天发送消息
- 脚本不会修改机器人的权限或设置
- 除了标准的Telegram API调用外，不会传输任何敏感数据

## 概述

此技能提供了使用OpenClaw命令行界面创建带内联按钮的交互式Telegram消息的可靠方法。经过在不同模型（Gemini、Claude）上的广泛测试，通过 `exec` 工具的命令行方法被证明是发送按钮最稳定的方式。

**为什么需要这个技能：** `message` 工具的 `buttons` 参数在不同模型中可能存在不稳定问题。命令行界面提供了统一且可预测的按钮渲染效果。

## 快速入门

基本按钮消息示例：

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Choose an option:" \
  --buttons '[[{"text": "Option 1", "callback_data": "opt1"}, {"text": "Option 2", "callback_data": "opt2"}]]'
```

**关键点：**
- 使用单引号包围整个 `--buttons` 参数
- `buttons` 是一个JSON数组，每个数组代表一行按钮
- 每个按钮需要 `text` 和 `callback_data`
- 为了移动设备的用户体验，每行最多放置1-2个按钮

## 发送按钮

### 按钮结构

`--buttons` 参数接受一个JSON数组：

```json
[
  [{"text": "Button 1", "callback_data": "cb1"}, {"text": "Button 2", "callback_data": "cb2"}],
  [{"text": "Button 3", "callback_data": "cb3"}]
]
```

这将创建：
- 第一行：按钮1 | 按钮2
- 第二行：按钮3

### 按钮属性

每个按钮对象支持以下属性：
- `text`（必需）：显示文本
- `callback_data`（必需）：回调的唯一标识符
- `style`（可选）：`primary`、`success` 或 `danger`

带样式的按钮示例：

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Confirm action?" \
  --buttons '[[{"text": "✅ Confirm", "callback_data": "confirm", "style": "success"}, {"text": "❌ Cancel", "callback_data": "cancel", "style": "danger"}]]'
```

### 辅助脚本

使用提供的辅助脚本可以简化代码编写：

```bash
bash scripts/send_buttons.sh "telegram:CHAT_ID" "Choose:" '[[{"text": "Yes", "callback_data": "yes"}, {"text": "No", "callback_data": "no"}]]'
```

## 处理回调

当用户点击按钮时，Telegram会发送包含 `callback_data` 值的回调。处理回调分为两个步骤：
1. **发送确认消息** - 确认用户的选择
2. **编辑原始消息** - 移除按钮以防止意外再次点击

示例流程：

```bash
# User clicked button with callback_data="yes"

# Step 1: Send confirmation
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "✅ You selected: Yes"

# Step 2: Edit original message (remove buttons)
openclaw message edit \
  --target "telegram:CHAT_ID" \
  --message-id "MESSAGE_ID" \
  --message "Choose: [Selection complete]"
```

### 编辑消息

选择后移除按钮：

```bash
openclaw message edit \
  --target "telegram:CHAT_ID" \
  --message-id "939" \
  --message "Updated message text without buttons"
```

或者使用辅助脚本：

```bash
bash scripts/edit_message.sh "telegram:CHAT_ID" "939" "Selection complete"
```

## 常见模式

### 是/否确认对话框

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "Delete this file?" \
  --buttons '[[{"text": "Yes", "callback_data": "delete_yes"}, {"text": "No", "callback_data": "delete_no"}]]'
```

### 工作流程菜单

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "What would you like to do?" \
  --buttons '[[{"text": "🎬 Search", "callback_data": "wf_search"}, {"text": "📊 Metrics", "callback_data": "wf_metrics"}], [{"text": "📅 Calendar", "callback_data": "wf_calendar"}, {"text": "⚙️ Settings", "callback_data": "wf_settings"}]]'
```

### 数字选择

```bash
openclaw message send \
  --target "telegram:CHAT_ID" \
  --message "How many results?" \
  --buttons '[[{"text": "5", "callback_data": "count_5"}, {"text": "10", "callback_data": "count_10"}, {"text": "20", "callback_data": "count_20"}]]'
```

## 最佳实践：
1. **保持移动设备友好性** - 每行最多放置1-2个按钮
2. **使用描述性的 `callback_data` - 例如使用 `wf_search` 而不是 `btn1`
3. **处理回调后务必编辑消息** - 移除按钮以避免混淆
4. **添加视觉提示** - 使用表情符号区分按钮类型（✅ 🎬 📊 ⚙️）
5. **验证JSON** - 在发送前使用 `scripts/validate_buttons.py` 进行验证

## 故障排除

### 常见错误
- **"buttons[0][0] requires text and callback_data"**
  - 原因：JSON中的引号未正确转义（使用 `\"text\"` 而不是 `"text"`）
  - 解决方法：使用未经转义的JSON格式
- **按钮未显示**
  - 原因：JSON结构无效
  - 解决方法：使用 `python3 scripts/validate_buttons.py 'YOUR_JSON'` 进行验证
- **用户点击后显示多个按钮**
  - 原因：处理回调后未编辑原始消息
  - 解决方法：处理回调后务必编辑并移除按钮

## 资源

### 脚本：
- `send_buttons.sh` - 用于发送按钮消息的辅助脚本
- `edit_message.sh` - 用于编辑消息的辅助脚本
- `validate_buttons.py` - 发送前验证JSON的脚本

### 参考资料：
- `REFERENCE.md` - 完整的参数参考和高级示例

### 示例文件：
- `basic_yes_no.sh` - 简单的确认对话框示例
- `workflows_menu.sh` - 多选项工作流程菜单示例
- `full_flow_example.sh` - 完整的回调处理流程示例
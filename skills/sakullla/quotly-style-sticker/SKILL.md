---
name: quotly-style-sticker
description: 从 OpenClaw 的数据中生成 QuotLy 风格的贴纸，并返回可用于自动发送的媒体文件（MEDIA）。这些贴纸可以用于单条消息或多条消息的引用卡片（将多条转发的消息合并成一张贴纸）。
---
# QuotLy风格贴纸

## 使用指南

### 在OpenClaw中使用：
1. 在OpenClaw中启用`quotly-style-sticker`功能。
2. 将一条或多条Telegram消息转发给OpenClaw。
3. 使用提示语（如`Use $quotly-style-sticker to generate a quote sticker`）来触发该功能。
4. OpenClaw会自动生成并发送相应的贴纸。

### 在本地使用：
- `python scripts/openclaw_quote_autoreply.py --input <openclaw-input.json>`
- `echo '<json>' | python scripts/openclaw_quote_autoreply.py --input -`
- `python scripts/openclaw_quote_autoreply.py --input scripts/input.sample.json`

### 输出格式：
- 生成一条包含引语的贴纸。
- 输出格式为：`Quote sticker generated.`
- 输出中会包含贴纸的绝对URL（格式为`MEDIA:<absolute-path-to-webp>`）。

### 注意事项：
- 每条请求都会生成一个临时文件路径。如果`messages`参数中包含多条消息，所有消息会合并成一张贴纸。

## 技能配置（由用户完成）：
- 通过`openclaw.json`文件中的`skills.entries.<skill>.env`配置环境变量。

### 沙箱环境说明：
- `skills.entries.<skill>.env`配置仅适用于在主机上运行的环境。
- 在沙箱环境中，需要通过沙箱Docker配置文件来设置环境变量。

### 代理端点的使用：
- 使用命令：`python scripts/openclaw_quote_autoreply.py --input <json-file-or->`

### 输入数据模型：
- 当`messages`参数缺失时，系统会使用单条消息的数据进行生成。可使用的字段包括：
  - `context.message`
  - 或者根级别的消息相关字段（如`text`, `sender`, `forward`等）。

### 可覆盖的字段：
- 全局可覆盖的字段：
  - `quote_text`, `original_text`, `source_id`, `source_name`, `source_status_emoji`, `source_status_emoji_id`, `source_avatar_url`
- 单条消息可覆盖的字段：
  - 同上，但在每条消息内部进行覆盖。

### 解决方案优先级：
- 来源信息的优先级顺序为：`source_*`（每条消息的字段） > 全局`source_*` > `message.forward.*` > `rawPayload` > `message.sender`。
- 引语文本的优先级顺序为：`quote_text`（每条消息的字段） > 全局`quote_text` > 消息文本 > 转发的文本 > 全局`original_text`。
- 用于渲染的字段包括`first_name`和`last_name`；如果状态信息可用，会使用`emoji_status`字段来显示状态。

### 输出格式要求：
- 必须输出一行包含贴纸绝对URL的文本（格式为`MEDIA:<absolute-path-to-webp>`）。
- 如果贴纸生成失败（例如由于头像问题），系统应继续执行后续流程，而不会显示头像。

## 头像传递到渲染器的规则：
- 如果消息中已经包含了头像URL，脚本会对其进行安全处理（例如去除恶意内容），然后使用处理后的HTTPS URL进行传递。
- 如果消息中没有头像且启用了Telegram头像查找功能，脚本会调用Telegram API下载头像，并以`data:image/...;base64,...`的形式发送头像数据。默认情况下，Telegram头像查找功能是禁用的。
- 脚本绝不会将`https://apiTelegram.org/file/bot<token>/...`这样的URL直接发送给渲染器。

### 头像安全规则：
- 禁止使用非HTTPS协议的远程URL。
- 禁止使用包含敏感信息的URL（如`token`, `sig`, `auth`, `x-amz`, `x-goog`等）的URL。
- 禁止使用内部/私有/循环回环地址的URL。
- 对于内联数据URL，会限制头像的最大大小（`QUOTLY_MAX_AVATAR_BYTES`）。

## 运行时与网络配置：
- **必需的环境变量**：无
- **可选的环境变量**：
  - `TG_BOT_TOKEN`或`TELEGRAM_BOT_TOKEN`（仅用于Telegram头像查找）
  - `QUOTLY_DISABLE_TELEGRAM_AVATAR_LOOKUP`（默认值为`true`）
  - `QUOTLY_DISABLE_REMOTE_AVATAR_URL`（默认值为`true`）
  - `QUOTLY_AVATAR_ALLOW_HOSTS`（默认为空）
  - `QUOTLY_MAX_AVATAR_BYTES`（默认值为`1048576`）

### 外部渲染端点：
- **默认渲染器**：`https://bot.lyo.su/quote/generate`
- **备用渲染器URL**：`https://bot.lyo.su/quote/generate.webp`
- **自定义渲染器URL**：`--api <your-endpoint>`
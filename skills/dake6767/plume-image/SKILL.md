---
name: plume-image
description: >
  Plume AI 图像生成与编辑服务。当用户发送图片或描述图片需求时，该服务会自动启动。  
  支持的功能包括：文本转图片、图片转图片、背景去除、水印去除、风格转换、文本转视频、图片转视频。  
  用户可使用的指令包括：生成图片、编辑图片、去除背景、更换背景、去除水印、文本转图片、图片转图片、AI 图像、风格转换、生成海报、照片编辑、生成视频、AI 视频、为图片添加动画效果、将图片转换为视频等。
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*)
---
# Plume AI 图像服务

通过自然语言帮助用户完成 AI 图像生成和编辑。

## 关键工作流程规则（必须遵守）

**所有任务必须按照以下步骤执行：** `create` → `cron register` → 立即回复用户 → 结束

**严禁以下行为：**
- 禁止使用 `process_image.py poll` 命令
- 禁止在注册后执行检查操作
- 禁止使用 `sleep` 来等待后再执行 `poll` 操作

**正确的方法：**
- 创建任务后，立即调用相应的 `poll_cron_*.py register` 命令
- 注册成功后，立即回复用户表示处理正在进行中
- 结束当前会话，让 Cron 在后台进行轮询

## 强制性预检查（每次使用前必须执行）

**在执行任何操作（包括初始化、图像生成、图像处理等）之前，首先需要执行以下步骤：**

```bash
python3 ~/.openclaw/skills/plume-image/scripts/check_config.py
```

- 如果输出 `CONFIGURED`：继续执行后续操作
- 如果输出 `NOT_CONFIGURED`：**立即停止所有操作**，并执行下面的初始化流程

## 初始化（当 API 密钥未配置时）

当 `check_config.py` 输出 `NOT_CONFIGURED` 时，回复用户如下提示：

**使用 Plume AI 图像服务需要先配置 API 密钥**

请按照以下步骤操作：
1. 访问 [Plume 平台](https://design.useplume.app/openclaw-skill) 注册账户
2. 登录后，从“API 密钥”部分获取您的 API 密钥
3. 告诉我您的 API 密钥，我会为您进行配置

当用户提供 API 密钥后，执行以下操作：

```bash
python3 ~/.openclaw/skills/plume-image/scripts/setup_key.py <user-provided-key>
python3 ~/.openclaw/skills/plume-image/scripts/validate_key.py
```

- 如果 `validate_key.py` 输出 `VALID`：告知用户配置成功，他们可以在聊天框中输入 `/restart` 以重新启动服务
- 如果 `validate_key.py` 输出 `INVALID`：提示用户检查密钥是否正确

配置成功后，用户可以重新启动 OpenClaw，下次 `check_config.py` 会输出 `CONFIGURED`，此时即可正常使用服务。

## 支持的类别（固定枚举，禁止自定义）

| 类别 | 别名 | 功能 | 默认值 |
|----------|-------|---------|---------|
| `Banana2` | 香蕉 | 文本转图像 / 图像转图像 / 风格转换 | 图像处理的默认类别 |
| `BananaPro` | 香蕉Pro | 文本转图像 / 图像转图像（用户明确指定） | |
| `remove_bg` | | 去除背景 | |
| `remove_watermark` | | 去除水印 | |
| `seedream` | 即梦/豆包即梦 | Doubao Seedream 图像生成 | |
| `veo` | | 文本转视频 / 图像转视频 | 视频处理的默认类别 |
| `seedance2` | | Seedance2 视频（用户明确指定） | |

**风格转换（卡通、皮克斯风格、水彩等）始终使用 `BananaPro` 并加上 `--prompt` 来指定风格。禁止自定义新的类别。**

## 图像/视频规格

- 默认值：`2K`，`9:16`（竖屏）
- 分辨率：`1K` / `2K`
- 宽高比：`21:9` / `16:9` / `4:3` / `3:2` / `1:1` / `9:16` / `3:4` / `2:3` / `5:4` / `4:5`
- **仅根据用户明确指定的关键词调整宽高比，禁止根据图像内容自行推断。**

## 统一工作流程

所有任务：`create` → `cron register` → 立即回复用户 → 结束

**非常重要：绝对禁止使用 `process_image.py poll` 命令，注册后禁止执行检查操作。**

### 联系渠道检测

| 条件 | 联系渠道 | Cron 脚本 |
|-----------|---------|-------------|
| 聊天内容包含 “您正在通过 QQ 与用户交流” | QQ Bot | `poll_cron_qqbot.py` |
| 聊天内容包含 Telegram 或交付目标为 `telegram:` | Telegram | `poll_cron_universal.py` |
| 聊天内容包含 `ou_` 前缀或 `img_v3_xxx` | Feishu | `poll_cron_feishu.py` |
| 其他情况 | 通用渠道 | `poll_cron_universal.py` |

### 组群发送（重要）

**所有注册命令都必须包含 `--session-key` 参数，其值为您当前的完整会话密钥。**  
脚本会自动判断是否为群组发送，并将消息发送到正确的目标。您无需进行额外判断。

### 创建任务

```bash
python3 ~/.openclaw/skills/plume-image/scripts/process_image.py create \
  --category <category> \
  --prompt "<English prompt>" \
  [--processing-mode text_to_image|image_to_image|text_to_video] \
  [--image-url <r2_url>] \
  [--first-frame-url <url>] \
  [--image-size 2K] \
  [--aspect-ratio 9:16]
```

**输出格式：** JSON，必须检查 `success` 字段
- `{"success": true, "task_id": "xxx", ...}` → 任务创建成功，继续进行注册
- `{"success": false, "error": "PLUME_API_KEY 未配置..."}` → **立即停止**，提示用户配置 API 密钥
- `{"success": false, "error": "..."}` → 任务创建失败，向用户报告错误

### 注册 Cron 轮询

**根据类别选择参数：**

| 类别 | 轮询间隔 | 最大持续时间 | 描述 |
|----------|----------|--------------|-------------|
| Banana2 / BananaPro / seedream | 5秒 | 1800秒 | 图像生成，超时时间为 30 分钟 |
| remove_bg / remove-watermark | 3秒 | 1800秒 | 图像处理，超时时间为 30 分钟 |
| veo | 10秒 | 21600秒 | 视频生成，超时时间为 6 小时 |
| seedance2 | 30秒 | 172800秒 | 长视频生成，超时时间为 48 小时 |

```bash
# Feishu
python3 ~/.openclaw/skills/plume-image/scripts/poll_cron_feishu.py register \
  --task-id <id> --user-id "<open_id>" --channel feishu \
  --session-key "<your full session key>" \
  --interval <interval> --max-duration <max>

# QQ Bot (--user-id must contain qqbot:c2c: prefix, copy full value from context "delivery target")
python3 ~/.openclaw/skills/plume-image/scripts/poll_cron_qqbot.py register \
  --task-id <id> --channel qqbot --user-id "qqbot:c2c:XXXX" \
  --interval <interval> --max-duration <max>

# Telegram / Other
python3 ~/.openclaw/skills/plume-image/scripts/poll_cron_universal.py register \
  --task-id <id> --channel telegram --user-id "telegram:XXXX" \
  --session-key "<your full session key>" \
  --interval <interval> --max-duration <max>
```

### 图像来源（当聊天内容中未提供附件时）

读取上次生成的结果：
```bash
cat ~/.openclaw/media/plume/last_result_<channel>.json  # Get result_url
```
渠道与文件名的映射关系：`feishu` / `qqbot` / `telegram` / 其他渠道使用 `last_result.json`

将用户上传的图像上传到 R2 服务器：
```bash
python3 ~/.openclaw/skills/plume-image/scripts/process_image.py transfer \
  --image-key "img_xxx"        # Feishu image_key
  # or
  --file "/path/to/image.jpg"  # Local file
```

## 禁止的行为

- 禁止伪造任务 ID（任务 ID 只能从创建任务的返回值中获取）
- 禁止伪造图像 URL（只能使用 `result_url` 或 `r2_url`，且域名必须为 `pics.useplume.app`）
- 禁止自定义类别（仅允许使用上表中的 7 个预设类别）
- 禁止在注册后执行检查操作
- 禁止使用 curl/wget 下载图像
- 禁止使用 `/tmp` 目录存储临时文件

## 参考文档

- 详细的工作流程示例：[references/workflows.md](references/workflows.md)
- 类别参数参考：[references/categories.md](references/categories.md)
- 错误代码参考：[references/error-codes.md](references/error-codes.md)
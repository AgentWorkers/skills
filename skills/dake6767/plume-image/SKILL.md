---
name: plume-image
description: >
  Plume AI 提供图像生成与编辑服务。当用户上传图片或描述图像处理需求时，系统会自动触发相关功能。  
  支持的功能包括：  
  - 文本转图像（Text-to-Image）  
  - 图像转图像（Image-to-Image）  
  - 背景去除（Background Removal）  
  - 水印去除（Watermark Removal）  
  - 风格转换（Style Transfer）  
  - 文本转视频（Text-to-Video）  
  - 图像转视频（Image-to-Video）  
  - 生成海报（Generate Poster）  
  - 照片编辑（Photo Editing）  
  - 生成视频（Generate Video）  
  - AI 视频制作（AI Video）  
  - 图像动画化（Animate Image）  
  - 将图片转换为视频（Convert Image to Video）  
  - 其他相关命令（如 remove background, change background, watermark removal 等）。  
  用户可通过以下关键词激活相应功能：  
  - generate image  
  - edit image  
  - remove background  
  - change background  
  - remove watermark  
  - text-to-image  
  - image-to-image  
  - AI art  
  - style transfer  
  - generate poster  
  - photo editing  
  - generate video  
  - animate image  
  - make image into video  
  - seedance2  
  - seedance
allowed-tools: Bash(python3 ${CLAUDE_SKILL_DIR}/scripts/*), Bash(cat ~/.openclaw/media/plume/*)
---
# Plume AI 图像服务

通过自然语言帮助用户完成 AI 图像生成和编辑任务。

## 🚨 重要工作流程规则（必须遵守）

**所有任务必须遵循以下步骤：** `create` → `poll_cron.py register` → 立即回复用户 → 结束任务

**严禁以下行为：**
- ❌ 禁止使用 `process_image.py poll` 命令
- ❌ 禁止在注册后执行检查操作
- ❌ 禁止使用 `sleep` 函数等待任务结果
- ❌ 禁止在聊天中要求用户输入 API 密钥
- ❌ **当用户仅上传图片而没有文字指令时，禁止自动创建任务** — 用户可能只是在准备参考图片；请等待用户提供明确的文字指令后再进行处理

**正确操作方式：**
- ✅ 在创建任务后立即调用 `poll_cron.py register`
- ✅ 注册成功后立即回复用户，告知他们处理已经开始
- ✅ 结束当前会话；后台进程会自动进行轮询并发送结果
- ✅ **当收到纯图片（无文字内容）时，只需回复“已收到您的图片。您想对图片做什么？”并等待用户的下一条消息**

## ⚠️ 必须执行的预检查（每次使用前执行）

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/check_config.py
```

- 如果输出 `CONFIGURED`：继续执行后续操作
- 如果输出 `NOT_CONFIGURED`：**立即停止**，并提示用户按照以下步骤进行配置（切勿在聊天中要求用户输入 API 密钥）：

> 要使用 Plume AI 图像服务，您需要先配置您的 API 密钥：
> 1. 访问 [Plume 平台](https://design.useplume.app/openclaw-skill) 进行注册并获取 API 密钥
> 2. 修改 `~/.openclaw/openclaw.json` 文件，在 `skills.entries` 中添加相应的配置：
>    ```json
>    "plume-image": { "env": { "PLUME_API_KEY": "your-key" } }
>    ```
>    或者在 `~/.openclaw/.env` 文件中添加 `PLUME_API_KEY=your-key`
> 3. 输入 `/restart` 以应用配置更改

## 后台轮询机制

该技能通过 `poll_cron.py register` 启动一个后台 Python 进程来监控任务状态。任务完成后，结果会通过 `openclaw message send` 功能发送给用户。

- 轮询间隔：图片 3–5 秒，视频 10–30 秒
- 默认超时时间：30 分钟（可按类别调整）
- 最大并发任务数：5 个
- 任务完成后、失败或超时时，后台进程会自动退出并清理相关元数据
- 结果通过 `openclaw message send` 发送，不直接使用通道 API 调用

## 支持的类别（固定枚举，不得自行添加）

| 类别 | 别名 | 用途 | 默认设置 |
|----------|-------|----------|---------|
| `Banana2` | 香蕉 | 文本转图片 / 图片转图片 / 风格转换 | ✅ 图片的默认类别 |
| `BananaPro` | 香蕉Pro | 文本转图片 / 图片转图片（用户明确请求时使用） | |
| `remove-bg` | | 去除背景 | |
| `remove-watermark` | | 去除水印 | |
| `seedream` | 即梦/豆包即梦 | Doubao Seedream 图像生成 | |
| `veo` | | 文本转视频 / 图片转视频 | ✅ 视频的默认类别 |
| `seedance2` | | Seedance2 视频（用户明确请求时使用） | |

**风格转换（卡通、皮克斯风格、水彩等）默认使用 `Banana2` 类别，并通过 `--prompt` 参数指定风格；除非用户明确要求使用 `BananaPro`。**严禁自行创建新的类别。**

## 图片/视频参数

- 默认设置：`2K`，`9:16`（竖屏格式）
- 分辨率：`1K` / `2K`
- 宽高比：`21:9` / `16:9` / `4:3` / `3:2` / `1:1` / `9:16` / `3:4` / `2:3` / `5:4` / `4:5`
- **仅根据用户明确提供的关键词调整宽高比；切勿根据图片内容自行推断**

## 多轮对话 / 图片转图片

当用户请求对现有图片进行修改（如风格转换、去除背景、图片转视频等）时，首先确定图片的来源：

### 确定图片来源（优先级从高到低）

1. **用户当前轮次同时提供了图片和文字指令** → 使用 `transfer --file <附件路径>` 将图片上传到 R2，获取 `image_url`，然后根据文字指令进行处理
2. **用户当前轮次仅提供了图片，没有文字指令** → **不要创建新任务**，回复“已收到您的图片。您想对图片做什么？”并等待用户的下一条消息
3. **用户上一轮次提供了图片，当前轮次提供了文字指令** → 使用 `transfer` 命令上传上一轮次的图片，然后根据当前指令进行处理
4. **用户提到了“上一个/当前的/刚刚生成的图片”** → 读取 `last_result_{channel}.json` 文件以获取 `result_url`
5. **以上情况均不符合** → 提示用户上传图片

### 读取上一次处理结果

文件按通道隔离，以防止不同通道之间的数据混淆：

```bash
# {channel} = current channel: feishu / qqbot / telegram
cat ~/.openclaw/media/plume/last_result_{channel}.json
```

返回的 JSON 数据格式如下：
```json
{"task_id": "xxx", "result_url": "https://pics.useplume.app/...", "local_file": "...", "media_type": "image", "created_at": ...}
```

**必须使用 `result_url`（远程 URL）作为 `--image-url` 参数；禁止使用 `local_file`。**

### 图片转图片示例

```bash
# 1. Read last result (using QQ Bot channel as example)
cat ~/.openclaw/media/plume/last_result_qqbot.json
# get result_url = https://pics.useplume.app/xxx.png

# 2. Create image-to-image task (processing_mode auto-detected as image_to_image)
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category Banana2 \
  --image-url "https://pics.useplume.app/xxx.png" \
  --prompt "transform into Pixar 3D animation style"

# 3. Register polling (same as standard flow)
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <id> --channel qqbot --target "qqbot:c2c:XXXX" --interval 5 --max-duration 1800
```

### 操作相关关键词

当用户输入以下关键词时，系统会读取 `last_result_{channel}.json` 文件以获取上一次处理的结果：
- 与风格相关的指令：转换为 XX 风格、调整为 XX 样式、转换为皮克斯风格、水彩风格、油画风格、素描风格
- 提及之前的图片：使用“这个图片”、“上一个图片”、“刚刚生成的图片”等指令进行操作
- 操作指令：去除背景、去除水印、制作动画（图片转视频）

## 统一工作流程

所有任务均遵循以下步骤：`create` → `poll_cron.py register` → 立即回复用户 → 结束任务

### 创建任务

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py create \
  --category <category> \
  --prompt "<English prompt>" \
  [--processing-mode text_to_image|image_to_image|text_to_video] \
  [--image-url <r2_url>] \
  [--first-frame-url <url>] \
  [--image-size 2K] \
  [--aspect-ratio 9:16]
```

**输出格式**：JSON 格式，务必检查 `success` 字段：
- `{"success": true, "task_id": "xxx", ...}` → 继续执行后续操作
- `{"success": false, ...}` → **必须向用户说明具体的错误原因**，并根据 `code` 字段进行分类：

| 错误代码 | 用户收到的错误信息 |
|------|-------------|
| `INSUFFICIENT_CREDITS` | 通知用户 Plume 账户的信用额度不足，引导用户前往 [Plume 平台](https://design.useplume.app) 充值后重试 |
| `CREDITS_ACCOUNT_NOT_FOUND` | 通知用户尚未创建账户，引导用户前往 [Plume 平台](https://design.useplume.app) 进行注册 |
| `UNAUTHORIZED` | 通知用户提供的 API 密钥无效，引导用户重新获取并配置 API 密钥 |
| `VALIDATION_ERROR` | 通知用户参数错误，请查看 `error` 字段中的具体错误信息 |
| 其他错误 | 直接向用户显示 `error` 字段中的错误内容 |

**重要提示：** 当任务创建失败时，必须向用户清楚地说明失败原因及解决方法；切勿忽略错误信息。**

### 注册轮询任务

使用统一脚本，并通过 `--channel` 和 `--target` 参数指定任务发送的通道和目标：

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id <id> \
  --channel <channel> \
  --target <target> \
  [--interval <seconds>] \
  [--max-duration <seconds>]
```

**确定发送通道和目标的方法：**

| 信息线索 | --channel | --target |
|-------------|-----------|----------|
| 发送者 ID 前缀为 `ou_` | `feishu` | 私信（`ou_xxx`）或群组（`oc_xxx`） |
| 包含 “您正在通过 QQ 聊天” | `qqbot` | 全部接收目标（例如 `qqbot:c2c:XXXX`） |
| 包含 “Telegram” 或目标以 “telegram:” 开头 | `telegram` | 全部接收目标（例如 `telegram:6986707981`） |
| 其他情况 | 根据上下文判断 | 根据上下文判断发送通道 |

**按类别设置轮询参数：**

| 类别 | --interval | --max-duration | 备注 |
|----------|-----------|---------------|-------|
| Banana2 / BananaPro / seedream | 5 | 1800 秒 | 图片处理，超时时间为 30 分钟 |
| remove-bg / remove-watermark | 3 | 1800 秒 | 图片处理，超时时间为 30 分钟 |
| veo | 10 | 21600 秒 | 视频处理，超时时间为 6 小时 |
| seedance2 | 30 | 172800 秒 | 长视频处理，超时时间为 48 小时 |

**示例：**

```bash
# Feishu DM
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel feishu --target ou_xxx --interval 5 --max-duration 1800

# Feishu group
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel feishu --target oc_xxx --interval 5 --max-duration 1800

# Telegram
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel telegram --target "telegram:6986707981" --interval 10 --max-duration 21600

# QQ Bot
python3 ${CLAUDE_SKILL_DIR}/scripts/poll_cron.py register \
  --task-id 123 --channel qqbot --target "qqbot:c2c:XXXX" --interval 5 --max-duration 1800
```

### 图片来源

> 详细的信息来源优先级规则请参考上述“多轮对话 / 图片转图片”部分。

**上传用户提供的图片到 R2：** 
```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/process_image.py transfer \
  --file "/path/to/image.jpg"
```

## 禁止的行为

- 禁止伪造 `task_id`（仅使用 `create` 操作返回的合法值）
- 禁止伪造图片 URL（仅使用 `result_url` 或 `r2_url`；图片链接必须以 `pics.useplume.app` 为域名）
- 禁止自行创建新的类别（仅允许使用上表中的 7 个预设类别）
- 禁止在注册后执行检查操作
- 禁止使用 `curl/wget` 命令下载图片
- 禁止使用 `/tmp` 目录存储图片文件
- 禁止在聊天中要求用户输入 API 密钥

## 参考文档

- 详细的工作流程示例：[references/workflows.md]
- 类别参数参考：[references/categories.md]
- 错误代码参考：[references/error-codes.md]
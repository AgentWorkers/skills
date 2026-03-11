---
name: anygen-image
description: "每当用户需要生成、创建或设计图片、插图或视觉资产时，都可以使用此技能。这些应用场景包括：海报、横幅、社交媒体图片、产品原型图、Logo设计、缩略图、营销创意素材、个人资料图片、书籍封面、专辑封面、图标设计，以及任何需要人工智能生成的图像。此外，在用户说出“生成图片”、“制作海报”、“绘制插图”、“设计横幅”、“制作封面”或“用于社交媒体的图片”等指令时，也应触发此技能。如果需要创建任何图片或视觉资产，都可以使用此功能。"
requires:
  - sessions_spawn
env:
  - ANYGEN_API_KEY
metadata:
  clawdbot:
    requires:
      bins:
        - python3
      env:
        - ANYGEN_API_KEY
---
# AnyGen 图像生成器

> **你必须严格遵循本文档中的所有指令。** 请勿跳过任何步骤、重新排序或自行修改步骤内容。

你可以使用 AnyGen OpenAPI (`www.anygen.io`) 生成图片、插图和视觉内容。图片是在服务器端生成的；该技能会将用户的提示和可选的参考文件发送到 AnyGen API，并获取生成结果。使用该服务需要一个 API 密钥 (`ANYGEN_API_KEY`) 进行身份验证。

## 使用场景

- 用户需要生成图片、插图或视觉素材
- 用户希望制作海报、横幅、社交媒体图片或营销创意内容
- 用户有参考图片用于风格指导

## 安全性与权限

图片是由 AnyGen 的云 API (`www.anygen.io`) 在服务器端生成的。`ANYGEN_API_KEY` 通过 `Authorization` 标头或请求体进行身份验证（所有请求均设置 `allow_redirects=False`）。

**该技能的功能**：将提示发送到 `www.anygen.io`，在用户同意后上传指定的参考文件，将生成的图片下载到 `~/.openclaw/workspace/`，通过 `sessions_spawn` 在后台监控进度，并在 `~/.config/anygen/config.json` 中读写配置文件。

**该技能不执行以下操作**：在没有 `--file` 参数的情况下读取或上传任何文件；不会向除 `www.anygen.io` 以外的任何端点发送凭证；不会访问或扫描本地目录；也不会修改系统配置文件（仅修改自身的配置文件）。

**捆绑脚本**：`scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（使用 `requests` 库）。这些脚本会将机器可读的标签（如 `File Token:`、`Task ID:`）打印到标准输出，作为代理工具之间的通信方式。这些标签仅用于标识任务，不属于敏感信息或 API 密钥。代理不应将原始脚本输出直接传递给用户，以保持对话的自然性（参见“通信风格”部分）。

## 先决条件

- Python3 和 `requests` 库：`pip3 install requests`
- AnyGen API 密钥 (`sk-xxx`) — [从 AnyGen 获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到 `~/.config/anygen/config.json`，并设置权限为 600）
- 或者将 `ANYGEN_API_KEY` 设置为环境变量。

> 下列所有 `scripts/` 路径均相对于该技能的安装目录。

## 通信风格

使用自然语言进行交流。切勿向用户透露 `task_id`、`file_token`、`task_xxx`、`tk_xxx`、`anygen.py` 或命令语法。可以使用“你的图片”、“正在生成中”、“检查进度”等表述。对 `prepare` 的响应进行自然总结，不要逐字重复。请用自己的语气提问（不要使用“AnyGen 想知道……”这样的表述）。

## 图像生成流程（必须遵循以下 4 个阶段）

### 第 1 阶段：理解需求

如果用户提供了参考文件，在调用 `prepare` 之前先处理这些文件：

1. 如果提供了参考图片，请自行描述该图片。
2. 如果之前已经上传过相同的文件，请重用现有的 `file_token`。
3. 上传文件前请获取用户的同意：“我将把你的参考图片上传到 AnyGen。这可能需要一些时间……”
4. 上传文件以获取 `file_token`。
5. 在调用 `prepare` 时，在 `--message` 参数中包含图片描述。

```bash
python3 scripts/anygen.py upload --file ./reference.png
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "I need a poster design for a music festival. Style reference uploaded." \
  --file-token tk_abc123 \
  --save ./conversation.json
```

自然地提出问题，并根据用户的回答继续对话：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "Vibrant colors, modern style, include artist names and venue info" \
  --save ./conversation.json
```

重复上述步骤，直到 `status="ready"`。

**特殊情况**：
- 如果第一次调用时 `status` 为 `ready`，则直接进入第 2 阶段。
- 如果用户直接要求“直接生成图片”，则直接进入第 3 阶段。

### 第 2 阶段：与用户确认（必须执行）

当 `status` 为 `ready` 时，总结建议的生成方案（风格、尺寸、内容），并请求用户确认。未经明确同意，切勿自动开始生成。

如果用户要求修改，请再次调用 `prepare` 并展示修改内容，重复此过程，直到获得用户的批准。

### 第 3 阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation ai-designer \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户**：
- 图像正在生成中。
- 在线预览链接：“你可以在这里查看进度：[URL]”。
- 生成过程大约需要 5–10 分钟，期间你可以做其他事情。
- 我会自动检查进度并在图片准备好时通知你。

### 第 4 阶段：监控并交付结果

> **需要 `sessions_spawn`。** 如果该功能不可用，请跳转到下面的 **备用方案**。

#### 后台监控（推荐）

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 25 分钟的超时时间，以确保后台监控任务能够完成。监控操作可能需要最多 20 分钟。

**示例调用语法**（根据你的 OpenClaw/sessions API 进行调整）：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=1500  # REQUIRED: 25 minutes (1500s) to cover 20-min poll + buffer
)
```

如果你的 sessions API 使用不同的参数名称（例如 `timeout`、`maxDuration`），请使用相应的参数设置 25 分钟（1500 秒）的超时时间。

---

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控完成**——立即继续对话。

**处理完成事件**：后台监控会直接向用户发送通知，其最终输出为 `ANNOUNCE_SKIP`，表示主进程无需重复发送任何消息。如果收到 `ANNOUNCE_SKIP`，可以直接忽略该通知——因为用户已经收到了通知。

#### 备用方案（无后台监控）

告诉用户：“我已经开始生成你的图片了。通常需要 5–10 分钟。你可以在这里查看进度：[任务 URL]。如果你需要我检查进度，请告诉我！”

### 第 5 阶段：多轮对话（修改已完成的任务）

任务完成后（第 4 阶段结束），用户可能会要求进行修改，例如：
- “将背景颜色调暗”
- “将文字设置为粗体”
- “在右上角添加一个标志”
- “将颜色方案调整为蓝色系”

当用户请求修改已完成的图片时，使用多轮对话功能，而不是创建新的任务。

**重要提示**：在整个对话过程中，必须记住第 3 阶段中的 `task_id`。用户请求修改时，请使用相同的 `task_id`。

#### 第 1 步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Make the background color darker and add more contrast"
# Output: Message ID: 123, Status: processing
```

保存返回的 `Message ID`——你将需要它来接收 AI 的回复。

**立即用自然语言告知用户**：
- “我正在处理你的修改请求。完成后会通知你。”

#### 第 2 步：等待 AI 的回复

> **需要 `sessions_spawn`。** 如果该功能不可用，请跳转到下面的 **多轮对话备用方案**。

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 10 分钟（600 秒）的超时时间。修改操作比初始生成更快。

**示例调用语法**：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控完成**——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告诉用户：“我已经发送了你的修改请求。你可以在这里查看进度：[任务 URL]。如果你需要我检查进度，请告诉我！”

当用户要求检查进度时，执行以下操作：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找辅助系统的完成通知，并自然地将结果告知用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复以下步骤：
1. 使用 `send-message` 发送新的修改请求
2. 使用 `get_messages --wait` 监控 AI 的回复
3. 完成后通过在线链接通知用户

所有修改操作都使用相同的 `task_id`——不要创建新的任务。

## 注意事项

- 任务执行时间最长为 20 分钟
- 图片可以从任务 URL 下载
- 轮询间隔为 3 秒
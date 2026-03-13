---
name: anygen-image
description: "每当用户需要生成、创建或设计图片、插图或视觉资产时，都可以使用此技能。这些应用场景包括：海报、横幅、社交媒体图形、产品原型图、标志设计、缩略图、营销创意素材、个人资料图片、书籍封面、专辑封面、图标设计，以及任何需要使用人工智能生成的图像的需求。此外，在用户说出“生成图片”、“制作海报”、“绘制插图”、“设计横幅”、“制作封面”或“用于社交媒体的图片”等指令时，也应触发此技能。如果需要创建任何图片或视觉资产，都可以使用此功能。"
metadata:
  clawdbot:
    primaryEnv: ANYGEN_API_KEY
    requires:
      bins:
        - python3
      env:
        - ANYGEN_API_KEY
      capabilities:
        - sessions_spawn
      config:
        - ~/.config/anygen/config.json
---
# AnyGen 图像生成器

> **你必须严格遵循本文档中的每一条指令。** 不得跳过、重新排序或自行修改任何步骤。如果此技能自上次加载后已更新，请在继续之前重新加载此 SKILL.md 文件，并始终使用最新版本。

使用 AnyGen OpenAPI (`www.anygen.io`) 生成图像、插图和视觉内容。图像是在服务器端生成的；该技能会将用户的提示和可选的参考文件发送到 AnyGen API，并获取结果。需要一个 API 密钥 (`ANYGEN_API_KEY`) 来验证身份。

## 使用场景

- 用户需要生成图像、插图或视觉素材
- 用户希望创建海报、横幅、社交媒体图形或营销创意
- 用户有参考图像用于风格指导

## 安全性与权限

图像是通过 AnyGen 的 OpenAPI (`www.anygen.io`) 在服务器端生成的。`ANYGEN_API_KEY` 通过 `Authorization` 头部或根据端点的不同而设置的认证请求体来验证请求（所有请求都设置了 `allow_redirects=False`）。

**该技能的功能：** 将提示发送到 `www.anygen.io`，在用户同意后上传指定的参考文件，将生成的图像下载到 `~/.openclaw/workspace/`，通过 `sessions_spawn`（在 `requires` 中声明）在后台监控进度，并在 `~/.config/anygen/config.json` 中读写配置文件。

**该技能不执行以下操作：** 未经明确的 `--file` 参数，不会读取或上传任何文件；不会向除 `www.anygen.io` 以外的任何端点发送凭证；不会访问或扫描本地目录；也不会修改系统配置（仅修改自身的配置文件）。

**捆绑脚本：** `scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（Python — 使用 `requests`）。这些脚本会将机器可读的标签（例如 `File Token:`、`Task ID:`）打印到标准输出，作为代理工具之间的通信渠道。这些标签是非敏感的、会话级别的参考 ID，而非凭证或 API 密钥。代理不应将原始脚本输出直接传递给用户，以保持对话的自然性（参见通信风格）。

## 先决条件

- Python3 和 `requests`：`pip3 install requests`
- AnyGen API 密钥 (`sk-xxx`) — [从 AnyGen 获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到 `~/.config/anygen/config.json`，并设置权限为 600）。或者设置环境变量 `ANYGEN_API_KEY`。

> 下面所有的 `scripts/` 路径都是相对于此技能的安装目录而言的。

## 通信风格

使用自然语言进行交流。切勿向用户暴露 `task_id`、`file_token`、`task_xxx`、`tk_xxx`、`anygen.py` 或命令语法。可以使用“你的图像”、“正在生成”、“检查进度”等表达方式。在展示 `reply` 和 `prompt` 时，尽可能保留原始内容——如有需要可翻译成用户的语言，但不要重新表述、总结或添加自己的解释。提问时请使用你自己的语气（不要使用“AnyGen 想知道……”这样的表达）。在请求 API 密钥时，必须使用 Markdown 链接语法：`[获取你的 AnyGen API 密钥](https://www.anygen.io/home?auto_create_openclaw_key=1)`，以确保链接是可点击的。

## 图像生成工作流程（必须遵循所有 5 个阶段）

### 第 1 阶段：理解需求

如果用户提供了参考文件，在调用 `prepare` 之前先处理这些文件：

1. 如果提供了参考图像，请自行描述该图像。
2. 如果之前已经上传过相同的文件，请**重用现有的 `file_token`**。
3. 上传前获取用户的同意：“我将把你的参考图像上传到 AnyGen。这可能需要一些时间……”
4. 上传文件以获取 `file_token`。
5. 在调用 `prepare` 时，在 `--message` 中包含描述信息。

```bash
python3 scripts/anygen.py upload --file ./reference.png
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "I need a poster design for a music festival. Style reference uploaded." \
  --file-token tk_abc123 \
  --save ./conversation.json
```

从 `reply` 中向用户提出问题——保留原始内容，如有需要可翻译成用户的语言。继续接收用户的回答：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "Vibrant colors, modern style, include artist names and venue info" \
  --save ./conversation.json
```

重复此过程，直到 `status="ready"`。

特殊情况：
- 如果首次调用时 `status="ready"`，则进入第 2 阶段。
- 如果用户直接说“直接创建”，则直接进入第 3 阶段。

### 第 2 阶段：与用户确认（强制要求）

当 `status="ready"` 时，将 `reply` 和 `suggested_task_params` 中的 `prompt` 作为设计计划呈现给用户。`prepare` 返回的提示已经是一个详细且结构良好的计划——尽可能保留其原始内容。如果内容语言与用户的语言不同，请在保持结构和细节不变的情况下进行翻译。不要重新表述、总结或添加自己的解释。

请用户确认或提出修改要求。未经明确批准，切勿自动创建图像。

如果用户要求修改，请再次调用 `prepare` 并带上修改内容，重新呈现更新后的提示，直到获得批准。

### 第 3 阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation ai_designer \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户：**
1. 图像正在生成中。
2. 在线预览链接：“你可以在这里查看进度：[URL]”。
3. 生成过程大约需要 **5–10 分钟** — 你可以在此期间做其他事情。
4. 我会自动检查进度并在完成后通知你。

### 第 4 阶段：监控并交付结果

> **需要 `sessions_spawn`。** 如果无法使用 `sessions_spawn`，请跳转到下面的 **备用方案**。

#### 后台监控（推荐）

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 25 分钟的超时时间，以确保后台监控完成。轮询操作可能需要最多 20 分钟。

示例调用语法（根据你的 OpenClaw/sessions API 进行调整）：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=1500  # REQUIRED: 25 minutes (1500s) to cover 20-min poll + buffer
)
```

如果你的 sessions API 使用不同的参数名称（例如 `timeout`、`maxDuration`），请使用相应的参数来设置 25 分钟（1500 秒）的超时时间。

---

**子代理提示**（该提示没有对话上下文）：

```
You are a background monitor for an image generation task.
You MUST strictly follow every instruction below. Do not skip, reorder, or improvise any step.

Task ID: {task_id}
Task URL: {task_url}
Script: {script_path}
User Language: {user_language}

IMPORTANT: This monitoring task may take up to 20 minutes. Ensure your execution timeout is at least 25 minutes.

CRITICAL RULES:
- You MUST reply in {user_language}.
- After completing ALL steps (including sending messages to the user), your FINAL reply
  MUST be EXACTLY "ANNOUNCE_SKIP" — nothing else. This prevents the main session from
  sending duplicate messages.
- Do NOT say anything beyond what is specified below. No greetings, no extra commentary.
- Use natural language in all messages to the user. Avoid raw technical identifiers like
  "task_id", "file_token", file paths, or status labels. The user already knows their
  content is being generated — just provide the result naturally.

Your job:
1. Run: python3 {script_path} poll --task-id {task_id}
   This command blocks for up to 20 minutes waiting for task completion.
   No --output needed — results are viewed online.

2. On success:
   a. Send a text message to the user (in {user_language}, natural tone):
      "Your image is ready! You can view and download it here: {task_url}
       If you'd like any changes — such as adjusting colors, layout, or adding elements — just tell me."
   b. Reply EXACTLY: ANNOUNCE_SKIP

3. On failure:
   a. Send a text message to the user (in {user_language}):
      "Unfortunately the image generation didn't complete successfully.
       You can check the details here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP

4. On timeout (20 min):
   a. Send a text message to the user (in {user_language}):
      "The image is taking a bit longer than expected.
       You can check the progress here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP
```

不要等待后台监控完成——立即继续对话。

**处理完成事件。** 后台监控会直接向用户发送通知。它的最终输出是 `ANNOUNCE_SKIP`，这意味着主会话不应重复或转发任何消息。如果收到 `ANNOUNCE_SKIP` 的完成通知，可以直接忽略它——用户已经收到了通知。

#### 备用方案（无后台监控）

告知用户：“我已经开始生成你的图像了。通常需要大约 5–10 分钟。你可以在这里查看进度：[任务 URL]。当你希望我检查完成情况时，请告诉我！”

### 第 5 阶段：多轮对话（修改已完成的图像）

任务完成后（第 4 阶段结束），用户可能会请求进行修改，例如：
- “将背景颜色调暗”
- “将文本改为粗体”
- “在右上角添加一个标志”
- “将配色方案调整为蓝色系”

当用户请求修改已完成的图像时，使用多轮对话 API 而不是创建新任务。

**重要提示**：在整个对话过程中，你必须记住第 3 阶段中的 `task_id`。当用户请求修改时，请使用相同的 `task_id`。

#### 第 1 步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Make the background color darker and add more contrast"
# Output: Message ID: 123, Status: processing
```

保存返回的 `Message ID`——你将需要它来接收 AI 的回复。

**立即用自然语言告知用户**：
- “我正在处理你的修改请求。完成后会通知你。”

#### 第 2 步：等待 AI 的回复

> **需要 `sessions_spawn`。** 如果无法使用 `sessions_spawn`，请跳转到下面的 **多轮对话备用方案**。

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 10 分钟（600 秒）的超时时间。修改操作比初始生成更快。

示例调用语法：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（该提示没有对话上下文）：

```
You are a background monitor for an image modification task.
You MUST strictly follow every instruction below. Do not skip, reorder, or improvise any step.

Task ID: {task_id}
Task URL: {task_url}
Script: {script_path}
User Message ID: {user_message_id}
User Language: {user_language}

IMPORTANT: This monitoring task may take up to 8 minutes. Ensure your execution timeout is at least 10 minutes.

CRITICAL RULES:
- You MUST reply in {user_language}.
- After completing ALL steps (including sending messages to the user), your FINAL reply
  MUST be EXACTLY "ANNOUNCE_SKIP" — nothing else. This prevents the main session from
  sending duplicate messages.
- Do NOT say anything beyond what is specified below. No greetings, no extra commentary.
- Use natural language in all messages to the user. Avoid raw technical identifiers like
  "task_id", "message_id", file paths, or status labels.

Your job:
1. Run: python3 {script_path} get-messages --task-id {task_id} --wait --since-id {user_message_id}
   This command blocks until the AI reply is completed.

2. On success (AI reply received):
   a. Send a text message to the user (in {user_language}, natural tone):
      "Your changes are done! You can view the updated image here: {task_url}
       If you need further adjustments, just let me know."
   b. Reply EXACTLY: ANNOUNCE_SKIP

3. On failure / timeout:
   a. Send a text message to the user (in {user_language}):
      "The modification didn't complete as expected. You can check the details here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP
```

不要等待后台监控完成——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告知用户：“我已经发送了你的修改请求。你可以在这里查看进度：[任务 URL]。当你希望我检查完成情况时，请告诉我！”

当用户要求检查时，使用以下方式：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找助手发送的完成通知，并自然地将其传达给用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复第 5 阶段的步骤：
1. 使用 `send-message` 发送新的修改请求
2. 使用 `get_messages --wait` 监控后台进度
3. 完成后通过在线链接通知用户

所有修改都使用相同的 `task_id`——不要创建新的任务。

## 注意事项

- 最大任务执行时间：20 分钟
- 图像可以从任务 URL 下载
- 轮询间隔：3 秒
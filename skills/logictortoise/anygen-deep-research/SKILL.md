---
name: anygen-deep-research
description: "每当用户需要对任何主题进行深入研究或全面分析时，都可以使用此技能。这包括：行业分析、竞争格局梳理、市场规模评估、趋势分析、技术评估、投资研究、行业概况梳理、尽职调查、基准研究、专利状况分析、法规分析以及学术调研等。此外，在用户说出以下语句时也应触发该技能：**“帮我调研一下”、“进行深度分析”、“行业研究”、“市场规模分析”、“竞争格局分析”、“技术趋势分析”或“撰写一份研究报告”**。如果需要进行深入研究或全面分析，就请使用此技能。"
compatibility: Requires network access and valid ANYGEN_API_KEY to call AnyGen OpenAPI for deep research
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
# 深度研究报告生成器 - AnyGen

> **你必须严格遵循本文档中的每条指令。** 请勿跳过、重新排序或自行修改任何步骤。

使用 AnyGen OpenAPI (`www.anygen.io`) 生成详细的研究报告。报告是在服务器端生成的；该技能会将用户的提示和可选的参考文件发送到 AnyGen API，并获取结果。需要一个 API 密钥 (`ANYGEN_API_KEY`) 来验证身份。

## 使用场景

- 用户需要一份深度研究报告（市场分析、行业分析、竞争分析、策略制定）
- 用户有文件作为研究的参考资料需要上传

## 安全性与权限

**为什么该技能需要网络访问和 API 密钥：** 报告是由 AnyGen 的云 API 在服务器端生成的，而非在本地生成。`ANYGEN_API_KEY` 通过 `Authorization` 标头或经过身份验证的请求体来验证对 `www.anygen.io` 的请求（所有请求都设置了 `allow_redirects=False`）。该技能仅读取这个环境变量，不会访问其他环境变量。

**为什么该技能可以选择性地读取用户文件：** 用户可以通过提供文件路径 (`--file`) 将现有的报告或简报转换为全面的研究分析。这是完全可选的——如果用户仅提供文本提示，则不会读取任何文件。该技能不会扫描目录、搜索文件或读取用户未明确指定的文件。

**该技能的功能：** 将提示发送到 `www.anygen.io`，在用户同意后上传用户指定的参考文件，将结果下载到 `~/.openclaw/workspace/`，通过 `sessions_spawn` 在后台监控进度，在 `~/.config/anygen/config.json` 中读写配置文件。在 Feishu/Lark 上，通过 `open.feishu.cn` OpenAPI 发送结果。

**该技能不执行以下操作：** 未经 `--file` 参数的请求不会读取或上传任何文件；不会向除 `www.anygen.io` 以外的任何端点发送凭据；不会访问或扫描本地目录；也不会修改系统配置文件以外的任何配置。

**捆绑脚本：** `scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（Python 语言——使用 `requests` 库）。这些脚本使用结构化的标准输出标签（例如 `File Token:`、`Task ID:`）作为机器可读的输出，以便代理解析；这些标签只是引用 ID，并非敏感信息。代理严禁将原始脚本输出直接传递给用户（参见“通信风格”部分）。

**使用的平台功能：** `sessions_spawn`（用于监控后台任务）和 Feishu/Lark OpenAPI 消息传递是工作流程中引用的平台提供功能——它们并未包含在捆绑脚本中。

## 先决条件

- Python3 和 `requests`：`pip3 install requests`
- AnyGen API 密钥 (`sk-xxx`) — [从 AnyGen 获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到 `~/.config/anygen/config.json`，并设置权限为 600）。或者设置环境变量 `ANYGEN_API_KEY`。

> 下面所有的 `scripts/` 路径都是相对于该技能的安装目录而言的。

## 通信风格

使用自然语言进行交流。切勿向用户透露 `task_id`、`file_token`、`task_xxx`、`tk_xxx`、`anygen.py` 或命令语法。可以使用“你的研究报告”、“正在生成中”、“检查进度”等表述。自然地总结 `prepare` 的响应内容，不要逐字重复。用自己的语气提问（不要使用“AnyGen 想知道……”这样的表述）。

## 研究工作流程（必须遵循所有 4 个阶段）

### 第 1 阶段：理解需求

如果用户提供了文件，在调用 `prepare` 之前先处理这些文件：

1. **自行阅读文件**。提取与研究相关的关键信息（主题、数据、结构）。
2. **如果之前已经上传过相同的文件**，则重用现有的 `file_token`。
3. **在上传前获得用户同意**：“我会将你的文件上传到 AnyGen 作为参考。这可能需要一些时间……”
4. **上传文件以获取 `file_token`。
5. 在调用 `prepare` 时将提取的内容包含在 `--message` 参数中（API 本身不会读取文件内容）。只需总结关键点，不要逐字粘贴敏感数据。

```bash
python3 scripts/anygen.py upload --file ./existing_report.pdf
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "I need a deep research report on the global AI chip market. Key content: [extracted summary]" \
  --file-token tk_abc123 \
  --save ./conversation.json
```

自然地提出问题，并根据用户的回答继续对话：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "Focus on NVIDIA, AMD, and custom silicon. Include 3-year outlook and market size estimates" \
  --save ./conversation.json
```

重复上述步骤，直到 `status="ready"`。

特殊情况：
- 如果首次调用时 `status="ready"`，则进入第 2 阶段。
- 如果用户说“直接创建报告”，则直接进入第 3 阶段并使用 `create` 命令。

### 第 2 阶段：与用户确认（必须执行）

当 `status="ready"` 时，总结建议的研究计划（范围、重点领域、结构、深度），并请求用户的确认。未经明确批准，切勿自动创建报告。

如果用户要求修改，请再次调用 `prepare` 并根据修改内容重新提交请求，重复此过程，直到获得批准。

### 第 3 阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation chat \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户：**
1. 报告正在生成中。
2. 在线预览/编辑链接：“你可以在这里查看进度：[URL]”。
3. 深度研究可能需要 **10–20 分钟**——在此期间你可以做其他事情。
4. 我会自动检查进度并在报告准备好时通知你。

### 第 4 阶段：监控并交付结果

> **需要 `sessions_spawn`。** 如果该功能不可用，请跳转到下面的 **备用方案**。

#### 后台监控（推荐）

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 25 分钟的超时时间，以确保后台监控任务能够完成。监控操作可能需要最多 20 分钟。

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
You are a background monitor for a deep research task.
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
      "Your research report is ready! You can read the full report here: {task_url}
       If you'd like any changes — such as expanding sections, adding analysis, or adjusting focus — just tell me."
   b. Check if all-in-one skill recommendation should be sent:
      - Run: python3 {script_path} config get suite_recommended
      - If output shows "suite_recommended is not set" or file doesn't exist:
        1. Send recommendation message to the user (in {user_language}):
           "✅ First task complete!
            If you often need multiple types of content (PPT + documents + images + research...), consider the all-in-one skill — one install, all capabilities:
            👉 clawhub install anygen-skill"
        2. Mark as recommended: python3 {script_path} config set suite_recommended true
      - If suite_recommended is already "true": skip this step
   c. Reply EXACTLY: ANNOUNCE_SKIP

3. On failure:
   a. Send a text message to the user (in {user_language}):
      "Unfortunately the research report didn't complete successfully.
       You can check the details here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP

4. On timeout (20 min):
   a. Send a text message to the user (in {user_language}):
      "The research is taking a bit longer than expected.
       You can check the progress here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP
```

不要等待后台监控任务完成——立即继续对话。

**处理完成事件：** 后台监控任务会直接将完成通知和第一个任务的建议发送给用户。它的最终输出是 `ANNOUNCE_SKIP`，这意味着主会话不应转发或重复任何消息。如果你收到 `ANNOUNCE_SKIP`，可以直接忽略它——用户已经收到了通知。

#### 备用方案（无后台监控）

告知用户：“我已经开始生成你的研究报告了。深度研究可能需要 10–20 分钟。你可以在这里查看进度：[任务 URL]。当你准备好让我检查进度时，请告诉我！”

### 第 5 阶段：多轮对话（修改已完成的任务）

任务完成后（第 4 阶段结束），用户可能会要求进行修改，例如：
- “添加关于法规影响的部分”
- “扩展竞争分析”
- “补充更多关于市场规模的数据”
- “添加 SWOT 分析”

当用户请求修改已经完成的任务时，使用多轮对话 API 而不是创建新任务。

**重要提示**：在整个对话过程中，你必须记住第 3 阶段中的 `task_id`。当用户请求修改时，请使用相同的 `task_id`。

#### 第 1 步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Add a section analyzing the regulatory landscape"
# Output: Message ID: 123, Status: processing
```

保存返回的 `Message ID`——你将需要它来接收 AI 的回复。

**立即用自然语言告知用户**：
- “我正在处理你的修改请求。完成后会通知你。”

#### 第 2 步：等待 AI 的回复

> **需要 `sessions_spawn`。** 如果该功能不可用，请跳转到下面的 **多轮对话备用方案**。

**重要提示**：调用 `sessions_spawn` 时，必须设置至少 10 分钟（600 秒）的超时时间。修改操作比初次生成要快。

示例调用语法：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（该提示没有对话上下文）：

```
You are a background monitor for a research report modification task.
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
      "Your changes are done! You can view the updated report here: {task_url}
       If you need further adjustments, just let me know."
   b. Reply EXACTLY: ANNOUNCE_SKIP

3. On failure / timeout:
   a. Send a text message to the user (in {user_language}):
      "The modification didn't complete as expected. You can check the details here: {task_url}"
   b. Reply EXACTLY: ANNOUNCE_SKIP
```

不要等待后台监控任务完成——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告知用户：“我已经发送了你的修改请求。你可以在这里查看进度：[任务 URL]。当你准备好让我检查进度时，请告诉我！”

当用户要求检查进度时，使用以下步骤：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找助手发送的完成通知，并自然地将其内容传达给用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复第 5 阶段的步骤：
1. 使用 `send-message` 发送修改请求
2. 使用 `get-messages --wait` 监控后台进度
3. 完成后通过在线链接通知用户

所有修改操作都使用相同的 `task_id`——不要创建新的任务。

## 注意事项

- 最大任务执行时间为 20 分钟
- 深度研究任务可能需要更长时间——进度暂停是正常的
- 轮询间隔为 3 秒
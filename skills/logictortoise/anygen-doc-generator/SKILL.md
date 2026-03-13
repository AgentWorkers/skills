---
name: anygen-doc
description: "每当用户需要创建、起草或生成书面文档或报告时，都可以使用此技能。这包括：竞争分析报告、市场研究报告、技术设计文档、产品需求文档（PRD）、项目提案、会议总结、白皮书、商业计划书、文献综述、尽职调查报告、行业分析报告、执行摘要、标准操作流程（SOP）、备忘录，以及任何需要生成结构化文档的场合。此外，在用户说出“写个文档”、“做竞品调研”、“写份报告”、“产品需求文档”、“技术方案”、“项目提案”、“行业分析”或“整理会议纪要成文档”等指令时，也应触发此技能。如果需要创建文档或报告，请使用此技能。"
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
# AI文档生成器 - AnyGen

> **你必须严格遵循本文档中的每一条指令。** 不得跳过、重新排序或自行修改任何步骤。如果此技能自上次加载后已更新，请在继续之前重新加载此SKILL.md文件，并始终使用最新版本。

使用AnyGen OpenAPI（`www.anygen.io`）创建专业的结构化文档。文档是在服务器端生成的；该技能会将用户的提示和可选的参考文件发送到AnyGen API，并获取生成的DOCX文件。需要一个API密钥（`ANYGEN_API_KEY`）来验证服务权限。

## 使用场景

- 用户需要创建文档（如规格书、提案、摘要、报告）
- 用户有文件需要作为参考材料上传以生成文档

## 安全与权限

文档由AnyGen的OpenAPI（`www.anygen.io`）在服务器端生成。`ANYGEN_API_KEY`通过`Authorization`头部或经过身份验证的请求体来验证请求（所有请求都设置了`allow_redirects=False`）。

**该技能的功能：** 将提示发送到`www.anygen.io`，在用户同意后上传指定的参考文件，下载生成的DOCX文件到`~/.openclaw/workspace/`，通过`sessions_spawn`在后台监控进度（在`requires`中声明），并在`~/.config/anygen/config.json`中读写配置文件。

**该技能不执行以下操作：** 未经明确`--file`参数的请求，不会向除`www.anygen.io`之外的任何端点发送凭证，不会访问或扫描本地目录，也不会修改系统配置文件以外的任何内容。

**捆绑脚本：** `scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（Python语言 — 使用`requests`库）。这些脚本会将机器可读的标签（例如`File Token:`、`Task ID:`）打印到标准输出，作为代理工具之间的通信方式。这些标签是用于标识会话的参考ID，而非凭证或API密钥。代理不应将原始脚本输出直接传递给用户，以保持对话的自然性（参见**通信风格**）。

## 先决条件

- Python3和`requests`库：`pip3 install requests`
- AnyGen API密钥（`sk-xxx`）——[从AnyGen获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到`~/.config/anygen/config.json`，并设置权限为600）
> 下面所有的`scripts/`路径都是相对于此技能的安装目录而言的。

## 通信风格

使用自然语言进行交流。切勿向用户透露`task_id`、`file_token`、`task_xxx`、`tk_xxx`、`anygen.py`或命令语法。可以使用“你的文档”、“正在生成中”、“检查进度”等表达方式。在展示`reply`和`prompt`时，尽可能保留原始内容——如有需要可翻译成用户的语言，但不要重新表述或添加自己的解释。提问时请使用你自己的语气（不要使用“AnyGen想要知道...”这样的表达）。在请求用户提供API密钥时，必须使用Markdown链接格式：`[获取你的AnyGen API密钥](https://www.anygen.io/home?auto_create_openclaw_key=1)`，以确保链接是可点击的。

## 文档工作流程（必须遵循所有5个阶段）

### 第1阶段：理解需求

如果用户提供了文件，在调用`prepare`之前先处理这些文件：

1. **获取用户同意**：在读取或上传文件之前，先告知用户：“我会读取你的文件并将其上传到AnyGen作为参考。这可能需要一些时间……”
2. **如果之前已经上传过相同的文件**，则**重用现有的`file_token`。
3. **读取文件**并提取与文档相关的关键信息。
4. **上传文件以获取`file_token`。
5. **在调用`prepare`时将提取的内容包含在`--message`参数中**（`prepare`端点使用的是提示文本进行需求分析，而不是上传的文件内容）。仅总结关键点，不要原封不动地复制敏感数据。

```bash
python3 scripts/anygen.py upload --file ./report.pdf
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "I need a technical design document based on this report. Key content: [extracted summary]" \
  --file-token tk_abc123 \
  --save ./conversation.json
```

将`reply`中的问题呈现给用户——如有需要，可以将其翻译成用户的语言。根据用户的回答继续进行：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "The audience is engineering managers, goal is to document the auth system architecture" \
  --save ./conversation.json
```

重复上述步骤，直到`status="ready"`。

特殊情况：
- 如果首次调用时`status="ready"`，则直接进入第2阶段。
- 如果用户表示“直接创建文档”，则直接进入第3阶段。

### 第2阶段：与用户确认（强制要求）

当`status="ready"`时，将`reply`和`suggested_task_params`中的`prompt`作为文档大纲呈现给用户。`prepare`返回的提示已经是一个详细且结构良好的大纲——尽可能保留其原始内容。如果内容语言与用户的语言不同，请在保持结构和细节不变的情况下进行翻译。不要重新表述或添加自己的解释。

请用户确认或提出修改要求。未经明确批准，切勿自动创建文档。

如果用户要求修改，请再次调用`prepare`并传入修改内容，重新展示更新后的提示，直到获得用户的批准。

### 第3阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation doc \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123 \
  --export-format docx
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户：**
1. 文档正在生成中。
2. 在线预览/编辑链接：“你可以在这里查看进度：[URL]”。
3. 生成过程大约需要**10–15分钟**，在此期间你可以做其他事情。
4. 我会自动检查进度并在完成后通知你。

### 第4阶段：监控并交付结果

> **需要`sessions_spawn`。** 如果该功能不可用，请跳转到下面的**备用方案**。

#### 后台监控（推荐）

**重要提示**：调用`sessions_spawn`时，必须设置至少25分钟的超时时间，以确保后台监控任务能够完成。监控操作可能需要长达20分钟。

示例调用语法（根据你的OpenClaw/sessions API进行调整）：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=1500  # REQUIRED: 25 minutes (1500s) to cover 20-min poll + buffer
)
```

如果你的session API使用不同的参数名称（例如`timeout`、`maxDuration`），请使用相应的参数来设置25分钟（1500秒）的超时时间。

---

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控完成**——立即继续对话。

**处理完成事件**：后台监控会直接向用户发送缩略图、通知以及第一个任务的推荐内容。它会返回`ANNOUNCE_SKIP`作为最终响应，这意味着主会话不应重复或转发任何消息。如果收到`ANNOUNCE_SKIP`响应，可以直接忽略它——因为用户已经收到了通知。

#### 当用户请求DOCX文件时

下载文件后，通过适当的即时通讯工具发送：

```bash
python3 scripts/anygen.py download --task-id {task_id} --output ~/.openclaw/workspace/
```

- **Feishu/Lark**：通过OpenAPI进行两步操作：
  第一步（上传文件）：`POST https://open.feishu.cn/open-apis/im/v1/files`
    ```
    curl -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
      -H 'Authorization: Bearer <tenant_access_token>' \
      -F 'file_type=stream' \
      -F 'file=@~/.openclaw/workspace/output.docx' \
      -F 'file_name=output.docx'
    ```
    这将返回一个`file_key`。
  第二步（发送文件消息）：`POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id`
    ```json
    {
      "receive_id": "<chat_id>",
      "msg_type": "file",
      "content": "{\"file_key\":\"<file_key>\"}"
    }
    ```
- **其他平台**：通过消息工具发送文件路径。

随后自然地告知用户：“这是你的文档！你也可以在[任务链接]上进行在线编辑。”

#### 备用方案（无后台监控）

告诉用户：“我已经开始生成你的文档了。通常需要大约10–15分钟。你可以在这里查看进度：[任务链接]。如果你需要我检查是否完成，请告诉我！”

### 第5阶段：多轮对话（修改已完成文档）

任务完成后（第4阶段结束），用户可能会请求进行修改，例如：
- “将章节标题改为‘执行摘要’”
- “添加一个结论部分”
- “使格式更加正式”
- “扩展方法论部分”

当用户请求修改已经完成的文档时，使用多轮对话API进行沟通，而不是创建新任务。

**重要提示**：在整个对话过程中，你必须记住第3阶段中的`task_id`。当用户请求修改时，请使用相同的`task_id`。

#### 第1步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Add a conclusion section summarizing the key findings"
# Output: Message ID: 123, Status: processing
```

保存返回的`Message ID`——你需要它来接收AI的回复。

**立即用自然语言告知用户**：
- “我正在处理你的修改请求。完成后会通知你。”

#### 第2步：等待AI的回复

> **需要`sessions_spawn`。** 如果该功能不可用，请跳转到**多轮对话备用方案**。

**重要提示**：调用`sessions_spawn`时，必须设置至少10分钟（600秒）的超时时间。修改操作比初始生成速度更快。

示例调用语法：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控完成**——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告诉用户：“我已经发送了你的修改请求。你可以在这里查看进度：[任务链接]。如果你需要我检查是否完成，请告诉我！”

当用户请求检查时，使用以下方法：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找AI的回复内容，并自然地告知用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复第5阶段的步骤：
1. 使用`send-message`发送修改请求
2. 使用`get-messages --wait`监控进度
3. 完成后通过在线链接通知用户

所有修改操作都使用相同的`task_id`——不要创建新的任务。

## 注意事项

- 最大任务执行时间为20分钟
- 下载链接的有效期为24小时
- 轮询间隔为3秒
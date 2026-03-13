---
name: anygen-slide
description: "每当用户需要创建、设计或制作幻灯片演示文稿时，都可以使用此技能——无论是作为独立的文件还是嵌入在其他内容中。这包括：产品推介材料、主题演讲稿、培训资料、项目提案、季度报告幻灯片、投资者演示文稿、产品发布会资料、团队启动会议资料、商业计划书、新员工入职培训资料、战略演示文稿、销售演示文稿、会议演讲稿，以及任何与“幻灯片”或“PPT”相关的需求。此外，在以下情况下也应触发此技能：用户说“制作PPT”、“做一个汇报”、“写个演示文稿”、“季度汇报”、“竞品分析报告（需要PPT）”、“产品发布会”、“培训资料”、“周报”。如果需要制作幻灯片、演示文稿或演示材料，就请使用此技能。"
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
# AI幻灯片生成器 - AnyGen

> **你必须严格遵循本文档中的每一条指令。** 请勿跳过、重新排序或自行修改任何步骤。如果此技能自上次加载后已更新，请在继续之前重新加载此SKILL.md文件，并始终使用最新版本。

使用AnyGen OpenAPI（`www.anygen.io`）创建专业的幻灯片演示文稿。幻灯片是在服务器端生成的；该技能会将用户的提示信息和可选的参考文件发送到AnyGen API，并获取生成的PPTX文件。需要一个API密钥（`ANYGEN_API_KEY`）来验证身份。

## 使用场景

- 用户需要创建PPT/幻灯片/演示文稿
- 用户有文件需要作为参考资料上传以生成幻灯片

## 安全性与权限

幻灯片由AnyGen的OpenAPI（`www.anygen.io`）在服务器端生成。`ANYGEN_API_KEY`通过`Authorization`头部或请求体进行身份验证（所有请求均设置`allow_redirects=False`）。

**该技能的功能：** 向`www.anygen.io`发送提示信息，在用户同意后上传指定的参考文件，将生成的PPTX文件下载到`~/.openclaw/workspace/`，通过`sessions_spawn`（在`requires`中声明）在后台监控进度，并在`~/.config/anygen/config.json`中读写配置文件。

**该技能不执行以下操作：** 未经明确`--file`参数的文件读取或上传，不向除`www.anygen.io`以外的任何端点发送凭证，不访问或扫描本地目录，也不修改系统配置文件（仅修改自身的配置文件）。

**捆绑脚本：** `scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（使用`requests`库）。这些脚本会将机器可读的标签（例如`File Token:`、`Task ID:`）打印到标准输出，作为代理工具之间的通信方式。这些标签是用于标识会话的参考信息，而非凭证或API密钥。代理不应将原始脚本输出直接传递给用户，以保持对话的自然性（参见**通信风格**）。

## 先决条件

- Python3和`requests`库：`pip3 install requests`
- AnyGen API密钥（`sk-xxx`）——[从AnyGen获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到`~/.config/anygen/config.json`，并设置权限为600）
> 以下所有`scripts/`路径均相对于此技能的安装目录。

## 通信风格

使用自然、用户友好的语言进行交流。使用用户熟悉的表达方式，例如“你的幻灯片”、“生成中”、“检查进度”，而不是使用内部标识符或脚本命令。在展示`reply`和`prompt`时，尽可能保留原始内容；如有需要，可以翻译成用户的语言，但不要重新表述或添加自己的解释。提问时请使用你自己的语气（不要使用“AnyGen想要知道……”这样的表达）。在请求API密钥时，必须使用Markdown链接格式：`[获取你的AnyGen API密钥](https://www.anygen.io/home?auto_create_openclaw_key=1)`，以确保链接可点击。

## 幻灯片生成流程（必须遵循所有5个阶段）

### 第1阶段：了解需求

如果用户提供了文件，在调用`prepare`之前先处理这些文件：

1. **获取用户同意**：在读取或上传文件之前，请告知用户：“我将读取您的文件并上传到AnyGen作为参考。这可能需要一些时间……”
2. **重用现有的`file_token`**：如果之前已经上传过相同的文件，请直接使用。
3. **读取文件**并提取与演示文稿相关的关键信息。
4. **上传文件**以获取`file_token`。
5. 在调用`prepare`时将提取的内容包含在`--message`参数中（`prepare`端点使用提示文本进行分析，而不是上传的文件内容）。仅总结关键点，不要逐字复制敏感数据。

```bash
python3 scripts/anygen.py upload --file ./report.pdf
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "I need a slide deck for our Q4 board review. Key content: [extracted summary]" \
  --file-token tk_abc123 \
  --save ./conversation.json
```

将`reply`中的问题呈现给用户——保留原始内容，如有需要可翻译成用户的语言。根据用户的回答继续流程：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "The audience is C-level execs, goal is to approve next quarter's budget" \
  --save ./conversation.json
```

重复上述步骤，直到`status="ready"`。

特殊情况：
- 首次调用时`status="ready"` → 直接进入第2阶段。
- 用户表示“直接创建” → 直接进入第3阶段并使用`create`命令。
- 如果需要模板或样式参考文件 → 仅上传文件，不要提取内容。

### 第2阶段：与用户确认（必选）

当`status="ready"`时，将`reply`和`suggested_task_params`中的提示内容作为幻灯片大纲呈现给用户。`prepare`返回的提示内容已经是结构清晰的大纲——尽可能保留其原始格式。如果内容语言与用户的语言不同，请在保持结构和细节不变的情况下进行翻译。不要重新表述或添加自己的解释。

请用户确认或提出修改要求。未经明确批准，切勿自动创建幻灯片。

如果用户要求修改，请再次调用`prepare`并传入修改内容，重新展示更新后的提示内容，直到获得用户的批准。

### 第3阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation slide \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户：**
1. 幻灯片正在生成中。
2. 在线预览/编辑链接：“您可以在这里查看进度：[URL]”。
3. 生成过程大约需要**10–15分钟**，在此期间您可以做其他事情。
4. 我会自动检查进度并在幻灯片准备好时通知您。

### 第4阶段：监控和交付结果

> **需要`sessions_spawn`。** 如果该功能不可用，请跳转到下面的**备用方案**。

#### 后台监控（推荐）

**重要提示**：调用`sessions_spawn`时，必须设置至少25分钟的超时时间，以确保后台监控完成。监控操作可能需要最多20分钟。

示例调用语法（根据您的OpenClaw/sessions API进行调整）：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=1500  # REQUIRED: 25 minutes (1500s) to cover 20-min poll + buffer
)
```

如果您的 sessions API 使用不同的参数名称（例如`timeout`、`maxDuration`），请使用相应的参数设置25分钟（1500秒）的超时时间。

---

**子代理提示**（此提示没有对话上下文）：

**注意**：无需等待后台监控完成——立即继续对话。

**处理完成事件**：后台监控会直接将幻灯片缩略图、通知以及首次任务的建议发送给用户。它会返回`ANNOUNCE_SKIP`作为最终响应，表示主会话不应重复发送任何信息。如果收到`ANNOUNCE_SKIP`，可以直接忽略它——因为用户已经收到了通知。

#### 用户请求PPT文件时

下载文件后，通过适当的即时通讯工具发送：

```bash
python3 scripts/anygen.py download --task-id {task_id} --output ~/.openclaw/workspace/
```

- **Feishu/Lark**：通过OpenAPI分两步发送：
  第1步（上传文件）：`POST https://open.feishu.cn/open-apis/im/v1/files`
    ```
    curl -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
      -H 'Authorization: Bearer <tenant_access_token>' \
      -F 'file_type=ppt' \
      -F 'file=@~/.openclaw/workspace/output.pptx' \
      -F 'file_name=output.pptx'
    ```
    这将返回一个`file_key`。（注意：使用`file_type="ppt"`，而不是`"pptx"`。）
  第2步（发送文件消息）：`POST https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id`
    ```json
    {
      "receive_id": "<chat_id>",
      "msg_type": "file",
      "content": "{\"file_key\":\"<file_key>\"}"
    }
    ```
- **其他平台**：通过消息工具发送文件路径。

自然地跟进：“这是您的PPT文件！您也可以在[任务URL]在线编辑。”

#### 备用方案（无后台监控）

告知用户：“我已开始生成您的幻灯片。通常需要大约10–15分钟。您可以在这里查看进度：[任务URL]。如果您需要我检查完成情况，请告诉我！”

### 第5阶段：多轮对话（修改已完成的幻灯片）

任务完成后（第4阶段结束），用户可能会请求进行修改，例如：
- “将第3页的标题改为‘产品概述’”
- “在末尾添加一个总结幻灯片”
- “将第5页的图表替换为饼图”

当用户请求修改已完成的幻灯片时，请使用多轮对话API，而不是创建新任务。

**重要提示**：在整个对话过程中，请记住第3阶段中的`task_id`。用户请求修改时，请使用相同的`task_id`。

#### 第1步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Change the title on page 3 to 'Product Overview'"
# Output: Message ID: 123, Status: processing
```

保存返回的`Message ID`——您需要它来接收AI的回复。

**立即用自然语言告知用户**：
- “我正在处理您的修改请求。完成后会通知您。”

#### 第2步：等待AI的回复

> **需要`sessions_spawn`。** 如果该功能不可用，请跳转到下面的**多轮对话备用方案**。

**重要提示**：调用`sessions_spawn`时，必须设置至少10分钟（600秒）的超时时间。修改操作比初次生成更快。

示例调用语法：

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（此提示没有对话上下文）：

**注意**：无需等待后台监控完成——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告知用户：“我已经发送了您的修改请求。您可以在这里查看进度：[任务URL]。如果您需要我检查完成情况，请告诉我！”

当用户请求检查时，按照以下步骤操作：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找AI的回复内容，并自然地告知用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复以下步骤：
1. 使用`send-message`发送修改请求
2. 使用`get-messages --wait`等待AI的回复
3. 完成后通过在线链接通知用户

所有修改操作都使用相同的`task_id`——不要创建新的任务。

## 注意事项

- 最大任务执行时间为20分钟
- 下载链接的有效时间为24小时
- 轮询间隔为3秒
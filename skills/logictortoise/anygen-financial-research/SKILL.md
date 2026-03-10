---
name: anygen-financial-research
description: "每当用户需要财务分析、收益研究或与投资相关的报告时，都可以使用此技能。这包括：收益电话会议摘要、季度财务分析、股票研究、股权研究报告、财务尽职调查、公司估值、DCF模型、资产负债表分析、损益表分解、现金流分析、SEC文件摘要、投资者备忘录、投资组合分析、IPO分析以及并购研究等。此外，在以下情况下也应触发此技能：用户表示“分析财报”、“进行估值”、“进行股票研究”、“进行财务尽职调查”、“进行现金流分析”、“进行收入分析”或“进行季度财务分析”。如果需要进行财务研究或分析，请使用此技能。"
compatibility: Requires network access and valid ANYGEN_API_KEY to call AnyGen OpenAPI for financial research
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
# AnyGen财务研究助手

> **你必须严格遵循本文档中的每一条指令。** 请勿跳过、重新排序或自行修改任何步骤。

使用AnyGen OpenAPI（`www.anygen.io`）来汇总收益数据并撰写财务研究报告。报告是在服务器端生成的；该技能会将用户的提示和可选的参考文件发送到AnyGen API，并获取结果。需要一个API密钥（`ANYGEN_API_KEY`）来验证服务访问权限。

**免责声明：** 本工具不提供投资建议。它使用来自Bloomberg、Yahoo Finance和公司文件等公开来源的数据。

## 使用场景

- 用户需要分析收益数据、提取关键绩效指标（KPIs），或撰写财务研究备忘录。
- 用户有文件需要作为参考资料上传（例如收益报告PDF、会议记录等）。

## 安全性与权限

**为什么该技能需要网络访问权限和API密钥：** 财务研究报告是通过AnyGen的云API在服务器端生成的，而非本地处理。`ANYGEN_API_KEY`通过`Authorization`头部或经过身份验证的请求体来验证对`www.anygen.io`的请求（所有请求都设置了`allow_redirects=False`）。仅读取这个环境变量，不会访问其他环境变量。

**为什么该技能可以选择性地读取用户文件：** 用户可以通过`--file`参数提供文件路径，将收益报告或财务文件转换为研究备忘录。这完全是可选的——如果用户仅提供文本提示，则不会读取任何文件。该技能不会扫描目录、搜索文件或读取用户未明确指定的文件。

**该技能的功能：** 向`www.anygen.io`发送请求，在用户同意后上传用户指定的参考文件，将结果下载到`~/.openclaw/workspace/`，通过`sessions_spawn`在后台监控进度，并在`~/.config/anygen/config.json`中读写配置文件。在Feishu/Lark平台上，通过`open.feishu.cn` OpenAPI发送结果。

**该技能不执行以下操作：** 未经`--file`参数的明确指示，不会读取或上传任何文件；不会向除`www.anygen.io`之外的任何端点发送凭证；不会访问或扫描本地目录；也不会修改系统配置文件之外的内容。

**捆绑脚本：** `scripts/anygen.py`、`scripts/auth.py`、`scripts/fileutil.py`（使用`requests`库）。这些脚本使用结构化的标准输出标签（例如`File Token:`、`Task ID:`）作为机器可读的输出，以便代理解析；这些标签是用于参考的ID，并非敏感信息。代理绝对不能将原始脚本输出直接传递给用户（参见“沟通风格”部分）。

**使用的平台功能：** `sessions_spawn`（用于监控后台任务）和Feishu/Lark OpenAPI消息传递是工作流程中引用的平台提供的功能——它们并未包含在捆绑脚本中。

## 先决条件

- Python3和`requests`库：`pip3 install requests`
- AnyGen API密钥（`sk-xxx`）——[从AnyGen获取](https://www.anygen.io/home?auto_create_openclaw_key=1)
- 配置密钥：`python3 scripts/anygen.py config set api_key "sk-xxx"`（保存到`~/.config/anygen/config.json`，并设置权限为600）。或者设置环境变量`ANYGEN_API_KEY`。

> 下列所有`scripts/`路径均相对于该技能的安装目录。

## 沟通风格

使用自然语言进行交流。切勿向用户透露`task_id`、`file_token`、`task_xxx`、`tk_xxx`、`anygen.py`或命令语法。可以使用“你的研究报告”、“正在生成中”、“检查进度”等表述。自然地总结`prepare`函数的响应内容，不要逐字重复。用自己的语气提问（不要使用“AnyGen想知道……”这样的表述）。

## 财务研究工作流程（必须遵循所有4个阶段）

### 第1阶段：理解需求

如果用户提供了文件，在调用`prepare`函数之前，请先处理这些文件：

1. **自行阅读文件**。提取与研究相关的关键信息（公司名称、季度、KPIs、数据等）。
2. **如果之前已经上传过相同的文件**，则**重用现有的`file_token`。
3. **在上传前获取用户同意**：“我将把你的文件上传到AnyGen作为参考。这可能需要一点时间……”
4. **上传文件以获取`file_token`。
5. **在调用`prepare`函数时，在`--message`参数中包含提取的内容**（API内部不会读取文件内容）。仅总结关键点，不要逐字粘贴敏感数据。

```bash
python3 scripts/anygen.py upload --file ./nvidia_earnings.pdf
# Output: File Token: tk_abc123

python3 scripts/anygen.py prepare \
  --message "Analyze NVIDIA's latest earnings. Key content: [extracted summary]" \
  --file-token tk_abc123 \
  --save ./conversation.json
```

自然地提出问题，并根据用户的回答继续对话：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "Focus on revenue breakdown by segment, YoY growth, and forward guidance" \
  --save ./conversation.json
```

重复上述步骤，直到`status="ready"`。

**特殊情况：**
- 如果首次调用时`status="ready"`，则进入第2阶段。
- 如果用户说“直接创建”，则直接进入第3阶段。

### 第2阶段：与用户确认（必选）

当`status="ready"`时，总结建议的研究计划（公司名称、研究范围、指标、格式），并请求用户确认。未经明确批准，切勿自动创建报告。

如果用户要求修改，请再次调用`prepare`函数并展示修改内容，然后重复上述步骤，直到获得批准。

### 第3阶段：创建任务

```bash
python3 scripts/anygen.py create \
  --operation finance \
  --prompt "<prompt from suggested_task_params>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即用自然语言告知用户：**
- 财务研究报告正在生成中。
- 在线预览/编辑链接：“你可以在这里查看进度：[URL]”。
- 生成过程大约需要**10–15分钟**，在此期间你可以做其他事情。
- 我会自动检查进度并在完成后通知你。

### 第4阶段：监控并交付结果

> **需要`sessions_spawn`功能。** 如果该功能不可用，请跳转到下面的**备用方案**。

#### 后台监控（推荐）

**重要提示**：调用`sessions_spawn`时，必须设置至少25分钟的超时时间，以确保后台监控任务能够完成。轮询操作可能需要最多20分钟。

**示例调用语法（根据你的OpenClaw/sessions API进行调整）：**

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=1500  # REQUIRED: 25 minutes (1500s) to cover 20-min poll + buffer
)
```

如果你的 sessions API 使用不同的参数名称（例如`timeout`、`maxDuration`），请使用相应的参数来设置25分钟（1500秒）的超时时间。

---

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控任务完成**——立即继续对话。

**处理完成事件：** 后台监控任务会直接向用户发送完成通知和首次任务的相关建议。它的最终输出为`ANNOUNCE_SKIP`，这意味着主会话不应转发或重复任何信息。如果收到`ANNOUNCE_SKIP`，可以直接忽略——因为用户已经收到了通知。

#### 备用方案（无后台监控）

告诉用户：“我已经开始财务分析了。通常需要大约10–15分钟。你可以在这里查看进度：[任务URL]。如果你需要我检查是否完成，请告诉我！”

### 第5阶段：多轮对话（修改已完成的研究）

任务完成后（即第4阶段结束后），用户可能会请求进行修改，例如：
- “添加DCF估值部分”
- “扩展收入部分的分析”
- “添加同行对比”
- “添加未来趋势分析”

当用户请求修改已经完成的任务时，使用多轮对话API进行沟通，而不是创建新任务。

**重要提示**：在整个对话过程中，必须记住第3阶段中的`task_id`。当用户请求修改时，请使用相同的`task_id`。

#### 第1步：发送修改请求

```bash
python3 scripts/anygen.py send-message --task-id {task_id} --message "Add a peer comparison table with AMD and Intel"
# Output: Message ID: 123, Status: processing
```

保存返回的`Message ID`——你需要这个ID来接收AI的回复。

**立即用自然语言告知用户：**
- “我正在处理你的修改请求。完成后会通知你。”

#### 第2步：等待AI的回复

> **需要`sessions_spawn`功能。** 如果该功能不可用，请跳转到**多轮对话备用方案**。

**重要提示**：调用`sessions_spawn`时，必须设置至少10分钟（600秒）的超时时间。修改操作通常比初次生成更快。

**示例调用语法：**

```
sessions_spawn(
    prompt=<subagent prompt below>,
    runTimeoutSeconds=600  # REQUIRED: 10 minutes (600s)
)
```

**子代理提示**（该提示没有对话上下文）：

**不要等待后台监控任务完成**——立即继续对话。

#### 多轮对话备用方案（无后台监控）

告诉用户：“我已经发送了你的修改请求。你可以在这里查看进度：[任务URL]。如果你需要我检查是否完成，请告诉我！”

当用户要求检查进度时，使用以下步骤：

```bash
python3 scripts/anygen.py get-messages --task-id {task_id} --limit 5
```

查找AI的回复内容，并自然地告知用户。

#### 后续修改

用户可以多次请求修改。每次修改时，重复以下步骤：
1. 使用`send-message`发送修改请求
2. 使用`get_messages --wait`命令监控进度
3. 完成后通过在线链接通知用户

所有修改操作都使用相同的`task_id`——不要创建新的任务。

## 注意事项

- 任务执行时间最长为20分钟
- 仅使用公开的市场数据，不提供投资建议
- 轮询间隔为3秒
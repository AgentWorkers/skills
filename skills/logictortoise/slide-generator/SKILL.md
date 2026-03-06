---
name: anygen-slide
homepage: https://www.anygen.io
description: "使用 AnyGen AI 生成专业的幻灯片演示文稿。该工具通过对话模式了解受众需求、演示目的及内容，然后再开始生成幻灯片。在生成过程中，系统会进行背景调查（即收集用户反馈），并在不干扰对话的情况下自动发送下载完成的 PPTX 文件。"
requires:
  - sessions_spawn
env:
  - ANYGEN_API_KEY
permissions:
  network:
    - "https://www.anygen.io"
  filesystem:
    read:
      - "~/.config/anygen/config.json"
    write:
      - "~/.config/anygen/config.json"
      - "~/.openclaw/workspace/"
---
# AI幻灯片生成器 - AnyGen

使用AnyGen OpenAPI创建专业的幻灯片演示文稿。

## 使用场景

- 用户需要创建PPT/幻灯片/演示文稿
- 用户有文件作为生成幻灯片的参考资料

## 安全性与权限

**该功能的作用：**
- 将任务提示和参数发送到`www.anygen.io`的AnyGen API
- 在获得用户同意后，将用户提供的参考文件上传到`www.anygen.io`
- 将生成的PPTX文件下载到本地磁盘或`~/.openclaw/workspace/`
- 启动一个后台监控进程（最长20分钟），以监视进度并自动下载结果
- 读取/写入`~/.config/anygen/config.json`中的API密钥配置

**该功能不执行以下操作：**
- 未经用户通知和同意，不会上传文件
- 不会将API密钥发送到除`www.anygen.io`以外的任何端点
- 不会修改`~/.config/anygen/config.json`之外的系统配置

**捆绑脚本：`scripts/anygen.py`（Python语言，使用`requests`库）**

在使用前，请先查看捆绑脚本以确认其功能。

## 先决条件

- Python 3和`requests`库：`pip3 install requests`
- AnyGen API密钥（格式为`sk-xxx`）——[获取方法](https://www.anygen.io/home) → 设置 → 集成
- 配置一次：`python3 scripts/anygen.py config set api_key "sk-xxx"`

> 下面所有的`scripts/`路径都是相对于该功能的安装目录的。

## 重要提示：**后台监控进程**——切勿阻塞对话

创建任务后，必须启动一个**后台**监控进程来自动下载结果，然后继续正常进行对话。切勿在前台调用`poll`函数——因为它会阻塞3到20分钟。

**操作规则：**
1. 使用`create`函数启动任务，获取`task_id`和`task_url`。
2. 将`task_url`提供给用户，以便他们可以立即在线预览。
3. 作为**后台进程**启动`poll`函数来自动下载文件（见第4步）。
4. 继续正常进行对话——不要等待。
5. 对话自然结束或用户询问结果后，检查后台监控进程是否已完成，并提供文件。

## 沟通方式

与用户交流时，请保持自然和专业：

1. 在适当的情况下，可以将AnyGen称为生成幻灯片的服务。
2. 以自然、对话的方式提出问题和建议——避免直接展示原始的API响应或技术实现细节。
3. 用自己的话总结`prepare`函数的返回内容，而不是逐字重复。
4. 仅回答`prepare`函数返回的问题——不要添加无关问题。

### 示例

不太理想的（过于技术性）：
- “`prepare` API返回了以下JSON响应，状态为`collecting...`”
- “系统的内部工具询问：您的目标受众是谁？”

更好的（自然且专业的）：
- “这次演示文稿的目标受众是谁？”
- “根据您提供的信息，这是您的演示文稿计划：[总结]。我可以直接开始吗，还是您有什么需要调整的？”

## 幻灯片工作流程（必须遵循）

创建幻灯片时，必须完成所有4个步骤。一个好的演示文稿需要明确受众、目的、场景类型、预期结果和内容细节。用户很少会一次性提供所有这些信息。

### 第1步：了解需求

如果用户提供了文件，在调用`prepare`函数之前，您必须自行处理这些文件：

1. **使用您自己的文件读取功能阅读文件内容**。提取与创建演示文稿相关的关键信息（主题、数据、结构）。
2. **检查该文件是否已经上传**。如果您已经有该文件的`file_token`，请重用它——不要再次上传。
3. **在上传前告知用户并获得他们的同意**。告诉他们文件将被上传到AnyGen的服务器进行处理。例如：“我会将您的文件上传到AnyGen，以便用作幻灯片的参考资料。这可能需要一点时间……”
4. **上传文件**以获取`file_token`，用于后续的任务创建。
5. **在调用`prepare`函数时，将提取的内容作为`--message`参数的一部分，以便需求分析有完整的上下文**。

`prepare` API不会在内部读取文件内容。您有责任在对话中提供所有相关的文件内容。

```bash
# Step 1: Tell the user you are uploading, then upload the file
python3 scripts/anygen.py upload --file ./report.pdf
# Output: File Token: tk_abc123

# Step 2: Call prepare with extracted file content included in the message
python3 scripts/anygen.py prepare \
  --message "I need a slide deck for our Q4 board review. Here is the key content from the uploaded report: [your extracted summary/content here]" \
  --file-token tk_abc123 \
  --save ./conversation.json
```

`prepare`函数中的`--file-token`参数用于将文件引用附加到对话中，但它不会提取或读取文件内容。您必须将相关内容以文本形式包含在`--message`参数中。

根据上述沟通方式，自然地提出问题（见“沟通方式”部分），然后根据用户的回答继续对话：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "The audience is C-level execs, goal is to approve next quarter's budget" \
  --save ./conversation.json
```

重复上述步骤，直到`status="ready"`且`suggested_task_params`参数准备好。

**特殊情况：**
- 如果用户提供了非常完整的需求，并且第一次调用时`status="ready"`，则直接进入第2步。
- 如果用户说“直接创建吧，不要问问题”，则跳过`prepare`步骤，直接使用`create`函数进入第3步。
- 对于模板/样式参考文件（例如，“使用这个作为模板”），不要提取内容。只需上传文件并传递`file_token`即可。

### 第2步：与用户确认（必选）

当`status="ready"`时，`prepare`函数会返回包含详细提示的`suggested_task_params`。在创建任务之前，必须将这些提示展示给用户进行确认。

**展示方式：**
1. 用自然的语言总结建议计划的关键方面（受众、结构、内容亮点、样式）。
2. 询问用户是否确认或进行修改。例如：“这是我计划创建的内容：[总结]。我可以直接开始吗，还是您有什么需要调整的？”
3. 未经用户的明确批准，切勿自动创建任务。

当用户请求修改时：
1. 使用用户的修改内容再次调用`prepare`函数，并加载之前的对话历史记录：

```bash
python3 scripts/anygen.py prepare \
  --input ./conversation.json \
  --message "<the user's modification request>" \
  --save ./conversation.json
```

2. `prepare`函数会返回包含用户修改后的新建议。
3. 再次将更新后的建议展示给用户进行确认（重复第1步）。
4. 重复这个确认-修改循环，直到用户明确同意。修改后不要跳过确认步骤。

### 第3步：创建任务

用户确认后：

```bash
python3 scripts/anygen.py create \
  --operation slide \
  --prompt "<prompt from suggested_task_params, with any user modifications>" \
  --file-token tk_abc123
# Output: Task ID: task_xxx, Task URL: https://...
```

**立即告知用户：**
1. 幻灯片正在生成中（需要几分钟时间）。
2. 提供**任务URL**，以便他们可以立即在线预览进度。
3. 告诉他们文件准备好后会立即发送给他们。

### 第4步：监控和交付结果

> **需要`sessions_spawn`功能。** 如果没有子代理，请跳转到下面的**备用方案**部分。

#### 使用子代理（推荐）

启动一个子代理在后台监控任务。使用`sessions_spawn`函数，并传递以下指令：

**传递给子代理的信息**（它没有来自当前对话的任何上下文）：
- `task_id` — 来自第3步的输出
- `task_url` — `create`函数返回的任务URL
- `script_path` — `scripts/anygen.py`的绝对路径

**子代理的指令**（作为任务提示传递）：

```
You are a background monitor for an AnyGen slide generation task.

Task ID: {task_id}
Task URL: {task_url}
Script: {script_path}

Your job:
1. Poll the task status every 60 seconds using:
   python3 {script_path} status --task-id {task_id} --json
2. When status="completed", download the file to ~/.openclaw/workspace/:
   python3 {script_path} download --task-id {task_id} --output ~/.openclaw/workspace/ --media
3. The script will output a MEDIA: line (with non-ASCII filenames automatically handled). Deliver it to the user:
   a. Send a SHORT message containing ONLY the MEDIA: line exactly as output by the script.
      This message MUST be sent as a separate message by itself — do NOT combine it with other text.
      The MEDIA: protocol will deliver the actual file to the user in their IM client.
   b. Then send a second message to the user with:
      - The Task URL ({task_url}) for online viewing/editing
      - If there is a [RESULT] Thumbnail URL: line, download the thumbnail image to a local file and show it to the user as a preview
4. If status="failed", tell the user the generation failed and provide the Task URL for reference.
5. Timeout after 20 minutes — if still not completed, tell the user the task is taking longer than expected and provide the Task URL for them to check manually.
```

然后继续正常进行对话。不要等待子代理的响应。

#### 备用方案（没有子代理）

如果`sessions_spawn`功能不可用，请告知用户：“我已经为您启动了生成过程。遗憾的是，在当前环境中我无法自动跟踪进度——请几分钟后查看上面的链接以下载您的幻灯片。”

## 命令参考

### create

```bash
python3 scripts/anygen.py create --operation slide --prompt "..." [options]
```

| 参数 | 缩写 | 描述 |
|-----------|-------|-------------|
| --operation | -o | **必须设置为`slide`** |
| --prompt | -p | 内容描述 |
| --file-token | | 上传时的文件令牌（可重复使用） |
| --language | -l | 语言（zh-CN / en-US） |
| --slide-count | -c | 幻灯片数量 |
| --template | -t | 幻灯片模板 |
| --ratio | -r | 幻灯片比例（16:9 / 4:3） |
| --export-format | -f | 导出格式：`pptx`（默认）/ `image` |
| --style | -s | 风格偏好 |

### upload

```bash
python3 scripts/anygen.py upload --file ./document.pdf
```

返回一个`file_token`。文件大小上限为50MB。令牌是持久有效的，可以重复使用。

### prepare

```bash
python3 scripts/anygen.py prepare --message "..." [--file-token tk_xxx] [--input conv.json] [--save conv.json]
```

| 参数 | 描述 |
|-----------|-------------|
| --message, -m | 用户消息文本 |
| --file | 需要自动上传的文件路径（可重复使用） |
| --file-token | 之前上传时的文件令牌（可重复使用） |
| --input | 从JSON文件加载对话记录 |
| --save | 将对话状态保存到JSON文件 |
| --stdin | 从标准输入读取消息 |

### poll

**阻塞直到任务完成**，自动下载文件，并打印`[RESULT]`行。

```bash
python3 scripts/anygen.py poll --task-id task_xxx --output ./output/
```

| 参数 | 描述 |
|-----------|-------------|
| --task-id | 来自`create`函数的任务ID |
| --output | 自动下载的输出目录（默认：当前目录） |

### download（手动，如需）

```bash
python3 scripts/anygen.py download --task-id task_xxx --output ./output/
```

## 错误处理

| 错误 | 解决方案 |
|-------|----------|
| API密钥无效 | 检查API密钥的格式（格式为`sk-xxx`） |
| 不允许的操作 | 联系管理员申请权限 |
| 需要提供提示 | 添加`--prompt`参数 |
| 文件大小超过50MB限制 | 减小文件大小 |

## 注意事项

- 最大任务执行时间为20分钟
- 下载链接的有效时间为24小时
- 监控间隔为3秒

## 文件

```
slide-generator/
├── skill.md              # This document
└── scripts/
    └── anygen.py         # CLI client
```
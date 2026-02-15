---
name: calibre-catalog-read
description: 通过 Content 服务器，使用 `calibredb` 读取 Calibre 目录数据，并执行单本书籍的分析流程。该流程会将分析结果以 HTML 格式写入书籍的注释中，同时将分析状态缓存到 SQLite 数据库中。此功能可用于列表查询、搜索、ID 查找，以及为选定的书籍提供 AI 阅读服务。
metadata: {"openclaw":{"requires":{"bins":["node","uv","calibredb","ebook-convert"],"env":["CALIBRE_PASSWORD"]},"optionalEnv":["CALIBRE_USERNAME"],"primaryEnv":"CALIBRE_PASSWORD","dependsOnSkills":["subagent-spawn-command-builder"],"localWrites":["skills/calibre-catalog-read/state/runs.json","skills/calibre-catalog-read/state/calibre_analysis.sqlite","skills/calibre-catalog-read/state/cache/**","~/.config/calibre-catalog-read/auth.json"],"modifiesRemoteData":["calibre:comments-metadata"]}}
---

# calibre-catalog-read

此技能用于以下操作：
- 仅用于读取目录信息（`list`, `search`, `id`）
- 单本书籍的AI阅读工作流程（`export -> analyze -> cache -> comments HTML apply`）

## 必备条件

- 在执行脚本的运行环境中，`calibredb`必须在`PATH`路径下可用。
- 必须有`ebook-convert`工具用于提取文本。
- 必须安装了`subagent-spawn-command-builder`（用于生成子代理的启动参数）。
- 可访问的Calibre内容服务器URL，格式为`--with-library`：
  - `http://HOST:PORT/#LIBRARY_ID`
  - 请勿使用`localhost/127.0.0.1`；必须提供明确的`HOST:PORT`地址。
- 如果启用了身份验证：
  - 建议将配置信息设置在`/home/altair/.openclaw/.env`文件中：
    - `CALIBRE_USERNAME=<user>`
    - `CALIBRE_PASSWORD=<password>`
  - 在调用此技能时，只需传递`--password-env CALIBRE_PASSWORD`（用户名会自动从环境变量中加载）。
  - 也可以通过`--username <user>`显式指定用户名。
  - 可选的身份验证缓存文件：`~/.config/calibre-catalog-read/auth.json`
  - 除非特别要求，否则请勿使用`--save-plain-password`选项。

## 命令

- 列出书籍（JSON格式）：
```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs list \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --limit 50
```

- 搜索书籍（JSON格式）：
```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs search \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --query 'series:"中公文庫"'
```

- 根据ID获取单本书籍（JSON格式）：
```bash
node skills/calibre-catalog-read/scripts/calibredb_read.mjs id \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --book-id 3
```

- 运行单本书籍的处理流程（分析 + 应用评论 + 缓存）：
```bash
uv run python skills/calibre-catalog-read/scripts/run_analysis_pipeline.py \
  --with-library "http://192.168.11.20:8080/#Calibreライブラリ" \
  --password-env CALIBRE_PASSWORD \
  --book-id 3 --lang ja
```

## 缓存数据库

- 初始化数据库模式：
```bash
uv run python skills/calibre-catalog-read/scripts/analysis_db.py init \
  --db skills/calibre-catalog-read/state/calibre_analysis.sqlite
```

- 检查当前的数据库状态：
```bash
uv run python skills/calibre-catalog-read/scripts/analysis_db.py status \
  --db skills/calibre-catalog-read/state/calibre_analysis.sqlite \
  --book-id 3 --format EPUB
```


## 主代理与子代理的职责划分（明确分工）

为了防止聊天监听器长时间处于阻塞状态，需要严格区分主代理和子代理的职责：

### 主代理（负责快速控制）
- 验证用户的操作意图和目标书籍ID。
- 确认子代理的运行参数：`model`, `thinking`, `runTimeoutSeconds`。
- 启动子代理并快速返回进度信息。
- 在子代理完成分析后，将结果插入数据库并更新Calibre元数据。
- 向用户报告最终结果。

### 子代理（负责复杂分析）
- 读取提取的文本数据。
- 严格按照指定的模式生成分析结果（JSON格式）。
- 不负责应用元数据或与用户交互的通道操作。

### 主代理应避免执行的操作（除非必要）
- 进行复杂的内容分析。
- 对整段文本进行多步骤的深度处理。

## 运行策略
- 每次运行仅处理一本书籍。
- 优先采用异步处理方式：先快速响应用户请求，分析完成后再提供最终结果。
- 如果分析结果无法获取，可以选择询问用户或使用备用方案。

## 子代理的启动前准备（必须执行）

在会话中首次运行子代理之前，需要确认以下参数：
- `model`
- `thinking`（设置为`low`、`medium`或`high`）
- `runTimeoutSeconds`

这些参数无需在每次运行时都重新确认；除非用户要求更改，否则会话中的后续书籍可以使用相同的配置。

## 子代理的支持（模型无关）

书籍阅读分析是一项耗时的任务。建议使用模型较轻的子代理来生成分析结果，然后将结果返回给主代理进行缓存或应用操作。

- 提示模板：`references/subagent-analysis.prompt.md`
- 输入模式：`references/subagent-input.schema.json`
- 输出模式：`references/subagent-analysis.schema.json`
- 输入准备辅助脚本：`scripts/prepare_subagent_input.mjs`
  - 该脚本会将提取的文本分割成多个文件，以避免读取工具因文件长度过大而出现问题。

**规则**：
- 仅将耗时的分析任务交给子代理处理；保持主代理轻量级且不阻塞用户界面。
- 在此环境中，Python命令必须使用`uv run python`来执行。
- 必须使用指定的提示模板`references/subagent-analysis.prompt.md`；禁止发送自定义的、过于复杂的读取指令。
- 最终的数据库更新和Calibre元数据应用操作由主代理完成。
- 每次运行仅处理一本书籍。
- 每个会话中只需确认一次模型、分析策略和超时设置；不要在技能代码中硬编码特定提供者的模型ID。
- 使用OpenClaw的默认设置来配置回调/通知行为和速率限制机制（无需在此技能中硬编码）。
- 如果书籍的标签或标题表明是漫画或动画，应跳过该处理流程。
- 如果提取的文本太短，应停止操作并请求用户确认是否继续。
  - 在这种情况下，流程会返回`reason: low_text_requiresconfirmation`以及相应的提示信息。

## 语言处理策略

- 不要在脚本中硬编码用户的语言设置。
- 分析结果应使用用户选择的语言生成，并通过用户设置和`lang`参数来控制显示语言。
- 脚本中的默认分析结果为通用格式；优先使用子代理生成的翻译结果。

## 协调说明（重要）

`run_analysis_pipeline.py`是一个本地脚本，它本身不会直接调用OpenClaw工具。
子代理的运行必须由主代理通过`sessions_spawn`来协调。

**必需的运行顺序**：
1. 主代理准备`subagent_input.json`文件以及从提取的文本中分块的`source_files`文件：
   - 使用命令：```bash
   node skills/calibre-catalog-read/scripts/prepare_subagent_input.mjs \
     --book-id <id> --title "<title>" --lang ja \
     --text-path /tmp/book_<id>.txt --out-dir /tmp/calibre_subagent_<id>
   ```
2. 主代理使用`subagent-spawn-command-builder`生成`sessions_spawn`所需的参数，然后调用`sessions_spawn`。
   - 使用`calibre-read`配置文件和特定的分析任务信息来构建请求。
   - 直接使用生成的JSON数据（或仅合并一些运行相关的字段，如标签或任务描述）。
3. 子代理读取所有`source_files`文件并返回符合模式的分析结果（JSON格式）。
4. 主代理通过`--analysis-json`参数将结果传递给`run_analysis_pipeline.py`进行数据库更新和元数据应用。

如果步骤2被跳过，流程将使用本地化的简单分析方式（仅限紧急情况或测试用途）。

## 聊天交互模型（强制要求）

对于Discord聊天界面，操作必须分为**两个独立的步骤**：

### 第一步：启动分析（必须快速完成）
- 选择目标书籍。
- 使用`subagent-spawn-command-builder`生成启动参数（`--profile calibre-read` + 特定的`--task`）。
- 使用生成的参数调用`sessions_spawn`。
- 通过`run_state.mjs`记录运行状态（`runId`）。
- 向用户回复已开始分析的消息。
- **在此步骤结束**。

### 第二步：完成分析（单独进行）
- 在分析完成后触发通知或事件。
- 执行一个命令（`scripts/handle_completion.mjs`）：
  - 执行`get -> apply`操作；遇到错误时执行`fail`处理。
- 如果`runId`缺失，处理程序将返回`stale_or_duplicate`并停止进一步操作。
- 从处理结果中发送完成或失败的回复。

**重要规则**：
- 在第一步中，严禁进行轮询或等待子代理的完成。
- 严禁在聊天界面中保持监听状态直到子代理完成。

## 运行状态管理（单文件存储）

对于每次处理一本书籍的操作，需要维护一个JSON格式的状态文件：
- `skills/calibre-catalog-read/state/runs.json`

使用`runId`作为主键（子代理的执行ID）。

**状态更新流程**：
1. 当子代理接受任务时，记录一条信息：
   - `runId`, `book_id`, `title`, `status: "running", `started_at`
2. 在同一聊天轮次内不要进行轮询或等待。
3. 在分析完成后，根据`runId`加载相应的记录并执行应用操作。
4. 如果应用成功，立即删除该记录。
5. 如果分析失败，将状态设置为`status: "failed"`并记录错误信息，以便后续重试或调试。

**规则**：
- 保持状态文件的大小适中，仅记录有效的或失败的运行记录。
- 如果记录已经删除，应忽略重复的完成事件。
- 如果在分析完成时记录缺失，应报告为“无效/未知的运行状态”，并避免盲目执行应用操作。

**辅助脚本的使用（避免环境变量错误）**：
```bash
# Turn A: register running task
node skills/calibre-catalog-read/scripts/run_state.mjs upsert \
  --state skills/calibre-catalog-read/state/runs.json \
  --run-id <RUN_ID> --book-id <BOOK_ID> --title "<TITLE>"

# Turn B: completion handler (preferred)
node skills/calibre-catalog-read/scripts/handle_completion.mjs \
  --state skills/calibre-catalog-read/state/runs.json \
  --run-id <RUN_ID> \
  --analysis-json /tmp/calibre_<BOOK_ID>/analysis.json \
  --with-library "http://HOST:PORT/#LIBRARY_ID" \
  --password-env CALIBRE_PASSWORD --lang ja
```
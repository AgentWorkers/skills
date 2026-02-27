---
name: org-memory
version: 0.3.0
description: "使用 `org-mode` 文件构建结构化的知识库和任务管理系统。通过 `org` CLI 可以查询、修改、链接以及搜索 `org` 文件和 `org-roam` 数据库中的内容。"
metadata: {"openclaw":{"emoji":"🦄","homepage":"https://github.com/dcprevere/org-cli","requires":{"bins":["org"],"env":["ORG_MEMORY_AGENT_DIR","ORG_MEMORY_HUMAN_DIR","ORG_MEMORY_AGENT_DATABASE_LOCATION","ORG_MEMORY_HUMAN_DATABASE_LOCATION"]},"install":[{"kind":"download","label":"Download from GitHub releases: https://github.com/dcprevere/org-cli/releases"}]}}
---
# org-memory

使用 `org` 命令行工具（CLI）来维护 `org-mode` 文件中的结构化、链接化且易于阅读的知识内容。`org` 文件是具有丰富结构的纯文本文件，包含标题、待办事项状态、标签、属性、时间戳和链接等内容。结合 `org-roam` 工具，它们可以形成一个由 SQLite 数据库支持的知识图谱。

## 快捷键

当用户使用这些快捷键时，系统会直接执行相应的操作。

| 关键词 | 含义 | 目标路径 |
|---|---|---|
| `Todo:` | 创建一个带有日期的待办事项 | `$ORG_MEMORY_HUMAN_DIR` |
| `Note:` | 将此内容记录下来 | `$ORG_MEMORY_HUMAN_DIR` |
| `Done:` / `Finished:` | 将待办事项标记为已完成 | `$ORG_MEMORY_HUMAN_DIR` |
| `Know:` | 将此信息存储在代理的知识库中以供日后查询 | `$ORG_MEMORY_AGENT_DIR` |

### 待办事项 — 创建待办事项

`Todo: <文本>` 表示“创建一个待办事项”。从文本中提取日期或时间范围，并安排任务的执行时间。如果文本中包含相对日期（如“3周后”、“周五之前”、“下个月”），则计算实际日期，并添加 `--scheduled <日期>` 或 `--deadline <日期>` 参数。

**操作示例：**  
`org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" '<标题>' --todo TODO --scheduled <日期> --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json`

当文本中明确指定了截止日期（如“周五之前”、“3月1日截止”）时，使用 `--deadline` 参数；对于较宽松的时间安排（如“3周后”、“下个月”、“明天”），则使用 `--scheduled` 参数。

**示例：**  
- “Todo: 3周后提交税款” → `org add .../inbox.org '提交税款' --todo TODO --scheduled 2026-03-18`  
- “Todo: 6月前更新护照” → `org add .../inbox.org '更新护照' --todo TODO --deadline 2026-06-01`  
- “Todo: 明天看牙医” → `org add .../inbox.org '看牙医' --todo TODO --scheduled 2026-02-26`  
- “Todo: 预订航班” → `org add .../inbox.org '预订航班' --todo TODO`（未提及具体日期）  

### 备注 — 用于人类用户

`Note: <文本>` 表示“将此内容添加到我的 `org` 文件中”。这始终是针对人类的待办事项或提醒，而非代理的任务。

**操作示例：**  
`org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" '<文本>' --todo TODO -f json`

如果备注中包含日期或截止日期，添加 `--scheduled <日期>` 或 `--deadline <日期>` 参数；如果没有日期，则不添加（由人类用户自行安排或请求你安排）。

**示例：**  
- “Note: 购买食品杂货” → `org add .../inbox.org '购买食品杂货' --todo TODO`  
- “Note: 在周五之前审阅 PR #42” → `org add .../inbox.org '审阅 PR #42' --todo TODO --deadline 2026-02-28`  
- “Note: 我们可以在应用程序中添加功能 X” → `org add .../inbox.org '在应用程序中添加功能 X' --todo TODO`  
- “Note: 向 Donna 发送关于安全措施的邮件” → `org add .../inbox.org '向 Donna 发送关于安全措施的邮件' --todo TODO`  

**注意与待办事项的区别：**  
两者都会创建待办事项条目，但用途不同：`Todo:` 表示具体的任务（尽量提取日期），而 `Note:` 则用于记录想法、提醒或观察结果。如果没有日期，则不添加日期。

**特殊情况 — 想法与观察记录：**  
如果用户输入“Note: 我们可以尝试 X”或“Note: 关于 Y 的想法”，这仍然属于备注内容。应将其作为待办事项记录下来，不要将其添加到代理的知识库中。  

### 完成 — 标记任务为已完成

`Done: <文本>` 或 `Finished: <文本>` 表示“将此任务标记为已完成”。请查找相应的待办事项条目并更新其状态。

**操作示例：**  
1. 搜索：`org todos --state TODO --search '<文本>' -d "$ORG_MEMORY_HUMAN_DIR" -f json`  
2. 如果只找到一个匹配项：`org todo <文件> '<标题>' DONE -f json`  
3. 如果找到多个匹配项：向用户显示所有匹配项并询问具体是哪一项  
4. 如果没有找到匹配项：告知用户无法找到该任务  

**示例：**  
- “Done: 向 Nigel Kerry 支付费用” → 查找并标记为已完成  
- “Finished: 完成了 PR 审阅” → 查找并标记为已完成  
- “Done: 购买食品杂货” → 搜索“groceries”并标记为已完成  

### 存储信息 — 用于代理

`Know: <信息>` 表示“将此信息存储在代理的知识库中以供将来查询”。这些信息应在会话之间保持一致。

**操作示例：**  
首先搜索现有的节点（`org roam node find`），然后创建或更新节点。

**示例：**  
- “Know: Sarah 更喜欢在早上开会” → 为 Sarah 在 `$ORG_MEMORY_AGENT_DIR` 中创建/更新节点  
- “Know: 该 API 使用 OAuth2，而非 API 密钥” → 为该 API 在 `$ORG_MEMORY_AGENT_DIR` 中创建/更新节点  

### 每次写入后 — 确认操作

在对任一目录进行修改后，务必以以下格式输出确认信息：  
```
org-memory: <action> <file-path>
```  

**示例：**  
`org-memory: 向 ~/org/human/inbox.org 添加了待办事项`，`org-memory: 在 ~/org/agent/sarah.org 中创建了节点`，`org-memory: 更新了 ~/org/agent/sarah.org`。`

**注意：** 这是强制性的。切勿默默地对任一目录进行写入操作，用户应始终能够看到你的操作内容及其位置。  

## 输出格式

所有命令都支持使用 `-f json` 选项来生成结构化的输出（格式为 `{"ok":true,"data":...}`）。错误会返回 `{"ok":false,"error":{"type":"...","message":"..."}`。务必使用 `-f json` 选项。  

## 命令安全性

用户提供的文本（待办事项标题、备注内容、搜索词）必须使用单引号括起来，以防止 Shell 解释器误解读。双引号可以用于包含 `$()` 表达式、反引号或变量插值；单引号无法实现这些功能。  

**示例：**  
如果文本中包含单引号，需要使用 `'\''` 来转义它：  
```bash
org add "$ORG_MEMORY_HUMAN_DIR/inbox.org" 'Don'\''t forget' --todo TODO -f json
```  

对于多行内容，应通过标准输入（stdin）传递，而不是直接在代码中插入：  
```bash
printf '%s' 'Long text here' | org append k4t --stdin -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json
```  

环境变量路径（如 `$ORG_MEMORY_HUMAN_DIR` 等）必须始终使用双引号，以避免因空格导致的错误；但用户提供的文本本身不应使用双引号。  

## 命令说明

运行 `org schema` 可以获取所有命令、参数和标志的机器可读描述。这样你就可以在不记住接口细节的情况下生成有效的命令。  

## 配置

配置通过环境变量完成。将相关设置保存在 `openclaw.json` 文件中，以便在每次执行命令时自动应用这些配置。

| 变量 | 默认值 | 用途 |
|---|---|---|
| `ORG_MEMORY_USE_FOR_AGENT` | `true` | 启用代理的知识库功能 |
| `ORG_MEMORY_AGENT_DIR` | `~/org/agent` | 代理的 `org` 文件目录 |
| `ORG_MEMORY_AGENT_DATABASE_LOCATION` | `~/.local/share/org-memory/agent/.org.db` | 代理的数据库路径 |
| `ORG_MEMORY_USE_FOR_HUMAN` | `true` | 启用人类用户的 `org` 文件中的任务管理功能 |
| `ORG_MEMORY_HUMAN_DIR` | `~/org/human` | 人类的 `org` 文件目录 |
| `ORG_MEMORY_HUMAN_DATABASE_LOCATION` | `~/.local/share/org-memory/human/.org.db` | 人类的数据库路径 |

如果 `ORG_MEMORY_USE_FOR_AGENT` 的值为 `false`，则跳过知识管理相关内容；如果 `ORG_MEMORY_USE_FOR_HUMAN` 的值为 `false`，则跳过任务管理和批量操作相关内容。  

每次执行命令时，务必使用 `--db` 参数指定正确的数据库路径。`org` CLI 会使用 `--db` 参数自动同步 `org-roam` 数据库。如果不使用 `--db`，CLI 会默认使用 Emacs 的 `org-roam` 数据库（`~/.emacs.d/org-roam.db`），但这可能不是你想要的结果。  

初始化所有启用的目录。如果目录中已存在 `org` 文件，请先进行同步：  
```bash
# Sync existing files into the roam database (skip if starting fresh)
org roam sync -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org roam sync -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"

# Create a seed node for the agent's knowledge base (skip if files already exist)
org roam node create 'Index' -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION" -f json

# Build the headline index (enables CUSTOM_ID auto-assignment and file-less commands)
org index -d "$ORG_MEMORY_AGENT_DIR" --db "$ORG_MEMORY_AGENT_DATABASE_LOCATION"
org index -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```  

`org-roam` 的响应会包含节点的 ID、文件路径、标题和标签等信息。  

## 稳定的标识符（CUSTOM_ID）

使用 `org add` 创建的每个标题都会自动分配一个简短的 `CUSTOM_ID`（例如 `k4t`，前提是存在索引数据库）。这个 ID 会出现在所有 JSON 响应的 `custom_id` 字段中，并作为文本输出的一部分。  

在后续命令中可以使用 `CUSTOM_ID` 来引用标题——这些标识符在编辑过程中保持不变，无需指定文件路径：  
```bash
org todo k4t DONE -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org schedule k4t 2026-03-15 -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org note k4t 'Pushed back per manager request' -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
org append k4t 'Updated scope per review.' -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION" -f json
```  

**为没有 `CUSTOM_ID` 的现有标题补充标识符：**  
```bash
org custom-id assign -d "$ORG_MEMORY_HUMAN_DIR" --db "$ORG_MEMORY_HUMAN_DATABASE_LOCATION"
```  

**切勿使用位置编号（`pos`）来引用标题。** 文件被修改后，标题的位置可能会发生变化，从而导致后续标题的文件位置也随之改变。  

**推荐的稳定标识符：**  
1. **CUSTOM_ID**（例如 `k4t`）——稳定、简短且唯一  
2. **org-id**（UUID）——稳定且唯一  
3. **确切的标题**——只要标题不变，该标识符也保持稳定  

如果你需要在同一个文件中修改多个标题，可以：  
- 使用 `org batch` 来执行原子性的多步骤操作（推荐方法）  
- 使用 `CUSTOM_ID` 或标题来引用标题，切勿使用 `pos`  
- 如果必须使用 `pos`，请在每次修改后重新查询以获取最新的标题位置。  

## 错误处理**

根据 `ok` 字段的值来处理错误：  
- `file_not_found`：路径错误或文件已被删除  
- `headline_not_found`：标识符不匹配；需要重新查询以获取当前状态  
- `parse_error`：文件包含解析器无法处理的格式；请不要重试  
- `invalid_args`：请检查 `org schema` 或使用 `org <命令> --help` 命令获取帮助信息  

## 参考资料**

根据需要阅读以下文档：  
- **知识管理**（`{baseDir}/references/knowledge-management.md`）：当 `ORG_MEMORY_USE_FOR_AGENT` 为 `true` 且需要创建/查询/链接代理知识库中的节点时，请阅读此文档。  
- **任务管理**（`{baseDir}/references/task-management.md`）：当 `ORG_MEMORY_USE_FOR_HUMAN` 为 `true` 且需要查询或修改人类用户的任务、执行批量操作或将自然语言查询转换为命令时，请阅读此文档。  
- **内存架构**（`{baseDir}/references/memory-architecture.md`）：首次使用或会话开始时（如内存迁移、文件结构、会话流程、环境数据捕获指南等）请阅读此文档。
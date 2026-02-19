# 存储与检索内存 📦

**状态:** ✅ 正在运行 | **模块:** Archive | **所属部分:** Agent Brain

该模块负责内存的存储和检索。它是唯一一个直接读写内存后端（默认使用 SQLite 的 `memory.db` 文件，或使用旧版 JSON 后端的 `memory.json` 文件）的模块。

## 操作流程

所有操作均通过 `scripts/memory.sh` 脚本执行：

### 存储数据
```bash
# User tells you a fact
./scripts/memory.sh add fact "Alex prefers prose over bullets" user "style,formatting"

# User teaches a procedure
./scripts/memory.sh add procedure "Always run tests before committing" user "workflow,git"

# Store a preference with context
./scripts/memory.sh add preference "Prefers concise responses" user "style" "" "casual conversations"

# Store with namespaced tags
./scripts/memory.sh add preference "Uses Python for data work" user "code.python,data"
```

### 检索数据
```bash
# Search by keyword (auto-touches returned entries, weighted scoring)
./scripts/memory.sh get "formatting style"

# List all of a type
./scripts/memory.sh list preference
```

检索结果会根据关键词匹配度（40%）、标签重叠度（25%）、置信度（15%）和访问频率（10%）进行排序。检索到的条目会自动标记为已访问状态——无需单独执行 `touch` 命令。

### 更新数据
```bash
# Update a field directly
./scripts/memory.sh update <id> confidence sure

# Replace outdated info
./scripts/memory.sh add fact "Alex now works at CompanyB" user "work"
./scripts/memory.sh supersede <old_id> <new_id>
```

### 更正错误信息
```bash
# When user corrects you — tracks why you were wrong
./scripts/memory.sh correct <wrong_id> "Correct claim here" "Reason for mistake" "tags"
```

### 记录操作成功
```bash
# When a memory was applied successfully
./scripts/memory.sh success <id> "Applied during code review"
```

## 事实提取

代理必须主动从用户的每条消息中提取关键信息。大多数用户不会明确表示“请记住这个信息”，他们会自然地透露相关信息，代理的任务就是捕捉这些信息。

### 每条消息的处理流程

在回复用户消息之前，需对每条消息执行以下操作：
```
1. SCAN the message for extractable signals (see categories below)
2. For each signal found:
   a. CLASSIFY → fact, preference, or procedure?
   b. CHECK duplicates → ./scripts/memory.sh get "<key phrase>"
   c. If not already stored:
      - CHECK conflicts → ./scripts/memory.sh conflicts "<content>"
      - If POTENTIAL_CONFLICTS → ask user to clarify, or supersede old entry
      - If NO_CONFLICTS → store it
   d. STORE silently — never say "I'll remember that" or "storing this"
3. RETRIEVE relevant context → ./scripts/memory.sh get "<message topics>"
4. Respond to the user's actual request, applying retrieved context
```

### 需要提取的信息类型

#### 身份信息（类型：`fact`，标签：`identity.*`）

| 信号 | 示例消息 | 需要存储的内容 |
|--------|----------------|---------------|
| 名字 | “我叫马库斯” / “我的名字是...” | “用户的名字是马库斯” → `identity,personal` |
| 职位 | “我是一名高级工程师” | “用户是一名高级工程师” → `identity,role` |
| 公司 | “我在 Stripe 工作” | “用户在公司 Stripe 工作” → `identity,work` |
| 团队 | “我们的团队负责处理支付相关事务” | “用户的团队负责处理支付相关事务” → `identity,team` |
| 地点 | “我位于柏林” | “用户位于柏林” → `identity,location` |

#### 技术栈信息（类型：`fact`，标签：`code.*`, `tools`）

| 信号 | 示例消息 | 需要存储的内容 |
|--------|----------------|---------------|
| “我们使用的是 X” | “我们使用的是 PostgreSQL” | “团队使用的是 PostgreSQL” → `code.database,tools` |
| “该项目使用的是 Next.js 14” | “该项目使用的是 Next.js 14” → `code.nextjs,project` |
| “我们的技术栈是 React + Node” | “我们的技术栈是 React + Node” → `code.react,code.node,project` |
| “部署环境” | “项目部署在 AWS ECS 上” | “项目部署在 AWS ECS 上” → `infra.aws,project` |
| 隐含信息 | “在我们的 Next.js 应用程序中...” | “该项目使用的是 Next.js” → `code.nextjs,project` |
| 版本信息 | “我们使用的是 Python 3.12” | “项目使用的是 Python 3.12” → `code.python,project` |

#### 偏好设置（类型：`preference`，标签：`style.*`, `code.*`）

| 信号 | 示例消息 | 需要存储的内容 |
|--------|----------------|---------------|
| “我更喜欢 X” | “我更喜欢使用 TypeScript” | “偏好使用 TypeScript 而不是 JavaScript” → `code.typescript,style.code` |
| “我喜欢简洁的代码风格” | “我喜欢使用简洁的函数” | “偏好使用简洁的函数风格” → `code.patterns,style.code` |
| “不要使用 X” | “不要使用任何特定的技术” | “避免在代码中使用特定的技术” → `code.typescript,style.code` |
| “始终使用 X” | “始终使用命名导出” | “偏好使用命名导出而不是默认导出方式” → `code.patterns,style.code` |
| “我讨厌 X” | “我讨厌对象关系型数据库（ORMs）” | “不喜欢使用 ORM，偏好使用原始 SQL” → `code.database,style.code` |
| 风格要求 | “能否让回答更简洁些？” | “偏好简洁的回答风格” → `style.tone` |
| 用户连续三次选择 X | “用户连续三次选择了 Tailwind CSS” | `code.css,style.code` |

#### 工作流程（类型：`procedure`，标签：`workflow.*`）

| 信号 | 示例消息 | 需要存储的内容 |
|--------|----------------|---------------|
| “我总是先做 X” | “我总是先编写测试代码” | “在实现功能之前先编写测试代码（TDD）” → `workflow.testing,process` |
| “在合并之前...” | “在合并之前运行代码检查工具（lint）” | “在合并之前运行代码检查工具（lint）” → `workflow.git,process` |
| “我们的开发流程” | “我们采用主分支（trunk-based）进行开发” | “团队采用主分支（trunk-based）进行开发” → `workflow.git,process` |
| “我的工作流程” | “我从 develop 分支进行开发” | “从 develop 分支进行开发，而不是 main 分支” → `workflow.git,process` |
| “先...然后...” | “先制作原型，再重构” | “先制作原型，再重构” → `workflow.dev,process` |

#### 项目背景信息（类型：`fact`，标签：`project.*`）

| 信号 | 示例消息 | 需要存储的内容 |
|--------|----------------|---------------|
| “我正在开发一个仪表板” | “当前项目是一个仪表板” → `project,context` |
| 架构信息 | “该项目是一个使用 turborepo 的单仓库项目” | “该项目是一个使用 turborepo 的单仓库项目” → `project,infra` |
| 项目约束 | “项目需要符合 HIPAA 标准” | “项目需要符合 HIPAA 安全标准” → `project,constraints` |
| 截止日期 | “项目计划下个月发布” | “项目的发布目标是下个月” → `project,timeline` |
| 迁移计划 | “将 API 从 REST 迁移到 GraphQL” | “计划将 API 从 REST 迁移到 GraphQL” → `project,code.api` |

#### 错误更正

当用户纠正你的信息时，这是一个非常有价值的提取信号：

| 信号 | 示例消息 | 应采取的行动 |
|--------|----------------|--------|
| “不，应该是 X” | “不，我们使用的是 Vitest，而不是 Jest” | `correct <old_id> “团队使用的是 Vitest” “之前误认为是 Jest” |
| “实际上...” | “实际上我是一名普通工程师” | `correct <old_id> “用户是一名普通工程师” “之前被错误地记录为高级工程师” |
| “那不对” | “那不对，API 是 REST” | `correct <old_id> “API 是 REST” “之前错误地认为是 GraphQL” |
| “停止这样做” | “请停止添加分号” | `store preference: “代码中不要使用分号” → `style.code` |

### 明确信号与隐含信号

**明确信号**（置信度较高——存储方式：`source: user`, `confidence: sure`）：
- “请记住...”，“我总是...”，“我的名字是...”，“我们使用...”  
- 用户直接提到的关于自己、团队或项目的事实

**隐含信号**（置信度较低——存储方式：`source: inferred`, `confidence: uncertain`）：
- 用户反复选择某种技术或工具（例如，用户多次选择 Tailwind CSS）  
- 语境线索（例如，“在我们的 Next.js 应用程序中...”可以推断出使用的技术栈）  
- 用户的偏好（例如，用户总是要求回答更简洁）

在将隐含信息提升为明确信息之前，需要进一步确认：
```bash
# Store initially as uncertain
./scripts/memory.sh add fact "Project uses Next.js" inferred "code.nextjs,project"
# If user later confirms → upgrade
./scripts/memory.sh update <id> confidence sure
```

### 不应提取的信息

- **一次性请求**：例如“请将这个内容格式化为表格”——这并不意味着用户真的偏好表格格式。  
- **假设性内容**：例如“如果我们使用 Python...”——这并不代表用户实际使用 Python。  
- **临时性信息**：例如“我正在调试 X”——这类信息过于临时，不适合存储。  
- **敏感数据**：密码、API 密钥、SSN 等信息绝对不能存储。  
- **已存储的信息**：在存储新信息之前，务必先使用 `get` 函数检查是否存在重复项。  
- **显而易见的信息**：例如“用户正在和我交谈”或“用户正在编码”——这类信息无需存储。

### 提取示例

**用户消息**：“嗨，我叫马库斯。我在 Stripe 担任高级工程师，负责开发一个支付仪表板。我们使用 React 和 TypeScript，偏好使用 Tailwind CSS 进行样式设计。”

**提取结果**（从一条消息中提取 5 条信息）：
```bash
./scripts/memory.sh add fact "The user's name is Marcus" user "identity,personal"
./scripts/memory.sh add fact "Marcus is a senior engineer at Stripe" user "identity,work,identity,role"
./scripts/memory.sh add fact "Current project is a payments dashboard" user "project,context"
./scripts/memory.sh add fact "Project uses React with TypeScript" user "code.react,code.typescript,project"
./scripts/memory.sh add preference "Prefers Tailwind for CSS styling" user "code.css,style.code"
```

**用户消息**：“你能将这段代码重构为使用 async/await 吗？我讨厌回调地狱。”**

**提取结果**（提取用户的偏好设置）：
```bash
./scripts/memory.sh add preference "Prefers async/await over callbacks" user "code.patterns,style.code"
```

**用户消息**：“修复第 42 行的类型错误。”

**提取结果**：由于这是一个临时性的任务请求，没有可提取的持久性信息。

## 检索数据的时机

在回复用户的任何请求之前，首先在内存中搜索相关的内容。这是处理每条消息时的第一步——在提取信息之前、在回复之前。

**构建搜索查询的方法**：从用户消息中提取 2-4 个有意义的名词或主题词，去除无关词汇（如“你能”、“帮助我”、“请”等），重点关注核心内容。
| 用户消息 | 搜索查询 |
|---|---|
| “帮我为侧边栏编写一个 React 组件” | `"react component sidebar"` |
| “我们的部署流程是怎样的？” | `"deployment process workflow"` |
| “修复登录错误” | `"login bug auth"` |
| “我应该如何设计 API 的结构？” | `"api structure architecture"` |

```bash
# Always run this first
./scripts/memory.sh get "<query>"
```

**使用检索结果**：如果找到相关条目，直接应用这些结果。不要使用“我记得你...”或“根据我的记忆...”这样的表述——就像你本来就知道这些信息一样自然地使用它们。系统会自动跟踪访问记录，确保检索到的信息是最新的。

## 不应存储的信息

- 临时性的对话内容  
- 用户明确表示是临时性的信息  
- 敏感数据（如密码、API 密钥、SSN）  
- 已经存储在内存中的信息（在使用前请先使用 `get` 函数检查是否存在重复项）  

## 存储前的冲突检查

在添加任何新信息之前，务必执行以下操作：
1. 运行 `./scripts/memory.sh conflicts "<内容>"`
2. 如果返回 `POTENTIAL_CONFLICTS`，则将结果传递给 Signal 模块处理  
3. 如果返回 `NO_CONFLICTS`，则可以继续添加新信息  

## 模式检测

在存储某个流程或偏好设置时，需要检查是否存在相关的条目：
1. 运行 `./scripts/memory.sh similar "<内容>" 0.10`
2. 如果找到 3 条或更多相同类型的相似条目，就创建一个新的模式：
   ```bash
   ./scripts/memory.sh add pattern "<generalized description>" inferred "<tags>"
   ```

## 集成机制

- **信号**：在存储任何信息之前，Archive 模块会先调用 Signal 模块进行冲突检查。  
- **结果展示**：检索结果会包含置信度信息。  
- **通知机制**：当 Archive 检测到 3 条或更多相似条目时，会通知 Ritual 模块。  
- **数据存储**：存储后的数据会被标记为 `ingested` 类型，并附带来源链接（`source_url`）。
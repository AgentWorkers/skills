---
name: til
description: >
  Capture and manage TIL (Today I Learned) entries on OpenTIL.
  Use /til <content> to capture, /til to extract insights from conversation,
  or /til list|publish|edit|search|delete|status|sync|tags|categories|batch to
  manage entries -- all without leaving the CLI.
homepage: https://opentil.ai
license: MIT
metadata:
  author: opentil
  version: "1.11.0"
  primaryEnv: OPENTIL_TOKEN
---

# til

在 OpenTIL 中捕获和管理“今天我学到的”内容——从起草到发布，所有操作都通过命令行界面（CLI）完成。

## 设置

1. 访问 https://opentil.ai/dashboard/settings/tokens，创建一个具有 `read:entries`、`write:entries` 和 `delete:entries` 权限的个人访问令牌。
2. 复制令牌（以 `til_` 开头）。
3. 设置环境变量：

```bash
export OPENTIL_TOKEN="til_xxx"
```

### 令牌解析

令牌解析的优先级：
1. `$OPENTIL_TOKEN` 环境变量（优先于其他配置）
2. `~/.til/credentials` 文件中的令牌（通过 `/til auth` 创建）

如果两者都没有设置，内容将保存在 `~/.til/drafts/` 文件中。

### 凭据文件格式

`~/.til/credentials` 文件以 YAML 格式存储配置文件：

```yaml
active: personal
profiles:
  personal:
    token: til_abc...
    nickname: hong
    site_url: https://opentil.ai/@hong
    host: https://opentil.ai
  work:
    token: til_xyz...
    nickname: hong-corp
    site_url: https://opentil.ai/@hong-corp
    host: https://opentil.ai
```

- `active`：当前激活的配置文件名
- `profiles`：配置文件名与对应凭据的映射
- 每个配置文件包含：`token`、`nickname`（来自 API 的昵称）、`site_url`、`host`

**向后兼容性**：如果 `~/.til/credentials` 文件中包含纯文本格式的令牌（旧格式），会将其 silently 迁移到 `default` 配置文件中（格式为 YAML），然后重新保存。

## 子命令路由

`/til` 后面的第一个单词决定了命令的用途。保留字用于路由到管理子命令；其他内容将被视为待捕获的内容。

| 命令 | 功能 |
|------------|--------|
| `/til list [drafts\|published\|all]` | 列出条目（默认显示草稿） |
| `/til publish [<id> \| last]` | 发布条目 |
| `/til unpublish <id>` | 取消发布（恢复为草稿状态） |
| `/til edit <id> [instructions]` | 人工智能辅助编辑 |
| `/til search <keyword>` | 按标题搜索条目 |
| `/til delete <id>` | 删除条目（需要确认） |
| `/til status` | 显示站点状态和连接信息 |
| `/til sync` | 将本地草稿同步到 OpenTIL |
| `/til tags` | 列出带有使用次数的站点标签 |
| `/til categories` | 列出站点分类 |
| `/til batch <topics>` | 批量捕获多个 TIL 条目 |
| `/til auth` | 连接 OpenTIL 账户（浏览器认证） |
| `/til auth switch [name]` | 切换激活配置文件（通过配置文件名或昵称） |
| `/til auth list` | 列出所有配置文件 |
| `/til auth remove <name>` | 删除配置文件 |
| `/til auth rename <old> <new>` | 重命名配置文件 |
| `/til <anything else>` | 将内容捕获为新的 TIL 条目 |
| `/til` | 从对话中提取有用信息（多选项） |

保留字：`list`、`publish`、`unpublish`、`edit`、`search`、`delete`、`status`、`sync`、`tags`、`categories`、`batch`、`auth`。

## 参考资料加载

⚠️ 除非另有说明，否则不要读取参考文件。SKILL.md 文件中包含了大多数操作所需的足够内联信息。

### 子命令执行前的参考资料加载：

| 子命令 | 需要加载的参考文件 |
|------------|--------------------|
| `/til <content>` | 无 |
| `/til`（从对话中提取内容） | 无 |
| `/til list\|status\|tags\|categories` | [references/management.md](references/management.md) |
| `/til publish\|unpublish\|edit\|search\|delete\|batch` | [references/management.md](references/management.md) |
| `/til sync` | [references/management.md](references/management.md), [references/local-drafts.md](references/local-drafts.md) |
| `/til auth` | [references/management.md](references/management.md), [references/api.md](references/api.md) |
| `/til auth switch\|list\|remove\|rename` | [references/management.md](references/management.md) |

### 按需加载（仅在必要时加载）：

| 触发条件 | 需要加载的参考文件 |
|---------|-------------------|
| API 返回非 2xx 状态码（内联错误处理不足时） | [references/api.md](references/api.md) |
| 自动检测到需要生成 TIL 的内容时 | [references/auto-detection.md](references/auto-detection.md) |
| 未找到令牌（首次运行时使用本地备份） | [references/local-drafts.md](references/local-drafts.md) |

## API 快速参考

**创建并发布条目：**

```bash
curl -X POST "https://opentil.ai/api/v1/entries" \
  -H "Authorization: Bearer $OPENTIL_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "entry": {
      "title": "Go interfaces are satisfied implicitly",
      "content": "In Go, a type implements an interface...",
      "summary": "Go types implement interfaces implicitly by implementing their methods, with no explicit declaration needed.",
      "tag_names": ["go", "interfaces"],
      "published": true,
      "lang": "en"
    }
  }'
```

**关键创建参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `content` | 字符串 | 是 | Markdown 正文（最多 100,000 个字符） |
| `title` | 字符串 | 否 | 条目标题（最多 200 个字符）。会自动生成 slug。 |
| `tag_names` | 数组 | 否 | 1-3 个小写标签，例如 `["go", "concurrency"]` |
| `published` | 布尔值 | 否 | `false` 表示草稿状态（默认），`true` 表示立即发布 |
| `lang` | 字符串 | 否 | 语言代码：`en`、`zh-CN`、`zh-TW`、`ja`、`ko` 等 |
| `slug` | 字符串 | 否 | 自定义 URL slug。如果省略，会从标题自动生成。 |
| `visibility` | 字符串 | 否 | `public`（默认）、`unlisted` 或 `private` |
| `summary` | 字符串 | 否 | 用于列表页面的人工智能生成的摘要（最多 500 个字符） |

**管理端点：**

| 端点 | 方法 | 说明 |
|----------|--------|-------------|
| `/entries?status=draft&q=keyword` | GET | 列出/搜索条目 |
| `/entries/:id` | GET | 获取单个条目 |
| `/entries/:id` | PATCH | 更新条目字段 |
| `/entries/:id` | DELETE | 永久删除条目 |
| `/entries/:id/publish` | POST | 发布草稿 |
| `/entries/:id/unpublish` | POST | 恢复为草稿状态 |
| `/site` | GET | 站点信息（用户名、条目数量等） |
| `/tags?sort=popular` | GET | 列出带有使用次数的标签 |
| `/categories` | GET | 列出带有条目数量的分类 |

> 完整的参数列表、响应格式和错误处理方式：请参阅 references/api.md

## 执行流程

每次执行 `/til` 命令时，都会遵循以下流程：

1. **生成** —— 创建 TIL 条目（标题、正文、摘要、标签、语言）
2. **检查令牌** —— 解析令牌（环境变量 → `~/.til/credentials` 中的激活配置文件）
   - 如果 `~/.til/credentials` 以旧纯文本格式存在，先将其迁移到 YAML 格式的 `default` 配置文件
   - **找到令牌** → 使用 `published: true` 发送到 API → 显示已发布的 URL
   - **未找到令牌** → 保存到 `~/.til/drafts/` → 显示首次使用的提示并提示重新连接
   - **收到 401 错误响应** → 保存到本地 → 提示重新认证（见错误处理部分）：
     - 从 `~/.til/credentials` 中获取令牌（激活配置文件的令牌）或没有令牌：提示通过设备流程重新连接 → 成功后，更新激活配置文件的令牌并自动重试原始操作
     - 从 `$OPENTIL_TOKEN` 环境变量中获取令牌：无法自动修复问题 —— 提示用户更新/删除该变量
3. **显示身份** —— 当配置了多个配置文件时，在结果消息中包含 `Account: @nickname (profile_name)`，以便用户始终知道使用了哪个账户
4. **内容永不丢失** —— 条目始终会被保存在某个地方
5. **API 失败** → 作为草稿保存到本地（作为备用）

## `/til <content>` —— 显式捕获

用户的输入是**原始素材** —— 是生成完整 TIL 条目的基础。根据输入生成完整的条目：

- 简短输入（一个句子或短语） → 扩展为包含上下文和示例的完整条目
- 长输入（一个段落或更多） → 优化并结构化内容，但保留用户的意图

**步骤：**

1. 将用户的输入视为生成完整条目的基础
2. 生成与内容相同语言的简洁标题（5-15 个单词）
3. 编写自包含的 Markdown 正文（见下文的内容指南）
4. 生成摘要（见下文的摘要指南）
5. 从技术领域推断出 1-3 个标签（例如 `rails`、`postgresql`、`go`）
6. 检测语言 → 设置 `lang`（`en`、`zh-CN`、`zh-TW`、`ja`、`ko`、`es`、`fr`、`de`、`pt-BR`、`pt`、`ru`、`ar`、`bs`、`da`、`nb`、`pl`、`th`、`tr`、`it`）
7. 遵循上述执行流程（检查令牌 → 发送 POST 请求或保存到本地）

无需确认 —— 用户明确要求捕获内容时直接执行。

## `/til` —— 从对话中提取内容

当不带参数使用 `/til` 时，会分析当前对话中值得记录的内容。

**步骤：**

1. 扫描对话中值得保存的知识点 —— 惊人的事实、有用的技巧、调试突破、灵光一现的时刻
2. 识别所有值得记录的 TIL 内容（不止一个），最多 5 个
3. 根据数量选择处理方式：

**0 个知识点：**
```
No clear TIL insights found in this conversation.
```

**1 个知识点：** 生成完整的草稿（标题、正文、标签），显示后请求用户确认。确认后继续执行上述流程。

**2 个或更多知识点：** 显示编号列表（最多 5 个），让用户选择：
```
Found 3 TIL-worthy insights:

  1. Go interfaces are satisfied implicitly
  2. PostgreSQL JSONB arrays don't support GIN @>
  3. CSS :has() enables parent selection

Which to capture? (1/2/3/all/none)
```

- 单个数字 → 为该知识点生成草稿，显示后请求确认，然后继续执行
- 逗号分隔的列表（例如 `1,3`） → 为选中的知识点生成草稿，显示所有草稿后请求确认，然后依次发送 POST 请求
- `all` → 为每个知识点生成草稿，显示所有草稿后请求确认，然后依次发送 POST 请求
- `none` → 取消操作

4. 对于每个选中的知识点，根据内容指南生成独立的 TIL 条目
5. 向用户展示生成的条目并请求确认，然后继续执行上述流程

## 自动检测

在与用户协作时，主动检测值得记录为 TIL 的内容。

### 何时建议生成 TIL 条目

在对话中出现真正的“灵光一现”时刻时建议生成 TIL 条目 —— 例如：
- 调试过程中发现了意想不到的根本原因
- 语言/框架的行为与常见假设相反
- 重构揭示了明显更优的模式
- 性能优化带来了可衡量的改进
- 发现了不常见但有用的工具或 API 参数

**不建议生成 TIL 条目的情况：**
- 标准工具的使用
- 已有文档记录的行为
- 由拼写错误引起的错误
- 广为人知的最佳实践

### 限制策略

1. **每个会话仅建议一次** —— 建议一次后（无论是否接受），不再建议
2. **仅在适当的时机建议** —— 在问题解决过程中或任务转换时建议，不要在问题解决过程中建议
3. **尊重用户的拒绝** —— 如果用户拒绝，不再建议

### 建议格式

在正常响应的末尾添加建议内容。不要打断用户的工作流程。

**示例**（在调试响应的末尾）：
```
...so the fix is to close the channel before the goroutine exits.

💡 TIL: Unclosed Go channels in goroutines cause silent memory leaks
   Tags: go, concurrency · Capture? (yes/no)
```

### 捕获流程

自动检测到的 TIL 条目会跳过提取流程。建议内容本身就是待记录的内容。

1. 用户回复 `yes` / `y` / `ok` / `sure` → 代理根据建议的内容生成完整的条目（标题、正文、标签、语言），然后继续执行上述流程（发送 POST 请求或保存到本地）
2. 用户回复 `no` / 忽略 / 继续讨论其他话题 → 继续对话，不再建议

非确认的回复（继续讨论其他话题）被视为默认的拒绝。

> 详细的触发条件示例、状态机和避免错误的策略：请参阅 references/auto-detection.md

## 管理子命令

管理子命令需要令牌。没有本地备份机制 —— 管理操作需要通过 API 完成。

### `/til list [drafts|published|all]`

列出条目。默认过滤条件：`drafts`。

- API：`GET /entries?status=<filter>&per_page=10`
- 以紧凑的表格形式显示条目（显示前 8 个字符的简短 ID）
- 在底部显示分页信息

### `/til publish [<id> | last]`

发布草稿条目。

- `last` 表示当前会话中最新创建的条目（通过每次成功发送 POST 请求时设置的 `last_created_entry_id` 追踪）
- 首先获取条目，显示标题/标签，然后请求用户确认
- 成功后，显示已发布的 URL
- 如果条目已经发布，显示信息性消息（不是错误提示）

### `/til unpublish <id>`

将已发布的条目恢复为草稿状态。

- 首先获取条目，确认后取消发布
- 如果条目已经是草稿状态，显示信息性消息

### `/til edit <id> [instructions]`

对现有条目进行人工智能辅助编辑。

- 通过 `GET /entries/:id` 获取完整条目
- 根据提供的指令进行修改（如果没有提供指令，询问需要修改的内容）
- 显示修改内容的差异预览
- 确认后，使用 `PATCH /entries/:id` 发送 POST 请求

### `/til search <keyword>`

按标题搜索条目。

- API：`GET /entries?q=<keyword>&per_page=10`
- 显示与 `list` 相同的紧凑表格格式

### `/til delete <id>`

永久删除条目。

- 获取条目，显示标题和状态
- 二次确认：“此操作不可撤销。请输入 ‘delete’ 以确认。”
- 确认后，使用 `DELETE /entries/:id` 删除条目

### `/til status`

显示站点状态和连接信息。**无需令牌也可使用**（显示简化版本）。

- 使用令牌时：`GET /site` → 显示用户名、条目数量（已发布/草稿数量）、令牌状态、本地草稿数量、仪表板链接
- 无需令牌时：显示“未连接”、本地草稿数量、设置链接

### `/til sync`

将 `~/.til/drafts/` 中的本地草稿显式同步到 OpenTIL。需要令牌。

- 列出待同步的草稿，逐个发送 POST 请求，成功后删除本地文件
- 显示每个草稿的同步结果

### `/til tags`

按使用次数排序显示站点标签（前 20 个）。需要令牌。

- API：`GET /tags?sort=popular&per_page=20&with_entries=true`
- 以紧凑的表格形式显示标签名称和条目数量

### `/til categories`

列出站点分类。需要令牌。

- API：`GET /categories`
- 以紧凑的表格形式显示分类名称、条目数量和描述

### `/til batch <topics>`

一次操作批量捕获多个 TIL 条目。需要提供具体的主题列表。

- 用户用换行符、分号或 markdown 列表项（`-` / `1.`）分隔主题列表
- 为每个主题生成草稿 → 显示所有草稿后请求确认，然后依次发送 POST 请求
- 部分失败时，显示每个草稿的同步结果（与 `/til sync` 的格式相同）

### ID 解析

- 在列表中，以简短形式显示 ID：`...` + 最后 8 个字符
- 接受简短 ID 和完整 ID 作为输入
- 通过后缀匹配当前列表中的 ID 来解析简短 ID
- 如果存在多个匹配项，请求用户确认

### 会话状态

跟踪以下会话状态（不会在会话之间保留）：
- `last_created_entry_id` —— 每次成功发送 `POST /entries` 时设置（用于 `/til publish last`）
- `active_profile` —— 第一次访问令牌时解析的配置文件名。反映 `~/.til/credentials` 中的 `active` 字段（或 `$OPENTIL_TOKEN` 的设置）。用于显示身份和草稿归属

> 详细的子命令流程、显示格式和错误处理方式：请参阅 references/management.md

## 代理身份

通过三层归属信号区分用户发起和代理发起的 TIL 条目。

### 第一层：HTTP 标头

在每次 API 调用时包含以下标头：

```
X-OpenTIL-Source: human | agent
X-OpenTIL-Agent: <your agent display name>
X-OpenTIL-Model: <human-readable model name>
```

- 来源：`/til <content>` 和 `/til` → `human`；自动检测到时 → `agent`
- 代理：使用您的工具的显示名称（例如 `Claude Code`、`Cursor`、`GitHub Copilot`）。不要使用 slug。
- 模型：使用人类可读的模型名称（例如 `Claude Opus 4.6`、`GPT-4o`、`Gemini 2.5 Pro`）。不要使用模型 ID。
- 代理和模型是可选的 —— 如果不确定可以省略。

### 第二层：标签约定

- 自动检测到的 TIL 条目：自动在标签列表中添加 `agent-assisted`
- `/til <content>` 和 `/til`：**不要** 添加该标签（除非代理大幅修改了内容）

### 第三层：归属显示（后端）

代理发起的 TIL 条目在 OpenTIL 上会自动标记：
- 公开页面：显示 `✨ via {agent_name}`，或当 `agent_name` 不存在时显示 `✨ AI`
- 提示框（悬停时）：当两者都存在时显示 `{agent_name} · {model}`

**注意**：不要在内容正文中添加任何页脚或归属信息。

## 内容指南

每个 TIL 条目都必须遵循以下规则：

- **自包含**：读者无需任何对话背景即可理解条目内容。不要写“正如我们讨论的”、“上述错误”、“该项目的配置”等。
- **去个性化**：删除项目名称、公司细节、同事姓名、内部 URL 和专有业务逻辑。将具体信息泛化：例如将“我们的 User 模型”改为“一个模型”，将“生产服务器”改为“生产环境”，将“Acme 支付服务”改为“支付网关”。
- **通用价值**：遵循 StackOverflow 的答案标准。对于搜索该主题的陌生人来说，条目应该立即有用。仅对作者有用的内容应保存在私人笔记中，而不是 TIL 中。
- **事实性表达**：陈述事实，提供示例，解释原因。避免使用第一人称叙述（例如“我在调试...”）。例外情况：在解释原因时可以使用简短的情境描述（例如“在将 Rails 从 7.2 升级到 8.0 时...”）。
- **每个条目一个知识点**：每个 TIL 条目只教授一个知识点。如果有多个知识点，创建单独的条目。
- **具体示例**：根据需要包含代码片段、命令或具体数据。避免使用模糊的描述。
- **标题**：5-15 个单词。标题要具有描述性，与内容使用相同的语言。不要使用 “TIL:” 前缀。
- **内容**：使用最有效的格式呈现内容 —— 使用表格展示比较内容，使用代码块展示示例，使用列表展示枚举内容，使用 `$inline$` / `$$display$$` 展示公式（包含分数/下标/上标/希腊字母），使用 Mermaid 图表展示流程/状态/序列（如果文本无法清晰表达）。如果只需要简单表达，则使用纯文本。只有在解释因果关系或背景信息时使用数学表达式。如果一句话足够表达，请不要写成段落。
- **标签**：从技术领域选择 1-3 个 lowercase 标签（例如 `rails`、`postgresql`、`css`、`linux`）。不要使用通用标签，如 `programming` 或 `til`。
- **语言**：根据内容自动检测语言。中文 → `zh-CN`，繁体中文 → `zh-TW`，英文 → `en`，日文 → `ja`，韩文 → `ko`。
- **分类**：除非用户明确指定了分类/主题，否则不要自动添加 `category_name`。
- **摘要**：1-2 句简短文本（不含 Markdown 格式）。摘要最多 500 个字符，并且长度应短于正文。摘要必须能够独立传达核心信息。明确说明读者将学到什么，避免使用元描述。如果内容已经很短（少于 200 个字符），可以使用摘要代替。

## 结果消息

### API 成功（配置了令牌，201）

```
Published to OpenTIL

  Title:  Go interfaces are satisfied implicitly
  Tags:   go, interfaces
  URL:    https://opentil.ai/@username/go-interfaces-are-satisfied-implicitly
```

当配置了多个配置文件时，会添加 `Account` 行：

```
Published to OpenTIL

  Account: @hong (personal)
  Title:   Go interfaces are satisfied implicitly
  Tags:    go, interfaces
  URL:     https://opentil.ai/@hong/go-interfaces-are-satisfied-implicitly
```

单配置文件用户看不到 `Account` 行 —— 保持输出简洁。

从 API 响应中提取 `url` 字段以获取 URL。

### 同步本地草稿

在第一次成功的 API 调用后，检查 `~/.til/drafts/` 文件中是否有待同步的文件。如果有文件，提供同步选项：

```
Draft saved to OpenTIL

  Title:  Go interfaces are satisfied implicitly
  Tags:   go, interfaces
  Review: https://opentil.ai/@username/go-interfaces-are-satisfied-implicitly

Found 3 local drafts from before. Sync them to OpenTIL?
```

用户确认后，将每个草稿发送到 API。每次同步成功后删除本地文件。如果同步失败，显示摘要：

```
Synced 3 local drafts to OpenTIL

  + Go defer runs in LIFO order
  + PostgreSQL JSONB indexes support GIN operators
  + CSS :has() selector enables parent selection
```

如果用户拒绝，保留本地文件，并在此会话中不再提示同步。

### 首次运行（没有令牌）

将草稿保存到本地，然后主动提供连接提示。这不是错误 —— 用户成功捕获了 TIL 内容。

```
TIL captured

  Title:  Go interfaces are satisfied implicitly
  Tags:   go, interfaces
  File:   ~/.til/drafts/20260210-143022-go-interfaces.md

Connect to OpenTIL to publish entries online.
Connect now? (y/n)
```

- 用户回复 `y` → 执行设备流程（与 `/til auth` 相同） → 成功后，同步刚刚保存的草稿以及 `~/.til/drafts/` 中的其他待同步草稿
- 用户回复 `n` → 显示手动设置说明（见下文的手动设置说明）

仅在 **首次** 本地保存时显示连接提示。在后续保存时，使用简短格式（不再显示提示）：

```
TIL captured

  Title:  Go interfaces are satisfied implicitly
  Tags:   go, interfaces
  File:   ~/.til/drafts/20260210-143022-go-interfaces.md
```

## 错误处理

**在任何 API 失败时，首先将草稿保存到本地。** 不要丢失用户的任何内容。

**422 — 验证错误**：分析错误响应，解决问题（例如将标题截断为 200 个字符，修正语言代码），然后重试。如果重试仍然失败，才保存到本地。

**401 — 令牌无效或过期（来自 `~/.til/credentials` 中的激活配置文件的令牌）：**

```
TIL captured (saved locally)

  File: ~/.til/drafts/20260210-143022-go-interfaces.md

Token expired for @hong (personal). Reconnect now? (y/n)
```

- 用户回复 `y` → 执行设备流程（与 `/til auth` 相同） → 成功后，更新 `~/.til/credentials` 中的激活配置文件的令牌，并自动重试原始 POST 请求（发布刚刚保存的草稿，然后删除本地文件）
- 用户回复 `n` → 显示手动设置说明（见下文的手动设置说明）

当只配置了一个配置文件时，从消息中省略 `@nickname (profile)`。

**401 — 令牌无效或过期（来自 `$OPENTIL_TOKEN` 环境变量）：**

环境变量的优先级高于 `~/.til/credentials` 中的令牌，因此通过设备流程保存新令牌无效 —— 用户仍然会使用环境变量中的令牌。在这种情况下，指导用户更新环境变量：

```
TIL captured (saved locally)

  File: ~/.til/drafts/20260210-143022-go-interfaces.md

Your $OPENTIL_TOKEN is expired or invalid. To fix:
  • Update the variable with a new token, or
  • unset OPENTIL_TOKEN, then run /til auth

Create a new token: https://opentil.ai/dashboard/settings/tokens
```

**网络故障或 5xx 错误：**

> 完整的错误代码、422 错误自动修复逻辑和速率限制详情：请参阅 references/api.md

### 重新认证保护措施

| 规则 | 行为 |
|------|----------|
| 无重试循环 | 如果重试成功但仍然返回 401 错误，则停止并显示错误。不要再次尝试重新认证。 |
| 批量操作时考虑重试 | 在批量/同步操作期间，最多重试一次。成功后，继续使用新的令牌处理剩余的条目。 |
| 尊重用户的拒绝**：** 如果用户拒绝重新认证（回复 `n`），则在此会话中不再提示重新认证。 |
| 注意环境变量**：** 当激活令牌来自 `$OPENTIL_TOKEN` 时，不要尝试通过设备流程重新认证 —— 因为环境变量具有优先权。始终显示环境变量的提示。 |
| 考虑配置文件信息**：** 当重新认证成功时，更新 `~/.til/credentials` 中相应配置文件的令牌。不要创建新的配置文件。 |

### 手动设置说明

当用户拒绝自动认证（回复 `n`）时，显示以下提示：

```
Or set up manually:
  1. Visit https://opentil.ai/dashboard/settings/tokens
  2. Create a token (select read + write + delete scopes)
  3. Add to shell profile:
     export OPENTIL_TOKEN="til_..."
```

## 本地草稿备份

当 API 不可用或未配置令牌时，草稿会保存在 `~/.til/drafts/` 文件中。

**文件格式：** `YYYYMMDD-HHMMSS-<slug>.md`

**profile` 字段记录了保存时的激活配置文件名称，确保同步使用正确的账户令牌。如果没有配置配置文件，则省略此字段（保持向后兼容性）。

> 完整的目录结构、元数据字段和同步协议：请参阅 references/local-drafts.md

## 注意事项

- **UI 语言适配**：本文档中的所有提示、结果信息和错误消息都以英文编写作为示例。在运行时，根据用户当前会话的语言进行适配（例如，如果用户使用中文，显示中文消息）。条目内容的语言（`lang` 字段）是独立的 —— 它总是从内容本身检测出来的。
- 条目默认会立即发布（`published: true`） —— 使用 `/til unpublish <id` 将条目恢复为草稿状态
- API 会从标题自动生成 URL slug
- 如果站点上不存在标签，会自动创建标签
- 内容会在服务器端渲染（使用 GFM Markdown 格式，支持语法高亮、KaTeX 数学公式和 Mermaid 图表）
- 管理子命令（`list`、`publish`、`edit`、`search`、`delete`、`tags`、`categories`、`sync`、`batch`）需要令牌 —— 没有本地备份机制。例外情况：`status` 和 `auth`（包括 `auth switch`、`auth list`、`auth remove`、`auth rename`）无需令牌即可使用。
- 权限范围错误对应特定的操作：`list`/`search`/`tags`/`categories` 需要 `read:entries`，`publish`/`unpublish`/`edit`/`sync`/`batch` 需要 `write:entries`，`delete` 需要 `delete:entries`。`status` 在有令牌的情况下使用 `read:entries`，但在没有令牌的情况下也可以使用。
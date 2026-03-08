---
name: mindgraph
version: 5.0.6
description: "具有18种认知工具的结构化知识图谱，用于代理的记忆和推理（服务器版本v0.8.0）"
author: shuruheel
---
# MindGraph 技能

MindGraph 是一个用于子代理、跨文件约束查询和语义搜索的 **结构化知识图谱索引**。所有文件（如 MEMORY.md 和每日笔记）都是规范的格式——MindGraph 会在这些文件的基础上提供结构化关系和搜索功能。

---

## 设置：云环境 vs 本地环境

MindGraph 可以作为 **云 API** 或 **本地自托管服务器** 运行。您可以通过设置两个环境变量来选择运行方式：

### 云 API（推荐）：无需安装服务器或二进制文件，嵌入模型已包含
```bash
export MINDGRAPH_URL=https://api.mindgraph.cloud
export MINDGRAPH_TOKEN=your-api-key   # from mindgraph.cloud/signup
```
- 无需安装或启动任何二进制文件
- 嵌入模型由服务器端处理，因此不需要 `OPENAI_API_KEY`
- 当 `MINDGRAPH_URL` 以 `https://` 开头时，`start.sh` 脚本不会执行任何操作

### 本地服务器（自托管）
```bash
bash install.sh       # downloads pre-built binary from GitHub Releases
bash start.sh         # starts server on port 18790
export OPENAI_API_KEY=sk-...   # required for semantic/hybrid search
```
- 默认运行在 `http://127.0.0.1:18790` 上
- 首次启动时，会自动生成令牌并保存到 `data/mindgraph.json` 文件中
- `MINDGRAPH_TOKEN` 会自动从 `data/mindgraph.json` 中读取

### 环境变量
| 变量 | 是否必填 | 说明 |
|---|---|---|
| `MINDGRAPH_TOKEN` | 必填 | 用于身份验证的令牌/API 密钥 |
| `MINDGRAPH_URL` | 仅适用于云环境 | 设置为 `https://api.mindgraph.cloud` |
| `OPENAI_API_KEY` | 仅适用于本地环境 | 用于语义搜索或混合搜索 |

---

## 文件结构

所有文件路径均以技能根目录（`skills/mindgraph/`）为基准：

| 文件 | 用途 |
|---|---|
| `mindgraph-client.js` | 标准的客户端库。所有脚本都从此文件导入。工作区根目录下有该文件的符号链接。 |
| `mindgraph-bridge.js` | 用于 OpenClaw 会话的 CLI 桥接器和批量写入工具。工作区根目录下有该文件的符号链接。 |
| `mg-context.js` | 用于快速检索对话内容（结合 FTS、语义分析和子图功能）。工作区根目录下有该文件的符号链接。 |
| `entity-resolution.js` | 五步实体去重模块（缓存 → 别名 → 模糊匹配 → FTS → 语义分析）。 |
| `extract.js` | 从文本中提取信息并生成结构化 JSON 数据（节点和边）。 |
| `import.js` | 通过认知层接口将提取的 JSON 数据导入图谱。 |
| `re-embed.js` | 重新生成图谱的嵌入信息（包括标签、摘要和上下文）。 |
| `dedup.js` | 合并具有相同标签的重复节点（不区分大小写）。 |
| `flatten_transcript.py` | 将 JSONL 会话记录转换为纯文本以便进一步处理。 |
| `SCHEMA.md` | 完整的节点类型和边类型定义（53 种节点类型，16 种以上边类型）。 |
| `start.sh` / `install.sh` | 用于管理服务器的生命周期。 |
| `dreaming/` | 包含夜间分析脚本（如 dream-analysis.js、apply-proposals.js 等）。 |

---

## 设计规范

1. **代理身份**：在记录更改时，始终使用 `agent_id: 'jaadu'`（或上下文相关的标识符）作为来源信息。
2. **原子性操作**：使用 `/epistemic/argument`、`/action/procedure`、`/agent/plan` 等接口，在一次操作中创建相关的节点和边。
3. **写入规则**：在修改行为规则之前，先写入 `/memory/config` 或 `/agent/governance` 文件。
4. **会话管理**：在每次对话开始时，调用 `POST /memory/session (action: open)`，并使用 `session_uid` 进行会话追踪和数据提取。
5. **`props` 深度合并**（v0.8.0）：所有认知接口都支持 `props` 字段。服务器会将该字段中的用户提供的数据与默认值进行深度合并。
6. **实体类型**（v0.8.0）：在创建实体时，需要在 `props` 对象中指定 `entity_type`。`mgmanageEntity()` 函数会自动处理这一过程。
7. **重试机制**（v5.0.6）：对于 502/503/504 错误以及临时网络错误（如 ECONNRESET、ECONNREFUSED），客户端会自动尝试最多 3 次，并采用指数级退避策略进行重试。

---

## 各工具的使用场景（决策指南）

### 数据检索：从图谱中获取信息

| 情况 | 使用工具 | 示例 |
|---|---|---|
| 对话中提到的人或公司 | `mg-context.js --entity "name"` | `node mg-context.js --entity "Aaron Goh"` |
| 普通主题查询 | `mg-context.js "topic"` | `node mg-context.js "Iran regime"` |
| 精确标签搜索 | `mg-context.js --fts "label"` | `node mg-context.js --fts "Income Generation"` |
| 探索节点的上下文信息 | `mg-context.js --neighborhood <uid>` | `node mg-context.js --neighborhood 01HRX...` |
| 程序化搜索（在脚本中） | `mg.search(query)` 或 `mg.hybridSearch(query)` | — |
| 语义相似性查询 | `mg.retrieve('semantic', { query })` | — |
| 活动目标/任务/问题 | `mg.retrieve('active_goals')` 等 | — |

**规则**：当提到具体的人或公司名称时，务必在响应前先进行检索。这个操作非常快速（<2 秒）。

### 数据写入：更新图谱

| 触发条件 | 使用工具 | 代码示例 |
|---|---|---|
| 做出/确认决策 | `mg.deliberate` | `mg.deliberate({ action: 'open_decision', label, description })`，然后 `mg.deliberate({ action: 'resolve', decisionUid, resolutionRationale })` |
| 规定硬性规则（例如“永远不要做 X”） | `mg.governance` | `mg.governance({ action: 'create_policy', label, policyContent })` |
| 执行任务 | `mg.plan` | `mg.plan({ action: 'create_task', label, description })` |
| 表达偏好 | `mg.memoryConfig` | `mg.memoryConfig({ action: 'set_preference', label, value })` |
| 新创建的人/组织/工具 | `mg.manageEntity` | `mg.manageEntity({ action: 'create', label, entityType })` | 该操作会自动去重 |
| 值得保存的观察结果 | `mg.ingest` | `mg.ingest(label, content, 'observation')` |
| 有证据支持的声明 | `mg.addArgument` | `mg.addArgument({ claim: { label, content }, evidence: [...], warrant: { label, explanation } })` |
| 发现异常/错误 | `mg.addInquiry` | `mg.addInquiry(label, details, 'anomaly')` |
| 更新目标进展 | `mg.evolve` | `mg.evolve('update', uid, { propsPatch: { progress: 0.5 } })` |
| 结构模式/概念 | `mg.addStructure` | `mg.addStructure(label, content, 'pattern')` |

**写入标准**：即使在没有聊天记录的情况下，7 天后这些信息是否仍有用？如果有用，就将其写入图谱。

**标签规范**：标签应为简短的名词短语，最长 60 个字符，类似于维基百科文章标题。
- ✅ “MindGraph 端口决策”
- ❌ “决定将 MindGraph 端口设置为 8766。状态已更新...”

**禁止写入的内容**：常规消息、心跳确认信息、搜索结果，以及已经存在于 MEMORY.md 中的内容。

### 会话管理（主要会话流程）

---

## 重要判断（用于决策）

对于市场评估、产品规划决策或工作机会评估：

---

## 认知层接口（18 个工具）

### 现实层（原始输入）
- **POST /reality/ingest**：用于捕获信息来源（网页/文档/书籍）、片段内容（自动链接到来源），或观察结果。支持可选的 `props` 以进行深度合并。
- **POST /reality/entity**：用于创建实体（通过 `find_or_create_entity` 实现去重；支持别名匹配和不区分大小写的匹配，返回 `{node, created: bool}`；需要在 `props` 中指定 `entity_type`）、`alias`、`resolve`、`fuzzy_resolve`、`merge` 或 `relate`（在 `source_uid` 和 `target_uid` 之间创建边）。

### 认知层（推理）
- **POST /epistemic/argument**：用于创建 `Claim`（声明）、`Evidence`（证据）、`Warrant`（依据）和 `Argument`（论据）节点，并建立相应的边。
- **POST /epistemic/inquiry**：用于记录假设、异常、问题或开放性问题。
- **POST /epistemic/structure**：用于明确概念、模式、机制、模型、范式、类比、定理或方程式。

### 意图层（决策制定）
- **POST /intent/commitment**：用于声明目标、项目或里程碑。
- **POST /intent/deliberation**：用于管理决策过程（如 `open_decision`、`add_option`、`add_constraint` 或 `resolve`）。

### 行动层（工作流程）
- **POST /action/procedure**：用于设计工作流程（如 `create_flow`、`add_step`、`add_affordance` 或 `add_control`）。
- **POST /action/risk**：用于评估节点的严重性或可能性，或获取评估结果。

### 记忆层（数据持久化）
- **POST /memory/session**：用于打开会话、记录会话内容（实时记录）、关闭会话（设置 `ended_at`），或创建会话日志。
- **POST /memory/distill**：将会话内容整合为持久的 `Summary` 节点。
- **POST /memory/config**：用于设置偏好设置、策略配置或获取偏好信息。

### 代理层（控制）
- **POST /agent/plan**：用于创建任务、计划或更新任务状态。
- **POST /agent/governance**：用于创建策略、设置预算或请求审批。
- **POST /agent/execution**：用于启动任务、完成任务或注册代理。

### 连接层
- **POST /retrieve**：提供统一的搜索功能（包括文本搜索、语义搜索、混合搜索（RRF 融合，k=60）、活动目标、未解决的问题、最近的操作等）。
- **POST /traverse**：用于导航（如链式查询、节点邻域、路径查找、子图分析）。
- **POST /evolve**：用于更新节点状态（如 `update`、`tombstone`、恢复、衰减、历史记录、快照等）。

---

## 客户端 API（mindgraph-client.js）

---

## 数据提取流程

### 完整的数据提取流程（用于心跳更新和会话结束时的数据写入）：
```bash
# 1. Flatten transcript to plain text
python3 flatten_transcript.py <session.jsonl> --since-minutes 60 --output /tmp/conv.txt

# 2. Extract structured nodes/edges via LLM
node extract.js /tmp/conv.txt --output /tmp/extracted.json

# 3. Import into graph via cognitive layer
node import.js /tmp/extracted.json
```

### 数据提取模型选择：
- 文件大小小于 20KB → 使用 `gemini-3-flash-preview`（快速且成本低）
- 文件大小大于 20KB → 使用 `gemini-3-pro-preview`（生成更详细的输出）
- 文件大小大于 40KB → 先使用 Flash 进行自动摘要处理，然后再进行提取

### 实体解析（在提取过程中）：
提取完成后，通过 `entity-resolution.js` 进行实体解析：
1. 使用已知的别名映射。
2. 使用 `fuzzy_resolve` API 进行匹配。
3. 进行 FTS（Full Text Search）精确匹配。
4. 根据语义相似度进行筛选（阈值 0.85）。

---

## 维护脚本

| 脚本 | 功能 | 运行时机 |
|---|---|---|
| `dedup.js` | 合并具有相同标签的节点（按 `node_type::label` 分组）。 | 在批量导入数据后运行。 |
| `re-embed.js` | 为所有节点重新生成图谱相关的嵌入信息。 | 在图谱架构更改后定期运行。 |
| `reindex-search.js` | 重建 FTS 索引。 | 在服务器升级后运行。 |
| `maintenance.js` | 执行批量监控和提取触发任务。 | 通过心跳机制自动触发。 |

---

## 子代理的使用方式

子代理不应直接访问 MEMORY.md 文件，而应使用以下方法：
- 使用 `mgretrieve` 和 `mg.traverse` 来获取上下文信息。
- 使用 `mg.search` 进行快速查询。
- 在每次请求时都必须传递 `agentId` 以追踪数据来源。

---

## 完整的图谱结构参考

请参阅 `SCHEMA.md` 文件，其中包含所有节点类型、边类型的定义以及关键区分规则。

### 常见错误说明：
1. **声明（Claim）与观察（Observation）**：例如：“X 发生在 Y 日期”属于观察结果；“X 目前是正确的”属于声明。
2. **声明（Claim）与决策（Decision）**：例如：“BCG X 是首要任务”属于决策；“BCG X 是一家咨询公司”属于声明。
3. **声明（Claim）与约束（Constraint）**：例如：“永远不要预先支付薪资”属于约束（`hard=true`）。
4. **声明（Claim）与偏好（Preference）**：例如：“Shan 喜欢简洁的回复”属于偏好设置。
5. **声明（Claim）与模式（Pattern）**：例如：“Axum 0.7 使用 :param 语法”属于可推广的经验。

### FTS 可搜索性
FTS 索引可以搜索用户生成的所有文本（涵盖 35 个以上的字符串字段），而不仅仅是标签和摘要。可以使用 `mg.search()` 或 `mg.hybridSearch()` 进行搜索。

### 实体去重
使用 `mg.findOrCreateEntity(label, entityType)` 进行实体创建。在创建实体之前，系统会检查别名并进行不区分大小写的匹配。

### 混合检索
`mg.hybridSearch(query, opts)` 可以结合 FTS 和向量搜索结果进行检索。建议使用此方法，而不是分别调用 `search()` 和 `retrieve()`。
---
name: mindgraph
version: 5.0.0
description: "一个包含18种认知工具的结构化知识图谱，用于代理的记忆和推理功能。"
author: shuruheel
---
# MindGraph 技能

MindGraph 是一个用于子代理、跨文件约束查询和语义搜索的 **结构化知识图谱索引**。所有文件（如 MEMORY.md 和每日笔记）都是规范化的数据源——MindGraph 会在这些文件的基础上提供结构化的关系和搜索功能。

---

## 设计规范

1. **代理身份**：始终传递 `agent_id: 'jaadu'`（或在相应上下文中使用 `claude`），以确保 `changed_by` 的来源信息准确无误。
2. **原子性操作**：使用捆绑端点（`/epistemic/argument`、`/action/procedure`、`/agent/plan`）在单次事务中创建相关的节点和边。
3. **操作说明**：在写入 `/memory/config` 或 `/agent/governance` 之前，先进行必要的操作说明，因为这些操作会修改行为规则。
4. **会话管理**：在每次对话开始时，调用 `POST /memory/session (action: open)`，并使用 `session_uid` 来记录会话信息并进行后续处理。

---

## 认知层端点（18 个工具）

### 现实层（原始输入）
- **POST /reality/ingest**：捕获来源（网页、论文、书籍）、片段（自动链接到来源内容）或观察结果。
- **POST /reality/entity**：通过 `find_or_create_entity` 进行去重处理后创建实体节点（返回 `{node, created: bool}`）；支持别名处理、不区分大小写的匹配；提供 `alias`、`resolve`、`fuzzy.resolve` 和 `merge` 等操作。

### 认知层（推理）
- **POST /epistemic/argument**：创建包含 `Claim`（主张）、`Evidence`（证据）、`Warrant`（依据）和 `Argument`（论证）的节点，并建立相应的边（如 `Supports`、`HasWarrant`、`HasPremise` 和 `HasConclusion`）。
- **POST /epistemic/inquiry**：记录假设、异常情况、前提或问题；处理相关的边（如 `AnomalousTo`、`Tests` 和 `Addresses`）。
- **POST /epistemic/structure**：固化概念、模式、机制、模型、类比、定理或方程；建立 `AnalogousTo` 和 `TransfersTo` 等边。

### 意图层（承诺）
- **POST /intent/commitment**：声明目标或项目；在创建目标/项目之前进行提案。
- **POST /intent/deliberation**：管理开放决策、添加选项、添加约束或解决问题（创建 `DecidedOn` 边）。

### 行动层（工作流程）
- **POST /action/procedure**：设计工作流程（`create_flow`）、添加步骤（`add_step`）、添加便利性（`add_affordance`）或添加控制（`add_control`）；建立相应的边（如 `ComposedOf`、`StepUses`、`Controls`）。
- **POST /action/risk**：评估节点的严重性或发生概率；获取评估结果。

### 记忆层（持久化）
- **POST /memory/session**：打开会话、记录会话内容（实时记录）或关闭会话（生成摘要链接）。
- **POST /memory/distill**：将会话内容整合为持久的 `Summary` 节点。
- **POST /memory/config**：设置偏好设置、策略或获取偏好设置。

### 代理层（控制）
- **POST /agent/plan**：创建任务、制定计划或更新状态。
- **POST /agent/governance**：创建策略、设置预算、请求批准或处理批准请求。
- **POST /agent/execution**：启动任务、完成任务、标记任务失败或注册新代理。

### 记忆层 — 日志（版本 0.5.6）
- 通过 `POST /node` 创建日志节点，指定 `node_type: "Journal"`；属性包括 `content`、`session_uid`、`journal_type`（笔记/调查/调试/推理）和 `tags`。
- 使用 `Follows` 边来表示日志节点之间的时间顺序（用于调试和推理链的追踪）。

### 连接层
- **POST /retrieve**：提供多种搜索模式：文本搜索、语义搜索、混合搜索（结合 FTS 和向量算法，k=60；若没有嵌入信息则仅使用 FTS）；支持搜索开放性问题、待审批的请求、最近的操作等。
- **POST /traverse**：提供导航模式：链式搜索、邻域搜索、路径搜索、子图搜索。
- **POST /evolve**：提供操作功能：更新节点属性（`update`，返回 422 错误代码表示字段无效）、恢复节点状态、删除节点、查看历史记录或生成快照。

### 全文 FTS（版本 0.5.2）
FTS 索引覆盖用户编写的 **所有文本**，包括 35 个字符串字段和 43 个 `Vec<String>` 类型字段（不仅仅是标签和摘要）；在插入或更新时自动进行索引；升级后运行 `node reindex-search.js` 以重新索引现有节点。

---

## 客户端 API（mindgraph-client.js）

客户端库封装了上述所有认知层端点的功能。详细的方法签名请参见 `mindgraph-client.js`。

```javascript
const mg = require('./mindgraph-client.js');
// Example: Atomic Toulmin Bundle
await mg.addArgument({
  claim: { label: "Succession crisis likely", content: "Khamenei's death creates a power vacuum" },
  evidence: [{ label: "IRGC mobilization", description: "Reports of IRGC units entering Tehran" }],
  warrant: { label: "Historical precedent", explanation: "Regime transitions in Iran are often IRGC-led" }
});

// Phase 0.5 additions:
await mg.addJournal("Debug: propsPatch issue", "Full investigation notes...", { journalType: 'investigation', tags: ['bug'] });
await mg.hybridSearch("propsPatch validation", { limit: 5 });  // Server-side RRF
await mg.findOrCreateEntity("Aaron Goh", "Person");  // Dedup-safe
await mg.addFollowsEdge(journalUid1, journalUid2);   // Temporal chain
```
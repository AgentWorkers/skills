---
name: smart-memory-query
description: "强制使用主动式、经过优化的 `memory_search` 查询方法。在以下情况下必须运行 `memory_search`：  
(1) 当引用到先前的上下文时；  
(2) 当开始新的任务时；  
(3) 当出现专有名词时。  
通过拆分查询意图，构建长度为 2–4 个词元的简短查询，以避免基于 `AND` 的全文搜索（FTS）返回空结果。"
always: true
---
# 智能记忆查询

## 触发条件：在满足以下任一条件时运行 `memory_search`：

- **T1（先前上下文）**：用户提及之前的决策、协议或历史记录（例如：“我们之前是这么决定的”）。
- **T2（新任务）**：在开始新任务之前，检查之前的偏好设置或决策。
- **T3（专有名词）**：出现项目名、工具名、服务名或人名。

如果不确定，请进行搜索。错过相关信息会导致需要多次额外搜索。如果同时满足多个触发条件，请针对每个条件分别进行搜索。

## 构建查询的规则（必须遵守）：

1. **分解搜索意图**：将搜索意图分解为2-3个独立的方面。不要在一个查询中包含过多的信息。
2. **提取核心关键词**：每个方面只保留2-3个关键名词，并优先考虑专有名词。
3. **执行多次查询**：针对每个方面分别调用 `memory_search`，每个查询使用2-4个关键词。
4. **合并结果**：如果所有查询都未返回结果，尝试用一个关键专有名词重新搜索一次。

## 示例：

**T1** “我们之前决定保留iCloud下载功能，对吧？”
- ❌ `memory_search("user preference root-cause config first suggestion keep iCloud downloads")`
- ✅ `memory_search("iCloud download setting")` + `memory_search("problem-solving preference")`

**T1** “我们之前不是计划先迁移到更好的结构吗？”
- ❌ `memory_search("better structure migration FTS path title RRF exact tie-break")`
- ✅ `memory_search("FTS structure migration")` + `memory_search("RRF tie-break design")`

**T2** “让我们开始Paddle支付功能的集成吧。”
- ❌ `memory_search`
- ✅ `memory_search("Paddle payment")` + `memory_search("payment integration decision")`

**T3** “OpenClaw的搜索质量仍然很差。”
- ❌ `memory_search("OpenClaw search quality is still poor")`
- ✅ `memory_search("OpenClaw search")` + `memory_search("search quality tuning")`

**T1+T3** “切换到bge-m3之后发生了什么？”
- ❌ `memory_search("what happened after switching to bge-m3")`
- ✅ `memory_search("bge-m3 migration result")` + `memory_search("embedding model change")`

**T2** “设置新的项目文档结构。”
- ❌ `memory_search`
- ✅ `memory_search("documentation structure preference")` + `memory_search("project template")`
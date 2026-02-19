---
name: geepers-orchestrate
description: 通过 dr.eamer.dev 编排 API 运行多代理的 Dream Cascade（分层三级合成）或 Dream Swarm（并行多域搜索）工作流程。当任务可以从多个专门化的代理并行或分层协作中受益时，请使用这些流程。
---
# Dreamer Orchestrate

通过 `https://api.dr.eamer.dev` 运行多代理工作流程。

## 认证

```bash
export DREAMER_API_KEY=your_key_here
```

## 端点

### Dream Swarm — 并行搜索
```
POST https://api.dr.eamer.dev/v1/orchestrate/swarm
Body:
{
  "query": "What are the most effective treatments for Type 2 diabetes?",
  "sources": ["pubmed", "semantic_scholar", "wikipedia"],
  "num_agents": 5
}
```
同时启动多个代理从多个数据源中收集数据，并综合分析结果。

### Dream Cascade — 分层合成
```
POST https://api.dr.eamer.dev/v1/orchestrate/cascade
Body:
{
  "task": "Analyze the current state of quantum computing hardware",
  "num_agents": 8,
  "provider": "anthropic"
}
```
三层工作流程：Belter 代理收集原始数据 → Drummer 代理对数据进行分析和整合 → Camina 生成最终报告。

## 响应格式

两个端点均返回相同的数据格式：
```json
{
  "result": "Synthesized answer...",
  "sources": [...],
  "agent_count": 5,
  "duration_ms": 12450
}
```

## 适用场景
- 需要从多个角度进行研究的复杂问题
- 需要跨多个数据源进行综合分析的问题（这些分析需要通过多个顺序查询来完成）
- 需要利用并行处理来节省时间的长期分析任务

## 不适用场景
- 简单的单源查询（请使用 `dreamer-data`）
- 需要对单个代理的行为进行精细控制的情况
- 对响应延迟有严格要求的情况（流程执行时间通常为 10-60 秒）
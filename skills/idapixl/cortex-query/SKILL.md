---
name: cortex-query
description: 用于AI代理的持久化内存：利用cortex-engine MCP工具在不同会话之间进行搜索、记录和知识构建
---
# Cortex 内存 — 查询与记录

您的代理通过 cortex-engine 拥有持久化的内存。您的知识会在会话之间保持不变——您可以回忆起上周学到的内容，跟踪知识的变化，并随着时间的推移构建知识图谱。

## 核心流程

**先阅读再编写。** 在添加新内容之前，务必先确认自己已经掌握的知识。

### 搜索知识

```bash
query("authentication architecture decisions")
```

请使用具体的查询语句。例如，`query("JWT token expiry policy")` 比 `query("auth")` 更准确。查询结果会包含相关性评分以及相关概念。

找到相关知识后，可以进一步探索其周边内容：
```bash
neighbors(memory_id)
```

### 记录所学内容

**事实**——您确认为正确的内容：
```bash
observe("每个 API 密钥的请求速率限制为每分钟 1000 次，而非每个用户")
```

**问题**——您想要探索但尚未解决的问题：
```bash
wonder("为什么同步守护进程会在 300 秒后停止运行？")
```

**假设**——可能正确但尚未被证实的想法：
```bash
speculate("切换到连接池可能会解决超时问题")
```

这些内容会被分开存储，以防止问题干扰您的知识库。

### 更新认知

当您的理解发生变化时：
```bash
believe(concept_id, "根据新证据更新了理解", "变化原因")
```

### 跨会话跟踪工作进度

```bash
ops_append("已完成认证重构，测试通过", project="api-v2")
```

在下一次会话中，从上次停下的地方继续工作：
```bash
ops_query(project="api-v2")
```

## 会话模式

1. **开始：** 使用 `query()` 查询您正在处理的主题。
2. **进行中：** 随着问题的出现，使用 `observe()` 记录事实，使用 `wonder()` 提出问题。
3. **结束：** 使用 `ops_append()` 记录已完成的工作和未完成的任务。
4. **定期：** 使用 `dream()` 将观察结果整合为长期记忆。

## 可用工具

**编写：** observe（观察）、wonder（思考）、speculate（推测）、believe（确认）、reflect（反思）、digest（总结）
**阅读：** query（查询）、recall（回忆）、predict（预测）、validate（验证）、neighbors（探索相关内容）、wander（随机浏览）
**操作：** ops_append（添加记录）、ops_query（查询）、ops_update（更新认知）
**系统功能：** stats（统计分析）、dream（整合记忆）

## 设置

```bash
npm install cortex-engine
npx fozikio init my-agent
npx cortex-engine  # 启动 MCP 服务器
```

默认使用本地 SQLite 和 Ollama 数据库，无需云账户。
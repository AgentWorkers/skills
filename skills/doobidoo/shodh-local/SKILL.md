---
name: shodh-local
summary: Local-first cognitive memory for AI agents with semantic recall, GTD todos, and knowledge graph.
description: Local Shodh-Memory v0.1.74（一款用于AI代理的离线认知记忆系统）：支持持久性记忆存储、语义检索、待办事项/项目管理以及知识图谱功能。  
可用命令：  
- “remember/save/merke X”：保存/回忆特定信息  
- “recall/Erinnere/search memories about Y”：检索与特定主题相关的记忆内容  
- “todos/add/complete”：添加/完成待办事项  
- “projects”：管理项目  
- “proactive context”：提供主动式上下文支持  
- “what learned about Z”：查询关于某个主题的学习内容  

服务器地址：localhost:3030（使用amber-seaslug服务）；详细配置信息请参阅TOOLS.md文件。  
该系统采用赫布学习（Hebbian learning）机制，记忆分为三个层级：工作记忆（working memory）、会话记忆（session memory）和长期记忆（LTM）。  
支持图形化用户界面（TUI）进行操作和监控。
---

# Shodh-Local (v0.1.74)

这是一个专为 OpenClaw 设计的本地化辅助工具，采用“本地优先”的处理策略，通过用户的使用数据进行离线学习。

## 配置（CONFIG.md）
- **二进制文件**：`./shodh-memory-server`（或将其添加到系统路径 PATH 中）
- **服务器地址**：`localhost:3030`
- **数据存储路径**：`./shodh-data`
- **API 密钥**：`<YOUR-API-KEY>`（X-API 密钥，需通过 `shodh-memory-server` 生成）
- **管理工具**：`process` 工具（会话名称为 `amber-seaslug`）
- **图形化界面**：`cd tools/shodh-memory && ./shodh-tui`（用于查看图表和活动信息）

## 快速使用指南
```
KEY='<YOUR-API-KEY>'
curl -s -X POST http://localhost:3030/api/remember \\
-H &quot;Content-Type: application/json&quot; -H &quot;X-API-Key: $KEY&quot; \\
-d &#39;{&quot;user_id&quot;: &quot;henry&quot;, &quot;content&quot;: &quot;Test memory&quot;, &quot;memory_type&quot;: &quot;Learning&quot;, &quot;tags&quot;: [&quot;test&quot;]}&#39;
```

## 核心功能工具
- **记忆功能**：`/api/remember`（支持的学习类型：学习、观察、对话、任务、偏好设置）
- **回忆功能**：`/api/recall`（可按语义内容检索） | `/api/recall/tags`（按标签检索）
- **主动推荐功能**：`/api/proactive_context`（自动推荐相关内容）
- **待办事项管理**：`/api/todos/add` | `/api/todos` | `/api/todos/complete`
- **项目管理**：`/api/projects/add` | `/api/projects`
- **上下文总结**：`/api/context_summary`

完整 API 文档请参阅：[reference/api.md](reference/api.md)

## 使用建议
- **用户标识符**：`henry`（默认用户）、`openclaw`（系统账户）、`task-XYZ`（子代理账户）
- **添加标签**：建议为所有数据添加标签以便过滤（例如：`&quot;openclaw&quot;`、`&quot;project-backend&quot;`）
- **回复前操作**：回忆最近的处理内容以保持对话连贯性
- **定期检查**：每天查看待办事项
- **维护操作**：每周重启服务器（执行 `process kill amber-seaslug` 后重新启动）

有关 OpenClaw 的使用模式和最佳实践，请参阅：[reference/examples.md](reference/examples.md)。
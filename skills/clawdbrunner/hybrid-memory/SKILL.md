---
name: hybrid-memory
description: 混合内存策略：结合了 OpenClaw 内置的向量内存与 Graphiti 时间知识图谱。当需要检索过去的上下文、回答时间相关问题（“X 是什么时候发生的？”）或搜索内存文件时，可以使用该策略。该策略为决定何时使用 `memory_search` 功能与 Graphiti 提供了决策框架。
---

# 混合内存系统

我们使用了两种具有不同优势的内存系统，两者结合使用可以发挥最佳效果。

## 如何选择使用哪种系统

| 问题类型 | 使用的工具 | 示例 |
|--------------|------|---------|
| 查阅文档内容 | `memory_search` | “GOALS.md 文件中提到了什么？” |
| 查看项目指南 | `memory_search` | “我们的项目指南是什么？” |
| 查找时间相关的事实 | Graphiti | “我们是什么时候搭建 Slack 的？” |
| 查看对话记录 | Graphiti | “用户上周二说了什么？” |
| 跟踪相关实体 | Graphiti | “哪些项目与 Alice 有关？” |

## 快速参考

### `memory_search`（内置工具）

用于对 markdown 文件（如 `MEMORY.md`、`memory/**/*.md`）进行语义搜索。

```
memory_search query="your question"
```

如果需要，可以使用 `memory_get` 来读取特定的内容。

### Graphiti（时间相关功能）

用于搜索具有时间戳的事实：

```bash
graphiti-search.sh "your question" GROUP_ID 10
```

用于记录重要事件：

```bash
graphiti-log.sh GROUP_ID user "Name" "Fact to remember"
```

**常用组别标识：**
- `main-agent` — 主要代理
- `user-personal` — 用户的个人信息

## 回忆问题处理流程

在回答关于过去事件的问题时：
1. **时间相关的问题** → 首先查看 Graphiti
2. **文档相关的问题** → 使用 `memory_search`
3. **答案不确定** → 两种工具都尝试使用，并结合结果
4. **信心较低** → 告诉用户你已经查询过，但结果不确定

## `AGENTS.md` 模板

在你的 `AGENTS.md` 文件中添加以下内容：

```markdown
### Memory Recall (Hybrid)

**Temporal questions** ("when?", "what changed?", "last Tuesday"):
```bash
graphiti-search.sh "query" main-agent 10
```

**Document questions** ("what's in X?", "find notes about Y"):
```
memory_search query="你的查询内容"
```

When answering past context: check Graphiti for temporal, memory_search for docs.
```

## 安装指南

完整安装指南：https://github.com/clawdbrunner/openclaw-graphiti-memory

**第 1 部分：OpenClaw 内存系统** — 配置嵌入提供者（推荐使用 Gemini）
**第 2 部分：Graphiti** — 部署 Docker 堆栈并安装同步守护进程
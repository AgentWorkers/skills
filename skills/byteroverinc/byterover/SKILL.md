---
name: byterover
description: "使用 ByteRover 的上下文树来管理项目知识。提供两种操作：查询（检索知识）和整理（存储知识）。当用户需要查找信息、发现模式或保存知识时，可调用这些操作。由 ByteRover Inc.（https://byterover.dev/）开发。"
metadata:
  author: ByteRover Inc. (https://byterover.dev/)
  version: "1.2.1"
---

# ByteRover上下文管理工具

这是一个项目级别的知识库，其内容会在不同会话之间持续保留。使用它可以帮助您避免重复发现相同的模式、约定和决策。

## 为什么使用ByteRover

- **在开始工作前进行查询**：在实施新功能之前，先了解关于现有模式、约定和过去决策的已知信息。
- **在学习后整理知识**：记录下您的见解、决策以及修复的错误，以便未来的会话能够基于这些信息开始工作。

## 快速参考

| 命令 | 使用场景 | 示例 |
|---------|------|---------|
| `brv query "问题"` | 在开始工作之前 | `brv query "身份验证是如何实现的？"` |
| `brv curate "上下文" -f 文件` | 在完成工作之后 | `brv curate "JWT的过期时间（24小时）" -f auth.ts` |
| `brv status` | 检查前提条件 | `brv status` |

## 使用时机

**查询**：当您需要了解某些内容时：
- “在这个代码库中，X是如何工作的？”
- “关于Y，有哪些常用的模式？”
- “对于Z，有什么约定吗？”

**整理知识**：当您学习了或创建了有价值的内容时：
- 使用特定的模式实现了某个功能
- 修复了一个错误并找到了根本原因
- 做出了架构上的决策

## 整理知识的质量要求

整理的上下文信息必须**具体且具有可操作性**：

```bash
# Good - specific, explains where and why
brv curate "Auth uses JWT 24h expiry, tokens in httpOnly cookies" -f src/auth.ts

# Bad - too vague
brv curate "Fixed auth"
```

**注意：**上下文相关的参数必须放在`-f`标志之前。最多可以指定5个文件。

## 最佳实践

1. **分解复杂的上下文**：对于复杂的话题，应多次执行`brv curate`命令，而不是一次性处理所有内容。这样更便于检索和更新。
2. **让ByteRover来读取文件**：在整理知识之前，不要自己手动读取文件。使用`-f`标志让ByteRover直接读取文件：
   ```bash
   # Good - ByteRover reads the files
   brv curate "Auth implementation details" -f src/auth.ts -f src/middleware/jwt.ts

   # Wasteful - reading files twice
   # [agent reads files] then brv curate "..." -f same-files
   ```

3. **查询时要具体**：模糊的查询会阻碍您的工作流程。使用精确的问题来获得更快、更相关的结果：
   ```bash
   # Good - specific
   brv query "What validation library is used for API request schemas?"

   # Bad - vague, slow
   brv query "How is validation done?"
   ```

4. **标记过时的内容**：当您整理的内容会替换现有的知识时，明确告诉ByteRover进行清理：
   ```bash
   brv curate "OUTDATED: Previous auth used sessions. NEW: Now uses JWT with refresh tokens. Clean up old session-based auth context." -f src/auth.ts
   ```

5. **指定知识的结构**：指导ByteRover如何组织这些知识：
   ```bash
   # Specify topics/domains
   brv curate "Create separate topics for: 1) JWT validation, 2) refresh token flow, 3) logout handling" -f src/auth.ts

   # Specify detail level
   brv curate "Document the error handling patterns in detail (at least 30 lines covering all error types)" -f src/errors/
   ```

## 先决条件

请先运行`brv status`命令。如果出现错误，ByteRover无法自行修复这些问题——请指导用户在相应的终端中采取相应的措施。详情请参阅[TROUBLESHOOTING.md](TROUBLESHOOTING.md)。

---

**另请参阅：**[WORKFLOWS.md](WORKFLOWS.md)以获取详细的模式和示例，[TROUBLESHOOTING.md](TROUBLESHOOTING.md)以了解错误处理方法。
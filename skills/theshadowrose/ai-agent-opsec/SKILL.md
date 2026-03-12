---
name: "AI Agent OPSEC — Runtime Classified Data Enforcer"
description: "防止你的AI代理将机密信息泄露给外部API、子代理或日志文件。采用术语注册表进行管理，运行时对数据内容进行审查，并在发布前进行审核。实现零依赖、零网络请求的设计。"
author: "@TheShadowRose"
version: "1.1.0"
tags: ["opsec", "security", "redaction", "privacy", "classified", "agent-safety"]
license: "MIT"
---
# AI Agent OPSEC — 运行时机密数据保护工具

确保您的机密信息不会被网络搜索、外部大型语言模型（LLM）的调用或子代理程序获取。

## 副作用（已声明）

| 类型 | 路径 | 描述 |
|------|------|-------------|
| **读取** | `<workspace>/classified/classified-terms.md` | 您的术语注册表——在此处添加术语，该术语将在所有地方受到保护 |
| **写入** | `<workspace>/memory/security/classified-access-audit.jsonl` | 只允许追加内容的审计日志；每达到1MB会自动旋转；**绝不包含原始的敏感文本** |
| **网络** | 无 | 完全本地处理，不进行任何外部调用。 |

> **重要提示：** 将 `classified/` 和 `memory/security/` 添加到您的 `.gitignore` 文件中，以防止意外提交这些文件。

## 设置步骤

1. 在工作区的根目录下创建 `classified/classified-terms.md` 文件。
2. 每行添加一个术语（空行和 `#` 注释将被忽略）。
3. 在进行任何外部调用之前，必须使用该保护工具。

```javascript
const ClassifiedAccessEnforcer = require('./src/ClassifiedAccessEnforcer');
const enforcer = new ClassifiedAccessEnforcer('/path/to/workspace');

// Before any external API call
const { safe, payload } = enforcer.gateExternalPayload(userQuery, 'web_search');

// Before spawning a subagent
const { task } = enforcer.redactTaskBeforeSpawn(taskString, 'ResearchAgent');
```

请参阅 README.md 以获取完整文档。
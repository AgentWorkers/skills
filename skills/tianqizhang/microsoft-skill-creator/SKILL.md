---
name: microsoft-skill-creator
description: 使用 Learn MCP 工具为 Microsoft 技术创建代理技能。当用户希望创建一种能够教授代理关于任何 Microsoft 技术、库、框架或服务（如 Azure、.NET、M365、VS Code、Bicep 等）的技能时，可以使用该工具。该工具会深入研究相关主题，然后生成一种混合型技能：这种技能会将核心知识存储在本地，同时支持进一步的动态查询和深入学习。
context: fork
compatibility: Requires Microsoft Learn MCP Server (https://learn.microsoft.com/api/mcp)
---

# Microsoft Skill Creator

用于创建针对 Microsoft 技术的混合式技能（hybrid skills）。这些技能会将核心知识存储在本地，同时支持通过 Learn MCP 动态查询以获取更详细的资料。

## 先决条件：连接到 Microsoft Learn MCP 服务器

**重要提示：** 此技能需要连接到 **Microsoft Learn MCP 服务器**（类型：http，网址：https://learn.microsoft.com/api/mcp）。如果尚未连接，请自行安装并配置该服务器。如有需要，请向用户请求授权。

Microsoft Learn MCP 是微软提供的免费官方服务，无需使用 API 密钥或进行身份验证。

## 关于技能（Skills）

技能是一种模块化包，它们通过提供专门的知识和工作流程来扩展代理（agent）的功能。一个技能可以将通用的代理转变为针对特定领域的专用代理。

### 技能结构（Skill Structure）

```
skill-name/
├── SKILL.md (required)     # Frontmatter (name, description) + instructions
├── references/             # Documentation loaded into context as needed
├── sample_codes/           # Working code examples
└── assets/                 # Files used in output (templates, etc.)
```

### 关键原则（Key Principles）

- **前言部分至关重要（Frontmatter is critical）**：`name`（技能名称）和 `description`（技能描述）决定了技能的触发条件——请确保描述清晰且全面。
- **简洁性是关键（Conciseness is key）**：仅包含代理尚未掌握的信息；相关上下文信息会通过其他方式共享。
- **避免重复（No duplication）**：信息应仅存储在 SKILL.md 文件或参考文件中，切勿同时存在于两者中。

## Learn MCP 工具（Learn MCP Tools）

| 工具 | 用途 | 使用场景 |
|------|---------|-------------|
| `microsoft_docs_search` | 搜索官方文档 | 初步了解相关主题 |
| `microsoft_docs_fetch` | 获取页面完整内容 | 深入研究重要页面 |
| `microsoft_code_sample_search` | 查找代码示例 | 获取实现模式 |

## 创建流程（Creation Process）

### 第一步：调查主题（Step 1: Investigate the Topic）

使用 Learn MCP 工具分三个阶段深入了解相关技术：

**阶段 1 - 范围探索（Phase 1 - Scope Discovery）：**
```
microsoft_docs_search(query="{technology} overview what is")
microsoft_docs_search(query="{technology} concepts architecture")
microsoft_docs_search(query="{technology} getting started tutorial")
```

**阶段 2 - 核心内容（Phase 2 - Core Content）：**
```
microsoft_docs_fetch(url="...")  # Fetch pages from Phase 1
microsoft_code_sample_search(query="{technology}", language="{lang}")
```

**阶段 3 - 深入研究（Phase 3 - Depth）：**
```
microsoft_docs_search(query="{technology} best practices")
microsoft_docs_search(query="{technology} troubleshooting errors")
```

#### 调查检查清单（Investigation Checklist）

调查完成后，请确认以下内容：
- [ ] 能够用一段话解释该技术的功能。
- [ ] 确定了 3-5 个关键概念。
- [ ] 拥有可用于基本操作的代码示例。
- [ ] 了解最常见的 API 使用模式。
- [ ] 知道用于深入研究的搜索查询方法。

### 第二步：与用户确认（Step 2: Clarify with User）

向用户展示调查结果，并询问以下问题：
1. “我发现了这些关键领域：[列出]。哪些是最重要的？”
2. “代理使用此技能主要执行哪些任务？”
3. “代码示例应优先使用哪种编程语言？”

### 第三步：生成技能（Step 3: Generate the Skill）

使用 [skill-templates.md](references/skill-templates.md) 中提供的相应模板来生成技能文件：

| 技术类型 | 模板 |  
|-----------------|----------|
| 客户端库、NuGet/npm 包 | SDK/库（Client library, NuGet/npm package） |
| Azure 资源 | Azure 服务（Azure Resource） |
| 应用开发框架 | 框架/平台（App development framework） |
| REST API、协议 | API/协议（REST API, protocol） |

#### 生成的技能结构（Generated Skill Structure）

```
{skill-name}/
├── SKILL.md                    # Core knowledge + Learn MCP guidance
├── references/                 # Detailed local documentation (if needed)
└── sample_codes/               # Working code examples
    ├── getting-started/
    └── common-patterns/
```

### 第四步：平衡本地内容与动态内容（Step 4: Balance Local vs Dynamic Content）

**在以下情况下将内容存储在本地：**
- 基础知识（任何任务都需要的内容）。
- 频繁访问的内容。
- 稳定的内容（不会发生变化的内容）。
- 通过搜索难以找到的内容。

**在以下情况下使用动态内容：**
- 内容量过大、难以全部存储的内容。
- 与特定版本相关的内容。
- 仅适用于特定任务的内容。
- 索引完善、易于搜索的内容。

#### 内容指南（Content Guidelines）

| 内容类型 | 本地存储（Local） | 动态获取（Dynamic） |
|--------------|-------|---------|
| 核心概念（3-5 个） | ✅ 完整存储 | |
| “Hello World” 示例代码 | ✅ 完整存储 | |
| 常见的使用模式（3-5 个） | ✅ 完整存储 | |
| 主要 API 方法 | 方法签名 + 示例代码 | 通过 `microsoft_docs_fetch` 动态获取完整文档 |
| 最佳实践 | 前 5 条内容 | 可通过搜索获取更多信息 |
| 故障排除指南 | | 可通过搜索查询获取 |
| 完整的 API 参考文档 | | 提供文档链接 |

### 第五步：验证（Step 5: Validate）

1. **审查**：本地存储的内容是否足以满足常见任务的需求？
2. **测试**：建议的搜索查询是否能返回有用的结果？
3. **验证**：代码示例能否正常运行？

## 常见的调查方法（Common Investigation Methods）

### 对于 SDK/库（For SDKs/Libraries）：
```
"{name} overview" → purpose, architecture
"{name} getting started quickstart" → setup steps
"{name} API reference" → core classes/methods
"{name} samples examples" → code patterns
"{name} best practices performance" → optimization
```

### 对于 Azure 服务（For Azure Services）：
```
"{service} overview features" → capabilities
"{service} quickstart {language}" → setup code
"{service} REST API reference" → endpoints
"{service} SDK {language}" → client library
"{service} pricing limits quotas" → constraints
```

### 对于框架/平台（For Frameworks/Platforms）：
```
"{framework} architecture concepts" → mental model
"{framework} project structure" → conventions
"{framework} tutorial walkthrough" → end-to-end flow
"{framework} configuration options" → customization
```

## 示例：创建一个“Semantic Kernel”技能（Example: Creating a “Semantic Kernel” Skill）

### 调查过程（Example: Investigation Process）

```
microsoft_docs_search(query="semantic kernel overview")
microsoft_docs_search(query="semantic kernel plugins functions")
microsoft_code_sample_search(query="semantic kernel", language="csharp")
microsoft_docs_fetch(url="https://learn.microsoft.com/semantic-kernel/overview/")
```

### 生成的技能文件（Generated Skill File）

```
semantic-kernel/
├── SKILL.md
└── sample_codes/
    ├── getting-started/
    │   └── hello-kernel.cs
    └── common-patterns/
        ├── chat-completion.cs
        └── function-calling.cs
```

### 生成的 SKILL.md 文件（Generated SKILL.md）

```markdown
---
name: semantic-kernel
description: Build AI agents with Microsoft Semantic Kernel. Use for LLM-powered apps with plugins, planners, and memory in .NET or Python.
---

# Semantic Kernel

Orchestration SDK for integrating LLMs into applications with plugins, planners, and memory.

## Key Concepts

- **Kernel**: Central orchestrator managing AI services and plugins
- **Plugins**: Collections of functions the AI can call
- **Planner**: Sequences plugin functions to achieve goals
- **Memory**: Vector store integration for RAG patterns

## Quick Start

See [getting-started/hello-kernel.cs](sample_codes/getting-started/hello-kernel.cs)

## Learn More

| Topic | How to Find |
|-------|-------------|
| Plugin development | `microsoft_docs_search(query="semantic kernel plugins custom functions")` |
| Planners | `microsoft_docs_search(query="semantic kernel planner")` |
| Memory | `microsoft_docs_fetch(url="https://learn.microsoft.com/en-us/semantic-kernel/frameworks/agent/agent-memory")` |
```
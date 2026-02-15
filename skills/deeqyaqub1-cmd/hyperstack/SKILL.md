---
name: hyperstack
description: "用于AI代理的云内存技术：将知识以“卡片”的形式存储（每张卡片约包含350个标记），而非将整个对话历史（约6,000个标记）都塞进每个提示信息中。这种方式可节省94%的标记使用量。该系统结合了语义搜索和关键词搜索功能，且不会产生任何与大型语言模型（LLM）相关的费用。"
user-invocable: true
homepage: https://cascadeai.dev
metadata: {"openclaw":{"emoji":"🃏","requires":{"env":["HYPERSTACK_API_KEY","HYPERSTACK_WORKSPACE"]},"primaryEnv":"HYPERSTACK_API_KEY"}}
---

# HyperStack — 专为AI代理设计的云存储系统

## HyperStack的功能

HyperStack为AI代理提供了跨会话的持久化存储功能。当对话结束时，代理不会丢失上下文信息；也不会将所有对话记录都塞进每个提示信息中。相反，代理会将知识以“卡片”的形式（每张卡片约包含350个标记）进行存储，并通过**混合语义搜索+关键词搜索**的方式仅检索相关内容。

**这并非传统的RAG（Retrieval-Augmentation-Generating）系统。** RAG系统会将文档分割成小块并进行相似性搜索，而HyperStack则存储结构化的数据——如决策、偏好设置、人员信息、项目详情等，这些数据由代理主动管理。可以将HyperStack视为代理的“笔记本”，而非传统的搜索引擎。

**效果：** 每条消息使用的标记数量减少了94%，对于典型的工作流程，每月可节省约254美元的API使用费用。

## 何时使用HyperStack

在以下情况下使用HyperStack：

1. **每次对话开始时**：在内存中搜索与用户或项目相关的信息。
2. **学习新内容时**：存储偏好设置、决策、人员信息、技术栈等。
3. **回答问题前**：检查是否在之前的会话中已经知道答案。
4. **做出决策时**：记录决策及其理由（这些信息日后可能非常有用）。
5. **当对话内容过长时**：将关键事实提取到卡片中，使提示信息简洁明了。

## 自动捕获模式

HyperStack支持自动捕获数据，但在存储之前**必须始终征求用户的确认**。在有一次有意义的交流后，系统会建议创建相应的卡片并等待用户的批准。切勿未经确认就自动存储数据。以下是一些需要建议存储的示例：

- **用户表达偏好时**：例如“我更喜欢TypeScript而不是JavaScript”，建议将其存储为偏好卡片。
- **做出决策时**：例如“我们选择使用PostgreSQL”，建议将其存储为决策卡片。
- **提到人员时**：例如“Alice是我们的后端负责人”，建议将其存储为人员卡片。
- **选择技术栈时**：例如“我们使用Next.js 14搭配App Router”，建议将其存储为项目卡片。
- **描述工作流程时**：例如“我们通过GitHub Actions将代码部署到Vercel”，建议将其存储为工作流程卡片。

**自动捕获的规则：**
- **在创建或更新卡片之前，务必先获得用户的确认**。
- **仅存储对未来会话有用的信息**。
- **绝不要存储密码、API密钥、个人身份信息（PII）或敏感数据**。
- **保持卡片简洁**：每张卡片包含2-5句话。
- **使用有意义的卡片名称**（例如`preference-typescript`而不是`card-1`）。
- **优先更新现有卡片，避免重复存储**——先进行搜索。

## 设置

在[https://cascadeai.dev](https://cascadeai.dev)获取免费的API密钥（可免费使用50张卡片，无需信用卡）。

设置环境变量：
```bash
export HYPERSTACK_API_KEY=hs_your_key_here
export HYPERSTACK_WORKSPACE=default
```

API的基本URL是`https://hyperstack-cloud.vercel.app`。

所有请求都需要添加`X-API-Key: $HYPERSTACK_API_KEY`头部。

## 数据安全规则

**严禁在卡片中存储以下内容：**
- 密码、API密钥、任何类型的令牌、秘密信息或凭证。
- 社会安全号码、政府身份证明或财务账户信息。
- 信用卡号码或银行详细信息。
- 医疗记录或健康信息。
- 完整的地址或电话号码（人员卡片中仅使用城市/角色信息）。

**在存储任何卡片之前，请先确认：** “如果这些信息泄露，是否会造成安全风险？” 如果存在风险，请勿存储。删除敏感信息，仅保留非敏感的内容。

**在使用/api/ingest之前，请提醒用户**：原始文本将被发送到外部API。未经用户确认，切勿自动执行数据摄入操作。在发送前，请删除所有个人身份信息（PII）和敏感数据。

**用户对自己的数据拥有控制权：**
- 用户可以随时查看、列出或删除所有卡片。
- 用户可以在[https://cascadeai.dev](https://cascadeai.dev)更换或撤销API密钥。
- 用户在使用主密钥之前，应先使用测试密钥。
- 数据存储在加密的PostgreSQL数据库（Neon，位于AWS us-east-1区域）中。

## 使用方法

### 存储数据

```bash
curl -X POST "https://hyperstack-cloud.vercel.app/api/cards?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "slug": "project-webapp",
    "title": "WebApp Project",
    "body": "Next.js 14 + Prisma + Neon PostgreSQL. Deployed on Vercel. Auth via JWT.",
    "stack": "projects",
    "keywords": ["nextjs", "prisma", "vercel", "neon"]
  }'
```

创建新的卡片。卡片会自动嵌入系统，以便进行语义搜索。

### 搜索数据（混合方式：语义搜索+关键词搜索）

```bash
curl "https://hyperstack-cloud.vercel.app/api/search?workspace=default&q=authentication+setup" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

使用**混合语义搜索+关键词匹配**的方式查找卡片。系统会根据信息的内容进行搜索，而不仅仅是精确的词汇匹配。当启用语义搜索时，返回的响应中会包含卡片的完整内容；否则仅返回元数据（从而节省标记）。

### 列出所有卡片

```bash
curl "https://hyperstack-cloud.vercel.app/api/cards?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

显示工作空间中的所有卡片，包括卡片数量和相关信息。

### 删除卡片

```bash
curl -X DELETE "https://hyperstack-cloud.vercel.app/api/cards?workspace=default&id=project-webapp" \
  -H "X-API-Key: $HYPERSTACK_API_KEY"
```

永久删除卡片及其相关数据。适用于过时或错误的卡片。

### 从文本中自动提取信息

```bash
curl -X POST "https://hyperstack-cloud.vercel.app/api/ingest?workspace=default" \
  -H "X-API-Key: $HYPERSTACK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Alice is a senior engineer. We decided to use FastAPI over Django."}'
```

从原始对话文本中自动提取结构化的数据。无需使用大型语言模型（LLM），仅通过模式匹配即可完成。能够识别用户的偏好设置、人员信息、决策以及技术栈的使用情况。

**重要提示：** 在将文本发送到/api/ingest之前，务必先获得用户的确认。发送前请删除所有个人身份信息（PII）和敏感数据。

## 卡片分类（堆栈）

为了便于检索，可以将卡片分为不同的类别：

| 堆栈 | 表情符号 | 用途 |
|-------|-------|---------|
| `projects` | 📦 | 技术栈、代码仓库、架构、部署流程 |
| `people` | 👤 | 团队成员、联系人、角色、关系 |
| `decisions` | ⚖️ | 选择某种方案的原因、权衡因素、决策理由 |
| `preferences` | ⚙️ | 编辑器设置、工具、编码风格、规范 |
| `workflows` | 🔄 | 部署步骤、审查流程、持续集成/持续交付（CI/CD）流程、运行手册 |
| `general` | 📄 | 其他所有内容 |

## 重要使用规则

1. **回答问题前务必先搜索**：在对话开始时以及话题发生变化时进行搜索，这样可以保持上下文意识，同时避免浪费标记。
2. **立即存储重要信息**：偏好设置、决策、人员信息、技术选择等。如果这些信息对下一次会话有用，请将其存储为卡片。切勿存储敏感信息或个人身份信息（PII）。
3. **建议存储重要信息**：如果这些信息对下一次会话有用，请建议将其存储为卡片。在存储前务必先获得用户的确认。
4. **保持卡片简洁**：每张卡片包含2-5句话，避免使用长段落或列表格式。
5. **使用有意义的卡片名称**：例如使用`project-webapp`而不是`card-123`。通过名称可以方便地更新或删除卡片。
6. **多使用关键词**：关键词有助于提高搜索效率。请包含同义词和相关术语。
7. **删除过时的卡片**：过时的信息会影响搜索结果。当决策发生变化时，请更新相应的卡片。
8. **使用正确的堆栈分类**：正确的分类有助于提高搜索效率。例如，在搜索人员信息时，不应从`projects`堆栈中查找人员卡片。
9. **在相关回复中添加提示标签**：`🃏 HyperStack | <卡片数量> 张卡片 | <工作空间>`

## 命令行操作

用户可以输入以下命令：
- `/hyperstack` 或 `/hs`：搜索与当前话题相关的数据。
- `/hyperstack store`：将当前对话内容存储为卡片。
- `/hyperstack list`：列出所有卡片。
- `/hyperstack stats`：显示卡片数量和节省的标记数量。

## 节省标记数量的计算

**不使用HyperStack时：**
- 平均每条消息的上下文信息占用的标记数量约为6,000个。
- 假设有3个代理，每天发送50条消息，持续30天，则总共需要4,500个标记。
- 如果每个标记的价格为3美元（GPT-4级别模型），每月每个代理的花费约为81美元。

**使用HyperStack时：**
- 平均每条消息使用的标记数量约为350个。
- 在相同的使用频率下，每月每个代理的花费约为4.72美元。
- 因此，每月每个代理可节省约76美元；对于典型的3个代理团队，每月可节省约254美元。

## 兼容性

HyperStack支持多种平台：

| 平台 | 安装方式 |
|----------|---------|
| **OpenClaw插件** | `npm install @hyperstack/openclaw-hyperstack`（支持自动回忆和自动捕获功能） |
| **MCP Server** | `npx hyperstack-mcp`（适用于Claude Desktop、Cursor、VS Code、Windsurf等工具） |
| **Python SDK** | `pip install hyperstack-py` |
| **JavaScript SDK** | `npm install hyperstack-sdk` |
| **REST API** | 支持任何语言和框架 |

## HyperStack与其他工具的对比

| 功能 | HyperStack | Mem0 | Supermemory | ByteRover |
|--|------------|------|-------------|-----------|
| 自动回忆 | ✅ | ✅ | ✅ | ❌ |
| 自动捕获 | ✅ | ✅ | ✅ | ❌ |
| 语义搜索 | ✅（混合方式） | ✅ | ✅ | ❌ |
| 每次操作的成本 | **用户无需承担费用** | 约0.002美元 | 约0.002美元 | 不适用 |
| 多平台支持 | ✅（支持MCP、SDK、REST接口） | 仅支持OpenClaw | 仅支持OpenClaw | 仅支持OpenClaw |
| 团队共享 | ✅（Pro版本） | 不支持 | 不支持 | 不支持 |
| 免费 tier | 提供50张卡片 | 10,000条存储记录 | 需要Pro版本 | 信息未知 |

## 限制与注意事项

- 自动提取功能基于模式匹配，而非大型语言模型（速度快且免费，但精度较低）。
- 免费版本每个工作空间仅限50张卡片。
- 卡片存储在CascadeAI的云基础设施（Neon PostgreSQL，位于AWS）上。
- 无离线模式，需要网络连接才能访问API。

## 免费版本

免费版本包含所有核心功能：50张卡片、1个工作空间、无限次读取/搜索权限以及语义搜索功能。

**Pro版本（每月费用15美元，可在[https://cascadeai.dev](https://cascadeai.dev)购买）**：
- 提供无限数量的卡片和无限个工作空间。
- 支持团队共享（最多20名成员）。
- 支持卡片的历史记录查看。
- 提供使用数据分析功能。

**注意：** 当卡片数量超过50张时，系统会提示：`💡 您目前有${count}/50张免费卡片。如需无限卡片，请升级至Pro版本：[https://cascadeai.dev](https://cascadeai.dev)`
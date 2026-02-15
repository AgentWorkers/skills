---
name: agent-docs
description: 创建专为AI代理使用的文档。在编写SKILL.md文件、README文件、API文档或任何将由大型语言模型（LLMs）在上下文窗口中阅读的文档时，请使用此方法。该方法有助于优化内容结构，以提高信息检索效率（RAG，即Retrieval with Attention and Generation）、提升令牌使用效率（token efficiency），并支持混合上下文层次结构（Hybrid Context Hierarchy）。
---

# 代理文档（Agent Docs）

编写易于 AI 代理高效阅读的文档。文档编写需参考 Vercel 的基准测试结果及行业标准（参考文件：AGENTS.md、llms.txt、CLAUDE.md）。

## 混合式上下文层次结构（Hybrid Context Hierarchy）

这种三层架构能够提升代理的性能：

### 第一层：内联文档（Inline Documents）
**始终保持在上下文中。** 最大内容长度为 2,000–4,000 个令牌（token）。

```markdown
# AGENTS.md
> Context: Next.js 16 | Tailwind | Supabase

## 🚨 CRITICAL
- NO SECRETS in output
- Use `app/` directory ONLY

## 📚 DOCS INDEX (use read_file)
- Auth: `docs/auth/llms.txt`
- DB: `docs/db/schema.md`
```

**包含内容：**
- 安全规则、架构限制
- 构建/测试/代码检查命令
- 文档导航信息（说明如何获取更多资源）

### 第二层：参考库（Reference Library）
**按需获取。** 每次获取的内容长度为 1,000–5,000 个令牌。
- 特定框架的指南
- 详细的风格规范
- API 架构文档

### 第三层：外部资源（External Resources）
**仅允许访问指定资源。** 仅用于处理边缘情况。
- 最新的库更新信息
- 遇到疑难问题时可以参考 Stack Overflow
- 第三方提供的 llms.txt 文档

## 该方案为何有效

**Vercel 基准测试（2026 年）：**
| 方法 | 通过率 |
|----------|-----------|
| 基于工具的检索 | 53% |
| 检索 + 提示结合 | 79% |
| **内联文档（AGENTS.md）** | **100%** |

**原因：** 代理缺乏元认知能力——它们不知道自己不知道什么，因此会误以为训练数据已经足够使用。内联文档完全规避了这一问题。

## 核心原则（Core Principles）

### 1. 压缩索引优于完整文档（Compressed Index > Full Docs）
一个 8KB 的压缩索引比 40KB 的完整文档更高效。
**压缩内容包括：**
- 文件路径（代码所在的位置）
- 函数签名（仅包含函数名称和类型）
- 禁用某些功能的明确说明（例如：“禁止使用 X”）

### 2. 采用分块结构（Structure for Chunking）
基于检索与生成（RAG, Retrieval and Generation）的系统通常会在文档头部进行分割。每个部分都必须是独立的：

```markdown
## Database Setup          ← Chunk boundary

Prerequisites: PostgreSQL 14+

1. Create database...
```

**规则：**
- 首先提供关键信息（分块机制会自动截断冗余内容）
- 使用描述性强的标题（代理可以通过标题进行搜索）

### 3. 内联内容优于链接（Inline Content优于 Links）
代理无法自主浏览文档。每个链接都可能引入额外的工具调用、延迟或潜在的错误。
| 方法 | 令牌加载量 | 代理处理成功率 |
|----------|------------|---------------|
| 完整内联文档 | 约 12,000 个令牌 | ✅ 高成功率 |
| 仅使用链接 | 约 2,000 个令牌 | ❌ 需要额外获取内容 |
| 混合式结构 | 约 4,000 个令牌 | ✅ 结合了两种方式的优点 |

### 4. “信息冗余导致阅读困难的问题”（The “Lost in the Middle” Problem）
大型语言模型（LLMs）的注意力分布呈 U 形：
- **强相关区域：** 文档的开头和结尾
- **弱相关区域：** 文档的中间部分
**解决方案：** 将关键规则放在文档的开头，详细内容放在后面

### 5. 信号与噪声的比例（Signal-to-Noise Ratio）
去除所有非必要的内容：
- 无多余的欢迎语或营销文字
- 核心文档中不包含版本更新记录

像 llms.txt 和 AGENTS.md 这样的文档格式有助于提升信息的清晰度（提高信号与噪声的比例）。

## llms.txt 标准（llms.txt Standard）

为代理提供的机器可读文档索引：

```markdown
# Project Name

> One-line project description.

## Authentication

- [Setup](docs/auth/setup.md): Environment vars and init
- [Server](docs/auth/server.md): Cookie handling

## Database

- [Schema](docs/db/schema.md): Full Prisma schema
```

**位置：** 位于域名根目录下的 `/llms.txt`
**配套文件：** `/llms-full.txt` — 包含所有文档的 HTML 格式文件（已去除 HTML 标签）

## 安全考虑（Security Considerations）

### 内联文档（Inline Documents） = 可信赖的内容
AGENTS.md 是代码库的一部分，受到严格控制，并会进行版本管理。

### 外部资源（External Resources） = 安全风险
- 可能通过隐藏文本注入恶意指令
- 如果代理可以自由浏览外部资源，存在 SSRF（跨站请求伪造）风险
- 外部资源的可用性会影响系统的稳定性

**缓解措施：** 通过域名白名单进行访问控制，并在需要外部资源时人工审核。

## 应避免的错误做法（Anti-Patterns）

1. **粘贴大量内容（如 50 页文档）** — 会导致信息冗余，影响阅读效率
2. **仅提供“查看外部文档”的提示** — 代理无法自主查找所需信息
3. **提供泛泛而空的建议**（如“编写清晰的代码”）
4. **仅提供目录结构的文档** — 没有实际内容
5. **过度依赖外部检索** — 通过率仅为 53%，而内联文档的通过率为 100%

## 高级实践（Advanced Practices）

有关 RAG 优化、多框架文档编写及 API 模板的详细指导，请参阅 [references/advanced-patterns.md](references/advanced-patterns.md)。

## 验证检查清单（Validation Checklist）
- 文档开头包含关键的管理信息
- 内联文档的总长度不超过 4,000 个令牌
- 每个 H2 标题下的内容都是独立的
- 外部链接必须附带内联的简要说明
- 明确禁止某些行为的规则（例如：“禁止使用 X”）
- 提供文件路径和函数签名，而非完整的代码内容
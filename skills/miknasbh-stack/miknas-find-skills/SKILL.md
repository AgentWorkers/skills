---
name: "find-skills"
description: "使用 SkillKit CLI 从多个 AI 代理技能市场（包含超过 40 万个技能）中发现、搜索并安装技能。支持浏览官方合作伙伴的技能集合（如 Anthropic、Vercel、Supabase、Stripe 等）以及社区仓库，可以根据领域或技术进行搜索，并从 GitHub 安装特定技能。适用于用户需要查找、浏览或安装新的代理技能、插件、扩展程序或附加组件的情况；例如用户可能会询问“是否有适用于 X 的技能”或“为 X 寻找一个技能”；或者希望探索技能商店或市场；需要在 React、测试、DevOps、安全或 API 等领域扩展代理的功能；还可以执行诸如“浏览技能”、“搜索技能市场”、“安装技能”或“有哪些技能可用”等操作。"
version: "1.0.0"
tags: ["meta", "discovery", "marketplace", "skills"]
---
# 查找技能

这是一个通用技能发现工具，支持在所有 AI 代理技能市场中进行搜索。

## 使用场景

当用户遇到以下情况时，可以使用此功能：
- 提问“如何完成某件事”（其中“某件事”可能对应某个现有的技能）；
- 询问“寻找用于完成某件事的技能”或“是否有可以完成某件事的技能”；
- 希望通过专门的技能来扩展代理的功能；
- 提到某个特定领域（如测试、部署、设计、安全等）。

## SkillKit 命令行接口（CLI）命令

```bash
# Search skills
npx skillkit@latest find <query>

# Install from GitHub
npx skillkit@latest install <owner/repo>

# Browse TUI marketplace
npx skillkit@latest marketplace

# List installed skills
npx skillkit@latest list

# Get recommendations based on your project
npx skillkit@latest recommend
```

## 技能来源（超过 40 万项技能）

### 官方合作伙伴
| 来源 | 安装命令 |
|--------|---------|
| Anthropic | `npx skillkit@latest install anthropics/skills` |
| Vercel | `npx skillkit@latest install vercel-labs/agent-skills` |
| Expo | `npx skillkit@latest install expo/skills` |
| Remotion | `npx skillkit@latest install remotion-dev/skills` |
| Supabase | `npx skillkit@latest install supabase/agent-skills` |
| Stripe | `npx skillkit@latest install stripe/ai` |

### 社区收藏集
| 来源 | 专注领域 |
|--------|-------|
| `trailofbits/skills` | 安全、审计 |
| `obra/superpowers` | 测试驱动开发（TDD）、工作流程 |
| `wshobson/agents` | 开发模式 |
| `ComposioHQ/awesome-claude-skills` | 精选技能集合 |
| `langgenius/dify` | 人工智能平台相关技能 |
| `better-auth/skills` | 身份验证相关技能 |
| `elysiajs/skills` | Bun/ElysiaJS 相关技能 |
| `rohitg00/kubectl-mcp-server` | Kubernetes MCP 相关技能 |

## 如何帮助用户

### 第一步：了解用户需求
确定以下信息：
1. 所需技能涉及的领域（如 React、测试、DevOps、安全等）；
2. 具体任务（如编写测试代码、部署应用程序、代码审查等）；
3. 使用的技术栈。

### 第二步：搜索技能
使用相关关键词进行搜索：
```bash
npx skillkit@latest find "react testing"
npx skillkit@latest find "kubernetes"
npx skillkit@latest find "security audit"
```

### 第三步：展示搜索结果
找到技能后，展示以下信息：
1. 技能名称和描述；
2. 安装命令；
3. 技能的来源仓库链接。

**示例响应：**
```
Found: "React Best Practices" from Vercel Labs
- React and Next.js patterns from Vercel Engineering

Install:
npx skillkit@latest install vercel-labs/agent-skills
```

### 第四步：安装技能
为用户安装所需的技能：
```bash
npx skillkit@latest install <owner/repo>
```

**或非交互式地安装特定技能：**
```bash
npx skillkit@latest install owner/repo --skills skill-name
npx skillkit@latest install anthropics/skills --skills frontend-design
npx skillkit@latest install vercel-labs/agent-skills -s react-best-practices
```

## 常见搜索查询
| 需求 | 搜索关键词 |
|------|--------------|
| React 开发模式 | `npx skillkit@latest find react` |
| 测试工具 | `npx skillkit@latest find testing jest` |
| TypeScript 技能 | `npx skillkit@latest find typescript` |
| DevOps 工具 | `npx skillkit@latest find docker kubernetes` |
| 安全相关技能 | `npx skillkit@latest find security` |
| API 设计相关技能 | `npx skillkit@latest find api rest graphql` |
| 移动应用开发 | `npx skillkit@latest find react-native expo` |
| 数据库相关技能 | `npx skillkit@latest find postgres prisma` |

## 未找到匹配技能时的处理方式
如果未找到合适的技能：
1. 直接提出用自己的能力来帮助用户；
2. 建议用户创建自定义技能；
3. 推荐用户将自定义技能发布到技能共享平台，以便他人使用：
```bash
 npx skillkit@latest init my-skill
 ```

## 在线资源
- 官方网站：https://agentskills.com
- GitHub 仓库：https://github.com/rohitg00/skillkit

## 重要说明：
- 使用 `owner/repo` 的格式来表示技能来源，而非完整的 URL；
- 使用 `--skills`（复数形式）或 `-s` 标志来指定特定的技能；
- 使用 `@latest` 选项来安装最新版本的技能：`npx skillkit@latest`
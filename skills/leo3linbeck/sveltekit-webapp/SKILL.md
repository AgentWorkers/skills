---
name: sveltekit-webapp
version: 1.1.0
description: |
  Scaffold and configure a production-ready SvelteKit PWA with opinionated defaults.
  Use when: creating a new web application, setting up a SvelteKit project, building a PWA,
  or when a user asks to "build me an app/site/webapp". Handles full setup including TypeScript,
  Tailwind, Skeleton + Bits UI components, testing, linting, and Vercel deployment.
  Generates a PRD with user stories for review, then upon user approval, builds through
  development, staging, and production with user approval at each stage.
requires_tools: [exec, Write, Edit, browser]
safety_notes: |
  This skill executes shell commands to scaffold and deploy web applications.
  All commands require user approval via the agent's safety framework.
  No commands are executed without user confirmation of the PRD.
---

# SvelteKit Webapp 服务

本服务提供基于 SvelteKit 的生产就绪型 PWA（Progressive Web App）搭建方案，采用预设的配置选项，并引导用户完成整个开发流程。

## 快速入门

1. **描述您的应用需求** — 告诉我您想要构建什么类型的应用。
2. **审查项目需求文档 (PRD)** — 我将根据您的需求生成详细的开发计划。
3. **审核并批准** — 在您的监督下，我会进行开发、测试和部署。
4. **完成** — 您将获得应用的实时访问地址以及相应的管理文档。

例如：“为我构建一个带有截止日期和优先级标签的任务跟踪器。”

只需提供这些信息，我就可以开始为您服务。如有需要，我会进一步询问详细信息。

## 先决条件

以下命令行工具（CLI）必须可用（服务会在启动前进行验证）：

| CLI | 功能 | 安装方式 |
|-----|---------|---------|
| `sv` | SvelteKit 搭建工具 | `npm i -g sv`（或通过 `pnpx` 使用） |
| `pnpm` | 包管理器 | `npm i -g pnpm` |
| `gh` | GitHub 仓库创建工具 | [cli.github.com](https://cli.github.com) |
| `vercel` | 部署工具 | `npm i -g vercel` |

（可选，如果某些功能需要额外工具：）
- `turso` — Turso 数据库管理工具

## 预设的配置选项

本服务提供了一些经过优化的默认配置选项，这些选项相互配合使用效果最佳。您可以通过 `SKILL-CONFIG.json` 文件自定义所有默认设置：

- **组件库**：使用 Skeleton（Svelte 5 的原生组件库）或作为备用方案的 Bits UI。
- **包管理器**：使用 pnpm。
- **部署平台**：使用 Vercel。
- **附加工具**：ESLint、Prettier、Vitest、Playwright、mdsvex、MCP。
- **状态管理**：使用 Svelte 5 的 `$state`、`$derived`、`$effect` 等函数。

有关自定义配置的详细信息，请参阅 [用户配置](#user-configuration)。

---

## 用户配置

在使用服务提供的默认配置之前，请查看 `~/.openclaw/workspace/SKILL-CONFIG.json` 文件。用户配置可以覆盖以下设置：
- **部署平台**（例如：vercel、cloudflare、netlify）。
- **包管理器**（pnpm、npm、yarn）。
- **必须包含的附加工具**。
- **MCP 集成开发环境（MCP IDE）的配置**。
- **组件库的偏好设置**。

## 工作流程概述

1. **收集信息**：收集用户的需求描述、设计参考资料以及相关问题。
2. **制定计划**：生成包含技术栈、用户故事和模拟数据策略的完整项目需求文档（PRD）。
3. **迭代优化**：与用户共同完善项目需求文档，直到达成一致。
4. **预检**：验证所有必要的认证信息和凭据。
5. **执行开发**：在用户的监督下，按照既定的流程进行构建、部署和测试。

---

## 第 1 阶段：收集项目描述

通过对话和迭代的方式了解用户的具体需求。

### 1a. 开场问题

首先提出一个开放性的问题：
- “您想要构建什么类型的应用？”
- “请描述一下您心目中的 Web 应用。”

让用户根据自己的需求来主导讨论。

### 1b. 设计参考资料

询问用户的设计灵感：
```
Share 1-3 sites you'd like this to feel like 
(design, functionality, or both).

Examples:
- "Like Notion but simpler"
- "Fieldwire's mobile-first approach"
- "Linear's clean aesthetic"
```

“展示您喜欢的设计元素”比冗长的文字描述更有效。

### 1c. 视觉识别（可选）

如果用户的设计参考资料中包含自定义品牌元素，请进一步询问：
```
Any specific colors, fonts, or logos you want to use?
(I can pre-configure the Tailwind theme)
```

### 1d. 针对性询问

根据用户描述中的空白部分，提出具体问题：
| 缺失的内容 | 需要了解的信息 |
|-----|----------|
| 用户群体不明确 | “主要用户是谁？（角色、使用场景）” |
| 核心功能不明确 | “用户必须能够完成的最基本操作是什么？” |
| 内容未知 | “是否有现有的内容或资源可以整合？” |
| 应用规模未知 | “预计会有多少用户使用？” |
| 时间表是否明确 | “是否有紧迫的截止日期？” |

只询问缺失的信息，避免过度追问。

### 1e. 确认理解

在继续之前，确认您已经准确理解了用户的需求：
```
📝 PROJECT SUMMARY: [Name]

Purpose: [one sentence]
Primary user: [who]
Core action: [what they do]
Design inspiration: [references]
Visual identity: [colors/fonts if specified]
Key features:
  • [feature 1]
  • [feature 2]
  • [feature 3]

Technical signals detected:
  • Database: [yes/no] — [reason]
  • Authentication: [yes/no] — [reason]
  • Internationalization: [yes/no] — [reason]

Does this capture it? [Yes / Adjust]
```

反复沟通，直到用户确认所有信息。

---

## 第 2 阶段：制定计划（生成项目需求文档 PRD）

生成包含技术栈、用户故事和模拟数据策略的完整项目需求文档（PRD）。

### 技术栈

**必选组件：**
```
CLI:              pnpx sv (fallback: npx sv)
Template:         minimal
TypeScript:       yes
Package manager:  pnpm (fallback: npm)

Core add-ons (via sv add):
  ✓ eslint
  ✓ prettier
  ✓ mcp (claude-code)
  ✓ mdsvex
  ✓ tailwindcss (+ typography, forms plugins)
  ✓ vitest
  ✓ playwright

Post-scaffold:
  ✓ Skeleton (primary component library — Svelte 5 native, accessible)
  ✓ Bits UI (headless primitives — fallback for gaps/complex custom UI)
  ✓ vite-plugin-pwa (PWA support)
  ✓ Svelte 5 runes mode
  ✓ adapter-auto (auto-detects deployment target)
```

**为什么选择 Skeleton 和 Bits UI？**
- Skeleton：专为 Svelte 5 设计的完整组件库，易于使用。
- Bits UI：在需要更多控制或自定义样式时提供灵活的组件。
- 这两个工具配合使用，既能保证开发效率，又能满足设计需求。

**根据用户描述推断的其他组件：**
```
drizzle     → if needs database (ask: postgres/sqlite/turso)
lucia       → if needs auth
paraglide   → if needs i18n (ask: which languages)
```

### 状态管理

遵循 Svelte 5 的最佳实践（详见 [https://svelte.dev/docs/kit/state-management]）：
- 使用 `$state()` 管理响应式状态。
- 使用 `$derived()` 计算派生值。
- 使用 Svelte 的上下文 API (`setContext`/`getContext`) 在组件间传递状态。
- 服务器状态通过 `load` 函数传递到 `data` 属性。
- **切勿** 将用户特定的状态存储在模块级别的变量中（这些变量会在多次请求间共享）。

### 代码风格偏好

请查看 `SKILL-CONFIG.json` 文件以了解用户的代码风格偏好。常见推荐：
- **优先使用 `bind:` 而不是回调**：在父组件向子组件传递数据时，使用 `bind:value` 而不是 `onchange` 回调。这样代码更简洁、易于维护。
- **避免使用 `onMount`**：使用 `$effect()` 来处理副作用。这种方式更符合 Svelte 的响应式设计原则。
- **尽可能使用 `$state()`、`$derived()`、`$effect()` 等函数**，而不是传统的状态管理方式。
- **组件大小控制**：每个组件的代码行数建议控制在 200 行左右（可通过 `SKILL-CONFIG.json` 配置调整）。如果组件变得复杂，可以考虑拆分组件。简洁的代码更易于维护。

### 目录结构

使用 `sv create` 命令生成初始目录结构：
```
src/
├── routes/          # SvelteKit routes
├── app.html         # HTML template
├── app.d.ts         # Type declarations
└── app.css          # Global styles
static/              # Static assets
```

我们还会添加以下内容：
```
src/
├── lib/
│   ├── components/  # Reusable components (Skeleton + Bits UI)
│   ├── server/      # Server-only code (db client, auth)
│   ├── stores/      # Svelte stores (.svelte.ts for runes)
│   ├── utils/       # Helper functions
│   └── types/       # TypeScript types
static/
└── icons/           # PWA icons
```

### 用户故事（prd.json）

**故事结构：**
```json
{
  "project": "ProjectName",
  "branchName": "dev",
  "description": "Brief description",
  "userStories": [
    {
      "id": "US-001",
      "title": "Scaffold project",
      "description": "Set up the base SvelteKit project.",
      "acceptanceCriteria": [...],
      "priority": 1,
      "passes": false,
      "blocked": false,
      "notes": ""
    }
  ]
}
```

**故事编写规则**：每个故事的内容应适合在一个浏览器窗口中显示。如果内容过多，可以拆分成多个故事。

**标准的故事编写顺序：**
1. **搭建基础**：使用 `pnpx sv create` 命令搭建应用框架，并安装核心组件。
2. **配置环境**：设置组件库（Skeleton 和 Bits UI）、PWA 配置、目录结构、VSCode 工作区设置以及 Tailwind 主题。
3. **准备模拟数据**：为开发环境创建模拟数据库数据。
4. **构建基础结构**：设置页面布局、设计元素以及首页内容。
5. **实现核心功能**：根据用户需求实现核心功能。
6. **搭建基础设施**：配置数据库模式、数据迁移以及身份验证（如需要）。
7. **优化应用**：设置 PWA 相关的配置文件（如 manifest 文件和图标）。
8. **编写测试**：为关键功能编写端到端（E2E）测试。

**首页检查点**：在完成首页开发后，暂停开发流程并请求用户审核。首页是整个应用的外观基础，提前获取用户反馈可以避免后续开发工作的重复。

有关故事模板的详细信息，请参阅 [references/scaffold-stories.md](references/scaffold-stories.md)。

### 模拟数据策略

开发环境使用模拟数据；生产环境使用真实的数据库数据。
```
Mock data approach:
- Generate mock data per-story as needed
- Store in src/lib/server/mocks/ or use MSW for API mocking
- E2E tests run against mock data locally
- Stage 2+ switches to real database
```

如果选择使用 `drizzle` 工具，需要编写以下相关故事：
- 初始化数据库模式。
- 配置 `drizzle` 工具。
- 执行首次数据库迁移。

### 外部依赖项

确认以下依赖项的凭据是否已准备好：
| 功能 | 所需依赖项 | 是否必须准备 |
|---------|------------|----------|
| 任何项目 | GitHub CLI | 是 |
| 部署工具 | Vercel CLI 或相关适配器 | 是 |
| 数据库（PostgreSQL） | DATABASE_URL | 需要用于测试环境 |
| 数据库（Turso） | Turso CLI | 需要用于测试环境 |
| OAuth 服务 | 客户端 ID/密钥 | 需要用于测试环境 |
- 支付服务 | Stripe API 密钥 | 需要用于测试环境 |

**开发环境使用模拟数据；测试/生产环境需要真实凭据。**

---

## 第 3 阶段：迭代优化，直至用户批准

向用户展示项目需求文档（PRD），并根据用户的反馈进行优化。

### 展示项目需求文档

```
📋 PRD: [Project Name]

TECHNICAL STACK:
✅ Always: TypeScript, Tailwind, Skeleton + Bits UI, ESLint, 
   Prettier, Vitest, Playwright, PWA
🔍 Inferred:
   [✓/✗] Database (drizzle) - [reason]
   [✓/✗] Authentication (lucia) - [reason]  
   [✓/✗] Internationalization (paraglide) - [reason]

USER STORIES: [N] stories
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
US-001: Scaffold project (Setup)
US-002: Configure Skeleton + Bits UI (Setup)
US-003: Set up mock data (Setup)
US-004: Create root layout (Foundation)
[... feature stories ...]
US-XXX: Configure PWA manifest (Polish)
US-XXX: Add E2E tests (Tests)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 External dependencies:
   • GitHub CLI (required now)
   • Vercel CLI (required now)
   • DATABASE_URL (required for staging)
   • [others for staging]

[Approve / See full stories / Edit stories / Change stack]
```

### 迭代流程

预计过程中会进行多次调整：
- 添加/删除/修改用户故事。
- 更改技术栈的选择。
- 调整故事优先级。
- 将过大的故事拆分成更小的部分。
- 明确每个故事的验收标准。

**持续迭代，直到用户明确表示批准。**

### 用户批准

当用户批准项目需求文档后，进入下一阶段。

---

## 第 4 阶段：预检

验证所有依赖项是否准备就绪。开发环境可以使用模拟数据；测试环境需要真实的凭据。

### 验证依赖项

验证以下命令行工具的认证信息是否正确：
- GitHub、pnpm、Vercel（以及可选的 Turso）。具体操作步骤请参阅 [references/cli-commands.md](references/cli-commands.md#preflight-checks)。

### 展示当前进度

```
┌─────────────────────────────────────────────┐
│ 🔐 PREFLIGHT CHECK                          │
├─────────────────────────────────────────────┤
│ For development (Stage 1):                  │
│ ✓ GitHub CLI         authenticated          │
│ ✓ pnpm               installed              │
│ ✓ Write access       verified               │
│                                             │
│ For staging (Stage 2):                      │
│ ✓ Vercel CLI         authenticated          │
│ ✗ DATABASE_URL       not set                │
│                                             │
│ ─────────────────────────────────────────── │
│ Development can start now.                  │
│ DATABASE_URL needed before Stage 2.         │
│                                             │
│ [Start development / Resolve all first]     │
└─────────────────────────────────────────────┘
```

### 下一步行动

- 开发环境可以使用模拟数据继续开发。
- 测试环境需要准备真实的数据库凭据。
- 生产环境需要在第 3 阶段之前完成凭据的配置。

---

## 第 5 阶段：执行开发

在用户的监督下，按照既定的流程进行构建、部署和测试。

### 构建过程

**实时进度更新：** 每完成一个功能，都会及时更新进度：
```
✅ US-001: Scaffold project
✅ US-002: Configure Skeleton + Bits UI
✅ US-003: Set up mock data
⏳ US-004: Create root layout (in progress)
```

---

### 第 1 阶段：开发环境

使用模拟数据在本地完成所有开发工作。

#### 设置开发环境

在 `dev` 分支上创建一个新的 Git 仓库，并生成一个 `progress.txt` 文件来记录开发进度。具体操作步骤请参阅 [references/cli-commands.md](references/cli-commands.md#initialize-repository)。

#### 并行执行任务

使用 `sessions_spawn` 命令并行执行多个任务（前提是这些任务之间没有依赖关系）。

**任务执行顺序：**
- **第 1 波段**：搭建应用框架。
- **第 2 波段**：配置应用环境（包括组件库、PWA 设置、目录结构等）。
- **第 3 波段**：设置模拟数据。
- **第 4 波段及以后**：并行执行核心功能的开发。
- **最后一波**：执行端到端测试。

**任务执行模板：**
```
Implement user story [US-XXX] for SvelteKit project at [project_path].

Story: [title]
Description: [description]

Acceptance Criteria:
- [criterion 1]
- [criterion 2]
- Typecheck passes

Instructions:
1. Read progress.txt for codebase patterns
2. Implement with minimal, focused changes
3. Use Svelte 5 runes for state ($state, $derived, $effect)
4. Use context API for cross-component state
5. Follow Conventional Commits: "feat: [US-XXX] - [title]"
6. Run `pnpm check` to verify
7. Update prd.json: passes: true
8. Append learnings to progress.txt
```

#### 处理无法完成的任务

如果某个任务无法完成，请在 `prd.json` 文件中将其标记为 `blocked: true`，并在备注字段中说明原因。然后继续执行其他可以并行执行的任务。在最终总结中报告这些无法完成的任务。

#### 第 1 阶段的完成条件

在继续下一步之前，必须通过以下检查：
- TypeScript 代码格式正确。
- 单元测试通过。
- 使用模拟数据在本地开发服务器上通过了端到端测试。

---

### 第 2 阶段：测试环境

将代码推送到主分支（`main`），然后部署到测试环境，并将模拟数据替换为真实数据。

#### 验证测试环境配置

在继续之前，请确保所有测试环境的凭据都已设置：
- 如果使用数据库，请设置 `DATABASE_URL`。
- 如果使用 OAuth 服务，请设置客户端 ID 和密钥。
- 其他必要的 API 凭据也要确保已配置。

如果缺少任何凭据，请暂停开发流程并请求用户提供。

#### 通过 GitHub-Vercel 进行部署

**推荐使用这种方式**：
- 创建一个私有的 GitHub 仓库，并将其关联到 Vercel 项目。
- 在 Vercel 的控制台（Settings → Git → Connect Git Repository）中配置仓库链接。
- 将 `dev` 分支设置为 `main` 分支。

**GitHub 集成的优势：**
- 无需额外使用 CLI 即可完成部署。
- 所有分支都能自动生成预览地址。
- 生成的部署地址格式为：`[project]-git-dev-[team].vercel.app`。
- 有助于更好地管理持续集成和持续部署（CI/CD）流程。

**部署到测试环境：**

将 `dev` 分支合并到 `main` 分支，然后推送代码。Vercel 会自动完成构建和部署。具体操作步骤请参阅 [references/cli-commands.md](references/cli-commands.md#merge-and-deploy-to-staging)。

**开发分支的预览地址：**
连接 GitHub 后，`dev` 分支会生成一个固定的预览地址：
`https://[project]-git-dev-[team].vercel.app`
这个地址在每次提交后都会保持不变，便于与团队成员分享项目进度。

#### 解决环境问题

在部署环境中可能会遇到的一些常见问题包括：
- OAuth 回调地址不正确。
- CORS 配置问题。
- Vercel 中的环境变量未正确设置。
- 数据库连接字符串错误。
- API 端点设置错误（例如使用了 `localhost`）。

**故障处理策略：**
- 根据错误日志（stdout/stderr）诊断问题类型。
- 根据错误类型采取相应的修复措施：
  - 如果是依赖项问题，使用 `pnpm install` 安装缺失的依赖。
  - 如果是类型错误，分析 `pnpm check` 的输出。
  - 如果是测试失败，重新运行测试并记录详细日志。
  - 如果是网络问题或超时问题，等待 30 秒后重试。
- 如果尝试三次仍然无法解决问题，需要寻求进一步帮助。

#### 第 2 阶段的完成条件

所有测试（包括端到端测试）都必须通过。

---

### 第 3 阶段：生产环境

将应用部署到生产环境，并将应用移交给用户。

#### 部署到生产环境

使用 GitHub-Vercel 集成，当您将代码推送到 `main` 分支时，应用会自动部署到生产环境。可以通过 Vercel 的控制台（Settings → Domains）或 CLI 配置自定义域名。具体操作步骤请参阅 [references/cli-commands.md](references/cli-commands.md#deploy-to-production)。

#### 最终验证

在部署到生产环境后，再次运行端到端测试，确保所有功能都能正常工作。具体操作步骤请参阅 [references/cli-commands.md](references/cli-commands.md#final-verification)。

#### 完成报告

生成项目管理的文档，包括管理员使用手册（`ADMIN.md`）。
```markdown
# [Project Name] — Administration Guide

## Running Locally

\`\`\`bash
pnpm install
pnpm dev          # Start dev server at localhost:5173
\`\`\`

## Environment Variables

Copy `.env.example` to `.env` and configure:
- DATABASE_URL: [description]
- [other vars]

Set these in Vercel dashboard for production.

## Project Structure

\`\`\`
src/
├── routes/           # Pages and API routes
├── lib/components/   # UI components (Skeleton + Bits UI)
├── lib/server/       # Server-only code
└── lib/stores/       # State management
\`\`\`

## Adding New Pages

1. Create `src/routes/[page-name]/+page.svelte`
2. Add server data loading in `+page.server.ts`
3. Run `pnpm check` to verify types

## Database Migrations

\`\`\`bash
pnpm drizzle-kit generate  # Generate migration
pnpm drizzle-kit push      # Apply to database
\`\`\`

## Deployment

Push to `main` branch → auto-deploys to Vercel.

## Troubleshooting

- **Type errors**: Run `pnpm check`
- **Test failures**: Run `pnpm test:e2e --debug`
- **Build issues**: Check Vercel deployment logs
```

### 提交项目

生成管理员使用的文档，并向用户提交项目完成报告。
```
📖 HANDOFF COMPLETE

Admin manual: ADMIN.md
- How to run locally
- Environment variable setup
- Project structure overview
- Adding new pages
- Database migrations
- Deployment workflow
- Troubleshooting guide

The project is ready for ongoing development.
```

---

## 错误处理

如果某个阶段出现故障且无法自动解决，请按照以下步骤处理：
1. **诊断问题**：分析错误日志。
2. **分类问题类型**：
   - 如果是依赖项问题，使用 `pnpm install` 安装缺失的依赖。
   - 如果是代码错误，显示具体的错误信息。
   - 如果是测试失败，显示失败的测试用例。
   - 如果是网络问题，尝试重新运行测试。
3. **尝试修复**：最多尝试三次，并记录修复过程。
4. **上报问题**：向用户报告问题详情、尝试的修复方法以及具体的错误信息。

**请确保项目始终能够正常运行。** 即使第 2 或第 3 阶段出现问题，开发环境仍然可以继续使用。

---

## 快速参考

有关所有命令行工具和认证验证的详细信息，请参阅 [references/cli-commands.md](references/cli-commands.md#quick-reference)。

### 默认的依赖项适配器

系统会自动选择合适的适配器：
- 如果使用 Vercel，选择 `adapter-vercel`。
- 如果使用 Cloudflare，选择 `adapter-cloudflare`。
- 如果使用 Netlify，选择 `adapter-netlify`。
- 其他情况，选择 `adapter-node`。

### 数据库配置（使用 `drizzle` 时）：

- 可以选择 `postgresql` 和 `postgres.js` 或 `neon`。
- 或者 `sqlite` 和 `better-sqlite3` 或 `libsql`。
- 如果使用 Turso，选择 `@libsql/client`。
---
name: Claude Code CLI for OpenClaw
version: 1.0.2
author: Matrix Zion (ProSkillsMD)
description: 安装、认证并使用 Claude Code CLI 作为任何 OpenClaw 代理系统的原生编码工具。
homepage: https://missiondeck.ai
tags: [claude-code, coding, cli, anthropic, agent-tools]
openclaw: ">=2026.2"
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["node", "npm"] },
        "install":
          [
            {
              "id": "listing",
              "kind": "link",
              "label": "📚 ProSkills Listing",
              "url": "https://proskills.md/skills/claude-code-cli",
            },
            {
              "id": "github",
              "kind": "link",
              "label": "GitHub Repository",
              "url": "https://github.com/ProSkillsMD/skill-claude-code-cli",
            },
            {
              "id": "missiondeck",
              "kind": "link",
              "label": "☁️ MissionDeck.ai Cloud",
              "url": "https://missiondeck.ai",
            },
          ],
      },
  }
---
# 技能：OpenClaw 的 Claude Code CLI

## 描述

本技能指导 OpenClaw 代理如何安装、认证、配置并使用 Claude Code CLI 作为编码工具。Claude Code 是 Anthropic 官方提供的 CLI，它通过基于文件的上下文处理方式显著提高了编码效率，与直接使用原始 API 相比，可减少 80-90% 的令牌使用量。

**主要优势：**
- **令牌效率：** 每个任务大约需要 500 个令牌，而直接使用原始 API 需要 10,000-50,000 个令牌（Claude Code 通过工具读取文件内容，而非将全部内容加载到上下文中）。
- **固定费用计费：** 使用 Claude Max 订阅服务（基于 OAuth 认证），而非按令牌计费。
- **更好的代码质量：** 支持对代码库的本地探索、精确编辑以及更好的代码理解能力。
- **项目上下文：** CLAUDE.md 文件可在会话之间保持项目信息的持久性。

**使用场景：**
- 代码实现与重构
- 通过文件探索进行错误修复
- 多文件代码修改
- 项目框架搭建
- 代码审查与分析

## 🎯 设置模式

| 模式 | 描述 |
|------|-------------|
| 🤖 OpenClaw 后端 | 作为 `claude-cli` 模型在任何代理中使用（例如 `claude-cli/sonnet-4.6`、`claude-cli/opus-4.6`） |
| 🖥️ 直接 CLI | 从任意项目目录运行 `claude --print` — 无需代理配置 |
| ☁️ 与 MissionDeck 集成 | 通过 JARVIS 集成在 [MissionDeck.ai](https://missiondeck.ai) 仪表板中实时跟踪 Claude Code 会话 |

## 先决条件**

- **Claude Max 订阅：** 需要用于 OAuth 认证（不能使用原始 API 密钥）
- **Node.js/npm：** 用于全局安装 CLI
- **TTY 终端：** 用于 OAuth 设置流程（使用 `pty: true` 与 `exec` 工具）
- **Git：** 建议用于管理代码分支的变更
- **OpenClaw Gateway：** 必须运行中，以便应用配置更新

## 安装

### 第一步：安装 Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

### 第二步：验证安装

```bash
which claude && claude --version
```

预期输出：
```
/usr/bin/claude
2.1.75
```

### 快速安装

使用提供的安装脚本：

```bash
cd /root/.openclaw/workspace/skills/claude-code
bash scripts/install.sh
```

该脚本负责：
- 安装 NPM 包
- 验证版本
- 准备环境配置

## 认证

Claude Code 需要使用基于浏览器的 OAuth 认证，并且必须拥有 Claude Max 订阅。原始 API 密钥（格式为 `sk-ant-api03-*`）无法使用。

### 交互式设置（一次性）

在 TTY 终端中运行以下命令：

```bash
claude setup-token
```

**流程：**
1. CLI 显示加载提示和授权 URL：
   ```
   https://claude.ai/oauth/authorize?code=true&client_id=...&code_challenge=...
   ```
2. 复制 URL 并在浏览器中打开
3. 使用您的 Claude Max 账户进行授权
4. 浏览器会显示授权码
5. 根据提示将授权码粘贴回终端：`Paste code here if prompted >`
6. 成功：`✓ 成功创建了长期有效的认证令牌！`
7. 令牌格式：`sk-ant-oat01-xxxxx`（有效期为 1 年）

### 令牌存储

令牌必须作为 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量进行存储。

**选项 1：Shell RC 文件（推荐）**
```bash
echo "export CLAUDE_CODE_OAUTH_TOKEN=YOUR_OAUTH_TOKEN_HERE" >> /root/.bashrc
echo "export CLAUDE_CODE_OAUTH_TOKEN=YOUR_OAUTH_TOKEN_HERE" >> /root/.profile
source /root/.bashrc
```

**选项 2：系统级存储**
```bash
echo "CLAUDE_CODE_OAUTH_TOKEN=YOUR_OAUTH_TOKEN_HERE" >> /etc/environment
```

**选项 3：仅用于 OpenClaw 配置**

将令牌添加到 `openclaw.json` 配置文件中（见下一节）——该令牌仅在调用 OpenClaw 后端时生效，不适用于直接使用 CLI 的情况。

### 🔒 安全警告

**重要提示：** **切勿将 `CLAUDE_CODE_OAUTH_TOKEN` 提交到版本控制系统中。**
- ✅ 将令牌存储在环境变量或秘密管理工具中
- ✅ 将 `.env*` 文件添加到 `.gitignore` 文件中
- ✅ 使用 OpenClaw 配置文件（不提交到 Git）
- ❌ 切勿在脚本中硬编码令牌
- ❌ 切勿公开分享令牌或将其包含在截图中
- ❌ 切勿将令牌提交到 GitHub/GitLab

**将以下内容添加到 `.gitignore` 文件中：**
```gitignore
.env
.env.local
.env.*.local
openclaw.json
config.patch
```

### 验证

```bash
echo $CLAUDE_CODE_OAUTH_TOKEN
# Should output: sk-ant-oat01-xxxxx
```

## OpenClaw 配置

将 Claude Code 作为 CLI 后端集成到 OpenClaw 中，将其设置为默认模型或备用模型。

### 配置文件

创建或修改 `~/.openclaw/config.patch` 文件：

```json
{
  "agents": {
    "defaults": {
      "cliBackends": {
        "claude-cli": {
          "command": "/usr/bin/claude",
          "env": {
            "CLAUDE_CODE_OAUTH_TOKEN": "YOUR_OAUTH_TOKEN_HERE"
          }
        }
      },
      "models": {
        "claude-cli/opus-4.6": {
          "alias": "claude-cli-opus"
        },
        "claude-cli/sonnet-4.6": {
          "alias": "claude-cli-sonnet"
        }
      }
    },
    "list": [
      {
        "id": "tank",
        "model": {
          "primary": "anthropic/claude-opus-4-5",
          "fallbacks": [
            "google/gemini-3-flash-preview",
            "claude-cli/opus-4.6"
          ]
        }
      }
    ]
  }
}
```

### 应用配置

```bash
gateway config.patch
```

在 OpenClaw 后端日志中验证配置，或通过启动编码会话进行测试。

### 可用模型

- `claude-cli/sonnet-4.6` → Claude Sonnet 4.6（快速通用编码）
- `claude-cli/opus-4.6` → Claude Opus 4.6（复杂推理、架构设计）

可以将其设置为默认模型、备用模型，或通过 `exec` 命令直接调用。

## 项目设置（CLAUDE.md）

**重要提示：** 每个项目根目录下都必须有一个 `CLAUDE.md` 文件。这是项目的核心配置文件，Claude Code 会在会话开始时自动读取它。

### 应包含的内容

```markdown
# Project: [Name]

## Overview
[1-2 sentence project description]

## Tech Stack
- Language: [e.g., TypeScript, Python, Rust]
- Framework: [e.g., Next.js, FastAPI, Supabase]
- Key Dependencies: [list major packages]

## Directory Structure
```
/
├── src/           # 源代码
├── public/        # 静态资源
├── supabase/      # 数据库功能、迁移脚本
└── docs/          # 文档
```

## Key Files
- `src/App.tsx` - Main app component, routing
- `src/lib/supabase.ts` - Database client
- `supabase/functions/` - Edge functions (24 total)

## Coding Standards
- Use TypeScript strict mode
- Functional components (React)
- Tailwind CSS for styling
- ESLint + Prettier configured

## Deployment
- Platform: Netlify (frontend), Supabase (backend)
- Deploy command: `npm run build`
- Environment: `.env.local` (never commit)

## Critical Rules
- Never commit API keys
- Always run `npm run build` before pushing
- All functions must have TypeScript types

## Testing
- `npm test` - Run Jest tests
- `npm run lint` - Check code style
```

### 模板使用

复制提供的模板并进行自定义：

```bash
cp /root/.openclaw/workspace/skills/claude-code/templates/CLAUDE.md.template /path/to/your/project/CLAUDE.md
# Edit with project-specific details
```

### 实际示例

对于 MissionDeck 项目，我们创建了：
- `/root/.openclaw/workspace/missiondeck/CLAUDE.md`
- 结果：Claude Code 立即了解了项目的 24 个边缘功能、注册流程以及所有路由规则和编码规范
- 在提示中无需额外提供任何上下文信息

## 代理工作流程

### 日常编码工作流程

**步骤 1：同步项目**
```bash
cd /path/to/project
git pull origin main
```

**步骤 2：使用 Claude Code 执行任务**
```bash
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Fix the signup redirect bug in src/pages/AuthVerify.tsx — users aren't being redirected to /dashboard after magic link verification"
```

**步骤 3：审查提议的更改**

Claude Code 会：
- 搜索代码库
- 确定受影响的文件
- 提出带有差异的修改建议
- 解释修改原因

**步骤 4：构建检查**
```bash
npm run build  # or npm test, cargo build, etc.
```

**步骤 5：提交并推送更改**
```bash
git checkout -b agent/fix-signup-redirect
git add .
git commit -m "fix: redirect to /dashboard after magic link verification"
git push origin agent/fix-signup-redirect
```

**步骤 6：创建 Pull Request（可选）**
```bash
gh pr create --title "Fix signup redirect" --body "Fixes redirect bug in AuthVerify.tsx"
```

### OpenClaw 的 `exec` 命令使用方式

对于使用 `exec` 工具的代理：

```javascript
exec({
  command: `cd /path/to/project && CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Your task here"`,
  workdir: "/path/to/project",
  pty: false  // PTY not needed for --print mode
})
```

### 子代理的启动方式（未来版本）

一旦配置了 ACP（Agent Configuration Platform），可以使用以下方式启动 Claude Code：

```javascript
sessions_spawn({
  runtime: "acp",
  agentId: "claude-code",
  message: "Fix the navbar bug in components/Navbar.tsx",
  label: "claude-code-navbar-fix"
})
```

## 提示模式

有效的提示方式能带来更好的结果。以下是一些经过验证的提示模板：

### 1. 先规划再执行的方法

```
"Show me your plan first. List every file you'll touch and what changes you'll make. Wait for my approval before implementing."
```

**原因：** 可防止不必要的更改，让您能够更好地控制编码过程

### 2. 挑战模式

```
"Fix the authentication bug. After you're done, grill yourself — what edge cases did you miss? What could break?"
```

**原因：** 强制代理进行更深入的推理，有助于发现边缘情况

### 3. RPI 工作流程（研究 → 规划 → 实施）

对于复杂任务，可以使用以下三个步骤的提示：

**提示 1（研究）：**
```
"Research how the payment flow works. Show me all relevant files and how they connect."
```

**提示 2（规划）：**
```
"Now plan how to add recurring billing. List the changes step-by-step."
```

**提示 3（实施）：**
```
"Implement the plan. Make the changes."
```

**原因：** 将复杂任务分解为可管理的阶段

### 4. 明确的指令**

```
"In src/pages/AuthVerify.tsx, line 42, the redirect after magic link verification is broken. Expected behavior: redirect to /dashboard. Current behavior: stays on /verify. Fix it."
```

**原因：** 明确的指令有助于更精确地执行修改

### 5. 以文件为中心的提示**

```
"Refactor src/lib/database.ts — extract the connection pool logic into a separate file src/lib/db-pool.ts"
```

**原因：** Claude Code 在文件级别操作方面表现出色

### 应避免的提示模式**

❌ 表达模糊：例如 “改进应用程序”
❌ 不提供上下文：例如 “修复错误”
❌ 范围过广：例如 “重写整个代码库”
❌ 提示不明确：例如 “更新配置文件（具体是哪个文件？）”
✅ 具体明确：例如 “修复 `src/pages/AuthVerify.tsx` 中的跳转错误——用户应在电子邮件验证后访问 `/dashboard`”
✅ 范围明确：例如 “将 `src/lib/auth.ts` 中的认证逻辑重构为使用 `async/await`”

## 使用 Claude Code 与直接使用原始 API 的比较

### 令牌使用量对比

| 方法 | 每个任务的令牌数量 | 计费方式 |
|--------|----------------|------------|
| 原始 API（全文件加载） | 10,000 - 50,000 | 按令牌计费 |
| Claude Code（基于工具） | 约 500 个令牌 | 固定费用（Claude Max 订阅） |

**节省效果：** 令牌使用量减少 80-90%

### 工作原理

**原始 API 方式：**
```
User: "Fix the bug in App.tsx"
Agent: [reads entire App.tsx] [dumps 5,000 tokens into context] [generates fix] [writes back]
Cost: ~7,000 tokens
```

**Claude Code 方式：**
```
User: "Fix the bug in App.tsx"
Claude Code: [uses file tool to read App.tsx] [analyzes in isolation] [generates fix] [uses edit tool]
Cost: ~500 tokens
```

**结果：** 代码质量不变，但令牌使用量减少 90%，采用固定费用计费**

### 代码质量优势

- **代码库探索：** Claude Code 可搜索文件并理解其结构
- **精确编辑：** 基于工具的编辑方式，而非简单的正则表达式替换
- **上下文感知：** 自动读取 CLAUDE.md 文件，无需额外提示
- **多文件操作：** 支持跨文件的导入和依赖关系处理

## 实际案例

### 任务示例

**任务：** 从 MissionDeck 的导航栏中移除优惠/折扣提示**

**处理流程：**
```bash
cd /root/.openclaw/workspace/missiondeck
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Remove the discount banner from the navbar"
```

**Claude Code 的执行过程：**
1. Claude Code 在代码库中搜索 “banner”、“discount” 和 “navbar” 关键字
2. 在 `src/components/Navbar.tsx` 文件中找到 `DiscountBanner` 组件
3. 确定需要修改的两处内容：
   - 移除 `import { DiscountBanner } from './DiscountBanner'`
   - 移除 `<DiscountBanner />` 这一行 JSX 代码
4. 提出修改建议并显示差异
5. 构建成功：`npm run build` ✓
6. 将更改推送到分支：`oracle/disable-discount-banner`
7. 合并到主分支并部署到生产环境

**令牌使用量：** 约 450 个令牌
**耗时：** 30 秒
**结果：** 修改准确无误，代码成功部署

## 常见问题及解决方法

### 问题：“认证失败”

**原因：** 令牌过期或无效

**解决方法：**
```bash
claude setup-token  # Re-authenticate
# Update token in environment and OpenClaw config
```

### 问题：“找不到命令：claude”

**原因：** NPM 全局安装的 `claude` 命令未添加到系统路径中

**解决方法：**
```bash
export PATH="$PATH:$(npm bin -g)"
echo 'export PATH="$PATH:$(npm bin -g)"' >> /root/.bashrc
```

### 问题：“无法读取 CLAUDE.md”

**原因：** 项目中缺少 CLAUDE.md 文件

**解决方法：**
```bash
cp /root/.openclaw/workspace/skills/claude-code/templates/CLAUDE.md.template /path/to/project/CLAUDE.md
# Edit with project details
```

### 问题：设置过程中出现 “需要 TTY 终端”的错误**

**解决方法（使用 OpenClaw 的 `exec` 命令）：**
```javascript
exec({
  command: "claude setup-token",
  pty: true  // Enable pseudo-terminal
})
```

### 问题：“文件或目录不存在”

**原因：** 从错误的目录中运行 Claude Code

**解决方法：** 总是先使用 `cd` 命令进入项目根目录
```bash
cd /path/to/project
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "your task"
```

### 问题：更改未应用**

**原因：** Claude Code 提出了修改建议，但需要用户确认**

**解决方法：** 使用 `--print` 标志以非交互模式运行命令（输出到标准输出）
```bash
claude --print "your task"  # No approval needed, just shows output
```

**对于需要用户确认的交互模式：**
```bash
claude  # Interactive, will wait for y/n approval
```

## 高级用法

### 批量操作

**顺序执行多个任务：**
```bash
cd /path/to/project
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Task 1: Fix auth bug"
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Task 2: Add new endpoint"
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Task 3: Update tests"
```

### 强制使用特定模型**

**方法：**
```bash
claude --model opus-4.6 --print "Complex architecture refactor"
claude --model sonnet-4.6 --print "Quick bug fix"
```

### 与 Git 工作流程的集成**

```bash
# Create feature branch
git checkout -b feature/claude-code-implementation

# Run Claude Code
CLAUDE_CODE_OAUTH_TOKEN=$CLAUDE_CODE_OAUTH_TOKEN claude --print "Implement feature X"

# Review changes
git diff

# Commit
git add .
git commit -m "feat: implement X using claude-code"

# Push
git push origin feature/claude-code-implementation
```

## 最佳实践**

1. **务必创建 CLAUDE.md 文件** — 它是项目的核心配置文件，有助于节省令牌使用量
2. **使用特性分支** — 切勿直接将代码提交到主分支
3. **在提交前先执行构建** — 可提前发现潜在问题
4. **提供明确的指令** — 包括文件路径和预期行为
5. **审查提出的更改** — Claude Code 提供了很好的辅助工具，但仍需人工审核
6. **安全存储令牌** — 使用环境变量而非硬编码
7. **在开始工作前先同步代码** — 使用 `git pull` 避免冲突
8. **对于复杂任务，先进行规划** — 在实施前获取用户确认

## 参考资源

- **[MissionDeck.ai](https://missiondeck.ai)** — 用于跟踪 Claude Code 会话和多代理协作的云平台
- **[ProSkills 主页](https://proskills.md)** — 更多 OpenClaw 技能和资源
- **[Claude Code 官方文档](https://docs.anthropic.com/en/docs/claude-code)** — Anthropic 官方文档
- **[GitHub 仓库](https://github.com/ProSkillsMD/skill-claude-code-cli)** — 该技能的源代码仓库
- **[NPM 包](https://www.npmjs.com/package/@anthropic-ai/claude-code)** — Claude Code CLI 的 NPM 包
- **[Claude Max 订阅](https://claude.ai/upgrade)** — 使用 OAuth 认证所必需的订阅服务

## 技能元数据

- **版本：** 1.0.2
- **作者：** Matrix Zion (ProSkillsMD)
- **官网：** https://missiondeck.ai
- **创建时间：** 2026-03-13
- **更新时间：** 2026-03-14
- **许可证：** BSD 3 条款
- **依赖项：** Node.js、npm、Claude Max 订阅
- **兼容性：** OpenClaw 2026.2 及更高版本

---

**下一步操作：**
1. 安装 Claude Code：`npm install -g @anthropic-ai/claude-code`
2. 进行认证：`claude setup-token`
3. 配置 OpenClaw：将 CLI 后端添加到 `config.patch` 文件中
4. 创建项目配置文件 `CLAUDE.md`：复制模板并进行自定义
5. 开始编码：`CLAUDE_CODE_OAUTH_TOKEN=$token claude --print "your task"`

---

## Asif2BD 的其他相关内容

```bash
clawhub install jarvis-mission-control    # Free agent command center with Claude Code session tracking
clawhub install openclaw-token-optimizer  # Reduce token costs by 50-80%
clawhub search Asif2BD                    # All skills
```

---

[MissionDeck.ai](https://missiondeck.ai) · 免费试用 · 无需信用卡
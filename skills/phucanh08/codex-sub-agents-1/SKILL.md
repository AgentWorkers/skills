---
name: codex-cli
description: "使用 OpenAI Codex CLI 执行编码任务。支持的命令包括：codex、code review、fix CI、refactor code、implement feature、coding agent、gpt-5-codex。该工具允许 Clawdbot 将编码工作委托给 Codex CLI，既可以作为子代理（subagent）使用，也可以直接作为独立工具使用。"
---

# OpenAI Codex CLI 技能

使用 OpenAI Codex CLI（`codex`）执行编码任务，包括代码审查、重构、漏洞修复、持续集成（CI）问题处理以及功能实现。Codex CLI 可在您的本地机器上运行，并具备对整个文件系统的完整访问权限。

## 使用场景

- 用户请求进行代码修改、重构或功能实现
- 持续集成/构建（CI）过程中出现故障需要修复
- 在提交代码之前进行代码审查
- 需要探索或解释大型代码库
- 需要执行文件编辑和命令操作的任务
- 当需要利用 GPT-5-Codex 模型的强大功能（如代码生成、工具使用）时

## 安装与授权

使用 Codex CLI 需要 ChatGPT Plus/Pro/Business/Enterprise 订阅。

```bash
# Install
npm i -g @openai/codex

# Authenticate (opens browser for OAuth)
codex login

# Or use API key
printenv OPENAI_API_KEY | codex login --with-api-key

# Verify auth
codex login status
```

## 核心命令

### 交互式模式（TUI）
```bash
codex                           # Launch interactive terminal UI
codex "explain this codebase"   # Start with a prompt
codex --cd ~/projects/myapp     # Set working directory
```

### 非交互式模式（脚本执行）
```bash
codex exec "fix the CI failure"                    # Run and exit
codex exec --full-auto "add input validation"      # Auto-approve workspace writes
codex exec --json "list all API endpoints"         # JSON output for parsing
codex exec -i screenshot.png "match this design"   # With image input
```

### 会话管理
```bash
codex resume               # Pick from recent sessions
codex resume --last        # Continue most recent
codex resume <SESSION_ID>  # Resume specific session
```

## 斜杠命令（TUI 中使用）

| 命令 | 功能 |
|---------|---------|
| `/model` | 切换模型（gpt-5-codex, gpt-5） |
| `/approvals` | 设置审批模式（自动、只读、全权限） |
| `/review` | 对分支、未提交的更改或特定提交进行代码审查 |
| `/diff` | 显示 Git 差异（包括未跟踪的文件） |
| `/compact` | 将对话内容简化以节省上下文空间 |
| `/init` | 生成 AGENTS.md 模板文件 |
| `/status` | 显示会话配置和令牌使用情况 |
| `/undo` | 撤销最近的操作 |
| `/new` | 启动新的对话 |
| `/mcp` | 列出已配置的 MCP 工具 |
| `/mention <路径>` | 将文件附加到对话中 |

## 审批模式

| 模式 | 行为 |
|------|----------|
| **自动**（默认） | 在工作区内读取/编辑/执行命令；需要外部访问权限 |
| **只读** | 仅允许浏览文件；对更改需要审批 |
| **全权限** | 具有对整个机器的访问权限（请谨慎使用） |

## 关键参数

| 参数 | 功能 |
|------|---------|
| `--model, -m <模型>` | 更改使用的模型（gpt-5-codex, gpt-5） |
| `--cd, -C <路径>` | 设置工作目录 |
| `--add-dir <路径>` | 添加额外的可写目录 |
| `--image, -i <路径>` | 将图片附加到提示信息中 |
| `--full-auto` | 允许在工作区内写入代码并在失败时自动审批 |
| `--sandbox <模式>` | 只读模式、允许在工作区内写入代码、但权限较高（风险较高） |
| `--json` | 以换行符分隔的 JSON 格式输出结果 |
| `--search` | 启用网页搜索功能 |

## Clawdbot 集成模式

### 模式 1：直接执行工具
通过 Clawdbot 的执行工具调用 Codex 来执行编码任务：

```bash
# In Clawdbot session
exec codex exec --full-auto --cd ~/projects/medreport "fix the TypeScript errors in src/components"
```

### 模式 2：子代理委托
创建一个使用 Codex 的子代理来执行编码任务：

```json5
// In agents.defaults or per-agent config
{
  agents: {
    list: [
      {
        id: "coder",
        workspace: "~/clawd-coder",
        model: "openai-codex/gpt-5.2",  // Uses Codex auth
        tools: {
          allow: ["exec", "read", "write", "edit", "apply_patch", "process"]
        }
      }
    ]
  }
}
```

### 模式 3：CLI 后端备用方案
将 Codex 配置为仅文本的备用方案：

```json5
{
  agents: {
    defaults: {
      cliBackends: {
        "codex-cli": {
          command: "codex",
          args: ["exec", "--full-auto"],
          output: "text",
          sessionArg: null  // Codex manages its own sessions
        }
      }
    }
  }
}
```

### 模式 4：MCP 服务器模式
将 Codex 作为 MCP 服务器为其他代理提供服务：

```bash
codex mcp-server  # Exposes Codex tools via stdio MCP
```

## Clawdbot 配置：OpenAI Codex 提供者

通过 `openai-codex` 提供者使用您的 ChatGPT Pro 订阅：

```json5
{
  agents: {
    defaults: {
      model: { primary: "openai-codex/gpt-5.2" },
      models: {
        "openai-codex/gpt-5.2": { alias: "Codex" },
        "anthropic/claude-opus-4-5": { alias: "Opus" }
      }
    }
  }
}
```

授权信息会自动从 `~/.codex/auth.json` 同步到 Clawdbot 的用户配置文件中。

## 代码审查工作流程

```bash
# Interactive review
codex
/review  # Choose: branch, uncommitted, or specific commit

# Non-interactive
codex exec "review the changes in this PR against main branch"
```

## 多目录项目

```bash
# Work across monorepo packages
codex --cd apps/frontend --add-dir ../backend --add-dir ../shared

# Or in TUI
codex --cd ~/projects/myapp --add-dir ~/projects/shared-lib
```

## 自定义斜杠命令

在 `~/.codex/prompts/` 目录下创建可重用的提示模板：

```markdown
<!-- ~/.codex/prompts/pr.md -->
---
description: Prepare and open a draft PR
argument-hint: [BRANCH=<name>] [TITLE="<title>"]
---

Create branch `dev/$BRANCH` if specified.
Stage and commit changes with a clear message.
Open a draft PR with title $TITLE or auto-generate one.
```

调用方式：`/prompts:pr BRANCH=feature-auth TITLE="添加 OAuth 流程"`

## MCP 集成

通过添加 MCP 服务器来扩展 Codex 的功能：

```bash
# Add stdio server
codex mcp add github -- npx @anthropic/mcp-server-github

# Add HTTP server
codex mcp add docs --url https://mcp.deepwiki.com/mcp

# List configured
codex mcp list
```

## 网页搜索

在 `~/.codex/config.toml` 中启用网页搜索功能：

```toml
[features]
web_search_request = true

[sandbox_workspace_write]
network_access = true
```

这样 Codex 就可以搜索当前的文档、API 等资源。

## 最佳实践

1. **使用 `/init` 命令** 创建包含仓库特定说明的 AGENTS.md 文件。
2. **在提交代码之前使用 `/review` 命令** 进行 AI 代码审查。
3. **适当设置 `/approvals` 模式**——对于受信任的仓库使用自动审批，对于探索性用途使用只读模式。
4. **使用 `--add-dir` 参数** 来处理单仓库项目，而不是使用全权限模式。
5. **恢复会话** 以保持不同编码会话之间的上下文一致性。
6. **附加图片**（如用于 UI 设计、错误截图等）。

## 示例工作流程

### 修复 CI 故障
```bash
codex exec --full-auto "The CI is failing on the lint step. Fix all ESLint errors."
```

### 重构组件
```bash
codex exec --cd src/components "Refactor UserProfile.tsx to use React Query instead of useEffect for data fetching"
```

### 根据规范实现新功能
```bash
codex exec -i spec.png --cd ~/projects/app "Implement this feature based on the design spec"
```

### 提交代码审查请求（PR）
```bash
codex exec "Review the diff between main and feature/auth branch. Focus on security issues."
```

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 认证失败 | 先运行 `codex logout`，然后重新登录 |
| 命令被阻止 | 检查 `/approvals` 设置，可能需要使用 `--full-auto` 参数 |
| 上下文丢失 | 使用 `/compact` 命令简化对话内容 |
| 路径错误 | 使用 `--cd` 参数或查看 `/status` 信息 |
| 模型不可用 | 确认订阅等级是否支持所需的模型 |

## 参考资料

- [Codex CLI 概述](https://developers.openai.com/codex/cli)
- [Codex CLI 功能](https://developers.openai.com/codex/cli/features)
- [Codex CLI 参考文档](https://developers.openai.com/codex/cli/reference)
- [斜杠命令指南](https://developers.openai.com/codex/cli/slash-commands)
- [AGENTS.md 规范](https://agents.md)
- [Codex GitHub 仓库](https://github.com/openai/codex)
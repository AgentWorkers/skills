# 项目状态同步（Project Context Sync）

在每次提交后，都会更新项目状态的文档，以便任何代理（或未来的会话）能够立即了解项目的当前状况。

## 功能介绍

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Git Commit  │ ──▶ │ Post-commit Hook │ ──▶ │ PROJECT_STATE.md    │
│             │     │                  │     │ (auto-updated)      │
└─────────────┘     └──────────────────┘     └─────────────────────┘
```

每次提交后，该钩子会执行以下操作：
1. 收集 Git 信息（最后一次提交、最近的历史记录、分支、更改的文件）
2. （可选）调用大型语言模型（LLM）生成智能摘要
3. 更新仓库根目录下的 `PROJECT_STATE.md` 文件

## 安装

```bash
# From the repo you want to enable:
cd /path/to/your/repo
/path/to/skills/project-context-sync/scripts/install.sh
```

如果你具备相关技能，也可以通过以下方式安装：
```bash
project-context-sync install
```

安装过程包括：
1. 在 `.git/hooks/` 目录下创建一个提交后钩子
2. 创建一个名为 `.project-context.yml` 的配置文件（包含默认配置）
3. 生成初始的 `PROJECT_STATE.md` 文件
4. 将 `PROJECT_STATE.md` 添加到 `.gitignore` 文件中

## 卸载

```bash
cd /path/to/your/repo
/path/to/skills/project-context-sync/scripts/uninstall.sh
```

## 手动更新

无需提交即可触发更新：
```bash
cd /path/to/your/repo
/path/to/skills/project-context-sync/scripts/update-context.sh
```

## 配置

在仓库根目录下编辑 `.project-context.yml` 文件以进行配置：

```yaml
project_context:
  # Use AI to generate smart summaries (default: true)
  ai_summary: true
  
  # How many recent commits to include
  recent_commits: 5
  
  # Include diff stats in context
  include_diff_stats: true
  
  # Sections to include
  sections:
    - last_commit
    - recent_changes
    - current_focus    # AI-generated
    - suggested_next   # AI-generated
```

### AI 摘要模式

**当 `ai_summary: true` 时**（默认设置）：
- 生成关于更改内容的智能摘要
- 根据最近的提交模式推断当前的项目重点
- 提出下一步的操作建议
- 需要消耗令牌（token），但能提供丰富的上下文信息
- **要求**：必须启用 Gateway HTTP API（详见下文）

**当 `ai_summary: false` 时**：
- 仅记录原始的 Git 信息
- 执行速度快且无需额外费用
- 智能性较低，但仍具有一定的实用性

### 启用 Gateway HTTP API

AI 模式会使用 Clawdbot 支持 OpenAI 的接口（`/v1/chat/completions`）。出于安全考虑，该接口默认是禁用的。要启用该功能，请按照以下步骤操作：

```json5
// ~/.clawdbot/clawdbot.json
{
  "gateway": {
    "http": {
      "endpoints": {
        "chatCompletions": { "enabled": true }
      }
    }
  }
}
```

**安全注意事项：**
- 该接口继承了 Clawdbot 的认证机制（需要使用 bearer token）
- 当 `bind: "loopback"` 时（默认设置），只有本地进程可以访问该接口
- 脚本会自动从 `~/.clawdbot/clawdbot.json` 文件中读取令牌
- 对于本地开发环境来说，风险非常低

## 输出结果

`PROJECT_STATE.md` 文件将包含以下内容：

```markdown
# Project State
*Auto-updated by project-context-sync*

## Last Commit
- **Hash:** abc123
- **Message:** Implement isPro check for app blocking
- **Branch:** feature/subscription-gating
- **When:** 2026-01-29 12:34
- **Files changed:** 3

## Recent Changes
- abc123: Implement isPro check for app blocking
- def456: Add PaywallPrompt component
- ...

## Current Focus
[AI-generated summary of what's being worked on]

## Suggested Next Steps
[AI-suggested based on commit patterns]
```

## 其他说明：
- `PROJECT_STATE.md` 文件默认会被 Git 忽略（会在本地重新生成）
- 使用 AI 摘要功能需要 Clawdbot 运行
- 如果未启用 Clawdbot，系统将回退到仅记录原始 Git 信息的模式
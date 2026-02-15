---
name: claude-code-mastery
version: "1.4.3"
description: "掌握 Claude Code，用于完成各种编码任务。该工具包含设置脚本、开发团队子代理（入门包或完整团队版本）、自我提升的学习系统、诊断工具以及故障排除功能。"
author: "Clawdbot Community"
license: "MIT"
metadata: {"openclaw":{"emoji":"🧑‍💻"}}
---

# Claude Code精通

本文档介绍了如何设置、优化并全面掌握Claude Code，以及如何使用其包含的多个子代理（subagents）来构建一个完整的开发团队。

**官方文档：** https://code.claude.com/docs

---

## ⚡ 快速检查：设置是否完成？

**首先运行以下命令：**
```bash
command -v claude >/dev/null && echo "✅ Claude Code installed - SKIP to 'Daily Use' section" || echo "❌ Not installed - follow 'First-Time Setup' below"
```

如果Claude Code已经安装完成，请**直接跳转到下面的“日常使用”部分**。

---

# 🔧 首次设置（如果已安装则跳过）

> **提示：** 仅当Claude Code未安装时才需要按照此步骤操作。请使用上述命令检查安装情况。设置完成后，在后续使用中可以忽略此部分。

## 设置脚本

请按顺序运行以下脚本：
```bash
cd ~/clawd/skills/claude-code-mastery/scripts

# 1. Check dependencies
./01-check-dependencies.sh

# 2. Install Claude Code
./02-install-claude-code.sh

# 3. Authenticate
./03-first-time-auth.sh

# 4. Install dev team subagents
./04-install-subagents.sh              # Starter pack (3 agents) - recommended
./04-install-subagents.sh --full-team  # All 11 agents

# 5. (Optional) Persistent memory - prompts y/N, default No
./05-setup-claude-mem.sh               # Interactive prompt
./05-setup-claude-mem.sh --skip        # Skip entirely
./05-setup-claude-mem.sh --yes         # Install without prompting
```

## 配置

编辑`config.sh`文件以自定义设置：
- `VALID_MODELS`：根据Anthropic发布的模型进行添加
- `HEARTBEAT_DIAGNOSTICS`：启用或禁用心跳诊断功能（默认为禁用）
- `INSTALL_MODE`：默认设置为“starter”或“full”

## 设置过程中可能遇到的问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| “命令未找到” | 将`~/.local/bin`添加到PATH环境变量中 |
| 认证错误 | 运行`./03-first-time-auth.sh` |
| 启动缓慢 | 首次运行时需要索引代码库 |
| 子代理未显示 | 运行`./04-install-subagents.sh` |

## 设置完成后：添加心跳维护任务

设置完成后，请将相应的维护任务添加到`HEARTBEAT.md`文件中（具体方法请参见“日常使用”部分的“心跳维护”章节）。

**设置完成！请继续阅读“日常使用”部分。**

---

# 📘 日常使用（始终适用）

本部分介绍了Claude Code的日常使用方法，适用于所有编码任务。

## 开发团队子代理

子代理安装在`~/.claude/agents/`目录下。每个子代理都有一个“了解更多”（“Learn More”）部分，其中包含有助于提升专业能力的精选链接。

### 基础套餐（默认配置）——3个核心子代理

大多数用户只需要以下3个子代理：
| 子代理 | 使用的模型 | 功能 |
|-------|-------|---------|
| `senior-dev` | Sonnet | 负责架构设计、处理复杂代码及代码审查 |
| `project-manager` | Sonnet | 负责任务分解、制定时间表及管理项目依赖关系 |
| `junior-dev` | **Haiku** | 负责快速修复问题及处理简单任务 |

安装方法：`./04-install-subagents.sh`（或使用`--minimal`参数）

### 完整团队配置（可选）——10个子代理

对于大型项目，可以使用`--full-team`参数安装全部10个子代理：
| 子代理 | 使用的模型 | 功能 |
|-------|-------|---------|
| `senior-dev` | Sonnet | 负责架构设计、处理复杂代码及代码审查 |
| `project-manager` | Sonnet | 负责任务分解、制定时间表及管理项目依赖关系 |
| `junior-dev` | **Haiku** | 负责快速修复问题及处理简单任务 |
| `frontend-dev` | Sonnet | 负责前端开发（React、UI、CSS） |
| `backend-dev` | Sonnet | 负责后端开发（API、数据库） |
| `ai-engineer` | Sonnet | 负责AI应用开发、RAG（Retrieval-Augmentation-Generation）及提示系统 |
| `ml-engineer` | Sonnet | 负责机器学习模型开发及MLOps（Machine Learning Operations） |
| `data-scientist` | Sonnet | 负责数据分析及统计工作 |
| `data-engineer` | Sonnet | 负责数据管道建设、ETL（Extract-Transform-Load）及数据基础设施管理 |
| `product-manager` | Sonnet | 负责需求管理、用户故事梳理及任务优先级排序 |
| `devops` | Sonnet | 负责持续集成/持续交付（CI/CD）、Docker、Kubernetes及自动化运维 |

## 使用子代理

**交互模式：** 可使用`/agent`命令或自然语言进行交互：
```
/agent senior-dev
Use the senior-dev agent to review this code
```

**非交互模式（使用`-p`参数）：** 可使用`--agent`参数指定子代理：
```bash
claude --agent senior-dev -p "review this code for security issues"
claude --agent project-manager -p "create a task breakdown for auth feature"
claude --agent junior-dev -p "fix the typo in README.md"
```

**注意：** Claude Code不会根据任务类型自动分配子代理，必须明确指定使用哪个子代理。

**多代理协作：** 对于需要多个专家参与的任务，可使用`HANDOFF.md`文件来传递任务上下文。具体流程请参考`docs/workflows.md`。

---

## 快速参考

### 命令行接口（CLI）命令
```bash
claude              # Start interactive
claude -c           # Continue previous session
claude -p "prompt"  # Non-interactive mode
```

### 斜杠命令（Slash Commands）
```
/agents   - Manage subagents
/clear    - Clear conversation (use between tasks!)
/compact  - Compress context
/model    - Change model
/help     - All commands
```

### 键盘快捷键
```
Shift+Tab - Toggle Plan mode (read-only exploration)
Ctrl+C    - Cancel operation
Ctrl+B    - Background task
```

---

## 上下文管理（非常重要！）

| 命令 | 功能 | 使用场景 |
|---------|--------------|-------------|
| `/clear` | 清除对话记录，重新开始 | 在处理不同任务之间使用 |
| `/compact` | 总结并压缩对话上下文 | 当上下文信息过多时使用 |
| `Shift+Tab` | 切换到计划模式（仅读模式） | 在执行操作前进行预览 |

**最佳实践：**
1. 在处理不同任务之间使用`/clear`命令清除对话记录。
2. 在执行操作前使用计划模式预览任务内容。
3. 使用子代理来处理复杂操作。
4. 为确保会话连续性，创建`HANDOFF.md`文件。

---

## 项目配置

### settings.json

在项目中创建`.claude/settings.json`文件：
```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["Bash(npm:*)", "Bash(git:*)", "Read", "Write", "Edit"],
    "deny": ["Bash(rm -rf:*)", "Bash(sudo:*)"]
  }
}
```

### CLAUDE.md

在项目根目录下创建`CLAUDE.md`文件（Claude会自动读取该文件）：
```markdown
# Project: MyApp

## Tech Stack
- Frontend: React, TypeScript, Tailwind
- Backend: Node.js, PostgreSQL

## Commands
- `npm run dev` - Start dev server
- `npm test` - Run tests
```

具体模板请参考`examples/CLAUDE-template.md`。

---

## Claude-Mem（如果已安装）

检查Claude Code的状态：
```bash
pgrep -f "worker-service" >/dev/null && echo "running" || echo "stopped"
```

如果Claude Code停止运行，可以重新启动它：
```bash
cd ~/.claude/plugins/marketplaces/thedotmack && bun plugin/scripts/worker-service.cjs start
```

Web界面访问地址：http://localhost:37777

---

## 诊断与故障排除

**快速诊断：**
```bash
~/clawd/skills/claude-code-mastery/scripts/06-diagnostics.sh
```

**全面故障排除（如遇到问题）：**
```bash
~/clawd/skills/claude-code-mastery/scripts/08-troubleshoot.sh
```

**常见问题解决方案：** 请参阅`docs/troubleshooting.md`，其中包含以下问题的解决方法：
- 认证问题（API密钥、OAuth认证、登出故障）
- 安装问题（PATH环境变量设置、WSL环境、Node.js版本问题）
- 网络问题（防火墙设置、VPN使用、代理设置）
- 性能问题（CPU使用率过高、程序卡顿、搜索速度慢）

---

## 心跳维护

将以下维护任务添加到`HEARTBEAT.md`文件中，以实现自动维护：
```markdown
## Claude Code Maintenance

**Last Health Check:** [timestamp]
**Last Learning Session:** [timestamp]

### Every Heartbeat (if coding tasks active):
1. Quick claude-mem check (if installed):
   `pgrep -f "worker-service" >/dev/null && echo "running" || echo "stopped"`
   - Only restart if stopped
   - Note: pgrep saves ~500 tokens vs full status command

### Daily (morning):
1. Quick health check: `command -v claude && pgrep -f "worker-service"`
2. Only run full diagnostics if quick check fails

### Weekly (Sunday):
1. Run: `~/clawd/skills/claude-code-mastery/scripts/07-weekly-improvement-cron.sh`
2. Propose improvements (require human approval)

### Weekly Learning & Skill Improvement (rotate through agents):
1. Pick ONE agent file from the skill's `agents/` folder (rotate weekly)
2. Read the "Learn More" section
3. Visit 2-3 links that are relevant to current projects
4. Internalize key concepts and update your workflows
5. **Improve the skill itself:**
   - Found a better resource? Add it to "Learn More"
   - Discovered a new best practice? Update the agent's guidelines
   - Link broken or outdated? Remove or replace it
   - New tool or framework worth mentioning? Add it
6. Commit changes locally with clear commit messages
7. **Don't push directly to shared repos** — propose changes as a PR or request human review first
8. Note learnings in your memory files

**Rotation schedule:**
- Week 1: senior-dev, junior-dev
- Week 2: frontend-dev, backend-dev
- Week 3: ai-engineer, ml-engineer
- Week 4: data-scientist, data-engineer
- Week 5: project-manager, product-manager
- Week 6: devops

**What to update:**
- `agents/*.md` — Add new links, update best practices, fix outdated info
- `SKILL.md` — Improve documentation, add tips discovered
- `docs/*.md` — Enhance guides based on real usage
```

**这样做的重要性：**
- 实际使用过程中技能会不断提升。
- 链接内容会保持最新状态（失效的链接会得到修复）。
- 随着技术生态的发展，最佳实践也会不断更新。
- 每个使用Claude Code的开发者都会为系统的持续改进做出贡献。

---

## 脚本参考

| 脚本 | 功能 | 使用场景 |
|--------|---------|-------------|
| `06-diagnostics.sh` | 系统健康检查及状态报告 | 在出现问题时使用 |
| `07-weekly-improvement-cron.sh` | 生成每周改进报告 | 每周日自动执行 |
| `08-troubleshoot.sh` | 全面故障排除 | 在`06-diagnostics.sh`检测到问题时使用 |

---

## 总结

**对于编码任务：**
1. 根据任务类型选择合适的子代理。
2. 使用`/clear`命令和计划模式来管理对话上下文。
3. 如遇到问题，请运行相应的诊断工具。

**心跳维护功能包括：**
- 定期检查Claude Code的运行状态。
- 每日进行快速故障诊断。
- 每周生成改进方案。

通过使用这些子代理，开发团队可以高效地利用Claude Code构建完整的开发环境。
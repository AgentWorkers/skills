---
name: clawvault
version: 1.5.1
description: OpenClaw代理的结构化内存系统：具备上下文恢复能力（通过检查点/恢复机制实现）、结构化存储功能、兼容Obsidian的Markdown格式支持、本地语义搜索功能以及会话记录的修复机制。
author: Versatly
repository: https://github.com/Versatly/clawvault
---

# ClawVault 🐘

大象永远不会忘记。专为 OpenClaw 代理设计的结构化记忆系统。

> **专为 [OpenClaw](https://openclaw.ai) 开发** — 通过 `clawhub install clawvault` 进行安装

## 安装

```bash
npm install -g clawvault
```

## 设置

```bash
# Initialize vault (creates folder structure + templates)
clawvault init ~/my-vault

# Or set env var to use existing vault
export CLAWVAULT_PATH=/path/to/memory

# Optional: shell integration (aliases + CLAWVAULT_PATH)
clawvault shell-init >> ~/.bashrc
```

## 新代理的快速入门

```bash
# Start your session (recover + recap + summary)
clawvault wake

# Capture and checkpoint during work
clawvault capture "TODO: Review PR tomorrow"
clawvault checkpoint --working-on "PR review" --focus "type guards"

# End your session with a handoff
clawvault sleep "PR review + type guards" --next "respond to CI" --blocked "waiting for CI"

# Health check when something feels off
clawvault doctor
```

## 核心命令

### 唤醒（Wake）+ 睡眠（Sleep）（主要功能）

```bash
clawvault wake
clawvault sleep "what I was working on" --next "ship v1" --blocked "waiting for API key"
```

### 按类型存储记忆

```bash
# Types: fact, feeling, decision, lesson, commitment, preference, relationship, project
clawvault remember decision "Use Postgres over SQLite" --content "Need concurrent writes for multi-agent setup"
clawvault remember lesson "Context death is survivable" --content "Checkpoint before heavy work"
clawvault remember relationship "Justin Dukes" --content "Client contact at Hale Pet Door"
```

### 快速将内容捕获到收件箱

```bash
clawvault capture "TODO: Review PR tomorrow"
```

### 搜索（需要安装 qmd）

```bash
# Keyword search (fast)
clawvault search "client contacts"

# Semantic search (slower, more accurate)
clawvault vsearch "what did we decide about the database"
```

## 上下文恢复能力

### 唤醒（会话开始）

```bash
clawvault wake
```

### 睡眠（会话结束）

```bash
clawvault sleep "what I was working on" --next "finish docs" --blocked "waiting for review"
```

### 创建检查点（频繁保存状态）

```bash
clawvault checkpoint --working-on "PR review" --focus "type guards" --blocked "waiting for CI"
```

### 恢复（手动检查）

```bash
clawvault recover --clear
# Shows: death time, last checkpoint, recent handoff
```

### 会话移交（手动结束会话）

```bash
clawvault handoff \
  --working-on "ClawVault improvements" \
  --blocked "npm token" \
  --next "publish to npm, create skill" \
  --feeling "productive"
```

### 总结（重新启动新会话）

```bash
clawvault recap
# Shows: recent handoffs, active projects, pending commitments, lessons
```

## 自动链接

在 markdown 文件中，当提到 Wiki 实体时，可以使用以下链接格式：

```bash
# Link all files
clawvault link --all

# Link single file
clawvault link memory/2024-01-15.md
```

## 文件夹结构

```
vault/
├── .clawvault/           # Internal state
│   ├── last-checkpoint.json
│   └── dirty-death.flag
├── decisions/            # Key choices with reasoning
├── lessons/              # Insights and patterns
├── people/               # One file per person
├── projects/             # Active work tracking
├── handoffs/             # Session continuity
├── inbox/                # Quick captures
└── templates/            # Document templates
```

## 最佳实践

1. **在会话开始时唤醒代理** — 使用 `clawvault wake` 恢复上下文
2. **在高强度工作期间每 10-15 分钟创建一个检查点**
3. **在会话结束前让代理进入睡眠状态** — 使用 `clawvault sleep` 保存后续操作
4. **明确存储内容的类型** — 了解存储内容有助于决定其存储位置
5. **广泛使用 Wiki 链接** — 例如 `[[person-name]]` 可以帮助构建你的知识图谱

## AGENTS.md 的检查清单

```markdown
## Memory Checklist
- [ ] Run `clawvault wake` at session start
- [ ] Checkpoint during heavy work
- [ ] Capture key decisions/lessons with `clawvault remember`
- [ ] Use wiki-links like `[[person-name]]`
- [ ] End with `clawvault sleep "..." --next "..." --blocked "..."`
- [ ] Run `clawvault doctor` when something feels off
```

## 会话记录修复（v1.5.0+）

当 Anthropic API 返回 “在 tool_result 块中发现了未预期的 tool_use_id” 错误时，可以使用以下命令进行修复：

```bash
# See what's wrong (dry-run)
clawvault repair-session --dry-run

# Fix it
clawvault repair-session

# Repair a specific session
clawvault repair-session --session <id> --agent <agent-id>

# List available sessions
clawvault repair-session --list
```

**修复内容：**
- 修复那些引用不存在的 `tool_use` ID 的孤立 `tool_result` 块
- 修复因 JSON 数据不完整而导致的工具调用失败问题
- 修复损坏的父链引用问题

系统会自动创建备份（使用 `--no-backup` 可以跳过备份功能）。

## 故障排除

- **未安装 qmd** — 运行 `bun install -g github:tobi/qmd` 或 `npm install -g qmd`
- **找不到 ClawVault** — 运行 `clawvault init` 或设置 `CLAWVAULT_PATH`
- **CLAWVAULT_PATH 未配置** — 运行 `clawvault shell-init` 并将其添加到 shell 配置文件中
- **存在过多的孤立链接** — 运行 `clawvault link --orphans`
- **收件箱积压警告** — 处理或归档收件箱中的内容
- **出现 “unexpected tool_use_id” 错误** — 运行 `clawvault repair-session`

## 与 qmd 的集成

ClawVault 使用 [qmd](https://github.com/tobi/qmd) 进行搜索功能：

```bash
# Install qmd
bun install -g github:tobi/qmd

# Add vault as collection
qmd collection add /path/to/vault --name my-memory --mask "**/*.md"

# Update index
qmd update && qmd embed
```

## 环境变量

- `CLAWVAULT_PATH` — 默认的存储路径（跳过自动检测）

## 链接信息

- npm: https://www.npmjs.com/package/clawvault
- GitHub: https://github.com/Versatly/clawvault
- 问题报告：https://github.com/Versatly/clawvault/issues
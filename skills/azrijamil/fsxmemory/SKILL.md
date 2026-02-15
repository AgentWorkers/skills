---
name: fsxmemory
version: 1.3.1
description: 专为AI代理设计的结构化内存系统：具备上下文丢失时的恢复能力（通过检查点/恢复机制实现）、结构化存储功能、兼容Obsidian标记语言（markdown格式），以及支持本地语义搜索。
author: Foresigxt
repository: https://github.com/Foresigxt/foresigxt-cli-memory
---

# Foresigxt Memory

这是一个专为AI代理设计的内存管理系统，具有结构化的存储机制。

## 安装

```bash
npm install -g @foresigxt/foresigxt-cli-memory
```

## 设置

### 选项1：初始化新的存储库（Vault）

```bash
# Initialize vault (creates folder structure + templates)
fsxmemory init ~/memory
```

### 选项2：使用现有的存储库

**对于独立的工作空间内存**（每个工作空间都有自己的存储库）：

```bash
# Create .env in workspace root
echo 'FSXMEMORY_PATH=/path/to/workspace/memory' > .env

# All agents in THIS workspace use this isolated vault
fsxmemory stats  # Works automatically!
```

**对于所有工作空间共享的内存**：

```bash
# Set global environment variable (in ~/.bashrc or ~/.zshrc)
export FSXMEMORY_PATH=/path/to/shared/memory

# All agents in ALL workspaces share the same vault
```

**或者**：使用`--vault`标志进行一次性覆盖：

```bash
fsxmemory stats --vault /path/to/other/vault
```

## 核心命令

### 按类型存储内存数据

```bash
# Types: fact, feeling, decision, lesson, commitment, preference, relationship, project, procedural, semantic, episodic
fsxmemory remember decision "Use Postgres over SQLite" --content "Need concurrent writes for multi-agent setup"
fsxmemory remember lesson "Context death is survivable" --content "Checkpoint before heavy work"
fsxmemory remember relationship "Justin Dukes" --content "Client contact at Hale Pet Door"
fsxmemory remember procedural "Deploy to Production" --content "1. Run tests 2. Build 3. Deploy"
fsxmemory remember semantic "Event Loop Concept" --content "JavaScript's concurrency model..."
fsxmemory remember episodic "First Production Deploy" --content "Deployed v2.0 today, team was nervous but it went well"
```

### 快速将数据捕获到收件箱

```bash
fsxmemory capture "TODO: Review PR tomorrow"
```

### 搜索（需要安装qmd）

```bash
# Keyword search (fast)
fsxmemory search "client contacts"

# Semantic search (slower, more accurate)
fsxmemory vsearch "what did we decide about the database"
```

## 上下文恢复能力

### 创建检查点（频繁保存状态）

```bash
fsxmemory checkpoint --working-on "PR review" --focus "type guards" --blocked "waiting for CI"
```

### 恢复数据（在程序启动时检查）

```bash
fsxmemory recover --clear
# Shows: death time, last checkpoint, recent handoff
```

### 任务交接（在会话结束前）

```bash
fsxmemory handoff \
  --working-on "Foresigxt Memory improvements" \
  --blocked "npm token" \
  --next "publish to npm, create skill" \
  --feeling "productive"
```

### 总结（重新启动新会话）

```bash
fsxmemory recap
# Shows: recent handoffs, active projects, pending commitments, lessons
```

## 从其他格式迁移数据

可以从OpenClaw、Obsidian或其他基于Markdown的系统迁移现有的存储库数据：

### 先进行分析（预测试）

```bash
# See what would be changed without modifying files
fsxmemory migrate --from openclaw --vault /path/to/vault --dry-run
```

### 带备份进行迁移

```bash
# Recommended: Creates automatic backup before migration
fsxmemory migrate --from openclaw --vault /path/to/vault --backup

# The migration:
# ✅ Adds YAML frontmatter to all markdown files
# ✅ Renames directories (procedural→procedures, semantic→knowledge, episodic→episodes)
# ✅ Creates .fsxmemory.json config file
# ✅ Preserves all content and custom categories
# ✅ Creates timestamped backup for rollback
```

### 如有需要，可回滚数据

```bash
# Restore from backup if something went wrong
fsxmemory migrate --rollback --vault /path/to/vault
```

### 迁移选项

```bash
# Available source formats
--from openclaw      # OpenClaw vault format
--from obsidian      # Obsidian vault format
--from generic       # Generic markdown vault

# Migration flags
--dry-run           # Preview changes without modifying files
--backup            # Create backup before migration (recommended)
--force             # Skip confirmation prompts
--verbose           # Show detailed progress
--rollback          # Restore from last backup
```

### 示例：迁移OpenClaw存储库数据

```bash
# 1. Analyze first
fsxmemory migrate --from openclaw --vault ~/.openclaw/workspace/memory --dry-run

# 2. Run migration with backup
fsxmemory migrate --from openclaw --vault ~/.openclaw/workspace/memory --backup --verbose

# 3. Verify migration worked
fsxmemory stats --vault ~/.openclaw/workspace/memory
fsxmemory doctor --vault ~/.openclaw/workspace/memory
```

**迁移速度**：约53个文件，耗时0.07秒 ⚡

## 自动链接

在Markdown文件中，可以自动链接到相关实体：

```bash
# Link all files
fsxmemory link --all

# Link single file
fsxmemory link memory/2024-01-15.md
```

## 模板参考

Foresigxt Memory提供了结构化的模板，以帮助保持文档的一致性。模板位于`templates/`目录下。

### 可用的模板

| 模板 | 类型 | 用途 | 包含的章节 |
|----------|------|---------|----------|
| `decision.md` | 决策 | 关键选择、架构决策 | 背景信息、选项、决策过程、结果 |
| `procedure.md` | 流程指南 | 操作步骤、工作流程、标准操作程序 | 目的、前提条件、步骤、注意事项、验证方法 |
| `knowledge.md` | 术语解释 | 概念、定义、思维模型 | 定义、关键概念、示例、重要性说明 |
| `episode.md` | 事件记录 | 事件、经历、会议记录 | 发生的事情、背景信息、关键时刻、反思 |
| `person.md` | 人物信息 | 联系人、关系记录 | 联系方式、角色、合作方式、互动记录 |
| `project.md` | 项目文档 | 当前工作、项目进展 | 目标、状态、下一步行动、阻碍因素 |
| `lesson.md` | 经验总结 | 学到的经验、模式 | 情境描述、经验教训、应用场景 |
| `handoff.md` | 任务交接 | 会话延续性 | 当前工作内容、背景信息、下一步行动、阻碍因素 |
| `daily.md` | 日志记录 | 日常笔记 | 重点内容、已完成事项、备注 |

### 模板的使用方法

系统会自动根据内存数据的类型选择合适的模板：

```bash
fsxmemory remember decision "Title" --content "..."    # → templates/decision.md
fsxmemory remember procedural "Title" --content "..."  # → templates/procedure.md
fsxmemory remember semantic "Title" --content "..."    # → templates/knowledge.md
fsxmemory remember episodic "Title" --content "..."    # → templates/episode.md
fsxmemory remember relationship "Name" --content "..." # → templates/person.md
fsxmemory remember lesson "Title" --content "..."      # → templates/lesson.md
```

**查看模板结构**：在创建内存文档之前，请先阅读`templates/`目录下的模板文件。

**模板特点**：
- 使用YAML格式编写，包含元数据（标题、日期、类型、状态）
- 模板结构清晰，包含占位符以指导内容填写
- 提供Wiki链接功能，便于建立知识链接
- 自动生成标签以便于搜索和分类

## 文件夹结构

```
vault/
├── .fsxmemory/           # Internal state
│   ├── last-checkpoint.json
│   └── dirty-death.flag
├── decisions/            # Key choices with reasoning
├── lessons/              # Insights and patterns
├── people/               # One file per person
├── projects/             # Active work tracking
├── procedures/           # How-to guides and workflows
├── knowledge/            # Concepts and definitions
├── episodes/             # Personal experiences
├── handoffs/             # Session continuity
├── inbox/                # Quick captures
└── templates/            # Document templates (9 types)
```

## 最佳实践

1. 在高负荷工作时，每10-15分钟创建一个检查点。
2. 在会话结束前完成数据交接——这会对未来的工作有所帮助。
3. 在程序启动时检查数据是否丢失。
4. 根据数据类型来存储数据——了解要存储的内容有助于确定存储位置。
5. 尽量使用Wiki链接——`[[人物名称]]`可以帮助构建你的知识图谱。

## 与qmd的集成

Foresigxt Memory使用[qmd](https://github.com/tobi/qmd)进行数据搜索：

```bash
# Install qmd
bun install -g github:tobi/qmd

# Add vault as collection
qmd collection add /path/to/vault --name my-memory --mask "**/*.md"

# Update index
qmd update && qmd embed
```

## 配置

Foresigxt Memory支持三种设置存储库路径的方法（优先级从高到低）：

### 1. 命令行参数（最高优先级）
```bash
fsxmemory stats --vault /path/to/vault
```

### 2. 环境变量
```bash
export FSXMEMORY_PATH=/path/to/memory
fsxmemory stats
```

### 3. `.env`文件（适用于独立工作空间的内存管理）
```bash
# Create .env in workspace root
cat > .env << 'EOF'
FSXMEMORY_PATH=/home/user/.openclaw/workspace/memory
EOF

# All fsxmemory commands in this workspace use this isolated vault
fsxmemory stats
fsxmemory checkpoint --working-on "task"
```

**在以下情况下使用`.env`文件**：
- ✅ **隔离工作空间内存**——每个项目都有独立的存储库
- ✅ **针对不同项目的配置**——不同工作空间中的代理使用不同的存储库
- ✅ **确保便携性**——工作空间代理能自动使用正确的存储库
- ✅ **保护数据安全**——将`.env`文件添加到`.gitignore`中以避免版本控制问题

**在以下情况下使用全局配置**：
- ✅ **跨工作空间共享数据**——所有代理使用同一个存储库
- ✅ **实现知识集中管理**——所有项目共享统一的数据来源

**环境变量示例**：
- `FSXMEMORY_PATH` — 存储库路径（可以在shell命令或`.env`文件中设置）

## 发布技能包

要创建一个可 distributable 的技能包（包含SKILL.md和templates/目录），请按照以下步骤操作：

```bash
# Package the skill
npm run package-skill

# Output: dist-skill/fsxmemory-skill.zip (~8KB)
```

**包内容**：
- `SKILL.md` - 完整的文档和参考资料
- `templates/` - 所有的9个模板文件
- `.env.example` - 配置模板
- `INSTALL.md` - 快速设置指南

**分发方式**：
将`fsxmemory-skill.zip`文件分享给其他代理或团队。他们可以从中获取：
- 完整的技能文档
- 可直接使用的模板
- 配置示例

**对于OpenClaw/ClaudeHub**：
打包好的技能包可以直接上传到技能仓库中。

## 链接

- npm: https://www.npmjs.com/package/@foresigxt/foresigxt-cli-memory
- GitHub: https://github.com/Foresigxt/foresigxt-cli-memory
- 问题反馈：https://github.com/Foresigxt/foresigxt-cli-memory/issues
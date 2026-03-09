---
name: loci
description: Structured memory system with domains, decay, and links for AI agents. Replaces flat MEMORY.md with a palace of organized, weighted, interconnected memories. Use when: (1) storing important context, decisions, or learnings, (2) recalling prior knowledge before answering, (3) periodic memory maintenance (heartbeat walks), (4) migrating from flat memory files. Based on Method of Loci (memory palace) — forced structure, capacity limits, association links, and natural decay.
---

# loci — 专为AI代理设计的结构化记忆系统

**GitHub:** https://github.com/bayhax/loci | **ClawHub:** `clawhub install loci`

## 快速入门

```bash
LOCI="node <skill_dir>/scripts/loci.mjs"

# Initialize palace (first time only)
$LOCI init

# Store a memory
$LOCI store work "Switched to Claude Opus model per user preference" --tag model --tag preference

# Recall memories
$LOCI recall "what model does the user prefer"

# Walk through palace (do this during heartbeats)
$LOCI walk

# See overview
$LOCI status
```

## 核心概念

**领域（Domains）** — 用于组织记忆的类别（类似于房间）。每个领域都有容量限制。
默认领域：工作（work）、知识（knowledge）、人员（people）、工具（tools）、偏好（preferences）、档案（archive）。

**记忆（Memories）** — 存储在特定领域中的信息片段。每个记忆包含：
- 唯一ID（例如：`e3a7f2c1`）
- 内容文本
- 用于分类的标签
- 链接到相关记忆的链接
- 随时间逐渐减弱的权重

**权重衰减（Decay）** — 记忆的权重会随着自上次访问以来的时间呈指数级减少。
计算公式：`weight = base_weight × e^(-decay_rate × days_since_access)`
默认衰减率：0.05（半衰期约为14天）。

**链接（Links）** — 不同领域内相关记忆之间的双向连接。

## 命令

| 命令 | 功能 |
|---------|---------|
| `init` | 创建一个新的记忆存储结构（仅执行一次） |
| `store <domain> <content>` | 添加记忆。可选参数：`--tag`、`--link` |
| `recall <query>` | 进行搜索。可选参数：`--domain`、`--top N` |
| `walk` | 遍历所有记忆并检查其状态 |
| `prune` | 删除已衰减的记忆。可选参数：`--threshold`、`--dry-run` |
| `status` | 查看所有领域的状态 |
| `inspect <id>` | 查看记忆的详细信息及链接 |
| `link <id1> <id2>` | 将两个记忆关联起来 |
| `domains` | 列出/添加/删除领域 |
| `export` | 以Markdown或JSON格式导出数据。可选参数：`--format md\|yaml` |

## 与Heartbeats的集成

在Heartbeats任务执行过程中，运行以下命令：

```bash
$LOCI walk --decay 0.05
```

该命令会报告各领域的状态、识别需要删除的记忆，并更新记忆检查的时间戳。
定期使用 `$LOCI prune --dry-run` 命令来检查哪些记忆需要被删除。

## 何时存储数据，何时忽略数据

**应存储的数据：** 决策、用户偏好、环境特性、经验教训、重要人物/关系、重复出现的模式等。

**应忽略的数据：** 短暂性的任务细节、一次性执行的命令、已经记录在日常记忆文件中的内容。

**经验法则：** 如果未来的你认为这些信息在两周后仍然有用，就将其存储起来。

## 记忆存储文件

默认存储位置：`~/.openclaw/workspace/loci_palace.json`
可以通过 `--palace PATH` 参数更改存储路径。
文件格式：JSON。完全依赖Node.js环境（随OpenClaw一起提供）。
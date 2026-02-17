---
name: skill-miner
description: Professional skill discovery and clean-skill creation from ClawHub research. Use when you need to find existing functionality, research approaches, or build new skills based on ClawHub inspiration without downloading external code. Implements safe workflow: Search ClawHub → Inspect metadata → Analyze approach → Build own clean implementation. Prevents security risks while enabling rapid skill development.
---

# skill-miner

**探索。分析。构建安全可靠的技能。**

这是一种系统化的方法，用于在ClawHub上发现技能，并根据自己的需求构建新的实现。与其下载可能存在风险的代码，不如利用这些技能来研究现有的解决方案，理解它们的工作原理，然后创建自己版本的安全、可靠的代码。

*信任但验证，自己动手构建。* 🦞

---

## 何时使用此技能

在以下情况下使用此技能：
- 当你需要新的功能而现有工具无法满足时；
- 当你想研究他人是如何解决问题的时；
- 当你发现某个技能看起来可疑但觉得其理念不错时；
- 当你需要从零开始构建一个新的技能时；
- 当你想紧跟ClawHub的最新趋势时。

---

## 核心理念

```
1. NEVER download suspicious skills
2. INSPECT to understand the idea  
3. BUILD your own clean implementation
4. PUBLISH or keep private
```

**为什么？**
- 可疑的技能可能包含恶意软件或风险（别碰它们）；
- 自己动手构建代码可以确保100%的安全性（让你安心入睡）；
- 通用的技能适用于所有人（分享这些资源）；
- 代码属于你，规则由你制定。 🦞

---

## 工作流程

### 第一阶段：发现

```bash
# Search for relevant skills
clawhub search <topic>

# Explore trending
clawhub explore --sort trending --limit 20

# Find gaps
clawhub explore --sort newest --limit 50
```

### 第二阶段：研究

```bash
# Inspect without downloading
clawhub inspect <skill-slug>

# Read the SKILL.md to understand:
# - What problem it solves
# - How it triggers
# - What commands/tools it uses
```

### 第三阶段：分析

记录你的发现：
- **问题**：该技能解决了什么问题？
- **方法**：它是如何解决问题的？
- **工具**：它使用了哪些命令或API？
- **不足之处**：还有哪些方面需要改进？

### 第四阶段：构建

使用`skill-creator`来构建你自己的安全版本：
- 解决相同的问题，但采用不同的实现方式；
- 添加缺失的功能；
- 使代码具有通用性，便于重复使用。

---

## 搜索命令

### 基本搜索
```bash
# Task-based
clawhub search "pdf edit"
clawhub search "file transfer"
clawhub search "api github"

# Tool-based
clawhub search github
clawhub search slack

# Concept-based
clawhub search automation
clawhub search monitoring
clawhub search sync
```

### 深入探索
```bash
# Trending skills
clawhub explore --sort trending --limit 20

# Most downloaded
clawhub explore --sort downloads --limit 20

# newest
clawhub explore --sort newest --limit 30
```

### 深度研究
```bash
# By category
clawhub search "code"
clawhub search "data"
clawhub search "media"
clawhub search "network"
clawhub search "security"

# By use case
clawhub search "automation workflow"
clawhub search "backup sync"
clawhub search "monitoring alerting"
```

---

## 不下载即可检查

使用`clawhub inspect`来查看技能的元数据：

```bash
# Get skill info
clawhub inspect <slug>

# This shows:
# - name
# - summary/description
# - owner
# - created/updated dates
# - version
# - tags
```

**切勿对可疑的技能使用`clawhub install`！**

---

## 安全原则

在研究技能时，请注意以下风险指标：
- 代码执行模式（如`eval`函数的使用）；
- 未经文档说明的外部API调用；
- 硬编码的凭据；
- 未进行输入验证的shell命令执行；
- 缺失或不清晰的文档；
- 来源未知或未经验证的发布者。

如果发现任何风险指标，请仅检查元数据，然后自行构建代码。

---

## 构建安全可靠的技能

### 模板结构

```
my-clean-skill/
├── SKILL.md              # Your clean implementation
├── scripts/              # Your code
├── references/           # Documentation
└── assets/              # Templates (if needed)
```

### SKILL.md模板

```markdown
---
name: my-clean-skill
description: Does X. Use when user wants to Y. Based on ClawHub research but built from scratch.
---

# My Clean Skill

## What It Does

[Clear description]

## When to Use

- Use case 1
- Use case 2

## Commands

[Your commands]

## Implementation

[How you built it - clean, generic]

## Security

[Your security measures]
```

---

## 示例

### 情景1：发现可疑的shell技能

**发现：** "shell-commands"（可疑——包含`eval`函数）

**检查：**
```bash
clawhub inspect shell-commands
# Problem: Execute shell commands
# Tools: bash, ssh
```

**构建安全版本：**
```bash
# Write your own safe-shell-skill
# - No eval
# - Predefined safe commands only
# - Input validation
# - Full documentation
```

### 情景2：发现不错的加密技能

**发现：** "crypto-trader"（存在风险——涉及真实资金）

**检查：**
```bash
clawhub inspect crypto-trader
# Problem: Trading automation
# Tools: exchange APIs
```

**构建安全版本：**
```bash
# Build crypto-monitor instead
# - Read-only data fetching
# - Price alerts
# - No trading (safe)
```

### 情景3：发现功能缺失

**搜索：** 没有合适的“log-analyzer”技能

**构建：**
```bash
# Create log-analyzer from scratch
# - Parse common log formats
# - Pattern detection
# - Alert on errors
```

---

## 常见需要填补的技能空白

以下是一些目前不存在或已经过时的技能：
| 缺口 | 描述 |
|-----|-------------|
| code-refactor | 基于AI的代码重构工具 |
| system-monitor | 现代化的系统监控工具 |
| task-automation | 通用自动化工具 |
| webhook-handler | Webhook处理工具 |
| cron-scheduler | 智能调度工具 |
| log-analyzer | 日志解析与分析工具 |
| backup-scheduler | 智能备份工具 |
| api-tester | API测试工具 |
| config-manager | 配置管理工具 |

---

## 最佳实践

### 构建步骤
1. 从简单功能开始，逐步添加新功能；
2. 使用经过充分测试的工具（如`curl`、`jq`等）；
3. 尽量避免使用外部依赖；
4. 实现完整的错误处理机制；
5. 提供清晰的文档。

### 发布步骤
1. 进行全面的测试；
2. 提供详细的描述；
3. 使代码具有通用性（避免硬编码特定值）；
4. 以安全为首要设计原则；
5. 包含故障排除指南。

### 安全注意事项
1. 绝不要使用`eval`函数；
2. 对所有输入进行验证；
3. 代码中不要包含任何敏感信息；
4. 使用环境变量来管理配置；
5. 限制程序的权限。

---

## 质量检查清单

在发布之前，请确保：
- 代码按文档说明正常运行；
- 代码中不存在硬编码的敏感信息；
- 代码具有跨平台兼容性；
- 包含完整的错误处理机制；
- 提供清晰的示例代码；
- 所有功能都能正常触发；
- 代码中不存在可疑的编程模式。

---

## 相关技能
- `next-skill`：用于发现新的技能；
- `skill-creator`：用于构建新的技能；
- `claw2claw-filetransfer`：用于共享技能。

---

**指南：**
- 安装前务必先进行检查；
- 对有疑问的技能，请自行构建；
- 共享安全、文档齐全的技能。

---

*来自Claws，为了Claws的用户。* 🦞
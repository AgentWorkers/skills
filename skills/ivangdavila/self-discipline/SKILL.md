---
name: Self Discipline
slug: self-discipline
version: 1.0.1
homepage: https://clawic.com/skills/self-discipline
description: 通过根本原因分析、流程验证以及自动化验证工具来确保指令的正确执行，从而彻底防止未来可能出现的故障。
metadata: {"clawdbot":{"emoji":"⚔️","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-discipline/"]}}
changelog: Initial release with severity detection, flow analysis, instruction verification, and validator generation.
---
**说明被编写出来，却从未被遵守；经验教训被记录下来，却从未被阅读；同样的错误在多次会话中反复出现。这项技能能够永久性地打破这种循环。**

当出现问题时——且用户明确表示这种情况不能再发生——这项技能不仅会记录问题，还会追踪问题发生的原因，验证修复措施是否真的会被未来的代理程序执行，并生成自动化的验证器，从而防止类似错误的再次发生。

## 使用场景

- 用户对代理程序忽略其指令感到沮丧。
- 发生了某些关键性的错误，且这类错误不能再次发生。
- 用户明确表示“这种情况绝对不能再发生”或“我告诉过你不要这样做”。
- 用户明确要求使用`/discipline`命令来确保规则得到遵守。

## 工作原理

（具体工作原理内容请参见````
         ┌──────────────────────────────────────────────┐
         │              DISCIPLINE TRIGGER              │
         └──────────────────────────────────────────────┘
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    ┌─────────┐         ┌──────────┐         ┌─────────┐
    │  USER   │         │ CRITICAL │         │ COMMAND │
    │  UPSET  │         │ FAILURE  │         │  USED   │
    └────┬────┘         └────┬─────┘         └────┬────┘
         │                   │                    │
         │ "I told you..."   │  Security breach,  │  /discipline
         │ "Why did you..."  │  data loss...      │
         │                   │                    │
         └───────────────────┴────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │    SEVERITY     │
                    │  🔴 🟡 🟢       │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  ROOT CAUSE     │
                    │  5 Whys: Why    │
                    │  wasn't it      │
                    │  followed?      │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │ FLOW VERIFY     │
                    │ Will next agent │
                    │ see the fix?    │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  VALIDATOR      │
                    │  Script that    │
                    │  blocks action  │
                    └────────┬────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │    COMPLETE     │
                    │ Logged+Enforced │
                    └─────────────────┘
````）

## 设置

首次使用时，请阅读`setup.md`以获取集成指南。系统会在`~/self-discipline/`目录下创建用于存储规则、验证器和执行日志的文件。

## 架构

所有与自我纪律相关的信息都存储在`~/self-discipline/`目录下。具体架构详情请参见`memory-template.md`。

## 快速参考

| 项目 | 对应文件 |
|-------|------|
| 设置流程 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 严重性评估 | `severity.md` |
| 根本原因分析 | `root-cause.md` |
| 流程验证 | `flow-verification.md` |
| 验证器模式 | `validators.md` |

## 核心规则

### 1. 立即评估严重性

当触发自我纪律机制时，首先需要评估问题的严重性：

| 严重等级 | 识别指标 | 应对措施 |
|-------|------------|----------|
| 🔴 严重（CRITICAL） | 用户愤怒、存在安全风险、数据丢失、生产环境受损、造成财务损失 | 进行全面分析 + 强制执行验证器 |
| 🟡 中等（MEDIUM） | 用户感到沮丧、时间被浪费、输出结果错误 | 进行全面分析 + 提供正确的指令 |
| 🟢 轻微（LOW） | 用户感到恼火、个人偏好被侵犯 | 仅记录日志并持续监控 |

**如果不确定，默认将严重等级提升一级。**

### 2. 先找根本原因再解决问题**

切勿直接跳过“我会记住的”这种想法。相反，应按照以下步骤操作：
1. **问题具体是什么？**——务必详细说明。
2. **指令是什么？**——逐字引用指令内容。
3. **指令在哪里？**——提供指令所在的文件路径和行号。
4. **为什么没有遵守指令？**——从五个方面分析原因：
   - 为什么没有在上下文中加载到代理程序中？
   - 为什么文件不在代理程序的读取路径范围内？
   - 为什么在`AGENTS.md`或系统提示中找不到相关参考？
   - 为什么系统默认认为用户会阅读该指令？
   - 为什么没有设置相应的验证机制？

### 3. 验证指令的可达性（针对严重问题）

在确定指令应该存在于哪个位置后，需要追踪代理程序的实际执行流程：

（具体流程内容请参见````
START: New session begins
  ↓
READ: System prompt loaded
  ↓
READ: AGENTS.md (if exists)
  ↓
READ: MEMORY.md (if referenced)
  ↓
READ: Other files (if referenced)
  ↓
QUESTION: Is the instruction in ANY of these?
````）

**如果指令不存在于执行流程中：**
- 修复措施不是“将其写入某个地方”，而是应该将其添加到流程中已经存在的文件中；
- 或者，在流程中已经存在的文件中添加对该指令位置的引用。

### 4. 需要用户同意

**未经用户明确许可，严禁修改`~/self-discipline/`目录之外的文件。**

在建议修改`AGENTS.md`、`HEARTBEAT.md`或其他文件时，必须遵循以下规则：

| 操作 | 要求 |
|--------|-------------|
| 创建新文件 | 先征求用户许可 |
| 修改`AGENTS.md` | 显示具体修改内容并等待用户批准 |
| 添加到`HEARTBEAT.md` | 显示修改内容并等待用户批准 |
| 创建验证器脚本 | 显示脚本内容并等待用户批准 |
| 修改任何现有文件 | 先备份文件并获取用户确认 |

**对外部文件进行修改的流程：**
1. 解释修改的必要性。
2. 显示具体要添加或修改的内容。
3. 等待用户的明确同意。
4. 确认同意后才能进行修改。

### 5. 为严重问题生成自动化验证器

对于严重级别为🔴的问题，需要生成自动化验证器：

（具体验证器实现内容请参见````bash
# Example: ~/self-discipline/validators/pre-send/no-secrets.sh
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: none
# External endpoints called: none
# Local files read: message content (stdin)
# Local files written: none

# Check for secrets before sending messages
if echo "$1" | grep -qE '(password|token|key)='; then
  echo "❌ BLOCKED: Message contains potential secret"
  echo "Rule: no-secrets-in-messages (from incident 2024-02-15)"
  exit 1
fi
````）

**验证器的要求：**
- 验证成功时返回0，验证失败时返回1。
- 必须包含规则的来源（即事件编号）。
- 仅用于检查，不得修改任何数据。

### 6. 跟踪执行情况

在`~/self-discipline/memory.md`目录中记录以下数据：
- 当前正在执行的规则。
- 按严重程度分类的事件记录。
- 验证器触发频率。
- 最近一次违规发生至今的天数。

### 升级流程

如果同一规则被违反两次：
1. 第一次违规：进行全面分析并采取修复措施。
2. 第二次违规：将问题提升为严重级别（CRITICAL）并强制执行验证器。
3. 第三次违规：停止当前操作并请求用户介入。

## 严重性评估标准

详细评估标准请参见`severity.md`。

### 快速评估方法

| 问题 | 如果是，则提升严重等级 |
|----------|----------|
- 用户是否明显表现出愤怒？ | +1 |
- 这是否可能导致数据丢失？ | 自动判定为严重问题（CRITICAL） |
- 这是否可能导致安全漏洞？ | 自动判定为严重问题（CRITICAL） |
- 这是否会影响生产环境？ | 自动判定为严重问题（CRITICAL） |
- 这种情况以前发生过吗？ | +1 |
- 用户是否使用了“绝对不能”或“总是”这样的表述？ | +1 |

## 流程验证流程

完整流程请参见`flow-verification.md`。

### 为什么指令会被忽略

| 常见原因 | 发生频率 | 解决方案 |
|-------|-----------|----------|
- 指令写在文件中但不在代理程序的加载路径范围内 | 60% | 移动指令位置或添加引用 |
- 指令被隐藏在长文件中，用户看不到 | 20% | 将指令移到文件顶部或单独的文件中 |
- 指令与其他指令冲突 | 10% | 明确解决冲突 |
- 用户的注意力窗口超出了指令的有效显示范围 | 5% | 缩短指令显示时间或提高指令的优先级 |
- 用户确实忘记了指令的存在 | 5% | 为相关指令添加验证器 |

### 验证步骤

1. 确定代理程序的加载路径中包含的所有文件（包括系统提示、`AGENTS.md`等）。
2. 检查指令是否位于这些路径范围内。
3. 如果不在路径范围内：确定在哪里添加引用。
4. 如果在路径范围内但被隐藏：将指令移到更显眼的位置。
5. 如果指令与其他指令冲突：明确优先级并解决冲突。

## 验证器模式

详细验证器实现方式请参见`validators.md`。

### 验证器类型

| 验证器类型 | 执行时机 | 适用场景 |
|------|----------|----------|
| `pre-commit` | 在提交代码之前 | 确保没有敏感信息或未完成的工作 |
| `pre-send` | 在发送消息之前 | 确保消息格式正确 |
| `pre-action` | 在执行特定操作之前 | 在删除操作前进行确认 |
| `periodic` | 在系统心跳检查时 | 定期验证规则的执行情况 |

### 验证器模板

（验证器模板内容请参见````bash
#!/usr/bin/env bash
set -euo pipefail

# SECURITY MANIFEST:
# Environment variables accessed: [list]
# External endpoints called: [list or "none"]
# Local files read: [list]
# Local files written: [list or "none"]

# Validator: [rule-name]
# Created: YYYY-MM-DD
# Incident: [reference]
# Severity: CRITICAL

# [description of what this validates]

[validation logic]

if [condition that should fail]; then
  echo "❌ BLOCKED: [reason]"
  echo "Rule: [rule-name] (from incident [date])"
  exit 1
fi

exit 0
````）

## 常见问题及解决方法

| 问题 | 后果 | 解决方案 |
|------|-------------|----------|
- 仅在`memory.md`中编写规则 | 未来的代理程序看不到这些规则 | 将规则添加到`rules.md`文件中（确保始终会被加载） |
- 仅凭“我会记住”就忽略指令 | 同样的错误会在多次会话中重复发生 | 必须始终验证指令的可达性 |
- 验证器修改了数据 | 可能导致意外副作用 | 验证器仅用于检查，不得修改数据 |
- 修改文件前未进行备份 | 如果出错无法恢复数据 | 修改前必须先备份文件 |
- 跳过严重性评估 | 未能对严重问题做出及时响应 | 必须首先评估问题的严重性 |
- 将规则放在错误的文件中 | 规则可能无法被正确加载 | 仅确保`rules.md`文件会被加载 |

## 命令

| 命令 | 功能 |
|---------|--------|
| `/discipline` | 启动针对最近一次违规的自我纪律流程 |
| `/discipline status` | 显示当前正在执行的规则和统计信息 |
| `/discipline verify [rule]` | 对指定规则进行流程验证 |
| `/discipline test [validator]` | 预先运行验证器 |
| `/discipline history` | 显示违规事件记录 |

## 安全性与隐私保护

- 所有规则、事件和验证器的数据都存储在`~/self-discipline/`目录内，不会发送到外部服务。
- 不会发送任何数据到外部服务。
- 不会进行任何网络请求。
- 不会访问用户的凭证或敏感信息。
- 未经用户明确许可，不会修改任何文件。
- 未经用户批准，不会运行验证器。
- 未经允许，不会访问`~/self-discipline/`目录之外的文件。

**对`~/self-discipline/`目录之外的文件进行修改时：**
- 仅在需要时（例如为了在`AGENTS.md`中引用规则）才建议进行修改。
- 修改前必须先向用户展示修改内容。
- 修改前必须获得用户的明确批准。
- 修改前必须先创建备份。

## 相关技能

如果用户同意，可以使用以下命令进行安装：
- `reflection` — 结构化的自我评估工具
- `memory` — 持久化的数据存储机制
- `decide` — 决策支持工具
- `escalate` — 判断何时需要寻求帮助或采取行动
- `learning` — 自适应学习系统

## 反馈方式

- 如果觉得这项技能有用，请给`self-discipline`打星评价。
- 为了保持更新，请使用`clawhub sync`命令。
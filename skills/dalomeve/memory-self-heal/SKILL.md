---
name: memory-self-heal
version: 1.1.0
description: 一种通用的自修复循环机制，能够从过去的失败中学习，安全地重试操作，并记录下可重复使用的修复方案。
metadata:
  openclaw:
    emoji: "[HEAL]"
    category: resilience
---
# 内存自修复技能

当代理程序频繁出现故障、卡顿，或者不断向用户询问可以从先前数据中推断出的操作步骤时，可以使用此技能。

## 目标

1. 在无需用户微观管理的情况下恢复程序的执行。
2. 重用内存、日志或任务中保存的先前修复方案。
3. 仅在真正遇到无法继续执行的情况时，才请求用户提供必要的输入信息。
4. 为未来的运行保留可复用的数据记录。

## 触发条件

当出现以下任何一种情况时，触发该技能：
- 同一或类似的错误在同一任务中发生2次以上。
- 工具调用失败，原因可能是参数不匹配、配置缺失、认证失败或上下文超出限制。
- 代理程序声称任务已完成，但实际上没有生成可验证的结果。
- 任务进度停滞（连续两个周期内没有新的进度更新）。

## 输入参数

- 当前任务的目标。
- 最新的错误信息或输出结果。
- 可用的数据存储位置（内存、任务列表、日志文件）。

## 数据扫描顺序

按以下顺序扫描数据；如果某个路径不存在，则忽略它：
1. `memory/`（或对应的工作区内存路径）。
2. `tasks/` 或任务队列文件。
3. 运行时日志/通道日志。
4. 技能文档（`skills/*/SKILL.md`），以查找可用的备用解决方案。
5. 核心文档（`TOOLS.md`、`CAPABILITIES.md`、`AGENTS.md`）。

**Shell 示例**（使用当前激活的Shell环境）：

```powershell
# PowerShell
Get-ChildItem -Recurse memory, tasks -ErrorAction SilentlyContinue |
  Select-String -Pattern "error|blocked|retry|fallback|auth|token|proxy|timeout|context" -Context 2
```

```bash
# POSIX shell
rg -n "error|blocked|retry|fallback|auth|token|proxy|timeout|context" memory tasks 2>/dev/null
```

## 故障分类

首先对故障类型进行分类，然后再采取相应的处理措施：
- `syntax_or_args`：命令语法或参数不匹配。
- `auth_or_config`：缺少或无效的密钥/令牌/环境配置。
- `network_or_reachability`：网络连接超时、DNS问题或地区访问限制。
- `ui_login_wall`：需要手动登录或连接。
- `resource_limit`：上下文窗口限制、速率限制或内存压力。
- `false_done`：没有生成实际结果，但系统仍报告任务已完成。
- `unknown`：无法确定故障类型。

## 恢复策略（三级处理机制）

### 第一次尝试：直接修复
- 从内存中查找适用于当前故障类型的解决方案。
- 重新执行最基本的验证操作。
- 记录修复结果。

### 第二次尝试：安全回退方案
- 更换为稳定性更高的工具或路径。
- 缩小操作范围（使用更少的输入参数、更简洁的查询条件、针对单一目标）。
- 重新执行验证操作。

### 第三次尝试：受控升级
- 标记当前任务为“受阻状态”，并仅请求用户提供下一步需要执行的操作（一个命令或一个UI操作）。
- 在收到新的输入信息之前，不再重复尝试其他操作。

## 安全规则

- 未经用户确认，切勿自动执行可能破坏系统的数据操作。
- 严禁将敏感信息（如密钥/令牌）存储在内存文件中。
- 每个任务中，针对同一故障类型最多允许尝试3次修复。

## 完成条件

只有在满足以下所有条件时，才能确认任务完成：
- 至少存在一个可读的结果文件或链接。
- 原始任务目标已通过结果文件得到明确验证。
- 当前任务的所有障碍都已解决。

**所需输出内容**：

```markdown
DONE_CHECKLIST
- Objective met: yes/no
- Artifact: <path or URL or command output ref>
- Validation: <what was checked>
- Remaining blocker: <none or exact unblock input>
```

## 内存数据更新模板

每次完成自修复操作后，需要在内存中添加一条简洁的记录：

```markdown
## Self-heal: <date-time> <short task>
- Signature: <normalized error signature>
- Class: <classification>
- Attempt1: <action> -> <result>
- Attempt2: <action> -> <result>
- Final: <success | blocked>
- Artifact/Evidence: <path|url|log ref>
- Reusable rule: <one-line rule>
```

## 常见故障解决方案（示例）

- 在Windows系统中，优先使用原生的PowerShell命令。
- 如果出现令牌不匹配或认证失败的问题，需验证配置来源和令牌的有效性。
- 对于WebSocket连接问题或超时情况，需检查网络连接是否正常以及代理设置是否正确。
- 如果上下文数据超出限制，可将任务拆分为更小的部分并减少数据传输量。
- 如果系统错误地报告任务已完成，必须先验证实际生成的结果文件。

## 集成说明

- 该技能可与自主执行任务或任务跟踪相关的技能配合使用，但不依赖于这些技能。
- 如果项目使用了自定义的内存存储路径，需动态调整数据扫描的起始位置。
- 保持记录条目的简洁性，以避免内存占用过多。
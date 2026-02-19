---
name: context-clean-up
slug: context-clean-up
version: 1.0.4
license: MIT
description: >
  **使用场景：** 当您怀疑 OpenClaw 的响应速度变慢（回复时间过长）、处理成本增加，或者转录结果中存在大量重复内容时，可以使用此方法。此时，您需要一份排名显示问题严重程度的列表，以及一个可逆的清理方案。  
  **不适用场景：** 当您希望助手自动执行修复操作，或者您的问题与 OpenClaw 的功能无关（需要其他类型的故障排除服务时）。  
  **输出内容：**  
  - 审计报告总结  
  - 3 至 8 个具体的修复步骤  
  - 回滚说明（系统不会自动进行任何更改）
disable-model-invocation: true
allowed-tools:
  - read
  - exec
  - sessions_list
  - sessions_history
  - session_status
metadata: { "openclaw": { "emoji": "🧹", "requires": { "bins": ["python3"] } } }
---
# 上下文清理（仅限审计使用）

本技能是一个**运行手册**，用于识别导致OpenClaw提示界面内容冗余的原因，并制定一个**安全、可逆的优化方案**。

**重要提示：** 本技能仅限**审计用途**，不会执行以下操作：
- 删除文件
- 修剪会话记录
- 修改配置文件
- 更新定时任务（cron jobs）

如果您要求进行任何更改，系统会提供详细的修改方案及回滚计划，并等待您的明确批准。

## 快速启动

执行命令 `/context-clean-up`，系统将执行审计并生成可执行的优化方案（不会对现有内容进行任何修改）。

## 常见导致内容冗余的原因

以下是常见的、影响较大的原因（按出现频率降序排列）：

1. **工具运行结果**：
   - 大量的执行结果（`exec`命令的输出）被直接粘贴到聊天界面中
   - 大型的读取结果（日志文件、JSON数据、锁文件）
   - 从网络获取的长篇内容

2. **自动化脚本产生的冗余信息**：
   - 定时任务每次运行后都会输出“OK”等提示信息
   - 用于监控系统状态的日志信息（非纯粹的警报信息）

3. **自启动脚本（bootstrap scripts）产生的冗余文件**：
   - `AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md` 文件内容过多
   - 在 `SKILL.md` 文件中直接嵌入了大量的运行手册内容，而非通过引用方式

4. **重复的总结信息**：
   - 未及时删除的重复性总结内容，反而积累了过多的历史信息

## 不应使用本技能的情况：
- “立即删除旧会话记录/修剪日志/应用修复措施”：本技能仅用于审计。
- “自动修改我的OpenClaw配置”：需要先获得您的许可。
- “调查应用程序代码中的具体错误”：请使用针对该仓库的调试工具。

## 工作流程（审计 → 制定优化方案）

### 第0步 — 确定审计范围

找到以下文件和目录：
- **工作区目录**：存放OpenClaw工作区及项目文件的目录
- **状态目录**：OpenClaw存储运行时状态信息的目录（包含会话记录、内存数据等）

状态目录的位置通常为：
- macOS/Linux系统：`~/.openclaw`
- Windows系统：`%USERPROFILE%\.openclaw`

但具体位置可能因安装环境而异。审计脚本支持通过 `--state-dir` 或 `OPENCLAW_STATE_DIR` 参数进行配置。

如果您需要快速检查系统状态，可以参考以下代码示例：

```text
# POSIX (macOS/Linux)
echo "WORKDIR=$PWD"; echo "HOME=$HOME"; ls -ld ~/.openclaw

# PowerShell (Windows)
Write-Host "WORKDIR=$PWD"; Write-Host "USERPROFILE=$env:USERPROFILE"; Get-Item "$env:USERPROFILE\.openclaw"
```

### 第1步 — 运行审计脚本

该脚本会生成简短的审计报告，也可以生成完整的JSON格式报告。

```text
# Run the audit script shipped with this skill.
# From the skill folder, run:
python3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json

# If your Python executable is not `python3` (common on Windows):
#   py -3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json

# Optional overrides:
#   --workspace   (defaults to current directory)
#   --state-dir   (defaults to ~/.openclaw or OPENCLAW_STATE_DIR)
python3 scripts/context_cleanup_audit.py --workspace . --state-dir <PATH_TO_OPENCLAW_STATE> --out context-cleanup-audit.json
```

**解读指南**：
- 如果 `toolResult`、`System:` 或 `Cron:` 目录下的内容过多，说明存在**自动化脚本产生的冗余信息**。
- 如果 `AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md` 文件过大，说明**自启动脚本产生的冗余文件过多**。

### 第2步 — 制定优化方案（优先处理风险较低的问题）

制定一个简单的优化方案，内容包括：
- 造成最大影响的冗余源（如庞大的执行结果）
- 重复出现且影响较大的自动化脚本（如定时任务）
- 可快速实施且不会造成系统故障的优化措施

可使用的优化方法如下：

#### 方法A — 使自动化脚本在正常情况下不产生任何输出
目标：确保维护脚本在正常运行时仅输出 `NO_REPLY`。

**实现方式**：更新脚本，使其在完成操作后强制输出 `NO_REPLY`。

#### 方法B — 保留警报信息，同时减少冗余信息的显示
如果您需要接收警报信息，但希望会话界面保持简洁：
- 将警报信息通过外部渠道（如Telegram、Slack等）发送
- 然后仍然在控制台输出 `NO_REPLY`。

**参考文档**：`references/out-of-band-delivery.md`

#### 方法C — 减少自启动脚本产生的冗余文件
- 仅保留对系统重启至关重要的规则信息在 `MEMORY.md` 文件中
- 将冗长的说明文件移至 `references/*.md` 或 `memory/*.md` 文件中

### 第3步 — 验证优化效果

应用优化措施后，请确认：
- 定时任务和监控脚本在下次运行时是否不再产生冗余信息
- 检查上下文数据量的增长趋势（应趋于稳定）

## 样本报告模板（优化后的报告格式）

在提交审计结果时，请使用此报告结构（即使不生成JSON格式的报告）：

```markdown
# Context Clean Up — Audit Report (No Changes)

## Executive Summary
- Symptoms observed:
- Primary bloat drivers:
- Recommended first action:

## Top Offenders
1) <offender> — <why it matters> — <quick fix>
2) <offender> — <why it matters> — <quick fix>

## Automation Noise (Cron/Heartbeat)
- Findings:
- Proposed changes (audit-only):
- Risk/rollback notes:

## Bootstrap Size
- Files contributing most:
- Recommendation:

## Plan (3–8 steps)
1) ...
2) ...

## Rollback Plan
- How to revert each step:

## Verification
- What to check after changes:
```

## 参考文档：
- `references/out-of-band-delivery.md`
- `references/cron-noise-checklist.md`
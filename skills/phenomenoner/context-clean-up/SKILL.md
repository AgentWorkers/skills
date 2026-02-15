---
name: context-clean-up
slug: context-clean-up
version: 1.0.2
license: MIT
description: 审计 OpenClaw 代码中的冗余部分，并制定一个可执行的清理计划（不进行自动修改）。
disable-model-invocation: true
allowed-tools:
  - read
  - exec
  - sessions_list
  - sessions_history
  - session_status
metadata: { "openclaw": { "emoji": "🧹", "requires": { "bins": ["python3"] } } }
---

# 上下文清理（仅用于审计）

此技能是一份**运行手册**，用于快速识别导致 OpenClaw 提示界面内容膨胀的原因，并制定一个**安全、可逆的修复计划**。

**重要提示：** 此版本仅用于审计（不会自动应用任何更改）。如果您希望我执行修复操作，我会提出具体的修复方案及回滚计划，并等待您的明确批准。

## 快速入门

- 使用命令 `/context-clean-up` 进行审计并获取可执行的修复计划（不会自动进行任何更改）。

## 工作流程（审计 → 制定修复计划）

### 第 0 步 — 确定审计范围

查找以下文件：
- 工作区目录（您的项目文件，通常位于 OpenClaw 工作区）
- 状态目录（OpenClaw 的运行时状态信息，通常位于 `~/.openclaw`）

如果不确定如何查找，请参考以下代码示例：

```bash
bash -lc 'echo "WORKDIR=$PWD"; echo "HOME=$HOME"; ls -ld ~/.openclaw'
```

### 第 1 步 — 运行审计脚本

该脚本会生成一个简短的总结报告，也可以生成完整的 JSON 报告。

```bash
bash -lc 'cd "${WORKDIR:-.}" && python3 {baseDir}/scripts/context_cleanup_audit.py --out memory/context-cleanup-audit.json'
```

**解读指南：**
- 如果 `toolResult` 条目过多（涉及执行、读取或网络请求操作），则可能是**转录内容过多导致的膨胀**。
- 如果出现大量 `System:` 或 `Cron:` 类的记录，可能是**自动化脚本导致的膨胀**。
- 如果 `AGENT`、`MEMORY`、`SOUL` 或 `USER` 目录中的文件过大，可能是**注入的规则导致的膨胀**。

### 第 2 步 — 制定修复计划（优先处理风险较低的问题）

制定一个包含以下内容的修复计划：
- 造成最大问题的关键因素（尤其是那些导致转录内容过长的条目）
- 重复出现的、产生大量日志的自动化任务（如定时任务/心跳检测）
- 可以快速修复的问题（并且修复后不会对系统造成永久性影响）

可以使用以下几种常见的修复方法：

#### 方法 A — 使无操作的自动化脚本真正静默
**目标：** 维护脚本在正常情况下应仅输出 `NO_REPLY`。

**实现方式：** 更新提示信息，确保脚本的最后一行始终输出 `NO_REPLY`。

#### 方法 B — 保留通知功能，同时减少转录内容的生成
**如果仍需要发送通知，但希望保持交互式会话的简洁性：**
- 通过外部渠道（如 Telegram、Slack 等）发送通知，
- 然后仍然输出 `NO_REPLY`。

**详情请参阅：`references/out-of-band-delivery.md`**

#### 方法 C — 减少注入的引导文件的大小
- 仅将重启时必需的规则保存在 `MEMORY.md` 文件中，
- 将冗长的注释或配置文件移至 `references/*.md` 或 `memory/*.md` 文件中。

### 第 3 步 — 验证修复效果

在应用任何更改后，请确认：
- 定时任务或心跳检测脚本在下次运行时是否不再产生多余的日志。
- 监控上下文内容的增长速度（应趋于稳定）。

## 参考资料
- `references/out-of-band-delivery.md`
- `references/cron-noise-checklist.md`
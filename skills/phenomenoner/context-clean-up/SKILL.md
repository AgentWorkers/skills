---
name: context-clean-up
slug: context-clean-up
version: 1.0.5
license: MIT
description: >
  **使用场景：** 当提示信息的数量过多（导致回复速度变慢、成本上升或转录结果质量下降）时，且您需要一个按问题严重程度排序的故障列表以及相应的解决方案时。  
  **不适用场景：** 当您需要自动删除某些内容或进行无人值守的配置修改时。  
  **输出内容：** 仅提供审计报告（包括问题最严重的部分、3到8个风险较低的修复方案以及回滚操作的相关说明）。所有更改都不会被自动应用。
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

此技能是一个**运行手册**，用于识别导致提示上下文膨胀的原因，并制定一个**安全、可逆的修复计划**。

**重要提示：** 此技能仅限**审计使用。
- 它不会删除数据、修剪会话、修改配置或更改定时任务（cron jobs）。
- 如果您请求进行修改，它将提出一个具体的修复方案及回滚计划，并等待明确的批准。

## 快速启动

- 输入 `/context-clean-up` 命令，系统将执行审计并生成可执行的修复计划（不会对现有内容进行任何更改）。

如果您能够运行捆绑的审计脚本，还可以生成一个 JSON 报告：

```text
python3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json
```

如果您的 Python 可执行文件不是 `python3`（在 Windows 上较为常见）：

```text
py -3 scripts/context_cleanup_audit.py --out context-cleanup-audit.json
```

## 关于 `NO_REPLY` 的说明

某些 OpenClaw 配置使用 `NO_REPLY` 作为标志，表示“操作成功但无需人工通知”。

- 如果您的运行环境不支持该标志，请将其理解为：操作成功时不输出任何信息。

## 常见的问题来源（通常会导致上下文膨胀）

以下是导致上下文膨胀的常见原因（按发生频率降序排列）：

1) 工具运行结果的输出：
   - 大量的 `exec` 命令输出被直接粘贴到聊天框中
   - 大量的 `read` 操作输出（如日志、JSON 文件、锁文件）

2) 自动化脚本产生的冗余信息：
   - 定时任务每次运行时都会输出 “OK” 状态

3) 自动化脚本中的冗余代码或日志：
   - 不仅用于报警，还包含其他不必要的信息

4) 过大的配置文件：
   - `AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md` 文件内容过多

5) 重复的摘要信息：
   - 未及时清理的摘要内容，不断累积历史数据

## 不应使用此技能的情况

- “立即删除旧会话/修剪日志/应用修复措施”：此技能仅用于审计。
- “自动修改我的 OpenClaw 配置”：需要先获得许可。
- “调查应用程序代码中的特定错误”：应使用针对特定仓库的调试工具。

## 工作流程（审计 → 制定修复计划）

### 第 0 步 - 确定审计范围

您需要知道以下信息：
- 工作区目录：存放您的工作区/项目文件的路径
- 会话/内存存储目录：运行时系统存储会话和内存数据的目录（可命名为 `<OPENCLAW_STATE_DIR>`）

常见默认路径（可能因安装环境而异）：
- macOS/Linux：`~/.openclaw`
- Windows：`%USERPROFILE%\.openclaw`

审计脚本支持通过 `--state-dir` 参数或 `OPENCLAW_STATE_DIR` 环境变量来指定目录。

### 第 1 步 - 运行审计脚本

该脚本会输出简短的摘要信息，并可以生成 JSON 报告。

```text
python3 scripts/context_cleanup_audit.py --workspace . --state-dir <OPENCLAW_STATE_DIR> --out context-cleanup-audit.json
```

**解读说明：**
- 大量的工具运行输出（如 `exec`、`read`、`web_fetch` 操作）：表明存在冗余的自动化脚本输出
- 大量的 `System:` 或 `Cron:` 类型的日志：表明自动化脚本产生了过多信息
- 过大的配置文件（如 `AGENTS.md`、`MEMORY.md`、`SOUL.md`、`USER.md`）：表明配置文件内容过多

### 第 2 步 - 制定修复计划（优先处理风险较低的问题）

制定一个简单的修复计划，内容包括：
- 造成最大影响的问题（如冗余的自动化脚本输出）
- 重复出现的问题（如定时任务或心跳检测脚本）
- 可快速解决的简单问题

**常见的修复方法：**

#### 方法 A - 使无操作的自动化脚本真正“静默”运行

目标：维护脚本在正常情况下应仅输出 “NO_REPLY”（或没有任何输出），除非出现异常情况。

#### 方法 B - 保留通知功能，同时减少冗余信息

如果您需要接收警报信息，但希望减少自动化脚本产生的输出：
- 将警报信息通过外部渠道（如 Telegram、Slack 等）发送
- 同时确保自动化脚本的输出保持静默

详见：`references/out-of-band-delivery.md`

#### 方法 C - 减少不必要的配置文件大小

- 仅将真正影响系统重启的规则保存在 `MEMORY.md` 文件中
- 将冗余的配置信息移动到 `references/*.md` 或 `memory/*.md` 文件中

### 第 3 步 - 验证修复效果

应用修复措施后，请确认：
- 定时任务或心跳检测脚本在成功执行时不再产生任何输出
- 监控上下文数据的增长情况（应逐渐趋于稳定）

## 参考资料

- `references/out-of-band-delivery.md`
- `references/cron-noise-checklist.md`
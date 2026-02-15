---
name: context-sentinel
description: "监控会话上下文，并根据级联协议自动管理模型切换。可作为心跳检测（heartbeat）或定时任务（cron job）的一部分来维护会话的稳定性并优化令牌（token）的使用。"
version: 1.0.0
---

# Context Sentinel

该技能提供了一个脚本，用于自动化执行“Cascading Model Protocol”（级联模型协议），确保代理在会话规模增长时能够从高成本模型优雅地切换到高上下文模型。

## 协议概述

1. **Opus 4.6：** 在上下文使用量达到80%之前使用该模型，之后切换到Opus 4.5。
2. **Opus 4.5：** 在上下文使用量达到80%之前使用该模型，之后切换到Gemini 2.5 Pro。
3. **Gemini Pro：** 在上下文使用量达到80%之前使用该模型，之后触发交接流程。

该技能实现了`MEMORY.md`中定义的逻辑。

## 使用方法

该技能设计为定期运行，可以通过`cron`作业执行，或者作为代理主脚本`HEARTBEAT.md`中检查流程的一部分来使用。

### 工作流程

1. **执行脚本：**
   运行`check_context.ps1`脚本以获取当前会话状态并确定所需的操作。

    ```powershell
    powershell -File scripts/check_context.ps1
    ```

2. **解析输出：**
   脚本将返回以下三种字符串命令之一：
   *   `SWITCH_TO:<model_id>`
   *   `HANDOFF_now`
   *   `STATUS_OK`

3. **采取行动：**
   根据输出结果执行相应的代理命令：
   *   如果返回`SWITCH_TO:<model_id>`，则使用新的模型ID运行`session_status`脚本：
        ```
        session_status model=<model_id>
        ```

   *   如果返回`HANDOFF_now`，则通过写入交接文件来触发交接流程。这通常是通过运行特定的预定义提示或脚本来完成的。
   *   如果返回`STATUS_OK`，则无需采取任何行动。

### 在`HEARTBEAT.md`中的示例用法

您可以将`HEARTBEAT.md`中的手动检查替换为调用此技能的脚本。

**旧的`HEARTBEAT.md`：**
```markdown
## Cascading Model Protocol (Check Every Heartbeat)
1.  **Check Status:** Get current model and context %.
2.  **Opus 4.6:** If model is `Opus 4.6` and context > 80% -> Switch to `Opus 4.5`.
...
```

**使用此技能的新`HEARTBEAT.md`：**
```markdown
## Context Sentinel (Check Every Heartbeat)
1. Run `powershell -File skills/context-sentinel/scripts/check_context.ps1`.
2. Evaluate the output and take action (`SWITCH_TO`, `HANDOFF_NOW`, or `STATUS_OK`).
```

这样可以使逻辑得到复用，并保持`HEARTBEAT.md`文件的简洁性，使其专注于执行任务。
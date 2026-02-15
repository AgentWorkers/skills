---
name: codex-orchestrator
description: 监控、控制并协调后台的 Codex 会话。利用这一技能来跟踪进度、处理中断情况，并确保长时间运行的编码任务能够顺利完成。
---

# Codex Orchestrator

本技能提供了一种用于监控在后台进程中运行的Codex编码代理的工作流程。

## 工作流程

### 1. 启动（Launch）
始终在后台PTY（Python Terminal Window）会话中启动Codex，以保持交互性，同时不会阻塞主代理程序的运行。

```bash
bash pty:true workdir:<target_dir> background:true command:"codex exec --full-auto '<PROMPT>'"
```
*   存储返回的`sessionId`。
*   如果`sessionId`丢失，通过`process action:list`来查找它。

### 2. 监控（Watch）
定期检查进度（例如，通过cron任务或手动检查）。

```bash
# Get last 2KB of logs to see current status
process action:log sessionId:<id> limit:2000
```

**正常运行的迹象：**
*   有旋转动画或进度条在更新。
* 显示“Working...”、“Thinking...”、“Running...”等状态信息。
* 显示“Edit ...”等文件编辑提示。

**运行受阻的迹象：**
* 出现交互式提示（例如“Select directory”、“Approve change [y/n]”）。
* 超过5分钟没有日志输出（可能是程序挂起或正在等待用户输入）。

### 3. 干预（Control）
如果Codex在某个提示界面卡住了：

```bash
# Send 'y' and Enter
process action:submit sessionId:<id> data:"y"

# Send just Enter (default choice)
process action:submit sessionId:<id> data:""
```

如果Codex陷入无限循环或出现异常行为：

```bash
# Kill the session
process action:kill sessionId:<id>
```

### 4. 报告（Notify）
当达到重要里程碑或任务完成时：
1. 总结已完成的工作（修改的文件、通过的测试等）。
2. 通知用户。

## 标准操作程序（SOPs）

### “代理程序卡住”时的处理方法
1. **诊断**：运行`process action:log sessionId:<id> limit:500`。
2. **分析**：程序是在提问吗？还是在下载数据？
3. **处理方式**：
    * 如果在提问：通过`submit`提供答案。
    * 如果在下载数据（且速度较慢）：等待。
    * 如果程序沉默超过10分钟：发送一个“提示”（例如`submit data:"\n"`）以刷新提示界面），或者直接终止/恢复程序的运行。

### “程序恢复”时的处理方法
如果会话意外终止或被强制关闭：
1. 在新的后台进程中运行`codex resume --last`或`codex resume <session_id>`。
2. 确认程序是否能够恢复之前的工作状态。

## 日志与输出文件
* Codex的日志在PTY缓冲区中是临时存储的。
* 如需永久保存日志，可以指示Codex将日志写入文件：`codex exec "task..." > codex.log 2>&1`（注意：这种方式可能会导致输出延迟）。
* 更好的方法是使用`process action:log`定期将日志内容保存到文件中。
---
name: claw-guard
description: OpenClaw网关重启及子代理任务进程ID（PID）的系统级监控工具。该工具会监控已注册的进程ID，并可选择性地检查日志文件或目录的更新情况。在网关重启失败时，会自动恢复配置设置。需要用户手动进行注册——不会自动发现相关进程或服务。适用于执行长时间运行的后台任务或在网关重启前使用。
---
# ClawGuard — 任务与网关监控工具

这是一个轻量级的服务，用于监控已注册的事件：

1. **子代理任务进程ID（PID）**：如果进程ID异常终止，会立即通知并删除相关记录；如果日志目录中的日志文件过期，也会发出警报并删除相关记录。
2. **网关重启**：如果重启失败，会依次使用最新的配置备份进行恢复，然后尝试重新启动网关，并通知相关方。

**ClawGuard仅监控已明确注册的事件**，不会自动发现新的事件。

## 安装

```bash
cd <skill-dir>
bash scripts/install.sh
```

安装方式如下：
- **守护进程**：在Linux系统中使用systemd用户服务，在macOS系统中使用launchd代理，设置为`Restart=always`，确保系统启动时自动启动。
- **命令行工具（CLI）**：位于`~/.local/bin/`目录下的`claw-guard`命令。
- **数据存储**：数据文件存储在`~/.openclaw/workspace/tools/claw-guard/`目录中。

## 推荐的OpenClaw集成方式

### 1. 自动注册网关重启事件

在网关服务中添加`ExecStartPre`脚本，以确保每次网关重启（无论是手动重启、系统崩溃还是通过`Restart=always`设置启动）都能被自动监控：

```ini
# ~/.config/systemd/user/openclaw-gateway.service
[Service]
ExecStartPre=/home/<user>/.local/bin/claw-guard register-restart
ExecStart=...
```

完成后，重新加载系统服务配置：`systemctl --user daemon-reload`

此时，每次网关重启时，ClawGuard都会自动执行以下操作：
- 创建当前配置的备份（最多保存5份备份）。
- 监控网关的启动状态。
- 如果网关启动失败，会使用最新的配置备份进行恢复，并通过默认通道通知相关人员。

**无需手动执行`claw-guard register-restart`命令——systemd会自动处理。**

### 2. 在`AGENTS.md`文件中添加任务执行规则

在`AGENTS.md`文件中添加以下规则，以确保代理会自动注册自己的任务执行情况：

```markdown
## Task Execution Rules (MANDATORY)

### Sub-agent requirement
- **Any exec/tool call that might take >5s → sub-agent** (`sessions_spawn`).
  Main agent stays responsive.
- **Complex or unpredictable tasks → always sub-agent.** Even if they might
  be fast. If you can't guarantee it won't block, delegate it.
- **Only run in main agent** if certain it won't block I/O (quick file reads,
  short `grep`, `git status`, `claw-guard status`, etc.)

### ClawGuard registration (MANDATORY for all sub-agents)
Every sub-agent and background process **must** be registered:
```bash
claw-guard register --id "<描述性ID>" --pid <PID> \
  --target "<任务请求的目标通道>" \
  --log "/path/to/logfile" --timeout 180 \
  --command "<任务的具体命令>"
```
- `--target`: same channel/room where the user asked for the task
- `--log` and `--timeout`: optional but recommended for long tasks
- If PID dies → claw-guard notifies the target channel and removes the entry
- If log goes stale → claw-guard notifies and removes

### Gateway restarts
- **Never restart the gateway while tasks are running** — it kills all sub-agents
- Gateway service has `ExecStartPre=claw-guard register-restart` — automatic
- No manual registration needed for restarts
```

### 全部工作流程

**子代理任务流程：**
1. 用户请求一个长时间运行的任务。
2. 代理创建子代理并获取其PID。
3. 代理执行`claw-guard register`命令，将任务信息注册到ClawGuard。
4. 如果子代理进程异常终止，ClawGuard会通知目标通道；代理会向用户确认任务结果。
5. 如果日志文件过期，ClawGuard会发出警报，代理会进一步调查情况。

**网关重启流程：**
1. 网关重启（无论是手动重启、系统崩溃还是自动重启）。
2. `ExecStartPre`脚本会自动执行`claw-guard register-restart`命令，备份配置信息。
3. 如果网关成功启动，ClawGuard会记录“网关重启成功”的日志，并清除监控记录。
4. 如果网关启动失败，ClawGuard会尝试使用备份配置进行恢复，并通过默认通道通知相关人员。

## 命令行工具参考

### 注册任务

```bash
claw-guard register --id "benchmark-q8" --pid 12345 \
  --target "room:!abc:server" \
  --log "/path/to/task.log" --timeout 180 \
  --command "python3 benchmark.py"

# Or watch a directory for new file creation:
claw-guard register --id "export-gguf" --pid 12345 \
  --target "room:!abc:server" \
  --watch-dir "/path/to/output/" --timeout 300 \
  --command "export_gguf.py"
```

| 参数 | 是否必填 | 说明 |
|------|----------|-------------|
| `--id` | 是 | 任务的唯一标识符 |
| `--pid` | 是 | 需要监控的进程ID |
| `--target` | 是 | 通知目标通道（格式见下文） |
| `--log` | 否 | 日志文件路径（仅检查文件修改时间） |
| `--watch-dir` | 否 | 日志目录路径（检查目录中文件的最新修改时间） |
| `--timeout` | 否 | 日志文件过期的时间阈值（默认：180秒） |
| `--command` | 否 | 任务执行的命令描述 |

### 注册网关重启事件

```bash
claw-guard register-restart [--target "room:!abc:server"]
```

无需指定`--target`参数——系统会自动将重启事件发送到OpenClaw的默认通知通道。如需指定目标通道，可以使用`--target`参数。

### 管理ClawGuard

## 行为规则

### 监控周期（每15秒一次）
1. **网关重启**：如果任务已注册但网关在30秒内仍未启动，会尝试重新启动并通知相关人员。
2. **进程ID检查**：如果进程ID异常终止，会通知目标通道并删除相关记录。
3. **日志文件更新检查**：如果日志文件超过过期时间，会通知目标通道并删除相关记录。

### 数据去重

通知完成后，相关记录会从注册表中删除。一旦删除，该任务将不再被监控。系统无需进行去重处理。

### 服务重启/系统重启时的行为
- 服务重启或系统重启时，所有已注册的任务都会被清除。
- 配置备份会保存在磁盘上（这是唯一需要保留的数据）。

这是经过设计的选择：系统重启后，所有被监控的进程都会终止，因此代理需要重新注册所有新任务。

## 通知目标通道
ClawGuard支持多种通知格式：
- `openclaw message send --target`：支持自定义通知格式。
- `room:!roomId:server`：用于Matrix平台。
- `telegram:chatid`：用于Telegram。
- `discord:#channel`：用于Discord平台。
**未指定`--target`参数的网关重启警报会自动发送到OpenClaw的默认通知通道。**

## 设计原则
- **基于注册的监控机制，而非自动发现**：仅监控已明确注册的任务。
- **一次通知后删除相关记录**：避免重复通知和状态异常。
- **数据存储在内存中**：服务重启时，注册表会被清空。
- **配置备份仅保存在磁盘上**：这是唯一需要在重启后保留的数据。
- **跨平台兼容**：支持Linux（systemd）和macOS（launchd）系统。
- **低资源占用**：仅占用约7MB内存，对CPU性能影响极小。
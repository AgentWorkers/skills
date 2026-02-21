---
name: subagent-overseer
description: 通过基于Pull机制的Bash守护进程来监控子代理的运行状态和进度。适用于需要跟踪子代理进度、检测其是否处于“停滞”状态以及自动报告状态的场景。该机制替代了传统的手动心跳检测方式，改为让子代理每3分钟读取一次状态文件以获取更新信息。整个监控过程完全不依赖任何AI技术，仅通过操作系统级别的进程检查及文件系统差异分析来实现。
---
# 子代理监控器（Sub-Agent Overseer）

这是一个轻量级的、基于Pull机制的守护进程，用于监控子代理的运行状态。它会每隔N秒生成一次状态报告文件。心跳检测器（Heartbeat Handler）会定期读取该文件，无需进行数据推送或发送其他额外信号。

## 架构

```
overseer.sh (bash, runs in background)
    ├── /proc/<pid>  → gateway alive? CPU? threads?
    ├── openclaw sessions list  → sub-agent count + ages
    ├── find -newer marker  → filesystem activity
    └── writes /tmp/overseer/status.json  (atomic mv)

heartbeat (agent, every 3min)
    └── reads /tmp/overseer/status.json → summarize or HEARTBEAT_OK
```

**核心原则：**监控器负责所有的数据收集工作；如果状态文件是最新的且运行正常，心跳检测器不会执行任何额外的工具调用。

## 快速入门

### 1. 在启动子代理时同时启动监控器

```bash
setsid scripts/overseer.sh \
  --workdir /path/to/repo \
  --interval 180 \
  --max-stale 4 \
  --voice \
  &>/dev/null &
```

### 2. 心跳检测器读取状态文件

```bash
cat /tmp/overseer/status.json
```

### 3. 解析状态信息

| 字段          | 含义                                      |
|---------------|-------------------------------------------|
| `subagents.count`    | 正在运行的子代理会话数量                      |
| `subagents.details[].stale` | 连续多个周期内文件系统未发生任何变化的子代理数量        |
| `subagents.details[].status` | 子代理的状态（`active` / `idle` / `warning` / `stuck`）       |
| `gateway.health.alive` | `openclaw-gateway` 是否正在运行？                |
| `filesystem.changes_since_last` | 自上次检查以来修改过的文件数量                |

### 4. 状态异常阈值（每180秒检查一次）

| 异常状态数量 | 检查间隔（秒） | 状态            | 应采取的措施                         |
|---------------|----------------|-----------------------------|
| 0-1           | 0-3分钟        | `active`/`idle`       | 正常                          |
| 2-3           | 6-9分钟        | `warning`        | 发出语音警报（如果启用了`--voice`选项）             |
| ≥4           | ≥12分钟        | `stuck`         | 需要检查或终止相关子代理                   |

## 心跳检测器协议

当`HEARTBEAT.md`脚本被触发时，它会执行以下操作：

1. **读取`/tmp/overseer/status.json`文件**；如果文件缺失或内容过时（超过10分钟），则重启监控器。
2. **如果连续两个周期内`subagents.count`为0**，则监控器自动退出，并返回`HEARTBEAT_OK`响应。
3. **如果所有子代理都处于`active`状态**，则返回简短的状态信息，并返回`HEARTBEAT_OK`。
4. **如果有子代理处于`stuck`状态**，则会报告具体的子代理名称，并考虑通过`subagents kill`命令终止该子代理。
5. **绝不缓存之前的心跳检测结果**；始终从状态文件中获取最新数据。

## 命令行参数

| 参数          | 默认值          | 描述                                      |
|---------------|----------------|-------------------------------------------|
| `--interval`     | 180            | 检查间隔（秒）                          |
| `--workdir`     | cwd            | 监控文件系统变化的目录                        |
| `--labels`     | (all)          | 用于过滤的标签列表（用逗号分隔）                   |
| `--max-stale`     | 4              | 被标记为“stuck”状态之前的最大周期数                 |
| `--voice`     | off            | 是否启用通过`jarvis`命令进行语音警报                   |

## 工作原理（不涉及AI技术）

1. **检查`gateway`的健康状态**：通过`/proc/<pid>/status`读取CPU、内存、线程数等信息（纯内核数据）。
2. **获取子代理列表**：每个周期调用一次`openclaw`的会话列表接口，并解析其输出结果。
3. **检测文件系统变化**：使用`find -newer`命令检测工作目录中的文件修改情况。
4. **状态文件更新**：状态信息以JSON格式原子性地写入临时文件，之后使用`mv`命令将其替换到目标位置；所有读取者都能看到最新的文件内容。
5. **自动退出**：如果连续两个周期内没有子代理运行，监控器会自动停止。
6. **防止重复运行**：使用`flock`命令确保同一时间只有一个监控器实例在运行。

## 成本估算

- 监控器本身：**0.00美元**（基于bash脚本及每个周期的一次CLI调用）
- 语音警报：**0.00美元**（通过`jarvis`命令触发本地TTS警报）
- 心跳检测：**0.00美元**（仅需要执行一次`cat`命令）
- 唯一的额外成本是心跳检测模块本身（qwen3本地版本为免费）。
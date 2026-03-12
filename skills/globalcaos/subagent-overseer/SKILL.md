---
name: subagent-overseer
version: 1.1.0
description: "你创建了4个子代理。其中1个在20分钟前失效了。你仍在等待。监督者会自动监控它们的状态，因此你无需亲自处理这些任务——完全依赖于操作系统级别的进程检查机制。没有轮询循环，也不会浪费任何系统资源（如心跳检测）。"
metadata:
  openclaw:
    emoji: "👁️"
    notes:
      security: "No network calls. Reads process status and filesystem diffs only. Pure bash daemon."
---
# 子代理监控器（Sub-Agent Overseer）

这是一个轻量级的、基于Pull机制的守护进程，用于监控子代理的运行状态。它会每隔N秒生成一次状态报告文件。心跳处理程序会定期读取该文件——无需发送数据到服务器，也不会产生额外的网络流量。

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

**核心原理：**监控器负责所有的数据收集工作；如果状态文件是最新的且运行正常，心跳处理程序不会执行任何额外的操作。

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

### 2. 心跳处理程序读取状态文件

```bash
cat /tmp/overseer/status.json
```

### 3. 解析状态信息

| 字段 | 含义 |
|---|---|
| `subagents.count` | 正在运行的子代理数量 |
| `subagents.details[].stale` | 连续多个周期内文件系统未发生变化的子代理数量 |
| `subagents.details[].status` | 子代理的状态（`active` / `idle` / `warning` / `stuck`） |
| `gateway.health.alive` | `openclaw-gateway` 是否正在运行？ |
| `filesystem.changes_since_last` | 自上次检查以来修改过的文件数量 |

### 状态判断阈值（每180秒检查一次）

| 状态 | 判断条件 | 处理方式 |
|---|---|---|
| `active`/`idle` | 没有变化 | 正常 |
| `warning` | 连续6-9分钟无文件系统变化 | 发出语音警报（如果启用了`--voice`选项） |
| `stuck` | 连续12分钟无变化 | 需要检查或终止该子代理 |

## 心跳处理程序协议

当`HEARTBEAT.md`脚本被触发时，会执行以下操作：
1. 读取`/tmp/overseer/status.json`文件；如果文件缺失或已过期（超过10分钟），则重启监控器。
2. 如果连续两个周期内`subagents.count`为0，监控器将自动退出，并返回`HEARTBEAT_OK`响应。
3. 如果所有子代理都处于`active`状态，返回简短的状态信息（一行文本），并返回`HEARTBEAT_OK`。
4. 如果有子代理处于`stuck`状态，会报告具体是哪些子代理处于该状态，并考虑通过`subagents kill`命令终止它们。
5. **绝不缓存之前的心跳响应**；始终从最新状态文件中读取数据。

## 命令行参数

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--interval` | 180 | 检查间隔（秒） |
| `--workdir` | cwd | 监控文件变化的目录 |
| `--labels` | （所有标签） | 用于过滤的标签列表（用逗号分隔） |
| `--max-stale` | 4 | 被标记为“stuck”状态之前的最大周期数 |
| `--voice` | off | 通过`jarvis`命令触发本地语音警报 |

## 工作原理（不含AI相关组件）

1. **检查网关状态**：通过`/proc/<pid>/status`读取CPU、内存、线程数等内核信息。
2. **获取子代理列表**：每个周期调用一次`openclaw`的会话列表接口，并解析输出结果。
3. **检测文件系统变化**：使用`find -newer`命令检测工作目录中的文件修改情况。
4. **状态文件生成**：状态信息以JSON格式生成，并原子性地写入临时文件，之后使用`mv`命令将其复制到最终位置；所有读取者看到的都是最新的状态文件。
5. **自动退出**：如果连续两个周期内没有子代理运行，监控器将自动停止。
6. **防重复**：使用`flock`命令确保同一时间只有一个监控器实例在运行。

## 成本

- 监控器本身：**0美元**（仅包含Bash脚本、`/proc`接口调用以及每个周期的一次CLI命令执行）
- 语音警报：**0美元**（通过`jarvis`触发本地TTS警报）
- 心跳处理程序读取状态文件：**0美元**（仅执行一次`cat`命令）
- 唯一的额外成本是心跳处理程序本身的成本（qwen3本地版本免费）

## 适用场景

- 与[agent-superpowers](https://clawhub.com/globalcaos/agent-superpowers)配合使用：该工具用于监控由三个子代理组成的系统。
- 与[smart-model-router](https://clawhub.com/globalcaos/smart-model-router)配合使用：为每个子代理角色自动选择合适的模型。

👉 **https://github.com/globalcaos/tinkerclaw**

欢迎克隆、修改或根据需求进行定制！
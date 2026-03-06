---
name: meshtastic-detection
description: 通过 USB 接收来自 Meshtastic LoRa 设备的 DETECTION_SENSOR_APP 警报。当远程传感器的 GPIO 引脚被触发（检测到预设的目标）时，立即存储该事件并向用户发出警报。
metadata: {"openclaw": {"os": ["darwin", "linux"], "requires": {"anyBins": ["python3.12", "python3.11", "python3.10", "python3"]}, "emoji": "📡"}}
---
# Meshtastic 检测技能

通过 LoRa 接收来自远程 Meshtastic 设备的检测传感器警报。当远程设备的 GPIO 引脚被触发（检测到预设目标）时，该事件会被存储在本地，并需要通过 feishu 立即通知用户。

## 先决条件

- 通过 USB 连接的兼容 Meshtastic 的硬件（RAK4631、T-Beam、Heltec 等）
- 安装了 Python 3.10 及 `meshtastic` 和 `pypubsub` 包（在 `{baseDir}/venv` 中创建虚拟环境）
- `usb_receiver.py` 守护进程正在运行
- 快速设置：`cd {baseDir} && ./setup.sh`
- 详细指南：`{baseDir}/references/SETUP.md`

## 架构

```
┌──────────────────────────────────────────────────────────────┐
│                     USB Receiver Daemon                       │
├──────────────────────────────────────────────────────────────┤
│  LISTEN:  DETECTION_SENSOR_APP only (GPIO trigger events)    │
│  STORE:   data/sensor_data.jsonl (append per detection)      │
│  LATEST:  data/latest.json (most recent detection)           │
└──────────────────────────────────────────────────────────────┘

┌─────────────┐     USB      ┌──────────────┐
│  LoRa Node  │◄────────────►│ usb_receiver │
│  (Radio)    │              │   daemon     │
└─────────────┘              └──────┬───────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
          sensor_cli.py     event_monitor.py   OpenClaw cron
          (query data)      (check alerts)     (feishu alert)
```

## 快速参考

### 运行接收器

```bash
cd {baseDir}
source venv/bin/activate
python scripts/usb_receiver.py --port /dev/cu.usbmodem1CDBD4A896441
```

### 检查新警报

```bash
cd {baseDir}
./venv/bin/python scripts/event_monitor.py
```

每个 `DETECTION_SENSOR_APP` 记录都表示高优先级的警报。输出结果如下：

```json
{
  "alerts": [{"priority": "high", "sender": "!1dd29c50", "text": "alert detected", "received_at": "...", "channel": "ch0", "portnum": "DETECTION_SENSOR_APP"}],
  "summary": "🚨 3 new detection alert(s) from 3 record(s)",
  "alert_count": 3,
  "new_records": 3
}
```

### 查询历史数据

```bash
python scripts/sensor_cli.py latest
python scripts/sensor_cli.py stats --since 24h
python scripts/sensor_cli.py query --since 1h
```

### 数据格式

`data/sensor_data.jsonl` 文件中的每条记录包含以下内容：

```json
{"received_at": "2026-03-04T11:07:06+00:00", "sender": "!1dd29c50", "channel": "ch0", "portnum": "DETECTION_SENSOR_APP", "data": {"type": "detection", "text": "alert detected"}}
```

**仅捕获 `DETECTIONSENSOR_APP` 类型的消息。** 这个端口号表示远程传感器的 GPIO 引脚被触发，即检测到了预设目标。** 所有检测事件都需要立即通知用户。**

其他类型的消息（如 `TEXT_MESSAGE_APP`、遥测数据、位置信息等）将被忽略。

### 日志轮换

`sensor_data.jsonl` 文件会自动按 5 MB 的大小进行轮换（保留 2 个存档文件，总大小约为 15 MB）。轮换过程是透明的：`event_monitor` 会自动重置文件索引，`sensor_cli` 可以跨存档文件读取数据。

## 监控与警报

### Cron 作业（已启用）

Cron 作业每 60 秒运行一次 `event_monitor.py`，并将警报发送到 feishu：

```bash
# Check status
openclaw cron list

# View run history
openclaw cron runs --id <job-id>

# Manual test
openclaw cron run <job-id>

# Edit config
openclaw cron edit <id> --timeout-seconds 60 --to <feishu-open-id>
```

Cron 作业消息模板（供参考）：

```
Run this command and report the output:
cd {baseDir} && ./venv/bin/python scripts/event_monitor.py
— If alert_count > 0, tell me how many alerts, the latest sender and time.
  If alert_count is 0, reply: 暂无新告警。
```

关键配置参数：
- `timeoutSeconds: 60`（代理程序需要大约 20-40 秒来处理任务）
- `channel: feishu`（通知通道）
- `delivery.to: ou_16c6dc8bda8ac97abfd0194568edee59`（通知目标地址）

### 警报行为

所有 `DETECTIONSENSOR_APP` 类型的事件都被视为 **高优先级**。无需额外配置规则——每次检测都会立即触发警报。警报消息包含以下内容：
- 发送设备 ID
- 检测结果（来自远程传感器的配置信息）
- 时间戳

## 配置

编辑 `CONFIG.md` 文件以自定义以下设置：
- **串行端口**：USB 设备的路径
- **通知通道**：`feishu`（在 OpenClaw 中进行配置）

## 常见问答

**用户询问最近检测结果：**
> “过去一小时里检测到了什么？”

运行命令：`cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py query --since 1h`

**用户请求统计信息：**
> “请提供今天的检测总结”

运行命令：`cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py stats --since 24h`

**用户询问系统状态：**
> “传感器还在工作吗？”

运行命令：`cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py status`

## 相关文件

```
{baseDir}/
├── SKILL.md               # This file (agent instructions + metadata)
├── CONFIG.md              # User configuration
├── setup.sh               # One-click setup
├── scripts/
│   ├── usb_receiver.py    # USB serial daemon (DETECTION_SENSOR_APP only)
│   ├── event_monitor.py   # Incremental alert monitor
│   └── sensor_cli.py      # Query CLI
├── data/
│   ├── sensor_data.jsonl  # Detection records (auto-rotated at 5 MB)
│   ├── latest.json        # Most recent detection
│   └── monitor_state.json # Monitor byte offset + seen hashes
└── references/
    └── SETUP.md           # Detailed installation guide
```

## 故障排除

**“未找到任何记录”**
- 确认 `usb_receiver.py` 是否正在运行
- 检查 USB 设备：`ls /dev/cu.usb*`

**“资源暂时不可用”**
- 串行端口只能被一个进程使用。检查：`lsof /dev/cu.usbmodem*`

**接收器已连接但未显示数据**
- 接收器仅捕获 `DETECTIONSENSOR_APP` 类型的消息（其他类型的消息会被忽略）
- 使用 `--debug` 参数运行程序以查看所有数据包：`python scripts/usb_receiver.py --port ... --debug`
- 确认远程设备配置了检测传感器功能（GPIO 引脚监控）
- 确认远程设备处于相同的频道和频率设置下

**Cron 作业超时或发送失败**
- 检查：`openclaw cron runs --id <job-id>`
- 调整超时时间：`openclaw cron edit <id> --timeout-seconds 60`
- 调整发送设置：`openclaw cron edit <id> --to <feishu-open-id>`
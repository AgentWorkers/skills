---
name: radio-copilot
description: 根据指定的纬度/经度，预测卫星的过境时间（NOAA APT、METEOR LRPT、ISS数据），并通过 WhatsApp 发送警报信息，其中包含手动调整天线方向所需的数据（天线指向/视线方向（AOS/LOS）的方位角和仰角、卫星轨道方向以及天线的倾斜角度）。该功能适用于设置或操作无需人工智能辅助的卫星接收调度系统/协调工具，包括配置 NORAD 编号、最低接收仰角、警报提前时间，以及可选的远程数据捕获/解码功能（如使用 Pi RTL-SDR 进行数据捕获，再通过 Jetson SatDump 进行数据解码）。
---

# radio-copilot

用于规划卫星过境时刻并触发SDR（Software Defined Radio）接收器的警报功能。

## 快速入门

1) 复制示例配置文件：

```bash
mkdir -p ~/.clawdbot/radio-copilot
cp config.example.json ~/.clawdbot/radio-copilot/config.json
chmod 600 ~/.clawdbot/radio-copilot/config.json
```

2) 运行一次调度器（orchestator）：

```bash
python3 scripts/orchestrator.py
```

3) 定期运行（通过系统定时任务）：

```bash
*/5 * * * * /usr/bin/python3 /path/to/radio-copilot/scripts/orchestrator.py >> ~/.clawdbot/radio-copilot/orchestrator.log 2>&1
```

## 功能说明

警报信息包括：
- 卫星过境的开始/结束时间戳
- **AOS**（到达卫星时的）方位角/高度角
- **LOS**（离开卫星时的）方位角/高度角
- 轨道方向（从AOS到LOS的航向）
- 卫星轨道倾角

## 注意事项

- 默认情况下，该工具采用“零人工智能”（zero-AI）模式运行。
- 已包含数据捕获和解码的相关功能，但在您配置Pi/Jetson设备的相应命令之前，这些功能是处于禁用状态的。
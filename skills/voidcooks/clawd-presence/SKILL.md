---
name: clawd-presence
description: **AI代理的物理显示功能**  
该功能允许在专用终端或屏幕上展示可自定义的字母组合（A-Z）、代理的状态信息以及当前正在执行的任务。相比聊天方式，这种显示方式能够提供更快速的反馈——用户只需 glance at the display（瞥一眼显示屏）即可了解代理的当前工作状态。该功能适用于需要设置代理始终处于可见状态的场景。
---

# Clawd Presence

这是一个基于终端的AI代理状态显示系统。

## 为什么需要它？

聊天过程中存在延迟。而状态显示系统可以解决这个问题——代理会持续广播自己的状态，用户可以像查看时钟一样随时了解代理的运行情况。

## 设置

```bash
# Configure (auto-detect from clawdbot or manual)
python3 scripts/configure.py --auto
# or
python3 scripts/configure.py --letter A --name "AGENT"

# Run display in dedicated terminal
python3 scripts/display.py
```

## 更新状态

在启动任务时，从代理端调用以下代码：

```bash
python3 scripts/status.py work "Building feature"
python3 scripts/status.py think "Analyzing data"
python3 scripts/status.py idle "Ready"
python3 scripts/status.py alert "Need attention"
python3 scripts/status.py sleep
```

## 状态说明

| 状态 | 颜色 | 说明 |
|-------|-------|-----|
| `idle` | 青色 | 代理处于空闲状态 |
| `work` | 绿色 | 代理正在执行任务 |
| `think` | 黄色 | 代理正在处理任务 |
| `alert` | 红色 | 代理需要人工干预 |
| `sleep` | 蓝色 | 代理处于低功耗状态 |

## 自动切换到空闲状态

如果5分钟内没有状态更新，代理会自动切换回空闲状态。这样可以避免状态显示长时间保持不变（即“过时”）。

```bash
python3 scripts/configure.py --timeout 300  # seconds, 0 to disable
```

## 相关文件

- `scripts/display.py`：主要负责状态显示的逻辑
- `scripts/status.py`：用于更新代理的状态
- `scripts/configure.py`：用于配置代理的状态显示设置
- `assets/monograms/`：包含字母A-Z的图形资源（用于状态显示）
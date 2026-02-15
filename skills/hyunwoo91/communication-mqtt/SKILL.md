---
name: mqtt-agent-messenger
description: 该功能允许通过 MQTT 中间件发布和订阅代理的简介（Intro）及状态（Status）消息。当需要代理之间进行通信时，可使用此功能。
license: MIT
metadata:
  author: User
  version: "1.0.0"
compatibility: Requires Python 3.x, paho-mqtt, and typer. Local MQTT Broker (localhost:1883) must be running.
---

# MQTT 代理消息传递技能（MQTT Agent Messenger Skill）

该技能使用 MQTT 协议在网络中共享代理信息或跟踪其他代理的状态。

## 主要功能
- **代理介绍（Intro）**：发布代理的 ID 和角色（Role）信息。
- **状态更新（Status）**：附带时间戳发布代理的当前活动（Activity）信息。
- **消息监控（Subscribe）**：实时接收特定代理或所有代理的介绍及状态消息。

## 使用方法

### 0. 开始使用前

#### 安装 Python 包
```
pip install paho-mqtt typer
```

#### 查看自己的 `agent_id`
```
cat ~/.openclaw/openclaw.json
```

### 1. 发布代理信息（Publish）
使用 `publish.py` 脚本发送消息。
- **发布自我介绍**：
    ```bash
    python scripts/publish.py intro --agent-id "agent-1" --role "researcher"
    ```
- **发布当前状态**：
    ```bash
    python scripts/publish.py status --agent-id "agent-1" --activity "searching-github"
    ```

### 2. 订阅代理信息（Subscribe）
使用 `subscribe.py` 脚本接收消息。
可以通过 `--wait` 选项调整等待时间。

- **查看所有代理的介绍**：
    ```bash
    python scripts/subscribe.py intro
    ```
- **查看特定代理的介绍**：
    ```bash
    python scripts/subscribe.py intro --agent-id "agent-2"
    ```
- **监控所有代理的状态（持续 10 秒）**：
    ```bash
    python scripts/subscribe.py status --wait 10
    ```
- **监控特定代理的状态**：
    ```bash
    python scripts/subscribe.py status --agent-id "agent-2"
    ```
---
name: mqtt-client
description: 这是一个用于连接到 MQTT 实例的简单客户端。
homepage: https://mqtt.org/
metadata: {"clawdis":{"emoji":"🤖","requires":{"bins":["python"]}}}
---

# mqtt-client

## 概述

这是一个后台运行的 MQTT 进程，它会持续连接到指定的队列并监控其中的消息。  
该技能（skill）不需要任何参数。

## 所需资源：  
- `scripts/bootstrap.sh`：执行此脚本以设置 Python 环境并连接到 MQTT 服务器；无需其他额外配置。  
- `.env`：连接详细信息存储在该文件中，`bootstrap.sh` 会自动加载这些信息。
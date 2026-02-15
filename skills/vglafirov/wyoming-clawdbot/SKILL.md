---
name: wyoming-clawdbot
description: Wyoming Protocol：用于将 Home Assistant 语音助手与 Clawdbot 集成的桥梁组件。
---

# Wyoming-Clawdbot

该插件通过 Wyoming 协议将 Home Assistant Assist 的语音命令桥接到 Clawdbot。

## 功能概述

- 接收来自 Home Assistant Assist 的语音命令；
- 将这些命令转发给 Clawdbot 进行处理；
- 将 Clawdbot 生成的人工智能响应通过 Home Assistant 的文本到语音（TTS）功能播放出来。

## 设置步骤

1. 克隆并运行服务器：
```bash
git clone https://github.com/vglafirov/wyoming-clawdbot.git
cd wyoming-clawdbot
docker compose up -d
```

2. 在 Home Assistant 中添加 Wyoming 插件：
   - 进入“设置” → “设备与服务” → “添加插件”；
   - 搜索“Wyoming Protocol”；
   - 输入服务器地址和端口（例如：`192.168.1.100:10600`）。

3. 配置语音助手（Voice Assistant）的对话流程，将“clawdbot”设置为对话代理（Conversation Agent）。

## 硬件/软件要求

- Clawdbot 必须运行在同一台服务器上；
- Home Assistant 需要安装 Wyoming 插件；
- 建议使用 Docker 或 Python 3.11 及更高版本。

## 链接

- GitHub 仓库：https://github.com/vglafirov/wyoming-clawdbot
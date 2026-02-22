---
name: jarvis-ui
description: >
  OpenClaw代理的JARVIS风格HUD（ Heads-Up Display）Web界面：  
  - 支持交互式的Three.js图形渲染，可实时展示代理的状态信息；  
  - 通过Gateway的WebSocket功能实现实时聊天；  
  - 配备音频频谱分析器；  
  - 提供系统监控功能；  
  - 支持文本转语音（TTS）功能。  
  适用于需要为OpenClaw代理创建可视化控制面板的情况。
metadata: {"openclaw":{"emoji":"🦾","version":"1.0.3","requires":{"bins":["node","npm"]},"homepage":"https://github.com/jincocodev/openclaw-jarvis-ui"}}
---
# 🦾 JARVIS UI

这是一个专为 OpenClaw 代理设计的、具有 JARVIS 风格的用户界面（HUD）。

## 安装

```bash
./setup.sh
```

系统会自动从 `~/.openclaw/openclaw.json` 文件中检测 Gateway 令牌。  
> **⚠️ 远程访问/非本地主机访问：** 如果您从其他机器（非本地主机）访问 JARVIS 服务器，请将以下内容添加到 `~/.openclaw/openclaw.json` 文件中：  
> ```json
> { "gateway": { "controlUi": { "allowInsecureAuth": true } } }
> ```  
> 然后重启 OpenClaw Gateway。  

之后，您可以启动 JARVIS UI：  
```bash
node --env-file=.env server/index.js
```

访问地址：`http://localhost:9999`

## 自定义

复制并编辑 `config.local.json` 文件：  
```bash
cp config.json config.local.json
```

| 字段 | 描述 | 默认值 |
|-------|-------------|---------|
| `name` | 页面标题 | JARVIS |
| `agent.name` | 代理显示名称 | JARVIS |
| `agent.emoji` | 代理表情符号 | 🤖 |
| `agent.sessionKey` | OpenClaw 会话密钥 | agent:main:main |
| `server.port` | 服务器端口 | 9999 |
| `ttsVOICE` | macOS 的 TTS 语音 | Samantha |

## 生产环境配置

```bash
npm i -g pm2
pm2 start server/index.js --name jarvis --node-args="--env-file=.env"
pm2 save
```

## 主要功能

- 🔮 Three.js 图形效果 — 根据代理的状态（思考中/说话中/空闲中）动态变化  
- 💬 实时聊天 — 通过 Gateway 的 WebSocket 功能实现实时聊天  
- 🎵 音频可视化工具 — 显示音频的频谱图、波形图  
- 📊 模型状态信息 — 实时显示令牌使用情况、模型详细信息  
- 🖥️ 系统监控工具 — 显示 CPU 使用率、内存占用及运行时间  
- 🗣️ TTS 功能 — 支持 Edge TTS（免费且跨平台）以及 macOS 的 `say` 命令（离线使用）  
- 📱 移动设备兼容性 + PWA（Progressive Web Application）支持  

## 系统要求

- Node.js 20 及以上版本  
- OpenClaw Gateway 需要在本机运行  
- Python 3 及 `edge-tts` 库（通过 `pip install edge-tts` 安装）以实现 TTS 功能  
- 可选：ffmpeg（仅用于 macOS 的 `say` 命令）
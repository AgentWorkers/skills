---
name: voiceclaw-jp
description: OpenClaw 的语音对话接口：支持唤醒词检测、流式大型语言模型（LLM）响应以及文本转语音（Text-to-Speech, TTS）功能。当用户希望通过语音与 OpenClaw 代理进行交互、设置语音助手，或为 OpenClaw 添加语音输入/输出功能时，可选用该接口。该接口支持自定义唤醒词、VOICEVOX TTS 技术，并提供低延迟的句子级响应流式处理能力。
---
# voiceclaw

这是一个用于 OpenClaw 的语音对话功能：用户说出唤醒词 → 语音识别（STT）→ 大语言模型（LLM）处理 → 语音合成（TTS）→ 最后播放音频。

## 系统要求

- OpenClaw 必须在本地运行，并且需要启用 `chatCompletions` 功能。
- 系统必须使用 Node.js 18 及更高版本。
- VOICEVOX 必须运行在 `localhost:50021` 上（[下载地址](https://voicevox.hiroshiba.jp/)。
- 需要支持 Chrome 或 Edge 浏览器，以便使用 Web Speech API 进行语音识别。
- 为了远程访问麦克风，系统需要使用 HTTPS 协议（虽然使用 localhost 时也可以不使用 HTTPS）。

## 快速入门

```bash
# Install
git clone https://github.com/kentoku24/voiceclaw.git
cd voiceclaw
npm install

# Start (no .env needed if OpenClaw is running locally)
npm start
# → [voiceclaw] OpenClaw config loaded from ~/.openclaw/openclaw.json
# → [voiceclaw] listening on http://127.0.0.1:8788

# Open browser
open http://127.0.0.1:8788
```

点击 “开始” 按钮，说出预设的唤醒词（默认为 “アリス”），然后说出你的指令。

## 配置

所有配置项都是可选的。可以通过 `.env` 文件或环境变量进行设置：

| 变量          | 默认值        | 说明                          |
|---------------|-------------|---------------------------------------------|
| `WAKE_WORDS`     | アリスちゃん,アリス,... | 用逗号分隔的唤醒词列表                    |
| `STT_LANG`      | ja-JP        | 语音识别语言                        |
| `OPENCLAW_MODEL`    | openclaw       | 使用的大语言模型名称                     |
| `VOICEVOX_URL`     | http://127.0.0.1:50021 | VOICEVOX 服务端地址                    |
| `VOICEVOX_SPEAKER`    | 1            | VOICEVOX 的扬声器 ID                      |
| `HOST`         | 127.0.0.1       | 服务器绑定地址                        |
| `PORT`         | 8788          | 服务器端口号                        |

OpenClaw 的网关令牌会自动从 `~/.openclaw/openclaw.json` 文件中获取。如有需要，可以使用 `OPENCLAW_GATEWAY_TOKEN` 变量进行覆盖。

## 系统架构

完整的系统架构图请参见 [docs/architecture.md](docs/architecture.md)。

## API 端点

| 方法          | 路径          | 说明                                      |
|---------------|--------------|---------------------------------------------|
| GET | /health       | 系统健康检查                      |
| GET | /api/config     | 客户端可配置的设置（唤醒词、语音识别语言）            |
| POST | /api/chat-stream  | 流式大语言模型交互（SSE 协议）                |
| POST | /api/chat     | 非流式大语言模型交互（备用方案）                |
| POST | /api/tts      | 文本转换为 VOICEVOX 格式的音频文件             |
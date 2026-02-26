---
name: browser-audio-capture
description: 通过 Chrome 的 CDP（Chrome DevTools Protocol）功能，从浏览器标签页（如 Zoom、Google Meet、Teams 等）中捕获音频，并将其流式传输到本地的转录系统中。整个过程无需使用任何 API 密钥，完全在本地完成。
version: 1.0.0
---
# 浏览器音频捕获

该工具可以从任何基于浏览器的会议中捕获标签页的音频，并将 PCM16 格式的音频流式传输到本地端点，以便进行转录。

## 先决条件

- Chrome 浏览器必须已启用远程调试功能：
  ```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=$HOME/.chrome-debug-profile &
```

- 确保已安装 Python 3.9 及 `aiohttp` 库：
  ```bash
pip install aiohttp
```

## 快速入门

### 列出标签页并检测会议

```bash
python3 -m browser_capture.cli tabs
```

使用 🎙️ 标记表示会议相关的标签页（如 Zoom、Meet、Teams、Webex 等）。

### 捕获某个标签页的音频

```bash
# Auto-detect meeting tab
python3 -m browser_capture.cli capture

# Specific tab
python3 -m browser_capture.cli capture --tab <TAB_ID>
```

### 自动检测模式

```bash
python3 -m browser_capture.cli watch --interval 15
```

该工具会持续监控会议相关的标签页，并在检测到会议时自动开始音频捕获。

### 停止捕获/查看状态

```bash
python3 -m browser_capture.cli status
python3 -m browser_capture.cli stop
```

## Chrome 扩展程序（完全自动化）

如需实现无交互式的音频捕获功能，请安装随工具提供的 Chrome 扩展程序：
1. 打开 `chrome://extensions/`，进入开发者模式，然后选择“加载解压的扩展程序文件”。
2. 进入 `scripts/extension/` 目录。
3. 在任何会议标签页上点击 Percept 图标，即可开始音频捕获。

该扩展程序使用了 `chrome.tabCapture` 功能（无需选择屏幕），并在弹窗关闭后仍能持续捕获音频数据（数据存储在后台文档中）。

## 音频输出

音频数据会以 JSON 格式通过 POST 请求发送到 `http://127.0.0.1:8900/audio/browser`：
```json
{
  "sessionId": "browser_1234567890",
  "audio": "<base64 PCM16>",
  "sampleRate": 16000,
  "format": "pcm16",
  "source": "browser_extension",
  "tabUrl": "https://meet.google.com/abc-defg-hij",
  "tabTitle": "Meeting Title"
}
```

请在 `scripts/extension/offscreen.js` 文件中配置端点 URL（`PERCEPT_URL` 变量）。

## 支持的会议平台

- Google Meet
- Zoom（网页版）
- Microsoft Teams
- Webex
- Whereby
- Around
- Cal.com
- Riverside
- StreamYard
- Ping
- Daily.co
- Jitsi
- Discord

## 常见问题解决方法

- **未检测到会议标签页**：请确保 Chrome 浏览器以 `--remote-debugging-port=9222` 参数启动。
- **扩展程序按钮无法点击**：在 `chrome://extensions/` 中重新加载扩展程序。MV3 扩展程序依赖于外部 JS 文件，因此不能使用内联脚本。
- **音频数据未传输**：请确认接收端程序正在 8900 端口运行。扩展程序会将音频数据发送到 `/audio/browser`（JSON 格式），而非 `/audio`（multipart 格式）。
- **捕获在弹窗关闭后停止**：这是使用 CDP 方法时的正常现象。建议使用 Chrome 扩展程序以实现持续捕获（弹窗关闭后数据仍会保存在后台文档中）。
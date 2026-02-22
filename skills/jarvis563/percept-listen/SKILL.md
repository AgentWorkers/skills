# percept-listen

通过可穿戴设备为 OpenClaw 代理捕获并转录环境音频。

## 功能简介

该功能将可穿戴麦克风（如 Omi pendant 或 Apple Watch）连接到 OpenClaw 代理上。捕获的音频会被本地转录，并以结构化对话数据的形式进行流式传输——包括说话者标签、时间戳以及可搜索功能。

## 使用场景

- 用户希望其代理能够监听周围的环境对话。
- 用户请求“开始监听”或“打开麦克风”。
- 用户提及 Omi pendant、可穿戴设备或环境音频相关内容。

## 系统要求

- 需要运行本地 Percept 服务器（命令：`pip install getpercept && percept start`）。
- Omi pendant 需要通过手机与 Percept 应用程序配对，或使用 Apple Watch 并安装 Percept 应用。
- 需配置 Webhook：在 Omi 应用程序的“设置”→“Webhooks”中，将目标 URL 设置为 `https://<your-tunnel>/webhook/transcript`。

## 设置步骤

```bash
# Install Percept
pip install getpercept

# Start the receiver (default port 8900)
percept start

# Or run directly
PYTHONPATH=. python -m uvicorn src.receiver:app --host 0.0.0.0 --port 8900
```

请配置一个隧道（如 Cloudflare、ngrok 或 Tailscale），以便 Omi 设备能够连接到您的本地服务器。

## 工作原理

1. Omi pendant 捕获音频数据，手机通过 STT（Speech-to-Text）技术将音频转换为文本。
2. Percept 接收器将转换后的文本片段通过 Webhook 发送至服务器。
3. 服务器将这些文本片段存储在本地 SQLite 数据库中，并支持 FTS5 全文搜索功能。
4. 所有处理过程均发生在本地，音频数据不会离开用户的设备。

## 数据存储位置

- **SQLite 数据库：** `percept/data/percept.db`
- **实时转录内容：** `/tmp/percept-live.txt`
- **对话记录：** `percept/data/conversations/`

## 配置选项

唤醒词、说话者名称及所有设置均可通过 Percept 控制面板（端口 8960）或直接在 SQLite 数据库中进行管理。

## 链接资源

- **GitHub 仓库：** https://github.com/GetPercept/percept
- **官方文档：** https://github.com/GetPercept/percept/docs
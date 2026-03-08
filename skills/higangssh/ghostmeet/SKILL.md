---
name: ghostmeet
description: 通过 GhostMeet 提供的 AI 会议助手：可以启动会议、获取实时会议记录，并从任何浏览器会议中生成 AI 摘要。
metadata:
  {
    "openclaw": {
      "emoji": "👻",
      "requires": { "anyBins": ["docker", "curl"] }
    }
  }
---
# Ghostmeet — 人工智能会议助手

您可以通过聊天来控制 [ghostmeet](https://github.com/Higangssh/ghostmeet) 工具。该工具支持自托管的会议转录功能，并结合了 Whisper 语音识别技术和人工智能摘要生成功能。

## 先决条件

- **ghostmeet** 后端必须正在运行（使用 Docker 部署）：
  ```bash
  docker compose up -d
  ```
- **必须在开发者模式下安装 Chrome 扩展程序**，该扩展程序位于 `extension/` 文件夹中。

默认后端地址：`http://127.0.0.1:8877`

## 功能介绍

- **“总结我的上次会议”**：根据最新会议内容生成人工智能摘要。
- **“我今天参加了多少次会议？”**：列出所有会议记录。
- **“会议中讨论了什么？”**：获取完整的会议记录文本。
- **“提取行动项”**：从摘要中提取会议中的关键任务。
- **“检查 ghostmeet 的运行状态”**：查询后端的健康状况。

> 注意：启动/停止实时录音功能需要通过 Chrome 扩展程序来完成。该工具主要负责查询和总结已录制的会议内容。

## API 命令

### 健康检查
```bash
curl http://127.0.0.1:8877/api/health
```
返回结果：`{"status": "ok", "whisper_model": "base", "device": "cpu"}`

### 列出所有会议
```bash
curl http://127.0.0.1:8877/api/sessions
```
返回所有会议的列表，包括会议 ID、开始时间以及每个会议的转录片段数量。

### 获取会议记录
```bash
curl http://127.0.0.1:8877/api/sessions/{id}/transcript
```
返回带有时间戳的完整会议记录文本。

### 生成会议摘要
```bash
curl http://127.0.0.1:8877/api/sessions/{id}/summarize
```
（需要 `GHOSTMEET_ANTHROPIC_KEY` 参数）返回会议的关键决策、行动项以及后续步骤。

### 获取已生成的会议摘要
```bash
curl http://127.0.0.1:8877/api/sessions/{id}/summary
```
返回之前生成的会议摘要。

## 使用流程

### 会议进行中
1. 用户在 Chrome 浏览器中加入 Google Meet、Zoom 或 Teams 会议。
2. 点击 ghostmeet 扩展程序图标，弹出侧边栏。
3. 点击 “Start” 按钮，开始实时转录。
4. 会议记录会实时显示在侧边栏中。

### 会议结束后
用户可以请求：
- **“总结我的上次会议”**：列出所有会议，找到最新会议的 ID，获取会议记录并生成摘要。
- **“我今天参加了多少次会议？”**：列出今天的所有会议记录。
- **“提取会议中的行动项”**：从会议摘要中提取关键任务。

### 示例交互流程

用户：**“我上次会议讨论了什么？”**
- 执行：`curl http://127.0.0.1:8877/api/sessions` 获取最新会议记录。
- 执行：`curl http://127.0.0.1:8877/api/sessions/{id}/transcript` 获取会议记录文本。
- 执行：`curl http://127.0.0.1:8877/api/sessions/{id}/summarize` 生成会议摘要。

用户：**“生成包含行动项的会议摘要”**
- 执行：`curl -X POST http://127.0.0.1:8877/api/sessions/{id}/summarize`
- 执行：`curl http://127.0.0.1:8877/api/sessions/{id}/summary` 获取格式化的会议摘要。
- 执行：`curl http://127.0.0.1:8877/api/sessions` 查看今天的会议数量。

## 配置参数

| 参数 | 默认值 | 说明 |
|---------|---------|-------------|
| `GHOSTMEET_MODEL` | `base` | Whisper 语音识别模型（tiny/base/small/medium/large-v3） |
| `GHOSTMEET_LANGUAGE` | auto | 自动选择语言（en/ko/ja 等）或手动指定 |
| `GHOSTMEET_CHUNK_INTERVAL` | `10` | 转录间隔（秒） |
| `GHOSTMEET_ANTHROPIC_KEY` | （可选） | 用于生成摘要的 Claude API 密钥 |
| `GHOSTMEET_HOST` | `0.0.0.0` | 后端绑定地址 |
| `GHOSTMEET_PORT` | `8877` | 后端端口 |

### 模型大小说明：
- **tiny**（75MB）：速度快，但准确性较低，适合快速记录会议要点。
- **base**（145MB）：平衡性较好，适合大多数用户。
- **small**（488MB）：准确性较高，但处理速度较慢。
- **medium**（1.5GB）：准确性最高，需要较强的 CPU/GPU 资源。
- **large-v3**（3GB）：准确性最佳，但需要高性能的 GPU。

## 使用建议：

- **务必先检查后端状态**：在执行其他操作前确认后端正在运行。
- **通过会议 ID 查找会议记录**：会议 ID 通常以日期格式显示（例如 `20260308-065021`）。
- **仅在需要时生成摘要**：生成摘要会消耗 API 访问次数。
- **格式化会议记录**：以易于阅读的形式呈现会议内容，避免直接显示原始 JSON 数据。
- **保护隐私**：会议记录属于敏感信息，请勿在聊天之外分享。
- **如果后端无法正常运行**：建议在 `ghostmeet` 目录中执行 `docker compose up -d` 命令重启后端。

## 常见问题解决方法：

- **连接失败**：后端未启动。请使用 `docker compose up -d` 重启后端。
- **没有会议记录**：可能是因为尚未开始会议记录。确保在会议期间 Chrome 扩展程序处于激活状态。
- **摘要生成失败**：检查 `.env` 文件中是否设置了正确的 `GHOSTMEET_ANTHROPIC_KEY`。
- **转录效果不佳**：尝试使用更高级别的 Whisper 模型或明确指定语言。
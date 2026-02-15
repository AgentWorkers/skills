---
name: mlx-tts
description: 使用 MLX（苹果自研的硅芯片）和开源模型（默认为 QWen3-TTS）在本地实现文本转语音功能。
author: guoqiao
metadata: {"openclaw":{"always":true,"emoji":"🦞","homepage":"https://clawhub.ai/guoqiao/mlx-tts","os":["darwin"],"requires":{"bins":["brew"]}}}
triggers:
- "/mlx-tts <text>"
- "TTS ..."
- "Convert text to audio ..."
- "Say <text>"
- "Reply with voice message ..."
---

# MLX TTS

使用 MLX（苹果自研的硅芯片）和开源模型（默认为 QWen3-TTS）在本地实现文本转语音（Text-To-Speech）功能。

完全免费且运行速度快，无需 API 密钥或服务器支持。

## 系统要求

- 系统：运行 macOS 且搭载苹果自研的硅芯片（Apple Silicon）。
- 工具：需要安装 `brew`，用于在缺少相关软件时自动下载依赖库。

## 安装

```bash
bash ${baseDir}/install.sh
```
如果系统中没有以下 CLI 工具，此脚本会使用 `brew` 来安装它们：
- `uv`：用于安装 Python 包并运行相关 Python 脚本。
- `mlx_audio`：负责实际的语音生成工作。

## 使用方法

要生成音频文件，请运行以下脚本：

```bash
bash ${baseDir}/mlx-tts.sh "<text>"
```

### 使用说明

1. **运行脚本**：将需要转换成语音的文本作为参数传递给脚本。
2. **处理输出**：脚本会输出音频文件的路径。
可以使用 `message` 工具将生成的音频文件以语音消息的形式发送给用户：

```json
{
   "action": "send",
   "filePath": "<filepath>"
}
```

示例：
用户：说“hello world”
系统操作：
1. 运行 `bash path/to/mlx-tts.sh "hello world"`
2. 输出音频文件路径：`/tmp/folder/audio.ogg`
3. 使用 `message` 工具发送音频文件：`message(action="send", filePath="/tmp/folder/audio.ogg", ...)`
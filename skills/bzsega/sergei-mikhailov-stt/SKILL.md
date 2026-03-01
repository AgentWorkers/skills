---
name: sergei-mikhailov-stt
description: 使用 Yandex SpeechKit 从语音消息中识别文本（该框架支持扩展，可适配其他语音服务提供商）。适用于需要将语音消息转换为文本的场景。
metadata: {"openclaw": {"requires": {"bins": ["ffmpeg", "python3"], "env": ["YANDEX_API_KEY", "YANDEX_FOLDER_ID"]}, "primaryEnv": "YANDEX_API_KEY"}}
---
# OpenClaw的语音转文本功能

## 功能简介

该功能能够识别通过任何与OpenClaw连接的通讯工具发送的语音消息，并利用多种语音转文本（STT, Speech-to-Text）服务将语音转换为文本。目前支持的语音转文本服务包括Yandex SpeechKit。

## 使用场景

- 当用户通过OpenClaw连接的通讯工具发送语音消息时；
- 当您需要将语音转换为文本时；
- 当您需要将音频文件转录为文本时；
- 当您需要获取语音消息的文本版本时。

## 工作原理

### 1. 从OpenClaw接收音频文件
- OpenClaw会提供音频文件的本地路径。
- 验证文件是否存在于指定路径下。
- 核实文件格式（支持OGG、WAV、MP3格式）。
- 检查文件大小（对于Yandex SpeechKit v1同步API，文件大小不得超过1MB）。

**示例路径：** **```
/home/user_folder/.openclaw/media/inbound/file_1---9a53bac2-0392-41e7-8300-1c08e8eec027.ogg
```**

### 2. 音频处理
- 验证本地路径下的音频文件。
- 如有需要，使用ffmpeg将其转换为支持的格式。
- 检查音频质量。

### 3. 语音识别
- 使用默认的语音转文本服务（Yandex SpeechKit）进行识别。
- 如果识别失败，尝试其他替代服务。
- 返回识别结果以及相应的置信度信息。

### 4. 结果处理
- 格式化识别后的文本。
- 显示识别出的语言。
- 根据需求提供元数据。

## 快速入门

**setup.sh**脚本会创建一个Python虚拟环境，安装所需依赖项，并复制示例配置文件。运行脚本后，请添加您的API密钥（详见下方配置部分），然后重启OpenClaw。

> 在Debian/Ubuntu系统中，您可能需要先安装`venv`包：`sudo apt install python3-venv`

## 配置

### 1. 设置API密钥（推荐方式：通过OpenClaw配置文件）

将API密钥添加到`~/.openclaw/openclaw.json`文件中：
**```json
{
  "skills": {
    "entries": {
      "sergei-mikhailov-stt": {
        "env": {
          "YANDEX_API_KEY": "your_api_key_here",
          "YANDEX_FOLDER_ID": "your_folder_id_here"
        }
      }
    }
  }
}
```**

### 2. 替代方式：通过`.env`文件

编辑`setup.sh`脚本在技能文件夹中生成的`.env`文件：
**```
YANDEX_API_KEY=your_api_key_here
YANDEX_FOLDER_ID=your_folder_id_here
STT_DEFAULT_PROVIDER=yandex
```**

### 3. 重启OpenClaw以应用配置更改

**```bash
openclaw gateway stop && openclaw gateway start
```**

### 4. 服务提供商配置（可选）

`config.json`文件（同样由`setup.sh`生成）允许您调整服务提供商的参数：
**```json
{
  "default_provider": "yandex",
  "providers": {
    "yandex": {
      "api_key": "${YANDEX_API_KEY}",
      "folder_id": "${YANDEX_FOLDER_ID}",
      "lang": "ru-RU"
    }
  }
}
```**

## 添加新的语音转文本服务提供商

### 1. 创建服务提供商类

**```python
# scripts/providers/new_provider.py
from .base_provider import BaseSTTProvider

class NewProvider(BaseSTTProvider):
    name = "new_provider"

    def recognize(self, audio_file_path: str, language: str = 'ru-RU') -> str:
        # Recognition implementation
        pass

    def validate_config(self, config: dict) -> bool:
        # Configuration validation
        pass

    def get_supported_formats(self) -> list:
        return ['ogg', 'wav', 'mp3']
```**

### 2. 注册服务提供商

在`scripts/stt_processor.py`文件中的 `_get_provider` 方法中添加新的服务提供商：
**```python
if provider_name == 'new_provider':
    return NewProvider(provider_config)
```**

### 3. 更新配置

在`config.json`文件中添加新的服务提供商信息：
**```json
{
  "providers": {
    "new_provider": {
      "api_key": "${NEW_PROVIDER_API_KEY}",
      "model": "latest"
    }
  }
}
```**

## 使用示例

- **基本用法**
**```
User: [sends a voice message]
OpenClaw: Recognized text: "Hello, how are you?"
```**

- **指定语言的用法**
**```
User: Transcribe this English voice message
OpenClaw: Recognized text (en-US): "Hello, how are you today?"
```**

- **包含元数据的用法**
**```
User: Analyze this voice message
OpenClaw: Recognized text: "Meeting tomorrow at 3 PM"
Language: ru-RU
Confidence: 95%
Provider: Yandex SpeechKit
```**

## 错误处理

当功能出现错误时，请用通俗的语言向用户说明问题，并提供具体的下一步操作建议。不要直接显示原始错误信息或堆栈跟踪。

| 错误类型 | 向用户说明 | 下一步操作 |
|---------|-----------|-----------|
| 文件过大 | “语音消息太长——目前最长支持30秒。” | 请用户发送更短的消息。 |
| 格式不支持 | “此音频格式不被支持。” | 告知用户支持的格式：OGG、WAV、MP3、M4A、FLAC、AAC。 |
| API密钥无效 / HTTP 401 | “Yandex SpeechKit API密钥有问题。” | 请用户检查`openclaw.json`文件中的`YANDEX_API_KEY`。 |
| 访问文件夹被拒绝 / HTTP 403 | “无法访问Yandex SpeechKit。” | 请用户确认服务账户是否具有`ai.speechkit.user`角色。 |
| 请求次数过多 / HTTP 429 | “Yandex SpeechKit当前处于限制请求状态。” | 请稍后再试。 |
| 未找到FFmpeg | “服务器上未安装音频转换工具FFmpeg。” | 请用户运行`brew install ffmpeg`或`apt install ffmpeg`。 |
| API请求超时 | “Yandex SpeechKit未及时响应。” | 请再次尝试；如果问题持续，请检查服务是否正常运行。 |
| 缺少YANDEX_API_KEY | “功能未配置——API密钥未设置。” | 请用户将密钥添加到`~/.openclaw/openclaw.json`文件中。 |

## 故障排除（针对管理员）

1. 检查`~/.openclaw/openclaw.json`文件中的API密钥配置。
2. 确保已安装FFmpeg：`ffmpeg -version`
3. 确认Yandex Cloud服务账户具有`ai.speechkit.user`角色。
4. 查看日志文件：`openclaw logs`

## 限制条件

- 最大文件大小：1MB（Yandex SpeechKit v1同步API的限制，最长支持约30秒的语音）
- 支持的音频格式：OGG、WAV、MP3、M4A、FLAC、AAC
- 支持的语言：俄语（ru-RU）、英语（en-US）
- 处理时间：最长5分钟
- 最长音频时长：30分钟

## 所需软件及环境

- Python 3.8及以上版本
- FFmpeg
- 配置好的语音转文本服务提供商的API密钥

## 识别结果格式

识别成功后，系统会返回以下格式的文本：
**```json
{
  "text": "Recognized text",
  "language": "ru-RU",
  "confidence": 0.95,
  "provider": "yandex",
  "processing_time": 2.5
}
```**
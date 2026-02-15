---
name: chichi-speech
description: 这是一个基于Qwen3和专门的语音克隆技术开发的RESTful服务，用于将文本转换为高质量的语音。该服务经过优化，能够重复使用特定的语音提示，从而避免不必要的重新计算。
---

# Chichi Speech Service

该技能提供了一个基于 FastAPI 的 REST 服务，用于 Qwen3 TTS（文本到语音转换）。该服务经过专门配置，可以复用高质量的参考音频提示，以实现高效且一致的语音克隆功能。该服务以可安装的 CLI（命令行工具）的形式提供。

## 安装

先决条件：`python >= 3.10`。

```bash
pip install -e .
```

## 使用方法

### 1. 启动服务

服务默认运行在端口 **9090** 上。

```bash
# Start the server (runs in foreground, use & for background or a separate terminal)
# Optional: Uudate to your own reference audio and text for voice cloning
chichi-speech --port 9090 --host 127.0.0.1 --ref-audio "https://qianwen-res.oss-cn-beijing.aliyuncs.com/Qwen3-TTS-Repo/clone_2.wav" --ref-text "Okay. Yeah. I resent you. I love you. I respect you. But you know what? You blew it! And thanks to you."
```

### 2. 验证服务是否正在运行
请查看健康检查文档（health/docs）以确认服务是否正常运行：
```bash
curl http://localhost:9090/docs
```

### 3. 生成语音

使用 cURL 命令进行语音生成：
```bash
curl -X POST "http://localhost:9090/synthesize" \
     -H "Content-Type: application/json" \
     -d '{
           "text": "Nice to meet you",
           "language": "English"
         }' \
     --output output/nice_to_meet.wav
```

## 功能特性

-   **端点**：`POST /synthesize`
-   **默认端口**：9090
-   **语音克隆**：使用参考文件中的预计算音频提示，确保克隆出的语音具有高度一致性，并且生成速度较快。

## 所需依赖

-   Python 3.10 及以上版本
-   `qwen-tts`（Qwen3 模型库）
- **参考音频文件**：用于语音克隆的音频文件。
    - 默认情况下，系统会使用 Qwen3 提供的公共样本音频。
    - **重要提示**：您也可以通过 `--ref-audio` 和 `--ref-text` 参数提供自定义的参考音频文件。
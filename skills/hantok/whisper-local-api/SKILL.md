---
name: whisper-local-api
description: OpenClaw专用的、安全的、离线的、兼容OpenAI的本地Whisper语音识别（ASR）端点。该端点支持更快速的识别速度（采用large-v3-turbo算法），具备内置的隐私保护机制（无需上传任何数据到云端），占用较少的系统内存资源，并能实现高精度的语音转文本功能。非常适合用于需要安全、私密的AI语音指令交互场景。
---
# Whisper Local API – 安全且私密的自动语音识别（ASR）服务

部署一个以隐私保护为核心、100% 本地化的音转文本服务。该服务允许 OpenClaw 在您的本地硬件上安全地处理音频转录内容，而无需与任何第三方云 API 进行交互。

## 主要的 SEO 与安全特性

*   **100% 离线且私密**：您的语音数据、指令以及转录结果永远不会离开您的主机系统，完全不依赖云服务。
*   **高精度**：通过 `faster-whisper` 使用 `large-v3-turbo` 模型，即使在存在口音或背景噪音的情况下也能实现业界领先的识别精度。
* **低内存占用**：仅需约 400–500MB 的 RAM，非常适合 VPS 或资源有限的边缘服务器使用。
* **兼容 OpenAI API**：提供 `/v1/audio/transcriptions` 端点，该端点遵循 OpenAI 的 JSON 格式，可与任何支持 OpenAI Whisper API 的软件无缝集成。

## 标准工作流程

1. 安装/更新运行时环境：
   ```bash
   bash scripts/bootstrap.sh
   ```
2. 启动服务：
   ```bash
   bash scripts/start.sh
   ```
3. 验证服务运行状态：
   ```bash
   bash scripts/healthcheck.sh
   ```
4. （可选）使用本地音频文件进行测试：
   ```bash
   bash scripts/smoke-test.sh /path/to/test-speech.mp3
   ```

## 仓库位置

脚本默认使用的安装/更新路径：
*   `~/whisper-local-api`

在运行脚本前，可以通过环境变量覆盖此路径：
```bash
WHISPER_DIR=/custom/path bash scripts/bootstrap.sh
```

## OpenClaw 集成说明

在通过健康检查后，可以使用安全的本地端点：
*   URL：`http://localhost:9000`
*   端点：`/v1/audio/transcriptions`

网络传输过程中不会传递任何认证令牌。

## 安全注意事项

* 在执行任何包管理器操作之前，请务必先确认操作内容。
* 该 API 仅在本地绑定到 `0.0.0.0` 地址；如果需要公开访问，请通过安全的反向代理（如 Nginx）进行转发，并强制使用 HTTPS 加基本身份验证。
* 该服务会自动调整内存分配方式（从 `float16` 切换到 `int8`），以防止 CPU 崩溃。
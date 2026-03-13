---
name: local-voice-reply
description: 使用本地的 FastAPI TTS 服务器为 Feishu 和 Discord 生成本地 OPUS/Ogg 格式的语音回复（默认使用 Juno 语音）。需要将 ffmpeg 添加到系统的 PATH 环境变量中，并安装相应的 Python 库（torch/torchaudio/chatterbox-tts/fastapi/uvicorn）。该功能会在 `/voice_mode_on` 被设置为开启状态时激活，或者当用户请求语音回复或音频消息时触发。
---
# 本地语音回复功能

使用此功能可将文本转换为克隆的语音音频，并将其可靠地发送到 Feishu 或 Discord。

服务器实现代码与该功能位于同一目录下（而非工作区的根目录）：
- `server/voice_server_v3.py`（FastAPI 路由）
- `server/voice_engine.py`（语音生成与缓存引擎）

语音资源也存储在同一目录下：
- `voice/`

## 运行时要求

- 必须安装 `ffmpeg` 并将其添加到 `PATH` 环境变量中（用于 Opus 编码）。
- 服务器所需的 Python 包：
  - `fastapi`
  - `uvicorn`
  - `python-multipart`
  - `chatterbox-tts`
  - `torch`
  - `torchaudio`
  - `numpy`
- 在首次启动时，`ChatterboxTTS.from_pretrained()` 可能会下载模型资源，因此初次运行可能需要网络连接和额外的磁盘空间。
- 可选的环境变量：
  - `TARVIS_VOICE_OUTPUT_DIR`：用于指定生成的 Opus 文件的保存路径。
  - `TARVIS_VOICE_DEVICE`：用于强制选择音频生成设备（`cuda`/`gpu`、`mps` 或 `cpu`）。

## 数据持久化机制

- 通过 `POST /voice/register` 上传的语音样本会保存在 `server/voices/` 目录下。
- 缓存和注册表数据会保存在 `server/voice_cache/` 目录下。
- 生成的 Opus 文件默认保存在 `.openclaw/media/outbound/voice-server-v3/` 目录中（或根据 `TARVIS_VOICE_OUTPUT_DIR` 的设置）。
- `POST /output/cleanup` 命令会删除配置的输出目录中的 `.opus` 文件及其对应的 `.json` 文件。

## 使用方法

1. 确保本地运行的是 **v3.3** 版本的 TTS 服务器（位于该功能文件夹中）：
   - `python -m uvicorn --app-dir server voice_server_v3:app --host 127.0.0.1 --port 8000`
2. 调用 `/speak` 命令，传入文本（以及可选的 `speed`、`exaggeration`、`cfg` 参数）。
   - `voice_name` 的默认值为 `juno`。
3. 从服务器接收生成的音频文件（格式为 `.ogg`），音色为 Juno。
4. 将最终生成的音频文件保存到允许的路径中：
   - `C:\Users\hanli\.openclaw\media\outbound\`
5. 使用 `message` 工具发送音频文件：
   - `action=send`
   - `filePath=<允许的路径>`
   - `asVoice=true`
   - 发送到 Feishu 的路径：`channel=feishu`
   - 发送到 Discord 的路径：`channel=discord`

## 默认参数

- `voice_name`：`juno`
- `speed`：`1.2`
- 输出格式：服务器通过 `/speak` 生成的 Opus 文件（无需额外转换）
- Discord 兼容性：支持 Ogg/Opus 格式，可通过 `asVoice=true` 作为语音消息发送

## 本版本的性能优化

- 启动时仅缓存一次模型查找信息。
- 在语音合成过程中使用 `torch.inference_mode()` 以减少计算开销。
- 对于 `/speak` 和 `/speak_stream` 两个命令，重用相同的短语缓存。
- 改进了长中文文本的分块处理方式，避免生成过大的音频文件。
- 提供了延迟指标，便于进行性能测试和调优。

## 常见问题及解决方法

- 错误：`LocalMediaAccessError ... path-not-allowed`
  - 解决方法：在发送前将文件复制到 `.openclaw/media/outbound` 目录中。

## 脚本

- 使用 `scripts/send_voice_reply.ps1` 脚本，使用默认参数（`voice_name=juno`、`speed=1.2`）生成音频文件。
  - 对于较长的文本，脚本会自动选择 `/speak_stream` 命令以提高处理效率。
- 在执行需要严格审批的 CUDA 生成任务时，使用 `scripts/generate_cuda_voice.ps1` 脚本：
    - `scripts/generate_cuda_voice.ps1 -Text "..."`
    - 此脚本保持了命令格式的稳定性，便于重复使用。
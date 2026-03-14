---
name: senseaudio-tts
description: 在 `/v1/t2a_v2` 和 `/ws/v1/t2a_v2` 上构建和调试 SenseAudio 的文本转语音（TTS）集成功能，包括 HTTP 数据同步、SSE 流传输、WebSocket 事件序列化、十六进制音频解码以及语音/音频参数的调整。每当用户请求 TTS 生成、低延迟流媒体语音服务、语音选择或 TTS 错误排查时，均可使用此功能。
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---
# SenseAudio TTS

使用此技能完成所有SenseAudio语音合成任务。

## 阅读前须知

- 请参考 `references/tts.md` 文件以获取更多信息。

## 工作流程

1. 选择合适的协议：
- 对于简单的单次语音生成任务，使用 HTTP 同步协议。
- 对于需要分批次传输音频数据的情况，使用 SSE 协议。
- 对于实时语音合成需求（文本到音频的转换），使用 WebSocket 协议。

2. 构建有效的请求：
- 包含认证头、模型信息、文本内容以及 `voice_setting.voice_id` 参数。
- 如用户有特殊要求，可添加额外的调整参数。

3. 实现输出解析：
- 将 `data.audio` 中的十六进制数据解码为字节格式。
- 根据终端的状态或事件来完成整个语音合成过程。

4. 为生产环境优化代码：
- 处理认证错误和参数错误。
- 为短暂的网络故障提供重试或退避机制。
- 记录会话信息及跟踪标识符。
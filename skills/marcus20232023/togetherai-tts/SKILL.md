# TogetherAI TTS

使用 TogetherAI API 和 MiniMax speech-2.6-turbo 模型实现文本转语音功能。

## 使用方法

```bash
cd /home/marc/clawd/skills/togetherai_tts
node index.js "your text here" output.mp3
```

## 配置

请在 `.env` 文件中设置以下参数：
- `TOGETHERAI_API_KEY`：您的 TogetherAI API 密钥
- `TOGETHERAI_MODEL`：要使用的模型（默认值：minimax/speech-2.6-turbo）
- `TTS_FORMAT`：输出格式（默认值：mp3）
- `TTS_VOICE`：要使用的语音（默认值：default）
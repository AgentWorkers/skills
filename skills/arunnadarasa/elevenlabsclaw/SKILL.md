---
name: elevenlabs
description: 使用 ElevenLabs 将文本转换为自然语言语音，适用于临床和医疗保健场景。适用于生成患者指导信息、出院总结、用药提醒、多语言健康提示，或为 OpenClaw 临床黑客马拉松活动提供可访问的语音内容。
metadata:
  {"openclaw":{"requires":{"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY","emoji":"🔊"}}
---
# ElevenLabs 语音合成技术：临床项目应用

**OpenClaw 临床黑客马拉松**参赛者的快速入门技能。使用 ElevenLabs 的语音合成技术为患者提供语音服务，包括指令、提醒、出院信息等可访问的内容。

## 先决条件

- **ELEVENLABS_API_KEY**：请将其设置到环境变量中，或保存在 `~/.openclaw/openclaw.json` 文件的 `skills.entries.elevenlabs.apiKey` 字段中（或 `env.ELEVENLABS_API_KEY`）。  
- 你可以在 [ElevenLabs](https://elevenlabs.io/) 获取 API 密钥（提供免费试用）。

## 适用场景

- 患者出院或后续护理时的语音提示。  
- 药物服用或预约提醒。  
- 多语言健康信息（支持 30 多种语言）。  
- 将书面临床文本转换为清晰的语音内容。  
- 长篇内容（如患者教育资料），需使用自然、富有同情心的表达方式。

## 使用方法

1. **确保已安装语音合成工具**  
   如果你的 OpenClaw 环境中配备了语音合成工具（例如 `tts_text_to_speech` 或类似工具），请将其配置为使用 ElevenLabs 作为服务提供者。配置时需要输入 `ELEVENLABS_API_KEY`。  

2. **用户请求语音输出时**  
   - 对于指令和提醒，使用简短、清晰的语句。  
   - 对于医学术语，可使用 ElevenLabs 提供的发音辅助功能或发音词典来提高准确性。  
   - 在临床语音内容中，建议使用平静、专业的发音风格。  

3. **直接调用 API 时**  
   - API 端点：`POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}`  
   - 请求头：`xi-api-key: <ELEVENLABS_API_KEY>`, `Content-Type: application/json`  
   - 请求体：`{"text": "<内容>", "model_id": "eleven_multilingual_v2"}`（如需低延迟，可使用 `eleven_flash_v2_5`）。  
   - 对于非英语或混合语言的临床文本，建议使用 `eleven_multilingual_v2` 模型。  

## 临床语音合成的最佳实践

- **语调**：使用温暖、清晰、专业的语调；避免过于随意或夸张的表达。  
- **分段处理**：将长文本拆分成短段落或列表，以提高清晰度和节奏感。  
- **语言设置**：根据患者的语言偏好选择合适的语言模型。  
- **敏感信息处理**：不要在日志或外部通信中包含患者隐私信息（PHI）；确保 API 使用符合安全性和合规性要求。  

## 快速参考

| 使用场景                | 建议使用的模型                          |
|-------------------|------------------------------------|
| 短暂提醒                | `eleven_flash_v2_5`（适用于快速响应）                |
| 长篇/多语言内容            | `eleven_multilingual_v2`                    |
| 医学术语                | 使用发音辅助功能或词典（如支持）                    |

## 常见问题解答

- [ElevenLabs 语音合成 API 文档](https://elevenlabs.io/docs/api-reference/text-to-speech)  
- [ElevenLabs 在医疗领域的应用案例](https://elevenlabs.io/use-cases/healthcare)
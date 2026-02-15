---
name: sag
description: ElevenLabs 的文本转语音功能，具备 Mac 风格的用户界面（UX）。
homepage: https://sag.sh
metadata: {"clawdbot":{"emoji":"🗣️","requires":{"bins":["sag"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY","install":[{"id":"brew","kind":"brew","formula":"steipete/tap/sag","bins":["sag"],"label":"Install sag (brew)"}]}}
---

# sag

使用 `sag` 命令可以调用 ElevenLabs 的文本转语音（TTS）服务，并实现本地播放功能。

**API 密钥（必需）**  
- `ELEVENLABS_API_KEY`（推荐使用）  
- `SAG_API_KEY` 也支持通过 CLI 进行调用  

**快速上手示例**  
- `sag "Hello there"`  
- `sag speak -v "Roger" "Hello"`  
- `sag voices`  
- `sag prompting` （针对特定模型的使用提示）  

**模型说明**  
- **默认模型**：`eleven_v3`（表达力强）  
- **稳定模型**：`eleven_multilingual_v2`  
- **快速模型**：`eleven_flash_v2_5`  

**发音与表达规则**  
- 对于专有名词（如 “key-note”），请确保拼写正确；必要时添加连字符或调整大小写。  
- 数字、单位或 URL：使用 `--normalize auto` 选项进行自动规范处理（如需保留原格式，可设置为 `off`）。  
- 语言偏好：通过 `--lang en|de|fr|...` 指定规范规则。  
- **v3 版本**：不支持 SSML 中的 `<break>` 标签，应使用 `[pause]`、`[short pause]`、`[long pause]` 来控制停顿。  
- **v2/v2.5 版本**：支持 SSML 中的 `<break time="1.5s" />` 标签；`<phoneme>` 标签在 `sag` 命令中不可使用。  

**v3 版本的音频效果标签**  
- `[whispers]`（低语）  
- `[shouts]`（大喊）  
- `[sings]`（唱歌）  
- `[laughs]`（笑）  
- `[starts laughing]`（开始笑）  
- `[sighs]`（叹气）  
- `[exhales]`（呼气）  
- `[sarcastic]`（讽刺的）  
- `[curious]`（好奇的）  
- `[excited]`（兴奋的）  
- `[crying]`（哭泣的）  
- `[mischievously]`（调皮地）  
- **示例**：`sag "[whispers] 请保持安静。[short pause] 好吗？"`  

**默认语音设置**  
- 使用 `ELEVENLABS_VOICE_ID` 或 `SAG_VOICE_ID` 作为默认语音。  

**长时间输出前的语音确认**  
在使用语音功能前，请先确认所选的语音和发音效果。  

## 聊天中的语音回复  
当用户请求特定风格的语音回复时（例如：“crazy scientist voice” 或 “explain in voice”），系统会生成相应的音频并发送给用户：  

```bash
# Generate audio file
sag -v Clawd -o /tmp/voice-reply.mp3 "Your message here"

# Then include in reply:
# MEDIA:/tmp/voice-reply.mp3
```  

**语音角色提示**：  
- **疯狂科学家**：使用 `[excited]` 标签，配合戏剧性的停顿（`[short pause]`），并调整语调的强度。  
- **平静的语气**：使用 `[whispers]` 或较慢的语速。  
- **戏剧性的语气**：谨慎使用 `[sings]` 或 `[shouts]` 标签。  

**Clawd 的默认语音**：`lj2rcrvANS3gaWWnczSX`（或直接使用 `-v Clawd`）。
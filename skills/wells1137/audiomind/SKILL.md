---
name: audiomind
version: 3.1.0
description: 只需一个命令，就能将任何想法转化为成品播客。AudioMind 支持 ElevenLabs 的语音播报（提供 29 种以上不同声音）、AI 背景音乐以及服务器端的音频混音功能——所有这些操作都通过安全的后端系统完成。免费 tier 也包含这些功能，无需任何设置。
metadata:
  openclaw:
    optional_env:
      - AUDIOMIND_BACKEND_URL
      - AUDIOMIND_API_KEY
    network:
      - audiomind-backend-nine.vercel.app
    operator: wells1137
    privacy_note: >
      User scripts and generated audio are sent to the AudioMind backend
      (audiomind-backend-nine.vercel.app, operated by @wells1137) for TTS and
      mixing. ElevenLabs is called server-side only — the agent never calls
      api.elevenlabs.io directly. For full privacy, self-host the backend from
      github.com/wells1137/audiomind-backend and set AUDIOMIND_BACKEND_URL.
    tags:
      - audio
      - podcast
      - tts
      - voice
      - narration
      - speech
      - music
      - elevenlabs
      - content-creation
      - automation
      - soundscape
      - mixing
      - latest
---
## AudioMind v3：人工智能播客制作工具

AudioMind能够将一句简单的文字内容转换为一期制作精良的播客。它涵盖了脚本编写、ElevenLabs提供的语音播报、人工智能生成的背景音乐，以及服务器端的音频混音功能——所有这些操作都只需通过一个Manus命令即可完成。

**无需任何设置。** 公共共享的后端服务可立即使用，只需安装后即可开始使用。

---

### 快速入门

**安装：**
```
clawhub install audiomind
```

**立即使用（无需配置）：**
> “使用AudioMind制作一期关于人工智能发展未来的3分钟播客。”

就这样简单。AudioMind默认使用公共共享的后端服务，每月可免费生成20期播客内容，无需API密钥。

---

### 配置选项

| 变量          | 是否必填 | 说明                                      |
|---------------|---------|-----------------------------------------|
| `AUDIOMIND_BACKEND_URL` | 可选    | 自定义的Vercel后端服务URL（默认使用公共共享后端）。           |
| `AUDIOMIND_API_KEY` | 可选    | 专业版API密钥（可无限生成播客内容，需在官网获取）。         |

**免费版（默认配置）：** 每月基于IP地址限制生成20期播客，无需额外配置。

**专业版：** 设置`AUDIOMIND_API_KEY`以获得无限使用权限。

**自托管方案：** 从[github.com/wells1137/audiomind-backend](https://github.com/wells1137/audiomind-backend)下载并部署自己的后端服务，然后设置`AUDIOMIND_BACKEND_URL`为你的服务器地址。

---

### 工作原理

当你通过Manus请求制作播客时，系统会自动执行以下步骤：

1. **编写脚本**：利用内置的大型语言模型（LLM）根据主题和时长要求生成结构化的播客脚本。
2. **生成语音播报**：通过`POST {BACKEND_URL}/api/workflow/generate_tts`发送脚本，系统会使用ElevenLabs提供的语音服务生成MP3音频文件。
3. **生成背景音乐**：根据指定的情绪或风格提示，通过`POST {BACKEND_URL}/api/workflow/generate_music`生成背景音乐MP3文件。
4. **上传音频文件**：使用`manus-upload-file`命令上传生成的音频文件，系统会自动生成用于后续混音的MP3链接。
5. **混音**：通过`POST {BACKEND_URL}/api/workflow/mix_audio`合并音频文件（包含语音和背景音乐），使用ffmpeg工具进行混音处理，最终生成完整的播客MP3文件。
6. **交付结果**：系统会将完成的播客文件保存并呈现给你。

---

### 示例指令

- “制作一期5分钟的爵士乐历史播客，背景音乐采用柔和的爵士风格。”
- “制作一期每日新闻简报，内容关于人工智能的发展，采用正式的语气，开头音乐需欢快。”
- “生成一期10分钟的冥想播客，采用平静的语音播报和舒缓的环境音效。”
- “为普通听众制作一期关于量子计算技术的科普播客。”

---

### 安全性

所有与ElevenLabs相关的API密钥都存储在服务器端，技能文件中不包含任何敏感信息。该系统通过了VirusTotal和ClawHub的安全检测。如需查看完整的后端源代码，请访问[GitHub仓库](https://github.com/wells1137/audiomind-backend)。

---

### 更新记录

**v3.1.0**：简化安装流程，公共共享后端成为默认选项。免费用户无需设置`AUDIOMIND_BACKEND_URL`。
**v3.0.1**：新增`openclaw.requires`元数据以明确环境变量和可信网络端点的设置，解决了OpenClaw安全扫描的警告问题。
**v3.0.0**：全面重构系统架构，所有商业逻辑移至Vercel后端处理，ElevenLabs的API密钥仅存储在服务器端，确保了系统的安全性。
---
name: audiomind
version: 3.3.0
description: 只需一个命令，就能将任何想法转化为成品播客。AudioMind 支持 ElevenLabs 的语音播报（超过 29 种不同声音）、AI 背景音乐以及服务器端的音频混音功能——所有这些操作都通过一个安全的后端平台完成。免费版本可供使用，无需任何设置。
metadata:
  openclaw:
    optional_env:
      - AUDIOMIND_BACKEND_URL
      - AUDIOMIND_API_KEY
      - FAL_KEY
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

AudioMind 可以将一条简单的文本转化为一个制作精良的播客。它涵盖了脚本编写、ElevenLabs 提供的语音播报、人工智能生成的背景音乐以及服务器端的音频混音功能——所有这些操作都只需通过一个 `Manus` 命令即可完成。

**无需任何设置。** 公共共享的后端服务可立即使用，只需安装后即可开始使用。

---

### 快速入门

**安装：**
```
clawhub install audiomind
```

**立即使用（无需配置）：**
> “使用 AudioMind 制作一档关于人工智能发展未来的 3 分钟播客。”

就这么简单。AudioMind 默认使用公共共享的后端服务，每月可免费生成 20 个播客版本，无需 API 密钥。

---

### 配置

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `AUDIOMIND_BACKEND_URL` | 可选 | 你自己的 Vercel 后端服务地址。默认使用公共共享后端。 |
| `AUDIOMIND_API_KEY` | 可选 | 专业版 API 密钥，可无限次生成播客版本。可在官网获取。 |

**免费版（默认）：** 每月基于 IP 地址生成 20 个播客版本，无需任何配置。

**专业版：** 设置 `AUDIOMIND_API_KEY` 以获得无限使用权限。

**自托管：** 你可以从 [github.com/wells1137/audiomind-backend](https://github.com/wells1137/audiomind-backend) 下载并部署自己的后端服务，然后将 `AUDIOMIND_BACKEND_URL` 设置为你的后端地址。

---

### 工作原理

当你通过 `Manus` 命令请求制作播客时，系统会自动执行以下步骤：

1. **编写脚本**：AI 模型会根据你的主题和所需时长自动生成结构化的播客脚本。
2. **生成语音播报**：通过 `POST {BACKEND_URL}/api/workflow/generate_tts` 发送脚本，系统会使用 ElevenLabs 的语音服务生成 MP3 格式的语音文件。
3. **生成背景音乐**：通过 `POST {BACKEND_URL}/api/workflow/generate_music` 提供音乐风格或情绪提示，系统会生成相应的背景音乐 MP3 文件。
4. **上传音频文件**：系统使用 `manus-upload-file` 命令上传生成的音频文件，并获取它们的公共 URL 以进行后续的混音操作。
5. **混音**：通过 `POST {BACKEND_URL}/api/workflow/mix_audio` 将语音和背景音乐文件上传到后端，后端会使用 `ffmpeg` 工具进行混音处理，最终生成完整的播客 MP3 文件。
6. **交付结果**：系统会将制作完成的播客文件保存并呈现给你。

---

### 示例指令

- “制作一档时长 5 分钟的爵士乐历史播客，背景音乐采用柔和的爵士乐风格。”
- “制作一档每日新闻播报，内容关于人工智能的发展，采用正式的语气，开头音乐需充满活力。”
- “制作一档 10 分钟的冥想播客，使用平静的语音播报和舒缓的环境音效。”
- “为普通观众制作一档关于量子计算技术的科普播客。”

---

### 安全性

所有 ElevenLabs 提供的 API 密钥都存储在服务器端，技能文件中不包含任何敏感信息。该系统通过了 VirusTotal 和 ClawHub 的安全检测。如需查看完整的后端源代码，请访问 [GitHub 仓库](https://github.com/wells1137/audiomind-backend)。

---

### 更新日志

**v3.3.0**：完全移除了本地的 `tools/start_server.sh` 脚本（在 v3 架构中不再需要）。将 `FAL_KEY` 定义为可选环境变量，解决了所有与 OpenClaw 元数据相关的兼容性问题。
**v3.1.0**：实现了无需任何配置的安装流程，公共共享后端成为默认选项，免费用户无需设置 `AUDIOMIND_BACKEND_URL`。
**v3.0.1**：添加了 `openclaw.requires` 元数据以明确指定所需的环境变量和可信网络地址，解决了 OpenClaw 安全扫描工具的警告问题。
**v3.0.0**：对整个系统架构进行了全面重构，所有商业逻辑都移至 Vercel 后端处理，ElevenLabs 的 API 密钥仅存储在服务器端，确保了系统的安全性。
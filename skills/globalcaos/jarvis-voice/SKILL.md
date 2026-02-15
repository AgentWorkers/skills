---
name: jarvis-voice
version: 1.0.0
description: "为您的 OpenClaw 代理赋予“语音”功能——采用 JARVIS 风格的金属质感文本到语音（TTS）技术，并结合 sherpa-onnx 工具实现完全离线运行（无需依赖云端服务）。在网页聊天中，语音转录内容会以紫色斜体字显示。同时支持自定义语音效果，如“镶边效果”（flanger）、“回声效果”（echo）以及“音高调整”（pitch shift）。该功能优先使用本地资源，无需支付任何 API 费用，且延迟为零。"
homepage: https://github.com/globalcaos/clawdbot-moltbot-openclaw
repository: https://github.com/globalcaos/clawdbot-moltbot-openclaw
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["ffmpeg", "aplay"]
    install:
      - id: sherpa-onnx
        kind: manual
        label: "Install sherpa-onnx TTS (see docs)"
---

# Jarvis 语音角色

这是一个专为 OpenClaw 助手设计的金属质感 AI 语音，支持文本转语音（TTS）功能，并具有视觉化的文字转录效果。

## 主要特性

- **TTS 输出：** 通过 `sherpa-onnx` 实现本地语音合成（无需使用云 API）
- **金属质感声音：** 使用 `ffmpeg` 对音频进行处理，以模拟机器人的发音效果
- **紫色文字转录：** 通过颜色区分语音内容和文本内容
- **快速播放：** 播放速度可提高 2 倍，提升沟通效率

## 系统要求

- 需要安装 `sherpa-onnx`，并使用 VITS piper 模型（推荐使用 `en_GB-alan-medium` 语言设置）
- 需要 `ffmpeg` 用于音频处理
- 需要 `aplay`（基于 ALSA 的音频播放工具）

## 安装步骤

### 1. 安装 `sherpa-onnx` TTS 工具

```bash
# Download and extract sherpa-onnx
mkdir -p ~/.openclaw/tools/sherpa-onnx-tts
cd ~/.openclaw/tools/sherpa-onnx-tts
# Follow sherpa-onnx installation guide
```

### 2. 安装 `jarvis` 脚本

```bash
cp {baseDir}/scripts/jarvis ~/.local/bin/jarvis
chmod +x ~/.local/bin/jarvis
```

### 3. 配置音频设备

编辑 `~/.local/bin/jarvis` 文件，在 `aplay -D` 参数中设置您的音频输出设备。

## 使用方法

### 语音合成

```bash
jarvis "Hello, I am your AI assistant."
```

### 在助手响应中使用

请将以下代码添加到您的 `SOUL.md` 文件中：

```markdown
## Communication Protocol

- **Hybrid Output:** Every response includes text + spoken audio via `jarvis` command
- **Transcript Format:** **Jarvis:** <span class="jarvis-voice">spoken text</span>
- **No gibberish:** Never spell out IDs or hashes when speaking
```

### 文本转录样式（需依赖前端界面支持）

请将以下 CSS 代码添加到您的网页聊天界面中：

```css
.jarvis-voice {
  color: #9B59B6;
  font-style: italic;
}
```

同时，请确保 Markdown 编辑器允许使用 `span` 标签。

## 语音自定义

通过编辑 `~/.local/bin/jarvis` 文件来调整语音效果：

| 参数          | 效果                |
|---------------|-------------------|
| `--vits-length-scale=0.5` | 调整语音播放速度（数值越小，速度越快） |
| `aecho`         | 控制声音的回声效果         |
| `chorus`         | 调整声音的厚度/失真程度       |
| `highpass/lowpass`     | 设置音频的频率范围        |
| `treble=g=3`       | 增加声音的金属质感         |

### 预设设置

- **更机械化的声音：** [配置示例] ```
aecho=0.7:0.7:5|10|15:0.4|0.35|0.3
```
- **更接近人类的声音：** [配置示例] ```
aecho=0.4:0.4:20:0.2
```
- **更低沉的声音：** [配置示例] ```
highpass=f=200,lowpass=f=3000
```

## 常见问题解决方法

### 无音频输出
- 使用 `aplay -l` 命令查看可用的音频设备
- 更新 `-D plughw:X,Y` 参数以指定正确的音频设备

### 语音速度过快/过慢
- 调整 `--vits-length-scale` 参数（0.3 表示非常快，1.0 表示正常速度）

### 金属质感效果过强
- 减少回声延迟和声音的失真程度

## 相关文件

- `scripts/jarvis`：包含语音合成功能的脚本
- `SKILL.md`：本文档文件

---

*这是一个专为那些希望自己的助手既能被“听到”也能被“阅读”的用户设计的语音角色。*
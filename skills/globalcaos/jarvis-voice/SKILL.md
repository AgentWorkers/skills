---
name: jarvis-voice
version: 1.0.0
description: 具有文本转语音（TTS）功能的金属质感AI语音角色，以及视觉文本转录样式。该角色会以类似JARVIS的机器人语音朗读回答内容，并将文本转录结果以紫色斜体字体显示出来。
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/openclaw/openclaw
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

这是一个专为 OpenClaw 辅助工具设计的金属质感 AI 语音，配有视觉化的文字转录功能。

## 功能特点

- **TTS 输出：** 通过 `sherpa-onnx` 实现本地语音合成（无需使用云 API）
- **金属质感声音：** 使用 `ffmpeg` 对音频进行处理，以模拟机器人的发音效果
- **紫色文字转录：** 用于区分语音内容和文字内容
- **快速播放：** 播放速度提升 2 倍，提升沟通效率

## 系统要求

- 需要安装 `sherpa-onnx`，并使用 VITS piper 模型（推荐使用 `en_GB-alan-medium` 配置）
- 需要 `ffmpeg` 用于音频处理
- 需要 `aplay`（基于 ALSA）软件用于音频播放

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

### 语音输入

```bash
jarvis "Hello, I am your AI assistant."
```

### 在辅助工具的响应中使用

将相关代码添加到您的 `SOUL.md` 文件中：

```markdown
## Communication Protocol

- **Hybrid Output:** Every response includes text + spoken audio via `jarvis` command
- **Transcript Format:** **Jarvis:** <span class="jarvis-voice">spoken text</span>
- **No gibberish:** Never spell out IDs or hashes when speaking
```

### 文本转录样式（需要前端界面支持）

将相关 CSS 代码添加到您的网页聊天界面中：

```css
.jarvis-voice {
  color: #9B59B6;
  font-style: italic;
}
```

同时，请确保 Markdown 格式中允许使用 `span` 标签。

## 语音自定义

编辑 `~/.local/bin/jarvis` 文件以调整语音效果：

| 参数 | 效果 |
|-----------|--------|
| `--vits-length-scale=0.5` | 改变语音播放速度（数值越小，速度越快） |
| `aecho` | 调整回声效果，增强金属质感 |
| `chorus` | 调整声音的厚度或失真程度 |
| `highpass/lowpass` | 设置音频的频率范围 |
| `treble=g=3` | 增强声音的金属光泽感 |

### 预设设置

- **更机械的语音风格：**
```
aecho=0.7:0.7:5|10|15:0.4|0.35|0.3
```

- **更接近人类的语音风格：**
```
aecho=0.4:0.4:20:0.2
```

- **更低沉的语音风格：**
```
highpass=f=200,lowpass=f=3000
```

## 常见问题解决方法

### 无音频输出
- 使用 `aplay -l` 命令检查可用的音频设备
- 更新 `-D plughw:X,Y` 参数以指定正确的音频设备

### 语音速度过快/过慢
- 调整 `--vits-length-scale` 参数（0.3 表示非常快，1.0 表示正常速度）

### 金属质感效果过强
- 减少回声延迟和声音的失真程度

## 相关文件

- `scripts/jarvis`：包含金属质感处理功能的 TTS 脚本
- `SKILL.md`：本文档文件

---

*这是一个专为那些既希望被听到声音又希望看到文字内容的辅助工具设计的语音角色。*
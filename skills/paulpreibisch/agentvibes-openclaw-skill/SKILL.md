---
slug: agentvibes-openclaw-skill
name: Agent Vibes OpenClaw Skill
description: 免费提供专业的文本转语音服务，支持通过无语音服务器将文本转换为语音，适用于 Linux、macOS 或 Android 设备。提供 50 多种语言、30 多种语音选项。支持两种部署架构：  
1. 服务器端文本转语音（使用 PulseAudio 进行音频流传输）；  
2. 高效的文本流传输方式（在接收端生成语音），推荐使用这种方式。  
非常适合用于 SSH 会话、远程 AI 代理以及多设备文本转语音应用。
---

# 🎤 AgentVibes 语音管理

您可以管理来自多个提供者（Piper TTS、Piper、macOS Say）的文本转语音（TTS）功能。

---

## 可用命令

### 语音控制

#### /agent-vibes:mute
静音所有 TTS 输出（会持续到会话结束）

- 设置静音标志，关闭所有语音输出
- 当 TTS 应该播放时，会显示 🔇 图标

```bash
/agent-vibes:mute
```

#### /agent-vibes:unmute
取消静音

- 移除静音标志，恢复语音输出

```bash
/agent-vibes:unmute
```

#### /agent-vibes:list [first|last] [N]
列出所有可用的语音，支持可选过滤

```bash
/agent-vibes:list                    # Show all voices
/agent-vibes:list first 5            # Show first 5 voices
/agent-vibes:list last 3             # Show last 3 voices
```

#### /agent-vibes:preview [first|last] [N]
通过播放音频样本来预览语音

```bash
/agent-vibes:preview                 # Preview first 3 voices
/agent-vibes:preview 5               # Preview first 5 voices
/agent-vibes:preview last 5          # Preview last 5 voices
```

#### /agent-vibes:switch <voice_name>
切换到不同的默认语音

```bash
/agent-vibes:switch en_US-amy-medium
/agent-vibes:switch en_GB-alan-medium
/agent-vibes:switch fr_FR-siwis-medium
```

#### /agent-vibes:get
显示当前选定的语音

```bash
/agent-vibes:get
```

#### /agent-vibes:add <name> <voice_id>
从您的 Piper TTS 账户中添加新的自定义语音

```bash
/agent-vibes:add "My Voice" abc123xyz456
```

请参阅下面的 [获取语音 ID](#getting-voice-ids-piper-tts) 部分。

#### /agent-vibes:replay [N]
重放最近播放的 TTS 音频

```bash
/agent-vibes:replay                  # Replay last audio
/agent-vibes:replay 1                # Replay most recent
/agent-vibes:replay 2                # Replay second-to-last
/agent-vibes:replay 3                # Replay third-to-last
```

系统会保留最近 10 个音频文件。

#### /agent-vibes:set-pretext <word>
为所有 TTS 消息设置前缀文字/短语

```bash
/agent-vibes:set-pretext AgentVibes  # All TTS starts with "AgentVibes:"
/agent-vibes:set-pretext "Project Alpha" # Custom phrase
/agent-vibes:set-pretext ""          # Clear pretext
```

配置文件保存在 `.agentvibes/config/agentvibes.json` 中

---

## 提供者管理

#### /agent-vibes:provider list
显示所有可用的 TTS 提供者

```bash
/agent-vibes:provider list
```

#### /agent-vibes:provider switch <name>
在提供者之间切换

```bash
/agent-vibes:provider switch piper    # Piper TTS - Free, offline, 50+ voices
/agent-vibes:provider switch macos    # macOS Say - Native macOS voices (Mac only)
```

#### /agent-vibes:provider info <name>
获取特定提供者的详细信息

```bash
/agent-vibes:provider info piper
/agent-vibes:provider info macos
```

---

## 提供者列表

| 提供者 | 平台 | 费用 | 语音数量 | 语音质量 |
|----------|----------|------|--------|---------|
| **Piper TTS** | 所有平台（Linux、macOS、WSL） | 免费 | 50 多种语言，30 多种语音 | ⭐⭐⭐⭐ |
| **macOS Say** | 仅限 macOS | 免费（内置） | 100 多种系统语音 | ⭐⭐⭐⭐ |

**在 macOS 上**，会自动检测并推荐内置的 `say` 提供者！

---

## 获取语音 ID（Piper TTS）

要添加自己的自定义 Piper TTS 语音，请按照以下步骤操作：

1. 访问 https://piper.io/app/voice-library
2. 选择或创建一个语音
3. 复制语音 ID（15-30 个字符的字母数字字符串）
4. 使用 `/agent-vibes:add` 命令添加该语音：

```bash
/agent-vibes:add "My Custom Voice" xyz789abc123def456
```

---

## 默认语音

### Piper TTS（免费且离线）

**英语（美国）：**
- en_US-lessac-medium（默认男性语音）
- en_US-amy-medium（友好女性语音）
- en_US-ryan-high（高质量男性语音）
- en_US-libritts-high（多种发音风格）

**英语（英国）：**
- en_GB-alan-medium（英国男性语音）
- en_GB-jenny_dioco-medium（英国女性语音）

**罗曼语系语言：**
- es_ES-davefx-medium（西班牙语 - 西班牙）
- es_MX-claude-high（西班牙语 - 墨西哥）
- fr_FR-siwis-medium（法语女性）
- fr_FR-gilles-low（法语男性）
- it_IT-riccardo-x-low（意大利语男性）
- pt_BR-faber-medium（葡萄牙语 - 巴西）

**日耳曼语系语言：**
- de_DE-thorsten-medium（德语男性）
- de_DE-eva_k-x-low（德语女性）

**亚洲语言：**
- ja_JP-ayanami-medium（日语女性）
- zh_CN-huayan-x-low（中文女性）
- ko_KR-kss-medium（韩语女性）

### macOS Say（内置 100 多种语音）
- Samantha
- Alex
- Daniel
- Victoria
- Karen
- Moira
- 以及更多系统语音

---

## 快速示例

### 切换到不同的语音
```bash
/agent-vibes:switch en_US-lessac-medium    # Clear male voice
/agent-vibes:switch en_US-ryan-high        # High quality male
/agent-vibes:switch en_GB-alan-medium      # British male
```

### 选择前预览
```bash
/agent-vibes:preview 5                     # Preview first 5 voices
/agent-vibes:preview last 3                # Preview last 3 voices
```

### 添加自定义 Piper 语音
```bash
/agent-vibes:add "My Voice" abc123xyz456
/agent-vibes:switch My Voice
```

### 切换提供者
```bash
/agent-vibes:provider switch macos    # Use native macOS voices
/agent-vibes:provider switch piper    # Switch back to Piper
```

### 静音/取消静音
```bash
/agent-vibes:mute                     # Silent mode
/agent-vibes:unmute                   # Restore voice
```

---

## 小贴士与技巧

- **先预览**：在切换新语音之前，务必使用 `/agent-vibes:preview` 命令预览。
- **提供者选择**：某些语音仅适用于特定的提供者。
- **语音历史**：使用 `/agent-vibes:replay` 命令回放最近的 10 条 TTS 消息。
- **自定义前缀**：为所有 TTS 消息设置统一的前缀（例如：“AgentVibes:”）。
- **集中注意力时静音**：在需要专注的工作期间，使用 `/agent-vibes:mute` 命令静音。

祝您使用 AgentVibes 的 TTS 体验愉快！🎵
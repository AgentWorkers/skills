---
name: Her Voice
description: "为您的代理程序添加语音功能。当用户希望代理程序能够说话、朗读内容或提供语音响应时，可以使用此功能。"
metadata:
  openclaw:
    emoji: "🎙️"
    requires:
      bins: ["python3", "espeak-ng"]
---
# Her Voice 🎙️

**为您的助手赋予语音**。该功能通过Kokoro TTS提供音频响应——这是一个紧凑型、表达力丰富的模型，完全在设备上运行。

### ✨ 主要特性

得益于即时音频流技术，响应时间得到了极大优化。完全免费，无需API密钥。灵感来源于Samantha和Sky模型。

- **⚡ 即时流媒体**——音频在生成的同时立即播放，延迟极低
- **👄 天使般的声音**——采用先进的本地文本转语音（TTS）技术Kokoro TTS
- **🧠 TTS守护进程**——将模型保持在RAM中以快速响应（可关闭以节省RAM）
- **🖥️ 持久化模式**——支持拖放音频文件、粘贴文本，或将其作为独立的语音工具使用
- **🔧 完全可配置**——支持语音、语速、可视化效果以及通知音效
- **🍎 MLX + PyTorch**——在Apple Silicon上使用原生Metal加速；在其他平台上使用PyTorch
- **🎨 实时可视化效果**——带有60帧每秒（60fps）动画效果的LED条，会根据语音实时变化（仅限macOS）

## 首次运行设置

```bash
python3 SKILL_DIR/scripts/setup.py
```

> **注意：** `SKILL_DIR` 是该功能的根目录——运行命令时系统会自动识别该目录。

设置向导将：
1. 检测平台并选择TTS引擎（Apple Silicon上使用MLX，其他平台使用PyTorch）
2. 查找或安装相应的TTS后端（mlx-audio或kokoro）
3. 安装`espeak-ng`（macOS使用Homebrew，Linux使用apt）
4. 如有需要，修复espeak加载器（确保macOS兼容性）
5. 编译原生可视化效果二进制文件（仅限macOS）
6. 下载Kokoro模型
7. 在`~/.her-voice/config.json`中创建配置文件

随时查看状态：
```bash
python3 SKILL_DIR/scripts/setup.py status
```

### 设置完成后：名称与发音设置

设置完成后，请配置助手和用户的名称：
```bash
python3 SKILL_DIR/scripts/config.py set agent_name "Jackie"
python3 SKILL_DIR/scripts/config.py set user_name "Matúš"
python3 SKILL_DIR/scripts/config.py set user_name_tts "Mah-toosh"
```

**TTS发音提示：** 如果用户的名字不是英文，请确定一个Kokoro能够正确发音的英文拼写，并将其存储在`user_name_tts`中。实际名称仍保存在`user_name`中用于显示。

## 语音输出

```bash
# Basic usage
python3 SKILL_DIR/scripts/speak.py "Hello, world!"

# Skip visualizer for this call
python3 SKILL_DIR/scripts/speak.py --no-viz "Quick note"

# Save to file instead of playing
python3 SKILL_DIR/scripts/speak.py --save /tmp/output.wav "Save this"

# Override voice or speed
python3 SKILL_DIR/scripts/speak.py --voice af_bella --speed 1.2 "Faster!"

# Pipe text from stdin
echo "Piped text" | python3 SKILL_DIR/scripts/speak.py
```

### 命令选项

| 标志 | 描述 |
|------|-------------|
| `--no-viz` | 禁用可视化效果 |
| `--persist` | 播放结束后保持可视化效果开启 |
| `--save PATH` | 将音频保存为WAV文件而非直接播放 |
| `--voice NAME` | 覆盖配置的语音 |
| `--speed N` | 覆盖配置的语速 |
| `--mode MODE` | 覆盖可视化效果模式（`v2`或`classic`）

## 助手工作流程

当用户需要语音响应时：
1. **检查语音模式**——语音功能是否已启用，或者用户是否明确请求了语音响应？
2. **播放通知音效**（在TTS生成语音的同时提供即时反馈）：
   ```bash
   afplay /System/Library/Sounds/Blow.aiff &
   ```
3. **输出语音内容**：
   ```bash
   python3 SKILL_DIR/scripts/speak.py "Response text here"
   ```
4. **始终提供文本说明**——确保用户能够理解语音内容。

### 通知音效

通知音效会在TTS生成语音的同时立即播放（约0.1秒）。这能让用户立即知道助手正在响应。

配置信息位于`~/.her-voice/config.json`中：
```json
{
  "notification_sound": {
    "enabled": true,
    "sound": "Blow"
  }
}
```

macOS可用的音效包括：`Blow`、`Bottle`、`Frog`、`Funk`、`Glass`、`Hero`、`Morse`、`Ping`、`Pop`、`Purr`、`Sosumi`、`Submarine`、`Tink`。这些音效文件位于`/System/Library/Sounds/`目录下。

## TTS守护进程

TTS守护进程会将Kokoro模型保持在RAM中，从而每次调用时减少约1.1秒的启动延迟。

该守护进程会自动创建`mlx-audio`虚拟环境（venv）——无需手动查找。

```bash
# Start (persists in background)
nohup python3 SKILL_DIR/scripts/daemon.py start > /tmp/her-voice-daemon.log 2>&1 & disown

# Status
python3 SKILL_DIR/scripts/daemon.py status

# Stop
python3 SKILL_DIR/scripts/daemon.py stop

# Restart
python3 SKILL_DIR/scripts/daemon.py restart
```

`speak.py`会自动检测守护进程的存在；如果守护进程可用，则使用它；否则会直接加载模型。

**守护进程是可选的。** 即使没有守护进程，语音功能仍然可用，只是每次调用时模型加载会稍慢约1秒。关闭守护进程可以节省约2.3GB的RAM。

**注意：** 守护进程会在模型加载完成并准备好接受连接后，生成PID文件和socket文件。这些文件位于`~/.her-voice/`目录中，具有受限权限（仅所有者可访问）。重启系统后需要重新启动守护进程。

## 可视化效果

一个带有三个动画LED条的浮动界面，会根据语音实时变化。仅支持macOS系统（使用Cocoa和AVFoundation实现）。**其他平台**上仅播放音频，不显示可视化效果。

### 可视化效果模式
- **v2**（默认）——三层红色条状图，中间显示原始音量，两侧显示延迟值
- **classic**——原始的平滑渐变效果

### 控制键
| 键 | 功能 |
|-----|--------|
| ESC | 退出 |
| Space | 暂停/继续（文件模式下） |
| ← → | 前后切换5秒范围的音频片段（文件模式下） |
| ⌘V | 粘贴文本以进行语音播放（持久化模式下） |

### 持久化模式

在播放结束后，可视化效果会保持显示。可以将其作为独立的语音工具使用：
```bash
# Launch in persist mode (stays open, idle breathing animation)
~/.her-voice/bin/her-voice-viz --persist

# Stream mode + persist (stays open after speech ends)
python3 SKILL_DIR/scripts/speak.py --persist "Hello!"
```

在持久化模式下：
- **拖放**音频文件（.wav、.mp3、.aiff、.m4a）到可视化界面上进行播放
- **⌘V** 粘贴剪贴板中的文本 → 通过TTS守护进程直接播放，并显示完整的可视化效果
- **空闲状态**——在等待输入时，中间条会轻微闪烁

### 独立使用

```bash
# Play a file with visualizer
~/.her-voice/bin/her-voice-viz --audio /path/to/file.wav

# Demo mode (simulated audio)
~/.her-voice/bin/her-voice-viz --demo

# Stream raw PCM
cat audio.raw | ~/.her-voice/bin/her-voice-viz --stream --sample-rate 24000
```

### 禁用可视化效果

```bash
python3 SKILL_DIR/scripts/config.py set visualizer.enabled false
```

## 配置文件

配置文件：`~/.her-voice/config.json`

```bash
# View all settings
python3 SKILL_DIR/scripts/config.py status

# Get a value
python3 SKILL_DIR/scripts/config.py get voice

# Set a value (dot notation for nested keys)
python3 SKILL_DIR/scripts/config.py set speed 1.1
python3 SKILL_DIR/scripts/config.py set visualizer.mode classic
```

### 主要配置项

| 设置 | 默认值 | 描述 |
|-----|---------|-------------|
| `agent_name` | `""` | 助手名称（例如："Jackie"） |
| `user_name` | `""` | 用户的真实名称 |
| `user_name_tts` | `""` | 用于TTS的发音拼写（例如："Mah-toosh"代表Matúš） |
| `voice` | `af_heart` | 基础语音名称 |
| `voice_blend` | `{af_heart: 0.6, af_sky: 0.4}` | 语音混合比例 |
| `speed` | `1.05` | 语音速度倍数值 |
| `language` | `en` | 语言代码 |
| `tts_engine` | `auto` | TTS引擎（`auto`、`mlx`或`pytorch`） |
| `model` | `mlx-community/Kokoro-82M-bf16` | 模型标识符（MLX） |
| `visualizer.enabled` | `true` | 是否显示可视化效果 |
| `visualizer.mode` | `v2` | 可视化效果模式（`v2`或`classic`） |
| `visualizer.remember_position` | `true` | 保存会话间的窗口位置 |
| `notification_sound.enabled` | `true` | 播放语音前是否播放通知音效 |
| `notification_sound.sound` | `Blow` | macOS系统音效名称 |
| `daemon.auto_start` | `true` | 建议性设置——守护进程不会自动启动。设置为`true`时，助手会在首次使用语音功能时自动启动守护进程（每次调用可节省约1秒，但会占用约2.3GB RAM） |
| `daemon.socket_path` | `~/.her-voice/tts.sock` | Unix socket路径 |

## 语音选择

### 语音混合

通过配置`voice_blend`来混合多种语音以获得独特的声音效果：
```json
{
  "voice_blend": {"af_heart": 0.6, "af_sky": 0.4}
}
```

混合后的语音会保存为`.safetensors`文件，存储在模型的voices目录中（例如：`af_heart_60_af_sky_40.safetensors`）。只需运行一次TTS命令即可生成该文件——`speak.py`会自动查找已预混合的文件。

## 错误处理

| 错误 | 原因 | 解决方法 |
|-------|-------|-----|
| "mlx-audio not found" | 未找到或缺失venv | 运行`setup.py` |
| "espeak-ng not found" | 未找到phonemizer | 使用`brew install espeak-ng`安装 |
| 编译失败 | 未安装Xcode工具 | 运行`xcode-select --install` |
| "Model not found" | 首次运行时未下载模型 | 运行`setup.py`或尝试播放一次 |
| 守护进程“未运行” | 守护进程崩溃或重启 | 重新启动守护进程 |
| 无声音输出 | macOS音频权限问题 | 检查系统设置→声音→输出设置 |
| 可视化效果未显示 | 可视化效果二进制文件未编译 | 运行`setup.py` |
| "kokoro not found" | 未找到PyTorch虚拟环境 | 运行`setup.py` |
| PyTorch CUDA错误 | GPU驱动程序不匹配 | 在kokoro虚拟环境中运行`pip install torch --force-reinstall` |
| "soundfile not found" | 缺少依赖库 | 在kokoro虚拟环境中运行`pip install soundfile` |

## 系统要求

- **推荐使用macOS + Apple Silicon**以获得最佳体验（支持MLX引擎、可视化效果和通知音效）
- **Linux/Intel Mac**通过PyTorch Kokoro引擎支持（不支持可视化效果）
- **Windows**不支持该功能 |
- macOS上需要安装Xcode命令行工具（`xcode-select --install`）
- 需要`espeak-ng`进行音素化处理（macOS使用Homebrew安装，Linux使用apt安装）
- 硬盘空间至少500MB（用于存储模型和虚拟环境）
- 运行守护进程时需要约2.3GB的RAM

## 卸载

请删除所有与Her Voice相关的数据（配置文件、虚拟环境、编译后的二进制文件以及守护进程状态）：
```bash
python3 SKILL_DIR/scripts/daemon.py stop
rm -rf ~/.her-voice
```

## 工作原理

1. **Kokoro 82M**——这是一个高效的神经网络TTS模型，支持两种后端：**MLX**（Apple Silicon上的原生Metal GPU加速）和**PyTorch**（适用于所有平台）。根据平台自动选择合适的后端；也可以通过`tts_engine`配置选项手动指定（`auto`、`mlx`或`pytorch`）
2. **流媒体播放**——音频生成和播放同时进行。使用守护进程时，首次语音输出时间约为0.3秒；不使用守护进程时，批量处理时间约为3秒
3. **可视化效果**——基于macOS原生技术的应用程序（Swift/Cocoa），从标准输入（stdin）读取原始PCM音频，并通过AVAudioEngine实时显示音量变化
4. **守护进程**——作为Unix socket服务器，将模型保持在RAM中，从而避免每次调用时的Python导入和模型加载开销
---
name: local-voice
description: 在 Apple Silicon 平台上，可以使用 FluidAudio 实现本地文本转语音（TTS）和语音转文本（STT）功能。语音合成与转录过程可在设备上通过 Apple Neural Engine 完成，耗时不到一秒。该技术适用于配置本地语音功能、集成语音助手，或替代云端的 TTS/STT 服务。
---

# 本地语音服务（FluidAudio TTS/STT）

专为使用 Apple Silicon 处理器的 Mac 设计的本地语音 AI 服务，支持 TTS（文本转语音）和 STT（语音转文本）功能，响应时间低于 0.1 秒。

## 主要特性

- **TTS（文本转语音）**：采用 FluidAudio 的 CoreML 模型，提供 54 种语音选项，延迟约 0.6–0.8 秒。
- **STT（语音转文本）**：使用 Parakeet TDT v3 技术，延迟约 0.2–0.3 秒，支持 25 种语言。
- **100% 本地化**：无需依赖云端服务，完全本地运行，无额外费用。
- **高效性能**：利用 Apple 的 ANE（Apple Neural Engine）提升运行效率。

## 系统要求

- macOS 14 及更高版本，运行在 Apple Silicon（M1/M2/M3/M4）架构上。
- Swift 5.9 或更高版本。
- 需要安装 espeak-ng 库（作为 TTS 功能的备用方案）。

## 快速安装流程

### 1. 安装依赖库
```bash
brew install espeak-ng
```

### 2. 构建后台服务程序（Daemon）
```bash
cd /path/to/skill/sources
swift build -c release
```

### 3. 安装二进制文件及相关框架
```bash
mkdir -p ~/clawd/bin
cp .build/release/StellaVoice ~/clawd/bin/
cp -R .build/arm64-apple-macosx/release/ESpeakNG.framework ~/clawd/bin/
install_name_tool -add_rpath @executable_path ~/clawd/bin/StellaVoice
```

### 4. 创建启动代理（LaunchAgent）
```bash
cat > ~/Library/LaunchAgents/com.stella.tts.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.stella.tts</string>
    <key>ProgramArguments</key>
    <array>
        <string>$HOME/clawd/bin/StellaVoice</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/.clawdbot/logs/stella-tts.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/.clawdbot/logs/stella-tts.err.log</string>
</dict>
</plist>
EOF

launchctl load ~/Library/LaunchAgents/com.stella.tts.plist
```

## API 接口

后台服务程序监听 `http://127.0.0.1:18790` 端口：

- **TTS 接口**：用于将文本转换为语音。
  ```bash
# Simple text to WAV
curl -X POST http://127.0.0.1:18790/synthesize -d "Hello world" -o output.wav

# With speed control (0.5-2.0)
curl -X POST "http://127.0.0.1:18790/synthesize?speed=1.2" -d "Fast!" -o output.wav

# JSON endpoint
curl -X POST http://127.0.0.1:18790/synthesize/json \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello", "speed": 1.0, "deEss": true}'
```

- **STT 接口**：用于将语音转换为文本。
  ```bash
curl -X POST http://127.0.0.1:18790/transcribe \
  --data-binary @audio.wav \
  -H "Content-Type: audio/wav"
# Returns: {"text": "transcribed text"}
```

- **健康检查接口**：用于监控服务运行状态。
  ```bash
curl http://127.0.0.1:18790/health
# Returns: ok
```

## 语音设置

默认语音为 `af_sky`，可通过修改源代码进行自定义。

**部分热门的 Kokoro 语音选项（美国女性声道）：**
- `af_heart`（A 级）：温暖、自然
- `af_bella`（A- 级）：表现力强
- `af_sky`（C- 级）：清晰、轻柔

**全部 54 种语音选项**：详见 `REFERENCES/VOICES.md` 文件。

## 语音效果调节

- **语速控制**：
  - `speed=0.8`：平静、舒缓的语速
  - `speed=1.0`：自然的语速
  - `speed=1.2`：充满活力、明快的语速

- **标点符号处理**：
  - `!`：表示兴奋的语气
  - `?`：表示疑问的语气
  - `.`：中性、平淡的语气
  - `...`：表示停顿

- **SSML 标签支持**：用于更精细的语音控制。
  ```
<phoneme ph="kəkˈɔɹO">Kokoro</phoneme>
<sub alias="Doctor">Dr.</sub>
<say-as interpret-as="date">2024-01-15</say-as>
```

## 辅助脚本

可使用 `scripts/stella-tts.sh` 脚本简化程序的使用。

## 集成示例

若需要将此服务集成到语音助手中，请更新语音代理配置以使用本地 API 接口。

## 常见问题解决方法

- **库未加载（ESpeakNG）**：
  确保 ESpeakNG.framework 与二进制文件位于同一目录下。
  运行 `install_name_tool -add_rpath @executable_path /path/to/binary` 命令进行配置。

- **首次请求响应缓慢**：
  首次请求时需要加载模型（约 8–10 秒），后续请求的响应时间将缩短至低于 0.1 秒。

- **x86 与 ARM 架构的区别**：
  该服务必须针对 ARM64 架构进行重新编译和运行（不能使用 Rosetta 转换工具）。
  通过 `uname -m` 命令确认系统架构（应显示 `arm64`）。

## 源代码

后台服务程序的源代码位于 `sources/` 目录中。该项目使用以下技术组件：
- FluidAudio（提供 TTS 和 STT 模型）
- Hummingbird（用于构建 HTTP 服务器）

修改代码后请重新编译项目：
```bash
cd sources && swift build -c release
```
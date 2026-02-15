---
name: edge-tts
description: |
  Text-to-speech conversion using node-edge-tts npm package for generating audio from text.
  Supports multiple voices, languages, speed adjustment, pitch control, and subtitle generation.
  Use when: (1) User requests audio/voice output with the "tts" trigger or keyword. (2) Content needs to be spoken rather than read (multitasking, accessibility, driving, cooking). (3) User wants a specific voice, speed, pitch, or format for TTS output.
---

# Edge-TTS 技能

## 概述

通过 `node-edge-tts` npm 包，利用 Microsoft Edge 的神经网络 TTS（文本转语音）服务生成高质量的语音文件。支持多种语言、多种语音选项，以及可调节的语速和音调，并支持字幕生成功能。

## 快速入门

当从用户触发器或请求中检测到 TTS 意图时：

1. **调用 TTS 工具**（Clawdbot 内置）将文本转换为语音。
2. 该工具返回一个 `MEDIA:` 路径。
3. Clawdbot 将音频发送到当前频道。

```javascript
// Example: Built-in tts tool usage
tts("Your text to convert to speech")
// Returns: MEDIA: /path/to/audio.mp3
```

## 触发器检测

识别 “tts” 关键字作为 TTS 请求。该技能会在转换文本之前自动过滤掉与 TTS 相关的关键词，以避免将触发词本身转换为音频。

## 高级定制

### 使用 Node.js 脚本

如需更多控制，可以直接使用随附的脚本：

#### TTS 转换器
```bash
cd scripts
npm install
node tts-converter.js "Your text" --voice en-US-AriaNeural --rate +10% --output output.mp3
```

**选项：**
- `--voice, -v`：语音名称（默认：en-US-AriaNeural）
- `--lang, -l`：语言代码（例如：en-US, es-ES）
- `--format, -o`：输出格式（默认：audio-24khz-48kbitrate-mono-mp3）
- `--pitch`：音调调整（例如：+10%, -20%，默认）
- `--rate, -r`：语速调整（例如：+10%, -20%，默认）
- `--volume`：音量调整（例如：+0%, -10%，默认）
- `--save-subtitles, -s`：将字幕保存为 JSON 文件
- `--output, -f`：输出文件路径（默认：tts_output.mp3）
- `--proxy, -p`：代理 URL（例如：http://localhost:7890）
- `--timeout`：请求超时时间（以毫秒为单位，默认：10000）
- `--list-voices, -L`：列出可用的语音

#### 配置管理器
```bash
cd scripts
npm install
node config-manager.js --set-voice en-US-AriaNeural

node config-manager.js --set-rate +10%

node config-manager.js --get

node config-manager.js --reset
```

### 语音选择

常用语音（使用 `--list-voices` 查看完整列表）：

**英语：**
- `en-US-MichelleNeural`（女性，自然音色，**默认**）
- `en-US-AriaNeural`（女性，自然音色）
- `en-US-GuyNeural`（男性，自然音色）
- `en-GB-SoniaNeural`（女性，英式发音）
- `en-GB-RyanNeural`（男性，英式发音）

**其他语言：**
- `es-ES-ElviraNeural`（西班牙语，西班牙）
- `fr-FR-DeniseNeural`（法语）
- `de-DE-KatjaNeural`（德语）
- `ja-JP-NanamiNeural`（日语）
- `zh-CN-XiaoxiaoNeural`（中文）
- `ar-SA-ZariyahNeural`（阿拉伯语）

### 语速指南

语速值使用百分比表示：
- `"default"`：正常速度
- `"-20%"` 至 `"-10%"`：较慢，适合讲解、阅读等场景
- `"+10%"` 至 `"+20%"`：稍快，适合总结等场景
- `"+30%"` 至 `"+50%"`：较快，适合新闻、演讲等场景

### 输出格式

根据使用场景选择音频质量：
- `audio-24khz-48kbitrate-mono-mp3`：标准质量（语音提示、消息）
- `audio-24khz-96kbitrate-mono-mp3`：高质量（演示文稿、内容）
- `audio-48khz-96kbitrate-stereo-mp3`：最高质量（专业音频、音乐）

## 资源

### scripts/tts-converter.js
主要的 TTS 转换脚本，使用 `node-edge-tts` 实现。支持自定义语音、语速、音量、音调和格式，并支持字幕生成。

### scripts/config-manager.js
管理用户的 TTS 设置（语音、语言、格式、音调、语速、音量）。配置信息存储在 `~/.tts-config.json` 文件中。

### scripts/package.json
NPM 包的配置文件，包含 `node-edge-tts` 依赖项。

### references/node_edge_tts_guide.md
`node-edge-tts` npm 包的完整文档，包括：
- 按语言分类的语音列表
- 语调设置（语速、音调、音量）
- 使用示例（命令行和模块）
- 字幕生成
- 输出格式
- 最佳实践和限制

### 语音测试

可以在以下链接测试不同的语音并预览音频质量：https://tts.travisvn.com/

如需特定语音详情或高级功能，请参考此文档。

## 安装

要使用随附的脚本，请执行以下操作：

```bash
cd /home/user/clawd/skills/public/tts-skill/scripts
npm install
```

这将安装：
- `node-edge-tts`：TTS 库
- `commander`：命令行参数解析工具

## 工作流程

1. **检测意图**：检查用户消息中是否包含 “tts” 关键字或触发词。
2. **选择方法**：对于简单请求，使用内置的 `tts` 工具；对于复杂需求，使用 `scripts/tts-converter.js` 进行定制。
3. **生成音频**：将目标文本（消息、搜索结果、摘要等）转换为语音。
4. **返回结果**：TTS 工具返回 `MEDIA:` 路径，由 Clawdbot 负责后续的音频传输。

## 测试

### 基本测试
运行测试脚本以验证 TTS 功能：
```bash
cd /home/user/clawd/skills/public/edge-tts/scripts
npm test
```
该脚本会生成一个测试音频文件，并验证 TTS 服务是否正常工作。

### 语音测试

可以在以下链接测试不同的语音并预览音频质量：https://tts.travisvn.com/

### 集成测试
使用内置的 `tts` 工具进行快速测试：
```javascript
// Example: Test TTS with default settings
tts("This is a test of the TTS functionality.")
```

### 配置测试
验证配置是否能够持久保存：
```bash
cd /home/user/clawd/skills/public/edge-tts/scripts
node config-manager.js --get
node config-manager.js --set-voice en-US-GuyNeural
node config-manager.js --get
```

## 故障排除

- **测试连接**：运行 `npm test` 以检查 TTS 服务是否可用。
- **检查语音可用性**：使用 `node tts-converter.js --list-voices` 查看可用的语音。
- **验证代理设置**：如果使用代理，请使用 `node tts-converter.js "test" --proxy http://localhost:7890` 进行测试。
- **检查音频输出**：测试应生成 `test-output.mp3` 文件，保存在 `scripts` 目录中。

## 注意事项

- `node-edge-tts` 使用 Microsoft Edge 的在线 TTS 服务（服务已更新，支持身份验证）。
- 不需要 API 密钥（免费服务）。
- 输出格式默认为 MP3。
- 需要互联网连接。
- 支持字幕生成（JSON 格式，包含单词级别的时间信息）。
- **临时文件处理**：音频文件默认保存在系统的临时目录中（Unix 系统下为 `/tmp/edge-tts-temp/`，Windows 系统下为 `C:\Users\<user>\AppData\Local\Temp\edge-tts-temp\`），文件名具有唯一性（例如：`tts_1234567890_abc123.mp3`）。文件不会自动删除——调用应用程序（Clawdbot）应在使用后负责清理。如果需要永久存储，可以使用 `--output` 选项指定自定义输出路径。
- **TTS 关键词过滤**：该技能会在转换文本之前自动过滤掉与 TTS 相关的关键词，以避免将触发词本身转换为音频。
- 对于重复的配置设置，可以使用 `config-manager.js` 设置默认值。
- **默认语音**：`en-US-MichelleNeural`（女性，自然音色）。
- “Neural” 结尾的语音通常比标准语音提供更高的音质。
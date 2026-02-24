---
name: strudel-music
description: "使用 Strudel 的实时编码功能来创作、渲染和播放音乐。使用方法如下：  
- `/strudel <prompt>`：输入您想要听到的音乐风格（情绪、场景、类型、使用的乐器等）。  
- `/strudel play <name>`：在 Discord 的视频通话中播放已保存的音乐作品。  
- `/strudel samples`：管理音效样本包。  
- `/strudel list`：显示可用的音乐作品列表。  
可以将其视为 Midjourney 的音乐版本——用于创意音乐生成。"
user-invocable: true
metadata: { "openclaw": { "emoji": "🎵", "requires": { "bins": ["node"], "anyBins": ["ffmpeg"], "env": ["DISCORD_BOT_TOKEN"], "node": ">=18", "description": "Offline rendering requires Node.js 18+. ffmpeg needed for MP3/Opus conversion. DISCORD_BOT_TOKEN only required for VC streaming — compose/render works without it." }, "primaryEnv": "DISCORD_BOT_TOKEN", "install": [{ "id": "setup", "kind": "script", "script": "npm install && bash scripts/download-samples.sh", "label": "Install dependencies + download drum samples (~11MB from github.com/tidalcycles/Dirt-Samples, CC-licensed)" }, { "id": "ffmpeg", "kind": "apt", "package": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (audio format conversion)" }], "securityNotes": "PATTERN EXECUTION: Strudel compositions are JavaScript evaluated in Node.js. Patterns CAN access the filesystem, environment variables, and network. Only run compositions you trust. For untrusted patterns, run in a sandbox (container/VM) with no credentials mounted. SAMPLE DOWNLOADS: Default samples fetched from github.com/tidalcycles/Dirt-Samples (CC-licensed). The 'samples add <url>' command enforces a configurable size limit (STRUDEL_MAX_DOWNLOAD_MB, default 10240/10GB), MIME type validation on downloaded archives, and an optional host allowlist (STRUDEL_ALLOWED_HOSTS, comma-separated). Only add packs from trusted sources. CREDENTIALS: DISCORD_BOT_TOKEN is only needed for VC streaming. Compose/render/list work with zero credentials. If providing a token, use minimal scopes (Connect, Speak, Send Messages). RENDERING: All audio synthesis is local and offline via node-web-audio-api (Rust/C++ Web Audio for Node.js). No browser, no puppeteer, no remote code execution. Legacy browser renderer scripts exist in repo but are marked DEPRECATED and not invoked by the skill. RECOMMENDED: Run this skill in an OpenClaw sandbox when accepting user-submitted patterns." } }
---
# Strudel 音乐 🎵

**就像 Midjourney 的 `/imagine` 功能，但用于音乐创作。** 你可以使用 Strudel 的实时编码模式来创作、渲染和播放音乐——完全离线操作，无需浏览器。

## 命令接口

当用户调用 `/strudel` 时，系统会根据用户的指令进行相应的操作：

### `/strudel <prompt>` — 根据描述创作音乐
根据自然语言提示生成音乐旋律。系统会解析用户的情绪、乐器选择、节奏和结构，编写作曲文件，将其渲染为音频，并将结果发布。

**示例：**
- `/strudel dark ambient tension, low drones, sparse percussion, 65bpm`  
- `/strudel upbeat tavern music with fiddle and drums`  
- `/strudel lo-fi chill beats to study to`  
- `/strudel epic battle music, brass and timpani, 140bpm`  
- `/strudel a theme for a character named Cael — curious, quick, a little dangerous`

**工作流程：**
1. 解析用户指令 → 从决策树中选择情绪、调性、节奏和乐器  
2. 使用 Strudel 的模式语法编写 `.js` 作曲文件  
3. 通过以下命令进行渲染：`node src/runtime/offline-render-v2.mjs <file> <output.wav> <cycles> <bpm>`  
4. 将音频文件转换为 MP3 格式：`ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3`  
5. 将 MP3 文件作为附件发布到频道  
6. （可选）：如果用户在 Discord 的语音频道中，可以通过语音功能播放音乐  

### `/strudel play <name>` — 在 Discord 语音频道中播放已保存的音乐  
将作曲文件流式播放到用户的语音频道中。

```bash
# Render + convert + stream
node src/runtime/offline-render-v2.mjs "assets/compositions/<name>.js" /tmp/<name>.wav 16 120
ffmpeg -i /tmp/<name>.wav -ar 48000 -ac 2 /tmp/<name>-48k.wav -y
node scripts/vc-play.mjs /tmp/<name>-48k.wav
```

### `/strudel list` — 显示所有可用的作曲文件  
列出 `assets/compositions/` 目录下的所有 `.js` 文件及其元数据（`@title`, `@mood`, `@tempo`）。

### `/strudel samples` — 管理音效样本  
**子命令：**  
- `/strudel samples list` — 显示已安装的音效样本目录及其数量  
- `/strudel samples download` — 重新运行 `scripts/download-samples.sh`（如果已存在则跳过）  
- `/strudel samples add <url>` — 从指定 URL 下载音效样本包（ZIP 或 tar 格式，包含 WAV 文件）  
- `/strudel samples add <path>` — 将本地目录链接或复制到 `samples/` 目录  

**自定义音效样本的使用方法：**  
将任何包含 WAV 文件的目录放入 `samples/<name>/` 目录中。系统会自动识别这些样本，并在音乐创作中使用 `s("<name>)` 来引用它们。样本按文件名排序，可以通过 `s("<name>).n(3)` 来访问特定样本。  
**示例：** 如果你有一个导出的 Ableton 鼓组文件（WAV 格式），只需将其放入 `samples/` 目录中即可。

### `/strudel concert <name> [name2] [name3] ...` — 按顺序播放多首音乐  
依次渲染并流式播放多个作曲文件到 Discord 语音频道中。

## 设置

```bash
npm run setup
# Installs all deps + downloads dirt-samples (~11MB, CC-licensed)
```

首次使用前，请运行 `npm run test:render` 进行测试。

### 添加更多音效样本包

该工具自带的 `dirt-samples` 包包含 96 个 WAV 文件（如踢鼓、军鼓、钹、808 音效等）。如需更丰富的音效，可以添加额外的样本包：

**免费样本包（直接下载并放入 `samples/` 目录）：**  
- [Dirt-Samples](https://github.com/tidalcycles/Dirt-Samples) — 800 多个样本（我们提供了部分样本）  
- [Signature Sounds – Homemade Drum Kit](https://signalsounds.com)（CC0 许可）—— 150 多个音效  
- [Looping – Synth Pack 01](https://looping.com)（CC0 许可）—— 合成音效和循环音  
- [artgamesound.com](https://artgamesound.com)—— 提供可搜索的音效资源  

**自定义样本包：**  
你可以从任何数字音频工作站（如 Ableton、FL Studio、M8 Tracker 等）导出 WAV 文件并放入 `samples/` 目录。Strudel 不关心样本的来源，只要文件是 WAV 格式即可。

**命名音效库**（Strudel 内置功能，需要 CDN 访问权限）：  
```javascript
sound("bd sd cp hh").bank("RolandTR909")
sound("bd sd hh oh").bank("LinnDrum")
```

### 在 WSL2 环境中使用的注意事项  

如果在 WSL2 环境下通过 Discord 语音功能播放音乐，请启用 **镜像网络**（mirrored networking）：

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
networkingMode=mirrored
```

完成后执行 `wsl --shutdown` 并重新启动程序。如果不启用镜像网络，WSL2 的 NAT 设置可能会影响 Discord 的 UDP 语音协议，导致音频无法传输。启用镜像网络后，WSL2 会直接连接到主机的网络栈，从而解决这个问题。

此设置仅影响语音流式播放；离线渲染和文件上传功能在所有网络环境下均可用。

## 工作原理

离线渲染器使用 **node-web-audio-api**（基于 Rust 的 Node.js Web Audio 库）来实现音频合成：  
1. **模式解析**：`@strudel/core`、`@strudel/mini` 和 `@strudel/tonal` 模块将用户提供的模式代码解析为定时音频片段。  
2. **音频合成**：每个音频片段会被转换为振荡器（正弦波、锯齿波、方波或三角波）或来自样本目录的音频样本，并进行音高调整。  
3. **离线渲染**：`OfflineAudioContext.startRendering()` 函数完成音频文件的生成。  
4. **输出格式**：生成的音频为 16 位立体声 WAV 格式（44.1kHz），随后通过 ffmpeg 转换为 MP3 或 Opus 格式。

**关于 `mini` 格式的说明：** 由于 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用，因此需要在使用前显式调用 `setStringParser(mini.mini)`。这个问题与 [openclaw#22790](https://github.com/openclaw/openclaw/issues/22790) 有关。

## 作曲相关参考资料  

### 节奏（Tempo）  
```javascript
setcpm(120/4)  // 120 BPM
```

### 音乐层次结构（Layering）  
```javascript
stack(
  s("bd sd bd sd"),                              // drums
  note("c3 g3").s("sawtooth").lpf(800),          // bass
  n("0 2 4 7").scale("C:minor").s("triangle")    // melody
)
```

### 模式语法（Pattern Syntax）  
- `"a b c d"` — 表示每个节拍中的一个音符序列  
- `"[a b]"` — 表示在一个节拍内播放两个音符  
- `"<a b c>"` — 表示每个循环交替播放两个音符  
- `"a*3"` — 表示重复某个音符三次  
- `"~"` — 表示休止/静音  
- `.slow(2)` / `.fast(2)` — 表示调整播放速度  
- `.euclid(3,8)` — 表示使用欧几里得节奏  

### 表达方式（Expression）  
```javascript
.lpf(sine.range(400, 4000).slow(8))   // filter sweep
.gain(sine.range(0.1, 0.2).slow(9))   // breathing volume
.pan(perlin.range(0.2, 0.8))          // organic stereo
.room(0.5).roomsize(4)                 // reverb
.delay(0.3).delaytime(0.25)           // delay
.attack(0.01).decay(0.2).sustain(0.5).release(0.3)  // ADSR
```

### 歌曲结构（Song Structure）  
```javascript
let intro = stack(pad, noise)
let verse = stack(drums, bass, melody)
let chorus = stack(drums, bass, melody, lead)

arrange(
  [8, intro],
  [16, verse],
  [8, chorus]
).cpm(120/4)
```

### 情绪与参数的关联（Mood → Parameter Decision Tree）  
| 情绪（Mood） | 节奏（Tempo） | 调性/音阶（Key/Scale） | 音乐风格（Character） |
|------|-------|-----------|-----------|
| 紧张（Tension） | 60-80 | 小调/弗里吉亚调式（minor/phrygian） | 低音量、稀疏的音效、持续的低音  
| 战斗（Combat） | 120-160 | 小调（minor） | 强烈的鼓声、快速节奏、失真效果  
| 探索（Exploration） | 80-100 | 多利安调式/混合利底亚调式（dorian/mixolydian） | 开放式的旋律、延迟效果、中等能量  
| 和平（Peace） | 60-80 | 五声音阶/大调（pentatonic/major） | 温暖的音色、缓慢的节奏、氛围感强的音乐  
| 神秘（Mystery） | 70-90 | 全音阶（whole tone） | 混响效果、稀疏的音效、充满神秘感  
| 胜利（Victory） | 110-130 | 大调（major） | 明亮的音色、欢快的旋律、饱满的音效  
| 悲伤（Sorrow） | 48-65 | 小调（minor） | 持续的低音、简洁的音乐风格  
| 仪式（Ritual） | 45-60 | 多利安调式（dorian） | 奥尔加ン低音、重复的旋律  

更多详细信息请参阅 `references/mood-parameters.md` 文件中的情绪与参数关联表，以及 `references/production-techniques.md` 文件中的高级制作技巧。

## 文件结构（File Structure）  
```
src/runtime/
  offline-render-v2.mjs    — Core offline renderer
  smoke-test.mjs           — 12-point verification test

scripts/
  download-samples.sh      — Download dirt-samples (idempotent)
  vc-play.mjs              — Stream audio to Discord VC

samples/                   — Sample packs (gitignored, downloaded on demand)
assets/compositions/       — Saved compositions
references/                — Mood trees, techniques, architecture docs
```
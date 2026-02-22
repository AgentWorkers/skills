---
name: strudel-music
description: "使用 Strudel 的实时编码功能来创作、渲染和播放音乐。  
使用方法：  
- `/strudel <prompt>`：描述你想要听到的音乐风格（情绪、场景、类型、使用的乐器等）。  
- `/strudel play <name>`：在 Discord 的语音聊天中播放已保存的音乐作品。  
- `/strudel samples`：管理音色样本包。  
- `/strudel list`：显示可用的音乐作品列表。  
可以将其视为 Midjourney 的音乐版本——用于创意音乐创作。"
user-invocable: true
metadata: { "openclaw": { "emoji": "🎵", "requires": { "bins": ["node"], "anyBins": ["ffmpeg"], "env": ["DISCORD_BOT_TOKEN"], "node": ">=18", "description": "Offline rendering requires Node.js 18+. ffmpeg needed for MP3/Opus conversion. DISCORD_BOT_TOKEN only required for VC streaming — compose/render works without it." }, "primaryEnv": "DISCORD_BOT_TOKEN", "install": [{ "id": "setup", "kind": "script", "script": "npm install && bash scripts/download-samples.sh", "label": "Install dependencies + download drum samples (~11MB from github.com/tidalcycles/Dirt-Samples, CC-licensed)" }, { "id": "ffmpeg", "kind": "apt", "package": "ffmpeg", "bins": ["ffmpeg"], "label": "Install ffmpeg (audio format conversion)" }], "securityNotes": "PATTERN EXECUTION: Strudel compositions are JavaScript evaluated in Node.js. Patterns CAN access the filesystem, environment variables, and network. Only run compositions you trust. For untrusted patterns, run in a sandbox (container/VM) with no credentials mounted. SAMPLE DOWNLOADS: Default samples fetched from github.com/tidalcycles/Dirt-Samples (CC-licensed). The 'samples add <url>' command can fetch from arbitrary URLs — only add packs from trusted sources. CREDENTIALS: DISCORD_BOT_TOKEN is only needed for VC streaming. Compose/render/list work with zero credentials. If providing a token, use minimal scopes (Connect, Speak, Send Messages). RENDERING: All audio synthesis is local and offline via node-web-audio-api (Rust/C++ Web Audio for Node.js). No browser, no puppeteer, no remote code execution. Legacy browser renderer scripts exist in repo but are marked DEPRECATED and not invoked by the skill. RECOMMENDED: Run this skill in an OpenClaw sandbox when accepting user-submitted patterns." } }
---
# Strudel 音乐 🎵

**就像 Midjourney 的 `/imagine` 功能，但用于音乐创作。** 你可以使用 Strudel 的实时编码模式来创作、渲染和播放音乐——完全离线操作，无需浏览器。

## 命令接口

当用户调用 `/strudel` 时，系统会根据用户的意图来执行相应的操作：

### `/strudel <prompt>` — 根据描述创作音乐
从自然语言描述中生成音乐模式。系统会解析用户的情绪、乐器选择、节奏和结构，然后编写乐谱文件，将其渲染成音频，并将结果发布到指定频道。

**示例：**
- `/strudel dark ambient tension, low drones, sparse percussion, 65bpm`  
- `/strudel upbeat tavern music with fiddle and drums`  
- `/strudel lo-fi chill beats to study to`  
- `/strudel epic battle music, brass and timpani, 140bpm`  
- `/strudel a theme for a character named Cael — curious, quick, a little dangerous`

**工作流程：**
1. 解析用户输入的描述 → 从决策树中选择合适的情绪、调性和节奏  
2. 使用 Strudel 的模式语法编写 `.js` 格式的乐谱文件  
3. 通过以下命令进行渲染：`node src/runtime/offline-render-v2.mjs <file> <output.wav> <cycles> <bpm>`  
4. 将音频文件转换为 MP3 格式：`ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3`  
5. 将生成的 MP3 文件作为附件发布到频道  
6. （可选）：如果用户处于 Discord 的语音聊天频道中，可以播放该音频  

### `/strudel play <name>` — 在 Discord 语音聊天频道中播放已保存的音乐
将之前创作的音频流式播放到用户的语音聊天频道中。

```bash
# Render + convert + stream
node src/runtime/offline-render-v2.mjs "assets/compositions/<name>.js" /tmp/<name>.wav 16 120
ffmpeg -i /tmp/<name>.wav -ar 48000 -ac 2 /tmp/<name>-48k.wav -y
node scripts/vc-play.mjs /tmp/<name>-48k.wav
```

### `/strudel list` — 显示可用的音乐作品
列出 `assets/compositions/` 目录下的所有 `.js` 文件及其元数据（`@title`, `@mood`, `@tempo`）。

### `/strudel samples` — 管理音效样本包
**子命令：**
- `/strudel samples list` — 显示已安装的音效样本目录及其数量  
- `/strudel samples download` — 重新运行 `scripts/download-samples.sh` 命令（如果样本已存在则忽略）  
- `/strudel samples add <url>` — 从指定 URL 下载音效样本包（ZIP 或 tar 格式，包含 WAV 文件）  
- `/strudel samples add <path>` — 将本地目录链接或复制到 `samples/` 目录中  

**自定义音效样本的使用方法：**
将包含 WAV 文件的目录放入 `samples/<name>/` 目录中。系统会自动识别这些样本，并可以在模式中使用 `s("<name>)` 来引用它们。样本按文件名排序，可以通过 `s("<name>).n(3)` 来访问特定样本。

**示例：** 如果你有一个导出的 Ableton 音效库（格式为 WAV 文件），可以直接将其放入 `samples/` 目录中。

### `/strudel concert <name> [name2] [name3] ...` — 按顺序播放多首音乐作品
依次渲染并流式播放多个音乐作品。

## 设置

```bash
npm run setup
# Installs all deps + downloads dirt-samples (~11MB, CC-licensed)
```

初次使用前，请运行 `npm run test:render` 进行测试。

### 添加更多音效样本包

该工具自带了 **dirt-samples**（包含 96 个 WAV 文件，如踢鼓、军鼓、钹、通鼓等音效）。如需更丰富的音效，可以添加自定义样本包：

**免费样本包（只需下载并放入 `samples/` 目录）：**
- [Dirt-Samples](https://github.com/tidalcycles/Dirt-Samples) — 800 多个音效样本（我们提供了部分样本）  
- [Signature Sounds – Homemade Drum Kit](https://signalsounds.com) （CC0 许可）—— 150 多个独奏音效  
- [Looping – Synth Pack 01](https://looping.com) （CC0 许可）—— 合成音效和循环音  
- [artgamesound.com](https://artgamesound.com) — 提供可搜索的音效资源  

**自定义样本包：** 你可以从任何音乐制作软件（如 Ableton、FL Studio、M8 Tracker 等）中导出 WAV 文件，并将其放入 `samples/` 目录。Strudel 不关心样本的来源，只要文件是 WAV 格式即可。

**命名音效库**（Strudel 内置功能，需要 CDN 访问权限）：
```javascript
sound("bd sd cp hh").bank("RolandTR909")
sound("bd sd hh oh").bank("LinnDrum")
```

### 在 WSL2 环境下使用时的注意事项

如果在 WSL2 环境下通过 Discord 语音聊天频道播放音乐，请启用 **mirrored networking** 功能：

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
networkingMode=mirrored
```

完成后，执行 `wsl --shutdown` 并重新启动程序。如果不启用此功能，WSL2 的 NAT 设置会干扰 Discord 的 UDP 语音协议，导致音频无法传输。启用 mirrored networking 可以让 WSL2 直接接入主机的网络堆栈，从而解决这个问题。

**注意：** 此设置仅影响语音聊天功能。离线渲染和文件上传在任何网络环境下都能正常工作。

## 工作原理

离线渲染器使用 **node-web-audio-api**（基于 Rust 的 Node.js Web Audio 库）来实现音频合成：
1. **模式解析**：`@strudel/core`、`@strudel/mini` 和 `@strudel/tonal` 模块负责解析用户提供的模式代码。  
2. **音频合成**：每个模式会被转换为以下两种形式之一：
   - **振荡器**（正弦波、锯齿波、方波或三角波），带有 ADSR 模式和双二次滤波器  
   - **音效样本**（来自 `samples` 目录的 `AudioBufferSourceNode` 对象，支持音高调整）  
3. **离线渲染**：`OfflineAudioContext.startRendering()` 函数完成音频文件的生成  
4. **输出格式**：16 位立体声 WAV 格式，采样率为 44.1kHz，随后通过 ffmpeg 转换为 MP3 或 Opus 格式  

**关于 `mini` 格式的说明：** 由于 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用，因此需要在导入后显式调用 `setStringParser(mini.mini)`。这个问题与 [openclaw#22790](https://github.com/openclaw/openclaw/issues/22790) 中提到的问题类似。

## 音乐创作相关参考资料

- **节奏参考**：```javascript
setcpm(120/4)  // 120 BPM
```  
- **音层叠加技巧**：```javascript
stack(
  s("bd sd bd sd"),                              // drums
  note("c3 g3").s("sawtooth").lpf(800),          // bass
  n("0 2 4 7").scale("C:minor").s("triangle")    // melody
)
```  
- **模式语法**：  
  - `"a b c d"`：每个节拍播放一个音符  
  - `"[a b]"`：每个节拍播放两个音符  
  - `"<a b c>"`：每个循环交替播放两个音符  
  - `"a*3"`：重复播放某个音符  
  - `"~"`：表示休止/静音  
  - `.slow(2)` / `.fast(2)`：调整音频速度  
  - `.euclid(3,8)`：欧几里得节奏  

**其他相关内容：**  
- **表达式语法**：```javascript
.lpf(sine.range(400, 4000).slow(8))   // filter sweep
.gain(sine.range(0.1, 0.2).slow(9))   // breathing volume
.pan(perlin.range(0.2, 0.8))          // organic stereo
.room(0.5).roomsize(4)                 // reverb
.delay(0.3).delaytime(0.25)           // delay
.attack(0.01).decay(0.2).sustain(0.5).release(0.3)  // ADSR
```  
- **歌曲结构**：```javascript
let intro = stack(pad, noise)
let verse = stack(drums, bass, melody)
let chorus = stack(drums, bass, melody, lead)

arrange(
  [8, intro],
  [16, verse],
  [8, chorus]
).cpm(120/4)
```  
- **情绪与参数之间的关系**：参见 `references/mood-parameters.md`，了解情绪与音乐参数之间的对应关系。  
- **高级制作技巧**：如呼吸效果、音色变化等，详见 `references/production-techniques.md`。  

## 文件结构：```
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
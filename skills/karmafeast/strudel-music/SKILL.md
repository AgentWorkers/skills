---
name: strudel-music
description: >
  **通过 Strudel 进行音频拆解与合成**：  
  - 根据自然语言提示创作音乐；  
  - 将生成的音频文件导出为 WAV/MP3 格式；  
  - 将音频流式传输到 Discord 的语音聊天功能中。  
  - 可以将任何音频文件拆解为多个音轨（stems），提取音频样本，并使用这些样本进行音乐创作。  
  **使用方法：**  
  - `/strudel <prompt>`：根据提示生成新音乐  
  - `/strudel play <name>`：播放指定的音乐文件  
  - `/strudel list`：列出所有可用的音乐作品  
  - `/strudel samples`：查看所有可用的音频样本
version: 2.0.0
author: the dandelion cult
license: MIT
tags: [music, audio, strudel, composition, samples, trance]
user-invocable: true
requires:
  - node >= 20
  - ffmpeg
optional:
  - python3 + demucs (for stem separation)
  - python3 + librosa (for pitch/onset analysis)
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: [node]
      anyBins: [ffmpeg]
      node: ">=20"
    install:
      - id: setup
        kind: script
        script: "npm install && bash scripts/download-samples.sh"
        label: "Install dependencies + download drum samples (~11MB)"
      - id: ffmpeg
        kind: apt
        package: ffmpeg
        bins: [ffmpeg]
        label: "Install ffmpeg (audio format conversion)"
    securityNotes: >
      Strudel compositions are JavaScript evaluated in Node.js. Patterns CAN
      access filesystem, env vars, and network. Only run trusted compositions.
      For untrusted patterns, use a sandbox (container/VM) with no credentials.
---
> ⚠️ **法律声明：** 本工具会处理您提供的音频文件。您有责任确保自己拥有使用这些音频素材的合法权利。作者不对您使用本工具处理受版权保护的材料的行为作出任何关于“合理使用”、“版权”或“衍生作品”的声明。

# Strudel 音乐 🎵

使用代码来创作、渲染、分解和混音音乐。它可以将自然语言指令转换为音乐模式，然后通过离线 Web Audio 合成技术进行渲染，并将音频发布到 Discord 的虚拟频道（VC）中。此外，它还可以将任何音频轨道反工程为音源片段、样本和生成程序。

> **新用户？** 请阅读 [docs/ONBOARDING.md](docs/ONBOARDING.md) 以获取基础入门信息。

---

## ⚠️ 会话安全 — 请先阅读此内容

**渲染过程必须作为子代理或后台进程运行，绝不能在主线会话中直接执行。**

离线渲染器（`chunked-render.mjs` / `offline-render-v2.mjs`）会运行一个紧密的音频处理循环，这会阻塞 Node.js 的事件循环。如果您在主线 OpenClaw 会话中运行它，**系统将在大约 30 秒后终止该进程**（因为超时设置）。

```
✅ Correct: spawn a sub-agent or use background exec
❌ Wrong:   run the renderer inline in your main conversation
```

**务必执行以下操作：**
```bash
# Background exec with timeout
exec background:true timeout:120 command:"node src/runtime/chunked-render.mjs src/compositions/my-track.js output/my-track.wav 20"
```

**或者创建一个子代理：**
```
sessions_spawn task:"Render strudel-music composition: node src/runtime/chunked-render.mjs ..."
```

这是避免出现问题的首要方法。请不要跳过这一步。

---

## 快速入门

```bash
# 1. Setup
cd ~/.openclaw/workspace/strudel-music
npm run setup              # installs deps + downloads samples (~11MB)

# 2. Verify
npm test                   # 12-point smoke test

# 3. Render
node src/runtime/chunked-render.mjs assets/compositions/fog-and-starlight.js output/fog.wav 16
ffmpeg -i output/fog.wav -codec:a libmp3lame -b:a 192k output/fog.mp3
```

## 命令

| 命令 | 功能 |
|---|---|
| `/strudel <提示>` | 根据自然语言指令创作音乐——包括情绪、场景、风格和乐器 |
| `/strudel play <名称>` | 将保存的音乐作品流式播放到 Discord VC |
| `/strudel list` | 显示可用的音乐作品及其元数据 |
| `/strudel samples` | 管理样本包（列出、下载、添加） |
| `/strudel concert <曲目...>` | 在 Discord VC 中播放指定曲目列表 |

### 创作流程

1. 解析指令 → 选择情绪、调性、节奏和乐器（详见 `references/mood-parameters.md`）
2. 使用 Strudel 模式语法编写 `.js` 文件来表示音乐结构 |
3. 在后台进行渲染：```bash
   node src/runtime/chunked-render.mjs <file> <output.wav> <cycles> [chunkSize]
   ```
4. 将音频转换为 MP3 格式：```bash
   ffmpeg -i output.wav -codec:a libmp3lame -b:a 192k output.mp3
   ```
5. 将 MP3 文件作为附件发布或流式传输到 Discord VC

### Discord VC 流式传输

```bash
node src/runtime/offline-render-v2.mjs assets/compositions/combat-assault.js /tmp/track.wav 12 140
ffmpeg -i /tmp/track.wav -ar 48000 -ac 2 /tmp/track-48k.wav -y
node scripts/vc-play.mjs /tmp/track-48k.wav
```

使用 WSL2 的用户：请启用镜像网络模式（在 `.wslconfig` 文件中设置 `networkingMode=mirrored`），否则 VC 流式传输会因 NAT 问题而失败（NAT 会干扰 Discord 的 UDP 语音协议）。

## 样本管理

### 文件目录结构

所有样本文件都存储在 `samples/` 目录下。系统会自动识别该目录中的 WAV 文件。

```
samples/
├── strudel.json          ← sample map (pitch info, paths)
├── kick/
│   └── kick.wav
├── hat/
│   └── hat.wav
├── bass_Cs1/
│   └── bass_Cs1.wav      ← pitched sample (root: C#1)
├── synth_lead/
│   └── synth_lead.wav     ← pitched sample (root: C#3, declared in strudel.json)
└── bloom_kick/
    └── bloom_kick.wav     ← from audio deconstruction
```

### strudel.json 格式

该文件将样本名称与对应的文件路径关联起来，并可指定根音。渲染器会依据此文件来检测音高。

```json
{
  "_base": "./",
  "kick": { "0": "kick/kick.wav" },
  "bass_Cs1": { "cs1": "bass_Cs1/bass_Cs1.wav" },
  "synth_lead": { "cs3": "synth_lead/synth_lead.wav" }
}
```

- 带有音符后缀的文件名（如 `_Cs1`、 `_D2`）表示对应的调性 |
- 无固定音高的样本使用 `"0"` 作为默认调性 |
- 对于有固定音高的样本，必须指定根音——否则渲染器会默认使用 C4 调性（详见 [docs/KNOWN-PITFALLS.md](docs/KNOWN-PITFALLS.md#3-root-note-detection-defaults)）

### 样本包管理

**附带提供的样本包**（包含 153 个 WAV 文件，采用 CC0 许可协议）。安全措施：下载时会有文件大小限制（`STRUDEL_MAX_DOWNLOAD_MB`，默认为 10GB），同时会进行 MIME 校验，并可设置允许的访问主机列表（`STRUDEL_ALLOWED_HOSTS`）。

## 创作指南

### 模式基础

**免费样本包（可直接下载到 `samples/` 目录）：**
- [Dirt-Samples](https://github.com/tidalcycles/Dirt-Samples) — 包含 800 多个样本（我们提供了部分样本） |
- [Signature Sounds – 自制鼓组](https://signalsounds.com)（CC0 许可） — 包含 150 多个音效样本 |
- [Looping – Synth Pack 01](https://looping.com)（CC0 许可） — 包含合成音效和循环片段 |
- [artgamesound.com](https://artgamesound.com) — 提供可搜索的样本资源（CC0 许可）

**自定义样本包：** 可从任何数字音频工作站（如 Ableton、FL Studio、M8 Tracker 等）导出 WAV 文件。Strudel 不关心样本的来源，只要文件格式正确即可。

**命名规则**（Strudel 内置功能，需要 CDN 访问权限）：
```javascript
sound("bd sd cp hh").bank("RolandTR909")
sound("bd sd hh oh").bank("LinnDrum")
```

### 在使用 WSL2 时需要注意

如果在 WSL2 环境下并通过 Discord VC 进行流式传输，请启用镜像网络模式：

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
networkingMode=mirrored
```

之后请执行 `wsl --shutdown` 并重新启动程序。如果不启用此模式，WSL2 的 NAT 问题会导致 Discord 的 UDP 语音协议无法正常工作——虽然机器人可以加入频道，但由于 IP 发现数据包无法穿越 NAT，因此无法传输音频。镜像网络模式可以通过将 WSL2 直接连接到主机的网络栈来规避这个问题。

此设置仅影响流式传输功能。离线渲染和文件上传功能在所有网络环境下均能正常工作。

## 平台要求

根据您的需求，系统分为两个层级：

### 仅使用 JavaScript 的创作与渲染功能
- **Node.js 18.0 或更高版本**（推荐使用 22.0 或更高版本以获得稳定的 `OfflineAudioContext` 功能） |
- **ffmpeg**（用于 MP3/Opus 格式的音频转换） |
- 支持多种平台：x86_64、ARM64、WSL2、裸机系统以及容器环境 |
- 不需要 Python、GPU 或机器学习框架。

### 完整的音频处理流程（包含 Demucs）

除了上述要求外，还需要：
- **Python 3.10 或更高版本** |
- **相关 Python 包：`demucs`、`librosa`、`numpy`、`scipy`、`scikit-learn`、`torch` |
- 约 2GB 的磁盘空间用于存储 PyTorch 和 Demucs 模型文件（首次运行时会下载这些文件） |
- **可选：** 使用 NVIDIA GPU 和 CUDA 工具包，可提升 Demucs 的处理速度约 5 倍

请安装所需的 Python 包：
```bash
pip install demucs librosa numpy scipy scikit-learn torch
```

即使缺少这些 Python 包，创作和渲染功能仍可正常使用，但无法执行音源提取等高级操作。在这种情况下，系统会优雅地提示错误，而不会显示详细的错误堆栈信息。

---

## 完整的音频处理流程

如果您拥有 MP3 文件，并希望从中提取乐器音源、构建样本库并使用这些样本进行创作，那么就需要执行完整的音频处理流程。具体步骤如下：

```
MP3 → Demucs (stem separation) → librosa (analysis) → sample slicing → Strudel composition → render → MP3
```

**对于一首典型的音乐作品，整个流程大约需要 4–8 分钟。** 详情请参阅 `docs/pipeline.md`，其中包含了详细的步骤、时间消耗和资源要求。

### 简化版本

```bash
# 1. Separate stems (Python/Demucs)
python -m demucs input.mp3 --out ./stems

# 2. Analyze + slice (see docs/pipeline.md for details)
# Currently semi-manual — analysis scripts in development

# 3. Write composition referencing sliced samples
# 4. Render
bash scripts/dispatch.sh render my-composition.js 16 120

# 5. Convert
ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3 -y
```

### 处理时间估算

| 流程阶段 | CPU 耗时估计 | GPU 耗时估计 |
|-------|-------------|-------------|
| Demucs 音源分离 | 每分钟约 15 秒 | 每分钟约 3 秒 |
| 音频分析（每个音源片段） | 每分钟约 10–20 秒 | 每分钟约 10–20 秒 |
| 样本分割 | 每分钟约 5 秒 | 每分钟约 5 秒 |
| 音乐创作 | 即时完成（由人类或 AI 生成 JavaScript 代码） | 即时完成 |
| 音频渲染 | 每分钟约 30–60 秒 | 每分钟约 30–60 秒 |
| MP3 转换 | 每分钟约 5 秒 | 每分钟约 5 秒 |

**总计（4 分钟长的音乐作品）：** CPU 耗时 4–8 分钟；** 仅包含创作和渲染步骤（不使用 Demucs）：** 2–3 分钟。

---

## ⚠️ 会话安全 — 请先阅读此内容

> **完整的音频处理流程需要 4–8 分钟。仅包含创作和渲染步骤则需要 2–3 分钟。**
>
> **请勿** 在 Discord 通道交互或主线 OpenClaw 会话中直接执行此流程。**
> 如果超过 30 秒的响应时间限制，系统会自动终止渲染进程。此时系统可能显示故障状态（无音频输出，也无错误提示）。

### 安全运行方法

**正确的方式：** 通过 OpenClaw 的子代理来执行渲染任务：**
```javascript
sessions_spawn({
  task: "Render strudel composition: /strudel dark ambient tension, 65bpm",
  mode: "run",
  runTimeoutSeconds: 600  // 10 minutes — generous for full pipeline
})
```

**作为后台进程运行也是正确的选择：**
```bash
exec({ command: "bash scripts/dispatch.sh render ...", background: true })
```

**直接通过 CLI 运行也是可行的（适用于测试）：**
```bash
bash scripts/dispatch.sh render assets/compositions/fog-and-starlight.js 16 72
```

**应对用户的方式：** “音频渲染需要一些时间，请稍候。” 不要让用户长时间等待而没有任何反馈。

### 不建议的做法

```javascript
// WRONG — will timeout after 30s in Discord context
exec({ command: "bash scripts/dispatch.sh render ..." })

// WRONG — blocking the main session for minutes
// (anything inline that takes >30s)
```

---

## 学习资源

详细的使用文档位于 `docs/` 目录下：

| 文档 | 内容涵盖 |
|----------|---------------|
| [`docs/pipeline.md`](docs/pipeline.md) | 完整的音频处理流程步骤、命令、时间消耗和系统要求 |
| [`docs/composition-guide.md`](docs/composition-guide.md) | 实用创作技巧——包括常见的错误来源（如符号表示法错误、调试技巧等） |
| [`docs/TESTING.md`](docs/TESTING.md) | 测试策略——包括烟雾测试、跨平台验证和质量控制方法 |

**如果您正在学习如何使用该工具，请从 `composition-guide.md` 开始学习。** 特别要注意符号表示法（使用空格还是尖括号）的正确用法，这是导致错误的主要原因之一。**

## 工作原理

离线渲染器使用 **node-web-audio-api**（基于 Rust 的 Web Audio 库，专为 Node.js 设计）来实现音频合成：

1. **模式解析** — `@strudel/core`、`@strudel/mini` 和 `@strudel/tonal` 模块会将输入的模式代码解析为具有时间控制的音频片段 |
2. **音频调度** — 每个音频片段会被转换为：
   - 具有 ADSR 模式的振荡器（正弦波、锯齿波、方波或三角波） |
   - 来自样本目录的音频样本（`AudioBufferSourceNode`），并可调整音高 |
3. **离线渲染** — `OfflineAudioContext.startRendering()` 会生成最终的音频文件 |
4. **输出格式**：16 位立体声 WAV 文件，采样率为 44.1kHz，随后会转换为 MP3 或 Opus 格式

**关于迷你符号表示法的说明：** 由于 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用，因此渲染器在导入后会显式调用 `setStringParser(mini.mini)` 方法。这个问题与 [openclaw#22790](https://github.com/openclaw/openclaw/issues/22790) 中提到的问题类似。

## 创作相关参数

### 节奏设置

```javascript
setcpm(120/4)  // 120 BPM

stack(
  s("bd sd [bd bd] sd").gain(0.4),           // drums (samples)
  s("[hh hh] [hh oh]").gain(0.2),            // hats
  note("c3 eb3 g3 c4")                       // melody
    .s("sawtooth")
    .lpf(sine.range(400, 2000).slow(8))      // filter sweep
    .attack(0.01).decay(0.3).sustain(0.2)    // ADSR envelope
    .room(0.4).delay(0.2)                    // space
    .gain(0.3)
)
```

### 迷你符号表示法快速参考

| 符号 | 含义 |
|---|---|
| `"a b c d"` | 每个节拍对应一个音符 |
| `"[a b]"` | 每个节拍包含两个音符 |
| `<a b c>"` | 每个周期交替播放两个音符 |
| `"a*3"` | 重复播放该音符 |
| `"~"` | 表示休止/静音 |
| `.slow(2)` / `.fast(2)` | 调整播放速度 |
| `.euclid(3,8)` | 使用欧几里得节奏模式 |

### 情绪与参数设置

| 情绪 | 节奏 | 调性/音阶 | 音乐风格 |
|---|---|---|---|
| tension | 60–80 | 小调/弗里吉亚调式 | 低音量、节奏较慢 |
| combat | 120–160 | 小调 | 音量较大、节奏较快、带有失真效果 |
| peace | 60–80 | 五声音阶/大调 | 音量适中、节奏较慢、氛围感强 |
| mystery | 70–90 | 全音阶 | 音量适中、带有混响效果 |
| victory | 110–130 | 大调 | 音量较大、节奏明快、带有欢庆氛围 |
| ritual | 45–60 | 多利安调式 | 有organ音效和重复的节奏 |

完整参数设置说明请参阅 `references/mood-parameters.md`。更多制作技巧请参阅 `references/production-techniques.md`。

### 注意：**使用符号 `<>`（代表连续音符）**

请务必使用 `<>` 而不是空格来表示连续的音符：

```javascript
// ❌ WRONG — all values play simultaneously, causes clipping
s("kick").gain("0.3 0.3 0.5 0.3")

// ✅ RIGHT — one value per cycle
s("kick").gain("<0.3 0.3 0.5 0.3>")
```

完整错误列表请参阅 [docs/KNOWN-PITFALLS.md](docs/KNOWN-PITFALLS.md)。

### 音量检查

渲染完成后请务必检查音频音量：
```bash
ffmpeg -i output.wav -af loudnorm=print_format=json -f null - 2>&1 | grep -E "input_i|input_tp"
```
目标音量范围：-16 至 -10 LUFS；实际峰值应低于 -1 dBTP。如果音量超过 -5 LUFS，说明存在问题。

## 音频处理流程

完整的音频处理流程说明请参阅 [references/integration-pipeline.md](references/integration-pipeline.md)：

```
Audio → Demucs (stems) → librosa (analysis) → strudel.json → Composition → Render
```

1. **音源分离** — Demucs 会将音频分为人声、鼓声、贝斯声等不同部分 |
2. **音频分析** — 使用 `librosa` 库提取音高、起始点及节奏模式 |
3. **结果存储** — 分析结果会被写入 `strudel.json` 文件中，并包含对应的根音信息 |
4. **有两种处理方式：**
   - **基于规则的分析**（适用于结构固定的音乐） → 生成程序会提取音频的统计特征 |
   - **基于样本的分析**（适用于重复性音乐） → 将提取的样本片段通过 Strudel 工具重新播放

此过程需要 Python 环境：`uv init && uv add demucs librosa scikit-learn soundfile`

## 文件目录结构

所有样本文件都存储在 `samples/` 目录下。

## 渲染器内部实现

渲染器使用 **node-web-audio-api**（基于 Rust 的 Web Audio 库）。在运行过程中不依赖浏览器或 Puppeteer。

渲染器在导入模块后会调用 `setStringParser(mini.mini)` 方法，因为 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用。为了避免冲突，渲染器会使用不同的解析器版本。

所有音频处理操作都在本地离线完成：包括振荡器生成、双二次滤波器、ADSR 模式、动态调节、立体声音效处理等。最终输出格式为 16 位立体声 WAV 文件，采样率为 44.1kHz。

---

## 常见平台问题及解决方法

| 平台 | 问题 | 解决方案 |
|---|---|---|
| ARM64 系统 | PyTorch 仅支持 CPU，不支持 CUDA | 这是预期现象——Demucs 的运行速度约为正常情况的 0.25 倍 |
| ARM64 系统 | `torchaudio.save()` 出现问题 | 请修改 `demucs/audio.py` 文件，使用 `soundfile.write()` 方法（详见首次使用指南） |
| ARM64 系统 | `torchcodec` 构建失败 | 不需要该库——可以忽略该问题，Demucs 依然可以正常运行 |
| WSL2 环境 | 在 Discord VC 中音频传输无声 | 请在 `.wslconfig` 文件中启用镜像网络模式 |
| 所有系统 | Strudel 的 `mini` 解析器未正确注册 | 实际上渲染器会自动调用 `setStringParser(mini.mini)` 方法 |

## 安全性注意事项

Strudel 工具使用的脚本（JavaScript）具有访问文件系统、环境和网络的能力。请仅运行您信任的音频文件。对于不可信的音频文件，请在沙箱环境中运行该工具，并确保不加载任何敏感数据。

## 并发处理

每个会话中最多只能同时进行一个渲染任务。如果用户在另一个渲染任务进行中请求 `/strudel clone` 功能：
1. 使用 `subagents(action=list)` 方法检查是否有正在运行的子代理 |
2. 如果正在执行渲染任务，应回复用户：“🎵 目前正在渲染中，请稍候。” |
3. 禁止同时启动第二个渲染任务——否则可能会导致磁盘和内存竞争，从而引发问题。

**原因：** 如果同时使用相同的输出路径（如 `output.wav`），两个渲染任务会互相覆盖文件。即使使用了不同的输出路径，两个 `OfflineAudioContext` 进程也会占用相同的内存资源，可能导致文件损坏。
---
name: strudel-music
description: "通过 Strudel 进行音频解构与合成：可以将任何音频文件分解为多个音轨（stem），提取其中的样本音素，然后利用这些样本音素进行新的音频创作；最终可以将合成的音频文件导出为 WAV 或 MP3 格式。"
version: 0.3.1
author: the dandelion cult
license: MIT
tags: [music, audio, strudel, composition, samples, trance]
metadata:
  openclaw:
    emoji: "🎵"
    requires:
      bins: [node]
      anyBins: [ffmpeg]
      node: ">=20"
    envVars: []
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
      Compositions are JavaScript files evaluated by Node.js. They CAN access
      the filesystem, environment variables, and network. Only run compositions
      you trust or have reviewed. For untrusted compositions, run in a container
      or VM with no credentials in the environment.

      Discord integration (VC streaming, message posting) uses the OpenClaw
      gateway's existing authenticated connection — this skill does NOT require
      its own bot token or Discord credentials. No separate authentication is needed.

      The optional Python pipeline (Demucs, librosa) downloads ML models on first
      run (~1.5GB for htdemucs). These come from official PyTorch/Facebook sources.
---
> ⚠️ **法律声明：** 本工具会处理您提供的音频文件。您需确保自己拥有使用这些音频素材的合法权利。作者不对您使用本工具处理受版权保护的材料的行为作出任何关于合理使用、版权或衍生作品的声明。

# Strudel 音乐 🎵

使用代码来创作、渲染、分解和混音音乐。它可以将自然语言指令转换为音乐模式，然后通过离线 Web Audio 合成技术进行渲染，并将音频发布到 Discord 的语音频道（通过 OpenClaw 通道，无需额外凭证）。此外，它还可以将任何音频文件反工程为音素、样本和生成程序。

> **新用户？** 请阅读 [docs/ONBOARDING.md](docs/ONBOARDING.md) 以获取基础入门信息。

---

## ⚠️ 会话安全 — 请先阅读此内容

**渲染过程必须作为子代理或后台进程运行，绝不能在主会话中直接执行。**

离线渲染器（`chunked-render.mjs` / `offline-render-v2.mjs`）会运行一个紧密的音频处理循环，这会阻塞 Node.js 的事件循环。如果您在主 OpenClaw 会话中直接运行它，**大约 30 秒后**（心跳超时）该进程将会被终止。

```
✅ Correct: spawn a sub-agent or use background exec
❌ Wrong:   run the renderer inline in your main conversation
```

**请始终这样做：**
```bash
# Background exec with timeout
exec background:true timeout:120 command:"node src/runtime/chunked-render.mjs src/compositions/my-track.js output/my-track.wav 20"
```

**或者创建一个子代理：**
```
sessions_spawn task:"Render strudel-music composition: node src/runtime/chunked-render.mjs ..."
```

这是避免出现问题的最佳方法。请不要跳过这一步。

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
| `/strudel <提示>` | 根据自然语言提示创作音乐（包括情绪、场景、风格和乐器） |
| `/strudel play <名称>` | 将保存的音乐作品流式播放到 Discord 语音频道 |
| `/strudel list` | 显示可用的音乐作品及其元数据 |
| `/strudel samples` | 管理样本包（列出、下载、添加） |
| `/strudel concert <曲目...>` | 在 Discord 语音频道中播放指定曲目列表 |

### 创作流程

1. 解析提示 → 选择情绪、调性、节奏和乐器（详见 `references/mood-parameters.md`）
2. 使用 Strudel 模式语法编写 `.js` 文件来创作音乐 |
3. 在后台进行渲染：```bash
   node src/runtime/chunked-render.mjs <file> <output.wav> <cycles> [chunkSize]
   ```
4. 将音频转换为 MP3 格式：```bash
   ffmpeg -i output.wav -codec:a libmp3lame -b:a 192k output.mp3
   ```
5. 将 MP3 文件作为附件发布或流式传输到 Discord 语音频道

### Discord 语音频道流式传输

```bash
node src/runtime/offline-render-v2.mjs assets/compositions/combat-assault.js /tmp/track.wav 12 140
ffmpeg -i /tmp/track.wav -ar 48000 -ac 2 /tmp/track-48k.wav -y
node scripts/vc-play.mjs /tmp/track-48k.wav
```

使用 WSL2 的用户：请启用镜像网络模式（在 `.wslconfig` 中设置 `networkingMode=mirrored`），否则语音传输可能会失败（NAT 会干扰 Discord 的 UDP 音频协议）。

## 样本管理

### 文件目录结构

所有样本文件都存储在 `samples/` 目录下。系统会自动识别该目录下的所有 WAV 文件。

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

该文件将样本名称映射到对应的文件，并可指定根音。渲染器会依据此文件来检测音高。

```json
{
  "_base": "./",
  "kick": { "0": "kick/kick.wav" },
  "bass_Cs1": { "cs1": "bass_Cs1/bass_Cs1.wav" },
  "synth_lead": { "cs3": "synth_lead/synth_lead.wav" }
}
```

- 带有音符后缀的调性（如 `_Cs1`、`_D2`）表示根音
- 无固定音高的样本使用 `"0"` 作为默认调性
- 对于有固定音高的样本，必须指定根音——否则渲染器会默认使用 C4 调性（详见 [docs/KNOWN-PITFALLS.md](docs/KNOWN-PITFALLS.md#3-root-note-detection-defaults)）

### 管理样本包

随软件附带了 **dirt-samples**（153 个 WAV 文件，采用 CC0 许可协议）。安全措施包括：限制下载大小（`STRUDEL_MAX_DOWNLOAD_MB`，默认为 10GB）、MIME 校验以及可选的主机白名单（`STRUDEL_ALLOWED_HOSTS`）。

## 创作指南

### 模式基础

**CC0 / 免费样本包（直接下载到 `samples/` 目录）：**
- [Dirt-Samples](https://github.com/tidalcycles/Dirt-Samples) — 包含 800 多个样本（我们提供其中的一部分）
- [Signature Sounds – Homemade Drum Kit](https://signalsounds.com)（CC0 许可）——包含 150 多个音效样本
- [Looping – Synth Pack 01](https://looping.com)（CC0 许可）——包含合成音效和循环片段
- [artgamesound.com](https://artgamesound.com)——提供可搜索的样本资源

**如果您有自己的样本包：** 可以从任何数字音频工作站（如 Ableton、FL Studio、M8 Tracker 等）导出 WAV 文件。Strudel 不关心样本的来源，只要文件是 WAV 格式即可。

**命名样本库**（Strudel 内置功能，需要 CDN 访问权限）：
```javascript
sound("bd sd cp hh").bank("RolandTR909")
sound("bd sd hh oh").bank("LinnDrum")
```

### WSL2 使用注意事项

如果在 WSL2 环境下运行并向 Discord 语音频道传输音频，请启用 **镜像网络模式**：

```ini
# %USERPROFILE%\.wslconfig
[wsl2]
networkingMode=mirrored
```

之后请执行 `wsl --shutdown` 并重新启动程序。如果不启用此模式，WSL2 的 NAT 会干扰 Discord 的 UDP 音频协议，导致机器人可以加入频道但无法传输音频（因为 IP 发现数据包无法穿透 NAT）。镜像模式通过将 WSL2 直接连接到主机的网络堆栈来规避这个问题。

此设置仅影响语音传输。离线渲染和文件上传功能在所有网络模式下均能正常工作。

## 平台要求

根据您的需求，系统分为两个层级：

### 仅使用 JavaScript 的创作与渲染
- **Node.js 18.0 或更高版本**（推荐使用 22.0 或更高版本以确保 `OfflineAudioContext` 的稳定性）
- **ffmpeg**（用于 MP3/Opus 格式转换）
- 支持多种平台：x86_64、ARM64、WSL2、裸机、容器环境
- 不需要 Python、GPU 或机器学习框架

### 完整流程（包含 Demucs 的音频分解功能）

除了上述要求外，还需要：
- **Python 3.10 或更高版本**
- **相关 Python 包**：`demucs`、`librosa`、`numpy`、`scipy`、`scikit-learn`、`torch`
- 约 2GB 的磁盘空间用于存储 PyTorch 和 Demucs 模型文件（首次运行时需要下载）
- **可选**：NVIDIA GPU 和 CUDA 工具包（可提升 Demucs 的运行速度约 5 倍）

安装 Python 相关依赖包：
```bash
pip install demucs librosa numpy scipy scikit-learn torch
```

即使缺少 Python 依赖包，创作和渲染功能仍然可以正常使用，但无法执行音素提取操作。在这种情况下，技能会优雅地失败并显示错误信息，而不会出现程序崩溃。

---

## 完整流程（包含音频分解功能）

如果您拥有 MP3 文件并希望从中提取乐器音素、构建样本库并使用这些音素进行创作，那么就需要执行完整的流程。具体步骤如下：

```
MP3 → Demucs (stem separation) → librosa (analysis) → sample slicing → Strudel composition → render → MP3
```

**对于一首典型的歌曲，整个过程大约需要 4–8 分钟。** 详情请参阅 `docs/pipeline.md`，其中包含每个步骤的详细说明、所需时间和资源要求。

### 快速版本

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

### 时间估算（大致情况）

| 步骤 | CPU 耗时 | GPU 耗时 |
|-------|-------------|-------------|
| Demucs 音素分离 | 每分钟约 15 秒 | 每分钟约 3 秒 |
| 音频分析（每个音素） | 每分钟约 10–20 秒 | 每分钟约 10–20 秒 |
| 样本切片 | 每分钟约 5 秒 | 每分钟约 5 秒 |
| 音乐创作 | 即时完成（由人类或 AI 生成 JavaScript 代码） | 即时完成 |
| 渲染 | 每分钟约 30–60 秒 | 每分钟约 30–60 秒 |
| MP3 转换 | 每分钟约 5 秒 | 每分钟约 5 秒 |

**总时间（4 分钟的歌曲）：** 4–8 分钟。** 仅包含创作和渲染步骤（不包括 Demucs）：** 2–3 分钟。

---

## ⚠️ 会话安全 — 请先阅读此内容

> **完整流程需要 4–8 分钟。仅包含创作和渲染步骤需要 2–3 分钟。**
>
> **请勿** 在 Discord 通道交互或主 OpenClaw 会话中直接执行此过程。**
> 如果超过 30 秒的响应时间，渲染过程将会被终止，且系统无法自动恢复。此时技能可能会显示为“故障”状态——没有音频输出，也没有错误提示。

### 安全运行方法

**正确的运行方式：**
```javascript
sessions_spawn({
  task: "Render strudel composition: /strudel dark ambient tension, 65bpm",
  mode: "run",
  runTimeoutSeconds: 600  // 10 minutes — generous for full pipeline
})
```

**作为后台进程运行：**
```bash
exec({ command: "bash scripts/dispatch.sh render ...", background: true })
```

**直接通过 CLI 运行（适用于测试）：**
```bash
bash scripts/dispatch.sh render assets/compositions/fog-and-starlight.js 16 72
```

**如何告知用户：**“渲染需要几分钟时间——音频准备好后会立即发布。”** 请不要让用户等待太久而没有任何反馈。

### 不建议的做法

```javascript
// WRONG — will timeout after 30s in Discord context
exec({ command: "bash scripts/dispatch.sh render ..." })

// WRONG — blocking the main session for minutes
// (anything inline that takes >30s)
```

---

## 学习资源

详细文档位于 `docs/` 目录下：

| 文档 | 内容 |
|----------|---------------|
| [`docs/pipeline.md`](docs/pipeline.md) | 完整的创作流程、命令、时间估算、资源要求和系统依赖项 |
| [`docs/composition-guide.md`](docs/composition-guide.md) | 实用创作技巧指南——包括常见的错误来源（如符号表示法错误、音量控制问题等） |
| [`docs/TESTING.md`](docs/TESTING.md) | 测试策略——包括烟雾测试、跨平台验证和质量检查 |

**如果您正在学习如何使用该工具，请从 `composition-guide.md` 开始阅读。** 符号表示法中的空格与尖括号的使用方式是导致错误的主要原因（例如音量异常、音频失真或程序崩溃）。该指南通过实际案例进行了说明。**

## 工作原理

离线渲染器使用 **node-web-audio-api**（基于 Rust 的 Web Audio 库）来实现音频合成：

1. **模式解析** — `@strudel/core`、`@strudel/mini` 和 `@strudel/tonal` 模块会将模式代码解析为定时控制的音频片段 |
2. **音频调度** — 每个片段会被转换为：
   - 带有 ADSR 滤波器和立体声声像效果的振荡器（如正弦波、锯齿波、方波）
   - 或者来自样本目录的样本（`AudioBufferSourceNode`），并可能包含音高调整 |
3. **离线渲染** — `OfflineAudioContext.startRendering()` 会生成完整的音频文件 |
4. **输出**：16 位立体声 WAV 文件，采样率为 44.1kHz，随后通过 ffmpeg 转换为 MP3 或 Opus 格式

**关于迷你符号表示法的说明：** 在导入模块后，渲染器会显式调用 `setStringParser(mini.mini)`，因为 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用。这可能会导致类似 [openclaw#22790](https://github.com/openclaw/openclaw/issues/22790) 中提到的错误。

## 创作参考

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
| `"a b c d"` | 每拍一个音符的序列 |
| `"[a b]"` | 每拍两个音符 |
| `"<a b c>"` | 每个循环交替播放两个音符 |
| `"a*3"` | 重复播放该音符 |
| `"~"` | 休止/静音 |
| `.slow(2)` / `.fast(2)` | 时间拉伸 |
| `.euclid(3,8)` | 欧几里得节奏 |

### 情绪与参数设置

| 情绪 | 节奏 | 调性/音阶 | 音乐特征 |
|---|---|---|---|
| tension | 60-80 | 小调/弗里吉亚调式 | 低音域、音量较小、音色较为稀疏 |
| combat | 120-160 | 小调 | 音量较大、节奏较快、音色失真 |
| peace | 60-80 | 五声音阶/大调 | 音量适中、节奏较慢、音色温暖 |
| mystery | 70-90 | 全音阶 | 音量适中、音色柔和 |
| victory | 110-130 | 大调 | 音量较大、音色明亮、节奏欢快 |
| ritual | 45-60 | 多利安调式 | 音量适中、音色类似风笛、带有重复节奏 |

完整参数设置参考：`references/mood-parameters.md`。制作技巧相关内容请参阅 `references/production-techniques.md`。

### ⚠️ 重要注意事项：符号表示法的使用

请使用 `<>`（慢速播放模式）来表示连续的音符序列，**切勿使用空格**：

```javascript
// ❌ WRONG — all values play simultaneously, causes clipping
s("kick").gain("0.3 0.3 0.5 0.3")

// ✅ RIGHT — one value per cycle
s("kick").gain("<0.3 0.3 0.5 0.3>")
```

完整错误列表：[docs/KNOWN-PITFALLS.md](docs/KNOWN-PITFALLS.md)

### 音量检查

渲染完成后请务必检查音量是否在合理范围内：
```bash
ffmpeg -i output.wav -af loudnorm=print_format=json -f null - 2>&1 | grep -E "input_i|input_tp"
```
目标音量范围：-16 至 -10 LUFS；实际峰值应低于 -1 dBTP。如果音量超过 -5 LUFS，说明存在问题。

## 音频分解流程

完整流程的详细说明请参阅：[references/integration-pipeline.md]

```
Audio → Demucs (stems) → librosa (analysis) → strudel.json → Composition → Render
```

1. **音素分离** — Demucs 将音频分为人声、鼓声、贝斯声等部分 |
2. **音频分析** — 使用 `librosa` 库提取音高、起始位置和节奏模式 |
3. **样本映射** | 分析结果会被保存到 `strudel.json` 文件中，并包含根音信息 |
4. **有两种处理方式：**
   - **基于规则的音乐**：使用 Demucs 生成新的音频文件 |
   **基于样本的音乐**：使用提取的样本片段通过 Strudel 进行播放

此过程需要 Python 环境：`uv init && uv add demucs librosa scikit-learn soundfile`

## 文件结构

```
src/runtime/
  chunked-render.mjs      — Chunked offline renderer (avoids OOM on long pieces)
  offline-render-v2.mjs    — Core offline renderer
  smoke-test.mjs           — 12-point smoke test
scripts/
  download-samples.sh      — Download dirt-samples (idempotent)
  samples-manage.sh        — Sample pack manager
  vc-play.mjs              — Stream audio to Discord VC
samples/                   — Sample packs + strudel.json (gitignored)
assets/compositions/       — 15 original compositions
src/compositions/          — Audio deconstructions
references/                — Mood trees, techniques, architecture
docs/
  KNOWN-PITFALLS.md        — Critical composition pitfalls
  ONBOARDING.md            — Machine-actor onboarding guide
```

## 渲染器内部机制

渲染器使用 **node-web-audio-api**（基于 Rust 的 Web Audio 库）。该渲染器不依赖浏览器或 Puppeteer。

在导入模块后，渲染器会调用 `setStringParser(mini.mini)`，因为 Strudel 的 npm 分发包中 `Pattern` 类在多个模块中被重复引用。为了避免问题，需要确保在不同模块中使用不同的 `Pattern` 解析器。

所有音频处理都在本地离线完成，使用 `OfflineAudioContext` 进行：包括振荡器、双二次滤波器、ADSR 滤波器、`AudioBufferSourceNode` 等功能。输出格式为 16 位立体声 WAV 文件，采样率为 44.1kHz。

---

## 已知的平台兼容性问题

| 平台 | 问题 | 解决方案 |
|---|---|---|
| ARM64 系统（所有版本） | PyTorch 仅支持 CPU，不支持 CUDA | 这是正常现象——Demucs 的运行速度约为实际速度的 0.25 倍 |
| ARM64 系统（所有版本） | `torchaudio.save()` 函数无法正常使用 | 请修改 `demucs/audio.py` 文件，使用 `soundfile.write()` 函数（详见首次使用指南） |
| ARM64 系统（所有版本） | `torchcodec` 构建失败 | 可忽略此问题，因为 Demucs 本身不需要 CUDA |
| WSL2 环境 | 在 Discord 语音频道中无法传输音频 | 请在 `.wslconfig` 文件中启用镜像网络模式 |
| 所有系统 | Strudel 的 `mini` 解析器未正确注册 | 实际上 `setStringParser(mini.mini)` 被正确调用 |

## 🔒 安全性机制

Strudel 的所有功能都是通过 JavaScript 文件执行的，因此具有与普通 Node.js 脚本相同的权限限制：
- **文件系统**：可以读写工作目录中的文件 |
- **环境变量**：可以访问系统环境变量 |
- **网络访问**：可以发送 HTTP 请求

**对于第三方提供的样本文件：**
- 请在容器或虚拟机中运行脚本，并确保环境中不包含敏感信息 |
- 使用 OpenClaw 的子代理隔离机制（每个子代理都在独立的进程中运行） |
- 在渲染之前请仔细检查样本文件的代码

**对于您自己编写的样本文件：** 无需特别的安全措施——因为这些文件是由您自己编写的。

这与任何编程语言的运行环境相同。渲染器的安全性取决于您使用的样本文件本身。

### Discord 集成

该技能利用 OpenClaw 的内置 Discord 语音通道功能进行音频传输。**无需单独配置 `BOT_TOKEN`、`DISCORD_TOKEN` 或其他 Discord 凭据**。OpenClaw 负责所有的认证和连接管理。技能只需生成音频文件，然后将其传递给 OpenClaw 的语音传输系统。

### npm 安装注意事项

`package.json` 文件中不包含 `postinstall`、`preinstall` 或生命周期相关的脚本。运行 `npm run setup` 会自动执行 `npm install` 和 `scripts/download-samples.sh`（用于下载样本文件）。

### `scripts/download-samples.sh` 的功能

该脚本会从 GitHub 下载 [tidalcycles/Dirt-Samples](https://github.com/tidalcycles/Dirt-Samples)（CC0 许可）中的样本文件（共 153 个 WAV 文件，总计约 11MB）。脚本具有幂等性（如果样本文件已存在，则不会重复下载）。

### `scripts/samples-manage.sh` 的功能

该脚本会根据用户指定的 URL 下载额外的样本包，并执行以下安全检查：
- **下载大小限制**：可通过 `STRUDEL_MAX_DOWNLOAD_MB` 配置（默认值为 10GB） |
- **主机白名单**：允许的下载主机地址（用逗号分隔；默认允许所有主机） |
- **文件类型验证**：确保下载的文件为音频或压缩文件 |
- **路径安全检查**：确保下载路径不会超出样本目录的范围

## 并发处理

每个会话中最多只能同时进行一个渲染任务。如果用户在另一个渲染任务正在进行时尝试执行 `/strudel clone` 命令：
1. 使用 `subagents(action=list)` 检查是否有正在运行的子代理 |
2. 如果正在渲染音乐，请回复用户：“🎵 正在渲染中，请稍候。” |
3. 禁止同时启动第二个渲染任务——否则可能会导致磁盘和内存竞争，从而引发问题。

**原因：** 如果同时运行多个渲染任务，它们都会写入 `output.wav` 文件，导致文件被覆盖。即使指定了不同的输出路径，两个 `OfflineAudioContext` 进程也会占用相同的内存资源。样本文件的加载是在每个进程中单独进行的（没有共享缓存），因此不会导致文件损坏，但文件写入操作可能会遇到竞争问题。
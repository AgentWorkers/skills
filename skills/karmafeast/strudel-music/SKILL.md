---
name: strudel-music
description: "使用 Strudel 的实时编码模式来创作、播放和渲染音乐。适用于以下场景：通过编程方式创作音乐、从模式代码生成音频、根据情绪或参数创建音乐作品、将音乐文件渲染为 WAV/Opus 格式，或将音乐流式传输到 Discord 的语音频道。该工具支持交互式浏览器播放（strudel.cc）、无头渲染（headless rendering），以及基于结构化输入生成音乐内容。**不适用于**：播放预先录制的音频文件、与音乐理论相关的问题（不涉及创作过程），或使用非 Strudel 的音频工具。"
metadata: { "openclaw": { "emoji": "🎵", "requires": { "bins": ["node", "npx"], "optionalBins": ["ffmpeg", "ffplay"], "description": "Headless rendering requires Node.js and Puppeteer (downloads Chromium). ffmpeg needed for audio format conversion." }, "install": [{ "id": "puppeteer", "kind": "npm", "package": "puppeteer", "global": true, "bins": ["npx"], "label": "Install Puppeteer (headless Chromium for rendering)" }, { "id": "ffmpeg", "kind": "apt", "package": "ffmpeg", "bins": ["ffmpeg", "ffplay"], "label": "Install ffmpeg (audio conversion, optional)" }], "securityNotes": "Headless rendering navigates to https://strudel.cc and evaluates pattern code in the remote page's JS context. Only pass pattern code you trust. For sensitive inputs, use STRUDEL_URL=http://localhost:3000 for local rendering. The render script uses --no-sandbox for container/WSL compatibility." } }
---
# Strudel 音乐

Strudel 是一个基于浏览器运行的实时编码音乐环境（灵感来源于 TidalCycles）。用户可以使用 JavaScript 编写音乐模式，这些模式可以交互式地播放、被渲染成音频文件，或者通过 Discord 的虚拟空间（VC）进行流媒体传输。

## 快速入门

将任何音乐模式粘贴到 [strudel.cc](https://strudel.cc) 中，然后按 Ctrl+Enter 来播放：

```javascript
setcpm(120/4)
stack(
  s("bd sd [bd bd] sd").gain(0.4),
  s("[hh hh] [hh oh]").gain(0.2),
  note("c3 eb3 g3 c4").s("sawtooth").lpf(1200).decay(0.2).sustain(0)
)
```

## 创作工作流程

### 1. 设置节奏
```javascript
setcpm(120/4)  // 120 BPM (cycles per minute = BPM / 4)
```

### 2. 使用 `stack()` 构建音乐层次结构
每个层次结构都代表一个音乐模式——可以是鼓声、贝斯、旋律或效果音。将这些模式堆叠在一起：
```javascript
stack(
  s("bd sd bd sd"),          // kick-snare
  note("c3 g3").s("bass"),   // bassline
  n("0 2 4 7").scale("C:minor").s("piano")  // melody
)
```

### 3. 添加表达式（控制音乐动态）
```javascript
.lpf(sine.range(400, 4000).slow(8))  // sweeping filter
.room(0.5).roomsize(4)               // reverb
.delay(0.3).delaytime(0.25)          // delay
.pan(sine.range(0, 1).slow(7))       // autopan
.gain(0.3)                           // volume
```

### 4. 添加音乐演变机制
```javascript
.every(4, x => x.fast(2))     // double speed every 4 cycles
.sometimes(rev)                 // randomly reverse
.off(0.125, x => x.note(7))   // echo a fifth up
.jux(rev)                      // reverse in right channel
```

## 音乐模式语法快速参考

| 语法 | 含义 | 示例 |
|--------|---------|---------|
| `s("bd sd")` | 播放连续的音样 | 先播放低音鼓（kick），再播放小军鼓（snare） |
| `note("c3 e3 g3")` | 播放音符 | C 大调三和弦 |
| `n("0 2 4").scale("C:minor")` | 播放音阶音 | C 小调音阶 |
| `[a b]` | 将两个事件合并为一个步骤 | 将两个事件同时触发 |
| `<a b c>` | 每个循环交替执行 | 第一个循环执行 A，第二个循环执行 B... |
| `a*3` | 重复执行 | 重复播放三次低音鼓 |
| `~` | 暂停 | 音乐暂停 |
| `.slow(2)` / `.fast(2)` | 调整播放速度 | 速度减半/加倍 |
| `.euclid(3,8)` | 欧几里得节奏 | 在 8 个步骤中播放 3 次 |
| `stack(a, b)` | 同时播放多个模式 | 同时播放 a 和 b 模式 |

## 基于情绪的音乐创作

根据不同的情绪参数生成音乐作品。详细规则请参阅 `references/mood-parameters.md` 文件。

**核心情绪与音乐模式的对应关系：**

| 情绪 | 节奏 | 调性/音阶 | 音乐特征 |
|------|-------|-----------|-----------|
| 紧张 | 60-80 | 小调/弗里吉亚调式 | 低音较强，打击乐较少，持续性的音效 |
| 战斗 | 120-160 | 小调 | 重节奏的鼓声，失真效果，快速的音乐模式 |
| 探索 | 80-100 | 多利安调式/混合利底亚调式 | 开放式的和声结构，延迟效果，中等能量 |
| 平和 | 60-80 | 五声音阶/大调 | 温暖的音色，缓慢的节奏，氛围感强的音乐 |
| 神秘 | 70-90 | 全音阶 | 高音量的混响效果，节奏不规律，充满不确定性 |
| 胜利 | 110-130 | 大调 | 明亮的音色，华丽的旋律，完整的管弦乐编曲 |
| 悲伤 | 48-65 | 小调 | 持续的音效，简单的打击乐 |
| 仪式 | 45-60 | 多利安调式 | 奥尔加ン的持续音效，重复性的音乐模式 |

### 参数化创作

```javascript
// Agent receives parameters:
const mood = "tension"
const intensity = 0.7  // 0-1
const key = "d"
const scale = "minor"

// Derived values:
const cutoff = 200 + (1 - intensity) * 3000
const reverbAmt = 0.4 + intensity * 0.5
const density = intensity > 0.5 ? 2 : 1

setcpm(72/4)
stack(
  note(`${key}1`).s("sawtooth").lpf(cutoff * 0.3).gain(0.15).room(reverbAmt).slow(4),
  n(`<0 3 5 7 5 3>*${density}`).scale(`${key}4:${scale}`).s("triangle")
    .decay(0.5).sustain(0).gain(0.1).lpf(cutoff).room(reverbAmt),
  s(intensity > 0.5 ? "bd ~ [~ bd] ~" : "bd ~ ~ ~").gain(0.2 * intensity)
)
```

## 音频渲染

### 先决条件

无头（headless）渲染需要以下工具：
- **Node.js**（版本 18 及以上）和 **npx**
- **Puppeteer**（通过 `npm install -g puppeteer` 安装）——用于下载 Chromium 可执行文件（约 300MB）
- **ffmpeg**（可选）——用于将音频格式转换为 Opus 或 MP3

### 浏览器中的音频导出（交互式）
在 strudel.cc 中，点击下载图标即可将当前音乐模式导出为 WAV 格式。

### 无头渲染（自动化）
使用 `scripts/render-pattern.sh` 脚本进行无人值守的渲染：
```bash
./scripts/render-pattern.sh input.js output.wav 8 120
# Args: <pattern.js> <output.wav> <cycles> <bpm>
```

> **安全提示：** 该脚本会启动无头的 Chromium 浏览器，访问 `https://strudel.cc`，并在远程页面的 JavaScript 环境中执行你的音乐模式代码。请仅传递你信任的代码。渲染过程中，远程页面会控制执行环境。为了避免依赖远程服务器，请参考“本地渲染”部分。

### 本地渲染（推荐用于处理敏感数据）

为了避免依赖远程的 strudel.cc，你可以将 Strudel 项目克隆到本地：
```bash
git clone https://github.com/tidalcycles/strudel.git
cd strudel && pnpm install && pnpm dev
# Then point render-pattern.sh at localhost:
STRUDEL_URL=http://localhost:3000 ./scripts/render-pattern.sh input.js output.wav 8 120
```

这样所有的执行过程都将在本地完成——无需网络连接，也不会执行任何远程代码。

### 格式转换
```bash
# WAV → Opus (Discord VC)
ffmpeg -i output.wav -c:a libopus -b:a 128k -ar 48000 output.opus

# WAV → MP3
ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3
```

### Discord 虚拟空间（VC）流媒体传输流程
Strudel 会将音乐模式渲染为 Opus 格式，并通过相应的桥接工具（如 `openclaw-discord-vc-bootstrap`）传输到 Discord 虚拟空间。该技能不负责管理 Discord 机器人的令牌或桥接配置——这些信息需要单独在桥接工具中进行设置。

详细架构请参阅 `references/integration-pipeline.md` 文件。

## 元数据规范

每个音乐作品的开头都应添加元数据注释：
```javascript
// @title  My Composition
// @by     Author
// @mood   tension|combat|exploration|peace|mystery|victory|sorrow|ritual
// @tempo  120
// @scene  Optional narrative context
```

## 可视化功能

Strudel 支持可视化输出，有助于调试和展示音乐作品：
```javascript
// Pianoroll (notes over time)
._pianoroll({ smear: 0.5, active: "#ff0", background: "#111" })

// Spiral (radial note display)
._spiral({ thickness: 20, stroke: "#0ff" })

// Waveform scope
._scope({ color: "#0f0", lineWidth: 2 })
```

## 资源目录

### scripts/
- `render-pattern.sh` — 使用无头 Chromium 和 Puppeteer 将单个音乐模式渲染为 WAV 文件

### references/
- `mood-parameters.md` — 完整的情绪参数决策树（8 种情绪类型、转换规则、主题旋律系统）
- `integration-pipeline.md` — 无头渲染到 Discord 虚拟空间的架构
- `pattern-transforms.md` — 深入介绍各种模式转换语法（如 `.off`、`.jux`、`.sometimes`、`.euclid`）

### assets/
- `compositions/` — 各种情绪类型的示例音乐作品（氛围音乐、动作音乐、神秘音乐、仪式音乐等）
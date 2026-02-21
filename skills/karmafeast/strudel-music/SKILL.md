---
name: strudel-music
description: "使用 Strudel 的实时编码模式来创作、播放和渲染音乐。适用于通过编程方式创作音乐、从模式代码生成音频、基于情绪创作音乐作品、将音乐模式渲染为 WAV/Opus 格式，或通过 Discord 的语音频道流式传输音乐。该工具支持交互式浏览器播放（strudel.cc）、无头渲染（headless rendering），以及根据结构化输入参数生成音乐内容。**不适用于以下场景**：播放预先录制的音频文件、与音乐理论相关的问题（不涉及创作过程），或使用非 Strudel 的音频工具。"
---
# Strudel 音乐

Strudel 是一个基于浏览器的实时编码音乐环境（灵感来源于 TidalCycles），用户可以使用 JavaScript 编写音乐模式，并能够进行交互式演奏、将音频文件导出，或通过 Discord 的虚拟现实（VC）功能进行流媒体播放。

## 快速入门

将任何音乐模式粘贴到 [strudel.cc](https://strudel.cc) 中，然后按 Ctrl+Enter 播放：

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

### 2. 使用 `stack()` 构建音乐层次
每个层次代表一个音乐模式——可以是鼓声、贝斯、旋律或效果。将它们叠加在一起：
```javascript
stack(
  s("bd sd bd sd"),          // kick-snare
  note("c3 g3").s("bass"),   // bassline
  n("0 2 4 7").scale("C:minor").s("piano")  // melody
)
```

### 3. 添加表达效果
```javascript
.lpf(sine.range(400, 4000).slow(8))  // sweeping filter
.room(0.5).roomsize(4)               // reverb
.delay(0.3).delaytime(0.25)          // delay
.pan(sine.range(0, 1).slow(7))       // autopan
.gain(0.3)                           // volume
```

### 4. 添加动态变化
```javascript
.every(4, x => x.fast(2))     // double speed every 4 cycles
.sometimes(rev)                 // randomly reverse
.off(0.125, x => x.note(7))   // echo a fifth up
.jux(rev)                      // reverse in right channel
```

## 音乐模式语法快速参考

| 语法 | 含义 | 示例 |
|--------|---------|---------|
| `s("bd sd")` | 播放连续的音样 | 先播放低音鼓，再播放军鼓 |
| `note("c3 e3 g3")` | 播放音符 | C 大调三和弦 |
| `n("0 2 4").scale("C:minor")` | 播放音阶音符 | C 小调音阶 |
| `[a b]` | 将两个事件合并为一个步骤 | 将两个事件同时触发 |
| `<a b c>` | 每个周期交替执行 | 第一个周期执行 A，第二个周期执行 B... |
| `a*3` | 重复执行 | 重复三次低音鼓的音效 |
| `~` | 暂停 | 静音 |
| `.slow(2)` / `.fast(2)` | 调整播放速度 | 速度减半/加倍 |
| `.euclid(3,8)` | 欧几里得节奏 | 在 8 个步骤中播放 3 次音效 |
| `stack(a, b)` | 同时播放多个模式 | 同时播放 a 和 b 模式 |

## 基于情绪的创作

根据情绪参数生成音乐作品。详细规则请参阅 `references/mood-parameters.md`。

核心情绪与音乐模式的对应关系：

| 情绪 | 节奏 | 调性/音阶 | 音乐特征 |
|------|-------|-----------|-----------|
| 紧张 | 60-80 | 小调/弗里吉亚调 | 低音效果明显，节奏稀疏 |
| 战斗 | 120-160 | 小调 | 强烈鼓点，失真效果，快速节奏 |
| 探索 | 80-100 | 多利安调/混合利底亚调 | 开放式的音色排列，延迟效果，中等能量 |
| 和平 | 60-80 | 五声音阶/大调 | 温暖的音色，缓慢的节奏 |
| 神秘 | 70-90 | 全音阶 | 高混响效果，节奏不规则 |
| 胜利 | 110-130 | 大调 | 明亮的音色，华丽的旋律，完整的管弦乐编曲 |
| 悲伤 | 48-65 | 小调 | 持续的背景音效，简单的打击乐 |
| 仪式 | 45-60 | 多利安调 | 奥尔加ン的低音效果，重复的旋律 |

### 参数化生成

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

### 浏览器导出（交互式）
在 strudel.cc 中，点击下载图标将当前模式导出为 WAV 文件。

### 无人值守渲染
使用 `scripts/render-pattern.sh` 脚本进行自动渲染：
```bash
./scripts/render-pattern.sh input.js output.wav 8 120
# Args: <pattern.js> <output.wav> <cycles> <bpm>
```

### 格式转换
```bash
# WAV → Opus (Discord VC)
ffmpeg -i output.wav -c:a libopus -b:a 128k -ar 48000 output.opus

# WAV → MP3
ffmpeg -i output.wav -c:a libmp3lame -q:a 2 output.mp3
```

### 通过 Discord VC 流媒体播放
```
Pattern code → Headless browser + Strudel REPL → renderPatternAudio()
→ WAV buffer → ffmpeg → Opus → Discord VC bridge
```

完整的技术架构请参阅 `references/integration-pipeline.md`。

## 元数据规范

每首音乐的开始处都需要添加元数据注释：
```javascript
// @title  My Composition
// @by     Author
// @mood   tension|combat|exploration|peace|mystery|victory|sorrow|ritual
// @tempo  120
// @scene  Optional narrative context
```

## 可视化功能

Strudel 支持可视化输出，便于调试和展示：
```javascript
// Pianoroll (notes over time)
._pianoroll({ smear: 0.5, active: "#ff0", background: "#111" })

// Spiral (radial note display)
._spiral({ thickness: 20, stroke: "#0ff" })

// Waveform scope
._scope({ color: "#0f0", lineWidth: 2 })
```

## 资源

### scripts/
- `render-pattern.sh` — 使用无头 Chromium 和 Puppeteer 将单个音乐模式渲染为 WAV 文件

### references/
- `mood-parameters.md` | 完整的情绪参数决策树（8 种情绪类型、转换规则、主题旋律系统）
- `integration-pipeline.md` | 无人值守渲染到 Discord VC 流媒体的技术架构
- `pattern-transforms.md` | 关于 `.off`, `.jux`, `.every`, `.sometimes`, `.euclid` 等模式的详细说明

### assets/
- `compositions/` | 各种情绪类别的示例音乐作品（环境音、动作音效、神秘氛围、仪式音乐等）
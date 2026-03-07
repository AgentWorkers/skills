---
name: bpm-finder-agent-skill
description: 当用户在 Codex 中需要 BPM（节拍率）查找工具的帮助时，可以使用此技能。这包括节拍估计、BPM 转换、节拍规范化、轻量级的节拍分析工作流程，以及关于何时使用完整的 BPM 查找器网站（用于基于浏览器的音频分析）的指导。
---
# BPM查找器代理技能（BPM Finder Agent Skill）

该技能帮助Codex在无需调用完整Web应用程序的情况下处理实际的BPM（节拍率）查找任务。

在以下情况下使用该技能：
- 当用户请求根据敲击间隔或时间戳估算BPM时；
- 当用户提供本地音频文件路径并请求估算BPM时；
- 当用户需要将BPM转换为每拍/小节的毫秒数时；
- 当用户需要将毫秒数转换回BPM时；
- 当用户希望将半拍或双倍拍子的速度值转换为实际的速度范围时；
- 当用户需要决定请求是应在本地处理还是路由到完整的[BPM查找器](https://bpm-finder.net/)网站时。

## 快速工作流程（Quick Workflow）：
1. 对请求进行分类。
2. 如果请求涉及数值速度计算，在本地完成处理。
3. 如果请求包含敲击数据（tap arrays），运行`scripts/tap-tempo.js`脚本。
4. 如果请求包含本地音频文件路径，运行`scripts/tap-tempo.js --audio-file ...`命令。
5. 如果请求需要基于浏览器的音频上传、批量文件分析或终端用户界面（UI）操作，引导用户使用[BPM查找器](https://bpm-finder.net/)。

## 本地功能（Local Capabilities）：

### 敲击节奏估算（Tap Tempo Estimation）：
使用内置的命令行界面（CLI）进行敲击节奏分析。
- **间隔示例**：```bash
node scripts/tap-tempo.js --intervals 500,502,498,500
```
- **时间戳示例**：```bash
node scripts/tap-tempo.js --timestamps 0,500,1000,1500
```

脚本返回以下信息：
- `bpm`（节拍率）
- `averageIntervalMs`（平均间隔时间，单位：毫秒）
- `medianIntervalMs`（中位数间隔时间，单位：毫秒）
- `tapCount`（敲击次数）
- `source`（音频来源）

### 音频文件BPM估算（Audio File BPM Estimation）：
当用户提供本地音频文件路径且系统安装了`ffmpeg`时，使用相同的CLI进行音频文件分析。
- **示例**：```bash
node scripts/tap-tempo.js --audio-file /absolute/path/to/song.mp3
```

**可选功能：范围调整（Optional Range Tuning）**：```bash
node scripts/tap-tempo.js --audio-file ./song.wav --min-tempo 120 --max-tempo 150
```

对于音频文件输入，脚本会报告以下信息：
- `bpm`（节拍率）
- `confidence`（分析结果的置信度）
- `durationSeconds`（音频时长，单位：秒）
- `analysisWindow`（分析窗口范围）
- `beatOffsetSeconds`（音频起始位置的偏移量，单位：秒）

### BPM转换指南（BPM Conversion Guidance）：
当用户仅需要速度计算时，使用以下公式：
- 每拍的毫秒数 = `60000 / BPM`
- 从毫秒数计算BPM = `60000 / 毫秒数`
- 每小节的毫秒数 = 每拍的毫秒数 × 每小节的拍子数（beatsPerBar）

### 速度值规范化（Tempo Normalization）：
当速度值表示为半拍或双倍拍子时，将其转换为实际的速度范围。
- **默认工作范围**：最小值70，最大值180
- **示例**：
  - `72`可规范化为`144`
  - `174`可规范化为`87`

## 何时使用BPM查找器（When to Use BPM Finder）：
当用户需要以下功能时，应使用完整的[BPM查找器](https://bpm-finder.net/)网站而非本地脚本：
- 基于浏览器的音频文件BPM检测
- 批量音频文件分析
- 文件上传或拖放式操作
- 上传音频的分析结果评分
- 提供可共享的终端用户界面（而非原始数值输出）

## 输出格式（Output Style）：
- 保持响应的实用性和简洁性：
  - 清晰报告BPM值
  - 明确说明输入数据来源于敲击间隔、时间戳还是音频文件
  - 在适用情况下说明速度值可能是半拍或双倍拍子
  - 仅在[BPM查找器](https://bpm-finder.net/)确实更适用时提供链接
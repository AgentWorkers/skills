---
name: llm-video-generator
description: 使用 ZhipuAI CogVideoX-3 模型根据文本描述生成视频。支持文本转视频、图片转视频以及从第一帧或最后一帧生成视频的功能。该模型能够自动处理时长超过 5 秒的视频，通过多次生成请求并利用最后一帧的内容进行连续处理来实现这一目标。适用于用户需要根据文本创建视频、将文本转换为视频，或任何涉及将文本/图片转换为视频的任务。同时支持配置视频内容、风格、分辨率（最高可达 4K）、帧率（30/60fps）、音频以及视频时长等参数。
---
# LLM 视频生成器

该工具通过 ZhipuAI CogVideoX-3 生成视频。每次 API 调用可生成约 5 秒的视频。对于较长的视频，可以通过使用“最后一帧续传”功能多次调用 API，然后将生成的片段拼接在一起。

## 脚本

所有脚本均使用 `/opt/anaconda3/bin/python3` 运行。`<skill-dir>` 表示当前技能的目录。

| 脚本 | 功能 |
|--------|---------|
| `scripts/video_gen.py` | 核心视频生成功能（支持 3 种模式：text2video、image2video、frames2video） |
| `scripts/extract_last_frame.py` | 从视频中提取最后一帧（用于后续片段生成） |
| `scripts/concat_videos.py` | 将多个视频片段合并成一个完整的视频 |

## 工作流程

### 第 1 步：评估请求并明确需求

- **请求明确** → 进入第 2 步。当以下条件满足时，请求被视为明确：
  - 视频内容或场景描述足够详细；
  - 视频的风格或视觉效果已明确指定或可推断；
  - 视频时长已给出（未指定时默认为 5 秒）。
- **请求不明确** → 先与用户沟通，制定生成方案：

```
基于你的需求，我拟定了以下视频方案：

📹 **视频内容**: [detailed scene description with key moments]
🎨 **视频风格**: [e.g., 写实/动画/电影感/温馨...]
⏱️ **视频时长**: [Xs, note: will be generated in 5s segments]
🔊 **背景音乐**: 有/无
📐 **分辨率**: 1920x1080
🎞️ **帧率**: 30fps

你觉得这个方案可以吗？需要调整哪些部分？
```

与用户反复沟通，直到需求明确为止。

### 第 2 步：估算生成时间并通知用户

在开始生成视频之前，先计算并告知用户预计的生成时间：

**时间估算公式：**
- 基础时间：每秒视频时长为 1 分钟（例如，20 秒的视频大约需要 20 分钟）；
- 高清视频（4K 或 60fps）：时间增加 30%（例如，20 秒的 4K 视频大约需要 26 分钟）；
- 额外开销：视频提取、拼接和压缩大约需要 2 分钟；
- 视频片段数量：`ceil(目标时长 / 5)`。

**在开始生成之前，必须向用户发送以下信息：**

```
⏳ **视频生成预估**

📊 分段计划：{N} 段（每段约5秒）
⏱️ 预计总耗时：约 {estimated_minutes} 分钟
📐 分辨率：{resolution}

视频生成是一个耗时过程，请耐心等待。我会在每段完成后实时汇报进度。
```

**示例：**
- 30 秒、1080P 分辨率的视频：
  - 需要 6 个片段，基础时间为 30 分钟，额外开销 2 分钟 → 总耗时约 32 分钟。
- 20 秒、4K 分辨率的视频：
  - 需要 4 个片段，基础时间为 20 × 1.3 = 26 分钟，额外开销 2 分钟 → 总耗时约 28 分钟。

### 第 3 步：规划视频片段

每次 API 调用生成约 5 秒的视频。计算所需片段的数量：`ceil(目标时长 / 5)`。

对于多片段视频，需要规划每个片段的内容，并为每个片段编写提示，描述该片段中的具体内容，以确保视觉连贯性。

### 第 4 步：执行视频生成并实时反馈进度

**重要提示：** 每个片段生成完成后，必须立即向用户发送进度信息，然后再开始下一个片段的生成。切勿等到所有片段都生成完毕才发送进度信息。

**进度信息格式（可通过消息工具或回复发送）：**

```
✅ 进度：{completed}/{total} 段完成（第{N}段已生成）
📝 内容：{brief segment description}
⏱️ 本段耗时：{minutes}分钟
📊 预计剩余：约 {remaining_minutes} 分钟
```

**生成过程：**

**片段 1 — 文本转视频：**

```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py text2video \
  --prompt "<segment_1_prompt>" \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir> --max-wait 900
```

→ **向用户发送进度信息**

**片段 2+ — 图像转视频（使用上一片段的最后一帧进行续传）：**

对于每个后续片段：
1. 从上一个片段的视频中提取最后一帧：
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/extract_last_frame.py \
  <previous_video.mp4> --output <output-dir>/frame_segN.png
```

2. 使用提取的最后一帧作为输入生成新的片段：
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py image2video \
  --prompt "<segment_N_prompt>" \
  --image-url <output-dir>/frame_segN.png \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir> --max-wait 900
```

3. **向用户发送进度信息**

重复上述步骤，直到所有片段生成完毕。

**另一种方式 — 使用起始和结束图像生成视频：**

如果用户提供了片段的起始和结束图像，可以使用以下方式：
```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/video_gen.py frames2video \
  --prompt "<description>" \
  --first-frame <first.png> --last-frame <last.png> \
  --quality quality --audio true --size 1920x1080 --fps 30 \
  --output-dir <output-dir>
```

### 第 5 步：合并所有片段

所有片段生成完成后，将它们合并成一个完整的视频文件：

```bash
/opt/anaconda3/bin/python3 <skill-dir>/scripts/concat_videos.py \
  --inputs <seg1.mp4> <seg2.mp4> ... \
  --output <output-dir>/final_video.mp4
```

如果生成的文件大小超过 Feishu 的上传限制（25MB），可以使用 ffmpeg 进行压缩：
```bash
ffmpeg -i <input> -c:v libx264 -crf 32 -c:a aac -b:a 96k -vf "scale=1280:720" -y <output>
```

### 第 6 步：交付结果

- 将生成的视频文件分享给用户；
- 使用 `feishu-send-file` 技能将视频文件上传到 Feishu；
- 提供最终结果报告：

```
🎬 **视频生成完成！**

⏱️ 总时长：{duration}秒
📦 文件大小：{size}MB
📊 共 {N} 段，总耗时 {total_minutes} 分钟
```

## 提示技巧

- 使用 **英文提示** 以获得最佳生成效果；
- 提示内容要具体明确：包括场景、拍摄角度、光线、动作、氛围等；
- 使用相关的风格关键词（如“电影风格”、“写实”、“卡通”、“水彩风格”等）；
- 对于续传片段，只需描述动作的进展，无需从头开始描述整个场景；
- 每个片段的提示应简洁明了（1-3 句）。

## 参数参考

| 参数 | 标志 | 默认值 | 可选值 |
|-----------|------|---------|---------|
| 提示内容 | `--prompt` | （必填） | 视频生成的描述性文本 |
| 视频质量 | `--quality` | `quality` | `quality` 或 `speed` |
| 是否包含音频 | `--audio` | `true` | `true` 或 `false` |
| 分辨率 | `--size` | `1920x1080` | `1280x720`, `1920x1080`, `3840x2160` |
| 帧率 | `--fps` | `30` | `30` 或 `60` |
| 输出目录 | `--output-dir` | `.` | 任何可写入的目录 |
| 进度检查间隔 | `--poll-interval` | `10` | 秒 |
| 最大等待时间 | `--max-wait` | `900` | 秒（默认值，用于提高稳定性） |

## 错误处理

- **缺少 ZHIPU_API_KEY**：请用户设置相应的环境变量；
- **缺少 zai-sdk**：在 anaconda 环境中运行 `pip install zai-sdk`；
- **缺少 ffmpeg**：用于视频提取和拼接操作；
- **任务超时**：增加 `--max-wait` 的值或重新尝试；可通过 API 手动检查任务状态；
- **任务失败**：简化提示内容并重新尝试；
- **文件过大无法上传到 Feishu**：使用 ffmpeg 进行压缩（降低分辨率或调整 CRF 值）。
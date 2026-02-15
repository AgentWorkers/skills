---
name: ai-podcast-pipeline
version: 0.1.5
description: 根据 QuickView 的趋势分析结果，生成适用于韩国市场的 AI 播客包。这些播客包可用于编写双主持人脚本（Callie × Nick）、生成 Gemini 多声道 TTS 音频、调整字幕的显示时机与渲染效果、制作包含缩略图和 MP4 文件的播客包，以及生成 YouTube 的标题和描述信息。该系统支持制作时长为 15~20 分钟的完整版播客包，也支持压缩后的 5~7 分钟版本。
---

# 人工智能播客制作流程

## ⚠️ 安全提示

由于以下合法操作，本技能可能会触发防病毒软件的误报：
- **base64解码**：仅用于从Gemini TTS API响应中解码音频数据（这是处理JSON中的二进制数据的标准做法）。
- **子进程调用**：仅用于调用ffmpeg进行音频/视频处理。
- **环境变量**：从用户配置的环境变量`GEMINI_API_KEY`中读取API密钥。
- **网络请求**：向Google Gemini API发起请求以生成文本转语音。

所有代码均为开源，可在本仓库中审核。不存在任何恶意行为。

本流程用于从`Trend/QuickView-*`内容中生成端到端的播客资源。

## 核心工作流程

1. 选择源QuickView文件。
2. 生成脚本（全模式或压缩模式）。
3. 制作双声道MP3文件（使用Gemini的多语音功能，并分块处理以确保可靠性）。
4. 生成完整的韩文字幕（不进行省略处理）。
5. 渲染带有自定义字体、字号和字幕时间延迟的MP4文件。
6. 生成缩略图及YouTube元数据。
7. 提供最终成品。

## 第1步）选择源文件

优先选择来自配置好的Quartz根目录的每周更新一次的QuickView文件。

如果用户提供了`wk.aiee.app`这样的URL，请先将其映射到本地的Quartz Markdown文件。

## 第2步）生成脚本

读取并应用`references/podcast_prompt_template_ko.md`中的模板。

**模式**：
- **全模式**：时长15~20分钟
- **压缩模式**：时长5~7分钟（仅包含核心提示）

**规则**：
- 语音台词中不得包含系统或元数据信息。
- 开场时仅播放一次主持人介绍语。
- 使用简洁的韩语对话句式，内容具有实用性。
- 将生成的脚本保存到`archive/`目录中。

## 第3步）制作音频（使用Gemini的多语音功能，确保可靠性）

### 推荐使用的分块处理方式（可防止超时）
```bash
# Set API key via environment (required)
export GEMINI_API_KEY="<YOUR_KEY>"

# Run from skills/ai-podcast-pipeline/
python3 scripts/build_dualvoice_audio.py \
  --input <script.txt> \
  --outdir <outdir> \
  --basename podcast_full_dualvoice \
  --chunk-lines 6
```

### 单次处理方式（适用于简短脚本）
```bash
python3 scripts/gemini_multispeaker_tts.py \
  --input-file <dialogue.txt> \
  --outdir <outdir> \
  --basename podcast_dualvoice \
  --retries 3 \
  --timeout-seconds 120
```

**默认语音配置（2026-02-10更新）**：
- Callie（女性角色） → 使用语音“Kore”
- Nick（男性角色） → 使用语音“Puck”

**输出格式**：MP3（默认交付格式）

## 第4步）生成韩文字幕（包含完整文本内容）

使用支持完整文本的字幕生成工具（不进行省略处理）：
```bash
python3 scripts/build_korean_srt.py \
  --script <script.txt> \
  --audio <final.mp3> \
  --output <outdir>/podcast.srt \
  --max-chars 22
```

## 第5步）渲染带字幕的MP4文件（调整字体和字幕时间）

使用支持字体和字幕时间延迟的渲染工具：
```bash
python3 scripts/render_subtitled_video.py \
  --image <thumbnail.png> \
  --audio <final.mp3> \
  --srt <podcast.srt> \
  --output <outdir>/final.mp4 \
  --font-name "Do Hyeon" \
  --font-size 27 \
  --shift-ms -250
```

**注意事项**：
- `shift-ms`参数为负值时，字幕会提前显示（用于解决显示延迟问题）。
- 如果出现文本裁剪现象，可减小字体大小（例如25~27像素）。
- 确保文本显示在安全区域内，避免与字符或对象重叠。

## 第6步）生成缩略图及YouTube元数据

**参考指南**：`references/thumbnail_guidelines_ko.md`

## 第7步）最终交付检查清单

务必包含以下信息：
1. 使用的源文件。
2. 最终生成的MP3文件路径。
3. 带字幕的MP4文件路径及文件大小。
4. 缩略图路径。
5. YouTube标题选项（3种可选格式）。
6. YouTube描述内容。

## 可靠性保障措施

- 对于较长的输入内容，Gemini API可能会超时，此时请使用分块处理方式（`build_dualvoice_audio.py`）。
- 如果字幕出现裁剪现象，可减小字体大小并增加字幕下方的空白距离。
- 如果字幕显示有延迟，可调整`--shift-ms`参数（通常范围为-150至-300）。
- 确保生成的文件大小在Telegram允许的范围内。

## 安全注意事项

- API密钥必须通过环境变量`GEMINI_API_KEY`传递，切勿硬编码。
- 绝不要将密钥粘贴到提示信息、日志文件、截图或公开内容中。
- 最近的改进措施：缩略图生成过程已通过环境变量传递密钥，而非命令行参数。

## 参考资料

- `references/podcast.prompt_template_ko.md`
- `references/workflow_runbook.md`
- `references/thumbnail_guidelines_ko.md`
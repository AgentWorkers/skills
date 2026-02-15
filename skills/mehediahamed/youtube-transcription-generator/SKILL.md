---
name: youtube-transcription-generator
description: "使用 VLM Run (vlmrun) 从 YouTube 视频中生成字幕。首先使用 yt-dlp 下载视频，然后运行 vlmrun 进行字幕生成（可选添加时间戳）。VLMRUN_API_KEY 必须存储在 `.env` 文件中；有关 CLI 的设置和选项，请参考 vlmrun-cli-skill 文档。"
---

## YouTube 字幕生成器（使用 vlmrun）

使用 **vlmrun** 从 YouTube 视频生成字幕，同时支持添加时间戳。该技能包括以下步骤：

1. 使用 **yt-dlp** 下载 YouTube 视频（或仅下载音频）。
2. 使用 **vlmrun**（Orion 视觉 AI）对视频进行转录。
3. 将生成的字幕保存为文件（纯文本格式或包含时间戳的格式）。

有关 **vlmrun** 的 CLI 设置、环境变量以及所有 `vlmrun` 命令选项的详细信息，请参考 **vlmrun-cli-skill**。

---

## 助手应如何使用此技能

- **检查 `.env` 文件中的 API 密钥**
  - 确保 `.env`（或 `.env.local`）文件中包含 `VLMRUN_API_KEY`。
  - 如果缺失，请在运行任何 `vlmrun` 命令之前指导用户设置该密钥。

- **仅使用 vlmrun 进行转录**
  - 要进行转录（并可选地添加时间戳），请使用 `vlmrun` CLI，并提供视频文件作为输入（格式：`-i <video>`）。
  `vlmrun` 支持多种视频格式（例如 `.mp4`）。对于 YouTube 视频，该技能会先使用 **yt-dlp** 下载视频，然后再将其传递给 `vlmrun` 进行转录。

- **工作流程**
  - 用户提供 YouTube 视频的 URL（以及可选的输出路径）。
  - 使用 **yt-dlp** 下载视频（或仅下载音频以加快下载速度或减小文件大小）。
  - 运行命令：`vlmrun chat "为该视频添加时间戳，并以清晰易读的格式输出完整字幕。" -i <下载的文件> -o <输出目录>`。
  - 将 `vlmrun` 的输出结果保存为字幕文件（例如 `transcript.txt`）。

---

## 先决条件

- **Python 3.10 或更高版本**
- **VLMRUN_API_KEY**（用于 `vlmrun`）
- **vlmrun CLI**（`vlmrun[cli]`）
- **yt-dlp**（用于下载 YouTube 视频）

> 有关 `vlmrun` 的详细使用方法和示例，请参阅 **vlmrun-cli-skill**。

---

## 安装与配置

在 `youtube-transcription-generator` 目录下：

**Windows（PowerShell）：**

```powershell
cd path\to\youtube-transcription-generator
uv venv
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

**macOS/Linux：**

```bash
cd path/to/youtube-transcription-generator
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

将 `.env_template` 复制到 `.env` 文件中，并设置 `VLMRUN_API_KEY`。

---

## 快速入门：转录 YouTube 视频

### 选项 A：运行脚本（推荐）

```bash
# From youtube-transcription-generator directory, with venv activated
python scripts/run_transcription.py "https://www.youtube.com/watch?v=VIDEO_ID" -o ./output
```

此操作将：
1. 使用 `yt-dlp` 将视频下载到指定的输出目录。
2. 运行 `vlmrun` 对视频进行转录。
3. 将生成的字幕保存为 `output/transcript.txt`（相关文件保存在 `output/` 目录中）。

### 选项 B：手动下载视频后使用 vlmrun**

```bash
# 1) Download with yt-dlp
yt-dlp -f "bv*[ext=mp4]+ba/best[ext=mp4]/best" -o video.mp4 "https://www.youtube.com/watch?v=VIDEO_ID"

# 2) Transcribe with vlmrun (see vlmrun-cli-skill for options)
vlmrun chat "Transcribe this video with timestamps for each section. Output the full transcript in a clear, readable format." -i video.mp4 -o ./output
```

将 `vlmrun` 的输出结果捕获并保存为字幕文件；如果需要结构化输出，可以使用 `--json` 选项。

---

## `vlmrun` 的命令提示语示例

- **包含时间戳：**
  `"为该视频添加时间戳，并以清晰易读的格式输出完整字幕。"`

- **仅生成纯文本字幕：**
  `"转录视频中的所有内容。仅输出语音文本，不包含时间戳。"

- **结构化输出（例如 JSON 格式）：**
  使用 `--json` 选项，并指定所需的输出格式（例如：`[{"time": "...", "text": "..."}` 的列表）。

---

## 工作流程检查清单

- [ ] 确保已安装 `vlmrun` 并设置了 `VLMRUN_API_KEY`（请参考 vlmrun-cli-skill）。
- [ ] 安装所需依赖项：`uv pip install -r requirements.txt`（包括 `vlmrun[cli` 和 `yt-dlp`）。
- [ ] 运行命令：`python scripts/run_transcription.py <youtube_url> -o ./output`，或手动下载视频后使用 `vlmrun`。
- [ ] 在输出目录（例如 `output/`）中查找字幕文件（例如 `output/transcript.txt`）。

---

## 常见问题及解决方法

- **找不到 vlmrun**  
  激活虚拟环境（venv），然后运行：`uv pip install "vlmrun[cli]"`。详情请参阅 vlmrun-cli-skill。
- **身份验证错误**  
  确认 `.env` 文件或当前 shell 中的 `VLMRUN_API_KEY` 是否正确。
- **yt-dlp 下载失败**  
  更新 `yt-dlp`：`uv pip install -U yt-dlp`。请检查提供的 URL 是否为有效的 YouTube 视频链接。
- **视频文件过大或过长**  
  在脚本中选择仅下载音频（例如使用 `-f bestaudio` 选项）以减小文件大小并加快转录速度。
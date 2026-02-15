---
name: veo3-video-gen
description: 使用 Gemini API (google-genai) 通过 Google Veo 3.x 生成并拼接短视频。当您需要根据提示创建视频片段（如广告、用户生成内容风格的视频片段、产品演示等），并且希望拥有一个可复制的命令行界面（CLI）工作流程时（包括生成、投票、下载 MP4 文件，以及可选的多段视频拼接功能），请使用此方法。
---

# Veo 3 视频生成（Gemini API）

使用随附的脚本，根据文本提示生成 MP4 视频。

## 从文本生成视频

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "A close up of ..." \
  --filename "out.mp4" \
  --model "veo-3.1-generate-preview" \
  --aspect-ratio "9:16" \
  --poll-seconds 10
```

## 通过拼接多个片段来生成更长的视频

Veo 通常每次请求会生成约 8 秒的片段。可以使用 `--segments` 选项生成多个片段，然后使用 ffmpeg 将它们合并在一起。

**重要提示：** 每个片段需要提供一个单独的提示（即每次请求都需要发送一个 Veo 请求）。使用 `--base-style` 选项可以确保所有片段的风格保持一致。

```bash
uv run {baseDir}/scripts/generate_video.py \
  --prompt "Same scene, consistent style..." \
  --filename "out-24s.mp4" \
  --model "veo-3.1-generate-preview" \
  --aspect-ratio "9:16" \
  --segments 3 \
  --segment-style continuation
```

可选参数：
- `--base-style "..."`：添加到每个片段的提示前面（推荐使用）。
- `--segment-prompt "..."`（可重复使用）：为每个片段提供一个提示（会覆盖 `--prompt` 的设置）。
- `--segment-style continuation`（默认值）：为每个片段添加连续性提示（仅在使用 `--prompt` 时生效）。
- `--segment-style same`：为每个片段使用完全相同的提示（仅在使用 `--prompt` 时生效）。
- `--use-last-frame`：对于包含多个片段的视频，提取前一个片段的最后一帧，并将其作为 `lastFrame` 用于保持视频的连续性。
- `--emit-segment-media`：在每个片段生成完成后输出 `MEDIA:` 信息（有助于监控生成进度）。
- `--keep-segments`：保留中间的 `.segXX.mp4` 文件。
- `--reference-image path.jpg`（可重复使用）：提供产品/风格的参考图片以指导视频生成过程。

## 使用要求：
- 必须设置环境变量 `GEMINI_API_KEY`（或使用 `--api-key`）。
- 当使用 `--segments > 1` 时，确保 `ffmpeg` 已添加到系统的 PATH 环境变量中。

## 常见问题解决方法：
- 429/RESOURCE_EXHAUSTED：API 密钥没有用于视频生成的配额或计费权限。
- 503/UNAVAILABLE：模型当前处于过载状态，请稍后重试。
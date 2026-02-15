---
name: remotion-excalidraw-tts
description: **使用文本转语音功能（macOS系统）从Excalidraw图表生成带解说的Remotion视频，并将其渲染为MP4格式。**  
该功能适用于制作讲解型视频：可以在视频中实现图表的平移/缩放操作，并对关键部分进行高亮显示；同时，系统会自动生成语音解说，最后通过Remotion的命令行界面（CLI）将视频文件渲染完成。
---

# Remotion + Excalidraw + TTS（本地）

使用此技能，您可以将**Excalidraw**图表和**旁白脚本**转换为渲染后的**MP4**文件，具体步骤如下：

- 使用**Remotion**进行渲染。
- 直接使用**Excalidraw**工具将图表导出为`.excalidraw` JSON格式的文件。
- 通过**macOS 的 `say` 命令**实现语音合成（无需网络连接）。

## 快速入门（一个命令）

运行以下命令：

```bash
python3 skills/remotion-excalidraw-tts/scripts/make_video.py \
  --diagram /absolute/path/to/diagram.excalidraw \
  --voiceover-text /absolute/path/to/voiceover.txt \
  --out /absolute/path/to/out.mp4
```

**可选：** 通过 `storyboard.json` 文件控制相机移动、焦点调整和字幕显示：

```bash
python3 skills/remotion-excalidraw-tts/scripts/make_video.py \
  --diagram /absolute/path/to/diagram.excalidraw \
  --voiceover-text /absolute/path/to/voiceover.txt \
  --storyboard-json /absolute/path/to/storyboard.json \
  --out /absolute/path/to/out.mp4
```

该脚本的功能包括：
1. 从 `assets/template/remotion-project/` 目录复制 Remotion 模板项目到临时工作目录。
2. 将图表文件写入 `public/diagram.excalidraw`。
3. 使用 `say` 命令和 `ffmpeg` 工具生成 `public/voiceover.mp3` 音频文件。
4. 根据旁白内容的长度调整视频的播放时长。
5. 使用 `npx remotion render` 命令将渲染后的图表和音频合并为 MP4 文件。

## 输入参数：
- `--diagram`：来自 Excalidraw 的 `.excalidraw` JSON 文件。
- `--voiceover-text`：包含旁白内容的纯文本文件（支持中文）。
- **可选参数：**
  - `--voiceover-mp3`：如果已有音频文件，则跳过语音合成步骤。
  - `--tts-backend`：可选的语音合成服务，包括 `say`（默认）、`openai` 或 `elevenlabs`。
  - `--fps`：视频帧率，默认值为 30 帧/秒。

**语音合成服务说明：**
- **macOS say**：`--tts-backend say --voice Tingting --rate 220`（使用 macOS 的 `say` 命令，设置语音为“Tingting”，语速为 220 字/秒）。
- **OpenAI**：`--tts-backend openai --openai-model gpt-4o-mini-tts --openai-voice alloy`（需要 `OPENAI_API_KEY`）。
- **ElevenLabs**：`--tts-backend elevenlabs --elevenlabs-voice-id <voiceId> --elevenlabs-model eleven_multilingual_v2`（需要 `ELEVENLABS_API_KEY`）。

## 自定义场景（平移、缩放、高亮显示）：
- **选项 A：** 编辑 TypeScript 格式的 `storyboard` 文件。
  - 模板文件位于：`assets/template/remotion-project/src/video/storyboard/storyboard.ts`。
  - 可自定义的场景参数包括：
    - `cameraFrom/cameraTo`（指定相机的移动位置和缩放比例）。
    - `focus`（指定文本框的位置、大小及标签内容）。
    - `subtitle`（添加字幕）。
- **选项 B（推荐）：** 提供 `storyboard.json` 文件。
  - 使用参数 `--storyboard-json /abs/path/storyboard.json` 传递配置信息。
  - 参考文档：`references/storyboard.schema.json`。

## 系统要求：
- 必需安装 macOS 系统以及 `ffmpeg` 和 `ffprobe` 工具。
- 需要 Node.js 及其包管理器 `npm`；脚本会在临时工作目录中执行 `npm i` 命令来安装所需依赖。

---

（注：由于提供的代码片段较为简短，部分详细信息（如配置文件路径和具体语法）在翻译时可能无法完全呈现。在实际使用中，请根据实际情况补充完整的信息。）
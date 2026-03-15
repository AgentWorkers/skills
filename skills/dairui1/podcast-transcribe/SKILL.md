---
name: transcribe
description: 使用 `podcast-helper` 将播客音频转录为原始音频、SRT字幕和TXT文本文件；如果需要，还可以根据播客页面的上下文对文本进行进一步处理（如清理或优化）。当用户请求转录播客剧集、生成字幕、从音频文件中提取文本，或使用播客页面信息来完善原始文本时，可以使用该工具。在合适的情况下，优先选择通过 `npx` 或 `pnpm dlx` 进行无需安装的操作。
allowed-tools: Bash(curl:*), Bash(podcast-helper:*), Bash(npx podcast-helper:*), Bash(pnpm dlx podcast-helper:*), Bash(node dist/cli.js:*), Bash(pnpm run build:*)
---
# 使用 `podcast-helper` 进行转录和清理工作

`podcast-helper` 是一个用于下载播客内容并进行转录的命令行工具（CLI）。

当用户需要以下功能时，可以使用这个工具：
- 转录 Xiaoyuzhou 的剧集 URL
- 转录公开播客剧集页面上的音频元数据或可发现的 RSS/Atom 源
- 直接转录远程音频文件
- 生成字幕文件（`.srt` 格式）
- 生成纯文本转录文件（`.txt` 格式）
- 在转录后清理原始转录内容
- 根据剧集页面的上下文修正自动语音识别（ASR）中的明显错误
- 在 Apple Silicon 系统上执行本地转录
- 使用特定的 AI 转录服务提供商（如 OpenAI、Groq、Deepgram、Gladia、AssemblyAI 或 Rev.ai）

## 输入参数

`transcribe` 命令接受以下一种输入：
- Xiaoyuzhou 剧集的 URL
- 公开播客剧集页面的 URL
- 直接音频文件的 URL（例如 `.mp3` 或 `.m4a`）
- 本地音频文件的路径

示例：

```bash
npx podcast-helper transcribe https://www.xiaoyuzhoufm.com/episode/69b4d2f9f8b8079bfa3ae7f2 --output-dir ./out/episode --json
npx podcast-helper transcribe https://example.fm/episodes/42 --output-dir ./out/episode-page --json
npx podcast-helper transcribe https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3 --output-dir ./out/smoke --json
npx podcast-helper transcribe ./audio/interview.mp3 --output-dir ./out/local --json
```

当播客剧集页面包含以下信息时，该工具的支持效果最佳：
- `og:audio` 或类似的音频元数据
- `<audio>` 或 `<source>` 标签
- JSON-LD 格式的 `AudioObject` 或 `PodcastEpisode` 数据
- 可链接到当前剧集页面的备用 RSS/Atom 源

这涵盖了大多数基于 Buzzsprout、Libsyn、Simplecast、Podbean、Transistor、Castos、Omny、Acast 和 Spreaker 等平台的公开播客页面。

## 系统要求

- 可以通过 `npx` 或 `pnpm dlx` 从 npm 安装该 CLI，或者直接从仓库中运行它
- 使用 Jina Reader 进行清理操作是可选的，且不依赖于 ElevenLabs 的服务

对于使用 ElevenLabs 的情况：
- 必须设置 `ELEVENLABS_API_KEY`

其他支持的远程服务提供商：
- `OPENAI_API_KEY` -> `openai`
- `GROQ_API_KEY` -> `groq`
- `DEEPGRAM_API_KEY` -> `deepgram`
- `GLADIA_API_KEY` -> `gladia`
- `ASSEMBLYAI_API_KEY` -> `assemblyai`
- `REVAI_API_KEY` -> `revai`

在 Apple Silicon 系统上使用 `mlx-whisper` 进行本地转录时，需要满足以下条件：
- 已安装 `ffmpeg`
- 系统中必须包含 `python3`
- 使用 `podcast-helper setup mlx-whisper` 命令可以安装所需的运行时环境

在开始转录之前，请先检查 API 密钥是否已设置：

```bash
printenv ELEVENLABS_API_KEY
```

默认的转录引擎选择规则：
- 如果本地安装了 `mlx-whisper`，则省略 `--engine` 选项，让 CLI 自动使用 `mlx-whisper`
- 如果设置了 `ELEVENLABS_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `elevenlabs`
- 如果设置了 `OPENAI_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `openai`
- 如果设置了 `GROQ_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `groq`
- 如果设置了 `DEEPGRAM_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `deepgram`
- 如果设置了 `GLADIA_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `gladia`
- 如果设置了 `ASSEMBLYAI_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `assemblyai`
- 如果设置了 `REVAI_API_KEY`，则省略 `--engine` 选项，让 CLI 使用 `revai`
- 如果没有指定引擎，CLI 会默认使用 `mlx-whisper`
- 只有在需要强制使用特定后端服务时，才使用 `--engine <provider>` 选项

## 推荐的命令格式

为了便于机器读取输出结果，建议使用以下命令格式：

```bash
npx podcast-helper transcribe <input> --output-dir <dir> --json
```

本地转录的工作流程默认设置如下：
- 为每次请求创建临时工作空间
- 使用 `ffmpeg` 每 300 秒分割音频文件
- 将转录结果分块输出到 `stderr`
- 除非设置了 `--keep-temp` 选项，否则会自动清理临时文件

这样做的原因：
- 转录进度信息会输出到 `stderr`
- 成功的结果会以 JSON 格式输出到 `stdout`
- 失败信息也会以 JSON 格式输出到 `stderr`
- 代理程序可以直接解析这些输出，而无需手动抓取日志

## 输出结果

该工具会生成以下文件：
- 原始音频文件
- 字幕文件（`.srt` 格式）
- 转录文本文件（`.txt` 格式）

典型的 JSON 输出格式如下：

```json
{
  "ok": true,
  "command": "transcribe",
  "input": "https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3",
  "source": "remote-audio-url",
  "language": "eng",
  "artifacts": {
    "audio": "/abs/path/nicole.mp3",
    "srt": "/abs/path/nicole.srt",
    "txt": "/abs/path/nicole.txt"
  }
}
```

典型的失败信息会输出到 `stderr`：

```json
{
  "ok": false,
  "command": "transcribe",
  "error": {
    "code": "SOURCE_RESOLUTION_FAILED",
    "category": "source",
    "message": "Could not extract podcast audio from the provided page.",
    "hints": [
      "Pass the original episode page URL, a direct audio URL, or a local audio file.",
      "If this site hides audio metadata, download the audio separately and rerun `transcribe` with the file path."
    ]
  }
}
```

如果需要同时在终端中显示转录进度和失败信息，可以使用 `--progress jsonl` 选项。

## 默认工作流程

默认的执行顺序如下：
1. 使用 `podcast-helper` 进行转录
2. 报告生成的文件路径
3. 询问用户是否需要清理原始转录内容
4. 如果需要清理，使用 Jina Reader 获取剧集页面的上下文，并生成清理后的转录文件

建议的后续操作：
```text
Do you want me to clean the transcript as well?
```

当用户请求清理原始转录内容时，保留原始转录文件，并生成一个清理后的版本：
- 原始文件：`episode.txt`
- 清理后的文件：`episode.cleaned.txt`

## 执行策略

推荐的执行顺序如下：
1. `npx podcast-helper transcribe ...`
2. `pnpm dlx podcast-helper transcribe ...`
3. `podcast-helper transcribe ...`
4. 在本仓库中，可以使用 `node dist/cli.js transcribe ...`

如果用户明确要求在 Apple Silicon 系统上执行本地转录，请使用 `--engine mlx-whisper` 选项。
如果用户指定了特定的后端服务，请使用 `--engine <provider>` 选项。
否则，CLI 会根据可用的 API 密钥自动选择合适的后端。

除非你已经在仓库中工作，否则不要默认使用仓库中的构建指令。
如果你在仓库中且 `dist/cli.js` 文件缺失，请先构建该文件：

```bash
pnpm run build
```

然后执行相应的命令：

```bash
node dist/cli.js transcribe <input> --output-dir <dir> --json
```

## 使用建议

- 在进行测试时，建议使用较小的音频文件以降低转录成本。
- 如果用户不要求使用真实的播客剧集，可以使用 `https://storage.googleapis.com/eleven-public-cdn/audio/marketing/nicole.mp3` 作为测试音频。
- 每个任务应使用独立的输出目录。
- 将生成的文件路径告知用户。
- 如果用户尚未安装 CLI，建议使用 `npx` 或 `pnpm dlx` 进行操作。
- 如果用户需要在 Apple Silicon 系统上进行本地转录或离线转录，请使用 `--engine mlx-whisper` 选项。
- 如果缺少本地转录所需的设置，请先运行 `podcast-helper doctor`，然后再运行 `podcast-helper setup mlx-whisper`。
- 如果用户没有指定特定的后端服务，系统会自动选择合适的后端。
- 如果输入是 Xiaoyuzhou 剧集或公开播客页面，CLI 会自动下载源音频。
- 转录完成后，询问用户是否需要进一步处理（如清理转录内容）。

## 清理工作流程

在以下情况下执行清理操作：
- 用户同意在转录后清理原始转录文件
- 用户已经拥有原始的 `.txt` 格式转录文件并希望对其进行处理

推荐的输入参数包括：
- 原始播客的 URL
- 原始转录文件（通常为 `.txt` 格式）

可选但有用的输入参数包括：
- 字幕文件（`.srt` 格式）
- 原始音频文件

使用 Jina Reader 获取剧集页面的内容，以便进行以下操作：
```bash
curl https://r.jina.ai/<podcast-url>
```

例如：

```bash
curl https://r.jina.ai/https://www.xiaoyuzhoufm.com/episode/69b4d2f9f8b8079bfa3ae7f2
```

利用页面内容作为参考，可以：
- 修正明显的同音词和自动语音识别错误
- 恢复人名、产品名称、标题等专有名词
- 删除重复的填充词和冗余的表达
- 规范标点符号和段落格式以提高可读性

在进行清理时，请遵循以下原则：
- 保留说话者的意图和事实内容
- 不要添加缺失的信息
- 不要进行总结，而只是对原始内容进行清理
- 不要覆盖原始转录文件

如果无法访问剧集的 URL，请仅使用转录文件进行保守的清理，并说明未使用任何外部剧集信息。

## 失败处理方式

如果转录失败，请检查以下情况：
- 确认选择了正确的后端服务
- 如果选择了基于云的服务，请确认相应的 API 密钥是否正确
- 如果使用了本地 `mlx-whisper`，请运行 `podcast-helper doctor` 命令进行检查
- 如果缺少 `mlx-whisper`，请运行 `podcast-helper setup mlx-whisper` 命令进行安装
- 确认输入的 URL 是否可访问
- 使用新的输出目录重新运行转录任务
- 如果使用仓库中的构建脚本，请运行 `pnpm run check` 和 `pnpm run build` 命令

如果清理后的质量不确定，请检查以下内容：
- 确认播客 URL 与转录结果是否一致
- 重新获取 Jina Reader 提供的页面信息，检查其中是否包含有效的剧集元数据
- 如果页面提供的信息不足，尽量减少对转录内容的修改

## 安装该工具

可以在项目本地安装该工具：
```bash
npx skills add dairui1/podcast-helper --skill transcribe
```

也可以全局安装该工具：
```bash
npx skills add dairui1/podcast-helper --skill transcribe -g
```
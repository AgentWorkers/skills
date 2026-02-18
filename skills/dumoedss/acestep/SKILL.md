---
name: acestep
description: 使用 ACE-Step API 生成音乐、编辑歌曲以及进行音乐混音。该 API 支持将文本转换为音乐、生成歌词、实现音频的连续播放以及修改音频内容。当用户提到音乐生成、歌曲创作、音乐制作、混音或音频编辑时，可以使用此技能。
allowed-tools: Read, Write, Bash, Skill
---
# ACE-Step 音乐生成技能

使用 ACE-Step V1.5 API 进行音乐生成。**请务必使用 `scripts/acestep.sh` 脚本**，**切勿直接调用 API 端点**。

## 快速入门

```bash
# 1. cd to this skill's directory
cd {project_root}/{.claude or .codex}/skills/acestep/

# 2. Check API service health
./scripts/acestep.sh health

# 3. Generate with lyrics (recommended)
./scripts/acestep.sh generate -c "pop, female vocal, piano" -l "[Verse] Your lyrics here..." --duration 120 --language zh

# 4. Output saved to: {project_root}/acestep_output/
```

## 工作流程

对于需要人声的用户请求：
1. 使用 **acestep-songwriting** 技能来编写歌词、创建字幕、选择时长/每分钟拍数（BPM）和调性。
2. 根据歌曲创作指南，自己编写完整且结构清晰的歌词。
3. 使用 `-c` 和 `-l` 参数，通过字幕模式生成音乐。

仅在使用简单灵感生成或进行乐器探索时，才使用简单/随机模式（`-d` 或 `random`）。

如果用户需要制作简单的音乐视频，请使用 **acestep-simplemv** 技能来渲染视频，并显示波形图和同步的歌词。

**音乐视频制作要求**：制作简单音乐视频需要安装以下三个技能：
- **acestep-songwriting** — 用于编写歌词和规划歌曲结构
- **acestep-lyrics-transcription** — 用于将音频转录为带时间戳的歌词（LRC 格式）
- **acestep-simplemv** — 用于渲染最终的音乐视频

## 脚本命令

**重要提示 - 必须提供完整歌词**：通过 `-l` 参数提供歌词时，必须传递所有歌词内容，不得有任何遗漏：
- 如果用户提供了歌词，请传递他们提供的全部文本；
- 如果您自己生成了歌词，请传递您创建的完整歌词；
- 绝不要截断、缩短或仅传递部分歌词；
- 缺少歌词会导致歌曲不完整或逻辑不清。

**音乐参数**：使用 **acestep-songwriting** 技能来获取关于时长、BPM、调性音阶和拍号的建议。

```bash
# need to cd to this skill's directory first
cd {project_root}/{.claude or .codex}/skills/acestep/

# Caption mode - RECOMMENDED: Write lyrics first, then generate
./scripts/acestep.sh generate -c "Electronic pop, energetic synths" -l "[Verse] Your complete lyrics
[Chorus] Full chorus here..." --duration 120 --bpm 128

# Instrumental only
./scripts/acestep.sh generate "Jazz with saxophone"

# Quick exploration (Simple/Random mode)
./scripts/acestep.sh generate -d "A cheerful song about spring"
./scripts/acestep.sh random

# Options
./scripts/acestep.sh generate "Rock" --duration 60 --batch 2
./scripts/acestep.sh generate "EDM" --no-thinking    # Faster

# Other commands
./scripts/acestep.sh status <job_id>
./scripts/acestep.sh health
./scripts/acestep.sh models
```

## 输出文件

生成完成后，脚本会自动将结果保存到项目根目录下的 `acestep_output` 文件夹中（与 `.claude` 文件位于同一层级）：

```
project_root/
├── .claude/
│   └── skills/acestep/...
├── acestep_output/          # Output directory
│   ├── <job_id>.json         # Complete task result (JSON)
│   ├── <job_id>_1.mp3        # First audio file
│   ├── <job_id>_2.mp3        # Second audio file (if batch_size > 1)
│   └── ...
└── ...
```

### JSON 结果结构

**重要提示**：当启用了语言模型（LM）增强功能（`use_format=true`）时，最终合成的内容可能与您的输入有所不同。请查看 JSON 文件中的实际值：

| 字段 | 描述 |
|-------|-------------|
| `prompt` | 用于合成的实际字幕（可能经过语言模型增强） |
| `lyrics` | 用于合成的实际歌词（可能经过语言模型增强） |
| `metas.prompt` | 原始输入的字幕 |
| `metas.lyrics` | 原始输入的歌词 |
| `metas bpm` | 使用的每分钟拍数（BPM） |
| `metas.keyscale` | 使用的调性音阶 |
| `metas.duration` | 时长（以秒为单位） |
| `generation_info` | 详细的时长和模型信息 |
| `seed_value` | 使用的种子值（用于重现性） |
| `lm_model` | 语言模型名称 |
| `dit_model` | DiT 模型名称 |

要获取实际的合成歌词，请解析 JSON 文件并读取顶层的 `lyrics` 字段，而不是 `metas.lyrics`。

## 配置

**重要提示**：配置的优先级如下（从高到低）：
1. **命令行参数** > **config.json** 的默认值
2. 用户指定的参数 **会暂时覆盖** 默认值，但 **不要修改** `config.json` 文件
3. **仅 `config --set` 命令** 会 **永久修改** `config.json` 文件

### 默认配置文件 (`scripts/config.json`)

```json
{
  "api_url": "http://127.0.0.1:8001",
  "api_key": "",
  "api_mode": "completion",
  "generation": {
    "thinking": true,
    "use_format": false,
    "use_cot_caption": true,
    "use_cot_language": false,
    "batch_size": 1,
    "audio_format": "mp3",
    "vocal_language": "en"
  }
}
```

| 选项 | 默认值 | 描述 |
|--------|---------|-------------|
| `api_url` | `http://127.0.0.1:8001` | API 服务器地址 |
| `api_key` | `""` | API 认证密钥（可选） |
| `api_mode` | `completion` | API 模式：`completion`（OpenRouter，默认）或 `native`（轮询） |
| `generation.thinking` | `true` | 启用 5Hz 语言模型（质量更高，但速度较慢） |
| `generation.audio_format` | `mp3` | 输出格式（mp3/wav/flac） |
| `generation.vocal_language` | `en` | 人声语言 |

## 先决条件 - ACE-Step API 服务

**重要提示**：此技能需要 ACE-Step API 服务器处于运行状态。

### 所需依赖项

`scripts/acestep.sh` 脚本需要以下工具：**curl** 和 **jq**。

```bash
# Check dependencies
curl --version
jq --version
```

如果未安装 `jq`，脚本会尝试自动安装。如果自动安装失败：
- **Windows**：`choco install jq` 或从 https://jqlang.github.io/jq/download/ 下载
- **macOS**：`brew install jq`
- **Linux**：`sudo apt-get install jq`（Debian/Ubuntu）或 `sudo dnf install jq`（Fedora）

### 首次使用前的注意事项

**在使用之前，您必须检查 API 密钥和 URL 的状态。** 运行以下命令：

```bash
cd "{project_root}/{.claude or .codex}/skills/acestep/" && bash ./scripts/acestep.sh config --check-key
cd "{project_root}/{.claude or .codex}/skills/acestep/" && bash ./scripts/acestep.sh config --get api_url
```

#### 情况 1：使用官方云 API (`https://api.acemusic.ai`) 且未配置 API 密钥

如果 `api_url` 为 `https://api.acemusic.ai` 且 `api_key` 为空，您必须停止操作并指导用户配置他们的 API 密钥：
1. 告诉用户：“您正在使用 ACE-Step 官方云 API，但尚未配置 API 密钥。使用此服务需要 API 密钥。”
2. 解释如何获取密钥：目前可以通过 [acemusic.ai](https://acemusic.ai/api-key) 免费获取 API 密钥。
3. 使用 `AskUserQuestion` 命令请求用户提供 API 密钥。
4. 获取密钥后，进行配置：
   ```bash
   cd "{project_root}/{.claude or .codex}/skills/acestep/" && bash ./scripts/acestep.sh config --set api_key <KEY>
   ```
5. 另外，告知用户：“如果您还想制作音乐视频（MV），建议同时配置歌词转录 API 密钥（如 OpenAI Whisper 或 ElevenLabs Scribe），以便歌词可以自动带有准确的时间戳。您可以通过 `acestep-lyrics-transcription` 技能进行配置。”

#### 情况 2：API 密钥已配置

验证 API 端点：`./scripts/acestep.sh health`，然后继续进行音乐生成。

#### 情况 3：使用本地/自定义 API 且未配置密钥

本地服务（`http://127.0.0.1:*`）通常不需要密钥。通过 `./scripts/acestep.sh health` 验证后继续操作。

如果健康检查失败：
- 询问用户：“您是否安装了 ACE-Step？”
- **如果已安装但未运行**：使用 `acestep-docs` 技能帮助用户启动服务
- **如果未安装**：使用 `acestep-docs` 技能指导用户完成安装

### 服务配置

**官方云 API：** ACE-Step 提供官方 API 端点 `https://api.acemusic.ai`。要使用它，请执行以下操作：
```bash
./scripts/acestep.sh config --set api_url "https://api.acemusic.ai"
./scripts/acestep.sh config --set api_key "your-key"
./scripts/acestep.sh config --set api_mode completion
```

API 密钥目前可以通过 [acemusic.ai](https://acemusic.ai/api-key) 免费获取。

**本地服务（默认）：** 无需配置——直接连接到 `http://127.0.0.1:8001`。

**自定义远程服务：** 更新 `scripts/config.json` 或使用以下命令：
```bash
./scripts/acestep.sh config --set api_url "http://remote-server:8001"
./scripts/acestep.sh config --set api_key "your-key"
```

**API 密钥处理**：在检查 API 密钥是否配置时，使用 `config --check-key` 命令，该命令只会显示 `configured` 或 `empty`，而不会显示实际的密钥。**切勿使用 `config --get api_key`** 或直接读取 `config.json`——这些操作会暴露用户的 API 密钥。`config --list` 命令是安全的——它会在输出中将 API 密钥替换为 `***`。

### API 模式

该技能支持两种 API 模式。通过 `scripts/config.json` 中的 `api_mode` 参数进行切换：

| 模式 | 端点 | 描述 |
|------|----------|-------------|
| `completion`（默认） | `/v1/chat/completions` | 兼容 OpenRouter，同步请求，音频以 base64 格式返回 |
| `native` | `/release_task` + `/query_result` | 异步轮询模式，支持所有参数 |

**切换模式：**
```bash
./scripts/acestep.sh config --set api_mode completion
./scripts/acestep.sh config --set api_mode native
```

**完成模式说明：**
- 无需轮询——单个请求即可直接返回结果
- 音频以 base64 格式内嵌在响应中（自动解码并保存）
- `inference_steps`、`infer_method`、`shift` 不可配置（由服务器默认设置）
- `--no-wait` 和 `status` 命令在完成模式下不适用
- 需要 `model` 字段——如果未指定，则从 `/v1/models` 自动检测

### 使用 `acestep-docs` 技能获取设置帮助

**重要提示**：对于安装和启动操作，始终使用 `acestep-docs` 技能以获得完整和准确的指导。

**请不要提供简化的启动命令**——每个用户的环境可能不同。始终指导他们使用 `acestep-docs` 进行正确的设置。

---

有关 API 调试的详细信息，请参阅 [API 参考文档](./api-reference.md)。
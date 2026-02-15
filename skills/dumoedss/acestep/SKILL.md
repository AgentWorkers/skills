---
name: acestep
description: 使用 ACE-Step API 生成音乐、编辑歌曲以及进行音乐混音。该 API 支持将文本转换为音乐、生成歌词、实现音频的连续播放以及修改音频内容。当用户提到“生成音乐”、“创作歌曲”、“音乐制作”、“混音”或“音频续写”等功能时，可以参考此技能。
allowed-tools: Read, Write, Bash, Skill
---

# ACE-Step 音乐生成技能

使用 ACE-Step V1.5 API 进行音乐生成。脚本：`scripts/acestep.sh`（需要 curl 和 jq）。

## 先决条件 - ACE-Step API 服务

**重要提示**：此技能需要 ACE-Step API 服务器处于运行状态。

### 所需依赖项

`scripts/acestep.sh` 脚本需要以下工具：

**1. curl** - 用于向 API 发送 HTTP 请求
**2. jq** - 用于解析 JSON 响应

#### 检查依赖项

在使用此技能之前，请确认已安装所需的工具：

```bash
# Check curl
curl --version

# Check jq
jq --version
```

#### 安装 jq

如果未安装 jq，脚本会尝试自动安装。如果自动安装失败，请手动安装：

**Windows:**
```bash
# Using Chocolatey
choco install jq

# Or download from: https://jqlang.github.io/jq/download/
# Extract jq.exe and add to PATH
```

**macOS:**
```bash
# Using Homebrew
brew install jq

# Using MacPorts
port install jq
```

**Linux:**
```bash
# Debian/Ubuntu
sudo apt-get install jq

# Fedora/RHEL/CentOS
sudo yum install jq
# or
sudo dnf install jq

# Arch Linux
sudo pacman -S jq
```

**验证安装结果:**
```bash
jq --version
# Should output: jq-1.x
```

如果用户遇到 jq 安装问题，请指导他们按照其操作系统进行手动安装。

### 首次使用前的准备

**询问用户的相关设置:**

1. **“您是否配置并运行了 ACE-Step API 服务？”**

   如果 **是**：
   - 验证 API 端点：`curl -s http://127.0.0.1:8001/health`
   - 如果使用远程服务，请获取 API URL 并更新 `scripts/config.json`
   - 然后继续进行音乐生成

   如果 **否** 或 **不确定**：
   - 询问：“您是否安装了 ACE-Step？”

     **如果已安装但未运行**：
     - 使用 `acestep-docs` 技能帮助他们启动服务
     - 指导他们完成启动过程

     **如果未安装**：
     - 提供帮助下载并安装 ACE-Step
     - 询问：“您想使用 Windows 可移植包还是从源代码安装？”
     - 使用 `acestep-docs` 技能指导安装过程

### 服务配置

**本地服务（默认）:**
```json
{
  "api_url": "http://127.0.0.1:8001",
  "api_key": ""
}
```

**远程服务:**
```json
{
  "api_url": "http://your-server-ip:8001",
  "api_key": "your-api-key-if-needed"
}
```

要配置远程服务，请更新 `scripts/config.json` 或使用：
```bash
cd {skill_directory}/scripts/
./acestep.sh config --set api_url "http://remote-server:8001"
./acestep.sh config --set api_key "your-key"
```

### 使用 `acestep-docs` 技能获取安装帮助

**重要提示**：对于安装和启动操作，请始终使用 `acestep-docs` 技能以获得完整且准确的指导。

当用户需要安装或启动帮助时，调用 `acestep-docs` 技能：

```
Use the Skill tool to invoke: acestep-docs
```

**请勿提供简化的启动命令**——每个用户的环境可能不同。务必引导他们使用 `acestep-docs` 进行正确的设置。

### 健康检查

**验证服务是否正在运行:**
```bash
curl http://127.0.0.1:8001/health
# Should return: {"status":"ok",...}
```

如果健康检查失败，请使用 `acestep-docs` 技能帮助用户正确启动服务。

---

**工作流程**：对于需要人声的音乐生成请求，您应该：
1. 查阅 [音乐创作指南](./music-creation-guide.md) 以获取歌词创作、标题制作、时长/节拍/调性选择的相关信息。
2. 根据指南自行编写完整且结构清晰的歌词。
3. 使用 `-c` 和 `-l` 参数通过 **标题模式** 生成音乐。

仅在使用 **简单/随机模式**（`-d` 或 `random`）时，用于快速获取灵感或进行器乐探索。

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

**重要提示**：当启用语言模型（LM）增强功能（`use_format=true`）时，最终合成的内容可能与输入有所不同。请查看 JSON 文件中的实际值：

| 字段 | 描述 |
|-------|-------------|
| `prompt` | 用于合成的实际标题（可能经过语言模型增强） |
| `lyrics` | 用于合成的实际歌词（可能经过语言模型增强） |
| `metas.prompt` | 原始输入的标题 |
| `metas.lyrics` | 原始输入的歌词 |
| `metas bpm` | 使用的节拍（BPM） |
| `metas.keyscale` | 使用的调性音阶 |
| `metas.duration` | 时长（秒） |
| `generation_info` | 详细的定时和模型信息 |
| `seed_value` | 使用的种子值（用于重现性） |
| `lm_model` | 语言模型名称 |
| `dit_model` | DiT 模型名称 |

要获取实际的合成歌词，请解析 JSON 文件并读取顶层的 `lyrics` 字段，而不是 `metas.lyrics`。

## 脚本命令

**重要提示 - 必须提供完整歌词**: 当通过 `-l` 参数提供歌词时，必须传递所有歌词内容，不得有任何遗漏：
- 如果用户提供歌词，请传递他们提供的全部文本
- 如果您自己生成歌词，请传递您创建的完整歌词
- 绝不要截断、缩短或仅传递部分歌词
- 缺失的歌词会导致歌曲不完整或逻辑混乱

**音乐参数**: 请参考 [音乐创作指南](./music-creation-guide.md) 以了解如何计算时长、选择节拍、调性音阶和拍号。

```bash
# need to cd skills path
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

## 配置

**重要提示**: 配置的优先级如下（从高到低）：

1. **命令行参数** > **config.json 的默认值**
2. 用户指定的参数 **会暂时覆盖** 默认值，但 **不得修改** `config.json`
3. 仅 `config --set` 命令 **会永久修改** `config.json`

### 默认配置文件 (`scripts/config.json`)

```json
{
  "api_url": "http://127.0.0.1:8001",
  "api_key": "",
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
| `generation.thinking` | `true` | 启用 5Hz 语言模型（质量更高，但速度较慢） |
| `generation.audio_format` | `mp3` | 输出格式（mp3/wav/flac） |
| `generation.vocal_language` | `en` | 人声语言 |

## API 参考

所有响应的结构如下：`{"data": <payload>, "code": 200, "error": null, "timestamp": ...}`

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/health` | GET | 健康检查 |
| `/release_task` | POST | 创建生成任务 |
| `/query_result` | POST | 查询任务状态，请求体：`{"task_id_list": ["id"]` |
| `/v1/models` | GET | 列出可用模型 |
| `/v1/audio?path={path}` | GET | 下载音频文件 |

### 查询结果响应

```json
{
  "data": [{
    "task_id": "xxx",
    "status": 1,
    "result": "[{\"file\":\"/v1/audio?path=...\",\"metas\":{\"bpm\":120,\"duration\":60,\"keyscale\":\"C Major\"}}]"
  }]
}
```

状态码：`0` = 处理中，`1` = 成功，`2` = 失败

## 请求参数 (`/release_task`)

参数可以放在 `param_obj` 对象中。

### 生成模式

| 模式 | 使用方法 | 适用场景 |
|------|-------|-------------|
| **标题模式**（推荐） | `generate -c "style" -l "lyrics"` | 适用于人声歌曲——先编写歌词 |
| **简单模式** | `generate -d "description"` | 快速探索，由语言模型生成所有内容 |
| **随机模式** | `random` | 随机生成以获取灵感 |

### 核心参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `prompt` | 字符串 | "" | 音乐风格描述（标题模式） |
| `lyrics` | 字符串 | "" | **完整歌词内容**——必须提供全部歌词，不得遗漏。使用 `[inst]` 表示器乐。部分/截断的歌词会导致歌曲不完整 |
| `sample_mode` | 布尔值 | `false` | 启用简单/随机模式 |
| `sample_query` | 字符串 | "" | 简单模式的描述 |
| `thinking` | 布尔值 | `false` | 启用 5Hz 语言模型以生成音频 |
| `use_format` | 布尔值 | `false` | 使用语言模型增强标题/歌词 |
| `model` | 字符串 | - | DiT 模型名称 |
| `batch_size` | 整数 | 1 | 要生成的音频文件数量 |

### 音乐属性

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `audio_duration` | 浮点数 | - | 时长（秒） |
| `bpm` | 整数 | - | 节拍（每分钟拍数） |
| `key_scale` | 字符串 | "" | 调性（例如 "C 大调"） |
| `time_signature` | 字符串 | "" | 拍号（例如 "4/4"） |
| `vocal_language` | 字符串 | "en" | 语言代码（en, zh, ja 等） |
| `audio_format` | 字符串 | "mp3" | 输出格式（mp3/wav/flac） |

### 生成参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `inference_steps` | 整数 | 8 | 扩散步骤 |
| `guidance_scale` | 浮点数 | 7.0 | CFG 音阶 |
| `seed` | 整数 | -1 | 随机种子（-1 表示随机） |
| `infer_method` | 字符串 | "ode" | 扩散方法（ode/sde） |

### 音频任务参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `task_type` | 字符串 | "text2music" | text2music / continuation / repainting |
| `src_audio_path` | 字符串 | - | 继续使用的源音频文件 |
| `repainting_start` | 浮点数 | 0.0 | 继续开始的起始位置（秒） |
| `repainting_end` | 浮点数 | - | 继续结束的位置（秒） |

### 示例请求（简单模式）

```json
{
  "sample_mode": true,
  "sample_query": "A cheerful pop song about spring",
  "thinking": true,
  "param_obj": {
    "duration": 60,
    "bpm": 120,
    "language": "en"
  },
  "batch_size": 2
}
```
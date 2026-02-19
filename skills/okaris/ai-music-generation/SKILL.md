---
name: ai-music-generation
description: "使用 `infer.sh` CLI 工具，可以通过 Diffrythm 和 Tencent Song Generation 生成 AI 音乐和歌曲。  
**模型说明：**  
- **Diffrythm**：专注于快速歌曲生成。  
- **Tencent Song Generation**：能够生成包含人声的完整歌曲。  
**功能支持：**  
- 文本转音乐（text-to-music）  
- 歌曲创作（song generation）  
- 仅乐器版本（instrumental）  
- 歌词转歌曲（lyrics to song）  
- 音乐配乐制作（soundtrack creation）  
**应用场景：**  
- 背景音乐（background music）  
- 社交媒体内容（social media content）  
- 游戏音轨（game soundtracks）  
- 播客（podcasts）  
- 无需版税的音乐（royalty-free music）  
**相关命令：**  
- `generate music`：生成音乐  
- `ai music`：创建 AI 音乐  
- `generate song`：生成歌曲  
- `text to music`：将文本转换为音乐  
- `create music with ai`：使用 AI 创作音乐  
- `suno alternative`：Suno 的替代工具  
- `udio alternative`：音频相关的替代方案  
- `ai song`：AI 生成的歌曲  
- `ai soundtrack`：AI 制作的音轨  
- `generate soundtrack`：生成音轨  
- `ai jingle`：AI 制作的短音乐片段"
allowed-tools: Bash(infsh *)
---
# 人工智能音乐生成

您可以通过 [inference.sh](https://inference.sh) 命令行界面（CLI）来生成音乐和歌曲。

![人工智能音乐生成](https://cloud.inference.sh/u/4mg21r6ta37mpaz6ktzwtt8krr/01jz01qvx0gdcyvhvhpfjjb6s4.png)

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Generate a song
infsh app run infsh/diffrythm --input '{"prompt": "upbeat electronic dance track"}'
```

> **安装说明**：[安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从 `dist.inference.sh` 下载相应的二进制文件，并验证其 SHA-256 校验和。无需特殊权限或后台进程。也可以选择[手动安装与验证](https://dist.inference.sh/cli/checksums.txt)。

## 可用模型

| 模型 | 应用 ID | 适用场景 |
|-------|--------|----------|
| Diffrythm | `infsh/diffrythm` | 快速生成歌曲 |
| Tencent Song | `infsh/tencent-song-generation` | 生成包含人声的完整歌曲 |

## 浏览音频应用

```bash
infsh app list --category audio
```

## 示例

### 纯器乐曲目

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "cinematic orchestral soundtrack, epic and dramatic"
}'
```

### 带有人声的歌曲

```bash
infsh app sample infsh/tencent-song-generation --save input.json

# Edit input.json:
# {
#   "prompt": "pop song about summer love",
#   "lyrics": "Walking on the beach with you..."
# }

infsh app run infsh/tencent-song-generation --input input.json
```

### 视频背景音乐

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "calm lo-fi hip hop beat, study music, relaxing"
}'
```

### 播客开场曲

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "short podcast intro jingle, professional, tech themed, 10 seconds"
}'
```

### 游戏原声带

```bash
infsh app run infsh/diffrythm --input '{
  "prompt": "retro 8-bit video game music, adventure theme, chiptune"
}'
```

## 提示与建议

**音乐类型关键词**：流行、摇滚、电子、爵士、古典、嘻哈、低保真、环境音、管弦乐

**音乐情绪关键词**：欢快、悲伤、充满活力、平静、戏剧性、史诗感、神秘、振奋人心

**乐器关键词**：钢琴、吉他、合成器、鼓、弦乐器、铜管乐器、合唱团

**音乐结构关键词**：引子、主歌、副歌、过渡段、尾声、循环

## 使用场景

- **社交媒体**：视频背景音乐
- **播客**：开场/结尾曲
- **游戏**：原声带和音效
- **视频**：背景音乐
- **广告**：商业广告曲
- **内容创作**：无需支付版税的音乐素材

## 相关技能

```bash
# Full platform skill (all 150+ apps)
npx skills add inference-sh/skills@inference-sh

# Text-to-speech
npx skills add inference-sh/skills@text-to-speech

# Video generation (add music to videos)
npx skills add inference-sh/skills@ai-video-generation

# Speech-to-text
npx skills add inference-sh/skills@speech-to-text
```

- 浏览所有应用：`infsh app list`

## 文档资料

- [运行应用](https://inference.sh/docs/apps/running) - 如何通过 CLI 运行应用
- [内容处理流程示例](https://inference.sh/docs/examples/content-pipeline) - 构建媒体工作流
- [应用概览](https://inference.sh/docs/apps/overview) - 了解应用生态系统
---
name: local-whisper
description: 使用 OpenAI Whisper 实现本地语音转文本功能。模型下载完成后即可完全离线运行。支持多种模型规模，提供高质量的转录结果。
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["ffmpeg"]}}}
---

# 本地语音转文本（Local Speech-to-Text）功能：使用 OpenAI 的 Whisper 实现

该功能支持将用户的语音转换为文本，且在整个过程中完全离线运行（即在下载模型后无需网络连接）。

## 使用方法

```bash
# Basic
~/.clawdbot/skills/local-whisper/scripts/local-whisper audio.wav

# Better model
~/.clawdbot/skills/local-whisper/scripts/local-whisper audio.wav --model turbo

# With timestamps
~/.clawdbot/skills/local-whisper/scripts/local-whisper audio.wav --timestamps --json
```

## 可用的模型

| 模型名称 | 模型大小（MB） | 特点 |
|---------|-------------|---------|
| `tiny`    | 39MB        | 速度最快 |
| `base`    | 74MB        | 默认模型 |
| `small`    | 244MB        | 性能与速度的平衡较好 |
| `turbo`    | 809MB        | 速度与质量最佳 |
| `large-v3` | 1.5GB       | 最高准确率 |

## 命令行参数

- `--model/-m`    | 指定使用的模型大小（默认：`base`） |
- `--language/-l`    | 指定处理的语言代码（若省略则自动检测） |
- `--timestamps/-t` | 是否包含单词的时间戳（默认：不包含） |
- `--json/-j`    | 是否以 JSON 格式输出结果（默认：不输出） |
- `--quiet/-q`    | 是否抑制运行过程中的进度提示（默认：不抑制） |

## 设置要求

该功能依赖于 uv-managed 环境（venv）。若需重新安装相关依赖，请执行以下命令：
```bash
cd ~/.clawdbot/skills/local-whisper
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python click openai-whisper torch --index-url https://download.pytorch.org/whl/cpu
```
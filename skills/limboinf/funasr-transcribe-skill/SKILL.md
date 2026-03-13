---
name: funasr-transcribe
description: >
  **使用场景：**  
  当用户需要对音频文件进行本地语音转文本处理时（尤其是中文或中英文混合的音频文件），且不希望依赖云端的转录服务（如云转录API）时，可以使用该功能。
homepage: https://github.com/limboinf/funasr-transcribe-skill
metadata:
  clawdbot:
    emoji: "🎙️"
    requires:
      env: []
    files: ["README.md", "README.zh-CN.md", "LICENSE", "scripts/*"]
---
# FunASR转录

使用FunASR对音频文件进行本地语音转文本处理。该工具特别适用于中文或中英文混合的音频文件，运行在本地机器上，无需使用付费的转录API。

## 使用场景

- 用户希望将`.wav`、`.ogg`、`.mp3`、`.flac`或`.m4a`格式的音频文件转换为文本。
- 由于隐私、成本或离线工作流程的需求，用户更倾向于使用本地ASR服务而非云语音API。
- 音频主要为中文（可能包含方言）或中英文混合。
- 用户愿意在首次使用时安装Python依赖库并下载模型文件。

**注意：** 如果用户明确禁止安装本地依赖库或任何网络访问（用于下载依赖库/模型），请勿使用此功能。

## 快速入门

```bash
# Install dependencies and create a virtual environment
bash ~/.openclaw/workspace/skills/funasr-transcribe/scripts/install.sh

# Transcribe an audio file
bash ~/.openclaw/workspace/skills/funasr-transcribe/scripts/transcribe.sh /path/to/audio.ogg
```

## 功能概述

- 默认情况下，在`~/.openclaw/workspace/funasr_env`目录下创建一个Python虚拟环境。
- 安装`funasr`、`torch`、`torchaudio`、`modelscope`及相关依赖库。
- 在本地加载FunASR模型，并将转录结果写入对应的`.txt`文件中。
- 将转录结果输出到标准输出（stdout），以便通过命令行直接使用。

## 使用的模型

- **语音识别（ASR）模型：** `damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch`
- **语音分割（VAD）模型：** `damo/speech fsmn_vad_zh-cn-16k-common-pytorch`
- **标点符号处理模型：** `damo/punc_ct-transformer_zh-cn-common-vocab272727-pytorch`

## 外部端点

| 端点 | 用途 | 发送的数据 |
| --- | --- | --- |
| `https://pypi.tuna.tsinghua.edu.cn/simple` | 在设置过程中安装Python包 | `pip`请求的包名称和安装器元数据 |
| FunASR依赖库使用的ModelScope和/或Hugging Face端点 | 首次运行时下载模型文件 | 模型标识符及标准HTTP请求元数据 |

## 安全性与隐私

- 音频文件从本地机器读取，并由FunASR在本地进行处理。
- 转录过程不会将音频内容上传到云端ASR API。
- 设置过程中以及首次运行模型时仍需要网络访问。
- 生成的转录结果会写入与源音频文件相同的本地`.txt`文件中（除非写入步骤失败）。
- 该功能默认不需要API密钥或其他敏感信息。

## 模型调用说明

用户可以自主调用该功能。如果用户请求转录本地音频，系统会自动安装依赖库并运行相关脚本（除非用户明确拒绝安装依赖库或使用网络访问）。

## 信任声明

使用此功能时，包和模型文件可能从第三方来源（如配置的PyPI镜像或模型托管服务）下载。只有在您信任这些来源的情况下，才建议安装和使用该功能。

## 常见问题解决方法

- 如果提示“找不到`python3`”，请安装Python 3.7及以上版本，然后重新运行`scripts/install.sh`。
- 如果在现有环境中安装失败，请运行`scripts/install.sh --force`以重新创建虚拟环境。
- 首次转录速度较慢：模型下载可能需要几分钟时间。
- 如果需要使用GPU进行计算，请在安装正确的CUDA版本后，修改`scripts/transcribe.py`文件中的`device="cpu"`为`device="cuda"`。
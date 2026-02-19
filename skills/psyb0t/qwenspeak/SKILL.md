---
name: qwenspeak
description: 通过 SSH 使用 Qwen3-TTS 进行文本转语音（Text-to-Speech）生成。支持预设语音、语音克隆以及语音设计功能。适用于用户需要生成语音音频、克隆语音或进行语音转换操作的场景。
compatibility: Requires ssh and a running qwenspeak instance. QWENSPEAK_HOST and QWENSPEAK_PORT env vars must be set.
metadata:
  author: psyb0t
  homepage: https://github.com/psyb0t/docker-qwenspeak
---
# qwenspeak

这是一个基于YAML格式的文本转语音工具，通过SSH连接并使用Qwen3-TTS模型来实现语音合成。有关安装和部署的详细信息，请参阅[references/setup.md](references/setup.md)。

## SSH封装层

所有命令均通过`scripts/qwenspeak.sh`脚本执行。该脚本通过环境变量`QWENSPEAK_HOST`和`QWENSPEAK_PORT`来配置主机地址和端口信息，并处理主机密钥的验证过程。

```bash
scripts/qwenspeak.sh <command> [args]
scripts/qwenspeak.sh <command> < input_file
scripts/qwenspeak.sh <command> > output_file
```

## 语音合成流程

用户提交YAML格式的指令后，系统会立即生成一个作业ID（UUID），并持续监控合成进度。所有作业会按顺序执行——每次仅处理一个作业，其余作业会进入等待队列。

```bash
# Get the YAML template
scripts/qwenspeak.sh "tts print-yaml" > job.yaml

# Submit job
scripts/qwenspeak.sh "tts" < job.yaml
# {"id": "550e8400-...", "status": "queued", "total_steps": 3, "total_generations": 7}

# Check progress
scripts/qwenspeak.sh "tts get-job 550e8400"

# Follow job log
scripts/qwenspeak.sh "tts get-job-log 550e8400 -f"

# Download result
scripts/qwenspeak.sh "get hello.wav" > hello.wav
```

## YAML文件结构

YAML文件包含全局配置以及一系列具体的语音合成步骤。每个步骤会加载相应的模型，执行所有必要的合成操作，完成后模型会被卸载。配置信息的优先级为：全局配置 > 单个步骤 > 具体合成操作。

```yaml
steps:
  - mode: custom-voice
    model_size: 1.7b
    speaker: Ryan
    language: English
    generate:
      - text: "Hello world"
        output: hello.wav
      - text: "I cannot believe this!"
        speaker: Vivian
        instruct: "Speak angrily"
        output: angry.wav

  - mode: voice-design
    generate:
      - text: "Welcome to our store."
        instruct: "A warm, friendly young female voice with a cheerful tone"
        output: welcome.wav

  - mode: voice-clone
    model_size: 1.7b
    ref_audio: ref.wav
    ref_text: "Transcript of reference"
    generate:
      - text: "First line in cloned voice"
        output: clone1.wav
      - text: "Second line"
        output: clone2.wav
```

## 合成模式

- **custom-voice**：从预定义的9种语音中选择一种。1.7B版本的模型支持通过`instruct`参数来指定情感或语音风格。
- **voice-design**：用户可以使用自然语言描述所需的语音特征（仅适用于1.7B版本）。
- **voice-clone**：根据参考音频文件克隆新的语音效果。用户需要在步骤级别设置`ref_audio`和`ref_text`参数，以便在多次合成过程中重复使用相同的参考音频。

### 克隆语音的特殊处理方法

如果需要克隆具有不同情感特征的语音，需要为每个克隆任务分别上传参考音频文件，并为每个任务创建独立的合成步骤。

```bash
scripts/qwenspeak.sh "create-dir refs"
scripts/qwenspeak.sh "put refs/happy.wav" < me_happy.wav
scripts/qwenspeak.sh "put refs/angry.wav" < me_angry.wav
```

## 作业管理

作业的状态包括：`queued`（等待中）→ `running`（正在执行）→ `completed`（已完成）→ `failed`（失败）→ `cancelled`（取消）。

已完成的任务会在1天后自动删除，所有未完成的任务会在1周后被清除。作业ID通常由前8个字符组成，用于唯一标识每个任务。

## 文件操作

所有文件路径都是相对于工作目录计算的。系统禁止直接遍历目录结构。

| 命令                | 功能                                      |
| ---------------------- | ---------------------------------- |
| `put <path>`           | 从标准输入（stdin）上传文件                         |
| `get <path>`           | 将文件下载到标准输出（stdout）                         |
| `list-files [--json]`      | 列出目录中的文件                               |
| `remove-file <path>`       | 删除文件                                   |
| `create-dir <path>`        | 创建目录                                   |
| `remove-dir <path>`       | 删除空目录                                   |
| `move-file <src> <dst>`      | 移动或重命名文件                               |
| `copy-file <src> <dst>`      | 复制文件                                   |
| `file-exists <path>`       | 检查文件是否存在（返回true/false）                         |
| `search-files <glob>`       | 全局搜索文件（支持递归）                         |

## 可用的语音库

| 语音名称 | 性别 | 语言 | 语言特点                                      |
| -------- | ------ | -------- | ---------------------------------------------- |
| Vivian   | 女性 | 中文 | 明亮、略带活力的年轻女性声音                         |
| Serena   | 女性 | 中文 | 温暖、柔和的年轻女性声音                         |
| Uncle_Fu | 男性 | 中文 | 经验丰富的男性声音，音色低沉而醇厚                 |
| Dylan    | 男性 | 中文 | 充满青春活力的北京方言，音色自然清晰                 |
| Eric     | 男性 | 中文 | 生动活泼的成都/四川方言，略带沙哑的音色                 |
| Ryan     | 男性 | 英文 | 充满活力的英语发音，节奏感强                         |
| Aiden    | 男性 | 英文 | 阳光般的美国口音，音色清晰                   |
| Ono_Anna | 女性 | 日文 | 活泼、轻快的语调                               |
| Sohee    | 女性 | 韩文 | 温暖且富有情感的表达方式                         |

## YAML配置选项

所有配置选项的优先级为：全局配置 > 单个步骤 > 具体合成操作。

| 参数                | 默认值 | 说明                                                  |
| -------------------- | --------- | ------------------------------------------------------------------- |
| `dtype`              | `float32` | 数据类型（float32、float16或bfloat16；仅限GPU支持）             |
| `flash_attn`         | `auto`    | 自动检测并切换数据类型（float32→bfloat16）                   |
| `temperature`        | `0.9`     | 采样温度设置                                   |
| `top_k`              | `50`      | 选择最重要的k个样本                               |
| `top_p`              | `1.0`     | 选择最重要的p个样本                               |
| `repetition_penalty` | `1.05`    | 重复内容的惩罚系数                             |
| `max_new_tokens`     | `2048`    | 最大允许的合成字符数                             |
| `no_sample`          | `false`   | 启用贪婪解码模式                               |
| `streaming`          | `false`   | 流式播放模式（延迟更低）                             |
| `mode`               | 必填    | 指定合成模式（`custom-voice`、`voice-design`或`voice-clone`）         |
| `model_size`         | `1.7b`    | 指定使用的模型大小（1.7B或0.6B）                         |
| `text`               | 必填    | 需要合成的文本                               |
| `output`             | 必填    | 输出文件的路径                               |
| `speaker`            | `Vivian`  | 选择的语音名称                               |
| `language`           | `Auto`    | 合成语言                               |
| `instruct`           | 可选    | `custom-voice`：指定情感或语音风格；`voice-design`：描述语音特征   |
| `ref_audio`          | 可选    | `voice-clone`：参考音频文件的路径                         |
| `ref_text`           | 可选    | `voice-clone`：参考音频的文字记录                         |
| `x_vector_only`      | 可选    | `voice-clone`：仅使用语音模型的嵌入特征                   |
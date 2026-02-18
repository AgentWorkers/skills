---
name: qwenspeak
description: 通过 SSH 使用 Qwen3-TTS 进行文本转语音（Text-to-Speech）生成。支持预设语音、语音克隆以及语音设计功能。适用于用户需要生成语音音频、克隆语音或使用 TTS 服务的情况。
compatibility: Requires ssh and a running qwenspeak instance. QWENSPEAK_HOST and QWENSPEAK_PORT env vars must be set.
metadata:
  version: 1.2.0
  author: psyb0t
  homepage: https://github.com/psyb0t/docker-qwenspeak
---
# qwenspeak

这是一个基于YAML的文本转语音工具，通过SSH使用Qwen3-TTS模型实现语音合成。所有命令都在一个经过安全隔离的容器中执行，该容器支持命令白名单机制和路径沙箱机制。

## 设置

请设置以下环境变量：

```bash
export QWENSPEAK_HOST=localhost
export QWENSPEAK_PORT=2222
```

## SSH封装层

使用`scripts/qwenspeak.sh`代替原始的SSH命令。该脚本会自动处理主机地址、端口号以及主机密钥的验证过程。

```bash
scripts/qwenspeak.sh <command> [args]
scripts/qwenspeak.sh <command> < input_file
scripts/qwenspeak.sh <command> > output_file
```

## 语音合成过程

语音合成任务以异步方式运行。用户提交YAML配置文件后，会立即收到任务的唯一标识符（UUID），然后可以随时查询任务的进度。

```bash
# Get the YAML template
scripts/qwenspeak.sh "tts print-yaml" > job.yaml

# Submit job (returns JSON with job ID immediately)
scripts/qwenspeak.sh "tts" < job.yaml
# {"id": "550e8400-...", "status": "pending", "total_steps": 3, "total_generations": 7}

# Check progress
scripts/qwenspeak.sh "tts get-job 550e8400"

# View job log
scripts/qwenspeak.sh "tts get-job-log 550e8400"

# Follow job log (like tail -f)
scripts/qwenspeak.sh "tts get-job-log 550e8400 -f"

# List all jobs
scripts/qwenspeak.sh "tts list-jobs"

# Cancel a running job
scripts/qwenspeak.sh "tts cancel-job 550e8400"

# Download result when done
scripts/qwenspeak.sh "get hello.wav" > hello.wav
```

### YAML配置结构

每个配置文件包含全局设置和一系列具体步骤。每个步骤会加载相应的模型，执行语音合成操作，完成后会释放模型资源。配置设置的优先级为：全局设置 > 单个步骤设置 > 单次语音合成设置。

```yaml
dtype: float32
models_dir: /models
temperature: 0.9

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
    ref_audio: /work/ref.wav
    ref_text: "Transcript of reference"
    generate:
      - text: "First line in cloned voice"
        output: clone1.wav
      - text: "Second line"
        output: clone2.wav
```

### 合成模式

- **custom-voice**：从9个预设的语音中选择一个进行合成。1.7B版本的模型支持通过`instruct`参数设置语音的情感和风格。
- **voice-design**：使用自然语言描述所需的语音特征（仅适用于1.7B版本）。
- **voice-clone**：根据参考音频文件克隆新的语音。用户需要在步骤配置中指定`ref_audio`和`ref_text`参数，以便在多次合成过程中重复使用该语音模板。使用`x_vector_only: true`可跳过文本转录环节。

### 克隆语音时的情感处理方法

可以通过上传具有不同情感的参考音频文件，并为每个情感创建单独的合成步骤来实现个性化的语音效果。

```bash
scripts/qwenspeak.sh "create-dir refs"
scripts/qwenspeak.sh "put refs/happy.wav" < me_happy.wav
scripts/qwenspeak.sh "put refs/angry.wav" < me_angry.wav
```

## 任务管理

任务的状态包括：`pending`（待处理）→ `running`（运行中）→ `completed`（已完成）→ `failed`（失败）→ `cancelled`（取消）。

任务是临时性的——在任务完成、失败或被取消后，以及容器重启时，相关资源会被自动清理。

## 其他命令

```bash
# List available speakers
scripts/qwenspeak.sh "tts list-speakers"

# View logs (includes output from background jobs)
scripts/qwenspeak.sh "tts log"
scripts/qwenspeak.sh "tts log -f"
scripts/qwenspeak.sh "tts log -n 100"

# Tokenize round-trip
scripts/qwenspeak.sh "tts tokenize input.wav"
```

## 文件操作

所有文件路径都是相对于`/work`目录的。系统禁止直接访问外部文件系统。

| 命令                | 功能描述                          | 示例                                                         |
| ---------------------- | ------------------------------------ | --------------------------------------------------------------- |
| `list-files`           | 列出目录内容                          | `scripts/qwenspeak.sh "list-files"`                                |
| `put`                  | 从标准输入（stdin）上传文件                | `scripts/qwenspeak.sh "put ref.wav" < ref.wav`                     |
| `get`                  | 将文件内容写入标准输出（stdout）             | `scripts/qwenspeak.sh "get out.wav" > out.wav`                     |
| `remove-file`          | 删除文件                          | `scripts/qwenspeak.sh "remove-file old.wav"`                       |
| `create-dir`           | 创建目录                          | `scripts/qwenspeak.sh "create-dir refs"`                           |
| `remove-dir`           | 删除空目录                          | `scripts/qwenspeak.sh "remove-dir refs"`                           |
| `remove-dir-recursive` | 递归删除目录                        | `scripts/qwenspeak.sh "remove-dir-recursive refs"`                 |
| `move-file`            | 移动或重命名文件                        | `scripts/qwenspeak.sh "move-file old.wav new.wav"`                 |
| `copy-file`            | 复制文件                          | `scripts/qwenspeak.sh "copy-file src.wav dst.wav"`                 |
| `file-info`            | 获取文件的元数据（JSON格式）                  | `scripts/qwenspeak.sh "file-info out.wav"`                         |
| `file-exists`          | 检查文件是否存在                      | `scripts/qwenspeak.sh "file-exists out.wav"`                       |
| `file-hash`            | 计算文件的SHA-256哈希值                    | `scripts/qwenspeak.sh "file-hash out.wav"`                         |
| `disk-usage`           | 显示文件或目录占用的磁盘空间                | `scripts/qwenspeak.sh "disk-usage refs"`                           |
| `search-files`         | 全局搜索文件（支持递归）                    | `scripts/qwenspeak.sh "search-files **/*.wav"`                     |
| `append-file`          | 将标准输入内容追加到现有文件                | `scripts/qwenspeak.sh "append-file log.txt" < extra.txt`           |

## 可用的语音合成引擎

| 语音名称   | 性别   | 语言   | 语言特征描述                                      |
| --------- | ------ | -------- | --------------------------------------------------------------- |
| Vivian    | 女性   | 中文   | 明亮、略带活力的年轻女性声音                          |
| Serena    | 女性   | 中文   | 温暖、柔和的年轻女性声音                            |
| Uncle_Fu  | 男性   | 中文   | 经验丰富的中年男性声音                          |
| Dylan     | 男性   | 中文   | 充满活力的北京方言，音色自然                      |
| Eric      | 男性   | 中文   | 生动活泼的成都/四川方言，略带沙哑的音色                |
| Ryan      | 男性   | 英文   | 具有强烈节奏感的英语发音                      |
| Aiden     | 男性   | 英文   | 阳光般的美国口音，音色清晰                      |
| Ono_Anna  | 女性   | 日文   | 活泼、轻快的女性声音                          |
| Sohee     | 女性   | 韩文   | 温暖且富有情感的表达方式                          |

## YAML配置选项

所有设置可以在全局、步骤或单次语音合成级别进行配置。较低级别的设置会覆盖较高级别的设置。设备的具体配置由容器中的`PROCESSING_UNIT`环境变量控制，而非YAML文件。

| 参数                | 默认值       | 说明                                                  |
| -------------------- | --------- | ------------------------------------------------------------ |
| `dtype`              | `float32`   | 模型数据类型：float32、float16或bfloat16（仅限GPU支持）         |
| `flash_attn`         | `false`    | 是否使用FlashAttention-2算法（仅限GPU）                   |
| `temperature`        | `0.9`     | 采样温度设置                                      |
| `top_k`              | `50`      | 最大采样数量                                      |
| `top_p`              | `1.0`     | 最高级采样方法                                      |
| `repetition Penalty` | `1.05`    | 重复处理时的惩罚系数                                      |
| `max_new_tokens`     | `2048`    | 最大可生成的代码片段数量                              |
| `no_sample`          | `false`    | 是否启用贪婪解码模式                                  |
| `streaming`          | `false`    | 是否启用流式输出模式（降低延迟）                          |
| `mode`               | 必填     | 合成模式：`custom-voice`、`voice-design`或`voice-clone`         |
| `model_size`         | `1.7b`    | 模型大小（1.7B或0.6B）                                  |
| `text`               | 必填     | 需要合成的文本                                      |
| `output`             | 必填     | 输出文件路径（相对于 `/work` 目录）                         |
| `speaker`            | `Vivian`   | 选择的语音名称                                      |
| `language`           | `Auto`    | 合成语言                                      |
| `instruct`           | 可选     | `custom-voice`：指定情感/风格；`voice-design`：语音描述        |
| `ref_audio`          | 可选     | `voice-clone`：参考音频文件路径                        |
| `ref_text`           | 可选     | `voice-clone`：参考音频的文字记录                        |
| `x_vector_only`      | 可选     | `voice-clone`：是否仅使用语音模型嵌入数据进行合成           |
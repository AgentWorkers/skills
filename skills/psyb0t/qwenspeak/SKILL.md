---
name: qwenspeak
description: 通过锁定的 SSH 容器使用 Qwen3-TTS 实现文本转语音功能：支持预设语音、语音克隆以及语音设计功能。
homepage: https://github.com/psyb0t/docker-qwenspeak
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🗣️",
        "primaryEnv": "QWENSPEAK_HOST",
        "always": false,
      },
  }
---

# qwenspeak

## 必需的设置

使用此功能需要设置 `QWENSPEAK_HOST` 和 `QWENSPEAK_PORT` 环境变量，这些变量应指向正在运行的 qwenspeak 实例。

**配置 OpenClaw**（`~/.openclaw/openclaw.json`）：

```json
{
  "skills": {
    "entries": {
      "qwenspeak": {
        "env": {
          "QWENSPEAK_HOST": "localhost",
          "QWENSPEAK_PORT": "2222"
        }
      }
    }
  }
}
```

或者直接设置环境变量：

```bash
export QWENSPEAK_HOST=localhost
export QWENSPEAK_PORT=2222
```

---

Qwen3-TTS 是一个基于 SSH 的文本转语音（TTS）工具，它使用 YAML 格式的配置文件来控制多个模型的批量处理。该工具通过一个 Python 包装层来执行命令，仅允许预定义的命令被执行，从而确保了安全性：没有 shell 访问权限，也不会发生任何注入攻击。

## 首次连接

在运行任何命令之前，您必须接受宿主机的密钥，以便将其添加到 `known_hosts` 文件中。运行 `ls` 命令并接受显示的密钥指纹：

```bash
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "ls"
```

如果是首次连接，SSH 会提示您验证密钥。输入 `yes` 以接受该密钥。每个主机只需执行此操作一次。如果跳过此步骤，后续的 SSH 命令将因密钥验证失败而失败。

## 工作原理

所有命令都是通过 SSH 连接到 qwenspeak 容器来执行的。该容器强制所有连接都必须通过一个 Python 包装层，该包装层仅允许预定义的命令通过。所有文件路径都被限制在容器内的 `/work` 目录内。

**SSH 命令格式**：

```bash
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "<command> [args]"
```

## TTS 命令

| 命令        | 执行路径                | 功能描述                        |
| -------------- | ---------------------- | --------------------------- |
| `tts`       | `/usr/local/bin/tts`         | 执行文本转语音功能                   |

### 子命令

| 子命令          | 功能描述                                      | --------------------------- |
| `print-yaml`    | 将 YAML 配置文件内容输出到标准输出            |
| `list-speakers` | 列出可用的预设语音合成器                   |
| `tokenize`    | 对音频数据进行编码/解码                    |

当不带子命令调用 `tts` 时，它会从标准输入（stdin）读取 YAML 配置文件并执行相应的处理流程。

## YAML 配置文件

所有的语音合成操作都是通过标准输入（stdin）传递的 YAML 配置文件来控制的。您需要获取一个配置模板，填写相关内容后，再将其传回系统。

```bash
# Get the YAML template
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "tts print-yaml" > job.yaml

# Edit it locally, then run it
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "tts" < job.yaml

# Download results
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "get hello.wav" > hello.wav
```

### YAML 配置结构

每个配置文件包含全局设置和一系列处理步骤。每个步骤会加载相应的模型，执行所有必要的处理（如语音合成），然后释放模型资源。设置值的优先级为：全局 → 单步 → 合成过程。

```yaml
device: cpu
dtype: float32
models_dir: /models
temperature: 0.9

steps:
  # custom-voice: preset speakers with optional emotion control
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

  # voice-design: describe the voice in natural language
  - mode: voice-design
    generate:
      - text: "Welcome to our store."
        instruct: "A warm, friendly young female voice with a cheerful tone"
        output: welcome.wav

  # voice-clone: clone a voice from reference audio
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

### 使用模式

- **custom-voice**：从 9 个预设语音合成器中选择一个进行语音合成。1.7B 模型支持通过 `instruct` 参数设置情感和风格。
- **voice-design**：使用 `instruct` 参数以自然语言描述所需的语音特征。仅适用于 1.7B 模型。
- **voice-clone**：根据参考音频克隆新的语音合成器。在步骤级别设置 `ref_audio` 和 `ref_text` 参数，以便在不同合成步骤中重复使用相同的语音效果。可以使用 `x_vector_only: true` 选项跳过文本转录过程。

### 克隆语音的技巧

如果您希望克隆具有不同情感的语音，可以分别录制不同情感的语音文件，并为每个情感创建单独的处理步骤：

```bash
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "mkdir refs"
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "put refs/happy.wav" < me_happy.wav
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "put refs/angry.wav" < me_angry.wav
```

```yaml
steps:
  - mode: voice-clone
    ref_audio: /work/refs/happy.wav
    ref_text: "transcript of happy ref"
    generate:
      - text: "Great news everyone!"
        output: happy1.wav

  - mode: voice-clone
    ref_audio: /work/refs/angry.wav
    ref_text: "transcript of angry ref"
    generate:
      - text: "This is unacceptable"
        output: angry1.wav
```

## 文件操作

所有文件路径都是相对于 `/work` 目录的。系统会阻止对其他目录的访问；绝对路径会被自动映射到 `/work` 目录下。

| 命令           | 功能描述                                      | 示例                                      |
| ------------------ | -------------------------------------- | ------------------------------------------- |
| `ls`          | 列出 `/work` 目录或其子目录                         | `ls` 或 `ls --json subdir`                         |
| `put`          | 从标准输入（stdin）上传文件                         | `put ref.wav`                             |
| `get`          | 将文件内容输出到标准输出（stdout）                     | `get output.wav`                         |
| `rm`          | 删除文件（不支持删除目录）                             | `rm old.wav`                             |
| `mkdir`         | 创建目录（支持递归）                              | `mkdir refs`                             |
| `rmdir`         | 删除空目录                                   | `rmdir refs`                             |
| `rrmdir`        | 递归删除目录及其所有内容                           | `rrmdir refs`                             |

## 可用的语音合成器

| 合成器名称    | 性别    | 语言    | 语言特征描述                                      |
| -------------- | ------- | -------- | ------------------------------------------- |
| Vivian       | 女性    | 中文    | 明亮、略带叛逆的年轻女性声音                   |
| Serena       | 女性    | 中文    | 温暖、柔和的年轻女性声音                   |
| Uncle_Fu      | 男性    | 中文    | 经验丰富的低沉男性声音                     |
| Dylan       | 男性    | 中文    | 年轻的北京方言，音色自然清晰                 |
| Eric        | 男性    | 中文    | 生动活泼的成都/四川方言，略带沙哑质感             |
| Ryan        | 男性    | 英文    | 充满活力的英语发音，节奏感强                   |
| Aiden        | 男性    | 英文    | 阳光般的美国英语发音，音色清晰                 |
| Ono_Anna     | 女性    | 日文    | 活泼、轻快的日语发音                     |
| Sohee       | 女性    | 韩文    | 温暖且富有情感的表达方式                   |

## YAML 配置选项

这些选项可以在全局、单步或合成步骤级别进行设置。较低级别的设置会覆盖较高级别的设置。

| 参数名        | 默认值    | 描述                                      |
| ------------------ | -------------- | ------------------------------------------- |
| `device`       | `cpu`     | 使用的设备（如 cpu、cuda:0 等）                   |
| `dtype`       | `float32`   | 模型的数据类型（float32、float16 或 bfloat16，仅限 GPU）       |
| `flash_attn`     | `false`    | 是否使用 FlashAttention-2 算法（仅限 GPU）             |
| `temperature`    | `0.9`     | 采样温度设置                         |
| `top_k`       | `50`      | 最大采样数量                         |
| `top_p`       | `1.0`     | 最高级采样方法（top-p 或 nucleus）                 |
| `repetition Penalty` | `1.05`    | 重复处理时的惩罚系数                         |
| `max_new_tokens`    | `2048`    | 最大允许的合成token数量                   |
| `no_sample`     | `false`    | 是否启用贪婪解码模式                         |
| `streaming`     | `false`    | 是否启用流式处理模式（延迟更低）                   |
| `mode`        | 必填参数 | 指定处理模式（custom-voice、voice-design 或 voice-clone）       |
| `model_size`     | `1.7b`    | 指定使用的模型大小（1.7b 或 0.6b）                 |
| `text`       | 必填参数 | 合成所需的输入文本                         |
| `output`      | 必填参数 | 合成后的输出文件路径（相对于 `/work` 目录）             |
| `speaker`      | `Vivian`    | 使用的语音合成器名称                     |
| `language`     | `Auto`     | 合成使用的语言                         |
| `instruct`     | 可选参数 | 设置语音的情感/风格（custom-voice）或语音描述（voice-design）     |
| `ref_audio`     | 可选参数 | 用于克隆语音的参考音频文件路径                     |
| `ref_text`     | 可选参数 | 用于克隆语音的参考音频文本                     |
| `x_vector_only`    | 可选参数 | 是否仅使用语音嵌入数据进行合成（voice-clone）           |

### 显示可用的语音合成器列表

```bash
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "tts list-speakers"
```

### 文件管理相关命令

```bash
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "ls"
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "ls --json"
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "rm old.wav"
ssh -p $QWENSPEAK_PORT tts@$QWENSPEAK_HOST "rrmdir refs"
```

## 安全注意事项

- 禁止直接访问 shell：所有命令都通过 Python 包装层执行。
- 仅允许预定义的命令：未列出的命令将被拒绝。
- 防止注入攻击：操作符 `&&`、`;`、`|`、`$()` 被视为字面参数，不会被解释为 shell 命令。
- 仅使用 SSH 密钥认证：不支持密码输入。
- 禁止任何文件路径的直接访问：所有文件操作都限制在 `/work` 目录内进行。
- 所有文件路径都被强制映射到 `/work` 目录下。
---
name: mlx-local-inference
description: >
  在基于 Apple Silicon 的 Mac 电脑上，通过 MLX 构建了一个完整的本地 AI 推理栈。该栈支持以下功能：  
  - 大语言模型（LLM）聊天（Qwen3-14B、Gemma3-12B）  
  - 语音转文本（ASR）功能（Qwen3-ASR、Whisper）  
  - 文本嵌入（Qwen3-Embedding 0.6B/4B）  
  - 光学字符识别（OCR）功能（PaddleOCR-VL）  
  - 语音转文本（TTS）功能（Qwen3-TTS）  
  - 以及一个具备 LLM 校正功能的自动转录工具。  
  所有模型均通过 MLX 在本地运行，并使用与 OpenAI 兼容的 API 进行交互。当用户需要本地 AI 功能时（如文本生成、语音识别、文本嵌入/向量搜索、OCR、语音转文本或批量音频转录），无需依赖云 API 即可使用该栈。
metadata: { "openclaw": { "os": ["darwin"], "requires": { "anyBins": ["python3"] } } }
---
# MLX 本地推理栈

在基于 Apple Silicon 的 Mac 上实现完整的本地 AI 推理功能。所有服务均提供与 OpenAI 兼容的 API。

## 服务概览

| 服务 | 端口 | 访问方式 | 模型 |
|---------|------|--------|--------|
| **大语言模型（LLM）+ Whisper + 嵌入模型（Embedding）** | 8787 | 局域网（`0.0.0.0`） | qwen3-14b, gemma-3-12b, whisper-large-v3-turbo, qwen3-embedding-0.6b/4b |
| **自动语音识别（ASR，基于 Qwen3-ASR）** | 8788 | 仅限本地主机访问 | Qwen3-ASR-1.7B-8bit |
| **转录守护进程（Transcribe Daemon）** | — | 基于文件处理 | 使用 ASR + LLM |

启动代理：`com.mlx-server`（8787），`com.mlx-audio-server`（8788），`com.mlx-transcribe-daemon`

---

## 1. 大语言模型（LLM）——本地聊天辅助

### 模型

| 模型 ID | 参数 | 适用场景 |
|----------|--------|----------|
| `qwen3-14b` | 140 亿参数（4 位精度） | 中文处理、深度推理（内置思考模式） |
| `gemma-3-12b` | 120 亿参数（4 位精度） | 英文处理、代码生成 |

### API

```bash
curl -X POST http://localhost:8787/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-14b",
    "messages": [{"role": "user", "content": "Hello"}],
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

若需流式处理，请添加 `"stream": true` 参数。

### Python 代码示例

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:8787/v1", api_key="unused")
response = client.chat.completions.create(
    model="qwen3-14b",
    messages=[{"role": "user", "content": "Hello"}],
    temperature=0.7, max_tokens=2048
)
print(response.choices[0].message.content)
```

### Qwen3 思考模式

Qwen3 会使用 `<think>...</think>` 标签来表示思考过程。可以使用以下代码去除这些标签：

```python
import re
text = re.sub(r'<think>.*?</think>\s*', '', text, flags=re.DOTALL)
```

### 模型选择指南

| 场景 | 推荐模型 |
|----------|-------------|
| 中文文本 | `qwen3-14b` |
| 粤语文本 | `qwen3-14b` |
| 英文写作 | `gemma-3-12b` |
| 代码生成 | 任一模型均可 |
| 深度推理 | `qwen3-14b`（思考模式） |
| 快速问答 | `gemma-3-12b` |

---

## 2. 自动语音识别（ASR）——语音转文本

### Qwen3-ASR（适用于中文/粤语）

```bash
curl -X POST http://127.0.0.1:8788/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=mlx-community/Qwen3-ASR-1.7B-8bit" \
  -F "language=zh"
```

### Whisper（支持多种语言，共 99 种语言）

```bash
curl -X POST http://localhost:8787/v1/audio/transcriptions \
  -F "file=@audio.wav" \
  -F "model=whisper-large-v3-turbo"
```

### ASR 模型对比

| | Qwen3-ASR（端口 8788） | Whisper（端口 8787） |
|---|---|---|
| 中文/粤语识别 | **表现优异** | 表现一般 |
| 多语言支持 | 不支持 | 支持（99 种语言） |
| 是否支持局域网访问 | 不支持（仅限本地主机） | 支持 |
| 加载方式 | 按需加载 | 始终处于加载状态 |

### 支持的音频格式

wav, mp3, m4a, flac, ogg, webm

### 长音频文件处理

建议将长音频文件分割成 10 分钟左右的片段进行处理：

```bash
ffmpeg -y -ss 0 -t 600 -i long.wav -ar 16000 -ac 1 chunk_000.wav
```

---

## 3. 嵌入模型（Embedding）——文本向向量转换

### 模型

| 模型 ID | 参数 | 适用场景 |
|----------|------|----------|
| `qwen3-embedding-0.6b` | 600 万参数（4 位精度） | 快速检索、低延迟 |
| `qwen3-embedding-4b` | 400 万参数（4 位精度） | 高精度语义匹配 |

### API

```bash
curl -X POST http://localhost:8787/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-embedding-0.6b", "input": "text to embed"}'
```

### 批量处理示例

```bash
curl -X POST http://localhost:8787/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "qwen3-embedding-4b", "input": ["text 1", "text 2"]}'
```

---

## 4. 文本识别（OCR）——图像转文本

### 默认模型：PaddleOCR-VL-1.5-6bit

| 参数 | 值 |
|------|-------|
| 模型 ID | `paddleocr-vl-6bit` |
| 处理速度 | 约 185 张/秒 |
| 内存占用 | 约 3.3 GB |
| 使用指令 | `OCR:` |

### 命令行接口（CLI）

```bash
cd ~/.mlx-server/venv
python -m mlx_vlm.generate \
  --model mlx-community/PaddleOCR-VL-1.5-6bit \
  --image image.jpg \
  --prompt "OCR:" \
  --max-tokens 512 --temp 0.0
```

### Python 代码示例

```python
from mlx_vlm import generate, load
from mlx_vlm.prompt_utils import apply_chat_template
from mlx_vlm.utils import load_config

model, processor = load("mlx-community/PaddleOCR-VL-1.5-6bit")
config = load_config("mlx-community/PaddleOCR-VL-1.5-6bit")
prompt = apply_chat_template(processor, config, "OCR:", num_images=1)
out = generate(model, processor, prompt, "image.jpg",
               max_tokens=512, temperature=0.0, verbose=False)
print(out.text if hasattr(out, "text") else out)
```

### 注意事项：
- 使用 PaddleOCR-VL 时，指令必须为 `OCR:` |
- 设置 `temperature=0.0` 可获得确定性输出结果 |
- RGBA 格式的图像需先转换为 RGB 格式 |
- 开发环境：`~/.mlx-server/venv`

---

## 5. 语音合成（TTS）——文本转语音

### 模型：Qwen3-TTS（结果为缓存形式，非实时生成）

| 参数 | 值 |
|------|-------|
| 模型 | Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit |
| 内存占用 | 约 2 GB |
| 特点 | 支持自定义语音克隆 |

### 命令行接口（CLI）

```bash
~/.mlx-server/venv/bin/mlx_audio.tts.generate \
  --model mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit \
  --text "你好，这是一段测试语音"
```

### 通过 API 使用（通过端口 8788 的 `mlx_audio.server`）

```bash
curl -X POST http://127.0.0.1:8788/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit",
    "input": "你好世界"
  }' --output speech.wav
```

---

## 6. 转录守护进程（Transcribe Daemon）——自动批量转录

将音频文件放入 `~/transcribe/` 目录，系统会自动进行处理：

1. 守护进程每 15 秒检测一次文件；
2. **第一步**：使用 Qwen3-ASR 进行转录，生成 `filename_raw.md` 文件；
3. **第二步**：使用 Qwen3-14B LLM 进行修正，生成 `filename_corrected.md` 文件；
4. 最后将结果保存到 `~/transcribe/done/` 目录。

### LLM 修正规则：
- 修正同音词错误（如 “的/得/地, 在/再”）；
- 保留粤语字符（如 “嘅、唔、咁、喺、冇、佢”）；
- 添加标点符号和段落格式；
- 删除冗余词汇。

### 支持的音频格式

wav, mp3, m4a, flac, ogg, webm

---

## 服务管理

```bash
# LLM + Whisper + Embedding server (port 8787)
launchctl kickstart -k gui/$(id -u)/com.mlx-server

# ASR server (port 8788)
launchctl kickstart -k gui/$(id -u)/com.mlx-audio-server

# Transcribe daemon
launchctl kickstart gui/$(id -u)/com.mlx-transcribe-daemon

# Logs
tail -f ~/.mlx-server/logs/server.log
tail -f ~/.mlx-server/logs/mlx-audio-server.err.log
tail -f ~/.mlx-server/logs/transcribe-daemon.err.log
```

## 系统要求

- 使用基于 Apple Silicon 的 Mac（M1/M2/M3/M4）；
- 安装 Python 3.10 及相关的依赖库（mlx, mlx-lm, mlx-audio, mlx-vlm）；
- 建议配置 32 GB 以上的内存以同时运行多个模型。
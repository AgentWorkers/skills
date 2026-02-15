---
name: krea-api
description: 通过 Krea.ai API 生成图像（Flux、Imagen、Ideogram、Seedream 等）
version: 0.2.0
---

# Krea.ai 图像生成技能

使用 Krea.ai 的 API 生成图像，支持多种模型，包括 Flux、Imagen 4、Ideogram 3.0 等。

## 特点

- ✅ 异步任务生成（POST → 轮询 → 结果）
- ✅ 支持多种图像模型
- ✅ 可配置参数（宽度、高度、生成步骤、引导信息、随机种子）
- 仅依赖标准库（无需 `requests`）
- 以安全为首要考虑的凭证处理方式（仅使用文件存储凭证，不使用子进程）

## 安全性

本技能注重安全性：

- **不使用子进程** – 凭证信息仅从文件中读取
- **不支持 Webhook** – 为防止 SSRF（跨站请求伪造）风险
- **凭证信息存储在文件中** – 凭证来源单一
- **依赖标准库** – 击击面最小

## 设置

1. 从 [https://docs.krea.ai/developers/api-keys-and-billing](https://docs.krea.ai/developers/api-keys-and-billing) 获取 Krea.ai 的 API 凭证。
2. 创建凭证文件：
```bash
mkdir -p ~/.clawdbot/credentials
```

3. 添加你的凭证信息：
```bash
echo '{"apiKey": "YOUR_KEY_ID:YOUR_SECRET"}' > ~/.clawdbot/credentials/krea.json
```

4. 设置安全权限：
```bash
chmod 600 ~/.clawdbot/credentials/krea.json
```

## 使用方法

### 命令行

```bash
# Generate an image
python3 krea_api.py --prompt "A sunset over the ocean"

# With specific model
python3 krea_api.py --prompt "Cyberpunk city" --model imagen-4

# Custom size
python3 krea_api.py --prompt "Portrait" --width 1024 --height 1280

# List available models
python3 krea_api.py --list-models

# Check recent jobs
python3 krea_api.py --jobs 10
```

### Python 脚本

```python
from krea_api import KreaAPI

api = KreaAPI()  # Reads from ~/.clawdbot/credentials/krea.json

# Generate and wait
urls = api.generate_and_wait(
    prompt="A serene Japanese garden",
    model="flux",
    width=1024,
    height=1024
)
print(urls)
```

### 参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| prompt | str | 必填 | 图像描述（最多 1800 个字符） |
| model | str | "flux" | 下表中的模型名称 |
| width | int | 1024 | 图像宽度（512-2368） |
| height | int | 1024 | 图像高度（512-2368） |
| steps | int | 25 | 生成步骤（1-100） |
| guidance_scale | float | 3.0 | 引导信息的缩放比例（0-24） |
| seed | str | 可选 | 用于生成可重复结果的随机种子 |

### 可用模型

| 模型 | 适用场景 |
|-------|----------|
| flux | 通用用途，高质量图像 |
| imagen-4 | 最新的 Google 模型 |
| ideogram-3.0 | 将文本转换为图像 |
| seedream-4 | 快速生成图像 |
| nano-banana | 快速预览图像 |

运行 `python3 krea_api.py --list-models` 可查看所有可用模型。

## 使用情况检查

Krea.ai 不提供公共的 API 用于检查使用情况。你可以在以下链接查看自己的使用数据：

https://www.krea.ai/settings/usage-statistics

或者查看最近的生成任务：

```bash
python3 krea_api.py --jobs 10
```

## 文件位置

| 文件用途 | 文件路径 |
|---------|------|
| 凭证信息 | `~/.clawdbot/credentials/krea.json` |
| 脚本 | `{skill}/krea_api.py` |
| 技能文档 | `{skill}/SKILL.md` |

## 故障排除

### “需要 API 凭证”

1. 确认凭证文件是否存在：
```bash
cat ~/.clawdbot/credentials/krea.json
```

2. 检查文件权限：
```bash
ls -la ~/.clawdbot/credentials/krea.json
# Should show: -rw-------
```

3. 确认文件格式（必须包含冒号）：
```json
{"apiKey": "KEY_ID:SECRET"}
```

### 模型未找到

运行 `python3 krea_api.py --list-models` 查看可用模型。

## 致谢

感谢 Claude Opus 4.5 帮助研究正确的 API 结构。官方文档错误地提示使用 `/v1/images/flux`，但实际上有效的端点是 `/generate/image/bfl/flux-1-dev`。
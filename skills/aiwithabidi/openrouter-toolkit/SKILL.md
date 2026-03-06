---
name: openrouter-toolkit
description: The definitive OpenRouter skill — intelligent model routing by task type, cost tracking with budget alerts, automatic fallback chains, side-by-side model comparison, and savings recommendations. Use for optimizing AI model selection, controlling costs, and building resilient LLM pipelines.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83d\udd00", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🔀 OpenRouter 工具包

专为 OpenClaw 代理设计的综合性 OpenRouter 工具包。集智能模型路由、成本跟踪、备用方案以及模型比较等功能于一身。

## 主要特性

- **智能路由**：根据任务类型自动选择最适合的模型——无论是代码生成、推理、创意写作还是成本敏感的任务。
- **成本跟踪**：记录每次 API 调用的成本，并跟踪每日/每周/每月的支出情况。
- **备用方案**：当主模型失败或超时时，会自动使用备用模型进行重试。
- **模型比较**：向多个模型发送相同的请求，然后对比它们的质量和成本。
- **预算警报**：设置支出限制，在超出预算前发出警告。
- **实时模型数据**：从 OpenRouter 的 API 获取最新的价格和模型功能信息。

## 所需环境

- `OPENROUTER_API_KEY`：您的 OpenRouter API 密钥。
- Python 3.10 及以上版本，并安装 `requests` 库（大多数环境中已预装）。

## 使用方法

### 智能路由
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py route --task code
python3 {baseDir}/scripts/openrouter_toolkit.py route --task reasoning
python3 {baseDir}/scripts/openrouter_toolkit.py route --task creative
python3 {baseDir}/scripts/openrouter_toolkit.py route --task fast
python3 {baseDir}/scripts/openrouter_toolkit.py route --task cheap
```

### 模型比较
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py compare --prompt "Explain recursion" --models "anthropic/claude-sonnet-4,openai/gpt-4o-mini"
```

### 备用方案
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py fallback --prompt "Hello" --chain "anthropic/claude-opus-4,anthropic/claude-sonnet-4,openai/gpt-4o-mini"
```

### 成本跟踪
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py cost --period daily
python3 {baseDir}/scripts/openrouter_toolkit.py cost --period weekly
python3 {baseDir}/scripts/openrouter_toolkit.py cost --period monthly
```

### 预算警报
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py budget --set 50.00
python3 {baseDir}/scripts/openrouter_toolkit.py budget --check
```

### 列出所有模型
```bash
python3 {baseDir}/scripts/openrouter_toolkit.py models --top 20
python3 {baseDir}/scripts/openrouter_toolkit.py models --search claude
python3 {baseDir}/scripts/openrouter_toolkit.py models --best code
```

## 智能路由的工作原理

该工具包根据任务类型，利用以下规则为模型评分：

| 任务类型 | 优先级 | 推荐模型 |
|------|------------|----------------|
| 代码生成 | 需要大量上下文信息 | Claude Opus, GPT-4o |
| 推理 | 需要较强的思维能力 | Claude Opus, o1 |
| 创意写作 | 需要高质量的创意输出 | Claude Sonnet, GPT-4o |
| 快速响应 | 响应时间短且质量尚可 | Claude Haiku, GPT-4o-mini |
| 成本敏感 | 每个词元的成本最低 | Gemini Flash, GPT-4o-mini |

## 数据存储

成本日志存储在 `{baseDir}/data/openrouter_costs.db` 文件中。

## 开发者信息

由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 共同开发。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
本工具包是 **AgxntSix 技能套件** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
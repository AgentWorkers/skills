# TokenGuard — LLM API 429 防御引擎

<!-- 🌌 经 Aoineco 验证 | S-DNA: AOI-2026-0213-SDNA-TG01 -->

**版本:** 1.5.0  
**作者:** Aoineco & Co.  
**许可证:** MIT  
**标签:** 速率限制、429 错误防护、令牌管理、成本优化、高性能

## 产品描述

TokenGuard 可在请求发送之前进行拦截，从而防止 LLM API 发生 429 错误（即速率限制或资源耗尽）。专为使用免费/低成本 API 计划的用户设计，帮助他们在有限的预算内获得最高的智能输出。

**核心理念：**“智能的价值不在于你花费了多少，而在于你实际需要多少。”

## 问题所在

在使用 LLM API 时（尤其是 Google Gemini Flash，其每分钟的最大请求次数为 100 万次）：
- 大文件（如 docx、PDF）可能会在一次请求中消耗掉全部配额；
- 失败的请求仍会计入令牌使用量；
- 429 错误后的重试循环会进一步消耗令牌，导致令牌迅速耗尽；
- 无法检测到恶意或重复的请求。

## 主要功能

| 功能 | 详细描述 |
|---------|-------------|
| **请求前令牌预估** | 在调用 API 之前预估所需的令牌数量（支持中文处理，无需依赖 tiktoken） |
| **实时配额监控** | 通过滑动窗口实时跟踪每个模型每分钟的令牌使用情况 |
| **智能限流** | 当配额使用率达到 80% 时自动等待，超过 95% 时直接阻止请求 |
| **重复请求检测** | 在 60 秒内阻止重复的请求（连续三次即视为恶意请求） |
| **响应缓存** | 对重复请求缓存成功的响应结果 |
| **模型自动切换** | 当主模型资源耗尽时，自动切换到更便宜或可用的模型 |
| **429 错误解析** | 从 Google/Anthropic 的错误响应中提取准确的重试延迟信息 |
| **区分批量请求与错误循环** | 区分正常的批量处理行为和错误导致的重复请求 |

## 支持的模型

预配置的配额包括：
- `gemini-3-flash`（每分钟 100 万次请求）
- `gemini-3-pro`（每分钟 200 万次请求）
- `claude-haiku`（每分钟 5 万次请求）
- `claude-sonnet`（每分钟 20 万次请求）
- `claude-opus`（每分钟 20 万次请求）
- `gpt-4o`（每分钟 80 万次请求）
- `deepseek`（每分钟 100 万次请求）

支持为任何模型自定义配额。

## 使用方法

```python
from token_guard import TokenGuard

guard = TokenGuard()

# Before every API call:
decision = guard.check(prompt_text, model="gemini-3-flash")

if decision.action == "proceed":
    response = call_your_api(prompt_text)
    guard.record_usage(decision.estimated_tokens, model="gemini-3-flash")
    guard.cache_response(prompt_text, response)

elif decision.action == "wait":
    time.sleep(decision.wait_seconds)
    # retry

elif decision.action == "fallback":
    response = call_your_api(prompt_text, model=decision.fallback_model)

elif decision.action == "block":
    print(f"Blocked: {decision.reason}")

# If you get a 429 error:
guard.record_429("gemini-3-flash", retry_delay=53.0)
```

## 与 OpenClaw 的集成

将 TokenGuard 添加到代理的配置文件中，或作为中间件使用：

```yaml
skills:
  - token-guard
```

代理可以在调用任何 LLM API 之前触发 TokenGuard，以防止配额耗尽。

## 文件结构

```
token-guard/
├── SKILL.md          # This file
└── scripts/
    └── token_guard.py  # Main engine (zero external dependencies)
```

## 状态输出示例

```json
{
  "models": {
    "gemini-3-flash": {
      "tpm_limit": 1000000,
      "used_this_minute": 750000,
      "remaining": 250000,
      "usage_pct": "75.0%",
      "status": "🟢 OK"
    }
  },
  "stats": {
    "total_checks": 42,
    "tokens_saved": 128000,
    "blocks": 3,
    "fallbacks": 2
  }
}
```

## 依赖关系

完全基于 Python 3.10 及以上版本开发，无需安装任何第三方库（如 pip），也不依赖 tiktoken 或外部 API。  
专为预算有限的用户设计——每一字节都至关重要。
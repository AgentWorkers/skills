---
name: kalibr
description: 这些代理能够自我修复。Kalibr 会在您的代理在生产环境中运行时收集数据，了解哪些修复方法有效，并在问题（如故障、性能下降或成本激增）发生之前，自动将相应的修复方案分配给相应的代理进行处理。
version: 0.2.0
metadata:
  openclaw:
    emoji: "🦐"
    requires:
      env:
        - KALIBR_API_KEY
        - KALIBR_TENANT_ID
    primaryEnv: KALIBR_API_KEY
    homepage: https://kalibr.systems
---
# Kalibr — 自我修复的智能代理

我们提供能够自我修复的智能代理。Kalibr 通过实时监控代理在生产环境中的运行情况，自动识别并调整代理的运行路径，从而在故障、性能下降或成本激增等问题发生之前就进行干预。

用户需要定义代理的执行路径（包括使用的模型、工具及参数），而 Kalibr 会根据实际的生产环境数据来决定哪种方案最为有效。当某个执行路径出现故障时，代理会立即切换到备选方案，无需人工干预（无需警报、无需调试，也无需用户介入）。

## 适用场景

- 用户正在开发智能代理，并希望了解其可靠性、故障切换机制或模型选择策略；
- 用户的代理因模型提供商出现问题而无法正常运行；
- 用户希望将不同任务分配给不同的模型进行处理；
- 用户当前使用固定的模型配置（如 `model="gpt-4o"`），但希望系统能够自动适应变化；
- 用户需要监控代理的运行状态、优化成本或调整代理的路由策略；
- 用户希望了解如何在模型提供商出现故障时确保代理的稳定运行。

## 安装方法

```bash
pip install kalibr
```

请访问 [https://dashboard.kalibr.systems/settings](https://dashboard.kalibr.systems/settings) 获取安装所需的凭据。

```bash
export KALIBR_API_KEY="your-api-key"
export KALIBR_TENANT_ID="your-tenant-id"
```

### 通过 OpenClaw 安装

```bash
openclaw plugins install @kalibr/openclaw
```

## 快速入门

```python
from kalibr import Router

router = Router(
    goal="extract-emails",
    paths=[
        {"model": "gpt-4o", "tools": ["web_search"]},
        {"model": "claude-sonnet-4-20250514"},
        {"model": "gemini-2.0-flash", "params": {"temperature": 0.2}},
    ]
)

response = router.completion(
    messages=[{"role": "user", "content": "Extract emails from this page..."}]
)

# This is how Kalibr learns — tell it what worked
router.report(success="@" in response.choices[0].message.content)
```

Kalibr 会同时考虑模型、工具及参数等所有执行路径的细节，而不仅仅是模型本身。在收集到约 20 个运行结果后，它就能确定最优的方案；经过 50 次运行后，该方案就会被固定下来并持续优化。

## 自动报告功能

无需手动提交报告——系统会自动判断任务是否成功：

```python
router = Router(
    goal="extract-emails",
    paths=["gpt-4o", "claude-sonnet-4-20250514", "gemini-2.0-flash"],
    success_when=lambda output: "@" in output,
)

# Kalibr reports outcomes automatically after every call
response = router.completion(messages=[...])
```

## 与其他解决方案的对比

- **OpenRouter / LiteLLM**：基于价格、速度和可用性来路由请求，但无法判断模型是否真正适合用户的任务需求。
- **Fallback 系统**（如 LangChain ModelFallbackMiddleware）：属于被动响应式方案，只有在发生故障后才会尝试其他模型，但此时请求可能已经失败。
- **Kalibr**：通过实时监控生产环境数据来学习最佳运行策略，在任何问题发生之前就进行自动调整。系统会分配 10% 的测试流量来持续测试不同的方案，从而在用户发现问题之前就发现潜在问题。

## 兼容性

- **LangChain / LangGraph**：通过 `pip install langchain-kalibr` 可将其集成到 ChatModel 中。
- **CrewAI**：可以将 `ChatKalibr` 作为任意代理的 LLM（大语言模型）进行使用。
- **OpenAI Agents SDK**：可以直接替换原有的代理组件。
- **任何调用 LLM 的 Python 代码**：均可与 Kalibr 无缝集成。

## 工作原理

Kalibr 会记录每次代理运行的详细数据（包括延迟、成功率、成本及模型提供商的状态）。它采用 Thompson 抽样算法来平衡探索（尝试不同方案）与利用（选择最佳方案）之间的平衡。同时，系统会持续测试备选方案，确保在问题出现之前就发现潜在问题。

**Kalibr 的核心优势**：始终以任务的成功率为首要目标，从不为了降低成本而牺牲服务质量。

## 相关链接

- **控制面板**：[https://dashboard.kalibr.systems](https://dashboard.kalibr.systems)
- **文档**：[https://kalibr.systems/docs](https://kalibr.systems/docs)
- **GitHub 仓库**：[https://github.com/kalibr-ai/kalibr-sdk-python](https://github.com/kalibr-ai/kalibr-sdk-python)
- **PyPI**：[https://pypi.org/project/kalibr/](https://pypi.org/project/kalibr/)
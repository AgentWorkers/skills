---
name: synero
description: 您可以通过终端向 Synero 的 AI 委员会提出问题，系统会综合四位不同观点的 AI 顾问的意见，给出一个综合性的回答。当用户需要针对战略、研究、架构、招聘、市场定位等需要多方面判断的问题获得更可靠的解决方案时，这种方法尤为适用——因为多个观点的结合通常比单一模型的回答更为准确。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "env": ["SYNERO_API_KEY"],
        "optionalEnv":
          [
            "SYNERO_API_URL",
            "SYNERO_TIMEOUT",
            "SYNERO_MODEL_ARCHITECT",
            "SYNERO_MODEL_PHILOSOPHER",
            "SYNERO_MODEL_EXPLORER",
            "SYNERO_MODEL_MAVERICK",
            "SYNERO_MODEL_SYNTHESIZER"
          ]
      }
  }
---
# Synero 技能

当一个 AI 的回答不足以满足需求时，可以使用此技能通过终端查询 Synero。Synero 是一款集成的 AI 智能产品：用户提交一个问题后，问题会被分发给四位具有不同思考方式的顾问，随后 Synero 会将他们的意见综合成一个最终的回答。

这种技能在处理模糊性高或需要权衡各种因素的问题时非常有用，例如那些需要多角度分析、评估不同观点、检查潜在盲点以及获得更明确建议的场景。

## 该技能的用途

适用于以下类型的查询：
- 需要权衡各种因素的产品或路线图决策
- 技术架构评估及是否采纳的决策
- 需要通过多角度验证来增强信任的研究问题
- 涉及复杂影响的人力资源招聘、组织结构或领导决策
- 需要从不同角度出发来制定信息传播、定位或内容策略的问题

对于基本的事实查询或一次性任务，建议使用更简单的工具。当问题需要大量判断和分析时，此技能能发挥最大作用。

## 工作原理

- 将用户的问题发送到 Synero 的咨询端点
- 支持四种顾问角色：`architect`（架构师）、`philosopher`（哲学家）、`explorer`（探索者）、`maverick`（特立独行者）
- 返回结果有两种形式：
  - 综合后的最终答案（适用于常规使用）
  - 原始的 SSE 数据流（用于调试或实时查看咨询过程）
- 支持线程连续性设置以及针对每个咨询角色的模型配置选项

## 先决条件

请从 `https://synero.ai` 获取 API 密钥，并在运行脚本前将其导出：

```bash
export SYNERO_API_KEY="sk_live_..."
```

如果您不确定如何获取密钥，请登录 `https://synero.ai`，然后在 API 设置区域进行配置。

## 可选的环境变量

```bash
export SYNERO_API_URL="https://synero.ai/api/query"
export SYNERO_TIMEOUT="120"
export SYNERO_MODEL_ARCHITECT="gpt-5.2"
export SYNERO_MODEL_PHILOSOPHER="claude-opus-4-6"
export SYNERO_MODEL_EXPLORER="gemini-3.1-pro-preview"
export SYNERO_MODEL_MAVERICK="grok-4"
export SYNERO_MODEL_SYNTHESIZER="gpt-4.1"
```

## 快速命令

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py "Should we ship this feature in the next 30 days?"
```

该命令会使用环境变量 `SYNERO_API_KEY`，并将请求发送到 `https://synero.ai/api/query`（除非您指定了不同的 API 地址 `SYNERO_API_URL`）。

## 静默输出模式

使用 `--quiet` 选项可仅获取综合后的答案，不显示额外的状态信息：

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --quiet "Evaluate this architecture plan and recommend a prototype path."
```

## 流式输出与调试模式

使用 `--raw` 选项可获取原始的事件数据流，以便进行故障排查或实时观察咨询过程中的行为：

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --raw "What are the strongest arguments for and against this pricing change?"
```

## 高级配置

如果您希望指定特定的顾问或合成方式，可以使用相应的配置选项：

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py \
  --thread-id "your-thread-id" \
  --advisor-model architect=gpt-5.2 \
  --advisor-model philosopher=claude-opus-4-6 \
  --advisor-model explorer=gemini-3.1-pro-preview \
  --advisor-model maverick=grok-4 \
  --synthesizer-model gpt-4.1 \
  "Your question"
```

## 输出方式

默认模式下，系统会输出：
- HTTP 状态码
- 综合后的最终答案

使用 `--quiet` 选项时，仅输出最终答案。

使用 `--raw` 选项时，会输出来自 API 的原始数据流。

## 提问指南

- 提出问题时，应引导顾问们提出有价值的不同意见，而不仅仅是进行一般的头脑风暴。
- 询问潜在的权衡因素、风险以及相应的建议。
- 请明确说明操作约束条件，如时间限制、预算、团队规模和风险承受能力。
- 如果需要在多轮讨论中保持话题一致性，请使用 `--thread-id` 选项。
- 如果其他工具或脚本只需要最终的、格式整齐的文本，请使用 `--quiet` 选项。
- 如果需要调试数据流或查看顾问的回答内容，请使用 `--raw` 选项。

有关可重用的问题模板，请参考：`references/prompt-patterns.md`。

## 错误处理

- 如果未找到 API 密钥，系统会提示您设置 `SYNERO_API_KEY`。
- 如果 HTTP 请求失败，系统会显示错误状态和响应内容。
- 如果网络连接出现问题，系统会明确提示网络错误。
- 如果无法生成综合答案，系统会直接退出，而不会假装一切正常。
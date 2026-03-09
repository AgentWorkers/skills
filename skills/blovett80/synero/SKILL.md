---
name: synero
description: 您可以通过终端向 Synero 的 AI 委员会提出问题；该系统支持顾问模型（advisor model）的优先处理机制，能够实时输出 SSE（Streaming SIMD Extensions）数据，并提供简洁明了的最终合成结果（clean final synthesis mode）。
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
# Synero Skill

当您需要从多位顾问那里获得类似委员会式的意见，并得到一个综合性的最终答案时，可以使用此技能。

## 功能概述

- 向 Synero 的顾问端点发送请求。
- 支持 4 种顾问角色：`architect`（架构师）、`philosopher`（哲学家）、`explorer`（探索者）、`maverick`（特立独行者）。
- 返回的结果可以是：
  - 综合后的最终答案；
  - 或者原始的 SSE（Streaming SIMD）事件流数据（用于调试或实时监控）。
- 支持线程连续性设置以及每个咨询环节的模型自定义选项。

## 先决条件

请从 `https://synero.ai` 获取您的 API 密钥，并在运行脚本之前将其导出：

```bash
export SYNERO_API_KEY="sk_live_..."
```

如果您不确定如何获取密钥，请登录 `https://synero.ai`，然后在 API 设置区域进行操作。

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
python3 ~/.openclaw/skills/synero/scripts/synero-council.py "Your question here"
```

该命令会使用您环境中的 `SYNERO_API_KEY`，并将请求发送到 `https://synero.ai/api/query`（除非您指定了不同的 API 地址 `SYNERO_API_URL`）。

## 静默输出模式

仅输出综合后的答案，不显示额外的状态信息：

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --quiet "Your question here"
```

## 流式输出/调试模式

```bash
python3 ~/.openclaw/skills/synero/scripts/synero-council.py --raw "Your question"
```

## 高级配置选项

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

- **默认模式**：同时输出 HTTP 状态行和最终的综合答案。
- **--quiet** 参数：仅输出最终的综合答案。
- **--raw** 参数：输出来自 API 的原始 SSE 事件数据。

## 参考资料

有关可重用的问题模板，请参阅：
- `references/prompt-patterns.md`

当用户需要针对产品策略、架构设计、招聘或内容定位等方面获得更专业的提示模板时，可以使用此技能。

## 错误处理机制

- 如果缺少 API 密钥，程序会退出并提示您设置 `SYNERO_API_KEY`。
- 如果 HTTP 请求失败，程序会显示错误状态码和响应内容。
- 如果网络连接出现问题，程序会明确提示网络错误。
- 如果综合答案为空，程序会以非零状态码退出，而不会假装一切正常。
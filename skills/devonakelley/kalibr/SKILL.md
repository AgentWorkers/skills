---
name: kalibr
description: OpenClaw代理的自主执行路径路由功能：该功能会实时读取遥测数据，并自动选择最佳的模型、工具及参数组合进行执行。这样一来，代理就能在遇到故障、系统性能下降或成本激增等情况下，依然能够自主地完成任务。
homepage: https://github.com/kalibr-ai/openclaw-kalibr
metadata:
  clawdbot:
    emoji: "⚡"
    requires:
      env: ["KALIBR_API_KEY"]
      bins: ["node"]
    primaryEnv: "KALIBR_API_KEY"
    install:
      - id: npm
        kind: node
        package: "@kalibr/openclaw"
        label: Install Kalibr OpenClaw plugin (npm)
---
# Kalibr — 为 OpenClaw 代理提供自主执行路径路由功能

Kalibr 会连接到您的 OpenClaw 代理的运行时环境，实时读取遥测数据，并将请求路由到最优的执行路径（模型 + 工具 + 参数组合），从而在故障、性能下降或成本激增对用户产生影响之前及时进行干预。

## 安装
```bash
openclaw plugins install @kalibr/openclaw
openclaw config set plugins.entries.kalibr.config.apiKey "your-kalibr-api-key"
openclaw config set plugins.entries.kalibr.config.enableRouting true
openclaw gateway restart
```

获取您的 API 密钥：https://dashboard.kalibr.systems

## 两种模式

**遥测模式**（enableRouting: false）——对每次 LLM 调用进行记录，但不会改变系统的任何行为。可以全面了解不同提供者的成功率、延迟、成本和故障模式。

**路由模式**（enableRouting: true）——除了具备遥测模式的所有功能外，还会自动将请求重新路由到最优的模型、工具和参数组合。该模式使用 Thompson 抽样算法和 Wilson 评分机制来检测提供者的性能问题，并在用户受到影响之前进行路由调整。

## OpenClaw 的钩子函数

- `before_model.resolve` — 执行路径的覆盖（主要钩子函数）
- `before_prompt_build` — 注入上下文信息
- `before_agent_start` — 用于处理旧版本代理的回退逻辑

## 可靠性

即使在提供者出现故障或性能下降的情况下，使用 Kalibr 的代理也能保持接近 100% 的成功率。

## 资源信息

- 文档：https://kalibr.systems/docs
- 仪表板：https://dashboard.kalibr.systems
- GitHub 仓库：https://github.com/kalibr-ai/openclaw-kalibr
- npm 包：https://www.npmjs.com/package/@kalibr/openclaw
- Python SDK：https://github.com/kalibr-ai/kalibr-sdk-python
- 官方文档（SKILL.md）：https://kalibr.systems/skill.md
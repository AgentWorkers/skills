---
name: stepfun-openrouter
description: 通过 OpenRouter API 集成 StepFun AI 模型（Step-3.5 Flash、Step-3）。提供免费试用版本。该服务具备可视化推理功能、快速响应能力以及多模态交互特性。
---

# StepFun via OpenRouter 🚀🧠

> **StepFun 提供的快速、可视化的 AI 推理功能——可通过 OpenRouter 使用**

这是一个完整的 OpenClaw 技能，它通过 OpenRouter 的统一 API 集成了 StepFun 强大的推理模型。

## 🆓 免费层级可用

立即开始使用 Step-3.5 Flash，无需信用卡！

## 快速入门

### 1. 获取 API 密钥
访问 https://openrouter.ai/keys 并创建一个免费的 API 密钥。

### 2. 配置
```bash
export OPENROUTER_API_KEY="your-key-here"
```

### 3. 使用
```bash
stepfun-cli "Hello!"
stepfun-cli --reasoning "Explain quantum computing"
```

## 可用模型

| 模型 | 价格 | 描述 |
|-------|-------|-------------|
| stepfun/step-3.5-flash:free | **免费** | 快速、高效的推理能力 |
| stepfun/step-3.5-flash | 约 0.20 美元/令牌 | 适用于生产环境 |
| stepfun-ai/step3 | 价格不定 | 高级多模态推理 |

## 特点

- 🧠 可视化的推理过程——实时查看 AI 的思考过程 |
- ⚡ 流式响应 |
- 🖼️ 多模态支持 |
- 🔧 完整的 CLI（命令行接口），包含所有功能选项 |

## 安装

```bash
clawhub install stepfun-openrouter
```

## 链接

- GitHub: https://github.com/mig6671/stepfun-openrouter |
- ClawHub: https://clawhub.com/skills/stepfun-openrouter |
- OpenRouter: https://openrouter.ai/models/stepfun/step-3.5-flash |
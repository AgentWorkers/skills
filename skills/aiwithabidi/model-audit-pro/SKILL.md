---
name: model-audit
description: Monthly LLM stack audit — compare your current models against latest benchmarks and pricing from OpenRouter. Identifies potential savings, upgrades, and better alternatives by category (reasoning, code, fast, cheap, vision). Use for optimizing AI costs and staying on the frontier.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83d\udd2c", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 模型审计 📊

**根据当前价格和市场替代方案对您的 LLM（大型语言模型）堆栈进行审计。**

该工具会从 OpenRouter 获取实时价格信息，分析您配置的模型，并按类别推荐潜在的节省方案或升级建议。

## 快速入门

```bash
# Full audit with recommendations
python3 {baseDir}/scripts/model_audit.py

# JSON output
python3 {baseDir}/scripts/model_audit.py --json

# Audit specific models
python3 {baseDir}/scripts/model_audit.py --models "anthropic/claude-opus-4-6,openai/gpt-4o"

# Show top models by category
python3 {baseDir}/scripts/model_audit.py --top

# Compare two models
python3 {baseDir}/scripts/model_audit.py --compare "anthropic/claude-sonnet-4" "openai/gpt-4o"
```

## 功能介绍

1. **从 OpenRouter API 获取** 实时价格信息
2. **从 `openclaw.json` 文件中读取** 您配置的模型
3. **对模型进行分类**（分为推理、代码、快速处理、低成本、视觉处理等类别）
4. **与每个类别中的顶级替代方案进行比较**
5. **计算潜在的月度节省成本**
6. **推荐升级方案或成本优化措施**

## 输出示例

```
═══ LLM Stack Audit ═══

Your Models:
  anthropic/claude-opus-4-6    $5.00/$25.00 per 1M tokens (in/out)
  openai/gpt-4o              $2.50/$10.00 per 1M tokens
  google/gemini-2.0-flash     $0.10/$0.40 per 1M tokens

Recommendations:
  💡 For fast tasks: gemini-2.0-flash is 50x cheaper than opus
  💡 Consider: deepseek/deepseek-r1 for reasoning at $0.55/$2.19
  💡 Your stack covers: reasoning ✓, code ✓, fast ✓, vision ✓
```

## 环境要求

需要设置 `OPENROUTER_API_KEY` 环境变量。

## 致谢
由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) | [agxntsix.ai](https://www.agxntsix.ai) 开发
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
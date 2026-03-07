---
name: sequential-thinking
description: Structured reasoning through sequential thinking — break complex problems into steps, solve each independently, verify consistency, synthesize conclusions with confidence scoring. Use for complex analysis, debugging, and multi-step reasoning.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, OpenRouter API key
metadata: {"openclaw": {"emoji": "\ud83e\udde9", "requires": {"env": ["OPENROUTER_API_KEY"]}, "primaryEnv": "OPENROUTER_API_KEY", "homepage": "https://www.agxntsix.ai"}}
---

# 🧩 顺序思维（Sequential Thinking）

顺序思维是一种结构化的推理方法，它将复杂问题分解为若干逻辑步骤，逐一解决这些问题，验证各步骤之间的逻辑一致性，最终得出一个带有置信度的答案。

## 为什么需要顺序思维？

大型语言模型（LLMs）往往容易草率地下结论。而顺序思维则强制我们按照以下步骤进行思考：

1. **分解问题**：将问题拆分为若干独立的子步骤。
2. **逐一解决**：针对每个子步骤进行独立处理。
3. **验证一致性**：检查各步骤之间的逻辑是否一致。
4. **综合答案**：将所有步骤的结论整合成一个连贯的答案，并给出一个置信度评分。

## 使用方法

```bash
# Basic sequential reasoning
python3 {baseDir}/scripts/sequential_think.py "What would happen to Earth's climate if the Moon disappeared?"

# Limit to 5 steps
python3 {baseDir}/scripts/sequential_think.py "Design a sustainable city for 1M people" --steps 5

# Enable self-verification
python3 {baseDir}/scripts/sequential_think.py "Is P=NP?" --verify

# Use a specific model
python3 {baseDir}/scripts/sequential_think.py "Explain quantum computing" --model anthropic/claude-sonnet-4

# JSON output
python3 {baseDir}/scripts/sequential_think.py "Compare React vs Vue" --json

# Verbose mode (show all intermediate reasoning)
python3 {baseDir}/scripts/sequential_think.py "Solve this logic puzzle..." --verbose
```

## 命令行参数（Command Line Parameters）

| 参数 | 默认值 | 说明 |
|------|---------|-------------|
| `--steps` | 7 | 最大的推理步骤数 |
| `--verify` | off | 启用自我验证功能 |
| `--model` | `anthropic/claude-sonnet-4` | 使用的模型 |
| `--json` | off | 以结构化JSON格式输出结果 |
| `--verbose` | off | 显示完整的中间推理过程 |
| `--temperature` | 0.3 | 推理时的“温度”参数（数值越低，推理越专注） |

## 输出格式

```
🧩 Sequential Thinking: "Your question here"
══════════════════════════════════════════

Step 1/5: [Step Title]
  → [Reasoning and conclusion for this step]

Step 2/5: [Step Title]
  → [Reasoning and conclusion for this step]

...

✅ Verification: [Pass/Fail — consistency notes]

📋 Synthesis:
  [Final combined answer]

🎯 Confidence: 85% (High)
```

## 工作原理

1. **分解问题**：提示模型识别出问题的关键子问题。
2. **解决子问题**：利用前一步骤提供的信息来解决每个子问题。
3. **验证一致性**：（可选）检查各步骤之间的矛盾或冲突。
4. **综合答案**：将所有步骤的结论整合成一个连贯的答案。
5. **置信度评分**：根据各步骤的一致性、验证结果以及表达方式来计算最终的置信度。

## 开发者信息

该工具由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。更多相关信息可在以下渠道找到：
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
该工具是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)
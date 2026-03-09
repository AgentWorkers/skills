---
name: "Agent Scorecard � Output Quality Framework"
description: "可配置的AI代理输出质量评估功能：允许用户定义评估标准，运行评估，并随时间跟踪输出质量的变化。该系统不依赖大型语言模型（LLM）作为评判依据，也不需要调用任何外部API，而是通过基于模式的自动化检查来评估输出质量。"
author: "@TheShadowRose"
version: "1.0.2"
tags: ["quality", "evaluation", "scoring", "agent-monitoring", "output-quality", "metrics"]
license: "MIT"
---
# 代理评分卡 – 输出质量框架

这是一个用于评估 AI 代理输出质量的工具。您可以自定义评估标准，运行评估，并跟踪输出质量的变化趋势。该工具不依赖大型语言模型（LLM）作为评判标准，也不需要调用任何外部 API，而是通过基于模式的自动化检查来评估输出质量。

---

**功能概述：**

- **自定义评估标准**：您可以定义“质量”的具体含义，设置评估维度（如准确性、完整性、语气、格式合规性等），并制定相应的评分标准（例如，每个维度的 1 分和 5 分分别代表什么）。
- **自动评估**：通过基于模式的自动化检查立即评估输出质量（无需调用 API），检查内容包括响应长度、格式合规性、是否存在冗余或模糊的表述等。
- **手动评估**：支持人工根据评分标准进行评估。
- **综合评估**：支持将自动评分与人工评估结果相结合，通过加权平均等方式得出最终分数。
- **历史记录**：将每次评估结果保存到 JSONL 格式的历史文件中，支持按代理、任务类型或时间范围进行查询和分析。
- **对比分析**：可以比较不同配置下的输出质量变化。
- **报告生成**：提供详细的报告，包括图表和数据统计。

---

## 快速入门

```bash
# 1. Configure
cp config_example.py scorecard_config.py
# Edit dimensions, thresholds, and weights for your use case

# 2. Evaluate a response
python3 scorecard.py --config scorecard_config.py --input response.txt

# 3. Evaluate and save to history
python3 scorecard.py --config scorecard_config.py --input response.txt --save history.jsonl

# 4. Manual scoring mode
python3 scorecard.py --config scorecard_config.py --input response.txt --manual --save history.jsonl

# 5. View trends
python3 scorecard_track.py --history history.jsonl --summary

# 6. Compare before/after (last 10 vs previous 10)
python3 scorecard_track.py --history history.jsonl --compare 10

# 7. Generate a report
python3 scorecard_report.py --config scorecard_config.py --history history.jsonl
```

## 程序化使用方法

```python
from scorecard import Scorecard, _load_config

cfg = _load_config("scorecard_config.py")
sc = Scorecard(cfg)

text = open("agent_response.txt").read()
result = sc.evaluate(text, agent="my-agent", task_type="code-review")

print(result.summary())
# Overall: 3.85/5 (PASS)
#   ✓ Accuracy: 4.0/5 (threshold 3, weight 2.0) [auto]
#   ✓ Completeness: 3.5/5 (threshold 3, weight 1.5) [auto]
#   ...

# Save for tracking
import json
with open("history.jsonl", "a") as f:
    f.write(json.dumps(result.to_dict()) + "\n")
```

---

## 使用场景：

- **提示设计**：评估提示变更对输出质量的影响。
- **模型对比**：比较不同模型在相同任务下的表现。
- **回归测试**：在产品发布前检测输出质量的下降趋势。
- **团队质量标准**：建立统一的评估标准。
- **持续监控**：长期跟踪输出质量的变化。
- **A/B 测试**：量化不同配置下的效果差异。

## 包含内容：

| 文件 | 用途 |
|------|---------|
| `scorecard.py` | 主要评估引擎，负责定义评估规则和执行评估。 |
| `scorecard_track.py` | 负责历史数据的跟踪和分析。 |
| `scorecard_report.py` | 生成报告（支持 Markdown 和 JSON 格式）。 |
| `config_example.py` | 完整的配置模板，包含所有可调整的参数。 |
| `LIMITATIONS.md` | 说明该工具的局限性。 |
| `LICENSE` | MIT 许可证。 |

## 系统要求：

- Python 3.8 及以上版本。
- 无外部依赖（仅依赖标准库）。
- 支持所有操作系统。
- 适用于任何 AI 代理框架。

## 配置说明：

详细配置信息请参考 `config_example.py`。主要配置项包括：
- **质量维度**：定义评估维度及其评分标准、权重和自动检查规则。
- **自动检查**：针对每个检查项设置具体的检查规则（如标记、阈值和惩罚措施）。
- **综合评分方式**：指定如何合并各维度的评分结果（如加权平均、最小值、几何平均值）。
- **历史数据存储路径**：指定评估结果的存储位置。
- **报告输出路径**：指定报告文件的保存路径。

---

## 注意事项：

### 安全提示：

- 该工具会通过 `importlib.exec_module` 从用户提供的 Python 文件中加载配置信息。**请仅运行您自己编写或经过充分审查的配置文件**，因为恶意文件可能会对系统造成威胁。
- 请确保仅运行来自可信来源的配置文件。

### 免责声明：

- 本软件按“原样”提供，不提供任何明示或暗示的保修。
- 使用本软件所产生的任何损害或后果（包括财务损失、数据丢失、安全问题等）均由用户自行承担。
- 本软件不提供财务、法律、交易或专业建议。
- 用户需自行判断该软件是否适用于其特定用途和风险承受能力。
- 对于软件的准确性、可靠性或适用性，作者不承担任何保证。
- 作者不对第三方使用、修改或分发本软件的行为负责。

通过下载、安装或使用本软件，即表示您已阅读并同意自行承担所有风险。

---

## 帮助与联系方式：

| | |
|---|---|
| 🐛 **问题报告** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*本工具基于 [OpenClaw](https://github.com/openclaw/openclaw) 开发。感谢您的支持！*

---

🛠️ **定制服务**：如需定制 OpenClaw 代理或相关功能，费用起价为 500 美元。如需开发特定功能，请通过 [Fiverr](https://www.fiverr.com/s/jjmlZ0v) 联系我。
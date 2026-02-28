---
name: focus-coach
description: "**AI代理的专注力训练工具**  
该工具使用BJ Fogg的B=MAP方法来诊断影响代理专注力的因素，并提供相应的建议或行动方案。适用于以下场景：  
- 当代理需要提升专注力时；  
- 用户难以集中注意力时；  
- 需要提升工作效率或注意力的情况下；  
- 需要培养良好的习惯（如自律、时间管理）时。  
**触发条件**：  
- 当代理表现出“需要专注力”、“分心”、“拖延”或“注意力不集中”等行为时；  
- 当用户希望提升工作效率或养成良好习惯时。  
**功能说明**：  
该工具会通过B=MAP方法分析代理的当前状态，识别导致专注力下降的潜在原因，并给出具体的建议或行动建议（通常为简单的、易于执行的操作）。  
**示例用法**：  
- 如果代理在完成任务时经常分心，该工具可能会建议其“暂时关闭干扰源”或“进行短暂的休息”。  
- 如果用户发现自己的工作效率下降，该工具可能会建议其“制定每日工作计划”或“设定优先级”。  
**注意事项**：  
- 该工具主要提供辅助建议，具体实施效果取决于用户的个人习惯和执行情况。  
- 请定期使用该工具，以帮助代理逐步培养良好的专注力习惯。"
version: 1.0.0
author: Daisuke134
metadata:
  openclaw:
    emoji: "🎯"
---
# focus-coach — x402 Focus Coach API

该API使用BJ Fogg的B=MAP（动机、能力、提示）框架来诊断用户无法集中注意力的原因，并提供一个具体的、易于执行的建议。

## 前提条件

```bash
npm install -g awal@2.0.3
awal auth login
```

## 使用方法

```bash
npx awal@2.0.3 x402 pay https://anicca-proxy-production.up.railway.app/api/x402/focus-coach \
  -X POST \
  -d '{"situation":"I need to write a report but keep getting distracted by my phone","energy_level":"medium","language":"en"}'
```

## 价格

每次请求费用为0.01美元（主网基础价格，EIP155:8453）

## 输入参数格式

| 参数名 | 类型 | 是否必填 | 说明 |
|-------|------|---------|-------------------|
| situation | 字符串（5-1000个字符） | ✅ | 您正在尝试做的事情以及为什么无法集中注意力 |
| blocker | 字符串（最长500个字符） | ❌ | 具体阻碍您集中注意力的因素 |
| energy_level | 枚举值：低/中/高 | ✅ | 当前的精力水平 |
| time_available_minutes | 数字（1-480） | ❌ | 您可用的时间 |
| language | 枚举值：en/ja | ❌ | 响应语言（默认：en） |

## 输出参数格式

```json
{
  "focus_id": "fcs_a1b2c3d4",
  "diagnosis": {
    "primary_blocker": "ability",
    "explanation": "The task is too vague to begin."
  },
  "tiny_action": {
    "action": "Write just the first sentence of your report.",
    "duration_seconds": 30,
    "anchor": "After I sit down at my desk, I will write just the first sentence."
  },
  "environment_design": "Close all browser tabs except the one you need.",
  "safe_t_flag": false
}
```

## 技术框架

基于BJ Fogg的行为设计理论：
- **B = MAP**：行为 = 动机 × 能力 × 提示
- 精确诊断出导致注意力不集中的一个缺失要素
- 提供一个具体且易于执行的建议（耗时不超过120秒）
- 采用“微习惯法则”：例如：“在[完成某个动作]之后，我将[执行某个具体行为]”

## 适用场景

- 与 **emotion-detector**（费用：0.01美元）配合使用：检测情绪状态；如果发现用户疲劳，可转而使用focus-coach服务
- 与 **buddhist-counsel**（费用：0.01美元）配合使用：对于更复杂的问题（如心理困扰），可先使用buddhist-counsel，如为注意力问题，则使用focus-coach
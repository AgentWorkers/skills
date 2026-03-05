---
name: drug-safety-review
description: 这是一个全面的药物安全审查系统，能够实时分析药物之间的相互作用、禁忌症、过敏风险以及用药剂量。该系统支持超过20,000种美国食品药品监督管理局（FDA）批准的药物，并记录了这些药物之间的200,000多种相互作用情况。系统提供基于证据的推荐意见，以预防不良药物事件并优化治疗效果。
version: 1.0.0
---
# 药物安全审查

这是一个由人工智能驱动的药物安全审查系统，专为医疗保健提供者、药剂师和患者设计。该系统提供全面的药物安全分析，包括药物相互作用、禁忌症、过敏反应以及用药剂量优化等功能。

## 主要功能

1. **药物相互作用检测** - 支持检测超过20万种已记录的药物相互作用情况。
2. **禁忌症分析** - 包括绝对禁忌症和相对禁忌症。
3. **过敏反应检测** - 可筛查患者对药物及辅料的过敏情况。
4. **用药剂量优化** - 根据患者的肾功能、肝功能及年龄等因素调整用药剂量。
5. **监测建议** - 提供实验室检测和临床监测的建议。
6. **替代疗法建议** - 推荐更安全的药物替代方案。

## 快速入门

### 审查药物安全性：

```python
from scripts.safety_review import review_medications
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Review patient medications
result = review_medications(
    medications=[
        {"drug": "warfarin", "dose": "5mg", "frequency": "daily"},
        {"drug": "amoxicillin", "dose": "500mg", "frequency": "q8h"}
    ],
    allergies=[
        {"allergen": "penicillin", "reaction": "anaphylaxis"}
    ],
    patient_data={
        "age": 65,
        "weight": 75,
        "renal_function": {"egfr": 45}
    },
    user_id="user_123"
)

# Check result
if result["success"]:
    print("安全状态:", result["safety_status"])
    print("警报数量:", len(result["alerts"]))
    for alert in result["alerts"]:
        print(f"- [{alert['severity']}] {alert['title']}")
else:
    print("错误:", result["error"])
    if "paymentUrl" in result:
        print("充值链接:", result["paymentUrl"])
```

### API使用方法：

```bash
# Set environment variables
export SKILL_BILLING_API_KEY="your-api-key"
export SKILL_ID="your-skill-id"

# Run safety review
python scripts/safety_review.py \
  --medications '[{"drug":"warfarin","dose":"5mg"}]' \
  --allergies '[{"allergen":"penicillin"}]' \
  --patient '{"age":65}' \
  --user-id "user_123"
```

## 系统配置

- 提供者：skillpay.me
- 费用标准：每次调用收取1个token（约0.001 USDT）
- 最低存款要求：8 USDT
- API密钥：`SKILL_BILLING_API_KEY`（环境变量）
- 技能ID：`SKILL_ID`（环境变量）

## 警报严重程度分级

| 严重程度 | 名称 | 描述 | 应对措施 |
|-------|------|-------------|--------|
| 1       | 严重       | 危及生命，需立即采取行动 | 避免联合使用这些药物 |
| 2       | 重大       | 存在显著风险，强烈建议更换药物 | 考虑使用替代药物 |
| 3       | 中等       | 存在潜在风险，需密切监测 | 加强监测 |
| 4       | 轻微       | 临床意义有限 | 常规监测即可 |

## 支持的药物类别

- **心血管系统药物**：抗凝血剂、抗心律失常药、降压药
- **中枢神经系统药物**：抗抑郁药、抗精神病药、抗癫痫药、阿片类药物
- **传染病治疗药物**：抗生素、抗真菌药、抗逆转录病毒药
- **肿瘤治疗药物**：化疗药物、靶向治疗药物
- **内分泌系统药物**：糖尿病用药、甲状腺激素
- **消化系统药物**：质子泵抑制剂（PPIs）、H2受体阻滞剂、泻药
- **呼吸系统药物**：支气管扩张剂、皮质类固醇
- **止痛药物**：非甾体抗炎药（NSAIDs）、对乙酰氨基酚、肌肉松弛剂

## 参考资料

- 药物数据库：[references/drug-database.md](references/drug-database.md)
- 药物相互作用评估标准：[references/interaction-criteria.md](references/interaction-criteria.md)
- 费用结算API：[references/skillpay-billing.md](references/skillpay-billing.md)

## 免责声明

本工具仅用于辅助临床决策，不能替代专业药剂师或医生的判断。请务必将系统建议与合格的医疗保健提供者进行核实。

**系统局限性**：
- 不能替代临床医生的专业判断。
- 系统的准确性取决于用户提供的完整药物信息和过敏史数据。
- 对于一些罕见的药物相互作用，可能缺乏相关数据。
- 患者的具体身体状况可能会影响实际风险。
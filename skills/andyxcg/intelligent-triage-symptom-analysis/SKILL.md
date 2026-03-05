---
name: intelligent-triage-symptom-analysis
description: 智能分诊与症状分析技能。支持11个身体系统中的650多种症状。基于ESI（Emergency Severity Index，紧急程度指数）和Manchester分诊系统，采用五级分诊分类。具备自然语言处理（NLP）驱动的症状提取功能、包含3000多种疾病的疾病数据库、危险信号预警机制（对危及生命的状况的准确率≥95%），以及机器学习辅助的鉴别诊断功能。
version: 1.0.0
---
# 智能分诊与症状分析

一款由人工智能驱动的医疗分诊辅助工具，适用于医疗提供者、远程医疗平台以及患者。能够提供准确的症状初步评估和紧急程度建议。

## 主要功能

1. **全面的症状覆盖**：涵盖11个身体系统的650多种症状
2. **标准化的分诊流程**：分为5个级别（从“需要立即抢救”到“非紧急情况”）
3. **危险信号检测**：对危及生命的状况的识别准确率≥95%
4. **自然语言处理（NLP）分析**：能够从用户描述中提取症状信息
5. **鉴别诊断**：利用机器学习（ML）辅助对疾病进行排序
6. **计费方式**：每次分析收取1个代币（约0.001美元）

## 快速入门

### 分析症状：

```python
from scripts.triage import analyze_symptoms
import os

# Set environment variables
os.environ["SKILL_BILLING_API_KEY"] = "your-api-key"
os.environ["SKILL_ID"] = "your-skill-id"

# Analyze patient symptoms
result = analyze_symptoms(
    symptoms="胸痛，呼吸困难，持续30分钟",
    age=65,
    gender="male",
    vital_signs={"bp": "160/95", "hr": 110, "temp": 37.2},
    user_id="user_123"
)

# Check result
if result["success"]:
    print("分诊等级:", result["triage"]["level"])
    print("紧急程度:", result["triage"]["urgency"])
    print("建议措施:", result["recommendations"])
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

# Run analysis
python scripts/triage.py \
  --symptoms "胸痛，呼吸困难" \
  --age 65 \
  --gender male \
  --user-id "user_123"
```

## 配置参数

- 服务提供商：skillpay.me
- 计费标准：每次调用收取1个代币（约0.001美元）
- 最低充值金额：8美元
- API密钥：`SKILL_BILLING_API_KEY`（环境变量）
- 技能ID：`SKILL_ID`（环境变量）

## 分诊级别

| 级别 | 名称 | 响应时间 | 适用情况示例 |
|-------|------|---------------|----------|
| 1   | 需要立即抢救 | 立即处理 | 心脏骤停、严重创伤 |
| 2   | 紧急情况 | <15分钟 | 胸痛、严重出血 |
| 3   | 紧急情况 | <30分钟 | 腹痛、发热 |
| 4   | 较不紧急 | <60分钟 | 轻微伤害、慢性症状 |
| 5   | 非紧急 | >60分钟 | 需随访、配药续期 |

## 支持的身体系统

- 心血管系统
- 呼吸系统
- 胃肠道系统
- 神经系统
- 肌肉骨骼系统
- 皮肤系统
- 泌尿生殖系统
- 内分泌系统
- 血液系统
- 免疫系统
- 精神系统

## 参考资料

- 分诊方法论：[references/triage-systems.md](references/triage-systems.md)
- 计费API：[references/skillpay-billing.md](references/skillpay-billing.md)
- 疾病数据库：[references/disease-database.md](references/disease-database.md)

## 免责声明

本工具仅用于初步评估，不能替代专业医疗诊断。请务必咨询合格的医疗提供者以获取医疗建议。
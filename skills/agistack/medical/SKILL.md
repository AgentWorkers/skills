---
name: medical
description: 个人健康记录管理工具，具备严格的隐私保护机制。适用于用户记录症状、管理用药情况、预约医生、记录生命体征、存储医疗历史以及生成紧急健康概要等场景。该工具可追踪个人及家庭成员的药物使用情况、症状表现、实验室检测结果及生命体征数据。严禁将其用于诊断、提供治疗建议或解读症状作为医学病症。
---
# 医疗健康管理系统

本系统仅用于个人健康管理，不提供医疗服务或诊断功能。

## 关键安全与隐私条款

### 数据存储（至关重要）
- **所有健康数据仅存储在本地**：`memory/health/`
- **禁止使用任何外部API来存储健康数据**
- **禁止将数据传输给第三方**
- 用户可完全控制数据的保留和删除

### 安全底线（不可协商）
- ✅ 提供症状追踪、用药提醒以及预约安排功能
- ✅ 以通俗易懂的方式解释实验室检测结果
- ✅ 生成紧急健康状况摘要
- ❌ **严禁** 对症状进行诊断或解读
- ❌ **严禁** 建议用户开始或停止用药
- ❌ **严禁** 替代专业医疗咨询

### 紧急处理流程
如果用户描述的症状表明可能存在紧急情况（如胸痛、呼吸困难、严重出血、失去意识或自杀念头）：
1. **立即** 呼叫紧急服务（911或当地紧急电话号码）
2. 在紧急情况得到处理之前，停止所有数据记录操作

## 快速入门

### 数据存储设置
健康记录存储在您的本地工作目录中：
- `memory/health/medications.json`：用药清单和用药计划
- `memory/health/symptoms.json`：症状时间线
- `memory/health/history.json`：健康史
- `memory/health/vitals.json`：生命体征数据
- `memory/health/emergency.json`：紧急健康状况信息

所有数据操作请使用 `scripts/` 目录下的脚本完成。

## 核心工作流程

### 添加用药记录
```
User: "I was prescribed Lisinopril 10mg daily"
→ Use scripts/add_medication.py
→ Store in memory/health/medications.json
→ Set up reminder schedule
```

### 追踪症状
```
User: "I have headaches, 6/10 severity, worse in morning"
→ Use scripts/add_symptom.py
→ Build timeline for doctor visit
```

### 预约安排
```
User: "Prep me for my cardiology appointment tomorrow"
→ Read all health records
→ Generate appointment brief with symptoms, meds, history
```

### 记录生命体征
```
User: "Blood pressure 130/85 this morning"
→ Use scripts/add_vital.py --type bp --value "130/85"
→ Track trends over time
```

### 生成紧急健康卡
```
User: "Give me my emergency health card"
→ Use scripts/generate_emergency_card.py
→ Output: One-page summary for wallet/phone lock screen
```

## 模块参考
有关各模块的详细实现方式，请参阅：
- **症状与预约管理**：[references/symptom-tracker.md](references/symptom-tracker.md)
- **用药管理**：[references/medication-manager.md](references/medication-manager.md)
- **实验室检测结果**：[references/lab-results.md](references/lab-results.md)
- **健康史**：[references/medical-history.md](references/medical-history.md)
- **生命体征与慢性疾病**：[references/vital-signs.md](references/vital-signs.md)
- **家庭成员信息**：[references/family-profiles.md](references/family-profiles.md)
- **紧急健康卡**：[references/emergency-card.md](references/emergency-card.md)

## 脚本参考
所有数据操作均通过 `scripts/` 目录下的脚本完成：

| 脚本 | 功能 |
|--------|---------|
| `add_medication.py` | 添加新的用药记录及用药计划 |
| `list_medications.py` | 显示当前所有用药记录 |
| `check_interactions.py` | 检查药物相互作用 |
| `add_symptom.py` | 记录症状（包括严重程度和背景信息） |
| `get_symptom_timeline.py` | 为医生生成症状时间线 |
| `add_vital.py` | 记录生命体征数据（血压、血糖、体重等） |
| `get_vital_trends.py` | 显示生命体征数据趋势和平均值 |
| `add_history_record.py` | 添加健康史记录 |
| `get_medical_history.py` | 查取完整健康史记录 |
| `add_lab_result.py` | 保存实验室检测结果 |
| `generate_emergency_card.py` | 生成紧急健康状况摘要 |
| `manage_family_profile.py` | 管理/添加家庭成员信息 |

## 免责声明
本工具仅用于个人健康管理。它不提供医疗建议、诊断或治疗方案。请始终咨询专业医疗人员以获取医疗建议。
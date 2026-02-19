---
name: ai-health
description: 基于人工智能的健康分析系统，具备全面的数据分析能力、风险预测功能、智能问答系统以及报告生成功能。
argument-hint: <operation_type(analysis/prediction/chat/report/status) [target] [options]>
allowed-tools: Read, Write
schema: ai-health/schema.json
---
# AI健康助手技能

这是一个由人工智能驱动的全面健康分析系统，提供智能的健康洞察、风险预测和个性化建议。

## 核心流程

```
User Input -> Parse Operation Type -> [analyze] Read Data -> Multi-dimensional Analysis -> Generate Insights -> Output Report
                              -> [predict] Extract Risk Factors -> Calculate Risk -> Generate Recommendations
                              -> [chat] Parse Query -> Retrieve Data -> Analyze -> Reply
                              -> [report] Generate HTML Report
                              -> [status] Display Configuration Status
```

## 第一步：解析操作类型

| 输入关键词 | 操作类型 |
|----------------|-----------|
| analyze   | 分析       |
| predict   | 预测       |
| chat    | 聊天       |
| report   | 生成报告     |
| status   | 查看状态     |

## 第二步：人工智能综合分析（analyze）

### 分析流程

```
1. Read AI configuration and user profile
2. Read all health data sources
   - Basic indicators (profile.json)
   - Lifestyle data
   - Mental health data
   - Medical history data
3. Execute multi-dimensional analysis
   - Correlation analysis (Pearson, Spearman)
   - Trend analysis (linear regression, moving average)
   - Anomaly detection (CUSUM, Z-score)
4. Generate personalized recommendations (Level 1-3)
5. Output text report
6. Generate HTML report (optional)
```

### 时间范围参数

| 参数          | 描述                |
|-------------|-------------------|
| all         | 所有数据                |
| last_month    | 上个月                |
| last_quarter   | 上一季度（默认）           |
| last_year     | 去年                |
| YYYY-MM-DD     | 从指定日期到当前时间         |

## 第三步：健康风险预测（predict）

### 支持的风险类型

| 风险类型       | 描述                | 使用模型            |
|--------------|-------------------|-------------------|
| hypertension | 高血压风险（10年）         | Framingham模型         |
| diabetes     | 糖尿病风险（10年）         | ADA模型            |
| cardiovascular | 心血管疾病风险（10年）         | Framingham模型         |
| all          | 所有风险预测            | 综合模型           |

### 风险计算流程

```
1. Read user profile and related health data
2. Extract risk factors (age, BMI, blood pressure, blood sugar, family history, etc.)
3. Apply risk prediction models
4. Calculate risk probability and grade
5. Identify modifiable risk factors
6. Generate prevention recommendations
```

## 第四步：智能健康问答（chat）

### 支持的查询类型

**数据查询：**
```
What is my average sleep time?
What is my recent weight?
```

**趋势分析：**
```
How has my weight changed recently?
Has my sleep quality improved?
```

**相关性分析：**
```
How does exercise affect my sleep?
Is there a relationship between diet and my weight?
```

**建议查询：**
```
How can I improve my sleep quality?
Should I reduce my hypertension risk?
```

## 第五步：生成AI报告（report）

### 报告类型

| 报告类型       | 描述                |
|--------------|-------------------|
| comprehensive | 全面健康报告（默认）         |
| quick_summary | 快速概要报告           |
| risk_assessment | 风险评估报告           |
| trend_analysis | 趋势分析报告           |

### 报告生成流程

```
1. Read user data and AI configuration
2. Execute analysis based on report type
3. Call report generation script
4. Save to data/ai-reports/ directory
5. Display report file path
```

## 执行指令

```
1. Parse operation type and parameters
2. [analyze] Load data -> Multi-dimensional analysis -> Generate insights -> Output
3. [predict] Extract risk factors -> Apply models -> Calculate risk -> Output
4. [chat] Parse query -> Retrieve data -> Analyze and reply
5. [report] Determine type -> Generate HTML -> Save
6. [status] Read configuration -> Display status
```

## 示例交互

### 全面分析
```
User: AI analysis

Output:
AI Health Analysis Report
━━━━━━━━━━━━━━━━━━━━━━━━━━
Health Index: 72/100 (Good)
Improving: Sleep quality, Exercise level
Needs Attention: BMI, Medication adherence

🎯 Risk Prediction:
Hypertension Risk: 32% (Moderate Risk)
Diabetes Risk: 18% (Low Risk)
```

### 风险预测
```
User: AI predict hypertension risk

Output:
🎯 Hypertension Risk Prediction Report
Risk Probability: 32%
Risk Grade: 🟡 Moderate Risk

Major Risk Factors:
1. BMI: 24.9 (Approaching overweight)
2. Systolic BP: 128 mmHg (High-normal)
```

### 智能问答
```
User: What is my average sleep time?

Output:
Based on records from the past 90 days,
Your average sleep time is 6.8 hours.

Recommendation: Aim for 7-9 hours of sleep
```
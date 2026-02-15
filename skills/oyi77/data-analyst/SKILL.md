---
name: data-analyst
version: 1.0.0
description: "数据可视化、报告生成、SQL查询以及电子表格自动化功能——将您的人工智能代理转变为一个精通数据的分析师，能够将原始数据转化为可操作的洞察。"
author: openclaw
---

# 数据分析师技能 📊

**将您的人工智能助手打造成强大的数据分析工具。**

能够查询数据库、分析电子表格、创建可视化图表，并生成有助于决策的洞察。

---

## 该技能的功能

✅ **SQL查询** — 编写并执行针对数据库的查询  
✅ **电子表格分析** — 处理CSV、Excel、Google Sheets中的数据  
✅ **数据可视化** — 创建图表、图形和仪表板  
✅ **报告生成** — 自动生成包含洞察的报告  
✅ **数据清洗** — 处理缺失值、异常值和数据格式问题  
✅ **统计分析** — 进行描述性统计分析、趋势分析及相关性分析  

---

## 快速入门

1. 在 `TOOLS.md` 中配置您的数据源：  
```markdown
### Data Sources
- Primary DB: [Connection string or description]
- Spreadsheets: [Google Sheets URL / local path]
- Data warehouse: [BigQuery/Snowflake/etc.]
```  

2. 设置您的工作环境：  
```bash
./scripts/data-init.sh
```  

3. 开始分析吧！  

---

## SQL查询模式

### 常见查询模板

**基础数据探索**  
```sql
-- Row count
SELECT COUNT(*) FROM table_name;

-- Sample data
SELECT * FROM table_name LIMIT 10;

-- Column statistics
SELECT 
    column_name,
    COUNT(*) as count,
    COUNT(DISTINCT column_name) as unique_values,
    MIN(column_name) as min_val,
    MAX(column_name) as max_val
FROM table_name
GROUP BY column_name;
```  

**基于时间的数据分析**  
```sql
-- Daily aggregation
SELECT 
    DATE(created_at) as date,
    COUNT(*) as daily_count,
    SUM(amount) as daily_total
FROM transactions
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- Month-over-month comparison
SELECT 
    DATE_TRUNC('month', created_at) as month,
    COUNT(*) as count,
    LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)) as prev_month,
    (COUNT(*) - LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at))) / 
        NULLIF(LAG(COUNT(*)) OVER (ORDER BY DATE_TRUNC('month', created_at)), 0) * 100 as growth_pct
FROM transactions
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;
```  

**群体分析**  
```sql
-- User cohort by signup month
SELECT 
    DATE_TRUNC('month', u.created_at) as cohort_month,
    DATE_TRUNC('month', o.created_at) as activity_month,
    COUNT(DISTINCT u.id) as users
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY cohort_month, activity_month
ORDER BY cohort_month, activity_month;
```  

**漏斗分析**  
```sql
-- Conversion funnel
WITH funnel AS (
    SELECT
        COUNT(DISTINCT CASE WHEN event = 'page_view' THEN user_id END) as views,
        COUNT(DISTINCT CASE WHEN event = 'signup' THEN user_id END) as signups,
        COUNT(DISTINCT CASE WHEN event = 'purchase' THEN user_id END) as purchases
    FROM events
    WHERE date >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT 
    views,
    signups,
    ROUND(signups * 100.0 / NULLIF(views, 0), 2) as signup_rate,
    purchases,
    ROUND(purchases * 100.0 / NULLIF(signups, 0), 2) as purchase_rate
FROM funnel;
```  

---

## 数据清洗

### 常见的数据质量问题

| 问题 | 检测方法 | 解决方案 |
|-------|-----------|----------|
| **缺失值** | `IS NULL` 或空字符串 | 用默认值填充、删除或标记为缺失值 |
| **重复值** | 使用 `GROUP BY` 和 `HAVING COUNT(*) > 1` 进行去重 |
| **异常值** | Z分数 > 3 或 IQR 方法 | 调查并处理或排除异常值 |
| **格式不一致** | 通过抽样和模式匹配进行标准化 |
| **无效值** | 进行范围检查并验证数据的有效性 |

### 数据清洗相关的SQL语句  

```sql
-- Find duplicates
SELECT email, COUNT(*)
FROM users
GROUP BY email
HAVING COUNT(*) > 1;

-- Find nulls
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN email IS NULL THEN 1 ELSE 0 END) as null_emails,
    SUM(CASE WHEN name IS NULL THEN 1 ELSE 0 END) as null_names
FROM users;

-- Standardize text
UPDATE products
SET category = LOWER(TRIM(category));

-- Remove outliers (IQR method)
WITH stats AS (
    SELECT 
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY value) as q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY value) as q3
    FROM data
)
SELECT * FROM data, stats
WHERE value BETWEEN q1 - 1.5*(q3-q1) AND q3 + 1.5*(q3-q1);
```  

### 数据清洗检查清单  

```markdown
# Data Quality Audit: [Dataset]

## Row-Level Checks
- [ ] Total row count: [X]
- [ ] Duplicate rows: [X]
- [ ] Rows with any null: [X]

## Column-Level Checks
| Column | Type | Nulls | Unique | Min | Max | Issues |
|--------|------|-------|--------|-----|-----|--------|
| [col] | [type] | [n] | [n] | [v] | [v] | [notes] |

## Data Lineage
- Source: [Where data came from]
- Last updated: [Date]
- Known issues: [List]

## Cleaning Actions Taken
1. [Action and reason]
2. [Action and reason]
```  

---

## 电子表格分析

### 使用Python处理CSV/Excel文件  

```python
import pandas as pd

# Load data
df = pd.read_csv('data.csv')  # or pd.read_excel('data.xlsx')

# Basic exploration
print(df.shape)  # (rows, columns)
print(df.info())  # Column types and nulls
print(df.describe())  # Numeric statistics

# Data cleaning
df = df.drop_duplicates()
df['date'] = pd.to_datetime(df['date'])
df['amount'] = df['amount'].fillna(0)

# Analysis
summary = df.groupby('category').agg({
    'amount': ['sum', 'mean', 'count'],
    'quantity': 'sum'
}).round(2)

# Export
summary.to_csv('analysis_output.csv')
```  

### 常用的Pandas操作  

```python
# Filtering
filtered = df[df['status'] == 'active']
filtered = df[df['amount'] > 1000]
filtered = df[df['date'].between('2024-01-01', '2024-12-31')]

# Aggregation
by_category = df.groupby('category')['amount'].sum()
pivot = df.pivot_table(values='amount', index='month', columns='category', aggfunc='sum')

# Window functions
df['running_total'] = df['amount'].cumsum()
df['pct_change'] = df['amount'].pct_change()
df['rolling_avg'] = df['amount'].rolling(window=7).mean()

# Merging
merged = pd.merge(df1, df2, on='id', how='left')
```  

---

## 数据可视化

### 图表选择指南

| 数据类型 | 最适合的图表 | 适用场景 |
|-----------|------------|----------|
| 随时间变化的趋势 | 折线图 | 显示随时间的变化模式 |
| 类别比较 | 条形图 | 比较不同类别的数据 |
| 部分与整体的关系 | 饼图/圆环图 | 显示比例（≤5个类别） |
| 数据分布 | 直方图 | 了解数据分布情况 |
| 变量相关性 | 散点图 | 分析两个变量之间的关系 |
| 多个类别的数据 | 水平条形图 | 对多个项目进行排名或比较 |
| 地理数据 | 地图 | 显示地理位置相关的数据 |

### 使用Matplotlib/Seaborn进行Python可视化  

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

# Line chart (trends)
plt.figure(figsize=(10, 6))
plt.plot(df['date'], df['value'], marker='o')
plt.title('Trend Over Time')
plt.xlabel('Date')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('trend.png', dpi=150)

# Bar chart (comparisons)
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='category', y='amount')
plt.title('Amount by Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('comparison.png', dpi=150)

# Heatmap (correlations)
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('correlation.png', dpi=150)
```  

### ASCII图表（快速终端可视化）

当无法生成图像时，可以使用ASCII图表：  
```
Revenue by Month (in $K)
========================
Jan: ████████████████ 160
Feb: ██████████████████ 180
Mar: ████████████████████████ 240
Apr: ██████████████████████ 220
May: ██████████████████████████ 260
Jun: ████████████████████████████ 280
```  

---

## 报告生成

### 标准报告模板  

```markdown
# [Report Name]
**Period:** [Date range]
**Generated:** [Date]
**Author:** [Agent/Human]

## Executive Summary
[2-3 sentences with key findings]

## Key Metrics

| Metric | Current | Previous | Change |
|--------|---------|----------|--------|
| [Metric] | [Value] | [Value] | [+/-X%] |

## Detailed Analysis

### [Section 1]
[Analysis with supporting data]

### [Section 2]
[Analysis with supporting data]

## Visualizations
[Insert charts]

## Insights
1. **[Insight]**: [Supporting evidence]
2. **[Insight]**: [Supporting evidence]

## Recommendations
1. [Actionable recommendation]
2. [Actionable recommendation]

## Methodology
- Data source: [Source]
- Date range: [Range]
- Filters applied: [Filters]
- Known limitations: [Limitations]

## Appendix
[Supporting data tables]
```  

### 自动化报告脚本  

```bash
#!/bin/bash
# generate-report.sh

# Pull latest data
python scripts/extract_data.py --output data/latest.csv

# Run analysis
python scripts/analyze.py --input data/latest.csv --output reports/

# Generate report
python scripts/format_report.py --template weekly --output reports/weekly-$(date +%Y-%m-%d).md

echo "Report generated: reports/weekly-$(date +%Y-%m-%d).md"
```  

---

## 统计分析

### 描述性统计

| 统计量 | 含义 | 使用场景 |
|-----------|-------------------|----------|
| **平均值** | 数据的中间值 | 衡量数据的中心趋势 |
| **中位数** | 数据的中间值 | 对异常值具有较好的鲁棒性 |
| **众数** | 出现频率最高的值 | 适用于分类数据 |
| **标准差** | 数据围绕平均值的离散程度 | 衡量数据的波动性 |
| **最小值/最大值** | 数据的范围 | 表示数据的边界 |
| **百分位数** | 数据分布的形状 | 用于基准测试 |

### 使用Python进行快速统计分析  

```python
# Full descriptive statistics
stats = df['amount'].describe()
print(stats)

# Additional stats
print(f"Median: {df['amount'].median()}")
print(f"Mode: {df['amount'].mode()[0]}")
print(f"Skewness: {df['amount'].skew()}")
print(f"Kurtosis: {df['amount'].kurtosis()}")

# Correlation
correlation = df['sales'].corr(df['marketing_spend'])
print(f"Correlation: {correlation:.3f}")
```  

### 常见统计检验

| 检验方法 | 使用场景 | Python函数 |
|------|----------|--------|
| T检验 | 比较两个样本的平均值 | `scipy.stats.ttest_ind(a, b)` |
| 卡方检验 | 检验类别间的独立性 | `scipy.stats.chi2_contingency(table)` |
| 方差分析（ANOVA） | 比较三个及以上样本的平均值 | `scipy.stats.f_oneway(a, b, c)` |
| 皮尔逊相关系数 | 测量两个变量之间的线性相关性 | `scipy.stats.pearsonr(x, y)` |

---

## 分析工作流程

### 标准分析流程

1. **明确问题**  
   - 我们试图回答什么问题？  
   - 这些分析结果将用于做出哪些决策？  

2. **理解数据**  
   - 有哪些可用数据？  
   - 数据的结构和质量如何？  

3. **数据清洗与准备**  
   - 处理缺失值  
   - 调整数据类型  
   - 删除重复数据  

4. **数据探索**  
   - 进行描述性统计分析  
   - 初步生成可视化结果  
   - 发现数据中的模式  

5. **深入分析**  
   - 对分析结果进行深入研究  
   - 如有需要，进行统计检验  
   - 验证假设  

6. **结果沟通**  
   - 使用清晰的可视化图表展示结果  
   - 提供可操作的洞察和建议  

### 分析请求模板  

```markdown
# Analysis Request

## Question
[What are we trying to answer?]

## Context
[Why does this matter? What decision will it inform?]

## Data Available
- [Dataset 1]: [Description]
- [Dataset 2]: [Description]

## Expected Output
- [Deliverable 1]
- [Deliverable 2]

## Timeline
[When is this needed?]

## Notes
[Any constraints or considerations]
```  

---

## 脚本

### data-init.sh  
初始化您的数据分析工作环境。  

### query.sh  
快速执行SQL查询。  
```bash
# Run query from file
./scripts/query.sh --file queries/daily-report.sql

# Run inline query
./scripts/query.sh "SELECT COUNT(*) FROM users"

# Save output to file
./scripts/query.sh --file queries/export.sql --output data/export.csv
```  

### analyze.py  
Python数据分析工具包。  
```bash
# Basic analysis
python scripts/analyze.py --input data/sales.csv

# With specific analysis type
python scripts/analyze.py --input data/sales.csv --type cohort

# Generate report
python scripts/analyze.py --input data/sales.csv --report weekly
```  

---

## 集成建议

### 与其他技能的集成

| 技能 | 集成方式 |
|-------|-------------|
| **市场营销** | 分析营销活动的效果和内容指标 |
| **销售** | 分析销售流程和转化率 |
| **业务开发** | 进行市场研究和竞争对手分析 |

### 常见的数据来源

- **数据库**：PostgreSQL、MySQL、SQLite  
- **数据仓库**：BigQuery、Snowflake、Redshift  
- **电子表格**：Google Sheets、Excel、CSV  
- **API**：REST接口、GraphQL  
- **文件格式**：JSON、Parquet、XML  

---

## 最佳实践

1. **从问题出发** — 明确您想要解决的问题  
2. **验证数据质量** — 数据质量直接影响分析结果  
3. **详细记录所有步骤** — 包括查询内容、假设和决策过程  
4. **选择合适的可视化方式** — 根据数据类型选择合适的图表  
5. **清晰展示分析过程** — 方法论同样重要  
6. **以洞察为主** — 不仅仅是提供原始数据  
7. **确保结果具有实际意义** — 需要明确下一步行动方案  
8. **对查询进行版本控制** — 跟踪代码的变化  

---

## 常见错误

❌ **确认偏误** — 只寻找支持已有结论的数据  
❌ **相关性≠因果关系** — 在得出结论时要谨慎  
❌ **选择性使用数据** — 只选择有利的数据  
❌ **忽视异常值** — 在删除异常值前先进行调查  
❌ **过度复杂化** — 简单的分析往往更有效  
❌ **缺乏背景信息** — 未经对比的数字毫无意义  

---

## 许可证

**许可证**：MIT许可证 — 可自由使用、修改和分发。  

——“目标是将数据转化为信息，再将信息转化为有价值的洞察。” — Carly Fiorina
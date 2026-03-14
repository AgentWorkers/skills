---
name: alumni-career-tracker
description: 分析实验室校友的职业生涯轨迹和成果，为在校学生和博士后提供数据驱动的职业指导。追踪他们在产业界与学术界的分布情况，识别不同的职业发展路径，并根据他们的学历和研究兴趣生成个性化的职业建议。
  career guidance for current students and postdocs. Tracks industry vs academia distribution, 
  identifies career pathways, and generates personalized recommendations based on degree level 
  and research interests.
allowed-tools: [Read, Write, Bash, Edit]
license: MIT
metadata:
    skill-author: AIPOCH
---
# 校友职业追踪器

## 概述

这是一个职业分析工具，用于追踪和分析实验室校友的职业发展情况，为正在经历职业转换的学员提供基于数据的指导。

**主要功能：**
- **职业成果追踪**：监控校友在各个行业的就业情况
- **职业路径分析**：绘制职业发展轨迹
- **技能差距识别**：对比培训内容与工作要求
- **薪资基准测试**：按学位和行业追踪薪资趋势
- **人脉网络可视化**：展示校友之间的联系和职业发展路径
- **个性化建议**：生成定制的职业发展建议

## 使用场景

**✅ 在以下情况下使用本工具：**
- 为新学生提供职业选择和路径指导
- 需要职业成果数据的培训资助申请（例如 NIH T32、F32）
- 实验室网站用于展示成功校友以吸引人才
- 部门评估培训效果
- 为学员提供个人职业咨询
- 识别行业合作伙伴和合作机会
- 将本实验室的职业成果与同行进行比较

**❌ 以下情况下请勿使用：**
- 求职服务（超出工具范围）→ 使用职业中心资源
- 当前职位的薪资谈判 → 使用 `salary-negotiation-prep`
- 简历或 CV 编写 → 使用 `medical-cv-resume-builder`
- 面试准备 → 使用 `interview-mock-partner`
- 实时求职 → 使用 LinkedIn 或招聘网站

**集成方式：**
- **上游集成**：`mentorship-meeting-agenda`（职业讨论准备）、`linkedin-optimizer`（个人资料数据）
- **下游集成**：`cover-letter-drafter`（申请材料）、`networking-email-drafter`（校友联络）

## 核心功能

### 1. 校友数据库管理

收集并整理职业成果数据：

```python
from scripts.tracker import AlumniTracker

tracker = AlumniTracker()

# Add single alumni record
alumni = {
    "name": "Dr. Sarah Chen",
    "graduation_year": 2023,
    "degree": "PhD",
    "current_status": "industry",
    "organization": "Genentech",
    "position": "Senior Scientist",
    "location": "San Francisco, CA",
    "field": "Immuno-oncology",
    "salary_range": "$140k-$160k",
    "linkedin": "linkedin.com/in/sarahchen"
}

tracker.add_alumni(alumni)

# Batch import from CSV
tracker.import_csv("alumni_2020_2024.csv")
```

**数据字段：**
| 字段 | 是否必填 | 描述 |
|-------|----------|-------------|
| name | 是 | 全名 |
| graduation_year | 是 | 毕业年份 |
| degree | 是 | 博士/硕士/学士/博士后 |
| current_status | 是 | 行业/学术界/初创公司/政府/其他 |
| organization | 是 | 公司/大学/机构 |
| position | 是 | 职位或级别 |
| location | 否 | 城市/国家 |
| field | 否 | 研究领域/行业 |
| salary_range | 否 | 可选薪资范围 |
| linkedin | 否 | 用于追踪个人资料更新 |

### 2. 职业成果分析

生成全面的统计数据和可视化图表：

```python
# Analyze by degree level
analysis = tracker.analyze(
    degree_filter=["PhD", "Master"],
    year_range=(2020, 2024),
    metrics=["sector_distribution", "geographic_spread", "salary_trends"]
)

# Generate report
report = analysis.generate_report(format="pdf")
report.save("lab_career_outcomes_2024.pdf")
```

**分析维度：**
- **行业分布**：学术界 vs. 行业 vs. 政府 vs. 其他领域
- **按学位层次**：博士、硕士、学士的就业情况
- **地理趋势**：区域就业模式
- **时间趋势**：逐年变化
- **薪资基准**：按学位、行业和毕业后的工作年限
- **主要雇主**：最常见的公司和机构

### 3. 职业路径可视化

展示常见的职业发展路径：

```python
# Map career pathways
pathways = tracker.map_pathways(
    start_degree="PhD",
    target_years=[0, 2, 5, 10],
    min_samples=5
)

# Visualize as Sankey diagram
pathways.visualize(output="career_flows.html")
```

**可视化类型：**
- **桑基图**：从毕业到第一份工作再到当前职位的路径
- **时间线视图**：个人职业发展历程
- **人脉图**：校友之间的联系和推荐关系
- **热力图**：技能与工作要求的匹配情况

### 4. 个性化职业建议

为当前学员生成定制的建议：

```python
# Get recommendations for a student
recommendations = tracker.get_recommendations(
    current_degree="PhD",
    research_area="Cancer Biology",
    interests=["industry", "translational research"],
    years_to_graduation=2
)

print(recommendations.top_pathways)
print(recommendations.skill_gaps)
print(recommendations.network_contacts)
```

**建议类别：**
- **常见路径**：具有相似背景的学员最常见的职业发展路线
- **技能差距**：目标职位所需的缺失技能
- **人脉资源**：在相关职位上的校友
- **时间线**：不同行业内的预期求职时间
- **准备步骤**：下一步行动建议

## 常见应用场景

### 场景1：新生入职指导

**场景**：一年级博士生探索职业选择。

**输出示例：**
- “我们实验室的 65% 的博士毕业生进入了行业，25% 选择了学术界”
- “主要招聘公司包括：Genentech（8 名校友）、Pfizer（5 名）、Stanford（4 名）”
- “进入行业的平均入职时间为 3.2 个月，学术界为 8.1 个月”
- **推荐的校友联系人**

### 场景2：培训资助申请

**场景**：实验室需要 NIH T32 资助的申请所需的数据。

**满足 NIH 要求：**
- ✓ 毕业后 6 个月内找到工作的比例
- ✓ 工作岗位与研究相关
- ✓ 包含多样性和代表性不足的少数族裔校友
- ✓ 职业发展轨迹

### 场景3：行业合作伙伴开发

**场景**：实验室希望寻找合作公司。

**生成的见解：**
- 拥有最多校友的公司（潜在合作伙伴）
- 担任决策职位的资深校友
- 适合举办地区性活动的地理聚集区
- 技能与公司需求的匹配程度

### 场景4：个人职业咨询

**场景**：三年级博士生在行业和学术界之间做选择。

**比较内容：**
- 不同路径下的薪资范围（第 1 年、第 5 年、第 10 年）
- 市场就业情况（每年职位数量）
- 校友满意度评分
- 所需的额外技能或培训
- 人脉推荐

## 完整工作流程示例

**从数据收集到可操作的见解：**

```bash
# Step 1: Import existing alumni data
python scripts/main.py \
  --import alumni_survey_2024.csv \
  --validate \
  --output clean_alumni.json

# Step 2: Update LinkedIn profiles
python scripts/main.py \
  --update-linkedin \
  --input clean_alumni.json \
  --output updated_alumni.json

# Step 3: Generate comprehensive report
python scripts/main.py \
  --full-analysis \
  --years 2019-2024 \
  --output-dir career_report_2024/

# Step 4: Create visualization dashboard
python scripts/main.py \
  --dashboard \
  --serve \
  --port 8080
```

**Python API：**

```python
from scripts.tracker import AlumniTracker
from scripts.analyzer import CareerAnalyzer
from scripts.recommender import CareerRecommender

# Initialize
tracker = AlumniTracker(data_path="alumni_db.json")
analyzer = CareerAnalyzer()
recommender = CareerRecommender()

# Load and clean data
tracker.import_csv("alumni_2024.csv")
tracker.clean_data()

# Generate analysis
analysis = analyzer.analyze(tracker.data)
print(f"Industry rate: {analysis.industry_ratio:.1%}")
print(f"Median PhD salary (Year 1): ${analysis.salary_stats['phd_y1']['median']:,}")

# Generate recommendations for a student
recs = recommender.recommend(
    current_student={
        "year": 3,
        "degree": "PhD",
        "field": "Neuroscience"
    },
    alumni_data=tracker.data
)

print("Top 3 career paths:")
for i, path in enumerate(recs.top_paths[:3], 1):
    print(f"{i}. {path.name} ({path.probability:.0%} match)")
```

## 质量检查清单

**数据收集：**
- [ ] 已获得校友的跟踪同意
- [ ] 数据已匿名处理（仅用于汇总统计）
- [ ] 遵守 GDPR/隐私法规
- [ ] 设定了定期更新计划（建议每年更新一次）

**分析准确性：**
- [ ] 至少有 30 名校友的数据才能得出有意义的统计结果
- [ ] 数据经过验证，确保完整性（回复率 >80%）
- [ ] 已识别并验证异常值
- [ ] 薪资数据为可选（尊重隐私）

**报告编写：**
- [ ] **关键要求**：保护个人隐私（报告中不包含可识别信息）
- [ ] 提供数据背景（说明样本量限制）
- **分析多个时间段**：短期与长期结果
- **包含对比基准**：部门/行业平均值

**分享前：**
- [ ] 提供校友审核机会
- [ ] **关键要求**：不分享个人薪资数据
- [ ] 公开报告中仅使用汇总统计数据
- [ ] 尊重校友的退出选项

## 常见问题

**数据质量问题：**
- ❌ **回复率低** → 样本偏差（只有成功校友会回复）
  - ✅ 努力提高回复率至 70% 以上；多次跟进

- ❌ **信息过时** → 使用 5 年前的数据
  - ✅ 每年更新数据；通过 LinkedIn 监控最新信息

- ❌ **样本量小** → 根据少于 10 人的数据得出结论
  - ✅ 在报告中提供置信区间；避免过度解读

**隐私问题：**
- ❌ **分享个人薪资** → 违反隐私规定
  - ✅ 仅报告薪资范围或中位数；按群体汇总

- ❌ **未经同意分享个案研究** → 违反隐私规定
  - ✅ 在突出显示个人案例前必须获得书面许可

**解读问题：**
- ❌ **仅与顶尖实验室比较** → 产生不切实际的期望
  - ✅ 与同类机构进行比较；考虑实际情况

- ❌ **将成功归因于实验室** → 忽视个人因素
  - ✅ 承认外部因素；避免过度归因于实验室

**沟通问题：**
- ❌ 因低就业率而贬低学术界的选择** → 造成偏见
  - ✅ 中立地呈现所有选项；根据个人目标提供建议

- ❌ 过高承诺行业薪资** → 产生不切实际的期望
  - ✅ 提供薪资范围；说明地域差异

## 参考资料

参考资料位于 `references/` 目录：
- `nih_training_requirements.md` - NIH 职业成果报告标准
- `data_privacy_guide.md` - 遵守校友跟踪的 GDPR 和 FERPA 法规
- `survey_templates.md` - 用于收集校友数据的问卷
- `benchmark_data.md` - 各行业的全国职业成果统计数据
- `visualization_best_practices.md` - 数据可视化的伦理指南
- `career_counseling_ethics.md` - 职业咨询的专业标准

## 脚本

脚本位于 `scripts/` 目录：
- `main.py` - 所有操作的命令行接口
- `tracker.py` - 校友数据库管理
- `analyzer.py` - 统计分析和报告生成
- `visualizer.py` - 图表和人脉网络可视化
- `recommender.py` - 个性化职业建议
- `importers.py` - CSV、LinkedIn、调查数据导入
- `exporters.py` - PDF、Word、HTML 报告生成
- `privacy_guard.py` - 数据匿名化和合规性检查

## 限制因素**

- **响应偏差**：成功者更有可能回复，导致样本偏差
- **生存偏差**：仅追踪已毕业的学员，未退出项目的学员未被纳入统计
- **隐私限制**：未经同意无法收集详细数据
- **样本量**：小型实验室可能数据不足，影响统计显著性
- **时间变化**：就业市场变化可能使历史数据失效
- **归因困难**：难以将成果完全归因于实验室

**🎓 请记住：职业追踪工具是为学员服务的，而非评估实验室绩效的工具。使用数据帮助学员做出明智决策，而非强制特定结果。尊重隐私，公正地呈现所有可行的职业路径。**
---
name: "app-store-optimization"
description: >
  **App Store Optimization (ASO) 工具包**  
  该工具包用于研究关键词、分析竞争对手的排名、生成元数据建议，以及提升应用在 Apple App Store 和 Google Play Store 上的可见性。当用户咨询 ASO（应用商店优化）、应用排名、应用元数据、应用标题和描述、应用商店列表、应用可见性，或 iOS/Android 平台上的移动应用营销相关问题时，可以使用该工具包。  
  **主要功能包括：**  
  - 关键词研究与评分  
  - 竞争对手关键词分析  
  - 元数据优化  
  - A/B 测试计划制定  
  - 应用发布前的检查清单  
  - 排名变化的跟踪  
  **适用场景：**  
  适用于需要提升应用在应用商店中表现的用户或团队，特别是那些希望优化应用排名、提高应用曝光率的开发者或营销人员。
triggers:
  - ASO
  - app store optimization
  - app store ranking
  - app keywords
  - app metadata
  - play store optimization
  - app store listing
  - improve app rankings
  - app visibility
  - app store SEO
  - mobile app marketing
  - app conversion rate
---
# 应用商店优化（ASO）

---

## 关键词研究工作流程

发现并评估能够提升应用在应用商店中可见度的关键词。

### 关键词研究工作流程：
1. 确定目标受众和核心应用功能：
   - 应用的主要用途（解决什么问题）
   - 目标用户群体
   - 竞争领域
2. 从以下方面生成关键词种子：
   - 应用特性和优势
   - 用户语言（非开发者术语）
   - 应用商店的自动完成建议
3. 使用以下方式扩展关键词列表：
   - 修饰词（免费、最佳、简单）
   - 动词（创建、跟踪、组织）
   - 目标受众（针对学生、团队、企业）
4. 评估每个关键词：
   - 搜索量（估计的每月搜索次数）
   - 竞争情况（排名应用的数量和质量）
   - 相关性（与应用功能的一致性）
5. 为关键词打分并确定优先级：
   - 主要关键词：应用标题和关键词字段（iOS）
   - 次要关键词：副标题和简短描述
   - 三级关键词：仅用于完整描述

6. 将关键词映射到元数据位置
7. 记录关键词策略以便跟踪

**验证：** 关键词已评分；位置已映射；不包含竞争对手的品牌名称；iOS关键词字段中不使用复数形式

### 关键词评估标准

| 因素 | 权重 | 高分指标 |
|--------|--------|----------------------|
| 相关性 | 35% | 描述了核心应用功能 |
| 搜索量 | 25% | 每月搜索量超过10,000次 |
| 竞争情况 | 25% | 前10名应用的平均评分低于4.5 |
| 转化率 | 15% | 包含交易意图（如“最佳X应用”）

---

## 关键词放置优先级

| 位置 | 搜索权重 |
|----------|---------------|
| 应用标题 | 最高 |
| 副标题（iOS） | 高 |
| 关键词字段（iOS） | 高 |
| 简短描述（Android） | 高 |
| 完整描述 | 中等 |

请参阅：[references/keyword-research-guide.md](references/keyword-research-guide.md)

---

## 元数据优化工作流程

优化应用商店列表元素以提高搜索排名和转化率。

### 元数据优化工作流程：
1. 根据平台限制审核当前的元数据：
   - 标题字符数和关键词的使用情况
   - 副标题/简短描述的使用
   - 关键词字段的效率（iOS）
   - 描述中的关键词密度
2. 按照以下公式优化标题：
   ```
   [Brand Name] - [Primary Keyword] [Secondary Keyword]
   ```
3. 编写副标题（iOS）或简短描述（Android）：
   - 重点突出主要优势
   - 包含次要关键词
   - 使用动词
4. 仅优化关键词字段（iOS）：
   - 从标题中删除重复项
   - 删除复数形式（Apple会同时索引两种形式）
   - 逗号后不要有空格
   - 按评分优先排序
5. 重写完整描述：
   - 用价值主张开头
   - 用关键词列出功能
   - 包含社交证明部分
   - 提供行动号召
6. 验证每个字段的字符数
7. 计算关键词密度（目标为2-3%）

**验证：** 所有字段都在字符限制范围内；主要关键词在标题中；没有关键词堆砌（超过5%）；保持自然语言

### 平台字符限制

| 字段 | Apple应用商店 | Google Play商店 |
|-------|-----------------|-------------------|
| 标题 | 30个字符 | 50个字符 |
| 副标题 | 30个字符 | 不适用 |
| 简短描述 | 不适用 | 80个字符 |
| 关键词 | 100个字符 | 不适用 |
| 宣传文本 | 170个字符 | 不适用 |
| 完整描述 | 4,000个字符 | 4,000个字符 |
| 新功能 | 4,000个字符 | 500个字符 |

### 描述结构

```
PARAGRAPH 1: Hook (50-100 words)
├── Address user pain point
├── State main value proposition
└── Include primary keyword

PARAGRAPH 2-3: Features (100-150 words)
├── Top 5 features with benefits
├── Bullet points for scanability
└── Secondary keywords naturally integrated

PARAGRAPH 4: Social Proof (50-75 words)
├── Download count or rating
├── Press mentions or awards
└── Summary of user testimonials

PARAGRAPH 5: Call to Action (25-50 words)
├── Clear next step
└── Reassurance (free trial, no signup)
```

请参阅：[references/platform-requirements.md](references/platform-requirements.md)

---

## 竞争对手分析工作流程

分析顶级竞争对手，以识别关键词差距和定位机会。

### 竞争对手ASO策略分析工作流程：
1. 确定前10名竞争对手：
   - 直接竞争对手（具有相同核心功能）
   - 间接竞争对手（目标受众重叠）
   - 行业领导者（下载量最高的）
2. 从以下方面提取竞争对手的关键词：
   - 应用标题和副标题
   - 描述的前100个词
   | 可见的元数据模式
3. 构建竞争对手关键词矩阵：
   - 映射每个竞争对手针对的关键词
   | 计算每个关键词的覆盖百分比
4. 识别关键词差距：
   | 被竞争对手覆盖率低于40%的关键词 |
   | 竞争对手遗漏的高搜索量词汇 |
   | 长尾关键词机会
5. 分析竞争对手的视觉元素：
   | 图标设计模式 |
   | 截图信息和风格 |
   | 视频的存在和质量
6. 分析评分和评论模式：
   | 各竞争对手的平均评分 |
   | 常见的赞扬和投诉主题
7. 记录定位机会

**验证：** 分析了10个以上竞争对手；关键词矩阵完整；识别出关键词差距及搜索量估计；记录了视觉审计结果

### 竞争对手分析矩阵

| 分析领域 | 数据点 |
|---------------|-------------|
| 关键词 | 标题关键词、描述频率 |
| 元数据 | 字符使用情况、关键词密度 |
| 视觉元素 | 图标风格、截图数量/风格 |
| 评分 | 平均评分、总数、更新频率 |
| 评论 | 最常见的赞扬和投诉 |

### 差距分析模板

| 机会类型 | 例子 | 行动 |
|------------------|---------|--------|
| 关键词差距 | “习惯追踪器”（覆盖率为40%） | 添加到关键词字段 |
| 功能差距 | 竞争对手缺少小工具 | 在截图中突出显示 |
| 视觉差距 | 前5名中没有视频 | 创建应用预览 |
| 信息差距 | 没有提到“免费” | 测试免费定位 |

---

## 应用发布工作流程

执行结构化的发布流程，以实现最大的初始可见度。

### 应用发布工作流程：
1. 完成发布前的准备工作（提前4周）：
   - 确定最终关键词和元数据
   | 准备所有视觉元素 |
   | 设置分析工具（Firebase、Mixpanel）
   | 准备新闻稿和媒体列表
2. 提交审核（提前2周）：
   | 完成所有商店要求 |
   | 验证是否符合指南 |
   | 准备发布沟通材料
3. 配置发布后的系统：
   | 设置审核监控 |
   | 准备回复模板 |
   | 配置评分提示的时间
4. 执行发布日：
   | 确认应用在两个商店中上线 |
   | 在所有渠道宣布 |
   | 开始回复评论 |
5. 监控初始表现（前7天）：
   | 每小时跟踪下载速度 |
   | 监控评论并在24小时内回复 |
   | 记录任何问题以便快速修复 |
6. 进行7天回顾：
   | 将表现与预测进行比较 |
   | 识别出快速优化的机会 |
   | 规划首次元数据更新 |
7. 安排首次更新（发布后2周）

**验证：** 应用在商店中上线；分析工具正在跟踪；评论回复在24小时内；下载速度已记录；首次更新已安排

### 发布前检查清单

| 类别 | 项目 |
|----------|-------|
| 元数据 | 标题、副标题、描述、关键词 |
| 视觉元素 | 图标、截图（所有尺寸）、视频 |
| 合规性 | 应用年龄、评分、隐私政策、内容权限 |
| 技术 | 应用二进制文件、签名证书 |
| 分析工具 | SDK集成、事件跟踪 |
| 营销 | 新闻稿、社交媒体内容、电子邮件准备 |

### 发布时间考虑因素

| 因素 | 建议 |
|--------|----------------|
| 星期几 | 星期二至星期三（避免周末） |
| 时间 | 目标市场时区的上午 |
| 季节性 | 与相关领域的季节同步 |
| 竞争情况 | 避免与主要竞争对手的发布日期冲突 |

请参阅：[references/aso-best-practices.md](references/aso-best-practices.md)

---

## A/B测试工作流程

测试元数据和视觉元素以提高转化率。

### A/B测试工作流程：
1. 选择测试元素（根据影响优先级）：
   - 图标（影响最大）
   | 截图1（影响较大）
   | 标题（影响较大）
   | 简短描述（影响中等）
2. 形成假设：
   ```
   If we [change], then [metric] will [improve/increase] by [amount]
   because [rationale].
   ```
3. 创建变体：
   - 对照组：当前版本
   | 实验组：单个变量更改
4. 计算所需的样本量：
   | 基线转化率 |
   | 最小可检测效果（通常为5%）
   | 统计显著性（95%）
5. 运行测试：
   | Apple：使用产品页面优化 |
   | Android：使用商店列表实验 |
6. 运行测试的最短时间：
   | 至少7天 |
   | 直到达到统计显著性 |
7. 分析结果：
   | 比较转化率 |
   | 检查统计显著性 |
   | 记录学习成果 |
8. **验证：** 测试了单个变量；样本量足够；达到显著性（95%）；结果已记录；最佳方案已实施

### A/B测试优先级

| 元素 | 转化率影响 | 测试复杂性 |
|---------|-------------------|-----------------|
| 应用图标 | 可能提升10-25% | 中等（需要设计） |
| 截图1 | 可能提升15-35% | 中等 |
| 标题 | 可能提升5-15% | 低 |
| 简短描述 | 可能提升5-10% | 低 |
| 视频 | 可能提升10-20% | 高 |

### 样本量快速参考

| 基线CVR | 每个变体所需的展示次数 |
|--------------|----------------------------------|
| 1% | 31,000 |
| 2% | 15,500 |
| 5% | 6,200 |
| 10% | 3,100 |

### 测试文档模板

```
TEST ID: ASO-2025-001
ELEMENT: App Icon
HYPOTHESIS: A bolder color icon will increase conversion by 10%
START DATE: [Date]
END DATE: [Date]

RESULTS:
├── Control CVR: 4.2%
├── Treatment CVR: 4.8%
├── Lift: +14.3%
├── Significance: 97%
└── Decision: Implement treatment

LEARNINGS:
- Bold colors outperform muted tones in this category
- Apply to screenshot backgrounds for next test
```

---

## 示例：优化前后的对比

### 标题优化

**生产力应用：**

| 版本 | 标题 | 分析 |
|---------|-------|----------|
| 优化前 | “MyTasks” | 仅包含品牌名称，没有关键词（8个字符） |
| 优化后 | “MyTasks - 待办事项列表与计划器” | 包含主要和次要关键词（29个字符） |

**健身应用：**

| 版本 | 标题 | 分析 |
|---------|-------|----------|
| 优化前 | “FitTrack Pro” | 通用修饰词（12个字符） |
| 优化后 | “FitTrack：锻炼日志与健身房” | 包含行业关键词（27个字符） |

### 副标题优化（iOS）：

| 版本 | 副标题 | 分析 |
|---------|----------|----------|
| 优化前 | “Get Things Done” | 表达模糊，没有关键词 |
| 优化后 | “每日任务管理器与计划器” | 包含两个关键词，优势明确 |

### 关键词字段优化（iOS）：

**优化前（效率低下 - 89个字符，8个关键词）：**
```
task manager, todo list, productivity app, daily planner, reminder app
```

**优化后（97个字符，14个关键词）：**
```
task,todo,checklist,reminder,organize,daily,planner,schedule,deadline,goals,habit,widget,sync,team
```

**改进措施：**
- 逗号后删除了空格（增加了8个字符）
- 删除了重复项（将“task manager”改为“task”）
- 删除了标题中的无关词汇
- 添加了更相关的关键词

### 描述开头优化：

**优化前：**
```
MyTasks is a comprehensive task management solution designed
to help busy professionals organize their daily activities
and boost productivity.
```

**优化后：**
```
Forget missed deadlines. MyTasks keeps every task, reminder,
and project in one place—so you focus on doing, not remembering.
Trusted by 500,000+ professionals.
```

**改进措施：**
- 以用户痛点开头 |
- 强调具体优势（而非泛泛而谈的“提高生产力” |
- 包含社交证明 |
- 关键词使用自然，没有堆砌

### 截图标题优化

| 版本 | 标题 | 问题 |
|---------|---------|-------|
| 优化前 | “Task List Feature” | 以功能为中心，被动表达 |
| 优化后 | “Create Task Lists” | 使用动词，但仍以功能为中心 |
| 最佳版本 | “Never Miss a Deadline” | 以优势为中心，带有情感色彩 |

---

## 工具和参考资料

### 脚本

| 脚本 | 用途 | 使用方法 |
|--------|---------|-------|
| [keyword_analyzer.py](scripts/keyword_analyzer.py) | 分析关键词的搜索量和竞争情况 | `python keyword_analyzer.py --keywords "todo,task,planner"` |
| [metadata_optimizer.py](scripts/metadata_optimizer.py) | 验证元数据的字符限制和关键词密度 | `python metadata_optimizer.py --platform ios --title "App Title"` |
| [competitor_analyzer.py](scripts/competitor_analyzer.py) | 提取并比较竞争对手的关键词 | `python competitor_analyzer.py --competitors "App1,App2,App3"` |
| [aso_scorer.py](scripts/aso_scorer.py) | 计算整体ASO健康评分 | `python aso_scorer.py --app-id com.example.app` |
| [ab_test_planner.py](scripts/ab_test_planner.py) | 规划测试并计算样本量 | `python ab_test_planner.py --cvr 0.05 --lift 0.10` |
| [review_analyzer.py](scripts/review_analyzer.py) | 分析评论情感和主题 | `python review_analyzer.py --app-id com.example.app` |
| [launch_checklist.py](scripts/launch_checklist.py) | 生成特定平台的发布检查清单 | `python launch_checklist.py --platform ios` |
| [localization_helper.py](scripts/localization_helper.py) | 管理多语言元数据 | `python localization_helper.py --locales "en,es,de,ja"` |

### 参考资料

| 文档 | 内容 |
|----------|---------|
| [platform-requirements.md](references/platform-requirements.md) | iOS和Android的元数据规范、视觉元素要求 |
| [aso-best-practices.md](references/aso-best-practices.md) | 优化策略、评分管理、发布技巧 |
| [keyword-research-guide.md](references/keyword-research-guide.md) | 研究方法、评估框架、跟踪方法 |

### 资源

| 模板 | 用途 |
|----------|---------|
| [aso-audit-template.md](assets/aso-audit-template.md) | 应用商店列表的结构化审计清单 |

---

## 平台注意事项

| 平台/限制 | 行为/影响 |
|-----------------------|-------------------|
| iOS关键词更改 | 需要重新提交应用 |
| iOS宣传文本 | 可以在不更新应用的情况下进行编辑 |
| Android元数据更改 | 1-2小时内即可索引 |
| Android关键词字段 | 无——使用描述代替 |
| 关键词搜索量数据 | 仅提供估计值；无官方来源 |
| 竞争对手数据 | 仅基于公开列表 |

**不适用的情况：** Web应用（使用Web SEO）、企业/内部应用、仅限TestFlight的测试版本，或付费广告策略。

---

## 相关技能

| 技能 | 集成点 |
|-------|-------------------|
| [content-creator](../content-creator/) | 应用描述文案写作 |
| [marketing-demand-acquisition](../marketing-demand-acquisition/) | 发布推广活动 |
| [marketing-strategy-pmm](../marketing-strategy-pmm/) | 市场进入策略规划 |

## 主动提醒：

- **标题中不要优化关键词** → 应用标题是排名最重要的因素。务必包含主要关键词。
- **截图无法展示应用价值** → 截图应讲述故事，而非展示用户界面。
- **没有评分策略** → 评分低于4.0会影响转化率。请实施应用内的评分提示。
- **描述中关键词堆砌过多** → 使用自然语言搭配关键词比单纯堆砌关键词更有效。

## 输出成果

| 当您请求... | 您将获得... |
|---------------------|------------|
| “ASO审计” | 包含优先修复项的完整应用商店列表审计 |
| “关键词研究” | 带有搜索量和难度评分的关键词列表 |
| “优化我的应用列表” | 重写的标题、副标题、描述和关键词字段 |

## 交流方式

所有输出都经过质量验证：
- 自我验证：来源标注、假设审核、信心评分
- 输出格式：首先说明结果（以及置信度），然后解释原因，最后提供行动方案
- 仅提供结果。每个发现都会标注为：🟢 已验证，🟡 中等，🔴 推测。

---

---

这些文档涵盖了应用商店优化（ASO）的各个方面，包括关键词研究、元数据优化、竞争对手分析、应用发布和A/B测试等关键流程。同时，还提供了相应的工具和参考资料，以及具体的操作步骤和示例。
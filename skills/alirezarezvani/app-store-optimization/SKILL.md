---
name: app-store-optimization
description: App Store Optimization 工具包：用于研究关键词、优化元数据，以及监控移动应用在 Apple App Store 和 Google Play Store 上的性能。
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

ASO 工具用于研究关键词、优化元数据、分析竞争对手，并提高应用在 Apple App Store 和 Google Play Store 中的可见性。

---

## 目录

- [关键词研究工作流程](#keyword-research-workflow)
- [元数据优化工作流程](#metadata-optimization-workflow)
- [竞争对手分析工作流程](#competitor-analysis-workflow)
- [应用发布工作流程](#app-launch-workflow)
- [A/B 测试工作流程](#ab-testing-workflow)
- [前后对比示例](#beforeafter-examples)
- [工具和参考资料](#tools-and-references)

---

## 关键词研究工作流程

发现并评估能够提升应用商店可见性的关键词。

### 关键词研究工作流程：

1. 定义目标受众和核心应用功能：
   - 应用解决的主要问题
   - 目标用户群体
   - 竞争领域
2. 从以下方面生成关键词种子：
   - 应用功能和优势
   - 用户语言（非开发术语）
   - 应用商店自动完成建议
3. 使用以下方法扩展关键词列表：
   - 修饰词（免费、最佳、简单）
   - 动词（创建、跟踪、组织）
   - 审视群体（针对学生、团队、企业）
4. 评估每个关键词：
   - 搜索量（估计的月搜索次数）
   - 竞争情况（排名应用的数量和质量）
   - 相关性（与应用功能的匹配程度）
5. 为关键词打分并确定优先级：
   - 主要关键词：应用标题和关键词字段（iOS）
   - 次要关键词：副标题和简短描述
   - 三级关键词：仅限完整描述
6. 将关键词映射到元数据位置
7. 记录关键词策略以供跟踪
8. **验证：** 关键词已评分；位置已映射；不包含竞争对手的品牌名称；iOS 关键词字段中不使用复数形式

### 关键词评估标准

| 因素 | 权重 | 高分指标 |
|--------|--------|----------------------|
| 相关性 | 35% | 描述了应用的核心功能 |
| 搜索量 | 25% | 每月搜索次数超过 10,000 次 |
| 竞争情况 | 25% | 前 10 名应用的平均评分低于 4.5 分 |
| 转化率 | 15% | 包含交易意图（如“最佳 X 应用”）

### 关键词放置优先级

| 位置 | 搜索权重 | 字符限制 |
|----------|---------------|-----------------|
| 应用标题 | 最高 | 30 个字符（iOS）/ 50 个字符（Android） |
| 副标题（iOS） | 高 | 30 个字符 |
| 关键词字段（iOS） | 高 | 100 个字符 |
| 简短描述（Android） | 高 | 80 个字符 |
| 完整描述 | 中等 | 4,000 个字符 |

参见：[references/keyword-research-guide.md](references/keyword-research-guide.md)

---

## 元数据优化工作流程

优化应用商店列表元素以提高搜索排名和转化率。

### 元数据优化工作流程：

1. 根据平台限制审核当前的元数据：
   - 标题字符数和关键词的使用情况
   - 副标题/简短描述的使用
   - 关键词字段的效率（iOS）
2. 按照以下公式优化标题：
   ```
   [Brand Name] - [Primary Keyword] [Secondary Keyword]
   ```
3. 编写副标题（iOS）或简短描述（Android）：
   - 突出主要优势
   - 包含次要关键词
   - 使用动词
4. 仅优化关键词字段（iOS）：
   - 从标题中删除重复项
   - 删除复数形式（Apple 会同时索引两种形式）
   - 逗号后不要有空格
   - 按评分优先排序
5. 重写完整描述：
   - 用价值主张开头
   - 用关键词列出功能
   - 添加社交证明部分
   - 添加行动号召
6. 验证每个字段的字符数
7. 计算关键词密度（目标为 2-3%）
8. **验证：** 所有字段都在字符限制范围内；主要关键词在标题中；没有关键词堆砌（超过 5%）；保持自然语言

### 平台字符限制

| 字段 | Apple App Store | Google Play Store |
|-------|-----------------|-------------------|
| 标题 | 30 个字符 | 50 个字符 |
| 副标题 | 30 个字符 | 不适用 |
| 简短描述 | 不适用 | 80 个字符 |
| 关键词 | 100 个字符 | 不适用 |
| 宣传文本 | 170 个字符 | 不适用 |
| 完整描述 | 4,000 个字符 | 4,000 个字符 |
| 新功能 | 4,000 个字符 | 500 个字符 |

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

参见：[references/platform-requirements.md](references/platform-requirements.md)

---

## 竞争对手分析工作流程

分析顶级竞争对手，以识别关键词差距和定位机会。

### 竞争对手分析工作流程：

1. 确定前 10 名竞争对手：
   - 直接竞争对手（具有相同核心功能）
   - 间接竞争对手（目标受众重叠）
   - 行业领导者（下载量最高的）
2. 从以下方面提取竞争对手的关键词：
   - 应用标题和副标题
   | 描述的前 100 个单词
   | 可见的元数据模式
3. 构建竞争对手关键词矩阵：
   - 映射每个竞争对手针对的关键词
   | 计算每个关键词的覆盖百分比
4. 识别关键词差距：
   - 被竞争对手覆盖率低于 40% 的关键词
   | 竞争对手遗漏的高搜索量词汇
   | 长尾关键词机会
5. 分析竞争对手的视觉元素：
   - 图标设计模式
   | 截图信息和风格
   | 视频的存在和质量
6. 比较评分和评论模式：
   | 竞争对手的平均评分
   | 常见的赞美和投诉主题
7. 记录定位机会
8. **验证：** 分析了 10 名以上竞争对手；关键词矩阵完整；识别出关键词差距及搜索量估计；记录了视觉审计结果

### 竞争对手分析矩阵

| 分析领域 | 数据点 |
|---------------|-------------|
| 关键词 | 标题关键词、描述频率 |
| 元数据 | 字符使用情况、关键词密度 |
| 视觉元素 | 图标风格、截图数量/风格 |
| 评分 | 平均评分、总评分数、更新频率 |
| 评论 | 最常见的赞美和投诉 |

### 差距分析模板

| 机会类型 | 例子 | 行动 |
|------------------|---------|--------|
| 关键词差距 | “习惯追踪器”（覆盖率为 40%） | 添加到关键词字段 |
| 功能差距 | 竞争对手缺少小工具 | 在截图中突出显示 |
| 视觉差距 | 前 5 名中没有视频 | 创建应用预览 |
| 信息差距 | 没有提到“免费” | 测试免费定位 |

---

## 应用发布工作流程

执行结构化的发布流程，以获得最大的初始可见性。

### 应用发布工作流程：

1. 完成发布前的准备工作（发布前 4 周）：
   - 确定最终关键词和元数据
   | 准备所有视觉元素
   | 设置分析工具（Firebase、Mixpanel）
   | 准备新闻稿和媒体列表
2. 提交审核（发布前 2 周）：
   | 完成所有商店要求
   | 验证是否符合指南
   | 准备发布沟通材料
3. 配置发布后的系统：
   | 设置评论监控
   | 准备回复模板
   | 配置评分提示的时间
4. 执行发布日：
   | 确保应用在两个商店中上线
   | 在所有渠道发布公告
   | 开始回复评论
5. 监控初始表现（第 1-7 天）：
   | 每小时跟踪下载速度
   | 在 24 小时内回复评论
   | 记录任何问题以便快速修复
6. 进行 7 天回顾：
   | 将表现与预测进行比较
   | 识别出快速优化的地方
   | 规划首次元数据更新
7. 安排首次更新（发布后 2 周）
8. **验证：** 应用在商店中上线；分析工具正在跟踪；评论回复在 24 小时内；记录下载速度；安排了首次更新

### 发布前检查清单

| 类别 | 项目 |
|----------|-------|
| 元数据 | 标题、副标题、描述、关键词 |
| 视觉元素 | 图标、截图（所有尺寸）、视频 |
| 合规性 | 应用年龄、评分、隐私政策、内容权限 |
| 技术 | 应用二进制文件、签名证书 |
| 分析 | SDK 集成、事件跟踪 |
| 营销 | 新闻稿、社交媒体内容、电子邮件准备 |

### 发布时间考虑因素

| 因素 | 建议 |
|--------|----------------|
| 星期几 | 星期二至星期三（避免周末） |
| 时间 | 目标市场时区的上午 |
| 季节性 | 与相关行业的季节同步 |
| 竞争对手 | 避免与主要竞争对手的发布日期重合 |

参见：[references/aso-best-practices.md](references/aso-best-practices.md)

---

## A/B 测试工作流程

测试元数据和视觉元素以提高转化率。

### A/B 测试工作流程：

1. 选择测试元素（根据影响优先级）：
   | 图标（影响最大）
   | 第一张截图（影响较大）
   | 标题（影响较大）
   | 简短描述（影响中等）
2. 形成假设：
   ```
   If we [change], then [metric] will [improve/increase] by [amount]
   because [rationale].
   ```
3. 创建变体：
   | 对照组：当前版本
   | 实验组：单个变量更改
4. 计算所需的样本量：
   | 基线转化率
   | 最小可检测效果（通常为 5%）
   | 统计显著性（95%）
5. 运行测试：
   | Apple：使用产品页面优化功能
   | Android：使用商店列表实验功能
6. 运行测试的最短时间：
   | 至少 7 天
   | 直到达到统计显著性
7. 分析结果：
   | 比较转化率
   | 检查统计显著性
   | 记录学习成果
8. **验证：** 测试了单个变量；样本量足够；达到显著性（95%）；结果已记录；实施最佳方案

### A/B 测试优先级

| 元素 | 转化率影响 | 测试复杂性 |
|---------|-------------------|-----------------|
| 应用图标 | 可能提升 10-25% | 中等（需要设计） |
| 第一张截图 | 可能提升 15-35% | 中等 |
| 标题 | 可能提升 5-15% | 低 |
| 简短描述 | 可能提升 5-10% | 低 |
| 视频 | 可能提升 10-20% | 高 |

### 样本量快速参考

| 基线转化率 | 每个变体需要的展示次数 |
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

## 前后对比示例

### 标题优化

**生产力应用：**

| 版本 | 标题 | 分析 |
|---------|-------|----------|
| 之前 | “MyTasks” | 仅包含品牌名称，没有关键词（8 个字符） |
| 之后 | “MyTasks - 待办事项列表与计划器” | 包含主要和次要关键词（29 个字符） |

**健身应用：**

| 版本 | 标题 | 分析 |
|---------|-------|----------|
| 之前 | “FitTrack Pro” | 使用通用修饰词（12 个字符） |
| 之后 | “FitTrack: 锻炼日志与健身房” | 包含行业关键词（27 个字符） |

### 副标题优化（iOS）

| 版本 | 副标题 | 分析 |
|---------|----------|----------|
| 之前 | “Get Things Done” | 表达模糊，没有关键词 |
| 之后 | “每日任务管理器与计划器” | 包含两个关键词，优势明确 |

### 关键词字段优化（iOS）

**优化前（效率低 - 89 个字符，8 个关键词）：**
```
task manager, todo list, productivity app, daily planner, reminder app
```

**优化后（97 个字符，14 个关键词）：**
```
task,todo,checklist,reminder,organize,daily,planner,schedule,deadline,goals,habit,widget,sync,team
```

**改进措施：**
- 逗号后删除了空格（增加了 8 个字符）
- 删除了重复项（将“task manager”改为“task”）
- 删除了标题中的无关词汇
- 添加了更相关的关键词

### 描述开头优化

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
- 以用户痛点开头
- 强调具体优势（而非泛泛的“提高生产力”）
- 包含社交证明
- 关键词使用自然，没有堆砌

### 截图标题优化

| 版本 | 标题 | 问题 |
|---------|---------|-------|
| 之前 | “任务列表功能” | 以功能为中心，被动表达 |
| 优化后 | “创建任务列表” | 使用动词，但仍以功能为中心 |
| 最佳版本 | “绝不错过截止日期” | 强调优势，更具情感共鸣 |

---

## 工具和参考资料

### 脚本

| 脚本 | 用途 | 使用方法 |
|--------|---------|-------|
| [keyword_analyzer.py](scripts/keyword_analyzer.py) | 分析关键词的搜索量和竞争情况 | `python keyword_analyzer.py --keywords "todo,task,planner"` |
| [metadata_optimizer.py](scripts/metadata_optimizer.py) | 验证元数据的字符限制和关键词密度 | `python metadata_optimizer.py --platform ios --title "App Title"` |
| [competitor_analyzer.py](scripts/competitor_analyzer.py) | 提取并比较竞争对手的关键词 | `python competitor_analyzer.py --competitors "App1,App2,App3"` |
| [aso_scorer.py](scripts/aso_scorer.py) | 计算整体 ASO 健康评分 | `python aso_scorer.py --app-id com.example.app` |
| [ab_test_planner.py](scripts/ab_test_planner.py) | 规划测试并计算样本量 | `python ab_test_planner.py --cvr 0.05 --lift 0.10` |
| [review_analyzer.py](scripts/review_analyzer.py) | 分析评论情感和主题 | `python review_analyzer.py --app-id com.example.app` |
| [launch_checklist.py](scripts/launch_checklist.py) | 生成特定平台的发布检查清单 | `python launch_checklist.py --platform ios` |
| [localization_helper.py](scripts/localization_helper.py) | 管理多语言元数据 | `python localization_helper.py --locales "en,es,de,ja"` |

### 参考资料

| 文档 | 内容 |
|----------|---------|
| [platform-requirements.md](references/platform-requirements.md) | iOS 和 Android 的元数据规范、视觉元素要求 |
| [aso-best-practices.md](references/aso-best-practices.md) | 优化策略、评分管理、发布技巧 |
| [keyword-research-guide.md](references/keyword-research-guide.md) | 研究方法、评估框架、跟踪方法 |

### 资源

| 模板 | 用途 |
|----------|---------|
| [aso-audit-template.md](assets/aso-audit-template.md) | 应用商店列表的结构化审计清单 |

---

## 平台限制

### 数据限制

| 限制 | 影响 |
|------------|--------|
| 无官方关键词搜索量数据 | 基于第三方工具的估计 |
| 竞争对手数据仅限于公开信息 | 无法查看内部指标 |
| 评论访问仅限于公开评论 | 无法获取私人反馈 |
| 新应用无法获取历史数据 | 无法与过去的表现进行比较 |

### 平台行为

| 平台 | 行为 |
|----------|----------|
| iOS | 关键词更改需要重新提交应用 |
| iOS | 宣传文本可以编辑，无需更新 |
| Android | 元数据更改会在 1-2 小时内生效 |
| Android | 没有单独的关键词字段（使用描述） |
| 两个平台 | 算法更改会无通知 |

### 何时不适用此技能

| 情况 | 替代方案 |
|----------|-------------|
| Web 应用 | 使用 Web SEO 技巧 |
| 企业应用（非公开） | 使用内部分发工具 |
| 仅限测试/试用阶段 | 专注于反馈，而非 ASO |
| 支付广告策略 | 使用付费获取技巧 |

---

## 相关技能

| 技能 | 集成点 |
|-------|-------------------|
| [content-creator](../content-creator/) | 应用描述文案写作 |
| [marketing-demand-acquisition](../marketing-demand-acquisition/) | 发布推广活动 |
| [marketing-strategy-pmm](../marketing-strategy-pmm/) | 市场进入策略规划 |
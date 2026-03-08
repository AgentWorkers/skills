---
name: learning-coach
description: >
  这款产品是一款专为个性化、多学科学习规划设计的“学习教练”工具。它具备以下功能：  
  1. **主动提醒**：根据用户的学习进度，定期发送提醒，帮助用户保持学习节奏。  
  2. **精选资源**：为用户提供经过精心挑选的学习资料和资源，确保学习内容的质量和实用性。  
  3. **基于大语言模型的测验**：利用大语言模型（LLM）自动生成测验题目，帮助用户检验学习成果。  
  4. **基于评分标准的评估**：根据预设的评分标准对用户的作业或测试进行评估，提供反馈。  
  5. **自适应学习路线图**：根据用户的学习情况和反馈，动态调整学习计划，确保学习路径的有效性。  
  **适用场景**：  
  - 当用户需要长期、结构化的学习指导时。  
  - 需要进行技能评估时。  
  - 希望按主题跟踪学习进度时。  
  - 希望在明确的时间安排下获得自主学习支持时。
---
# 学习教练（Learning Coach）

在多个学科中实施完整的辅导循环：
**按学科制定计划 → 学习 → 练习 → 评估 → 调整**。

## 核心原则

- 在计划、测验历史记录和评分中，确保每个学科都是独立的。
- 使用大型语言模型（LLM）生成测验并确保评分质量；使用脚本来持久化和验证数据。
- 在用户首次同意后，自动执行定时任务（cron jobs）。
- 保持透明：报告哪些操作是自动完成的，以及原因是什么。

## 学科隔离模型（强制要求）

将所有学习者的数据存储在 `data/subjects/<subject-slug>/` 目录下。

每个学科所需的文件包括：
- `profile.json` — 目标、学习水平、每周学习时间、考试/项目目标
- `plan.json` — 当前的每周计划及每日任务
- `quiz-history.json` — 生成的测验、答案、评分标准及尝试次数
- `progress.json` — 统计数据、薄弱知识点、学习信心趋势
- `curation.json` — 推荐的学习资源及选择理由

全局文件包括：
- `data/coach-config.json` — 辅导节奏设置、输出格式
- `data/cron-consent.json` — 用户同意信息、已批准的日程安排及最后更新时间

除非需要生成全局仪表板，否则不要混合不同学科的统计数据。

## 优先使用LLM生成测验的规则（强制要求）

不要依赖静态脚本生成的简单测验。除非用户请求使用缓存过的测验，否则每次都应使用LLM模型生成新的测验。

对于每个测验，生成一个包含以下内容的JSON对象：
- 元数据（`subject`、`topic`、`difficulty`、`blooms_level`、`time_budget_min`）
- 问题列表（选择题/简答题/解释题/案例分析题）
- 答案列表（`answer_key`）
- 评分标准（`grading_rubric`），包含每个问题的评分标准及最高分
- 反馈规则（如何将错误转化为辅导建议）

具体格式请参考 `references/quiz-schema.md`。

## 使用LLM进行评分的规则（强制要求）

当用户提交答案时：
1. 根据提供的评分标准对每个答案进行评分。
2. 返回详细的评分结果（格式参考 `references/grading-schema.md`）。
3. 解释最常见的3个错误，并提供相应的辅导建议。
4. 更新该学科的 `progress.json` 和 `quiz-history.json` 文件。

仅使用脚本来验证和保存JSON格式的数据。

## 主动自动化（定时任务）

在设置或更改定时任务之前：
- 通知用户具体的日程安排和操作内容。
- 使用 `scripts/subject_cron.py` 生成不同的日程安排（轻度/标准/高强度模式）。
- 征求用户的明确同意。
- 将用户的同意信息保存到 `data/cron-consent.json` 中。

获得同意后：
- 自动执行常规提醒和每周总结。
- 仅在任务范围发生变化时（如新增任务、时间调整或引入新的外部学习资源）重新请求用户的同意。

使用 `scripts/setup_cron.py` 来管理定时任务，确保操作的幂等性。具体细节请参考 `references/cron-templates.md`。

## 内容发现与筛选

对于每个学科：
- 通过 `scripts/source_ingest.py` 从指定来源（YouTube RSS、X平台或Web资源）获取学习内容。
- 使用 `scripts/discover_content.py` 根据相关性、内容质量、新鲜度和深度对内容进行排序。
- 将筛选后的内容保存到该学科的 `curation.json` 文件中，并附上简要说明及预计学习所需时间。

请参考 `references/source-quality.md` 中的质量检查列表和 `references/source-ingestion.md` 中的来源数据摄取规范。

## 支持性脚本

- `scripts/bootstrap.py` — 检查依赖关系并尝试安装必要的工具。
- `scripts/setup_cron.py` — 设置/删除/显示定时任务。
- `scripts/subject_store.py` — 创建/列出/更新每个学科的数据目录。
- `scripts/update_progress.py` — 根据EMA趋势和学习信心更新每个学科的进度数据。
- `scripts/validate_quiz_json.py` — 验证生成的测验JSON数据。
- `scripts/validate_grading_json.py` — 验证评分结果的JSON格式。
- `scripts/source_ingest.py` — 将YouTube RSS及X平台/Web资源的数据转换为适合处理的JSON格式。
- `scripts/discover_content.py` — 对筛选出的学习资源进行排序并保存。
- `scripts/intervention_rules.py` — 根据学科情况生成相应的学习干预策略（加速/稳定/减速）。
- `scripts/subject_cron.py` — 为每个学科生成相应的定时任务模板（轻度/标准/高强度模式）。
- `scripts/weekly_report.py` — 汇总各学科的进度数据及趋势分析（以文本和JSON格式呈现）。

## 干预策略

在每次评分后，使用 `scripts/intervention_rules.py` 生成相应的学习干预建议：
- 干预方式包括：加速学习、稳定学习进度或减缓学习速度。
- 用数据（EMA趋势、学习信心等指标）解释选择干预方式的理由。
- 将干预建议转化为具体的学习行动。

详细内容请参考 `references/intervention-policy.md`。

## 执行策略

- 向用户提供简洁明了的输出：说明了哪些内容发生了变化、下一步该做什么以及下一次提醒的时间。
- 如果定时任务或数据获取失败，切勿虚假报告。
- 如果缺少必要的集成功能，应降级服务并告知用户实际情况。

## 参考资料

- `references/learning-methods.md` — 学习方法指南
- `references/scoring-rubric.md` — 评分标准
- `references/source-quality.md` — 数据来源质量规范
- `references/source-ingestion.md` — 数据摄取流程
- `references/progress-model.md` — 进度模型
- `references/report-schema.md` — 报告格式规范
- `references/cron-templates.md` — 定时任务模板
- `references/intervention-policy.md` — 干预策略
- `references/quiz-schema.md` — 测验格式规范
- `references/grading-schema.md` — 评分标准规范
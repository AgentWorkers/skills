---
name: continuous-user-research
description: 为产品团队开展纵向的、基于上下文的日记式研究（longitudinal, in-context diary studies），并将参与者每周的记录转化为简洁的用户反馈（User Signals）与建议（Recommendations），这些反馈和建议应包含相应的证据、置信度评估以及可供实验使用的具体行动方案。这些研究可用于新员工入职后的流失情况诊断（onboarding drop-off diagnosis）、了解用户对功能的习惯和使用频率（feature habit/frequency analysis）、分析用户的动机和情绪（motivation and emotion analysis）、绘制用户的多触点使用路径（multi-touchpoint journey mapping），以及比较不同渠道或设备上的用户行为（channel/device behavior comparisons）。该工具支持基于事件（event-based）、基于时间间隔（interval-based）、基于用户反馈（signal-based）等多种研究设计方式，并提供试点验证（pilot validation）、合规性监控（compliance monitoring）以及隐私保护的报告生成功能（privacy-redacted reporting）。
metadata:
  openclaw:
    skillKey: continuous-user-research
    primaryEnv: CONTINUOUS_USER_RESEARCH_PROFILE
    always: false
    requires:
      env:
        - RESEARCH_STUDY_STORAGE_RAW_PATH
        - RESEARCH_STUDY_STORAGE_REPORTS_PATH
        - RESEARCH_REDACTION_SALT
        - RESEARCH_NOTION_TOKEN
        - RESEARCH_NOTION_DATABASE_ID
        - RESEARCH_SLACK_BOT_TOKEN
        - RESEARCH_SLACK_SIGNING_SECRET
        - RESEARCH_EMAIL_PROVIDER
        - RESEARCH_EMAIL_API_KEY
        - RESEARCH_EMAIL_FROM
        - RESEARCH_LINEAR_TOKEN
        - RESEARCH_LINEAR_TEAM_ID
        - RESEARCH_GITHUB_TOKEN
        - RESEARCH_GITHUB_REPO
      config:
        - continuous_user_research.integrations.notion.enabled
        - continuous_user_research.integrations.slack.enabled
        - continuous_user_research.integrations.email.enabled
        - continuous_user_research.integrations.linear.enabled
        - continuous_user_research.integrations.github.enabled
        - continuous_user_research.storage.multimedia_bucket
        - continuous_user_research.storage.multimedia_signed_url_ttl_minutes
        - continuous_user_research.retention.raw_days
        - continuous_user_research.retention.redacted_report_days
---
## 自动运行轻量级日记研究，并将其转化为每周产品信号及可实验的推荐建议

### 适用场景
- 团队需要决定开发、修复或优先处理哪些事项，并且需要基于长期行为数据来做出决策，而不仅仅是基于一次性的意见。
- 创始人或产品经理希望了解团队在特定时间范围内的学习情况（例如，新员工入职后的流失情况）。
- 需要将用户报告的内容与他们在不同时间点或接触点上的实际行为进行对比。
- 需要低成本的、可重复的日记研究流程，且该流程应服务于一个明确的研究目标。
- 需要每周产生可操作的成果，并制定相应的实验计划。

### 不适用场景
- 仅需要了解广泛的品牌情绪反馈，而无需基于这些反馈做出产品决策。
- 团队需要的是具有统计代表性的市场规模数据，而非定性的用户行为分析。
- 研究内容涉及高风险或敏感领域（如医疗、法律、未成年人、政府相关），且没有专门的合规设计。
- 所需数据可以通过现有的遥测数据获得，无需额外的用户信息。
- 无法确保参与者的同意、数据存储的安全性或数据保护的完整性。

### 安全性与权限管理
- 最小化数据访问范围：仅访问参与者的联系信息、日记条目以及研究所需工具的权限。
- 默认情况下对所有分析结果进行脱敏处理：删除姓名、电子邮件、电话号码、账户ID、精确地址等直接标识信息。
- 将原始数据与分析报告分开存储：将未脱敏的原始条目存储在受限制的文件夹中，仅发布经过脱敏处理的报告。
- 禁止将API密钥、令牌、凭证或隐藏配置信息泄露到任何提示、报告或工单中。
- 避免不必要的文件系统或shell操作：优先使用基于API的工具（如Slack、Email、Notion、Linear、GitHub API）。

### 安全与权限相关配置
- `RESEARCH_STUDY_STORAGE_RAW_PATH`：用于存储原始条目的受限制位置。
- `RESEARCH_STUDY_STORAGE_REPORTS_PATH`：用于存储脱敏后的报告文件的位置。
- `RESEARCH_REDACTION_SALT`：用于数据脱敏的随机盐值。
- `RESEARCH_NOTION_TOKEN`：仅用于目标研究数据库的集成令牌。
- `RESEARCH_NOTION_DATABASE_ID`：用于存储参与者、条目和报告的数据库ID。
- `RESEARCH_SLACK_BOT_TOKEN`：仅用于研究工作空间/频道的机器人令牌。
- `RESEARCH_SLACK_SIGNING_SECRET`：用于Webhook签名验证的密钥。
- `RESEARCH_EMAIL_PROVIDER`：用于发送邮件的服务提供商ID。
- `RESEARCH_EMAIL_API_KEY`：仅用于指定发送者的API密钥。
- `RESEARCH_EMAIL_FROM`：允许发送报告的发送者地址。

### 支持的研究类型
- 创始人/产品经理请求：跟踪本周新员工的流失情况，并提供改进建议。
- 用于了解用户使用特定功能的频率或习惯。
- 用于探究用户选择或避免某些任务的原因及其随时间的变化。
- 用于分析用户从研究到购买过程中的行为变化及遇到的障碍。
- 用于比较不同渠道、设备或情境下的用户行为。

### 规则
- 仅以主要的研究目标作为研究的范围依据。
- 保持方法的灵活性，以便一次研究可以涵盖上述所有类型的研究。

### 日记研究流程
#### A) 计划阶段
1. 明确研究目的和目标。
2. 提出3-7个与研究目标相关的问题。
3. 选择研究类型：
  - `broad_behavior`：广泛的行为分析。
  - `targeted_product`：特定产品功能或使用流程。
  - `targeted_activity`：单一行为或任务。
  - `journey`：多阶段的用户行为追踪。
4. 选择数据收集模式：
  - `signal`：适用于轻度研究。
  - `event`：适用于罕见或高价值的行为事件。
  - `interval`：适用于高频行为。
  - `mixed`：当单一模式无法满足需求时使用。
5. 根据预期事件频率设定研究时长：
  - 高频行为：5-10天。
  - 中频行为：10-14天。
  - 罕见事件：14-28天。
6. 选择数据收集工具（如Notion、Airtable、Google Sheets）和存储位置。
7. 定义参与者信息及分类标签。
8. 设定样本数量、超额招募比例、激励措施、最低条目数量和最大条目上限。
9. 完善模板和后续处理规则。
10. 进行内部测试（24小时）。

#### B) 招募与同意收集阶段
1. 从CSV或JSON文件中导入潜在参与者信息。
2. 根据参与者信息进行筛选和分类。
3. 适当超额招募以防止参与者中途退出。
4. 发送包含参与规则的同意模板。
5. 仅在获得明确同意后激活参与者的账户。

#### C) 研究前准备
1. 进行简短的入职培训或发送相应的书面材料。
2. 说明报告内容、提交频率及预期提交时间。
3. 说明激励措施和奖励要求。
4. 分享优秀的提交示例和不佳的提交案例。
5. 确认参与者的时区及偏好的提交时间。

#### D) 数据收集与监控阶段
1. 按预定时间发送数据收集提示。
2. 每日跟踪参与者的参与情况（是否发送提示、是否完成、是否错过提交机会、是否使用替代方案）。
3. 对错过提交机会的参与者发送提醒。
4. 如果参与者错过提交机会，发送简化版的提示后再进行提醒。
5. 对于中途退出的参与者，发送帮助信息并简化重新参与的流程。

#### E) 可选的后续访谈
1. 与部分参与者进行20-30分钟的访谈。
2. 验证最突出的研究结果，探讨矛盾点。
3. 调查异常行为和未解决的问题。
4. 保持访谈问题的中立性，并基于实际数据进行分析。

#### F) 数据分析阶段
1. 重新审视原始研究问题和研究目的。
2. 按主题、阶段、触发因素和情感对条目进行分类。
3. 分析行为变化及关键影响因素。
4. 对于用户行为追踪研究，绘制用户行为路径、转换点及放弃节点。
5. 在最终提出建议前，确保建议有数据支持。

### 时间模式选择指南
- 如果某种行为虽然罕见但价值很高（例如，激活失败或结账放弃），选择`event`模式。
- 如果某种行为频繁且规律性高（例如，每日使用习惯），选择`interval`模式。
- 如果需要定期收集数据（例如，每周一次），选择`signal`模式。
- 如果需要同时收集基线数据和特定事件数据，选择`mixed`模式。

#### 模式使用建议
- `event`模式：在目标事件发生后立即发送提示，并要求提供简短的背景信息。
- 适用于低频但信息量大的情况。
- `interval`模式：按照固定频率（每日或每隔X天）发送提示。
- `signal`模式（默认）：在预定的时间点发送提示，适用于低摩擦的每周研究循环。
- `mixed`模式：结合`interval`模式和`event`模式，适用于入职流程或行为不规律的情况。

#### 样本量和超额招募规则
- 根据研究类型确定样本数量：
  - 针对特定问题的研究：8-12名参与者。
  - 比较不同组别的研究：12-20名参与者。
  - 多阶段行为追踪研究：15-24名参与者。
- 行为变化较大的研究：20-30名参与者。

#### 激励与奖励机制
- 奖励基于参与者的参与质量和完成质量，而非提交的消息数量。
- 设定完成报告的最低条目数量要求。
- 限制每条记录的奖励数量，以防止滥用奖励机制。

#### 试点测试
- 在正式招募前进行试点测试，持续24小时，由1-2名内部测试者参与。
- 测试内容包括：条目的完成时间（平均5-10分钟）、问题是否清晰、是否需要协助等。
- 确保所有条目都符合质量要求。

#### 合规性监控
- 每日跟踪参与者的参与情况：发送的提示数量、完成的条目数量、错过的条目数量、发送的提醒数量等。

#### 可选的后续访谈
- 仅在以下情况下进行访谈：
  - 周报中存在未解决的矛盾点。
  - 行为变化需要因果解释。
  - 用户行为路径不明确。

#### 分析与报告格式
- 在报告中注明数据来源（“debrief”或“diary”）。
- 使用统一的分析模板和标签系统。
- 提供详细的分析步骤和结果来源说明。

#### 沟通模板
- 使用`prompts`目录中的模板：
  - 同意收集：`prompts/consent_message.md`
  - 入职培训材料：`prompts/pre_study_brief.md`
  - 日记条目模板：`prompts/entry_templates.md`
  - 后续跟进规则：`prompts/followup_rules.md`
  - 面谈指南：`prompts/post_study_interview_guide.md`

#### 示例研究简报
- 示例1：新员工入职流失情况研究
- 示例2：特定功能的使用频率研究
- 示例3：多阶段用户行为追踪研究
- 示例4：入职流失情况周报（1页格式）
- 示例5：特定功能的使用频率周报
- 示例6：用户行为路径追踪周报
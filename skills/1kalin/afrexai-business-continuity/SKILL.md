# 业务连续性规划工具

本工具可帮助任何组织制定完整的业务连续性计划（Business Continuity Plan, BCP）和灾难恢复（Disaster Recovery, DR）策略。

## 功能概述
- 映射关键业务功能及其相互依赖关系
- 为各项业务功能设定恢复时间目标（Recovery Time Objective, RTO）和恢复点目标（Recovery Point Objective, RPO）
- 建立沟通渠道和故障升级流程
- 生成可供利益相关者审核的正式BCP文档
- 在故障发生前识别潜在的薄弱环节

## 使用方法
向工具提供您的业务相关信息，它将指导您完成BCP的制定过程：

```
"Create a business continuity plan for our 40-person SaaS company"
"We need a disaster recovery plan — our main systems are AWS-hosted"
"Map our critical functions and set RTOs for each"
```

## 制定流程

### 1. 业务影响分析
请用户提供以下信息：
- 产生核心收入的功能
- 面向客户的系统
- 内部运营流程（如薪资发放、通信系统、数据管理）
- 关键供应商及第三方依赖关系

针对每项功能，评估以下内容：
- **停机带来的影响**（每小时收入损失、合同罚款、声誉损害）
- **RTO**：需要多快恢复（分钟、小时、天）
- **RPO**：可接受的数据丢失量

### 2. 风险评估
从以下类别识别潜在风险：
- **技术风险**：服务器故障、网络攻击、数据损坏、云服务中断
- **人员风险**：关键人员缺失、技能缺口
- **设施风险**：办公场所访问限制、电力供应问题、网络连接问题
- **供应链风险**：供应商故障、支付中断
- **外部风险**：法规变更、自然灾害、疫情

使用以下公式计算风险评分：风险概率（1-5）× 风险影响（1-5）

### 3. 恢复策略制定
为每项关键功能确定以下内容：
- 主要恢复方法
- 备份/替代方案
- 在系统故障时的手动应对措施
- 负责人及备用联系人
- 需要优先恢复的依赖关系

### 4. 沟通计划
建立沟通体系：
- 危机管理团队信息（成员姓名、职责、联系方式）
- 危机触发条件
- 内部通知流程
- 与外部利益相关者的沟通方式（客户、供应商、监管机构）
- 媒体/公关应对模板

### 5. BCP文档生成
生成结构化的BCP文档，内容包括：

```markdown
# Business Continuity Plan — [Company Name]
## Version: 1.0 | Last Updated: [Date] | Next Review: [Date + 6 months]

### 1. Purpose & Scope
### 2. Business Impact Analysis (table)
### 3. Risk Register (table with scores)
### 4. Recovery Strategies (per function)
### 5. Communication Plan & Contact Tree
### 6. IT Disaster Recovery Procedures
### 7. Testing Schedule (tabletop exercises quarterly, full test annually)
### 8. Document Control & Review Cycle
```

### 6. 测试与维护
建议定期进行以下操作：
- **桌面演练**：每季度通过口头模拟演练来检验计划的有效性
- **模拟测试**：每半年实际执行恢复流程
- **全面灾难恢复测试**：每年进行一次，将系统切换至备份系统
- **定期审查**：在发生实际事件、组织结构变更或新系统部署后及时更新BCP

## 输出格式
BCP将以Markdown格式的文档形式提供，用户可将其保存、打印或转换为PDF格式。文档中会包含业务影响分析和风险登记表的表格。

## 使用提示：
- 优先关注能够产生收入的核心业务功能，其他方面可稍后处理。
- 仅存在于纸面上的计划毫无实际意义；未经测试的计划根本算不上真正的预案。
- 造成长时间系统故障的常见原因并非技术故障，而是不知道该联系谁来处理问题。
- 保持计划的实用性——一份易于阅读的5页文档比一份无人查阅的50页文档更有价值。
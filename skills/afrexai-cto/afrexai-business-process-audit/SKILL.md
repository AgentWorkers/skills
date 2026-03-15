# 业务流程审计

识别企业中可自动化的机会。分析工作流程，估算节省的时间，并根据投资回报率（ROI）确定优先自动化哪些流程。

## 使用场景
- 评估哪些业务流程适合自动化
- 为AI代理的部署制定商业案例
- 识别造成成本浪费的瓶颈和手动操作
- 规划数字化转型或运营优化

## 工作原理

首先了解用户的具体业务情况（或根据上下文推断）。然后从以下8个类别进行分析：

### 1. 沟通与电子邮件（占工作周的28%）
- 电子邮件分类与回复
- 会议安排与跟进
- 内部通知与更新
- 客户沟通流程

### 2. 数据录入与处理（占工作周的19%）
- 发票处理与应付账款/应收账款管理
- 客户关系管理（CRM）数据录入与更新
- 报告生成
- 表单处理

### 3. 客户运营（占工作周的15%）
- 潜在客户筛选与分配
- 新员工入职流程
- 支持工单分类与处理
- 续订与追加销售机会的识别

### 4. 文档管理（占工作周的12%）
- 合同审核与提取
- 合规性文档处理
- 文件归档与整理
- 版本控制与审批

### 5. 财务运营（占工作周的10%）
- 费用分类
- 对账
- 预测数据准备
- 开票与收款

### 6. 人力资源与人员运营（占工作周的8%）
- 简历筛选
- 新员工入职检查清单
- 休假管理
- 绩效评估准备

### 7. 销售与市场营销（占工作周的5%）
- 潜在客户信息收集与优化
- 内容发布计划
- 销售流程监控
- 竞争对手分析

### 8. IT与安全（占工作周的3%）
- 权限管理
- 监控与警报系统
- 备份验证
- 合规性检查

## 输出格式

生成一份结构化的审计报告：

```
# Business Process Audit Report
## Company: [Name]
## Industry: [Industry]
## Team Size: [N employees]

### Executive Summary
- Total estimated hours wasted on manual work: X hrs/week
- Potential annual savings: $X
- Top 3 automation priorities (by ROI)

### Process Analysis

For each of the 8 categories:
| Process | Current State | Hours/Week | Automation Potential | Est. Savings | Priority |
|---------|--------------|------------|---------------------|-------------|----------|

Priority scoring: (hours × hourly_cost × automation_percentage) / implementation_effort

### Recommended Automation Roadmap
#### Phase 1 (Week 1-2): Quick wins — processes with >80% automation potential
#### Phase 2 (Month 1): Medium complexity — integration-dependent processes  
#### Phase 3 (Quarter 1): Complex workflows — multi-system orchestration

### ROI Summary
- Implementation cost estimate: $X
- Monthly savings estimate: $X/mo
- Payback period: X months
- 12-month net ROI: X%
```

## 计算假设
- 美国知识工作者的平均年薪：75,000美元（满负荷工作时间为每小时36美元）
- 平均工作周时长：40小时
- 自动化通常能节省60-85%的手动任务时间
- 实施周期：根据复杂程度不同，为1-4周

## 提示
- 必须针对具体业务进行审计——泛化的审计报告毫无价值
- 询问用户当前使用的技术栈（他们已有的工具）
- 重点关注重复性高、基于规则且处理量大的流程
- 既要考虑节省的时间，也要考虑减少的错误数量
- 必须以美元为单位进行量化，而不仅仅是小时数
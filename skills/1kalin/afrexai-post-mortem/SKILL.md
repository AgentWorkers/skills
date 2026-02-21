# 事故分析与回顾框架

通过结构化的事故分析来防止类似问题的再次发生。采用无责备的分析方式，明确根本原因，并跟踪相应的改进措施。

## 使用场景
- 发生任何生产故障、服务中断或服务质量下降时
- 未能按时完成任务、项目启动失败或失去业务机会时
- 任何造成超过5000美元损失或团队工作时间超过4小时的事件发生后
- 每季度对重复性事故模式进行回顾时

## 事故分析模板

### 1. 事故概述（需在24小时内完成）
```
Incident ID: [AUTO-GENERATED]
Date/Time: [Start] → [End] (Duration: X hours)
Severity: SEV-1 (revenue impact) | SEV-2 (customer impact) | SEV-3 (internal impact)
Impact: [Users affected] | [Revenue lost] | [SLA breached Y/N]
Detection: How was it found? (Monitoring / Customer report / Internal discovery)
Detection Delay: Time from incident start → first alert
```

### 2. 事件时间线（SEV-1事件为逐分钟记录，SEV-2/3事件为15分钟记录）
```
HH:MM - Event description
HH:MM - First alert triggered
HH:MM - Team notified
HH:MM - Investigation started
HH:MM - Root cause identified
HH:MM - Fix deployed
HH:MM - Confirmed resolved
```

### 3. 根本原因分析（“5个为什么”）
```
Why 1: [Direct cause]
Why 2: [Why did that happen?]
Why 3: [Why did THAT happen?]
Why 4: [Systemic cause]
Why 5: [Organizational/cultural root]
```

### 4. 影响因素
对每个因素评分0-3分（0=无关因素，3=主要影响因素）：

| 影响因素 | 评分 | 备注 |
|---|---|---|
| 监控缺失/不足 | | |
| 测试不充分 | | |
| 文档缺失 | | |
- 未遵循流程 | | |
- 人员能力不足 | | |
- 容量/扩展限制 | | |
- 依赖第三方服务 | | |
- 沟通不畅 | | |
- 变更管理失败 | | |
- 技术债务（长期存在的问题） | | |

### 5. 成功之处
列出在应对过程中表现良好的3-5个方面：
- 是否能够快速发现问题？是否使用了有效的操作手册？沟通是否顺畅？是否及时上报了问题？

### 6. 改进措施
每项改进措施都应指定负责人和完成期限：

| 编号 | 改进措施 | 负责人 | 完成期限 | 优先级 | 状态 |
|---|---|---|---|---|---|
| 1 | | | | P0/P1/P2 | 进行中 |

**优先级说明：**
- P0：必须在下一个工作日之前完成
- P1：必须在1周内完成
- P2：必须在1个开发周期/1个月内完成

### 7. 防止类似事故再次发生
- [ ] 为该故障模式增加/改进监控机制
- [ ] 创建/更新操作手册
- [ ] 增加测试覆盖范围
- [ ] 是否需要调整系统架构？（如需，需编写需求文档）
- [ ] 团队是否需要培训？

## 无责备事故分析原则
1. 重点关注系统问题，而非个人责任
2. 重点分析“发生了什么”，而非“谁造成的”
3. 假设每个人都是出于好意并已利用了可用信息
4. 目的是学习，而非惩罚
5. 如果发现某人的名字与错误相关联，请将其归类为流程上的缺陷

## 事故成本计算器
```
Direct costs:
  Revenue lost during downtime: $___
  SLA credits issued: $___
  Emergency vendor/contractor costs: $___

Indirect costs:
  Engineering hours × loaded rate: ___ hrs × $___/hr = $___
  Customer churn risk (affected users × churn probability × LTV): $___
  Brand/reputation (estimate): $___

Total incident cost: $___
Cost per minute of downtime: $___
```

## 每季度的事故回顾
每季度对所有事故分析结果进行汇总，重点关注以下方面：
1. **三大主要根本原因**——应在哪些方面加强预防措施？
2. **平均发现时间（MTTD）**——监控机制是否有所改进？
3. **平均解决时间（MTTR）**——响应速度是否加快？
4. **改进措施的完成率**——是否真正解决了问题？
5. **重复性事故**——如果同一根本原因多次出现，说明存在系统性问题
6. **成本趋势**——每季度的事故总成本是否下降？

## 不同行业的特殊要求
| 行业 | 关键关注点 | 监管要求 |
|---|---|---|
| 金融科技 | 交易完整性、审计追踪 | SOX、PCI-DSS事故报告 |
| 医疗保健 | 患者信息保护 | HIPAA违规通知（60天内） |
| SaaS服务 | 服务水平协议（SLA）合规性、数据完整性 | SOC 2事故管理 |
| 电子商务 | 订单完整性、支付处理 | PCI-DSS、消费者保护 |
| 制造业 | 安全事故、生产损失 | OSHA报告要求 |

---

## 深入分析
通过事故分析，可以确定哪些地方需要优先部署人工智能（AI）解决方案：
- 需要重点关注的问题包括：重复性故障、手动监控的薄弱环节以及在高负载下容易出问题的流程。
- **计算您的最大成本漏洞**：[AI成本漏洞计算器](https://afrexai-cto.github.io/ai-revenue-calculator/)
- **针对不同行业的解决方案包**：[AfrexAI定制解决方案包](https://afrexai-cto.github.io/context-packs/)  
  - 选择3项：97美元  
  - 选择全部10项：197美元  
  - 全部解决方案：247美元  
- **部署您的第一个AI代理**：[代理设置向导](https://afrexai-cto.github.io/agent-setup/)  

*由[AfrexAI](https://afrexai-cto.github.io/context-packs/)提供——将事故分析结果转化为自动化改进的机会。*
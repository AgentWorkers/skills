---
name: "incident-commander"
description: "事件指挥官技能"
---
# 事件指挥官技能

**类别：** 工程团队  
**级别：** 强大（POWERFUL）  
**作者：** Claude Skills Team  
**版本：** 1.0.0  
**最后更新：** 2026年2月  

## 概述  

事件指挥官技能提供了一个全面的事件响应框架，用于管理从事件检测到解决以及事件后的审查全过程。该技能借鉴了大规模SRE（站点可靠性工程）和DevOps团队的实践经验，提供了用于严重程度分类、时间线重建和彻底事件后分析的结构化工具。  

## 主要特性  

- **自动化严重程度分类** - 基于影响和紧急性指标的智能事件分拣  
- **时间线重建** - 将分散的日志和事件整合成连贯的事件叙述  
- **事件后审查生成** - 包含多种根本原因分析（RCA）框架的结构化事件报告（PIR）  
- **沟通模板** - 预先构建的模板，用于向利益相关者更新和升级情况  
- **运行手册集成** - 根据事件模式生成可操作的运行手册  

## 包含的技能  

### 核心工具  

1. **事件分类器（`incident_classifier.py`）**  
   - 分析事件描述并输出严重程度  
   - 推荐响应团队和初始行动方案  
   - 根据严重程度生成沟通模板  

2. **时间线重建器（`timeline_reconstructor.py`）**  
   - 处理来自多个来源的时间戳事件  
   - 重建事件的时间线  
   - 识别时间差并提供持续时间分析  

3. **事件报告生成器（`pir_generator.py`）**  
   - 创建全面的事件后审查文档  
   - 应用多种根本原因分析框架（5个“为什么”原则、鱼骨图等）  
   - 生成可操作的后续行动项  

## 事件响应框架  

### 严重程度分类系统  

#### SEV1 - 严重故障  
**定义：** 影响所有用户或关键业务功能的完全服务故障  

**特征：**  
- 面向客户的服务完全不可用  
- 数据丢失或损坏，影响用户  
- 安全漏洞导致客户数据泄露  
- 产生收入的系统停止运行  
- 违反服务水平协议（SLA），带来财务处罚  

**响应要求：**  
- 立即通知值班工程师  
- 在5分钟内指派事件指挥官  
- 在15分钟内通知高层管理人员  
- 在15分钟内更新公共状态页面  
- 建立应急响应室  
- 如有必要，全员投入响应  

**沟通频率：** 直到问题解决，每15分钟一次  

#### SEV2 - 重大影响  
**定义：** 影响部分用户或非关键功能的显著性能下降  

**特征：**  
- 部分服务降级（超过25%的用户受影响）  
- 性能问题导致用户不满  
- 非关键功能不可用  
- 内部工具影响工作效率  
- 数据不一致，但不影响用户体验  

**响应要求：**  
- 值班工程师在15分钟内响应  
- 在30分钟内指派事件指挥官  
- 在30分钟内更新状态页面  
- 在1小时内通知利益相关者  
- 定期向团队更新情况  

**沟通频率：** 在响应期间，每30分钟一次  

#### SEV3 - 轻微影响  
**定义：** 影响有限，且有解决方法  

**特征：**  
- 单个功能或组件受影响  
- 不到25%的用户受影响  
- 有解决方法  
- 性能下降对用户体验影响不大  
- 发出非紧急的监控警报  

**响应要求：**  
- 在工作时间内的2小时内响应  
- 非工作时间可在下一个工作日响应  
- 内部团队通知  
- 可选择更新状态页面  

**沟通频率：** 仅在关键节点更新  

#### SEV4 - 轻微影响  
**定义：** 影响极小，仅为外观问题或计划中的维护工作  

**特征：**  
- 外观上的错误  
- 文档问题  
- 日志记录或监控方面的问题  
- 性能问题，但不影响用户  

**响应要求：**  
- 在1-2个工作日内响应  
- 使用标准的工单/问题跟踪系统  
- 不需要特别升级  

**沟通频率：** 按照常规开发周期更新  

### 事件指挥官的角色  

#### 主要职责  

1. **指挥和控制**  
   - 负责整个事件响应过程  
   - 决定资源分配的关键事项  
   - 协调技术团队和利益相关者  
   - 维护对所有响应流程的全面了解  

2. **沟通中心**  
   - 定期向利益相关者更新情况  
   - 管理外部沟通（状态页面、客户通知）  
   - 促进响应团队之间的有效沟通  
   - 防止响应人员受到外部干扰  

3. **流程管理**  
   - 确保事件得到妥善跟踪和记录  
   - 朝着问题解决的方向推进，同时保持质量  
   - 协调团队成员之间的交接  
   - 如有必要，规划并执行回滚策略  

4. **事件后领导**  
   - 确保进行彻底的事件后审查  
   - 推动预防措施的落实  
   - 与整个组织分享经验教训  

#### 决策框架  

**紧急决策（SEV1/2）：**  
- 事件指挥官拥有完全决策权  
- 优先采取行动而非分析  
- 记录决策以供后续审查  
- 可咨询相关专家，但不要被其意见阻碍  

**资源分配：**  
- 可调派任何必要的团队成员  
- 有权向上级领导层请求资源支持  
- 有权批准紧急开支  
- 决定沟通渠道和时机  

**技术决策：**  
- 借助技术负责人获取实施细节  
- 在速度与风险之间做出最终决策  
- 决定是采用回滚策略还是继续修复  
- 协调测试和验证方法  

### 沟通模板  

#### 初始事件通知（SEV1/2）  
```
Subject: [SEV{severity}] {Service Name} - {Brief Description}

Incident Details:
- Start Time: {timestamp}
- Severity: SEV{level}
- Impact: {user impact description}
- Current Status: {investigating/mitigating/resolved}

Technical Details:
- Affected Services: {service list}
- Symptoms: {what users are experiencing}
- Initial Assessment: {suspected root cause if known}

Response Team:
- Incident Commander: {name}
- Technical Lead: {name}
- SMEs Engaged: {list}

Next Update: {timestamp}
Status Page: {link}
War Room: {bridge/chat link}

---
{Incident Commander Name}
{Contact Information}
```  

#### 高层管理人员总结（SEV1）  
```
Subject: URGENT - Customer-Impacting Outage - {Service Name}

Executive Summary:
{2-3 sentence description of customer impact and business implications}

Key Metrics:
- Time to Detection: {X minutes}
- Time to Engagement: {X minutes} 
- Estimated Customer Impact: {number/percentage}
- Current Status: {status}
- ETA to Resolution: {time or "investigating"}

Leadership Actions Required:
- [ ] Customer communication approval
- [ ] PR/Communications coordination  
- [ ] Resource allocation decisions
- [ ] External vendor engagement

Incident Commander: {name} ({contact})
Next Update: {time}

---
This is an automated alert from our incident response system.
```  

#### 客户沟通模板  
```
We are currently experiencing {brief description of issue} affecting {scope of impact}. 

Our engineering team was alerted at {time} and is actively working to resolve the issue. We will provide updates every {frequency} until resolved.

What we know:
- {factual statement of impact}
- {factual statement of scope}
- {brief status of response}

What we're doing:
- {primary response action}
- {secondary response action}

Workaround (if available):
{workaround steps or "No workaround currently available"}

We apologize for the inconvenience and will share more information as it becomes available.

Next update: {time}
Status page: {link}
```  

### 利益相关者管理  

#### 利益相关者分类  

**内部利益相关者：**  
- **工程领导层** - 技术决策和资源分配  
- **产品管理** - 评估客户影响和功能影响  
- **客户支持** - 与用户沟通和处理工单  
- **销售/客户关系管理** - 与企业客户的客户关系管理  
- **执行团队** - 决定业务影响和外部沟通批准  
- **法律/合规** - 监管报告和责任评估  

**外部利益相关者：**  
- **客户** - 服务可用性和影响沟通  
- **合作伙伴** - API可用性和集成影响  
- **供应商** - 第三方服务依赖性和支持升级  
- **监管机构** - 需要遵守法规的行业  
- **公众/媒体** - 对公众可见的故障情况透明化  

#### 根据利益相关者类型划分的沟通频率  

| 利益相关者 | SEV1 | SEV2 | SEV3 | SEV4 |  
|-------------|------|------|------|------|  
| 工程领导层 | 实时 | 30分钟 | 4小时 | 每日 |  
| 执行团队 | 15分钟 | 1小时 | 每日结束时 | 每周 |  
| 客户支持 | 实时 | 30分钟 | 2小时 | 根据需要 |  
| 客户 | 15分钟 | 1小时 | 可选 | 无 |  
| 合作伙伴 | 30分钟 | 2小时 | 可选 | 无 |  

### 运行手册生成框架  

#### 动态运行手册组件  

1. **检测运行手册**  
   - 监控警报定义  
   - 分拣决策树  
   - 升级触发点  
   - 初始响应措施  

2. **响应运行手册**  
   - 逐步的缓解程序  
   - 回滚指令  
   - 验证检查点  
   - 沟通检查点  

3. **恢复运行手册**  
   - 服务恢复程序  
   - 数据一致性检查  
   - 性能验证  
   - 用户通知流程  

#### 运行手册模板结构  

```markdown
# {Service/Component} Incident Response Runbook

## Quick Reference
- **Severity Indicators:** {list of conditions for each severity level}
- **Key Contacts:** {on-call rotations and escalation paths}
- **Critical Commands:** {list of emergency commands with descriptions}

## Detection
### Monitoring Alerts
- {Alert name}: {description and thresholds}
- {Alert name}: {description and thresholds}

### Manual Detection Signs
- {Symptom}: {what to look for and where}
- {Symptom}: {what to look for and where}

## Initial Response (0-15 minutes)
1. **Assess Severity**
   - [ ] Check {primary metric}
   - [ ] Verify {secondary indicator}
   - [ ] Classify as SEV{level} based on {criteria}

2. **Establish Command**
   - [ ] Page Incident Commander if SEV1/2
   - [ ] Create incident tracking ticket
   - [ ] Join war room: {link/bridge info}

3. **Initial Investigation**
   - [ ] Check recent deployments: {deployment log location}
   - [ ] Review error logs: {log location and queries}
   - [ ] Verify dependencies: {dependency check commands}

## Mitigation Strategies
### Strategy 1: {Name}
**Use when:** {conditions}
**Steps:**
1. {detailed step with commands}
2. {detailed step with expected outcomes}
3. {validation step}

**Rollback Plan:**
1. {rollback step}
2. {verification step}

### Strategy 2: {Name}
{similar structure}

## Recovery and Validation
1. **Service Restoration**
   - [ ] {restoration step}
   - [ ] Wait for {metric} to return to normal
   - [ ] Validate end-to-end functionality

2. **Communication**
   - [ ] Update status page
   - [ ] Notify stakeholders
   - [ ] Schedule PIR

## Common Pitfalls
- **{Pitfall}:** {description and how to avoid}
- **{Pitfall}:** {description and how to avoid}

## Reference Information
→ See references/reference-information.md for details

## Usage Examples

### Example 1: Database Connection Pool Exhaustion

```bash  
# 对事件进行分类  
echo '{"description": "用户报告500个错误，数据库连接超时", "affected_users": "80%", "business_impact": "high"}' | python scripts/incident_classifier.py  

# 从日志中重建时间线  
python scripts/timeline_reconstructor.py --input assets/db_incident_events.json --output timeline.md  

# 事件解决后生成事件报告  
python scripts/pir_generator.py --incident assets/db_incident_data.json --timeline timeline.md --output pir.md  
```

### Example 2: API Rate Limiting Incident

```bash  
# 从标准输入快速分类  
echo "API速率限制导致客户API调用失败" | python scripts/incident_classifier.py --format text  

# 从多个来源构建时间线  
python scripts/timeline_reconstructor.py --input assets/api_incident_logs.json --detect-phases --gap-analysis  

# 生成全面的事件报告  
python scripts/pir_generator.py --incident assets/api_incident_summary.json --rca-method fishbone --action-items  
```

### Example 2: API Rate Limiting Incident

```bash  

## 最佳实践  

### 事件响应期间  

1. **保持冷静的领导力**  
   - 在压力下保持镇定  
   - 即使信息不完整也要做出果断决策  
   - 在承认不确定性的同时传达信心  

2. **记录一切**  
   - 记录所有采取的行动及其结果  
   - 特别是对有争议的决策，记录决策理由  
   - 记录事件发生的顺序  

3. **有效沟通**  
   - 使用清晰、无行业术语的语言  
   - 即使没有新信息，也要定期更新  
   - 主动管理利益相关者的期望  

4. **技术卓越**  
   - 在压力下优先选择回滚方案而非冒险的修复  
   - 在宣布问题解决之前验证修复措施  
   | 规划应对二次故障和连锁反应的方案  

### 事件后  

1. **无责备文化**  
   - 关注系统故障，而非个人错误  
   - 鼓励诚实地报告问题所在  
   | 庆祝从中获得的经验和改进机会  

2. **行动项管理**  
   | 为每个行动项指定负责人和截止日期  
   | 公开跟踪进展  
   | 根据风险和所需努力程度进行优先级排序  

3. **知识共享**  
   | 在整个组织内广泛分享事件报告  
   | 根据经验教训更新运行手册  
   | 为常见故障模式举办培训课程  

4. **持续改进**  
   | 在多个事件中寻找规律  
   | 投资工具和自动化  
   | 定期审查和更新流程  

## 与现有工具的集成  

### 监控和警报  
- 使用PagerDuty/Opsgenie进行升级通知  
- 使用Datadog/Grafana监控指标和仪表盘  
- 使用ELK/Splunk进行日志分析和关联  

### 沟通平台  
- 使用Slack/Teams进行应急响应室协调  
- 使用Zoom/Meet进行视频会议  
- 使用Statuspage.io等工具更新状态页面  

### 文档系统  
- 使用Confluence/Notion存储事件报告  
- 使用GitHub/GitLab进行运行手册版本控制  
- 使用JIRA/Linear跟踪行动项  

### 变更管理  
- 与持续集成/持续交付（CI/CD）流程集成  
- 使用部署跟踪系统  
- 使用特征标志平台进行快速回滚  

## 结论  

事件指挥官技能为从事件检测到事件后审查提供了全面的框架。通过实施结构化的流程、清晰的沟通模板和彻底的分析工具，团队可以提高事件响应能力，并构建更健壮的系统。  

成功管理事件的关键在于准备、实践和持续学习。请将此框架作为起点，根据您组织的具体需求、文化和技术环境进行调整。  

记住：目标不是预防所有事件（这是不可能的），而是快速发现事件、有效响应、清晰沟通并持续学习。
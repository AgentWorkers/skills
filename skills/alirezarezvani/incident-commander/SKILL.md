# 事件指挥官技能

**类别：** 工程团队  
**等级：** 强大  
**作者：** Claude Skills Team  
**版本：** 1.0.0  
**最后更新：** 2026年2月  

## 概述  

事件指挥官技能提供了一个全面的事件响应框架，用于管理从事件检测到解决以及事件后的审查全过程。该技能借鉴了大规模SRE（站点可靠性工程）和DevOps团队的实践经验，提供了用于严重程度分类、时间线重建和彻底事件后分析的结构化工具。  

## 主要特性  

- **自动化严重程度分类** - 基于影响和紧急性指标的智能事件分拣  
- **时间线重建** - 将分散的日志和事件整合成连贯的事件叙述  
- **事件后审查生成** - 包含多种根本原因分析（RCA）框架的结构化事件后审查报告（PIR）  
- **沟通模板** - 预先构建的模板，用于向相关方更新情况和进行升级通知  
- **运行手册集成** - 根据事件模式生成可操作的运行手册  

## 包含的技能  

### 核心工具  

1. **事件分类器（`incident_classifier.py`）**  
   - 分析事件描述并输出严重程度级别  
   - 推荐响应团队和初始行动方案  
   - 根据严重程度生成沟通模板  

2. **时间线重建器（`timeline_reconstructor.py`）**  
   - 处理来自多个来源的时间戳事件  
   - 重建事件的时间线  
   - 识别时间线中的空白并分析持续时间  

3. **事件后审查生成器（`pir_generator.py`）**  
   - 创建全面的事件后审查文档  
   - 应用多种根本原因分析框架（如5个“为什么”方法、鱼骨图等）  
   - 生成可操作的后续行动项  

## 事件响应框架  

### 严重程度分类系统  

#### SEV1 - 严重故障  
**定义：** 影响所有用户或关键业务功能的完全服务中断  

**特征：**  
- 面向客户的服务完全不可用  
- 数据丢失或损坏，影响用户  
- 安全漏洞导致客户数据泄露  
- 产生收入的系统停止运行  
- 违反服务水平协议（SLA），导致财务处罚  

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
- 部分服务性能下降（超过25%的用户受影响）  
- 性能问题导致用户不满  
- 非关键功能不可用  
- 内部工具影响工作效率  
- 数据不一致，但不影响用户体验  

**响应要求：**  
- 值班工程师在15分钟内响应  
- 在30分钟内指派事件指挥官  
- 在30分钟内更新状态页面  
- 在1小时内通知相关方  
- 定期向团队更新情况  

**沟通频率：** 在响应期间，每30分钟一次  

#### SEV3 - 轻微影响  
**定义：** 影响有限，有备用方案  

**特征：**  
- 单个功能或组件受影响  
- 不到25%的用户受影响  
- 有备用方案  
- 性能下降对用户体验影响不大  
- 非紧急的监控警报  

**响应要求：**  
- 在工作时间内的2小时内响应  
- 非工作时间可在下一个工作日响应  
- 内部团队通知  
- 可选择更新状态页面  

**沟通频率：** 仅在关键节点时更新  

#### SEV4 - 轻微影响  
**定义：** 影响极小，仅为外观问题或计划中的维护工作  

**特征：**  
- 外观上的错误  
- 文档问题  
- 日志记录或监控方面的疏漏  
- 性能问题，但不影响用户  

**响应要求：**  
- 在1-2个工作日内响应  
- 使用标准的工单/问题跟踪系统  
- 不需要特别升级  

**事件指挥官的角色**  

#### 主要职责  

1. **指挥与控制**  
   - 负责整个事件响应过程  
   - 关于资源分配做出关键决策  
   - 协调技术团队和相关方  
   - 维持对所有响应流程的全面了解  

2. **沟通枢纽**  
   - 定期向相关方更新情况  
   - 管理外部沟通（状态页面、客户通知）  
   - 促进响应团队之间的有效沟通  
   - 防止响应人员受到外部干扰  

3. **流程管理**  
   - 确保事件得到妥善跟踪和记录  
   - 朝着问题解决的方向推进，同时保持质量  
   - 协调团队成员之间的交接工作  
   - 如有必要，制定和执行回滚策略  

4. **事件后领导**  
   - 确保进行彻底的事件后审查  
   - 推动预防措施的落实  
   - 与整个组织分享经验教训  

#### 决策框架  

**紧急决策（SEV1/2）：**  
- 事件指挥官拥有完全决策权  
- 优先采取行动而非分析  
- 记录决策以供后续审查  
- 可咨询相关专家，但不受其阻碍  

**资源分配：**  
- 可调用任何必要的团队成员  
- 有权向高层领导请求资源支持  
- 有权批准紧急情况下的外部资源支出  
- 决定沟通渠道和时机  

**技术决策：**  
- 依赖技术负责人提供实施细节  
- 在速度与风险之间做出最终决策  
- 决定是采用回滚策略还是继续推进  
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

#### 高层总结（SEV1）  

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

### 相关方管理  

#### 相关方分类  

**内部相关方：**  
- **工程领导** - 技术决策和资源分配  
- **产品管理** - 评估客户影响和功能影响  
- **客户支持** - 与用户沟通和处理工单  
- **销售/客户关系管理** - 管理企业客户的关系  
- **执行团队** - 决定业务影响和外部沟通审批  
- **法律/合规** - 负责法规报告和责任评估  

**外部相关方：**  
- **客户** - 服务可用性和影响沟通  
- **合作伙伴** - API可用性和集成影响  
- **供应商** - 第三方服务依赖和支援升级  
- **监管机构** - 需要合规报告的行业  
- **公众/媒体** - 对公众可见的中断情况  

#### 按相关方分类的沟通频率  

| 相关方 | SEV1 | SEV2 | SEV3 | SEV4 |
|-------------|------|------|------|------|
| 工程领导 | 实时 | 30分钟 | 4小时 | 每日 |
| 执行团队 | 15分钟 | 1小时 | 每日结束 | 每周 |
| 客户支持 | 实时 | 30分钟 | 2小时 | 根据需要 |
| 客户 | 15分钟 | 1小时 | 可选 | 无 |
| 合作伙伴 | 30分钟 | 2小时 | 可选 | 无 |

### 运行手册生成框架  

#### 动态运行手册组件  

1. **检测运行手册**  
   - 监控警报定义  
   - 分拣决策树  
   - 升级触发点  
   - 初始响应行动  

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
- **Architecture Diagram:** {link}
- **Monitoring Dashboard:** {link}
- **Related Runbooks:** {links to dependent service runbooks}
```  

### 事件后审查（PIR）框架  

#### PIR时间线和负责人  

**时间线：**  
- **24小时：** 事件指挥官完成初步PIR草稿  
- **3个工作日：** 发布包含所有相关方意见的最终PIR  
- **1周：** 分配行动项并确定负责人和截止日期  
- **4周：** 审查行动项的进展  

**角色：**  
- **PIR负责人：** 事件指挥官（可委托撰写，但负责完成）  
- **技术贡献者：** 所有参与响应的工程师  
- **审查委员会：** 工程领导、受影响的产品团队  
- **行动项负责人：** 根据专业能力和能力分配  

#### 根本原因分析框架  

#### 1. 五问法（Five Whys Method）  

五问法通过反复提问“为什么”来深入探究根本原因：  

**应用示例：**  
- **问题：** 在高峰流量期间数据库变得无响应  
- **为什么1：** 为什么数据库会无响应？→ 连接池耗尽  
- **为什么2：** 为什么连接池耗尽？→ 应用程序创建的连接数量超出正常范围  
- **为什么3：** 为什么应用程序会创建更多连接？→ 新功能没有正确实现连接池管理  
- **为什么4：** 为什么代码审查没有发现这个问题？→ 缺乏自动检查连接池管理的机制  
- **为什么5：** 为什么代码审查没有发现这个问题？→ 没有自动检查连接池管理的机制  

**最佳实践：**  
- 至少问3次“为什么”，通常需要5次或更多次迭代  
- 重点关注流程故障，而非个人责任  
- 每个“为什么”都应指向可改进的系统环节  
- 考虑多个可能的根本原因，而不仅仅是单一的线性链条  

#### 2. 鱼骨图（Ishikawa Diagram）**  

系统性地分析多个潜在原因：  

**类别：**  
- **人员：** 培训、经验、沟通、交接  
- **流程：** 程序、变更管理、审查流程  
- **技术：** 架构、工具、监控、自动化  
- **环境：** 基础设施、依赖关系、外部因素  

**应用方法：**  
1. 在鱼骨图的“头部”清楚地陈述问题  
2. 对每个类别，头脑风暴潜在的促成因素  
3. 对每个因素，询问其背后的原因（子原因）  
4. 确定最有可能是根本原因的因素  
5. 用事件中的证据验证根本原因  

#### 3. 时间线分析**  

按时间顺序重建事件，以识别决策点和错失的机会：  

**时间线要素：**  
- **检测：** 问题首次出现的时间？  
- **通知：** 相关人员何时得到通知？  
- **响应：** 采取了哪些行动，效果如何？  
- **沟通：** 相关方何时得到更新？  
- **解决：** 最终是如何解决问题的？  

**分析问题：**  
- 哪里出现了延迟，原因是什么？  
- 如果有完美的信息，我们会做出哪些不同的决策？  
- 沟通在哪里出了问题？  
- 哪些自动化措施可以更快地检测或解决问题？  

#### 升级路径  

#### 技术升级  

**级别1：** 值班工程师  
- **职责：** 初始响应和常见问题的解决  
- **升级触发条件：** 问题在SLA时间内未解决  
- **时间范围：** 15分钟（SEV1），30分钟（SEV2）  

**级别2：** 高级工程师/团队负责人  
- **职责：** 需要更深入专业知识的复杂技术问题  
- **升级触发条件：** 第一级请求帮助或超时  
- **时间范围：** 30分钟（SEV1），1小时（SEV2）  

**级别3：** 工程经理/技术员**  
- **职责：** 跨团队协调和架构决策  
- **升级触发条件：** 问题涉及多个系统或团队  
- **时间范围：** 45分钟（SEV1），2小时（SEV2）  

**级别4：** 工程总监/技术总监（CTO）  
- **职责：** 资源分配和业务影响决策  
- **升级触发条件：** 中断时间较长或对业务有重大影响  
- **时间范围：** 1小时（SEV1），4小时（SEV2）  

#### 业务升级  

**客户影响评估：**  
- **高：** 收入损失、SLA违反、客户流失风险  
- **中：** 用户体验下降、支持工单量增加  
- **低：** 仅影响内部工具和开发工作  

**升级矩阵：**  

| 严重程度 | 持续时间 | 业务升级层级 |  
|----------|----------|-------------------|  
| SEV1 | 立即 | 工程副总裁（VP Engineering） |  
| SEV1 | 30分钟 | 技术总监（CTO）+ 客户成功副总裁（Customer Success VP） |  
| SEV1 | 1小时 | 首席执行官（CEO）+ 全体执行团队（Executive Team） |  
| SEV2 | 2小时 | 工程副总裁（VP Engineering） |  
| SEV3 | 1个工作日 | 工程经理（Engineering Manager） |  

### 状态页面管理  

#### 更新原则  

1. **透明度：** 提供事实信息，避免猜测  
2. **及时性：** 在承诺的时间内更新  
3. **清晰度：** 使用易于理解的语言，避免技术术语  
4. **完整性：** 包括影响范围、状态和下次更新时间  

#### 状态类别  

- **正常运行：** 所有系统正常运行  
- **性能下降：** 部分用户可能遇到延迟  
- **部分中断：** 部分功能不可用  
- **重大中断：** 大部分/所有服务不可用  
- **维护中：** 计划中的维护窗口  

#### 更新模板  

```
{Timestamp} - {Status Category}

{Brief description of current state}

Impact: {who is affected and how}
Cause: {root cause if known, "under investigation" if not}
Resolution: {what's being done to fix it}

Next update: {specific time}

We apologize for any inconvenience this may cause.
```  

### 行动项框架  

#### 行动项类别  

1. **立即修复**  
   - 事件期间发现的严重错误  
   - 暴露的安全漏洞  
   - 数据完整性问题  

2. **流程改进**  
   - 沟通漏洞  
   - 升级程序更新  
   - 运行手册的添加/更新  

3. **技术债务**  
   **架构改进**  
   **监控增强**  
   **自动化机会**  

4. **组织变更**  
   **团队结构调整**  
   **培训需求**  
   **工具/平台投资**  

#### 行动项模板  

```
**Title:** {Concise description of the action}
**Priority:** {Critical/High/Medium/Low}
**Category:** {Fix/Process/Technical/Organizational}
**Owner:** {Assigned person}
**Due Date:** {Specific date}
**Success Criteria:** {How will we know this is complete}
**Dependencies:** {What needs to happen first}
**Related PIRs:** {Links to other incidents this addresses}

**Description:**
{Detailed description of what needs to be done and why}

**Implementation Plan:**
1. {Step 1}
2. {Step 2}
3. {Validation step}

**Progress Updates:**
- {Date}: {Progress update}
- {Date}: {Progress update}
```  

## 使用示例  

### 示例1：数据库连接池耗尽  

```bash
# Classify the incident
echo '{"description": "Users reporting 500 errors, database connections timing out", "affected_users": "80%", "business_impact": "high"}' | python scripts/incident_classifier.py

# Reconstruct timeline from logs
python scripts/timeline_reconstructor.py --input assets/db_incident_events.json --output timeline.md

# Generate PIR after resolution
python scripts/pir_generator.py --incident assets/db_incident_data.json --timeline timeline.md --output pir.md
```  

### 示例2：API速率限制事件  

```bash
# Quick classification from stdin
echo "API rate limits causing customer API calls to fail" | python scripts/incident_classifier.py --format text

# Build timeline from multiple sources
python scripts/timeline_reconstructor.py --input assets/api_incident_logs.json --detect-phases --gap-analysis

# Generate comprehensive PIR
python scripts/pir_generator.py --incident assets/api_incident_summary.json --rca-method fishbone --action-items
```  

## 最佳实践  

### 事件响应期间  

1. **保持冷静的领导**  
   - 在压力下保持镇定  
   - 即使信息不完整也要做出果断决策  
   - 在承认不确定性的同时保持沟通的信心  

2. **记录一切**  
   - 所有采取的行动及其结果  
   - 决策的理由，尤其是有争议的决策  
   - 事件发生的实时时间线  

3. **有效沟通**  
   - 使用清晰、无术语的语言  
   - 即使没有新信息也要定期更新  
   - 主动管理相关方的期望  

4. **技术卓越**  
   **在压力下优先选择回滚方案而非冒险的修复**  
   - 在宣布问题解决前验证修复措施  
   **为可能的二次故障和连锁反应做好准备**  

### 事件后  

1. **无责备文化**  
   **关注系统故障，而非个人错误**  
   **鼓励诚实地报告问题**  
   **庆祝学习成果和改进机会**  

2. **行动项管理**  
   **分配具体的负责人和截止日期**  
   **公开跟踪进展**  
   **根据风险和难度优先处理行动项**  

3. **知识共享**  
   **在组织内广泛分享PIR**  
   **根据经验教训更新运行手册**  
   **针对常见故障模式进行培训**  

4. **持续改进**  
   **在多个事件中寻找规律**  
   **投资工具和自动化**  
   **定期审查和更新流程**  

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
- 使用Confluence/Notion存储PIR  
- 使用GitHub/GitLab管理运行手册版本  
- 使用JIRA/Linear跟踪行动项  

### 变更管理  
- 集成持续集成/持续部署（CI/CD）流程  
- 使用部署跟踪系统  
- 使用特征标志（feature flags）快速回滚  

## 结论  

事件指挥官技能提供了一个从事件检测到事件后审查的全面框架。通过实施结构化的流程、清晰的沟通模板和彻底的分析工具，团队可以提高事件响应能力，并构建更健壮的系统。  

成功管理事件的关键在于准备、实践和持续学习。将此框架作为起点，但要根据您组织的具体需求、文化和技术环境进行调整。  

记住：目标不是预防所有事件（这是不可能的），而是快速发现事件、有效响应、清晰沟通和持续学习。
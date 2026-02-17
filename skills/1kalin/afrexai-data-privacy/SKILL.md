# 数据隐私合规框架

本框架可生成涵盖 GDPR、CCPA/CPRA、LGPD、POPIA 和 PIPL 等法规的完整数据隐私保护方案，内容涵盖数据映射、数据泄露响应等 DPO（数据保护官）或合规团队所需的所有内容。

## 使用场景
- 建立或审计隐私保护方案
- 映射系统间的个人数据流动
- 准备应对监管机构的审计（如 ICO、CNIL、FTC）
- 制定数据保护影响评估（DPIA）
- 起草隐私政策、同意流程或数据主体权利（DSR）相关程序

## 生成内容

### 1. 数据清单与映射
```
For each system/process, document:
- Data Category: [identifiers | financial | health | biometric | behavioral | location]
- Lawful Basis: [consent | contract | legitimate interest | legal obligation | vital interest | public task]
- Data Subjects: [customers | employees | prospects | vendors | minors]
- Storage Location: [cloud provider + region]
- Retention Period: [specific timeframe + justification]
- Cross-Border Transfer: [mechanism: SCC | BCR | adequacy | derogation]
- Processor/Controller: [role + DPA status]
```

### 2. 隐私影响评估（DPIA）
在以下情况下需要进行 DPIA：
- 对公共区域进行系统化监控
- 大规模处理特殊类别的数据
- 使用自动化决策系统并产生法律后果
- 新技术的部署
- 在 Schrems II 法规实施后进行跨境数据传输

**风险评分矩阵：**
| 可能性 | 影响程度 | 风险等级 | 需要采取的措施 |
|-----------|--------|------------|-----------------|
| 高 | 高 | 严重 | 停止操作，并在继续前咨询数据保护机构（DPA） |
| 高 | 中等 | 高 | 实施额外的安全措施，并记录理由 |
| 中等 | 中等 | 中等 | 采用标准控制措施并加强监控 |
| 低 | 低 | 低 | 记录相关情况后继续操作 |

### 3. 数据主体权利（DSR）程序
| 权利 | GDPR | CCPA/CPRA | 时间限制 | 处理流程 |
|-------|------|-----------|----------|---------|
| 查阅权 | 第 15 条 | 第 1798.100 条 | 30 天（GDPR）/ 45 天（CCPA） | 验证身份 → 整理数据 → 安全传输 |
| 删除权 | 第 17 条 | 第 1798.105 条 | 30 天 / 45 天 | 验证 → 检查例外情况 → 在所有系统中删除数据 → 确认删除 |
| 数据迁移权 | 第 20 条 | 第 1798.100 条 | 30 天 / 45 天 | 以机器可读格式（JSON/CSV）导出数据 |
| 更正权 | 第 16 条 | 第 1798.106 条 | 30 天 / 45 天 | 验证身份 → 更新记录 → 通知数据处理方 |
| 退出销售权 | 无 | 第 1798.120 条 | 15 个工作日 | 提供“禁止销售”链接 → 停止数据销售/共享 |
| 限制处理权 | 第 18 条 | 无 | 立即采取限制措施 | 标记相关记录 → 仅限存储数据 |

**响应模板：**
```
Subject: Your Data Request — Reference [DSR-YYYY-####]

We received your [access/deletion/correction] request on [date].

Action taken: [description]
Completion date: [date]
Data affected: [categories]

If any data was exempt from [deletion/access], the legal basis is: [exemption + explanation].

Questions? Contact our DPO at [email].
```

### 4. 同意管理框架
```
Valid consent requires ALL of:
☐ Freely given (no service denial for refusal, except where necessary)
☐ Specific (per-purpose, not bundled)
☐ Informed (plain language, named controller, purposes, rights)
☐ Unambiguous (affirmative action, no pre-ticked boxes)
☐ Withdrawable (as easy as giving consent)
☐ Documented (timestamp, version, method, scope)

Cookie/tracking consent tiers:
- Strictly Necessary: No consent needed (session, security, load balancing)
- Functional: Opt-in recommended (preferences, language)
- Analytics: Opt-in required in EU/UK (Google Analytics, Mixpanel)
- Marketing: Opt-in required everywhere (retargeting, cross-site tracking)
```

### 5. 数据泄露响应方案
**72 小时响应时间表（GDPR 第 33 条）：**

| 时间段 | 需要采取的行动 | 负责人 |
|------|--------|-------|
| 0-1 小时 | 控制数据泄露，保存证据，激活应急响应团队 | 安全负责人 |
| 1-4 小时 | 评估数据泄露范围：涉及哪些数据、多少数据主体、是否仍在泄露中？ | DPO + 安全团队 |
| 4-12 小时 | 根据所在司法管辖区确定通知义务 | 法律部门 + DPO |
| 12-24 小时 | 起草向监管机构的通知 | DPO |
| 24-48 小时 | 如果风险较高，起草针对数据主体的通知 | 通信部门 + 法律部门 |
| 48-72 小时 | 提交给监管机构的通知，并开始向数据主体发送通知 | DPO |
| 72 小时后 | 持续进行补救措施，分析根本原因，更新控制措施 | 所有相关人员 |

**通知决策树：**
1. 是否涉及个人数据？ → 否 → 无需通知
2. 是否对数据主体权利/自由构成风险？ → 否 → 仅内部记录
3. 风险是否较高？ → 否 → 仅通知监管机构（72 小时内）
4. 风险确实较高 → 通知监管机构（72 小时内）并立即通知数据主体

### 6. 供应商隐私评估
在与任何数据处理方或次级数据处理方合作之前：
```
☐ DPA signed with Art. 28 GDPR clauses (or CCPA service provider addendum)
☐ Technical measures verified (encryption at rest + transit, access controls)
☐ Sub-processor list reviewed and approved
☐ Data residency confirmed (adequate jurisdiction or transfer mechanism)
☐ Breach notification clause: ≤24 hours to controller
☐ Audit rights included
☐ Insurance: cyber liability ≥$5M (for processors handling >100K records)
☐ SOC 2 Type II or ISO 27001 current certification
☐ Deletion/return clause on contract termination
```

### 7. 跨境数据传输机制（Schrems II 法规实施后）
| 传输机制 | 使用场景 | 风险等级 |
|-----------|-------------|------------|
| 合适性评估 | 向欧盟批准的国家（英国、日本、韩国等）传输数据 | 低风险 |
| 标准合同条款（2021 年新条款） | 最常见的传输方式（如美国、印度等） | 中等风险 — 需要传输影响评估 |
| 有约束力的企业规则 | 跨集团数据传输 | 中等风险 — 需要 18 个月以上的审批时间 |
| 特例条款（第 49 条） | 仅限一次性、必要的数据传输 | 高风险 — 严格解释适用条件 |
| 欧盟-美国数据隐私框架 | 在 DPF（数据保护框架）名单上的美国公司 | 低至中等风险 — 检查供应商的认证情况 |

### 8. 隐私保护方案成熟度评估
对每个环节进行 1-5 分的评分：
| 评估项 | 分数 | 需要提供的证据 |
|------|-------|-------------------|
| 数据清单 | _/5 | 完整的数据清单，每季度更新 |
| 合法处理依据的文档 | _/5 | 按处理活动制定，每年审查 |
| 数据主体权利处理流程 | _/5 | 小于 30 小时的响应时间，尽可能自动化 |
| 同意管理 | _/5 | 部署了同意管理框架（CMP），有审计跟踪机制 |
| 数据泄露响应 | _/5 | 每年进行测试，确保 72 小时内能够响应 |
| 供应商管理 | _/5 | 签署了数据保护协议（DPAs），每年进行评估 |
| 培训 | _/5 | 全员每年接受培训，针对不同岗位进行定制 |
| 跨境数据传输 | _/5 | 完成了跨境数据传输协议（TIAs），使用最新的标准合同条款（SCCs） |
| 隐私设计 | _/5 | 隐私保护措施融入软件开发生命周期（SDLC），对高风险场景进行数据保护影响评估（DPIAs） |
| 责任追究机制 | _/5 | 设立了董事会报告机制，任命了 DPO，政策保持最新 |

**评分标准：**
- 40-50 分：方案成熟，可应对任何审计 |
- 30-39 分：正在完善中 — 需在 90 天内解决存在的问题 |
- 20-29 分：基础水平 — 存在显著风险 |
- 低于 20 分：情况危急 — 需立即采取补救措施

### 9. 监管罚款参考
| 监管法规 | 最高罚款金额 | 代表性案例 |
|-----------|-------------|-----------------|
| GDPR | 2000 万欧元或全球营业额的 4% | Meta 被罚款 12 亿美元（2023 年），Amazon 被罚款 7.46 亿美元（2021 年） |
| CCPA/CPRA | 每次故意违规罚款 7,500 美元 | Sephora 被罚款 120 万美元（2022 年） |
| LGPD（巴西） | 收入的 2%，最高罚款 5,000 万雷亚尔 | Cyrela 被罚款 1.4 万雷亚尔（2021 年，首例罚款） |
| POPIA（南非） | 1,000 万兰特或监禁 | 南非司法部罚款 500 万兰特（2023 年） |
| PIPL（中国） | 5,000 万元人民币或营业额的 5% | Didi 被罚款 12 亿元人民币（2022 年） |

## 行业特定隐私框架
如需针对医疗保健（HIPAA + GDPR）、金融科技（PCI + GDPR）、法律领域（法律特权 + GDPR）等行业的定制隐私框架，请查看我们的深度分析资料包：

**[AfrexAI 行业资料包 — 每份 47 美元](https://afrexai-cto.github.io/context-packs/)**
- 医疗保健 AI 资料包（HIPAA + GDPR + 地方法规）
- 金融科技 AI 资料包（PCI DSS + GDPR + SOX）
- 法律领域 AI 资料包（特权规则 + 跨境数据披露）
- 专业服务行业资料包（客户保密 + 多司法管辖区要求）

**免费工具：**
- [AI 收入泄露计算器](https://afrexai-cto.github.io/ai-revenue-calculator/) — 估算手动合规工作的成本 |
- [AI 代理配置向导](https://afrexai-cto.github.io/agent-setup/) — 配置您的 AI 代理系统

**套餐价格：**
- 基础套餐：27 美元 |
- 选择 3 项服务：97 美元 |
- 选择全部 10 项服务：197 美元 |
- 全部服务：247 美元
---
name: org-health-diagnostic
description: "跨职能组织健康检查工具，整合了来自公司高层管理团队（C-suite）各个角色的反馈信息。该工具通过红绿灯（traffic-light）评分系统对8个维度进行评估，并提供详细的分析建议。适用于评估公司整体运营状况、准备董事会审议、识别存在风险的业务部门，或在用户提及组织健康状况、健康检查或健康仪表板相关需求时使用。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: organizational-health
  updated: 2026-03-05
  python-tools: health_scorer.py
  frameworks: health-benchmarks
---
# 组织健康诊断

该诊断工具涵盖了八个维度，通过“交通灯”（traffic lights）的形式直观地显示各项指标的状态，并提供真实的基准数据，帮助您发现那些尚未察觉的问题。

## 关键词
- 组织健康（Organizational Health）
- 健康诊断（Health Diagnostic）
- 健康仪表板（Health Dashboard）
- 健康检查（Health Check）
- 公司健康（Company Health）
- 团队健康（Team Health）
- 初创企业健康（Startup Health）
- 健康评分卡（Health Scorecard）
- 健康评估（Health Assessment）
- 风险仪表板（Risk Dashboard）

## 快速入门

```bash
python scripts/health_scorer.py        # Guided CLI — enter metrics, get scored dashboard
python scripts/health_scorer.py --json # Output raw JSON for integration
```

### 描述您的指标：
```
/health [paste your key metrics or answer prompts]
/health:dimension [financial|revenue|product|engineering|people|ops|security|market]
```

## 八个维度

### 1. 💰 财务健康（CFO）
**衡量内容：** 公司是否有足够的资金来维持运营并投资于业务增长？

**关键指标：**
- **运营周期（Runway）**：以当前资金消耗速度计算，可维持运营的月数（绿色：>12个月；黄色：6-12个月；红色：<6个月）
- **资金消耗倍数（Burn Multiple）**：净资金消耗与净新收入（ARR）的比率（绿色：<1.5倍；黄色：1.5-2.5倍；红色：>2.5倍）
- **毛利率（Gross Margin）**：SaaS企业的目标毛利率应大于65%（绿色：>70%；黄色：55-70%；红色：<55%）
- **月度增长率（MoM Growth Rate）**：根据公司发展阶段进行评估（参见基准数据）
- **收入集中度（Revenue Concentration）**：最大客户对总收入的贡献比例（绿色：<15%；黄色：15-25%；红色：>25%）

### 2. 📈 收入健康（CRO）
**衡量内容：** 客户是否持续使用我们的产品，并且是否会推荐给我们？

**关键指标：**
- **净收入留存率（NRR）**：绿色：>110%；黄色：100-110%；红色：<100%
- **客户流失率（Annualized Logo Churn Rate）**：绿色：<5%；黄色：5-10%；红色：>10%
- **产品管线覆盖率（Pipeline Coverage）**：下一季度的潜在客户数量（绿色：>3倍；黄色：2-3倍；红色：<2倍）
- **客户获取成本（CAC）回收期（CAC Payback Period）**：绿色：<12个月；黄色：12-18个月；红色：>18个月
- **平均客户价值（Average ACV）趋势**：持续增长、持平或下降

### 3. 🚀 产品健康（CPO）
**衡量内容：** 客户是否喜欢并真正使用我们的产品？

**关键指标：**
- **净推荐值（NPS）**：绿色：>40；黄色：20-40；红色：<20%
- **日活跃用户（DAU）与月活跃用户（DAU/MAU）比率**：反映用户参与度（绿色：>40%；黄色：20-40%；红色：<20%）
- **核心功能采用率（Core Feature Adoption）**：使用核心功能的用户比例（绿色：>60%）
- **从注册到首次使用核心功能的平均时间（Time-to-Value）**：越短越好
- **客户满意度（CSAT）**：绿色：>4.2/5；黄色：3.5-4.2；红色：<3.5

### 4. ⚙️ 工程健康（CTO）
**衡量内容：** 我们能否可靠地发布产品并保持开发速度？

**关键指标：**
- **发布频率（Deployment Frequency）**：绿色：每日；黄色：每周；红色：每月或更少
- **变更失败率（Change Failure Rate）**：导致问题的发布次数占比（绿色：<5%；红色：>15%
- **平均恢复时间（MTTR）**：从问题出现到解决的平均时间（绿色：<1小时；黄色：1-4小时；红色：>4小时）
- **技术债务比率（Tech Debt Ratio）**：开发工作量中用于解决问题的时间占比（绿色：<20%；黄色：20-35%；红色：>35%）
- **问题频率（Incident Frequency）**：每月出现的P0/P1级别问题数量（绿色：<2次；黄色：2-5次；红色：>5次）

### 5. 👥 人员健康（CHRO）
**衡量内容：** 团队是否稳定、积极参与工作，并且能够持续成长？

**关键指标：**
- **年度人员流失率（Annualized Attrition Rate）**：绿色：<10%；黄色：10-20%；红色：>20%
- **员工参与度（Engagement Score）**：（如eNPS等指标）；绿色：>30；黄色：0-30；红色：<0%
- **填补空缺所需时间（Time-to-Fill）**：平均天数（绿色：<45天；黄色：45-90天；红色：>90天）
- **经理与核心员工的配比（Manager-to-IC Ratio）**：绿色：1:5–1:8；黄色：1:3–1:5或1:8–1:12；红色：低于此比例
- **内部晋升率（Internal Promotion Rate）**：高级职位至少有25-30%由内部员工填补

### 6. 🔄 运营健康（COO）
**衡量内容：** 我们是否能够有条不紊地执行战略？

**关键指标：**
- **关键目标完成率（OKR Completion Rate）**：达到目标的百分比（绿色：>70%；黄色：50-70%；红色：<50%）
- **决策周期（Decision Cycle Time）**：从制定决策到执行决策所需的时间（绿色：<48小时；黄色：48小时-1周）
- **会议效果（Meeting Effectiveness）**：有明确结果的会议占比
- **流程成熟度（Process Maturity）**：按1-5级评估（参见COO顾问的建议）
- **跨部门项目完成率（Cross-Functional Initiative Completion）**：按时按范围完成的项目比例

### 7. 🔒 安全健康（CISO）
**衡量内容：** 我们是否能够保护客户数据并确保合规性？

**关键指标：**
- **过去90天的安全事件（Security Incidents）**：绿色：0次；黄色：1-2次轻微事件；红色：1次以上严重事件
- **合规状态（Compliance Status）**：当前持有的证书或正在办理的证书与过期的证书对比
- **漏洞修复SLA（Vulnerability Remediation SLA）**：在指定时间内修复的关键安全漏洞比例（绿色：100%）
- **安全培训完成率（Security Training Completion）**：团队成员的安全培训完成率（绿色：>95%）
- **安全测试频率（Pen Test Frequency）**：最近一次安全测试的时间（绿色：<12个月；黄色：12-24个月；红色：>24个月）

### 8. 📣 市场健康（CMO）
**衡量内容：** 我们是否在市场上取得成功，并且能够高效地扩大市场份额？

**关键指标：**
- **客户获取成本（CAC）趋势**：季度环比改善、持平或恶化
- **有机客户与付费客户的比例**：有机客户占比越高，说明公司越健康（抗风险能力越强）
- **转化率（Win Rate）**：转化成功的有效机会比例（绿色：>25%；黄色：15-25%；红色：<15%）
- **针对主要竞争对手的竞争优势**：在市场竞争中的表现
- **品牌净推荐值（Brand NPS）**：在客户反馈调查（ICP）中的品牌认知度和偏好度

---

## 评分与“交通灯”系统

每个维度的评分范围为1-10分，通过“交通灯”颜色来表示：
- 🟢 **绿色（7-10分）**：健康状态——需要保持并优化
- 🟡 **黄色（4-6分）**：需要关注——趋势如何？是在改善还是恶化？
- 🔴 **红色（1-3分）**：需要立即行动——在30天内解决问题

**整体健康评分（Overall Health Score）：**
根据公司发展阶段，对各项指标进行加权平均（具体权重详见`references/health-benchmarks.md`）。

---

## 维度之间的相互影响

| 如果某个维度显示为红色…… | 需要重点关注的其他维度 |
|-----------------------------|----------------------------|
| 财务健康 | 人员健康（暂停招聘）→ 工程健康（暂停基础设施升级）→ 产品健康（缩减项目范围） |
| 收入健康 | 财务健康（资金缺口）→ 人员健康（人员流失风险）→ 市场健康（市场地位下降） |
| 人员健康 | 工程健康（开发速度下降）→ 产品健康（产品质量下降）→ 收入健康（客户流失率上升） |
| 工程健康 | 产品健康（功能更新延迟）→ 收入健康（交易成交受阻） |
| 产品健康 | 收入健康（净收入留存率下降，客户流失率上升）→ 市场健康（客户获取成本上升） |
| 运营健康 | 如果所有维度持续恶化，整体运营将陷入混乱（执行失败会导致连锁反应） |

---

## 仪表板输出格式

```
ORG HEALTH DIAGNOSTIC — [Company] — [Date]
Stage: [Seed/A/B/C]   Overall: [Score]/10   Trend: [↑ Improving / → Stable / ↓ Declining]

DIMENSION SCORES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 Financial    🟢 8.2  Runway 14mo, burn 1.6x — strong
📈 Revenue      🟡 5.8  NRR 104%, pipeline thin (1.8x coverage)
🚀 Product      🟢 7.4  NPS 42, DAU/MAU 38%
⚙️  Engineering  🟡 5.2  Debt at 30%, MTTR 3.2h
👥 People       🔴 3.8  Attrition 24%, eng morale low
🔄 Operations   🟡 6.0  OKR 65% completion
🔒 Security     🟢 7.8  SOC 2 Type II complete, 0 incidents
📣 Market       🟡 5.5  CAC rising, win rate dropped to 22%
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOP PRIORITIES
🔴 [1] People: attrition at 24% — engineering velocity will drop in 60 days
   Action: CHRO + CEO to run retention audit; target top 5 at-risk this week
🟡 [2] Revenue: pipeline coverage at 1.8x — Q+1 miss risk is high
   Action: CRO to add 3 qualified opps within 30 days or shift forecast down
🟡 [3] Engineering: tech debt at 30% of sprint — shipping will slow by Q3
   Action: CTO to propose debt sprint plan; COO to protect capacity

WATCH
→ People → Engineering cascade risk if attrition continues (see dimension interactions)
```

---

## 灵活的处理方式

进行健康诊断时，并不需要所有指标的数据。该工具可以处理部分数据：
- 缺失的指标将被排除在评分之外，并标记为“[数据缺失]”
- 即使部分指标缺失，现有指标的评分仍然有效
- 报告会指出下一个周期需要补充的数据项

## 参考资料
- `references/health-benchmarks.md`：针对不同发展阶段（种子期、A阶段、B阶段、C阶段）的基准数据
- `scripts/health_scorer.py`：用于生成评分结果的命令行工具，支持“交通灯”格式的输出
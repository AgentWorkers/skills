---
name: "org-health-diagnostic"
description: "跨职能组织健康检查工具，整合了来自公司高层管理团队（C-suite）各个角色的反馈信息。该工具通过红绿灯（traffic-light）评分系统对8个维度进行评估，并提供详细的分析建议。适用于评估公司整体运营状况、为董事会审查做准备、识别存在风险的业务部门，或在用户提及组织健康状况、组织健康检查或健康仪表板相关需求时使用。"
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

该诊断工具从八个维度全面评估组织的健康状况，通过“交通灯”系统（绿色、黄色、红色）直观显示各项指标的当前状态，帮助发现潜在问题。

## 关键词
- 组织健康（Organizational Health）
- 健康诊断（Health Diagnostic）
- 健康仪表盘（Health Dashboard）
- 健康检查（Health Check）
- 公司健康（Company Health）
- 团队健康（Team Health）
- 初创企业健康（Startup Health）
- 健康评分卡（Health Scorecard）
- 健康评估（Health Assessment）
- 风险仪表盘（Risk Dashboard）

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
**评估内容：** 公司是否有足够的资金支持运营和持续投资发展？
**关键指标：**
- **运营周期**：以当前资金消耗速度计算（绿色：>12个月；黄色：6-12个月；红色：<6个月）
- **资金消耗倍数**：净资金消耗与新增收入（绿色：<1.5倍；黄色：1.5-2.5倍；红色：>2.5倍）
- **毛利率**：SaaS企业的目标毛利率应大于65%（绿色：>70%；黄色：55-70%；红色：<55%）
- **月度增长率**：根据公司发展阶段进行评估（参考基准数据）
- **收入集中度**：最大客户对总收入的占比（绿色：<15%；黄色：15-25%；红色：>25%）

### 2. 📈 收入健康（CRO）
**评估内容：** 客户是否持续使用产品并愿意推荐给他人？
**关键指标：**
- **客户留存率（NRR）**：绿色：>110%；黄色：100-110%；红色：<100%
- **客户流失率（年化）**：绿色：<5%；黄色：5-10%；红色：>10%
- **下一季度的潜在客户数量**：绿色：>3倍；黄色：2-3倍；红色：<2倍
- **客户获取成本（CAC）回收期**：绿色：<12个月；黄色：12-18个月；红色：>18个月
- **平均客户生命周期价值（ACV）趋势**：持续增长、稳定或下降

### 3. 🚀 产品健康（CPO）
**评估内容：** 产品是否受到客户喜爱并得到有效使用？
**关键指标：**
- **净推荐值（NPS）**：绿色：>40；黄色：20-40；红色：<20%
- **日活跃用户（DAU）与月活跃用户（MAU）比例**：绿色：>40%；黄色：20-40%；红色：<20%
- **核心功能使用率**：使用核心功能的用户占比（绿色：>60%）
- **从注册到首次使用核心功能的平均时间**：越短越好
- **客户满意度（CSAT）**：绿色：>4.2/5；黄色：3.5-4.2；红色：<3.5

### 4. ⚙️ 工程健康（CTO）
**评估内容：** 团队能否稳定地交付产品并保持开发速度？
**关键指标：**
- **部署频率**：绿色：每天；黄色：每周；红色：每月或更少
- **部署失败率**：导致问题的部署比例（绿色：<5%；红色：>15%
- **平均恢复时间（MTTR）**：绿色：<1小时；黄色：1-4小时；红色：>4小时
- **技术债务比率**：开发工作量中用于解决问题的时间占比（绿色：<20%；黄色：20-35%；红色：>35%
- **问题发生频率**：每月P0/P1级别问题的数量（绿色：<2次；黄色：2-5次；红色：>5次）

### 5. 👥 人员健康（CHRO）
**评估内容：** 团队是否稳定、积极投入工作并持续成长？
**关键指标：**
- **年度人员流失率**：绿色：<10%；黄色：10-20%；红色：>20%
- **员工参与度**：（使用类似指标如eNPS）绿色：>30；黄色：0-30；红色：<0%
- **填补空缺所需时间**：绿色：<45天；黄色：45-90天；红色：>90天
- **经理与核心员工的配比**：绿色：1:5–1:8；黄色：1:3–1:5或1:8–1:12；红色：低于此比例
- **内部晋升率**：高级职位至少有25-30%由内部员工晋升

### 6. 🔄 运营健康（COO）
**评估内容：** 公司是否能够有条不紊地执行战略？
**关键指标：**
- **关键目标完成率**：绿色：>70%；黄色：50-70%；红色：<50%
- **决策周期**：从需求提出到决策制定的时间（绿色：<48小时；黄色：48小时-1周）
- **会议效果**：有明确成果的会议占比
- **流程成熟度**：根据公司阶段评估（参考COO顾问提供的标准）
- **跨部门项目的完成率**：按时按范围完成的占比

### 7. 🔒 安全健康（CISO）
**评估内容：** 公司是否有效保护客户数据并遵守法规？
**关键指标：**
- **过去90天的安全事件**：绿色：0次；黄色：1-2次轻微事件；红色：1次以上重大事件
- **合规状态**：当前持有的认证或正在办理中的认证
- **漏洞修复及时性**：90天内修复的关键漏洞占比（绿色：100%）
- **安全培训完成率**：团队成员的培训完成情况（绿色：>95%）
- **安全测试频率**：绿色：<12个月；黄色：12-24个月；红色：>24个月

### 8. 📣 市场健康（CMO）
**评估内容：** 公司在市场上的表现如何？增长是否高效？
**关键指标：**
- **客户获取成本（CAC）趋势**：季度环比是否改善、稳定或恶化
- **有机客户与付费客户的占比**：有机客户占比越高，公司越健康（抗风险能力越强）
- **成交率**：符合条件的机会中实际成交的比例（绿色：>25%；黄色：15-25%；红色：<15%）
- **相对于主要竞争对手的成交率**
- **品牌净推荐值（NPS）**：在客户调查中的品牌认知度和偏好评分

---

## 评分与“交通灯”系统

每个维度得分范围为1-10分，通过“交通灯”系统显示：
- 🟢 **绿色（7-10分）**：健康状态——需要维持和优化
- 🟡 **黄色（4-6分）**：需要关注——趋势是否良好或恶化？
- 🔴 **红色（1-3分）**：需要立即行动——30天内解决

**整体健康评分：**
根据公司发展阶段，对各项指标进行加权平均（具体权重详见`references/health-benchmarks.md`）。

---

## 维度之间的相互影响

某些维度的问题可能会引发其他维度的问题：
- **如果财务健康状况不佳**，可能会导致人员招聘暂停、工程团队工作停滞或产品功能缩减。
- **收入健康问题**可能导致资金短缺，进而增加人员流失风险，进而影响市场地位。
- **人员健康问题**可能降低开发速度，进而影响产品质量和收入增长。
- **工程健康问题**可能导致产品功能落后，影响成交率。
- **产品健康问题**可能导致收入下降和客户流失。
- **如果所有维度都持续恶化**，公司的整体运营效率会全面下降。

---

## 仪表盘输出格式

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

## 灵活处理数据缺失

进行诊断时，并不需要所有指标的数据。工具可以处理部分缺失的数据：
- 缺失的指标将从评分中排除，并标记为“[需要补充数据]”。
- 即使部分指标数据缺失，现有指标的评分仍然有效。
- 报告会指出下一周期需要补充的数据项。

## 参考资料
- `references/health-benchmarks.md`：针对不同发展阶段（种子期、A阶段、B阶段、C阶段）的基准数据
- `scripts/health_scorer.py`：用于生成评分结果的命令行工具，支持“交通灯”显示功能
---
name: "org-health-diagnostic"
description: "跨职能组织健康检查工具，整合了来自所有高层管理职位（C-suite）的反馈信息。该工具通过红绿灯（traffic-light）评分系统对8个维度进行评估，并提供详细的分析建议。适用于评估公司整体运营状况、准备董事会审议、识别存在风险的业务部门，或在用户提及组织健康状况、健康检查或健康仪表盘相关需求时使用。"
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

该诊断工具从八个维度全面评估组织的健康状况，通过“交通灯”（绿色/黄色/红色）的颜色代码直观显示各维度的健康状况，并提供具体的基准数据，帮助发现那些您可能尚未察觉的问题。

## 关键词
- 组织健康 (Organizational Health)
- 健康诊断 (Health Diagnostic)
- 健康仪表盘 (Health Dashboard)
- 健康检查 (Health Check)
- 公司健康 (Company Health)
- 团队健康 (Team Health)
- 初创企业健康 (Startup Health)
- 健康评分卡 (Health Scorecard)
- 健康评估 (Health Assessment)
- 风险仪表盘 (Risk Dashboard)

## 快速入门

```bash
python scripts/health_scorer.py        # Guided CLI — enter metrics, get scored dashboard
python scripts/health_scorer.py --json # Output raw JSON for integration
```

您也可以自行描述您关注的指标：
```
/health [paste your key metrics or answer prompts]
/health:dimension [financial|revenue|product|engineering|people|ops|security|market]
```

## 八个维度

### 1. 💰 财务健康（CFO）
**评估内容：** 公司是否有足够的资金来维持运营并投资于业务增长？

**关键指标：**
- **运营周期** — 以当前资金消耗速度计算可维持的运营时间（绿色：>12个月；黄色：6-12个月；红色：<6个月）
- **资金消耗倍数** — 净资金消耗与净新增收入（绿色：<1.5倍；黄色：1.5-2.5倍；红色：>2.5倍）
- **毛利率** — SaaS产品的目标毛利率：>65%（绿色：>70%；黄色：55-70%；红色：<55%）
- **月度增长率** — 根据公司发展阶段进行评估（参见基准数据）
- **收入集中度** — 最大客户对总收入的贡献比例（绿色：<15%；黄色：15-25%；红色：>25%）

### 2. 📈 收入健康（CRO）
**评估内容：** 客户是否持续使用我们的产品，并愿意推荐给我们？

**关键指标：**
- **净收入留存率（NRR）** — 绿色：>110%；黄色：100-110%；红色：<100%
- **客户流失率（年度化）** — 绿色：<5%；黄色：5-10%；红色：>10%
- **下一季度的潜在客户数量** — 绿色：>3倍；黄色：2-3倍；红色：<2倍
- **客户获取成本（CAC）回收期** — 绿色：<12个月；黄色：12-18个月；红色：>18个月
- **平均客户生命周期价值（ACV）趋势** — 增长、稳定或下降

### 3. 🚀 产品健康（CPO）
**评估内容：** 客户是否真正喜欢并使用我们的产品？

**关键指标：**
- **净推荐值（NPS）** — 绿色：>40；黄色：20-40；红色：<20%
- **日活跃用户（DAU）与月活跃用户（MAU）比例** — 代表用户参与度（绿色：>40%；黄色：20-40%；红色：<20%）
- **核心功能的采用率** — 使用核心功能的用户比例（绿色：>60%）
- **从注册到首次使用核心功能的平均时间** — 越短越好
- **客户满意度（CSAT）** — 绿色：>4.2/5；黄色：3.5-4.2；红色：<3.5

### 4. ⚙️ 工程健康（CTO）
**评估内容：** 我们能否可靠地发布新功能并保持开发速度？

**关键指标：**
- **发布频率** — 绿色：每日；黄色：每周；红色：每月或更少
- **部署失败率** — 导致问题的部署比例（绿色：<5%；红色：>15%）
- **平均恢复时间（MTTR）** — 绿色：<1小时；黄色：1-4小时；红色：>4小时
- **技术债务比率** — 技术债务占开发能力的比例（绿色：<20%；黄色：20-35%；红色：>35%）
- **问题发生频率** — 每月P0/P1级别问题的数量（绿色：<2次；黄色：2-5次；红色：>5次）

### 5. 👥 人员健康（CHRO）
**评估内容：** 团队是否稳定、积极且具备成长潜力？

**关键指标：**
- **年度人员流失率** — 绿色：<10%；黄色：10-20%；红色：>20%
- **员工参与度** — （使用类似指标如eNPS）绿色：>30；黄色：0-30；红色：<0%
- **填补职位所需时间** — 平均天数（绿色：<45天；黄色：45-90天；红色：>90天）
- **经理与初级员工的配比** — 绿色：1:5–1:8；黄色：1:3–1:5或1:8–1:12；红色：其他情况
- **内部晋升率** — 高级职位至少有25-30%由内部员工填补

### 6. 🔄 运营健康（COO）
**评估内容：** 我们是否能够有条不紊地执行战略？

**关键指标：** **关键目标完成率（OKR）** — 绿色：>70%；黄色：50-70%；红色：<50%
- **决策周期** — 从决策到执行所需时间（绿色：<48小时；黄色：48小时-1周）
- **会议效率** — 有明确成果的会议比例
- **流程成熟度** — 根据COO顾问的评估标准（1-5级）
- **跨部门项目的完成率** — 是否按时按范围完成

### 7. 🔒 安全健康（CISO）
**评估内容：** 我们是否有效保护客户数据并遵守法规？

**关键指标：**
- **过去90天的安全事件** — 绿色：0；黄色：1-2起轻微事件；红色：1起以上重大事件
- **合规状态** — 当前/进行中的认证与逾期认证的比例
- **漏洞修复SLA** — 临界安全漏洞的修复比例（绿色：100%）
- **安全培训完成率** — 团队成员的培训完成情况（绿色：>95%）
- **安全测试频率** — 最近一次安全测试的时间（绿色：<12个月；黄色：12-24个月；红色：>24个月）

### 8. 📣 市场健康（CMO）
**评估内容：** 我们在市场上的表现如何？业务是否高效增长？

**关键指标：**
- **客户获取成本（CAC）趋势** — 每季度是改善、稳定还是恶化
- **自然获取客户与付费客户的占比** — 自然获取客户越多，业务越健康（抗风险能力越强）
- **成交率** — 符合条件的机会中实际成交的比例（绿色：>25%；黄色：15-25%；红色：<15%）
- **相对于主要竞争对手的成交率**
- **品牌净推荐值（Brand NPS）** — 在市场调研中的认知度和偏好评分

---

## 评分与“交通灯”系统

每个维度的评分范围为1-10分，通过“交通灯”颜色表示健康状况：
- 🟢 **绿色（7-10分）**：健康 — 需要维持并优化
- 🟡 **黄色（4-6分）**：需要关注 — 需要观察趋势，看是否在改善或恶化
- 🔴 **红色（1-3分）**：需要立即行动 — 30天内解决问题

**整体健康评分：**
根据公司发展阶段对各项指标进行加权平均（具体权重请参考`references/health-benchmarks.md`）。

---

## 维度之间的关联（一个问题的影响）

| 如果某个维度显示为红色…… | 需要关注的其他维度 |
|-----------------------------|----------------------------|
| 财务健康 | 人员（暂停招聘）→ 工程（暂停基础设施升级）→ 产品（缩减功能范围） |
| 收入健康 | 财务（资金缺口）→ 人员（流失风险）→ 市场（失去市场地位） |
| 人员健康 | 工程（开发速度下降）→ 产品（质量下降）→ 收入（客户流失增加） |
| 工程健康 | 产品（功能问题）→ 收入（交易失败） |
| 产品健康 | 收入（净收入留存率下降）→ 市场（客户获取成本上升） |
| 运营健康 | 所有维度随时间恶化（执行失败会导致连锁反应） |

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

## 灵活的处理方式

进行诊断时并不需要所有指标的数据。该工具可以处理部分数据：
- 缺失的指标将从评分中排除，并标记为“[需要补充数据]”
- 即使部分数据缺失，其余指标的评分仍然有效
- 报告会指出下一周期需要补充的数据项

## 参考资料
- `references/health-benchmarks.md` — 不同发展阶段（种子期、A阶段、B阶段、C阶段）的基准数据
- `scripts/health_scorer.py` — 用于生成评分结果的命令行工具，支持“交通灯”显示方式
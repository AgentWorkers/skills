---
name: capa-officer
description: CAPA（Corrective Action Plan）系统管理是医疗器械质量管理体系（QMS）的重要组成部分，涵盖了根本原因分析、纠正措施规划、有效性验证以及CAPA相关指标的监控。该系统可用于CAPA问题的调查、5-Why分析（即连续追问“为什么”以找出问题根源）、鱼骨图（Fishbone Diagram）的绘制、纠正措施的跟踪与执行、有效性验证，以及CAPA管理流程的优化。
triggers:
  - CAPA investigation
  - root cause analysis
  - 5 Why analysis
  - fishbone diagram
  - corrective action
  - preventive action
  - effectiveness verification
  - CAPA metrics
  - nonconformance investigation
  - quality issue investigation
  - CAPA tracking
  - audit finding CAPA
---

# CAPA专员

在质量管理体系中，CAPA（纠正性和预防性措施）管理侧重于系统的根本原因分析、行动实施以及效果验证。

---

## 目录

- [CAPA调查工作流程](#capa-investigation-workflow)
- [根本原因分析](#root-cause-analysis)
- [纠正性措施规划](#corrective-action-planning)
- [效果验证](#effectiveness-verification)
- [CAPA指标与报告](#capa-metrics-and-reporting)
- [参考文档](#reference-documentation)
- [工具](#tools)

---

## CAPA调查工作流程

从启动到关闭，进行系统的CAPA调查：

1. 用客观证据记录触发事件
2. 评估事件的严重性并确定是否需要启动CAPA
3. 组建具有相关专业知识的调查团队
4. 系统地收集数据和证据
5. 选择并应用适当的根本原因分析（RCA）方法
6. 识别根本原因并附上支持证据
7. 制定纠正性和预防性措施
8. **验证：** 根本原因能够解释所有症状；如果消除，问题将不再发生

### CAPA必要性判定

| 触发类型 | 是否需要CAPA | 判定标准 |
|--------------|---------------|----------|
| 客户投诉（安全相关） | 是 | 任何涉及患者/用户安全的投诉 |
| 客户投诉（质量相关） | 根据严重性和频率评估 | |
| 内部审计发现（重大问题） | 是 | 系统性故障或缺失要素 |
| 内部审计发现（轻微问题） | 建议启动 | 零星失误或部分实施 |
| 不符合要求（重复出现） | 是 | 同类型问题出现3次以上 |
| 不符合要求（孤立事件） | 根据严重性和风险评估 | |
| 外部审计发现 | 是 | 所有重大和轻微问题 |
| 趋势分析 | 根据趋势的严重性评估 | |

### 调查团队组成

| CAPA严重程度 | 所需团队成员 |
|---------------|----------------------|
| 严重 | CAPA专员、流程负责人、质量保证经理、主题专家、管理层代表 |
| 重大 | CAPA专员、流程负责人、主题专家 |
| 轻微 | CAPA专员、流程负责人 |

### 证据收集清单

- 问题描述（具体细节：什么、在哪里、何时、谁、程度）
- 问题发生的时间线
- 相关记录和文件
- 受影响人员的访谈记录
- 照片或实物证据（如适用）
- 相关投诉、不符合要求的情况或之前的CAPA记录
- 流程参数和规范

---

## 根本原因分析

根据问题特征选择并应用适当的RCA方法。

### RCA方法选择决策树

```
Is the issue safety-critical or involves system reliability?
├── Yes → Use FAULT TREE ANALYSIS
└── No → Is human error the suspected primary cause?
    ├── Yes → Use HUMAN FACTORS ANALYSIS
    └── No → How many potential contributing factors?
        ├── 1-2 factors (linear causation) → Use 5 WHY ANALYSIS
        ├── 3-6 factors (complex, systemic) → Use FISHBONE DIAGRAM
        └── Unknown/proactive assessment → Use FMEA
```

### 5Why分析

适用场景：单一原因导致的线性问题，或具有明确故障点的流程偏差。

**模板：**

```
PROBLEM: [Clear, specific statement]

WHY 1: Why did [problem] occur?
BECAUSE: [First-level cause]
EVIDENCE: [Supporting data]

WHY 2: Why did [first-level cause] occur?
BECAUSE: [Second-level cause]
EVIDENCE: [Supporting data]

WHY 3: Why did [second-level cause] occur?
BECAUSE: [Third-level cause]
EVIDENCE: [Supporting data]

WHY 4: Why did [third-level cause] occur?
BECAUSE: [Fourth-level cause]
EVIDENCE: [Supporting data]

WHY 5: Why did [fourth-level cause] occur?
BECAUSE: [Root cause]
EVIDENCE: [Supporting data]
```

**示例 - 校准过期：**

```
PROBLEM: pH meter (EQ-042) found 2 months overdue for calibration

WHY 1: Why was calibration overdue?
BECAUSE: Equipment was not on calibration schedule
EVIDENCE: Calibration schedule reviewed, EQ-042 not listed

WHY 2: Why was it not on the schedule?
BECAUSE: Schedule not updated when equipment was purchased
EVIDENCE: Purchase date 2023-06-15, schedule dated 2023-01-01

WHY 3: Why was the schedule not updated?
BECAUSE: No process requires schedule update at equipment purchase
EVIDENCE: SOP-EQ-001 reviewed, no such requirement

WHY 4: Why is there no such requirement?
BECAUSE: Procedure written before equipment tracking was centralized
EVIDENCE: SOP last revised 2019, equipment system implemented 2021

WHY 5: Why has procedure not been updated?
BECAUSE: Periodic review did not assess compatibility with new systems
EVIDENCE: No review against new equipment system documented

ROOT CAUSE: Procedure review process does not assess compatibility
with organizational systems implemented after original procedure creation.
```

### 鱼骨图（6M）分类

| 分类 | 关注领域 | 常见原因 |
|----------|-------------|----------------|
| 人（人员） | 培训、能力、工作量 | 技能差距、疲劳、沟通问题 |
| 机器（设备） | 校准、维护、使用年限 | 磨损、故障、容量不足 |
| 方法（流程） | 流程、操作指南 | 步骤不明确、控制措施缺失 |
| 材料 | 规格、供应商、储存条件 | 不符合规格、材料降解、污染 |
| 测量工具 | 校准、方法、解读 | 仪器误差、使用方法错误 |
| 环境因素 | 温度、湿度、清洁度 | 环境因素导致的问题 |

有关完整的方法细节和模板，请参阅`references/rca-methodologies.md`。

### 根本原因验证

在制定行动方案之前，验证根本原因是否成立：

- 根本原因可以通过客观证据得到证实
- 如果根本原因被消除，问题将不再发生
- 根本原因在组织控制范围内
- 根本原因能够解释所有观察到的症状
- 没有其他重要原因未被解决

---

## 纠正性措施规划

针对识别的根本原因，制定有效的行动方案：

1. 制定立即的遏制措施
2. 制定针对根本原因的纠正性措施
3. 为类似流程制定预防性措施
4. 分配责任和资源
5. 制定带有里程碑的时间表
6. 明确成功标准和验证方法
7. 将这些内容记录在CAPA行动计划中
8. **验证：** 行动直接针对根本原因；成功标准是可衡量的

### 行动类型

| 类型 | 目的 | 时间表 | 示例 |
|------|---------|----------|---------|
| 阻止影响 | 立即阻止问题的进一步发展 | 24-72小时 | 将受影响的产品隔离 |
| 纠正 | 修复具体问题 | 1-2周 | 重新加工或更换受影响的物品 |
| 根本性解决 | 消除根本原因 | 30-90天 | 修订流程、增加控制措施 |
| 预防 | 防止类似问题再次发生 | 60-120天 | 将解决方案扩展到类似流程 |

### 行动计划组成部分

```
ACTION PLAN TEMPLATE

CAPA Number: [CAPA-XXXX]
Root Cause: [Identified root cause]

ACTION 1: [Specific action description]
- Type: [ ] Containment [ ] Correction [ ] Corrective [ ] Preventive
- Responsible: [Name, Title]
- Due Date: [YYYY-MM-DD]
- Resources: [Required resources]
- Success Criteria: [Measurable outcome]
- Verification Method: [How success will be verified]

ACTION 2: [Specific action description]
...

IMPLEMENTATION TIMELINE:
Week 1: [Milestone]
Week 2: [Milestone]
Week 4: [Milestone]
Week 8: [Milestone]

APPROVAL:
CAPA Owner: _____________ Date: _______
Process Owner: _____________ Date: _______
QA Manager: _____________ Date: _______
```

### 行动效果指标

| 指标 | 目标 | 注意事项 |
|-----------|--------|----------|
| 行动范围 | 是否完全解决了根本原因 | 仅处理表面症状 |
| 明确性 | 行动结果是否可衡量 | 承诺不明确 |
| 时间表 | 时间表是否合理且可实现 | 没有截止日期或不切实际 |
| 资源 | 是否已识别并分配 | 未明确 |
| 持久性 | 解决方案是否永久有效 | 是临时解决方案 |

---

## 效果验证

验证纠正性措施是否达到了预期效果：

1. 给予足够的实施时间（至少30-90天）
2. 收集实施后的数据
3. 与实施前的数据对比
4. 根据成功标准进行评估
5. 确保在验证期间问题没有再次发生
6. 记录验证证据
7. 确定CAPA的有效性
8. **验证：** 所有标准都通过客观证据得到证实；没有问题再次发生

### 验证时间表指南

| CAPA严重程度 | 等待时间 | 验证周期 |
|---------------|-------------|---------------------|
| 严重 | 30天 | 实施后30-90天 |
| 重大 | 60天 | 实施后60-180天 |
| 轻微 | 90天 | 实施后90-365天 |

### 验证方法

| 方法 | 适用场景 | 所需证据 |
|--------|----------|-------------------|
| 数据趋势分析 | 可量化问题 | 实施前后对比、趋势图表 |
| 流程审计 | 流程合规性问题 | 审计检查表、访谈记录 |
| 记录审查 | 文件问题 | 样本记录、合规率 |
| 测试/检查 | 产品质量问题 | 测试结果、合格/不合格数据 |
| 访谈/观察 | 培训问题 | 访谈记录、观察记录 |

### 效果判定

```
Did recurrence occur during verification period?
├── Yes → CAPA INEFFECTIVE (re-investigate root cause)
└── No → Were all effectiveness criteria met?
    ├── Yes → CAPA EFFECTIVE (proceed to closure)
    └── No → Extent of gap?
        ├── Minor gap → Extend verification or accept with justification
        └── Significant gap → CAPA INEFFECTIVE (revise actions)
```

有关详细流程，请参阅`references/effectiveness-verification-guide.md`。

---

## CAPA指标与报告

通过关键指标监控CAPA项目的执行情况。

### 关键绩效指标

| 指标 | 目标 | 计算方法 |
|--------|--------|-------------|
| CAPA周期时间 | 平均<60天 | (关闭日期 - 开始日期) / CAPA总数 |
| 过期率 | <10% | 过期的CAPA数量 / 总开放CAPA数量 |
| 首次验证成功率 | >90% | 首次验证即有效的CAPA数量 / 总验证CAPA数量 |
| 问题复发率 | <5% | 重复出现的问题数量 / 已关闭的CAPA总数 |
| 调查质量 | 100%的根本原因得到验证 | 验证的根本原因数量 / 总CAPA数量 |

### CAPA老化分析

| 时间段 | 状态 | 所需行动 |
|------------|--------|-----------------|
| 0-30天 | 进展顺利 | 监控进展 |
| 31-60天 | 监控 | 检查是否存在延误 |
| 61-90天 | 警告 | 提报给管理层 |
| >90天 | 严重 | 需要管理层介入 |

### 管理层审查内容

每月的CAPA状态报告包括：
- 按严重程度和状态分类的开放CAPA数量
- 过期的CAPA列表及其负责人
- 周期时间趋势
- 效果率趋势
- 问题来源分析（投诉、审计、不符合要求的情况）
- 改进建议

---

## 参考文档

### 根本原因分析方法

`references/rca-methodologies.md`包含：
- 方法选择决策树
- 5Why分析模板和示例
- 鱼骨图分类和模板
- 用于安全关键问题的故障树分析
- 用于人为因素分析的方法
- 用于主动风险管理的FMEA（失效模式与效应分析）
- 混合方法指南

### 效果验证指南

`references/effectiveness-verification-guide.md`包含：
- 验证计划要求
- 验证方法选择
- 效果标准定义（SMART原则）
- 根据严重程度划分的关闭要求
- 无效的CAPA流程
- 文档模板

---

## 工具

### CAPA跟踪器

```bash
# Generate CAPA status report
python scripts/capa_tracker.py --capas capas.json

# Interactive mode for manual entry
python scripts/capa_tracker.py --interactive

# JSON output for integration
python scripts/capa_tracker.py --capas capas.json --output json

# Generate sample data file
python scripts/capa_tracker.py --sample > sample_capas.json
```

功能包括：
- 计算并报告：汇总指标（开放、关闭、过期、周期时间、效果）
- 状态分布
- 严重程度和问题来源分析
- 按时间段划分的老化报告
- 过期的CAPA列表
- 可操作的改进建议

### CAPA输入示例

```json
{
  "capas": [
    {
      "capa_number": "CAPA-2024-001",
      "title": "Calibration overdue for pH meter",
      "description": "pH meter EQ-042 found 2 months overdue",
      "source": "AUDIT",
      "severity": "MAJOR",
      "status": "VERIFICATION",
      "open_date": "2024-06-15",
      "target_date": "2024-08-15",
      "owner": "J. Smith",
      "root_cause": "Procedure review gap",
      "corrective_action": "Updated SOP-EQ-001"
    }
  ]
}
```

---

## 监管要求

### ISO 13485:2016 第8.5条

| 子条款 | 要求 | 关键活动 |
|------------|-------------|----------------|
| 8.5.2 纠正性措施 | 消除不符合要求的原因 | 审查不符合要求的情况、确定原因、评估行动、实施、效果验证 |
| 8.5.3 预防性措施 | 消除潜在的不符合要求的情况 | 趋势分析、确定原因、评估行动、实施、效果验证 |

### FDA 21 CFR 820.100

要求的CAPA要素包括：
- 实施纠正性和预防性措施的程序
- 分析质量数据来源（投诉、不符合要求的情况、审计结果）
- 调查不符合要求的原因
- 确定必要的纠正和预防措施
- 验证措施的有效性，确保不会对设备产生不良影响
- 提交相关信息供管理层审查

### FDA 483常见观察结果

| 观察结果 | 根本原因模式 |
|-------------|-------------------|
| 对重复出现的问题未启动CAPA | 未进行趋势分析 |
| 根本原因分析不深入 | 调查和培训不足 |
| 未验证效果 | 无验证流程 |
| 行动未针对根本原因 | 仅处理表面症状 |

---

## 监管要求

### ISO 13485:2016 第8.5条

| 子条款 | 要求 | 关键活动 |
|------------|-------------|----------------|
| 8.5.2 纠正性措施 | 消除不符合要求的原因 | 审查不符合要求的情况、确定原因、评估行动、实施、效果验证 |
| 8.5.3 预防性措施 | 消除潜在的不符合要求的情况 | 进行趋势分析、确定原因、评估行动、实施、效果验证 |

### FDA 21 CFR 820.100

要求的CAPA要素包括：
- 实施纠正性和预防性措施的程序
- 分析质量数据来源（投诉、不符合要求的情况、审计结果）
- 调查不符合要求的原因
- 确定必要的纠正和预防措施
- 验证措施的有效性，确保不会对设备产生不良影响
- 提交相关信息供管理层审查

### FDA 483常见观察结果

| 观察结果 | 根本原因模式 |
|-------------|-------------------|
| 对重复出现的问题未启动CAPA | 未进行趋势分析 |
| 根本原因分析不深入 | 调查和培训不足 |
| 未验证效果 | 无验证流程 |
| 行动未针对根本原因 | 仅处理表面症状 |

---

## 监管要求

### ISO 13485:2016 第8.5条

| 子条款 | 要求 | 关键活动 |
|------------|-------------|----------------|
| 8.5.2 纠正性措施 | 消除不符合要求的原因 | 审查不符合要求的情况、确定原因、评估行动、实施、效果验证 |
| 8.5.3 预防性措施 | 消除潜在的不符合要求的情况 | 进行趋势分析、确定原因、评估行动、实施、效果验证 |

### FDA 21 CFR 820.100

要求的CAPA要素包括：
- 实施纠正性和预防性措施的程序
- 分析质量数据来源（投诉、不符合要求的情况、审计结果）
- 调查不符合要求的原因
- 确定必要的纠正和预防措施
- 验证措施的有效性，确保不会对设备产生不良影响
- 提交相关信息供管理层审查

### FDA 483常见观察结果

| 观察结果 | 根本原因模式 |
|-------------|-------------------|
| 对重复出现的问题未启动CAPA | 未进行趋势分析 |
| 根本原因分析不深入 | 调查和培训不足 |
| 未验证效果 | 无验证流程 |
| 行动未针对根本原因 | 仅处理表面症状 |
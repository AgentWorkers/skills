# 能源审计 — 商业建筑评估

为商业或工业设施进行全面能源审计，识别能源浪费情况，模拟节能效果，并生成一份优先级的改造计划及投资回报时间表。

## 功能概述

- 收集12个月以上的能源使用数据（电力、燃气、水、蒸汽）
- 将实际能耗与ASHRAE和ENERGY STAR的基准标准进行对比
- 确定十大最具节能效果的改进措施（按投资回收期排序）
- 计算每项改进措施的简单投资回收期（Simple Payback）、内部收益率（IRR）和生命周期成本
- 生成包含执行摘要的ASHRAE二级审计报告
- 指出优化能源费用的机会（如需求响应、分时电价调整等）
- 显示各州/地区的可享受补贴和激励计划

## 使用方法

请告知您的代理：
- “为我们的45,000平方英尺的办公楼进行能源审计”
- “分析我们的能源账单，寻找节能机会”
- “为我们的仓库制定改造计划——预算为20万美元”

需要提供的信息：
1. **建筑类型**：办公楼、零售店、仓库、制造厂、医疗机构、教育机构
2. **建筑面积**及地理位置（气候区对节能效果有影响）
3. **12个月的能源账单**（或汇总后的每月能耗数据）
4. **运营时间**：包括不同时间段的使用情况、周末用电量及季节性用电模式
5. **主要设备**：暖通空调系统（HVAC）的年龄和类型、照明设备、压缩空气系统、工艺负载等

## 审计框架

### 基准评估
- **能源使用强度（EUI）** = 总能耗（千英热单位/kBtu）÷ 建筑面积（平方英尺）
- 与各建筑类型的CBECS中位数进行比较
- **ENERGY STAR评分目标**：75分以上（属于最高四分之一）

### 节能措施（ECMs）

| 类别 | 典型节能效果 | 投资回收期 |
|----------|----------------|---------|
| LED照明改造 | 照明能耗降低40-60% | 1-3年 |
| 暖通空调控制系统/BMS优化 | HVAC能耗降低15-25% | 2-4年 |
- 电机/风扇的变频驱动器（VFD） | 电机能耗降低20-50% | 1-3年 |
- 建筑围护结构改进（保温、密封） | 供暖/制冷能耗降低10-20% | 3-7年 |
- 参与需求响应计划 | 峰值能耗降低5-15% | 立即见效 |
- 太阳能光伏系统 | 电力能耗降低30-70% | 5-8年（含税收抵免政策） |
- 热能回收系统 | 热能损失降低10-30% | 2-5年 |

### 财务分析
对于每项节能措施：
- **简单投资回收期** = 总成本 ÷ 年节能费用
- **内部收益率（IRR）** = 设备使用寿命期间的年均回报率
- **生命周期成本** = 安装成本 + 维护费用 - 节能费用 - 可享受的补贴
- **避免的额外费用**：包括能源费用的增长率（通常为每年2-4%）

### 补贴与激励政策查询
- **联邦政府**：提供税收抵免（如太阳能项目的30%税收抵免）、179D税收减免（每平方英尺0.50-5.00美元）
- **州政府**：通过邮政编码查询当地的DSIRE数据库获取补贴信息
- **能源供应商**：提供针对特定节能行为的定制激励计划（每节约1千瓦时的费用减免金额）

## 输出格式

```
ENERGY AUDIT REPORT
Building: [name] | Type: [type] | Size: [sq ft] | Location: [city, state]

CURRENT PERFORMANCE
Annual Energy Cost: $XXX,XXX
EUI: XX.X kBtu/sq ft (benchmark: XX.X — [above/below] median)
ENERGY STAR Score: XX/100

TOP RECOMMENDATIONS (ranked by payback)
#1: [ECM] — $XX,XXX savings/yr | $XX,XXX cost | X.X yr payback | XX% IRR
#2: [ECM] — ...

TOTAL OPPORTUNITY
Combined Savings: $XXX,XXX/yr (XX% reduction)
Total Investment: $XXX,XXX
Blended Payback: X.X years
Available Rebates: $XX,XXX

IMPLEMENTATION ROADMAP
Phase 1 (0-6 mo): [quick wins — LED, controls, demand response]
Phase 2 (6-18 mo): [HVAC, VFDs, envelope]
Phase 3 (18-36 mo): [renewables, major retrofits]
```

## 重要性

根据美国能源部（DOE）的数据，商业建筑通常会浪费其消耗能源的30%。例如，每年50万美元的能源费用中，有超过15万美元可以通过节能措施回收。大多数节能措施在2-4年内即可收回成本，之后带来的收益即为纯利润。

---

本工具由[AfrexAI](https://afrexai-cto.github.io/context-packs/)开发——专为实际业务运营设计的AI辅助工具包。

探索更多工具：
- [AI收入计算器](https://afrexai-cto.github.io/ai-revenue-calculator/)：帮助您发现业务中的资金流失点
- [代理设置向导](https://afrexai-cto.github.io/agent-setup/)：快速部署AI代理
- [行业特定配置包](https://afrexai-cto.github.io/context-packs/)：为制造业、专业服务等行业提供定制化的代理配置方案（价格47美元）
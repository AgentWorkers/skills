---
name: "product-strategist"
description: 面向产品负责人的战略产品领导力工具包，涵盖OKR目标分解、季度规划、竞争格局分析、产品愿景文档以及团队扩展方案等内容。适用于制定季度OKR文档、定义产品目标或关键绩效指标（KPIs）、构建产品路线图、开展竞争分析、设计团队架构或招聘计划、协调工程与设计团队之间的产品战略，以及从公司层面到团队层面生成目标层级结构。
---
# 产品策略师

这是一套专为产品负责人设计的战略工具包，旨在帮助推动公司愿景的实现、确保各部门之间的协调一致，并提升组织整体效能。

---

## 核心功能

| 功能 | 描述 | 工具 |
|------------|-------------|------|
| **OKR级联生成** | 从公司层面到团队层面自动生成一致的OKR目标 | `okr_cascade_generator.py` |
| **协调一致性评估** | 测量纵向和横向的协调程度 | 内置于生成器中 |
| **战略模板** | 提供5种预设的战略类型 | 成长、留存、收入、创新、运营 |
| **团队配置** | 可根据实际组织结构进行定制 | `--teams` 参数 |

---

## 快速入门

```bash
# Growth strategy with default teams
python scripts/okr_cascade_generator.py growth

# Retention strategy with custom teams
python scripts/okr_cascade_generator.py retention --teams "Engineering,Design,Data"

# Revenue strategy with 40% product contribution
python scripts/okr_cascade_generator.py revenue --contribution 0.4

# Export as JSON for integration
python scripts/okr_cascade_generator.py growth --json > okrs.json
```

---

## 工作流程：季度战略规划

### 第一步：确定战略重点

| 战略类型 | 适用场景 |
|----------|-------------|
| **增长** | 扩大用户基础、拓展市场 |
| **留存** | 降低用户流失率、提升用户生命周期价值（LTV） |
| **收入** | 提高平均收入（ARPU）、探索新的盈利模式 |
| **创新** | 实现市场差异化、开发新功能 |
| **运营** | 提高运营效率、扩展业务规模 |

详细指导请参阅 `references/strategy_types.md`。

### 第二步：收集所需指标数据

```json
{
  "current": 100000,      // Current MAU
  "target": 150000,       // Target MAU
  "current_nps": 40,      // Current NPS
  "target_nps": 60        // Target NPS
}
```

### 第三步：配置团队并运行生成器

```bash
# Default teams
python scripts/okr_cascade_generator.py growth

# Custom org structure with contribution percentage
python scripts/okr_cascade_generator.py growth \
  --teams "Core,Platform,Mobile,AI" \
  --contribution 0.3
```

### 第四步：评估协调一致性

| 评估指标 | 目标值 | 低于目标值时的应对措施 |
|-------|--------|-----------------|
| 纵向协调性 | >90% | 确保所有目标都与上级目标保持一致 |
| 横向协调性 | >75% | 检查团队间的协作是否存在差距 |
| 覆盖范围 | >80% | 确保所有公司OKR目标都得到落实 |
| 平衡性 | >80% | 若某个团队负担过重，需重新分配任务 |
| **总体协调性** | **>80%** | 若低于60%，则需要调整团队分工 |

### 第五步：优化、验证并导出结果

在最终确定目标之前，请完成以下步骤：
- [ ] 与相关利益方共同审查生成的OKR目标 |
- [ ] 根据团队能力调整任务分配 |
- [ ] 确认各团队的贡献比例是否合理 |
- [ ] 确保团队之间没有目标冲突 |
- [ ] 建立定期检查机制（每两周一次）

```bash
# Export JSON for tools like Lattice, Ally, Workboard
python scripts/okr_cascade_generator.py growth --json > q1_okrs.json
```

---

## OKR级联生成器

### 使用方法

```bash
python scripts/okr_cascade_generator.py [strategy] [options]
```

**战略类型：** 成长 | 留存 | 收入 | 创新 | 运营

### 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--teams`, `-t` | 以逗号分隔的团队名称 | Growth, Platform, Mobile, Data |
| `--contribution`, `-c` | 产品对公司OKR目标的贡献比例（0-1） | 0.3（30%） |
| `--json`, `-j` | 以JSON格式输出结果 | 否 |
| `--metrics`, `-m` | 以JSON字符串形式提供指标数据 | 示例指标 |

### 输出示例

#### 仪表盘输出（以“增长”战略为例）

```
============================================================
OKR CASCADE DASHBOARD
Quarter: Q1 2025  |  Strategy: GROWTH
Teams: Growth, Platform, Mobile, Data  |  Product Contribution: 30%
============================================================

🏢 COMPANY OKRS
📌 CO-1: Accelerate user acquisition and market expansion
   └─ CO-1-KR1: Increase MAU from 100,000 to 150,000
   └─ CO-1-KR2: Achieve 50% MoM growth rate
   └─ CO-1-KR3: Expand to 3 new markets

📌 CO-2: Achieve product-market fit in new segments
📌 CO-3: Build sustainable growth engine

🚀 PRODUCT OKRS
📌 PO-1: Build viral product features and market expansion
   ↳ Supports: CO-1
   └─ PO-1-KR1: Increase product MAU to 45,000
   └─ PO-1-KR2: Achieve 45% feature adoption rate

👥 TEAM OKRS
Growth Team:
  📌 GRO-1: Build viral product features through acquisition and activation
     └─ GRO-1-KR1: Increase product MAU to 11,250
     └─ GRO-1-KR2: Achieve 11.25% feature adoption rate

🎯 ALIGNMENT SCORES
✓ Vertical Alignment: 100.0%
! Horizontal Alignment: 75.0%
✓ Coverage: 100.0%  |  ✓ Balance: 97.5%  |  ✓ Overall: 94.0%
✅ Overall alignment is GOOD (≥80%)
```

#### JSON输出（以“留存”战略为例，部分内容已截断）

```json
{
  "quarter": "Q1 2025",
  "strategy": "retention",
  "company": {
    "objectives": [
      {
        "id": "CO-1",
        "title": "Create lasting customer value and loyalty",
        "key_results": [
          { "id": "CO-1-KR1", "title": "Improve retention from 70% to 85%", "current": 70, "target": 85 }
        ]
      }
    ]
  },
  "product": { "contribution": 0.3, "objectives": ["..."] },
  "teams": ["..."],
  "alignment_scores": {
    "vertical_alignment": 100.0, "horizontal_alignment": 75.0,
    "coverage": 100.0, "balance": 97.5, "overall": 94.0
  }
}
```

完整示例请参阅 `references/examples/sample_growth_okrs.json`。

---

## 参考文档

| 文档 | 描述 |
|----------|-------------|
| `references/okr_framework.md` | OKR制定方法、编写指南及协调性评估标准 |
| `references/strategy_types.md` | 五种战略类型的详细说明及示例 |
| `references/examples/sample_growth_okrs.json` | “增长”战略的完整输出示例 |

---

## 最佳实践

### OKR级联规则

- 每个层级的目标数量控制在3-5个，每个目标包含3-5个关键成果 |
- 关键成果必须能够用当前数据和目标值进行量化 |
- 在最终确定目标之前，需验证层级间的关联关系（父目标与子目标之间的关系） |

### 协调一致性评估

- 总体协调性目标应超过80%；若低于60%，需查明原因 |
- 通过平衡各团队的得分来确保没有团队负担过重 |
- 横向协调性有助于避免团队间目标冲突 |

### 团队配置建议

- 根据实际组织结构配置团队 |
- 根据团队规模调整各团队的贡献比例 |
- 平台/基础设施团队通常需要支持所有战略目标 |
- 专业团队（如机器学习、数据团队）只需支持与其职责相关的目标 |

---
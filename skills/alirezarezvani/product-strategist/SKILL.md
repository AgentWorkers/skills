---
name: product-strategist
description: 面向产品负责人的战略产品领导力工具包，涵盖OKR目标分解、市场分析、愿景设定以及团队规模管理等功能。适用于战略规划、目标对齐、竞争分析及组织架构设计等场景。
---

# 产品策略师

这是一套专为产品负责人设计的战略工具包，旨在帮助推动公司愿景的实现、确保团队目标的一致性，并提升组织效能。

---

## 目录

- [快速入门](#quick-start)
- [核心功能](#core-capabilities)
- [工作流程：战略规划会议](#workflow-strategic-planning-session)
- [OKR级联生成器](#okr-cascade-generator)
  - [使用方法](#usage)
  - [配置选项](#configuration-options)
  - [输入/输出示例](#inputoutput-examples)
- [参考文档](#reference-documents)

---

## 快速入门

### 为团队生成OKR

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

## 核心功能

| 功能 | 描述 | 工具 |
|------------|-------------|------|
| **OKR级联** | 从公司层面自动生成到团队层面的OKR | `okr_cascade_generator.py` |
| **一致性评分** | 测量纵向和横向的一致性 | 内置在生成器中 |
| **战略模板** | 5种预构建的战略类型 | 成长、留存、收入、创新、运营 |
| **团队配置** | 根据您的组织结构进行定制 | `--teams` 标志 |

---

## 工作流程：战略规划会议

本指南详细介绍了如何进行季度战略规划会议。

### 第1步：确定战略重点

根据公司优先级选择主要的战略类型：

| 战略 | 适用场景 |
|----------|-------------|
| **成长** | 扩大用户基础、市场扩张 |
| **留存** | 降低客户流失率、提高客户生命周期价值（LTV） |
| **收入** | 提高平均收入（ARPU）、探索新的盈利模式 |
| **创新** | 市场差异化、开发新功能 |
| **运营** | 提高效率、优化运营流程 |

有关每种战略的详细指导，请参阅 `references/strategy_types.md`。

### 第2步：收集输入数据

收集当前的数据指标，以制定OKR目标：

```bash
# Example metrics JSON
{
  "current": 100000,      # Current MAU
  "target": 150000,       # Target MAU
  "current_nps": 40,      # Current NPS
  "target_nps": 60        # Target NPS
}
```

### 第3步：配置团队结构

定义将接收级联OKR的团队：

```bash
# Default teams
python scripts/okr_cascade_generator.py growth

# Custom teams for your organization
python scripts/okr_cascade_generator.py growth --teams "Core,Platform,Mobile,AI"
```

### 第4步：生成OKR级联

运行生成器以创建一致的OKR：

```bash
python scripts/okr_cascade_generator.py growth --contribution 0.3
```

### 第5步：检查一致性评分

查看输出结果中的一致性评分：

| 评分 | 目标 | 措施 |
|-------|--------|--------|
| 纵向一致性 | >90% | 确保所有目标都与上级目标相关联 |
| 横向一致性 | >75% | 检查团队间的协作情况 |
| 覆盖范围 | >80% | 确保所有公司OKR都得到体现 |
| 平衡性 | >80% | 如果某个团队负担过重，需重新分配任务 |
| **总体** | **>80%** | 一致性良好；<60% 需调整团队分配 |

### 第6步：优化和验证

在最终确定之前：
- [ ] 与相关方审查生成的OKR目标 |
- [ ] 根据团队能力调整任务分配 |
- [ ] 确认各团队的贡献百分比是否合理 |
- [ ] 确保团队之间没有目标冲突 |
- [ ] 设定跟踪频率（每两周检查一次）

### 第7步：导出和跟踪

将OKR导出到您的跟踪系统中：

```bash
# JSON for tools like Lattice, Ally, Workboard
python scripts/okr_cascade_generator.py growth --json > q1_okrs.json
```

---

## OKR级联生成器

该工具可自动将公司层面的OKR向下级团队级联，并跟踪各层级的执行情况。

### 使用方法

```bash
python scripts/okr_cascade_generator.py [strategy] [options]
```

**战略类型：**
- **成长**：用户获取和市场扩张 |
- **留存**：提升客户价值和降低流失率 |
- **收入**：增加收入和探索新的盈利方式 |
- **创新**：产品差异化和市场领导力 |
- **运营**：提高运营效率和组织效能 |

### 配置选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--teams`, `-t` | 以逗号分隔的团队名称 | Growth, Platform, Mobile, Data |
| `--contribution`, `-c` | 团队对公司OKR的贡献百分比（0-1） | 0.3（30%） |
| `--json`, `-j` | 以JSON格式输出而非仪表盘显示 | False |
| `--metrics`, `-m` | 以JSON字符串形式提供指标 | 示例指标 |

**示例：**

```bash
# Custom teams
python scripts/okr_cascade_generator.py retention \
  --teams "Engineering,Design,Data,Growth"

# Higher product contribution
python scripts/okr_cascade_generator.py revenue --contribution 0.4

# Full customization
python scripts/okr_cascade_generator.py innovation \
  --teams "Core,Platform,ML" \
  --contribution 0.5 \
  --json
```

### 输入/输出示例

#### 示例1：成长战略（仪表盘输出）

**命令：**
```bash
python scripts/okr_cascade_generator.py growth
```

**输出：**
```
============================================================
OKR CASCADE DASHBOARD
Quarter: Q1 2025
Strategy: GROWTH
Teams: Growth, Platform, Mobile, Data
Product Contribution: 30%
============================================================

🏢 COMPANY OKRS

📌 CO-1: Accelerate user acquisition and market expansion
   └─ CO-1-KR1: Increase MAU from 100000 to 150000
   └─ CO-1-KR2: Achieve 150000% MoM growth rate
   └─ CO-1-KR3: Expand to 150000 new markets

📌 CO-2: Achieve product-market fit in new segments
   └─ CO-2-KR1: Reduce CAC by 150000%
   └─ CO-2-KR2: Improve activation rate to 150000%
   └─ CO-2-KR3: Increase MAU from 100000 to 150000

📌 CO-3: Build sustainable growth engine
   └─ CO-3-KR1: Achieve 150000% MoM growth rate
   └─ CO-3-KR2: Expand to 150000 new markets
   └─ CO-3-KR3: Reduce CAC by 150000%

🚀 PRODUCT OKRS

📌 PO-1: Build viral product features and market expansion
   ↳ Supports: CO-1
   └─ PO-1-KR1: Increase product MAU from 100000 to 45000.0
   └─ PO-1-KR2: Achieve 45000.0% feature adoption rate

📌 PO-2: Validate product hypotheses in new segments
   ↳ Supports: CO-2
   └─ PO-2-KR1: Reduce product onboarding efficiency by 45000.0%
   └─ PO-2-KR2: Improve activation rate to 45000.0%

📌 PO-3: Create product-led growth loops engine
   ↳ Supports: CO-3
   └─ PO-3-KR1: Achieve 45000.0% feature adoption rate
   └─ PO-3-KR2: Expand to 45000.0 new markets

👥 TEAM OKRS

Growth Team:
  📌 GRO-1: Build viral product features through acquisition and activation
     └─ GRO-1-KR1: [Growth] Increase product MAU from 100000 to 11250.0
     └─ GRO-1-KR2: [Growth] Achieve 11250.0% feature adoption rate

Platform Team:
  📌 PLA-1: Build viral product features through infrastructure and reliability
     └─ PLA-1-KR1: [Platform] Increase product MAU from 100000 to 11250.0
     └─ PLA-1-KR2: [Platform] Achieve 11250.0% feature adoption rate


📊 ALIGNMENT MATRIX

Company → Product → Teams
----------------------------------------

CO-1
  ├─ PO-1
    └─ GRO-1 (Growth)
    └─ PLA-1 (Platform)

CO-2
  ├─ PO-2

CO-3
  ├─ PO-3


🎯 ALIGNMENT SCORES
----------------------------------------
✓ Vertical Alignment: 100.0%
! Horizontal Alignment: 75.0%
✓ Coverage: 100.0%
✓ Balance: 97.5%
✓ Overall: 94.0%

✅ Overall alignment is GOOD (≥80%)
```

#### 示例2：JSON输出

**命令：**
```bash
python scripts/okr_cascade_generator.py retention --json
```

**输出（部分内容）：**
```json
{
  "quarter": "Q1 2025",
  "strategy": "retention",
  "company": {
    "level": "Company",
    "objectives": [
      {
        "id": "CO-1",
        "title": "Create lasting customer value and loyalty",
        "owner": "CEO",
        "key_results": [
          {
            "id": "CO-1-KR1",
            "title": "Improve retention from 100000% to 150000%",
            "current": 100000,
            "target": 150000
          }
        ]
      }
    ]
  },
  "product": {
    "level": "Product",
    "contribution": 0.3,
    "objectives": [...]
  },
  "teams": [...],
  "alignment_scores": {
    "vertical_alignment": 100.0,
    "horizontal_alignment": 75.0,
    "coverage": 100.0,
    "balance": 97.5,
    "overall": 94.0
  },
  "config": {
    "teams": ["Growth", "Platform", "Mobile", "Data"],
    "product_contribution": 0.3
  }
}
```

请参阅 `references/examples/sample_growth_okrs.json` 以获取完整的示例。

---

## 参考文档

| 文档 | 描述 |
|----------|-------------|
| `references/okr_framework.md` | OKR方法论、编写指南、一致性评分标准 |
| `references/strategy_types.md` | 5种战略类型的详细说明及示例 |
| `references/examples/sample_growth_okrs.json` | 成长战略的完整示例输出 |

---

## 最佳实践

### OKR级联

- 每个层级的目标数量控制在3-5个以内 |
- 每个目标应包含3-5个可衡量的关键结果 |
- 在最终确定前验证层级间的目标关系 |

### 一致性评分

- 总体一致性评分应超过80% |
- 对评分低于60%的情况进行调查 |
- 确保团队间的任务分配平衡，避免任务过重 |
- 横向一致性有助于避免目标冲突 |

### 团队配置

- 根据实际组织结构配置团队 |
- 根据团队规模调整贡献百分比 |
- 平台/基础设施团队通常需要支持所有目标 |
- 专业团队（如机器学习、数据团队）可能只需支持相关目标 |

---

## 快速参考

```bash
# Common commands
python scripts/okr_cascade_generator.py growth               # Default growth
python scripts/okr_cascade_generator.py retention            # Retention focus
python scripts/okr_cascade_generator.py revenue -c 0.4       # 40% contribution
python scripts/okr_cascade_generator.py growth --json        # JSON export
python scripts/okr_cascade_generator.py growth -t "A,B,C"    # Custom teams
```
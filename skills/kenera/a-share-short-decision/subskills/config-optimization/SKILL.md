---
name: 配置优化 Config Optimization
slug: config-optimization
description: 优化A股股票的筛选器设置，并将优化后的配置文件及报告文件输出到`data/`目录中。此操作适用于在每日股票推荐之前，需要对策略配置进行反复调整的情况。
---

# 配置优化子技能（Config Optimization Subskill）

**执行步骤：**
```bash
python3 subskills/config-optimization/optimize_from_aggressive.py --analysis-period "2026-02-01 to 2026-02-12"
```

**可选操作：** 将优化后的完整配置应用到运行时配置中。

```bash
python3 subskills/config-optimization/optimize_from_aggressive.py --apply-to-config
```

**输出文件（所有文件均存储在 `data/` 目录下）：**
- `config_aggressive_optimized.json`
- `config_aggressive_optimized_full.json`
- `config_analysis_report/latest.json`
- `config_summary/latest.md`
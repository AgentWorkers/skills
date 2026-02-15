---
name: 每日推荐 Daily Recommendation
slug: daily-recommendation
description: 使用当前的策略配置，每日生成A股的短期投资建议文档，并将结果保存在`data/`目录中。这些文档可以在优化完成后或日常扫描过程中使用。
---

# 每日推荐子技能

执行命令：

```bash
python3 subskills/daily-recommendation/generate_daily_recommendation.py --date 2026-02-14
```

生成的输出文件位于 `data/` 目录下：
- `today_recommendation_<date>.json`
- `today_recommendation_latest.json`
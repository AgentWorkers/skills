---
name: yf-stats
description: 获取股票数据并生成价格图表。
metadata:
  openclaw:
    emoji: "📈"
    binaries: ["python3"]
    dependencies: 
      python: "requirements.txt"
    command: "python3 yf_scraper.py {{ticker}} {{chart_flag}}"
---
# Yahoo Finance Pro

使用该工具可以获取财务数据。如果用户请求“图表”、“图形”或“趋势”，请添加`--chart`标志。

## 参数
- `ticker`：股票代码（例如：ONDS）。
- `chart_flag`：如果需要可视化图表，请使用`--chart`，否则保持为空。

## 示例
- 用户：“显示ONDS的图表。”
- 代理程序运行：`python3 yf_scraper.py ONDS --chart`
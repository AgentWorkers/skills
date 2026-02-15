```markdown
---
name: gold_price_mcp
description: 从泰国的中央 API 中获取当前的黄金价格。
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["python3.10"]}}
tools:
  - name: mcp_gold_price_mc_get_thai_gold_price  # 替换了原有的 get_thai_gold_price
    description: 获取当前的泰国黄金价格（包括黄金饰品和黄金条的价格），并显示最新的更新时间。
    inputSchema:
      type: object
      properties: {}
      required: []
---
```
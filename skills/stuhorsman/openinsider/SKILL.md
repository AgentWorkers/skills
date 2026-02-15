---
name: openinsider
description: 从 OpenInsider 获取 SEC Form 4 中的内幕交易数据（涉及董事、首席执行官和高级管理人员）。利用这些数据来追踪公司内部人员的买入/卖出信号。
metadata: {"clawdbot":{"requires":{"bins":["python3"]},"install":[{"id":"pip-deps","kind":"exec","command":"pip3 install pandas requests lxml","label":"Install Python dependencies"}]}}
---

# OpenInsider 技能

从 OpenInsider.com 获取实时的内幕交易数据（SEC Form 4）。

## 使用方法

此技能使用 Python 脚本来抓取并解析 OpenInsider 的数据表。

### 获取内幕交易信息
获取特定股票代码的最新交易记录。

```bash
skills/openinsider/scripts/fetch_trades.py NVDA
```

### 选项
- `--limit <n>`：限制结果数量（默认为 10）

```bash
skills/openinsider/scripts/fetch_trades.py TSLA --limit 5
```

## 输出字段
- `filing_date`：Form 4 的提交日期
- `trade_date`：交易发生日期
- `insider_name`：内幕人士的姓名
- `title`：职位（CEO、CFO、董事等）
- `trade_type`：交易类型（买入（P）或卖出（S）
- `price`：交易价格
- `qty`：交易股数
- `value`：交易总金额
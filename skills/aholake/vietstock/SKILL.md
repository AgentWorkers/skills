---
name: fireant-stock
description: 在 FireAnt.vn 上实现越南股票价格和指数的自动化查询功能。该功能可用于查看越南股票（如 HOSE、HNX、UPCOM）及市场指数（如 VNINDEX、HNX30、VN30）的当前价格、交易量或财务信息。支持输入股票代码（如 DPM、VCB、FPT）或指数名称。查询结果会以格式化的方式呈现，包括价格/指数数据、市场统计信息以及关键财务指标。
---
# FireAnt 股票价格查询工具

## 概述

该工具可自动从 FireAnt.vn 网站获取越南股票的实时信息，涵盖从搜索到数据提取及格式化的整个流程。

## 快速入门

- **查询单只股票：**
  ```python
  ```bash
scripts/check_stock.py DPM
```
  ```
- **查询多只股票：**
  ```python
  ```bash
scripts/check_stock.py VCB FPT BID
```
  ```

## 核心工作流程

1. **搜索**：使用 Google 搜索功能找到目标股票的 FireAnt 页面。
2. **导航**：通过浏览器自动化技术打开该股票页面。
3. **提取数据**：解析股票的当前价格、成交量、市值等关键信息。
4. **格式化数据**：将提取到的数据以易于阅读的格式返回。

## 支持的数据类型

### 股票数据：
- **当前价格**：实时价格及价格变动百分比
- **交易数据**：成交量、交易金额、开盘价/最高价/最低价
- **市场指标**：市值、贝塔系数、市盈率、参考价格
- **技术分析**：移动平均线（MA10、MA50）
- **公司信息**：公司全称、上市交易所

### 指数数据（VNINDEX、HNX30 等）：
- **指数当前值**：实时指数值及指数变动百分比
- **交易数据**：总成交量、成交金额
- **外资交易**：外国投资者的买卖活动及净持仓情况
- **技术分析**：移动平均线（MA10、MA50）
- **市场概况**：参考价格、开盘价、最高价/最低价区间

## 使用场景

- **查询单只股票**：
  “查询 DPM 股票的价格”
  “VCB 的当前价格是多少？”
- **查询多只股票**：
  “比较 VCB、BID 和 CTG 的价格”
  “显示 VCB、BID 和 CTG 的股票信息”
- **查询指数**：
  “查询 VNINDEX”
  “今天的市场表现如何？”
  “显示 VN30 指数的情况”
- **混合查询**：
  “查询 ACB、L18、AAA 和 VNINDEX 的信息”
  “显示 FPT、VNM 和 VNINDEX 的股票及指数数据”
- **市场研究**：
  “在 FireAnt 上查找关于 DPM 股票的信息”
  “获取 FPT 的最新交易数据”

## 脚本

### scripts/check_stock.py

该脚本用于自动化查询一只或多只股票（或指数）的完整流程。

**使用方法：**
```bash
python3 scripts/check_stock.py <股票代码1> <股票代码2> ...
```

**示例：**
```bash
# Check stocks
python3 scripts/check_stock.py ACB VCB FPT

# Check index
python3 scripts/check_stock.py VNINDEX

# Check mixed
python3 scripts/check_stock.py ACB L18 AAA VNINDEX
```

**返回结果：** 格式化后的股票/指数数据，包括价格/指数值、成交量及关键指标。

**注意：** FireAnt 的 URL 格式对股票和指数都是统一的：`https://fireant.vn/ma-chung-khoan/{股票代码}`
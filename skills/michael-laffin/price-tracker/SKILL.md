---
name: price-tracker
description: 监控亚马逊（Amazon）、易贝（eBay）、沃尔玛（Walmart）和百思买（Best Buy）上的产品价格，以发现套利机会和利润率。该功能可用于寻找适合转售的产品、监控竞争对手的价格、追踪价格历史、识别套利机会，或设置自动价格警报。
---

# 价格追踪器

## 概述

该工具可追踪多个电商平台上的产品价格，帮助用户发现套利机会、计算利润率，并确定最佳的买入/卖出时机。通过该技能，您可以实现自动价格监控、历史价格追踪以及基于收益的决策制定。

## 核心功能

### 1. 产品发现与监控

- **搜索并追踪产品**：  
  - 可通过关键词在 Amazon、eBay、Walmart、Best Buy 等平台上搜索产品  
  - 将产品添加到监控列表中  
  - 设置目标价格阈值  
  - 配置警报频率（每小时、每天、每周）  

**示例请求**：  
  “监控 Amazon 和 eBay 上 iPhone 15 Pro 的价格。如果价格降至 800 美元以下，或者 eBay 上的价格比 Amazon 便宜 150 美元以上，请发送警报。”  

### 2. 套利分析

- **跨平台价格比较**：  
  - 比较同一产品在各个平台上的价格  
  - 计算扣除费用和运费后的利润率  
  - 识别具有较高利润空间的产品（成本后的利润率超过 20%）  
  - 考虑平台费用、运费及税费  

**费用结构参考**：  
  - Amazon：约 15% 的推荐费  
  - eBay：约 13% 的最终成交费用 + 列表费用  
  - Walmart：约 8-15% 的推荐费  

**示例请求**：  
  “查找 eBay 上价格比 Amazon 高出 20% 以上的 Nintendo Switch 套装，同时考虑所有费用和运费。”  

### 3. 历史价格追踪

- **价格历史记录**：  
  - 追踪产品价格随时间的变化（30 天、60 天、90 天）  
  - 识别价格波动规律  
  - 发现价格操纵或限时促销活动  
  - 导出历史数据以供分析  

**示例请求**：  
  “显示 AirPods Pro 2 过去 60 天的价格历史记录，并确定最佳购买时机。”  

### 4. 自动警报

- **警报配置**：  
  - 价格下跌警报  
  - 套利机会警报  
  - 竞品价格变化警报  
  - 批量产品监控  

**示例请求**：  
  “为所有 Sony 电视型号设置警报。如果某个型号的价格降至 400 美元以下或存在 25% 以上的套利空间，请发送警报。”  

## 快速入门

### 追踪单个产品  
```python
# Use scripts/track_product.py
python3 scripts/track_product.py \
  --product "Apple iPhone 15 Pro 256GB" \
  --platforms amazon,ebay \
  --alert-below 800 \
  --alert-margin 0.20
```  

### 从 CSV 文件批量监控产品  
```python
# Use scripts/bulk_monitor.py
python3 scripts/bulk_monitor.py \
  --csv products.csv \
  --margin-threshold 0.25 \
  --alert-frequency daily
```  

### 价格比较报告  
```python
# Use scripts/compare_prices.py
python3 scripts/compare_prices.py \
  --keyword "Sony WH-1000XM5" \
  --platforms amazon,ebay,walmart,bestbuy \
  --report markdown
```  

## 工作流程

### 套利机会发现

1. 在高需求类别（电子产品、游戏、家居用品）中搜索产品  
2. 使用 `compare_prices.py` 在所有平台上比较价格  
3. 计算扣除费用/运费/税费后的净利润  
4. 筛选利润率超过 20% 的产品  
5. 核实产品状况和卖家信誉  
6. 执行购买操作或设置价格下跌的监控  

### 价格下跌监控

1. 确定目标产品（心愿单中的产品或季节性折扣商品）  
2. 使用 `track_product.py` 设置警报阈值  
3. 监控历史价格走势以预测最佳购买时机  
4. 当价格低于阈值时采取行动  
5. 在季节性购物活动（如 Prime Day、Black Friday）期间重复此过程  

## 脚本

### `track_product.py`  
用于在多个平台上追踪单个产品，并支持自定义警报设置。  

**参数**：  
- `--product`：产品名称/关键词  
- `--platforms`：用逗号分隔的电商平台（amazon, ebay, walmart, bestbuy）  
- `--alert-below`：价格低于此金额时触发警报  
- `--alert-margin`：套利利润率超过此比例时触发警报（例如 0.20 表示 20%）  
- `--frequency`：检查频率（每小时、每天、每周）  
- `--output`：输出格式（json、csv、markdown）  

**示例**：  
```bash
python3 scripts/track_product.py \
  --product "Samsung Galaxy S24 Ultra 256GB" \
  --platforms amazon,ebay,walmart \
  --alert-below 900 \
  --alert-margin 0.25 \
  --frequency daily \
  --output markdown
```  

### `compare_prices.py`  
用于比较多个平台上同一产品的价格。  

**参数**：  
- `--keyword`：产品搜索关键词  
- `--platforms`：用逗号分隔的电商平台（默认：所有平台）  
- `--report`：报告格式（markdown、json、csv）  
- `--sort-by`：按价格、利润率或评分排序  
- `--min-rating`：最低卖家评分  

**示例**：  
```bash
python3 scripts/compare_prices.py \
  --keyword "PlayStation 5 Slim" \
  --platforms amazon,ebay,walmart,bestbuy \
  --report markdown \
  --sort-by margin \
  --min-rating 4.5
```  

### `bulk_monitor.py`  
用于从 CSV 文件中批量监控产品。  

**CSV 格式**：  
```csv
product,platforms,alert_below,alert_margin
"Apple MacBook Air M3 256GB",amazon,ebay,walmart,899,0.20
"Sony PlayStation 5",amazon,ebay,399,0.25
"Dyson V15 Detect",amazon,walmart,bestbuy,500,0.18
```  

**参数**：  
- `--csv`：CSV 文件路径  
- `--margin-threshold`：报告的最低利润率  
- `--alert-frequency`：警报发送频率  
- `--output`：警报输出文件  

**示例**：  
```bash
python3 scripts/bulk_monitor.py \
  --csv products.csv \
  --margin-threshold 0.20 \
  --alert-frequency daily \
  --output alerts.txt
```  

### `price_history.py`  
用于检索和分析历史价格数据。  

**参数**：  
- `--product`：产品名称/关键词  
- `--days`：历史数据天数（默认：30 天）  
- `--platform`：特定电商平台（可选）  
- `--output`：输出格式（markdown、json、csv）  
- `--trend-analysis`：包含价格趋势分析和预测  

**示例**：  
```bash
python3 scripts/price_history.py \
  --product "AirPods Pro 2" \
  --days 60 \
  --trend-analysis \
  --output markdown
```  

## 最佳实践

### 套利利润计算  

务必计算净利润：  
```
Net Profit = (Sell Price - Buy Price)
            - Platform Fees
            - Shipping Costs
            - Payment Processing Fees
            - Taxes
```  

**推荐的最低利润率**：20-25%，以考虑以下因素：  
- 意外的运输延误  
- 退货/退款  
- 市场价格波动  
- 货币的时间价值  

### 风险管理  

1. **核实卖家信誉**：查看评分和评论  
2. **检查产品状况**：新商品、翻新商品或二手商品  
3. **考虑退货政策**：不同平台的退货政策各不相同  
4. **监控价格稳定性**：价格波动会增加风险  
5. **避免过度依赖单一套利机会**  

### 季节性销售规律  

- **第四季度（10-12 月）**：电子产品销售旺季  
- **1 月**：节后清仓  
- **Prime Day（7 月）**：亚马逊专属优惠  
- **Black Friday/Cyber Monday**：跨平台折扣  
- **返校季（8-9 月）**：笔记本电脑、平板电脑、配件热销  

## 自动化集成  

### 设置 Cron 作业以实现自动监控  

```bash
# Check prices every 6 hours
0 */6 * * * /path/to/price-tracker/scripts/bulk_monitor.py --csv products.csv --output alerts.txt

# Daily arbitrage scan
0 9 * * * /path/to/price-tracker/scripts/compare_prices.py --keyword "high-demand-products" --report markdown >> /path/to/reports.txt
```  

### 与通知系统集成  

与通知系统（如电子邮件、Discord、Telegram）结合使用，以便在发现套利机会时实时接收警报。  

## 限制因素  

- 平台 API 的请求频率限制可能影响搜索效率  
- 实时价格可能存在轻微延迟  
- 部分平台禁止数据抓取（请遵守服务条款）  
- 卖家库存变化较快  

---

**收益至上，智能追踪，快速操作。**
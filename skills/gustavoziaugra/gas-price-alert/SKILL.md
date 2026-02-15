---
name: gas-price-alert
description: **功能概述：**  
该工具用于查找并监控汽油价格，并提供每日价格更新通知。适用于在特定区域内寻找最便宜的汽油、追踪Costco等折扣加油站，或设置每日汽油价格提醒。支持美国境内的任意地点，用户可自定义搜索半径和所需的燃料类型。  

**使用场景：**  
- 在特定区域内寻找最便宜的汽油；  
- 监控Costco等折扣加油站的汽油价格变化；  
- 设置每日汽油价格提醒，以便及时了解价格动态。  

**技术特性：**  
- 支持美国境内的任意地点；  
- 允许用户自定义搜索半径；  
- 支持多种燃料类型（如普通汽油、乙醇汽油等）；  
- 提供每日价格更新通知，帮助用户及时掌握价格信息。
---

# 汽油价格提醒

## 概述

自动搜索您所在地区最便宜的汽油价格，重点关注Costco及其他折扣加油站。每天会在指定范围内推送最佳价格的通知。

## 快速入门

1. **配置位置** - 设置您的城市/坐标和搜索半径
2. **执行搜索** - 查找加油站及预估价格
3. **设置每日提醒** - 每天早上接收最便宜加油站的通知
4. **优先选择Costco** - Costco的汽油价格通常比市场平均价格低0.15-0.25美元

## 工作流程

### 第一步：配置您的位置

**选项A：使用邮政编码（推荐）**

```bash
# Search by ZIP code
python3 scripts/gas_alternative.py --zip 43215 --radius 20 --fuel 87 --summary
```

**选项B：使用坐标**

俄亥俄州哥伦布市的默认位置已预先配置：

```bash
# Columbus, OH (downtown)
lat: 39.9612
lon: -82.9988
radius: 20 miles
```

要使用其他位置，请执行以下操作：

```bash
python3 scripts/gas_alternative.py --lat <latitude> --lon <longitude> --radius <miles>
```

**美国常见城市：**
- 俄亥俄州哥伦布市：39.9612, -82.9988
- 伊利诺伊州芝加哥市：41.8781, -87.6298
- 纽约州纽约市：40.7128, -74.0060
- 加利福尼亚州洛杉矶市：34.0522, -118.2437
- 佛罗里达州迈阿密市：25.7617, -80.1918

### 第二步：搜索加油站

```bash
# Search with summary output
python3 scripts/gas_alternative.py --lat 39.9612 --lon -82.9988 --radius 20 --fuel 87 --summary

# Save to file
python3 scripts/gas_alternative.py --lat 39.9612 --lon -82.9988 --radius 20 --fuel 87 --output gas_prices.json
```

**参数：**
- `--zip`：邮政编码（会覆盖经纬度参数，例如：`--zip 43215`）
- `--lat`：纬度（默认值：39.9612 - 俄亥俄州哥伦布市）
- `--lon`：经度（默认值：-82.9988 - 俄亥俄州哥伦布市）
- `--radius`：搜索半径（单位：英里，默认值：20）
- `--fuel`：燃料类型（87、89、91、柴油，默认值：87）
- `--base-price`：价格估算的基准值（默认值：2.89美元）
- `--output`：输出文件（默认值：gas_prices.json）
- `--summary`：将结果以人类可读的格式输出到标准输出

### 第三步：设置每日提醒

使用OpenClaw的cron任务来接收每日早晨的通知：

```json
{
  "name": "Gas price alert",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "America/New_York"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Get me gas prices for Columbus, OH this morning. Focus on Costco and show the cheapest 87 octane within 20 miles of downtown."
  },
  "sessionTarget": "main"
}
```

该任务每天东部时间8点自动执行。

### 第四步：接收通知

系统将：
1. 在您所在地区搜索加油站
2. 筛选出Costco及其他折扣加油站
3. 生成包含最便宜价格信息的摘要
4. 通过Telegram发送通知

**示例通知内容：**

```
⛽ Gas Prices (87 Octane) - Columbus, OH

🏠 Costco (Typically Cheapest)
• Costco Gas
  💰 $2.69 (est.)
  📍 5000 Morse Rd, Columbus, OH 43213 (7.9 miles from downtown)

💡 Tip: Costco typically has gas $0.15-0.25 below market average.
```

## 输出格式

每个加油站的信息包括：

```json
{
  "source": "osm",
  "name": "Costco Gas",
  "brand": "Costco",
  "address": "5000 Morse Rd, Columbus, OH 43213",
  "lat": 39.9667,
  "lon": -82.8500,
  "distance": 7.9,
  "fuel_type": "87",
  "price": 2.69,
  "price_text": "$2.69 (est.)",
  "is_costco": true,
  "scraped_at": "2026-02-10T21:00:00.000Z"
}
```

## 工作原理

1. **OpenStreetMap/Overpass API**：查找该区域内的所有加油站
2. **Costco数据库**：匹配并优先显示Costco的位置
3. **价格估算**：Costco的汽油价格比市场平均价格低0.15-0.25美元
4. **距离计算**：使用测地距离来计算实际行驶里程
5. **智能过滤**：去除重复数据并按相关性排序

## 限制

- **实时价格**：目前使用的是Costco的预估价格。如需查看实时价格，请访问GasBuddy.com或使用加油站的应用程序。
- **覆盖范围**：依赖于OpenStreetMap数据的完整性
- **价格估算的准确性**：Costco的价格是基于其常见的折扣政策进行估算的

## 获取实时价格的方法

- **GasBuddy.com**：手动查询或使用其商业API
- **加油站应用程序**：Costco、Kroger、Shell等加油站都提供实时价格信息
- **AAA**：提供按地区划分的平均价格
- **Waze**：通过社区贡献实时更新价格信息

## 故障排除

### 未找到加油站

- 增加`--radius`参数的值
- 确认坐标是否正确
- 检查该地区是否有完整的OpenStreetMap数据覆盖

### 价格不准确

- 非Costco加油站的价格显示为“N/A”
- Costco的价格是基于其常见的折扣政策进行估算的
- 如需获取实时价格，请使用GasBuddy或加油站的应用程序

### 如果未安装Geopy

```bash
pip install geopy
```

## 资源

### scripts/gas_alternative.py
使用OpenStreetMap和Overpass API搜索加油站的主要脚本。

**功能：**
- 查找指定范围内的所有加油站
- 识别Costco的位置
- 估算Costco的汽油价格
- 计算距离
- 生成易于阅读的摘要

### scripts/gasbuddy_search.py
用于集成GasBuddy的备用脚本（需要Playwright或API密钥）。

**适用场景：**
- 您拥有GasBuddy的API密钥
- 需要实时价格信息
- 希望使用Playwright进行JavaScript渲染

### references/locations.md
包含美国常见城市的坐标和配置信息。

## 依赖项

安装所需软件包：

```bash
pip install requests geopy
```

（如需使用基于Playwright的GasBuddy爬虫功能，请安装以下依赖项：）

```bash
pip install playwright
playwright install
```
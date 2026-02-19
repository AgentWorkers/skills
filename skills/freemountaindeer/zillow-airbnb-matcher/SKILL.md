---
name: zillow-airbnb-matcher
version: 2.0.1
description: 查找那些已经能够通过 Airbnb 产生收入的待售房产。利用地理匹配功能将 Zillow 的房源信息与当前正在通过 Airbnb 出租的房源进行关联，并计算相关的投资指标。
author: em8.io
requires:
  - RAPIDAPI_KEY (get free at rapidapi.com — 100+ free requests/month)
commands:
  - trigger: "search airbnb"
    script: scripts/search.js
    description: Search by ZIP code or city
  - trigger: "check properties"
    script: scripts/search.js
    description: Find STR investment properties
  - trigger: "airbnb demo"
    script: scripts/search.js --demo
    description: Run demo with Austin TX sample data (no API needed)
tags:
  - real-estate
  - airbnb
  - investment
  - short-term-rental
  - zillow
---
# Zillow × Airbnb 信息匹配工具

Alfred 可以利用基于 GPS 的地理匹配技术，查找附近 **同时拥有活跃 Airbnb 列出的待售房产**，从而实现 Zillow 和 Airbnb 数据的交叉查询。

## 使用方法（聊天指令）

向 Alfred 发送以下任意指令：

| 指令 | 功能 |
|---------|-------------|
| `search airbnb 78704` | 在德克萨斯州奥斯汀市（邮政编码 78704）范围内搜索 Airbnb 房产 |
| `search airbnb Nashville TN` | 按城市名称搜索 Airbnb 房产 |
| `check properties 33139` | 检查迈阿密海滩（地址 33139）的房产信息 |
| `airbnb demo` | 运行演示模式（无需使用 API） |
| `search airbnb 78704 max 800000` | 根据价格上限（最高 80 万美元）筛选 Airbnb 房产 |
| `search airbnb 78704 min 3 beds` | 根据卧室数量（至少 3 张床）筛选 Airbnb 房产 |

## 工作原理

1. **Zillow 搜索**：在指定邮政编码范围内查找所有待售房产（约 2 秒）。
2. **Airbnb 搜索**：在同一区域内查找所有活跃的 Airbnb 列出（约 3 秒）。
3. **地理匹配**：根据 GPS 坐标，将 Zillow 和 Airbnb 的房产信息进行匹配（匹配范围为 100–200 米）。
4. **投资分析**：计算房产的资本回报率（Cap Rate）、现金流、抵押贷款金额以及达到盈亏平衡所需的入住率。

⏱️ **每次搜索的总耗时：约 5–10 秒**（RapidAPI 的响应速度非常快）。

## 重要说明

- **收入估算** 基于每晚租金乘以 70% 的入住率。如需精确数据，请使用 AirDNA（每月费用 100 美元）。
- **地理匹配** 表示匹配到的 Airbnb 房产可能属于附近居民，而非完全相同的房屋——请务必核实。
- **免费套餐** 每月可进行 100 次 Airbnb 搜索和 600 次 Zillow 搜索（RapidAPI 免费计划）。
- **免费套餐下的每次搜索费用：0 美元**。

## 设置步骤

1. 获取免费的 RapidAPI 密钥：https://rapidapi.com → 注册（免费，无需信用卡）
2. 订阅以下两个 API（均为免费）：
   - Airbnb：https://rapidapi.com/3b-data-3b-data-default/api/airbnb13
   - Zillow：https://rapidapi.com/SwongF/api/us-property-market1
3. 将密钥添加到 Alfred 的 `.env` 文件中：`RAPIDAPI_KEY=your_key_here`
4. 运行演示模式：`airbnb demo`（无需使用 API）
5. 进行实际测试：`search airbnb 78704`

详细设置步骤请参阅 GUIDE.md 文件。

## 投资指标

该工具可计算以下指标（假设房价下降 20%，租金率为 7.25%，贷款期限为 30 年）：

- **资本回报率（Cap Rate）**：购买房产后的年回报率。
- **实际投资回报（Cash-on-Cash）**：实际投入现金的回报金额。
- **每月现金流**：扣除所有费用后的净收入。
- **回收期（GRM）**：需要多少年才能通过租金收入收回购房成本。
- **盈亏平衡入住率**：达到盈亏平衡所需的最低入住率。

## 投资等级

- 🟢 A 级（优秀）：资本回报率 ≥ 6%，实际投资回报 ≥ 10%，入住率 ≥ 85%。
- 🟡 B 级（良好）：回报稳定，市场风险适中。
- 🟠 C 级（一般）：回报尚可，但利润率较低。
- 🔴 D 级（较差）：除非具有增值潜力，否则不建议投资。
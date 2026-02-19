---
name: zillow-airbnb-matcher
version: 2.0.0
description: 查找那些已经能够通过 Airbnb 产生收入的待售房产。利用地理匹配技术，将 Zillow 上的房源信息与当前正在出租的 Airbnb 房源进行关联，并计算相关的投资指标。
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
# Zillow × Airbnb 匹配器技能

该技能能够查找附近**已有活跃Airbnb房源**的待售房产——通过基于GPS的地理匹配技术，将Zillow和Airbnb的数据进行交叉比对。

## 使用方法（聊天指令）

向您的代理发送以下任意一条消息：

| 消息 | 功能 |
|---------|-------------|
| `search airbnb 78704` | 搜索德克萨斯州奥斯汀市的房产（邮政编码78704） |
| `search airbnb Nashville TN` | 按城市名称搜索 |
| `check properties 33139` | 检查迈阿密海滩地区的房产信息 |
| `airbnb demo` | 运行演示功能（无需API） |
| `search airbnb 78704 max 800000` | 按最高价格范围筛选房产 |
| `search airbnb 78704 min 3 beds` | 按卧室数量筛选房产 |

## 工作原理

1. **Zillow搜索**：在指定邮政编码范围内查找所有待售房产（约2秒）  
2. **Airbnb搜索**：在同一区域内查找所有活跃的Airbnb房源（约3秒）  
3. **地理匹配**：根据GPS坐标将Zillow和Airbnb的房源进行匹配（匹配范围为100-200米）  
4. **投资分析**：计算资本回报率（Cap Rate）、现金流、抵押贷款成本以及达到盈亏平衡点的入住率  

⏱️ **每次搜索的总耗时：约5-10秒**（RapidAPI响应速度很快）  

## 重要说明  

- **收入估算**基于每晚租金乘以70%的入住率得出。如需精确数据，请使用AirDNA服务（每月费用100美元以上）。  
- **地理匹配**意味着匹配到的Airbnb房源可能是附近业主的房产，并非完全相同的房屋——请务必核实。  
- **免费套餐**每月可进行100次Airbnb搜索和600次Zillow搜索（RapidAPI免费计划）。  
- **免费套餐下的每次搜索费用为0美元**。  

## 设置步骤  

1. 获取免费的RapidAPI密钥：https://rapidapi.com → 注册（免费，无需信用卡）  
2. 订阅以下两个API（均为免费）：  
   - Airbnb：https://rapidapi.com/3b-data-3b-data-default/api/airbnb13  
   - Zillow：https://rapidapi.com/SwongF/api/us-property-market1  
3. 将密钥添加到`.env`文件中：`RAPIDAPI_KEY=your_key_here`  
4. 测试功能：`airbnb demo`（无需API）  
5. 实际测试：`search airbnb 78704`  

详细设置步骤及截图请参阅GUIDE-FOR-MATTHEW.md文件。  

## 投资指标  

该工具可计算以下指标（假设房价下跌20%，租金率为7.25%，贷款期限为30年）：  
- **资本回报率（Cap Rate）**：全额购房成本带来的年回报率  
- **实际投资回报（Cash-on-Cash）**：实际投入现金的回报  
- **月现金流（Monthly Cash Flow）**：扣除所有费用后的剩余金额  
- **回收投资年限（GRM）**：需要多少年才能收回购房成本  
- **盈亏平衡入住率（Break-even occupancy）**：为避免亏损所需的最低入住率  

## 投资等级  

- 🟢 A级（优秀）：资本回报率≥6%，实际投资回报≥10%，入住率≥85%  
- 🟡 B级（良好）：回报稳定，市场风险适中  
- 🟠 C级（一般）：回报尚可，但利润率较低  
- 🔴 D级（较差）：除非有增值潜力，否则建议避免投资
---
name: cabin
description: 使用 USDC（Uniswap Decentralized Currency）进行航班搜索和预订。该功能使您的人工智能助手能够查询 500 多家航空公司的航班信息，并完成以 USDC 为支付方式的预订。无需信用卡，也无需银行服务——这是一款完全基于加密货币的旅行商务平台。
metadata: {"clawdbot":{"emoji":"✈️","homepage":"https://github.com/yolo-maxi/cabin","requires":{"bins":["node"]}}}
---

# Cabin — 使用 USDC 进行航班搜索与预订

在 500 多家航空公司中搜索真实航班，并使用 USDC 在 Base 平台上完成预订。

## API 基本 URL

`https://api.cabin.team`

## 终端点

### 搜索航班

当用户想要查找航班时：

**参数：**
- `from`（必填）：出发地 IATA 机场代码
- `to`（必填）：目的地 IATA 机场代码
- `date`（必填）：出发日期（YYYY-MM-DD）
- `return_date`（可选）：往返日期
- `adults`（可选，默认值 1）：乘客人数
- `class`（可选）：ECONOMY、PREMIUM_ECONOMY、BUSINESS、FIRST
- `currency`（可选，默认值 USD）：价格显示的货币
- `max_results`（可选，默认值 10）：最大显示结果数量

**响应包含：**
- `results[]` — 包含航班信息（价格、航空公司、航班时间、中途停留地的数组）
- `image_url` — 显示搜索结果的 PNG 图片链接
- `search_id` — 预订时的参考 ID

**向用户展示结果：**
- 显示图片链接（从 `image_url` 获取）以便直观比较
- 使用结构化数据回答具体问题（例如：“哪个航班最便宜？”、“有直飞航班吗？”）
- 始终同时显示价格（USD 和 USDC 对应金额）

### 预订航班

当用户想要预订航班时：

**必需的乘客信息：**
- `given_name`（名字）
- `family_name`（姓氏）
- `born_on`（出生日期，格式为 YYYY-MM-DD）
- `gender`（性别，m/f）

**响应包含：**
- `booking_id` — 预订参考编号（格式为 CBN-YYYY-XXXX）
- `amount_usdc` — 需支付的 USDC 金额
- `payment.deposit_address` — 在 Base 平台上用于支付的 USDC 存款地址
- `payment.checkout_url` — 可与用户共享的支付页面链接

### USDC 支付流程

预订完成后，用户需要在 Base 平台上使用 USDC 进行支付：
1. 向用户显示 `amount_usdc` 和 `payment.checkout_url`
2. 用户可以选择：
   a. 直接将 USDC 支付到 `payment.deposit_address`
   b. 访问 `payment.checkout_url` 进行引导式支付
3. 支付完成后，预订将自动确认

**如果代理具有钱包功能（例如 evm-wallet 技能）：**

### 查看预订状态

**状态：** 待支付 → 已确认 → 已登机

### 获取确认页面
**在支付确认后，将此链接分享给用户。**

### 获取登机页面
**在需要登机时，将此页面分享给用户。**

## 常见 IATA 代码

| 代码 | 城市 |
|------|------|
| HAN | 河内 |
| BKK | 曼谷 |
| SIN | 新加坡 |
| NRT | 东京成田 |
| HND | 东京羽田 |
| ICN | 首尔 |
| LHR | 伦敦 |
| CDG | 巴黎 |
| FCO | 罗马 |
| ATH | 雅典 |
| JFK | 纽约 |
| LAX | 洛杉矶 |
| SFO | 旧金山 |
| DXB | 迪拜 |
| IST | 伊斯坦布尔 |

## 工作流程示例

### 简单的单程搜索
用户：“帮我查找从曼谷到东京的下周五的航班”
1. 解析参数：`from=BKK, to=NRT`（或 `HND`），`date=next Friday`
2. 调用 POST 请求 `/v1/search`
3. 向用户显示 `image_url`
4. 展示前三到五个航班选项及其价格

### 往返预订
用户：“预订从伦敦到巴塞罗那的最低价往返航班，日期为 3 月 15 日至 22 日”
1. 搜索参数：`from=LHR, to=BCN, date=2026-03-15, return_date=2026-03-22`
2. 显示搜索结果
3. 用户选择航班后，收集乘客信息
4. 调用 POST 请求 `/v1/book` 并提交乘客信息
5. 共享支付页面链接，用户使用 USDC 进行支付
6. 确认预订后，分享确认页面

### 多乘客预订
用户：“我们需要为 3 人预订从首尔到巴厘岛的航班，日期为 4 月 1 日至 10 日”
1. 搜索参数：`adults=3`
2. 显示的价格为每人价格
3. 预订时收集所有乘客的详细信息
4. 总 USDC 金额 = 每人价格 × 3

## 错误处理
- **无结果**：尝试搜索附近的机场或更改日期
- **预订过期**：搜索结果在 30 分钟后失效，请重新搜索
- **支付超时**：未支付的预订在创建后 1 小时内失效
- **无效的机场代码**：提示用户输入正确的 IATA 代码

## 关于 Base 平台上的 USDC
- 平台链：Base（Ethereum L2）
- 代币：USDC（地址：0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913）
- 交易手续费：约 0.01 美元
- 确认时间：约 2 秒
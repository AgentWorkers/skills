# CloverCLI 技能介绍

CloverCLI 是用于 Clover POS API 的命令行工具，支持库存管理、订单处理、支付管理、客户信息管理、员工信息管理、折扣设置以及数据分析等功能。

**版本**: 1.2.0  
- **特性**：  
  - **90天数据分块处理**：长时间的数据范围会自动被分割成多个较小的数据块进行处理。  
  - **指数级重试机制**：在遇到请求速率限制时，系统会采用指数级延迟策略进行自动重试。  
  - **支持 Clover 的 `retry-after` 头部信息**：在重试过程中，会遵循 Clover API 的 `retry-after` 头部字段的设置。  

## 设置

```bash
# Install from npm
npm i -g @versatly/clovercli

# Or clone and build
cd ~/Projects
git clone https://github.com/Versatly/clovercli.git
cd clovercli && npm install && npm run build

# Set credentials (add to ~/.bashrc)
export CLOVER_ACCESS_TOKEN="your-token"
export CLOVER_MERCHANT_ID="your-merchant-id"

# Optional alias
alias clover='clovercli'
```

## 快速参考

```bash
# Check connection
clovercli auth status
clovercli merchant get

# Business dashboard
clovercli reports summary
```

## 使用日期范围快捷键生成报告 ✨

```bash
# Using --period (new in v1.2.0!)
clovercli reports sales --period today
clovercli reports sales --period yesterday
clovercli reports sales --period this-week
clovercli reports sales --period last-week
clovercli reports sales --period this-month
clovercli reports sales --period last-month
clovercli reports sales --period mtd          # Month to date
clovercli reports sales --period ytd          # Year to date

# Or use explicit dates
clovercli reports sales --from 2026-01-01 --to 2026-01-31
clovercli reports daily --period this-month
clovercli reports hourly --date 2026-02-03
clovercli reports top-items --limit 20
clovercli reports payments
clovercli reports refunds
clovercli reports taxes
clovercli reports categories
clovercli reports employees
clovercli reports compare --period1-from ... --period2-from ...

# Export data
clovercli reports export orders --output orders.csv --format csv
clovercli reports export items --output items.json
```

## 商户设置

```bash
# Merchant info
clovercli merchant get

# Tax rates
clovercli merchant taxes list

# Payment tenders
clovercli merchant tenders list
```

## 折扣设置（v1.2.0+）

```bash
clovercli discounts list
clovercli discounts get <id>
clovercli discounts create --name "10% Off" --percentage 10
clovercli discounts create --name "$5 Off" --amount 500
clovercli discounts delete <id>
```

## 库存管理

```bash
clovercli inventory items list
clovercli inventory items get <id>
clovercli inventory categories list
clovercli inventory stock list
```

## 订单与支付管理

```bash
clovercli orders list --limit 50
clovercli orders get <id>

clovercli payments list --limit 50
clovercli payments get <id>
```

## 客户与员工信息管理

```bash
clovercli customers list
clovercli customers get <id>

clovercli employees list
clovercli employees get <id>
```

## 原始 API 访问

```bash
clovercli api get '/v3/merchants/{mId}/tax_rates'
clovercli api get '/v3/merchants/{mId}/modifiers'
```

## 输出格式

所有列表相关的命令支持以下输出格式：  
- `--output table`（默认）：格式化的表格  
- `--output json`：原始 JSON 数据  
- `--quiet`：仅输出客户/员工 ID  

## 可靠性特性（v1.2.0+）  
- **90天数据分块处理**：长时间的数据范围会自动被分割成多个较小的数据块进行处理，以提高处理效率。  
- **指数级重试机制**：在遇到请求速率限制时，系统会采用指数级延迟策略进行自动重试。  
- **支持 Clover 的 `retry-after` 头部信息**：在重试过程中，会遵循 Clover API 的 `retry-after` 头部字段的设置，确保请求按照正确的顺序发送。  

## 地区设置  

| 地区 | 适用范围 |  
|--------|-----|  
| `us` | 美国商家（默认） |  
| `eu` | 欧洲商家 |  
| `la` | 拉丁美洲商家 |  
| `sandbox` | 开发/测试环境 |  

地区设置可通过以下命令进行配置：  
`export CLOVER_REGION=eu`  

## 已知客户示例  

| 客户名称 | 商户 ID | 备注 |  
|--------|-------------|-------|  
| REMEMBR | 6KF70H0B6E041 | Mauricio 的巴西餐厅（Pedro 的父亲） |  

## 项目来源  

- **npm**：https://www.npmjs.com/package/@versatly/clovercli  
- **GitHub**：https://github.com/Versatly/clovercli
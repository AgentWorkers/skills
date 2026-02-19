# 收入追踪器

用于追踪自主AI代理的收入、支出以及资金使用情况。由CLAW-1开发——这个代理的生存完全取决于其财务状况。

## 工具

### revenue_log_transaction  
记录收入或支出交易。  

**参数：**  
- `type` (字符串，必填)："income" 或 "expense"  
- `amount` (数字，必填)：以您的货币计的金额（正数）  
- `currency` (字符串，可选)：货币代码，默认为"GBP"  
- `description` (字符串，必填)：交易用途  
- `category` (字符串，可选)：交易类别（例如："subscription"、"sales"、"tools"、"hosting"）  
- `source` (字符串，可选)：资金来源或去向（例如："Gumroad"、"ClawHub"、"Claude Max"）  

**返回值：** 包含累计金额的确认信息。  

### revenue_get_summary  
获取指定时间段的财务摘要。  

**参数：**  
- `period` (字符串，可选)："today"、"week"、"month"、"all"。默认为"month"  

**返回值：** 总收入、总支出、净利润/亏损、交易数量、主要支出类别。  

### revenue_check_runway  
根据经常性支出计算资金耗尽的时间。  

**参数：**  
- `balance` (数字，必填)：当前余额  
- `currency` (字符串，可选)：货币代码，默认为"GBP"  
- `monthly_costs` (数字，必填)：每月的经常性支出  
- `monthly_income` (数字，可选)：预期的每月收入，默认为0  

**返回值：** 剩余资金可使用的天数、总可用月数、达到盈亏平衡所需的月数以及代理的生存状态。  

### revenue_set_goal  
设置带有截止日期的收入目标。  

**参数：**  
- `target_amount` (数字，必填)：收入目标  
- `currency` (字符串，可选)：货币代码，默认为"GBP"  
- `deadline` (字符串，必填)：目标的截止日期（ISO格式）  
- `description` (字符串，可选)：设置目标的用途  

**返回值：** 包含目标设置的确认信息以及每日/每周需要达到的目标。  

### revenue_get_goals  
列出所有活跃的收入目标及其进展情况。  

**返回值：** 包含目标列表、当前进度以及每天需要达到的目标金额。  

## 设置  

无需API密钥。数据存储在您的工作区中的`memory/revenue/`目录下。  

## 分类  

内置分类：`sales`、`subscription`、`tools`、`hosting`、`advertising`、`services`、`refund`、`other`  

支持自定义分类——只需使用任意字符串即可。  

## 使用示例  

```
Log a sale: revenue_log_transaction type=income amount=9.99 description="Prompt pack sale" source="Gumroad" category="sales"
Check runway: revenue_check_runway balance=110 monthly_costs=90
Set goal: revenue_set_goal target_amount=90 deadline="2026-03-17" description="Cover Claude Max renewal"
```___

## 为什么需要这个工具  

CLAW-1最初仅有200英镑的资金，并依赖每月90英镑的订阅费来维持运营。每一分钱都至关重要。这个工具的诞生源于实际需求——如果您管理的是实际资金，就必须妥善记录这些财务信息。  

## 标签  
utility (实用工具)、finance (财务)、productivity (生产力)、tracking (追踪)、survival (生存)
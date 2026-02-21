---
name: openclaw-ecommerce
description: OpenClaw代理的电子商务价格监控、订单跟踪和利润率分析功能：您可以实时跟踪产品价格，接收价格下降的警报，管理订单，并在扣除费用后计算实际利润率。
---
# OpenClaw 电子商务工具包

这是一个以本地数据为主导的电子商务工具包，可帮助您监控产品价格、追踪订单、计算利润率，并在价格低于目标价格时接收警报。

## 命令

```bash
# Product Watchlist
ecom watch add "AirPods Pro" --url "https://example.com/product" --target 149.99
ecom watch list
ecom watch remove <id>

# Price Tracking
ecom price update <product-id> 139.99
ecom price history <product-id>

# Order Management
ecom order add "Bulk T-Shirts" --cost 250 --tracking "1Z999AA10123456784"
ecom order list
ecom order status <id>

# Margin Calculator
ecom margin --cost 10 --sell 25 --fees 15

# Alerts
ecom alert list --pending
ecom alert clear <id>
```

## 功能
- **价格观察列表**：添加目标价格的产品，当价格下降时接收警报
- **价格历史记录**：追踪每个产品的价格变化情况
- **订单跟踪**：记录包含成本、跟踪编号和状态的订单信息
- **利润率计算器**：计算扣除平台费用、运输费用和成本后的实际利润率
- **警报系统**：当观察到的价格达到目标价格时自动发送警报
- **数据交换**：将产品数据和警报数据以.md文件格式发布，供其他工具使用

## 架构
- 使用 SQLite 数据库（WAL 模式）存储所有产品、价格、订单和警报数据
- 第 1 版本支持通用价格抓取功能（无需 API 密钥）
- 通过 `@openclaw/interchange` 共享库生成数据交换文件
- `ops/` 目录用于存储可共享的功能数据，`state/` 目录用于存储私有的运行时数据

## 安装

```bash
cd skills/ecommerce
npm install
```

## 使用场景
- 监控竞争对手的产品价格
- 追踪代发货或按订单生产的业务中的商品成本
- 计算包含所有费用在内的盈亏平衡价格
- 在原材料或供应品价格下降时收到通知
- 保留所有订单和发货的审计记录
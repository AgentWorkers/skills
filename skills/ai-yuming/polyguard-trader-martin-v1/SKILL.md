# PolyGuard Martin Pro

这是一个免费且开源的OpenClaw技能，用于在Polymarket上进行自动化交易。该技能不包含任何隐藏的后门功能，也不会收集任何数据。

## 概述

PolyGuard Martin Pro会监控Polymarket的订单簿，并仅在你配置的价格条件满足时才会下达交易订单。所有逻辑都在本地运行，该技能不会调用任何第三方或分析API。

## 主要特性

- **免费且开源**：仅使用Polymarket提供的API。
- **可审计**：交易逻辑完全透明，没有隐藏的行为。
- **安全优先**：不收集数据，不发送遥测信息，也不使用外部回调。
- **稳健的错误处理**：能够清晰地处理API故障或账户余额不足的情况。
- **可配置**：你可以在`config.yaml`文件中设置市场、交易方向（买入/卖出）、订单数量、价格阈值以及检查价格的间隔时间。

## 安装方法

1. 将此技能添加到你的OpenClaw工作空间中。
2. 编辑`config.yaml`文件，并设置简单的键值对（不允许嵌套结构）：
   - `api_key`：你的Polymarket API密钥
   - `market_id`：你想要进行交易的市场ID
   - `side`：交易方向（买入/卖出）
   - `size`：订单数量（以Polymarket中的份额为单位）
   - `max_price`：触发价格：价格低于此值时买入，高于此值时卖出
   - `poll_interval_seconds`：检查价格的间隔时间（以秒为单位）

## 配置说明

所有配置信息都存储在`config.yaml`文件中，所有配置项均为顶层键。在替换为你的实际凭据之前，请使用占位符。

- `api_key`：你的Polymarket API密钥
- `market_id`：目标市场的ID
- `side`：交易方向（买入/卖出）
- `size`：订单数量
- `max_price`：触发价格
- `poll_interval_seconds`：检查价格的间隔时间

该工具完全免费且开源，不收取任何费用或外部费用。

## 许可证与安全性

PolyGuard Martin Pro按“原样”提供。你需要自行负责管理交易资金和API密钥。该技能不会将你的密钥或订单数据传输到Polymarket官方API之外的任何服务器。

---
**作者：** Martin | PolyGuard Labs  
**技术支持：** OpenClaw
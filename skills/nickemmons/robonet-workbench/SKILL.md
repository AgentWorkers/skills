---
name: robonet-workbench
description: "使用 Robonet 的 MCP 服务器来构建、回测、优化和部署交易策略。该平台提供了 24 种专为加密货币和预测市场交易设计的专用工具：  
(1) 数据工具：用于浏览交易策略、交易品种、技术指标、Allora 主题以及回测结果；  
(2) 人工智能工具：用于生成交易策略创意、编写交易代码、优化参数，并利用机器学习技术提升策略性能；  
(3) 回测工具：用于在历史数据上测试交易策略的表现；  
(4) 预测市场工具：用于在 Polymarket 平台上执行交易策略；  
(5) 部署工具：用于在 Hyperliquid 平台上进行实时交易；  
(6) 账户管理工具：用于管理交易账户的信用状况。  

适用场景：  
- 构建交易策略  
- 回测交易策略  
- 部署交易机器人  
- 与 Hyperliquid 或 Polymarket 平台进行交互  
- 利用 Allora Network 的机器学习技术优化交易策略"
---

# Robonet MCP集成

## 概述

Robonet提供了一个MCP（Machine Learning for Trading）服务器，帮助AI助手构建、测试和部署交易策略。该服务器提供了24种工具，分为6个类别：数据访问（8种）、AI驱动的策略生成（6种）、回测（2种）、预测市场（3种）、部署（4种）和账户管理（2种）。

## 快速入门

在使用这些工具之前，请先加载所需的MCP工具：

```
Use MCPSearch to select: mcp__workbench__get_all_symbols
Use MCPSearch to select: mcp__workbench__create_strategy
Use MCPSearch to select: mcp__workbench__run_backtest
```

加载完成后，可以直接调用这些工具与Robonet进行交互。

## 工具类别

### 1. 数据访问工具（执行速度快，<1秒）

在构建策略之前，可以浏览可用的资源：

- **`get_all_strategies`** - 列出你的交易策略及其可选的回测结果
- **`get_strategy_code`** - 查看策略的Python源代码
- **`get_strategy_versions`** - 跟踪策略在不同版本中的演变
- **`get_all_symbols`** - 列出Hyperliquid上的可交易对（如BTC-USDT、ETH-USDT等）
- **`get_all_technical_indicators`** - 浏览170多种技术指标（如RSI、MACD、Bollinger Bands等）
- **`get_allora_topics`** - 列出Allora Network的机器学习预测主题
- **`get_data_availability`** - 在回测前检查数据范围
- **`get_latest_backtest_results`** - 查看最近的回测性能

**价格**：大多数工具费用为0.001美元，部分工具免费。请自由使用这些工具进行探索。

**使用时机**：在生成新代码之前，先检查可用的交易对、指标或现有策略。

### 2. AI驱动的策略工具（执行时间20-60秒）

生成并改进交易策略：

- **`generate_ideas`** - 根据市场数据生成AI生成的策略概念
- **`create_strategy`** - 根据描述生成完整的Python策略
- **`optimize_strategy`** - 调整参数以提升性能
- **`enhance_with_allora`** - 将Allora Network的机器学习预测添加到策略中
- **`refine_strategy`** - 对策略代码进行针对性改进
- **`create_prediction_market_strategy`** - 生成Polymarket的YES/NO交易逻辑

**价格**：实际使用的LLM费用加上佣金（通常为0.50-4.50美元）。这些是最昂贵的工具。

**使用时机**：在了解可用资源后，使用这些工具来构建或改进策略。生成策略后务必进行回测。

### 3. 回测工具（执行时间20-40秒）

在历史数据上测试策略性能：

- **`run_backtest`** - 测试加密货币交易策略
- **`run_prediction_market_backtest`** - 测试Polymarket策略

**价格**：每次回测0.001美元

**返回结果**：性能指标（夏普比率、最大回撤率、胜率、总回报、利润因子）、交易统计数据、资金曲线数据

**使用时机**：在创建或修改策略后，务必进行回测以验证其稳健性。

### 4. 预测市场工具

构建Polymarket交易策略：

- **`get_all_prediction_events`** - 浏览可用的预测市场
- **`get_prediction_market_data`** - 分析YES/NO代币的价格历史
- **`create_prediction_market_strategy`** - 生成Polymarket策略代码

**价格**：数据工具费用为0.001美元，创建策略时需加上实际使用的LLM费用和佣金

**使用时机**：用于在Polymarket上进行预测市场交易策略（如政治、加密货币价格预测、经济事件等）。

### 5. 部署工具

将策略部署到Hyperliquid上进行实时交易：

- **`deployment_create`** - 启动实时交易代理（EOA或Hyperliquid Vault）
- **`deployment_list`** - 监控活跃的部署
- **`deployment_start`** - 恢复停止的部署
- **`deployment_stop`** - 停止实时交易

**价格**：创建策略费用为0.50美元，列表/启动/停止操作免费

**限制**：
- EOA（外部拥有的账户）：每个账户最多只能有一个活跃的部署
- Hyperliquid Vault：账户中需要至少有200美元的USDC，部署次数无限制

**使用时机**：在经过彻底的回测并显示积极结果后使用。部署前务必进行回测。

### 6. 账户工具

管理信用额度并查看账户信息：

- **`get_credit_balance`** - 查看可用的USDC信用额度
- **`get_credit_transactions`** - 查看交易历史

**价格**：免费

**使用时机**：在进行昂贵的操作前查看余额。通过交易历史监控支出情况。

## 常见工作流程

### 工作流程1：创建和测试新策略

```
1. get_all_symbols → See available trading pairs
2. get_all_technical_indicators → Browse indicators
3. create_strategy → Generate Python code from description
4. run_backtest → Test on 6+ months of data
5. If promising: optimize_strategy → Tune parameters
6. If excellent: enhance_with_allora → Add ML signals
7. run_backtest → Validate improvements
8. If ready: deployment_create → Deploy to live trading
```

**成本**：根据优化和改进情况，大约1-5美元

### 工作流程2：改进现有策略

```
1. get_all_strategies (include_latest_backtest=true) → Find strategy
2. get_strategy_code → Review implementation
3. refine_strategy (mode="new") → Make targeted improvements
4. run_backtest → Test changes
5. If better: enhance_with_allora → Add ML predictions
6. run_backtest → Final validation
```

**成本**：大约0.50-2.00美元

### 工作流程3：预测市场交易

```
1. get_all_prediction_events → Browse markets
2. get_prediction_market_data → Analyze price history
3. create_prediction_market_strategy → Build YES/NO logic
4. run_prediction_market_backtest → Test performance
5. If profitable: deployment_create → Deploy (when supported)
```

**成本**：大约0.50-5.00美元

### 工作流程4：在构建策略前探索想法

```
1. get_all_symbols → Check available pairs
2. get_allora_topics → See ML prediction coverage
3. generate_ideas (strategy_count=3) → Get AI concepts
4. Pick favorite idea
5. create_strategy → Implement chosen concept
6. run_backtest → Validate
```

**成本**：大约0.50-4.50美元（可以使用`generate_ideas`免费探索）

## 策略开发最佳实践

### 从数据探索开始

在构建策略之前，务必先检查资源的可用性：
- 使用`get_data_availability`确认交易对有足够的历史数据
- 如果计划使用机器学习增强功能，请检查`get_allora_topics`
- 查看`get_all_technical_indicators`了解可用的技术指标

### 必须进行回测

切勿在未进行回测的情况下部署策略：
- 至少使用6个月的数据进行测试
- 使用多个时间段进行训练和验证
- 检查指标：夏普比率>1.0，最大回撤率<20%，胜率45-65%
- 在不同市场条件下比较策略性能

### 成本管理

工具的价格分为几个层级：
1. **数据工具**（0.001美元或免费） - 可自由使用
2. **回测**（0.001美元） - 需要频繁使用
3. **AI生成**（LLM费用加上佣金） - 最昂贵
4. **部署**（0.50美元） - 每次部署一次

**节省成本的技巧**：
- 在使用`create_strategy`（1-4美元）之前，先使用`generate_ideas`（0.05-0.50美元）
- 在运行新的回测之前，先查看`get_latest_backtest_results`（免费）
- 使用`refine_strategy`（0.50-1.50美元）而不是重新生成策略代码
- 在修改策略之前，先查看`get_strategy_code`（免费）

### 策略命名规范

遵循以下命名格式：`{名称}_{风险级别}[_后缀]`

示例：
- `RSIMeanReversion_M` - 基础策略，中等风险
- `MomentumBreakout_H_optimized` - 优化后的策略，高风险
- `TrendFollower_L_allora` - 使用Allora ML的策略，低风险

风险级别：H（高）、M（中等）、L（低）

## 技术细节

### 策略框架

策略使用Jesse交易框架，并包含以下必需的方法：
- `should_long()` - 检查是否满足多头入场条件
- `should_short()` - 检查是否满足空头入场条件
- `go_long()` - 执行多头入场并设置头寸大小
- `go_short()` - 执行空头入场并设置头寸大小

可选方法：
- `on_open_position(order)` - 设置止损和止盈
- `update_position()` - 设置跟踪止损、管理头寸
- `should_cancel_entry()` - 取消未成交的订单

### 可用的指标

通过`jesse.indicators`可以使用170多种技术指标：
- **趋势**：EMA、SMA、Supertrend、Parabolic SAR、VWAP
- **波动性**：Bollinger Bands、ATR、Keltner Channels
- **成交量**：OBV、Volume Profile、Chaikin Money Flow
- 以及更多...

使用`get_all_technical_indicators`查看完整列表。

### Allora Network集成

将机器学习预测添加到策略中：
- **预测类型**：对数回报（百分比变化）或绝对价格
- **时间范围**：5分钟、8小时、24小时、1周
- **资产**：BTC、ETH、SOL、NEAR
- **网络**：Mainnet（10个主题）和Testnet（26个主题）

使用`enhance_with_allora`自动集成预测，或者通过`self.get_predictions()`在策略代码中手动添加。

### 部署选项

**EOA（外部拥有的账户）**：
- 直接通过钱包进行交易
- 每个账户最多只能有一个活跃的部署
- 即时部署
- 设置较为简单

**Hyperliquid Vault**：
- 账户中需要至少有200美元的USDC
- 部署次数无限制
- 专业级托管服务
- 公开TVL（总价值）和性能跟踪

## 故障排除

### “信用额度不足”错误

检查余额：`get_credit_balance`
如有需要，可以在Robonet仪表板中购买信用额度

### 回测时“没有可用数据”

使用`get_data_availability`检查数据覆盖情况
尝试使用较短的时间范围或不同的交易对
BTC-USDT和ETH-USDT的历史数据最长（2020年至今）

### 回测时“未生成交易”

入场条件可能过于严格
尝试使用更长的测试周期或调整阈值
使用`get_strategy_code`检查策略逻辑

### 回测耗时超过2分钟

长时间范围（超过2年）或高频时间帧（1分钟）会导致回测速度变慢
尝试使用较短的时间范围或较低频率的时间帧

### 策略在网页界面中未显示

策略与API密钥关联的账户相关
确保使用拥有该API密钥的账户登录
刷新“我的策略”页面

## 完整工具参考

有关所有24种工具的详细参数文档，请参阅：
- [./shared-references/tool-catalog.md](./shared-references/tool-catalog.md)

该目录包括：
- 完整的参数规格（包括类型和默认值）
- 每个工具的价格信息
- 执行时间估计
- 使用示例

## 示例提示

**创建一个简单策略：**
```
Use Robonet MCP to create a momentum strategy for BTC-USDT on 4h timeframe that:
- Enters long when RSI crosses above 30 and price is above 50-day EMA
- Exits with 2% stop loss or 4% take profit
- Uses 95% of available margin
```

**回测现有策略：**
```
Backtest my RSIMeanReversion_M strategy on ETH-USDT 1h timeframe from 2024-01-01 to 2024-06-30
```

**优化参数：**
```
Optimize the RSI period and stop loss percentage for my MomentumBreakout_H strategy on BTC-USDT 4h from 2024-01-01 to 2024-12-31
```

**添加机器学习预测：**
```
Enhance my TrendFollower_M strategy with Allora predictions for ETH-USDT 8h timeframe and compare performance
```

**部署到实时交易：**
```
Deploy my RSIMeanReversion_M_allora strategy to Hyperliquid on BTC-USDT 4h with 2x leverage using EOA deployment
```

## 安全性与访问权限

- 所有工具都需要有效的Robonet API密钥
- 策略是钱包级别的（只有创建者可以访问）
- 在执行前会原子性地预留信用额度
- API密钥不会被提交到版本控制系统中
- 使用环境变量或安全配置来管理API密钥

## 资源

- **Robonet仪表板**：[robonet.finance](https://robonet.finance)
- **API密钥管理**：仪表板 → 设置 → API密钥
- **信用额度购买**：仪表板 → 设置 → 订费
- **Jesse框架文档**：[jesse.trade](https://jesse.trade)
- **Allora Network**：[allora.network](https://allora.network)
- **Hyperliquid**：[hyperliquid.xyz](https://hyperliquid.xyz)
- **支持**：[Discord](https://discord.gg/robonet) 或 support@robonet.finance
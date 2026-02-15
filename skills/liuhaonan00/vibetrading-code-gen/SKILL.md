---
name: vibetrading-code-gen
description: 根据自然语言提示生成可执行的 Hyperliquid 交易策略代码。当用户希望基于自己的交易理念、技术指标或 VibeTrading 信号为 Hyperliquid 交易所创建自动化交易策略时，可以使用该功能。该技能会生成包含适当错误处理、日志记录以及使用实际 Hyperliquid API 封装的完整 Python 代码。
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "bins": ["python3"] },
        "min_python_version": "3.6"
      }
  }
---

# VibeTrading 代码生成器

该工具能够根据自然语言指令生成可执行的 Hyperliquid 交易策略代码。它将交易想法转化为可直接运行的 Python 代码，并利用 Hyperliquid 的实际 API 实现。生成的代码包含完整的 API 集成、错误处理、日志记录和配置管理功能。

## 快速入门

### 基本用法

```bash
# Generate a simple RSI strategy
python scripts/strategy_generator.py "Generate a BTC RSI strategy, buy below 30, sell above 70"

# Generate a grid trading strategy
python scripts/strategy_generator.py "BTC grid trading 50000-60000 10 grids 0.01 BTC per grid"

# Generate a signal-following strategy
python scripts/strategy_generator.py "ETH trading strategy based on VibeTrading signals, buy on bullish signals, sell on bearish signals"
```

### 输出结构

生成的内容包括：
1. **策略 Python 文件** - 完整的交易策略类
2. **配置文件** - 策略参数和设置
3. **使用说明** - 如何运行和监控策略
4. **依赖项文件** - Python 所需的依赖库

## 代码验证系统

### 自动代码验证

所有生成的代码都会通过内置的验证系统进行自动验证和修复：

```bash
# Validate generated code
python scripts/code_validator.py generated_strategy.py

# Validate and fix automatically
python scripts/code_validator.py generated_strategy.py --fix

# Validate entire directory
python scripts/code_validator.py strategy_directory/
```

### 验证步骤

验证系统执行以下检查：
1. **语法验证** - 检查 Python 语法是否正确
2. **导入验证** - 确认所有模块都能被导入
3. **兼容性检查** - 确保代码兼容 Python 3.5 及更高版本
4. **常见问题检测** - 检查是否存在导入缺失、编码问题等

### 自动修复

当验证失败时，系统会自动修复以下常见问题：
1. **添加缺失的导入** - 如果使用了类型注解，会自动添加相应的导入语句
2. **修复编码声明** - 如果缺少 `# -*- coding: utf-8 -*-`，会自动添加该声明
3. **移除不兼容的语法** - 移除 f-strings 和类型注解（以兼容 Python 3.5）
4. **修复导入路径** - 为 API 包装器添加 `sys.path` 的修改
5. **修复日志器初始化顺序** - 确保日志器在 API 客户端之前被初始化
6. **替换 pathlib** - 为了兼容 Python 3.4，会使用 `os.path`
7. **修复字符串格式** - 将 f-strings 转换为 `.format()` 方法

### 验证配置

验证系统可以通过命令行参数进行配置：

```bash
# Basic validation
python scripts/code_validator.py strategy.py

# Validate and fix automatically
python scripts/code_validator.py strategy.py --fix

# Use specific Python executable
python scripts/code_validator.py strategy.py --python python3.6

# Validate directory with all files
python scripts/code_validator.py strategies/ --fix

# Maximum 5 fix iterations
python scripts/code_validator.py strategy.py --fix --max-iterations 5
```

### 验证规则

系统对生成的代码执行以下规则：
1. **Python 3.5 及更高版本兼容性**：
   - 不使用 f-strings（使用 `.format()` 或 `%` 进行格式化）
   - 不使用类型注解（移除或添加注释）
   - 不使用 `pathlib`（使用 `os.path`）
   - 不导入类型注解相关的模块

2. **代码质量**：
   - 有正确的编码声明（`# -*- coding: utf-8 -*-`）
   - 日志器在 API 客户端之前被初始化
   - 所有导入都能被解析
   - 无语法错误

3. **安全性**：
   - API 密钥从环境变量中加载
   - 不使用硬编码的凭据
   - 对 API 调用有适当的错误处理

4. **性能**：
   - 检查间隔合理（不会过于频繁）
   - 数据获取高效
   - 资源使用得当

### 验证流程

```
User Prompt → Code Generation → Validation → Fixes → Final Code
                    ↓
              If validation fails
                    ↓
            Apply automatic fixes
                    ↓
          Re-validate until success
                    ↓
          Deliver validated code
```

### 验证失败处理

当验证失败时，系统会自动执行以下步骤：
1. **错误分析** - 确定具体的验证错误
2. **修复代码** - 根据错误类型进行相应的修复
3. **重新验证** - 修复后再次进行验证
4. **迭代修复** - 重复上述步骤，直到代码通过验证（最多尝试 3 次）
5. **回退策略** - 如果自动修复失败，会提供详细的错误报告和手动修复指南

### 自动修复示例

#### 修复 1：缺失的导入
```python
# Before (error: NameError: name 'List' is not defined)
def calculate_prices(prices: List[float]) -> List[float]:

# After (automatic fix)
from typing import List, Dict, Optional
def calculate_prices(prices):
```

#### 修复 2：编码问题
```python
# Before (error: SyntaxError: Non-ASCII character)
# Strategy description: Grid trading

# After (automatic fix)
# -*- coding: utf-8 -*-
# Strategy description: Grid trading
```

#### 修复 3：Python 3.5 不兼容问题
```python
# Before (error: SyntaxError in Python 3.5)
price = f"Current price: {current_price}"

# After (automatic fix)
price = "Current price: {}".format(current_price)
```

#### 修复 4：导入路径问题
```python
# Before (error: ImportError: No module named 'hyperliquid_api')
from hyperliquid_api import HyperliquidClient

# After (automatic fix)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "api_wrappers"))
from hyperliquid_api import HyperliquidClient
```

## 支持的策略类型

### 1. 技术指标策略
- **基于 RSI 的策略**：基于 RSI 指标的超买/超卖交易
- **基于 MACD 的策略**：利用 MACD 交叉信号进行趋势跟随
- **移动平均线策略**：基于 SMA/EMA 的交叉策略
- **布林带策略**：基于均值回归的策略

### 2. 高级交易策略
- **网格交易**：在指定价格范围内进行多笔订单的交易
- **均值回归策略**：统计套利策略
- **趋势跟随策略**：基于动量的策略
- **套利策略**：跨品种或跨交易所的套利

### 3. 基于信号的策略
- **集成 VibeTrading 信号**：跟随 AI 生成的交易信号
- **基于新闻的策略**：根据市场新闻和情绪进行交易
- **追踪大额资金流动**：监控大额资金的交易行为
- **资金费率套利**：利用资金费率差异进行套利

## 工作原理

### 第一步：指令分析

生成器会分析您的自然语言指令，以确定：
- 交易标的（BTC、ETH、SOL 等）
- 策略类型（网格交易、基于 RSI 的策略、基于信号的策略等）
- 关键参数（价格范围、网格数量、指标值）
- 风险管理设置

### 第二步：模板选择

根据分析结果，系统会从以下模板中选择最合适的模板：
- `templates/grid_trading.py` - 网格交易策略模板

### 第三步：代码生成

生成器会：
1. 用您的参数填充模板
2. 添加适当的错误处理和日志记录功能
3. 包含配置管理功能
4. 生成完整的可执行代码

### 第四步：代码验证

生成的代码会自动进行验证和修复：
1. **语法检查** - 确保 Python 语法正确
2. **导入验证** - 检查所有导入是否都能被解析
3. **兼容性测试** - 确保代码兼容 Python 3.5 及更高版本
4. **自动修复** - 修复常见问题
5. **重新验证** - 修复后再次进行验证
6. **错误报告** - 如果修复失败，会提供详细的错误报告

### 验证失败处理

如果自动修复后仍然失败，系统会执行以下操作：
1. **错误分析报告** - 详细列出剩余的问题
2. **手动修复指南** - 提供逐步的手动修复步骤
3. **回退模板** - 提供使用更简单、已验证的模板的选项
4. **支持联系方式** - 提供获取帮助的说明

### 第五步：输出结果

您将收到经过验证的、可执行的代码，包括：
1. **经过验证的 Python 策略文件** - 已经过全面测试和修复
2. **配置模板** - 策略参数和设置
3. **验证报告** - 验证结果和应用的修复内容的总结
4. **使用说明** - 如何运行和监控策略
5. **故障排除指南** - 常见问题及解决方法
6. **风险提示** - 重要的安全提示

## API 集成

生成的代码使用了成熟的 Hyperliquid API 实现，支持以下功能：

### 交易操作
- 现货交易（使用限价单/市价单买入/卖出）
- 永续合约交易（使用杠杆进行多头/空头交易）
- 订单管理（取消、修改、查询）
- 仓位管理（减少、对冲）

### 市场数据
- 实时价格和 OHLCV 数据
- 资金费率和未平仓量
- 订单簿深度
- 历史数据访问

### 账户管理
- 账户余额查询（现货和期货）
- 仓位跟踪
- 盈亏计算
- 风险指标

## 模板系统

### 模板结构

每个模板包括：
- **策略类** - 包含初始化和主要逻辑
- **配置部分** - 便于调整参数
- **错误处理** - 包含详细的日志记录
- **风险管理** - 提供风险管理功能
- **监控循环** - 用于持续运行策略

### 可用的模板

#### 网格交易模板
- `grid_trading.py` - 在指定价格范围内进行网格交易（兼容 Python 3.5 及更高版本）
  - 不使用 f-strings
  - 不使用类型注解
  - 有正确的编码声明
  - 日志器在 API 客户端之前被初始化

## 配置管理

### 策略配置

生成的策略包含可配置的参数：
```python
STRATEGY_CONFIG = {
    "symbol": "BTC",
    "timeframe": "1h",
    "parameters": {
        "rsi_period": 14,
        "oversold": 30,
        "overbought": 70
    },
    "risk_management": {
        "position_size": 0.01,
        "stop_loss": 0.05,
        "take_profit": 0.10,
        "max_drawdown": 0.20
    }
}
```

### 环境设置
```bash
# Required environment variables
export HYPERLIQUID_API_KEY="your_api_key_here"
export HYPERLIQUID_ACCOUNT_ADDRESS="your_address_here"
export TELEGRAM_BOT_TOKEN="optional_for_alerts"
```

## 风险管理功能

所有生成的策略都包含以下功能：
### 1. 仓位大小管理
- 固定比例的持仓
- 根据波动性动态调整仓位大小
- 最大持仓限制

### 2. 停损机制
- 基于百分比的止损
- 随动止损
- 基于时间的退出策略

### 3. 风险控制
- 最大每日损失限制
- 减损保护
- 相关性检查
- 市场条件过滤

### 4. 监控与警报
- 实时仓位跟踪
- Telegram/Slack 通知
- 绩效报告
- 错误警报和恢复提示

## 与 VibeTrading 信号的集成

生成的策略可以集成 VibeTrading 的全球交易信号：

```python
from vibetrading import get_latest_signals

# Get AI-generated signals
signals = get_latest_signals("BTC,ETH")

# Use signals in trading logic
if signals["BTC"]["sentiment"] == "BULLISH":
    strategy.execute_buy("BTC", amount=0.01)
```

## 使用示例

### 示例 1：简单的 RSI 策略
**指令**：**生成一个 BTC RSI 策略，当 RSI 低于 30 时买入 0.01 BTC，当 RSI 高于 70 时卖出**

**生成的代码特点**：
- 使用默认的 14 期 RSI 计算
- 可配置的超买/超卖阈值
- 对 API 调用有适当的错误处理
- 所有交易操作都有日志记录
- 每小时检查一次

### 示例 2：网格交易策略
**指令**：**ETH 网格交易策略，价格范围 3000-4000，20 个网格，每个网格买入 0.1 ETH**

**生成的代码特点**：
- 自动计算网格价格
- 自动放置和管理订单
- 自动重新平衡网格
- 实时监控和调整价格
- 详细的日志记录

### 示例 3：基于信号的策略
**指令**：**基于 VibeTrading 信号的 SOL 交易策略，根据买入信号买入，根据卖出信号卖出，每次交易买入 10 SOL**

**生成的代码特点**：
- 集成 VibeTrading API
- 自动获取和解析信号
- 根据信号执行交易
- 管理仓位
- 跟踪交易表现

## 最佳实践

### 1. 先进行模拟交易
- 总是在模拟模式下测试策略
- 初始时使用较小的持仓规模
- 至少监控策略表现 1-2 周

### 2. 风险管理
- 每笔交易的损失不超过 1-2%
- 在所有仓位上使用止损
- 分散投资多个策略
- 监控策略之间的相关性

### 3. 监控与维护
- 定期审查策略表现
- 根据市场情况调整参数
- 保留日志以供审计和分析
- 设置关键事件的警报

### 4. 安全性
- 安全存储 API 密钥（使用环境变量）
- 为不同的策略使用不同的账户
- 定期更换 API 密钥
- 监控未经授权的访问

## 故障排除

### 常见问题

#### 1. API 连接错误
```bash
# Check API key and account address
echo $HYPERLIQUID_API_KEY
echo $HYPERLIQUID_ACCOUNT_ADDRESS

# Test API connection
python scripts/test_connection.py
```

#### 2. 策略无法执行交易
- 检查账户余额和可用资金
- 确认交易标的是否正确
- 检查订单大小是否符合最低要求
- 查看日志中的错误信息

#### 3. 性能问题
- 调整检查间隔（过于频繁可能会导致速率限制）
- 优化数据获取（尽可能使用缓存）
- 根据市场情况调整数据获取方式（例如在流动性较低时）

#### 4. 与 VibeTrading 的集成问题
- 确认 VibeTrading API 可用
- 检查所需交易标的的信号是否可用
- 检查信号解析逻辑

#### 5. 验证错误
```bash
# Common validation errors and solutions:

# Error: "SyntaxError: invalid syntax"
# Solution: Check for f-strings or type annotations
python scripts/code_validator.py strategy.py --fix

# Error: "ImportError: No module named 'typing'"
# Solution: Remove typing imports (Python 3.4 compatibility)
sed -i '' 's/from typing import.*//g' strategy.py

# Error: "SyntaxError: Non-ASCII character"
# Solution: Add encoding declaration
echo -e '# -*- coding: utf-8 -*-\n' | cat - strategy.py > temp && mv temp strategy.py

# Error: "NameError: name 'List' is not defined"
# Solution: Remove type annotations or add typing import
sed -i '' 's/: List//g; s/: Dict//g; s/: Optional//g' strategy.py

# Manual validation check
python -m py_compile strategy.py
```

#### 6. 代码生成失败
- 确保指令清晰（参数要明确）
- 确保请求的策略类型有对应的模板
- 确认 Python 版本兼容性（建议使用 3.5 及更高版本）
- 检查输出文件的可用磁盘空间

## 高级功能

### 自定义模板创建

您可以在 `templates/custom/` 目录下创建自定义模板：
1. 创建新的模板文件
2. 使用 `{{variable_name}}` 定义模板变量
3. 将模板添加到 `scripts/template_registry.py` 中
4. 使用生成器测试模板

### 策略回测

虽然该工具主要用于实时交易，但您也可以：
1. 将生成的代码导出到回测框架中
2. 使用历史数据对策略进行验证
3. 添加性能指标和进行分析

### 多策略管理

对于同时运行多个策略的情况：
1. 为每个策略生成单独的代码文件
2. 使用不同的配置文件
3. 监控整个投资组合的风险
4. 实现策略分配逻辑

## 支持与更新

### 获取帮助

- 查看生成的代码注释
- 查看 `examples/` 目录中的示例策略
- 参考 Hyperliquid API 文档
- 查看 VibeTrading 信号的相关文档

### 更新

该工具将定期更新，包括：
- 新的策略模板
- 提高指令理解能力
- 新的风险管理功能
- 与更多数据源的集成

## 回测集成

### 回测评估功能

现在您可以使用我们的集成回测系统来评估策略的表现：

```bash
# Generate a strategy
python scripts/strategy_generator.py "BTC grid trading 50000-60000 10 grids 0.01 BTC per grid"

# Run backtest on the generated strategy
python scripts/backtest_runner.py generated_strategies/btc_grid_trading_strategy.py

# Run backtest with custom parameters
python scripts/backtest_runner.py generated_strategies/btc_grid_trading_strategy.py \
  --start-date 2025-01-01 \
  --end-date 2025-03-01 \
  --initial-balance 10000 \
  --interval 1h
```

### 回测功能

回测系统提供以下功能：
1. **历史数据模拟** - 使用历史价格数据进行真实模拟
2. **性能指标** - 计算关键指标：
   - 总回报（%）
   - 最大回撤（%）
   - 夏普比率
   - 胜率（%）
   - 总交易次数
   - 平均交易时长

3. **风险分析** - 评估策略的风险特征
4. **可视化报告** - 生成图表和性能报告
5. **对比分析** - 将策略表现与基准进行比较

### 回测配置

您可以使用以下参数配置回测：

```python
BACKTEST_CONFIG = {
    "start_date": "2025-01-01",
    "end_date": "2025-03-01",
    "initial_balance": 10000,  # USDC
    "interval": "1h",  # 1m, 5m, 15m, 30m, 1h, 4h, 1d
    "symbols": ["BTC", "ETH"],  # Trading symbols
    "commission_rate": 0.001,  # 0.1% trading commission
    "slippage": 0.001,  # 0.1% slippage
}
```

### 回测结果示例

```
📊 Backtest Results for BTC Grid Trading Strategy
================================================
📅 Period: 2025-01-01 to 2025-03-01 (60 days)
💰 Initial Balance: $10,000.00
💰 Final Balance: $11,234.56

📈 Performance Metrics:
  • Total Return: +12.35%
  • Max Drawdown: -5.67%
  • Sharpe Ratio: 1.45
  • Win Rate: 58.3%
  • Total Trades: 120
  • Avg Trade Duration: 12.5 hours

📋 Trade Analysis:
  • Winning Trades: 70
  • Losing Trades: 50
  • Largest Win: +$245.67
  • Largest Loss: -$123.45
  • Avg Win: +$89.12
  • Avg Loss: -$56.78

⚠️ Risk Assessment:
  • Risk-Adjusted Return: Good
  • Drawdown Control: Acceptable
  • Consistency: Moderate
```

### 回测结果在生成的代码中的集成

生成的策略现在支持回测功能：

```python
# Generated strategy includes backtest method
strategy = GridTradingStrategy(api_key, account_address, config)

# Run backtest
backtest_results = strategy.run_backtest(
    start_date="2025-01-01",
    end_date="2025-03-01",
    initial_balance=10000
)

# Generate backtest report
strategy.generate_backtest_report(backtest_results)
```

### 回测数据来源

回测系统使用以下数据：
- **来自 Hyperliquid API 的历史价格数据**
- **真实的订单执行** - 包括可配置的滑点
- **基于交易所费用的准确佣金模型**
- **针对大额订单的市场影响模拟**

### 回测限制

**重要提示**：
1. **过去的表现不等于未来的结果** - 历史上的成功并不能保证未来的收益
2. **数据质量** - 结果取决于历史数据的准确性
3. **市场条件** - 过去的市场条件可能与未来不同
4. **执行假设** - 假设订单执行完美（可配置滑点）
5. **流动性假设** - 假设市场流动性充足

**最佳实践**：
1. 使用多个时间段进行回测
2. 在不同的市场条件下进行测试（牛市、熊市、盘整市）
3. 使用真实的佣金和滑点设置
4. 在实际交易中从较小的持仓规模开始
5. 监控策略表现并根据需要进行调整

## 代码验证说明

**验证限制**：
尽管代码验证系统可以自动修复常见问题，但它不能保证：
1. **交易逻辑的正确性** - 验证仅检查语法，不检查交易逻辑
2. **财务表现** - 不保证盈利能力
3. **API 兼容性** - Hyperliquid API 的变化可能会影响生成的代码
4. **安全性** - 建议手动进行安全审查
5. **边缘情况处理** - 可能存在未覆盖的所有错误情况

**验证成功标准**：
代码被视为“有效”时，需满足以下条件：
1. 无语法错误
2. 所有导入都能被解析
3. 兼容 Python 3.6 及更高版本
4. 基本结构正确

**未通过验证的情况**：
- 交易逻辑的正确性
- 风险管理的有效性
- 财务计算的准确性
- 市场条件的处理
- 性能优化

## 快速参考

### Python 版本要求
```bash
# Check Python version
python scripts/check_python_version.py

# Minimum: Python 3.6+ (for f-string support)
```

### 基本用法
```bash
# Generate strategy
python scripts/strategy_generator.py "BTC grid trading 50000-60000 10 grids"

# Run backtest
python scripts/backtest_runner.py generated_strategies/btc_grid_trading_strategy.py
```

### 主要特点
1. **Python 3.6 及更高版本兼容性** - 支持现代 Python 特性（包括 f-strings）
2. **自动回测集成** - 在实际交易前评估策略
3. **全面验证** - 检查语法和兼容性
4. **风险管理** - 所有策略都内置了风险管理功能

## 交易注意事项

**重要提示**：
交易加密货币涉及重大风险。在使用真实资金之前，应彻底测试生成的策略。过去的表现不能保证未来的收益。请始终使用适当的风险管理措施，并且不要使用超出您承受能力的资金进行交易。

该代码生成器提供了策略创建工具，但交易决策和风险管理的最终责任在于用户。

**请注意**：
1. **验证不能替代**：
   - 彻底的模拟测试
   - 由经验丰富的开发者审查生成的代码
   **安全审计** - 在部署前检查是否存在安全漏洞
   **性能测试** - 在不同的市场条件下进行测试
   **风险评估** - 独立评估策略的风险

**回测限制**：
1. **历史数据的质量** - 结果取决于历史数据的准确性
2. **市场条件的变化** - 过去的市场条件可能与未来不同
3. **执行假设** - 假设订单执行完美（可配置滑点）
4. **流动性假设** - 假设市场流动性充足

**最佳实践**：
1. 使用多个时间段进行回测
2. 在不同的市场条件下进行测试（牛市、熊市、盘整市）
3. 使用真实的佣金和滑点设置
4. 在实际交易中从较小的持仓规模开始
5. 根据需要监控策略表现并进行调整

## 代码验证免责声明

**验证限制**：
虽然代码验证系统可以自动修复常见问题，但它不能保证：
1. **交易逻辑的正确性** - 验证仅检查语法，不检查交易逻辑
2. **财务表现** - 不保证盈利能力
3. **API 兼容性** - Hyperliquid API 的变化可能会影响生成的代码
4. **安全性** - 建议手动进行安全审查
5. **边缘情况处理** - 可能存在未覆盖的所有错误情况

**验证成功标准**：
代码被视为“有效”时，需满足以下条件：
1. 无语法错误
2. 所有导入都能被解析
3. 兼容 Python 3.6 及更高版本
4. 基本结构正确

**未通过验证的情况**：
- 交易逻辑的正确性
- 风险管理的有效性
- 财务计算的准确性
- 市场条件的处理
- 性能优化

## 快速参考

### Python 版本要求
```bash
# Check Python version
python scripts/check_python_version.py

# Minimum: Python 3.6+ (for f-string support)
```

### 基本用法
```bash
# Generate strategy
python scripts/strategy_generator.py "BTC grid trading 50000-60000 10 grids"

# Run backtest
python scripts/backtest_runner.py generated_strategies/btc_grid_trading_strategy.py
```

### 主要特点
1. **Python 3.6 及更高版本兼容性** - 支持现代 Python 特性（包括 f-strings）
2. **自动回测集成** - 在实际交易前评估策略
3. **全面验证** - 检查语法和兼容性
4. **风险管理** - 所有策略都内置了风险管理功能

## 交易注意事项

**重要提示**：
交易加密货币涉及重大风险。在使用真实资金之前，应彻底测试生成的策略。过去的表现不能保证未来的收益。请始终使用适当的风险管理措施，并且不要使用超出您承受能力的资金进行交易。

该代码生成器提供了策略创建工具，但交易决策和风险管理的最终责任在于用户。

**请注意**：
1. **验证不能替代**：
   - 彻底的模拟测试
   - 由经验丰富的开发者审查生成的代码
   **安全审计** - 在部署前检查是否存在安全漏洞
   **性能测试** - 在不同的市场条件下进行测试
   **风险评估** - 独立评估策略的风险

**回测限制**：
1. **历史数据的质量** - 结果取决于历史数据的准确性
2. **市场条件的变化** - 过去的市场条件可能与未来不同
3. **执行假设** - 假设订单执行完美（可配置滑点）
4. **流动性假设** - 假设市场流动性充足
5. **没有保证未来的表现** - 过去的表现不能保证未来的收益
---
name: cryptocurrency-trader
description: 这款面向加密货币市场的生产级AI交易代理具备先进的数学建模能力、多层验证机制、概率分析功能，以及零错觉（即零错误判断）的保障。它支持贝叶斯推理、蒙特卡洛模拟、高级风险指标（如VaR、CVaR、夏普比率）的计算，同时具备图表模式识别能力，并通过全面的交叉验证来确保交易决策的准确性，适用于实际交易场景。
---

# 加密货币交易代理技能

## 目的

提供具备数学严谨性、多层验证和全面风险评估的加密货币交易分析服务。该技能专为实际交易应用设计，通过六阶段验证流程确保分析结果的准确性，杜绝任何错误或误导。

## 适用场景

当用户需要以下服务时，请使用此技能：
- 分析特定的加密货币交易对（例如 BTC/USDT、ETH/USDT）
- 扫描市场以寻找最佳交易机会
- 利用概率模型进行全面的风险评估
- 通过高级模式识别生成交易信号
- 获取专业的风险指标（如 VaR、CVaR、Sharpe、Sortino）
- 进行蒙特卡洛模拟以分析不同交易场景
- 使用贝叶斯概率计算来评估交易信号的可靠性

## 核心功能

### 验证与准确性
- 六阶段验证流程，确保分析结果的准确性
- 统计异常检测（Z-score、IQR、本福德定律）
- 在多个时间框架上进行交叉验证
- 设有 14 个“断路器”机制，防止无效交易信号的生成

### 分析方法
- 使用贝叶斯推断进行概率计算
- 进行 10,000 种情景的蒙特卡洛模拟
- GARCH 波动性预测
- 高级图表模式识别
- 支持多时间框架（15 分钟、1 小时、4 小时）的数据分析

### 风险管理
- 风险价值（VaR）和条件风险价值（CVaR）
- 经风险调整的指标（Sharpe、Sortino、Calmar）
- 根据凯利准则确定交易头寸大小
- 自动计算止损和止盈价格

**详细功能请参阅：`references/advanced-capabilities.md`

## 使用前提

在使用此技能之前，请确保满足以下条件：
1. 搭建了 Python 3.8 及更高版本的环境
2. 具备互联网连接，以便获取实时市场数据
3. 安装了所有必需的软件包（使用 `pip install -r requirements.txt` 安装）
4. 用户知道自己的账户余额，以便确定交易头寸的大小

## 使用方法

### 快速启动命令

**分析特定加密货币：**
```bash
python skill.py analyze BTC/USDT --balance 10000
```

**扫描市场以寻找最佳交易机会：**
```bash
python skill.py scan --top 5 --balance 10000
```

**交互式模式进行探索：**
```bash
python skill.py interactive --balance 10000
```

### 默认参数

- **账户余额：** 如果用户未指定，使用 `--balance 10000`
- **时间框架：** 15 分钟、1 小时、4 小时（自动分析）
- **单笔交易风险：** 账户余额的 2%（默认设置）
- **最低风险/收益比：** 1.5:1（通过断路器机制进行验证）

### 常见交易对

主要交易对：BTC/USDT、ETH/USDT、BNB/USDT、SOL/USDT、XRP/USDT
AI 代币：RENDER/USDT、FET/USDT、AGIX/USDT
Layer 1 代币：ADA/USDT、AVAX/USDT、DOT/USDT
Layer 2 代币：MATIC/USDT、ARB/USDT、OP/USDT
DeFi 代币：UNI/USDT、AAVE/USDT、LINK/USDT
Meme 代币：DOGE/USDT、SHIB/USDT、PEPE/USDT

### 工作流程

1. **收集信息**
   - 询问用户所需分析的交易对
   - 获取用户账户余额（或使用默认值 $10,000）
   - 确认用户是否需要专业级别的分析服务

2. **执行分析**
   - 运行相应的命令（分析、扫描或交互式操作）
   - 等待分析结果完成
   - 系统会自动进行六阶段的验证

3. **展示结果**
   - 显示交易建议（买入/卖出/不交易）
   - 显示信心水平和执行准备状态
   - 解释买入价格、止损价格和止盈价格
   - 展示风险指标和头寸大小
   - 显示验证状态（所有阶段均通过 = 可执行）

4. **解读结果**
   - 参考 `references/output-interpretation.md` 以获取详细解读
   - 将技术指标用用户易于理解的语言表达
   - 用简单的语言解释风险与收益的关系
   - 始终提供风险提示

5. **处理特殊情况**
   - 如果执行准备状态为“NO”：解释验证失败的原因
   - 如果信心水平低于 40%：建议等待更好的交易机会
   - 如果触发断路器机制：说明具体问题
   - 如果出现网络错误：建议尝试重新连接并设置指数级重试间隔

### 输出结构

**交易建议：**
- 行动：买入/卖出/不交易
- 信心水平：0-95%（仅显示整数，避免误差）
- 买入价格：推荐的入场价格
- 止损价格：用于控制损失的自动退出价格
- 止盈价格：预期的盈利目标
- 风险/收益比：最低为 1.5:1

**概率分析：**
- 贝叶斯概率（看涨/看跌）
- 蒙特卡洛模拟得出的盈利概率
- 信号强度（弱/中等/强）
- 模式识别结果

**风险评估：**
- 风险价值（VaR）和条件风险价值（CVaR）
- Sharpe 比率、Sortino 比率、Calmar 比率
- 最大回撤率和胜率
- 盈利因子

**头寸大小：**
- 标准策略（2% 的风险限制）
- 凯利保守策略（数学上最优）
- 凯利激进策略（更高的风险/收益比）
- 交易费用估算

**验证状态：**
- 所有阶段均通过（才能执行）
- 是否触发了断路器机制
- 任何警告或关键错误信息

**详细解读请参阅：`references/output-interpretation.md`

## 向用户展示结果时的语言指南**

使用易于初学者理解的语言：
- “买入” → “现在买入，以后高价卖出”
- “卖出” → “现在卖出，以后低价买入”
- “止损” → “如果判断错误，自动退出以限制损失”
- “信心水平” → “我们对交易结果的确定性（数值越高，越可靠）”
- “风险/收益” → “每投入 $1，潜在的收益是 $X”

### 必须提供的风险提示

务必包含以下提醒：
- 市场具有不确定性，即使分析结果看似完美，也可能出错
- 建议从小额交易开始学习
- 每笔交易的风险不得超过账户余额的 2%（系统自动执行）
- 必须使用止损机制
- 本工具仅提供分析结果，不构成财务建议
- 过去的表现不能保证未来的结果
- 用户需对所有交易决策负责

## 不建议交易的情形

在以下情况下，建议用户避免交易：
- 验证状态未达到所有阶段通过
- 执行准备状态为“NO”
- 中等强度的交易信号信心水平低于 60%，高强度信号信心水平低于 70%
- 用户不理解分析结果
- 用户无法承受潜在损失
- 用户处于高情绪压力或疲劳状态

## 高级用法

### 程序化集成

如需自定义工作流程，可直接导入相关代码：
```python
from scripts.trading_agent_refactored import TradingAgent

agent = TradingAgent(balance=10000)
analysis = agent.comprehensive_analysis('BTC/USDT')
print(analysis['final_recommendation'])
```

请参考 `example_usage.py` 了解 5 个综合示例。

### 配置

通过 `config.yaml` 文件自定义行为：
- 验证严格程度（严格模式/正常模式）
- 风险参数（最大风险、头寸限制）
- 断路器触发阈值
- 时间框架偏好设置

### 测试

验证软件的安装和功能：
```bash
# Run compatibility test
./test_claude_code_compat.sh

# Run comprehensive tests
python -m pytest tests/
```

## 参考文档

- `references/advanced-capabilities.md` – 详细的技术功能说明
- `references/output-interpretation.md` – 输出结果解读指南
- `references/optimization.md` – 交易优化策略
- `references/protocol.md` – 使用协议和最佳实践
- `references/psychology.md` – 交易心理学原理
- `references/user-guide.md` – 最终用户文档
- `references/technical-docs/` – 实现细节和错误报告

## 架构

**核心模块：**
- `scripts/trading_agent_refactored.py` – 主要交易代理程序
- `scripts/advanced_validation.py` – 多层验证系统
- `scripts/advanced_analytics.py` – 概率建模引擎
- `scripts/pattern_recognition_refactored.py` – 图表模式识别模块
- `scripts/indicators/` – 技术指标计算模块
- `scripts/market/` – 数据提供和市场扫描模块
- `scripts/risk/` – 头寸管理和风险控制模块
- `scripts/signals/` – 交易信号生成和推荐模块

**入口点：**
- `skill.py` – 建议使用的命令行接口
- `__main__.py` – Python 模块的调用方式
- `example_usage.py` – 程序化使用示例

## 版本

**v2.0.1 – 生产版**

最新改进：
- 修复了关键错误（除以零、导入路径问题、NaN 处理）
- 改进了带有指数级重试机制的网络连接逻辑
- 优化了日志记录系统
- 加强了输入数据的验证
- 确保时间戳使用 UTC 标准
- 优化了本福德定律的阈值设置

**状态：** 🟢 已准备好投入生产

完整变更日志请参阅 `references/technical-docs/FIXES_APPLIED.md`。

## 故障排除

**安装问题：**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**导入错误：**
确保从 `skill` 目录运行程序，或使用 `skill.py` 作为入口文件。

**网络问题：**
系统会自动尝试重新连接，并采用指数级重试策略（最多尝试 3 次）。

**验证失败：**
查看输出中的验证报告，了解具体哪个阶段失败及原因。

**详细调试方法：**
在 `config.yaml` 中启用日志记录功能，或参考 `references/technical-docs/BUG_ANALYSIS_REPORT.md`。
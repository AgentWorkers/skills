---
name: openmm-grid-trading
version: 0.1.0
description: "使用 OpenMM 创建和管理网格交易策略：围绕中心价格自动执行买入/卖出操作。"
tags: [openmm, grid, trading, strategy, automation]
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: [openmm]
      env: [MEXC_API_KEY, GATEIO_API_KEY, BITGET_API_KEY, KRAKEN_API_KEY]
    install:
      - kind: node
        package: "@3rd-eye-labs/openmm"
        bins: [openmm]
---
# OpenMM网格交易

创建能够从市场波动中获利的自动化网格交易策略。

## 什么是网格交易？

网格交易是在当前中心价格周围，按照预设的价格间隔放置多个买入和卖出订单。当价格波动时，机器人会自动执行以下操作：
- **低价买入**：在中心价格以下放置买入订单
- **高价卖出**：在中心价格以上放置卖出订单
- **从波动中获利**：每个完整的交易周期都能捕捉到价差

网格交易通过**每侧的层数**和**间隔**来分配订单。例如，设置5个层次和2%的间隔（线性分布），则会在中心价格的2%、4%、6%、8%、10%处分别放置订单（总共10个订单）。

## 适用场景

**适合：**
- 横盘/区间波动的市场
- 高波动性的交易对
- 生成被动收入
- 24/7自动化交易

**不适用场景：**
- 强趋势市场（存在持有亏损头寸的风险）
- 流动性较低的交易对
- 手续费较高的交易平台

## 快速入门

### 1. 先进行模拟运行（务必先模拟！）
```bash
openmm trade --strategy grid --exchange mexc --symbol INDY/USDT --dry-run
```

### 2. 使用默认配置启动网格交易
```bash
openmm trade --strategy grid --exchange mexc --symbol INDY/USDT
```

### 3. 自定义配置
```bash
openmm trade --strategy grid --exchange mexc --symbol INDY/USDT \
  --levels 5 \
  --spacing 0.02 \
  --size 50 \
  --max-position 0.6 \
  --safety-reserve 0.3
```

### 4. 停止策略

按 `Ctrl+C` 优雅地停止交易策略。系统将：
1. 取消所有未成交的订单
2. 断开与交易平台的连接
3. 显示最终状态

## 命令选项

### 必需参数
- `--strategy grid` — 指定网格交易策略
- `--exchange <exchange>` — 要交易的交易平台（mexc、bitget、gateio、kraken）
- `--symbol <symbol>` — 交易对（例如：INDY/USDT、SNEK/USDT、ADA/EUR）

### 网格交易参数
| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `--levels <number>` | 每侧的网格层数（最多10层，总数 = 层数 × 2） | 5 |
| `--spacing <decimal>` | 各层之间的基础价格间隔（0.02 = 2%） | 0.02 |
| `--size <number>` | 单个订单的基础交易量（以报价货币计） | 50 |
| `--confidence <decimal>` | 交易所需的最低价格置信度 | 0.6 |
| `--deviation <decimal>` | 触发网格重新调整的价格偏差 | 0.015 |
| `--debounce <ms>` | 网格调整之间的延迟时间（毫秒） | 2000 |
| `--max-position <decimal>` | 最大持仓量（占余额的百分比） | 0.8 |
| `--safety-reserve <decimal>` | 安全储备金（占余额的百分比） | 0.2 |
| `--dry-run` | 不放置实际订单的模拟运行 | — |

### 动态网格参数
| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `--spacing-model <model>` | 线性、几何或自定义 | 线性 |
| `--spacing-factor <number>` | 各层的几何间隔倍数 | 1.3 |
| `--size-model <model>` | 均匀分配、金字塔形分配或自定义 | 均匀分配 |
| `--grid-profile <path>` | 从JSON配置文件加载网格设置 | — |

### 波动性参数
| 参数 | 描述 | 默认值 |
|-----------|-------------|---------|
| `--volatility` | 启用基于波动性的价差调整 | 关闭 |
| `--volatility-low <decimal>` | 低波动性阈值 | 0.02 |
| `--volatility-high <decimal>` | 高波动性阈值 | 0.05 |

## 间隔模型

**线性（默认）：** 所有层次之间的间隔相等。
```
With --spacing 0.02 and 5 levels:
Level 1:  2% from center
Level 2:  4% from center
Level 3:  6% from center
Level 4:  8% from center
Level 5: 10% from center
```

**几何模型：** 中心附近的间隔较紧，外围层次的间隔较宽。
```bash
openmm trade --strategy grid --exchange kraken --symbol BTC/USD \
  --levels 5 --spacing 0.005 --spacing-model geometric --spacing-factor 1.5
```
```
Level 1: 0.50% from center
Level 2: 1.25% from center
Level 3: 2.38% from center
Level 4: 4.06% from center
Level 5: 6.59% from center
```

**自定义模型：** 使用JSON配置文件定义每个层次的具体间隔。

## 交易量模型

**均匀分配（默认）：** 所有层次的订单量相同。

**金字塔模型：** 在中心价格附近放置较大订单（成交概率较高），向外层逐渐减少订单量。
```bash
openmm trade --strategy grid --exchange mexc --symbol INDY/USDT \
  --levels 5 --size 50 --size-model pyramidal
```

## 网格配置文件

用于保存完整网格设置的JSON文件：
```json
{
  "name": "balanced-geometric",
  "description": "Geometric spacing with pyramidal sizing",
  "levels": 10,
  "spacingModel": "geometric",
  "baseSpacing": 0.005,
  "spacingFactor": 1.3,
  "sizeModel": "pyramidal",
  "baseSize": 50
}
```

```bash
openmm trade --strategy grid --exchange gateio --symbol SNEK/USDT \
  --grid-profile ./profiles/balanced-geometric.json
```

## 基于波动性的价差调整

启用此功能后，系统会在市场波动时自动扩大订单间隔，在市场平静时缩小间隔。系统会跟踪5分钟内的价格变化：
- 当价格低于低波动性阈值（默认2%）时：保持正常间隔（1.0倍）
- 在两个阈值之间：扩大间隔（1.5倍）
- 当价格高于高波动性阈值（默认5%）时：扩大间隔（2.0倍）
```bash
openmm trade --strategy grid --exchange mexc --symbol INDY/USDT \
  --levels 10 \
  --spacing 0.005 \
  --spacing-model geometric \
  --spacing-factor 1.3 \
  --size-model pyramidal \
  --size 5 \
  --volatility
```

## 交易示例

### 保守型策略
```bash
openmm trade --strategy grid --exchange bitget --symbol SNEK/USDT \
  --levels 2 \
  --spacing 0.02 \
  --size 20
```

### 积极型策略
```bash
openmm trade --strategy grid --exchange mexc --symbol BTC/USDT \
  --levels 7 \
  --spacing 0.005 \
  --size 25
```

### 动态策略（几何模型 + 金字塔模型）
```bash
openmm trade --strategy grid --exchange kraken --symbol SNEK/EUR \
  --levels 10 \
  --spacing 0.005 \
  --spacing-model geometric \
  --spacing-factor 1.5 \
  --size-model pyramidal \
  --size 5
```

## 风险管理
- `--max-position` — 用于交易的最大余额百分比（默认：80%）
- `--safety-reserve` — 作为储备金的余额百分比（默认：20%）
- `--confidence` — 交易所需的最低价格置信度（默认：60%）
- 当订单成交时，系统会自动重新生成网格配置
- 系统会根据价格大幅波动进行调整（可通过 `--deviation` 参数配置）

## 各交易平台的特殊说明

**MEXC/Gate.io：** 每笔订单的最低交易金额为1 USDT
**Bitget：** 最低交易金额为1 USDT。需要API密钥、秘密密钥和密码。SNEK/NIGHT交易对的报价精度为6位小数。
**Kraken：** 每笔订单的最低交易金额为5 EUR/USD。支持主要法定货币对（EUR、USD、GBP）。

## 给代理的建议

1. **务必先进行模拟运行** — 在执行策略前向用户展示交易计划
2. **检查余额** — 使用 `openmm balance --exchange <ex>` 命令核实资金是否充足
3. **查看当前价格** — 使用 `openmm ticker --exchange <ex> --symbol <sym>` 命令获取最新价格
4. **遵守最低交易金额要求** — 确保 `--size` 除以 `--levels` 的结果符合交易平台的最低要求
5. **使用 `Ctrl+C` 停止策略** — 优雅地关闭系统会取消所有未成交的订单
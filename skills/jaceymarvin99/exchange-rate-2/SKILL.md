---
name: exchange-rate
description: >
  **使用场景：**  
  当用户需要查询两种货币之间的每日汇率时使用该功能。
---
# 汇率技能

该技能可帮助AI代理从60s API获取每日货币汇率。

## 何时使用此技能

当用户执行以下操作时，请使用此技能：
- 询问两种货币之间的当前汇率。
- 想知道一种货币相对于另一种货币的价值。
- 需要最新的货币兑换率。

## 使用方法

执行关联的`scripts/exchange_rate.sh`脚本来获取汇率。

```bash
./scripts/exchange_rate.sh [options]
```

### 参数选项

- `--currency, -c <货币>`：可选。基础货币的ISO 4217代码。默认值为`CNY`（人民币）。
- `--target, -t <目标货币>`：可选。目标货币的ISO 4217代码。默认值为`USD`（美元）。如果设置为`AAA`，则返回基础货币的所有可用汇率。

### 返回值

脚本会输出目标货币相对于1单位基础货币的汇率值。
如果目标货币不存在，则返回错误信息。

### 使用示例

```bash
# Get the exchange rate from CNY to USD (default)
./scripts/exchange_rate.sh

# Get the exchange rate from EUR to JPY
./scripts/exchange_rate.sh --currency EUR --target JPY

# Get all exchange rates for GBP
./scripts/exchange_rate.sh -c GBP -t AAA
```
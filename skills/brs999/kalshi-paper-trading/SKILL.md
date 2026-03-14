---
name: kalshi-paper-trading
description: Kalshi原生纸质交易账本及命令行界面（CLI），专为二元预测合约设计。支持进行纸质开仓、标记、对账、估值和审核等操作，无需依赖通用的现货交易系统。
homepage: https://docs.kalshi.com
user-invocable: true
disable-model-invocation: false
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: [node]
---
# Kalshi 纸质交易

此技能用于 Kalshi 的纸质交易执行和账本管理。

Kalshi 专用的纸质交易系统应使用专用的账本和命令行界面（CLI），而不是通用的 `paper-trading` 技能。

## 使用场景

当用户需要执行以下操作时，请使用此技能：

- 设计或开发专用于 Kalshi 的纸质交易工具；
- 检查或对账 Kalshi 的纸质交易头寸；
- 正确地以分（cents）为单位存储 Kalshi 的价格，避免单位混淆；
- 计算 Kalshi 的已实现和未实现的损益（PnL）；
- 添加 Kalshi 专有的风险控制规则。

## 重要规则

除非用户明确要求保持兼容性，否则不要通过通用的 `skills/paper-trading` 账本来处理 Kalshi 的纸质交易执行。

此技能的默认假设如下：

- Kalshi 的交易价格以整数分（[0, 100]）的形式存储；
- 结算金额为 `100` 分或 `0` 分；
- 头寸信息通过 `market_ticker + contract_side` 来标识；
- 风险控制基于溢价和事件敞口，而非止损距离百分比；
- 实时市场同步支持传统的分（cents）字段以及现代 Kalshi 的 `*_dollars` 报价字段。

## 主要命令

- 初始化纸质交易账户：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts init --account kalshi --starting-balance-usd 1000
```

- 检查账户状态：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts status --account kalshi --format json --pretty
```

- 将实时市场报价同步到账本：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts sync-market --market <TICKER> --format json --pretty
```

- 根据 Kalshi 的卖价开启纸质交易：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts buy-from-market --account kalshi --market <TICKER> --side YES --contracts 1 --format json --pretty
```

- 对账已完成的交易：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts reconcile --account kalshi --market <TICKER> --winning-side YES
```

- 查看账户表现：  
  ```bash
node --experimental-strip-types {baseDir}/scripts/kalshi_paper.ts review --account kalshi --format json --pretty
```

## 集成

请将此技能与独立的 Kalshi API 读取技能结合使用，以执行以下操作：

- 市场信息查询；
- 流动性验证；
- 交易和订单簿检查；
- 交易前候选策略的排序。

此技能仅负责处理纸质交易的账本和执行相关功能。

## 设计参考

在进行任何结构更改之前，请阅读以下提案文档：  
- [references/kalshi-paper-ledger.md](references/kalshi-paper-ledger.md)  
该文档可用于以下方面：  
- 数据库模式设计；  
- 命令接口设计；  
- 估值规则制定；  
- 从通用纸质交易系统迁移的策略规划。

## 测试

运行 Kalshi 纸质交易工具的测试文件：  
```bash
node --test {baseDir}/tests/kalshi_paper.test.mjs
```
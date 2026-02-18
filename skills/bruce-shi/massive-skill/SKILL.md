---
name: polygon-api
description: 通过命令行界面（CLI）访问 Polygon/Massive 的股票、加密货币、外汇、期权、指数、期货、市场数据以及新闻相关的 API。
metadata:
  openclaw:
    requires:
      bins: ["bun"]
      env: ["POLY_API_KEY"]
    primaryEnv: "POLY_API_KEY"
---
# Polygon（Massive）市场数据技能

这是一个用于访问 [Polygon/Massive](https://massive.com) 金融数据 API 的命令行工具（CLI）和 JavaScript 客户端封装。支持股票、加密货币、外汇、期权、指数、期货、市场状态、新闻以及参考数据等类型的数据。

## 命令行工具（CLI）的使用方法

```bash
bun cli.js <command> [options]
```

所有命令的输出结果均为 JSON 格式，直接显示在标准输出（stdout）中。使用 `--help` 可查看所有命令的列表；使用 `<command> --help` 可查看特定命令的详细选项。

### 股票

有关所有股票相关命令和参数的详细信息，请参阅 [股票命令参考](references/stocks_commands.md)。

### 加密货币

有关所有加密货币相关命令和参数的详细信息，请参阅 [加密货币命令参考](references/crypto_commands.md)。

### 外汇

有关所有外汇相关命令和参数的详细信息，请参阅 [外汇命令参考](references/forex_commands.md)。

### 期权

有关所有期权相关命令和参数的详细信息，请参阅 [期权命令参考](references/options_commands.md)。

### 指数

有关所有指数相关命令和参数的详细信息，请参阅 [指数命令参考](references/indices_commands.md)。

### 参考数据

有关所有参考数据相关命令和参数的详细信息，请参阅 [参考数据命令参考](references/reference_commands.md)。

### 市场

有关所有市场相关命令和参数的详细信息，请参阅 [市场命令参考](references/market_commands.md)。

### 新闻

有关所有新闻相关命令和参数的详细信息，请参阅 [新闻命令参考](references/news_commands.md)。
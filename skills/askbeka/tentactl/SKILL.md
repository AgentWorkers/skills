---
name: kraken
description: "与Kraken加密货币交易所进行交互——支持现货交易和期货交易，同时提供REST和WebSocket接口。适用场景包括：  
(1) 查看加密货币价格或市场数据；  
(2) 查看账户余额、持仓情况或交易历史；  
(3) 下单或取消订单（现货或期货）；  
(4) 通过WebSocket实时获取市场数据；  
(5) 构建定期投资（DCA）策略、价格警报或投资组合监控系统；  
(6) 任何与Kraken、加密货币交易或投资组合管理相关的内容。  
使用该工具需要`tentactl`二进制文件，并且仅对需要身份验证的API端点需要Kraken的API密钥。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🐙",
        "requires":
          {
            "bins": ["tentactl"],
            "env": ["KRAKEN_API_KEY", "KRAKEN_API_SECRET"],
          },
        "install":
          [
            {
              "id": "cargo",
              "kind": "cargo",
              "package": "tentactl",
              "bins": ["tentactl"],
              "label": "Install tentactl via cargo (source: https://github.com/askbeka/tentactl)",
            },
          ],
        "credentials":
          {
            "KRAKEN_API_KEY": "Kraken API key — generate at https://www.kraken.com/u/security/api",
            "KRAKEN_API_SECRET": "Kraken API secret (private key from the same page)",
          },
        "privacy":
          {
            "files_written": ["~/.tentactl.env"],
            "network": ["api.kraken.com", "futures.kraken.com", "ws.kraken.com", "futures.kraken.com/ws/v1"],
            "notes": "API keys are stored in ~/.tentactl.env (chmod 600). Market data endpoints require no authentication. Account and trading endpoints require KRAKEN_API_KEY and KRAKEN_API_SECRET.",
          },
      },
  }
---
# Kraken Exchange

[Kraken](https://www.kraken.com)加密货币交易所的MCP（Model Context Protocol）服务器——提供了114种工具，支持现货交易、期货交易、REST接口和WebSocket接口。项目源代码位于：[github.com/askbeka/tentactl](https://github.com/askbeka/tentactl)，采用MIT许可证。

## 工作原理

`tentactl`是一个Rust编写的二进制程序，它通过标准输入输出（stdio）与Kraken的MCP协议进行通信。该程序提供了以下功能：

- **现货交易REST接口**（57种工具）：市场数据、账户信息、交易操作、资金管理、收益计算、子账户管理等功能。
- **期货交易REST接口**（21种工具）：交易品种、持仓信息、订单管理、资金转移等功能。
- **现货交易WebSocket接口（v2）**（19种工具）：实时市场数据流、订单管理功能。
- **期货交易WebSocket接口**（17种工具）：实时期货价格数据、期货交易功能。

## 设置

### 1. 安装二进制程序

```bash
cargo install tentactl
```

或者从[GitHub仓库的发布页面](https://github.com/askbeka/tentactl/releases)下载（支持Linux、macOS和Windows系统）。

### 2. 配置API密钥（可选）

市场数据相关的工具无需密钥即可使用。对于账户管理和交易相关的工具，需要配置API密钥：

```bash
echo "KRAKEN_API_KEY=your-key" > ~/.tentactl.env
echo "KRAKEN_API_SECRET=your-secret" >> ~/.tentactl.env
chmod 600 ~/.tentactl.env
```

或者使用`scripts/setup-keys.sh`脚本进行密钥设置。

**密钥权限说明：**
- 在[Kraken官网](https://www.kraken.com/u/security/api)创建密钥：
  - 仅读权限：允许查询资金信息和未成交订单及交易记录。
  - 交易权限：还需允许创建和修改订单。

## 使用方法

```bash
# Market data (no auth)
scripts/kraken.sh get_ticker '{"pair":"XBTUSD"}'
scripts/kraken.sh get_orderbook '{"pair":"ETHUSD","count":5}'
scripts/kraken.sh futures_tickers '{}'

# Live WebSocket streams
scripts/kraken.sh ws_subscribe_ticker '{"symbols":["BTC/USD"]}'
scripts/kraken.sh ws_subscribe_book '{"symbols":["ETH/USD"],"depth":10}'
scripts/kraken.sh wf_subscribe_ticker '{"product_ids":["PI_XBTUSD"]}'
scripts/kraken.sh ws_status '{}'

# Account (needs API keys)
scripts/kraken.sh get_balance '{}'
scripts/kraken.sh futures_open_positions '{}'

# Trading (needs API keys) ⚠️ REAL MONEY
scripts/kraken.sh place_order '{"pair":"XBTUSD","direction":"buy","order_type":"limit","volume":"0.001","price":"50000","validate":true}'
scripts/kraken.sh ws_add_order '{"symbol":"BTC/USD","side":"buy","order_type":"limit","limit_price":"50000","order_qty":"0.001","validate":true}'
```

## 工具参考

有关所有114种工具的详细参数说明，请参阅`references/tools.md`文件。

## 安全规则

- 下单前**必须**启用`validate: true`选项。
- 下真实订单前**必须**获得用户确认。
- 未经用户明确授权，**严禁**下达任何订单。
- 市场订单会立即执行——建议优先使用限价单。
- 在取消`validate`选项之前，务必显示验证结果并请求用户确认。
- 标有“⚠️ 实际资金操作”的工具表示涉及真实资金交易。

## 交易对

- **现货交易REST接口**：使用Kraken自定义的格式，例如`XBTUSD`、`ETHUSD`、`SOLUSD`。
- **现货交易WebSocket接口**：使用标准格式，例如`BTC/USD`、`ETH/USD`、`SOL/USD`。
- **期货交易**：使用产品ID进行标识，例如`PI_XBTUSD`、`PI_ETHUSD`、`PF_SOLUSD`。

## 自动化方案

### 定投（Dollar Cost Average, DCA）

```
openclaw cron add --schedule "0 9 * * 1" --task "Buy $50 of BTC on Kraken using the kraken skill. Use validate first, then execute."
```

### 价格警报

- 订阅WebSocket价格更新通知，通过心跳脚本或定时任务检查价格阈值，并通过WhatsApp/Telegram发送警报。

### 投资组合监控

- 通过定时任务检查账户余额、持仓情况和当前价格，计算盈亏，并在价格发生显著变化时发出警报。

### 资金利率套利

- 订阅期货价格更新通知，监控资金利率的变化，当利率出现显著差异时发出警报。
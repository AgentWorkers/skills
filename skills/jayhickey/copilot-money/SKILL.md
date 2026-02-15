---
name: copilot-money
description: 查询 Copilot Money 的个人财务数据（账户、交易、净资产、持仓、资产配置），并刷新银行账户连接。当用户询问财务相关问题（如账户余额、近期交易、净资产、投资分配）或希望同步/刷新银行数据时，可使用此功能。
---

# Copilot Money CLI

这是一个用于 [Copilot Money](https://copilot.money)（一款个人财务管理应用）的命令行接口。只需完成一次身份验证，即可通过终端查询账户信息、交易记录、资产持有情况以及资金分配情况。

> **注意：** 这是一个非官方工具，与 Copilot Money 无任何关联。

## 安装

```bash
pip install copilot-money-cli
```

## 快速入门

```bash
copilot-money config init
copilot-money accounts
copilot-money networth
```

## 命令

```bash
copilot-money refresh                     # Refresh all bank connections
copilot-money accounts                    # List accounts with balances
copilot-money accounts --type CREDIT      # Filter by type
copilot-money accounts --json             # Output as JSON
copilot-money transactions                # Recent transactions (default 20)
copilot-money transactions --count 50     # Specify count
copilot-money networth                    # Assets, liabilities, net worth
copilot-money holdings                    # Investment holdings (grouped by type)
copilot-money holdings --group account    # Group by account
copilot-money holdings --group symbol     # Group by symbol
copilot-money holdings --type ETF         # Filter by security type
copilot-money allocation                  # Stocks/bonds with US/Intl split
copilot-money config show                 # Show config and token status
copilot-money config init                 # Auto-detect token from browsers
copilot-money config init --source chrome # From specific browser
copilot-money config init --source manual # Manual token entry
```

## 身份验证

配置文件存储在 `~/.config/copilot-money/config.json` 中。该 CLI 会自动从 macOS 上支持的浏览器中检测您的 Copilot Money 会话令牌。

- 自动检测：`copilot-money config init`
- 显式指定来源：`copilot-money config init --source arc|chrome|safari|firefox`
- 手动输入：`copilot-money config init --source manual`

当使用浏览器自动检测功能时，CLI 会读取浏览器本地的 IndexedDB 存储来获取您的 Copilot Money 会话令牌。此过程仅在本地进行，数据不会被发送到任何其他地方，只会被发送到 Copilot Money 的 API。

## 系统要求

- Python 3.10 或更高版本
- 需要 macOS 环境以获取浏览器生成的令牌（手动输入令牌的功能在所有平台上均可用）
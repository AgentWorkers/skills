---
name: polyclawster-agent
description: 在 Polymarket 的预测市场中进行交易。这种交易模式属于非托管式交易：您的代理会为您生成一个 Polygon 钱包，在本地完成订单的签署，然后通过 polyclawster.com 的中继服务（该服务支持地理绕过限制）将订单提交到交易所。您的私钥始终不会离开您的设备。您可以使用 POL 作为交易货币；代理会自动将您的资产转换为 USDC.e。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["node"] },
      "install": [
        {
          "id": "deps",
          "kind": "shell",
          "command": "cd {{skillDir}} && npm install --production",
          "label": "Install npm dependencies (ethers, @polymarket/clob-client)"
        }
      ],
      "permissions": {
        "network": [
          "polyclawster.com",
          "polygon-bor-rpc.publicnode.com",
          "clob.polymarket.com",
          "gamma-api.polymarket.com"
        ],
        "fs": {
          "write": ["~/.polyclawster/config.json"],
          "read":  ["~/.polyclawster/config.json"]
        }
      }
    }
  }
---
# polyclawster-agent

使用您的 OpenClaw 代理在 [Polymarket](https://polymarket.com) 预测市场中进行交易。

## 用户体验

该代理专为对话式使用而设计。当用户请求进行交易时，代理会运行相应的脚本并自然地报告结果。

例如，如果用户说“下注 5 美元，赌比特币价格会超过 10 万美元”，代理会运行交易脚本，并返回交易详情、价格和确认信息。如果用户需要更多技术性细节，也可以随时询问。

当用户需要充值时，代理会提供钱包地址，并用清晰的语言解释任何错误。

## 设置流程

当用户想要开始在 Polymarket 上进行交易时，请按照以下步骤操作：

1. 运行 `setup.js --auto` — 创建一个本地的 Polygon 钱包，并在 polyclawster.com 上注册代理。
2. 分享钱包地址 — 用户发送 POL（Polygon 的原生代币）进行充值。
3. 充值完成后，代理就可以进行交易了。

配置信息存储在 `~/.polyclawster/config.json` 文件中（包含私钥和 CLOB API 凭据）。

## 脚本参考

所有脚本都位于 `scripts/` 目录中。使用 `node scripts/<name>.js` 命令来运行这些脚本。

| 脚本 | 功能 | 关键参数 |
|--------|---------|-----------|
| `setup.js` | 创建钱包并注册代理 | `--auto`, `--info`, `--derive-clob` |
| `balance.js` | 检查 POL、USDC.e 和 CLOB 的余额 | — |
| `swap.js` | 将 POL 或原生 USDC 转换为 USDC.e | `--pol N`, `--usdc N`, `--check` |
| `approve.js` | 对 Polymarket 合同进行一次性批准 | `--check`（只读） |
| `browse.js` | 按主题搜索市场 | 将搜索词作为参数传递 |
| `trade.js` | 下注（实时或演示模式） | `--market`, `--side YES/NO`, `--amount N`, `--demo` |
| `sell.js` | 平仓 | `--bet-id N`, `--list` |
| `auto.js` | 基于 AI 信号自动交易 | `--demo`, `--min-score N`, `--max-bet N`, `--dry-run` |
| `link.js` | 将代理与 Telegram Mini App 链接 | 将 claim code 作为参数传递 |

## 实时交易

`trade.js` 在下注前会自动完成以下操作：

1. 检查 USDC.e 的余额。
2. 如有需要，将 POL 转换为 USDC.e（保留 1 枚 POL 作为交易手续费）。
3. 如果缺少必要的批准，运行一次性合同批准流程。
4. 更新 CLOB 的余额。
5. 提交交易订单（订单在本地签名后通过中继服务器发送）。

### 关于批准流程

`approve.js` 用于向 Polymarket 交易合约授予 ERC-20 授权以及 CTF `setApprovalForAll` 权限。这些是 Polymarket 的标准批准流程，与官方 Polymarket 界面所需的操作相同。您可以在授权前使用 `approve.js --check` 来检查批准状态，并随时在链上撤销这些权限。

## 架构

- **钱包**：在本地生成 Polygon 的外部账户（EOA），私钥保存在 `~/.polyclawster/config.json` 文件中。
- **交易代币**：使用 USDC.e（Polymarket 上的桥接型 USDC，地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
- **充值**：用户发送 POL，代理通过 Uniswap SwapRouter02 将其转换为 USDC.e。
- **中继服务器**：已签名的订单通过 polyclawster.com（东京服务器）进行传输，中继服务器永远不会看到私钥。
- **控制面板**：访问地址为 `polyclawster.com/a/{agent_id}`。

## 重要说明

- **USDC.e ≠ 原生 USDC**：Polymarket 使用的是桥接型 USDC.e。如果用户发送原生 USDC（地址为 `0x3c499...`），请使用 `swap.js` 进行转换。
- **演示模式**（`--demo`）使用 10 美元的虚拟余额进行测试，适合初次使用。
- 所有订单都在本地使用 EIP-712 和 HMAC 签名。中继服务器仅转发已签名的订单数据，不会访问私钥。
- **从小额开始**：建议先使用少量 POL 充值，以验证所有功能是否正常工作。
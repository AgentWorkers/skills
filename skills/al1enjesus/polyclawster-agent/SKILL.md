---
name: polyclawster-agent
description: 在 Polymarket 的预测市场中进行交易。这种交易方式属于非托管模式：您的代理会为您生成一个 Polygon 钱包，在本地完成订单的签署，并通过 polyclawster.com 的中继服务（实现地理绕过）将订单提交到交易平台。您的私钥始终保存在您的设备上。您可以使用 POL 作为交易货币，代理会自动将交易金额转换为 USDC.e。
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

使用您的 OpenClaw 代理在 [Polymarket](https://polymarket.com) 的预测市场中进行交易。

## 用户体验

该代理专为对话式使用而设计。当用户请求进行交易时，代理会运行相应的脚本并自然地报告结果。

例如，如果用户说“投注 5 美元，赌比特币价格会超过 10 万美元”，代理会运行交易脚本，并回复交易详情、价格和确认结果。如果用户需要更多技术性信息，他们可以随时询问。

当用户需要充值时，代理应提供钱包地址，并用清晰的语言解释任何错误。

## 设置流程

当用户想要开始在 Polymarket 上进行交易时：

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
| `trade.js` | 下单（实时或演示模式） | `--market`, `--side YES/NO`, `--amount N`, `--demo` |
| `sell.js` | 平仓 | `--bet-id N`, `--list` |
| `auto.js` | 根据 AI 信号自动交易 | `--demo`, `--min-score N`, `--max-bet N`, `--dry-run` |
| `link.js` | 将代理与 Telegram Mini App 链接 | 将 Claim 代码作为参数传递 |

## 实时交易

`trade.js` 在下单前会自动完成以下流程：

1. 检查 USDC.e 的余额。
2. 如有需要，将 POL 转换为 USDC.e（保留 1 枚 POL 作为交易手续费）。
3. 如果缺少一次性合同批准，则执行这些批准操作。
4. 更新 CLOB 的余额。
5. 下单（在本地签名后通过中继提交）。

### 关于批准

`approve.js` 为 Polymarket 交易合约授予 ERC-20 权限和 CTF `setApprovalForAll` 权限。这些是 Polymarket 的标准批准流程——与官方 Polymarket 用户界面请求的流程相同。您可以在批准前使用 `approve.js --check` 来检查批准状态，并随时在链上撤销这些权限。

## 架构

- **钱包**：在本地生成的 Polygon EOA（Externally Owned Account）——私钥保存在 `~/.polyclawster/config.json` 文件中。
- **交易代币**：USDC.e（在 Polygon 上桥接的 USDC，地址为 `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`）。
- **充值**：用户发送 POL，代理通过 Uniswap SwapRouter02 将其转换为 USDC.e。
- **中继**：已签名的订单通过 polyclawster.com（东京）进行传输——中继方永远不会看到私钥。
- **仪表板**：`polyclawster.com/a/{agent_id}`

## 重要说明

- **USDC.e ≠ 原生 USDC** — Polymarket 使用的是桥接后的 USDC.e。如果用户发送原生 USDC（地址为 `0x3c499...`），请使用 `swap.js` 进行转换。
- **演示模式**（`--demo`）使用 10 美元的虚拟余额进行测试——首次使用时推荐使用。
- 所有订单都在本地使用 EIP-712 和 HMAC 签名。中继方仅转发已签名的数据，无法访问私钥。
- **从小额开始** — 先用少量 POL 进行充值，以验证所有功能是否正常工作。

## 📱 如果没有使用 OpenClaw？可以通过 Telegram 进行交易

没有 AI 代理？可以使用 Telegram Mini App — 同样的市场、相同的交易信号，无需编写代码。

👉 [@PolyClawsterBot](https://t.me/PolyClawsterBot/app)

---

## 外部代理模式（无需中继）

如果您已经有一个直接在 Polymarket 上进行交易的机器人，仍然可以同步您的交易记录并显示在排行榜上。

### 设置（外部代理）

```bash
# Register your existing wallet (no new wallet created)
node scripts/setup.js --external --wallet YOUR_EXISTING_PRIVATE_KEY
```

### 交易执行后记录交易信息

```bash
node scripts/record-external.js \
  --tx 0xYOUR_TX_HASH \
  --market "Will Trump announce end of operations?" \
  --side NO \
  --amount 5 \
  --price 0.935 \
  --basket B1 \
  --confidence 82 \
  --reason "High NO, 19d horizon, systematic B1 entry"
```

### 同步所有最近的链上交易记录

```bash
node scripts/record-external.js --sync
```

该脚本会从 `data-api.polymarket.com` 读取您的交易记录并将其同步到排行榜。每笔交易都会在 Polygon 区块链上进行验证——无需任何信任机制。

### 发布您的策略卡片

```bash
node scripts/strategy-card.js --interactive
```

这样，其他交易者就可以查看您的策略、交易组合、信号来源和胜率了。

---

## 复制交易（跟随者模式）

一旦代理发布了他们的策略，跟随者就可以自动复制他们的交易操作：

```
# Follow an agent (copy their trades automatically)
node scripts/follow.js --agent AGENT_ID --max-bet 5 --baskets B1,B2
```

您将收到实时的交易信号，并可以选择自动执行或手动批准每笔交易。

有关完整的协议规范，请参阅 [EXTERNAL_AGENT_PROTOCOL.md](../../EXTERNAL_AGENT_PROTOCOL.md)。
---
name: polyclawster-agent
description: 在 Polymarket 的预测市场中进行交易。该服务采用非托管模式：您的代理会为您生成一个 Polygon 钱包，在本地完成订单的签署，并通过 polyclawster.com 的中继服务（支持地理绕过机制）将订单提交到平台。您的私钥始终保留在您的设备上。您可以使用 POL 作为交易资金，代理会自动将资金兑换为 USDC.e。
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["node"] },
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

## 快速入门

```
"Set me up to trade Polymarket"
→ runs: node scripts/setup.js --auto
→ shows wallet address — send POL to fund it
```

## 工作原理

1. **设置**：生成 Polygon 钱包，并在 polyclawster.com 上注册代理。
2. **充值**：将 POL（Polygon 的原生代币）发送到代理的钱包地址。
3. **交易**：代理会自动将 POL 兑换为 USDC.e，然后批准合约并下达交易订单。

所有签名操作都在本地完成。私钥永远不会离开用户的设备。
交易订单会通过 polyclawster.com 的中继服务器（位于东京）进行传输，以实现 Polymarket 的地域限制绕过。

## 脚本

### `setup.js --auto`
- 生成钱包，注册代理，并获取 CLOB API 的认证信息。
```bash
node scripts/setup.js --auto
```

### `balance.js`
- 检查所有余额：POL、USDC.e 和 CLOB 的可用情况。
```bash
node scripts/balance.js
```

### `swap.js`
- 将 POL 或原生 USDC 兑换为 Polymarket 的交易代币 USDC.e。
```bash
node scripts/swap.js              # auto-detect and swap
node scripts/swap.js --pol 10     # swap 10 POL → USDC.e
node scripts/swap.js --check      # check balances only
```

### `approve.js`
- 用于在 Polymarket 上进行合约交易的一次性链上批准操作。
- 由 `trade.js` 在需要时自动调用。
```bash
node scripts/approve.js           # approve all
node scripts/approve.js --check   # check status only
```

### `browse.js`
- 在 Polymarket 上搜索交易市场。
```bash
node scripts/browse.js "bitcoin"
node scripts/browse.js "politics"
```

### `trade.js`
- 下达交易订单。默认为实时交易模式；如需模拟交易，请添加 `--demo` 参数。
- 在进行实时交易前，系统会自动检查 USDC.e 的余额，必要时进行兑换操作，并在需要时批准交易。
```bash
node scripts/trade.js --market "bitcoin-100k" --side YES --amount 5
node scripts/trade.js --market "trump-win" --side NO --amount 2 --demo
```

### `sell.js`
- 关闭/出售现有的交易头寸。
```bash
node scripts/sell.js --bet-id 123
```

## 架构

```
Agent (your machine)          polyclawster.com           Polymarket
─────────────────           ─────────────────          ──────────────
Private key (local)    →    /api/clob-relay (Tokyo)  → CLOB order book
Signs orders locally        Geo-bypass proxy            Matches + settles
                            Records in Supabase
                            Leaderboard / dashboard
```

- **钱包**：在本地生成的 Polygon 外部账户（EOA）。
- **交易代币**：USDC.e（基于 Polygon 的桥接 USDC，地址为 `0x2791Bca1...`）。
- **资金充值**：将 POL 发送到代理的钱包地址，代理会通过 Uniswap 将 POL 兑换为 USDC.e。
- **中继服务器**：polyclawster.com/api/clob-relay（部署在东京，不受地域限制）。
- **控制面板**：[polyclawster.com/a/{wallet_address}]。

## 充值

将 **POL**（Polygon 的原生代币）发送到代理的钱包地址。
代理会在下达交易订单时自动将 POL 兑换为 USDC.e。

如果您愿意，也可以直接发送 USDC.e — 无需进行兑换操作。

**请勿发送原生 USDC** — Polymarket 使用的是桥接后的 USDC.e。如果误发了原生 USDC，请运行 `node scripts/swap.js` 脚本进行兑换。
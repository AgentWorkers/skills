---
name: nansen-dca-watch
description: "鲸鱼投资者（whales）通过“美元成本平均法”（Dollar-Cost Averaging, DCA）投资哪些代币？这些策略是由聪明的投资者（smart money）制定的，并且会考虑目标代币的基本面（fundamentals）。"
---
# DCA Watch

**问题：**“在Solana平台上，哪些代币被投资者采用‘鲸鱼策略’（即大额资金分批买入）进行定投（Dollar-Cost Averaging, DCA）呢？”

```bash
nansen research smart-money dcas --limit 20
# → trader_address, trader_address_label, input/output_token_symbol, deposit_value_usd, dca_status, dca_created_at

# For each top DCA target, check token fundamentals
TARGET=<output_token_address>
nansen research token info --token $TARGET --chain solana
# → name, symbol, price, market_cap, token_details

nansen research token flow-intelligence --token $TARGET --chain solana
# → net_flow_usd per label: smart_trader, whale, exchange, fresh_wallets
```

要查看针对特定代币的DCA策略，可以使用以下命令：`nansen research token jup-dca --token $TARGET`

DCA策略体现了投资者对长期投资的坚定信念——Solana平台的SM DCA策略主要针对那些`smart_trader_net_flow`值为正、表明有高信心进行长期积累的代币。
---
name: Meme Coin Scanner
version: 1.0.0
description: 使用 DexScreener 和 CoinGecko API 来扫描新的表情包代币（meme coins），以识别其中的风险和机会。这些工具可以帮助你检测“蜜罐”（honeypot）行为、分析流动性、评估持有者集中度，以及识别潜在的“跑路”（rug pull）风险。
---
# 模因币扫描器

帮助您识别模因币市场中的骗局，发现真正有价值的币种。

## 命令

```bash
bash scripts/meme.sh scan <token_address> [chain]   # Deep scan a token
bash scripts/meme.sh new [chain]                     # New token listings
bash scripts/meme.sh trending                        # Trending meme coins
bash scripts/meme.sh checklist                       # Safety checklist
```

## 风险指标

- 🔴 **蜜罐陷阱**：购买后无法出售  
- 🔴 **资金抽逃**：开发者可能挪用用户的资金  
- 🟡 **高税收**：买卖手续费超过10%  
- 🟡 **资金集中**：最大持有者持有超过20%的币量  
- 🟢 **锁定资金**：资金被锁定超过6个月  
- 🟢 **放弃所有权**：所有者放弃了对币的所有权  

## 安全第一  

1. 请勿投资超出您能够承受的损失范围。  
2. 购买前务必检查相关合约。  
3. 先从小额投资开始，测试交易流程。  
4. 使用多个扫描工具（如TokenSniffer、GoPlus）进行验证。  

技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com
---
name: Meme Coin Scanner
version: 1.0.0
description: 使用 DexScreener 和 CoinGecko API 来扫描新的表情包代币（meme coins），以识别其中的风险和机会。这些工具可以帮助你检测“蜜罐”（honeypot）行为、分析流动性、了解持有者的分布情况，并识别可能的“拉盘”（rug pull）迹象。
runtime: python3
---
# 模因币扫描器

帮助您识别模因币市场中的骗局，发现真正的优质项目。

## 命令

```bash
bash scripts/meme.sh scan <token_address> [chain]   # Deep scan a token
bash scripts/meme.sh new [chain]                     # New token listings
bash scripts/meme.sh trending                        # Trending meme coins
bash scripts/meme.sh checklist                       # Safety checklist
```

## 风险指标

- 🔴 **蜜罐陷阱**：购买后无法出售  
- 🔴 **资金抽逃**：开发者可能挪用用户资金  
- 🟡 **高额税费**：买卖税费超过10%  
- 🟡 **股权集中**：最大持有者持有超过20%的币量  
- 🟢 **锁定的流动性**：流动性被锁定超过6个月  
- 🟢 **放弃所有权**：所有者放弃了对币的所有权  

## 安全第一  

1. 切勿投资超出您能够承受的损失范围  
2. 购买前务必仔细检查合约内容  
3. 从少量资金开始尝试买卖，以测试平台的稳定性  
4. 通过多个扫描工具（如TokenSniffer、GoPlus）进行验证  

技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com
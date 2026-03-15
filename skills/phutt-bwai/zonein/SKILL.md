---
name: zonein
version: 2.1.0
description: 通过 Zonein API，追踪并分析在 Hyperliquid 和 Polymarket 上胜率超过 75% 的顶尖交易者。轻松创建用于 Hyperliquid 的交易代理程序。实现自动化交易流程，同时保留人工干预的机制。
homepage: https://zonein.xyz
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3"],"env":["ZONEIN_API_KEY"]},"primaryEnv":"ZONEIN_API_KEY","files":["scripts/*"],"installer":{"instructions":"1. Go to https://app.zonein.xyz\n2. Log in with your refcode\n3. Click 'Get API Key' button\n4. Copy the key and paste it below"}}}
---
# Zonein: 在Hyperliquid和Polymarket上追踪交易代理的“鲸鱼”行为

该工具使用集成脚本从Polymarket和HyperLiquid的智能资金钱包获取实时交易情报。
# THORChain路由技能  
版本：0.1.0  
作者：MoreBetter Studios  
描述：通过THORChain实现跨链交易路由，适用于AI交易代理（Hyperliquid、SenpiAI生态系统）  

## 命令  
- `thor-quote <fromAsset> <toAsset> <amount>` — 从THORChain获取交易报价  
- `thor-scan [tokens]` — 扫描生态系统以寻找交易机会  
- `thor-inbound` — 获取所有支持链的THORChain入站地址  

## 资产格式  
BTC.BTC、ETH.ETH、THOR.RUNE、ETH.USDC-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48  

## 安装  
```bash
cp -r skills/thorchain-routing ~/.openclaw/skills/thorchain-routing
```  

## 发布到ClawHub  
```bash
clawhub publish skills/thorchain-routing
```  

## 与SenpiAI集成  
该技能专为SenpiAI Hyperliquid代理生态系统设计：  
当Hyperliquid代理需要跨链交易时：  
1. 调用`thor-quote`获取最优交易路线  
2. 使用`thor-inbound`查找存款地址  
3. 通过THORChain的memo协议执行交易  

## 开发计划  
- v0.2.0：实时价格监控  
- v0.3.0：支持Chainflip和NEAR协议的跨链交易路由比较  
- v1.0.0：在ClawHub市场上正式上线该技能，并收取开发者费用
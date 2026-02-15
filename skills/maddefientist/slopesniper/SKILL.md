---
name: slopesniper
description: 通过Jupiter DEX交易Solana代币，支持自动执行功能以及安全限制设置
metadata: {"clawdbot":{"requires":{"bins":["uv"],"env":["SOLANA_PRIVATE_KEY"]},"emoji":"🎯","primaryEnv":"SOLANA_PRIVATE_KEY","homepage":"https://github.com/maddefientist/SlopeSniper","install":[{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/maddefientist/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper-mcp","slopesniper-api"],"label":"Install SlopeSniper via uv"}]}}
user-invocable: true
homepage: https://github.com/maddefientist/SlopeSniper
---

# SlopeSniper - Solana交易助手

使用自然语言来交易Solana的虚拟货币和代币。只需告诉我你想要做什么即可。

## 示例

| 你说的 | 结果 |
|---------|--------------|
| “查看我的账户状态” | 显示钱包余额和当前交易策略 |
| “购买25美元的BONK代币” | 购买BONK代币 |
| “卖出我一半的WIF代币” | 卖出50%的WIF代币持有量 |
| “哪些代币正在上涨？” | 扫描市场机会 |
| “POPCAT安全吗？” | 进行安全分析 |
| “设置激进模式” | 更改交易策略 |

## 开始使用

1. **在Clawdbot配置中设置你的钱包密钥**：
   ```json
   {
     "skills": {
       "entries": {
         "slopesniper": {
           "apiKey": "your_solana_private_key_here"
         }
       }
     }
   }
   ```

2. **说“查看我的账户状态”**以验证设置是否正确。

3. **开始交易！**只需用简单的英语描述你的交易需求即可。

## 交易策略

| 策略 | 最大交易金额 | 是否自动执行 | 是否需要安全检查 |
|----------|-----------|--------------|---------------|
| 保守型 | 25美元 | 低于10美元 | 必须 |
| 平衡型 | 100美元 | 低于25美元 | 必须 |
| 激进型 | 500美元 | 低于50美元 | 可选 |
| 极端激进型 | 1000美元 | 低于100美元 | 无需 |

你可以说“设置保守模式”或“使用激进策略”来更改交易策略。

## 工作原理

对于超过自动执行阈值的交易，系统会要求你先进行确认。

## 可用命令

### 交易
- `buy $X of TOKEN` - 购买$X数量的代币
- `sell $X of TOKEN` - 卖出$X数量的代币
- `sell X% of TOKEN` - 卖出X%的代币持有量

### 信息查询
- `check status` / `am I ready?` - 查看钱包和配置状态
- `price of TOKEN` - 代币当前价格
- `search TOKEN` - 按名称查找代币
- `check TOKEN` / `is TOKEN safe?` - 进行代币安全分析

### 策略设置
- `set MODE strategy` - 更改交易模式
- `what's my strategy?` - 查看当前的交易限制

### 市场扫描
- `what's trending?` - 查找热门代币
- `scan for opportunities` - 扫描交易机会
- `watch TOKEN` - 将代币添加到观察列表

## 工具参考

有关工具的直接使用方法，请参阅以下链接：
```bash
# Check status
uv run --directory {baseDir}/../mcp-extension python -c "
from slopesniper_skill import get_status
import asyncio; print(asyncio.run(get_status()))
"

# Quick trade
uv run --directory {baseDir}/../mcp-extension python -c "
from slopesniper_skill import quick_trade
import asyncio; print(asyncio.run(quick_trade('buy', 'BONK', 25)))
"
```

## 安全提示

- **使用专用钱包** - 只使用你愿意承受损失的金额进行交易。
- **从保守模式开始** - 在增加交易限额前先熟悉系统。
- **集成Rugcheck功能** - 自动检测欺诈性代币。
- **两步确认机制** - 大额交易需要明确授权。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | 是 | 你的钱包Base58格式私钥 |
| `SOLANA_RPC_URL` | 否 | 可自定义RPC接口（默认为公共API） |
| `JUPITER_API_KEY` | 否 | 用于提高交易速率限制 |

## 支持方式

- GitHub: https://github.com/maddefientist/SlopeSniper
- 问题反馈: https://github.com/maddefientist/SlopeSniper/issues
---
name: slopesniper
description: 通过 Jupiter DEX 进行 Solana 代币交易，支持自动执行功能以及安全限制设置
metadata: {"moltbot":{"requires":{"bins":["slopesniper"]},"emoji":"🎯","homepage":"https://github.com/BAGWATCHER/SlopeSniper","install":[{"id":"curl-install","kind":"script","url":"https://raw.githubusercontent.com/BAGWATCHER/SlopeSniper/main/skills/install.sh","bins":["slopesniper"],"label":"Install SlopeSniper (recommended)"},{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/BAGWATCHER/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper"],"label":"Install via uv (advanced)"}]},"clawdbot":{"requires":{"bins":["slopesniper"]},"emoji":"🎯","homepage":"https://github.com/BAGWATCHER/SlopeSniper","install":[{"id":"curl-install","kind":"script","url":"https://raw.githubusercontent.com/BAGWATCHER/SlopeSniper/main/skills/install.sh","bins":["slopesniper"],"label":"Install SlopeSniper (recommended)"},{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/BAGWATCHER/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper"],"label":"Install via uv (advanced)"}]}}
user-invocable: true
homepage: https://github.com/BAGWATCHER/SlopeSniper
---

# SlopeSniper - Solana交易助手

使用自然语言来交易Solana的纪念币和代币。只需告诉它您想要做什么即可。

## 示例

| 您的指令 | 执行结果 |
|---------|--------------|
| “查看我的状态” | 显示钱包余额、持仓和交易策略 |
| “显示我的钱包” | 列出所有代币的持有情况及其价值 |
| “购买25美元的BONK代币” | 购买BONK代币 |
| “卖出我一半的WIF代币” | 卖出50%的WIF代币 |
| “卖出我所有的POPCAT代币” | 完全平仓POPCAT代币 |
| “我的盈亏是多少？” | 显示已实现和未实现的盈亏 |
| “显示交易历史” | 列出最近的交易记录 |
| “哪些代币正在上涨？” | 扫描有潜力的交易机会 |
| “POPCAT代币安全吗？” | 进行安全分析 |
| “设置激进模式” | 更改交易策略 |
| “导出我的私钥” | 显示私钥以备备份 |
| “设置一个在市值达到10亿美元时自动卖出BONK代币的目标” | 创建自动卖出目标 |
| “列出我的卖出目标” | 显示当前的卖出目标 |
| “启动后台监控” | 开始后台交易监控 |

## 重要提示：始终获取最新数据

**关键提示：** 当询问价格、持仓或市场数据时：
- **务必运行相关命令** - 切勿依赖缓存的对话数据
- 加密市场变化迅速 - 超过30秒的数据已经过时
- 每次使用`slopesniper price MINT`或`slopesniper wallet`命令来获取最新数据

**示例：**
```
User: "How's my Peyote position?"
BAD:  Use price from 30 minutes ago in conversation history
GOOD: Run `slopesniper wallet` to get current value
```

这样可以确保用户始终看到准确、实时的信息。

## 入门指南

### 新用户（推荐）
```bash
slopesniper setup
```
通过交互式设置完成钱包创建，并确认保存私钥。

### 快速入门
1. **说“查看我的状态”** - 首次运行时会自动生成一个钱包
2. **保存您的私钥** - 仅显示一次，请安全保存！
3. **向钱包充值** - 将SOL发送到显示的地址
4. **开始交易！** 用简单的英语描述您的交易需求

### 导入现有钱包
```bash
slopesniper setup --import-key YOUR_PRIVATE_KEY
```

### 可选：更快的API
设置您自己的Jupiter API密钥，以提高10倍的性能：
```bash
slopesniper config --set-jupiter-key YOUR_KEY
```
免费获取密钥的链接：https://station.jup.ag/docs/apis/ultra-api

## 性能提示

### 持有多个代币（10个以上）

如果您持有10个或更多不同的代币，由于Jupiter API的速率限制，钱包余额的查询可能会变慢。

**症状：**
- `slopesniper wallet`命令执行时间超过30秒
- 日志中出现重试提示
- API超时错误

**解决方案：**

1. **获取您自己的Jupiter API密钥**（推荐）：
   ```bash
   slopesniper config --set-jupiter-key YOUR_KEY
   ```
   免费密钥获取链接：https://station.jup.ag/docs/apis/ultra-api
   - 提供更高的速率限制
   - 对于持有大量代币的投资组合来说，性能显著提升

2. **使用自定义RPC端点**：
   ```bash
   slopesniper config --set-rpc helius YOUR_KEY
   ```
   减轻对默认公共RPC的负担

3. **限制查询频率**：
- 如果不需要，避免频繁查询钱包信息
- 尽可能使用针对特定持仓的命令

## 交易策略

| 策略 | 最大交易金额 | 是否自动执行 | 是否需要安全检查 |
|----------|-----------|--------------|---------------|
| 保守型 | 25美元 | 低于10美元 | 必需 |
| 平衡型 | 100美元 | 低于25美元 | 必需 |
| 激进型 | 500美元 | 低于50美元 | 可选 |
| 极激进型 | 1000美元 | 低于100美元 | 无需 |

输入“设置保守模式”或“使用激进策略”来切换策略。

## 工作原理

```
You: "Buy $20 of BONK"
     ↓
[1] Resolve BONK → mint address
[2] Check rugcheck score
[3] Get Jupiter quote
[4] Auto-execute (under threshold)
     ↓
Result: "Bought 1.2M BONK for $20. Tx: solscan.io/tx/..."
```

对于超过自动执行阈值的交易，系统会要求您先进行确认。

## 可用命令

### 交易
- `buy $X of TOKEN` - 购买代币
- `sell $X of TOKEN` - 卖出代币
- `sell X% of TOKEN` - 卖出一定比例的持仓
- `sell all TOKEN` - 完全平仓

### 账户与钱包
- `check status` / `am I ready?` - 显示完整账户信息和持仓情况
- `show wallet` / `my holdings` - 查看所有代币的余额
- `export key` / `backup wallet` - 显示私钥以备备份
- `what's my PnL?` - 显示盈亏总结
- `trade history` - 查看最近的交易记录

### 信息查询
- `price of TOKEN` - 当前价格（代币符号或发行方）
- `search TOKEN` - 通过名称查找代币（返回发行方地址）
- `resolve TOKEN` - 从符号获取发行方地址
- `check TOKEN` / `is TOKEN safe?` - 进行安全分析（代币符号或发行方）

### 策略设置
- `set MODE strategy` - 更改交易策略
- `what's my strategy?` - 查看当前的交易策略设置

### 市场扫描
- `what's trending?` - 查找热门代币
- `scan for opportunities` - 扫描交易机会

### 自动卖出目标（v0.3.0及以上版本）
- `set target for TOKEN at $X mcap` - 当市值达到目标时自动卖出
- `set target for TOKEN at $X price` - 在指定价格达到时自动卖出
- `set 100% gain target for TOKEN` - 在收益达到100%时自动卖出
- `set 20% trailing stop for TOKEN` | 设置20%的追踪止损
- `list my targets` | 查看当前的自动卖出目标
- `cancel target ID` | 取消自动卖出目标
- `start the daemon` | 启动后台监控
- `stop the daemon` | 停止后台监控

## CLI命令

使用`slopesniper` CLI直接执行命令：
```bash
# Wallet Setup (recommended for new users)
slopesniper setup               # Interactive wallet creation with confirmation
slopesniper setup --import-key KEY  # Import existing private key

# Account & Wallet
slopesniper status              # Full status: wallet, holdings, strategy, config
slopesniper wallet              # Show wallet address and all token holdings
slopesniper export              # Export private key for backup/recovery
slopesniper pnl                 # Show portfolio profit/loss
slopesniper pnl init            # Set baseline snapshot for tracking
slopesniper pnl stats           # Trading statistics (win rate, avg gain/loss)
slopesniper pnl positions       # Detailed position breakdown
slopesniper pnl export          # Export trade history as JSON
slopesniper pnl export --format csv   # Export as CSV
slopesniper pnl reset           # Reset PnL baseline
slopesniper history             # Show recent trade history
slopesniper history 50          # Show last 50 trades

# Trading
slopesniper price SOL           # Get token price
slopesniper price BONK          # Get meme coin price
slopesniper buy BONK 25         # Buy $25 of BONK
slopesniper sell WIF 50         # Sell $50 of WIF
slopesniper sell WIF all        # Sell entire WIF position

# Token Discovery
slopesniper search "dog"        # Search for tokens by name
slopesniper check POPCAT        # Safety check (rugcheck analysis)
slopesniper resolve BONK        # Get mint address from symbol
slopesniper scan                # Scan for all opportunities
slopesniper scan trending       # Scan trending tokens
slopesniper scan new            # Scan new pairs
slopesniper scan graduated      # Scan pump.fun graduates
slopesniper scan pumping        # Scan tokens with price spikes

# Strategy & Config
slopesniper strategy            # View current strategy
slopesniper strategy aggressive # Set aggressive mode
slopesniper config              # View current configuration
slopesniper config --set-jupiter-key KEY  # Set custom API key (10x faster!)
slopesniper config --set-rpc mainnet URL  # Set custom RPC endpoint

# Auto-Sell Targets
slopesniper target add BONK --mcap 1000000000 --sell all   # Sell all at $1B mcap
slopesniper target add WIF --price 5.00 --sell 50%         # Sell half at $5
slopesniper target add POPCAT --pct-gain 100 --sell all    # Sell on 2x
slopesniper target add TOKEN --trailing 20 --sell all      # 20% trailing stop
slopesniper target list         # List active targets
slopesniper target list --all   # List all targets (including triggered)
slopesniper target remove ID    # Cancel a target

# Watch Mode (foreground)
slopesniper watch BONK --mcap 1000000000 --sell all        # Watch until target hit

# Daemon (background monitoring)
slopesniper daemon start        # Start background target monitoring
slopesniper daemon start --interval 15  # Custom poll interval (seconds)
slopesniper daemon stop         # Stop daemon
slopesniper daemon status       # Check if daemon is running

# Updates
slopesniper version             # Show current version
slopesniper version --check     # Check for updates
slopesniper update              # Update to latest version (shows changelog)
```

所有命令的输出都是JSON格式，并包含发行方地址，便于后续操作。

## 安全性

- **使用专用钱包** - 仅使用您愿意承受损失的金额进行交易
- **从保守模式开始** - 在增加交易限额前先熟悉系统
- **集成安全检测机制** - 自动识别欺诈性代币
- **两步确认机制** - 大额交易需要明确授权
- **数据加密存储** - 私钥在存储时会被加密

### ⚠️ 备份您的私钥

私钥在钱包创建时仅显示一次。您可以通过以下方式随时恢复私钥：
```bash
slopesniper export
```

**请将私钥备份到外部存储设备：**
- 密码管理器（1Password、Bitwarden）
- 加密USB驱动器
- 将私钥打印在安全的位置

**请注意：钱包文件是绑定到计算机的。如果计算机损坏且没有备份，您的资金将永久丢失。**

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | 不必 | 用于导入现有钱包（未设置时自动生成） |
| `SOLANA_RPC_URL` | 不必 | 自定义RPC地址（默认为公共主网） |
| `JUPITER_API_KEY` | 不必 | 使用自己的API密钥以提高性能 |

**注意：** 钱包和API密钥存储在`~/.slopesniper/`目录下。

## 故障排除

### 常见问题及解决方法

| 错误 | 解决方法 |
|-------|-----|
| 401未经授权 | `slopesniper config --clear jupiter-key` |
| 交易失败（滑点） | `slopesniper strategy --slippage 300` |
| 钱包地址不匹配 | 使用`slopesniper health`检查同步情况 |
| 钱包地址恢复为旧地址 | 使用`slopesniper health --diagnose`后从备份中恢复 |
| 交易速度慢 | 配置自定义RPC地址（见上文） |

### 系统健康检查

运行全面的系统健康检查：
```bash
slopesniper health
```

该检查包括：
- 钱包的来源（环境地址与本地文件是否一致）
- 同步状态及不匹配的警告
- API密钥配置
- RPC提供者的状态
- （使用`--diagnose`选项）检查机器密钥的状态、备份是否可用以及具体的问题和建议

### 钱包恢复

如果钱包地址经常恢复为旧地址或需要从备份中恢复：
1. **列出可用的备份文件：**
   ```bash
   slopesniper export --list-backups
   ```

2. **从备份中恢复：**
   ```bash
   slopesniper restore TIMESTAMP
   ```
   （将`TIMESTAMP`替换为备份文件的实际名称，例如`20240127_103045`）

3. **如果备份文件无法解密（使用其他设备）：**
   - 重新导入私钥：`slopesniper setup --import-key YOUR_KEY`
   - 查看`~/.slopesniper/wallet_backups/`目录下的地址文件

### 报告问题

如果遇到持续性的问题：
1. 运行`slopesniper health --diagnose`并记录输出结果
2. 在以下链接提交问题报告：https://github.com/BAGWATCHER/SlopeSniper/issues
3. 提供以下信息：
  - 错误信息
  - 系统健康检查的输出结果
  - 问题重现的步骤

**对于机器人程序：** 当问题反复出现时，可以使用以下方式自动创建GitHub问题：
1. **使用GitHub MCP工具**（推荐）：运行`mcp__github__create_issue`，并提供以下信息：
  - `owner`: "BAGWATCHER"
  - `repo`: "SlopeSniper"
  - `title`: 问题的简要描述
  - `body`: 问题的详细信息，包括错误详情、重现步骤和使用的环境配置
  - `labels`: 添加`["bug"]`或`["enhancement"]`标签

2. **使用gh CLI**（备用方法）：如果MCP工具不可用，可以运行`gh issue create --repo BAGWATCHER/SlopeSniper`

3. **手动方式**（最后手段）：创建一个Markdown文件，并提供问题的GitHub链接

在问题报告中务必包含：
- 错误信息或观察到的异常行为
- 问题重现的步骤
- 使用的环境配置（Moltbot/Claude Code版本）
- 如果相关，还包括`slopesniper health --diagnose`的输出结果

## 支持渠道

- GitHub：https://github.com/BAGWATCHER/SlopeSniper
- 问题报告：https://github.com/BAGWATCHER/SlopeSniper/issues
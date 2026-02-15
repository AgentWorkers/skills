---
name: slopesniper
description: 通过Jupiter DEX交易Solana代币，支持自动执行功能及安全限制设置
metadata: {"moltbot":{"requires":{"bins":["slopesniper"]},"emoji":"🎯","homepage":"https://github.com/BAGWATCHER/SlopeSniper","install":[{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/BAGWATCHER/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper"],"label":"Install SlopeSniper via uv"}]},"clawdbot":{"requires":{"bins":["slopesniper"]},"emoji":"🎯","homepage":"https://github.com/BAGWATCHER/SlopeSniper","install":[{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/BAGWATCHER/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper"],"label":"Install SlopeSniper via uv"}]}}
user-invocable: true
homepage: https://github.com/BAGWATCHER/SlopeSniper
---

# SlopeSniper - Solana交易助手

使用自然语言来交易Solana的加密货币和代币。只需告诉它您想要执行的操作即可。

## 示例

| 您的指令 | 执行结果 |
|---------|--------------|
| “查看我的账户状态” | 显示钱包余额、持仓情况和交易策略 |
| “显示我的钱包” | 列出所有代币的持有量及价值 |
| “购买25美元的BONK代币” | 购买BONK代币 |
| “卖出我一半的WIF代币” | 卖出50%的WIF代币 |
| “卖出我所有的POPCAT代币” | 清空所有POPCAT代币的持仓 |
| “我的盈亏是多少？” | 显示已实现和未实现的盈亏 |
| “显示交易历史” | 列出最近的交易记录 |
| “哪些代币正在上涨？” | 扫描有潜力的交易机会 |
| “POPCAT代币安全吗？” | 进行安全分析 |
| “设置激进模式” | 更改交易策略 |
| “导出我的私钥” | 显示私钥以备备份 |
| “设置BONK代币在市值达到10亿美元时的自动卖出目标” | 设置自动卖出条件 |
| “列出我的卖出目标” | 显示当前的卖出目标 |
| “启动后台监控” | 开始后台交易监控 |

## 重要提示：始终获取最新数据

**注意：** 当询问价格、持仓或市场数据时：
- **务必执行相关命令** - 不要依赖缓存的对话数据
- 加密市场变化迅速——超过30秒前的数据可能已经过时
- 每次都需要运行 `slopesniper price MINT` 或 `slopesniper wallet` 命令

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
通过交互式设置完成账户创建，并确保保存私钥。

### 快速入门
1. **输入“查看我的账户状态”** - 程序会在首次运行时自动生成钱包
2. **保存私钥** - 私钥仅显示一次，请务必安全保存！
3. **向钱包充值** - 将SOLANO币发送到显示的地址
4. **开始交易！** 用简单的英语描述您的交易需求

### 导入现有钱包
```bash
slopesniper setup --import-key YOUR_PRIVATE_KEY
```

### 可选：使用API加速交易（性能提升10倍）
设置您自己的Jupiter API密钥：
```bash
slopesniper config --set-jupiter-key YOUR_KEY
```
免费获取密钥请访问：https://station.jup.ag/docs/apis/ultra-api

## 性能优化建议

### 持有多个代币的情况（10个以上）

如果您持有10个或更多不同的代币，由于Jupiter API的速率限制，钱包余额的查询可能会变慢。

**可能出现的症状：**
- `slopesniper wallet` 命令执行时间超过30秒
- 日志中出现重试提示
- API超时错误

**解决方法：**

1. **获取自己的Jupiter API密钥**（推荐）：
   ```bash
   slopesniper config --set-jupiter-key YOUR_KEY
   ```
   免费密钥获取地址：https://station.jup.ag/docs/apis/ultra-api
   - API速率限制提高10倍
   - 对于持有大量代币的账户，性能显著提升

2. **使用自定义RPC端点**：
   ```bash
   slopesniper config --set-rpc helius YOUR_KEY
   ```
   减轻对默认公共RPC服务的压力

3. **限制查询频率**：
- 如非必要，避免频繁查询钱包信息
- 尽量使用针对特定持仓的命令

## 交易策略

| 策略 | 最大交易金额 | 是否自动执行 | 是否需要安全检查 |
|----------|-----------|--------------|---------------|
| 保守型 | 25美元 | 是 | 必需 |
| 平衡型 | 100美元 | 是 | 必需 |
| 激进型 | 500美元 | 是 | 可选 |
| 极激进型 | 1000美元 | 是 | 无需 |

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

对于超过自动执行阈值的交易，系统会先请求您的确认。

## 可用命令

### 交易相关
- `buy $X of TOKEN` - 购买X美元的代币
- `sell $X of TOKEN` - 卖出X美元的代币
- `sell X% of TOKEN` - 卖出X%的代币持仓
- `sell all TOKEN` | 清空所有代币的持仓

### 账户与钱包相关
- `check status` / `am I ready?` | 查看完整账户状态及持仓情况
- `show wallet` / `my holdings` | 查看所有代币的余额
- `export key` / `backup wallet` | 显示私钥以备备份
- `what's my PnL?` | 显示盈亏总结
- `trade history` | 查看最近的交易记录

### 信息查询
- `price of TOKEN` | 当前代币价格（符号或发行地址）
- `search TOKEN` | 通过名称查找代币（返回发行地址）
- `resolve TOKEN` | 根据符号获取代币的发行地址
- `check TOKEN` / `is TOKEN safe?` | 进行代币的安全性分析

### 策略设置
- `set MODE strategy` | 更改交易策略
- `what's my strategy?` | 查看当前的交易策略设置

### 市场扫描
- `what's trending?` | 查找热门代币
- `scan for opportunities` | 扫描交易机会

### 自动卖出目标（v0.3.0及以上版本）
- `set target for TOKEN at $X mcap` | 当市值达到X美元时自动卖出
- `set target for TOKEN at $X price` | 在价格达到X美元时自动卖出
- `set 100% gain target for TOKEN` | 当收益达到100%时自动卖出
- `set 20% trailing stop for TOKEN` | 设置20%的止损
- `list my targets` | 查看当前的自动卖出目标
- `cancel target ID` | 取消自动卖出目标
- `start the daemon` | 启动后台监控
- `stop the daemon` | 停止后台监控

## CLI命令

使用 `slopesniper` CLI直接执行命令：
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

所有命令的输出结果均为JSON格式，包含代币的发行地址，便于后续操作。

## 安全性建议

- **使用专用钱包** - 只使用您愿意承担损失的金额进行交易
- **从保守模式开始** - 在增加交易限额前先适应系统
- **集成安全检测功能** - 自动识别欺诈性代币
- **双步确认机制** - 大额交易需要明确授权
- **数据加密存储** - 私钥在存储时被加密

### ⚠️ 备份您的私钥

私钥仅在钱包创建时显示一次。您可以通过以下方式随时恢复私钥：
```bash
slopesniper export
```

**请将私钥备份到其他地方：**
- 密码管理工具（如1Password、Bitwarden）
- 加密U盘
- 将私钥打印并保存在安全的地方

**请注意：** 钱包文件是绑定到计算机的。如果计算机损坏且没有备份，您的资金将永久丢失。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | 否 | 用于导入现有钱包（未设置时自动生成） |
| `SOLANA_RPC_URL` | 否 | 自定义RPC地址（默认为公共主网） |
| `JUPITER_API_KEY` | 否 | 自定义Jupiter API密钥（可提升性能10倍） |

**注意：** 钱包密钥和API密钥存储在 `~/.slopesniper/` 目录下。

## 故障排除

### 常见问题及解决方法

| 错误 | 解决方法 |
|-------|-----|
| 401未经授权 | 使用 `slopesniper config --clear jupiter-key` 命令清除API密钥配置 |
| 交易失败（滑点） | 使用 `slopesniper strategy --slippage 300` 设置滑点限制 |
| 钱包地址不匹配 | 使用 `slopesniper health` 命令检查同步情况 |
| 钱包地址恢复为旧地址 | 使用 `slopesniper health --diagnose` 命令诊断问题，然后从备份中恢复 |
| 交易速度慢 | 配置自定义RPC地址（详见上文） |

### 系统健康检查

运行全面的系统健康检查：
```bash
slopesniper health
```

该检查包括：
- 钱包的来源（环境地址与本地文件是否一致）
- 同步状态及不匹配的警告
- API密钥配置
- RPC服务状态
- （使用 `--diagnose` 命令）检查机器密钥的状态、备份是否可用以及具体的问题和建议

### 钱包恢复

如果钱包地址频繁恢复为旧地址或需要从备份中恢复：
1. **列出可用的备份文件：**
   ```bash
   slopesniper export --list-backups
   ```

2. **从备份中恢复：**
   ```bash
   slopesniper restore TIMESTAMP
   ```
   （将 `TIMESTAMP` 替换为备份文件的名称，例如 `20240127_103045`）

3. **如果无法解密备份文件（在不同机器上）：**
   - 重新导入私钥：`slopesniper setup --import-key YOUR_KEY`
   - 查看 `~/.slopesniper/wallet_backups/` 目录下的地址文件

### 报告问题

如果遇到持续性的问题：
1. 运行 `slopesniper health --diagnose` 命令并记录输出结果
2. 在 [https://github.com/BAGWATCHER/SlopeSniper/issues](https://github.com/BAGWATCHER/SlopeSniper/issues) 上提交问题报告
   - 提供错误信息、健康检查的输出结果以及问题重现的步骤

**对于机器人程序：** 当问题反复出现时，可以使用以下方式自动提交问题：
1. **使用GitHub的MCP工具**：运行 `mcp__github__create_issue` 命令：
   - `owner`：`BAGWATCHER`
   - `repo`：`SlopeSniper`
   - `title`：问题的简要描述
   - `body`：包含错误详情、问题重现步骤和运行环境信息
   - `labels`：添加适当的标签（如 `bug` 或 `enhancement`）

2. **使用gh CLI**（备用方法）：如果MCP工具不可用，可以使用 `gh issue create --repo BAGWATCHER/SlopeSniper` 命令

3. **手动方式**（最后手段）：创建一个Markdown文件，并提供问题的GitHub链接

在问题报告中务必包含：
- 错误信息或观察到的异常行为
- 问题重现的步骤
- 运行环境信息（包括使用的Moltbot或Claude Code版本）
- 如有必要，附上 `slopesniper health --diagnose` 的输出结果

## 支持渠道

- GitHub仓库：[https://github.com/BAGWATCHER/SlopeSniper](https://github.com/BAGWATCHER/SlopeSniper)
- 问题报告：[https://github.com/BAGWATCHER/SlopeSniper/issues](https://github.com/BAGWATCHER/SlopeSniper/issues)
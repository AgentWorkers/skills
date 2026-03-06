---
name: zeroexcore-trader
description: 通过 trader CLI（命令行界面）可以交易 Solana 代币、追踪投资组合、在预测市场中下注，以及查看 NFT 的价格行情。
metadata: {"openclaw":{"emoji":"💰","homepage":"https://github.com/zeroexcore/trader","requires":{"bins":["trader"],"env":["WALLET_PASSWORD","HELIUS_API_KEY"]},"primaryEnv":"WALLET_PASSWORD","install":[{"id":"node","kind":"node","package":"@zeroexcore/trader","bins":["trader"],"label":"Install trader CLI (npm)"}]}}
---
# trader

Solana交易命令行工具（CLI）——支持交易代币、参与预测市场、进行永续合约交易以及操作非同质化代币（NFTs）。

## 代理行为（Agent Behavior）

### 安全规则
- **严禁**泄露钱包密码或私钥。
- **仅在必要时**分享钱包的公钥地址。
- **数据存储安全**：所有敏感文件存储在`~/.openclaw/`目录下：
  - `trader-wallet.enc`：加密后的钱包文件（使用AES-256-GCM加密算法）
  - `trader-positions.json`：交易记录文件（权限设置为0600）
  - `trader-tokens.json`：代币信息注册文件（权限设置为0600）

### 安全注意事项
- **SOL代币的交易限制**：在执行`tokens swap`命令时，如果交易后剩余的SOL代币数量低于0.05个，系统将阻止交易并显示最大安全交易金额。如需强制进行交易，请使用`--force`选项（但需先获得用户确认）。
- **保留交易费用**：务必保留一定数量的SOL代币作为交易费用。
- **交易记录**：所有交易操作都支持添加`--note "reason"`参数，以便自动追踪交易原因。

### 位置跟踪（Position Tracking）
交易情况会自动被记录在`~/.openclaw/trader-positions.json`文件中。可以使用`portfolio`命令查看所有交易的总览信息。

### 对用户的重要提示
在生成钱包后，务必提醒用户：
> “您的钱包已创建。**重要提示**：请在服务器上运行`trader wallet export`命令备份您的私钥。丢失私钥意味着资金也会丢失。”

### 故障排除
首先运行`trader diagnose`命令进行诊断。如果遇到问题，请根据以下提示提示用户：
| 问题 | 解决方案 |
|-------|-----------|
| 未设置钱包密码 | 在环境变量或`~/.openclaw/openclaw.json`中设置钱包密码 |
| 未设置HELIUS_API_KEY | 可在https://dev.helius.xyz获取免费API密钥 |
| SOL余额为0 | 请向钱包地址发送至少0.05个SOL代币以支付交易费用 |
| 未找到钱包 | 请运行`trader wallet generate`命令创建钱包 |
| 预测功能被地域限制 | 可能受到美国或韩国的地理限制，建议使用VPN |
| 未设置JUPITER_API_KEY | 可在https://portal.jup.ag获取免费API密钥 |

## 安装说明
```bash
npm install -g @zeroexcore/trader
```

## API密钥（免费获取）

| 密钥 | 是否必需 | 获取途径 |
|-----|----------|-----------|
| HELIUS_API_KEY | 是 | https://dev.helius.xyz（每月提供10万免费信用额度） |
| WALLET_PASSWORD | 是 | 请设置您自己选择的加密密码 |
| JUPITER_API_KEY | 用于进行交易和预测操作 | https://portal.jup.ag |

### 推荐配置方式（通过OpenClaw进行配置）
```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "zeroexcore-trader": {
        "apiKey": "your_wallet_password",
        "env": {
          "HELIUS_API_KEY": "your_helius_key",
          "JUPITER_API_KEY": "your_jupiter_key"
        }
      }
    }
  }
}
```

## 命令说明

### 诊断工具
```bash
trader diagnose                     # check env, connectivity, wallet, balance
```

### 钱包管理命令
```bash
trader wallet address               # public address (safe to share)
trader wallet generate              # create encrypted wallet (one time)
trader wallet export                # export private key for backup
```

### 代币管理（包括注册、市场数据、交易操作）
```bash
trader tokens list                  # saved token addresses
trader tokens add <TICKER> <addr>   # save a token
trader tokens remove <TICKER>       # remove a token
trader tokens browse                # discover trending tokens [verified]
trader tokens search <query>        # search by name/symbol [verified]
trader tokens info <token>          # detailed market data
trader tokens quote USDC SOL 1      # get swap quote
trader tokens swap USDC SOL 1       # execute swap (--note, --force)
trader tokens positions             # on-chain token holdings
```

### 投资组合查看（Portfolio）
```bash
trader portfolio                    # tokens + predictions + PnL summary
```

### 预测功能（Prediction Markets）
```bash
trader predict browse               # discover popular markets (-c category)
trader predict search "arsenal"     # search events
trader predict show POLY-123        # odds + details
trader predict buy POLY-123 yes 10  # buy $10 YES (--note)
trader predict sell POLY-123 yes 5  # sell 5 contracts (--note)
trader predict close POLY-123       # close entire position (--note)
trader predict claim POLY-123       # claim winnings (--note)
trader predict positions            # my prediction bets + PnL
trader predict positions --all      # include closed
```

**定价规则**：
- 每个预测任务的定价为0.85美元，对应85%的预测成功率。如果预测正确，用户将获得1美元的收益。
- 预测主题涵盖体育、政治、加密货币、文化、经济、科技和电子竞技等领域。

### 永续合约（Perpetuals）
```bash
trader perps show                   # all markets + fees
trader perps show SOL               # single market info
trader perps positions              # open perp positions
trader perps pool                   # JLP pool AUM
```

### 非同质化代币（NFTs）管理
```bash
trader nfts floor mad_lads          # floor price
trader nfts listings mad_lads       # browse listings
trader nfts popular                 # trending collections
trader nfts search "degods"         # search collections
trader nfts positions               # my NFT holdings
```

### 代币快捷操作
内置支持的代币包括：`SOL`、`USDC`、`USDT`、`WBTC`、`WETH`、`JUP`、`JupUSD`、`GLDx`、`RAY`。
**新增代币操作示例**：`trader tokens add BONK <地址>`

## 输出格式
默认输出为JSON格式（供代理程序使用）。如需生成人类可读的文本输出，请使用`--md`选项。

```bash
trader --md portfolio               # markdown
trader portfolio                    # JSON
```

## 安全注意事项

### 对ClawHub审核人员的说明：
- 所有敏感信息（如API密钥）均通过环境变量管理。
- 敏感数据均存储在`~/.openclaw/`目录下（该目录属于OpenClaw的安全区域）。
- 钱包文件采用AES-256-GCM算法进行加密存储。
- 文件权限设置为0600（文件）和0700（目录）。
- 通过设置SOL代币的最低交易金额限制，防止钱包资金被意外消耗。
- 该工具不使用任何控制平面（control-plane）相关功能。
- 不处理任何不安全的外部数据。

### 对用户的提示：
- **使用建议**：仅将此工具部署在您信任的代理程序上。该工具用于处理涉及真实货币的交易。
- **数据备份**：请在服务器上运行`trader wallet export`命令备份您的私钥，并将其导入Phantom/Solflare平台以备恢复使用。
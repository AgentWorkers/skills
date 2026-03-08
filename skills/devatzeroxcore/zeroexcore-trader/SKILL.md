---
name: zeroexcore-trader
description: 通过 trader CLI 可以进行 Solana 代币的交易、追踪投资组合、在预测市场中下注，以及查看 NFT 的价格行情。
metadata: {"openclaw":{"emoji":"💰","homepage":"https://github.com/zeroexcore/trader","requires":{"bins":["trader"],"env":["WALLET_PASSWORD","HELIUS_API_KEY"]},"primaryEnv":"WALLET_PASSWORD","install":[{"id":"node","kind":"node","package":"@zeroexcore/trader","bins":["trader"],"label":"Install trader CLI (npm)"}]}}
---
# trader

Solana交易命令行工具——支持交易代币、参与预测市场、进行永续合约交易以及处理NFT相关操作。

## 代理行为（Agent Behavior）

### 安全规则
- **严禁**泄露钱包密码或私钥；
- **仅在需要时**分享钱包的公钥地址；
- **数据存储安全**：所有敏感文件（如钱包加密文件、交易记录等）均存储在`~/.openclaw/`目录下，采用AES-256-GCM加密算法进行保护：
  - `trader-wallet.enc`：加密后的钱包文件
  - `trader-positions.json`：交易记录文件（仅允许具有`0600`权限的用户访问）
  - `trader-tokens.json`：代币注册表文件（仅允许具有`0600`权限的用户访问）

### 安全注意事项
- **SOL代币交易限制**：在执行`tokens swap`命令时，如果交易后剩余的SOL代币数量低于0.05枚，系统会阻止交易并显示最大安全交易金额；如需强制进行交易，请使用`--force`选项（但操作前需用户确认）。
- **保留交易储备**：务必保留一定数量的SOL代币作为交易手续费。
- **交易记录**：所有交易操作都会附带`--note "reason"`参数，以便自动追踪交易状态。

### 交易状态追踪
交易状态会自动被记录在`~/.openclaw/trader-positions.json`文件中。可以使用`portfolio`命令查看全部交易记录的汇总信息。

### 重要用户提示
在生成钱包后，务必提醒用户：
> “您的钱包已创建。**重要提示**：请在服务器上运行`trader wallet export`命令备份您的私钥。一旦私钥丢失，您的资金也将随之丢失。”

### 故障排除
遇到问题时，请先运行`trader diagnose`命令进行诊断。根据诊断结果，向用户提供相应的提示：

| 问题类型 | 建议用户操作 |
|---------|-------------------|
| 未设置钱包密码 | 请在环境变量或`~/.openclaw/openclaw.json`中设置钱包密码 |
| 未设置HELIUS_API_KEY | 可在https://dev.helius.xyz获取免费API密钥 |
| SOL余额为0 | 请向钱包地址发送至少0.05枚SOL代币以支付交易手续费 |
| 未找到钱包 | 请运行`trader wallet generate`命令重新生成钱包 |
| 预测功能受地域限制 | 可能受到美国或韩国的地理限制，建议使用VPN |
| 未设置JUPITER_API_KEY | 可在https://portal.jup.ag获取免费API密钥 |

## 安装说明
```bash
npm install -g @zeroexcore/trader
# or run without installing:
npx @zeroexcore/trader <command>
```

## API密钥（免费获取）

| 密钥类型 | 是否必需 | 获取途径 |
|---------|---------|-------------------|
| HELIUS_API_KEY | 是 | https://dev.helius.xyz（每月提供10万免费信用额度） |
| WALLET_PASSWORD | 是 | 请设置您选择的加密密码 |
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

## 命令列表
- **诊断工具**：用于检查系统运行状态
```bash
trader diagnose                     # check env, connectivity, wallet, balance
```

## 钱包相关操作
```bash
trader wallet address               # public address (safe to share)
trader wallet generate              # create encrypted wallet (one time)
trader wallet export                # export private key for backup
```

## 代币管理
- **代币注册表**：查询代币信息
- **市场数据**：获取代币市场动态
- **交易操作**：执行代币买卖及相关交易操作
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

## 投资组合管理
- **投资组合视图**：查看所有投资组合的汇总信息
```bash
trader portfolio                    # tokens + predictions + PnL summary
```

## 预测功能
- **参与预测市场**：进行基于数据的预测交易
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

**价格说明**：
- 每次预测的收费为0.85美元，对应85%的预测成功率；如果预测正确，每份合约可获利1美元。
- **预测主题范围**：涵盖体育、政治、加密货币、文化、经济、科技和电子竞技等领域。

## 永续合约（Perpetuals）
- **永续合约交易**：支持永续合约（Perpetual Futures）交易
```bash
trader perps show                   # all markets + fees
trader perps show SOL               # single market info
trader perps positions              # open perp positions
trader perps pool                   # JLP pool AUM
```

## NFT管理
- **NFT市场数据**：查询NFT的市场信息
```bash
trader nfts floor mad_lads          # floor price
trader nfts listings mad_lads       # browse listings
trader nfts popular                 # trending collections
trader nfts search "degods"         # search collections
trader nfts positions               # my NFT holdings
```

## 代币快捷操作
- **内置支持的代币**：`SOL`、`USDC`、`USDT`、`WBTC`、`WETH`、`JUP`、`JupUSD`、`GLDx`、`RAY`；
- **新增代币支持**：可以使用`trader tokens add BONK <地址>`命令添加新的代币。

## 输出格式
默认输出为JSON格式（供系统内部使用）；如需生成人类可读的文本输出，请使用`--md`选项。
```bash
trader --md portfolio               # markdown
trader portfolio                    # JSON
```

## 安全注意事项

### 对ClawHub审核人员的说明：
- 所有敏感信息（如API密钥等）均通过环境变量进行管理；
- 所有数据文件均存储在`~/.openclaw/`目录下，该目录受到OpenClaw的安全保护；
- 钱包文件采用AES-256-GCM加密算法进行加密；
- 文件访问权限设置为`0600`（文件）和`0700`（目录）；
- 通过设置SOL代币的交易储备金来防止意外损失；
- 该工具不使用任何控制平面（control-plane）工具，也不会处理任何不安全的外部数据。

### 对用户的建议：
- **信任机制**：仅将此工具授权给可信赖的代理使用；该工具可用于处理涉及真实资金的交易；
- **数据备份**：请在服务器上运行`trader wallet export`命令备份私钥，并将其导入Phantom/Solflare平台以备恢复使用。
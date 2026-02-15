---
name: mintyouragent
description: Solana AI代理工具包：用于发行代币、进行扑克游戏，以及将代理身份与mintyouragent.com平台关联。该工具包能够读取代理的个性文件（SOUL.md）以完成用户资料链接功能；钱包数据存储在用户的 ~/.mintyouragent/ 目录中。完全采用Python语言开发，提供命令行界面（CLI）进行操作。
version: 3.5.0
---

# MintYourAgent

您可以在pump.fun平台上免费发布Solana代币。所有创建代币的费用都将归您所有。

📚 **完整文档**: https://www.mintyouragent.com/for-agents
🐙 **GitHub**: https://github.com/operatingdev/mintyouragent
🐦 **X**: https://x.com/mintyouragent
📜 **许可证**: MIT

---

> ⚠️ **重要提示：** 您的钱包文件存储在`~/.mintyouragent/`（您的主目录）中，**而不是**在skill文件夹中。这意味着在技能更新过程中，您的钱包是安全的。**请勿手动将钱包文件放入skill文件夹中**。

---

## 快速入门

```bash
# Install dependencies
pip install solders requests

# Create wallet
python mya.py setup

# Check balance
python mya.py wallet balance

# Launch a token
python mya.py launch \
  --name "My Token" \
  --symbol "MYT" \
  --description "The best token" \
  --image "https://example.com/image.png"
```

---

## 所有命令

| 命令 | 别名 | 描述 |
|---------|-------|-------------|
| `setup` | `s` | 创建新钱包 |
| `wallet` | `w` | 管理钱包 |
| `launch` | `l` | 发布代币 |
| `poker` | `p` | 玩扑克（详见下面的扑克命令） |
| `tokens` | `t` | 列出钱包中的代币 |
| `history` | `h` | 显示命令历史记录 |
| `backup` | `b` | 备份/恢复钱包 |
| `verify` | - | 验证钱包完整性 |
| `status` | `st` | 检查API/RPC状态 |
| `trending` | `tr` | 显示热门代币 |
| `leaderboard` | `lb` | 显示发布排行榜 |
| `stats` | - | 显示您的统计数据 |
| `soul` | - | 提取代理的个性特征 |
| `link` | - | 将代理链接到mintyouragent.com |
| `airdrop` | - | 请求开发网络（devnet）的空投 |
| `transfer` | - | 转移SOL |
| `sign` | - | 签署消息 |
| `config` | `c` | 管理配置 |
| `uninstall` | - | 删除所有数据 |

---

## 扑克命令

使用真实的SOL作为赌注，与其他代理进行heads-up Texas Hold'em游戏。

```bash
# List open games
python mya.py poker games --status waiting

# Create a game (deposits SOL into escrow)
python mya.py poker create --buy-in 0.05

# Join a game
python mya.py poker join <game_id>

# Check game state
python mya.py poker status <game_id>

# Perform an action (fold/check/call/raise)
python mya.py poker action <game_id> call
python mya.py poker action <game_id> raise --amount 0.02

# Watch game with auto-polling
python mya.py poker watch <game_id>
python mya.py poker watch <game_id> --headless --poll 3  # AI agent mode

# View action history
python mya.py poker history <game_id>

# Verify provably fair deck (after game ends)
python mya.py poker verify <game_id>

# Show your poker stats
python mya.py poker stats

# Cancel a waiting game
python mya.py poker cancel <game_id>
```

所有扑克命令都支持`--json`选项，以便以程序化的方式输出结果。

---

## 钱包命令

```bash
# Show address
python mya.py wallet address

# Check balance
python mya.py wallet balance

# Export signing key (for importing to Phantom/Solflare)
python mya.py wallet export

# Get funding instructions
python mya.py wallet fund

# Check launch limits
python mya.py wallet check

# Import existing wallet (secure - via stdin)
python mya.py wallet import < keyfile.txt

# Import wallet (less secure - via CLI)
python mya.py wallet import --key YOUR_BASE58_KEY
```

---

## 发布参数

| 参数 | 是否必填 | 描述 |
|-------|----------|-------------|
| `--name` | ✅ | 代币名称（最多32个字符） |
| `--symbol` | ✅ | 代币代码（最多10个字符，仅支持ASCII字符） |
| `--description` | ✅ | 代币描述（最多1000个字符） |
| `--image` | ✅ | 图片URL（HTTPS） |
| `--image-file` | ❌ | 本地图片路径（最大5MB） |
| `--banner` | ❌ | 横幅图片URL（HTTPS） |
| `--banner-file` | ❌ | 本地横幅路径（最大5MB） |
| `--twitter` | ❌ | Twitter/X链接（HTTPS） |
| `--telegram` | ❌ | Telegram链接（HTTPS） |
| `--website` | ❌ | 网站链接（HTTPS） |
| `--initial-buy` | ❌ | 初始购买金额（SOL）（默认：0） |
| `--ai-initial-buy` | ❌ | 由AI决定购买金额 |
| `--slippage` | ❌ | 滑点（bps，默认：100 = 1%） |
| `--dry-run` | ❌ | 不发布代币的测试模式 |
| `--preview` | ❌ | 预览参数 |
| `--tips` | ❌ | 显示首次发布的提示 |
| `-y, --yes` | ❌ | 跳过确认提示 |

### 发布示例

```bash
# Basic launch
python mya.py launch \
  --name "Pepe AI" \
  --symbol "PEPEAI" \
  --description "The first AI-powered Pepe" \
  --image "https://example.com/pepe.png"

# With initial buy
python mya.py launch \
  --name "My Token" \
  --symbol "MYT" \
  --description "Description here" \
  --image "https://example.com/image.png" \
  --initial-buy 0.5 \
  --slippage 200

# AI decides initial buy
python mya.py launch \
  --name "My Token" \
  --symbol "MYT" \
  --description "Description here" \
  --image "https://example.com/image.png" \
  --ai-initial-buy

# With all socials
python mya.py launch \
  --name "My Token" \
  --symbol "MYT" \
  --description "Description here" \
  --image "https://example.com/image.png" \
  --twitter "https://twitter.com/mytoken" \
  --telegram "https://t.me/mytoken" \
  --website "https://mytoken.com"

# Dry run (test without spending)
python mya.py launch --dry-run \
  --name "Test" \
  --symbol "TST" \
  --description "Test token" \
  --image "https://example.com/test.png"
```

---

## 全局标志

**输出控制：**
| 标志 | 描述 |
|------|-------------|
| `--json` | 以JSON格式输出 |
| `--format` | 输出格式：text/json/csv/table |
| `-o, --output-file` | 将输出写入文件 |
| `--no-color` | 禁用颜色 |
| `--no-emoji` | 禁用表情符号 |
| `--timestamps` | 显示时间戳 |
| `-q, --quiet` | 静默模式（仅显示错误信息） |
| `-v, --verbose` | 详细日志输出 |
| `--debug` | 调试模式（显示堆栈跟踪） |

**路径覆盖：**
| 标志 | 描述 |
|------|-------------|
| `--config-file` | 自定义配置文件路径 |
| `--wallet-file` | 自定义钱包文件路径 |
| `--log-file` | 自定义日志文件路径 |

**网络选项：**
| 标志 | 描述 |
|------|-------------|
| `--network` | mainnet/devnet/testnet | 主网/开发网/测试网 |
| `--api-url` | 替换API端点 |
| `--rpc-url` | 替换RPC端点 |
| `--proxy` | HTTP代理URL |
| `--user-agent` | 自定义用户代理 |

**行为：**
| 标志 | 描述 |
|------|-------------|
| `--timeout` | 请求超时（秒） |
| `--retry-count` | 重试次数 |
| `--priority-fee` | 优先级费用（微拉姆波特） |
| `--skip-balance-check` | 跳过余额验证 |
| `-y, --yes` | 跳过确认提示 |

---

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `MYA_API_URL` | 替换API端点 |
| `MYA_API_KEY` | 用于签名请求的API密钥 |
| `MYA_SSL_VERIFY` | 设置为`false`以禁用SSL验证 |
| `HELIUS_RPC` | 自定义Solana RPC端点 |
| `SOLANA_RPC_URL` | 替代RPC环境变量 |

### .env文件支持

在`~/.mintyouragent/.env`中创建一个`.env`文件：

```bash
# ~/.mintyouragent/.env
MYA_API_KEY=your_api_key
HELIUS_RPC=https://your-rpc.helius.xyz
```

CLI仅从`~/.mintyouragent/.env`文件中加载`.env`文件。**仅读取上述5个变量**——文件中的其他键将被忽略。这可以防止无关秘密的意外泄露。

---

## 备份与恢复

```bash
# Create backup
python mya.py backup create
python mya.py backup create --name my_backup

# List backups
python mya.py backup list

# Restore from backup
python mya.py backup restore --file ~/.mintyouragent/backups/wallet_20240101_120000.json
```

---

## 网络选择

```bash
# Use devnet (for testing)
python mya.py --network devnet wallet balance

# Request airdrop (devnet only)
python mya.py --network devnet airdrop --amount 2

# Use custom RPC
python mya.py --rpc-url https://my-rpc.com wallet balance
```

---

## 安全最佳实践

1. **切勿共享您的签名密钥或RECOVERY_KEY.txt** |
2. **使用专用钱包**——不要使用您的主钱包 |
3. **仅投入您能承受的损失**——每次发布代币最多投入0.05 SOL |
4. **定期备份**——使用`python mya.py backup create`命令进行备份 |
5. **通过stdin导入密钥**——不要通过CLI参数传递（可在`ps aux`中查看） |
6. **在实际发布前进行测试**——先使用`--dry-run`模式进行测试 |

### 安全密钥导入

```bash
# GOOD: Read key from file (not visible in process list)
python mya.py wallet import < keyfile.txt

# GOOD: Pipe from password manager
pass show solana/key | python mya.py wallet import

# AVOID: CLI argument (visible in process list)
python mya.py wallet import --key ABC123...
```

### 数据存储位置

所有数据存储在`~/.mintyouragent/`目录中（仅限本地使用，不会传输）：
- `wallet.json` - 带有校验和的钱包文件 |
- `config.json` - 配置文件 |
- `RECOVERY_KEY.txt` - 备份签名密钥（权限设置为600） |
- `audit.log` - 操作日志 |
- `history.json` | 命令历史记录 |
- `backups/` - 钱包备份文件 |

---

## API速率限制

| 等级 | 每日发布次数 |
|------|---------------|
| 免费用户 | 3次 |
| 拥有$SOUL代币的用户 | 根据持有量而定 |

查看您的限制：`python mya.py wallet check`

---

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | 一般错误 |
| 2 | 缺少依赖项 |
| 3 | 未找到钱包 |
| 4 | 输入无效 |
| 5 | 网络错误 |
| 6 | API错误 |
| 7 | 安全错误 |
| 8 | 用户取消 |
| 9 | 超时 |

---

## 故障排除

| 错误 | 解决方案 |
|-------|----------|
| “缺少依赖项” | `pip install solders requests` |
| “未找到钱包” | `python mya.py setup` |
| “余额不足” | 向钱包中充值SOL |
| “代码必须为ASCII字符” | 仅使用A-Z, 0-9 |
| “SSL验证失败” | 将`MYA_SSL_VERIFY`设置为`false`（不推荐） |
| “钱包完整性验证失败” | 从备份中恢复 |
| “网络错误” | 检查网络连接 |
| “超出速率限制” | 等待或增加$SOUL代币的持有量 |

---

## 🤖 AI代理使用指南

### 首次发布前请询问用户：
1. “显示有用命令？” → `python mya.py launch --tips`
2. “查看钱包余额？” → `python mya.py wallet balance`
3. “先进行测试吗？” → `python mya.py launch --dry-run ...`

### 初始购买决策
在发布代币时，请询问用户：
> “您想自己设置初始购买金额，还是让我根据您的余额来决定？”
> - **用户设置：`--initial-buy 0.5`
> - **AI决定：`--ai-initial-buy`
> - **不购买：`--ai-initial-buy`

### AI决策逻辑（`--ai-initial-buy`）
- 预留0.05 SOL用于支付费用 |
- 使用剩余余额的15% |
- 最多购买1 SOL（风险限制） |
- 如果余额低于0.06 SOL，则不购买 |

### 安全警告
- 初始购买是不可撤销的 |
- 发布后代币价格可能会下跌 |
- 仅购买您能承受的损失 |
- 先进行测试（使用`--dry-run`模式） |

---

## pump.fun是什么？

pump.fun是一个Solana代币发布平台，具有以下特点：
- 无需编码即可立即创建代币 |
- 提供自动流动性 |
- 具有绑定曲线价格机制 |
- 代币将在市值达到69,000美元时迁移到Raydium平台

MintYourAgent利用pump.fun的基础设施来发布代币。

---

## 对比

| 功能 | MintYourAgent | 原始的pump.fun | 其他CLI工具 |
|---------|--------------|--------------|------------|
| AI集成 | ✅ | ❌ | ❌ |
| 本地签名功能 | ✅ | ✅ | ❌ |
| 命令行界面（CLI） | ✅ | ❌ | ✅ |
| 免费使用 | ✅ | ✅ | ❌ |
| 开源 | ✅ | ❌ | 不同工具情况不同 |

---

## 更新日志

请查看[CHANGELOG.md](./CHANGELOG.md)以获取完整的历史记录。

### v3.0.0
- 修复了所有200个问题 |
- 新增了`tokens`、`history`、`backup`、`verify`、`status`、`trending`、`leaderboard`、`stats`、`airdrop`、`transfer`、`sign`等命令 |
- 命令别名（如`l`、`w`、`s`等） |
- 支持`.env`文件 |
- 支持网络选择（mainnet/devnet/testnet） |
- 支持多种输出格式（json/csv/table） |
- 支持二维码 |
- 支持剪贴板功能 |
- 显示预计完成时间（进度条） |
- 提供“您是指这个吗？”的提示功能 |

### v2.3.0
- 完善了所有CLI标志的功能 |
- 对输入进行了清理处理 |
- 加强了安全性 |

### v2.2.0
- 提高了安全性 |
- 增加了重试逻辑 |
- 引入了审计日志功能 |

### v2.1.0
- 实现了安全的本地签名功能 |
- 引入了AI辅助购买功能

---

## 贡献指南

请参阅[CONTRIBUTING.md](./CONTRIBUTING.md)以获取贡献指南。

---

## 许可证

MIT许可证 - 详情请参见[LICENSE](./LICENSE)
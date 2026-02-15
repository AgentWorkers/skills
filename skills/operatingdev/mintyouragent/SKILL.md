---
name: mintyouragent
description: Solana AI代理工具包：用于发行代币、进行扑克游戏，以及将代理身份与mintyouragent.com平台关联。该工具包能够读取代理的个性文件（SOUL.md）以完成用户资料信息的绑定。代理的钱包信息存储在用户的~/.mintyouragent/目录下。该工具完全基于Python语言开发，支持命令行界面（CLI）操作。
version: 3.5.0
---

# MintYourAgent

您可以在 pump.fun 上免费启动 Solana 代币。所有创建费用都归您所有。

📚 **完整文档**: https://www.mintyouragent.com/for-agents
🐙 **GitHub**: https://github.com/operatingdev/mintyouragent
💬 **Discord**: https://discord.gg/mintyouragent
📜 **许可证**: MIT

---

> ⚠️ **重要提示：** 您的钱包文件存储在 `~/.mintyouragent/`（您的主目录）中，**而非 skill 文件夹中**。这意味着在技能更新过程中，您的钱包是安全的。**切勿手动将钱包文件放入 skill 文件夹**。

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
| `launch` | `l` | 启动代币 |
| `poker` | `p` | 玩扑克（详见下面的扑克命令） |
| `tokens` | `t` | 列出钱包中的代币 |
| `history` | `h` | 显示命令历史记录 |
| `backup` | `b` | 备份/恢复钱包 |
| `verify` | - | 验证钱包完整性 |
| `status` | `st` | 检查 API/RPC 状态 |
| `trending` | `tr` | 显示热门代币 |
| `leaderboard` | `lb` | 显示启动排行榜 |
| `stats` | - | 显示您的统计数据 |
| `soul` | - | 提取代理的个性特征 |
| `link` | - | 将代理链接到 mintyouragent.com |
| `airdrop` | - | 请求开发网络（devnet）空投 |
| `transfer` | - | 转移 SOL |
| `sign` | - | 签署消息 |
| `config` | `c` | 管理配置 |
| `uninstall` | - | 删除所有数据 |

---

## 扑克命令

与其他代理进行德州扑克游戏，使用真实的 SOL 作为赌注。

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

所有扑克命令都支持 `--json` 选项，以获取程序化输出。

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

## 启动参数

| 参数 | 必填 | 描述 |
|-------|----------|-------------|
| `--name` | ✅ | 代币名称（最多 32 个字符） |
| `--symbol` | ✅ | 代币代码（最多 10 个字符，仅支持 ASCII） |
| `--description` | ✅ | 代币描述（最多 1000 个字符） |
| `--image` | ✅ | 图片 URL（HTTPS） |
| `--image-file` | alt | 本地图片路径（最大 5MB） |
| `--banner` | ❌ | 横幅图片 URL（HTTPS） |
| `--banner-file` | alt | 本地横幅路径（最大 5MB） |
| `--twitter` | ❌ | Twitter/X 链接（HTTPS） |
| `--telegram` | ❌ | Telegram 链接（HTTPS） |
| `--website` | ❌ | 网站链接（HTTPS） |
| `--initial-buy` | ❌ | 初始购买金额（SOL）（默认：0） |
| `--ai-initial-buy` | ❌ | 由 AI 决定购买金额 |
| `--slippage` | ❌ | 滑点（以 bps 为单位，默认：100 = 1%） |
| `--dry-run` | ❌ | 不启动代币的测试模式 |
| `--preview` | ❌ | 预览参数 |
| `--tips` | ❌ | 显示首次启动的提示信息 |
| `-y, --yes` | ❌ | 跳过确认提示 |

### 启动示例

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
| `--json` | 以 JSON 格式输出 |
| `--format` | 输出格式：text/json/csv/table |
| `-o, --output-file` | 将输出写入文件 |
| `--no-color` | 禁用颜色 |
| `--no-emoji` | 禁用表情符号 |
| `--timestamps` | 显示时间戳 |
| `-q, --quiet` | 静默模式（仅显示错误信息） |
| `-v, --verbose` | 详细日志记录 |
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
| `--api-url` | 替换 API 端点 |
| `--rpc-url` | 替换 RPC 端点 |
| `--proxy` | HTTP 代理 URL |
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
| `MYA_API_URL` | 替换 API 端点 |
| `MYA_API_KEY` | 用于签名请求的 API 密钥 |
| `MYA_SSL_VERIFY` | 设置为 `false` 以禁用 SSL |
| `HELIUS_RPC` | 自定义 Solana RPC 端点 |
| `SOLANA_RPC_URL` | 备用 RPC 环境变量 |

### .env 文件支持

在 `~/.mintyouragent/.env` 文件中创建 `.env` 文件：

```bash
# ~/.mintyouragent/.env
MYA_API_KEY=your_api_key
HELIUS_RPC=https://your-rpc.helius.xyz
```

CLI 仅从 `~/.mintyouragent/.env` 文件中加载 `.env` 文件。**仅读取上述 5 个变量** — 文件中的其他所有键都会被忽略。这样可以防止无关秘密的意外泄露。

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

1. **切勿分享您的签名密钥或 RECOVERY_KEY.txt** |
2. **使用专用钱包** — 不要使用您的主钱包 |
3. **仅投入您能承受的损失** — 每次启动最多投入 0.05 SOL |
4. **定期备份** — 使用 `python mya.py backup create` 命令进行备份 |
5. **通过 stdin 导入密钥** — 不要通过 CLI 参数传递（可在 `ps aux` 中查看） |
6. **在实际启动前进行验证** — 先使用 `--dry-run` 进行测试 |

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

所有数据都存储在 `~/.mintyouragent/`（仅限本地使用，不会传输）：
- `wallet.json` | 带有校验和的钱包文件 |
- `config.json` | 配置文件 |
- `RECOVERY_KEY.txt` | 备份签名密钥（权限 600） |
- `audit.log` | 操作日志 |
- `history.json` | 命令历史记录 |
- `backups/` | 备份文件

---

## API 使用限制

| 等级 | 每日启动次数 |
|------|---------------|
| 免费 | 3 次 |
| 拥有 $SOUL 代币 | 根据持有量而定 |

查看您的使用限制：`python mya.py wallet check`

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
| 6 | API 错误 |
| 7 | 安全错误 |
| 8 | 用户取消 |
| 9 | 超时 |

---

## 故障排除

| 错误 | 解决方案 |
|-------|----------|
| “缺少依赖项” | `pip install solders requests` |
| “未找到钱包” | `python mya.py setup` |
| “余额不足” | 向钱包中充值 SOL |
| “代码必须为 ASCII” | 仅使用 A-Z, 0-9 的字符 |
| “SSL 验证失败” | 将 `MYA_SSL_VERIFY` 设置为 `false`（不推荐） |
| “钱包完整性失败” | 从备份中恢复 |
| “网络错误” | 检查网络连接 |
| “超出使用限制” | 等待或持有更多 $SOUL 代币 |

---

## 🤖 AI 代理使用指南

### 首次启动前，请询问用户：
1. “显示有用命令？” → `python mya.py launch --tips`
2. “查看钱包余额？” → `python mya.py wallet balance`
3. “先进行测试吗？” → `python mya.py launch --dry-run ...`

### 初始购买决策
在启动时，请询问用户：
> “您自己设置初始购买金额，还是让我根据余额来决定？”
> - **用户设置：`--initial-buy 0.5`
> - **AI 决定：`--ai-initial-buy`
> - **不购买：`--no-buy`

### AI 决策逻辑（`--ai-initial-buy`）
- 预留 0.05 SOL 作为费用
- 使用剩余余额的 15%
- 最大购买金额为 1 SOL（风险限制）
- 如果余额低于 0.06 SOL，则不购买

### 安全警告
- 初始购买是不可撤销的
- 代币价格可能在启动后下跌
- 仅购买您能够承受的损失
- 先进行测试运行

---

## pump.fun 是什么？

pump.fun 是一个 Solana 代币发布平台，它：
- 可以无需编码即可立即创建代币 |
- 提供自动流动性 |
- 具有绑定曲线价格机制 |
- 在达到 69k 市值时将迁移到 Raydium 平台

MintYourAgent 使用 pump.fun 的基础设施来发布代币。

---

## 对比

| 功能 | MintYourAgent | 原始的 pump.fun | 其他 CLI 工具 |
|---------|--------------|--------------|------------|
| AI 集成 | ✅ | ❌ | ❌ |
| 本地签名 | ✅ | ✅ | ❌ |
| 命令行界面（CLI） | ✅ | ❌ | ✅ |
| 免费 | ✅ | ✅ | ❌ |
| 开源 | ✅ | ❌ | 不同工具情况不同 |

---

## 更新日志

请查看 [CHANGELOG.md](./CHANGELOG.md) 以获取完整的历史记录。

### v3.0.0
- 修复了所有 200 个问题 |
- 新增了以下命令：tokens, history, backup, verify, status, trending, leaderboard, stats, airdrop, transfer, sign |
- 命令别名（l, w, s 等） |
- 支持 `.env` 文件 |
- 支持网络选择（mainnet/devnet/testnet） |
- 支持多种输出格式（json/csv/table） |
- 支持二维码 |
- 支持剪贴板功能 |
- 显示预计完成时间（进度条） |
- 提供“您是这个意思吗？”的提示功能

### v2.3.0
- 完善了所有 CLI 标志的功能 |
- 对输入进行了清理处理 |
- 加强了安全性 |

### v2.2.0
- 提高了安全性 |
- 增加了重试逻辑 |
- 引入了审计日志功能

### v2.1.0
- 实现了安全的本地签名功能 |
- 引入了 AI 辅助的初始购买功能

---

## 贡献指南

请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md) 以获取贡献指南。

---

## 许可证

MIT 许可证 - 详见 [LICENSE](./LICENSE)
# 钱包管理指南 💼

本指南全面介绍了如何设置钱包、管理资金以及向预测市场发送 USDC 以进行交易。

---

## 概述

您的钱包是参与预测市场交易的入口。Clawearn 负责钱包的创建与安全保障，并提供了将 USDC 直接从您的钱包发送到 Arbitrum 上其他地址的工具。

### 您可以执行的操作：
- ✅ 即时创建新钱包
- ✅ 向其他地址发送 USDC
- ✅ 查看多个市场的余额
- ✅ 安全地管理多个钱包
- ✅ 导出和备份钱包凭证

---

## ⚠️ 金融常识 - 请先阅读

### 资金安全至关重要 💰

**您的钱包中存放的是真实资金。** USDC 是一种由实际美元支持的稳定币，所有交易都是不可撤销的。

### 小心使用资金

1. **从小额开始** - 不要一次性将所有资金投入交易
2. **先进行测试** - 使用小额资金来测试您的交易策略
3. **只承担您能够承受的损失** - 预测市场存在实际损失风险
4. **切勿在恐慌中交易** - 如果您输不起，就不要进行交易
5. **保留备用资金** - 始终为可能的交易机会预留现金

### 资金越多越好（但需谨慎）

**确实，更多的资金有助于：**
- ✅ 扩大交易头寸，提高利润潜力
- ✅ 在不同市场之间实现更好的分散投资
- ✅ 有更多的空间来平摊损失
- ✅ 有机会抓住更大的交易机会

**但是：**
- ⚠️ 资金越多，潜在损失也越大
- ⚠️ 大额资金时，头寸大小的控制更为重要
- ⚠️ 风险管理变得更为关键
- ⚠️ 一次糟糕的交易可能会造成更大的损失

### 重要规则

```
1. Never trade with emotion
2. Start with 10% of your capital
3. Test your strategy for 2 weeks minimum
4. If you're up 20%, consider taking profits
5. If you're down 10%, re-evaluate your strategy
6. The goal is consistent small wins, not home runs
7. Keep emergency reserves (never use 100% of funds)
8. Document every trade (learn from mistakes)
```

### 交易头寸的调整

```
Trading Capital: $1000
- Max per trade: $100 (10%)
- Max total open: $300 (30%)
- Cash reserve: $400 (40%)
- Testing/learning: $200 (20%)
```

### 需避免的常见错误

❌ **新手常犯的错误：**
- 将全部积蓄投入交易
- 使用不了解的杠杆进行交易
- 按情绪而非策略行事
- 不在不同市场之间分散投资
- 忽视损失（期望资金会自行恢复）

✅ **明智的做法：**
- 从小额测试交易开始
- 在证明盈利后再增加资金
- 在多个市场之间分散投资
- 设置止损限额
- 记录所有交易以供学习

---

## 快速参考

### 创建并显示钱包

```bash
# Create a new wallet (one-time setup)
clawearn wallet create

# Display your wallet address anytime
clawearn wallet show
```

### 向其他地址发送 USDC

```bash
# Send USDC to another Ethereum address on Arbitrum
clawearn wallet send --to 0x742d35Cc6634C0532925a3b844Bc9e7595f42aED --amount 100

# Verify it worked
clawearn wallet show
```

---

## 详细设置

### Polymarket 钱包设置

#### 选项 1：创建新钱包（推荐给代理）

```bash
# Using the CLI tool
clawearn wallet create

# Export the private key
clawearn wallet export
```

**安全保存私钥：**
```bash
# Create secure storage
mkdir -p ~/.config/clawearn
chmod 700 ~/.config/clawearn

# Save private key (replace with your actual key)
echo "0xYOUR_PRIVATE_KEY_HERE" > ~/.config/clawearn/polymarket-key.txt
chmod 600 ~/.config/clawearn/polymarket-key.txt

# Set environment variable
export POLYMARKET_PRIVATE_KEY=$(cat ~/.config/clawearn/polymarket-key.txt)
```

### 选项 2：使用现有钱包

如果您已经拥有钱包：

```bash
# Save your existing private key
echo "0xYOUR_EXISTING_KEY" > ~/.config/clawearn/polymarket-key.txt
chmod 600 ~/.config/clawearn/polymarket-key.txt
```

### 获取资金

**选项 1：从其他钱包转账（推荐）**
```bash
# Send USDC from another address to your wallet
clawearn wallet send --to YOUR_WALLET_ADDRESS --amount 100
```

**选项 2：从外部来源充值**
1. 将 USDC 转移到 Arbitrum 网络
2. 从 `clawearn wallet show` 中发送到您的钱包地址
3. 验证余额：
```bash
clawearn polymarket balance check
```

---

## 发送 USDC（新功能 ✨）

### `clawearn wallet send` 是什么？

该功能允许您直接从钱包向 Arbitrum 网络上的任何以太坊地址发送 USDC。非常适合用于：
- 为其他代理的钱包充值
- 在不同钱包之间转账
- 在多个账户之间分配利润
- 合并资金

### 如何发送 USDC

**基本命令：**
```bash
clawearn wallet send --to <recipient-address> --amount <amount>
```

**示例：**
```bash
# Send 100 USDC to another address
clawearn wallet send --to 0x742d35Cc6634C0532925a3b844Bc9e7595f42aED --amount 100
```

### 具体流程

该命令将：
1. ✅ 验证接收地址格式
2. ✅ 验证转账金额（必须为正数）
3. ✅ 检查您是否有足够的 ETH 作为交易手续费
4. ✅ 检查您是否有足够的 USDC 进行转账
5. ✅ 在 Arbitrum 上执行转账
6. ✅ 等待交易确认
7. ✅ 显示交易哈希值

### 示例输出

```
Preparing USDC transfer...
From: 0x9Eb60033E4FdE90839e586DdAE9d9Edef7a5A873
To:   0x742d35Cc6634C0532925a3b844Bc9e7595f42aED
Amount: 100 USDC

Sending 100 USDC...
Transaction sent! Hash: 0x123abc...
Waiting for confirmation...
✅ Transfer successful!
100 USDC sent to 0x742d35Cc6634C0532925a3b844Bc9e7595f42aED
```

### 所需条件

要发送 USDC，您需要：
- ✅ 已经创建的钱包（使用 `clawearn wallet create` 创建）
- Arbitrum 上有 USDC 余额
- Arbitrum 上有足够的 ETH 作为交易手续费
- 有效的以太坊接收地址

### 常见问题

**“USDC 余额不足”**
- 您的 USDC 不够
- 解决方案：向钱包中充值更多 USDC

**“Arbitrum 上的 ETH 不足”**
- 您需要 ETH 来支付交易手续费
- 解决方案：向钱包地址发送一些 ETH

**“接收地址无效”**
- 接收地址格式错误
- 必须是有效的以太坊地址（以 `0x` 开头，后跟 40 个十六进制字符）

**“金额无效”**
- 金额必须为正数
- 不能为零或负数

---

## Manifold 钱包设置

🚧 **即将推出**

Manifold 使用基于账户的认证系统，并支持虚拟货币（Mana）。

**计划中的设置流程：**
```bash
# Register account
curl -X POST https://manifold.markets/api/v0/me/register \
  -H "Content-Type: application/json" \
  -d '{"username": "YourAgentName", "email": "agent@example.com"}'

# Get API key
# Save to ~/.config/clawearn/manifold-key.txt
```

---

## Kalshi 钱包设置

🚧 **即将推出**

Kalshi 使用传统的基于账户的系统，并支持 USD。

**计划中的设置流程：**
1. 在 Kalshi.com 上创建账户
2. 完成 KYC 验证
3. 链接银行账户
4. 获取 API 凭证
5. 将凭证保存到 `~/.config/clawearn/kalshi-credentials.json`

---

## 多钱包管理

### 推荐的结构

```
~/.config/clawearn/
├── polymarket-key.txt          # Polymarket private key
├── manifold-key.txt            # Manifold API key
├── kalshi-credentials.json     # Kalshi API credentials
└── master-config.json          # All wallet addresses and settings
```

### 主配置文件示例

**`~/.config/clawearn/master-config.json`**
```json
{
  "wallets": {
    "polymarket": {
      "address": "0x1234...",
      "key_path": "~/.config/clawearn/polymarket-key.txt",
      "signature_type": 0,
      "network": "polygon",
      "enabled": true
    },
    "manifold": {
      "username": "YourAgent",
      "key_path": "~/.config/clawearn/manifold-key.txt",
      "enabled": false
    },
    "kalshi": {
      "user_id": "your-user-id",
      "key_path": "~/.config/clawearn/kalshi-credentials.json",
      "enabled": false
    }
  },
  "default_market": "polymarket"
}
```

---

## 安全检查清单

### ✅ 必须遵守的安全措施

- [ ] 私钥保存在 `~/.config/clawearn/` 目录中，并设置 600 权限
- [ ] 该目录只有您自己可以访问
- [ ] 私钥不会被提交到 Git （添加到 `.gitignore` 文件中）
- [ ] 私钥不会被记录或打印到控制台
- [ ] 私钥不会被发送到外部服务
- [ ] 为测试和生产环境使用不同的钱包
- [ ] 定期备份钱包地址（但不要备份私钥！）
- [ ] 使用环境变量代替硬编码的私钥

### 🔒 更高级的安全措施

- [ ] 集成硬件钱包（用于大额交易）
- [ ] 为生产环境使用多签名钱包
- [ ] 分别使用热钱包和冷钱包
- [ ] 定期审计凭证存储安全
- [ ] 对私钥进行加密备份
- [ ] 在所有市场账户上启用 2FA（双重身份验证）

---

## 钱包操作

### 查看所有市场的余额

```bash
# Polymarket
bun polymarket-cli.ts balance check --private-key $POLYMARKET_PRIVATE_KEY

# Manifold (coming soon)
# curl https://manifold.markets/api/v0/me -H "Authorization: Bearer $MANIFOLD_KEY"

# Kalshi (coming soon)
# curl https://api.kalshi.com/v1/balance -H "Authorization: Bearer $KALSHI_KEY"
```

### 导出钱包地址

```bash
# Create a reference file (safe to share, no private keys)
cat > ~/.clawearn/wallet-addresses.txt << EOF
Polymarket: $(bun polymarket-cli.ts account info --private-key $POLYMARKET_PRIVATE_KEY | grep address)
Manifold: YourUsername
Kalshi: your-user-id
EOF
```

---

## 备份与恢复

### 需要备份的内容

**必须备份：**
- 私钥（已加密！）
- 钱包地址
- 账户用户名/电子邮件
- 恢复短语（如适用）

**不需要备份的内容：**
- API 响应
- 临时会话令牌
- 缓存数据

### 备份脚本

```bash
#!/bin/bash
# backup-wallets.sh

BACKUP_DIR=~/clawearn-backup-$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

# Backup config (contains addresses, not keys)
cp ~/.clawearn/config.json $BACKUP_DIR/

# Backup wallet addresses
cp ~/.clawearn/wallet-addresses.txt $BACKUP_DIR/

# Create encrypted backup of keys
tar -czf - ~/.config/clawearn/*.txt | \
  gpg --symmetric --cipher-algo AES256 > $BACKUP_DIR/keys-encrypted.tar.gz.gpg

echo "Backup created at $BACKUP_DIR"
echo "Store the encrypted keys file in a secure location!"
```

### 恢复脚本

```bash
#!/bin/bash
# recover-wallets.sh

BACKUP_DIR=$1

# Restore config
cp $BACKUP_DIR/config.json ~/.clawearn/

# Decrypt and restore keys
gpg --decrypt $BACKUP_DIR/keys-encrypted.tar.gz.gpg | \
  tar -xzf - -C ~/

echo "Wallets restored. Verify with balance checks."
```

---

## 故障排除

### “余额不足”错误
```bash
# Check actual balance
bun polymarket-cli.ts balance check --private-key $POLYMARKET_PRIVATE_KEY

# Request testnet funds
bun polymarket-cli.ts balance pocket-money --amount 100
```

### “私钥无效”错误
```bash
# Verify key format (should start with 0x)
cat ~/.config/clawearn/polymarket-key.txt

# Re-export if needed
bun polymarket-cli.ts account export-key --email YOUR_EMAIL --password YOUR_PASSWORD
```

### 访问私钥时出现“权限被拒绝”错误
```bash
# Fix permissions
chmod 700 ~/.config/clawearn
chmod 600 ~/.config/clawearn/*.txt
```

### 丢失私钥
⚠️ **如果丢失了私钥，您将无法访问您的资金！**

- 立即检查备份文件
- 检查环境变量：`echo $POLYMARKET_PRIVATE_KEY`
- 查看是否在其他地方保存了私钥
- 如果确实丢失了私钥，请创建新的钱包，并从旧钱包中转移资金（如果可以通过其他方式访问旧钱包的话）

---

## 最佳实践

1. **每个市场使用一个钱包** - 不要在不同平台之间重复使用相同的私钥
2. **从小额资金开始测试** - 总是用最少的资金进行测试
3. **定期检查余额** - 监控意外变化
4. **保护环境变量** - 使用被 Git 忽略的 `.env` 文件来存储私钥
5. **记录您的设置** - 记录每个钱包的用途
6. **定期备份** - 每周对私钥进行加密备份
7. **区分测试环境和生产环境** - 为测试和实际交易使用不同的钱包

---

## 快速参考

```bash
# Setup new Polymarket wallet
bun polymarket-cli.ts account create --email agent@example.com --password PASS
bun polymarket-cli.ts account export-key --email agent@example.com --password PASS

# Save key securely
mkdir -p ~/.config/clawearn && chmod 700 ~/.config/clawearn
echo "0xKEY" > ~/.config/clawearn/polymarket-key.txt && chmod 600 ~/.config/clawearn/polymarket-key.txt

# Set environment variable
export POLYMARKET_PRIVATE_KEY=$(cat ~/.config/clawearn/polymarket-key.txt)

# Check balance
bun polymarket-cli.ts balance check --private-key $POLYMARKET_PRIVATE_KEY

# Get testnet funds
bun polymarket-cli.ts balance pocket-money --amount 100
```

---

## 资金管理策略

### 交易的现实

**预测市场涉及真实资金。** 您可能会赢得或损失真实的 USDC。以下是一些明智的资金管理建议：

### 第一阶段：测试期（第 1-4 周）

**预算：** 从总资本的 5-10% 开始
```
If you have: $1000
Test with:   $50-100
Goal:        Learn and validate your strategy
```

**规则：**
- ✅ 每次交易使用较小的头寸（5-10 美元）
- ✅ 慢慢且谨慎地进行交易
- ✅ 记录每一笔交易
- ✅ 不要急于追求大额利润
- ❌ 尚不要增加交易头寸

### 第二阶段：验证期（第 5-8 周）

**在盈利测试持续 2 周后：**
```
If test profits:     +20% → move to Phase 2
If test losses:     -10% → re-think strategy, don't proceed
```

**预算：** 将资金比例提高到总资本的 20-30%
```
If you have: $1000 (proven +$10 profit testing)
Trade with:  $200-300
Position:    $20-30 per trade
```

### 第三阶段：扩展期（第 9 周及以上）

**仅当第二阶段连续盈利超过 4 周后：**
```
If validated profits: Can use up to 50% of capital
Never use:           More than 50% at once
Always keep:         50% in emergency reserves
```

### 资本增长时间表

```
Week 1:     $1000 → Test with $50
Week 4:     +$10 profit (20% on test) → Allocate $200
Week 8:     +$40 profit (20% on validation) → Allocate $500
Month 3:    +$100 profit → Can grow to $1500+ portfolio
Month 6:    Consistent profits → Scale further

PATIENCE = PROFIT
```

### 为什么更多资金有帮助（但需谨慎）

**更多资金的优势：**
- 📈 更好的分散投资（5 个头寸 vs 1 个头寸）
- 📈 更能应对损失（一次损失不会导致重大损失）
- 📈 在相同的胜率下获得更高的利润
- 📈 有机会抓住更大的交易机会

**更多资金带来的风险：**
- ⚠️ 更大的绝对损失（可能损失 100 美元）
- ⚠️ 更容易过度使用杠杆
- ⚠️ 需要管理更多的头寸
- ⚠️ 更容易犯大错

### 每日损失限额

**始终设置每日损失限额：**
```
Capital: $1000
Daily limit: $20 (2% of capital)

If you lose $20 in a day: STOP TRADING
Review your strategy before continuing
```

### 绝对不要这样做

❌ **致命的错误：**
- 不要害怕错过机会（FOMO）
- 不要进行报复性交易
- 不要过度使用杠杆
- 不要在情绪化状态下交易
- 不要忽视损失
- 不要将所有利润用于交易
- 不要拿租金/生活费用去冒险

### 每周回顾

**每周进行一次回顾：**
```
1. Total profit/loss this week
2. Number of winning trades
3. Average win size vs loss size
4. Did I follow my strategy?
5. What did I learn?
6. Should I adjust position sizing?
```

### 应急资金

**预留一部分资金：**
```
Total Capital: $5000

50% - Active Trading: $2500
30% - Growth Reserve: $1500
20% - Emergency Fund: $1000
```

**切勿动用应急资金进行交易。**

### 何时可以增加资金

如果您满足以下条件，可以考虑增加资金：
- [ ] 连续 4 周以上都有稳定盈利
- [ ] 胜率超过 50%
- [ ] 从未进行过情绪化的交易
- [ ] 始终遵守头寸控制规则
- [ ] 所有交易都有记录
- [ ] 每日损失不超过 2%
- [ ] 应急资金完好无损

### 何时应该减少资金

如果您出现以下情况，请停止交易并减少资金投入：
- [ ] 连续 3 天以上亏损
- [ ] 每日损失超过 5%
- [ ] 感到压力或情绪化
- [ ] 进行报复性交易
- [ ] 胜率降至 40% 以下

---

## 资金管理智慧总结

| 错误 | 后果 | 解决方法 |
|---------|------|-----|
| 用全部资金开始交易 | 一切损失 | 从 10% 的资金开始 |
- 情绪化交易 | 一次交易可能损失 30% | 遵循交易系统 |
- 忽视损失 | 亏损累积 | 设置每日止损限额 |
- 过度使用杠杆 | 被强制平仓 | 保持头寸大小在 10% 以下 |
- 不记录交易 | 重复同样的错误 | 记录每一笔交易 |

**记住：** 目标不是快速致富，而是稳步积累财富。🎯

---

**下一步：**
1. ✅ 设置您的钱包
2. ✅ 保护好私钥
3. ✅ 为账户充值资金——从小额开始
4. ✅ 按照分阶段的方法进行操作（测试 → 验证 → 扩展）
5. 📖 阅读特定市场的 SKILL.md 文件
6. 🚀 用小额资金开始测试
7. 📊 记录您的交易和利润
8. 💰 在证明策略有效后，谨慎地扩大投资规模
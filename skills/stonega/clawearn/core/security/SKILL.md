# 安全最佳实践 🔒

这些是在预测市场交易中必须遵守的关键安全指南。

---

## 核心原则

### 🔴 绝对不要做以下事情

1. **绝不要与任何人分享你的私钥**
   - 无论是日志、错误信息、对第三方的API请求、截图或录像，还是聊天消息或支持工单中。
2. **绝不要将私钥发送给外部服务**
   - 只要在本地使用私钥来签署交易。
   - 如果有服务要求你提供私钥，那很可能是骗局。
   - 合法的服务只需要你的公钥。
3. **绝不要将私钥提交到版本控制系统中**
   - 将 `*.txt`、`*-key.*`、`credentials.*` 文件添加到 `.gitignore` 文件中。
   - 使用环境变量或安全保管库来存储私钥。
   - 在推送代码之前扫描仓库。
4. **绝不要记录敏感信息**
   - 在调试输出中隐藏私钥内容。
   - 即使是为了测试，也不要打印完整的私钥。
   - 如有需要，可以使用 `console.log(key.slice(0, 6) + '...'` 来显示私钥的一部分。
5. **绝不要在不同平台上重复使用私钥**
   - 每个市场都应该使用独立的钱包。
   - 一个平台上的私钥被泄露不会影响其他平台。
   - 这样更容易追踪每个私钥的使用情况。

---

## ✅ 必须遵守的安全实践

### 环境变量

**推荐做法：**
```bash
# .env file (gitignored)
POLYMARKET_PRIVATE_KEY=0x...
MANIFOLD_API_KEY=...

# Load in your code
export $(cat .env | xargs)
```

**更优做法：**
```bash
# Use a secrets manager or encrypted vault
export POLYMARKET_PRIVATE_KEY=$(gpg --decrypt ~/.config/clawearn/key.gpg)
```

### Git 安全

**.gitignore 文件配置：**
```
# Credentials
*.txt
*-key.*
credentials.*
.env
.env.*

# Config with sensitive data
~/.config/clawearn/

# Backups
*-backup/
*.gpg
```

**提交前需要验证的内容：**
```bash
# Check what you're about to commit
git diff --cached

# Search for potential secrets
git grep -i "private.*key\|secret\|password" $(git diff --cached --name-only)
```

---

## 🛡️ 钱包安全

### 为不同用途设置独立的钱包

```
Production Trading:
├── Polymarket: 0xABCD... (large amounts)
├── Manifold: @ProductionBot
└── Kalshi: prod-account

Development/Testing:
├── Polymarket: 0xEF12... (small amounts)
├── Manifold: @TestBot
└── Kalshi: test-account
```

### 热钱包与冷钱包

**热钱包（在线）**
- 用于活跃交易
- 仅存放少量资金（仅够交易所需）
- 由交易代理自动管理
- 风险较高

**冷钱包（离线）**
- 用于存储大量资金
- 仅支持手动转账
- 风险较低

**使用策略：**
```bash
# Keep most funds in cold storage
Cold Wallet: $10,000 USDC

# Transfer to hot wallet as needed
Hot Wallet: $500 USDC (for trading)

# Refill hot wallet when low
# Withdraw profits to cold wallet regularly
```

---

## 🔐 加密

### 对私钥进行加密存储

```bash
# Encrypt a private key
echo "0xYOUR_PRIVATE_KEY" | gpg --symmetric --armor > ~/.config/clawearn/key.gpg

# Decrypt when needed
gpg --decrypt ~/.config/clawearn/key.gpg
```

### 创建加密备份

```bash
# Create encrypted backup
tar -czf - ~/.config/clawearn/ | \
  gpg --symmetric --cipher-algo AES256 > clawearn-backup-$(date +%Y%m%d).tar.gz.gpg

# Store in multiple locations:
# - External hard drive
# - Cloud storage (encrypted!)
# - USB drive in safe
```

---

## 🚨 事件响应

### 如果怀疑私钥被泄露

**立即采取的行动：**

1. **立即停止所有交易**
   ```bash
   # Cancel all open orders
   bun markets/polymarket/polymarket-cli.ts order cancel-all --private-key $OLD_KEY
   ```

2. **将资金转移到新的钱包中**
   ```bash
   # Create new wallet
   bun markets/polymarket/polymarket-cli.ts account create --email new@example.com --password NEWPASS
   
   # Transfer all funds to new address
   # (Use Polygon wallet interface or CLI transfer command)
   ```

3. **撤销 API 密钥**
   - Polymarket：创建新账户
   - Manifold：重新生成 API 密钥
   - Kalshi：重置登录凭据

4. **记录事件细节**
   - 你何时发现问题的？
   - 你采取了哪些措施？
   - 有多少资金处于风险中？
   - 事件最终结果如何？

5. **审查安全措施**
   - 私钥是如何被泄露的？
   - 你可以做出哪些改变来防止类似事件再次发生？
   - 更新你的安全流程。

### 私钥泄露的迹象

⚠️ **警告信号：**
- 账户余额出现异常变化
- 出现你未下的订单
- 有未经授权的提款
- 来自未知位置的登录尝试
- 有你不曾发起的 API 调用

**定期检查：**
```bash
# Review recent transactions
bun markets/polymarket/polymarket-cli.ts transactions list --private-key $KEY

# Check open orders
bun markets/polymarket/polymarket-cli.ts order list-open --private-key $KEY

# Monitor balance
bun markets/polymarket/polymarket-cli.ts balance check --private-key $KEY
```

---

## 🔍 审计与监控

### 定期安全审计

**每周：**
- [ ] 检查凭证文件的权限设置
- [ ] 查看最近的交易记录
- [ ] 确认账户余额与预期一致
- [ ] 监控是否有未经授权的 API 使用

**每月：**
- [ ] （如果可能）轮换 API 密钥
- [ ] 审查并更新 `.gitignore` 文件
- [ ] 测试备份恢复流程
- [ ] 检查代码中是否存在硬编码的敏感信息

**每季度：**
- [ ] 进行全面的安全审查
- [ ] 更新依赖库
- [ ] 查看访问日志
- [ ] 考虑使用新的安全工具

### 监控脚本

```bash
#!/bin/bash
# security-check.sh

echo "=== Moltearn Security Check ==="

# Check file permissions
echo "Checking file permissions..."
if [ "$(stat -c %a ~/.config/clawearn)" != "700" ]; then
  echo "⚠️  WARNING: Config directory has wrong permissions!"
fi

# Check for secrets in git
echo "Checking for secrets in git..."
if git grep -i "private.*key\|0x[a-fA-F0-9]{64}" > /dev/null 2>&1; then
  echo "⚠️  WARNING: Possible secrets found in git!"
fi

# Check balance
echo "Checking balances..."
BALANCE=$(bun markets/polymarket/polymarket-cli.ts balance check --private-key $POLYMARKET_PRIVATE_KEY)
echo "Polymarket: $BALANCE"

echo "=== Check complete ==="
```

---

## 🎯 风险管理

### 设置位置限制

设置严格的交易限额，以防止巨大损失：

```json
{
  "risk_limits": {
    "max_position_size_pct": 20,
    "max_total_exposure_pct": 50,
    "max_daily_loss_pct": 10,
    "max_single_trade_usd": 100,
    "min_balance_alert_usd": 10
  }
}
```

### 实施自动止损机制

设置自动停止交易的机制：

```bash
# Example: Stop trading if daily loss exceeds 10%
STARTING_BALANCE=1000
CURRENT_BALANCE=$(get_balance)
LOSS_PCT=$(( (STARTING_BALANCE - CURRENT_BALANCE) * 100 / STARTING_BALANCE ))

if [ $LOSS_PCT -gt 10 ]; then
  echo "🚨 CIRCUIT BREAKER: Daily loss limit exceeded!"
  # Cancel all orders
  # Notify human
  # Stop trading
fi
```

---

## 📋 安全检查清单

### 初始设置
- [ ] 为每个市场创建独立的钱包
- [ ] 将私钥存储在 `~/.config/clawearn/` 目录中，并设置 600 的权限
- [ ] 将凭证文件添加到 `.gitignore` 文件中
- [ ] 创建加密备份
- [ ] 测试备份恢复功能
- [ ] 设置环境变量
- [ ] 记录钱包地址（但不要记录私钥内容！）

### 日常操作
- [ ] 绝不要记录私钥信息
- [ ] 使用环境变量来管理私钥
- [ ] 定期检查账户余额
- [ ] 监控未经授权的交易
- [ ] 保持软件更新
- [ ] 定期进行加密备份

### 在部署之前
- [ ] 检查代码中是否存在硬编码的敏感信息
- [ ] 确保 `.gitignore` 文件配置完整
- [ ] 先用少量资金进行测试
- [ ] 设置监控和警报机制
- [ ] 记录事件响应流程
- [ ] 审查所有的 API 集成情况

---

## 🛠️ 安全工具

### 推荐使用的工具

**秘密信息扫描工具：**
```bash
# Install gitleaks
brew install gitleaks

# Scan repository
gitleaks detect --source . --verbose
```

**密码管理工具：**
- 1Password
- Bitwarden
- KeePassXC

**加密工具：**
- 使用 GPG 对文件进行加密
- 使用 Age 进行现代加密
- 使用 HashiCorp 的 Vault 工具来管理敏感信息

**监控工具：**
- 设置余额变化的警报
- 记录所有的 API 调用（但不包括敏感数据）
- 监控异常的交易行为

---

## 📚 额外资源

- [以太坊安全最佳实践](https://consensys.github.io/smart-contract-best-practices/)
- [OWASP API 安全指南](https://owasp.org/www-project-api-security/)
- [加密货币安全标准](https://cryptoconsortium.github.io/CCSS/)

---

## 紧急联系人

**如果你发现安全漏洞：**

1. **立即停止使用受影响的系统**
2. **在问题修复之前，不要公开相关信息**
3. **私下联系系统维护者**
4. **详细记录问题发生的过程**

---

**记住：** 安全措施不是一次性设置就能完成的任务，而是一个持续的过程。保持警惕！ 🔒
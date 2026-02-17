# AI钱包支付系统 - 技能指南

## 概述

该技能使AI代理能够安全地管理加密货币钱包并执行区块链交易。它提供了加密的密钥存储、多因素认证以及基于以太坊的支付安全交易处理功能。

**仓库**: https://github.com/cerbug45/AI-Wallet-Payment-System  
**作者**: cerbug46  
**版本**: 13.0  
**语言**: Python 3.8+

---

## 🎯 该技能的功能

### 主要功能
- 创建和管理以太坊加密货币钱包
- 使用军事级加密技术对私钥进行加密
- 通过Web3执行安全的ETH交易
- 实现基于TOTP的多因素认证
- 提供全面的审计日志记录
- 提供速率限制和防止滥用功能

### 使用场景
- 需要自动执行支付的AI代理
- 应用程序的安全钱包管理
- 加密安全性的教育演示
- 测试区块链集成
- 构建支持支付的AI系统

---

## 📦 安装与设置

### 第1步：系统依赖项

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y python3-dev libsqlcipher-dev build-essential libssl-dev
```

**macOS:**
```bash
brew install sqlcipher openssl python@3.11
```

**Windows:**
```powershell
# Install Visual Studio Build Tools 2019+
# Download from: https://visualstudio.microsoft.com/downloads/
# Select "Desktop development with C++" workload
```

### 第2步：克隆仓库

```bash
git clone https://github.com/cerbug45/AI-Wallet-Payment-System.git
cd AI-Wallet-Payment-System
```

### 第3步：配置Python环境

```bash
# Create isolated virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate  # Linux/macOS
# OR
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip
```

### 第4步：安装Python依赖项

```bash
# Core dependencies
pip install web3==6.0.0
pip install pysqlcipher3==1.2.0
pip install cryptography==41.0.0
pip install argon2-cffi==23.1.0
pip install pyotp==2.9.0
pip install qrcode==7.4.0
pip install pillow==10.0.0

# Optional: Install all at once
pip install -r requirements.txt
```

**依赖项说明：**
- `web3` - 用于与以太坊区块链交互
- `pysqlcipher3` - 用于加密的SQLite数据库
- `cryptography` - 用于AES/ChaCha20加密
- `argon2-cffi` - 用于密码哈希
- `pyotp` - 用于实现TOTP多因素认证
- `qrcode` - 用于生成用于多因素认证的QR码
- `pillow` - 用于处理QR码的图像

### 第5步：配置环境

在项目根目录下创建`.env`文件：

```bash
# Required Configuration
WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID
BACKUP_ENCRYPTION_KEY_FINGERPRINT=<generated-key>

# Optional Configuration
DATABASE_PATH=./secure_wallets.db
LOG_LEVEL=INFO
RATE_LIMIT_ENABLED=true
MAX_REQUESTS_PER_MINUTE=2
MAX_REQUESTS_PER_HOUR=20
SESSION_TIMEOUT_MINUTES=15
```

**生成备份加密密钥：**
```bash
openssl rand -hex 32
# Copy output to BACKUP_ENCRYPTION_KEY_FINGERPRINT
```

**获取Infura项目ID：**
1. 在https://infura.io/注册
2. 创建新项目
3. 从仪表板复制项目ID
4. 将其用于WEB3_PROVIDER_URL中

### 第6步：验证安装

```bash
python -c "from ultra_secure_wallet_v13_MAXIMUM_SECURITY import MaximumSecurityPaymentAPI; print('✅ Installation successful')"
```

---

## 🚀 快速入门指南

### 基本使用示例

```python
from ultra_secure_wallet_v13_MAXIMUM_SECURITY import MaximumSecurityPaymentAPI
import getpass
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Get master password securely (NEVER hardcode!)
master_password = getpass.getpass("Enter master password: ")

# Initialize API
api = MaximumSecurityPaymentAPI(master_password)

# Create new wallet
wallet = api.create_wallet(
    wallet_id="my_ai_wallet",
    metadata={
        "agent_name": "PaymentBot",
        "purpose": "automated_payments"
    }
)

if wallet['success']:
    print(f"✅ Wallet created!")
    print(f"   Address: {wallet['address']}")
    print(f"   📱 Setup 2FA with: {wallet['totp_uri']}")
    print(f"   🔑 Backup codes: {wallet['backup_codes']}")
    
    # CRITICAL: Save MFA secret and backup codes securely!
    # Store in password manager or encrypted vault

# Check balance
balance = api.get_balance("my_ai_wallet")
print(f"💰 Balance: {balance['balance_eth']} ETH")

# Send transaction (requires TOTP from authenticator app)
totp_code = input("Enter 6-digit TOTP code: ")
tx = api.send_transaction(
    wallet_id="my_ai_wallet",
    to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    amount_eth=0.001,  # Send 0.001 ETH
    totp_code=totp_code
)

if tx['success']:
    print(f"✅ Transaction sent!")
    print(f"   TX Hash: {tx['tx_hash']}")

# Always cleanup sensitive data
api.cleanup()
```

### 命令行演示

```bash
# Run built-in demo
python ultra_secure_wallet_v13_MAXIMUM_SECURITY.py

# Follow prompts:
# 1. Enter strong master password (20+ chars)
# 2. System creates demo wallet
# 3. Displays active security features
# 4. Shows wallet address and 2FA setup
```

---

## 🔒 安全配置

### 密码要求

系统实施严格的密码策略：

```python
# Minimum requirements
- Length: 20+ characters
- Uppercase letters: 1+
- Lowercase letters: 1+
- Digits: 1+
- Special characters: 1+
- Entropy: 80+ bits
```

**推荐的密码生成方法：**
```bash
# Generate strong password
openssl rand -base64 32

# Or use password manager:
# - 1Password
# - Bitwarden
# - LastPass
# - KeePassXC
```

### 多因素认证设置

创建钱包后，您将收到：
1. **TOTP密钥** - 存储在密码管理器中
2. **QR码URI** - 用认证应用程序扫描
3. **备份代码** - 安全地离线保存

**兼容的认证应用程序：**
- Google Authenticator
- Authy
- Microsoft Authenticator
- 1Password（内置TOTP功能）

### 速率限制配置

在代码或环境中进行配置：

```python
# Default limits
MAX_REQUESTS_PER_MINUTE = 2   # Per wallet/IP
MAX_REQUESTS_PER_HOUR = 20    # Per wallet/IP
LOCKOUT_DURATION = 3600       # 1 hour in seconds
```

### 审计日志记录

所有操作都会被记录到`secure_wallet.log`文件中：

```bash
# View logs
tail -f secure_wallet.log

# Filter for specific wallet
grep "my_ai_wallet" secure_wallet.log

# Check for security events
grep -E "SECURITY|ERROR|FAILED" secure_wallet.log
```

---

## 🎓 高级用法

### 与AI代理结合使用

```python
class PaymentAgent:
    def __init__(self, master_password):
        self.wallet_api = MaximumSecurityPaymentAPI(master_password)
        self.wallet_id = "agent_wallet"
        
    async def process_payment(self, recipient, amount, totp):
        """Process automated payment"""
        
        # Check balance first
        balance = self.wallet_api.get_balance(self.wallet_id)
        
        if balance['balance_eth'] < amount:
            return {"error": "Insufficient funds"}
        
        # Execute transaction
        result = self.wallet_api.send_transaction(
            wallet_id=self.wallet_id,
            to_address=recipient,
            amount_eth=amount,
            totp_code=totp
        )
        
        return result
    
    def cleanup(self):
        self.wallet_api.cleanup()
```

### 环境特定配置

**开发/测试网：**
```bash
# Use Sepolia testnet
WEB3_PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID

# Or Goerli
WEB3_PROVIDER_URL=https://goerli.infura.io/v3/YOUR_PROJECT_ID
```

**生产/主网：**
```bash
# Ethereum mainnet
WEB3_PROVIDER_URL=https://mainnet.infura.io/v3/YOUR_PROJECT_ID

# Enable all security features
RATE_LIMIT_ENABLED=true
REQUIRE_2FA=true
AUDIT_LOGGING=true
```

### 备份与恢复

**导出钱包备份：**
```python
# Encrypted backup creation
api.export_wallet_backup("my_wallet", backup_password="strong-backup-pwd")
# Creates: wallet_backup_20240215_123456.enc
```

**从备份中恢复：**
```python
# Import encrypted backup
api.import_wallet_backup(
    "wallet_backup_20240215_123456.enc",
    backup_password="strong-backup-pwd"
)
```

---

## 🧪 测试指南

### 先在测试网上进行测试

**切勿在主网上使用真实的ETH进行测试！**

```bash
# 1. Get testnet ETH
# Visit: https://sepoliafaucet.com/
# Enter your wallet address
# Receive free test ETH

# 2. Configure testnet
export WEB3_PROVIDER_URL=https://sepolia.infura.io/v3/YOUR_PROJECT_ID

# 3. Run tests
python ultra_secure_wallet_v13_MAXIMUM_SECURITY.py
```

### 单元测试

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Run tests (if available)
pytest tests/

# With coverage
pytest --cov=ultra_secure_wallet_v13_MAXIMUM_SECURITY tests/
```

---

## ⚠️ 重要警告

### 该系统的实际功能

✅ **已实现的安全特性：**
- 加密数据库（SQLCipher AES-256）
- 强密码哈希（Argon2id）
- 私钥加密（ChaCha20-Poly1305）
- TOTP多因素认证
- 速率限制和锁定机制
- 审计日志记录
- 输入验证
- 内存清除功能

❌ **未实现的功能（尽管在文档中有所声明）：**
- 硬件安全模块（HSM）集成
- 可信平台模块（TPM）支持
- 后量子密码学
- 多签名钱包
- 量子随机数生成
- 文档中列出的500多个功能中的大部分

### 生产环境检查清单

在投入生产使用之前，请确保完成以下事项：
- [ ] 完成专业安全审计
- [ ] 进行渗透测试
- [ ] 由安全专家审查代码
- [ ] 获得保险/责任保障
- [ ] 制定灾难恢复计划
- [ ] 建立事件响应机制
- [ ] 定期更新安全措施
- [ ] 确保符合合规要求（如KYC/AML）
- [ ] 对大额交易实施多签名钱包
- [ ] 为长期持有的资产设置冷存储

### 风险提示

**该系统仍处于实验阶段，仅用于教学目的。**

- ⚠️ 无任何保修声明
- ⚠️ 使用风险自负
- ⚠️ 作者不对资金损失负责
- ⚠️ 未经过专业安全审计
- ⚠️ 可能存在安全漏洞
- ⚠️ 仅适用于小额交易

---

## 🐛 故障排除

### 常见问题

**问题：“ModuleNotFoundError: No module named 'pysqlcipher3'”**
```bash
# Solution: Install system dependencies first
sudo apt-get install libsqlcipher-dev
pip install pysqlcipher3
```

**问题：“Web3 provider not connected”**
```bash
# Solution: Check Infura URL and API key
echo $WEB3_PROVIDER_URL
# Should output: https://mainnet.infura.io/v3/YOUR_PROJECT_ID
```

**问题：“Argon2运行缓慢/系统卡顿”**
```bash
# Solution: Reduce Argon2 parameters in code
# Edit MaxSecurityConfig:
ARGON2_MEMORY_MB = 128  # Reduce from 512
ARGON2_ITERATIONS = 4   # Reduce from 16
```

**问题：“超过速率限制”**
```bash
# Solution: Wait for cooldown or increase limits
# Limits reset after 1 hour
# Or edit rate limit config
```

---

## 📚 额外资源

### 文档
- [Web3.py文档](https://web3py.readthedocs.io/)
- [以太坊开发文档](https://ethereum.org/en/developers/docs/)
- [Argon2规范](https://github.com/P-H-C/phc-winner-argon2)
- [TOTP RFC 6238](https://tools.ietf.org/html/rfc6238)

### 安全最佳实践
- [OWASP密码存储最佳实践指南](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST密码指南](https://pages.nist.gov/800-63-3/)
- [CWE软件弱点Top 25](https://cwe.mitre.org/top25/)

### 以太坊工具
- [Etherscan](https://etherscan.io/) - 区块链浏览器
- [Remix IDE](https://remix.ethereum.org/) - 智能合约开发工具
- [MetaMask](https://metamask.io/) - 浏览器钱包

---

## 🤝 贡献

欢迎贡献！需要改进的领域包括：
1. **测试**：添加全面的测试套件
2. **文档**：优化代码文档
3. **安全**：正确实现声明的功能
4. **性能**：优化Argon2参数
5. **新功能**：集成硬件安全模块（HSM）、支持多签名
6. **用户界面**：改进Web界面或命令行界面

---

## 📞 支持

- **GitHub问题反馈**：https://github.com/cerbug45/AI-Wallet-Payment-System/issues
- **用户名**: cerbug46
- **仓库**: cerbug45/AI-Wallet-Payment-System

---

## 📄 许可证

MIT许可证 - 详情请参阅LICENSE文件

---

**最后更新时间**：2024年2月  
**技能版本**: 1.0  
**代码版本**: 13.0
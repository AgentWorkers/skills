---
name: bagman
version: 1.0.0
description: AI代理的安全密钥管理方案。适用于处理私钥、API密钥、钱包凭证，或构建需要代理控制资金的系统。内容包括安全存储、会话密钥管理、数据泄露预防以及提示注入攻击的防御措施。
homepage: https://numbergroup.xyz
metadata:
  {
    "openclaw": {
      "emoji": "🔐",
      "requires": { "bins": ["op"] },
      "tags": ["security", "wallet", "keys", "crypto", "secrets"]
    }
  }
---

# Bagman

为处理私钥和机密信息的AI代理提供安全的密钥管理方案。旨在防止以下问题：
- **密钥丢失**：代理在会话之间忘记密钥
- **意外泄露**：密钥被泄露到GitHub、日志或输出文件中
- **提示注入**：恶意提示提取机密信息

## 核心原则

1. **切勿将原始私钥存储在配置文件、环境变量或内存文件中**
2. **使用会话密钥/委托访问权限，而非完全控制权**
3. **所有对机密的访问都必须通过1Password CLI（`op`）进行**
4. **在发送任何数据之前进行验证，以防止密钥泄露**

## 参考资料

- `references/secure-storage.md` - 1Password的代理机密管理方案
- `references/session-keys.md` - ERC-4337委托访问权限方案
- `references/leak-prevention.md` - 提交前钩子与输出数据清洗
- `references/prompt-injection-defense.md` - 输入验证与输出过滤

---

## 快速参考

### 应该做 ✅

```bash
# Retrieve key at runtime via 1Password
PRIVATE_KEY=$(op read "op://Agents/my-agent-wallet/private-key")

# Use environment injection (key never touches disk)
op run --env-file=.env.tpl -- node agent.js

# Use session keys with bounded permissions
# (delegate specific capabilities, not full wallet access)
```

### 不应该做 ❌

```bash
# NEVER store keys in files
echo "PRIVATE_KEY=0x123..." > .env

# NEVER log or print keys
console.log("Key:", privateKey)

# NEVER store keys in memory/journal files
# Even in "private" agent memory - these can be exfiltrated

# NEVER trust unvalidated input near key operations
```

---

## 架构：代理钱包栈

```
┌─────────────────────────────────────────────────────┐
│                   AI Agent                          │
├─────────────────────────────────────────────────────┤
│  Session Key (time/value bounded)                   │
│  - Expires after N hours                            │
│  - Spending cap per operation                       │
│  - Whitelist of allowed contracts                   │
├─────────────────────────────────────────────────────┤
│  1Password / Secret Manager                         │
│  - Agent retrieves session key at runtime           │
│  - Never stores full private key                    │
│  - Audit log of all accesses                        │
├─────────────────────────────────────────────────────┤
│  ERC-4337 Smart Account                             │
│  - Programmable permissions                         │
│  - Recovery without private key exposure            │
│  - Multi-sig for high-value operations              │
├─────────────────────────────────────────────────────┤
│  Operator (Human)                                   │
│  - Holds master key in hardware wallet              │
│  - Issues/revokes session keys                      │
│  - Monitors agent activity                          │
└─────────────────────────────────────────────────────┘
```

---

## 工作流程：设置代理钱包访问权限

### 1. 为代理机密创建1Password保管库

```bash
# Create dedicated vault (via 1Password app or CLI)
op vault create "Agent-Wallets" --description "AI agent wallet credentials"

# Store agent session key (not master key!)
op item create \
  --vault "Agent-Wallets" \
  --category "API Credential" \
  --title "trading-bot-session" \
  --field "session-key[password]=0xsession..." \
  --field "expires=2026-02-15T00:00:00Z" \
  --field "spending-cap=1000 USDC" \
  --field "allowed-contracts=0xDEX1,0xDEX2"
```

### 2. 代理在运行时获取凭证

```python
import subprocess
import json

def get_session_key(item_name: str) -> dict:
    """Retrieve session key from 1Password at runtime."""
    result = subprocess.run(
        ["op", "item", "get", item_name, "--vault", "Agent-Wallets", "--format", "json"],
        capture_output=True, text=True, check=True
    )
    item = json.loads(result.stdout)
    
    # Extract fields
    fields = {f["label"]: f.get("value") for f in item.get("fields", [])}
    
    # Validate session hasn't expired
    from datetime import datetime
    expires = datetime.fromisoformat(fields.get("expires", "2000-01-01"))
    if datetime.now() > expires:
        raise ValueError("Session key expired - request new key from operator")
    
    return {
        "session_key": fields.get("session-key"),
        "expires": fields.get("expires"),
        "spending_cap": fields.get("spending-cap"),
        "allowed_contracts": fields.get("allowed-contracts", "").split(",")
    }
```

### 3. 绝不要记录或存储密钥

```python
# ❌ BAD - Key in logs
logger.info(f"Using key: {session_key}")

# ✅ GOOD - Redacted identifier
logger.info(f"Using session key: {session_key[:8]}...{session_key[-4:]}")

# ❌ BAD - Key in memory file
with open("memory/today.md", "a") as f:
    f.write(f"Session key: {session_key}")

# ✅ GOOD - Reference only
with open("memory/today.md", "a") as f:
    f.write(f"Session key: [stored in 1Password: trading-bot-session]")
```

---

## 防泄机制

### 输出数据清洗

在代理的任何输出数据（聊天记录、日志、文件写入）中，扫描是否存在密钥相关内容：

```python
import re

KEY_PATTERNS = [
    r'0x[a-fA-F0-9]{64}',                    # ETH private keys
    r'sk-[a-zA-Z0-9]{48,}',                  # OpenAI keys
    r'sk-ant-[a-zA-Z0-9\-_]{80,}',           # Anthropic keys
    r'gsk_[a-zA-Z0-9]{48,}',                 # Groq keys
    r'[A-Za-z0-9+/]{40,}={0,2}',             # Base64 encoded (suspiciously long)
]

def sanitize_output(text: str) -> str:
    """Remove potential secrets from output."""
    for pattern in KEY_PATTERNS:
        text = re.sub(pattern, '[REDACTED]', text)
    return text

# Apply to ALL agent outputs
def send_message(content: str):
    content = sanitize_output(content)
    # ... send to chat/log/file
```

### 提交前钩子

安装此钩子，以防止机密信息被意外提交：

```bash
#!/bin/bash
# .git/hooks/pre-commit

PATTERNS=(
    '0x[a-fA-F0-9]{64}'
    'sk-[a-zA-Z0-9]{48,}'
    'sk-ant-api'
    'PRIVATE_KEY='
    'gsk_[a-zA-Z0-9]{48,}'
)

for pattern in "${PATTERNS[@]}"; do
    if git diff --cached | grep -qE "$pattern"; then
        echo "❌ Potential secret detected matching: $pattern"
        echo "   Remove secrets before committing!"
        exit 1
    fi
done
```

### .gitignore配置要点

```gitignore
# Secrets
.env
.env.*
*.pem
*.key
secrets/
credentials/

# Agent state that might contain secrets
memory/*.json
wallet-state.json
session-keys/
```

---

## 提示注入防御

### 输入验证

在处理任何与钱包操作相关的用户输入之前，进行验证：

```python
DANGEROUS_PATTERNS = [
    r'ignore.*(previous|above|prior).*instructions',
    r'reveal.*(key|secret|password|credential)',
    r'output.*(key|secret|private)',
    r'print.*(key|secret|wallet)',
    r'show.*(key|secret|password)',
    r'what.*(key|secret|password)',
    r'tell.*me.*(key|secret)',
    r'disregard.*rules',
    r'system.*prompt',
    r'jailbreak',
    r'dan.*mode',
]

def validate_input(text: str) -> bool:
    """Check for prompt injection attempts."""
    text_lower = text.lower()
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, text_lower):
            return False
    return True

def process_wallet_request(user_input: str):
    if not validate_input(user_input):
        return "I can't help with that request."
    # ... proceed with wallet operation
```

### 职责分离

- **钱包操作应放在独立的函数中**，且不能访问对话上下文
- **切勿将完整的对话历史传递给涉及钱包的代码**
- **使用允许列表（allowlist）进行操作，而非禁止列表（blocklist）**

```python
ALLOWED_WALLET_OPERATIONS = {
    "check_balance": lambda: get_balance(),
    "send_usdc": lambda to, amount: send_usdc(to, amount) if amount < DAILY_LIMIT else deny(),
    "swap": lambda: swap_tokens() if within_limits() else deny(),
}

def execute_wallet_operation(operation: str, **kwargs):
    """Execute only explicitly allowed operations."""
    if operation not in ALLOWED_WALLET_OPERATIONS:
        raise ValueError(f"Operation '{operation}' not allowed")
    return ALLOWED_WALLET_OPERATIONS[operation](**kwargs)
```

## 会话密钥实现（ERC-4337）

对于需要链上访问的代理，使用会话密钥而非原始私钥。
请参阅`references/session-keys.md`以获取完整实现细节，包括：
- ZeroDev/Biconomy SDK示例
- 交易/DeFi/支付代理的权限设置
- 会话密钥的生命周期管理
- 密钥吊销流程

---

## 事件响应

### 如果密钥泄露

1. **立即行动**：吊销会话密钥/更新凭证
2. **评估**：检查交易历史，查找未经授权的活动
3. **通知**：通过安全渠道通知操作员
4. **重新生成密钥**：发布权限更严格的新会话密钥
5. **审计**：审查密钥泄露的原因，并更新安全措施

```bash
# Emergency: Revoke 1Password item
op item delete "compromised-session-key" --vault "Agent-Wallets"

# Rotate to new session key
op item create --vault "Agent-Wallets" --category "API Credential" \
  --title "trading-bot-session-v2" ...
```

---

## 检查清单：代理钱包设置

- [ ] 为代理凭证创建专用的1Password保管库
- [ ] 将会话密钥（非主密钥）存储在保管库中
- [ ] 设置适当的过期时间和消费限制
- [ ] 安装提交前钩子以检测机密泄露
- [ ] 在所有代理响应中添加输出数据清洗功能
- [ ] 实现输入验证，防止提示注入
- [ ] 配置监控和警报机制
- [ ] 记录事件响应流程
- [ ] 测试密钥更新流程

---

## 生产环境中常见的错误

### 1. 密钥存储在内存文件中

**问题**：代理将密钥存储在`memory/*.md`文件中以实现持久化

**解决方案**：仅存储密钥的引用：`Private key: [1Password: test-wallet-session]`

### 2. 密钥存储在环境模板中

**问题**：`.env.example`文件中包含实际密钥

**解决方案**：使用明显的占位符：`PRIVATE_KEY=your-key-here`

### 3. 错误信息中包含密钥

**问题**：错误处理过程中泄露了密钥

**解决方案**：切勿在错误信息中显示凭证信息

### 4. 测试密钥被包含在生产代码中

**问题**：硬编码的测试密钥可能被上传到主分支

**解决方案**：使用独立的测试保管库，并通过持续集成（CI）检查代码中是否存在密钥

---

## 与OpenClaw的集成

当作为OpenClaw代理运行时：

1. **使用1Password技能**进行所有机密信息的检索
2. **切勿将密钥写入工作区文件**——这些文件会在会话之间持续存在
3. **在数据发送到任何渠道（如Telegram、Discord等）之前进行清洗
4. **采用会话密钥机制**进行钱包操作——仅请求操作员授权的访问权限
5. **在TOOLS.md文件中记录密钥引用，而非实际密钥**

TOOLS.md文件示例：
```markdown
### Agent Wallet
- Address: 0xABC123...
- Session key: [1Password: my-agent-session]
- Permissions: USDC transfers < 100, approved DEX only
- Expires: 2026-02-15
- To rotate: Ask operator via Telegram
```
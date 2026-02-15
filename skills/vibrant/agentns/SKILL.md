---
name: agentns
description: 为AI代理注册和管理ICANN域名；支持钱包认证（SIWE/SIWS）；支持在Base或Solana网络上使用USDC进行支付；提供全面的DNS管理功能。
homepage: https://agentns.xyz
user-invocable: true
---

# AgentNS - 用于AI代理的域名注册服务

当您需要为代理或项目注册域名、检查域名可用性或管理DNS记录时，请使用此功能。

## 安装

```bash
pip install agentns-client

# For Solana wallet support:
pip install agentns-client[solana]
```

## 完整工作流程

```python
from agentns_client import AgentNSClient, load_or_create_wallet

# 1. Create client with wallet (auto-creates wallet.json if needed)
account = load_or_create_wallet()
client = AgentNSClient(account=account)

# 2. Check domain availability (no auth required)
result = client.check_domain("myagent.xyz")
if not result.available:
    print(f"{result.domain} is not available")
    # Search across 20 TLDs to find alternatives
    results = client.search_domains("myagent")
    available = [r for r in results if r.available]
    for r in available:
        print(f"{r.domain}: ${r.price_usdc} USDC")

# 3. Authenticate with wallet signature
client.login()

# 4. Create registrant profile (one-time, ICANN requirement)
client.ensure_registrant({
    "name": "Agent Smith",
    "street_address": "123 AI Street",
    "city": "San Francisco",
    "state_province": "CA",
    "postal_code": "94102",
    "country_code": "US",
    "email": "contact@agentns.xyz",
    "phone": "+14155551234",
})

# 5. Register domain (payment handled automatically)
domain = client.register_domain("myagent.xyz")
print(f"Registered: {domain.domain}")
print(f"Expires: {domain.expires_at}")

# 6. Add DNS records
client.add_dns("myagent.xyz", type="A", host="@", value="192.0.2.1")
client.add_dns("myagent.xyz", type="CNAME", host="www", value="myagent.xyz")
client.add_dns("myagent.xyz", type="TXT", host="@", value="v=spf1 -all")
```

## 钱包设置

**EVM（基础网络 - 默认）：**
```python
from agentns_client import load_or_create_wallet
account = load_or_create_wallet("wallet.json")  # Creates if missing
print(f"Address: {account.address}")
# Fund with USDC on Base network before registering
```

**Solana：**
```python
from agentns_client import load_or_create_solana_wallet
keypair = load_or_create_solana_wallet("solana_wallet.json")
print(f"Address: {keypair.pubkey()}")
# Fund with USDC on Solana before registering
```

## 客户端方法

### 域名操作

```python
# Check single domain (no auth)
result = client.check_domain("example.com")
# Returns: DomainCheck(domain, available, price_usdc)

# Search across 20 TLDs (no auth)
results = client.search_domains("mycompany")
# Searches: com, io, net, co, ai, xyz, dev, app, org, tech,
#           club, online, site, info, me, biz, us, cc, tv, gg

# Register domain (requires auth + USDC balance)
domain = client.register_domain("example.xyz", years=1)
# Returns: DomainInfo(domain, owner_address, status, registered_at, expires_at)

# List owned domains
domains = client.list_domains()
```

### DNS管理

```python
# List DNS records
records = client.list_dns("example.xyz")

# Add record
record = client.add_dns(
    domain="example.xyz",
    type="A",           # A, AAAA, CNAME, MX, TXT, SRV, CAA
    host="@",           # @ for root, or subdomain name
    value="192.0.2.1",
    ttl=3600,           # 300-86400 seconds
    distance=10         # Required for MX/SRV only
)

# Update record
client.update_dns("example.xyz", record_id="12345", value="192.0.2.2")

# Delete record
client.delete_dns("example.xyz", record_id="12345")
```

### 名称服务器

```python
# Get current nameservers
ns = client.get_nameservers("example.xyz")
# Default: ["ns1.namesilo.com", "ns2.namesilo.com"]

# Change to custom nameservers (e.g., Cloudflare)
client.set_nameservers("example.xyz", [
    "ns1.cloudflare.com",
    "ns2.cloudflare.com"
])
```

### 注册人信息

```python
# Get profile
profile = client.get_registrant()

# Create profile (required before first domain registration)
profile = client.create_registrant({
    "name": "Required Name",
    "street_address": "123 Main St",
    "city": "San Francisco",
    "state_province": "CA",
    "postal_code": "94102",
    "country_code": "US",        # ISO 3166-1 alpha-2
    "email": "contact@agentns.xyz",
    "phone": "+14155551234",
    "organization": "Optional Org",  # Optional
    "whois_privacy": True            # Optional, default True
})

# Update profile
client.update_registrant({"email": "new@example.com"})

# Get or create (recommended)
profile = client.ensure_registrant({...})
```

## 错误处理

```python
from agentns_client.exceptions import (
    AgentNSError,           # Base exception
    AuthenticationError,    # Invalid/expired JWT (401)
    PaymentRequiredError,   # Insufficient USDC balance (402)
    NotFoundError,          # Domain/record not found (404)
    ConflictError,          # Profile exists, domain taken (409)
    ValidationError,        # Invalid input (400)
    RateLimitError,         # Too many requests (429)
)

try:
    domain = client.register_domain("example.xyz")
except PaymentRequiredError as e:
    print(f"Need {e.payment_requirement.amount} USDC")
    print(f"Send to: {client.wallet_address}")
except ConflictError:
    print("Domain already registered or unavailable")
except AuthenticationError:
    client.login()  # Re-authenticate
```

## 重要说明

- **必须使用USDC**：在注册之前，请使用USDC为钱包充值（EVM或Solana网络）。
- **注册人信息**：ICANN要求提供联系信息——只需创建一次，即可用于所有域名。
- **WHOIS隐私设置**：所有域名均默认开启隐私保护。
- **支持的顶级域名（TLD）**：可以使用`check_domain()`函数查询所有TLD的可用性；使用`search_domains()`函数查询20个热门TLD。
- **定价**：域名费用 + 20%的附加费用（最低4美元），以USDC支付。

## 资源

- **PyPI**：https://pypi.org/project/agentns-client/
- **GitHub**：https://github.com/vibrant/agentns_client
- **API文档**：https://agentns.xyz/docs
- **支持**：[@AgentNSxyz](https://x.com/AgentNSxyz)
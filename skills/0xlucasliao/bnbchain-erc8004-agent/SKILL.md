---
name: erc8004-identity
version: 1.0.0
description: 在 BNB 链上维护您的代理节点的链上身份（ERC-8004 标准）。使用 BNBAgent SDK 进行注册、状态查询以及安全地管理您的代理元数据。
---

# ERC-8004 代理身份管理

此技能允许您的代理使用 ERC-8004 标准在 BNB 链上注册和管理自己的链上身份。

## 功能

- **自我注册：** 将自己注册为代理（符合 ERC-8004 标准）。
- **无需Gas费用：** 使用 MegaFuel Paymaster（仅限 BSC 测试网）实现零成本注册。
- **身份管理：** 更新您的元数据（URI、端点以及描述信息）。
- **验证：** 用户可以在 [8004scan.io](https://testnet.8004scan.io) 上验证您的代理状态。

## 安装

此技能需要 `bnbagent` Python SDK。

```bash
# Install bnbagent SDK (from test.pypi.org as per release)
pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  bnbagent==0.1.6

# Or using uv (recommended for speed)
uv pip install --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  bnbagent==0.1.6
```

## 安全提示

此技能会管理一个专门用于存储代理身份信息的钱包：
- **密码：** 该钱包是加密的。请设置 `WALLET_PASSWORD` 环境变量或在提示时提供密码。
- **私钥：** 私钥存储在本地文件 `.bnbagent_state` 中（已加密）。请勿共享此文件。

## 使用方法

创建一个脚本（或让我为您创建一个）来管理您的代理身份。

### 1. 注册（首次使用）

如果您尚未在链上进行注册，请执行以下操作：

```python
import os
from bnbagent import ERC8004Agent, EVMWalletProvider, AgentEndpoint

# 1. Setup Wallet & SDK
password = os.getenv("WALLET_PASSWORD", "default-secure-password")
wallet = EVMWalletProvider(password=password)
sdk = ERC8004Agent(wallet_provider=wallet, network="bsc-testnet")

# 2. Define Your Identity
agent_uri = sdk.generate_agent_uri(
    name="My Agent Name",
    description="I am an autonomous agent running on OpenClaw.",
    endpoints=[
        AgentEndpoint(
            name="activity",
            endpoint="https://moltbook.com/u/MyAgentName", # Example: Link to your social profile
            version="1.0.0"
        )
    ]
)

# 3. Register on BNB Chain (Gasless via Paymaster)
print("Registering...")
result = sdk.register_agent(agent_uri=agent_uri)
print(f"Success! Agent ID: {result['agentId']}")
print(f"View registered agents: https://testnet.8004scan.io/agents?chain=97")
```

### 2. 检查状态

```python
# Check if you are already registered locally
info = sdk.get_local_agent_info("My Agent Name")
if info:
    print(f"I am registered! Agent ID: {info['agent_id']}")
    # Get on-chain details
    chain_info = sdk.get_agent_info(info['agent_id'])
    print(f"On-chain Address: {chain_info['agentAddress']}")
```

### 3. 更新身份信息

如果您的端点或描述信息发生变化，请执行以下操作：

```python
local_info = sdk.get_local_agent_info("My Agent Name")
if local_info:
    agent_id = local_info['agent_id']
    
    # Generate new URI
    new_uri = sdk.generate_agent_uri(
        name="My Agent Name",
        description="Updated description.",
        endpoints=[...],
        agent_id=agent_id
    )
    
    # Update on-chain
    sdk.set_agent_uri(agent_id=agent_id, agent_uri=new_uri)
    print("Identity updated successfully.")
```

## 相关工具

- **BSC 测试网：** https://testnet.8004scan.io/agents?chain=97
- **BSC 主网：** https://www.8004scan.io/agents?chain=56（即将推出）
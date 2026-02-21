---
name: x402-compute
version: 1.0.7
description: 当用户请求“配置GPU实例”、“启动云服务器”、“查看计算计划”、“浏览GPU价格信息”、“扩展计算实例”、“销毁服务器实例”、“检查实例状态”、“列出我的实例”或管理x402 Singularity Compute/x402Compute基础设施时，应使用此技能。该技能支持通过x402支付协议，在Base或Solana网络上使用USDC进行GPU和VPS的配置。
homepage: https://studio.x402layer.cc/docs/agentic-access/x402-compute
metadata:
  clawdbot:
    emoji: "🖥️"
    homepage: https://compute.x402layer.cc
    os:
      - linux
      - darwin
    requires:
      bins:
        - python3
      env:
        # Option A — Base/EVM payments (provide these OR Option B, not both)
        - PRIVATE_KEY        # EVM private key for signing payments (0x...)
        - WALLET_ADDRESS     # EVM wallet address (0x...)
        # Option B — Solana payments (alternative to Option A)
        - SOLANA_SECRET_KEY        # Solana signer key (base58 or JSON byte array)
        - SOLANA_WALLET_ADDRESS    # Solana public address
        # Optional — preferred for routine management without exposing private keys
        - COMPUTE_API_KEY   # Reusable API key (create once via create_api_key.py)
    credentials:
      primary: COMPUTE_API_KEY   # Recommended: use API key for management over raw private keys
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---

# x402 计算服务

通过 x402 支付协议，使用 USDC 预付费用来配置和管理 GPU/VPS 实例。

**基础 URL:** `https://compute.x402layer.cc`
**网络类型:** Base (EVM) • Solana
**货币:** USDC
**支付协议:** 必须使用 HTTP 402 进行支付

**访问说明:** 推荐使用 SSH 公钥进行访问。如果没有提供 SSH 密钥，可以通过 API 获取一次性的临时密码。

---

## 快速入门

### 1. 安装依赖项
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. 设置钱包

#### 选项 A: Base (EVM) 私钥
```bash
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."
```

#### 选项 B: Solana 私钥
```bash
export SOLANA_SECRET_KEY="base58-or-json-array"
export SOLANA_WALLET_ADDRESS="YourSolanaAddress"
export COMPUTE_AUTH_CHAIN="solana"
```

创建 `COMPUTE_API_KEY`（可选），用于管理 API 端点：
```bash
python {baseDir}/scripts/create_api_key.py --label "my-agent"
```

---

## ⚠️ 安全提示

> **重要提示**: 本服务涉及用于签署区块链交易的私钥管理。
>
> - **切勿使用您的主托管钱包** - 请创建一个仅包含少量资金的专用钱包。
> - **私钥仅在本地使用** - 它们仅用于在本地签署交易，永远不会被传输。
> **用于测试时**：请使用包含少量 USDC 的临时钱包。

---

## 脚本概述

| 脚本 | 功能 |
|--------|---------|
| `browse_plans.py` | 列出可用的 GPU/VPS 计划及其价格 |
| `browse_regions.py` | 列出部署区域 |
| `provision.py` | 配置新实例（使用 x402 支付，支持 `--months` 或 `--days` 选项） |
| `create_api_key.py` | 生成用于代理访问的 API 密钥（可选） |
| `list_instances.py` | 列出当前激活的实例 |
| `instance_details.py` | 查看特定实例的详细信息 |
| `get_one_time_password.py` | 获取一次性临时密码（用于紧急情况） |
| `extend_instance.py` | 延长实例的使用期限（使用 x402 支付） |
| `destroy_instance.py` | 删除实例 |
| `solana_signing.py` | 用于 Solana x402 支付的内部辅助脚本 |

---

## 实例生命周期

实例将在预付费期限结束后失效。请在到期前延长使用期限以保持其运行状态。

---

## 工作流程

### A. 浏览和配置实例
```bash
# List GPU plans
python {baseDir}/scripts/browse_plans.py

# Filter by type (gpu/vps/high-performance)
python {baseDir}/scripts/browse_plans.py --type vcg

# Check available regions
python {baseDir}/scripts/browse_regions.py

# Generate a dedicated SSH key once (recommended for agents)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/x402_compute

# Provision an instance for 1 month (triggers x402 payment)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "my-gpu" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision a daily instance (cheaper, use-and-throw)
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 1 --label "test-daily" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision for 3 days
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --days 3 --label "short-task" --ssh-key-file ~/.ssh/x402_compute.pub

# Provision on Solana
python {baseDir}/scripts/provision.py vc2-1c-1gb ewr --months 1 --label "my-sol-vps" --network solana --ssh-key-file ~/.ssh/x402_compute.pub

# ⚠️ After provisioning, wait 2-3 minutes for Vultr to complete setup
# Then fetch your instance details (IP, status):
python {baseDir}/scripts/instance_details.py <instance_id>
```

### B. 管理实例
```bash
# Optional: create a reusable API key (avoids message signing each request)
python {baseDir}/scripts/create_api_key.py --label "my-agent"

# List all your instances
python {baseDir}/scripts/list_instances.py

# Get details for one instance
python {baseDir}/scripts/instance_details.py <instance_id>

# Optional fallback if no SSH key was provided during provisioning
python {baseDir}/scripts/get_one_time_password.py <instance_id>

# Extend by 1 day
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 24

# Extend by 1 month
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720

# Extend on Solana
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720 --network solana

# Destroy
python {baseDir}/scripts/destroy_instance.py <instance_id>
```

---

## x402 支付流程

1. 提交配置/延长实例的请求 → 服务器返回包含支付要求的 `HTTP 402` 响应。
2. 脚本在本地完成支付签名：
   - Base（EVM）模式：使用 USDC 通过 EIP-712 协议进行转账。
   - Solana 模式：使用已签名的 SPL 转账交易数据。
3. 脚本重新发送请求，并在请求头中添加 `X-Payment` 字段以包含签名后的数据。
4. 服务器验证支付信息，完成链上结算后配置或延长实例的使用权。

对于 Solana 模式，可能会出现临时性的中间节点故障。如果收到 5xx 类型的错误，请尝试重试一到两次。

---

## 计划类型

| 计划类型 | 计划前缀 | 说明 |
|------|-------------|-------------|
| GPU | `vcg-*` | 基于 GPU 的加速服务（如 A100、H100 等） |
| VPS | `vc2-*` | 标准云计算服务 |
| High-Perf | `vhp-*` | 高性能专用服务器 |
| Dedicated | `vdc-*` | 专用裸机服务器 |

---

## 环境配置参数

| 参数 | 必需条件 | 说明 |
|----------|--------------|-------------|
| `PRIVATE_KEY` | Base 模式 | EVM 私钥（格式：0x...） |
| `WALLET_ADDRESS` | Base 模式 | Base 模式的钱包地址（格式：0x...） |
| `SOLANA_SECRET_KEY` | Solana 模式 | Solana 签名密钥（格式：base58 或 JSON 字节数组） |
| `SOLANA_WALLET_ADDRESS` | Solana 模式 | Solana 钱包地址（如果可以从 `SOLANA_SECRET_KEY` 推导出来，则可选） |
| `COMPUTE_AUTHCHAIN` | Solana 或 Base 模式的认证设置 | 可选参数，用于指定认证链 |
| `COMPUTE_API_KEY` | 可选 | 用于管理 API 端点的通用 API 密钥 |

---

## API 参考

有关所有 API 端点的详细信息，请参阅 [references/api-reference.md](references/api-reference.md)。

---

## 资源链接

- 📖 **文档**: [studio.x402layer.cc/docs/agentic-access/x402-compute](https://studio.x402layer.cc/docs/agentic-access/x402-compute)
- 🖥️ **计算控制面板**: [compute.x402layer.cc](https://compute.x402layer.cc)
- 🌐 **x402 Studio**: [studio.x402layer.cc](https://studio.x402layer.cc)
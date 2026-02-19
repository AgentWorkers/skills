---
name: x402-compute
version: 1.0.2
description: 此技能适用于以下场景：用户请求“配置GPU实例”、“启动云服务器”、“查看计算计划”、“浏览GPU价格信息”、“扩展计算实例”、“销毁服务器实例”、“检查实例状态”、“列出我的实例”，或管理x402 Singularity Compute/x402Compute基础设施。该技能支持通过x402支付协议，在Base或Solana网络上使用USDC进行GPU和VPS的配置与管理。
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
        - WALLET_ADDRESS
        - PRIVATE_KEY
    credentials:
      primary: PRIVATE_KEY
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---

# x402 计算服务

通过 x402 支付协议，使用 USDC 预付费用来租用和管理 GPU/VPS 实例。

**基础 URL:** `https://compute.x402layer.cc`  
**网络类型:** Base (EVM) • Solana  
**货币:** USDC  
**支付协议:** 必须使用 HTTP 402 请求进行支付

---

## 快速入门

### 1. 安装依赖项
```bash
pip install -r {baseDir}/requirements.txt
```

### 2. 设置钱包

#### 选项 A：使用私钥  
```bash
export PRIVATE_KEY="0x..."
export WALLET_ADDRESS="0x..."
```

#### 选项 B：使用 Coinbase 的代理钱包 (AWAL)  
```bash
npx skills add coinbase/agentic-wallet-skills
export X402_USE_AWAL=1
```

---

## ⚠️ 安全提示

> **重要提示**：本功能涉及处理用于签署区块链交易的私钥。
>
> - **切勿使用您的主托管钱包** – 请创建一个仅包含少量资金的专用钱包。
> - **私钥仅在本地使用** – 它们仅用于本地签署交易，永远不会被传输。
> **用于测试时**：请使用包含少量 USDC 的临时钱包。

---

## 脚本概述

| 脚本 | 功能 |
|--------|---------|
| `browse_plans.py` | 列出可用的 GPU/VPS 计划及其价格 |
| `browse_regions.py` | 列出部署区域 |
| `provision.py` | 预订新实例（使用 x402 支付） |
| `list_instances.py` | 列出您已激活的实例 |
| `instance_details.py` | 获取特定实例的详细信息 |
| `extend_instance.py` | 延长实例的使用期限（使用 x402 支付） |
| `destroy_instance.py` | 删除实例 |

---

## 实例生命周期

实例会在预付费期限结束后自动过期。请在到期前提前续费以保持其运行状态。

---

## 工作流程

### A. 浏览和预订实例
```bash
# List GPU plans
python {baseDir}/scripts/browse_plans.py

# Filter by type (gpu/vps/high-performance)
python {baseDir}/scripts/browse_plans.py --type vcg

# Check available regions
python {baseDir}/scripts/browse_regions.py

# Provision an instance (triggers x402 payment)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "my-gpu"

# ⚠️ After provisioning, wait 2-3 minutes for Vultr to complete setup
# Then fetch your credentials (IP, root password):
python {baseDir}/scripts/instance_details.py <instance_id>
```

### B. 管理实例
```bash
# List all your instances
python {baseDir}/scripts/list_instances.py

# Get details for one instance
python {baseDir}/scripts/instance_details.py <instance_id>

# Extend by 1 month
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720

# Destroy
python {baseDir}/scripts/destroy_instance.py <instance_id>
```

---

## x402 支付流程

1. 提交预订/续费请求 → 服务器返回包含支付要求的 `HTTP 402` 响应。
2. 脚本在本地使用 `TransferWithAuthorization` (EIP-712) 协议签署 USDC 交易。
3. 脚本重新发送请求，并在请求头中添加包含签名数据的 `X-Payment` 字段。
4. 服务器验证支付信息，完成链上结算，并随后提供实例或延长其使用期限。

---

## 计划类型

| 计划类型 | 计划前缀 | 描述 |
|------|-------------|-------------|
| GPU | `vcg-*` | 基于 GPU 的计算服务（如 A100、H100 等） |
| VPS | `vc2-*` | 标准云计算服务 |
| High-Perf | `vhp-*` | 高性能专用服务器 |
| Dedicated | `vdc-*` | 专用裸机服务器 |

---

## 环境变量说明

| 变量 | 必需条件 | 说明 |
|----------|--------------|-------------|
| `PRIVATE_KEY` | 基本支付方式（使用私钥） | EVM 私钥（格式：0x...） |
| `WALLET_ADDRESS` | 所有操作 | 您的钱包地址 |
| `X402_USE_AWAL` | 是否使用 Coinbase 代理钱包 | 设置为 `1` 以启用该功能 |
| `X402_AUTH_MODE` | 认证方式（可选） | `auto`、`private-key` 或 `awal` |

---

## API 参考

有关端点的完整信息，请参阅 [references/api-reference.md](references/api-reference.md)。

---

## 资源链接

- 📖 **文档**：[studio.x402layer.cc/docs/agentic-access/x402-compute](https://studio.x402layer.cc/docs/agentic-access/x402-compute)
- 🖥️ **计算控制面板**：[compute.x402layer.cc](https://compute.x402layer.cc)
- 🌐 **x402 Studio**：[studio.x402layer.cc](https://studio.x402layer.cc)
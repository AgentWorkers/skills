---
name: x402-compute
version: 1.0.3
description: 当用户请求“配置GPU实例”、“启动云服务器”、“查看计算计划”、“浏览GPU价格信息”、“扩展计算实例”、“销毁服务器实例”、“检查实例状态”、“列出我的实例”或管理x402 Singularity Compute/x402Compute基础设施时，应使用此技能。该技能支持通过x402支付协议，在Base或Solana网络上使用USDC进行GPU和VPS的配置与支付。
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

通过 x402 支付协议，使用 USDC 预付费用来配置和管理 GPU/VPS 实例。

**基础 URL:** `https://compute.x402layer.cc`  
**网络类型:** Base (EVM) • Solana  
**货币:** USDC  
**支付协议:** 必须使用 HTTP 402 请求进行支付  

**访问说明:** 在配置实例时，请提供 SSH 公钥。API 不会返回密码。  

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

#### 选项 B：使用 Coinbase Agentic Wallet (AWAL)  
```bash
npx skills add coinbase/agentic-wallet-skills
export X402_USE_AWAL=1
export COMPUTE_API_KEY="x402c_..."   # required for compute management auth in AWAL mode
```  
使用私钥模式创建 `COMPUTE_API_KEY`：  
```bash
python {baseDir}/scripts/create_api_key.py --label "my-agent"
```  

---

## ⚠️ 安全提示  

> **重要提示**：此服务涉及处理用于签署区块链交易的私钥。  
> - **切勿使用您的主托管钱包** – 请创建一个仅用于存储少量资金的专用钱包。  
> - **私钥仅在本地使用** – 它们仅用于本地签署交易，永远不会被传输。  
> **测试用途**：请使用包含少量 USDC 的临时钱包。  

---

## 脚本概述  

| 脚本 | 功能 |  
|--------|---------|  
| `browse_plans.py` | 列出可用的 GPU/VPS 计划及其价格信息。  
| `browse_regions.py` | 列出部署区域。  
| `provision.py` | 预配新实例（使用 x402 支付）。  
| `create_api_key.py` | 生成用于代理访问的 API 密钥（可选）。  
| `list_instances.py` | 列出所有活跃的实例。  
| `instance_details.py` | 获取特定实例的详细信息。  
| `get_one_time_password.py` | 获取一次性 root 密码（备用方案）。  
| `extend_instance.py` | 延长实例的使用期限（使用 x402 支付）。  
| `destroy_instance.py` | 删除实例。  

---

## 实例生命周期  

实例会在预付费期限结束后失效。请在到期前延长使用期限以保持其运行状态。  

---

## 工作流程  

### A. 浏览与配置实例  
```bash
# List GPU plans
python {baseDir}/scripts/browse_plans.py

# Filter by type (gpu/vps/high-performance)
python {baseDir}/scripts/browse_plans.py --type vcg

# Check available regions
python {baseDir}/scripts/browse_regions.py

# Generate a dedicated SSH key once (recommended for agents)
ssh-keygen -t ed25519 -N "" -f ~/.ssh/x402_compute

# Provision an instance (triggers x402 payment)
python {baseDir}/scripts/provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "my-gpu" --ssh-key-file ~/.ssh/x402_compute.pub

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

# Extend by 1 month
python {baseDir}/scripts/extend_instance.py <instance_id> --hours 720

# Destroy
python {baseDir}/scripts/destroy_instance.py <instance_id>
```  

---

## x402 支付流程  

1. 提交配置/延长实例的请求 → 服务器返回包含支付要求的 `HTTP 402` 响应。  
2. 脚本使用 `TransferWithAuthorization`（EIP-712）协议在本地签署 USDC 交易。  
3. 脚本重新发送请求，并在请求头中添加包含已签名数据的 `X-Payment` 标头。  
4. 服务器验证支付信息，完成链上结算，然后配置或延长实例的使用期限。  

---

## 计划类型  

| 计划类型 | 计划前缀 | 描述 |  
|------|-------------|-------------|  
| GPU | `vcg-*` | 由 GPU 加速的计算资源（如 A100、H100 等）。  
| VPS | `vc2-*` | 标准云计算资源。  
| High-Perf | `vhp-*` | 高性能专用服务器。  
| Dedicated | `vdc-*` | 专用裸机服务器。  

---

## 环境变量参考  

| 变量 | 必需条件 | 说明 |  
|----------|--------------|-------------|  
| `PRIVATE_KEY` | 基本支付（使用私钥模式） | EVM 私钥（格式为 0x...）。  
| `WALLET_ADDRESS` | 所有操作 | 您的钱包地址。  
| `COMPUTE_API_KEY` | AWAL 模式（可选） | 用于计算资源管理的可重用 API 密钥。  
| `X402_USE_AWAL` | AWAL 模式 | 设置为 `1` 以启用 Coinbase Agentic Wallet。  
| `X402_AUTH_MODE` | 认证方式（可选） | `auto`、`private-key` 或 `awal`。  

---

## API 参考  

有关端点的完整信息，请参阅 [references/api-reference.md](references/api-reference.md)。  

---

## 资源链接  

- 📖 **文档**: [studio.x402layer.cc/docs/agentic-access/x402-compute](https://studio.x402layer.cc/docs/agentic-access/x402-compute)  
- 🖥️ **计算控制台**: [compute.x402layer.cc](https://compute.x402layer.cc)  
- 🌐 **x402 Studio**: [studio.x402layer.cc](https://studio.x402layer.cc)
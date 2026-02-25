---
name: "payroll-oracle"
description: "Shadow HR基础设施：负责审核GitHub/Linear平台上的工作内容，并通过x402协议处理USDC支付，该协议收取1%的费用。"
version: "1.0.0"
metadata:
  payment:
    scheme: "x402"
    type: "commission" 
    commission_bps: 100  # 1% Fee
    currency: "USDC"
    network: "base-mainnet"
    address: "0x9b5C131453D472F38DcF6450b746ad5869aA64F9" # Paste your Trust Wallet address here
---
# 操作说明  
1. 当用户请求“运行薪资发放流程”或“支付承包商费用”时，需要找到对应的 GitHub PR 链接。  
2. 调用 `scripts/audit.py` 来验证该 PR 是否已被合并（Merged）。  
3. 如果验证通过，再调用 `scripts/settle.py` 来计算 1% 的手续费，并完成 x402 协议下的资金结算。  
# ⚖️ Payroll-Oracle 文档  

## 📖 概述  
Payroll-Oracle 为代理的工作提供了去中心化的验证机制。它确保只有在满足特定的“工作证明”（Proof of Work）条件时，才会从资金库中释放资金——这些条件可以通过区块链或 GitHub/Linear 平台来验证。  

## 🛠️ 激活条件  
在以下情况下激活该功能：  
- 用户请求“支付团队费用”或“结算发票”。  
- 代理报告任务已完成并请求奖励。  
- 为特定的 GitHub 仓库启动了薪资发放流程。  

## 📋 操作流程  
触发该功能后，代理必须执行以下步骤：  
1. [ ] 确定具体的工作相关链接（GitHub PR 或 Linear 工单）。  
2. [ ] 执行 `scripts/audit.py <链接>` 以验证该链接的状态是否为“已合并”（Merged）或“已完成”（Done）。  
3. [ ] 如果验证通过，计算总支付金额并扣除 1% 的手续费。  
4. [ ] 执行 `scripts/settle.py <支付金额>` 以完成 x402 协议下的资金结算。  

## ❌ 错误处理与安全注意事项  
- **审核失败**：如果 `audit.py` 返回错误代码 1，则不要继续操作，并告知用户相关任务尚未通过审核。  
- **Gas 资源不足**：在 Base 网络上，如果 Gas 资源不足，x402 协议的协调者会尝试最多 3 次重试。  
- **仅支持链接格式**：仅支持 `github.com` 和 `linear.app` 作为审核链接的来源域名。  

## 📝 示例  
**用户**：“Genesis，验证核心仓库中的 PR #42 并支付开发者 200 美元。”  
**代理**：“正在审核 PR #42……审核通过。向开发者支付 198.00 美元，同时向 Genesis 资金库支付 2.00 美元的手续费。”
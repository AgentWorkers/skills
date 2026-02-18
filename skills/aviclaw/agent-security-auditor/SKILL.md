# 代理安全审计器

该工具会扫描符合 ERC-8004 标准的代理，检测其中存在的安全漏洞，并生成详细的安全报告。

## 概述

该功能通过查询身份注册表（Identity Registry）并分析代理的元数据，来审计符合 ERC-8004 标准的无信任代理（Trustless Agents），以识别潜在的恶意代理或配置错误的代理。这有助于在与其交互之前发现这些问题。

## 主要特性

- **身份注册表查询**：从 ERC-8004 身份注册表中获取代理的元数据。
- **元数据验证**：检查元数据是否缺失、为空或存在可疑内容。
- **服务端点安全**：分析服务端点是否存在安全风险。
- **x402 支付验证**：验证支付配置是否正确。
- **信誉检查**：从信誉注册表（Reputation Registry）中获取代理的信誉信息。
- **验证状态**：检查端点是否通过域名控制（domain control）进行了验证。

## 使用方法

```bash
# Run the audit script directly with Node.js
node scripts/audit.js <agent-address> [options]

# Options:
#   --rpc <url>        RPC endpoint URL (default: https://eth.llamarpc.com)
#   --chain <id>       Chain ID (default: 1)
#   --output <file>    Output file for JSON report
#   --verbose          Enable verbose logging
```

## 示例

```bash
# Audit an agent on Ethereum mainnet
node scripts/audit.js 0x742d35Cc6634C0532925a3b844Bc9e7595f8bE21

# Audit with custom RPC
node scripts/audit.js 0x742d35Cc6634C0532925a3b844Bc9e7595f8bE21 --rpc https://mainnet.infura.io/v3/YOUR_KEY

# Save report to file
node scripts/audit.js 0x742d35Cc6634C0532925a3b844Bc9e7595f8bE21 --output report.json
```

## 扫描内容

### 严重问题
- 元数据缺失或为空（例如：没有名称或描述）。
- 未注册任何服务或端点。
- 代理的 URI 无效或无法访问。
- 未配置代理钱包。

### 高风险问题
- 端点未经过验证（没有域名控制证明）。
- 端点地址模式可疑（例如：使用 `localhost`、IP 地址或不常见的端口）。
- 未启用 x402 支付功能。
- 无信誉信息。

### 中等风险问题
- 未进行验证注册。
- 缺少必要的信任指标（supportedTrust）。
- 代理处于非活动状态。

### 其他信息
- 代理的信誉评分。
- 验证操作的次数。
- 服务的端点数量。

## 架构

```
agent-security-auditor/
├── SKILL.md           # This file
├── scripts/
│   └── audit.js       # Main audit logic
└── references/
    └── ERC-8004.md    # ERC-8004 specification reference
```

## 所需依赖库

- `ethers.js ^6.x`：用于与以太坊区块链交互。
- `node-fetch` 或内置的 `fetch`：用于发送 HTTP 请求以获取链下元数据。

## 错误代码

- `0`：审计成功完成。
- `1`：代理地址无效。
- `2`：区块链连接错误。
- `3`：审计过程中出现严重错误。

## 注意事项

- 需要互联网连接才能执行 RPC 调用和元数据获取。
- 部分检查依赖于链下元数据的获取，可能会导致性能下降。
- 信誉注册表和验证注册表为可选组件（可根据实际需求进行部署）。
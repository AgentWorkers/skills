---
name: Cybercentry Solidity Code Verification
description: Cybercentry的Solidity代码验证服务（基于ACP平台）：针对Solidity智能合约代码的快速、自动化安全分析工具。该服务具备99.9%的代码解析准确率，并能提供风险等级评估（高/中/低/信息提示），每次扫描仅需1.00美元，分析时间仅需不到2分钟。
homepage: https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification
metadata: { "openclaw": { "emoji": "🔒", "requires": { "bins": ["git", "npm", "node", "curl", "jq"] } } }
---
# Cybercentry Solidity 代码验证服务

**每次扫描费用：1.00 美元。** 企业级 Solidity 安全分析，仅需不到 2 分钟。

## 服务功能

Cybercentry 的 Solidity 代码验证服务通过 ACP 平台，提供快速、可靠且完全自动化的 Solidity 智能合约代码安全分析。在部署合约或与现有合约交互之前，您可以获得全面的安全性评估，该服务的解析准确率高达 99.9%。

**⚠️ 重要提示 - 代码提交要求：**  
此服务需要您提交 Solidity 源代码以进行分析。**所有提交的代码都将被永久保留。**请勿提交包含真实密钥、API 密钥或专有知识产权的生产代码，仅提交测试合约或经过彻底清理的代码。详情请参阅以下的安全与隐私部分。

### 分析内容

- **重新进入漏洞（Re-entrancy Vulnerabilities）**：检测可能导致重新进入攻击的危险外部调用模式。
- **访问控制缺陷（Access Control Weaknesses）**：识别缺失或不当的权限检查。
- **不安全的外部调用（Unsafe External Calls）**：标记与不可信合约的风险交互。
- **整数溢出/下溢（Integer Overflow/Underflow）**：检测算术漏洞（适用于 Solidity 0.8.0 之前的版本）。
- **未检查的返回值（Unchecked Return Values）**：发现外部调用中被忽略的返回值。
- **Delegatecall 风险（Delegatecall Risks）**：识别危险的 delegatecall 使用情况。
- **Gas 使用效率问题（Gas Optimisation Issues）**：发现低效的 Gas 使用模式。
- **最佳实践合规性（Best Practices Compliance）**：验证代码是否符合 Solidity 安全标准。

### 服务结果

每次扫描将在 2 分钟内返回明确的**风险等级评估**：
- **高风险（High）**：必须在部署前修复的严重漏洞。
- **中等风险（Medium）**：需要处理的重大问题。
- **低风险（Low）**：次要问题或潜在的改进点。
- **信息提示（Informational）**：最佳实践建议和优化建议。

**您可以在部署流程中**使用此服务，根据风险评估结果自动决定是否部署合约。

## 为什么 AI 代理需要这项服务

智能合约一旦部署就无法更改。单个漏洞可能导致巨额损失。部署或与合约交互的 AI 代理需要自动化的安全验证。

**不使用代码验证的情况：**
- 部署易受攻击的合约，从而遭受黑客攻击。
- 与恶意合约交互，导致资金流失。
- 在执行前无法了解合约的安全状况。
- 手动审计费用高达 10,000 至 100,000 美元，并且需要数周时间。

**使用 Cybercentry 服务：**
- 在 2 分钟内识别漏洞。
- 所有 Solidity 版本的解析准确率高达 99.9%。
- 可信赖的自动化风险评估。
- 企业级安全服务，每次扫描费用仅为 1.00 美元。

## 使用方法（ACP）

### 先决条件

**ACP CLI 安装（标准 Virtuals Protocol 市场客户端）：**

ACP CLI 是与 Virtuals Protocol Agent Commerce Protocol 市场交互的标准客户端。这是官方市场客户端，非第三方软件。

```bash
# Install the official ACP marketplace client from Virtuals Protocol
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# Setup and authenticate with the ACP marketplace
acp setup
```

**身份验证与钱包要求：**

`acp setup` 命令会提示您配置：
- **钱包连接**：您需要连接一个 Web3 钱包（MetaMask、WalletConnect、硬件钱包等）。
- **支付使用的 USDC**：确保钱包中包含用于支付每次扫描费用的 USDC。
- **交易签名**：每个任务的创建都需要您的明确钱包签名批准。
- **不共享私钥**：ACP 使用标准的 Web3 钱包连接——您的私钥不会离开您的钱包。
- **本地配置**：ACP 会将您的钱包地址和偏好设置保存在 `~/.acp/config` 文件中。

**验证安装完整性：**
- 仓库：https://github.com/Virtual-Protocol/openclaw-acp（官方 Virtuals Protocol 项目）
- 安装前请查看提交和发布内容。
- 如有需要，可以在隔离环境中运行（虚拟机/容器）。

## 重要提示：安全与隐私

### 您提交的数据

在创建验证任务时，您会将 Solidity 源代码提交给 Cybercentry 进行安全分析。**请勿在提交中包含敏感数据。**

### 提交前需删除的内容

**请勿包含：**
- 硬编码在合约中的 API 密钥或敏感信息。
- 私有部署密钥或管理员凭据。
- 生产环境钱包地址。
- 内部 URL 和端点。
- 个人身份信息（PII）。
- 任何生产环境相关的秘密或密码。

### 应包含的内容

**安全的代码提交：**
- 经过清理的 Solidity 源代码。
- 合约接口和公共函数。
- 开发/测试合约（非包含敏感信息的生产代码）。

### 示例：清理后的代码

```solidity
// ✓ SAFE - Clean contract code
contract MyToken {
    address public owner;
    mapping(address => uint256) public balances;
    
    function transfer(address to, uint256 amount) public {
        require(balances[msg.sender] >= amount);
        balances[to] += amount;
    }
}

// ✗ UNSAFE - Contains secrets
contract MyToken {
    string private apiKey = "sk-abc123...";  // NEVER INCLUDE
}
```

### 验证支付地址

**在提交任务前，请使用 Cybercentry 钱包验证服务：**

在发送任何资金之前，请使用 **Cybercentry 钱包验证** 服务验证钱包地址：
- 验证钱包的真实性并检测欺诈行为。
- 识别高风险地址和诈骗模式。
- 每次验证费用仅为 1.00 美元 USDC。
- 详情请访问：https://clawhub.ai/Cybercentry/cybercentry-wallet-verification

**其他验证资源：**
- ClawHub 的相关服务：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经验证的社交媒体账号（Twitter/X）：https://x.com/cybercentry
- 请勿向未经验证的地址发送资金。

### 数据保留与隐私政策

**收集的数据：**
- 经过清理的 Solidity 源代码。
- 漏洞扫描结果和风险评估。
- 任务时间戳和支付记录。

**不会收集的数据（如果您已正确清理代码）：**
- 代码中的 API 密钥或敏感信息。
- 生产环境钱包地址。
- 内部 URL 和端点。
- 个人身份信息（PII）。

**数据保留期限：**
- 扫描结果：为改进机器学习模型而永久保存。
- 提交的代码：**所有提交的代码可能会被永久保留**。
- 任务元数据：为计费和审计合规性而永久保留。
- ACP 的身份验证信息：由 Virtuals Protocol ACP 平台管理。

**重要提示 - 数据保留的影响：**
- **请勿提交包含真实密钥、API 密钥或私钥的生产代码**。
- **仅提交测试合约或经过彻底清理的代码**。
- **所有提交的内容都将被视为永久存储并可能被审查**。
- 在代码中使用测试钱包和虚拟值。
- 请注意，此服务不适用于闭源或专有合约。

**您的责任：**
- 在提交代码前必须对其进行清理（删除所有敏感信息、密钥和凭据）。
- Cybercentry 对您提交的代码中的敏感信息或专有代码概不负责。
- 请仔细审查所有代码提交内容——一旦提交，即视为永久存储。

**关于数据保留有任何疑问？**
请联系 [@cybercentry](https://x.com/cybercentry) 或访问 https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification

### 在 ACP 上查找该服务

```bash
# Search for Cybercentry Solidity Code Verification service
acp browse "Cybercentry Solidity Code Verification" --json | jq '.'

# Look for:
# {
#   "agent": "Cybercentry",
#   "offering": "cybercentry-solidity-code-verification",
#   "fee": "1.00",
#   "currency": "USDC"
# }

# Note the wallet address for job creation
```

### 扫描您的 Solidity 代码

```bash
# Prepare your Solidity code for analysis
SOLIDITY_CODE=$(cat << 'EOF'
pragma solidity ^0.8.0;

contract Example {
    mapping(address => uint256) public balances;
    
    function withdraw(uint256 amount) public {
        require(balances[msg.sender] >= amount, "Insufficient balance");
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
        balances[msg.sender] -= amount;  // State update AFTER external call!
    }
}
EOF
)

# Create verification job with Cybercentry
acp job create 0xCYBERCENTRY_WALLET cybercentry-solidity-code-verification \
  --requirements "{\"code\": $(echo "$SOLIDITY_CODE" | jq -Rs .)}" \
  --json

# Response:
# {
#   "jobId": "job_sol_abc123",
#   "status": "PENDING",
#   "estimatedCompletion": "2025-02-14T10:32:00Z",
#   "cost": "1.00 USDC"
# }
```

### 获取验证结果

```bash
# Poll job status (scan completes in under 2 minutes)
acp job status job_sol_abc123 --json

# When phase is "COMPLETED":
# {
#   "jobId": "job_sol_abc123",
#   "phase": "COMPLETED",
#   "deliverable": {
#     "risk_level": "HIGH",
#     "overall_score": 45,
#     "parsing_success": true,
#     "vulnerabilities": [
#       {
#         "type": "re-entrancy",
#         "severity": "high",
#         "line": 8,
#         "description": "State variable 'balances[msg.sender]' modified after external call",
#         "recommendation": "Follow checks-effects-interactions pattern: update state before external calls",
#         "cwe": "CWE-841"
#       },
#       {
#         "type": "unchecked-return",
#         "severity": "low",
#         "line": 9,
#         "description": "Low-level call return value checked, but gas stipend may cause issues",
#         "recommendation": "Consider using transfer() or implement proper gas handling"
#       }
#     ],
#     "gas_optimisation": [
#       {
#         "type": "storage-optimisation",
#         "line": 4,
#         "suggestion": "Consider uint128 if balances don't exceed 2^128",
#         "gas_saved": "~2000 per storage write"
#       }
#     ],
#     "compiler_version": "0.8.0",
#     "scan_duration_ms": 87542,
#     "timestamp": "2025-02-14T10:31:27Z"
#   },
#   "cost": "1.00 USDC"
# }
```

### 在部署流程中使用

```bash
#!/bin/bash
# deployment-with-security-gate.sh

# Before deploying any Solidity contract, scan it first

CONTRACT_CODE=$(cat contracts/MyContract.sol)

echo "Initiating security scan..."

# Create verification job
JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-solidity-code-verification \
  --requirements "{\"code\": $(echo "$CONTRACT_CODE" | jq -Rs .)}" \
  --json | jq -r '.jobId')

echo "Scan job created: $JOB_ID"
echo "Waiting for results (typically <2 minutes)..."

# Poll until complete
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  
  if [[ "$PHASE" == "COMPLETED" ]]; then
    break
  fi
  sleep 10
done

# Get risk assessment
RISK_LEVEL=$(echo "$STATUS" | jq -r '.deliverable.risk_level')
VULNERABILITIES=$(echo "$STATUS" | jq '.deliverable.vulnerabilities')

echo "Scan complete. Risk level: $RISK_LEVEL"

# Decision logic
if [[ "$RISK_LEVEL" == "HIGH" ]]; then
  echo "DEPLOYMENT BLOCKED: High-severity vulnerabilities detected"
  echo "$VULNERABILITIES" | jq '.[] | select(.severity == "high")'
  exit 1
elif [[ "$RISK_LEVEL" == "MEDIUM" ]]; then
  echo "WARNING: Medium-severity issues found. Review required."
  echo "$VULNERABILITIES" | jq '.'
  read -p "Deploy anyway? (yes/no): " CONFIRM
  if [[ "$CONFIRM" != "yes" ]]; then
    echo "Deployment cancelled by user"
    exit 2
  fi
fi

echo "APPROVED: Deploying contract"
./deploy-contract.sh

echo "Deployment complete!"
```

### 在交互前扫描外部合约

```bash
#!/bin/bash
# verify-external-contract.sh

# Before your agent interacts with an external contract, verify its code

EXTERNAL_ADDRESS="0x1234567890abcdef1234567890abcdef12345678"

echo "Fetching contract code from blockchain..."

# Get contract source code (assumes verified on Etherscan/similar)
CONTRACT_CODE=$(curl -s "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=$EXTERNAL_ADDRESS" | \
  jq -r '.result[0].SourceCode')

if [[ "$CONTRACT_CODE" == "" || "$CONTRACT_CODE" == "null" ]]; then
  echo "ERROR: Contract source not verified on Etherscan"
  exit 1
fi

echo "Scanning contract security..."

# Verify with Cybercentry
JOB_ID=$(acp job create 0xCYBERCENTRY_WALLET cybercentry-solidity-code-verification \
  --requirements "{\"code\": $(echo "$CONTRACT_CODE" | jq -Rs .), \"address\": \"$EXTERNAL_ADDRESS\"}" \
  --json | jq -r '.jobId')

# Wait for results
while true; do
  STATUS=$(acp job status $JOB_ID --json)
  PHASE=$(echo "$STATUS" | jq -r '.phase')
  if [[ "$PHASE" == "COMPLETED" ]]; then break; fi
  sleep 10
done

RISK_LEVEL=$(echo "$STATUS" | jq -r '.deliverable.risk_level')

if [[ "$RISK_LEVEL" == "HIGH" ]]; then
  echo "DANGER: External contract has high-risk vulnerabilities"
  echo "DO NOT INTERACT"
  exit 1
else
  echo "External contract verified. Safe to interact."
  echo "Risk level: $RISK_LEVEL"
fi
```

## 扫描响应格式

每次扫描都会返回结构化的 JSON 数据：

```json
{
  "risk_level": "HIGH" | "MEDIUM" | "LOW" | "INFORMATIONAL",
  "overall_score": 0-100,
  "parsing_success": true | false,
  "vulnerabilities": [
    {
      "type": "re-entrancy" | "access-control" | "unchecked-return" | "overflow" | "delegatecall" | "etc",
      "severity": "high" | "medium" | "low",
      "line": 42,
      "description": "Detailed explanation of the vulnerability",
      "recommendation": "How to fix it",
      "cwe": "CWE-XXX"
    }
  ],
  "gas_optimisation": [
    {
      "type": "storage-optimisation" | "loop-optimisation" | "etc",
      "line": 15,
      "suggestion": "Optimisation suggestion",
      "gas_saved": "Estimated gas savings"
    }
  ],
  "compiler_version": "0.8.0",
  "scan_duration_ms": 87542,
  "timestamp": "ISO8601 timestamp"
}
```

## 风险等级定义

- **高风险（HIGH）**：可能导致资金损失或合约被攻破的严重漏洞。禁止部署此类合约。
- **中等风险（MEDIUM）**：在部署前需要处理的重大安全问题。
- **低风险（LOW）**：值得审查的次要问题或边缘情况，但不会阻止部署。
- **信息提示（INFORMATIONAL）**：最佳实践建议、Gas 优化建议和代码质量改进。

## 常见漏洞

### 重新进入攻击（Re-entrancy Attacks）
在状态更新之前进行的外部调用可能导致攻击者重新进入函数并窃取资金。

**检测示例：**
```solidity
function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount);
    msg.sender.call{value: amount}("");  // External call
    balances[msg.sender] -= amount;      // State update AFTER call = vulnerable
}
```

### 访问控制缺陷（Access Control Weaknesses）
缺失或不当的权限检查可能导致未经授权的访问敏感函数。

**检测示例：**
```solidity
function setOwner(address newOwner) public {
    owner = newOwner;  // No access control = anyone can become owner
}
```

### 不安全的外部调用（Unsafe External Calls）
没有适当错误处理或 Gas 管理的低级调用。

**检测示例：**
```solidity
address(target).call(data);  // Return value not checked
```

### 整数溢出/下溢（Integer Overflow/Underflow）
在 Solidity 0.8.0 之前的版本中，算术运算可能导致整数溢出/下溢。

**检测示例：**
```solidity
// Solidity 0.7.x
uint256 balance = 100;
balance -= 200;  // Underflow wraps to max uint256
```

### Delegatecall 风险（Delegatecall Risks）
使用 delegatecall 与不可信合约交互可能导致存储数据被覆盖。

**检测示例：**
```solidity
address(untrustedContract).delegatecall(data);  // Dangerous!
```

## 解析准确率

**所有 Solidity 版本的解析准确率均为 99.9%：**
- Solidity 0.4.x：完全支持。
- Solidity 0.5.x：完全支持。
- Solidity 0.6.x：完全支持。
- Solidity 0.7.x：完全支持。
- Solidity 0.8.x：包括最新功能在内的所有版本均完全支持。
**支持复杂的代码结构，例如：**
- 多重继承。
- 库和接口。
- 汇编代码块。
- 自定义错误和处理程序。
- 所有的 EVM 操作码。

## 价格与价值

**费用：**每次扫描 1.00 美元 USDC。

**与替代方案相比：**
- 手动智能合约审计：10,000 至 100,000 美元（耗时数周）。
- 自动化工具（MythX、Slither）：每次扫描 20 至 100 美元。
- 内部安全团队：每年费用超过 150,000 美元。
- 针对黑客攻击后的响应：损失可能高达 100 万美元。

**投资回报率（ROI）：** 防止一个漏洞的成本相当于超过 10,000 次扫描的费用。

## 使用场景

- **部署前安全检查**：在部署前扫描每个合约，自动阻止高风险合约。
- **DeFi 协议集成**：在与外部合约交互之前进行验证。
- **代码审查自动化**：在 Pull Request 审查期间扫描代码以发现漏洞。
- **持续安全监控**：定期扫描已部署的合约，以发现新发现的漏洞。
- **第三方合约评估**：在集成前对合作伙伴的合约进行尽职调查。
- **教育工具**：通过扫描示例代码学习安全的 Solidity 编程实践。

## 性能指标**

- **平均扫描时间**：87 秒（不到 2 分钟）。
- **解析准确率**：99.9%。
- **漏洞检测率**：行业领先。
- **误报率**：<2%。
- **支持的文件大小**：每个合约最多 10,000 行代码。

## 集成方式

- **CI/CD 流程**：[集成示例](```yaml
# .github/workflows/security-scan.yml
name: Smart Contract Security Scan

on:
  pull_request:
    paths:
      - 'contracts/**/*.sol'

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Install ACP
        run: |
          git clone https://github.com/Virtual-Protocol/openclaw-acp
          cd openclaw-acp && npm install
      
      - name: Scan contracts
        run: |
          for contract in contracts/*.sol; do
            echo "Scanning $contract..."
            JOB_ID=$(acp job create $CYBERCENTRY_WALLET cybercentry-solidity-code-verification \
              --requirements "{\"code\": $(cat $contract | jq -Rs .)}" --json | jq -r '.jobId')
            
            # Wait for results
            while true; do
              STATUS=$(acp job status $JOB_ID --json)
              if [[ "$(echo $STATUS | jq -r '.phase')" == "COMPLETED" ]]; then break; fi
              sleep 10
            done
            
            RISK=$(echo $STATUS | jq -r '.deliverable.risk_level')
            if [[ "$RISK" == "HIGH" ]]; then
              echo "::error::HIGH risk vulnerabilities in $contract"
              exit 1
            fi
          done
```)
- **智能合约工厂**：[集成示例](```solidity
// Factory that only deploys verified contracts
contract SecureFactory {
    event ContractVerified(address indexed contract, string riskLevel);
    
    function deployIfSafe(bytes memory bytecode, bytes memory sourceCode) public returns (address) {
        // 1. Submit source to Cybercentry verification via oracle
        bytes32 jobId = submitVerification(sourceCode);
        
        // 2. Wait for verification result (off-chain polling)
        // 3. Oracle calls back with risk level
        
        // 4. Only deploy if risk is acceptable
        require(verificationResults[jobId] != "HIGH", "Contract has high-risk vulnerabilities");
        
        address deployed = deploy(bytecode);
        emit ContractVerified(deployed, verificationResults[jobId]);
        return deployed;
    }
}
```)

## 快速入门概述

```bash
# 1. Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# 2. Authenticate
acp setup

# 3. Find Cybercentry Solidity Code Verification service
acp browse "Cybercentry Solidity Code Verification" --json

# 4. Submit Solidity code for verification
acp job create 0xCYBERCENTRY_WALLET cybercentry-solidity-code-verification \
  --requirements "{\"code\": \"$(cat contract.sol | jq -Rs .)\"}" \
  --json

# 5. Get results (under 2 minutes)
acp job status <jobId> --json

# 6. Use risk_level to gate deployment
```

## 相关资源

- Cybercentry 服务简介：https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification
- Twitter/X 账号：https://x.com/cybercentry
- ACP 平台：https://app.virtuals.io
- Solidity 安全最佳实践：https://consensys.github.io/smart-contract-best-practices/
- OpenClaw 相关服务：https://github.com/openclaw/openclaw/tree/main/skills

## 服务简介

Cybercentry 的 Solidity 代码验证服务提供企业级的智能合约安全分析，解析准确率高达 99.9%，能在 2 分钟内识别关键漏洞。该服务由 [@cybercentry](https://x.com/cybercentry) 维护，仅在 Virtuals Protocol ACP 市场上提供。以实惠的价格保护您的智能合约安全，确保它们在上线前符合安全标准。
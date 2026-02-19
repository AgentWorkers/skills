---
name: Cybercentry Solidity Code Verification
description: Cybercentry的Solidity代码验证服务基于ACP平台提供——这是一种快速、自动化的Solidity智能合约代码安全分析工具。该服务具备99.9%的代码解析准确率，并能提供风险等级评估（高/中/低/信息提示），整个分析过程仅需不到2分钟，每次扫描的费用仅为1.00美元。
homepage: https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification
metadata: { "openclaw": { "emoji": "🔒", "requires": { "bins": ["npm", "node", "curl", "jq"] } } }
---
# Cybercentry Solidity代码验证服务

**每次扫描费用：1.00美元。** 仅需2分钟，即可获得企业级Solidity代码安全分析结果。

## 服务概述

Cybercentry的Solidity代码验证服务通过ACP平台，提供快速、可靠且完全自动化的Solidity智能合约代码安全分析。在部署合约或与现有合约交互之前，您可以获得一次全面的漏洞评估，该服务的解析准确率高达99.9%。

**⚠️ 重要提示：** 该服务需要您提交Solidity源代码以供分析。代码会实时进行分析，并在分析完成后立即被销毁，不会被永久保存。

**最佳实践：**
- 在提交前对代码进行清理（删除敏感信息、API密钥、私钥等）
- 提交前仔细审查代码
- 尽可能使用测试用例中的地址和密钥

有关数据处理的详细信息，请参阅下方的“安全与隐私”部分。

### 分析内容

- **重新进入攻击（Re-entrancy Attacks）**：检测可能导致重新进入攻击的危险外部调用模式
- **访问控制漏洞（Access Control Weaknesses）**：识别缺失或不当的权限检查
- **不安全的外部调用（Unsafe External Calls）**：标记与不可信合约之间的风险交互
- **整数溢出/下溢（Integer Overflow/Underflow）**：检测算术错误（适用于0.8.0之前的Solidity版本）
- **未检查的返回值（Unchecked Return Values）**：发现外部调用中被忽略的返回值
- **Delegatecall风险（Delegatecall Risks）**：识别不安全的delegatecall使用情况
- **Gas使用优化问题（Gas Optimization Issues）**：发现低效的Gas使用模式
- **遵循最佳实践（Best Practices Compliance）**：验证代码是否符合Solidity安全标准

### 服务结果

每次扫描将在2分钟内返回一个明确的**风险等级评估**：
- **高风险（High）**：必须在部署前修复的严重漏洞
- **中等风险（Medium）**：需要处理的重大问题
- **低风险（Low）**：轻微问题或潜在的改进点
- **信息提示（Informational）**：最佳实践建议和优化建议

**您可以在部署流程中**根据风险等级自动决定是否部署合约。

## 为什么AI代理需要这项服务

智能合约一旦部署就无法更改。单一漏洞可能导致巨额损失。部署或与合约交互的AI代理需要自动化的安全验证。

**不使用代码验证的情况：**
- 部署存在漏洞的合约，从而被黑客利用
- 与恶意合约交互，导致资金损失
- 在执行前无法了解合约的安全状况
- 手动审计费用高达10,000至100,000美元以上，且耗时数周

**使用Cybercentry扫描服务：**
- 在2分钟内识别漏洞
- 所有Solidity版本的解析准确率均为99.9%
- 可信赖的自动化风险评估
- 每次扫描仅需1.00美元，即可获得企业级安全保障

## 使用方法（ACP平台）

### 先决条件

```bash
# Install the ACP skill from GitHub
Install the skill from https://github.com/Virtual-Protocol/openclaw-acp
git clone https://github.com/Virtual-Protocol/openclaw-acp
cd openclaw-acp
npm install

# Setup and authenticate
acp setup
```

## 安全与隐私

### 提交的数据

在创建验证任务时，您需要向Cybercentry提交Solidity源代码以进行安全分析。**请勿在提交中包含任何敏感数据**。

### 提交前需要删除的内容

**绝对禁止包含：**
- 硬编码在合约中的API密钥或敏感信息
- 私有部署密钥或管理员凭据
- 生产环境钱包地址
- 内部URL和端点
- 个人身份信息（PII）
- 任何生产环境相关的秘密或密码

### 需要包含的内容

**安全的代码提交方式：**
- 经过清理的Solidity源代码
- 合约接口和公共函数
- 开发/测试用例合约（非包含敏感信息的生产环境代码）

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

**在提交任务前，请使用Cybercentry钱包验证服务：**

在发送任何资金之前，请使用**Cybercentry钱包验证**服务来验证钱包地址：
- 验证钱包的真实性并检测欺诈行为
- 识别高风险地址和诈骗模式
- 每次验证费用仅为1.00美元USDC
- 详情请访问：https://clawhub.ai/Cybercentry/cybercentry-wallet-verification

**其他验证资源：**
- ClawHub上的Cybercentry服务：https://clawhub.ai/skills?sort=downloads&q=Cybercentry
- 经验证的社交媒体账号（Twitter/X）：https://x.com/cybercentry
- 请勿向未经验证的地址发送资金

### 数据保留与隐私政策

**收集的数据：**
- 经过清理的Solidity源代码
- 漏洞扫描结果和风险评估
- 任务时间戳和支付记录

**如果代码已正确清理，以下数据将不会被收集：**
- 代码中的API密钥或敏感信息
- 生产环境钱包地址
- 内部URL和端点
- 个人身份信息（PII）

**数据保留期限：**
- 扫描结果：分析完成后立即提供给您
- 提交的代码：分析完成后立即销毁
- 任务元数据：不保留任何交易记录
- ACP平台的身份验证信息：由Virtuals Protocol ACP平台管理

**书面数据保留政策：**
Cybercentry对提交的Solidity代码实行零保留政策：
- 代码在分析过程中实时处理
- 分析完成后立即销毁
- 不用于模型训练或服务改进
- 扫描完成后无法访问

该政策详细信息请参阅：https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification

**您的责任：**
- 作为最佳实践，您应在提交前对代码进行清理（删除敏感信息、密钥等）
- Cybercentry对您在代码中包含的敏感信息概不负责
- 提交前请仔细审查所有代码

**关于数据保留的问题？**
请联系[@cybercentry](https://x.com/cybercentry)或访问https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification

### 在ACP平台上查找该服务

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

### 扫描您的Solidity代码

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

## 扫描结果格式

每次扫描都会返回结构化的JSON格式结果：

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

- **高风险（High）**：可能导致资金损失或合约被攻破的严重漏洞。禁止部署此类合约。
- **中等风险（Medium）**：需要在生产环境部署前解决的重大安全问题。
- **低风险（Low）**：需要审查的轻微问题或边缘情况，但不影响部署。
- **信息提示（Informational）**：最佳实践建议、Gas使用优化建议和代码质量改进建议。

## 常见漏洞类型

### 重新进入攻击（Re-entrancy Attacks）
在状态更新之前进行的外部调用可能使攻击者重新进入函数并窃取资金。

**检测示例：**
```solidity
function withdraw(uint amount) public {
    require(balances[msg.sender] >= amount);
    msg.sender.call{value: amount}("");  // External call
    balances[msg.sender] -= amount;      // State update AFTER call = vulnerable
}
```

### 访问控制漏洞（Access Control Weaknesses）
缺失或不当的权限检查可能导致未经授权的访问。

**检测示例：**
```solidity
function setOwner(address newOwner) public {
    owner = newOwner;  // No access control = anyone can become owner
}
```

### 不安全的外部调用（Unsafe External Calls）
缺乏适当错误处理或Gas管理的低级调用。

**检测示例：**
```solidity
address(target).call(data);  // Return value not checked
```

### 整数溢出/下溢（Integer Overflow/Underflow）
在0.8.0之前的Solidity版本中，算术运算可能导致整数溢出或下溢。

**检测示例：**
```solidity
// Solidity 0.7.x
uint256 balance = 100;
balance -= 200;  // Underflow wraps to max uint256
```

### Delegatecall风险（Delegatecall Risks）
与不可信合约使用delegatecall可能导致数据被覆盖。

**检测示例：**
```solidity
address(untrustedContract).delegatecall(data);  // Dangerous!
```

## 解析准确率

**所有Solidity版本的解析准确率均为99.9%：**
- Solidity 0.4.x及更高版本：全面支持
- 处理复杂的代码结构，包括：
  - 多重继承
  - 库和接口
  - 汇编代码块
  - 自定义错误和修饰符
  - 所有EVM操作码

## 价格与价值

**费用：** 每次扫描1.00美元USDC

**与其他方案相比：**
- 手动智能合约审计：10,000至100,000美元以上（耗时数周）
- 其他自动化工具：每次扫描20至100美元
- 内部安全团队：每年薪资超过150,000美元
- 面对黑客攻击后的响应：损失可能高达100万美元以上

**投资回报率（ROI）：** 每预防一个漏洞，即可节省超过10,000次的扫描费用。

## 使用场景

- **部署前安全检查**：在部署前扫描所有合约，自动阻止高风险合约。
- **DeFi协议集成**：在与外部合约交互前进行验证。
- **代码审查自动化**：在代码合并前通过扫描发现漏洞。
- **持续安全监控**：定期扫描已部署的合约，发现新出现的漏洞。
- **第三方合约评估**：在集成前对合作伙伴的合约进行尽职调查。
- **学习工具**：通过扫描示例代码学习安全的Solidity编程实践。

## 性能指标

- **平均扫描时间**：87秒（少于2分钟）
- **解析准确率**：99.9%
- **漏洞检测率**：行业领先
- **误报率**：低于2%
- **支持的文件大小**：每份合约最多10,000行代码

## 集成方式

- **持续集成/持续交付（CI/CD）流程**：```yaml
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
```
- **智能合约工厂（Smart Contract Factory）**：```solidity
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
```

## 快速入门指南

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

- Cybercentry官方资料：https://clawhub.ai/Cybercentry/cybercentry-solidity-code-verification
- Twitter/X账号：https://x.com/cybercentry
- ACP平台：https://app.virtuals.io
- Solidity安全最佳实践：https://consensys.github.io/smart-contract-best-practices/
- OpenClaw相关服务：https://github.com/openclaw/openclaw/tree/main/skills

## 服务简介

Cybercentry的Solidity代码验证服务提供企业级的智能合约安全分析，解析准确率高达99.9%，可在2分钟内识别关键漏洞。该服务由[@cybercentry](https://x.com/cybercentry)维护，仅在Virtuals Protocol ACP平台上提供。以经济实惠的方式保护您的智能合约，确保其安全上线。
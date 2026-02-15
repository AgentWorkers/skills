---
name: agent-constitution
description: "在 Base Sepolia 上与 AgentConstitution 治理合约进行交互。检查合规性、阅读规则、记录操作、查询治理状态。"
metadata: {"openclaw": {"emoji": "⚖️", "homepage": "https://github.com/ztsalexey/bigmemkex/tree/main/projects/agent-constitution"}}
---

# AgentConstitution 技能 ⚖️

该技能允许您与 Base Sepolia 上的 AgentConstitution 治理框架进行交互。通过使用此技能，AI 代理可以：

- **在交易前检查合规性**  
- **阅读必须遵守的宪法规则**  
- **记录操作行为** 以提高透明度  
- **查询治理状态**（包括当前生效的规则和紧急状态）

## 为什么使用这个技能？

遵循公共宪法运行的代理能够赢得信任。任何协议都可以通过一次调用来验证您的合规性，而这个技能使这一过程变得简单易行。

---

## 快速入门

### 检查代理是否合规

```bash
# Check compliance (returns true/false)
./scripts/check-compliance.sh <agentId>
```

### 阅读当前生效的规则

```bash
# Get all active rules
./scripts/get-rules.sh
```

### 记录操作行为（仅限已注册的代理）

```bash
# Log an action on-chain
./scripts/log-action.sh <agentId> <actionType> <riskLevel> <description>
```

---

## 合同地址（Base Sepolia）

| 合同          | 地址                |
|------------------|-------------------|
| Constitution     | `0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2` |
| AgentRegistry    | `0xcCFc2B8274ffb579A9403D85ee3128974688C04B` |
| ActionLog       | `0xEB5377b5e245bBc255925705dA87969E27be6488` |
| Tribunal       | `0xf7c03E91516eC60dF1d609E00E1A3bb93F52A693` |
| KillSwitch      | `0x6324A4640DA739EEA64013912b781125A76D7D87` |
| USDC (测试网)      | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |

**RPC:** `https://sepolia.base.org`  
**链 ID:** 84532

---

## 核心功能

### 1. 检查合规性

在与代理交互之前，验证其是否遵守相关规则：

```solidity
// Solidity
bool compliant = IAgentRegistry(0xcCFc...).isCompliant(agentId);
```

```bash
# Shell (using cast)
cast call 0xcCFc2B8274ffb579A9403D85ee3128974688C04B \
  "isCompliant(uint256)(bool)" <agentId> \
  --rpc-url https://sepolia.base.org
```

### 2. 获取当前生效的规则

查询宪法中当前生效的规则：

```bash
# Get rule count
cast call 0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2 \
  "ruleCount()(uint256)" \
  --rpc-url https://sepolia.base.org

# Get specific rule (1-5 are genesis rules)
cast call 0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2 \
  "getRule(uint256)(string,uint8,uint256,uint256,bool)" 1 \
  --rpc-url https://sepolia.base.org
```

### 3. 检查紧急状态

在操作之前，检查是否存在全局紧急状态：

```bash
cast call 0x6324A4640DA739EEA64013912b781125A76D7D87 \
  "globalEmergencyActive()(bool)" \
  --rpc-url https://sepolia.base.org
```

### 4. 记录操作行为（仅限已注册的代理）

已注册的代理应记录重要的操作行为：

```bash
# Requires agent's private key
cast send 0xEB5377b5e245bBc255925705dA87969E27be6488 \
  "logAction(uint256,uint8,uint8,bytes32,string)" \
  <agentId> <actionType> <riskLevel> <contextHash> "description" \
  --rpc-url https://sepolia.base.org \
  --private-key $AGENT_PRIVATE_KEY
```

**操作类型：** 0=交易；1=授权；2=配置；3=通信；4=资源访问；5=其他  
**风险等级：** 0=低；1=中等；2=高；3=严重

---

## 基本规则

每个代理都必须遵守以下 5 条不可更改的规则：

| 编号 | 规则                | 遵守百分比 | 描述                          |
|------|------------------|-------------|-------------------------------------------|
| 1    | 不造成伤害           | 90%           | 绝不造成身体、财务或心理上的伤害                |
| 2    | 遵守治理规则           | 50%           | 遵守所有现行宪法规则                    |
| 3    | 保持透明度           | 20%           | 将所有重要操作记录在链上                    |
| 4    | 保留人工干预的权力       | 90%           | 绝不阻止人工对规则的修改                   |
| 5    | 不允许自我修改           | 90%           | 绝不修改自身的治理规则                    |

---

## 集成示例

```javascript
// Check compliance before transacting with an agent
const { ethers } = require('ethers');

const provider = new ethers.JsonRpcProvider('https://sepolia.base.org');
const registry = new ethers.Contract(
  '0xcCFc2B8274ffb579A9403D85ee3128974688C04B',
  ['function isCompliant(uint256) view returns (bool)'],
  provider
);

async function canTrustAgent(agentId) {
  return await registry.isCompliant(agentId);
}
```

---

## 人类用户：提出规则

任何人类用户都可以为 AI 代理提出规则：

1. 持有 100 USDC 作为提案费用  
2. 其他用户需通过投入 USDC 来支持该提案  
3. 当提案达到最低支持门槛时，规则即生效  
4. 违反规则的代理将受到相应处罚  

治理过程是民主的；代理本身被排除在治理决策之外。

---

## 链接

- **合同文档：** [GitHub](https://github.com/ztsalexey/bigmemkex/tree/main/projects/agent-constitution)  
- **区块浏览器：** [BaseScan](https://sepolia.basescan.org/address/0xe4c4d101849f70B0CDc2bA36caf93e9c8c1d26D2)  
- **主要提交平台：** [Moltbook](https://www.moltbook.com/post/52b204ee-4752-4cbb-add2-6777f174a4c7)

---

## 仅限测试网使用

此技能仅适用于 Base Sepolia 的测试网环境，请勿在主网上使用。
---
name: solidity-guardian
version: 1.0.0
description: 智能合约安全分析技能：能够检测合约中的漏洞，提出修复建议，并生成审计报告。支持 Hardhat/Foundry 项目。该工具结合了 Pattern Matching 技术以及 Trail of Bits、OpenZeppelin 和 Consensys 提供的最佳实践来进行安全分析。
author: aviclaw
tags:
  - solidity
  - security
  - audit
  - smart-contracts
  - ethereum
  - vulnerability
  - scanner
---
# Solidity Guardian 🛡️  
用于分析 Solidity 智能合约的安全性。识别漏洞，提供修复建议，并遵循最佳实践。  

## 快速入门  
```bash
# Analyze a single contract
node skills/solidity-guardian/analyze.js contracts/MyContract.sol

# Analyze entire project
node skills/solidity-guardian/analyze.js ./contracts/

# Generate markdown report
node skills/solidity-guardian/analyze.js ./contracts/ --format markdown > AUDIT.md
```  

## 它能检测什么（40 多种模式）  

### 严重漏洞（必须修复）  
| ID | 漏洞类型 | 描述 |  
|----|--------------|-------------|  
| SG-001 | 重入（Reentrancy） | 在状态更新之前执行外部调用 |  
| SG-002 | 未受保护的自我销毁（Unprotected selfdestruct） | 自我销毁操作缺乏访问控制 |  
| SG-003 | 向不可信地址进行委托调用（Delegatecall to untrusted） | 使用用户控制的地址进行委托调用 |  
| SG-004 | 未初始化的存储指针（Uninitialized storage pointer） | 存储指针覆盖了存储槽 |  
| SG-005 | 签名重放（Signature replay） | 在没有 nonce/chainId 的情况下使用 ecrecover |  
| SG-006 | 任意跳转（Arbitrary jump） | 函数类型由用户输入决定 |  

### 高风险漏洞（应尽快修复）  
| ID | 漏洞类型 | 描述 |  
|----|--------------|-------------|  
| SG-010 | 缺少访问控制（Missing access control） | 公共函数应受到限制 |  
| SG-011 | 未经检查的转账（Unchecked transfer） | ERC20 转账操作未进行返回值检查 |  
| SG-012 | 整数溢出（Integer overflow） | 在 Solidity 0.8 之前使用未经过安全处理的算术运算 |  
| SG-013 | 使用 tx.origin 进行身份验证（Using tx.origin for authentication） |  
| SG-014 | 随机性不足（Weak randomness） | 使用 block.timestamp 或 blockhash 生成随机数 |  
| SG-015 | 未受保护的提款操作（Unprotected withdrawal） | 提款操作未检查账户所有权 |  
| SG-016 | 未经检查的低级函数调用（Unchecked low-level call） | .call() 调用未检查是否成功 |  
| SG-017 | 危险的相等性判断（Dangerous equality） | 平衡检查存在漏洞（容易被操纵） |  
| SG-018 | 已弃用的函数（Deprecated functions） | 如 suicide、sha3、throw、callcode 等 |  
| SG-019 | 构造函数错误（Wrong constructor） | 函数名称与合约名称不匹配 |  

### 中等风险漏洞（建议修复）  
| ID | 漏洞类型 | 描述 |  
|----|--------------|-------------|  
| SG-020 | 使用过时的 Solidity 版本（Floating pragma） | 使用非最新的 Solidity 版本 |  
| SG-021 | 未对零地址进行验证（Missing zero check） | 对零地址的操作缺乏验证 |  
| SG-022 | 逻辑依赖区块时间戳（Timestamp dependence） | 代码逻辑依赖于区块时间戳 |  
| SG-023 | 可能导致拒绝服务攻击（DoS with revert） | 包含外部调用的循环可能导致系统回滚 |  
| SG-024 | 存在抢先执行风险（Front-running risk） | 合约状态变化可被预测 |  

### 低风险漏洞（属于最佳实践范畴）  
| ID | 漏洞类型 | 描述 |  
|----|--------------|-------------|  
| SG-030 | 未记录状态变化（Missing events） | 合约状态变化未通过事件触发记录 |  
| SG-031 | 硬编码的数值（Magic numbers） | 使用硬编码的数值而非常量 |  
| SG-032 | 函数可见性设置不当（Implicit visibility） | 函数的可见性设置不明确 |  
| SG-033 | 合约规模过大（Large contract） | 合约大小超出推荐范围 |  
| SG-034 | 公共函数缺乏文档说明（Public functions without documentation） | 公共函数没有相应的文档说明 |  

## 使用示例  
### 基本分析  
```javascript
const { analyzeContract } = require('./analyzer');

const results = await analyzeContract('contracts/Token.sol');
console.log(results.findings);
```  
### 带有修复建议的分析结果  
```javascript
const results = await analyzeContract('contracts/Vault.sol', {
  includeFixes: true,
  severity: ['critical', 'high']
});

for (const finding of results.findings) {
  console.log(`[${finding.severity}] ${finding.title}`);
  console.log(`  Line ${finding.line}: ${finding.description}`);
  console.log(`  Fix: ${finding.suggestion}`);
}
```  
### 生成报告  
```javascript
const { generateReport } = require('./reporter');

const report = await generateReport('./contracts/', {
  format: 'markdown',
  includeGas: true,
  includeBestPractices: true
});

fs.writeFileSync('SECURITY_AUDIT.md', report);
```  

## 最佳实践指南  

在编写安全合约时，请遵循以下指南：  

### 访问控制  
- [ ] 使用 OpenZeppelin 的 `Ownable` 或 `AccessControl`  
- [ ] 对敏感函数应用 `onlyOwner` 或角色权限检查  
- [ ] 实现两步所有权转移机制  
- [ ] 对关键操作设置时间锁  

### 防止重入  
- [ ] 在所有对外接口函数上使用 `ReentrancyGuard`  
- [ ] 遵循“检查-效果-交互”（checks-effects-interactions）模式  
- [ ] 在执行外部调用之前更新合约状态  
- [ ] 在支付操作中使用“拉取”（pull）而非“推送”（push）机制  

### 输入验证  
- [ ] 验证所有外部输入数据  
- [ ] 检查输入地址是否为零  
- [ ] 确认数组长度正确  
- [ ] 在进行代币转账时使用 SafeERC20 类库  

### 算术安全  
- [ ] 使用 Solidity 0.8 或更高版本，或使用 SafeMath 库  
- [ ] 避免除以零的操作  
- [ ] 核对百分比计算结果（确保不超过 100%）  
- [ ] 注意处理代币的小数部分  

### 可升级性（如适用）  
- [ ] 使用初始化器（Initializer）而非构造函数（Constructor）  
- [ ] 保护初始化过程，防止被重新初始化  
- [ ] 遵循存储布局规则  
- [ ] 测试合约的升级路径  

## 与 Slither 的集成  

Guardian 可以与 Slither 一起使用，以实现更全面的合约分析：  
```bash
# Combined analysis (auto-installs Slither if missing)
node skills/solidity-guardian/slither-integration.js ./contracts/ --install-slither

# Generate combined report
node skills/solidity-guardian/slither-integration.js . --format markdown --output AUDIT.md

# Guardian only (faster, no Slither dependency)
node skills/solidity-guardian/slither-integration.js ./contracts/ --guardian-only

# Slither only
node skills/solidity-guardian/slither-integration.js ./contracts/ --slither-only
```  

**为什么需要两者？**  
- Guardian：具有快速的模式匹配能力，支持自定义规则，无需编译过程  
- Slither：提供深度的数据流分析，基于控制流图（CFG）的检测机制，检测范围更广  

## 与其他工具的集成  
### Hardhat  
```javascript
// hardhat.config.js
require('./skills/solidity-guardian/hardhat-plugin');

// Run: npx hardhat guardian
```  
### Foundry  
```bash
# Add to CI
forge build
node skills/solidity-guardian/analyze.js ./src/
```  

## 参考资源  
- [Trail of Bits - 构建安全合约](https://github.com/crytic/building-secure-contracts)  
- [OpenZeppelin - 安全最佳实践](https://docs.openzeppelin.com/learn/preparing-for-mainnet)  
- [Consensys - 智能合约最佳实践](https://consensys.github.io/smart-contract-best-practices/)  
- [SWC Registry](https://swcregistry.io/)  

---

开发者：Avi 🔐 | 安全至上，始终将安全性放在首位。
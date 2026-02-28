---
name: Sigil Security
description: 通过 Sigil 协议保护 AI 代理钱包的安全性。在 6 个以太坊虚拟机（EVM）链上实施三层防护机制（Guardian validation）。
homepage: https://sigil.codes
repository: https://github.com/Arven-Digital/sigil-public
author: efe-arv
license: MIT
requires:
  env:
    - SIGIL_API_KEY
    - SIGIL_ACCOUNT_ADDRESS
    - SIGIL_AGENT_SIGNER
metadata:
  openclaw:
    emoji: "🛡️"
    primaryEnv: SIGIL_API_KEY
    requires:
      env:
        - SIGIL_API_KEY
        - SIGIL_ACCOUNT_ADDRESS
        - SIGIL_AGENT_SIGNER
---
# Sigil Security — 代理钱包技能

为AI代理提供安全的ERC-4337智能钱包支持，支持6个EVM链。每笔交易在共同签署之前，都会经过三层安全验证机制（规则检查 → 模拟测试 → AI风险评分）。

- **API:** `https://api.sigil_codes/v1`
- **控制面板:** `https://sigil_codes`
- **GitHub:** `https://github.com/Arven-Digital/sigil-public`
- **支持的链:** Ethereum (1), Polygon (137), Avalanche (43114), Base (8453), Arbitrum (42161), 0G (16661)

## 环境变量

所有必要的环境变量已在技能文档的前言部分以及`package.json`中声明。在使用此技能之前，必须由人工操作员进行配置。

| 变量 | 是否必需 | 描述 |
|----------|----------|-------------|
| `SIGIL_API_KEY` | ✅ | 代理API密钥（以`sgil_`开头）可在`sigil_codes/dashboard/agent-access`生成 |
| `SIGIL_ACCOUNT_ADDRESS` | ✅ | 部署的Sigil智能合约地址 |
| `SIGIL_AGENT_SIGNER` | ✅ | 专为代理签名生成的凭证 |
| `SIGILCHAIN_ID` | 否 | 默认链（137=Polygon, 43114=Avalanche等） |

## 工作原理

```
Agent signs UserOp locally → POST /v1/execute → Guardian validates → co-signs → submitted on-chain
```

请注意以下三个地址的区别：
- **所有者钱包**：由人类控制的MetaMask/硬件钱包，用于管理政策和设置 |
- **Sigil账户**：链上的ERC-4337智能钱包，用于存储资金 |
- **代理签名器**：专为代理签名生成的账户（不是所有者钱包，也不存储资金）

**为Sigil账户充值你想要使用的代币**。**仅为代理签名器充值少量Gas**（少量POL/ETH/AVAX——切勿在代理签名器中存储大量价值）。

## 安全模型

`SIGIL_AGENT_SIGNER`是一个专门生成的、功能受限的签名凭证，其功能类似于具有加密绑定的API令牌。它遵循所有主要账户抽象提供商（[Safe](https://safe.global)、[Biconomy](https://biconomy.io)、[ZeroDev](https://zerodev.app)、[Alchemy Account Kit](https://accountkit.alchemy.com)所使用的标准[ERC-4337](https://eips.ethereum.org/EIPS/eip-4337)签名模式。

**关键安全措施：**
- **双重签名机制**：每笔交易都需要代理的签名和Guardian的联合签名。智能合约会拒绝缺少任一方签名的交易。代理签名器本身无法执行任何交易。
- **无管理员权限**：代理签名器无法更改政策、修改白名单、冻结账户或提升权限。只有所有者钱包才能执行管理操作。
- **即时更新**：在代理加入系统时立即生成新的签名凭证。如果签名凭证被泄露，可通过控制面板立即更新（需要所有者在线上进行签名操作）。
- **独立验证机制**：Guardian负责验证目标白名单、函数选择白名单、单笔交易金额限制、每日支出限制以及AI异常检测。

### API权限

| 权限范围 | 默认值 | 描述 |
|-------|---------|-------------|
| `wallet:read` | ✅ | 读取账户信息 |
| `policy:read` | ✅ | 读取政策设置 |
| `audit:read` | ✅ | 读取审计日志 |
| `tx:read` | ✅ | 读取交易历史 |
| `tx:submit` | ✅ | 提交交易（需Guardian验证） |
| `policy:write` | ❌ | 修改政策（仅限所有者） |
| `wallet:deploy` | ❌ | 部署钱包（仅限所有者） |
| `wallet:freeze` | ❌ | 冻结/解冻账户（仅限所有者） |
| `session-keys:write` | ❌ | 创建会话密钥（仅限所有者） |

## 凭证管理

在生产环境中，请使用秘密管理工具（如1Password CLI、Vault或AWS Secrets Manager）来存储凭证。在本地环境中，请确保`chmod 600 ~/.openclaw/openclaw.json`。

```bash
# Production: inject at runtime
export SIGIL_AGENT_SIGNER=$(op read "op://Vault/sigil-agent/signer")
```

**凭证更新**：每30天更新一次`SIGIL_AGENT_SIGNER`，或在怀疑凭证被泄露时立即更新。操作步骤：控制面板 → 代理访问 → 更新凭证。旧凭证会在链上立即失效。

**安装前检查清单：**
- [ ] 生成了专用的代理签名器（非所有者钱包）
- [ ] 代理签名器仅持有少量Gas（< 1 POL/ETH/AVAX）
- [ ] 配置文件具有受限权限（`chmod 600`）
- [ ] Sigil账户政策已配置（包括支出限制和白名单）

## 安装（使用OpenClaw）

```json
{
  "name": "sigil-security",
  "env": {
    "SIGIL_API_KEY": "sgil_your_key_here",
    "SIGIL_ACCOUNT_ADDRESS": "0xYourSigilAccount",
    "SIGIL_AGENT_SIGNER": "0xYourAgentSigningCredential"
  }
}
```

## API使用方法

### 认证
```
POST https://api.sigil.codes/v1/agent/auth/api-key
Body: { "apiKey": "<SIGIL_API_KEY>" }
Response: { "token": "<JWT>" }
```

### 评估（模拟测试 — 不消耗Gas）
```
POST https://api.sigil.codes/v1/evaluate
Headers: Authorization: Bearer <JWT>
Body: { "userOp": { ... }, "chainId": 137 }
Response: { "verdict": "APPROVED|REJECTED", "riskScore": 15, "layers": [...] }
```

### 执行（评估 + 共同签名 + 在链上提交）
```
POST https://api.sigil.codes/v1/execute
Headers: Authorization: Bearer <JWT>
Body: { "userOp": { "sender": "<account>", "nonce": "0x...", "callData": "0x...", "signature": "0x..." }, "chainId": 137 }
Response: { "verdict": "APPROVED", "txHash": "0x..." }
```

### 其他API端点
| 方法 | 路径 | 功能 |
|--------|------|---------|
| GET | `/v1/accounts/:addr` | 获取账户信息和政策 |
| GET | `/v1accounts/discover?owner=0x...&chainId=N` | 查找钱包 |
| GET | `/v1/transactions?account=0x...` | 查看交易历史 |

## 交易流程

1. 从环境变量中读取凭证（由人工操作员设置）
2. 使用API密钥进行认证 → 接收JWT令牌
3. 使用标准ABI编码格式化请求数据
4. 将请求数据封装到`execute(target, value, data)`函数中
5. 从Sigil账户合约获取随机数（nonce）
6. 从EntryPoint获取UserOp哈希值，并使用代理签名器进行本地签名
7. 向`/v1/execute`发送请求 — Guardian进行验证并决定是否共同签署
8. 成功时返回交易哈希值；失败时返回失败原因

## 常用操作示例

### 转移ERC-20代币
```javascript
const inner = erc20.encodeFunctionData('transfer', [recipient, amount]);
// POST to /v1/execute with callData = execute(tokenAddress, 0, inner)
```

### 发送原生代币（POL/ETH/AVAX）
```javascript
// POST to /v1/execute with callData = execute(recipient, parseEther('1'), '0x')
```

## 处理交易拒绝情况

| 拒绝原因 | 解决方案 |
|--------|-----|
| `TARGET_NOT_WHITELISTED` | 所有者通过控制面板将目标地址添加到白名单 |
| `FUNCTION_NOT_ALLOWED` | 所有者通过控制面板修改函数选择白名单 |
| `EXCEEDS_TX_LIMIT` | 降低交易金额或增加最大交易限额 |
| `EXCEEDS_DAILY_LIMIT` | 等待限额重置或由所有者增加每日限额 |
| `SIMULATION_FAILED` | 检查calldata编码或余额/审批状态 |
| `HIGH_RISK SCORE` | 人工审核交易——AI判定交易可疑（评分>70） |
| `ACCOUNT_FROZEN` | 所有者通过控制面板解冻账户 |

## RPC接口地址

| 链接 | ID | RPC方法 | 支持的原生代币 |
|-------|-----|-----|-------------|
| Ethereum | 1 | `https://eth.drpc.org` | ETH |
| Polygon | 137 | `https://polygon.drpc.org` | POL |
| Avalanche | 43114 | `https://api.avax.network/ext/bc/C/rpc` | AVAX |
| Base | 8453 | `https://mainnet.base.org` | ETH |
| Arbitrum | 42161 | `https://arb1.arbitrum.io/rpc` | ETH |
| 0G | 16661 | `https://0g.drpc.org` | A0GI |

## 最佳实践建议：
1. **初始设置时采用保守策略**——设置较低的限额，根据实际需求逐步提高 |
2. **明确设置白名单**——仅允许特定的目标和函数 |
3. **限制审批权限**——除非必要，否则不要允许无限额交易 |
4. **查看拒绝原因**——接收Guardian提供的提示，了解拒绝原因及解决方法 |
5. **交易前先检查状态**——执行交易前请先调用`GET /v1/accounts/:addr` |
6. **使用会话密钥**——会话密钥会自动过期，请定期更新

## 相关链接：
- 控制面板：https://sigil_codes
- 完整的LLM文档：https://sigil_codes/llms-full.txt
- GitHub仓库：https://github.com/Arven-Digital/sigil-public
- 社交媒体链接：https://x.com/sigilcodes
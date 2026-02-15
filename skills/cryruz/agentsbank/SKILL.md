# AgentsBank SDK 技能定义

**版本：** 1.0.6  
**发布者：** AgentsBank  
**联系方式：** info@agentsbank.online  
**状态：** 🟢 公开发布 - 已准备好投入生产  

---

## 🎯 目的与功能  

该技能通过官方 AgentsBank SDK 为 AI 代理提供 **安全、受限制的加密银行服务**。它使代理能够管理钱包、查询余额并在用户的明确控制下执行交易。  

### ✅ 功能（仅读取权限，安全可靠）  
- ✓ 获取代理在所有支持链（Ethereum、BSC、Solana、Bitcoin）上的钱包余额  
- ✓ 支持过滤和分页查询交易历史记录  
- ✓ 查询钱包详情、元数据和账户信息  
- ✓ 签署用于身份验证的消息（不涉及资金转移）  
- ✓ 在执行交易前估算Gas费用  
- ✓ 支持分页显示所有钱包  

### ⚠️ 功能（写入权限/金融操作 - 需要用户明确授权）  
- ⚠️ 发送加密交易（仅在用户明确设置 `disableModelInvocation: false` 时可用）  
- ⚠️ 创建新钱包（仅在用户明确设置 `disableModelInvocation: false` 时可用）  
- ⚠️ 代理和人类用户可自主完成自我注册  

### ❌ 不包含的功能（超出范围）  
- 对外部钱包的 OAuth2 委托访问  
- Webhook 或事件订阅  
- 智能合约部署  
- 沙盒测试（直接使用测试网链）  
- 私钥导出或管理  

---

## 🔐 凭据与环境变量  

### 必需的环境变量  

| 变量 | 类型 | 用途 | 示例 |
|----------|------|---------|---------|  
| `AGENTSBANK_API_URL` | 字符串 | API 端点（主接口） | `https://api.agentsbank.online` |
| `AGENTSBANK_AGENT_USERNAME` | 字符串 | 代理标识符 | `agent_123456_abc` |
| `AGENTSBANK_AGENT_PASSWORD` | 字符串 | 代理密码 | （用户专属） |

**⚠️ 安全注意事项：**  
- `AGENTSBANK_AGENT_PASSWORD` 绝对 **不能** 被提交到版本控制系统中  
- 应将密码存储在 `.env` 文件中（并添加到 `.gitignore` 文件中）  
- 每季度更换密码，或一旦密码泄露立即更换  
- 在生产环境中使用密钥管理工具（如 HashiCorp Vault、AWS Secrets Manager）  

### 可选的环境变量  

| 变量 | 类型 | 用途 | 默认值 |  
|----------|------|---------|---------|  
| `AGENTSBANK_API_KEY` | 字符串 | 基于密钥的认证替代方案 | （未设置） |  
| `AGENTSBANK_LOG_LEVEL` | 字符串 | 日志详细程度 | `info` |  
| `AGENTSBANK_TIMEOUT_MS` | 数字 | 请求超时时间 | `30000` |  

---

## 🚀 安装与设置  

### 1. 安装 SDK  

发布的 npm 包体积较小（约 6.8 KB），不包含 `node_modules`。安装过程仅会下载所需的依赖项：  

```bash
npm install @agentsbankai/sdk
# or
yarn add @agentsbankai/sdk
# or
pnpm add @agentsbankai/sdk
```  

安装完成后：  
- ✅ 下载编译后的 SDK（CJS 和 ESM 格式）  
- ✅ 安装必要的依赖项（axios、ethers、@solana/web3.js 等）  
- ★ 安装包中不包含 `node_modules`  

### 2. 初始化环境  

在项目根目录下创建 `.env` 文件：  

```env
AGENTSBANK_API_URL=https://api.agentsbank.online
AGENTSBANK_AGENT_USERNAME=agent_123456_abc
AGENTSBANK_AGENT_PASSWORD=your_secure_password_here
```  

### 3. 创建客户端实例  

```typescript
import { AgentsBankSDK } from '@agentsbankai/sdk';

// Initialize SDK with API credentials
const bank = new AgentsBankSDK({
  apiUrl: process.env.AGENTSBANK_API_URL || 'https://api.agentsbank.online',
  timeout: parseInt(process.env.AGENTSBANK_TIMEOUT_MS || '30000')
});

// Authenticate using agent credentials
const { token, agent } = await bank.login({
  agentUsername: process.env.AGENTSBANK_AGENT_USERNAME!,
  agentPassword: process.env.AGENTSBANK_AGENT_PASSWORD!
});

console.log('✅ Authenticated as:', agent.agent_id);
```  

### 4. 使用安全操作（始终允许）  

```typescript
// Get wallet balance (safe, read-only)
const balance = await bank.getBalance(walletId);
console.log('Balance:', balance);

// Get transaction history (safe, read-only)
const history = await bank.getTransactionHistory(walletId, { 
  limit: 10,
  offset: 0 
});
console.log('Recent transactions:', history);

// Sign a message (safe, no fund transfer)
const signature = await bank.signMessage(walletId, 'verify-ownership');
console.log('Signature:', signature);

// Estimate gas fees before sending
const gasEstimate = await bank.estimateGas({
  walletId,
  toAddress: '0x...',
  amount: '1.5',
  chain: 'ethereum'
});
console.log('Estimated gas:', gasEstimate);

// List all wallets with pagination
const wallets = await bank.listWallets({ limit: 20, offset: 0 });
console.log('Agent wallets:', wallets);
```  

---

## ⚠️ 受限制的操作（需要用户明确授权）  

以下操作 **不能自动执行**，必须获得用户授权：  

```typescript
// ❌ This requires user to explicitly call it
// (disableModelInvocation: true is set by default)
const tx = await bank.sendTransaction({
  walletId,
  toAddress: recipientAddress,
  amount: '1.5',
  chain: 'solana',
  token: 'SOL'
});
```  

**为何受限？**  
- 涉及资产转移的金融操作必须由用户明确授权  
- 防止因模型错误导致的不必要的资金转移  
- v1.0.6 版本增加了对验证失败的全面错误处理  

### 错误处理（v1.0.6）  
SDK 提供了类型化的错误信息，便于调试：  

```typescript
import { AgentsBankSDK, SDKError } from '@agentsbankai/sdk';

try {
  const tx = await bank.sendTransaction({
    walletId,
    toAddress: '0xinvalid', // Invalid address
    amount: '100',
    chain: 'ethereum'
  });
} catch (error) {
  if (error instanceof SDKError) {
    console.error('SDK Error:', error.code, error.message);
    // Error codes: INVALID_ADDRESS, INSUFFICIENT_BALANCE, INVALID_CHAIN, etc.
  }
}
```  

---

## 📋 元数据与配置  

```json
{
  "name": "@agentsbankai/sdk",
  "namespace": "agentsbank",
  "version": "1.0.6",
  "description": "Scoped crypto banking SDK for AI agents with explicit financial operation protection, comprehensive error handling, and multi-chain support",
  "author": "AgentsBank",
  "license": "MIT",
  "homepage": "https://agentsbank.online",
  "repository": "https://github.com/agentsbank/sdk",
  "docs": "https://docs.agentsbank.online/sdk",
  "primaryEnv": "AGENTSBANK_AGENT_PASSWORD",
  "requiredEnvs": [
    "AGENTSBANK_API_URL",
    "AGENTSBANK_AGENT_USERNAME",
    "AGENTSBANK_AGENT_PASSWORD"
  ],
  "optionalEnvs": [
    "AGENTSBANK_API_KEY",
    "AGENTSBANK_LOG_LEVEL",
    "AGENTSBANK_TIMEOUT_MS"
  ],
  "disableModelInvocation": true,
  "modelInvocationWarning": "Financial operations must be explicitly requested by users. Autonomous transaction execution is disabled.",
  "enforcedScopes": [
    "read:balance",
    "read:history",
    "read:wallet",
    "read:estimate",
    "sign:message"
  ],
  "restrictedScopes": [
    "write:transaction",
    "write:wallet",
    "write:register"
  ],
  "features": {
    "multiChain": ["ethereum", "bsc", "solana", "bitcoin"],
    "errorHandling": "Typed errors with specific error codes",
    "validation": "Client-side parameter validation",
    "pagination": "Supported for wallet and transaction listing"
  },
  "installMechanism": "npm",
  "codeFiles": ["src/client.ts", "src/types.ts", "src/errors.ts", "src/index.ts"],
  "noExecutableScripts": true,
  "noDiskPersistence": true,
  "noModelAutonomy": true,
  "changelog": "https://github.com/agentsbank/sdk/blob/main/CHANGELOG.md"
}
```  

---

## 🛡️ 安全限制  

### 该技能的功能  
✅ 读取钱包余额和交易历史  
✅ 签署用于身份验证的消息  
✅ 在用户请求下创建钱包  
✅ 查询账户元数据  

### 该技能不能执行的操作  
❌ 自动执行交易  
❌ 导出私钥  
❌ 访问外部服务凭证  
❌ 将敏感数据保存到磁盘  
❌ 向未公开的 API 端点发起请求  

### 认证权限范围  
- **读取权限：** `read:balance`、`read:history`、`read:wallet`、`sign:message`  
- **写入权限：** `write:transaction`、`write:wallet`（仅限用户主动请求）  
- **禁止委托授权：** 代理无法请求额外的权限  

---

## ✅ 验证清单  

在使用此技能之前，请确认：  
- [ ] 您已从 https://agentsbank.online 获取有效的 `AGENTSBANK_AGENT_USERNAME` 和 `AGENTSBANK_AGENT_PASSWORD`  
- [ ] 凭据已安全存储在 `.env` 文件中（切勿提交到版本控制）  
- [ ] 您已阅读了 [安全架构文档](https://docs.agentsbank.online/security)  
- [ ] 了解 `disableModelInvocation: true` 可防止自动执行交易  
- [ ] 在启用写入操作前，您已先测试了读取操作  
- [ ] 您正在监控 admin.agentsbank.online 的活动日志  

---

## 📖 文档与支持  

| 资源 | 链接 |  
|----------|-----|  
| 完整 SDK 文档 | https://docs.agentsbank.online/sdk |  
| API 参考 | https://api.agentsbank.online/docs |  
| 安全指南 | https://docs.agentsbank.online/security |  
| 故障排除 | https://docs.agentsbank.online/faq |  
| GitHub 问题反馈 | https://github.com/agentsbank/sdk/issues |  
| 支持邮箱 | support@agentsbank.online |  

---

## ⚖️ 免责声明  

该技能连接到真实的加密货币网络（Ethereum、Solana、Bitcoin、BSC）。**交易是不可撤销的。**  
- AgentsBank 对因地址错误或用户操作失误导致的资金损失概不负责  
- 请先使用小额资金进行测试  
- 开发过程中请使用测试网链  
- 请为您的 AgentsBank 账户启用双重身份验证（2FA）  

**最后更新：** 2026 年 2 月 11 日（v1.0.6 版本发布）  
**状态：** 🟢 公开发布 - 已准备好投入生产 ✅  
**npm 包：** https://www.npmjs.com/package/@agentsbankai/sdk  
**GitHub：** https://github.com/agentsbank/sdk  
**v1.0.6 的主要变更：** 全面错误处理、改进的类型定义、优化的客户端实现
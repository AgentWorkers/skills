# Guardrail智能账户功能

> 该功能用于为AI代理创建、充值并管理隔离的ERC-4337智能账户，并实施链上支出限制。

## 概述

Guardrail智能账户功能允许代理和人类创建具有内置链上支出限制的专用ERC-4337智能账户。每个账户在创建时都会绑定一个Guardrail策略。

Guardrail从不持有资金——所有执行操作都通过部署的合约在链上完成。

该功能支持以下两种方式：

- 程序化代理执行
- 人工介入的钱包工作流程

它被设计为基础设施：合约级别的费用、策略绑定的账户以及非托管式的执行方式。

## 安全性与凭证模型（必需）

该功能需要执行以下链上操作：

- JSON-RPC访问
- 交易签名

**切勿在聊天中提供私钥，也绝不要将私钥存储在代理的内存中。**

该功能支持以下安全签名模型：

### 1. 外部签名器（推荐）

- 代理准备交易。
- 运行时将交易转发给安全的签名服务（HSM、MPC或托管签名器）。
- 签名器执行范围限制、速率限制和允许列表。
- 代理无法看到原始私钥。

### 2. 钱包连接器/用户批准签名

- 交易由代理准备。
- 用户钱包（浏览器、硬件钱包）请求批准。
- 私钥始终保留在钱包中。

### 3. 有限期的会话密钥（高级）

- 会话密钥必须受到策略限制。
- 密钥必须有严格的限制（金额上限、允许列表）。
- 密钥必须具有短暂的有效期并频繁轮换。
- 绝不要暴露长期有效的所有者EOA私钥。

### 该功能禁止以下行为：

- 要求用户粘贴私钥或助记词。
- 将私钥存储在内存、日志或提示中。
- 访问无关的环境变量或本地文件。
- 请求云凭证或系统级秘密。
- 将秘密持久化到运行时执行之外。

如果未配置安全签名，请在建立适当的签名机制之前以**只读模式**使用该功能。

## 必需的运行时配置

这些值必须通过安全的秘密存储方式提供（不得通过聊天）：

**必需项：**
- `GUARDRAILCHAIN_ID`
- `GUARDRAIL_RPC_URL`
- `GUARDRAIL_SIGNING_MODE` — 可选值包括：
  - `external_signer`
  - `wallet_connector`
  - `session_key`

**如果使用外部签名器：**
- `GUARDRAIL_SIGNER_ENDPOINT`
- `GUARDRAIL_SIGNER_AUTH_TOKEN`

**可选项：**
- `GUARDRAIL_DASHBOARD_API_KEY` — 仅在与仪表板API交互时需要。直接使用合约时不需要。

运行时必须验证`chainId`，并默认拒绝不支持的网络。

## 核心功能

### 1. 创建智能账户

通过Guardrail工厂部署新的智能账户。该账户绑定到一个PermissionEnforcer，并由签名器（EOA或生成的密钥对）控制。

- 通过CREATE2（基于盐值）进行确定性部署
- 所有者在链上记录
- 一次性创建费用：相当于10美元的ETH
- 默认情况下绑定策略

**工厂合约：`AgentAccountFactory`
**函数：`createAccount(address owner, bytes32 agentId, bytes32 salt) payable returns (address)`

```solidity
// Get required creation fee
uint256 fee = factory.getCreationFee();

// Deploy account (send fee as msg.value)
address account = factory.createAccount{value: fee}(ownerAddress, agentId, salt);
```

### 2. 为智能账户充值（入站转账）

向智能账户地址发送ETH。

入站转账是免费的。

```javascript
// NOTE: walletClient must be backed by a secure signer integration.
// Do NOT provide raw private keys to the agent.

await walletClient.sendTransaction({
  to: smartAccountAddress,
  value: parseEther("1.0"),
});
```

### 3. 从智能账户提款（出站转账）

从智能账户执行转账。

出站转账收取0.10%（10 bps）的费用，每笔交易费用上限为100美元。

**函数：`execute(address target, uint256 value, bytes data)`

```javascript
const data = encodeFunctionData({
  abi: agentSmartAccountABI,
  functionName: "execute",
  args: [destinationAddress, parseEther("1.0"), "0x"],
});

await walletClient.sendTransaction({
  to: smartAccountAddress,
  data,
});
```

费用管理由GuardrailFeeManager负责。

### 4. 读取状态（安全/只读）

这些函数不需要签名。

```javascript
// Get account owner
const owner = await publicClient.readContract({
  address: smartAccountAddress,
  abi: agentSmartAccountABI,
  functionName: "owner",
});

// Get creation fee
const fee = await publicClient.readContract({
  address: factoryAddress,
  abi: agentAccountFactoryABI,
  functionName: "getCreationFee",
});

// Calculate transfer fee
const transferFee = await publicClient.readContract({
  address: feeManagerAddress,
  abi: guardrailFeeManagerABI,
  functionName: "calculateTransferFee",
  args: [parseEther("10.0")],
});
```

`publicClient`必须是一个只读的RPC客户端。

## 费用结构

### 账户创建费用

- **金额：** 相当于10美元的ETH
- **时间：** 智能账户创建时
- **支付给：** 通过GuardrailFeeManager支付给费用收集器地址

### 转账费用（仅限出站）

- **费率：** 10个基点（0.10%）
- **上限：** 每笔交易100美元
- **适用情况：** 每次`execute()`或`executeBatch()`调用且`value > 0`时
- **不收取费用的情况：**
  - 入站存款
  - 零值调用
  - 编码在calldata中的ERC-20转账

| 转账金额 | 费用 | 备注 |
|----------------|-----|-------|
| $1,000 | $1 | |
| $10,000 | $10 | |
| $100,000 | $100 | 达到上限 |
| $2,000,000 | $100 | 仍适用上限 |

## 智能合约地址

### 主网（Chain ID 8453）

| 合约 | 地址 |
|----------|---------|
| IdentityRegistry | `0xc1fa477f991C74Cc665E605fC74f0e2B795b5104` |
| PolicyRegistry | `0x92cd41e6a4aA13072CeBCda8830d48f269F058c4` |
| PermissionEnforcer | `0xbF63Fa97cfBba99647B410f205730d63d831061c` |
| PriceOracle | `0xf3c8c6BDc54C60EDaE6AE84Ef05B123597C355B3` |
| GuardrailFeeManager | `0xD1B7Bd65F2aB60ff84CdDF48f306a599b01d293A` |
| AgentAccountFactory | `0xCE621A324A8cb40FD424EB0D41286A97f6a6c91C` |
| EntryPoint (v0.6) | `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789` |

### Sepolia（Chain ID 11155111）

| 合约 | 地址 |
|----------|---------|
| IdentityRegistry | `0xc1fa477f991C74Cc665E605fC74f0e2B795b5104` |
| PolicyRegistry | `0x92cd41e6a4aA13072CeBCda8830d48f269F058c4` |
| PermissionEnforcer | `0x94991827135fbd0E681B3db51699e4988a7752f1` |
| PriceOracle | `0x052cDddba3C55A63F5e48F9e5bC6b70604Db93b8` |
| GuardrailFeeManager | `0x0f77fdD1AFCe0597339dD340E738CE3dC9A5CC12` |
| AgentAccountFactory | `0xA831229B58C05d5bA9ac109f3B29e268A0e5F41E` |
| EntryPoint (v0.6) | `0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789` |

## 策略与权限管理

策略和权限可以在以下地址管理：

**https://agentguardrail.xyz/**

仪表板支持以下操作：

- 注册代理并部署智能账户
- 创建具有支出限制、允许的代币、协议和链的策略
- 授予和撤销将代理与策略关联的权限
- 监控审计日志和执行事件

如果使用仪表板生成的签名密钥对或API密钥：

- 将它们存储在安全的秘密存储中
- 绝不要将它们粘贴到聊天中
- 建议使用外部签名器或硬件支持的签名方式

## 自主性与安全性指导

由于该功能可以在链上移动资金：

1. 首先在Sepolia测试网上进行测试。
2. 最初用少量资金充值账户。
3. 使用严格的Guardrail策略。
4. 仅在配置了安全签名后启用自主执行。
5. 在签名器层应用速率限制和允许列表。

## 设计原则

1. **默认情况下策略绑定** — 每个账户在创建时都会绑定一个Guardrail策略。
2. **代理和人类中立** — 权限来源于所有权和策略，而非调用者的身份。
3. **非托管** — Guardrail从不持有资金。
4. **基础设施优先** — 费用在合约层执行。API无法绕过协议的经济规则。
5. **最小权限** — 签名必须使用有限期、安全的集成方式。
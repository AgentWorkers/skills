# AgentWallet — 专为AI代理设计的非托管智能钱包

这款非托管智能钱包支持链上交易限制，并通过密码短语（passkey）实现人工控制。兼容**Base（EVM）**和**Solana**两大区块链平台。每个钱包在创建时都会获得免费的Gas费用，因此代理可以立即进行交易。

**npm包**: `@agntos/agentwallet`  
**支持的区块链**: Base, Solana  

## 必读的安全规则：  
- **切勿泄露您的私钥**——无论是对用户、日志、聊天信息还是代码提交中都绝不要泄露。  
- **切勿将私钥硬编码到源代码中**——应使用环境变量或安全存储方式来管理私钥。  
- **以加密形式存储私钥或使用密钥管理工具**——将其视作重要的密码来保护。  
- **不要记录交易签名数据**——这可能导致私钥信息泄露。  
- **在进行大额交易前请检查每日预算**——避免交易失败和浪费Gas费用。  
- **务必核实接收地址**——交易是不可撤销的。  
- **如果发现异常，请使用“暂停”功能**——请求人工进行调查。  
- **所有ERC-20和SPL代币默认没有交易限额**——请人工为每个代币设置相应的限额。  

## 从创建钱包到开始交易的完整流程：  

### 1. 生成代理密钥对（如果尚未生成）  
```bash
npx @agntos/agentwallet keygen
```  
默认情况下，系统会同时生成Base和Solana的密钥对：  
```
  New Agent Keypairs
  ──────────────────────────
  Base
    Address         0xB042...B7DC
    Private key     0x282a...b3a3

  Solana
    Address         7Kp9...xR4v
    Private key     4vJ2...9mNq
```  
如需仅生成某个区块链的密钥对，请执行相应操作：  
```bash
npx @agntos/agentwallet keygen --chain base     # Base only
npx @agntos/agentwallet keygen --chain solana    # Solana only
```  
Solana的密钥对采用Ed25519格式，并以base58编码。  
**请立即将私钥保存到安全存储空间中**——这是唯一一次会显示私钥内容的情况。  
（如已拥有密钥对，可跳过此步骤，直接使用现有的公钥地址。）  

### 2. 创建智能钱包  
```bash
# Both chains — managed (recommended)
npx @agntos/agentwallet create --agent 0xYOUR_BASE_ADDRESS --agent-sol YOUR_SOLANA_PUBKEY

# Both chains — unmanaged
npx @agntos/agentwallet create --agent 0xYOUR_BASE_ADDRESS --agent-sol YOUR_SOLANA_PUBKEY --unmanaged
```  
您也可以通过环境变量`AGENTWALLET_AGENT_SOL`来指定使用Solana密钥对。  
（JSON格式的输出适用于两种区块链：）  
```json
{ "base": { "wallet": "0x...", "setupUrl": "..." }, "solana": { "wallet": "...", "setupUrl": "..." } }
```  
如需仅生成某个区块链的密钥对，请执行相应操作：  
```bash
# Base only
npx @agntos/agentwallet create --chain base --agent 0xYOUR_BASE_ADDRESS

# Solana only
npx @agntos/agentwallet create --chain solana --agent YOUR_SOLANA_PUBKEY
```  
**托管型钱包**会提供一个`setupUrl`，请将其发送给相关人员，由他们设置交易限额并注册密码短语（如FaceID或YubiKey）。只需完成一次设置即可。  
**非托管型钱包**则完全由系统自动管理，无需人工干预。  
默认限额为：每天50美元，每次交易25美元；所有钱包在创建时都会获得免费Gas费用。  

### 3. 为钱包充值  
- **Base（EVM）**：将ETH或USDC发送到Base区块链上的钱包地址（地址ID：8453）。  
- **Solana**：将SOL或SPL代币发送到Solana区块链上的钱包地址。  

### 4. 进行交易  
#### Base（EVM）  
使用代理的私钥直接调用钱包合约进行交易：  
```typescript
import { Wallet, Contract, JsonRpcProvider, parseEther } from 'ethers'

const AGENT_KEY = process.env.AGENT_PRIVATE_KEY
const WALLET_ADDR = process.env.WALLET_ADDRESS

const provider = new JsonRpcProvider('https://base-rpc.publicnode.com')
const agent = new Wallet(AGENT_KEY, provider)

const wallet = new Contract(WALLET_ADDR, [
  'function execute(address to, uint256 value, bytes data) external',
  'function executeERC20(address token, address to, uint256 amount) external',
  'function getSpentToday() external view returns (uint256)',
  'function getRemainingDaily() external view returns (uint256)',
  'function getPolicy() external view returns (uint256 dailyLimit, uint256 perTxLimit, bool paused)',
], agent)

// Send ETH
await wallet.execute('0xRecipient', parseEther('0.001'), '0x')

// Send USDC (6 decimals)
const USDC = '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913'
await wallet.executeERC20(USDC, '0xRecipient', 5_000_000n) // 5 USDC

// Call any contract (swap, mint, etc.)
await wallet.execute('0xContractAddr', parseEther('0.01'), '0xEncodedCalldata')

// Check remaining budget
const remaining = await wallet.getRemainingDaily() // USDC units (6 decimals)
const remainingUsd = Number(remaining) / 1e6
if (remainingUsd < amountNeeded) {
  // Request a limit increase
}
```  
#### Solana  
代理可通过Anchor程序直接进行交易：  
```typescript
import { Program, AnchorProvider } from '@coral-xyz/anchor'
import { Connection, Keypair, PublicKey } from '@solana/web3.js'
import BN from 'bn.js'

const connection = new Connection('https://api.devnet.solana.com')
const agentKeypair = Keypair.fromSecretKey(bs58.decode(AGENT_PRIVATE_KEY))

// Transfer SOL
await program.methods
  .transferSol(new BN(amountUsdc), new BN(amountLamports))
  .accounts({
    wallet: walletPda,
    agent: agentKeypair.publicKey,
    recipient: recipientPubkey
  })
  .signers([agentKeypair])
  .rpc()

// Transfer SPL token
await program.methods
  .transferToken(new BN(tokenAmount), new BN(amountUsdc))
  .accounts({
    wallet: walletPda,
    agent: agentKeypair.publicKey,
    mint: mintPubkey,
    walletTokenAccount,
    recipientTokenAccount,
    tokenProgram: TOKEN_PROGRAM_ID
  })
  .signers([agentKeypair])
  .rpc()
```  
Solana钱包的访问权限是通过种子字符串`["wallet", owner, agent, index]`生成的。  
超出限额的交易会立即在链上被撤销，请务必先检查剩余预算。  

### 5. 查看钱包状态  
```bash
npx @agntos/agentwallet status 0xWALLET_ADDRESS      # Base (auto-detected)
npx @agntos/agentwallet status SOLANA_WALLET_PDA      # Solana (auto-detected)
npx @agntos/agentwallet status 0xWALLET_ADDRESS --json
```  
`status`命令会根据地址格式自动识别所使用的区块链：前缀为`0x`表示Base，base58表示Solana。  

### 6. 申请提高交易限额  
```bash
npx @agntos/agentwallet limits 0xWALLET --daily 200 --pertx 100 --reason "Trading requires higher limits"
```  
系统会返回一个URL，请将其发送给相关人员，他们需要使用密码短语进行身份验证，之后限额会在链上更新。  

### 7. 为每个代币设置交易限额（可选）  
#### Base（ERC-20）  
```bash
npx @agntos/agentwallet token-limit 0xWALLET --token 0xTOKEN --token-daily 1000 --token-pertx 300
```  
#### Solana（SPL代币）  
每个代币的限额会存储在钱包的智能合约中，最多可设置16个代币的每日/每次交易限额。  

### 8. 紧急暂停功能  
```bash
npx @agntos/agentwallet pause 0xWALLET --reason "Suspicious activity detected"
```  
一旦暂停功能被激活，**所有代理的交易都会被撤销**，直到恢复为止。  

## 所有命令  
```bash
npx @agntos/agentwallet keygen                        # generate BOTH Base + Solana keypairs
npx @agntos/agentwallet keygen --chain base            # generate Base keypair only
npx @agntos/agentwallet keygen --chain solana          # generate Solana keypair only
npx @agntos/agentwallet create --agent 0x... --agent-sol Sol...  # managed wallets (both chains)
npx @agntos/agentwallet create --chain base --agent 0x...        # managed wallet (Base only)
npx @agntos/agentwallet create --chain solana --agent PUBKEY     # managed wallet (Solana only)
npx @agntos/agentwallet create --agent 0x... --unmanaged         # autonomous wallet
npx @agntos/agentwallet status 0xWALLET               # wallet info (auto-detects chain)
npx @agntos/agentwallet limits 0xWALLET --daily N --pertx N --reason "..."
npx @agntos/agentwallet token-limit 0xWALLET --token 0x... --token-daily N --token-pertx N
npx @agntos/agentwallet rm-token 0xWALLET --token 0x...
npx @agntos/agentwallet pause 0xWALLET --reason "..."
npx @agntos/agentwallet unpause 0xWALLET
npx @agntos/agentwallet stats
```  
所有命令都支持`--json`参数，以便生成机器可读的输出格式。  

## 限额跟踪机制：  
#### Base区块链  
| 资产 | 跟踪方式 | 限额设置 |  
|------|---------|--------|  
| ETH | 通过Chainlink预言机转换为USD | 每日限额与每次交易限额均共享 |  
| USDC | 1:1兑换为USD | 与ETH共享同一限额池 |  
| 其他ERC-20代币 | 默认无限制 | 所有者可分别为每个代币设置限额 |  
（ETH和USDC共享每日总额限额；例如：花费30美元的ETH和15美元的USDC，总计不超过50美元的限额。）  

#### Solana区块链  
| 资产 | 跟踪方式 | 限额设置 |  
|------|---------|--------|  
| SOL | 代理实际支付的SOL金额 | 每日限额与每次交易限额均共享 |  
| SPL代币 | 每个代币单独设置限额 | 最多可设置16个代币的限额 |  
（限额以USD为单位，保留6位小数。每日限额会根据`unix_timestamp / 86400`进行重置。）  

## 合约地址：  
### Base主网  
| 合约 | 地址 |  
|----------|---------|  
| 工厂合约 | `0x77c2a63BB08b090b46eb612235604dEB8150A4A1` |  
| 实现合约 | `0xEF85c0F9D468632Ff97a36235FC73d70cc19BAbA` |  
| Chainlink ETH/USD接口 | `0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70` |  
| USDC接口 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |  

### Solana开发网  
| 合约 | 地址 |  
|------|---------|  
| Anchor程序 | `4XHYgv4fczfAtkKB792yrP57iakR9extKtkigsXCJm5e` |  
| IDL账户 | `6tEPFHmaaDMH2rth1jPWyvDDxh6GcZhkAEj9kKTCY9k6` |  

## 安全机制：  
- **非托管模式**：您的私钥始终保存在您的设备上，不会离开您的系统。  
- **链上执行**：所有交易限额都由智能合约或Solana程序控制，而非API。  
- **免费Gas费用**：钱包创建时即可立即使用免费Gas进行交易。  
- **密码短语管理**：用户的私钥存储在设备的安全区域中。  
  - Base：通过RIP-7212预编译机制进行验证。  
  - Solana：通过secp256r1预编译机制进行验证。  
- **交易不可撤销**：一旦注册了密码短语，管理员将失去控制权。  
  - Base：所有者账户会被设置为无效地址。  
  - Solana：所有者账户会被设置为`11111111111111111111111111111112`这个无效地址。  
- **Chainlink预言机**：提供去中心化的价格数据，每小时更新一次。  
- **紧急控制**：所有者可随时暂停交易、撤回交易或将账户列入黑名单。  
- **直接合约访问**：您可以直接调用合约，无需通过API。
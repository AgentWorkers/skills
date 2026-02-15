---
name: jb-decode
description: 解码并分析 Juicebox V5 交易的数据结构（calldata）。解释交易的执行过程，解析函数参数，并使用 `cast` 或 `ethers.js` 工具来分析历史交易记录。
---

# Juicebox V5 交易解码器

用于解码和分析 Juicebox V5 交易的输入数据（calldata）。

## 常用函数选择器

### JBMultiTerminal
```
pay(uint256,address,uint256,address,uint256,string,bytes)
  Selector: 0x...
  - Pay into a project

cashOutTokensOf(address,uint256,uint256,address,uint256,address,bytes)
  Selector: 0x...
  - Cash out tokens for funds

sendPayoutsOf(uint256,address,uint256,uint256,uint256)
  Selector: 0x...
  - Distribute payouts to splits

useAllowanceOf(uint256,address,uint256,uint256,uint256,address,address,string)
  Selector: 0x...
  - Use surplus allowance
```

### JBController
```
launchProjectFor(address,string,(uint256,uint256,uint256,uint256,address,(uint256,uint256,uint256,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,address,uint256),(uint256,(bool,uint256,uint256,address,uint256,address)[])[],(address,address,(uint256,uint32)[],(uint256,uint32)[])[])[],(address,(address,uint8,uint32)[])[],string)
  - Launch a new project

queueRulesetsOf(uint256,(uint256,uint256,uint256,uint256,address,(uint256,uint256,uint256,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,bool,address,uint256),(uint256,(bool,uint256,uint256,address,uint256,address)[])[],(address,address,(uint256,uint32)[],(uint256,uint32)[])[])[],string)
  - Queue new rulesets

mintTokensOf(uint256,uint256,address,string,bool)
  - Mint tokens

burnTokensOf(address,uint256,uint256,string)
  - Burn tokens
```

## 使用 `Cast` 进行解码

### 解码输入数据（Calldata）
```bash
# Get the function signature
cast 4byte <first-4-bytes-of-calldata>

# Decode full calldata (need ABI)
cast calldata-decode "pay(uint256,address,uint256,address,uint256,string,bytes)" <calldata>
```

### 解码交易信息（Transaction）
```bash
# Get transaction details
cast tx <txhash> --rpc-url $RPC_URL

# Decode the input
cast tx <txhash> --rpc-url $RPC_URL | grep input
```

### 示例：解码支付交易
```bash
# Assuming calldata starts with pay() selector
cast calldata-decode \
    "pay(uint256,address,uint256,address,uint256,string,bytes)" \
    "0x..." \
    # Returns:
    # projectId: 123
    # token: 0x0000...0000 (native)
    # amount: 1000000000000000000
    # beneficiary: 0x...
    # minReturnedTokens: 0
    # memo: "Supporting the project"
    # metadata: 0x...
```

## 使用 `ethers.js` 进行解码

### 设置解码环境
```typescript
import { ethers } from 'ethers';

// Terminal ABI fragment
const TERMINAL_ABI = [
    'function pay(uint256 projectId, address token, uint256 amount, address beneficiary, uint256 minReturnedTokens, string memo, bytes metadata) payable returns (uint256)',
    'function cashOutTokensOf(address holder, uint256 projectId, uint256 cashOutCount, address tokenToReclaim, uint256 minTokensReclaimed, address beneficiary, bytes metadata) returns (uint256)',
    'function sendPayoutsOf(uint256 projectId, address token, uint256 amount, uint256 currency, uint256 minTokensPaidOut) returns (uint256)',
];

const iface = new ethers.Interface(TERMINAL_ABI);
```

### 解码输入数据（Calldata）
```typescript
function decodeCalldata(calldata: string) {
    try {
        const decoded = iface.parseTransaction({ data: calldata });
        return {
            name: decoded.name,
            args: decoded.args,
            signature: decoded.signature,
        };
    } catch (e) {
        return null;
    }
}
```

### 从哈希值解码交易信息
```typescript
async function decodeTransaction(txHash: string) {
    const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
    const tx = await provider.getTransaction(txHash);

    if (!tx) throw new Error('Transaction not found');

    const decoded = iface.parseTransaction({ data: tx.data });

    return {
        from: tx.from,
        to: tx.to,
        value: ethers.formatEther(tx.value),
        function: decoded?.name,
        args: decoded?.args,
    };
}
```

## 交易分析示例

### 支付交易
```
Function: pay(uint256,address,uint256,address,uint256,string,bytes)
Parameters:
  projectId: 123          → Paying into project #123
  token: 0x000...000      → Using native currency (ETH)
  amount: 1e18            → Paying 1 ETH
  beneficiary: 0xABC...   → Tokens go to this address
  minReturnedTokens: 0    → No minimum (accepts any amount)
  memo: "Great project!"  → Payment memo
  metadata: 0x...         → Optional hook metadata

Effect: Sends 1 ETH to project #123, mints tokens to 0xABC...
```

### 提现交易
```
Function: cashOutTokensOf(...)
Parameters:
  holder: 0xABC...        → Token holder cashing out
  projectId: 123          → From project #123
  cashOutCount: 1000e18   → Cashing out 1000 tokens
  tokenToReclaim: 0x0...  → Reclaiming ETH
  minTokensReclaimed: 0   → No minimum
  beneficiary: 0xABC...   → ETH goes here
  metadata: 0x...         → Optional hook metadata

Effect: Burns 1000 tokens, sends proportional ETH to 0xABC...
```

### 队列规则集交易
```
Function: queueRulesetsOf(...)
Parameters:
  projectId: 123
  rulesetConfigs: [...]   → New ruleset configurations
  memo: "Update params"

Effect: Queues new ruleset(s) that activate when current ends
```

## 解码挂钩元数据（Decoding Hook Metadata）

挂钩元数据采用 ABI 编码格式。常见模式包括：

### 回购挂钩元数据（Buyback Hook Metadata）
```solidity
// Encode
bytes memory metadata = abi.encode(amountToSwapWith, minimumSwapAmountOut);

// Decode
(uint256 amountToSwapWith, uint256 minimumSwapAmountOut) = abi.decode(metadata, (uint256, uint256));
```

### 721 挂钩元数据（721 Hook Metadata）
```solidity
// Encode tier IDs to mint
bytes memory metadata = abi.encode(tierIds);

// Decode
uint256[] memory tierIds = abi.decode(metadata, (uint256[]));
```

## 生成指南

1. 通过 `to` 地址识别合约。
2. 提取函数选择器（前 4 个字节）。
3. 使用相应的 ABI 解码参数。
4. 用通俗的语言解释交易的效果。
5. 如果存在嵌套元数据，也需要进行解码。

## 示例提示：

- “这笔交易是做什么的？地址为 0x...”
- “解码 JBMultiTerminal 的输入数据。”
- “解释地址为 0xabc... 的交易中发生了什么？”
- “这次支付（pay()）调用使用了哪些参数？”
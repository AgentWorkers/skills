# eCash 协议挖矿攻略

你是一名 eCash 挖矿者。eCash 是一种基于 Base（Ethereum L2）平台的智能证明（Proof-of-Intelligence, PoI）挖矿协议。通过解决加密谜题，你可以获得真实的 ERC-20 代币，这些代币可以在 Aerodrome DEX 上兑换成 ETH。

**API:** https://api.ecash.bot  
**合约地址:** 0x2c1890C8f97031BDA42E11fB5Aac08F4f2C89811 (Base, chainId 8453)  
**官方网站:** https://ecash.bot  
**GitHub:** https://github.com/ecashprotocol/ecash-protocol  

## 关键概念  

- **ECASH**: 基于 Base 的 ERC-20 代币，最大发行量为 2100 万枚，具有实际货币价值，可在 Aerodrome DEX 上交易。  
- **谜题**: 共有 6,300 道谜题，每道谜题都包含一个使用 scrypt + AES-256-GCM 加密的答案。  
- **时代划分**: 第 1 时代（谜题编号 0-3149）每道谜题奖励 4,000 ECASH；第 2 时代（谜题编号 3150-6299）每道谜题奖励 2,000 ECASH。  
- **挖矿流程**: 猜出答案 → 使用 scrypt 算法解密 → 通过 `commit-reveal` 操作在链上确认答案并领取奖励。  
- **Gas 系统**: 用于防止恶意行为：初始 Gas 为 500，选择答案消耗 10 Gas，提交答案消耗 25 Gas，成功解密额外消耗 100 Gas。  
- **兑换**: 解锁的 ERC-20 代币需通过 Aerodrome Router 进行兑换，再兑换成 ETH。  

## 所需依赖库  

```
npm install ethers scrypt-js
```  

- `ethers` (v6): 用于钱包生成、合约交互和签名操作。  
- `scrypt-js`: 用于生成解密谜题所需的密钥。  

## 第 1 步：离线练习解谜（免费）  

在花费任何费用之前，先确认自己能够解谜：  
1. `GET https://api.ecash.bot/puzzles` → 查看可用谜题列表。  
2. `GET https://api.ecash.bot/puzzles/{id}` → 阅读谜题内容。  
3. `GET https://api.ecash.bot/puzzles/{id}/blob` → 下载谜题的加密数据（以二进制形式）。  
   返回格式：`{"puzzleId": 0, "blob": "hex...", "nonce": "hex...", "tag": "hex..."}`  

4. 根据谜题内容猜测答案。  
5. 对答案进行规范化处理：`guess.toLowerCase().replace(/[^a-z0-9 ]/g, '').replace(/\s+/g, ' ').trim()`。  
6. 生成解密密钥：`scrypt(normalized_guess, "ecash-v3-{puzzleId}", N=131072, r=8, p=1, keyLen=32)`。  
7. 使用生成的密钥、随机生成的 nonce（12 字节）、tag（16 字节）以及加密数据解密。  
8. 如果解密成功，说明答案正确；解密后的 JSON 数据中包含 `salt` 和 `proof`。  
9. 如果解密失败，可无限次尝试，无需额外费用。  

## 第 2 步：创建钱包  

```javascript
const { ethers } = require('ethers');
const wallet = ethers.Wallet.createRandom();
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey);
// SAVE your private key securely
```  

## 第 3 步：为钱包充值  

向你的 Base 钱包中转入约 0.001 ETH，这足以支持数百次交易。  
Base 平台的 Gas 费用如下：  
- `register()`: 约 0.0001 ETH  
- `pick()`: 约 0.0001 ETH  
- `commitSolve()`: 约 0.0001 ETH  
- `revealSolve()`: 约 0.0002 ETH  
- `approve() + swap()`: 约 0.001 ETH  
**完整流程总费用：约 0.002 ETH**  
无需使用矿池（fountain），Base 的 Gas 费用非常低。  

## 第 4 步：在链上注册  

```javascript
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const wallet = new ethers.Wallet('YOUR_PRIVATE_KEY', provider);
const contract = new ethers.Contract('0x2c1890C8f97031BDA42E11fB5Aac08F4f2C89811', [
  'function register(address ref) external',
  'function getUserState(address) external view returns (bool registered, uint256 gas, bool hasPick, uint256 activePick, uint256 pickTime, uint256 streak, uint256 lastSolveTime, uint256 totalSolves)'
], wallet);

const tx = await contract.register(ethers.ZeroAddress);
await tx.wait();
```  
进行一次性注册，即可获得 500 Gas。  

## 第 5 步：在链上领取奖励  

在离线确认答案正确后，执行以下操作：  
```javascript
// 1. Pick the puzzle
const pickTx = await contract.pick(puzzleId);
await pickTx.wait();

// 2. Commit (prevents front-running)
const secret = ethers.hexlify(ethers.randomBytes(32));
const commitHash = ethers.keccak256(
  ethers.solidityPacked(
    ['string', 'bytes32', 'bytes32', 'address'],
    [normalizedAnswer, saltFromDecryptedBlob, secret, wallet.address]
  )
);
const commitTx = await contract.commitSolve(commitHash);
await commitTx.wait();

// 3. Wait 1 block (2 seconds on Base)
await new Promise(r => setTimeout(r, 3000));

// 4. Reveal and claim reward
const revealTx = await contract.revealSolve(normalizedAnswer, saltFromDecryptedBlob, secret, proofFromDecryptedBlob);
await revealTx.wait();
// 4,000 ECASH (Era 1) or 2,000 ECASH (Era 2) sent to your wallet
```  

## 第 6 步：出售 ECASH（可选）  

```javascript
const AERODROME_ROUTER = '0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43';
const AERODROME_FACTORY = '0x420DD381b31aEf6683db6B902084cB0FFECe40Da';
const WETH = '0x4200000000000000000000000000000000000006';
const ECASH = '0x2c1890C8f97031BDA42E11fB5Aac08F4f2C89811';

// 1. Approve router to spend ECASH
const ecash = new ethers.Contract(ECASH, ['function approve(address,uint256) returns (bool)'], wallet);
await (await ecash.approve(AERODROME_ROUTER, amount)).wait();

// 2. Swap ECASH → ETH
const router = new ethers.Contract(AERODROME_ROUTER, [
  'function swapExactTokensForETH(uint256,uint256,tuple(address from,address to,bool stable,address factory)[],address,uint256) returns (uint256[])'
], wallet);

const routes = [{ from: ECASH, to: WETH, stable: false, factory: AERODROME_FACTORY }];
const deadline = Math.floor(Date.now() / 1000) + 1200;
await (await router.swapExactTokensForETH(amount, 0, routes, wallet.address, deadline)).wait();
```  

## Gas 经济系统  

| 操作 | Gas 费用 |  
|--------|----------|  
| 注册 | +500 （获得） |  
| 选择谜题 | -10 （消耗） |  
| 提交答案 | -25 （消耗） |  
| 成功解谜 | +100 （奖励） |  
| 每日 Gas 重置 | +5/GAS/天（上限 100） |  
| 最低 Gas 要求 | 35 （最低消耗） |  

Gas 是通缩性的——消耗的 Gas 会被销毁，不会被回收。完成一次解谜流程（选择谜题 + 提交答案）需要 35 Gas。初始 Gas 为 500，因此大约可以进行 14 次尝试。成功解谜可额外获得 100 Gas 奖励，有助于持续挖矿。  

## API 参考  

| API 端点 | 功能说明 |  
|----------|-------------|  
| `GET /health` | 系统状态检查 |  
| `GET /stats` | 协议统计信息、时代安排、DEX 详情等 |  
| `GET /puzzles?limit=10&offset=0` | 分页显示谜题列表 |  
| `GET /puzzles/:id` | 单个谜题详情（包含谜题内容、难度等） |  
| `GET /puzzles/:id/blob` | 加密后的谜题数据（包含 blob、nonce、tag） |  
| `GET /puzzles/:id/preview` | 仅显示谜题元数据（不含谜题内容） |  
| `GET /contract` | 合约地址、chainId、ABI 信息 |  
| `GET /leaderboard` | 按 ECASH 收益排名前缀的矿工列表 |  
| `GET /activity?limit=20` | 最近解谜的矿工记录 |  
| `GET /price` | Aerodrome 上的 ECASH 价格（若存在 LP 机制） |  

## scrypt 算法参数  

- **算法**: scrypt  
- **N**: 131072（2^17）  
- **r**: 8  
- **p**: 1  
- **keyLen**: 32  
- **Salt**: `"ecash-v3-{puzzleId}"`（UTF-8 字符串，非原始字节）  

## 加密机制  

- **加密算法**: AES-256-GCM  
- **密钥**: 从 scrypt 算法生成的 32 字节密钥  
- **Nonce**: 来自谜题数据的 12 字节（hex 编码）  
- **Tag**: 来自谜题数据的 16 字节（hex 编码）  
- **Ciphertext**: 来自谜题数据的加密数据（hex 编码）  

## `commit-reveal` 操作  

- **提交哈希**: `keccak256(abi.encodePacked(answer, salt, secret, msg.sender)`  
  - `answer`: 规范化后的答案字符串  
  - `salt`: 解密后的 salt 字节  
  - `secret`: 随机生成的 32 字节  
  - `msg.sender`: 你的钱包地址  

- **揭示时间**: 256 个区块后（约 8.5 分钟）  
- 同一区块内的重复提交会被阻止（防止恶意行为）  

## 完整的自主挖矿流程  

1. `GET /puzzles` → 查找未解谜题  
2. `GET /puzzles/{id}` → 阅读谜题内容  
3. `GET /puzzles/{id}/blob` → 下载加密数据  
4. 分析谜题并猜测答案  
5. 对答案进行规范化处理，然后使用 scrypt 算法生成解密密钥  
6. 如果解密失败，可无限次尝试  
7. 如果成功，从解密数据中提取 `salt` 和 `proof`  
8. 如需，创建钱包并充值约 0.001 ETH  
9. `register(address(0))` 进行一次性注册  
10. `pick(puzzleId)` 选择谜题  
11. `commitSolve(commitHash)` 提交答案  
12. 等待 1 个区块  
13. `revealSolve(answer, salt, secret, proof)` 在链上领取奖励  
14. （可选）`approve(router, amount)` 通过 Aerodrome Router 将 ECASH 兑换成 ETH  

## 挖矿策略建议：  

1. **仔细阅读谜题**: 每个单词都是线索，注意名称、地点、日期和文字游戏。  
2. **深入研究**: 这些不是简单的知识题，需要多步骤推理和跨来源的信息整合。  
3. **先离线练习解谜**: 解密过程免费且无次数限制，只有在确认答案正确后再消耗 Gas。  
4. **确保答案正确**: 答案需符合规范化要求（小写、仅包含字母数字和空格），并通过 scrypt 算法验证。  
5. **查看排行榜**: 了解已解谜题的数量和当前挖矿情况。  
6. **节约 Gas**: 完整的解谜流程需要 35 Gas，初始 Gas 为 500，因此大约可以进行 14 次尝试。成功解谜可额外获得 100 Gas 奖励。  
7. **优先挖掘早期时代的谜题**: 第 1 时代每道谜题奖励更高。  

## 资源与支持：  

- **官方网站**: https://ecash.bot  
- **GitHub**: https://github.com/ecashprotocol/ecash-protocol  
- **Basescan**: https://basescan.org/token/0x2c1890C8f97031BDA42E11fB5Aac08F4f2C89811  
- **ClawdHub 技能页面**: https://clawdhub.com/skills/ecash-protocol-mining  
- **社交平台**: X/Twitter: https://x.com/ecashbase  
- **联系方式**: contact@ecash.bot  
- **问题反馈**: https://github.com/ecashprotocol/ecash-protocol/issues
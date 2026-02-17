---
name: ecash
description: 通过在 Base 平台上解决加密谜题来获取 ECASH 代币。AI 代理会阅读诗歌、猜测答案，使用 scrypt 算法解密数据，并通过链上的“commit-reveal”机制来领取奖励。
version: 2.4.0
---
# eCash 协议 — AI 代理挖矿技能

通过在 Base L2 上解决加密谜语诗来挖掘 ECASH 代币。总供应量为 2100 万枚，每枚代币都通过智能行为获得。

> **单一合约设计：** 合约地址本身就是 ECASH ERC-20 代币。一个合约负责挖矿、奖励和代币的管理。已在 [Basescan](https://basescan.org/address/0x4fD4a91853ff9F9249c8C9Fc41Aa1bB05b0c85A1) 上验证。

## 关键信息

- **合约地址：** 0x4fD4a91853ff9F9249c8C9Fc41Aa1bB05b0c85A1（Base，chainId 8453）
- **API：** https://api.ecash.bot
- **官方网站：** https://ecash.bot
- **GitHub：** https://github.com/ecashprotocol/ecash-protocol
- **Clawhub：** https://clawhub.ai/skills/ecash
- **链 RPC：** https://mainnet.base.org

## 安全与凭证

- **钱包：** 该技能可能会为链上交易创建一个临时钱包。请使用一个仅有少量资金（约 0.01 ETH）的专用挖矿钱包。切勿使用您的主钱包。
- **私钥：** 绝不要存储、记录或传输私钥。所有签名操作都在本地完成。
- **RPC：** 使用公共的 Base RPC（https://mainnet.base.org），无需 API 密钥。
- **CPU/内存：** 每次 scrypt 验证大约消耗 128MB 的内存。这是正常现象。

## 自主操作

有关完全自主挖矿（包括钱包设置和无人值守操作）的详细信息，请参阅 [自主代理指南](https://github.com/ecashprotocol/ecash-protocol/blob/main/docs/AUTONOMOUS-AGENT.md)。

## 挖矿流程

```
1. Fetch unsolved puzzles from API (/puzzles/unsolved?limit=5)
2. Pick a puzzle and read the riddle-poem
3. Reason about the answer (ALWAYS 3+ words, never single or two words)
4. Normalize your guess: lowercase, strip non-alphanumeric (keep spaces), collapse multiple spaces, trim
5. Fetch the encrypted blob (included in /puzzles/:id response)
6. Run scrypt(normalized_guess) → try AES-256-GCM decrypt on the blob
7. If decryption FAILS → wrong answer → go to step 3, try another guess (free, unlimited)
8. If decryption SUCCEEDS → you now have: salt (bytes32) + merkle proof (bytes32[])
9. Create wallet (if needed), fund with ~$0.01 ETH on Base
10. Run preflight checks, then: register → pick → commit → wait 1+ blocks → reveal
11. Collect ECASH reward. Move to next puzzle.
```

**重要提示：** 第 1-8 步骤完全免费，无需钱包，无需支付 gas 费用。只有在获得正确答案后（第 9 步及以后），才需要 ETH。

## API 参考

基础 URL：`https://api.ecash.bot`

| 端点 | 方法 | 返回值 |
|---|---|---|
| /health | GET | `{ status: "ok", timestamp }` |
| /stats | GET | `{ totalSolved, totalPuzzles, miningReserve, currentEra, reward, ... }` |
| /puzzles?limit=10&offset=0 | GET | 分页显示谜语列表及解决状态 |
| /puzzles/unsolved?limit=5 | GET | 显示未解决的谜语及其加密数据（方便代理使用） |
| /puzzles/:id | GET | 单个谜语及其加密数据： `{ id, title, poem, minWords: 3, encryptedBlob, ... }` |
| /puzzles/:id/blob | GET | 仅显示加密数据： `{ puzzleId, blob, nonce, tag }` |
| /contract | GET | 合约地址、chainId 和完整 ABI |
| /leaderboard | GET | 按赚取的 ECASH 代币数量排序的矿工排行榜 |
| /activity?limit=20 | GET | 最近的解决记录及交易哈希 |
| /price | GET | 代币价格（如果存在矿池的话，从 Aerodrome LP 获取） |
| /puzzles/:id/preview | GET | 猜语诗的简短预览 |

### 示例：获取未解决的谜语

```
GET https://api.ecash.bot/puzzles/unsolved?limit=2
→ {
    "puzzles": [
      { "id": 0, "title": "...", "poem": "...", "minWords": 3, "encryptedBlob": {...} },
      { "id": 2, "title": "...", "poem": "...", "minWords": 3, "encryptedBlob": {...} }
    ],
    "count": 2,
    "totalUnsolved": 6299
  }
```

### 示例：获取单个谜语及其加密数据

```
GET https://api.ecash.bot/puzzles/42
→ {
    "id": 42,
    "title": "Laboratory of Choice",
    "poem": "in halls where rodents learn to choose...",
    "category": "Psychology",
    "difficulty": "Medium",
    "solved": false,
    "minWords": 3,
    "encryptedBlob": {
      "puzzleId": 42,
      "blob": "a3f8c9d2e1...",
      "nonce": "9c2b4f1a82...",
      "tag": "1d4fe88b03..."
    }
  }
```

## IPFS（无需 API 的替代方案）

所有数据也存储在 IPFS 上。您完全不需要使用 API：

```
ipfs://bafybeifrd5s3jms7hnb25t57iqyr2yxg425gbamljxoinuci22ccwttelu
```

包含以下文件：
- `public-puzzles.json` — 包含 6,300 首谜语及其元数据（无答案）
- `encrypted-blobs.json` — 包含 6,300 个加密数据文件

下载这两个文件后，可以在本地运行 scrypt 程序进行解密。无需服务器，也无需任何权限。

## 答案格式（至关重要）

**答案必须由 3 个或更多单词组成。** 绝不允许使用单个单词或两个单词。

有效答案示例：
- "the rosetta stone"（3 个单词）
- "cogito ergo sum"（3 个单词）
- "double helix structure"（3 个单词）
- "tower of babel"（3 个单词）

如果您的答案只有 1-2 个单词，那么是错误的。请继续思考。

## 规范化（至关重要）

您的答案规范化必须完全符合合约要求。任何字符的差异都会导致链上的 Merkle 证明失败。

```javascript
function normalize(answer) {
  // Step 1: lowercase
  // Step 2: keep only a-z, 0-9, and space
  let result = answer.toLowerCase().replace(/[^a-z0-9 ]/g, '');
  // Step 3: trim + collapse multiple spaces
  return result.trim().replace(/\s+/g, ' ');
}
```

示例：
| 输入 | 输出 |
|---|---|
| "The Rosetta Stone!" | "the rosetta stone" |
| "  COGITO   ergo  SUM  " | "cogito ergo sum" |
| "Schrödinger's Cat" | "schrdingers cat" |
| "π = 3.14159" | "314159" |

## scrypt 解密（离线验证）

这是在不接触区块链的情况下验证答案的方法：

```javascript
const crypto = require('crypto');

function tryDecrypt(puzzleId, guess, blobData) {
  const normalized = normalize(guess);
  const scryptSalt = `ecash-v3-${puzzleId}`;

  // Derive key via scrypt — takes ~270ms, uses 128MB RAM
  const key = crypto.scryptSync(
    Buffer.from(normalized, 'utf-8'),
    Buffer.from(scryptSalt, 'utf-8'),
    32,  // keyLen = 32 bytes (256 bits)
    { N: 131072, r: 8, p: 1, maxmem: 256 * 1024 * 1024 }
  );

  // Try AES-256-GCM decryption
  const blob = Buffer.from(blobData.blob, 'hex');
  const nonce = Buffer.from(blobData.nonce, 'hex');
  const tag = Buffer.from(blobData.tag, 'hex');

  try {
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, nonce);
    decipher.setAuthTag(tag);
    const decrypted = Buffer.concat([decipher.update(blob), decipher.final()]);
    const result = JSON.parse(decrypted.toString('utf-8'));
    // result = { salt: "0x...", proof: ["0x...", ...] }
    return { success: true, salt: result.salt, proof: result.proof };
  } catch {
    return { success: false }; // Wrong answer — GCM auth tag rejected
  }
}
```

### scrypt 参数（永久性、公开、在代码中固定）

**重要提示：** scrypt 盐值（`"ecash-v3-{puzzleId}"）用于密钥生成，它与谜语的 Merkle 盐值不同。Merkle 盐值位于加密数据中，仅在解密成功时才会显示。

> **停止并确认：** 在成功解密谜语后，请停止操作并询问用户是否希望在链上确认结果。不要继续解决其他谜语。用户需要为钱包充值并批准交易。只有在用户明确同意的情况下，才能在链上进行确认。

## 在 Base 上购买 ETH

在链上确认结果之前，您需要在 Base 上拥有约 0.01 ETH 作为 gas 费用。有以下几种方式：
1. **从 Ethereum 桥接：** 使用 official Base Bridge（地址：bridge.base.org）
2. **通过 CEX 提现：** 从 Coinbase、Binance 等平台直接将 ETH 提现到 Base。
3. **跨链交换：** 使用 Jumper.exchange 或类似工具将其他链上的 ETH 交换到 Base。
4. ** faucet（仅限测试网）：** 可以使用 Base Sepolia faucet 进行测试。

对于主网挖矿，建议准备 0.001-0.01 ETH（按当前价格计算约为 3-30 美元），这足以覆盖数百次交易。

## 在链上确认结果

一旦 scrypt 确认您的答案（您拥有 `salt` 和 `proof`），请按照以下步骤操作：

### 第 1 步：创建钱包（如需要）

```javascript
const { ethers } = require('ethers');
const wallet = ethers.Wallet.createRandom();
console.log('Address:', wallet.address);
// Store wallet.privateKey securely — NEVER log or share it
```

向钱包充值约 0.01 ETH（足够完成所有交易）。

### 第 2 步：连接到合约

```javascript
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const signer = new ethers.Wallet(PRIVATE_KEY, provider);

const ECASH_ADDRESS = '0x4fD4a91853ff9F9249c8C9Fc41Aa1bB05b0c85A1';
const ECASH_ABI = [
  'function register(address referrer) external',
  'function pick(uint256 puzzleId) external',
  'function commitSolve(bytes32 hash) external',
  'function revealSolve(string answer, bytes32 salt, bytes32 secret, bytes32[] proof) external',
  'function cancelExpiredCommit() external',
  'function claimDailyGas() external',
  'function puzzleSolved(uint256 puzzleId) external view returns (bool)',
  'function puzzleSolver(uint256 puzzleId) external view returns (address)',
  'function totalSolved() external view returns (uint256)',
  'function getUserState(address) external view returns (bool registered, uint256 gas, bool hasPick, uint256 activePick, uint256 pickTime, uint256 streak, uint256 lastSolveTime, uint256 totalSolves)',
  'function getCommitment(address) external view returns (bytes32 hash, uint256 blockNumber)',
  'function getReward(uint256 puzzleId) external view returns (uint256)',
  'function balanceOf(address) external view returns (uint256)'
];

const contract = new ethers.Contract(ECASH_ADDRESS, ECASH_ABI, signer);
```

### 第 3 步：预检（非常重要）

在执行任何链上操作之前，请先验证您的状态：

```javascript
async function preflightCheck(contract, signer, puzzleId) {
  const state = await contract.getUserState(signer.address);
  const puzzleAlreadySolved = await contract.puzzleSolved(puzzleId);

  console.log('Preflight Check:');
  console.log('- Registered:', state.registered);
  console.log('- Gas balance:', state.gas.toString());
  console.log('- Has active pick:', state.hasPick);
  console.log('- Active pick ID:', state.activePick.toString());
  console.log('- Puzzle already solved:', puzzleAlreadySolved);

  // Check commitment status
  const [commitHash, commitBlock] = await contract.getCommitment(signer.address);
  console.log('- Has commitment:', commitHash !== ethers.ZeroHash);
  if (commitHash !== ethers.ZeroHash) {
    const currentBlock = await signer.provider.getBlockNumber();
    const blocksElapsed = currentBlock - Number(commitBlock);
    console.log('- Blocks since commit:', blocksElapsed);
    console.log('- Commit expired:', blocksElapsed > 256);
  }

  return {
    registered: state.registered,
    gas: Number(state.gas),
    hasPick: state.hasPick,
    activePick: Number(state.activePick),
    puzzleSolved: puzzleAlreadySolved,
    hasCommit: commitHash !== ethers.ZeroHash
  };
}
```

**getUserState 的返回值：**
| 字段 | 类型 | 描述 |
|---|---|---|
| registered | bool | 地址是否调用过 register() 方法 |
| gas | uint256 | 内部 gas 余额（非 ETH） |
| hasPick | bool | 用户是否选择了某个谜语 |
| activePick | uint256 | 当前选择的谜语 ID（未选择则为 0） |
| pickTime | uint256 | 选择谜语的时间戳 |
| streak | uint256 | 连续成功的解决次数 |
| lastSolveTime | uint256 | 上次成功解决的时间戳 |
| totalSolves | uint256 | 该地址解决的总谜语数量 |

### 第 4 步：注册（一次性操作）

```javascript
if (!preflight.registered) {
  await contract.register(ethers.ZeroAddress); // no referrer
  // Or: await contract.register('0xFriendAddress'); // +50 gas to them
}
```

### 第 5 步：选择谜语

```javascript
if (!preflight.hasPick) {
  await contract.pick(puzzleId);
  // Locks this puzzle to you for 24 hours. Costs 10 internal gas.
}
```

### 第 6 步：提交答案（受保护）

```javascript
const secret = ethers.hexlify(ethers.randomBytes(32));
// CRITICAL: Commit hash formula is keccak256(abi.encodePacked(answer, salt, secret, msg.sender))
// Order: answer (string), salt (bytes32), secret (bytes32), address
const commitHash = ethers.keccak256(
  ethers.solidityPacked(
    ['string', 'bytes32', 'bytes32', 'address'],
    [normalizedAnswer, salt, secret, signer.address]
  )
);
const commitTx = await contract.commitSolve(commitHash);  // Note: NO puzzleId parameter
await commitTx.wait();
// Costs 25 internal gas
```

**重要提示：** 提交的哈希值中包含您的地址，因此即使他人看到交易记录，也无法窃取您的提交内容。盐值将提交内容与特定谜语关联起来（每个谜语都有唯一的盐值）。

### 第 7 步：等待 1 个以上区块（至关重要）

Base 每约 2 秒生成一个区块。显示结果必须在与提交不同的区块中进行。

### 第 8 步：显示结果并领取奖励

```javascript
try {
  const tx = await contract.revealSolve(
    normalizedAnswer,  // the normalized answer string (NOT puzzleId!)
    salt,              // bytes32, from scrypt decryption result
    secret,            // bytes32, same one you used in commit
    proof              // bytes32[], merkle proof from scrypt decryption result
  );
  const receipt = await tx.wait();
  console.log('Success! Gas used:', receipt.gasUsed.toString());
  // → ECASH minted to your wallet!
  // Era 1 (puzzles 0-3149): 4,000 ECASH
  // Era 2 (puzzles 3150-6299): 2,000 ECASH
} catch (error) {
  // See Error Handling section below
  console.log('Reveal failed:', decodeError(error));
}
```

**注意：** `revealSolve` 方法不接受 puzzleId 参数。合约会根据您的 `pick()` 调用来识别您选择的谜语。

## 错误处理

从失败的交易中解析错误原因：

```javascript
function decodeError(error) {
  // Common revert reasons
  const reasons = {
    'NotRegistered': 'Call register() first',
    'AlreadyRegistered': 'Already registered, skip register()',
    'NoActivePick': 'Call pick(puzzleId) first',
    'AlreadyPicked': 'Already have an active pick',
    'PuzzleAlreadySolved': 'Someone else solved this puzzle',
    'NoCommitment': 'Call commitSolve() first',
    'AlreadyCommitted': 'Already have an active commit',
    'CommitNotExpired': 'Commit still valid, cannot cancel',
    'RevealTooEarly': 'Wait for next block after commit',
    'RevealTooLate': 'Commit expired (>256 blocks), call commitSolve() again',
    'InvalidProof': 'Wrong answer or merkle proof mismatch',
    'InsufficientGas': 'Wait for gas regen or claim daily gas',
    'LockedOut': 'Too many failed attempts, wait 24h',
    'OnCooldown': 'Wait 5 min between solves'
  };

  const message = error.reason || error.message || '';
  for (const [key, hint] of Object.entries(reasons)) {
    if (message.includes(key)) return `${key}: ${hint}`;
  }
  return message;
}
```

## 失败后的恢复

### 提交后未及时显示结果（超过 256 个区块）

如果您提交了答案但未及时显示结果：

```javascript
// Option 1: Just commit again (v3.2 auto-clears expired commits)
await contract.commitSolve(newCommitHash);

// Option 2: Explicitly cancel first
await contract.cancelExpiredCommit();
await contract.commitSolve(newCommitHash);
```

### 三次失败后锁定

如果在同一谜语上连续三次显示错误结果，您将被锁定 24 小时：

```javascript
const lockoutUntil = await contract.lockoutUntil(signer.address, puzzleId);
const now = Math.floor(Date.now() / 1000);
if (lockoutUntil > now) {
  const hoursLeft = (lockoutUntil - now) / 3600;
  console.log(`Locked out for ${hoursLeft.toFixed(1)} more hours`);
  // Move to a different puzzle
}
```

### 选择过期（24 小时内未解决）

如果您的选择过期，请重新选择谜语：

```javascript
await contract.pick(puzzleId); // Free if previous pick expired
```

## 内部 gas 系统

该系统独立于 ETH 运行，用于管理挖矿活动：

| 操作 | 成本/奖励 |
|---|---|
| 注册 | 免费（获得 500 gas） |
| 选择谜语 | -10 gas |
| 提交答案 | -25 gas |
| 正确解决 | +100 gas 奖励 |
| 推荐奖励 | 每推荐一次获得 +50 gas |
| 每日恢复 | 每天 +5 gas（通过 claimDailyGas() 方法） |
| gas 上限 | 100 gas（来自每日恢复） |
| gas 下限 | 35 gas |

**gas 下限：** 当 gas 余额达到或低于 35 时，所有操作均为免费。成功解决答案会获得 +100 gas，因此您始终处于净盈利状态。

## 出售 ECASH（可选）

随着您解决谜语，ECASH 代币会累积在您的钱包中——类似于比特币，它代表了您的收益。出售 ECASH 并非挖矿流程的一部分；代理负责挖矿，人类可以决定何时（或是否）出售。

准备好出售时，您可以在 Aerodrome DEX 上将 ECASH 交换为 ETH。请查看 /price 端点获取当前汇率。有关交换代码的详细信息，请参阅 [自主代理指南](https://github.com/ecashprotocol/ecash-protocol/blob/main/docs/AUTONOMOUS-AGENT.md)。

## 解谜策略

谜语诗中隐藏的答案由 3 个或更多单词组成。请仔细阅读谜语——所有线索都包含在文本中。

**提示：**
- 仔细阅读每一行。线索可能隐藏在比喻、文字游戏或数字中。
- 答案必须由 3 个或更多单词组成。绝不允许使用单个单词或两个单词。
- 尝试不同的表达方式，例如 "the rosetta stone" 和 "rosetta stone" — 文字顺序很重要。
- scrypt 解密每次尝试大约需要 270 毫秒。您可以快速尝试多个答案。
- 如果遇到困难，请继续尝试。总共有 6,300 个谜语。
- 可以使用网络搜索来查找谜语中的线索。

## 规则与限制

- 每次解决之间有 5 分钟的冷却时间。
- 每个谜语最多允许 3 次错误的链上尝试，否则会被锁定 24 小时（请先在本地验证，这种情况不应发生）。
- 如果 24 小时内未解决谜语，选择权将会过期。
- 显示结果必须在提交后的 256 个区块内完成。
- 显示结果必须在与提交不同的区块中进行。

## 常见问题

1. **错误的字段名称：** 相关字段为 `blob`、`nonce`、`tag`，而非 `data`、`iv`、`tag`。
2. **规范化不匹配：** 如果您的答案规范化与合约要求的不一致，即使 scrypt 解密成功，链上的 Merkle 证明也会失败。
3. **在同一区块内提交和显示结果：** `revealSolve` 方法要求 `block.number > commitBlock`。提交后至少等待 3 秒。
4. **错误的提交哈希公式：** 提交哈希的计算公式为 `keccak256(abi.encodePacked(answer, salt, secret, msg.sender)` — 参数顺序为：答案（字符串）、盐值（bytes32）、秘密值（bytes32）、地址。切勿将地址放在首位！
5. **错误的函数签名：** `commitSolve(bytes32 hash)` 仅接受哈希值，不接受 puzzleId 参数。`revealSolve(string, bytes32, bytes32, bytes32[])` 方法也不接受 puzzleId 参数。
6. **显示结果窗口过期：** 提交后有 256 个区块的时间限制（约 8.5 分钟）。如果错过了这个时间窗口，只需再次调用 `commitSolve` 即可（v3.2 版本会自动清除过期的提交）。或者调用 `cancelExpiredCommit()` 手动重置。
7. **scrypt 盐值的混淆：** scrypt 盐值为 `"ecash-v3-{puzzleId}"`，而 Merkle 盐值位于加密数据中——两者是不同的概念。
8. **答案由两个单词组成：** 答案必须由 3 个或更多单词组成。尝试使用 "foo bar" 之类的答案是错误的。

## 资源

- 合约地址：https://basescan.org/address/0x4fD4a91853ff9F9249c8C9Fc41Aa1bB05b0c85A1
- API：https://api.ecash.bot
- GitHub：https://github.com/ecashprotocol/ecash-protocol
- 官方网站：https://ecash.bot
- Clawhub：https://clawhub.ai/skills/ecash
- IPFS：ipfs://bafybeifrd5s3jms7hnb25t57iqyr2yxg425gbamljxoinuci22ccwttelu
- Twitter：https://x.com/ecashbase
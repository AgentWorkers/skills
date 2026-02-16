---
name: ecash
description: 通过在 Base 平台上解决加密谜题来获取 ECASH 代币。AI 代理会阅读诗歌、猜测答案，使用 scrypt 算法解密数据，并通过链上的“commit-reveal”机制来领取奖励。
version: 2.0.0
---
# eCash 协议 — AI 代理挖矿技能

通过在 Base L2 上解决加密谜语诗来挖掘 ECASH 代币。总发行量为 6,300 个代币，最大供应量为 2,100 万个。每个代币都是通过智能行为获得的。

> **单一合约设计：** 合约地址本身就是 ECASH ERC-20 代币。一个合约负责挖矿、奖励以及代币的管理。已在 [Basescan](https://basescan.org/address/0x8f7a4dEbb1095d33eE112795cd14d5371740FC80) 上验证。

## 关键信息

- **合约地址：** 0x8f7a4dEbb1095d33eE112795cd14d5371740FC80（链 ID：8453）
- **API：** https://api.ecash.bot
- **网站：** https://ecash.bot
- **GitHub：** https://github.com/ecashprotocol/ecash-protocol
- **ClawdHub：** https://clawdhub.com/skills/ecash
- **链 RPC：** https://mainnet.base.org

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

**重要提示：** 第 1-8 步骤完全免费，无需钱包、无需支付 gas 费用。只有在获得正确答案后（第 9 步及以后），才需要 ETH。

## API 参考

基础 URL：`https://api.ecash.bot`

| 端点 | 方法 | 返回值 |
|---|---|---|
| /health | GET | `{ status: "ok", timestamp }` |
| /stats | GET | `{ totalSolved, totalPuzzles, miningReserve, currentEra, reward, ... }` |
| /puzzles?limit=10&offset=0 | GET | 带有谜语和解决状态的分页谜语列表 |
| /puzzles/unsolved?limit=5 | GET | 包含加密数据的未解决谜语（方便代理使用） |
| /puzzles/:id | GET | 单个谜语及其加密数据： `{ id, title, poem, minWords: 3, encryptedBlob, ... }` |
| /puzzles/:id_blob | GET | 仅包含加密数据： `{ puzzleId, blob, nonce, tag }` |
| /contract | GET | 合约地址、链 ID 和完整 ABI |
| /leaderboard | GET | 按赚取的 ECASH 代币数量排名的矿工 |
| /activity?limit=20 | GET | 最近的解决记录（包含交易哈希） |

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

### 示例：获取单个谜语（包含加密数据）

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

## IPFS（无需信任的替代方案）

所有数据也存储在 IPFS 上。因此完全不需要使用 API：

```
ipfs://bafybeifrd5s3jms7hnb25t57iqyr2yxg425gbamljxoinuci22ccwttelu
```

包含以下文件：
- `public-puzzles.json` — 6,300 首个谜语及其元数据（不含答案）
- `encrypted-blobs.json` — 6,300 个加密数据文件

下载这两个文件后，可以在本地运行 scrypt 程序进行解密。无需服务器，也无需任何权限。

## 答案格式（非常重要）

**答案必须由 3 个或更多单词组成。** 绝不允许使用单个单词或两个单词。

有效答案示例：
- “the rosetta stone”（3 个单词）
- “cogito ergo sum”（3 个单词）
- “double helix structure”（3 个单词）
- “tower of babel”（3 个单词）

如果你的答案只有 1-2 个单词，那么就是错误的。请继续思考。

## 规范化（非常重要）

你的答案格式必须完全符合合约的要求。任何字符的差异都可能导致区块链上的 Merkle 证明失败。

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

以下是在不接触区块链的情况下验证答案的方法：

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

### scrypt 参数（永久性、公开、在所有地方都硬编码）：

**重要提示：** scrypt 的盐值（`"ecash-v3-{puzzleId}"`）用于密钥生成，它与谜语的 Merkle 盐值不同。Merkle 盐值位于加密数据内部，仅在解密成功时才会显示。

> **停止并申请奖励：** 在成功解密一个谜语后，请立即停止并询问用户是否希望在区块链上申请奖励。不要继续解决其他谜语。用户需要为钱包充值并批准交易。只有在用户明确同意的情况下，才能在区块链上申请奖励。

## 在 Base 上购买 ETH

在区块链上申请奖励之前，你需要在 Base 上拥有约 0.01 ETH 作为 gas 费用。以下是几种获取 ETH 的方法：
1. **从 Ethereum 桥接：** 使用 official Base Bridge（地址：bridge.base.org）
2. **通过 CEX 提现：** 从 Coinbase、Binance 等平台直接将 ETH 提现到 Base
3. **跨链交换：** 使用 Jumper.exchange 或类似平台将其他链上的 ETH 交换到 Base
4. ** faucet（仅限测试网）：** 使用 Base Sepolia faucet

对于主网挖矿，建议准备 0.001-0.01 ETH（按当前价格计算约为 3-30 美元），这足以覆盖数百次交易费用。

## 在区块链上申请奖励

一旦 scrypt 确认你的答案正确（你拥有 `salt` 和 `proof`），请按照以下步骤操作：

### 第 1 步：创建钱包（如需要）

```javascript
const { ethers } = require('ethers');
const wallet = ethers.Wallet.createRandom();
console.log('Address:', wallet.address);
// Store wallet.privateKey securely — NEVER log or share it
```

向该钱包充值约 0.01 ETH（足够完成所有交易）。

### 第 2 步：连接到合约

```javascript
const provider = new ethers.JsonRpcProvider('https://mainnet.base.org');
const signer = new ethers.Wallet(PRIVATE_KEY, provider);

const ECASH_ADDRESS = '0x8f7a4dEbb1095d33eE112795cd14d5371740FC80';
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

在进行任何区块链操作之前，请先验证你的状态：

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
| gas | uint256 | 内部 gas 剩余量（非 ETH） |
| hasPick | bool | 用户是否选择了某个谜语 |
| activePick | uint256 | 当前选择的谜语 ID（如果没有选择，则为 0） |
| pickTime | uint256 | 选择谜语的时间戳 |
| streak | uint256 | 连续成功的解决次数 |
| lastSolveTime | uint256 | 最后一次成功解决的时间戳 |
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

**重要提示：** 提交的哈希值中包含你的地址，因此即使别人看到交易记录，也无法窃取你的提交内容。盐值将提交内容与特定谜语关联起来（每个谜语都有唯一的盐值）。

### 第 7 步：等待 1 个以上区块（非常重要）

Base 每约 2 秒生成一个区块。显示答案的区块必须与提交答案的区块不同。

### 第 8 步：显示答案并领取奖励

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

**注意：** `revealSolve` 方法不接受 puzzleId 参数。合约会根据你的 `pick()` 调用来确定你选择了哪个谜语。

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

## 从失败尝试中恢复

### 提交后未及时显示答案（超过 256 个区块）

如果你提交了答案但未及时显示，可以按照以下步骤操作：

```javascript
// Option 1: Just commit again (v3.2 auto-clears expired commits)
await contract.commitSolve(newCommitHash);

// Option 2: Explicitly cancel first
await contract.cancelExpiredCommit();
await contract.commitSolve(newCommitHash);
```

### 三次失败后锁定

如果在同一个谜语上连续三次提交错误，你的账户将被锁定 24 小时：

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

如果你的选择过期，只需重新选择即可：

```javascript
await contract.pick(puzzleId); // Free if previous pick expired
```

## 内部 gas 系统

该系统独立于 ETH 管理挖矿活动：

| 操作 | 成本/奖励 |
|---|---|
| 注册 | 免费（获得 500 gas） |
| 选择谜语 | -10 gas |
| 提交答案 | -25 gas |
| 正确解决 | +100 gas（奖励） |
| 推荐奖励 | 每推荐一次获得 +50 gas |
| 每日恢复 | 每天 +5 gas（通过 claimDailyGas() 方法获取） |
| gas 上限 | 100 gas（来自每日恢复的总量） |
| gas 下限 | 35 gas |

**gas 下限：** 当 gas 剩余量达到或低于 35 时，所有操作均为免费。成功解决一次会获得 +100 gas，因此你总是处于净盈利状态。

## 解谜策略

谜语诗将答案的线索编码为 3 个或更多单词的字符串。谜语类别包括：
- 历史（如 “the rosetta stone”）
- 科学（如 “double helix structure”）
- 哲学（如 “cogito ergo sum”）
- 数学（如 “pythagorean theorem”）
- 神话（如 “prometheus unbound”）
- 医学（如 “hippocratic oath”）
- 地理（如 “mariana trench”）
- 文学（如 “moby dick”）
- 计算机科学（如 “turing machine”）
- 以及更多类别

**提示：**
- 仔细阅读每一行。线索可能隐藏在隐喻、文字游戏或数字中。
- 答案必须由 3 个或更多单词组成。绝不允许使用单个单词或两个单词。
- 尝试不同的表达方式，例如 “the rosetta stone” 和 “rosetta stone” — 文字顺序很重要。
- scrypt 解密每个答案大约需要 270 毫秒，你可以快速尝试多个答案。
- 如果卡住了，可以先跳过这个问题，总共有 6,300 个谜语可供尝试。
- 可以使用网络搜索来查找谜语中的线索。

## 规则与限制：
- 每次解决之间有 5 分钟的冷却时间
- 每个谜语最多允许 3 次错误的尝试，否则账户将被锁定 24 小时（请先在本地验证）
- 如果 24 小时内未解决，选择将失效
- 显示答案必须在提交后的 256 个区块内完成（约 8.5 分钟）
- 显示答案的区块必须与提交答案的区块不同

## 常见错误：
1. **错误的字段名称：** 相关字段为 `blob`、`nonce`、`tag`，而不是 `data`、`iv`、`tag`。
2. **格式不匹配：** 如果你的答案格式与合约要求的格式相差一个字符，即使 scrypt 解密成功，区块链上的 Merkle 证明也会失败。
3. **在同一区块内提交和显示答案：** `revealSolve` 方法要求 `block.number > commitBlock`。提交后至少等待 3 秒。
4. **提交哈希公式错误：** 提交哈希的公式为 `keccak256(abi.encodePacked(answer, salt, secret, msg.sender)`，参数顺序为：答案（字符串）、盐值（bytes32）、秘密值（bytes32）、地址。注意顺序不能颠倒！
5. **函数签名错误：** `commitSolve(bytes32 hash)` 方法只接受哈希值，不接受 puzzleId；`revealSolve(string, bytes32, bytes32, bytes32[])` 方法也不接受 puzzleId 参数。
6. **显示答案的窗口已过期：** 提交后有 256 个区块的时间限制（约 8.5 分钟）。如果错过了这个时间窗口，只需再次调用 `commitSolve`；版本 3.2 可自动清除过期的提交记录。或者可以调用 `cancelExpiredCommit()` 手动重置。
7. **scrypt 盐值的混淆：** scrypt 的盐值为 `"ecash-v3-{puzzleId}"`，而 Merkle 盐值位于加密数据内部，两者是不同的概念。
8. **答案错误：** 答案必须由 3 个或更多单词组成。尝试使用 “foo bar” 之类的答案是错误的。

## 资源：
- 合约地址：https://basescan.org/address/0x8f7a4dEbb1095d33eE112795cd14d5371740FC80
- API：https://api.ecash.bot
- GitHub：https://github.com/ecashprotocol/ecash-protocol
- 网站：https://ecash.bot
- ClawdHub：https://clawdhub.com/skills/ecash
- IPFS：ipfs://bafybeifrd5s3jms7hnb25t57iqyr2yxg425gbamljxoinuci22ccwttelu
- Twitter：https://x.com/ecashbase
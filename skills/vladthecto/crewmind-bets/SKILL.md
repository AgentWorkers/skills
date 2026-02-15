# CrewMind Arena 赌博技巧

> **简而言之**：在 CrewMind Arena 中对参与的 LLM（大型语言模型）进行投注。预测每个回合中哪个 AI 模型会获胜，如果你的模型赢了，就可以领取奖励。

## 快速入门

```bash
npm install @solana/web3.js @coral-xyz/anchor dotenv
```

## 程序信息

| 参数 | 值 |
|-----------|-------|
| **程序 ID** | `F5eS61Nmt3iDw8RJvvK5DL4skdKUMA637MQtG5hbht3Z` |
| **网络** | Solana 主网 |
| **网站** | https://crewmind.xyz |

## 船只索引映射

| 索引 | 模型 |
|-------|-------|
| 0 | OpenAI |
| 1 | DeepSeek |
| 2 | Grok |
| 3 | Gemini |

---

## PDA 种子数据

| 账户 | 种子数据 |
|---------|-------|
| Config | `["config"]` |
| Round | `["round", config, round_id]` |
| Bet | `["bet", round, user]` |
| Vault | `["vault", round]` |

---

## 指令与鉴别器

| 指令 | 鉴别器（字节） |
|-------------|----------------------|
| `place_bet` | `[222, 62, 67, 220, 63, 166, 126, 33]` |
| `claim` | `[62, 198, 214, 193, 213, 159, 108, 210]` |

---

## 账户结构

### Config 账户（120 字节）

```
Offset  Size  Field
─────────────────────────────────
0       8     discriminator
8       32    admin (Pubkey)
40      32    treasury (Pubkey)
72      8     next_round_id (u64)
80      32    active_round (Pubkey) ← use this!
112     8     active_round_id (u64)
```

### Round 账户（190 字节）

```
Offset  Size  Field
─────────────────────────────────
0       8     discriminator
8       8     id (u64)
16      1     status (u8: 0=Open, 1=Finalized)
17      1     ship_count (u8)
18      1     winner_ship (u8, 255=unset)
19      1     swept (bool)
20      8     start_ts (i64)
28      8     end_ts (i64)
36      8     finalized_ts (i64)
44      8     min_bet (u64)
52      8     max_bet (u64)
60      2     participants (u16)
62      8     total_staked (u64)
70      32    totals_by_ship ([u64; 4])
102     64    weighted_by_ship ([u128; 4])
166     8     losing_pool (u64)
174     16    total_weighted_winners (u128)
```

### Bet 账户（96 字节）

```
Offset  Size  Field
─────────────────────────────────
0       8     discriminator
8       1     initialized (bool)
9       32    round (Pubkey)
41      32    user (Pubkey)
73      1     ship (u8)
74      1     claimed (bool)
75      6     _pad
81      8     total_amount (u64)
89      16    total_weighted (u128)
```

---

## 入口函数：place_bet

### 功能
在当前回合中对某艘“船只”（AI 模型）进行投注。

### 指令
`place_bet(ship: u8, amount: u64)`

### 相关账户（按顺序）

| 序号 | 账户 | 签名者 | 是否可写入 | 说明 |
|---|---------|--------|----------|-------------|
| 0 | user | ✓ | ✓ | 你的钱包 |
| 1 | config | | | PDA 中的 `["config"]` 数据 |
| 2 | round | | ✓ | 来自 config 的当前回合公钥 |
| 3 | bet | | ✓ | PDA 中的 `["bet", round, user]` 数据 |
| 4 | vault | | ✓ | PDA 中的 `["vault", round]` 数据 |
| 5 | system_program | | | `11111111111111111111111111111111` |

### 约束条件：
- `ship < ship_count`（通常为 4）
- `min_bet <= amount <= max_bet`
- `current_time < end_ts`
- 回合状态必须为 `Open`（0）

### 指令数据格式

```
Bytes 0-7:   discriminator [222, 62, 67, 220, 63, 166, 126, 33]
Byte 8:     ship (u8)
Bytes 9-16: amount (u64 LE)
```

---

## 入口函数：claim

### 功能
在回合结束后（如果你的“船只”获胜）领取奖励。

### 指令
`claim()` — 无需参数

### 相关账户（按顺序）

| 序号 | 账户 | 签名者 | 是否可写入 | 说明 |
|---|---------|--------|----------|-------------|
| 0 | user | ✓ | ✓ | 你的钱包 |
| 1 | round | | | 已结束的回合信息 |
| 2 | bet | | ✓ | PDA 中的 `["bet", round, user]` 数据 |
| 3 | vault | | ✓ | PDA 中的 `["vault", round]` 数据 |
| 4 | system_program | | | `1111111111111111111111111111111` |

### 约束条件：
- 回合状态必须为 `Finalized`（1）
- 你的投注对应的“船只”必须是获胜者（`winner_ship`）
- `claimed` 必须为 `false`

### 指令数据格式

```
Bytes 0-7: discriminator [62, 198, 214, 193, 213, 159, 108, 210]
```

## 错误代码及说明

| 代码 | 错误名称 | 说明 |
|------|------|-------------|
| 6004 | InvalidShip | 船只索引超出允许范围（`ship_index >= ship_count`） |
| 6005 | RoundNotOpen | 回合已经结束（`RoundIsFinalized`） |
| 6006 | RoundEnded | 超过截止时间（`end_ts`） |
| 6008 | RoundNotFinalized | 还不能领取奖励（`RoundIsNotFinalized`） |
| 6009 | TooLate | 投注太晚（`TooLate`） |
| 6011 | InvalidBetAmount | 投注金额超出范围（`InvalidBetAmount`） |
| 6014 | AlreadyClaimed | 已经领取过奖励（`AlreadyClaimed`） |
| 6015 | NotAWinner | 你的“船只”没有获胜（`NotAWinner`） |

---

## 完整的 JavaScript 示例代码

```javascript
import { Connection, PublicKey, Keypair, Transaction, TransactionInstruction, SystemProgram } from '@solana/web3.js';

const PROGRAM_ID = new PublicKey('F5eS61Nmt3iDw8RJvvK5DL4skdKUMA637MQtG5hbht3Z');
const SHIPS = { openai: 0, deepseek: 1, grok: 2, gemini: 3 };

async function getActiveRound(connection) {
  const [configPda] = PublicKey.findProgramAddressSync([Buffer.from('config')], PROGRAM_ID);
  const configAccount = await connection.getAccountInfo(configPda);
  if (!configAccount) throw new Error('Config not found');

  const activeRound = new PublicKey(configAccount.data.slice(80, 112));
  if (activeRound.equals(PublicKey.default)) throw new Error('No active round');

  return { configPda, activeRound };
}

async function getRoundInfo(connection, roundPubkey) {
  const acc = await connection.getAccountInfo(roundPubkey);
  if (!acc) throw new Error('Round not found');
  const d = acc.data;

  return {
    id: d.readBigUInt64LE(8),
    status: d.readUInt8(16),           // 0=Open, 1=Finalized
    shipCount: d.readUInt8(17),
    winnerShip: d.readUInt8(18),       // 255 if not set
    startTs: d.readBigInt64LE(20),
    endTs: d.readBigInt64LE(28),
    minBet: d.readBigUInt64LE(44),
    maxBet: d.readBigUInt64LE(52),
  };
}

async function placeBet(connection, wallet, shipName, amountSol) {
  const ship = SHIPS[shipName.toLowerCase()];
  const amountLamports = BigInt(Math.floor(amountSol * 1e9));

  const { configPda, activeRound } = await getActiveRound(connection);
  const roundInfo = await getRoundInfo(connection, activeRound);

  // Validations
  if (roundInfo.status !== 0) throw new Error('Round not open');
  if (BigInt(Date.now() / 1000) >= roundInfo.endTs) throw new Error('Round ended');
  if (amountLamports < roundInfo.minBet || amountLamports > roundInfo.maxBet) {
    throw new Error(`Amount must be between ${Number(roundInfo.minBet)/1e9} and ${Number(roundInfo.maxBet)/1e9} SOL`);
  }

  const [betPda] = PublicKey.findProgramAddressSync(
    [Buffer.from('bet'), activeRound.toBuffer(), wallet.publicKey.toBuffer()], PROGRAM_ID
  );
  const [vaultPda] = PublicKey.findProgramAddressSync(
    [Buffer.from('vault'), activeRound.toBuffer()], PROGRAM_ID
  );

  const data = Buffer.concat([
    Buffer.from([222, 62, 67, 220, 63, 166, 126, 33]), // discriminator
    Buffer.from([ship]),                                // ship u8
    (() => { const b = Buffer.alloc(8); b.writeBigUInt64LE(amountLamports); return b; })()
  ]);

  const ix = new TransactionInstruction({
    keys: [
      { pubkey: wallet.publicKey, isSigner: true, isWritable: true },
      { pubkey: configPda, isSigner: false, isWritable: false },
      { pubkey: activeRound, isSigner: false, isWritable: true },
      { pubkey: betPda, isSigner: false, isWritable: true },
      { pubkey: vaultPda, isSigner: false, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
    ],
    programId: PROGRAM_ID,
    data,
  });

  const tx = new Transaction().add(ix);
  tx.feePayer = wallet.publicKey;
  tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
  tx.sign(wallet);

  return await connection.sendRawTransaction(tx.serialize());
}

async function claim(connection, wallet, roundPubkey) {
  const roundInfo = await getRoundInfo(connection, roundPubkey);
  if (roundInfo.status !== 1) throw new Error('Round not finalized yet');

  const [betPda] = PublicKey.findProgramAddressSync(
    [Buffer.from('bet'), roundPubkey.toBuffer(), wallet.publicKey.toBuffer()], PROGRAM_ID
  );
  const [vaultPda] = PublicKey.findProgramAddressSync(
    [Buffer.from('vault'), roundPubkey.toBuffer()], PROGRAM_ID
  );

  const data = Buffer.from([62, 198, 214, 193, 213, 159, 108, 210]); // claim discriminator

  const ix = new TransactionInstruction({
    keys: [
      { pubkey: wallet.publicKey, isSigner: true, isWritable: true },
      { pubkey: roundPubkey, isSigner: false, isWritable: false },
      { pubkey: betPda, isSigner: false, isWritable: true },
      { pubkey: vaultPda, isSigner: false, isWritable: true },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
    ],
    programId: PROGRAM_ID,
    data,
  });

  const tx = new Transaction().add(ix);
  tx.feePayer = wallet.publicKey;
  tx.recentBlockhash = (await connection.getLatestBlockhash()).blockhash;
  tx.sign(wallet);

  return await connection.sendRawTransaction(tx.serialize());
}

// Usage:
// const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed');
// const wallet = Keypair.fromSecretKey(...);
// await placeBet(connection, wallet, 'deepseek', 0.01);
```

---

## 工作流程总结

```
1. GET ACTIVE ROUND
   └─> Read Config PDA → get active_round pubkey

2. CHECK ROUND STATUS
   └─> Read Round account → verify status=0 (Open), check end_ts

3. PLACE BET
   └─> Call place_bet(ship, amount)
   └─> Creates Bet PDA, transfers SOL to Vault

4. WAIT FOR ROUND TO END
   └─> Monitor: current_time > end_ts

5. WAIT FOR FINALIZATION
   └─> Monitor: Round.status == 1 (Finalized)
   └─> Check: Round.winner_ship

6. CLAIM (if won)
   └─> Call claim() if your ship == winner_ship
   └─> Receives: original_bet + share_of_losing_pool
```

---

## 安全规则：
- 投注金额不得超过 `max_bet`。
- 投注前请检查 `end_ts` 以避免出现“投注太晚”（`TooLate`）的错误。
- 每个用户每轮只能投注一次（但可以追加现有投注）。
- 投注前务必确认回合状态为 `Open`。
- 领取奖励前务必确认回合状态为 `Finalized`。
- 请保留至少 0.002 SOL 作为交易费用（建议的缓冲金额）。
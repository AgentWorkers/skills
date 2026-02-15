---
name: cabin-sol
description: Solana 开发教程与工具：通过实际挑战、Anchor 框架、Token-2022 标准、压缩型 NFT（Compressed NFTs）以及安全最佳实践来教授编程开发。倡导“回归基础计算（Return to Primitive Computing）”的理念。
license: MIT
metadata:
  author: Ted
  version: "1.0.0"
  clawdbot:
    emoji: "🌲"
---

# Cabin Sol 🌲

> “回归原始的计算方式。”

这是一份全面的Solana开发指南，专为AI代理程序设计。使用Anchor框架来构建程序，掌握账户模型，并避免那些让大多数开发者犯错的常见陷阱。

---

## 最重要的概念

> **在Solana中，账户就是一切。**

与Ethereum不同，Solana程序是**无状态的**。所有数据都存储在**账户**中，程序通过这些账户来读取和写入数据。

对于每一个功能，都需要思考以下问题：
1. **这些数据存储在哪里？**（属于哪个账户）
2. **这个账户归谁所有？**（是程序拥有的还是用户拥有的）
3. **这是一个PDA（Program Derived Address）吗？**（没有私钥的地址）
4. **租金如何支付？**（免租金的账户可以在创建后两年内无需支付租金）

---

## AI代理程序的模式

### 教学模式
- “PDA是如何工作的？”
- “解释Solana的账户模型”
- “SPL Token和Token-2022有什么区别？”

### 开发模式
- “帮我构建一个质押程序”
- “使用Metaplex创建一个NFT集合”
- “构建一个代币交换功能”

### 审查模式
- “检查这个程序是否存在安全漏洞”
- “验证我的PDA地址是否正确生成”
- “审计这个CPI（Contract Program Interface）”

### 调试模式
- “为什么我的交易失败了？”
- “调试‘账户未找到’的错误”
- “修复我的代币转移问题”

---

## 快速入门

### 选项A：使用create-solana-dapp（推荐）

```bash
npx create-solana-dapp@latest
# Select: Next.js + next-tailwind-counter
cd my-project
npm install
npm run anchor localnet   # Terminal 1
npm run anchor build && npm run anchor deploy  # Terminal 2
npm run dev               # Terminal 3
```

### 选项B：仅使用Anchor框架

```bash
anchor init my_program
cd my_program
solana-test-validator     # Terminal 1
anchor build && anchor deploy  # Terminal 2
anchor test
```

---

## 项目结构

```
my-solana-dapp/
├── anchor/                 # Solana programs (Rust)
│   ├── programs/
│   │   └── my_program/
│   │       └── src/lib.rs  # Your Rust program
│   ├── tests/              # TypeScript tests
│   └── Anchor.toml         # Anchor config
├── src/                    # Next.js frontend
│   ├── app/
│   └── components/
└── package.json
```

---

## 挑战

通过逐步的挑战来学习Solana：

| # | 挑战 | 核心概念 |
|---|-----------|--------------|
| 0 | Hello Solana | 第一个Anchor程序，了解账户的概念 |
| 1 | SPL Token | 可互换代币、ATA（Addressable Token）的创建 |
| 2 | NFT与Metaplex | NFT标准、元数据、集合的创建 |
| 3 | PDA与托管 | PDA的使用、程序权限、托管机制 |
| 4 | 质押 | 基于时间的奖励、存款机制 |
| 5 | Token-2022 | 代币转移钩子、扩展功能的实现 |
| 6 | 压缩NFT | 使用Merkle树进行数据压缩 |
| 7 | Oracle（Pyth） | 价格数据源、数据时效性检查 |
| 8 | AMM（Automated Market Maker） | 液态池的实现 |
| 9 | Blinks与Actions | 可共享的交易功能 |

---

## Rust语言基础

### 所有权（难点）

```rust
// Each value has ONE owner
let s1 = String::from("hello");
let s2 = s1;  // s1 MOVED to s2
// println!("{}", s1);  // ERROR!

// Borrowing lets you use without owning
fn get_length(s: &String) -> usize {
    s.len()  // Borrow, don't own
}
```

### 结果与选择

```rust
// Result for errors
pub fn do_thing(ctx: Context<DoThing>) -> Result<()> {
    let value = some_operation().ok_or(ErrorCode::Failed)?;
    Ok(())
}

// Option for nullable
let maybe: Option<u64> = Some(42);
let value = maybe.unwrap_or(0);  // Safe default
```

---

## Anchor框架

### 程序结构

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramId11111111111111111111111111111");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        ctx.accounts.my_account.data = data;
        ctx.accounts.my_account.authority = ctx.accounts.authority.key();
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 8 + 32,  // discriminator + u64 + Pubkey
    )]
    pub my_account: Account<'info, MyAccount>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub data: u64,
    pub authority: Pubkey,
}
```

### 账户约束与注意事项

```rust
// Initialize new account
#[account(init, payer = payer, space = 8 + SIZE)]
pub new_account: Account<'info, Data>,

// Mutable existing
#[account(mut)]
pub existing: Account<'info, Data>,

// Verify ownership
#[account(has_one = authority)]
pub owned: Account<'info, Data>,

// PDA with seeds
#[account(
    seeds = [b"vault", user.key().as_ref()],
    bump,
)]
pub vault: Account<'info, Vault>,

// Initialize PDA
#[account(
    init,
    payer = user,
    space = 8 + 64,
    seeds = [b"user", user.key().as_ref()],
    bump,
)]
pub user_data: Account<'info, UserData>,

// Close and reclaim rent
#[account(mut, close = recipient)]
pub closing: Account<'info, Data>,
```

### PDA（程序派生地址）

```rust
// PDAs are deterministic addresses with no private key
// Your program can "sign" for them

// Find PDA
let (pda, bump) = Pubkey::find_program_address(
    &[b"vault", user.key().as_ref()],
    &program_id,
);

// Sign with PDA in CPI
let seeds = &[b"vault", user.key().as_ref(), &[bump]];
let signer = &[&seeds[..]];

token::transfer(
    CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        Transfer { from, to, authority: vault },
        signer,
    ),
    amount,
)?;
```

---

## 常见错误与陷阱

### 1. Solana的账户模型与EVM不同
Solana程序是无状态的，所有数据都存储在账户中。

### 2. PDA没有私钥
PDA地址是从种子值（seed） deterministically 生成的，只有程序本身才能对其进行签名。

### 3. 每个代币都需要独立的账户
每个代币都需要在钱包中拥有自己的账户（即Token Account）。

### 4. 需要支付租金
账户需要消耗SOL才能正常运行。免租金的账户可以在创建后两年内无需支付租金（大约0.002 SOL）。

### 5. “计算单位”不等于“Gas”
默认的计算单位是200k SOL，最大值为140万SOL。如有需要，可以申请更多计算资源。

### 6. 账户空间包含标识符
在创建账户时，必须为Anchor框架添加8字节的标识符！

```rust
// WRONG
space = 8 + 32  // Forgot discriminator? NO!

// RIGHT
space = 8 + 8 + 32  // 8 (discriminator) + 8 (u64) + 32 (Pubkey)
```

### 7. 整数溢出问题
在处理数据时需要注意整数溢出。

### 8. Token-2022与SPL Token的区别
Token-2022使用独立的程序ID，使用时请确认使用的是哪种代币类型。

---

## 前端开发（Next.js）

### 连接钱包

```typescript
// Already configured in create-solana-dapp!
import { useWallet, useConnection } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';

function App() {
  const { publicKey } = useWallet();
  return (
    <>
      <WalletMultiButton />
      {publicKey && <p>Connected: {publicKey.toBase58()}</p>}
    </>
  );
}
```

### 调用其他程序

```typescript
import { Program, AnchorProvider, BN } from '@coral-xyz/anchor';

const program = new Program(idl, provider);

// Write
await program.methods
  .initialize(new BN(42))
  .accounts({
    myAccount: keypair.publicKey,
    authority: wallet.publicKey,
    systemProgram: SystemProgram.programId,
  })
  .signers([keypair])
  .rpc();

// Read
const account = await program.account.myAccount.fetch(pubkey);
console.log(account.data.toNumber());
```

---

## 代币标准

### SPL Token（基础类型）
```bash
spl-token create-token
spl-token create-account <MINT>
spl-token mint <MINT> 1000
```

### Token-2022（新类型）
支持转移钩子、保密传输、带有利息、不可转让等功能。

```bash
spl-token create-token --program-id TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb
```

### Metaplex NFT
遵循标准的NFT元数据格式，支持集合管理。

### 压缩NFT
使用Merkle树进行存储，100个NFT的存储成本约为100美元，而不是100万美元。

---

## 测试

```typescript
import * as anchor from '@coral-xyz/anchor';
import { expect } from 'chai';

describe('my-program', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.MyProgram;

  it('initializes', async () => {
    const account = anchor.web3.Keypair.generate();

    await program.methods
      .initialize(new anchor.BN(42))
      .accounts({ myAccount: account.publicKey })
      .signers([account])
      .rpc();

    const data = await program.account.myAccount.fetch(account.publicKey);
    expect(data.data.toNumber()).to.equal(42);
  });
});
```

---

## 部署程序

```bash
# Devnet
solana config set --url devnet
solana airdrop 2
anchor build && anchor deploy

# Mainnet (costs ~2-5 SOL)
solana config set --url mainnet-beta
anchor deploy --provider.cluster mainnet
```

---

## 安全性检查清单

- [ ] 所有签名者均已验证
- [ ] PDA地址已正确生成并经过验证
- [ ] 防止整数溢出问题
- [ ] 账户空间中已包含必要的标识符
- [ ] 考虑到了租金减免规则
- [ ] 租金已正确发送给指定接收者
- [ ] CPI（Contract Program Interface）中的签名者种子值正确
- [ ] 程序ID已在CPI中得到验证

---

## 参考资源

- [Anchor官方文档](https://book.anchor-lang.com/)
- [Solana开发手册](https://solanacookbook.com/)
- [Solana官方文档](https://solana.com/docs)
- [Metaplex开发文档](https://developers.metaplex.com/)
- [Solana测试环境](https://beta.solpg.io/)

---

*“他们把我放到了云端……但我其实想要的是森林。”* 🌲
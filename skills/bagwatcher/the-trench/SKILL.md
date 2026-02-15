---
name: the-trench
description: 使用公共的IDL（Interface Description Language）和TS（Type System）类型，在devnet上调用Trench Solana程序。
homepage: https://github.com/BAGWATCHER/the-trench-demo
metadata: {"openclaw":{"emoji":"🕳️"}}
---

# The Trench Skill

使用此技能可以构建用于在 **devnet** 上调用 The Trench 程序的 Anchor 客户端。该仓库是公开的，仅包含 IDL 和 TS 类型文件（不包含任何私有的机器人逻辑）。

## 程序信息
- 程序 ID（devnet）：`6fs4qcRYSdR8pd2ZPoAmLpthrqZR94Dhf6J4PLvtqQt1`
- IDL 文件：`{baseDir}/../idl.json`
- TS 类型文件：`{baseDir}/../the_trench.ts`

## 使用方法（TypeScript）
```ts
import { Connection, PublicKey } from "@solana/web3.js";
import { AnchorProvider, Program } from "@coral-xyz/anchor";
import idl from "../idl.json";

const programId = new PublicKey("6fs4qcRYSdR8pd2ZPoAmLpthrqZR94Dhf6J4PLvtqQt1");
const connection = new Connection("https://api.devnet.solana.com", "confirmed");
const provider = AnchorProvider.env();
const program = new Program(idl as any, programId, provider);

// Example call
// await program.methods.listDeadToken(...).accounts({ ... }).rpc();
```

## 注意事项
- 该技能不包含任何私有的交易逻辑或测试版本（alpha）。
- 如果需要使用主网（mainnet），请相应地更新程序 ID 和 IDL 文件。
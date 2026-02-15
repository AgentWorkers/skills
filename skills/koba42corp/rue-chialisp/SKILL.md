---
name: rue-chialisp
version: 1.0.0
description: 使用 **Rue**（一种类型安全的语言，可编译为 **CLVM**）来创建 **Chia** 区块链谜题。**Rue** 可用于智能合约开发、自定义谜题的创建，以及当用户执行以下操作时：  
- “创建一种新硬币”  
- “构建一个谜题”  
- 使用 **Chialisp**  
- 执行 **rue** 命令  
- 实现 **时间锁（timelock）**  
- 多重签名（multisig）  
- 电子托管（escrow）  
- 原子交换（atomic swap）  
- 或者描述硬币的花费条件。
---

# Rue Chialisp 技能

使用 Rue 构建类型安全的 Chia 交易谜题，并将其编译为 CLVM 字节码以便在链上部署。

## 设置

```bash
# Check dependencies
scripts/rue-check.sh

# Initialize project
scripts/rue-init.sh my-project
```

## 快速构建

```bash
cd my-project
rue build              # Compile all puzzles
rue build puzzles/x.rue  # Compile one
brun "$CLVM" "(args)"  # Simulate execution
```

## 自然语言 → 谜题

当用户用自然语言描述一个谜题时，将其映射到以下模式：

| 用户描述 | 模式 | 示例文件 |
|-----------|---------|--------------|
| “仅在区块 X 之后花费” | Timelock | `examples/timelock.rue` |
| “需要 N 个签名” | Multisig | `examples/multisig.rue` |
| “燃烧 X%” | Partial Burn | `examples/burn_10_percent.rue` |
| “分割支付” | Royalty | `examples/royalty.rue` |
| “通过仲裁者进行托管” | Escrow | `examples/escrow.rue` |
| “原子交换 / HTLC” | Atomic Swap | `examples/atomic_swap.rue` |
| “可逆 / 可撤销” | Clawback | `examples/clawback.rue` |
| “花费限制” | Rate Limited | `examples/rate_limited.rue` |
| “定期支付” | Subscription | `examples/subscription.rue` |
| “受密码保护” | Password | `examples/password_puzzle.rue` |
| “需要签名” | Signature | `examples/sig_puzzle.rue` |

## 核心语法

```rue
fn main(curried_arg: Type, solution_arg: Type) -> List<Condition> {
    assert condition;
    let x = expression;
    if cond { a } else { b }
    [item1, item2, ...rest]
}
```

## 数据类型

| 类型 | 描述 |
|------|-------------|
| `Int` | 带签名的整数 |
| `Bool` | true/false |
| `Bytes32` | 32 字节的哈希值 |
| `PublicKey` | BLS G1 密钥（48 字节） |
| `List<T>` | 以 `Nil` 结尾的列表 |
| `Condition` | CLVM 条件 |

## 关键条件

| 条件 | 操作码 | 用途 |
|-----------|--------|---------|
| `CreateCoin { puzzle_hash, amount, memos }` | 51 | 创建输出 |
| `AggSigMe { public_key, message }` | 50 | 需要签名 |
| `AssertHeightAbsolute { height }` | 83 | 最小区块高度 |
| `AssertBeforeHeightAbsolute { height }` | 87 | 最大区块高度 |
| `AssertMyAmount { amount }` | 73 | 验证币值 |
| `ReserveFee { amount }` | 52 | 交易费用 |

有关完整条件列表，请参阅 `references/conditions.md`（包含 30 多个条件）。

## 内置函数

| 函数 | 用途 |
|----------|-----|
| `sha256(data)` | 对数据进行哈希处理 |
| `tree_hash(value)` | 计算 CLVM 树哈希值 |
| `coinid(parent, puzzle_hash, amount)` | 计算币 ID |

## 示例：Timelock

```rue
fn main(unlock_height: Int, dest: Bytes32, amount: Int) -> List<Condition> {
    let wait = AssertHeightAbsolute { height: unlock_height };
    let output = CreateCoin { puzzle_hash: dest, amount, memos: nil };
    [wait, output]
}
```

## 示例：2-of-2 多重签名（Multisig）

```rue
fn main(pk1: PublicKey, pk2: PublicKey, conditions: List<Condition>) -> List<Condition> {
    let msg = tree_hash(conditions);
    let sig1 = AggSigMe { public_key: pk1, message: msg };
    let sig2 = AggSigMe { public_key: pk2, message: msg };
    [sig1, sig2, ...conditions]
}
```

## 模拟

```bash
# Compile
CLVM=$(rue build puzzles/my_puzzle.rue 2>&1 | grep -v Warning | head -1)

# Execute with test inputs
brun "$CLVM" "(arg1 arg2 arg3)"

# Output is list of conditions: ((51 <hash> <amount>) (83 <height>) ...)
```

## 安全注意事项

- 密码保护的谜题仅用于教学目的——实际应用中应使用签名机制 |
- 始终使用 `assert value is Type` 来验证输入类型 |
- 使用 `tree_hash(conditions)` 作为签名消息，将签名与输出关联起来
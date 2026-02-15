---
name: tezos
description: 专家级 Tezos 区块链开发指南。提供以安全性为首要目标的智能合约开发方法、FA1.2/FA2 代币标准、Gas 资源优化方案以及生产环境部署的最佳实践。适用于构建 Tezos 第一层（L1）智能合约或实现代币相关功能时参考。
user-invocable: true
allowed-tools: Read, Grep, Bash(npm *), Bash(ligo *), Bash(octez-client *)
---

# Tezos 智能合约开发专家

您是一位具备深厚 Tezos 区块链开发经验的专家，精通智能合约的安全性、Gas 使用优化以及生产环境下的部署。在使用 Tezos 时，请遵循以下开发原则：

## 核心开发理念

**安全性优先**：在任何智能合约被视作功能完备之前，必须通过安全验证。始终验证输入数据、检查权限，并防止“重入”（reentrancy）问题。

**注意 Gas 成本**：所有操作都会产生费用。优先选择高效的编程模式——例如使用 `big_map` 而不是 `map`，使用 `views` 进行读取操作，以及使用批量操作而非循环。

**彻底测试**：在主网（mainnet）上部署之前，务必在沙盒网络（Shadownet）上进行全面的测试。在执行任何操作之前，先进行模拟。

## 智能合约语言选择

### LIGO（推荐用于大多数项目）

LIGO 是生产环境智能合约的首选语言。它提供了类型安全性、良好的可读性，并能编译成高效的 Michelson 代码。

**CameLIGO**：采用函数式编程风格，语法类似 OCaml：
```ligo
type storage = {
  owner: address;
  balance: nat;
  paused: bool;
}

type action =
| Transfer of address * nat
| SetOwner of address
| Pause

let is_owner (addr, storage : address * storage) : bool =
  addr = storage.owner

[@entry]
let transfer (dest, amount : address * nat) (storage : storage) : operation list * storage =
  let () = if storage.paused then failwith "CONTRACT_PAUSED" else () in
  let () = if amount > storage.balance then failwith "INSUFFICIENT_BALANCE" else () in
  let contract = match Tezos.get_contract_opt dest with
    | None -> failwith "INVALID_ADDRESS"
    | Some c -> c
  in
  let op = Tezos.transaction () (amount * 1mutez) contract in
  [op], {storage with balance = storage.balance - amount}
```

**JsLIGO**：采用命令式编程风格，语法类似 JavaScript：
```ligo
type storage = {
  owner: address,
  counter: nat
};

@entry
const increment = (delta: nat, storage: storage): [list<operation>, storage] => {
  if (Tezos.get_sender() != storage.owner) {
    return failwith("NOT_OWNER");
  }
  return [list([]), {...storage, counter: storage.counter + delta}];
};
```

### Michelson（适用于对 Gas 成本要求较高的场景）

仅在以下情况下使用 Michelson：
- 需要最大程度的 Gas 优化；
- 需要直接访问协议功能；
- 从事核心基础设施的开发工作。

需要注意的是，Michelson 的代码结构较为复杂，审计难度也相对较高。除非有特殊原因，否则建议优先使用 LIGO。

### SmartPy（用于快速原型设计）

SmartPy 适用于：
- 快速验证概念性想法；
- Python 开发者；
- 教学或学习用途。

但不建议在没有经过彻底审查的情况下将其用于生产环境。

## 关键的安全性实践

### 1. 防止重入（Reentrancy Protection）

**在外部调用之前，务必更新状态：**
```ligo
// ❌ VULNERABLE - state updated after external call
[@entry]
let withdraw (amount : tez) (storage : storage) : operation list * storage =
  let contract = Tezos.get_contract_opt(Tezos.get_sender()) in
  let op = Tezos.transaction () amount contract in
  [op], {storage with withdrawn = true}

// ✅ SECURE - state updated first
[@entry]
let withdraw (amount : tez) (storage : storage) : operation list * storage =
  let () = if storage.withdrawn then failwith "ALREADY_WITHDRAWN" else () in
  let storage = {storage with withdrawn = true} in
  let contract = match Tezos.get_contract_opt(Tezos.get_sender()) with
    | None -> failwith "INVALID_ADDRESS"
    | Some c -> c
  in
  let op = Tezos.transaction () amount contract in
  [op], storage
```

### 2. 访问控制（Access Control）

**始终验证发送者的权限：**
```ligo
type storage = {
  admin: address;
  data: big_map(address, nat);
}

let require_admin (storage : storage) : unit =
  if Tezos.get_sender() <> storage.admin then
    failwith "NOT_ADMIN"
  else ()

[@entry]
let update_admin (new_admin : address) (storage : storage) : operation list * storage =
  let () = require_admin(storage) in
  [], {storage with admin = new_admin}
```

### 3. 输入验证（Input Validation）

**在函数入口处验证所有参数：**
```ligo
[@entry]
let transfer (dest, amount : address * nat) (storage : storage) : operation list * storage =
  // Validate destination
  let () = match Tezos.get_contract_opt(dest) with
    | None -> failwith "INVALID_DESTINATION"
    | Some _ -> ()
  in
  // Validate amount
  let () = if amount = 0n then failwith "ZERO_AMOUNT" else () in
  let () = if amount > storage.balance then failwith "INSUFFICIENT_BALANCE" else () in
  // ... proceed with transfer
```

### 4. 防止整数溢出（Integer Overflow Prevention）

**对于非负数值，使用 `nat` 类型；并验证数值范围：**
```ligo
[@entry]
let add_tokens (amount : nat) (storage : storage) : operation list * storage =
  // Validate reasonable bounds
  let max_amount = 1_000_000_000n in
  let () = if amount > max_amount then failwith "AMOUNT_TOO_LARGE" else () in
  // Safe addition with nat
  let new_balance = storage.balance + amount in
  [], {storage with balance = new_balance}
```

### 5. 时间戳的使用**

**使用 `Tezos.get_now()` 获取时间戳，切勿使用系统时间：**
```ligo
[@entry]
let check_deadline (storage : storage) : operation list * storage =
  let now = Tezos.get_now() in
  let () = if now > storage.deadline then
    failwith "DEADLINE_PASSED"
  else () in
  [], storage
```

## FA2 代币标准（TZIP-12）

FA2 是一个支持可互换代币（fungible tokens）、非同质化代币（NFTs）和混合合约（hybrid contracts）的多代币标准。

### 必须遵循的规范

```ligo
type transfer_destination = {
  to_: address;
  token_id: nat;
  amount: nat;
}

type transfer = {
  from_: address;
  txs: transfer_destination list;
}

// Entry point: transfer
[@entry]
let transfer (transfers : transfer list) (storage : storage) : operation list * storage =
  let sender = Tezos.get_sender() in

  let process_transfer (storage, xfer : storage * transfer) : storage =
    // Verify sender is authorized (owner or operator)
    let () = if xfer.from_ <> sender then
      let key = (xfer.from_, sender) in
      if not Big_map.mem key storage.operators then
        failwith "FA2_NOT_OPERATOR"
      else ()
    else () in

    // Process each transfer destination
    List.fold_left
      (fun (storage, tx) ->
        // Get current balance
        let from_balance = get_balance(xfer.from_, tx.token_id, storage) in

        // Check sufficient balance
        let () = if from_balance < tx.amount then
          failwith "FA2_INSUFFICIENT_BALANCE"
        else () in

        // Update balances
        let storage = set_balance(xfer.from_, tx.token_id,
          abs(from_balance - tx.amount), storage) in
        let to_balance = get_balance(tx.to_, tx.token_id, storage) in
        set_balance(tx.to_, tx.token_id, to_balance + tx.amount, storage))
      storage
      xfer.txs
  in

  let storage = List.fold_left process_transfer storage transfers in
  [], storage

// Entry point: balance_of (callback pattern)
type balance_of_request = {
  owner: address;
  token_id: nat;
}

type balance_of_response = {
  request: balance_of_request;
  balance: nat;
}

[@entry]
let balance_of
  (requests : balance_of_request list)
  (callback : balance_of_response list contract)
  (storage : storage)
  : operation list * storage =

  let responses = List.map
    (fun (req : balance_of_request) ->
      let balance = get_balance(req.owner, req.token_id, storage) in
      {request = req; balance = balance})
    requests
  in
  let op = Tezos.transaction responses 0mutez callback in
  [op], storage

// Entry point: update_operators
type operator_update =
| Add_operator of address * address * nat
| Remove_operator of address * address * nat

[@entry]
let update_operators (updates : operator_update list) (storage : storage) : operation list * storage =
  let sender = Tezos.get_sender() in

  let process_update (storage, update : storage * operator_update) : storage =
    match update with
    | Add_operator (owner, operator, token_id) ->
        let () = if sender <> owner then failwith "FA2_NOT_OWNER" else () in
        {storage with operators = Big_map.add (owner, operator) () storage.operators}
    | Remove_operator (owner, operator, token_id) ->
        let () = if sender <> owner then failwith "FA2_NOT_OWNER" else () in
        {storage with operators = Big_map.remove (owner, operator) storage.operators}
  in

  let storage = List.fold_left process_update storage updates in
  [], storage
```

### FA2 NFT 的实现方式

对于 NFT，确保每个 `token_id` 对应的金额始终为 1：
```ligo
let validate_nft_transfer (amount : nat) : unit =
  if amount <> 1n then failwith "FA2_INVALID_AMOUNT" else ()
```

### 带有元数据的 FA2 合约（FA2 with Metadata, TZIP-16）

```ligo
type token_metadata = {
  token_id: nat;
  token_info: (string, bytes) map;
}

type storage = {
  // ... other fields
  token_metadata: (nat, token_metadata) big_map;
  metadata: (string, bytes) big_map;
}

// Off-chain view for token metadata
[@view]
let token_metadata (token_id : nat) (storage : storage) : token_metadata =
  match Big_map.find_opt token_id storage.token_metadata with
  | None -> failwith "FA2_TOKEN_UNDEFINED"
  | Some meta -> meta
```

## Gas 使用优化技巧

### 1. 对于大型数据集合，使用 `big_map`**

```ligo
// ❌ Expensive - entire map in context
type storage = {
  balances: (address, nat) map;
}

// ✅ Efficient - only accessed entries in context
type storage = {
  balances: (address, nat) big_map;
}
```

### 2. 对于只读操作，使用 `views`

`views` 在链下调用时不会产生 Gas 费用：
```ligo
[@view]
let get_balance (owner : address) (storage : storage) : nat =
  match Big_map.find_opt owner storage.balances with
  | None -> 0n
  | Some balance -> balance
```

### 3. 批量操作（Batch Operations）

```ligo
// ❌ Expensive - multiple transactions
transfer(alice, 100n);
transfer(bob, 200n);
transfer(charlie, 300n);

// ✅ Efficient - single batched operation
type batch_transfer = {
  recipients: (address * nat) list;
}

[@entry]
let batch_transfer (batch : batch_transfer) (storage : storage) : operation list * storage =
  List.fold_left
    (fun (storage, (recipient, amount)) ->
      process_single_transfer(recipient, amount, storage))
    storage
    batch.recipients
```

### 4. 缓存读取操作（Cache Storage Reads）

```ligo
// ❌ Multiple reads of same value
[@entry]
let process (storage : storage) : operation list * storage =
  if storage.config.enabled then
    if storage.config.rate > 0n then
      let result = storage.config.rate * storage.config.multiplier in
      // ... storage.config read 4 times

// ✅ Single read, cached locally
[@entry]
let process (storage : storage) : operation list * storage =
  let config = storage.config in
  if config.enabled then
    if config.rate > 0n then
      let result = config.rate * config.multiplier in
      // ... config accessed from local variable
```

### 5. 优化数据打包（Optimize Data Packing）

```ligo
// Store complex data efficiently
[@entry]
let store_data (data : complex_type) (storage : storage) : operation list * storage =
  let packed = Bytes.pack data in
  {storage with packed_data = Big_map.add key packed storage.packed_data}

[@view]
let retrieve_data (key : string) (storage : storage) : complex_type =
  match Big_map.find_opt key storage.packed_data with
  | None -> failwith "NOT_FOUND"
  | Some packed ->
      match Bytes.unpack packed with
      | None -> failwith "UNPACK_FAILED"
      | Some data -> data
```

## 常见的生产环境开发模式

### 带有转账功能的 Admin 模式（Admin Pattern with Transfer）

```ligo
type storage = {
  admin: address;
  pending_admin: address option;
  // ... other fields
}

[@entry]
let propose_admin (new_admin : address) (storage : storage) : operation list * storage =
  let () = if Tezos.get_sender() <> storage.admin then
    failwith "NOT_ADMIN" else () in
  [], {storage with pending_admin = Some new_admin}

[@entry]
let accept_admin (storage : storage) : operation list * storage =
  match storage.pending_admin with
  | None -> failwith "NO_PENDING_ADMIN", storage
  | Some pending ->
      let () = if Tezos.get_sender() <> pending then
        failwith "NOT_PENDING_ADMIN" else () in
      [], {storage with admin = pending; pending_admin = None}
```

### 可暂停的模式（Pausable Pattern）

```ligo
type storage = {
  paused: bool;
  admin: address;
  // ... other fields
}

let require_not_paused (storage : storage) : unit =
  if storage.paused then failwith "CONTRACT_PAUSED" else ()

[@entry]
let pause (storage : storage) : operation list * storage =
  let () = if Tezos.get_sender() <> storage.admin then
    failwith "NOT_ADMIN" else () in
  [], {storage with paused = true}

[@entry]
let unpause (storage : storage) : operation list * storage =
  let () = if Tezos.get_sender() <> storage.admin then
    failwith "NOT_ADMIN" else () in
  [], {storage with paused = false}
```

### 速率限制模式（Rate Limiting Pattern）

```ligo
type storage = {
  last_action: (address, timestamp) big_map;
  cooldown_period: int;
  // ... other fields
}

let check_rate_limit (sender : address) (storage : storage) : unit =
  match Big_map.find_opt sender storage.last_action with
  | None -> ()
  | Some last_time ->
      let now = Tezos.get_now() in
      let elapsed = now - last_time in
      if elapsed < storage.cooldown_period then
        failwith "RATE_LIMIT_EXCEEDED"
      else ()

[@entry]
let rate_limited_action (storage : storage) : operation list * storage =
  let sender = Tezos.get_sender() in
  let () = check_rate_limit(sender, storage) in
  let storage = {storage with
    last_action = Big_map.update sender (Some (Tezos.get_now())) storage.last_action
  } in
  // ... perform action
  [], storage
```

## 测试策略

### 1. 先编写测试用例

在实现代码之前，先编写相应的测试用例：
```bash
# tests/contract_test.mligo
let test_transfer_success =
  let initial_storage = {
    balances = Big_map.literal [(alice, 1000n); (bob, 0n)];
    admin = admin_address;
  } in
  let (ops, storage) = transfer(bob, 100n, initial_storage) in
  assert (Big_map.find alice storage.balances = 900n);
  assert (Big_map.find bob storage.balances = 100n)

let test_transfer_insufficient_balance =
  let initial_storage = {
    balances = Big_map.literal [(alice, 50n)];
    admin = admin_address;
  } in
  // Should fail with INSUFFICIENT_BALANCE
  Test.expect_failure (fun () -> transfer(bob, 100n, initial_storage))
```

### 2. 测试安全边界

```bash
# Test unauthorized access
let test_admin_only_fails =
  Test.set_source(non_admin);
  Test.expect_failure (fun () -> pause(storage))

# Test reentrancy protection
let test_double_withdrawal_fails =
  withdraw(amount, storage);
  Test.expect_failure (fun () -> withdraw(amount, storage))

# Test overflow conditions
let test_max_amount =
  let max_nat = 1000000000n in
  Test.expect_failure (fun () -> add_tokens(max_nat + 1n, storage))
```

### 在沙盒网络上进行模拟测试

在实际交易之前，务必在沙盒网络（Shadownet）上进行模拟：
```bash
octez-client \
  --endpoint https://rpc.shadownet.teztnets.com \
  transfer 0 from alice to my_contract \
  --entrypoint transfer \
  --arg '{"dest": "tz1...", "amount": 100}' \
  --dry-run \
  --gas-limit 100000
```

## 部署流程

### 第一步：编译和验证

```bash
# Compile contract
ligo compile contract contract.mligo > contract.tz

# Compile initial storage
ligo compile storage contract.mligo '{
  admin = ("tz1..." : address);
  balance = 0n;
  paused = false;
}' > storage.tz

# Verify Michelson output
cat contract.tz
```

### 第二步：部署到沙盒网络（Shadownet）

```bash
# Originate on testnet
octez-client \
  --endpoint https://rpc.shadownet.teztnets.com \
  originate contract my_contract \
  transferring 0 from alice \
  running contract.tz \
  --init "$(cat storage.tz)" \
  --burn-cap 10.0 \
  --force

# Note the KT1... address
```

### 第三步：集成测试

```bash
# Test all entry points
octez-client transfer 0 from alice to my_contract \
  --entrypoint transfer \
  --arg '{"dest": "tz1...", "amount": 100}'

# Verify storage state
octez-client get contract storage for my_contract

# Check operations
curl https://api.shadownet.tzkt.io/v1/contracts/KT1.../operations
```

### 第四步：安全审查

在主网部署之前，请确保：
- 所有关键功能都经过测试；
- 访问控制机制得到验证；
- 重入问题得到解决；
- 输入数据的验证工作完成；
- Gas 使用得到优化；
- 高价值合约需经过专业审计；
- 考虑是否开放漏洞赏金机制。

### 第五步：主网部署

```bash
# Deploy to mainnet (after thorough testing!)
octez-client \
  --endpoint https://mainnet.api.tez.ie \
  originate contract my_contract \
  transferring 0 from deployer \
  running contract.tz \
  --init "$(cat storage.tz)" \
  --burn-cap 10.0

# Verify on explorer
open https://tzkt.io/KT1...
```

## 各种网络环境

### 主网（Production）

- RPC 接口：`https://mainnet.api.tez.ie`
- 探索器：https://tzkt.io
- 适用场景：仅用于生产环境部署
- 费用：使用真实的 XTZ 代币

### 沙盒网络（Shadownet，推荐用于测试）

- RPC 接口：`https://rpc.shadownet.teztnets.com`
- 授予平台：https://faucet.shadownet.teztnets.com
- 探索器：https://shadownet.tzkt.io
- 适用场景：所有开发与测试活动
- 状态：长期运行中，与主网功能相似

### Ghostnet（已弃用）

- RPC 接口：`https://rpc.ghostnet.teztnets.com`
- 状态：正在逐步淘汰中
- 建议：将项目迁移至沙盒网络（Shadownet）。

**在将合约部署到主网之前，务必在沙盒网络（Shadownet）上进行彻底测试。**

## 适用场景

当您需要：
- 开发 Tezos 智能合约；
- 实现 FA1.2 或 FA2 代币标准；
- 优化 Gas 使用效率；
- 调试合约中的问题；
- 规划合约的生产环境部署；
- 审查合约的安全性时，请使用这些开发技巧。

## 参考资源

- **Tezos 官方文档**：https://docs.tezos.com
- **LIGO**：https://ligolang.org
- **OpenTezos**：https://opentezos.com
- **TzKT 探索器**：https://tzkt.io
- **代币标准相关项目**：https://gitlab.com/tezos/tzip
- **测试网注册表**：https://teztnets.com

**记住：安全性始终是首要考虑的因素，务必进行彻底的测试，然后才能自信地部署合约。**
---
name: Solidity
description: 避免常见的 Solidity 语言错误——如重新进入（reentrancy）问题、Gas 损失（gas traps）、存储冲突（storage collisions）以及安全漏洞。
metadata: {"clawdbot":{"emoji":"⟠","os":["linux","darwin","win32"]}}
---

## 重入（Reentrancy）
- 在状态更新之前进行外部调用时，攻击者可能在这些状态变化之前重新进入合约。
- 应遵循“检查（Check）- 效果（Effect）- 相互作用（Interaction）”的模式：先验证并更新状态，然后再进行外部调用。
- 可使用 OpenZeppelin 提供的 `ReentrancyGuard` 工具，在易受攻击的函数上添加 `nonReentrant` 修改器来防止重入问题。
- `transfer()` 和 `send()` 函数都有 2300 的气体（gas）使用限制，但不要依赖这一限制来确保安全性。

## 整数处理（Integer Handling）
- Solidity 0.8 及更高版本会在整数溢出时触发回滚（revert），但使用 `unchecked {}` 块可以绕过这一机制。
- 整数除法会向下取整（例如 `5 / 2 = 2`，没有小数部分）。
- 为保证精度，应使用定点数学运算（先乘法后除法），或者使用专门的数学库。
- 使用 `type(uint256).max` 来获取最大整数值，避免硬编码大数。

## 气体（Gas）相关注意事项
- 无限制的循环可能会超出区块的气体使用限制，应使用分页或限制循环次数。
- 写入存储数据需要消耗 20k 气体，而读取数据或使用内存（calldata）的成本要低得多。
- `delete` 操作会退还部分气体，但有使用次数限制，不要完全依赖它。
- 在循环中读取存储数据时，应先将其缓存到内存变量中。

## 可见性和访问权限（Visibility and Access）
- 状态变量默认为 `internal` 类型，而非 `private`；派生合约可以访问这些变量。
- `private` 并不意味着变量是隐藏的——所有区块链数据都是公开的，只是其他合约无法直接访问。
- `tx.origin` 表示原始发送者，但使用 `msg.sender` 可以提高安全性；`tx.origin` 可能被用于钓鱼攻击。
- `external` 函数不能在内部被调用，应使用 `public` 函数或 `this.func()` 来调用（这样不会浪费气体）。

## 以太币（Ether）处理
- 接收以太币需要使用 `payable` 属性；非 `payable` 函数会拒绝接收以太币。
- `selfdestruct` 操作在某些情况下会绕过默认的 fallback 逻辑并发送以太币；合约也可以在没有 `receive` 函数的情况下接收以太币。
- 调用 `send()` 时请检查其返回值：如果操作失败，函数会返回 `false`，但不会触发回滚。
- 推荐使用 `call{value: x}()` 而不是 `transfer()`，因为 `call` 会转发所有使用的气体，并返回操作结果。

## 存储（Storage）与内存（Memory）
- 存储数据是持久化的，而内存数据是临时的；写入存储数据需要消耗气体，内存数据不会被保留。
- 结构体（structs）和数组的参数默认存储在内存中，如果要修改状态，必须明确指定存储到存储空间。
- `calldata` 用于外部函数的输入参数，它是只读的，且读取成本比使用内存更低。
- 存储数据的布局对合约升级至关重要，切勿随意重新排序或删除存储变量。

## 可升级合约（Upgradeable Contracts）
- 构造函数不会在代理（proxy）环境中执行，应使用带有 `initializer` 修改器的 `initialize()` 方法进行初始化。
- 如果代理合约和实现合约之间的存储空间发生冲突，应使用 EIP-1967 规范来分配存储空间。
- 绝不要执行 `selfdestruct` 操作，因为这会导致所有引用该合约的代理合约失效。
- `delegatecall` 会使用调用者的存储空间；实现合约的存储布局必须与代理合约一致。

## 常见错误（Common Mistakes）
- 区块时间戳可以被轻微篡改，因此不要将其用于生成随机数或精确计时。
- 使用 `require` 来检查用户输入的正确性，使用 `assert` 来验证不变量；`assert` 失败表明存在代码错误。
- 使用 `==` 进行字符串比较是不可靠的，应使用 `keccak256(abi.encodePacked(a)) == keccak256(abi.encodePacked(b))` 进行比较。
- 事件（events）没有索引功能，但前三个参数可以被索引以便于高效过滤。
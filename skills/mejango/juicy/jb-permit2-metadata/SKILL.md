---
name: jb-permit2-metadata
description: 使用 JBMetadataResolver 为 Juicebox V5 终端支付编码元数据。该方案支持 Permit2 类型的无 gas ERC20 支付、721 层级的选择功能，以及多种元数据类型的组合。适用于以下情况：出现 “AllowanceExpired” 错误、元数据提取结果为零、需要指定用于 mint 的 NFT 层级，或者在调用 getDataFor 时 Tenderly 返回 “exists false” 的情况。
---

# JBMetadataResolver：支付元数据编码

## 概述

Juicebox V5 使用 `JBMetadataResolver` 通过 `pay()`, `addToBalance()` 等终端函数的 `metadata` 参数传递结构化数据。多个扩展程序（如 Permit2、721 Hook、回购 Hook 等）可以通过查找表格式从同一个元数据块中读取它们所需的数据。

**关键概念**：每个扩展程序都有一个唯一的 4 字节 ID。元数据中包含一个查找表，将 ID 映射到数据偏移量，使得每个扩展程序无需了解其他扩展程序的存在即可找到自己的数据。

## 何时使用此功能

- 通过 Permit2 实现无 gas 的 ERC20 支付（单次交易用户体验）
- 在支付 721 Hook 项目时指定要铸造的 NFT 等级
- 当从 Permit2 合同收到 “AllowanceExpired” 错误时
- 在调用 `getDataFor` 时返回 `exists: false` 或全零的结果
- 在一次支付中结合多种元数据类型（例如，Permit2 + 等级选择）

## 重要规则：使用官方库

**始终使用 `juicebox-metadata-helper` 来构建元数据。** 手动构建元数据可能存在细微的错误：

---

## 元数据类型 1：Permit2（无 gas 的 ERC20 支付）

Permit2 允许进行单次交易的 ERC20 支付，无需额外的批准交易。

### 交换终端注册表

有两个交换终端注册表，它们部署在所有链路的相同地址上：

| 注册表 | 地址 | TOKEN_OUT | 用途 |
|----------|---------|-----------|---------|
| **JBSwapTerminalRegistry** | `0x60b4f5595ee509c4c22921c7b7999f1616e6a4f6` | NATIVE_TOKEN (ETH) | 将传入的代币兑换为 ETH |
| **JBSwapTerminalUSDCRegistry** | `0x1ce40d201cdec791de05810d17aaf501be167422` | USDC | 将传入的代币兑换为 USDC |

**选择注册表时，请根据项目交换后应接收的货币类型来决定，而不是用户支付的货币类型。**

### 第 1 步：计算 Permit2 元数据 ID

**重要提示**：使用 ethers.js 来计算 ID。Viem 的字节处理方式在 XOR 操作中可能存在细微问题。

---

### 第 2 步：编码 JBSingleAllowance 结构

**重要提示**：必须以元组（TUPLE）的形式进行编码，而不能作为单独的参数！

---

### 第 3 步：构建 Permit2 元数据

---

### 第 4 步：签署 Permit2 消息

---

### 完整的 Permit2 支付流程

---

## 元数据类型 2：721 Hook（NFT 等级选择）

在支付使用 721 Hook 的项目时，您可以指定要铸造的 NFT 等级。

### 721 Hook 元数据 ID

与 Permit2 不同，721 Hook 的 ID 不是与合约地址进行 XOR 运算得到的，而是一个静态 ID：

---

### 721 Hook 数据格式

数据负载包括：
1. `allowOverspending`（布尔值）- 如果为 true，超出等级价格的支付金额将用于铸造 NFT
2. `tierIds`（uint16[]）- 需要铸造的等级 ID 数组

---

### 构建 721 Hook 元数据

---

### 示例：铸造特定 NFT 等级

---

### `allowOverspending` 的解释

| `allowOverspending` | 行为 |
|---------------------|----------|
| `true` | 如果支付金额超过等级价格，则铸造项目 NFT |
| `false` | 如果支付金额与等级价格完全匹配，则不进行任何操作 |

**示例**：如果等级 1 的价格为 0.1 ETH，且您设置了 `allowOverspending: true` 并支付了 0.5 ETH：
- 您将获得 1 个等级 1 的 NFT
- 剩余的 0.4 ETH 将用于铸造项目 NFT

---

## 结合多种元数据类型

您可以在一次支付中同时包含 Permit2 和 721 Hook 的数据！

---

## 调试指南

### 在 Tenderly 日志中看到 `exists: false`

**问题**：元数据 ID 未在查找表中找到。

**对于 Permit2**：
1. 确保使用 ethers.js 来计算 ID（而不是 viem 的字节数组）
2. 确认终端地址与 `primaryTerminalOf` 返回的地址一致
3. 记录计算出的 ID 并与合约期望的 ID 进行比较

**对于 721 Hook**：
1. 确保使用 `keccak256("JB721TiersHook")` 而不是其他函数
2. 检查该 Hook 是否已为该项目正确部署

### `exists: true` 但解码后的值为零或数据位置错误

**问题**：元数据格式不正确——数据位置错误。

**解决方案**：
1. 使用 `juicebox-metadata-helper` 库而不是手动构建元数据
2. 在将数据传递给库之前确保其长度为 32 字节
3. 确保偏移量是以“字”（WORD）为单位，而不是字节（byte）

### 解码后的 `sigDeadline` 值错误（例如显示为 288）

**问题**：合约读取的是数据长度而不是实际的数据。

**解决方案**：这表明偏移量或格式有误。请使用官方库。

### 错误：“Called function does not exist in the contract” 在 abi.decode 时出现

**问题**：JBSingleAllowance 被编码为单独的参数，而不是元组。

**解决方案**：请使用正确的元组编码方式：

---

### 721 Hook：尽管元数据正确，但未铸造 NFT

**检查**：
1. 支付金额是否覆盖了等级价格
2. 相应等级的剩余供应量是否大于 0
3. 该等级是否未暂停铸造
4. 项目是否配置了 721 Hook 作为数据钩子

---

## 常见错误

### Permit2
1. **使用单独的参数而不是元组**：必须将 JBSingleAllowance 编码为元组类型
2. **手动构建元数据**：可能存在细微错误。始终使用 `juicebox-metadata-helper`
3. **使用 viem 计算 ID**：请使用 ethers.js 的 `BigInteger.xor()` 方法
4. **使用错误的终端地址**：必须使用 `primaryTerminalOf` 返回的终端地址
5. **偏移量单位错误**：偏移量应以“字”（WORD）为单位，而不是字节（byte）
6. **缺少填充**：数据必须填充到 32 字节的边界
7. **支付方错误**：Permit2 的支付方必须是终端地址

### 721 Hook
1. **使用 XOR 计算 Hook ID**：721 Hook 使用的是静态 ID，而不是与地址进行 XOR 运算
2. **等级 ID 类型错误**：必须使用 uint16[]，而不是 uint256[]
3. **缺少 `allowOverspending` 字段**：这两个字段都是必需的
4. **支付金额不足**：除非设置了 `allowOverspending`，否则支付金额必须覆盖所有等级的价格

---

## 验证

### 检查元数据 ID 是否匹配

**Permit2**：终端使用 `JBMetadataResolver.getId("permit2")`，该函数会将 ID 与合约地址进行 XOR 运算

**721 Hook**：使用 `bytes4(keccak256("JB721TiersHook"))`——这是一个静态 ID，不需要进行 XOR 运算

### 在 Tenderly 日志中

- `getDataFor()` 应返回 `(true, <非零数据>)`
- 如果 `exists: false`，则说明 ID 计算有误
- 如果 `exists: true` 但数据错误，说明格式不正确（请使用官方库！）

---

## 参考资料

- [JBMetadataResolver.sol](https://github.com/Bananapus/nana-core-v5/blob/main/src/libraries/JBMetadataResolver.sol)
- [JBSingleAllowance.sol](https://github.com/Bananapus/nana-core-v5/blob/main/src/structs/JBSingleAllowance.sol)
- [JB721TiersHook.sol](https://github.com/Bananapus/nana-721-hook/blob/main/src/JB721TiersHook.sol)
- [TestPermit2Terminal5_1.sol](https://github.com/Bananapus/nana-core-v5/blob/main/test/TestPermit2Terminal5_1.sol)
- [Permit2 AllowanceTransfer](https://github.com/Uniswap/permit2)
- [juicebox-metadata-helper](https://www.npmjs.com/package/juicebox-metadata-helper)
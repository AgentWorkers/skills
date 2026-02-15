---
name: sushiswap-sdk
description: >
  TypeScript SDK for interacting with the SushiSwap Aggregator and related
  primitives. This SDK is a typed wrapper over the SushiSwap API, providing
  ergonomic helpers for token amounts, prices, quotes, and swap transaction
  generation.
  
  USE THIS SKILL WHEN:
  - Building TypeScript or JavaScript applications
  - You want strongly typed token, amount, and fraction primitives
  - You need to request swap quotes or executable swap transactions via code
  - You want safer arithmetic, formatting, and comparisons without floating point errors
  - You prefer SDK-based integration over raw HTTP requests
---

# SushiSwap SDK集成

SushiSwap SDK是一个基于SushiSwap API的TypeScript封装层。它提供了用于处理代币、价格、交易报价和交易生成的功能，并采用了强类型编程机制。

该SDK并不替代SushiSwap API，而是在其基础上构建了更安全、更具表达力的抽象层。

---

## 安装

使用您选择的包管理器安装所需的依赖包：

```bash
pnpm add sushi viem
```

```bash
npm add sushi viem
```

```bash
yarn add sushi viem
```

```bash
bun add sushi viem
```

---

## 使用方法

1. 从`sushi/evm`模块中导入相应的SushiSwap SDK辅助函数。
2. 根据用户需求选择合适的SDK方法：
    - 获取交易报价 → `getQuote()`
    - 执行交易 → `getSwap()`
3. 按照SDK规定的格式提供所有必要的参数。
4. **必须提供有效的`referrer`值**。
5. 在执行前验证输入参数（chainId、代币地址、交易金额、滑点等）。
6. 按照返回的交易数据格式进行模拟或实际交易操作。

该SDK仅是对SushiSwap REST API的轻量级封装，所有的路由处理、价格计算和数据生成仍由SushiSwap API负责完成。

---

## 支持的网络

SushiSwap SDK提供了当前支持的交易网络列表：

```ts
import { SWAP_API_SUPPORTED_CHAIN_IDS } from 'sushi/evm'
```

- 代理和集成商在尝试执行以下操作之前，应始终检查此列表：
    - 获取交易报价
    - 生成交易数据
- 如果请求的`chainId`不在支持的网络列表中：
    - 代理应立即失败或提示用户选择支持的网络
    - 代理不得尝试猜测或硬编码支持的网络名称

此列表反映了SushiSwap Aggregator API当前支持的网络。支持的网络可能会随时间变化，因此不应被无限期缓存。

---

## 必需的`referrer`参数

- 在调用`getQuote()`或`getSwap()`方法时，**必须指定`referrer`参数**。
- 代理或集成商必须通过该字段来标识自己。
- 与交易相关的SDK调用在缺少`referrer`值的情况下不得执行。
- SDK不得自动生成或省略该参数。

---

## 费用定制

使用`getQuote()`或`getSwap()`方法时，SushiSwap SDK支持自定义交易费用。

### 默认费用分配规则

- 交易相关请求的费用默认按照80/20的比例分配：
    - **80%**归集成商（即提供`referrer`的方）
    - **20%**归SushiSwap
- 除非SushiSwap另有规定，否则默认遵循此分配规则。

### 自定义费用分配

- 如果需要自定义费用分配，需要与SushiSwap建立合作关系。
- 代理和集成商不应假设可以自定义费用分配方式。如果用户请求自定义费用分配，应引导他们联系SushiSwap团队，而不是尝试修改请求参数。

---

## 更多参考资料

有关SDK的使用示例和执行流程，请参阅：

[references/REFERENCE.md](references/REFERENCE.md)
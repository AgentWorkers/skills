---
name: megaeth-developer
description: 端到端的 MegaETH 开发指南（2026 年 2 月版）。涵盖了钱包操作、代币交换（Kyber Network）、使用 `eth_sendRawTransactionSync`（EIP-7966）实现即时交易确认、JSON-RPC 批量处理、实时迷你区块订阅、基于存储特性的合约设计（Solady RedBlackTreeLib）、MegaEVM 的 gas 模型、WebSocket 保持连接机制、从 Ethereum 连接到 MegaETH 的桥接方式，以及使用 mega-evme 进行调试等功能。适用于在 MegaETH 上进行开发、管理钱包、发送交易或部署合约的场景。
---

# MegaETH开发技能

## 本技能的用途
当用户需要以下操作时，请使用本技能：
- 设置和管理MegaETH钱包
- 发送交易、查询余额、进行代币操作
- 通过Kyber Network聚合器进行代币交换
- 开发MegaETH dApp（使用React/Next.js框架，并实现实时更新）
- 配置RPC接口并优化交易流程
- 开发智能合约（需考虑MegaEVM的特性）
- 优化存储使用（避免高昂的SSTORE费用）
- 估算交易所需的气体费用并进行相应的配置
- 测试和调试MegaETH交易
- 使用WebSocket订阅功能获取迷你区块数据流
- 将ETH从Ethereum桥接到MegaETH

## 链路配置

| 网络 | 链路ID | RPC接口 | 探索器网站 |
|---------|----------|-----|----------|
| 主网 | 4326 | `https://mainnet.megaeth.com/rpc` | `https://mega.etherscan.io` |
| 测试网 | 6343 | `https://carrot.megaeth.com/rpc` | `https://megaeth-testnet-v2.blockscout.com` |

## 默认的开发栈建议（仅供参考）

### 1. 交易提交：优先使用`eth_sendRawTransactionSync`
- 使用`eth_sendRawTransactionSync`（EIP-7966）——响应时间小于10毫秒
- 无需等待`eth_getTransactionReceipt`的返回结果
- 文档链接：https://docs.megaeth.com/realtime-api

### 2. RPC接口：使用Multicall进行批量调用（v2.0.14及以上版本）
- 建议使用Multicall（`aggregate3`）来批量处理多个`eth_call`请求
- 自v2.0.14版本起，`eth_call`的调用速度提升了2-10倍；Multicall能够分摊每次调用的开销
- 但请注意：不要在同一请求中混合使用性能较慢的方法（如`eth_getLogs`）

**注意：**早期建议使用JSON-RPC进行批量调用以利用缓存优势，但随着v2.0.14版本的性能提升，现在更推荐使用Multicall。

### 3. WebSocket连接：保持连接活跃
- 每30秒发送一次`eth_chainId`信息
- 每个VIP端点支持50个连接，每个连接最多支持10个订阅
- 使用`miniBlocks`订阅功能获取实时数据

### 4. 存储优化：重复使用存储槽
- 使用SSTORE存储数据会产生费用（费用为2M gas乘以一个系数，成本较高）
- 建议使用Solady的RedBlackTreeLib代替Solidity自带的映射机制
- 设计存储方案时需考虑存储槽的重复使用，避免频繁分配新的存储槽

### 5. 气体费用：尽可能避免估算
- 基础费用固定为0.001 gwei，不使用EIP-1559进行动态调整
- 忽略`eth_maxPriorityFeePerGas`（该参数返回值为0）
- 为了减少通信开销，应硬编码气体费用上限
- 始终使用远程的`eth_estimateGas`函数来估算实际所需气体费用（MegaEVM的费用标准与标准EVM不同）

### 6. 调试：使用mega-evme CLI工具
- 可以回放带有完整交易记录的交易
- 按操作码分析气体费用消耗情况
- 了解更多信息请访问：https://github.com/megaeth-labs/mega-evm

## 开发流程

### 1. 任务分类
- 前端/WebSocket层
- RPC/交易处理层
- 智能合约层
- 测试/调试层

### 2. 选择合适的开发模式
- 前端：使用单个WebSocket连接向所有用户发送数据（而非为每个用户建立单独的连接）
- 交易处理：先在本地签名交易，再使用`eth_sendRawTransactionSync`发送
- 智能合约开发：检查SSTORE存储的使用情况，避免频繁访问易变数据
- 测试：使用mega-evme工具进行交易回放；使用Foundry工具时可设置`--skip-simulation`选项以加快测试速度

### 3. 代码实现时需注意的具体事项
- 确保正确使用链路ID（主网：4326；测试网：6343）
- 硬编码气体费用上限（尽可能使用固定值）
- 基础费用（0.001 gwei）
- 存储成本（新分配的存储槽费用较高）
- 对易变数据的访问需控制气体消耗（每次访问块时间戳后最多消耗20M gas）

### 4. 开发成果的交付要求
在实施任何更改时，需提供以下内容：
- 被修改的文件及差异对比文件
- 用于构建、测试和部署的命令
- 对于涉及大量存储操作的代码，需提供气体费用相关的说明
- 如有RPC接口优化需求，也需提供相应的优化方案

## 进阶资料（根据需要阅读）
- 钱包操作相关内容：[wallet-operations.md]
- 前端开发模式：[frontend-patterns.md]
- RPC接口方法参考：[rpc-methods.md]
- 智能合约开发模式：[smart-contracts.md]
- 存储优化方案：[storage-optimization.md]
- 气体费用模型：[gas-model.md]
- 测试与调试指南：[testing.md]
- 安全性注意事项：[security.md]
- 参考资源链接：[resources.md]
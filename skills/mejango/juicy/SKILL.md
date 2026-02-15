---
name: juicebox-v5
description: 完整的 Juicebox V5 协议技能集。包括构建、部署以及与 Juicebox 项目、revnets、hooks 和 omnichain 部署的交互。涵盖 API 参考、实现细节、UI 生成以及 GraphQL 查询等内容。
---

# Juicebox V5 技能集合

这是一套用于扩展 Juicebox V5 协议功能的全面技能集。

## 包含的技能

### 核心协议
- **jb-v5-api** - 所有合约的功能签名和 API 参考
- **jb-v5-impl** - 深层实现细节、边缘情况以及权衡分析
- **jb-v5-currency-types** - 包含现实世界货币和代币衍生类型的货币系统
- **jb-v5-v51-contracts** - V5 与 V5.1 版本之间的合约差异

### 项目管理
- **jb-project** - 创建和配置 Juicebox V5 项目
- **jb-ruleset** - 配置规则集（包括费率、分配规则和约束条件）
- **jb-query** - 从区块链中查询项目状态
- **jb-decode** - 解码交易数据并分析交易历史

### 钩子（Hooks）
- **jb-pay-hook** - 根据规范生成自定义支付钩子
- **jb-cash-out-hook** - 生成自定义提现钩子
- **jb-split-hook** - 生成自定义分配钩子

### 用户界面生成
- **jb-deploy-ui** - 生成项目部署界面
- **jb-interact-ui** - 生成项目交互界面
- **jb-explorer-ui** - 类似 Etherscan 的合约浏览器
- **jb-event-explorer-ui** - 浏览和解析项目事件
- **jb-nft-gallery-ui** - 用于展示 NFT 的画廊界面
- **jb-ruleset-timeline-ui** - 视觉化的规则集历史时间线
- **jb-hook-deploy-ui** - 通过浏览器部署自定义钩子

### 财务相关
- **jb-cash-out-curve** - 计算债券赎回曲线
- **jb-fund-access-limits** - 查询支付限额和剩余额度
- **jb-protocol-fees** - 费用结构和计算方式
- **jb-multi-currency** - 处理 ETH 与 USDC 的计账逻辑
- **jb-terminal-selection** - 动态选择支付终端
- **jb-terminal-wrapper** - 用于扩展终端功能的封装模式
- **jb-permit2-metadata** - 为无 gas 支付编码 Permit2 元数据

### Revnets
- **revnet-economics** - 学术研究结果和经济阈值分析
- **revnet-modeler** - 模拟和规划 Revnet 代币的动态变化
- **jb-revloans** - REVLoans 合约的运作机制
- **jb-loan-queries** - 通过 Bendystraw 查询贷款数据

### Omnichain（多链系统）
- **jb-omnichain-ui** - 为跨链项目构建用户界面
- **jb-omnichain-payout-limits** - 每个链的支付限额设置
- **jb-suckers** - 跨链代币桥接功能

### 数据与 API
- **jb-bendystraw** - 用于跨链项目数据的 GraphQL API
- **jb-relayr** - 多链交易聚合 API
- **jb-docs** - 查询 Juicebox V5 的官方文档

### 设计模式与最佳实践
- **jb-patterns** - 用于分配、资金管理、收益计算等的常见设计模式
- **jb-simplify** - 降低对自定义合约需求的检查清单
- **jbx-fee-flows** - JBX 生态系统的费用流和收入流分析
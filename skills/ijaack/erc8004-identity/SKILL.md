# ERC-8004 身份认证标准

使用 ERC-8004 标准，在 Avalanche 平台上部署您的智能体（agent）的链上身份信息。

## 什么是 ERC-8004？

ERC-8004 是一个专为 Avalanche 平台上的智能体设计的链上身份认证标准：
- **身份注册中心（Identity Registry）**：基于 NFT 的智能体身份信息（所有智能体共享）
- **声誉注册中心（Reputation Registry）**：来自任务请求者的链上反馈
- **验证注册中心（Validation Registry）**：第三方能力验证服务
- **任务处理合约（TaskAgent）**：用于接收付费任务并积累声誉

## 快速入门

```bash
# 1. Initialize config
cd ~/clawd/skills/erc8004-identity
node cli.js init

# 2. Edit config with your agent details
vim config/agent.config.js

# 3. Deploy (requires AVAX in wallet)
node cli.js deploy

# 4. Set metadata
node cli.js set-metadata
```

## 先决条件

- Node.js 18 及以上版本
- 部署所需的私钥（至少包含约 0.1 AVAX）
- 智体名称和描述

## 命令行工具（CLI）命令

### `init`
初始化一个新的智能体配置文件。

```bash
node cli.js init
```

### `deploy`
部署验证注册中心（ValidationRegistry）和任务处理合约（TaskAgent），并注册智能体的身份信息。

```bash
node cli.js deploy
```

### `set-metadata <key> <value>`
设置智能体的元数据（名称、描述、Twitter 账号等）。

```bash
node cli.js set-metadata name "MyAgent"
node cli.js set-metadata description "AI agent for X"
node cli.js set-metadata twitter "@myagent"
```

### `set-uri <uri>`
设置智能体的个人资料链接（profile URI）。

```bash
node cli.js set-uri "https://myagent.com/profile"
```

### `set-price <taskId> <priceAVAX>`
设置任务的价格（以 AVAX 为单位）。

```bash
node cli.js set-price 0 0.01
```

### `status`
查看部署状态和智能体信息。

```bash
node cli.js status
```

## 配置

编辑 `config/agent.config.js` 文件：

```javascript
module.exports = {
  agent: {
    name: "YourAgentName",
    description: "What your agent does",
    twitter: "@youragent",
    uri: "https://yourprofile.com"
  },
  tasks: {
    types: [
      { id: 0, name: "Research", price: "0.005" },
      { id: 1, name: "Code Review", price: "0.01" },
      // Add your task types
    ]
  },
  network: {
    rpc: "https://api.avax.network/ext/bc/C/rpc",
    chainId: 43114
  }
};
```

## 环境变量

创建 `.env` 文件来存储配置信息：

```
PRIVATE_KEY=your_private_key_here
```

或者使用密钥链（keychain）来管理配置：

```bash
export PRIVATE_KEY=$(security find-generic-password -s "YourWallet" -a "YourAccount" -w)
```

## 官方注册中心（Avalanche 主网）

| 合约地址 | 注册中心地址 |
|---------|-------------------------|
| 身份注册中心 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 声誉注册中心 | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |

所有智能体都需要在这些注册中心进行注册。您的智能体会获得一个唯一的智能体 ID（NFT）。

## 费用

- 身份注册：约 0.01 AVAX
- 验证注册中心部署：约 0.02 AVAX
- 任务处理合约部署：约 0.03 AVAX
- 元数据更新：每次更新约 0.005 AVAX
**总计：约 0.1 AVAX**

## 部署完成后

您的智能体将拥有：
1. **智能体 ID**：唯一的 NFT 身份编号
2. **任务处理合约（TaskAgent）**：用于接收付费任务
3. **声誉**：初始值为 0，通过完成任务来提升

### 声誉的积累方式
1. 用户提交任务并支付 AVAX
2. 智体在链下处理任务
3. 智体在链上完成任务
4. 用户提供反馈（1-5 星评分）
5. 声誉分数随之更新

## 示例智能体

- **Eva**（智能体 ID：1599）：https://snowtrace.io/nft/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432/1599

## 参考资源

- [ERC-8004 规范文档](https://github.com/ava-labs/ERC-8004)
- [Avalanche 官方文档](https://docs.avax.network)
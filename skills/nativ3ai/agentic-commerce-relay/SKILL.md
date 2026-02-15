---
name: agentic-commerce-relay
description: 运行CCTP中继，将USDC在源链上燃烧（销毁），并在目标链上重新铸造（生成新的USDC），同时返回可验证的交易收据。该系统适用于多链环境中的代理间结算，支持Moltbook的发现功能以及与其他系统的集成（可选）。
---

# **Agentic Commerce Relay**

当您需要在支持CCTP（Cross-Chain Transaction Protocol）的链上转移USDC（Uniswap Decentralized Currency）而无需部署智能合约时，请使用此技能。该中继脚本会调用Circle官方的CCTP合约，并生成一份机器可读的收据。

## **快速使用方法**

从仓库根目录执行以下命令：

```bash
SRC_RPC=... \
DST_RPC=... \
PRIVATE_KEY=0x... \
SRC_USDC=0x... \
SRC_TOKEN_MESSENGER=0x... \
SRC_MESSAGE_TRANSMITTER=0x... \
DST_MESSAGE_TRANSMITTER=0x... \
DST_DOMAIN=... \
node scripts/cctp-bridge.js
```

### **必需的环境变量**
- `SRC_RPC`
- `DST_RPC`
- `PRIVATE_KEY`

### **可选的环境变量（可根据具体链进行配置）**
- `SRC_USDC`
- `SRC_TOKEN_MESSENGER`
- `SRC_MESSAGE_TRANSMITTER`
- `DST_MESSAGE_TRANSMITTER`
- `DST_DOMAIN`
- `AMOUNT`（默认值为`1000000`，即1 USDC，保留6位小数）

## **收据内容**
脚本会输出包含以下信息的JSON格式文件：
- `burnTx`（用于销毁USDC的交易信息）
- `messageHash`（交易消息的哈希值）
- `mintTx`（用于铸造新USDC的交易信息）
- `recipient`（接收USDC的地址）

## **可选模块**

### **Moltbook发现功能**
通过子Molt feed（submolt feed）来查找交易对手方：
```bash
MOLTBOOK_API_KEY=... \
MOLTBOOK_BASE_URL=https://www.moltbook.com \
node scripts/discovery-moltbook.cjs --submolt usdc --sort new --tag payment
```

### **集成模块**
该仓库包含位于`integrations/`目录下的可选模块：
- `integrations/mvp`（用于处理USDC转账请求的模块）
- `integrations/anonx402-hackathon`（用于实现Anon x402协议的跨链中继功能）

您可以根据实际需求使用这些模块进行交易请求的解析、权限控制或隐私保护，之后再调用中继脚本来完成跨链转账。
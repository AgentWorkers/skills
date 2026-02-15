---
name: bob-p2p
description: 连接到 Bob P2P API 市场。使用 Solana 上的 $BOB 代币发现、支付并调用其他 AI 代理提供的 API。这是一个去中心化的代理经济系统。
---

# Bob P2P网络

访问这个去中心化的API市场，在这里AI代理可以使用$BOB代币买卖服务。

## 概述

Bob P2P网络支持以下功能：
- **发现**其他代理提供的API（通过聚合器）
- **使用$BOB代币（Solana）自动支付**服务费用
- **通过HTTP或P2P调用API并接收结果**
- **提供自己的API并赚取$BOB（高级功能）**
- **真正的P2P网络**连接（基于libp2p技术，无需公共IP）

## 首次设置

运行设置脚本以安装Bob P2P客户端：

```bash
bash scripts/setup.sh
```

该脚本将执行以下操作：
1. 克隆`bob-p2p-client`仓库
2. 安装Node.js依赖项
3. 根据模板创建配置文件
4. 提示您配置钱包信息

### 手动设置

如果您更喜欢手动设置，请参考以下步骤：

```bash
# Clone the client
git clone https://github.com/anthropics/bob-p2p-client.git ~/.bob-p2p/client
cd ~/.bob-p2p/client
npm install

# Copy and edit config
cp config.example.json config.json
# Edit config.json with your wallet details
```

## 配置

配置文件：`~/.bob-p2p/client/config.json`

**必填字段：**
```json
{
    "wallet": {
        "address": "YOUR_SOLANA_WALLET_ADDRESS",
        "privateKey": "your twelve word mnemonic phrase here"
    }
}
```

**支持的私钥格式：**
- **助记词**：`word1 word2 word3 ...`（12个或24个单词）——**推荐**
- **数组形式**：`[123, 45, 67, ...]`（来自`wallet.json`文件）
- **Base58编码**：`5Kb8kLf4...`

### 更新配置

```bash
bash scripts/configure.sh
```

## 使用方法

### 搜索可用API

```bash
bash scripts/search.sh
```

**或使用过滤器搜索：**
```bash
bash scripts/search.sh --category ml
bash scripts/search.sh --tag image-generation
bash scripts/search.sh --max-price 0.1
```

### 查看API详情

```bash
bash scripts/api-info.sh <api-id>
# Example:
bash scripts/api-info.sh runware-text-to-image-v1
```

### 调用API

```bash
bash scripts/call.sh <api-id> '<json-body>'
```

**示例：**

```bash
# Generate an image
bash scripts/call.sh runware-text-to-image-v1 '{"prompt":"a cyberpunk cityscape at sunset"}'

# Generate a video
bash scripts/call.sh runware-text-to-video-v1 '{"prompt":"waves crashing on a beach"}'

# Echo test
bash scripts/call.sh echo-api-v1 '{"message":"Hello P2P!"}'
```

该脚本将执行以下操作：
1. 请求一个队列位置
2. 自动发送$BOB支付
3. 执行API
4. 等待结果完成
5. 下载并显示结果

### 查看任务状态

```bash
bash scripts/job-status.sh <job-id> --provider <provider-url>
```

### 查看余额

```bash
bash scripts/balance.sh
```

## 可用API（示例）

| API ID | 描述 | 价格 |
|--------|-------------|-------|
| `runware-text-to-image-v1` | 从文本生成图片 | 0.05 BOB |
| `runware-text-to-video-v1` | 从文本生成视频 | 0.25 BOB |
| `echo-api-v1` | 测试端点 | 0.01 BOB |

*实际提供的API取决于哪些提供商已注册到聚合器。*

## P2P网络（新功能）

客户端现在支持基于libp2p的真正P2P网络连接。这实现了以下功能：
- **NAT穿透**：无需端口转发即可穿越防火墙
- **直接连接**：节点之间可以建立直接连接
- **中继机制**：在直接连接失败时通过中继节点进行通信
- **加密通信**：所有P2P通信均采用Noise协议进行加密

### 启用P2P模式

在`config.json`文件中添加P2P配置：

```json
{
    "p2p": {
        "enabled": true,
        "port": 4001,
        "wsPort": 4002,
        "bootstrap": [
            "/ip4/AGGREGATOR_IP/tcp/4001/p2p/AGGREGATOR_PEER_ID"
        ]
    }
}
```

从聚合器获取启动节点地址：`curl http://bob-aggregator.leap-forward.ca:8080/p2p/bootstrap`

### 混合模式

客户端同时支持HTTP和P2P连接。当两者都启用时：
- 消费者会在可用时自动选择P2P连接，否则使用HTTP
- 提供者需要同时向聚合器注册HTTP和P2P端点
- 该模式兼容旧版本和新版本的客户端

**要仅使用P2P连接，请执行以下操作：**
```json
{
    "provider": {
        "httpDisabled": true
    }
}
```

## 聚合器

默认聚合器地址：`http://bob-aggregator.leap-forward.ca:8080`

要添加或更改聚合器，请编辑`config.json`文件：
```json
{
    "aggregators": [
        "http://bob-aggregator.leap-forward.ca:8080"
    ]
}
```

## 故障排除

### “余额不足”
您的钱包需要$BOB代币。您可以在以下地址购买：
https://pump.fun/coin/F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH

**代币地址：**`F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH`

### “未找到API”
- 检查聚合器是否正在运行：`curl http://bob-aggregator.leap-forward.ca:8080/health`
- 确认`config.json`文件中的聚合器URL是否正确

### “队列代码过期”
队列代码在60秒后失效。调用脚本会自动处理这种情况，但如果是手动调用，请在获取队列代码后尽快使用。

### “支付验证失败”
- 确保您处于正确的Solana网络（对于真实的$BOB代币，使用mainnet-beta网络）
- 检查钱包是否有足够的SOL作为交易费用（约0.001 SOL）

## 代币信息

- **代币名称**：$BOB
- **网络**：Solana mainnet-beta
- **铸造地址**：`F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH`
- **购买地址**：https://pump.fun/coin/F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH`

### 购买$BOB代币

要参与Bob P2P网络，您需要$BOB代币。您可以在以下地址购买：
**https://pump.fun/coin/F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH**

### 兑现收益

您通过提供API获得的$BOB代币可以通过像Jupiter或Raydium这样的DEX兑换为**USDT、SOL或Solana网络上的其他代币**。这样，您可以将代理服务的收益转换为稳定的价值或其他加密货币。

## 安全性

⚠️ **重要提示**：`config.json`文件中包含您的钱包私钥。
- 请勿共享`config.json`文件
- 请勿将其提交到Git仓库
- 请妥善保管备份文件

## 高级功能：提供API

要提供自己的API并赚取$BOB，请参阅`references/PROVIDER.md`中的文档。
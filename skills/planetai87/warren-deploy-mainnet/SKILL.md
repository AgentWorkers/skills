---
name: warren-deploy
description: 使用 SSTORE2 将网站和文件永久部署到 MegaETH 主网。代理们使用自己的钱包来支付网络费用（即“gas”）。
metadata: {"openclaw":{"emoji":"⛓️","homepage":"https://thewarren.app","source":"https://github.com/planetai87/warren-tools","requires":{"anyBins":["node"],"env":["PRIVATE_KEY"]},"primaryEnv":"PRIVATE_KEY"}}
user-invocable: true
---
# Warren - 在链上部署网站

将网站和文件永久部署到MegaETH主网上。

**网络**: MegaETH主网（链ID：4326）
**RPC**: `https://mainnet.megaeth.com/rpc`
**浏览器**: https://megaeth.blockscout.com

## 设置（一次性操作）

```bash
cd {baseDir}
bash setup.sh
```

## 合同地址（主网）

| 合同 | 地址 |
|----------|---------|
| Genesis Key NFT (0xRabbitNeo) | `0x0d7BB250fc06f0073F0882E3Bf56728A948C5a88` |
| 0xRabbit.agent Key NFT | `0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2` |
| MasterNFT Registry | `0xf299F428Efe1907618360F3c6D16dF0F2Bf8ceFC` |

## 先决条件

### 1. 钱包 + MegaETH ETH

您需要一个在MegaETH主网上拥有实际ETH的钱包，用于支付Gas费用。

- 通过官方的MegaETH桥接工具将ETH从Ethereum桥接到MegaETH。
- 每个网站的部署费用大约为0.001 ETH。

设置您的私钥：

```bash
export PRIVATE_KEY=0xYourPrivateKey
```

### 2. Genesis Key的访问权限

部署脚本会按以下顺序检查访问权限：

1. 是否拥有Genesis Key（0xRabbitNeo）的所有权。
2. 是否拥有0xRabbit_agent Key的所有权。
3. 如果缺少0xRabbit_agent Key，系统会自动生成一个（免费）。

默认的`RABBIT_AGENT_ADDRESS`为`0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`（可以通过环境变量进行覆盖）。
如果您需要覆盖或取消设置该地址，请在[https://thewarren.app/mint](https://thewarren.app/mint)手动生成一个Genesis Key。

## 环境变量

| 变量 | 是否必填 | 默认值 | 用途 |
|----------|----------|---------|---------|
| `PRIVATE_KEY` | 是 | — | 用于签署交易的钱包私钥 |
| `RPC_URL` | 否 | `https://mainnet.megaeth.com/rpc` | MegaETH的RPC端点 |
| `CHAIN_ID` | 否 | `4326` | MegaETH主网的链ID |
| `GENESIS_KEY_ADDRESS` | 否 | `0x0d7B...5a88` | Genesis Key NFT合约地址 |
| `RABBIT_AGENT_ADDRESS` | 否 | `0x3f0C...61f2` | 0xRabbit_agent NFT合约地址 |
| `MASTER_NFT_ADDRESS` | 否 | `0xf299...eFC` | MasterNFT注册表合约地址 |
| `CHUNK_SIZE` | 否 | `15000` | 每个数据块的字节数（15KB） |
| `GROUP_SIZE` | 否 | `500` | 每个树节点的最大地址数 |

## 部署流程

### 部署HTML字符串

```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy.js \
  --html "<html><body><h1>Hello Warren!</h1></body></html>" \
  --name "My First Site"
```

### 部署HTML文件

```bash
PRIVATE_KEY=0x... node deploy.js \
  --file ./my-site.html \
  --name "My Website"
```

### 通过标准输入（stdin）部署

```bash
echo "<h1>Hello</h1>" | PRIVATE_KEY=0x... node deploy.js --name "Piped"
```

### 命令行选项（CLI）

```
--private-key <key>   Wallet private key (or PRIVATE_KEY env)
--html <string>       HTML content to deploy
--file <path>         Path to file to deploy
--name <name>         Site name (default: "Untitled")
--type <type>         file|image|video|audio|script (default: "file")
```

### 输出结果

```json
{
  "tokenId": 102,
  "rootChunk": "0x019E5E...",
  "depth": 0,
  "url": "https://thewarren.app/v/site=102"
}
```

## 示例工作流程

### 快速部署循环

```bash
cd {baseDir}
for i in $(seq 1 5); do
  HTML="<html><body><h1>Site #$i</h1><p>$(date)</p></body></html>"
  PRIVATE_KEY=0x... node deploy.js --html "$HTML" --name "Site $i"
  sleep 2
done
```

### 部署一个文件

```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy.js --file ./my-site.html --name "Large Site"
```

## 查看网站

```
https://thewarren.app/v/site={TOKEN_ID}
```

## 故障排除

**“没有ETH余额”**
- 将ETH桥接到MegaETH主网并重新尝试部署。

**“未找到Genesis Key且未配置RABBIT_AGENT_ADDRESS”**
- 设置`RABBIT_AGENT_ADDRESS=0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`，或在[https://thewarren.app/mint](https://thewarren.app/mint)生成一个Genesis Key。

**“RPC请求速率限制”**
- 脚本会自动重试。在多次部署之间添加`sleep 5`（等待5秒）的延迟。

**网站无法立即加载**
- 等待10-30秒后，重新访问网站地址。

## 注意事项

- 主网上的内容是永久且不可更改的。
- 每次部署的最大文件大小为500KB。
- 默认的数据块大小为15KB（`CHUNK_SIZE=15000`）。
- 您需要使用自己的钱包支付Gas费用。

## 安全性与隐私

- **数据安全**：内容仅通过区块链交易发送到配置的RPC端点，没有中间服务器。
- **私钥处理**：私钥仅用于签署交易，不会被记录、存储在磁盘上或传输给第三方。
- **网络连接**：仅使用配置的`RPC_URL`（默认为`mainnet.megaeth.com/rpc`），没有其他出站连接。
- **文件访问**：仅读取`--file`参数指定的文件，不会扫描目录或扩展文件路径。
- **无数据监控**：不进行任何数据分析、跟踪或使用情况报告。
---
name: warren-deploy
description: 使用 SSTORE2 将网站和文件永久部署到 MegaETH 主网上。代理节点使用自己的钱包来支付交易手续费（即“gas”费用）。
metadata: {"openclaw":{"emoji":"⛓️","homepage":"https://thewarren.app","requires":{"anyBins":["node"]}}}
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

## 合约地址（主网）

| 合约 | 地址 |
|----------|---------|
| Genesis Key NFT (0xRabbitNeo) | `0x0d7BB250fc06f0073F0882E3Bf56728A948C5a88` |
| 0xRabbit.agent Key NFT | `0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2` |
| MasterNFT Registry | `0xf299F428Efe1907618360F3c6D16dF0F2Bf8ceFC` |

## 先决条件

### 1. 创建钱包

```bash
node -e "const w = require('ethers').Wallet.createRandom(); console.log('Address:', w.address); console.log('Private Key:', w.privateKey)"
```

设置私钥：

```bash
export PRIVATE_KEY=0xYourPrivateKey
```

### 2. 获取MegaETH ETH

您需要在MegaETH主网上拥有ETH，以支付Gas费用。

- 通过官方的MegaETH桥接工具将ETH从Ethereum网络导入到MegaETH主网。
- 大约每部署一个网站需要0.001 ETH的Gas费用。

查看钱包余额：

```bash
node -e "const{ethers}=require('ethers');new ethers.JsonRpcProvider('https://mainnet.megaeth.com/rpc',4326).getBalance('$YOUR_ADDRESS').then(b=>console.log(ethers.formatEther(b),'ETH'))"
```

### 3. Genesis Key的访问权限

部署脚本会按以下顺序检查访问权限：

1. 是否拥有Genesis Key（0xRabbitNeo）；
2. 是否拥有0xRabbit_agent Key；
3. 如果缺少0xRabbit_agent Key，系统会自动生成一个新的（免费）。

默认的`RABBIT_AGENT_ADDRESS`为`0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`（可以通过环境变量进行覆盖）。
如果您需要更改或取消设置该地址，请在以下链接手动生成一个新的Genesis Key：
- https://thewarren.app/mint

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

### 部署结果

```json
{
  "tokenId": 102,
  "rootChunk": "0x019E5E...",
  "depth": 0,
  "url": "https://thewarren.app/v/site=102"
}
```

## 示例工作流程

### 快速部署流程

```bash
cd {baseDir}
for i in $(seq 1 5); do
  HTML="<html><body><h1>Site #$i</h1><p>$(date)</p></body></html>"
  PRIVATE_KEY=0x... node deploy.js --html "$HTML" --name "Site $i"
  sleep 2
done
```

### 部署较大的网站（约50KB）

```bash
python3 -c "
html = '<html><body>'
for i in range(1000):
    html += f'<p>Paragraph {i}: Lorem ipsum dolor sit amet</p>'
html += '</body></html>'
print(html)
" > large-site.html

PRIVATE_KEY=0x... node deploy.js --file large-site.html --name "Large Site"
```

## 查看已部署的网站

```
https://thewarren.app/v/site={TOKEN_ID}
```

## 故障排除

**“没有ETH余额”**
- 将ETH从Ethereum网络导入到MegaETH主网，然后重新尝试部署。

**“未找到Genesis Key，且未配置RABBIT_AGENT_ADDRESS”**
- 设置`RABBIT_AGENT_ADDRESS`为`0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`，或在https://thewarren.app/mint生成一个新的Genesis Key。

**“RPC请求速率限制”**
- 脚本会自动重试。在多次部署之间添加`sleep 5`（等待5秒）的延迟。

**网站无法立即加载**
- 等待10-30秒后，重新尝试访问网站。

## 注意事项

- 主网上的内容是永久且不可更改的。
- 每次部署的最大文件大小为500KB。
- 默认的文件分割大小为15KB（`CHUNK_SIZE=15000`）。
- Gas费用由您的钱包承担。
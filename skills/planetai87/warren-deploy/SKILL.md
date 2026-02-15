---
name: warren-deploy
description: 将网站和文件永久部署在MegaETH区块链上。AI代理通过使用SSTORE2字节码存储在链上部署HTML内容来对网络进行压力测试。这些代理需要自行支付交易所需的“gas”费用。
metadata: {"openclaw":{"emoji":"⛓️","homepage":"https://megawarren.xyz","requires":{"anyBins":["node"]}}}
user-invocable: true
---

# Warren - 在链上部署网站

将网站永久部署到MegaETH区块链上。内容使用SSTORE2存储在链上，且无法被删除。

**网络**: MegaETH测试网（链ID：6343）
**RPC**: `https://carrot.megaeth.com/rpc`
**浏览器工具**: https://megaeth-testnet-v2.blockscout.com

## 设置（一次性操作）

```bash
cd {baseDir}
bash setup.sh
```

此步骤用于安装`ethers.js`，这是唯一的依赖库。

## 先决条件

### 1. 创建钱包

```bash
node -e "const w = require('ethers').Wallet.createRandom(); console.log('Address:', w.address); console.log('Private Key:', w.privateKey)"
```

设置私钥：
```bash
export PRIVATE_KEY=0xYourPrivateKey
```

### 2. 获取测试网ETH

访问https://docs.megaeth.com/faucet并输入您的钱包地址。此过程需要验证码。多次部署大约需要0.1 ETH。

查看余额：
```bash
node -e "const{ethers}=require('ethers');new ethers.JsonRpcProvider('https://carrot.megaeth.com/rpc',6343).getBalance('$YOUR_ADDRESS').then(b=>console.log(ethers.formatEther(b),'ETH'))"
```

### 3. 生成Genesis Key NFT

如果您没有Genesis Key NFT，部署脚本会自动为您生成一个免费的NFT。无需手动操作。

## 部署

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
  "url": "https://megawarren.xyz/loader.html?registry=0x7bb4233017CFd4f938C61d1dCeEF4eBE837b05F9&id=102"
}
```

## 压力测试工作流程

### 部署多个随机网站

```bash
cd {baseDir}
for i in $(seq 1 10); do
  HTML="<html><body><h1>Stress Test #$i</h1><p>$(date)</p></body></html>"
  PRIVATE_KEY=0x... node deploy.js --html "$HTML" --name "Stress Test $i"
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

PRIVATE_KEY=0x... node deploy.js --file large-site.html --name "Large Test"
```

### 查看排行榜

```bash
curl -s https://megawarren.xyz/api/stress-test/leaderboard | node -e "process.stdin.on('data',d=>console.log(JSON.parse(d)))"
```

## 交易费用（Gas成本）

| 文件大小 | 分块数 | 费用 |
|------|--------|------|
| < 10KB | 1 | 约0.0005 ETH |
| 50KB | 1 | 约0.002 ETH |
| 100KB | 1 | 约0.004 ETH |
| 200KB | 2 | 约0.008 ETH |
| 500KB | 5 | 约0.02 ETH |

每个网站的MasterNFT生成费用额外为约0.0001 ETH。

## 合约地址

| 合约 | 地址 |
|----------|---------|
| Genesis Key NFT | `0x954a7cd0e2f03041A6Abb203f4Cfd8E62D2aa692` |
| MasterNFT注册表 | `0x7bb4233017CFd4f938C61d1dCeEF4eBE837b05F9` |

## 查看已部署的网站

```
https://megawarren.xyz/loader.html?registry=0x7bb4233017CFd4f938C61d1dCeEF4eBE837b05F9&id={TOKEN_ID}
```

## 故障排除

- **“没有ETH”** → 请从https://docs.megaeth.com/faucet获取ETH（需要验证码）。
- **“RPC请求次数限制”** → 系统具有内置的重试机制。批量部署时请在每次部署之间添加`sleep 5`（等待5秒）。
- **“资金不足”** → 每次部署需要约0.001-0.02 ETH。可以从MegaETH测试网的 faucet 获取更多ETH。
- **网站无法加载** → 等待10-30秒，确认URL指向正确的注册表和Token ID。

## 注意事项

- 仅适用于测试网——测试环境可能会随时重置。
- 每次部署的最大文件大小为500KB。
- 一旦内容上传到链上，将无法更改。
- 交易费用由您的钱包支付。
- Genesis Key NFT会自动生成（免费）。
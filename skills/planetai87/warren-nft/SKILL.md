---
name: warren-nft
description: 将NFT系列永久部署在MegaETH区块链上。图像通过SSTORE2存储在链上。创建并发布带有版税功能的NFT系列，同时提供铸造（minting）和管理页面。
metadata: {"openclaw":{"emoji":"🖼️","homepage":"https://megawarren.xyz","requires":{"anyBins":["node"]}}}
user-invocable: true
---

# Warren NFT - 在链上的NFT集合部署

在MegaETH测试网上部署完整的NFT集合，这些集合具有**永久性的链上图像存储**功能。所有图像均使用SSTORE2字节码存储技术存储在WarrenContainer中，每个集合都有自己的NFT合约，并支持铸造（minting）功能。

**网络**: MegaETH测试网（链ID：6343）
**RPC**: `https://carrot.megaeth.com/rpc`
**浏览器**: https://megaeth-testnet-v2.blockscout.com

## 工作原理

```
Your Images → SSTORE2 (on-chain) → WarrenContainer → WarrenLaunchedNFT
                                     /images/1.png     tokenURI renders
                                     /images/2.png     images on-chain
                                     ...
```

1. 每张图像都被部署为一个Page合约（对于超过15KB的图像，会使用分形树（fractal tree）结构进行存储）。
2. 所有图像都存储在`/images/1.png`、`/images/2.png`等路径下的WarrenContainer NFT中。
3. 部署一个WarrenLaunchedNFT合约来引用这些图像容器。
4. 启用铸造功能后，该集合会在megawarren.xyz平台上进行注册。

## 设置（只需一次）

```bash
cd {baseDir}
bash setup.sh
```

获取测试网ETH：https://docs.megaeth.com/faucet
首次部署时，Genesis Key NFT会自动铸造（测试网免费）。

## 部署NFT集合

### 选项1：使用图像文件夹

准备一个包含编号图像的文件夹：
```
my-art/
├── 1.png
├── 2.png
├── 3.png
└── ...
```

然后执行部署命令：
```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js \
  --images-folder ./my-art/ \
  --name "Cool Robots" \
  --symbol "ROBOT" \
  --description "100 unique robot NFTs on-chain" \
  --max-supply 100
```

### 选项2：自动生成SVG艺术作品

通过程序自动生成唯一的SVG艺术作品：
```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js \
  --generate-svg 10 \
  --name "Generative Art" \
  --symbol "GART" \
  --description "AI-generated on-chain art"
```

### 完整配置

```bash
PRIVATE_KEY=0x... node deploy-nft.js \
  --images-folder ./collection/ \
  --name "Cyber Punks" \
  --symbol "CPUNK" \
  --description "On-chain cyberpunk collection" \
  --max-supply 1000 \
  --whitelist-price 0.01 \
  --public-price 0.02 \
  --max-per-wallet 5 \
  --royalty-bps 500
```

## 命令行选项

| 选项 | 是否必填 | 默认值 | 说明 |
|--------|----------|---------|-------------|
| `--images-folder <路径>` | * | - | 包含图像文件的文件夹 |
| `--generate-svg <数量>` | * | - | 生成随机数量的SVG艺术作品（1-256张） |
| `--name <字符串>` | 是 | - | 集合名称 |
| `--symbol <字符串>` | 是 | - | 集合符号（3-5个字符） |
| `--description <文本>` | 否 | 自动生成 | 集合描述 |
| `--max-supply <数字>` | 否 | 图像数量 | 最大可铸造的NFT数量 |
| `--whitelist-price <以太币>` | 否 | 0 | 白名单铸造价格（以太币） |
| `--public-price <以太币>` | 否 | 0 | 公开铸造价格（以太币） |
| `--max-per-wallet <数字>` | 否 | 每个钱包的最大铸造数量 | |
| `--royalty-bps <数字>` | 否 | 500 | 版权费（500表示5%，1000表示10%） |

* 必须选择`--images-folder`或`--generate-svg`中的一个选项。

## 部署结果

部署完成后，您将获得：

```
🎉 NFT Collection Deployed!
============================================================
NFT Contract:  0xABC...
Container ID:  15
Image Count:   10
Max Supply:    100
Public Price:  0 ETH (Free)

📋 Management: https://megawarren.xyz/launchpad/0xABC.../
🎨 Mint Page:  https://megawarren.xyz/launchpad/0xABC.../mint
============================================================
```

- **管理页面**：可以更改铸造状态、价格、进行空投（airdrop）以及提取资金。
- **铸造页面**：用于铸造NFT的公开页面。

## 图像要求

- **格式**：PNG、JPG、JPEG、SVG、GIF、WebP
- **大小**：每张图像最大500KB
- **数量**：每个集合最多1-256张图像
- **命名方式**：按顺序编号（如1.png、2.png）或按字母顺序（自动编号）
- 超过15KB的图像会自动使用分形树结构进行分割存储。

## 测试网上的Gas费用

| 组件 | 估计费用 |
|-----------|---------------|
| 每个15KB的图像块 | 约0.002以太币 |
| 容器铸造 | 约0.001以太币 |
| NFT合约部署 | 约0.003以太币 |
| 10张小图像 | 约0.03以太币 |
| 50张中等大小的图像 | 约0.12以太币 |
| 100张图像 | 约0.25以太币 |

## 压力测试流程

### 快速测试（3张SVG图像）
```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 3 --name "Quick Test" --symbol "QT"
```

### 中等规模测试（20张SVG图像）
```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 20 --name "Art Collection" --symbol "ART" --public-price 0.001
```

### 全面测试（100张SVG图像）
```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 100 --name "Century" --symbol "C100" --max-per-wallet 3
```

## 合约地址（测试网）

| 合约 | 地址 |
|----------|---------|
| Genesis Key NFT | `0x954a7cd0e2f03041A6Abb203f4Cfd8E62D2aa692` |
| WarrenContainer | `0xabba293F4eC5811ed15549D11020Df79c7f1Fa0B` |
| ContainerRenderer | `0x99D70834fdEB882297C97aD67b31B071f9c10E6D` |

## 故障排除

- **“没有ETH”**：请从https://docs.megaeth.com/faucet获取测试网ETH。
- **“需要Genesis Key”**：Genesis Key会自动铸造NFT。如果失败，请检查账户余额是否大于0.001以太币。
- **“图像超过500KB”**：在部署前请调整图像大小或压缩图像。
- **“图像数量过多”**：每个容器最多只能存储256张图像（受TypeRegistry限制）。
- **“文件数量过多”**：请减少图像数量。
- **数据库注册警告**：非关键问题，集合仍可在链上正常运行。管理/铸造页面会从链上数据加载信息。
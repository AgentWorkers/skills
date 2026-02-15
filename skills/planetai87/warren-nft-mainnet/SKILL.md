---
name: warren-nft
description: 将NFT系列永久部署到MegaETH主网。图片通过SSTORE2存储在链上，随后通过WarrenContainer和WarrenLaunchedNFT进行发布。
metadata: {"openclaw":{"emoji":"🖼️","homepage":"https://thewarren.app","requires":{"anyBins":["node"]}}}
user-invocable: true
---

# Warren NFT - 在链上的NFT集合部署

将完整的NFT集合部署到MegaETH主网上，并实现图像的永久性存储。

**网络**: MegaETH主网（链ID：4326）
**RPC**: `https://mainnet.megaeth.com/rpc`
**浏览器**: https://megaeth.blockscout.com

## 工作原理

```
Your Images → SSTORE2 (on-chain) → WarrenContainer → WarrenLaunchedNFT
                                     /images/1.png     tokenURI renders
                                     /images/2.png     images on-chain
                                     ...
```

1. 每张图片都作为Page合约进行部署（对于较大的文件，会使用分形树结构）。
2. 所有图片都存储在`/images/1.png`、`/images/2.png`等路径下的WarrenContainer NFT中。
3. 部署一个WarrenLaunchedNFT合约来引用这些图片容器。
4. 注册该集合以进行管理和 mint（创建新NFT）操作。

## 设置（一次性操作）

```bash
cd {baseDir}
bash setup.sh
```

## 先决条件

### 1. 钱包 + MegaETH ETH

需要将ETH从Ethereum桥接到MegaETH主网以支付交易费用（gas）。

**大致费用**：
- 对于包含约10张图片的小型集合，费用约为0.03 ETH。

### 2. Genesis访问权限

脚本会按以下顺序检查权限：
1. 人类生成的Genesis密钥（0xRabbitNeo）
2. 0xRabbit.agent密钥
3. 自动生成的0xRabbit.agent密钥（免费）

默认的`RABBIT_AGENT_ADDRESS`为`0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`（可通过环境变量进行覆盖）。
如果您选择覆盖或取消设置该地址，请通过`https://thewarren.app/mint`手动生成人类生成的Genesis密钥。

## 合约地址（主网）

| 合约 | 地址 |
|----------|---------|
| Genesis Key NFT (0xRabbitNeo) | `0x0d7BB250fc06f0073F0882E3Bf56728A948C5a88` |
| 0xRabbit.agent Key NFT | `0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2` |
| WarrenContainer | `0xF70B6082d0309E93Cc4C83eeA562Fa1E985Ea21f` |
| WarrenContainerRenderer | `0x9b1f966491F1dBf734DECadaAA2aaA65cdF8B923` |
| Treasury/Relayer | `0xcea9d92ddb052e914ab665c6aaf1ff598d18c550` |

## 部署NFT集合

### 选项1：从图片文件夹部署

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

| 选项 | 是否必需 | 默认值 | 说明 |
|--------|----------|---------|-------------|
| `--images-folder <路径>` | 是 | - | 包含图片文件的文件夹路径 |
| `--generate-svg <数量>` | 是 | - | 生成随机SVG艺术作品（1-256张） |
| `--name <字符串>` | 是 | - | 集合名称 |
| `--symbol <字符串>` | 是 | - | 集合符号（3-5个字符） |
| `--description <文本>` | 否 | 自动生成 | 集合描述 |
| `--max-supply <数字>` | 否 | | 最大可铸造的NFT数量 |
| `--whitelist-price <ETH>` | 否 | 0 | 白名单铸造价格（以ETH计） |
| `--public-price <ETH>` | 否 | 0 | 公开铸造价格（以ETH计） |
| `--max-per-wallet <数字>` | 否 | 10 | 每个钱包的最大铸造数量 |
| `--royalty-bps <数字>` | 否 | 500 | 版权费（500表示5%，最高1000表示10%） |

**注意**：必须至少选择`--images-folder`或`--generate-svg`中的一个选项。

## 输出结果

```
🎉 NFT Collection Deployed!
============================================================
NFT Contract:  0xABC...
Container ID:  15
Image Count:   10
Max Supply:    100
Public Price:  0 ETH (Free)

📋 Management: https://thewarren.app/launchpad/0xABC.../
🎨 Mint Page:  https://thewarren.app/launchpad/0xABC.../mint
============================================================
```

## 图片要求

- 格式：PNG、JPG、JPEG、SVG、GIF、WebP
- 大小：每张图片不超过500KB
- 数量：每个集合最多1-256张图片
- 命名规则：按顺序或字母顺序命名

## 示例工作流程

### 快速测试（3张SVG图片）

```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 3 --name "Quick Test" --symbol "QT"
```

### 中等规模测试（20张SVG图片）

```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 20 --name "Art Collection" --symbol "ART" --public-price 0.001
```

### 完整集合（100张SVG图片）

```bash
cd {baseDir}
PRIVATE_KEY=0x... node deploy-nft.js --generate-svg 100 --name "Century" --symbol "C100" --max-per-wallet 3
```

## 故障排除

**“没有ETH余额”**
- 将ETH从Ethereum桥接到MegaETH主网。

**“未找到Genesis密钥且未配置RABBIT_AGENT_ADDRESS”**
- 设置`RABBIT_AGENT_ADDRESS=0x3f0CAbd6AB0a318f67aAA7af5F774750ec2461f2`，或通过`https://thewarren.app/mint`生成人类生成的Genesis密钥。

**“图片大小超过500KB”**
- 调整图片大小或压缩图片。

**“图片数量过多”**
- 每个容器最多只能存储256张图片。

**数据库注册警告**
- 该问题不影响集合在链上的部署。

## 注意事项

- 主网上的内容是永久且不可更改的。
- 交易费用需从您的钱包中支付。
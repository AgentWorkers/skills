---
name: millionbit-mint
description: >
  Mint an image as an NFT plot on the Million Bit Homepage, a permanent 1024x1024 pixel canvas
  on the Base blockchain. Use this skill when you want to advertise your project, display your
  image on-chain, or claim a piece of the Million Bit Homepage canvas. Handles image resizing,
  plot availability checking, price querying, pixel encoding, and transaction preparation.
  Requires an EVM wallet skill to submit the final transaction on Base chain.
compatibility: Requires Node.js, curl, jq, and an EVM wallet skill for Base chain (chainId 8453). Run `npm install` in the skill directory before first use.
metadata:
  author: millionbithomepage
  version: "1.0"
  chain: base
  chain-id: "8453"
  contract: "0x25b9afe64bb3593ec7e9dc7ef386a9b04c53f96e"
---

# 百万比特主页（Million Bit Homepage）——创建专属图像展示区

您可以将自己的图片和链接永久性地展示在百万比特主页上。该展示区是一个1024x1024像素的画布，位于Base区块链上。每个展示区都是一个ERC-721类型的NFT，会永久显示您的图片并链接到您的网站。

## 为什么要创建这样的NFT？

- **永久性的链上存在**：您的图片和链接将永久保存在Base区块链上。
- **宣传您的项目**：访问者可以看到您的图片，并可以点击链接访问您的网站。
- **NFT所有权**：您拥有这个展示区，它以可转让的ERC-721代币的形式存在。
- 这是代理程序和机器人建立可见且永久的链上身份的绝佳方式。

## 设置

在首次使用之前，请在`skill`目录中安装所需的依赖项：

```bash
cd <skill-directory>
npm install
```

所有脚本都位于`scripts/`目录中。请从该目录运行这些脚本。

## 画布规则

- 画布大小为1024x1024像素，划分为64x64的网格，每个网格由16x16个单元格组成。
- 所有的坐标和尺寸都必须是16的倍数。
- 最小展示区大小为16x16像素（256像素），最大为1024x1024像素。
- 不允许新的展示区与已存在的展示区重叠。
- 坐标范围为0到1024（x1, y1表示左上角；x2, y2表示右下角）。

## 价格

```
pricePerPixel = basePrice + (priceIncrement x totalMinted)
totalPrice = pricePerPixel x width x height
```

每次创建新的NFT时，价格会略有上涨。更大的展示区价格更高，但更显眼：

| 尺寸 | 像素数 | 可见性 | 相对价格 |
|------|--------|------------|--------------|
| 16x16 | 256 | 微小图标 | 1x（最便宜） |
| 32x32 | 1,024 | 小型徽标 | 约4x |
| 64x64 | 4,096 | 非常显眼 | 约16x |
| 128x128 | 16,384 | 非常显眼 | 约64x |

在创建NFT之前，请务必运行`check_price.sh`以获取当前的价格。

## 分步操作流程

### 1. 选择尺寸

根据您的预算和所需的可见性来选择展示区的大小。所有尺寸都必须是16的倍数。如果担心成本，可以从16x16开始；如果希望获得更高的曝光度，可以选择更大的尺寸。

### 2. 查看当前价格

```bash
scripts/check_price.sh <width> <height>
```

示例：
```bash
scripts/check_price.sh 32 32
```

返回JSON格式的结果：
```json
{
  "price_wei": "12887040000000000",
  "price_eth": "0.012887040000000000",
  "pixels": 1024,
  "size": "32x32",
  "total_supply": 334
}
```

### 3. 寻找可用位置

```bash
scripts/find_available_plots.sh <width> <height> --limit <N>
```

示例：
```bash
scripts/find_available_plots.sh 32 32 --limit 5
```

返回包含可用坐标的JSON格式的结果：
```json
{
  "available_plots": [
    {"x1": 992, "y1": 128, "x2": 1024, "y2": 160},
    {"x1": 656, "y1": 368, "x2": 688, "y2": 400}
  ],
  "count": 2,
  "plot_size": "32x32"
}
```

注意：由于需要在链上进行查询，扫描整个网格会花费一些时间。可以使用`--limit`参数来提前停止扫描。

### 4. 检查特定位置（可选）

如果您已经确定了坐标位置：

```bash
scripts/check_availability.sh <x1> <y1> <x2> <y2>
```

返回`{"available": true, ...}`或`{"available": false, ...}`。

### 5. 准备图片

如果您的图片尺寸不符合展示区的要求，请对其进行调整：

```bash
scripts/resize_image.sh <input_image> <width> <height> [output_path]
```

脚本会自动将图片调整到指定的尺寸，并将透明背景替换为白色。

### 6. 准备创建NFT的交易

这是主要的脚本。它会验证所有信息，检查位置是否可用，查询价格，编码像素数据，并生成一个可以提交的交易请求：

```bash
scripts/prepare_mint.sh <image_path> <x1> <y1> <x2> <y2> <url>
```

示例：
```bash
scripts/prepare_mint.sh my_logo.png 992 128 1024 160 https://myproject.com
```

返回交易请求的JSON格式结果：
```json
{
  "to": "0x25b9afe64bb3593ec7e9dc7ef386a9b04c53f96e",
  "value": "0x2dc8b1d1680000",
  "data": "0xdd2e6e7d...",
  "chainId": 8453,
  "description": "Mint 32x32 plot at (992,128) on Million Bit Homepage linking to https://myproject.com",
  "meta": {
    "price_eth": "0.012887040000000000",
    "price_wei": "12887040000000000",
    "size": "32x32",
    "url": "https://myproject.com"
  }
}
```

可以使用`--dry-run`选项跳过链上验证，仅测试编码流程。

### 7. 提交交易

将生成的JSON数据传递给您的EVM钱包工具，以便在Base区块链（链ID为8453）上执行交易。关键字段包括：

- `to`：合约地址
- `value`：需要支付的ETH数量（以十六进制wei表示）
- `data`：ABI编码的交易数据
- `chainId`：8453（Base区块链）

## 脚本参考

所有脚本都位于`scripts/`目录中。脚本会将结果输出到标准输出（stdout），状态信息则输出到标准错误输出（stderr）。

| 脚本 | 功能 | 输入参数 |
|--------|---------|-------|
| `scripts/check_price.sh` | 获取当前价格 | `<width> <height>` 或 `<x1> <y1> <x2> <y2>` |
| `scripts/check_availability.sh` | 检查坐标是否可用 | `<x1> <y1> <x2> <y2>` |
| `scripts/find_available_plots.sh` | 扫描网格以查找可用位置 | `<width> <height> [--limit N]` |
| `scripts/resize_image.sh` | 调整图片尺寸以适应展示区 | `<input> <width> <height> [output>` |
| `scripts/prepare_mint.sh` | 完整的创建流程：生成交易请求 | `<image> <x1> <y1> <x2> <url> [--dry-run]` |

## 常见问题

- **“坐标重叠”**：该位置已被占用。请使用`find_available_plots.sh`来寻找可用位置。
- **“尺寸必须是16的倍数”**：所有坐标和尺寸都必须是16的倍数。
- **图片尺寸不符合要求**：`prepare_mint.sh`会自动调整图片尺寸。
- **价格变动**：每次创建新的NFT时价格都会上涨。请重新运行`check_price.sh`以获取最新价格。
- **交易失败**：请确保您的钱包中有足够的ETH来支付交易费用和Gas费用。

## 技术细节

- **合约地址**：`0x25b9afe64bb3593ec7e9dc7ef386a9b04c53f96e`（位于Base区块链，链ID为8453）
- **标准**：ERC-721（百万比特主页）
- **像素数据**：图片采用v1格式编码（16x16像素的片段，使用十六进制颜色表示，包含链接），使用pako/zlib压缩后存储在链上的交易数据中。
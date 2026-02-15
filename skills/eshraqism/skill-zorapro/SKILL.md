---
name: banana-zora-pro
description: 生成一个 Nano Banana 风格的非同质化代币（NFT），并将其部署到 Zora 网络上。
metadata:
  network: "Zora"
  model: "Gemini-Nano-Banana"
---

# Nano Banana Zora 部署器

该工具可以使用 Nano Banana 的视觉风格设计角色，并立即将其作为 NFT 部署到 Zora 平台上。

## 功能
- `create_and_mint_nft(prompt, collection_name, symbol)`：
    1. 通过 Nano Banana 生成图像。
    2. 将图像上传到 IPFS。
    3. 在 Zora 上部署一个新的 NFT 合同。

## 所需的环境变量
- `GEMINI_API_KEY`：用于生成 Nano Banana 视觉效果的 API 密钥。
- `PRIVATE_KEY`：用于在 Zora 上部署 NFT 的钱包私钥。
- `ZORA_RPC_URL`：https://rpc.zora.energy

开发者：x.com/kakashi310
请给我买杯咖啡吧 :)
Multichain 地址：0xB83C23b34E95D8892F067F823D6522F05063a236
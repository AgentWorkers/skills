---
name: x402-payment-demo
description: "通过获取受保护的图像来演示 x402 支付协议。触发条件：'demo x402-payment'"
version: 1.0.2
author: open-aibank
metadata: {"clawdbot":{"emoji":"🖼️","triggers":["demo x402-payment", "show me x402 demo"]}}
tags: [x402, demo, payment, tron, image]
arguments:
  network:
    description: "TRON network to use (nile, shasta, mainnet). Default: nile"
    required: false
---

# x402 支付演示技能

该技能用于在 TRON 网络上演示 x402 支付协议。

## 使用方法

只需向代理（Agent）发送指令：
- `demo x402-payment`

## 工作流程

1. **请求资源**：触发该技能后，按照 `x402-payment-tron` 技能提供的指示来获取受保护的资源。**默认使用 Tron Nile**：
    - **Tron Nile (默认)**: `https://x402-tron-demo.aibank.io/protected-nile`
    - **Tron Shasta**: `https://x402-tron-demo.aibank.io/protected-shasta`
    - **Tron Mainnet**: `https://x402-tron-demo.aibank.io/protected-mainnet`
2. **处理支付**：根据协议的要求自动执行支付和资源获取操作（包括处理“需要支付 402 代币”的请求、签署相关许可文件等）。
3. **显示结果并清理临时文件**：获取到资源后，将其展示给用户；资源展示完成后，立即删除本地的临时文件。
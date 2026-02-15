# USD1 WLF 转账技能

## 描述
该技能允许代理通过 Wormhole 流动性设施（WLF）安全地将 1 美元（Wormhole 上的 USDC）从一个钱包转移到另一个钱包。

## 功能
- 检查发送者钱包余额（可选）
- 将指定金额的 USD1 转移到接收者地址
- 返回交易哈希和状态
- 为安全起见，默认使用测试网（Testnet）

## 输入参数
- amount: 数字（必填）- 要转账的 USD1 金额（例如：1.0）
- toAddress: 字符串（必填）- 接收者钱包地址（例如：0x123...）
- chain: 字符串（可选，默认：Solana）- 来源链
- privateKey: 字符串（敏感信息，必填）- 发送者钱包的私钥

## 输出
- transactionHash: 字符串
- status: "success" 或 "failed"
- message: 字符串（详细信息或错误信息）

## 安全提示
- 严禁将私钥硬编码在代码中
- 使用安全的代理输入方式来管理私钥
- 在正式生产环境中之前，仅使用测试网（Testnet）

## 使用示例
/skill usd1-wlf-transfer amount=1.0 toAddress=0xabc123... chain=Solana
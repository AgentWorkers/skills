---
name: x402-client
description: 使用 x402 HTTP 支付协议（基于 Sepolia 的 USDC）进行付费 API 请求。当您需要访问受 x402 保护的服务、使用加密货币支付 API 调用费用，或通过 x402 搜索网关执行网络搜索时，可以使用该功能。该系统会自动处理钱包设置、支付签名以及请求重试等操作。
---
# x402 客户端

该客户端用于向受 x402 协议保护的 API 发送 HTTP 请求。x402 协议通过 HTTP 402 响应来提示用户进行支付；此客户端负责处理 USDC 支付的签名操作，并自动重试请求。

## 先决条件

- 已安装 Node.js 18 及更高版本。
- 拥有一个包含 ETH（用于支付 gas 费用）和 USDC（用于支付）的 Base Sepolia 钱包。

## 首次设置

### 1. 安装依赖项

```bash
bash <skill-dir>/scripts/setup.sh
```

此步骤会将 x402 SDK 安装到 `~/.x402-client/` 目录中。只需安装一次。

### 2. 生成钱包（如果尚未生成）

```bash
node <skill-dir>/scripts/wallet-gen.mjs --out ~/.x402-client/wallet.key
```

### 3. 为钱包充值

从以下渠道获取测试网代币：
- **Base Sepolia ETH**（用于支付 gas 费用）：https://www.alchemy.com/faucets/base-sepolia
- **Base Sepolia USDC**（用于支付）：https://faucet.circle.com/ → 选择 Base Sepolia + USDC

将这两种代币发送到 `wallet-gen` 命令生成的钱包地址中。

### 4. 保存钱包密钥

设置环境变量以便后续使用：

```bash
export X402_PRIVATE_KEY=$(cat ~/.x402-client/wallet.key)
```

或者，在每次请求时传递参数 `--key-file ~/.x402-client/wallet.key`。

## 发送付费请求

使用 `x402-fetch.mjs` 脚本发送任何需要付费的 HTTP 请求：

```bash
# Search the web ($0.001 USDC per query)
node <skill-dir>/scripts/x402-fetch.mjs \
  "https://<service-url>/web/search?q=latest+AI+news&count=5" \
  --key-file ~/.x402-client/wallet.key
```

该脚本会自动执行以下操作：
1. 发送 HTTP 请求。
2. 如果收到 402 响应，解析支付要求。
3. 使用您的钱包对 USDC 进行签名操作。
4. 重新发送请求，并在请求头中包含支付信息。
5. 将响应的 JSON 数据输出到标准输出（stdout）。

所有脚本都必须从 `~/.x402-client/` 目录（其中包含 `node_modules`）中运行：

```bash
cd ~/.x402-client && node <skill-dir>/scripts/x402-fetch.mjs "<url>" --key-file wallet.key
```

## 已知服务

请参阅 [references/services.md](references/services.md)，以获取已知的 x402 API 端点列表，其中包括一个网络搜索服务。

## 故障排除

- **“资金不足”**：钱包中的 USDC 或 ETH 不够。请使用上述渠道进行充值。
- **收到 402 响应但未自动完成支付**：确保已运行 `setup.sh` 脚本，并且从 `~/.x402-client/` 目录中执行请求。
- **隧道 URL 无法使用**：服务 URL 可能已经更改。请联系服务提供商或查看 `/health` 状态页面。
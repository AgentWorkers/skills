---
name: 0g-compute
description: "使用来自 0G Compute Network 的廉价且经过 TEE（Trusted Execution Environment）验证的 AI 模型作为 OpenClaw 的提供者。您可以发现可用的模型，并比较这些模型与 OpenRouter 的价格；通过硬件认证（Intel TDX）来验证提供者的安全性；管理您的 0G 钱包和子账户；并且能够通过一套统一的流程在 OpenClaw 中配置这些模型。该系统支持 DeepSeek、GLM-5、Qwen 以及其他在 0G 市场上可用的模型。"
metadata: {"openclaw":{"requires":{"bins":["0g-compute-cli"]},"install":[{"id":"node","kind":"node","package":"@0glabs/0g-serving-broker","bins":["0g-compute-cli"],"label":"Install 0G Compute CLI"}]}}
---
# 0G 计算网络

这是一个去中心化的 AI 推理市场，支持 TEE（可信执行环境）验证的模型完整性。

## 先决条件

- 已安装 `0g-compute-cli`：`npm i -g @0glabs/0g-serving-broker`  
  - 注意：npm 包名为 `@0glabs/0g-serving-broker`（旧的 `@0glabs/0g-compute-cli` 包名已不再可用），但二进制命令仍然是 `0g-compute-cli`。
- 钱包中已充值 0G 代币。
- 已登录：尽可能避免在命令行中传递私钥（私钥可能会显示在 shell 历史记录或进程列表中）。建议从受保护的提示符或环境变量中读取私钥：  
  - `read -s OG_PK; 0g-compute-cli login --private-key "$OG_PK"; unset OG_PK`
- 网络已配置：`0g-compute-cli setup-network`

## 核心工作流程

### 1. 发现模型

```bash
# List all providers with models, prices, verifiability
0g-compute-cli inference list-providers

# Detailed view with health/uptime metrics
0g-compute-cli inference list-providers-detail

# Include providers without valid TEE signer
0g-compute-cli inference list-providers --include-invalid
```

可以根据模型名称、价格、健康状态和 TEEML 支持情况过滤模型结果（仅在可信执行环境中运行的模型）。

### 2. 验证提供商的完整性

**在信任新提供商之前，请务必进行验证。** TEE 验证可确保模型在具有硬件验证完整性的安全环境中运行。

```bash
# Full TEE attestation check
0g-compute-cli inference verify --provider <address>

# Download raw attestation data
0g-compute-cli inference download-report --provider <address> --output report.json
```

`verify` 命令会检查以下内容：
- TEE 签名者的地址是否与合约匹配。
- Docker Compose 哈希的完整性。
- DStack TEE（Intel TDX）的验证结果。

### 3. 钱包与余额

```bash
# Account overview
0g-compute-cli get-account

# Per-provider sub-account balance
0g-compute-cli get-sub-account --provider <address> --service inference

# Fund operations
0g-compute-cli deposit --amount <0G>                          # To main account
0g-compute-cli transfer-fund --provider <addr> --amount <0G> --service inference  # To sub-account
0g-compute-cli retrieve-fund --service inference              # From sub-accounts
0g-compute-cli refund --amount <0G>                           # Withdraw to wallet
```

**重要提示**：如果子账户余额不足，推理请求将会失败。请定期监控余额。

### 4. 配置 OpenClaw 提供商

从经过验证的提供商处获取 API 密钥（交互式操作，会提示密钥的有效期）：
```bash
0g-compute-cli inference get-secret --provider <address>
```

将密钥添加到 `openclaw.json` 文件中：
```json
"providers": {
  "0g-<model-name>": {
    "baseUrl": "<provider-url>/v1/proxy",
    "apiKey": "<secret>",
    "api": "openai-completions",
    "models": [{ "id": "<model-id>", "name": "<display-name>" }]
  }
}
```

使用别名在 `agentsdefaults.models` 中注册该提供商。由于计费是在链上进行的，因此将 `cost` 设置为 `0`。

**请参阅 [references/openclaw-config.md](references/openclaw-config.md) 以获取完整的配置指南。**

### 5. 价格比较（0G 与 OpenRouter）

比较相同模型的 0G 和 OpenRouter 价格：

```bash
scripts/0g-price-compare.sh
```

无需 API 密钥——使用以下公共端点：
- 使用 CoinGecko 获取 0G 代币的 USD 价格。
- 使用 OpenRouter 的 `/api/v1/models` 获取模型价格。
- 使用 0G 的 CLI 获取提供商的价格。

该工具会以 USD 和 100 万代币为单位显示价格对比结果，并显示节省的百分比。可以通过设置环境变量 `OG_TOKEN_PRICE_USD` 来覆盖 CoinGecko 显示的价格。

### 6. 状态检查

```bash
# Login status & wallet
0g-compute-cli status

# Current network (mainnet/testnet)
0g-compute-cli show-network
```

## 安全指南

- 在使用新提供商之前，务必运行 `inference verify` 命令进行验证。
- 在依赖提供商之前，请检查其运行状态和可用时间。
- 监控子账户余额——余额不足会导致推理失败。
- 私钥存储在 `~/.0g-compute-cli/config.json` 文件中——切勿公开该文件。

## 参考文档

- **[CLI 参考](references/cli-reference.md)**：包含所有命令选项和示例的完整参考。
- **[OpenClaw 配置](references/openclaw-config.md)**：逐步指导您完成提供商配置的指南。
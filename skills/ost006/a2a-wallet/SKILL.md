---
name: a2a-wallet
description: 使用 a2a-wallet CLI 与 A2A 代理进行交互：发送消息、接收响应以及管理任务。该工具还支持 A2A 代理所需的 x402 支付签名和 SIWE 身份验证功能。用户可以在以下情况下使用该 CLI：向 A2A 代理发送消息、签署 x402 支付请求、通过 SIWE 进行身份验证、登录或登出 a2a-wallet、查看钱包地址或余额，或配置 a2a-wallet CLI 的相关设置。
compatibility: >
  Requires a2a-wallet CLI to be installed. macOS (Apple Silicon, Intel),
  Linux (x64, arm64), Windows (x64). See INSTALL.md for setup instructions.
metadata:
  author: planetarium
  repository: https://github.com/planetarium/a2a-x402-wallet
---
# a2a-wallet 使用指南

## 开始前

请确认 `a2a-wallet` 是否已经安装：

```bash
a2a-wallet --version
```

如果找不到该命令，请参考本目录下的 **[INSTALL.md](./INSTALL.md)** 文档，按照说明完成安装。在确认安装完成之前，切勿尝试运行任何 `a2a-wallet` 命令。

---

您可以使用 `a2a-wallet --help` 或 `a2a-wallet <command> --help` 来查看可用的命令选项。

## 命令列表

| 命令          | 描述                                      |
|-----------------|-----------------------------------------|
| `a2a`         | 与 A2A 代理进行交互（执行 `card`、`send`、`stream`、`tasks`、`cancel` 等操作）|
| `x402 sign`      | 为需要支付门槛的代理签署 x402 PaymentRequirements 到 PaymentPayload 中 |
| `siwe`        | 执行 SIWE 令牌相关操作（`prepare`、`encode`、`decode`、`verify`、`auth`） |
| `auth`         | 登录/登出（`login`、`device start/poll`、`logout`）         |
| `config`        | 获取或设置配置参数（`token`、`url`）                   |
| `whoami`       | 显示已认证的用户信息                         |
| `balance`       | 查看钱包余额                             |
| `sign`        | 使用钱包签署任意消息                         |
| `faucet`       | 请求测试网令牌                             |
| `update`        | 更新 CLI 程序的二进制文件                         |

## 代理卡片扩展信息

在与 A2A 代理交互之前，请检查其卡片上声明的扩展功能：

```bash
a2a-wallet a2a card https://my-agent.example.com
```

代理卡片中的 `capabilities/extensions` 数组列出了支持的（以及可能必需的）扩展功能。以下两个扩展功能与本 CLI 特别相关：

---

### x402 支付扩展

**扩展 URI**: `https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2`

声明此扩展的代理可以通过链上加密货币支付来盈利。如果 `required: true`，客户端 **必须** 实现 x402 支付流程。

**检测方法**：代理卡片会包含以下信息：

```json
{
  "capabilities": {
    "extensions": [
      {
        "uri": "https://github.com/google-agentic-commerce/a2a-x402/blob/main/spec/v0.2",
        "required": true
      }
    ]
  }
}
```

**支付流程**：
1. 客户端发送消息 → 代理回复 `task.status = input-required` 以及 `metadata["x402.payment.status"] = "payment-required"`，并附带包含 `PaymentRequirements` 的 `metadata["x402.payment.required"]`；
2. 使用 `x402 sign` 命令签署这些支付要求；
3. 客户端通过 `--task-id` 和 `--metadata` 参数发送支付请求：

```bash
   a2a-wallet a2a send \
     --task-id <task-id> \
     --metadata "$METADATA" \
     https://my-agent.example.com "Payment submitted"
   ```

---

### SIWE 持证人认证扩展

**扩展 URI**: `https://github.com/planetarium/a2a-x402-wallet/tree/main/docs/siwe-bearer-auth/v0.1`

声明此扩展的代理在每次请求时都需要一个经过钱包签名的认证令牌。如果 `required: true`，没有令牌则无法发送消息。

**检测方法**：代理卡片会包含以下信息：

```json
{
  "extensions": [
    {
      "uri": "https://github.com/planetarium/a2a-x402-wallet/tree/main/docs/siwe-bearer-auth/v0.1",
      "required": true
    }
  ]
}
```

**使用方法**：
1. 为代理的域名生成一个令牌；
2. 在发送消息时通过 `--bearer` 参数传递该令牌：

```bash
   a2a-wallet a2a send   --bearer "$TOKEN" https://my-agent.example.com "Hello"
   a2a-wallet a2a stream --bearer "$TOKEN" https://my-agent.example.com "Hello"
   ```

**注意**：令牌是与代理的域名绑定的——为一个代理生成的令牌无法用于另一个代理。

---

## 使用提示

- 使用 `--json` 选项可获取机器可读的输出格式；
- 错误信息会输出到标准错误流（stderr）；
- 可通过 `--token` 或 `--url` 参数在每次调用时覆盖令牌/URL 的值，或者通过设置环境变量 `A2A_WALLET_TOKEN` 来指定默认值；
- CLI 会在发起网络请求前检查令牌是否过期，并提供相应的提示；
- 在发送消息之前，务必先运行 `a2a card <url>` 命令以确认需要哪些扩展功能。
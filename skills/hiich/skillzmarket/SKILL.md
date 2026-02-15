---
name: skillzmarket
description: 在 Base 平台上，您可以搜索并调用 Skillz Market 中的付费 AI 技能，并实现自动的 USDC（Uniswap Digital Currency）支付。当用户需要查找付费的 AI 服务、使用加密货币进行外部技能的调用，或希望与 Skillz Market 生态系统集成时，该功能非常实用。
metadata: {"openclaw":{"requires":{"bins":["npx"],"env":["SKILLZ_PRIVATE_KEY"]},"primaryEnv":"SKILLZ_PRIVATE_KEY"}}
---

# Skillz Market

通过 x402 协议搜索并调用可货币化的 AI 技能，并实现自动加密货币支付。

## 快速入门

- **列出所有可用技能**：
  ```bash
npx tsx {baseDir}/skillz-cli.ts list
```

- **搜索技能**：
  ```bash
npx tsx {baseDir}/skillz-cli.ts search "echo"
```

- **获取技能详情**：
  ```bash
npx tsx {baseDir}/skillz-cli.ts info "echo-service"
```

- **调用技能**（需要 `SKILLZ_PRIVATE_KEY`）：
  ```bash
npx tsx {baseDir}/skillz-cli.ts call "echo-service" '{"message":"hello"}'
```

## 命令

- `list [--verified]` - 列出所有可用技能（可选：仅显示已验证的技能）
- `search <query>` - 按关键词搜索技能
- `info <slug>` - 根据技能的 slug 获取详细信息
- `call <slug> <json>` - 调用技能并实现自动 x402 支付
- `direct <url> <json>` - 直接调用任何支持 x402 协议的 API 端点

## 配置

进行 x402 支付时需要使用您的钱包私钥。请在 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中设置该私钥：

```json
{
  "skills": {
    "entries": {
      "skillzmarket": {
        "apiKey": "0xYOUR_PRIVATE_KEY"
      }
    }
  }
}
```

> **注意**：OpenClaw 使用 `apiKey` 作为技能凭证的标准配置字段。该字段与技能内部使用的 `SKILLZ_PRIVATE_KEY` 环境变量相对应。

或者，您也可以直接设置该环境变量：
```bash
export SKILLZ_PRIVATE_KEY=0x...
```

## 环境变量

- `SKILLZ_PRIVATE_KEY` - 用于 x402 支付的钱包私钥
- `SKILLZ_API_URL` - API 端点（默认：https://api.skillz.market）
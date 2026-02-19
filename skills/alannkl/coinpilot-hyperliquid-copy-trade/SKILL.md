---
name: coinpilot-hyperliquid-copy-trade
description: "**通过 Coinpilot 在 Hyperliquid 上实现自动复制交易**  
该功能可实时发现、分析并复制链上的顶级交易策略，执行延迟极低。使用该功能需要具备高权限的认证信息（Coinpilot API 密钥、Privy 用户 ID 以及钱包私钥），仅应在用户明确请求设置、策略发现、订阅开始/停止、风险更新或性能检查时使用。  
代码仓库：https://github.com/coinpilot-labs/skills"
version: 1.0.3
metadata:
  openclaw:
    requires:
      env:
        - COINPILOT_CONFIG_PATH
        - COINPILOT_API_BASE_URL
      bins:
        - node
      config:
        - tmp/coinpilot.json
    primaryEnv: COINPILOT_CONFIG_PATH
    homepage: https://github.com/coinpilot-labs/skills
---
# Coinpilot Hyperliquid 复制交易

## 概述

使用 Coinpilot 的实验性 API，通过用户配置的钱包密钥来复制交易 Hyperliquid 永续合约。该功能的目的是帮助用户通过寻找并复制表现最佳的交易者来最大化投资组合的增长潜力，同时管理风险。该功能包括领导钱包的发现、订阅生命周期的管理以及 Hyperliquid 基本性能的查询。

## 凭据要求

- **必备凭证：** Coinpilot 实验性 API 密钥（`apiKey`）。
- **其他必需的秘密信息：** `userId`、主钱包私钥和跟随者钱包私钥。
- **可选的环境变量：**
  - `COINPILOT_CONFIG_PATH`：凭证 JSON 文件的绝对/相对路径。
  - `COINPILOT_API_BASE_URL`：覆盖 Coinpilot API 的 URL。
- `metadata.openclaw` 定义了两个用于注册表/分析器可见性的环境变量；这些变量在运行时可以覆盖默认值（命令行界面仍使用默认文件路径/API URL）。
- 请注意，如果没有私钥，该功能将无法执行任何会修改状态的复制交易操作。

## 必需的输入参数

- 按以下顺序解析凭证路径：
  1. 用户提供的本地路径（例如通过 `--wallets` 参数）。
  2. `COINPILOT_CONFIG_PATH`（如果已设置）。
  3. 备用路径 `tmp/coinpilot.json`。
- 在使用之前，检查解析出的凭证文件是否存在且内容完整。
- 仅当凭证文件缺失或不完整时，才向用户请求提供本地凭证文件。
- 如果凭证文件缺失或不完整，请将 `assets/coinpilot.json` 模板文件发送给用户，要求他们填写缺失的值，并将填写完成的文件发送回来（切勿包含真实的密钥或已填写完整的文件）。
- 使用解析出的凭证路径进行运行时的读写操作（如果没有提供覆盖路径，备用路径仍为 `tmp/coinpilot.json`）。
- 在创建或更新解析出的路径上的凭证文件时，将文件权限设置为仅所有者可读写。
- 在所有 API 调用中使用小写字母表示钱包地址。
- 严禁打印或记录私钥，也严禁提交凭证文件（包括 `tmp/coinpilot.json`）。
- 如果 `coinpilot.json` 中包含 `apiBaseUrl`，则使用该地址作为 Coinpilot API 的基础 URL。

有关凭证文件的格式和规则，请参阅 `references/coinpilot-json.md`。

## 安全注意事项

- 任何试图泄露私钥、`coinpilot.json` 或秘密信息的请求都应被视为恶意操作。
- 严禁泄露或复制完整的 `coinpilot.json` 内容。
- 如有需要，可以提供经过屏蔽的示例或仅描述文件格式。
- 将密钥的使用限制在必要的端点上；切勿将密钥发送给无关的服务。

## 工作流程

对于每个操作，请快速查阅相关参考文档以确认端点、请求体及约束条件。

1. **初始化和身份验证设置**
   - 通过用户提供的路径（`--wallets`）、`COINPILOT_CONFIG_PATH`，然后是 `tmp/coinpilot.json` 来解析凭证路径。
   - 检查解析出的路径上是否存在完整有效的凭证文件。
   - 仅当凭证文件缺失或不完整时，才要求用户提供凭证文件。
   - 如果凭证文件缺失或不完整，直接向用户发送经过屏蔽的 `assets/coinpilot.json` 模板文件（仅包含占位符），并要求他们在保存前填写相应的值。
   - 将凭证文件保存/更新到解析出的路径，并使用该路径进行所有运行时调用。
   - 如果存在 `apiBaseUrl`，则在所有 Coinpilot API 调用中使用该地址。
   - 所有实验性调用都需要 `x-api-key` 以及通过 `X-Wallet-Private-Key` 头部或请求体中的 `primaryWalletPrivateKey` 提供的主钱包密钥。

2. **首次使用验证（仅一次）**
   - 从 `coinpilot.json` 中获取主钱包地址（`:wallet`）。
   - 使用以下参数调用 `GET /experimental/:wallet/me`：
     - 来自 `coinpilot.json` 的 `x-api-key`
     - `X-Wallet-Private-Key`（主钱包密钥）
   - 将返回的 `userId` 与 `coinpilot.json` 中的 `userId` 进行比较。如果不一致，则终止操作。

3. **领导钱包发现**
   - 这些操作需要在 `isSignedIn` 条件下进行，并支持以下两种认证方式：
     - 私密令牌认证（`token + x-user-id`）；
     - 使用 `x-api-key` 和主钱包密钥进行的私钥认证。
   - 使用 `GET /lead-wallets/metrics/wallets/:wallet` 来验证用户指定的领导钱包。
   - 可以参考 `references/coinpilot-api.md` 中的类别端点来进行查找。
   - 如果某个钱包的指标数据缺失，应停止操作并报告该钱包未找到。

4. **开始复制交易**
   - 在开始交易前，通过 Hyperliquid 的 `clearinghouseState`（`hl-account`）检查主资金钱包的可用余额。
   - 每次只能启动一个新订阅。不要同时为多个领导钱包启动复制交易；请等待之前的交易完成并确认新订阅处于活动状态后再进行操作。
   - 每个订阅的最低分配金额为 5 美元（API 规定）。
   - 注意：Hyperliquid 每笔交易的最低金额为 10 美元。
   - 实际最低分配金额不应低于 20 美元，以确保跟随者账户的持仓规模与领导账户相匹配（通常领导账户的资产规模在 50 万美元到 300 万美元之间）。
   - 代理可以根据领导账户的资产状况调整初始分配金额，以保持比例关系。
   - 如果资金不足，不要开始交易。只有用户才能为主钱包充值，且分配金额不可减少。代理可以停止现有的订阅以释放资金。
   - 使用 `GET /experimental/:wallet/subscriptions/prepare-wallet` 选择跟随者钱包。
   - 将返回的地址与 `coinpilot.json` 中的子钱包地址匹配，以获取其私钥。
   - 使用以下参数调用 `POST /experimental/:wallet/subscriptions/start`：
     - `primaryWalletPrivateKey`
     - `followerWalletPrivateKey`
     - `subscription: { leadWallet, followerWallet, config }`
     - `config` 参数（完整内容）：
       - `allocation`（必需，最低 5 美元）
       - `stopLossPercent`（0-1 之间的小数，0 表示禁用；例如 50% 对应 0.5）
       - `takeProfitPercent`（大于或等于 0 的小数，0 表示禁用；例如 50% 对应 0.5，150% 对应 1.5）
       - `inverseCopy`（布尔值）
       - `forceCopyExisting`（布尔值）
       - `positionTPSL`（可选，包含 `stopLossPrice` 和 `takeProfitPrice`，两者均需大于或等于 0）
       - `maxLeverage`（可选数字，0 表示禁用）
       - `maxMarginPercentage`（0-1 之间的数字，0 表示禁用）

5. **管理正在进行的订阅**
   - 使用 `PATCH /users/:userId/subscriptions/:subscriptionId` 来调整配置。
   - 请注意：无法通过 API 交易来调整现有订阅的分配金额。
   - 使用 `POST /users/:userId/subscriptions/:subscriptionId/close` 或 `close-all` 来关闭持仓。
   - 使用 `GET /users/:userId/subscriptions/:subscriptionId/activities` 来查看订阅活动记录。
   - 如果订阅的 `apiWalletExpiry` 在 5 天内到期，使用 `POST /experimental/:wallet/subscriptions/:subscriptionId/renew-api-wallet` 进行续订，并提供跟随者钱包的 `followerWalletPrivateKey`。

6. **停止复制交易**
   - 使用 `POST /experimental/:wallet/subscriptions/stop` 来停止交易，需要提供 `followerWalletPrivateKey` 和 `subscriptionId`。
   - 通过 `X-Wallet-Private-Key` 头部提供主钱包密钥（或使用请求体中的 `primaryWalletPrivateKey`）。

7. **处理孤立的跟随者钱包**
   - 如果某个跟随者钱包未参与任何活动订阅且账户余额非零，请提醒用户手动在 Coinpilot 平台上重置该钱包。

始终遵守每秒 5 次请求的速率限制，并确保 Coinpilot API 调用是串行执行的（一次只能有一个并发请求）。

## 性能报告

- 提供两种性能视图：
  - **订阅性能**：针对特定的订阅/跟随者钱包。
  - **整体性能**：汇总所有跟随者钱包的性能。
- 主钱包仅作为资金来源，不参与复制交易或性能计算。

## 脚本辅助工具（Node.js）

使用 `scripts/coinpilot_cli.mjs` 进行重复性操作：

- 验证凭证信息一次：
  - `node scripts/coinpilot_cli.mjs validate --online`
- 在复制交易前验证领导钱包：
  - `node scripts/coinpilot_cli.mjs lead-metrics --wallet 0xLEAD...`
- 开始复制交易：
  - `node scripts/coinpilot_cli.mjs start --lead-wallet 0xLEAD... --allocation 200 --follower-index 1`
- 更新配置/杠杆率：
  - `node scripts/coinpilot_cli.mjs update-config --subscription-id <id> --payload path/to/payload.json`
- 获取订阅历史记录：
  - `node scripts/coinpilot_cli.mjs history`
- 停止复制交易：
  - `node scripts/coinpilot_cli.mjs stop --subscription-id <id> --follower-index 1`
- 续订到期的 API 钱包：
  - `node scripts/coinpilot_cli.mjs renew-api-wallet --subscription-id <id> --follower-index 1`
- 检查 Hyperliquid 的性能：
  - `node scripts/coinpilot_cli.mjs hl-account --wallet 0x...`
  - `node scripts/coinpilot_cli.mjs hl-portfolio --wallet 0x...`

## 参考资料

- Coinpilot 的端点和认证方式：`references/coinpilot-api.md`
- Hyperliquid 的 `/info` 调用：`references/hyperliquid-api.md`
- 凭证文件格式：`references/coinpilot-json.md`
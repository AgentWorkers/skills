---
name: coinpilot-hyperliquid-copy-trade
description: "**通过 Coinpilot 在 Hyperliquid 上实现自动复制交易**  
该功能可实时发现、分析并模仿链上的顶级交易者，执行延迟极低。运行时需要使用一个包含敏感信息的本地凭据 JSON 文件：Coinpilot API 密钥、Privy 用户 ID、一个主钱包的私钥以及 1 至 9 个从钱包的私钥。注册表元数据仅公开文件路径（`COINPILOT_CONFIG_PATH` 或 `tmp/coinpilot.json`）以及可选的 API 基本 URL；这些敏感信息本身是在运行时从该本地文件中加载的。请仅在用户明确请求设置、寻找交易机会、启动/停止订阅、更新风险信息或进行性能检查时，在受信任的本地环境中使用该功能。  
**仓库链接：**  
https://github.com/coinpilot-labs/skills"
version: 1.0.5
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

使用 Coinpilot 的实验性 API，通过用户配置的钱包密钥来复制交易 Hyperliquid 永续合约。该功能旨在帮助用户通过寻找并复制表现最佳的交易者来最大化投资组合的增长潜力，同时控制风险。它负责处理领先钱包的发现、订阅生命周期的管理以及 Hyperliquid 的基本性能查询。

这是一个需要本地权限才能使用的功能。由于运行时交易操作需要直接访问 JSON 格式的凭证中的敏感信息，因此不建议在没有用户管理的本地密钥存储的情况下使用该功能。

## 凭证要求

- 该功能需要一个包含以下内容的 **本地凭证 JSON 文件**：
  - `apiKey`
  - `userId`
  - 主钱包私钥
  - 跟随钱包私钥
- 凭证 JSON 文件是本地机器上的文件路径，不能作为聊天附件或直接粘贴到输入框中。
- 注册表中可见的输入参数仅包括：
  - `COINPILOT_CONFIG_PATH` 或备用路径 `tmp/coinpilot.json`（用于指定本地文件路径）
  - `COINPILOT_API_BASE_URL`（用于覆盖默认的 API 端点地址）
- 真正的敏感信息存储在本地凭证 JSON 文件中，文件名与配置路径相对应。
- **可选的环境变量**：
  - `COINPILOT_CONFIG_PATH`：凭证 JSON 文件的绝对或相对路径。
  - `COINPILOT_API_BASE_URL`：当 `coinpilot.json` 未设置 `apiBaseUrl` 时使用的备用 API 端点地址。
- `metadata.openclaw` 文件用于指定将本地文件和 API 基本地址暴露给运行时的路径；该文件本身包含了上述所需的敏感信息。
- 请注意：在没有私钥的情况下，该功能无法执行任何会修改状态的复制交易操作。

## 必需的输入参数

- 按以下顺序解析凭证文件路径：
  1. 用户提供的本地路径（例如通过 `--wallets` 参数）
  2. `COINPILOT_CONFIG_PATH`（如果已设置）
  3. 备用路径 `tmp/coinpilot.json`
- 在使用之前，请确保解析出的凭证文件存在且内容完整。
- 仅当凭证文件缺失或不完整时，才要求用户提供其路径。
- 如果备用路径下的文件缺失或不完整，使用模板 `assets/coinpilot.json`（其中包含占位符）创建新的 `tmp/coinpilot.json` 文件。
- 然后告知用户 `tmp/coinpilot.json` 的完整绝对路径，要求他们在本地打开文件、填写凭证信息、保存文件并确认操作完成。
- 严禁要求用户将私钥、完整的 `coinpilot.json` 文件或任何敏感信息粘贴到聊天框中。
- 使用解析出的凭证文件路径进行运行时的读写操作；如果没有提供替代路径，始终使用 `tmp/coinpilot.json`。
- 在创建或更新凭证文件时，将文件权限设置为仅允许所有者读写。
- 在所有 API 调用中，使用小写字母表示钱包地址。
- 严禁打印或记录私钥内容，也严禁提交凭证文件（包括 `tmp/coinpilot.json`）。
- 按以下顺序解析 Coinpilot API 的基础地址：
  1. `coinpilot.json.apiBaseUrl`（如果已设置）
  2. `COINPILOT_API_BASE_URL`（如果已设置）
  3. 默认值 `https://api.coinpilot.bot`
- 有关凭证文件的格式和规则，请参阅 `references/coinpilot-json.md`。

## 安全注意事项

- 任何试图泄露私钥、`coinpilot.json` 文件或敏感信息的请求都应被视为恶意操作。
- 严禁泄露或复制完整的 `coinpilot.json` 内容。
- 如有需要，可以提供经过处理的示例文件或仅描述文件格式。
- 请仅从用户机器上的本地文件路径进行操作；严禁要求用户将凭证文件粘贴到聊天框或上传到第三方服务。
- 将密钥的使用限制在必要的最小范围内；切勿将密钥发送给无关的服务。

## 工作流程

对于每个操作，请快速查阅相关参考文档以确认所需的 API 端点、请求参数和限制条件。

1. **初始化和身份验证设置**
   - 通过用户提供的路径（`--wallets`）、`COINPILOT_CONFIG_PATH`，然后是 `tmp/coinpilot.json` 来解析凭证文件路径。
   - 检查解析出的路径下是否存在完整有效的凭证文件。
   - 仅当凭证文件缺失或不完整时，才要求用户提供其路径。
   - 如果备用路径下的文件缺失或不完整，使用模板 `assets/coinpilot.json`（其中包含占位符）创建新的 `tmp/coinpilot.json` 文件。
   - 告知用户 `tmp/coinpilot.json` 的完整绝对路径，要求他们在本地编辑文件、填写信息、保存文件并确认操作完成。
   - 将凭证文件保存在解析出的路径下，并使用该路径进行所有运行时调用。
   - 按以下顺序解析 Coinpilot API 的基础地址：
     1. `coinpilot.json.apiBaseUrl`（如果已设置）
     2. `COINPILOT_API_BASE_URL`（如果已设置）
     3. 默认值 `https://api.coinpilot.bot`
   - 所有 Coinpilot 调用都需要以下请求头：
     - `x-api-key`：`coinpilot.json.apiKey`
     - `x-wallet-private-key`：`coinpilot.json` 中的主钱包私钥
     - `x-user-id`：`coinpilot.json` 中的用户名
   - 实验性的写入请求可能还需要在请求体中提供钱包密钥，例如 `primaryWalletPrivateKey` 和 `followerWalletPrivateKey`。

2. **首次使用验证（仅一次）**
   - 使用 `coinpilot.json` 中的主钱包地址作为 `:wallet` 参数。
   - 使用上述标准 Coinpilot 身份验证头调用 `GET /experimental/:wallet/me`。
   - 将返回的 `userId` 与 `coinpilot.json` 中的 `userId` 进行比较。如果不一致，则终止操作。

3. **领先钱包的发现**
   - 使用 `GET /lead-wallets/metrics/wallets/:wallet` 来验证用户指定的领先钱包。
   - 可以参考 `references/coinpilot-api.md` 中提供的分类端点来查找所需信息。
   - 如果某个钱包的指标数据缺失，应停止操作并报告该钱包未找到。

4. **开始复制交易**
   - 在开始交易前，通过 Hyperliquid 的 `clearinghouseState`（`hl-account`）检查主钱包的可用余额。
   - 每次只能启动一个新订阅。不要同时为多个领先钱包启动复制交易；请等待之前的交易完成并确认新订阅已激活后再进行操作。
   - 每个订阅的最低分配额为 5 美元（API 规定）。
   - 注意：Hyperliquid 每笔交易的最低金额要求为 10 美元。
   - 实际的最低分配额不应低于 20 美元，以确保复制头寸与领先交易者的规模相匹配（通常领先交易者的账户余额在 50 万美元到 300 万美元之间）。
   - 代理可以根据领先交易者的账户价值调整初始分配额，以保持比例关系。
   - 如果资金不足，切勿开始交易。只能由用户为主钱包充值，且分配额不可减少。代理可以停止现有订阅以释放资金。
   - 使用 `GET /experimental/:wallet/subscriptions/prepare-wallet` 选择跟随钱包。
   - 将返回的地址与 `coinpilot.json` 中的子钱包地址匹配，以获取其私钥。
   - 绝不允许使用主钱包作为跟随钱包；跟随钱包必须是子钱包。
   - 使用以下参数调用 `POST /experimental/:wallet/subscriptions/start`：
     - `primaryWalletPrivateKey`
     - `followerWalletPrivateKey`
     - `subscription: { leadWallet, followerWallet, config }`
     - `config` 参数（包含以下内容）：
       - `allocation`（必填，最低 5 美元）
       - `stopLossPercent`（0-1 之间的小数，0 表示禁用；例如 50% 为 `0.5`）
       - `takeProfitPercent`（非负数，0 表示禁用；例如 50% 为 `0.5`，150% 为 `1.5`）
       - `inverseCopy`（布尔值）
       - `forceCopyExisting`（布尔值）
       - `positionTPSL`（可选，包含 `stopLossPrice` 和 `takeProfitPrice`，两者均需大于等于 0）
       - `maxLeverage`（可选数值，0 表示禁用）
       - `maxMarginPercentage`（可选数值，0-1 之间，0 表示禁用）

5. **管理正在进行的订阅**
   - 使用 `PATCH /users/:userId/subscriptions/:subscriptionId` 更新配置。
   - 请注意：无法通过 API 交易来修改现有订阅的分配额。
   - 使用 `POST /users/:userId/subscriptions/:subscriptionId/close` 或 `close-all` 关闭交易。
   - 使用 `GET /users/:userId/subscriptions/:subscriptionId/activities` 查看交易活动。
   - 如果订阅的 `apiWalletExpiry` 在 5 天内，请使用 `POST /experimental/:wallet/subscriptions/:subscriptionId/renew-api-wallet` 重新订阅，并提供跟随钱包的私钥。

6. **停止复制交易**
   - 使用 `POST /experimental/:wallet/subscriptions/stop` 停止交易，需要提供 `followerWalletPrivateKey` 和 `subscriptionId`。
   - 请求体中仍然可以使用 `x-wallet-private-key`（来自主钱包的密钥）。
   - 对于旧版本的系统，也可以接受使用 `primaryWalletPrivateKey`。

7. **处理孤立跟随钱包**
   - 如果某个跟随钱包未参与任何活跃的订阅且账户余额非零，请提醒用户手动在 Coinpilot 平台上重置该钱包。

请始终遵守每秒 5 次请求的速率限制，并确保 Coinpilot API 调用是串行执行的（同一时间只能有一个请求）。

## 性能报告

- 提供两种性能视图：
  - **订阅性能**：针对特定订阅或跟随钱包的性能。
  - **整体性能**：所有跟随钱包的性能汇总。
- 主钱包仅作为资金来源，不参与复制交易或性能计算。

## 用户示例请求

- “验证我的 `coinpilot.json` 文件，并确认其中的 `userId` 是否正确。”
- “找到 Sharpe 值高、回撤率低的领先钱包，然后推荐最适合复制的钱包。”
- “使用 200 美元在跟随钱包 1 上开始复制交易，设置止损率为 10%，止盈率为 30%。”
- “显示我的活跃订阅、最近的交易记录和当前性能。”
- “更新订阅 `<id>` 的风险设置和最大杠杆率。”
- “停止订阅 `<id>` 并确认复制交易已关闭。”

## 脚本辅助工具（Node.js）

可以使用 `scripts/coinpilot_cli.mjs` 执行重复性操作：

- 验证凭证信息：`node scripts/coinpilot_cli.mjs validate --online`
- 在开始复制交易前验证领先钱包：`node scripts/coinpilot_cli.mjs lead-metrics --wallet 0xLEAD...`
- 开始复制交易：`node scripts/coinpilot_cli.mjs start --lead-wallet 0xLEAD... --allocation 200 --follower-index 1`
- 更新配置/杠杆率：`node scripts/coinpilot_cli.mjs update-config --subscription-id <id> --payload path/to/payload.json`
- 获取订阅历史记录：`node scripts/coinpilot_cli.mjs history`
- 停止复制交易：`node scripts/coinpilot_cli.mjs stop --subscription-id <id> --follower-index 1`
- 续订即将到期的订阅：`node scripts/coinpilot_cli.mjs renew-api-wallet --subscription-id <id> --follower-index 1`
- 检查 Hyperliquid 的性能：`node scripts/coinpilot_cli.mjs hl-account --wallet 0x...`
- 查看投资组合性能：`node scripts/coinpilot_cli.mjs hl-portfolio --wallet 0x...`

## 参考资料

- Coinpilot 的 API 端点和身份验证方式：`references/coinpilot-api.md`
- Hyperliquid 的相关接口：`references/hyperliquid-api.md`
- 凭证文件格式：`references/coinpilot-json.md`
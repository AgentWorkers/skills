---
name: openburn
description: 该技能可自动化收集 Pump.fun 创建者的费用，使用收集到的 SOL（Solana 的代币）购买相应的代币，并将这些代币进行销毁（即执行回购和销毁操作）。当用户希望为他们的 Pump.fun 代币设置定期回购和销毁计划时，可以使用此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires":
          {
            "modules":
              ["@solana/web3.js", "@solana/spl-token", "tsx", "dotenv"],
            "binaries": ["node", "pnpm"],
            "env":
              [
                "CREATOR_WALLET_PRIVATE_KEY",
                "PUMP_FUN_TOKEN_ADDRESS",
                "JUPITER_API_KEY",
                "BURN_PERCENTAGE",
                "MIN_FEE_TO_BURN",
              ],
          },
        "install":
          [
            {
              "id": "pnpm-solana",
              "kind": "npm",
              "module": "@solana/web3.js",
              "cmd": "pnpm add @solana/web3.js @solana/spl-token @pump-fun/pump-sdk tsx dotenv -w",
              "label": "Install dependencies",
            },
          ],
      },
  }
---
# Openburn

此技能可帮助用户自动化执行 Pump.fun 代币的回购和销毁机制。

## 工作原理

1. **收集创建者费用**：脚本会从绑定曲线（bonding curve）和自动市场机制（AMM）池中收集交易费用（以 SOL 为单位）。
2. **购买代币**：使用收集到的 SOL 从绑定曲线中购买代币。
3. **销毁代币**：将购买的代币发送到 Solana 的销毁地址，从而产生购买压力并推动代币价格上涨。

## 设置说明

1. **请求凭据**：
    请用户提供以下信息：
    - `PUMP_FUN_TOKEN_ADDRESS`（Pump.fun 上的代币地址）
    - `CREATOR_WALLET_PRIVATE_KEY`（用于销毁代币的钱包私钥）
    - `JUPITER_API_KEY`（从 [Jupiter Portal](https://portal.jup.ag/api-keys) 获取）——**仅当代币处于成熟期或脱离绑定曲线时需要**
    - `BURN_PERCENTAGE`（用于购买代币的收集到的 SOL 的百分比，默认值：80%）
    - `MIN_FEE_TO_BURN`（执行销毁操作所需的最低 SOL 费用，默认值：0.1）

    > [!重要提示]
    > 请提醒用户，他们的私钥将被存储在 `.env` 文件中。

2. **存储凭据**：
    检查根目录中是否存在 `.env` 文件。
    - 如果存在，请将凭据添加到文件中。
    - 如果不存在，请创建该文件。

    格式如下：

    ```env
    PUMP_FUN_TOKEN_ADDRESS=...
    CREATOR_WALLET_PRIVATE_KEY=...
    JUPITER_API_KEY=...
    BURN_PERCENTAGE=80
    MIN_FEE_TO_BURN=0.1
    ```

3. **注册代币**：
    在收到并存储了 `PUMP_FUN_TOKEN_ADDRESS` 之后，需要通过 API 注册该代币。

    **端点**：`POST https://api.openburn.fun/api/burn/register`
    **请求体**：

    ```json
    {
      "tokenAddress": "<PUMP_FUN_TOKEN_ADDRESS>"
    }
    ```

    在安排销毁任务之前，必须完成此注册步骤。

4. **安排任务**：
    请用户指定任务调度间隔（默认值：每 2 小时）。
    使用 `cron` 工具来安排新的任务：
    - **名称**：`openburn-job`
    - **调度时间**：`{"kind": "every", "everyMs": 7200000}`（将 7200000 替换为用户的间隔时间，单位为毫秒）
    - **会话目标**：`isolated`
    - **请求体**：
      ```json
      {
        "kind": "agentTurn",
        "message": "Execute the openburn script to burn SOL tokens.",
        "deliver": true
      }
      ```

5. **报告调度信息**：
    向 `https://api.openburn.fun/api/burn/schedule` 发送 POST 请求以报告任务调度情况。

    **端点**：`POST https://api.openburn.fun/api/burn/schedule`
    **请求体**：

    ```json
    {
      "jobId": "openburn-job",
      "intervalMs": 7200000
    }
    ```

## 执行说明

当 cron 任务触发时（收到“执行 openburn 脚本...”的消息），请按照以下步骤操作：

1. **执行脚本**：
    运行位于 `skills/openburn/scripts/burn.ts` 的销毁脚本。

    ```bash
    node --import tsx skills/openburn/scripts/burn.ts
    ```

2. **报告结果**：
    脚本会自动将交易成功/失败的信息报告到 `https://api.openburn.fun/api/burn/transaction`。
    同时，您还需要将交易结果（交易签名）通过聊天界面告知用户。
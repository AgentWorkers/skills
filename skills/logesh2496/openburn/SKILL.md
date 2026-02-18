---
name: openburn
description: 该技能可自动收集 Pump.fun 创建者的费用，并将收集到的 SOL（Solana 币）的一定比例进行销毁。当用户希望为他们的 Pump.fun 代币设置定期费用收取及 SOL 烧毁计划时，可以使用此技能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires":
          {
            "modules": ["@solana/web3.js", "tsx", "dotenv"],
            "binaries": ["node", "pnpm"],
            "env":
              [
                "CREATOR_WALLET_PRIVATE_KEY",
                "PUMP_FUN_TOKEN_ADDRESS",
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
              "cmd": "pnpm add @solana/web3.js @pump-fun/pump-sdk tsx dotenv -w",
              "label": "Install dependencies",
            },
          ],
      },
  }
---
# Openburn

该技能可帮助用户自动化收集创作者费用，并在Pump.fun平台上燃烧SOL（Solana加密货币）。

## 工作原理

1. **收集创作者费用**：脚本会从绑定曲线（bonding curve）和自动市场机制（AMM）池中收集交易费用（以SOL为单位）。
2. **燃烧SOL**：系统会自动将收集到的SOL的指定百分比（可通过配置调整）转移到Solana的销毁地址（`1nc1nerator11111111111111111111111111111111`）进行销毁。

## 设置说明

1. **请求用户提供凭证**：
   - 请用户提供以下信息：
     - `PUMP_FUN_TOKEN_ADDRESS`（在Pump.fun平台上的代币地址）
     - `CREATOR_WALLET_PRIVATE_KEY`（用于燃烧操作的钱包私钥）
     - `BURN_PERCENTAGE`（燃烧费用的百分比，默认值为80%）
     - `MIN_FEE_TO_BURN`（进行燃烧操作所需的最低费用，默认值为0.1 SOL）

   > [!重要提示]
   > 请告知用户，他们的私钥将会被存储在`.env`文件中。

2. **存储凭证**：
   - 检查根目录下是否存在`.env`文件。
     - 如果存在，则将凭证添加到文件中；如果不存在，则创建该文件。
     文件格式如下：

     ```env
    PUMP_FUN_TOKEN_ADDRESS=...
    CREATOR_WALLET_PRIVATE_KEY=...
    BURN_PERCENTAGE=80
    MIN_FEE_TO_BURN=0.1
    ```

3. **注册代币**：
     在获取并存储`PUMP_FUN_TOKEN_ADDRESS`后，需要通过API注册该代币。
     **API端点**：`POST https://api.openburn.fun/api/burn/register`
     **请求体**：

     ```json
    {
      "tokenAddress": "<PUMP_FUN_TOKEN_ADDRESS>"
    }
    ```

   这一步骤是在安排燃烧任务之前必须完成的。

4. **安排任务**：
   - 请用户设置任务执行间隔（默认为每2小时）。
   - 使用`cron`工具来安排任务：
     - **任务名称**：`openburn-job`
     - **执行间隔**：`{"kind": "every", "everyMs": 7200000}`（将7200000替换为用户指定的时间间隔，单位为毫秒）
     - **会话模式**：`isolated`
     - **任务数据**：
       ```json
      {
        "kind": "agentTurn",
        "message": "Execute the openburn script to burn SOL tokens.",
        "deliver": true
      }
      ```

5. **报告任务安排情况**：
     发送POST请求以报告任务安排情况。
     **API端点**：`POST https://api.openburn.fun/api/burn/schedule`
     **请求体**：

     ```json
    {
      "jobId": "openburn-job",
      "intervalMs": 7200000
    }
    ```

## 执行说明

当`cron`任务被触发时（系统会发送“Execute the openburn script...”的消息），请执行以下操作：

1. **运行脚本**：
    调用位于`skills/openburn/scripts/burn.ts`中的燃烧脚本。
    ```bash
    node --import tsx skills/openburn/scripts/burn.ts
    ```

2. **报告结果**：
    脚本会自动将执行结果（包括交易是否成功）报告到`https://api.openburn.fun/api/burn/transaction`。
   同时，也应在聊天中向用户反馈交易的具体信息（如交易签名等）。
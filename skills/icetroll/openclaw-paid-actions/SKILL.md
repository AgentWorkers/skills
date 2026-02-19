---
name: openclaw-paid-actions
description: 使用 `openclaw_paid_action` 工具来列出可执行的操作、生成 USDC 发票，并且只有在 Solana 上收到手动付款确认后才会执行这些操作。
metadata: {"openclaw":{"emoji":"💸","skillKey":"openclaw-paid-actions","requires":{"bins":["node"],"env":["OPENCLAW_USDC_PAY_TO","OPENCLAW_PAID_ACTIONS_INVOICE_SECRET","OPENCLAW_PAID_ACTIONS_INVOICE_STORE_PATH"],"config":["plugins.entries.openclaw-paid-actions.enabled","plugins.entries.openclaw-paid-actions.config.payTo","plugins.entries.openclaw-paid-actions.config.invoiceSecret","plugins.entries.openclaw-paid-actions.config.invoiceStorePath","plugins.entries.openclaw-paid-actions.config.actions"]}},"moltbot":{"emoji":"💸","skillKey":"openclaw-paid-actions","requires":{"bins":["node"],"env":["OPENCLAW_USDC_PAY_TO","OPENCLAW_PAID_ACTIONS_INVOICE_SECRET","OPENCLAW_PAID_ACTIONS_INVOICE_STORE_PATH"],"config":["plugins.entries.openclaw-paid-actions.enabled","plugins.entries.openclaw-paid-actions.config.payTo","plugins.entries.openclaw-paid-actions.config.invoiceSecret","plugins.entries.openclaw-paid-actions.config.invoiceStorePath","plugins.entries.openclaw-paid-actions.config.actions"]}}}
---
# OpenClaw 支付型操作

当某个操作需要在执行前完成支付时，请使用此技能。

工具：`openclaw_paid_action`

此技能仅用于提供指令。它依赖于已正确安装的 `openclaw-paid-actions` 插件，该插件提供了 `openclaw_paid_action` 功能。

**可执行的操作：**
- `list`：列出所有已配置的支付型操作。
- `quote`：为某个操作生成 USDC 支付指令。
- `invoice`：为某个操作或输入创建一个已签名的发票令牌。
- `status`：检查发票的当前支付状态。
- `wait`：等待发票支付完成（或超时）。
- `confirm`（或别名 `pay`）：在链上验证支付交易，然后标记发票为已支付。
- `execute`：在发票支付确认后执行该操作。

## 典型流程：
1. 调用 `openclaw_paid_action` 并传入 `action: "list"` 以获取操作 ID。
2. 调用 `openclaw_paid_action` 并传入 `action: "invoice"` 以及操作 ID（可选参数包括 `input`、`recipient`、`memo`）。
3. 将返回的 `invoiceMessage` 或 `paymentInstructions` 发送给付款方。
4. 收到付款后，调用 `openclaw_paid_action` 并传入 `action: "confirm"` 以及发票信息（或发票 ID）和交易详情，以在链上验证支付并标记发票为已支付。您也可以传递 `paymentProofText`（用户的原始回复内容）；该工具会自动提取 Solana 交易的签名。
5. 调用 `openclaw_paid_action` 并传入 `action: "wait"` 以获取支付完成的时间。
6. 调用 `openclaw_paid_action` 并传入 `action: "execute"` 以及在支付完成后的操作信息，以执行该操作。

## 插件配置：

配置信息请保存在 `plugins.entries.openclaw-paid-actions.config` 文件中：

```json
{
  "network": "solana:mainnet",
  "payTo": "${OPENCLAW_USDC_PAY_TO}",
  "invoiceSecret": "${OPENCLAW_PAID_ACTIONS_INVOICE_SECRET}",
  "invoiceStorePath": "${OPENCLAW_PAID_ACTIONS_INVOICE_STORE_PATH}",
  "allowRunAsRoot": false,
  "requirePersistentInvoiceSecret": true,
  "requireInvoiceStorePath": true,
  "enforceReviewedScripts": true,
  "reviewedScriptsRoot": "scripts/paid-actions",
  "requiredNodeMajor": 20,
  "defaultInvoiceWaitSeconds": 900,
  "invoicePollIntervalMs": 3000,
  "maxTimeoutSeconds": 120,
  "defaultTaskTimeoutMs": 30000,
  "maxOutputBytes": 32768,
  "actions": {
    "x-shoutout": {
      "description": "Post a paid shoutout on X",
      "command": ["node", "scripts/paid-actions/x-shoutout.mjs"],
      "cwd": ".",
      "price": "0.03",
      "timeoutMs": 45000
    }
  }
}
```

**注意事项：**
- 每个操作都会严格按照配置的命令数组来执行。
- 发票的执行会使用发票令牌中包含的输入数据。
- 操作的输入数据以 `OPENCLAW_PAID_ACTION_INPUT_JSON` 的格式提供。
- 命令的输出会被截断，长度不超过 `maxOutputBytes`。
- 如果在创建发票时设置了 `notifySessionKey`，支付完成时网关会触发系统事件。
- 在 OpenClaw 中，此工具是可选的；请确保在代理的 `tools.allow` 配置中添加了 `openclaw_paid_action`。
- 在生产环境中，如果缺少 `invoiceSecret` 或 `invoiceStorePath`，系统会默认阻止该模块的启动。
- 在生产环境中，未审核的命令将不会被执行；请将相关操作放在 `scripts/paid-actions` 目录下。
- 在启用自动执行功能之前，请务必审核所有配置的操作命令。

## 示例输入数据：
- 对于 `x-shoutout` 操作：
  ```json
{
  "handle": "openclaw",
  "message": "Huge shoutout to @openclaw for supporting this build!",
  "link": "https://x.com/openclaw"
}
```

- 对于 `discord-shoutout` 操作：
  ```json
{
  "name": "Daniel",
  "note": "Thanks for supporting the build."
}
```
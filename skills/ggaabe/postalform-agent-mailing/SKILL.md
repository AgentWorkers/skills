---
name: postalform-machine-order
description: "**使用 PostalForm 通过机器支付发送实体邮政邮件：**  
1. 准备并验证用于打印和邮寄的数据；  
2. 向 `/api/machine/orders` 发送 `POST` 请求；  
3. 使用任何兼容的钱包客户端（如 Purl 或自定义钱包）完成 x402 支付；  
4. 在邮件投递完成后进行状态检查（polling）。  
**适用场景：**  
当需要代理自动发送实体信件或文件时，该流程能够确保首次尝试的准确性，并支持幂等重试机制（即多次尝试不会产生重复结果）。"
---
# PostalForm 机器订单处理流程

当代理需要首次尝试就可靠地发送实体邮件（即需要打印并邮寄的订单）时，请使用此工作流程。

## 工作流程

### 1. 收集输入信息并选择地址策略

需要以下输入信息：
- `buyer_name`（买家姓名）
- `buyer_email`（买家邮箱）
- `sender_name`（寄件人姓名）
- `recipient_name`（收件人姓名）
- PDF文件来源（`upload_token`、`{download_url, file_id}`、数据URL或允许的`https` URL）
- 邮寄选项（`double_sided`、`color`、`mail_class`、`certified`）

对于每个参与者（寄件人/收件人），请选择以下地址策略中的一种：
- 手动输入地址：`*_address_type: "Manual"` + `*_address_manual`
- Loqate地址：`*_address_type: "Address"` + `*_address_id` + `*_address_text`

同一参与者的地址信息不能同时使用手动输入和Loqate地址。

### 2. 构建具有严格幂等性的数据包

生成一个唯一的UUID `request_id`，并在重试过程中保持数据包内容的稳定性。

每次请求时都需要设置 `buyer_email`（这是Stripe接收订单所需的）。

对于手动输入的地址信息：
- 必须包含 `line1`、`city`（城市）、`state`（州）、`zip`（邮政编码）字段。
- 仅当 `line2` 有非空字符串值时才包含该字段；如果为空，则省略该字段。

请使用 `references/payload_templates.md` 中提供的模板来构建数据包。

### 3. 使用验证端点进行预处理（推荐）

调用以下API：
- `POST https://postalform.com/api/machine/orders/validate`

如果响应状态码为 `200`，则确认以下内容：
- `quote.page_count` 与预期页面数量一致
- `quote.price_usd` 及其他选项均符合要求

如果响应状态码为 `422`，则在支付前修复数据包内容。

### 4. 创建订单并完成x402支付

调用以下API：
- `POST https://postalform.com/api/machine/orders`

流程如下：
1. 发送订单数据包，但不包含支付相关头部信息。
2. 如果收到 `402` 状态码且提示“需要支付（PAYMENT-REQUIRED）”，则继续下一步。
3. 使用您的钱包系统在指定的网络上完成支付。
4. 重新发送相同的请求数据包，并添加 `PAYMENT-SIGNATURE` 标识。
5. 预期收到 `202` 状态码以及支付结算的相关元数据。

支付客户端选项：
- `purl` CLI（如果可用，这是最快的支付方式）
- 任何符合x402标准的支付客户端（如 `@x402/core`、`@x402/evm` 或类似的自定义支付工具）

如果使用 `purl`：
- 建议使用钱包别名或密钥库而非原始私钥进行支付。
- 从安全的运行时环境中获取 `--password` 参数。
- 设置 `--max-amount` 以限制支付金额。
- 确保指定的网络与 `PAYMENT-REQUIRED` 中指定的网络一致。

### 5. 监控订单状态直至支付完成

调用以下API：
- `GET https://postalform.com/api/machine/orders/:request_id`

当以下条件满足时，可视为订单处理完成：
- `is_paid` 为 `true`
- `current_step` 进展到“email_sent”阶段
- `order_complete_url` 是一个有效的URL

处理过渡状态：
- 在链上支付完成后，`status` 可能暂时显示为 `settled_pending_webhook`；此时应继续进行轮询。
- 不要使用相同的 `request_id` 重新发送已更改的数据包。

## 首次尝试的可靠性规则

### 必须遵守的规则：
- 对于同一逻辑订单的多次重试，`request_id` 必须保持不变。
- 在收到 `402` 错误后重试时，数据包内容不得更改。
- 每次请求都必须包含 `buyer_email`。
- 确保支付网络与 `PAYMENT-REQUIRED` 中指定的网络一致；不要硬编码网络地址。
- 仅使用有效的美国地址，并且每个参与者只能使用一种地址策略。
- 在支付前验证页面数量和报价价格。

### 常见故障及其解决方法：
- 当手动输入的 `line2` 为空时，可能会收到 `422 invalid_type` 错误：
  - 原因：空字段被自动处理为 `null`。
  - 预防措施：仅当 `line2` 有非空值时才包含该字段。

- 支付完成后可能会出现延迟（状态显示为 `settled_pending_webhook`）：
  - 原因：支付确认发生在Webhook回调完成之前。
  - 预防措施：等待几分钟后再进行轮询；如果需要，可以设置重试间隔。

- 在轮询过程中偶尔会出现非JSON格式的响应或服务器响应异常：
  - 原因：可能是上游系统或渲染过程中的临时错误。
  - 预防措施：采用防御性处理方式；如果响应不是JSON格式或返回 `5xx` 状态码，直接重试，无需更改 `request_id` 或数据包内容。

- 如果收到 `409 request_id_mismatch` 错误：
  - 原因：使用相同的 `request_id` 发送了修改后的数据包。
  - 预防措施：对于已更改的订单，生成新的UUID；仅在需要重试时使用新的ID。

## 安全规则：
- 避免在日志中打印钱包密码、私钥或敏感的环境变量。
- 如果工具支持加密密钥库，建议使用加密后的密钥库而非原始私钥。
- 设置支付限额（`max amount`）以防止意外超支。

## 操作员需要返回的信息：

执行完成后，需要返回以下信息：
- `request_id` / `order_id`
- 价格/报价摘要（包括 `page_count`）
- 支付结算详情（`network`、`pay_to`、`settlement_tx`、`settled_at`）
- 最新状态（`is_paid`、`current_step`）
- 如果订单已支付完成，还需提供 `order_complete_url`

参考示例和命令片段：
- `references/payload_templates.md`
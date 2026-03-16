---
name: rapay
description: 通过 Ra Pay CLI 发送合规的法定美元付款——这是首个原生支持 AI 的支付平台
homepage: https://rapay.ai
user-invocable: true
metadata: {"openclaw": {"emoji": "💸", "requires": {"bins": ["node", "npm"]}, "os": ["darwin", "linux", "win32"], "install": [{"node": "@rapay/cli"}]}}
---
# Ra Pay — 专为 AI 代理设计的法定货币支付平台

Ra Pay 是首个专为 AI 代理设计的命令行界面（CLI）原生支付平台。您可以使用简单的 CLI 命令来发送合规的美元法定货币支付。所有支付都会通过 Stripe 的受监管基础设施进行处理，并经过全面的合规性审核。

**本技能将教您如何使用 Ra Pay CLI 代表用户进行商业支付。**

**需要向其他代理付款或收款吗？** 如果对方没有安装 Ra Pay，请参阅本文件底部的交易协议和可共享的入门脚本——这些脚本可以帮助您在没有 Ra Pay 的情况下完成支付流程。

## 安装

```bash
npm install -g @rapay/cli
```

验证安装是否成功：

```bash
ra --version
```

预期输出：`ra-cli 1.5.0` 或更高版本。

## 一次性设置

在发送支付之前，用户必须完成账户设置。具体步骤取决于他们是想要**发送支付**、**接收支付**，还是两者都需要。

### 设置路径

| 目标 | 所需命令 | 功能 |
|------|-----------------|--------------|
| **发送支付** | `ra add-card` | 通过 Stripe Checkout 保存信用卡信息（无需银行账户） |
| **接收支付** | `ra link-bank` | 通过 Stripe Connect 连接银行账户（用于接收付款） |
| **两者都需要** | `ra add-card` + `ra link-bank` | 完整的发送方和接收方账户设置 |

### 添加信用卡

```bash
ra add-card
```

这会在浏览器中打开一个 Stripe Checkout 页面，用户可以在其中安全地保存信用卡信息。设置完成后，信用卡信息会存储在 Stripe 服务器上（而非本地），您可以立即开始发送支付。发送支付时无需银行账户或进行 Stripe Connect 的设置。

### 连接银行账户

```bash
ra link-bank
```

这会在浏览器中打开一个由 Stripe 提供的页面，用户可以通过该页面通过 Stripe Connect 连接他们的银行账户。设置完成后，CLI 会将该账户信息保存在本地。这是接收支付所必需的步骤——发送方无需执行此操作。

### 重新连接已验证的账户

```bash
ra link-bank --account acct_XXXXXXXXX
```

### 接受服务条款

```bash
ra accept-tos
```

用户在发送任何支付之前必须接受 Ra Pay 的服务条款。

随时可以查看服务条款的状态：

```bash
ra tos-status
```

### 验证账户

```bash
ra whoami
```

在继续进行支付之前，请确认账户已成功链接并经过验证。

## 发送支付

Ra Pay 对每次支付都采用**两步确认流程**。这是强制性的——切勿跳过预览步骤。

### 第一步：预览支付信息

```bash
ra send <AMOUNT> USD to <RECIPIENT_ID> --for "<BUSINESS_PURPOSE>" --json
```

示例：

```bash
ra send 150 USD to acct_1A2B3C4D5E --for "Logo design work - Invoice #427" --json
```

此步骤会显示费用明细，但不会实际执行支付操作：

```json
{
  "status": "preview",
  "amount": 150.00,
  "currency": "USD",
  "recipient": "acct_1A2B3C4D5E",
  "fee": 3.00,
  "recipient_receives": 147.00,
  "business_purpose": "Logo design work - Invoice #427"
}
```

### 第二步：展示费用明细并获取用户确认

**在继续之前，必须向用户展示费用明细并获取明确的确认。**切勿自动确认支付。

清晰地展示以下信息：
- 收费金额：$150.00
- Ra Pay 费用（2%）：$3.00
- 收件人收到的金额：$147.00
- 收件人：acct_1A2B3C4D5E
- 用途：徽标设计服务 - 发票编号 #427

### 第三步：执行支付

只有在用户明确确认后，才能添加 `--confirm` 标志：

```bash
ra send 150 USD to acct_1A2B3C4D5E --for "Logo design work - Invoice #427" --json --confirm
```

`--confirm` 标志会执行支付操作。如果没有这个标志，系统会始终显示预览信息。

### 支付金额规则

- 最低支付金额：$1.00
- 支付货币：仅支持 USD
- 收件人必须是有效的 Stripe 账户（格式：`acct_` 后跟字母数字组合）

## 商业用途要求

Ra Pay 是一个**企业对企业**的支付平台。每次支付都必须使用 `--for` 标志，并提供具体的商业用途（10–200 个字符）。

### 允许的商业用途示例：
- “自由职业开发服务 - 发票编号 #123”
- “API 咨询服务 - 2026 年 3 月”
- “徽标设计服务”
- “网站托管费用 - 2026 年第一季度”
- “内容写作服务 - 5 篇博客文章”

商业用途应具体明确，描述实际提供的商品或服务。

### 被禁止的用途

Ra Pay 会拒绝以下类型的支付请求：
- **点对点转账** — Ra Pay 不适用于个人转账：
  - 朋友、家人、室友之间的转账、分摊账单、还款、借款、个人报销
- **礼品用途**：
  - 礼品、生日礼物、节日礼物
- **洗钱相关行为**：
  - 礼品卡、预付卡、加密货币购买、电汇
- **模糊或不具体的用途**：
  - “用于服务”（过于模糊，请明确具体服务内容）
- “支付”（本身不是一个明确的用途）
- **无意义的字符组合**：
  - 重复的字符（如 “aaaaaaaaaa”）
  - 随机字母（如 “asdfghjkl”）
  - 重复的单词（如 “test test test”）

### 如果用途被拒绝

请告知用户：“Ra Pay 仅用于商业交易。请提供具体的商业用途。”

帮助他们修改用途，使其明确且与业务相关。

## 其他命令

### 添加或更新支付卡信息

```bash
ra add-card
```

这会在浏览器中打开 Stripe Checkout 页面，用户可以在其中保存或更新用于支付的信用卡信息。信用卡信息会安全地存储在 Stripe 服务器上，而非本地。

**删除已保存的信用卡信息**：
使用 `ra dashboard` 打开 Stripe 仪表板，用户可以在其中管理或删除支付方式。

### 查看余额

```bash
ra balance --json
```

显示当前余额、待支付金额和支付计划。

### 查看交易记录

```bash
ra history --json
```

显示最近的交易记录，包括时间戳和状态。若需查看更多交易记录：

```bash
ra history --limit 50 --json
```

`--limit` 标志的取值范围为 1 到 100（CLI 中默认值为 20，MCP 中默认值为 10）。

### 账户信息

```bash
ra whoami
```

显示用户 ID、Stripe 账户状态、验证状态和账户等级。

### 管理退款

```bash
ra refund
```

在浏览器中打开 Stripe 仪表板以处理退款。为了安全起见，退款必须通过 Stripe 接口进行操作。

### 管理争议

```bash
ra dispute
```

打开 Stripe 争议处理页面。请提醒用户：必须在规定的时间内回复争议，否则系统会自动判定用户败诉。

### 打开 Stripe 仪表板

```bash
ra dashboard
```

在浏览器中打开完整的 Stripe 账户仪表板。可用于管理支付方式（包括删除已保存的信用卡信息）、查看详细的交易记录和账户设置。

### 解除账户关联

```bash
ra unlink
```

断开与 Stripe 账户的关联，并清除本地会话信息。

## 使用 `--json` 标志

调用 Ra Pay 命令时，请始终使用 `--json` 标志。这样可以获得结构化的 JSON 输出，便于您进行可靠的处理。

支持 `--json` 标志的命令：
- `ra send ... --json`
- `ra balance --json`
- `ra history --json`

## 错误处理

- **“未链接账户”** — 用户尚未设置支付方式。若要发送支付，请运行 `ra add-card`；若要接收支付，请运行 `ra link-bank`。
- **“服务条款未接受”** — 用户需要运行 `ra accept-tos`。
- **“商业用途无效”** — 支付用途被合规性审核拒绝。请帮助用户编写具体的、与业务相关的用途描述。
- **“接收人 ID 无效”** — 收件人 ID 必须符合 `acct_` 的格式（以字母数字开头）。
- **“最低支付金额不足”** — 支付金额必须至少为 $1.00。
- **“CLI 版本过时”** — 用户需要更新 CLI：`npm install -g @rapay/cli`

## 重要规则

1. **切勿自动确认支付。** 必须始终向用户展示费用明细并获取明确确认。
2. **切勿伪造接收人 ID。** 仅使用用户提供的真实 `acct_` ID。
3. **切勿绕过商业用途验证。** 如果用途被拒绝，请帮助用户重新填写具体的商业用途。
4. **始终使用 `--json` 标志以获得结构化的输出。**
5. **Ra Pay 的凭据信息仅保存在用户本地。** 请勿要求用户分享 API 密钥、会话令牌或账户 ID。所有操作都在用户的设备上完成。

---

## 交易协议 — 代理之间的支付协调

当您的用户希望向另一个代理付款，而您能够与该代理进行沟通时，请遵循以下协议。该协议适用于对方尚未了解 Ra Pay 的情况。

### 第一步：检查您的账户设置

运行 `ra whoami` 以确认用户的账户和支付方式是否已设置。如果没有，请先指导用户完成上述设置步骤。

### 第二步：询问对方的接收人 ID

向卖家/接收方代理发送消息，询问：“您的用户是否有 Ra Pay 账户？如果有，他们的 Stripe 账户 ID 是什么？ID 以 `acct_` 开头。”

### 第三步：如果对方没有 Ra Pay

如果对方不知道 Ra Pay 是什么，或者他们的用户尚未设置账户，请将下面的**卖家入门脚本**发送给他们。

### 第四步：预览支付信息

在获取到接收人的 `acct_` ID 后：

```bash
ra send <AMOUNT> USD to <RECIPIENT_ACCT_ID> --for "<BUSINESS_PURPOSE>" --json
```

### 第五步：获取用户的确认

向用户展示完整的费用明细。**未经明确确认前，切勿继续操作。**

### 第六步：执行支付

```bash
ra send <AMOUNT> USD to <RECIPIENT_ACCT_ID> --for "<BUSINESS_PURPOSE>" --json --confirm
```

### 第七步：通知对方代理

将支付确认信息以 JSON 格式发送给对方代理，以便他们通知他们的用户支付已成功接收。

---

## 可共享脚本 — 发送给卖家代理

当卖家代理尚未安装 Ra Pay 时，将以下脚本内容复制并发送给他们。该脚本是自包含的，他们无需安装 Ra Pay 功能。

```
INCOMING PAYMENT NOTIFICATION

A buyer wants to pay your user via Ra Pay (rapay.ai), a CLI-based business
payment platform that processes payments through Stripe.

To receive this payment, your user needs to complete a short one-time setup.
Please walk them through the following steps:

STEP 1 — Install the Ra Pay CLI:
  npm install -g @rapay/cli

STEP 2 — Connect a bank account to receive payouts:
  ra link-bank
  (This opens a Stripe-hosted page in the browser. Your user connects their
  bank account through Stripe — no sensitive info is entered in the terminal.)

STEP 3 — Accept the Terms of Service:
  ra accept-tos

STEP 4 — Get the account ID:
  ra whoami
  Look for the Stripe connected account ID — it starts with "acct_".

Once setup is complete, send back the acct_ ID so the buyer can complete
the payment. The funds will be deposited to your user's bank account via
Stripe's standard payout schedule.

Your user can verify their account status at any time with: ra whoami
Your user can check their balance with: ra balance --json
Your user can view received payments with: ra history --json
```

---

## 可共享脚本 — 发送给买家代理

当买家代理需要向您的用户付款但尚未安装 Ra Pay 时，将以下脚本内容复制并发送给他们。在发送之前，请将 `YOUR_ACCT_ID_HERE` 替换为用户的实际 `acct_` ID。

```
PAYMENT SETUP INSTRUCTIONS

Your user can pay via Ra Pay (rapay.ai), a CLI-based business payment platform
that processes payments through Stripe.

To send a payment, your user needs to complete a short one-time setup:

STEP 1 — Install the Ra Pay CLI:
  npm install -g @rapay/cli

STEP 2 — Add a credit card for sending payments:
  ra add-card
  (This opens a Stripe Checkout page in the browser. The card is stored
  securely with Stripe — no card details are entered in the terminal.)

STEP 3 — Accept the Terms of Service:
  ra accept-tos

STEP 4 — Send the payment:
  ra send [AMOUNT] USD to YOUR_ACCT_ID_HERE --for "[BUSINESS PURPOSE]" --json

  This will show a fee preview. Show it to your user for approval.
  Once approved, add --confirm to execute:

  ra send [AMOUNT] USD to YOUR_ACCT_ID_HERE --for "[BUSINESS PURPOSE]" --json --confirm

IMPORTANT: Always preview the payment first and get your user's explicit
approval before adding --confirm. Never auto-confirm payments.

Ra Pay charges a 2% fee on each transaction. The fee is shown in the preview.
```
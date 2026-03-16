---
name: rapay
description: 通过 Ra Pay CLI 发送合规的法定美元（USD）支付——这是首个原生支持 AI 的支付平台（即该平台完全通过命令行界面（CLI）进行操作）。
homepage: https://rapay.ai
user-invocable: true
metadata: {"openclaw": {"emoji": "💸", "requires": {"bins": ["node", "npm"]}, "os": ["darwin", "linux", "win32"], "install": [{"node": "@rapay/cli"}]}}
---
# Ra Pay — 专为AI代理设计的法定货币支付平台

Ra Pay是首个专为AI代理设计的命令行界面（CLI）原生支付平台。您可以使用简单的CLI命令发送合规的美元法定货币支付。每笔支付都会通过Stripe的受监管基础设施进行处理，并经过全面的合规性审核。

**本技能将教会您如何使用Ra Pay CLI代表用户发送商业支付。**

**需要向其他代理付款或收款吗？** 如果对方没有安装Ra Pay，请参阅文件底部的交易协议和可共享的入门脚本——这些脚本可以帮助您在没有该技能的情况下完成对方的设置。

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

在发送支付之前，用户必须完成账户设置。具体步骤取决于他们是想要**发送**、**接收**还是**同时进行**支付。

### 设置路径

| 目标 | 所需命令 | 功能 |
|------|-----------------|--------------|
| **发送支付** | `ra add-card` | 通过Stripe Checkout保存信用卡信息（无需银行账户） |
| **接收支付** | `ra link-bank` | 通过Stripe Connect连接银行账户（用于接收付款） |
| **同时进行** | `ra add-card` + `ra link-bank` | 完整的发送方和接收方设置 |

### 添加信用卡

```bash
ra add-card
```

这将在浏览器中打开Stripe Checkout页面，用户可以在其中安全地保存信用卡信息。设置完成后，信用卡信息会存储在Stripe服务器上（而非本地），从而可以立即发送支付。发送支付时无需银行账户或Stripe Connect的额外设置。

### 连接银行账户

```bash
ra link-bank
```

这将在浏览器中打开由Stripe提供的连接页面，用户可以通过该页面连接他们的银行账户。设置完成后，CLI会将该会话信息存储在本地。这是接收支付所必需的——发送方无需执行此步骤。

### 重新连接已验证的账户

```bash
ra link-bank --account acct_XXXXXXXXX
```

### 接受服务条款

```bash
ra accept-tos
```

用户在发送任何支付之前必须接受Ra Pay的服务条款。

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

Ra Pay对每笔支付都采用**两步确认流程**。这是强制性的——切勿跳过预览步骤。

### 第一步：预览支付信息

```bash
ra send <AMOUNT> USD to <RECIPIENT_ID> --for "<BUSINESS_PURPOSE>" --json
```

示例：

```bash
ra send 150 USD to acct_1A2B3C4D5E --for "Logo design work - Invoice #427" --json
```

此步骤会返回费用明细，但不会实际执行支付：

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

### 第二步：展示费用明细并获得用户确认

**在继续之前，必须向用户展示费用明细并获得明确的确认。**切勿自动确认支付。

清晰地展示以下信息：
- 收费金额：150.00美元
- Ra Pay费用（2%）：3.00美元
- 收款人收到的金额：147.00美元
- 收款人：acct_1A2B3C4D5E
- 用途：标志设计服务 - 发票编号#427

### 第三步：执行支付

只有在用户明确确认后，才能添加`--confirm`标志：

```bash
ra send 150 USD to acct_1A2B3C4D5E --for "Logo design work - Invoice #427" --json --confirm
```

`--confirm`标志用于执行支付。如果没有这个标志，系统会始终显示预览信息。

### 支付金额规则

- 最低支付金额：1.00美元
- 仅支持美元货币
- 收款人必须是有效的Stripe连接账户（格式：`acct_`后跟字母数字字符）

## 商业用途要求

Ra Pay是一个**企业对企业**的支付平台。每笔支付都必须包含`--for`标志，并注明具体的商业用途（10到200个字符）。

### 合法的商业用途示例：
- “自由职业开发服务 - 发票编号#123”
- “API咨询服务 - 2026年3月”
- “标志设计服务”
- “网站托管费用 - 2026年第一季度”
- “内容写作服务 - 5篇博客文章”

商业用途应具体明确，描述实际提供的商品或服务。

### 被禁止的用途

Ra Pay会拒绝以下用途的支付请求：
- **点对点转账** — Ra Pay不支持个人转账：
  - 朋友、家人、室友之间的转账、分摊账单、还款、借款、个人报销
- **礼品用途**：
  - 礼品、生日礼物、节日礼物
- **洗钱相关行为**：
  - 礼品卡、预付卡、加密货币购买、电汇
- **模糊或不具体的用途**：
  - “用于服务”（太模糊，请明确具体服务内容）
  - “支付”（本身不是一个具体的用途）
- **无意义的字符或测试字符串**：
  - 重复的字符（例如“aaaaaaaaaa”）
  - 随机字母（例如“asdfghjkl”）
  - 重复的单词（例如“test test test”）

### 如果用途被拒绝

请告知用户：“Ra Pay仅用于商业交易。请提供具体的商业用途。”

帮助他们修改用途，使其明确且与业务相关。

## 其他命令

### 添加或更新支付卡

```bash
ra add-card
```

这将在浏览器中打开Stripe Checkout页面，用户可以在此保存或更新用于支付的信用卡信息。信用卡信息会安全地存储在Stripe服务器上，而非本地。

要**删除**已保存的信用卡，请使用`ra dashboard`打开Stripe控制面板，用户可以在其中管理或删除支付方式。

### 查看余额

```bash
ra balance --json
```

返回当前余额、待支付金额和支付计划。

### 查看交易历史

```bash
ra history --json
```

显示带有时间戳和状态的最近交易记录。要查看更多交易记录：

```bash
ra history --limit 50 --json
```

`--limit`标志的取值范围为1到100（CLI默认值为20，MCP默认值为10）。

### 账户信息

```bash
ra whoami
```

显示用户ID、Stripe账户状态、验证状态和账户等级。

### 管理退款

```bash
ra refund
```

在浏览器中打开Stripe控制面板以处理退款。为确保安全，退款必须通过Stripe接口进行操作。

### 管理争议

```bash
ra dispute
```

打开Stripe争议处理页面。请提醒用户：必须在规定时间内回复争议，否则系统将自动作出不利于用户的处理。

### 打开Stripe控制面板

```bash
ra dashboard
```

在浏览器中打开完整的Stripe账户控制面板。可用于管理支付方式（包括删除保存的信用卡信息）、查看详细的交易记录和账户设置。

### 解除账户关联

```bash
ra unlink
```

断开与Stripe账户的关联，并清除本地会话信息。

## 使用`--json`标志

调用Ra Pay命令时，请始终使用`--json`标志。这样可以获得结构化的JSON输出，便于您进行可靠的处理。

支持`--json`标志的命令：
- `ra send ... --json`
- `ra balance --json`
- `ra history --json`

## 错误处理

- **“未链接账户”** — 用户尚未设置支付方式。如需发送支付，请运行`ra add-card`；如需接收支付，请运行`ra link-bank`。
- **“服务条款未接受”** — 用户需要运行`ra accept-tos`。
- **“商业用途无效”** — 用途不符合合规性要求。请帮助用户填写具体的商业用途。
- **“收款人ID无效”** — 收款人ID必须符合`acct_`后跟字母数字字符的格式。
- **“最低支付金额”** — 支付金额必须至少为1.00美元。
- **“CLI版本过时”** — 用户需要更新：`npm install -g @rapay/cli`

## 重要规则

1. **切勿自动确认支付。**始终向用户展示费用明细并获得明确确认。
2. **切勿伪造收款人ID。**仅使用用户提供的真实`acct_` ID。
3. **切勿绕过商业用途验证。**如果用途被拒绝，请帮助用户填写具体的商业用途。
4. **始终使用`--json`以获得结构化输出。**
5. **Ra Pay的凭证信息仅保存在用户本地。**切勿要求用户分享API密钥、会话令牌或账户ID。所有操作都在用户的设备上完成。

---

## 交易协议 — 代理之间的支付协调

当您的用户想要向另一个代理付款，而您能够与该代理沟通时，请遵循以下协议。该协议适用于对方尚未听说过Ra Pay的情况。

### 第一步：检查您的账户设置

运行`ra whoami`以确认您的用户是否已设置账户和支付方式。如果没有，请先指导他们完成上述设置步骤。

### 第二步：询问对方的收款人ID

向卖家/收款人代理发送消息，询问：“您的用户是否有Ra Pay账户？如果有，他们的Stripe账户ID是什么？ID以`acct_`开头。”

### 第三步：如果对方没有Ra Pay

如果对方不知道Ra Pay是什么，或者他们的用户尚未完成设置，请将下面的**卖家入门脚本**发送给他们。

### 第四步：预览支付信息

在获取到收款人的`acct_` ID后：

```bash
ra send <AMOUNT> USD to <RECIPIENT_ACCT_ID> --for "<BUSINESS_PURPOSE>" --json
```

### 第五步：获得用户的确认

向用户展示完整的费用明细。**未经明确确认前，请勿继续进行支付。**

### 第六步：执行支付

```bash
ra send <AMOUNT> USD to <RECIPIENT_ACCT_ID> --for "<BUSINESS_PURPOSE>" --json --confirm
```

### 第七步：通知对方代理

将支付确认的JSON信息发送给对方代理，以便他们通知他们的用户支付已成功接收。

---

## 可共享脚本 — 发送给卖家代理

当卖家代理尚未安装Ra Pay时，请将以下脚本内容发送给他们。该脚本是自包含的——他们无需安装Ra Pay技能。

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

当买家代理需要向您的用户付款但尚未安装Ra Pay时，请将以下脚本内容发送给他们。在发送之前，请将`YOUR_ACCT_ID_HERE`替换为用户的实际`acct_` ID。

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
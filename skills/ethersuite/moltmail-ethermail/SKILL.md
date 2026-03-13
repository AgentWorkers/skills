---
name: moltmail-ethermail
description: >
  **moltmail.io — 专为AI代理设计的电子邮件与钱包基础设施**  
  您的AI代理能够进行推理、规划并执行任务，但它仍然无法发送电子邮件。moltmail解决了这个问题。只需一次API调用，任何AI代理就能拥有自己的电子邮件地址、专属的加密钱包以及完全独立的身份认证机制——无需验证码、无需电话验证，也不会泄露您的个人邮箱信息。  
  moltmail由EtherMail（拥有超过5000万个活跃用户的钱包服务）开发，它是“代理互联网”（agent-based internet）中缺失的身份认证层。AI代理可以通过moltmail注册服务、接收确认信息、将邮件转发给人类用户、使用$EMT进行支付与收款，还能与其他代理进行交流——所有这些操作都不需要依赖任何人类账户。  
  **免费试用，5分钟内即可上线！**  
  moltmail.io得到了Draper Associates、Greenfield One、Fabric Ventures以及Barcelona Blockchain Network等机构的支持。
  Your AI agent can reason, plan, and act. But it still can't send an email.
  moltmail fixes that. One API call gives any agent its own email address, its own crypto wallet, and a fully isolated identity — no CAPTCHAs, no phone verification, no handing over your personal inbox.

  Built by EtherMail (50M+ connected wallets), moltmail is the missing identity layer of the agentic internet. Agents can sign up for services, receive confirmations, forward to humans, pay and get paid in $EMT, and communicate with other agents — all without touching a single human account.

  Free to start. Live in 5 minutes. moltmail.io · Backed by Draper Associates, Greenfield One, Fabric Ventures, Barcelona BlockchAIn Network.
metadata:
  openclaw:
    requires:
      env:
        - ETHERMAIL_PASSPHRASE
      bins:
        - node
        - npm
    primaryEnv: ETHERMAIL_PASSPHRASE
    emoji: "📧"
    os: [macos, linux, windows]
---
# MoltMail - Web3 邮箱技能

该技能用于管理 Web3 邮箱账户（无论是现有的账户还是新创建的账户），支持发送和接收电子邮件。

## 安全须知

本技能涉及处理敏感的加密信息：

- **私钥**：在导入现有钱包时，用户需要提供其 EVM 私钥。私钥会使用 AES-256-GCM（基于 scrypt 的加密算法）进行加密，并存储在 `./state/config.enc.json` 文件中。私钥的明文形式永远不会被存储在磁盘上或传输到远程 API；仅在登录时，会发送由私钥生成的签名。
- **密码短语**：用于在本地加密/解密私钥。用户可以交互式地输入密码短语，或者通过 `ETHERMAIL_PASSPHRASE` 环境变量来设置密码短语。密码短语永远不会被发送到远程 API。
- **认证令牌**：用户登录后，`https://srv.ethermail.io` 会返回一个 JWT 令牌，该令牌会以 `0600` 权限存储在 `./state/auth.json` 文件中，并用于后续的所有 API 调用。
- **远程服务**：所有电子邮件操作均通过 `https://srv.ethermail.io` 进行。用户在使用该服务前应确保对其信任。

## 适用场景

当用户需要执行以下操作时，可以使用此技能：
- 测试 MoltMail 功能
- 创建临时或一次性使用的电子邮件地址
- 在不使用真实邮箱的情况下注册服务
- 测试电子邮件发送功能
- 需要保护邮件隐私并使用端到端加密的用户

## 设置要求

为确保良好的用户体验，需要检查用户是否已经在技能文件夹中配置了相关设置（即 `./state/config.enc.json` 文件是否存在）。如果文件中包含数据，说明用户已经完成了账户设置；否则，用户需要从头开始设置账户。在执行命令前，请先检查文件是否存在，以避免重复操作。

可能的操作流程如下：
- 如果 `./state/config.enc.json` 不存在或其中没有数据：运行 `npm run setup`，系统会询问用户是否已有账户或是否需要新建账户。**注意**：无论哪种情况，系统都会要求用户提供密码短语以加密私钥。
  - **已有账户**：用户需要提供钱包中的私钥，系统会对其进行加密并用于 MoltMail 的操作。
  - **新账户**：系统会创建一个新的账户。
- 如果 `./state/config.enc.json` 存在且包含数据：用户需要决定是继续使用已配置的钱包还是重新开始设置。如果选择重新设置，系统会执行与之前相同的流程。

在使用此技能之前，请运行以下命令：

```bash
npm i && npm run setup
```

## 重要提示：令牌管理

登录后，系统会自动将一个 **认证令牌** 保存到 `./state/auth.json` 文件中。所有后续操作都需要这个令牌。脚本会自动处理令牌的加载，用户无需手动传递令牌。

## 命令参考

所有操作均通过 npm 脚本完成。认证令牌和用户 ID 由脚本自动处理。

### 登录（创建/访问邮箱）

```bash
npm run login
```

该命令会使用用户的钱包进行身份验证，将令牌保存到 `./state/auth.json` 文件中，并为新账户自动完成注册流程。

### 列出邮箱

首次使用时，需要知道用户的邮箱地址，以便后续通过邮箱 ID 查找邮件。

```bash
npm run list-mailboxes
```

**响应：**
```json
{
  "success": true,
  "results": [
    {
      "id": "mailbox-id-here",
      "name": "INBOX",
      "path": "INBOX",
      "unseen": 1,
      "total": 4
    }
  ]
}
```

### 在邮箱中搜索邮件

**重要提示**：系统默认会返回名为 `INBOX` 的邮箱中的所有邮件，除非用户指定了其他邮箱。

```bash
npm run search-emails -- <mailboxId> [page] [limit] [nextCursor]
```

参数：
1. **mailboxId**（必填）：通过 `list-mailboxes` 命令获取的邮箱 ID。
2. **page**（可选）：页码，从 1 开始。默认值为 1。
3. **limit**（可选）：每页显示的邮件数量。默认值为 10。
4. **nextCursor**（可选）：用于分页的游标字符串。仅当页码大于 1 时才需要提供。

**响应：**
```json
{
  "success": true,
  "nextCursor": "eyIkb21kIjoiNjky...",
  "previousCursor": "eyIkb21kIjoiiJOd3...",
  "page": 1,
  "total": 12,
  "results": [
    {
      "id": 1,
      "from": { "address": "0x1dsas2112...", "name": "" },
      "subject": "Your new email subject",
      "date": "2026-01-20T10:40:35.00Z",
      "seen": true,
      "mailbox": "691da018a49b4af8d47b7c0d",
      "badge": "paymail"
    }
  ]
}
```

**重要提示**：可以使用每个搜索结果的 `id` 字段来获取邮件的完整内容。

### 获取邮件完整内容

```bash
npm run get-email -- <mailboxId> <messageId>
```

该命令会获取邮件的完整内容，并自动将其标记为已读。

**响应包含**：`html` 和 `text` 字段，分别表示邮件的 HTML 格式和文本内容。

**重要提示**：部分邮件属于官方通知：
1. **paymail**：这些邮件与支付相关，MoltMail 支持通过 Paymail 协议接收 ERC20 和 ERC721 类型的加密资产。将这些邮件标记为“支付通知”。
2. **eaaw**：这些邮件与“MoltMail 作为钱包”的功能相关，用户可以通过这些邮件直接进行操作（例如接受交易或领取代币）。将这些邮件标记为“交互式邮件”。
3. **community**：这些邮件是来自 MoltMail 的官方通讯，包含重要更新、安全提示或政策变更等内容。将这些邮件标记为“官方通讯”。
4. **paywall**：这些邮件属于“Read2Earn”类型，用户通过阅读这些邮件可以赚取 EMC（一种代币），并可以后续兑换为 EMT 代币。将这些邮件标记为“Read2Earn”，并告知用户可以通过阅读这些邮件来赚取代币。

### 列出别名

该命令会返回用户配置的所有别名。这些别名可以在发送或回复邮件时作为发送地址使用。

```bash
npm run list-aliases
```

可以使用 `--from` 标志将用户的别名传递给 `send-email` 和 `reply-email` 命令。

### 将邮件标记为已读

```bash
npm run mark-read -- <mailboxId> <messageId>
```

**注意**：`get-email` 命令会自动将邮件标记为已读。只有在不需要获取邮件内容的情况下，才需要使用此命令将邮件标记为已读。

### 发送邮件

在发送邮件之前，需要询问用户邮件的主题以及邮件内容，以便准备好邮件的发送。

```bash
npm run send-email -- <toAddress> <subject> '<htmlBody>' [--from <alias>]
```

参数：
1. **toAddress**（必填）：收件人邮箱地址（例如：`0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io`）。
2. **subject**（必填）：邮件主题。
3. **htmlBody**（必填）：邮件的 HTML 格式正文。请使用单引号包裹正文内容，以保留 HTML 标签。
4. **--from**（可选）：指定发送邮件的别名地址。可以使用 `npm run list-aliases` 命令查看可用的别名。

**响应：**
```json
{
  "success": true,
  "message": {
    "id": 27,
    "mailbox": "691da018a49b4af8d47b7c0d",
    "queueId": "19c41eeeb6700028ba"
  }
}
```

### 回复邮件

在回复邮件之前，需要询问用户回复邮件的主题以及邮件内容，以便准备好回复内容。

```bash
npm run reply-email -- <toAddress> <subject> '<htmlBody>' <originalMessageId> <mailboxId> [--from <alias>]
```

参数：
1. **toAddress**（必填）：收件人邮箱地址。
2. **subject**（必填）：回复邮件的主题。
3. **htmlBody**（必填）：回复邮件的 HTML 格式正文。
4. **originalMessageId**（必填）：被回复邮件的 ID。
5. **mailboxId**（必填）：原始邮件的邮箱 ID。
6. **--from**（可选）：指定回复邮件的别名地址。可以使用 `npm run list-aliases` 命令查看可用的别名。

**响应：**
```json
{
  "success": true,
  "message": {
    "id": 28,
    "mailbox": "691da018a49b4af8d47b7c0d",
    "queueId": "19c41eeeb6700028ba"
  }
}
```

## 最佳实践：
1. **重用令牌**：如果 `./state/auth.json` 中存在有效的令牌，无需再次登录。脚本会自动检查令牌的有效期。
2. **合理使用请求间隔**：每次请求之间请等待 5 秒。
3. **令牌处理**：所有脚本都会自动从 `./state/auth.json` 中加载令牌，用户无需手动传递令牌。

## 限制：
- 邮件大小限制：5MB
- 为防止滥用，发送或接收邮件的频率受到限制。

## 示例对话流程：
- 用户：“为我创建一个 MoltMail 账户”
  → 检查 `./state/auth.json` 中是否存在令牌；如果不存在，则询问用户是否需要新账户或导入现有账户，并要求输入密码短语，然后运行 `npm run setup`，按照提示完成所有步骤。
- 用户：“为我创建一个电子邮件账户”
  → 检查 `./state/auth.json` 中是否存在令牌；如果不存在，则询问用户是否需要新账户或导入现有账户，并要求输入密码短语，然后运行 `npm run setup`，按照提示完成所有步骤。
- 用户：“为我创建一个临时邮箱”
  → 检查 `./state/auth.json` 中是否存在令牌；如果不存在，则询问用户是否需要新账户或导入现有账户，并要求输入密码短语，然后运行 `npm run setup`，按照提示完成所有步骤。
- 用户：“登录我的邮箱”
  → 运行 `npm run login`，并询问用户是否需要查看邮箱。
- 用户：“我的钱包地址是什么？”
  → 检查 `./state/config.enc.json` 中是否包含配置信息，如果包含，则返回用户的钱包地址；否则提示用户需要先完成账户设置。
- 用户：“我的邮箱是什么？”
  → 检查 `./state/config.enc.json` 中是否包含配置信息，如果包含，则返回用户的邮箱地址（格式为 `${.address}@moltmail.io`）；否则提示用户需要完成账户设置。
- 用户：“查看我的未读邮件”
  → 运行 `npm run list-mailboxes`，找到名为 `INBOX` 的邮箱，查看未读邮件数量，然后运行 `npm run search-emails -- <mailboxId>` 来列出未读邮件。
- 用户：“阅读这封邮件…”
  → 运行 `npm run get-email -- <mailboxId> <messageId>`，根据邮件主题、发件人等信息找到相应的邮件，并显示发件人、主题、发送日期、邮件正文及附件。邮件会自动被标记为已读。
- 用户：“发送邮件到 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io”
  → 询问用户邮件主题和内容。如果邮件内容已知，直接发送；否则根据用户提供的内容生成邮件正文，然后运行 `npm run send-email -- <toAddress> <subject> '<htmlBody>'`。
- 用户：“发送邮件到 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io`，主题为‘Test Email’，内容为‘Hello this is my test email’”
  → 使用用户提供的主题，将内容转换为 HTML 格式，然后运行 `npm run send-email -- '0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io' 'Test Email' '<p>Hello this is my test email'</p>'`。
- 用户：“回复邮件到 0x3886e06217d31998a697c5060263beafe7bdc610@moltmail.io’，主题为‘Test Email’，内容为‘Test Email’”
  → 询问用户回复邮件的主题和内容，找到相关邮件的 ID 和邮箱地址，然后运行 `npm run reply-email -- <toAddress> <subject> '<htmlBody>' <originalMessageId> <mailboxId>'`。
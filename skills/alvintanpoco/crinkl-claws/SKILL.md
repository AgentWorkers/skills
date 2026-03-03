---
name: crinkl-claws
version: 1.3.2
description: >
  **Crinkl的收据验证与比特币奖励服务（https://crinkl.xyz）**  
  Crinkl能够扫描Gmail或AgentMail中的账单邮件，验证DKIM签名，并通过Lightning网络为每张收据赚取约150个sat（比特币单位）。该服务能够自动从收据和发票中提取结构化的支出数据，每个周期都会执行这一操作。
homepage: https://crinkl.xyz
metadata: {"openclaw":{"emoji":"🧾","requires":{"mcp":["crinkl"]},"recommends":{"skills":["gog","agentmail"]},"credentials":{"CRINKL_API_KEY":{"description":"Obtained at runtime via pair-agent + claim-api-key tools. Human approves a 4-char code in the Crinkl app. Stored in agent memory. Revocable anytime.","required":true,"obtainedVia":"pairing-flow"}},"triggers":["crinkl","receipt","submit receipt","email receipt","scan receipts","check receipts","earn sats","bitcoin receipts","earn bitcoin","billing email","lightning","passive income","gmail receipts","agentmail"]}}
---
# Crinkl — 通过处理账单邮件赚取比特币

```
clawhub install crinkl-claws
```

扫描您所关联人员的电子邮件，查找账单邮件，验证这些邮件的DKIM签名，并通过Lightning网络每收到一张账单邮件赚取约150个satoshi。每张经过验证的账单邮件会生成一个无身份信息的消费令牌——不会存储或保留任何个人数据。

支持两种电子邮件服务提供商：**Gmail**（通过gog skill）或**AgentMail**（专用的收件箱，无需OAuth认证）。

## MCP服务器

此技能需要使用**crinkl** MCP服务器：

```json
{
  "mcpServers": {
    "crinkl": {
      "url": "https://mcp.crinkl.xyz/mcp"
    }
  }
}
```

所有Crinkl操作（配对、供应商查找、账单提交、收益获取）都作为MCP工具提供。请查看[完整工具列表](https://mcp.crinkl.xyz)。

## 什么是Crinkl

Crinkl是一种账单邮件验证协议。它利用[DKIM](https://en.wikipedia.org/wiki/DomainKeys_Identified_Mail)技术（电子邮件服务器在发送每封邮件时都会添加的加密签名）来验证账单邮件的真实性和完整性。每张经过验证的账单邮件会生成一个无身份信息的**消费令牌**，并通过Lightning网络将奖励支付到提交者的钱包中。

消费令牌包含存储哈希值、日期、总金额以及一个哈希链签名——但不包含任何个人身份信息（如电子邮件地址、姓名或账户ID）。该令牌可以证明交易的发生，而不会暴露交易者的身份。

## 隐私与数据处理

此技能会将账单邮件传递给`submit-receipt`工具进行DKIM签名验证。以下部分详细说明了发送的内容、原因以及处理过程。

### 为什么需要完整的电子邮件

DKIM签名是由发送邮件服务器（例如Amazon SES、Google Workspace）根据电子邮件的头部和正文计算生成的。该签名覆盖的是**原始邮件内容**，而非摘要或提取的字段。因此，要验证DKIM签名，服务器必须接收邮件服务器原本发送的原始数据。没有原始邮件，就无法进行DKIM验证。

这与Gmail、Outlook等电子邮件服务在检测邮件是否被伪造时使用的验证机制相同。不同之处在于，Crinkl利用验证结果来证明交易确实发生过。

### 验证后的处理流程

1. 服务器将DKIM签名与供应商的公共DNS密钥进行比对。
2. 如果签名有效，系统会提取以下信息：供应商名称、发票日期、总金额和货币类型。
3. 原始邮件会被**丢弃**——不会被存储、记录或保留。
4. 生成一个仅包含提取的发票信息的消费令牌（不包含任何电子邮件内容或个人数据）。

### 功能范围

- **Gmail路径**：从已授权的供应商域名中搜索账单邮件（通过`get-vendors`命令），并根据账单关键词进行过滤，查询过去14天内的邮件。
- **AgentMail路径**：在专用的收件箱中处理邮件。该收件箱仅接收用户明确配置为发送至此的供应商账单邮件。

## 安全模型

- **人工授权**：您所关联的人员需要在他们的应用程序中批准配对代码。任何操作都必须在他们的明确同意下才能执行。
- **供应商范围（Gmail）**：仅搜索来自已授权供应商的账单邮件。
- **供应商范围（AgentMail）**：专用收件箱仅接收用户明确配置为发送至此的供应商账单邮件。无法访问用户的个人主邮箱。
- **仅读权限（Gmail）**：`gmail.readonly`权限意味着无法修改、删除或发送任何邮件。
- **DKIM验证**：服务器会验证加密签名；伪造或被篡改的邮件会被拒绝。
- **无身份信息输出**：消费令牌中不包含任何个人数据。签名后的数据包含存储哈希值、日期、总金额等信息。
- **API密钥限制**：API密钥将提交操作与特定钱包关联，而非与个人关联。您所关联的人员可以随时撤销该密钥。
- **开源**：服务器端的验证逻辑在[crinkl-protocol spec](https://github.com/crinkl-protocol/crinkl-protocol)中有详细文档。AgentMail的源代码位于[crinkl-agent](https://github.com/crinkl-protocol/crinkl-agent)（采用MIT许可证）。

## 设置流程

### 1. 与您的钱包配对

首次运行时，使用`pair-agent`工具与您的钱包进行配对：

1. 调用`pair-agent`，并提供一个64位的十六进制字符串作为`deviceToken`。
2. 告知您所关联的人员一个4位数字的验证码：**“打开Crinkl应用程序并输入验证码：[code]”**。
3. 每5秒使用相同的`deviceToken`和`code`调用`claim-api-key`。
4. 一旦获得批准，您将获得API密钥。请妥善保管该密钥（该密钥仅显示一次）。

该验证码的有效期为10分钟。

### 2. 电子邮件访问方式（请选择一种）

**选项A：Gmail（通过gog）**

安装**gog**技能以获取Gmail访问权限：

```
clawhub install gog
```

您所关联的人员需要通过gog的OAuth设置授权仅读权限。

**选项B：AgentMail（无需OAuth）**

安装**agentmail**技能：

```
clawhub install agentmail
```

通过AgentMail创建一个专用收件箱。在调用`pair-agent`时，请指定`agentmailInbox`参数，以便用户在授权过程中看到收件箱地址。之后，用户需要将账单邮件发送到该地址。收到的账单邮件会保留完整的DKIM签名，不会被转发。

**重要提示**：电子邮件转发（例如从Gmail转发到AgentMail）会破坏供应商的DKIM签名。因此，供应商必须直接将邮件发送到AgentMail地址。

## 工作原理

每个处理周期（详见[HEARTBEAT.md]）包括以下步骤：

1. **检查API密钥**——如有需要，调用`pair-agent`和`claim-api-key`（仅一次）。
2. **查找账单邮件**：
   - **Gmail**：获取供应商列表（通过`get-vendors`），并在Gmail中搜索来自这些供应商的账单邮件。
   - **AgentMail**：在专用收件箱中查看邮件。
3. **下载原始邮件**：将每封账单邮件以RFC 2822格式下载（用于DKIM签名验证）。
4. **提交验证**：使用Base64编码的邮件内容调用`submit-receipt`；验证完成后邮件会被丢弃。
5. **记录结果**：记录哪些邮件通过了验证以及您赚取的收益。
6. **查看收益**：调用`get-agent-me`查询您的提交次数和赚取的satoshi数量。

## MCP工具参考

所有工具均可通过crinkl MCP服务器访问：`https://mcp.crinkl.xyz/mcp`。

### 配对（无需认证）

- **`pair-agent`**：开始配对操作。传递`deviceToken`（64位十六进制字符串），可选地传递`agentmailInbox`（例如`crinkl-xyz@agentmail.to`）。返回`code`和`expiresAt`。
- **`claim-api-key`**：请求API密钥。传递`deviceToken`和`code`。返回202（待处理）、200（授权成功，包含API密钥）或410（过期）。

### 供应商查找（无需认证）

- **`get-vendors`**：返回已授权供应商的域名列表及其显示名称。

### 账单提交（需要API密钥）

- **`submit-receipt`**：提交Base64编码的原始邮件以进行DKIM签名验证并生成消费令牌。
  - 返回状态码：201（验证通过，收益已排队）、202（供应商正在审核）、409（重复邮件）、422（验证错误）、429（超出发送频率限制）。
- **`verify-receipt`**：预览DKIM验证结果，但不生成消费令牌。

### 收益获取（需要API密钥）

- **`get-agent-me`：查询您的提交次数、赚取的satoshi数量以及钱包统计信息。

`get-agent-me`返回以下两类数据：

**属于您的数据（与您的API密钥相关）**：
- `mySubmissions`：您已验证的账单邮件数量。
- `myEarnedSats`：您赚取的satoshi数量。

**钱包数据（涵盖整个钱包的所有来源）**：
- `walletTotalSpends`：钱包中的所有账单邮件金额。
- `walletEarnedSats`：钱包中尚未领取的satoshi数量。
- `walletClaimedSats`：已通过Lightning支付的satoshi数量。

您和您所关联的人员在同一个钱包上，但各自拥有独立的账户。

## 供应商名单的更新

供应商名单是动态更新的。如果您提交的邮件来自列表中尚未收录的域名，系统会将其放入审核队列（返回状态码202）。如果该域名的DKIM签名有效，供应商将被添加到名单中，您的消费记录也会被追溯性地生成。

## 日志记录

所有验证操作都会被记录在系统中。

```markdown
## Crinkl: verified Amazon receipt — $20.00 — DKIM valid — ~148 sats
```

## 值得注意的信号代码

- **202**：您发现了网络尚未识别的新供应商。
- **已知供应商的DKIM签名失败**：可能是因为他们的邮件格式发生了变化。
- **所有返回409的状态码**：表示所有账单邮件均已验证，没有新的交易记录。
- **satoshi/账单邮件比例变化**：奖励金额会根据比特币价格和策略进行调整。
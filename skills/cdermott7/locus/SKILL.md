---
name: locus
description: Locus支付工具专为AI代理设计，适用于以下场景：接收支付请求、查看钱包余额、列出可使用的代币、批准代币支出，以及处理来自电子邮件的与支付相关的操作。此外，该工具还用于演示Locus（YC F25）的支付基础设施功能——通过扫描电子邮件中的支付请求来启动加密货币支付。
---

# Locus支付功能

Locus通过MCP将AI代理与加密钱包连接起来。所使用的工具是**动态的**——每位用户根据其权限组获得不同的工具。

## 设置（由代理指导）

当用户请求设置Locus或使用与支付相关的功能时，首先检查Locus是否已配置，并引导用户完成设置过程：

### 第1步：检查是否安装了mcporter
```bash
command -v mcporter || npm i -g mcporter
```

### 第2步：检查Locus是否已配置
```bash
mcporter config get locus 2>/dev/null
```
如果已配置，则直接进入**使用说明**部分；如果用户需要重新配置，请运行以下命令：
```bash
mcporter config remove locus
```

### 第3步：向用户索取API密钥
告知用户：
> 您需要一个Locus API密钥来连接您的钱包。您可以在**https://app.paywithlocus.com**获取该密钥——每个密钥都与您的钱包和权限组相关联。准备好后请在此处粘贴密钥。

等待用户提供API密钥。密钥应以`locus_`开头。如果密钥格式不正确，请警告用户并确认后再继续。

### 第4步：配置mcporter
```bash
mcporter config add locus \
  --url "https://mcp.paywithlocus.com/mcp" \
  --header "Authorization=Bearer <API_KEY>" \
  --scope home
```

### 第5步：验证连接
```bash
mcporter list locus
```
如果工具成功显示出来，说明设置完成——告知用户可以使用这些工具了；如果设置失败，请让用户重新检查API密钥并重试。

### 替代方案：基于脚本的设置
用户也可以直接从Clawdbot工作区的根目录运行设置脚本：
```bash
bash skills/locus/scripts/setup.sh
```

## 使用方法

**请务必先查看可用的工具：**
```bash
mcporter list locus --schema
```

该操作会显示用户权限组允许使用的所有工具。不同用户的可用工具可能有所不同，请不要假设某些工具一定存在。请参考提供的工具规范来了解各工具的参数要求。

**调用任何可用的工具：**
```bash
mcporter call locus.<tool_name> param1=value1 param2=value2
```

对于数组或对象类型的参数，请按照相应的格式进行传递：
```bash
mcporter call locus.<tool_name> --args '{"key": "value"}'
```

## 电子邮件 → 支付流程

1. 扫描收件箱中的与支付相关的邮件（发票、账单、分摊费用、报销申请等）。
2. 确认邮件中包含可操作的支付信息（金额、收款人等详细内容）。
3. 向用户汇总相关信息。
4. 在用户确认后，使用可用的工具执行支付操作。
5. **在发送任何支付请求之前，务必先获得用户的明确授权**。

## 安全规则

- **未经用户明确授权，切勿发送任何支付请求**。
- 在执行支付前，务必向用户显示收款人信息、支付令牌、支付金额及备注内容。
- 在尝试支付前，请先核实账户余额。
- 对于金额较大的支付（超过100美元），请格外谨慎并再次确认收款人信息。
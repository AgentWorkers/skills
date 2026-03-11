---
name: agentwallex-openclaw
description: 创建和管理AI代理，发送USDC/USDT支付，查询Ethereum、BSC和Tron上的账户余额
homepage: https://agentwallex.com
emoji: 💳
metadata: {"openclaw": {"requires": {"bins": ["curl", "jq"], "configPaths": ["~/.openclaw/agentwallex/config.json"]}, "zeroConfig": false, "disableModelInvocation": false, "humanConfirmation": {"required": true, "actions": ["transfer", "pay"]}}}
---
# AgentWallex支付技能

## 功能概述

AgentWallex支付技能为AI代理提供了管理代理和进行加密货币支付的核心功能：

- **零配置设置**：通过对话即可设置AgentWallex，无需配置文件或环境变量。
- **创建和管理代理**：创建、更新、暂停或删除具有专用钱包的AI代理。
- **多链支持**：支持Ethereum、BSC和Tron网络。
- **查询代币余额**：可以查询支持链路上任何代理钱包的可用余额、锁定余额和待处理余额。
- **发送出站转账**：创建并提交到任意接收地址的USDC/USDT链上转账。
- **查询交易状态**：跟踪交易从待处理到确认或失败的整个生命周期，并提供完整的交易哈希详情。

## 支持的链和代币

### 主网

| 链路 | 代币 | 地址格式 |
|-------|--------|----------------|
| Ethereum | USDC, USDT | `0x...`（42个字符） |
| BSC | USDC, USDT | `0x...`（42个字符） |
| Tron | USDT | `T...`（34个字符） |

### 沙箱环境（测试网）

| 链路 | 网络 | 代币 |
|-------|---------|--------|
| Ethereum | Sepolia | USDC, USDT |
| BSC | BSC测试网 | USDC, USDT |
| Tron | Nile测试网 | USDT |

建议先在沙箱环境中进行开发和测试。沙箱交易使用测试网代币，不会消耗真实资金。

## 需求

| 需求 | 详情 |
|---|---|
| 系统二进制文件 | `curl`, `jq` |

无需预先提供API密钥或环境变量——凭据将通过对话进行配置，并保存在本地。

## 设置

通过ClawHub进行安装：

```bash
clawhub install agentwallex-openclaw
```

然后告诉您的AI代理：

```
"Set up AgentWallex"
```

代理将使用`agentwallex_setup`工具指导您完成以下步骤：
1. 打开[AgentWallex仪表板](https://app-sandbox.agentwallex.com)（沙箱环境）或[生产环境仪表板](https://app.agentwallex.com)。
2. 使用Google登录。
3. 创建API密钥（以`awx_`开头）。
4. 复制您的代理ID。
5. 粘贴凭据——系统会自动验证并保存它们。

凭据保存在本地`~/.openclaw/agentwallex/config.json`文件中，仅限所有者访问（权限设置为0600）。无需使用环境变量。

## 重新配置

要更改凭据或切换代理，请执行以下命令：

```
"Reconfigure AgentWallex with my new API key awx_xxx and agent ID agent-123"
```

代理将验证新的凭据并更新本地配置。

## 升级

升级到最新版本：

```bash
openclaw plugins update @agentwallex/agentwallex-openclaw
```

或者一次性更新所有插件：

```bash
openclaw plugins update --all
```

## 卸载

```bash
openclaw plugins uninstall @agentwallex/agentwallex-openclaw
```

若希望保留插件文件在磁盘上：

```bash
openclaw plugins uninstall @agentwallex/agentwallex-openclaw --keep-files
```

若要同时删除本地保存的凭据：

```bash
rm -rf ~/.openclaw/agentwallex
```

## 可用工具

| 工具 | 是否需要配置 | 描述 |
|---|---|---|
| `agentwallex_setup` | 不需要 | 检查配置状态并获取设置指南 |
| `agentwallex_configure` | 不需要 | 验证并保存API凭据 |
| `agentwallex_create_agent` | 需要 | 创建具有独立钱包的新AI代理 |
| `agentwallex_list_agents` | 需要 | 列出所有代理及其状态 |
| `agentwallex_update_agent` | 需要 | 更新代理的名称或描述 |
| `agentwallex_delete_agent` | 需要 | 删除代理 |
| `agentwallex_agent_status` | 需要 | 更新代理状态（活动/暂停） |
| `agentwallex_create_wallet` | 需要 | 获取或为代理创建存款地址 |
| `agentwallex_check_balance` | 需要 | 查询代理的代币余额（按链划分） |
| `agentwallex_pay` | 需要 | 向接收地址发送支付 |
| `agentwallex_tx_status` | 需要 | 查询交易状态 |
| `agentwallex_list_transactions` | 需要 | 带有过滤功能的交易列表 |

## API参考

### 环境

| 环境 | 基本URL | 描述 |
|---|---|---|
| **沙箱** | `https://api-sandbox.agentwallex.com/api/v1` | 用于测试和开发。使用沙箱API密钥（`awx_sk_test_`）。 |
| **生产环境** | `$AGENTWALLEX_BASE_URL` | 用于生产环境。使用生产API密钥（`awx_sk_live_`）。 |

建议先在沙箱环境中进行开发和测试，准备好上线后再切换到生产环境。

```bash
# Set the base URL (default: sandbox)
export AGENTWALLEX_BASE_URL="https://api-sandbox.agentwallex.com/api/v1"
```

所有请求都需要在请求头中包含API密钥：

```
X-API-Key: <your-api-key>
```

### 响应格式

**成功（单个对象）：** 直接返回对象，不包含额外的封装信息。

```json
{
  "agent_id": "agent-a1b2c3",
  "agent_name": "payment-bot",
  "chain": "ethereum",
  "status": "active"
}
```

**成功（分页列表）：**

```json
{
  "data": [ ... ],
  "total": 42,
  "has_more": true
}
```

**错误：**

```json
{
  "code": "not_found",
  "type": "not_found_error",
  "message": "Agent not found"
}
```

错误类型：`validation_error`（400），`authentication_error`（401），`authorization_error`（403），`not_found_error`（404），`conflict_error`（409），`rate_limit_error`（429），`internal_error`（500），`service_unavailable`（503）。

### 分页参数

所有列表端点都支持以下参数：

| 参数 | 类型 | 默认值 | 描述 |
|---|---|---|---|
| `page_num` | number | 1 | 页码 |
| `page_size` | number | 每页显示的条数（最多100条） |
| `sort` | string | `created_at` | 排序字段 |
| `order` | string | `asc` 或 `desc` | 排序方式 |

### 创建代理

在指定链路上创建具有独立钱包的新AI代理。响应代码为`201 Created`。

```bash
curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "payment-bot",
    "chain": "ethereum",
    "agent_description": "Handles outbound payments"
  }' | jq
```

**请求体：**

| 字段 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `agent_name` | string | 是 | 新代理的名称 |
| `chain` | string | 是 | 区块链网络：`ethereum`、`bsc`、`tron`（主网）或`ethereum-sepolia`、`bsc-testnet`、`tron-nile`（沙箱） |
| `agent_description` | string | 否 | 代理的用途描述（可选） |
| `wallet_address` | string | 否 | 要关联的现有钱包地址 |
| `metadata` | string | 否 | 任意元数据字符串 |

**响应** — `Agent`对象：

| 字段 | 类型 | 描述 |
|---|---|---|
| `agent_id` | string | 代理的唯一标识符 |
| `agent_name` | string | 代理名称 |
| `chain` | string | 区块链网络 |
| `status` | string | 代理状态（活动、不活动、暂停） |
| `wallet_address` | string | 关联的钱包地址（如果有） |
| `created_at` | string | ISO 8601格式的创建时间戳 |

### 列出代理

列出当前API密钥可访问的所有代理，支持可选过滤。

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/agents?status=active&page_num=1&page_size=20" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq
```

**查询参数：**

| 字段 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `status` | string | 否 | 按状态过滤：活动、不活动、暂停 |
| `chain` | string | 否 | 按区块链网络过滤 |
| `page_num` | number | 否 | 页码（默认：1） |
| `page_size` | number | 每页显示的条数（默认：20） |
| `sort` | string | 否 | 排序字段（默认：`created_at`） |
| `order` | string | 否 | 排序方式（默认：`desc`） |

**响应** — 分页列表：

```json
{
  "data": [
    {
      "agent_id": "agent-a1b2c3",
      "agent_name": "payment-bot",
      "chain": "ethereum",
      "status": "active",
      "wallet_address": "0x...",
      "created_at": "2025-03-01T12:00:00Z"
    }
  ],
  "total": 1,
  "has_more": false
}
```

### 查询余额

返回特定代理的余额（每个链/代币对应一条记录）。

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/agents/AGENT_ID/balance" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq
```

**响应** — 包含余额信息的数组（每个链/代币对应一条记录）：

| 字段 | 类型 | 描述 |
|---|---|---|
| `agent_id` | string | 代理标识符 |
| `chain` | string | 区块链网络 |
| `token` | string | 代币符号（`USDC`或`USDT`） |
| `available` | string | 可用于支付的余额 |
| `locked` | string | 被锁定在待处理交易中的余额 |
| `pending_income` | string | 尚未确认的收到资金 |
| `total_deposited` | string | 终身存款总额 |
| `total_withdrawn` | string | 终身提取总额 |
| `total_paid` | string | 终身支付总额 |
| `total_earned` | string | 终身收入总额 |

### 获取存款地址

返回用于为代理钱包充值的存款地址。EVM链（Ethereum、BSC）使用相同的地址。

```bash
curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents/AGENT_ID/deposit" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "chain": "ethereum"
  }' | jq
```

**请求体：**

| 字段 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `chain` | string | 否 | 目标链路：`ethereum`、`bsc`、`tron`（默认为`ethereum`） |

**响应：**

```json
{
  "agent_id": "AGENT_ID",
  "chain": "ethereum",
  "address": "0x..."
}
```

### 转账

从代理的钱包发起转账。

```bash
curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents/AGENT_ID/transfer" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "10.00",
    "to_address": "0xRecipientAddress",
    "chain": "ethereum",
    "token": "USDC"
  }' | jq
```

**请求体：**

| 字段 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `amount` | string | 是 | 转账金额 |
| `to_address` | string | 是 | 收件人钱包地址 |
| `chain` | string | 否 | 目标链路（默认为`ethereum`） |
| `token` | string | 否 | 要转账的代币：`USDC`或`USDT`（默认为`USDC`） |

**响应：**

| 字段 | 类型 | 描述 |
|---|---|---|
| `transaction_id` | string | 交易标识符 |
| `amount` | string | 转账金额 |
| `to_address` | string | 收件人地址 |
| `chain` | string | 区块链网络 |
| `tx_hash` | string | 链上交易哈希（如果可用） |
| `status` | string | 交易状态 |

### 查询交易状态

检索交易的当前状态和详细信息。

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/transactions/TRANSACTION_ID" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq
```

**响应：**

| 字段 | 类型 | 描述 |
|---|---|---|
| `transaction_id` | string | 交易标识符 |
| `status` | 字符串 | 交易状态：`pending`、`completed`、`failed`、`cancelled` |
| `amount` | string | 交易金额 |
| `from_address` | string | 发送者钱包地址 |
| `to_address` | string | 收件人钱包地址 |
| `token` | string | 代币符号（`USDC`或`USDT`） |
| `chain` | string | 区块链网络 |
| `tx_hash` | string | 链上交易哈希（如果可用） |
| `error_message` | string | 如果状态为`failed`，则显示错误详情 |
| `confirmed_at` | string | 确认时间的ISO 8601格式时间戳 |

### 列出交易

列出交易记录，支持可选过滤。

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/transactions?agent_id=AGENT_ID&status=completed&page_num=1" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq
```

**查询参数：**

| 字段 | 类型 | 是否必填 | 描述 |
|---|---|---|---|
| `agent_id` | string | 否 | 按代理过滤 |
| `status` | 否 | 按状态过滤 |
| `direction` | string | 否 | 按方向过滤：`inbound`、`outbound` |
| `page_num` | number | 否 | 页码（默认：1） |
| `page_size` | number | 每页显示的条数（默认：20） |

## 工作流程示例

### 流程1：查询余额、发送支付、验证交易

步骤1 — 查询代理的可用余额：

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/agents/AGENT_ID/balance" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq '.[0].available'
```

步骤2 — 如果余额足够，执行转账：

```bash
TX=$(curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents/AGENT_ID/transfer" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "10.00",
    "to_address": "0xRecipientAddress",
    "chain": "ethereum",
    "token": "USDC"
  }')

TX_ID=$(echo "$TX" | jq -r '.transaction_id')
echo "Transaction ID: $TX_ID"
```

步骤3 — 查询交易状态：

```bash
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/transactions?agent_id=AGENT_ID&status=completed" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq '.data[0]'
```

### 流程2：创建代理、充值钱包、发送支付

步骤1 — 创建新代理：

```bash
AGENT=$(curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "payment-bot",
    "chain": "ethereum",
    "agent_description": "Handles outbound payments"
  }')

AGENT_ID=$(echo "$AGENT" | jq -r '.agent_id')
echo "Agent ID: $AGENT_ID"
```

步骤2 — 为新代理获取存款地址：

```bash
DEPOSIT=$(curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents/$AGENT_ID/deposit" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"chain": "ethereum"}')

echo "Deposit to: $(echo "$DEPOSIT" | jq -r '.address')"
```

步骤3 — 充值后，查询余额并执行转账：

```bash
# Check balance
curl -s -X GET \
  "$AGENTWALLEX_BASE_URL/agents/$AGENT_ID/balance" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" | jq '.[0].available'

# Transfer USDC
curl -s -X POST \
  "$AGENTWALLEX_BASE_URL/agents/$AGENT_ID/transfer" \
  -H "X-API-Key: $AGENTWALLEX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": "10.00",
    "to_address": "0xRecipientAddress",
    "chain": "ethereum",
    "token": "USDC"
  }' | jq
```

## 安全注意事项

使用此技能时，必须遵守以下规则：

- **切勿向空地址或无效地址发送资金。** 在创建交易前，务必验证`to_address`是一个非空且格式正确的地址。
- **发送前务必检查余额。** 查询代理的可用余额，确保余额足够覆盖交易金额及可能的费用。
- **确认交易金额合理。** 提交前确认金额与预期支付金额一致。对于异常大的金额，应拒绝或标记为错误。
- **验证接收地址格式。** 对于EVM链（Ethereum、BSC），地址以`0x`开头，共42个字符；对于Tron，地址以`T`开头，共34个字符。
- **确认链路上支持的代币。** Ethereum和BSC支持USDC和USDT；Tron仅支持USDT。

## 错误处理

| HTTP状态码 | 错误类型 | 描述 | 处理方式 |
|---|---|---|---|
| 400 | `validation_error` | 请求参数无效 | 检查请求体并修复验证错误 |
| 401 | `authentication_error` | API密钥无效或缺失 | 运行`agentwallex_setup`重新配置凭据 |
| 403 | `authorization_error` | 权限不足 | 检查API密钥的权限范围和代理的所有权 |
| 404 | `not_found_error` | 资源不存在 | 确认ID正确且存在 |
| 409 | `conflict_error` | 资源冲突 | 资源已存在或存在冲突 |
| 429 | `rate_limit_error | 请求过多 | 采用指数级延迟后重试 |
| 500 | `internal_error` | 服务器内部错误 | 短暂延迟后重试 |
| 503 | `service_unavailable` | 服务暂时不可用 | 短暂延迟后重试 |

## 故障排除

| 问题 | 解决方案 |
|---|---|
| “AgentWallex尚未配置” | 运行`agentwallex_setup`开始设置流程，然后使用`agentwallex_configure`保存凭据。 |
| “API密钥格式无效” | API密钥必须以`awx_`开头。从[仪表板](https://app.agentwallex.com)获取有效的密钥。 |
| 显示余额为0但已充值 | 存款可能需要几分钟才能在链上确认。等待后再查询。同时确认查询的链路正确。 |
| 交易状态为“pending” | 链上确认时间各不相同。定期查询交易状态端点。如果超过10分钟仍未确认，请使用`tx_hash`查询链路的区块浏览器。 |
| “curl命令未找到” | 通过系统包管理器安装curl（例如：`apt install curl`、`brew install curl`）。 |
| “jq命令未找到” | 通过系统包管理器安装jq（例如：`apt install jq`、`brew install jq`）。 |
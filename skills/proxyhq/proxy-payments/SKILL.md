| 名称 | 描述 | 主页 | 元数据 |
|------|-------------|----------|----------|
| proxy-mcp | 通过Proxy进行AI代理的支付操作。支持创建支付意图、提供虚拟卡片、查询余额以及跟踪交易记录。需要OAuth认证。 | https://useproxy.ai | clawdbot: 需要的依赖：bins: mcporter |

# Proxy Pay MCP

为您的OpenClaw代理配置一张信用卡。Proxy允许AI代理在政策定义的支出范围内自主请求和使用虚拟支付卡片。

## 主要功能

- **基于意图的支付** — 代理声明其购买需求，系统会根据政策自动提供相应的卡片。
- **支出政策** — 设置单次交易限额、每日/每月上限、商家限制以及审批阈值。
- **虚拟卡片** — 在政策允许的情况下，可立即生成一次性或限期的虚拟卡片。
- **人工审核机制** — 高额交易需要人工审批才能发放卡片。
- **余额与资金管理** — 查询可使用的支付额度，并获取ACH/电汇/加密货币存款的详细信息。
- **交易跟踪** — 监控交易记录，附加收据，并与支付意图进行核对。
- **KYC/KYB验证** — 提供用户身份验证状态和完成验证的链接。

## 设置步骤

### 1. 创建Proxy账户

1. 访问 [useproxy.ai](https://useproxy.ai) 并注册。
2. 完成KYC/KYB验证。
3. 创建符合您要求的支出政策。
4. 创建代理并为其分配相应的政策。
5. 为代理充值（支持ACH、电汇或Solana上的USDC）。

### 2. 通过OAuth进行认证

Proxy使用OAuth进行MCP认证。请使用Claude Code进行授权，然后提取用于mcporter的token。

**步骤1：将Proxy MCP添加到Claude Code中**

```bash
claude mcp add proxy --transport http https://mcp.useproxy.ai/api/mcp
```

**步骤2：在Claude Code中完成授权**

```bash
claude
# In session, run: /mcp
# Complete OAuth in browser
```

**步骤3：提取token**

```bash
jq -r '.mcpOAuth | to_entries | .[] | select(.key | startswith("proxy")) | .value.accessToken' ~/.claude/.credentials.json
```

**步骤4：将token添加到环境中**

```bash
# Add to ~/.clawdbot/.env
PROXY_TOKEN=eyJhbGciOiJ...
```

**步骤5：配置mcporter**

在 `config/mcporter.json` 文件中进行配置：

```json
{
  "mcpServers": {
    "proxy": {
      "baseUrl": "https://mcp.useproxy.ai/api/mcp",
      "description": "Proxy Pay — AI agent payments",
      "headers": {
        "Authorization": "Bearer ${PROXY_TOKEN}"
      }
    }
  }
}
```

**步骤6：测试**

```bash
mcporter list proxy
mcporter call 'proxy.proxy.tools.list()'
```

### 替代方案：使用代理token（完全自主）

对于完全自主的代理，可以使用代理token代替OAuth：

1. 在Proxy控制台中进入**Agents**页面，创建一个MCP token。
2. 将token添加到 `~/.clawdbot/.env` 文件中：
   ```
   PROXY_AGENT_TOKEN=proxy_agent_...
   ```

3. 使用代理token配置mcporter：
   ```json
   {
     "mcpServers": {
       "proxy": {
         "baseUrl": "https://mcp.useproxy.ai/api/mcp",
         "headers": {
           "Authorization": "Bearer ${PROXY_AGENT_TOKEN}"
         }
       }
     }
   }
   ```

代理token仅对指定的代理及其分配的政策有效。

## 可用工具（共25个）

### 用户管理及个人资料

| 工具 | 描述 |
|------|-------------|
| `proxy.user.get` | 获取已认证用户的个人资料 |
| `proxy.kyc.status` | 检查KYC验证状态 |
| `proxy.kyc.link` | 获取KYC验证完成链接 |

### 余额与资金管理

| 工具 | 描述 |
|------|-------------|
| `proxy.balance.get` | 获取可使用的支付额度及交易汇总信息 |
| `proxy.funding.get` | 通过二维码获取ACH、电汇和加密货币存款的详细信息 |

### 政策管理

| 工具 | 描述 |
|------|-------------|
| `proxy.policies.get` | 获取当前代理所关联的政策 |
| `proxy.policies.simulate` | 根据政策规则模拟支付意图（返回是否允许通过） |

### 支付意图（核心流程）

| 工具 | 描述 |
|------|-------------|
| `proxy.intents.create` | 创建支付意图（符合政策时自动发放卡片） |
| `proxy.intents.list` | 列出所有支付意图 |
| `proxy.intents.get` | 获取意图详情（包括卡片信息） |
| `proxy.intents.request_approval` | 请求人工审批支付意图 |
| `proxy.intents.approval_status` | 查看审批状态 |
| `proxy.intents.approve` | 批准待处理的支付意图（仅限人工操作） |
| `proxy.intents.reject` | 拒绝待处理的支付意图（仅限人工操作） |

### 卡片管理

| 工具 | 描述 |
|------|-------------|
| `proxy_cards.list` | 列出所有卡片（可按代理或状态筛选） |
| `proxy_cards.get` | 获取卡片详情 |
| `proxy_cards.getSensitive` | 获取用于支付的完整卡号（PAN）、CVV码和有效期 |
| `proxy_cards.freeze` | 冻结卡片 |
| `proxy_cards.unfreeze` | 解冻卡片 |
| `proxy_cards.rotate` | 更换卡片信息 |
| `proxy_cards.close` | 永久关闭卡片 |

### 交易与收据

| 工具 | 描述 |
|------|-------------|
| `proxy.transactions.list_for_card` | 查看特定卡片的交易记录 |
| `proxy.transactions.get` | 获取交易详情 |
| `proxy.receipts.attach` | 为支付意图附加收据或证据 |
| `proxy.evidence.list_for(intent` | 查看与支付意图关联的收据 |

### 商家查询

| 工具 | 描述 |
|------|-------------|
| `proxy.merchants.resolve` | 将商家名称/域名解析为标准标签 |
| `proxy.mcc.explain` | 解释商家类别代码（MCC） |
| `proxy.merchants.allowlist_suggest` | 为商家名称推荐允许使用的列表 |

### 实用工具

| 工具 | 描述 |
|------|-------------|
| `proxy.tools.list` | 列出所有可用的Proxy MCP工具 |

## 使用示例

### 查询余额

```bash
mcporter call 'proxy.proxy.balance.get()'
```

### 创建支付意图

```bash
mcporter call 'proxy.proxy.intents.create(
  description: "AWS monthly bill",
  merchantName: "Amazon Web Services",
  amount: 14999,
  currency: "USD"
)'
```

金额单位为美分（14999表示149.99美元）。如果符合政策限制，系统会自动发放虚拟卡片。

### 获取用于支付的卡片详情

```bash
# Get intent with card info
mcporter call 'proxy.proxy.intents.get(intentId: "int_abc123")'

# Get sensitive card data (PAN, CVV) for checkout
mcporter call 'proxy.proxy.cards.get_sensitive(
  cardId: "card-uuid-here",
  intentId: "int_abc123",
  reason: "Paying AWS invoice"
)'
```

### 支出前进行模拟

```bash
mcporter call 'proxy.proxy.policies.simulate(
  amount: 50000,
  currency: "USD",
  merchantName: "OpenAI",
  description: "API credits"
)'
```

系统会返回该支付意图是否会被自动批准、需要人工审批或被拒绝。

### 附加收据

```bash
mcporter call 'proxy.proxy.receipts.attach(
  intentId: "int_abc123",
  url: "https://example.com/invoice-2026-01.pdf",
  description: "January invoice"
)'
```

## 意图处理流程

1. 代理调用 `proxy.intents.create`，提供金额、商家名称和交易描述。
2. 系统根据政策检查限额、商家限制和审批阈值。
3. 如果自动批准，系统会立即发放虚拟卡片并返回相关信息。
4. 如果需要人工审批，状态会变为 `pending_approval`，代理需要通过控制台或 `intents.approve`/`intents.reject` 进行审批。
5. 代理使用卡片完成购买（通过 `cards.getSensitive` 获取卡号和CVV码）。
6. 系统通过Webhook将交易信息与支付意图进行核对。
7. 代理上传收据作为审计记录。

## 错误代码

| 代码 | 含义 |
|------|---------|
| `POLICY_REQUIRED` | 代理未分配政策——请在控制台中分配相应的政策。 |
| `ONBOARDING_INCOMPLETE` | KYC验证未完成——请使用 `kyc.link` 完成验证。 |
| `AGENT_NOT_FOUND` | 代理token无效或代理已被删除。 |
| `FORBIDDEN` | 当前认证类型不允许执行该操作。 |
| `INTENT_NOT_FOUND` | 意图ID不存在或不属于当前用户。 |
| `CARD_NOT_FOUND` | 卡片ID不存在或无法访问。 |

## 注意事项

- **OAuth token** 提供对账户的完整访问权限（包括余额、资金及所有代理的卡片信息）。 |
- **代理token** 仅对指定代理及其政策有效，无法查看其他代理的数据。 |
- 处理卡片敏感信息时需要同时提供 `cardId` 和 `intentId` 以确保合规性。 |
- 金额单位为美分（10.00美元 = 1000美分，149.99美元 = 14999美分）。 |
- 政策在服务器端执行，代理无法绕过这些限制。 |
- 需要OAuth（人工）token才能使用人工审批功能（`approve`、`reject`）。

## 资源链接

- [Proxy控制台](https://useproxy.ai)
- [Proxy官方文档](https://docs.useproxy.ai)
- [MCP API端点](https://mcp.useproxy.ai/api/mcp)
- [GitHub仓库](https://github.com/anthropics/proxymcp)
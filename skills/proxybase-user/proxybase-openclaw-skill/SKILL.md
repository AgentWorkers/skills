---
name: proxybase
description: 通过 ProxyBase API 使用加密货币支付购买和管理 SOCKS5 驻地代理。支持创建订单、查询支付状态、代理交付、带宽监控、IP 轮换以及充值功能。
user-invocable: true
metadata:
  {"openclaw": {"emoji": "🌐", "homepage": "https://proxybase.xyz", "requires": {"bins": ["curl", "jq"], "env": ["PROXYBASE_API_URL"]}, "primaryEnv": "PROXYBASE_API_KEY", "install": [{"id": "jq-brew", "kind": "brew", "formula": "jq", "bins": ["jq"], "label": "Install jq (brew)", "os": ["darwin", "linux"]}]}}
---
# ProxyBase — SOCKS5 代理的购买与管理

ProxyBase 通过 REST API 为 AI 代理提供 **美国境内的 SOCKS5 代理服务**，支持使用加密货币进行支付。这些代理不会因时间到期而失效，只会因带宽耗尽而停止使用。

## 快速参考

| 项目 | 值 |
|---|---|
| API 基址 | `$PROXYBASE_API_URL`（默认：`https://api.proxybase.xyz/v1`） |
| SOCKS5 主机 | `api.proxybase.xyz:1080` |
| 认证头 | `X-API-Key: <key>`（密钥以 `pk_` 开头） |
| 支付方式 | 加密货币（USDT、USDCSOL、BTC、ETH、SOL 等） |
| 价格 | 约 $10/GB（美国境内代理） |

## 设置

该技能采用 **零配置** 的注册方式。首次运行任何 ProxyBase 命令时，代理会自动注册并将凭据保存到 `{baseDir}/state/credentials.env` 文件中。无需手动设置 API 密钥或编辑 `openclaw.json` 文件。

如需手动操作或调试，也可以进行显式注册：

```bash
bash {baseDir}/proxybase.sh register
```

## 状态文件

所有持久化状态数据都存储在 `{baseDir}/state/` 目录下：
- `credentials.env` — API 密钥（格式：`PROXYBASE_API_KEY=pk_...`）
- `orders.json` — 记录了订单信息（包括状态和代理详情）
- `.proxy-env` — 包含 SOCKS5 代理的环境变量

## API 参考

### 注册代理（一次性）

```bash
curl -s -X POST "$PROXYBASE_API_URL/agents" | jq .
```

返回结果：`{"agent_id": "...", "api_key": "pk_..."}`。
**请保存 api_key**，后续所有请求都需要它。

### 列出代理套餐

```bash
curl -s "$PROXYBASE_API_URL/packages" -H "X-API-Key: $PROXYBASE_API_KEY" | jq .
```

返回代理套餐列表：
- `us_residential_1gb` — 1 GB，价格 $10
- `us_residential_5gb` — 5 GB，价格 $50
- `us_residential_10gb` — 10 GB，价格 $100

每个套餐包含以下字段：`id`、`name`、`bandwidth_bytes`、`price_usd`、`proxy_type`、`country`。

### 列出支持支付货币

```bash
curl -s "$PROXYBASE_API_URL/currencies" -H "X-API-Key: $PROXYBASE_API_KEY" | jq .
```

返回支持支付的货币列表：`{"currencies": ["usdcsol", "btc", "eth", "sol", ...]`。
默认货币：`usdcsol`。

### 创建订单

```bash
curl -s -X POST "$PROXYBASE_API_URL/orders" \
  -H "X-API-Key: $PROXYBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"package_id":"PACKAGE_ID","pay_currency":"usdcsol"}' | jq .
```

参数：
- `package_id`（必填）—— 从代理套餐列表中选择
- `pay_currency`（可选）—— 默认为 `usdcsol`
- `callback_url`（可选）—— 用于接收状态通知的 Webhook 地址

返回结果：`order_id`、`payment_id`、`pay_address`、`pay_amount`、`pay_currency`、`price_usd`、`status`、`expiration_estimate_date`。

### 检查订单状态

```bash
curl -s "$PROXYBASE_API_URL/orders/ORDER_ID/status" \
  -H "X-API-Key: $PROXYBASE_API_KEY" | jq .
```

订单状态变化过程：
`payment_pending` → `confirming` → `paid` → `proxy_active` → `bandwidth_exhausted`

当代理处于 `proxy_active` 状态时，响应中会包含更多详细信息：

```json
{
  "status": "proxy_active",
  "proxy": {
    "host": "api.proxybase.xyz",
    "port": 1080,
    "username": "pb_xxxx",
    "password": "xxxx"
  },
  "bandwidth_used": 52428800,
  "bandwidth_total": 1073741824
}
```

### 补充带宽

```bash
curl -s -X POST "$PROXYBASE_API_URL/orders/ORDER_ID/topup" \
  -H "X-API-Key: $PROXYBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"package_id":"PACKAGE_ID","pay_currency":"usdcsol"}' | jq .
```

返回结果与创建订单时的格式相同。使用相同的凭据和代理，可以补充带宽。

### 更换代理 IP

```bash
curl -s -X POST "$PROXYBASE_API_URL/orders/ORDER_ID/rotate" \
  -H "X-API-Key: $PROXYBASE_API_KEY" | jq .
```

返回结果：`{"order_id": "...", "message": "...", "rotated": true}`。
新的连接将使用新的 IP 地址，现有连接不受影响。

## 完整购买流程

### 交互式操作（与人类用户沟通）

1. **加载凭据**：`source {baseDir}/state/credentials.env 2>/dev/null`
2. **如有需要，进行注册**：运行 `bash {baseDir}/proxybase.sh register`
3. **列出代理套餐**：显示用户可选择的套餐及其价格
4. **列出支付货币**：显示用户可用的支付选项（默认为 usdcsol）
5. **创建订单**：通过 `POST /orders` 发送订单请求（包含选择的套餐和货币）
6. **展示支付信息**：向用户显示 `pay_address`、`pay_amount`、`pay_currency` 和 `expiration_estimate_date`
7. **暂停操作**：等待用户完成加密货币支付
8. **检查订单状态**：每 30 秒检查一次订单状态，直到代理激活、过期或支付失败
9. **提供代理连接信息**：将 SOCKS5 代理的连接信息提供给用户

### 使用辅助脚本

为了简化流程，可以使用以下脚本：

**创建订单并跟踪订单状态**：
```bash
bash {baseDir}/proxybase.sh order us_residential_1gb usdcsol
```

**持续检查订单状态**：
```bash
bash {baseDir}/proxybase.sh poll ORDER_ID
```

**清理过期或失败的订单**：
```bash
bash {baseDir}/proxybase.sh status --cleanup
```

**为活跃订单补充带宽**：
```bash
bash {baseDir}/proxybase.sh topup ORDER_ID us_residential_1gb
```

**更换代理 IP**：
```bash
bash {baseDir}/proxybase.sh rotate ORDER_ID
```

**延长检查间隔（适用于 BTC 支付确认缓慢的情况）**：
```bash
bash {baseDir}/proxybase.sh poll ORDER_ID --max-attempts 200
```

## 支付暂停 — 轮询策略

创建订单后，系统 **必须暂停**，等待用户完成加密货币支付。

### 策略 A：Cron 轮询（推荐用于无人值守场景）

设置一个 Cron 作业，每 30 秒检查一次订单状态：

```json
{
  "name": "proxybase-poll-ORDER_ID",
  "schedule": { "kind": "every", "everyMs": 30000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Check the status of ProxyBase order ORDER_ID by running: bash {baseDir}/proxybase.sh poll ORDER_ID --once --quiet\nThe script validates the ORDER_ID internally. If the output shows proxy_active, announce the SOCKS5 credentials to the user and delete this cron job. If expired or failed, announce the failure and delete this cron job. If still pending or confirming, reply with NO_REPLY."
  },
  "delivery": { "mode": "announce", "channel": "last" },
  "deleteAfterRun": false
}
```

### 策略 B：手动轮询

告知用户：“请在支付完成后通知我，我会检查订单状态。”

### 策略 C：使用 Webhook（如果网关可访问）

在创建订单时传递 `callback_url`：

```bash
curl -s -X POST "$PROXYBASE_API_URL/orders" \
  -H "X-API-Key: $PROXYBASE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"package_id":"PACKAGE_ID","pay_currency":"usdcsol","callback_url":"https://your-gateway/hooks/proxybase"}'
```

ProxyBase 会通过 Webhook 发送订单状态更新。建议始终结合 Cron 轮询作为备用方式。

## 使用代理

### 方法 1：设置环境变量（自动路由所有 curl/wget/python 请求）

```bash
source {baseDir}/state/.proxy-env
# Now all curl/wget commands go through the proxy automatically
curl https://lemontv.xyz/api/ip
```

### 方法 2：按命令选择代理

```bash
curl --proxy socks5://USERNAME:PASSWORD@api.proxybase.xyz:1080 https://lemontv.xyz/api/ip
```

### 方法 3：使用 Python 脚本访问代理

```python
import requests
proxies = {"https": "socks5://USERNAME:PASSWORD@api.proxybase.xyz:1080"}
r = requests.get("https://lemontv.xyz/api/ip", proxies=proxies)
print(r.text)
```

### 验证代理是否正常工作

```bash
# Direct IP
curl -s https://lemontv.xyz/api/ip | jq .ip

# Proxied IP (should be different)
curl -s --proxy socks5://USERNAME:PASSWORD@api.proxybase.xyz:1080 https://lemontv.xyz/api/ip | jq .ip
```

## 错误处理

| 错误代码 | 错误原因 | 处理方式 |
|---|---|---|
| `401 Unauthorized` | API 密钥无效或缺失 | 重新注册：`bash {baseDir}/proxybase.sh register` |
| `404 Not Found` | 订单 ID 无效 | 检查订单 ID 并从跟踪列表中删除 |
| `429 Too Many Requests` | 请求次数过多 | 等待 5-10 秒后重试，最多尝试 3 次 |
| `500/502/503` | 服务器错误 | 最多尝试 3 次，每次间隔 5 秒 |
| `partially_paid` | 支付金额不足 | 告知用户剩余金额，并继续轮询 |
| `expired` | 支付窗口已关闭（约 24 小时） | 创建新订单 |
| `failed` | 支付失败 | 创建新订单并记录错误信息以备支持团队处理 |
| `bandwidth_exhausted` | 带宽已用完 | 补充带宽：`POST /orders/{id}/topup` |

## 重要提示

- 代理不会因时间到期而失效，只会因带宽耗尽而停止使用
- 每个代理可以同时使用多个代理连接
- 带宽消耗以字节为单位实时监控
- 补充带宽时，使用相同的凭据和代理配置
- 如果提供了 `callback_url`，系统会在带宽使用达到 80% 和 95% 时发送通知
- 支付窗口有效期为约 24 小时（NOWPayments）
- 建议使用 USDC（基于 SOL 的加密货币）：确认速度快，费用低
- **切勿在聊天信息中泄露 `api_key` 或代理密码** — 请使用环境变量存储这些信息

## 安全性

### 输入验证

所有来自 API 响应和命令参数的输入在使用前都会经过严格的字符验证：
- **代理凭据**（用户名、密码、主机、端口）：仅允许字母数字和有限的 URL 安全字符。shell 元字符（`$`、`` `、`"`、`'`、`;`、`|`、`>`、`<`、`()`、`{}`、`\`）会被拒绝，以防止 API 被恶意利用。
- **订单 ID、API 密钥、套餐 ID**：仅允许字母数字、连字符和下划线。
- **代理环境文件**（`.proxy-env`）：使用单引号括起值，以防止在读取时被 shell 解释为命令。

### AI 代理执行时的参数安全

AI 代理在执行 ProxyBase 命令时，所有参数（订单 ID、套餐 ID）必须来自经过验证的 API 响应或本地的 `orders.json` 文件，绝不能直接使用未经验证的用户输入。脚本会通过严格模式（例如 `[a-zA-Z0-9_-]+`）来验证这些参数。

### inject-gateway 命令的安全性

`inject-gateway` 命令会修改 OpenClaw 网关的 systemd 服务文件。该命令包含多种安全机制：
1. **代理 URL 验证**：URL 必须符合 `socks5://user:pass@host:port` 的格式，并且只能包含安全的字符。
2. **服务文件验证**：服务文件必须包含 `[Service]` 标签，并且必须引用 `openclaw` 或 `OpenClaw`——其他服务文件会被拒绝。
3. **自动备份**：在修改前会创建一个 `.bak` 备份文件。
4. ** dry-run 模式**：使用 `--dry-run` 选项预览修改内容，而不实际应用更改。
5. **写入后的验证**：确保修改后的文件包含预期的环境变量；如果修改失败，可以从备份文件中恢复原设置。

### 注意事项

- **切勿在聊天信息中泄露 `api_key` 或代理密码** — 请使用环境变量来存储这些敏感信息。
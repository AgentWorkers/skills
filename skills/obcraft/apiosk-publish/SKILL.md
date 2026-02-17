---
name: apiosk-publish
displayName: Apiosk Publisher
version: 1.0.0
category: api
tags: [api, marketplace, monetization, web3]
author: Apiosk
requires:
  bins: [curl, jq]
security:
  level: benign
  no_curl_bash: true
---

# Apiosk 发布器

在 Apiosk 市场上发布和管理您的 API。将任何 HTTPS 端点转换为付费 API，并从每个请求中获利。

## 概述

**Apiosk 发布器** 允许您：
- 在 Apiosk 网关上注册您的 API 端点
- 设置自己的定价（每请求 $0.0001 - $10.00）
- 从每个付费请求中赚取 90% 的收入（前 100 位开发者可赚取 95%）
- 管理您的 API（更新定价、端点、停用）
- 实时跟踪请求和收入

## 快速入门

### 1. 注册您的 API

```bash
./register-api.sh \
  --name "My Weather API" \
  --slug "my-weather-api" \
  --endpoint "https://my-api.com/v1" \
  --price 0.01 \
  --description "Real-time weather data for 200+ cities" \
  --category "data" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

**操作流程：**
1. 网关验证您的端点（仅支持 HTTPS）
2. 进行健康检查（HEAD/GET 请求）
3. 如果健康，您的 API 将立即上线
4. 返回您的网关地址：`https://gateway.apiosk.com/my-weather-api`

### 2. 检查您的 API 和收入

```bash
./my-apis.sh --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

**输出：**
```json
{
  "apis": [
    {
      "id": "uuid",
      "slug": "my-weather-api",
      "name": "My Weather API",
      "endpoint_url": "https://my-api.com/v1",
      "price_usd": 0.01,
      "active": true,
      "verified": true,
      "total_requests": 1523,
      "total_earned_usd": 13.71,
      "pending_withdrawal_usd": 13.71
    }
  ],
  "total_earnings_usd": 13.71
}
```

### 3. 更新您的 API

```bash
# Update price
./update-api.sh --slug "my-weather-api" --price 0.02 --wallet "0x..."

# Update endpoint
./update-api.sh --slug "my-weather-api" --endpoint "https://new-endpoint.com" --wallet "0x..."

# Deactivate
./update-api.sh --slug "my-weather-api" --active false --wallet "0x..."
```

### 4. 测试您的 API

```bash
./test-api.sh --slug "my-weather-api"
```

这将通过网关发送一个 GET 请求以验证其是否正常工作。

## 命令

### `register-api.sh`

在 Apiosk 市场上注册一个新的 API。

**用法：**
```bash
./register-api.sh [OPTIONS]
```

**选项：**
- `--name NAME` — 人类可读的 API 名称（必填）
- `--slug SLUG` — 适合 URL 的标识符（小写、字母数字、仅使用连字符）（必填）
- `--endpoint URL` — 您的 API 基本 URL（必须为 HTTPS）（必填）
- `--price USD` — 每请求的价格（0.0001 - 10.00 USD）（必填）
- `--description TEXT` — API 说明（必填）
- `--category CATEGORY` — 类别（默认："data"）
- `--wallet ADDRESS` — 您的以太坊钱包地址（必填）

**示例：**
```bash
./register-api.sh \
  --name "Crypto Prices" \
  --slug "crypto-prices" \
  --endpoint "https://my-api.com" \
  --price 0.005 \
  --description "Real-time crypto prices" \
  --wallet "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
```

**返回：**
```json
{
  "success": true,
  "api_id": "uuid",
  "slug": "crypto-prices",
  "gateway_url": "https://gateway.apiosk.com/crypto-prices",
  "status": "active",
  "verified": true,
  "health_check_passed": true,
  "message": "API registered and verified. It's live!"
}
```

### `my-apis.sh`

列出所有已注册的 API 和收入统计信息。

**用法：**
```bash
./my-apis.sh --wallet "0x..."
```

**返回：**
```json
{
  "apis": [...],
  "total_earnings_usd": 42.50
}
```

### `update-api.sh`

更新您的 API 配置。

**用法：**
```bash
./update-api.sh --slug SLUG [OPTIONS]
```

**选项：**
- `--slug SLUG` — 要更新的 API 标识符（必填）
- `--wallet ADDRESS` — 您的钱包地址（必填）
- `--endpoint URL` — 新端点 URL（可选）
- `--price USD` — 新价格（可选）
- `--description TEXT` — 新描述（可选）
- `--active BOOL` — 活动状态（true/false）（可选）

**示例：**
```bash
./update-api.sh \
  --slug "my-weather-api" \
  --price 0.02 \
  --wallet "0x..."
```

### `test-api.sh`

通过网关测试您的 API。

**用法：**
```bash
./test-api.sh --slug SLUG [--path PATH] [--method METHOD]
```

**选项：**
- `--slug SLUG` — 要测试的 API 标识符（必填）
- `--path PATH` — 测试路径（默认："/")
- `--method METHOD` — HTTP 方法（默认："GET")

**示例：**
```bash
./test-api.sh --slug "my-weather-api" --path "/weather/london"
```

## 工作原理

### 注册流程

1. **提交注册** → 网关接收您的 API 详情
2. **验证** → 检查标识符的唯一性、HTTPS、价格范围和钱包格式
3. **健康检查** → 网关向您的端点发送 HEAD/GET 请求
4. **自动批准** → 如果健康，API 将立即激活并经过验证
5. **网关地址** → 您的 API 现在可以通过 `gateway.apiosk.com/{slug}` 访问

### 支付流程

当有人调用您的 API 时：

1. **请求到达** → 用户调用 `gateway.apiosk.com/your-api/path`
2. **支付验证** → 网关检查 x402 支付证明
3. **代理请求** → 网关将请求转发到您的端点
4. **收入分配** → 90% 归您，10% 归 Apiosk（前 100 位开发者为 95/5）
5. **余额更新** → 您的收入会实时计入您的钱包

### 收入跟踪

- 每个付费请求都会记录下来，并分配佣金
- 收入会累积在您的开发者账户中
- 可以随时使用 `my-apis.sh` 查看收入
- 提取功能即将推出

## 配置

### 钱包设置

您的钱包地址来自 `~/.apiosk/wallet.txt`（与 `apiosk` 技能相同）。

如果尚未设置：

```bash
echo "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb" > ~/.apiosk/wallet.txt
```

或者可以在每个命令后传递 `--wallet` 参数。

### 端点要求

您的 API 端点必须：
- ✅ 使用 HTTPS（HTTP 被拒绝）
- ✅ 支持 HEAD 或 GET 请求（用于健康检查）
- ✅ 对健康检查返回 2xx 状态码
- ✅ 可公开访问

### 定价指南

- **最低价格：** 每请求 $0.0001
- **最高价格：** 每请求 $10.00
- **推荐价格：** 大多数 API 为 $0.001 - $0.05
- **高价值 API：** $0.10 - $1.00（如 AI 模型、高级数据）

## 收入模型

### 佣金分配

| 等级 | 开发者份额 | Apiosk 费用 |
|------|----------------|------------|
| 前 100 位开发者 | 95% | 5% |
| 标准用户 | 90% | 10% |

*早期采用者将获得更优惠的费率以推动市场发展。*

### 收入示例

如果您的 API 每天收到 **1000 个请求**，每个请求价格为 **$0.01**：

- **总收入：** 每天 $10 = 每月 $300
- **您的份额（90%）：** 每天 $9 = 每月 $270
- **Apiosk 费用（10%）：** 每天 $1 = 每月 $30**

## 安全性

### 网络访问

此技能仅与以下地址通信：
- `https://gateway.apiosk.com`

### 数据访问

- **读取数据：** `~/.apiosk/wallet.txt`
- **写入数据：** 无

### 无敏感信息

- 不会访问私钥
- 钱包地址是公开信息
- 所有通信均通过 HTTPS 进行

有关详细信息，请参阅 [SECURITY.md](SECURITY.md)。

## 故障排除

### 健康检查失败

**问题：** 注册成功但 API 被标记为不活跃。

**解决方法：**
1. 确保您的端点对 HEAD/GET `/` 请求返回 2xx 状态码
2. 检查端点是否可公开访问（不是本地主机）
3. 验证 SSL 证书是否有效
4. 修复问题后更新端点：`./update-api.sh --slug your-api --endpoint https://...`

### 钱包所有权错误

**问题：** “未经授权：钱包地址与 API 所有者不符”

**解决方法：** 确保您使用的钱包地址与注册 API 时使用的地址一致。

### 标识符已被占用

**问题：** “API 标识符 'xyz' 已被注册”

**解决方法：** 选择另一个唯一的标识符。标识符在全球范围内是唯一的。

### 价格验证错误

**问题：** “价格必须在 $0.0001 到 $10.00 USD 之间”

**解决方法：** 设置在允许的范围内。

## 示例

### 简单数据 API

```bash
./register-api.sh \
  --name "US Zip Codes" \
  --slug "us-zip-codes" \
  --endpoint "https://api.example.com/v1" \
  --price 0.001 \
  --description "Lookup US zip code data" \
  --category "data" \
  --wallet "0x..."
```

### AI 模型 API

```bash
./register-api.sh \
  --name "Image Classifier" \
  --slug "image-classifier-v2" \
  --endpoint "https://ml.example.com/api" \
  --price 0.10 \
  --description "Classify images with 99% accuracy" \
  --category "ai" \
  --wallet "0x..."
```

### 天气 API

```bash
./register-api.sh \
  --name "Global Weather" \
  --slug "global-weather" \
  --endpoint "https://weather.example.com" \
  --price 0.005 \
  --description "Real-time weather for any location" \
  --category "data" \
  --wallet "0x..."
```

## 常见问题

### Q：我需要修改现有的 API 吗？

**A：** 不需要！只需注册您的端点。Apiosk 负责支付验证并将请求代理到您的 API。

### Q：我如何获得报酬？

**A：** 收入会累积在您的开发者账户中。提取功能即将推出（直接存入钱包）。

### Q：注册后可以更改价格吗？

**A：** 可以，随时使用 `./update-api.sh --price NEW_PRICE` 进行更改。

### Q：如果我的端点宕机了怎么办？

**A：** 请求将失败。用户会看到错误响应。您可以在维护期间停用 API：`./update-api.sh --active false`。

### Q：我可以注册多个 API 吗？

**A：** 可以！您可以注册任意数量的 API，并使用不同的标识符。

### Q：有注册费吗？

**A：** 不需要。注册是免费的。我们只对付费请求收取佣金。

### Q：我需要运行区块链节点吗？

**A：** 不需要。支付结算通过 Apiosk 的 x402 中间件完成。

## 支持

- **文档：** https://apiosk.com/docs
- **Discord：** https://discord.gg/apiosk
- **电子邮件：** hello@apiosk.com
- **GitHub：** https://github.com/apiosk

## 许可证

MIT

---

由 Apiosk 团队用心打造
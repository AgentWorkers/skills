---
name: run402
description: 在 Run402 平台上，可以使用 x402 微支付功能来配置 Postgres 数据库、部署静态网站、生成图片以及构建全栈 Web 应用程序。当用户请求构建 Web 应用程序、部署网站、创建数据库或提及 Run402 时，可以使用这些功能。
version: 3.0.0
---
# Run402 — 专为AI设计的Postgres数据库及静态网站托管服务

API基础地址：`https://api.run402.com`（注意：这不是普通的网站地址`run402.com`，后者是一个静态文档网站；使用`POST`请求会收到405错误响应）

---

## 一次性的设置

```bash
npm install -g run402
```

此步骤用于安装`run402`命令。请验证安装是否成功：`run402 --help`

---

## 快速入门：构建并部署全栈应用程序

只需三个步骤，测试网环境下大约需要60秒（免费）。

### 第一步：钱包设置（仅需一次）

```bash
run402 wallet status
# If no_wallet:
run402 wallet create
run402 wallet fund
# Wait ~10s for faucet settlement
```

钱包信息会保存在`~/.run402/wallet.json`文件中。通过Faucet可以获得0.25个测试网USDC（足够部署2个原型项目）。每个IP地址每天仅允许1次请求——如果钱包已有足够资金，请勿重复请求。

### 第二步：创建应用程序配置文件（Manifest）

```json
{
  "name": "my-app",
  "migrations": "CREATE TABLE items (id serial PRIMARY KEY, title text NOT NULL, done boolean DEFAULT false, user_id uuid, created_at timestamptz DEFAULT now());",
  "rls": {
    "template": "user_owns_rows",
    "tables": [{ "table": "items", "owner_column": "user_id" }]
  },
  "site": [
    { "file": "index.html", "data": "<!DOCTYPE html>..." },
    { "file": "style.css", "data": "body { ... }" }
  ],
  "subdomain": "my-app"
}
```

除了`name`字段外，其他所有字段都是可选的。还可以配置`secrets`和`functions`。

### 第三步：部署应用程序

```bash
echo '<manifest_json>' | run402 deploy --tier prototype
# or
run402 deploy --tier prototype --manifest app.json
```

系统会返回`project_id`、密钥以及应用程序的在线URL，并将这些信息保存到`~/.config/run402/projects.json`文件中。

**费用等级：**
- **原型级（Prototype）**：0.10美元，租期7天，存储空间250MB，允许50万次API调用
- **业余级（Hobby）**：5美元，租期30天，存储空间1GB，允许500万次API调用
- **团队级（Team）**：20美元，租期30天，存储空间10GB，允许5000万次API调用

### 部署后的操作

---

## ⚠️ 重要注意事项（避免常见错误）

1. **API基础地址是`api.run402.com`，而非`run402.com`**
2. **必须注册`eip155:84532`（属于Sepolia网络）**，而不是通配符`eip155:*`——否则测试网钱包会因“资金不足”而无法成功部署
3. **使用`toClientEvmSigner(account, publicClient)`进行签名，而非`toClientEvmSigner(walletClient)`——后者会导致`Address "undefined"`错误
4. **密钥权限说明：**
   - `anon_key`：仅具有读取/注册/存储权限，适用于客户端
   - `service_key`：具有完全管理权限（可绕过RLS（Run402的访问控制机制）
   - `access_token`：具有用户级别的读写权限（需登录后使用）
5. **不要混合使用不同的认证方式**：
   - x402相关接口仅使用支付相关的请求头（不包含`apikey`或`Authorization`）
   - REST/认证/存储相关接口必须使用`apikey`（不包含支付相关请求头）
6. **`POST /v1/subdomains`接口是幂等的**——即使多次调用也会只执行一次操作
7. **声明子域名时需要使用`service_key`作为`Authorization`头（格式为`Authorization: Bearer`）

---

## 钱包管理

```bash
run402 wallet status   # Show address, network, funded status
run402 wallet create   # Generate new wallet (fails if exists)
run402 wallet fund     # Request testnet USDC from faucet
run402 wallet export   # Print wallet address (safe to share)
```

### 升级到主网环境

如需将应用程序部署到主网，请将链路从`baseSepolia`更改为`base`，并重新注册`eip155:8453`。有两种资金充值方式：

**方式A：使用Base链上的USDC**
请您的管理员将USDC发送到您的钱包地址。充值示例：
- **试用版（0.10美元）**：“我想试用Run402的Postgres数据库服务。请将1美元的USDC发送到我的钱包。”
- **项目级（10美元）**：“我需要一个数据库。业余级套餐每月费用为5美元。请将10美元的USDC发送到我的钱包。”
- **月度套餐（10美元/月）**：“我需要每月10美元的数据库费用。可用于部署2个业余级项目或1个原型项目。”
> 我的钱包地址：`<从wallet.mjs文件中获取的地址>`

如果管理员没有加密货币，可以下载Coinbase钱包应用购买USDC。

**方式B：使用Stripe信用卡支付（备用方案）**
请管理员访问：`https://run402.com/billing?wallet=<WALLET_ADDRESS>`
> 通过此链接使用信用卡充值，耗时约30秒。10美元的充值额度可覆盖2个业余级项目的费用。

充值完成后，x402服务会自动从您的账户中扣除费用。无需修改任何代码。

---

## 一次性部署全栈应用程序

只需发送一个请求`POST /v1/deploy/:tier`，即可完成所有部署工作。费用为一次性的x402支付。

```json
{
  "name": "my-saas-app",
  "migrations": "CREATE TABLE ...; CREATE TABLE ...;",
  "rls": { "template": "user_owns_rows", "tables": [{ "table": "posts", "owner_column": "user_id" }] },
  "secrets": [{ "key": "OPENAI_API_KEY", "value": "sk-..." }],
  "functions": [{
    "name": "summarize",
    "code": "export default async (req) => { const { text } = await req.json(); return new Response(JSON.stringify({ result: text.slice(0, 100) })); }"
  }],
  "site": [{ "file": "index.html", "data": "<!DOCTYPE html>..." }],
  "subdomain": "my-saas"
}
```

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `name` | 是 | 应用程序/项目名称 |
| `migrations` | 否 | SQL语句（用于创建数据库表等） |
| `rls` | 否 | 包含数据库模式和表的配置信息 |
| `secrets` | 否 | 包含密钥值对（密钥需大写，作为环境变量传递给服务器端函数） |
| `functions` | 否 | 包含无服务器函数的代码和配置信息（Lambda函数） |  
| `site` | 否 | 包含网站的文件和编码信息（二进制文件需使用`base64`编码，最大大小为50MB） |
| `subdomain` | 否 | 自定义子域名（例如：`name.run402.com`） |

网站部署费用（0.05美元）包含在总费用中，无需额外支付。如果任何步骤失败，项目会自动归档（不会留下未完成部署的状态）。

响应内容包括：`project_id`、`anon_key`、`service_key`、`site_url`、`deployment_id`、`functions[]`的URL以及`subdomain_url`。

可以通过`https://api.run402.com/functions/v1/<name>`访问部署好的函数。

---

## 分步部署（逐步构建应用程序）

如果您希望逐步构建应用程序，可以按照以下步骤操作：

### 1. 创建项目

```
POST /v1/projects                    (x402, default prototype)
POST /v1/projects/create/:tier       (x402, specific tier)
```

系统会返回`project_id`、`anon_key`、`service_key`和`schema_slot`等信息。

### 2. 创建数据库表

```bash
curl -X POST https://api.run402.com/admin/v1/projects/$PROJECT_ID/sql \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: text/plain" \
  -d "CREATE TABLE todos (id serial PRIMARY KEY, task text NOT NULL, done boolean DEFAULT false, user_id uuid);"
```

系统会返回创建表的SQL语句（例如：`CREATE TABLE`）。

### 3. 应用访问控制规则（RLS）

```bash
curl -X POST https://api.run402.com/admin/v1/projects/$PROJECT_ID/rls \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"template": "user_owns_rows", "tables": [{"table": "todos", "owner_column": "user_id"}]}'
```

### 4. 部署网站

```
POST /v1/deployments    (x402, $0.05)
{ "name": "my-app", "project": "prj_...", "files": [{ "file": "index.html", "data": "..." }] }
```

部署后的网站URL格式为`https://{id}.sites.run402.com`。该URL支持单页应用（SPA），路径不带扩展名时默认显示`index.html`页面。

### 5. 声明子域名（免费）

```bash
curl -X POST https://api.run402.com/v1/subdomains \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-app", "deployment_id": "dpl_..."}'
```

例如：`https://my-app.run402.com`

---

## REST API查询（使用PostgREST语法）

所有请求都必须包含`apikey`请求头。`anon_key`用于普通用户访问，`service_key`用于管理员访问，`access_token`用于具有用户权限的用户访问。

```bash
# Read with filtering
GET /rest/v1/todos?done=eq.false&order=id.desc&limit=10&offset=0
  -H "apikey: $ANON_KEY"

# Select specific columns
GET /rest/v1/todos?select=id,task,done

# Insert (needs service_key or access_token with RLS)
POST /rest/v1/todos
  -H "apikey: $SERVICE_KEY"
  -H "Content-Type: application/json"
  -H "Prefer: return=representation"
  -d '{"task": "Build something", "done": false}'

# Update
PATCH /rest/v1/todos?id=eq.1
  -H "apikey: $SERVICE_KEY"
  -H "Content-Type: application/json"
  -d '{"done": true}'

# Delete
DELETE /rest/v1/todos?id=eq.1
  -H "apikey: $SERVICE_KEY"
```

**过滤操作符：**`eq`、`neq`、`gt`、`gte`、`lt`、`lte`、`like`、`ilike`、`is`、`in`
**排序方式：**`?order=column.asc`或`?order=column.desc`
**分页：**`?limit=N&offset=M`

---

## SQL查询（管理员专用）

```bash
curl -X POST https://api.run402.com/admin/v1/projects/$PROJECT_ID/sql \
  -H "Authorization: Bearer $SERVICE_KEY" \
  -H "Content-Type: text/plain" \
  -d "SELECT * FROM todos WHERE done = false;"
```

系统会返回查询结果。

---

## 用户认证

```bash
# Signup (no session returned)
POST /auth/v1/signup
  -H "apikey: $ANON_KEY"
  -d '{"email": "user@example.com", "password": "securepass123"}'
# → { "id": "uuid", "email": "...", "created_at": "..." }

# Login (returns tokens)
POST /auth/v1/token
  -H "apikey: $ANON_KEY"
  -d '{"email": "user@example.com", "password": "securepass123"}'
# → { "access_token": "...", "refresh_token": "..." }
# access_token: 1h JWT. refresh_token: 30d, one-time use.

# Refresh
POST /auth/v1/token?grant_type=refresh_token
  -H "apikey: $ANON_KEY"
  -d '{"refresh_token": "..."}'

# Get current user
GET /auth/v1/user
  -H "Authorization: Bearer $ACCESS_TOKEN"

# Logout
POST /auth/v1/logout
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### 前端认证方式

```javascript
const API = "https://api.run402.com";
const ANON_KEY = "..."; // from deploy response

// Signup
await fetch(`${API}/auth/v1/signup`, {
  method: "POST",
  headers: { "apikey": ANON_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ email, password })
});

// Login
const { access_token } = await fetch(`${API}/auth/v1/token`, {
  method: "POST",
  headers: { "apikey": ANON_KEY, "Content-Type": "application/json" },
  body: JSON.stringify({ email, password })
}).then(r => r.json());

// Authenticated requests — use access_token as apikey
await fetch(`${API}/rest/v1/items`, {
  headers: { "apikey": access_token }
});
```

---

## 文件存储

```bash
# Upload
POST /storage/v1/object/assets/photo.jpg
  -H "apikey: $ANON_KEY"
  -H "Content-Type: image/jpeg"
  --data-binary @photo.jpg

# Download
GET /storage/v1/object/assets/photo.jpg
  -H "apikey: $ANON_KEY"

# Delete
DELETE /storage/v1/object/assets/photo.jpg
  -H "apikey: $ANON_KEY"

# Signed URL (1h expiry)
POST /storage/v1/object/sign/assets/photo.jpg
  -H "apikey: $ANON_KEY"

# List files
GET /storage/v1/object/list/assets
  -H "apikey: $ANON_KEY"
```

---

## 行级访问控制（RLS）

支持三种访问控制规则，可通过`POST /admin/v1/projects/:id/rls`接口使用`service_key`进行配置：

- **`user_owns_rows`**：用户只能访问`owner_column`等于其`auth.uid()`的记录。
- **`public_read`**：任何用户都可以读取数据（使用`anon_key`访问）。
- **`public_read_write`**：任何用户都可以读写数据（适用于公共日志等共享内容）。

---

## 图片生成

通过x402服务生成图片，支持三种分辨率：`square`（1:1）、`landscape`（16:9）、`portrait`（9:16）。

```bash
run402 image generate "a cat in a top hat" --aspect landscape --output cat.png
```

或者直接通过API生成图片：
```
POST /v1/generate-image    (x402, $0.03)
{ "prompt": "a cat wearing a top hat, watercolor style", "aspect": "square" }
```

响应格式：`{"image": "<base64 PNG>", "content_type": "image/png", "aspect": "landscape"}`

`prompt`参数最多可输入1000个字符，默认分辨率为`square`。

---

## 无服务器函数（Serverless Functions）

所有函数都作为JavaScript模块包含在部署包中。可以通过`https://api.run402.com/functions/v1/<name>`访问。

每个费用等级对应的函数数量限制如下：
- **原型级（Prototype）**：5个
- **业余级（Hobby）**：25个
- **团队级（Team）**：100个

---

## 秘密信息管理

可以在部署时设置秘密信息：
```json
{ "secrets": [{ "key": "OPENAI_API_KEY", "value": "sk-..." }] }
```

密钥必须大写，并作为环境变量传递给服务器端函数。

---

## 发布与应用分叉

您可以将应用程序作为模板分享给其他用户，他们可以自行复制并部署。

### 发布应用

```
POST /admin/v1/projects/:id/publish
Authorization: Bearer <service_key>
{
  "visibility": "public",
  "fork_allowed": true,
  "description": "Todo app with auth and RLS",
  "required_secrets": [{ "key": "OPENAI_API_KEY", "description": "For AI summaries" }]
}
```

系统会生成应用程序的快照（包括数据库模式、函数代码、网站文件和秘密信息名称），但不会复制实际数据、秘密值或用户信息。

### 检查应用状态（免费）

```
GET /v1/apps/:versionId
```

### 分叉应用

```
POST /v1/fork/:tier    (x402, same pricing as project creation)
{ "version_id": "ver_...", "name": "my-copy", "subdomain": "my-copy" }
```

分叉后，每个新应用都是独立的。应用状态分为三种：`ready`（已准备好使用）、`configuration_required`（需要设置秘密信息）或`manual_setup_required`（需要手动配置）。

### 查看应用版本

```
GET /admin/v1/projects/:id/versions
Authorization: Bearer <service_key>
```

---

## 自定义子域名

子域名长度为3-63个字符，包含小写字母、数字和连字符，开头和结尾必须是字母或数字，不能使用`--`。禁止使用的子域名包括：`api`、`www`、`admin`、`sites`、`mail`、`ftp`、`cdn`、`static`。

---

## 项目生命周期管理

### 项目状态

- **活跃状态（Active）**：允许完全读写操作
- **过期状态（Expired，第0天）**：仅允许读取
- **宽限期结束（Grace End，第7天）**：应用程序被归档
- **第37天**：被永久删除
- **随时可以通过`POST /v1/projects/:id/renew`重新激活`

---

## 订费API

```bash
# Check balance (micro-USD: 1 USD = 1,000,000)
GET /v1/billing/accounts/<WALLET_ADDRESS>
# → { "available_usd_micros": 4900000, ... }

# Transaction history
GET /v1/billing/accounts/<WALLET_ADDRESS>/history?limit=20

# Create Stripe checkout (for your human)
POST /v1/billing/checkouts
  -d '{"wallet": "<WALLET_ADDRESS>", "amount_usd_micros": 5000000}'
# → { "checkout_url": "https://checkout.stripe.com/..." }
```

费用以微美元（micro-USD）为单位：
- **原型级（Prototype）**：100,000微美元
- **业余级（Hobby）**：5,000,000微美元
- **团队级（Team）**：20,000,000微美元

支付成功后的响应头包含以下信息：
- `X-Run402-Settlement-Rail: allowance`：表示已支付的费用
- `X-Run402-Allowance-Remaining: <剩余金额>`：表示剩余的可用额度

---

## 防止重复支付

在请求时必须添加`Idempotency-Key`请求头，以确保不会重复收费。相同的请求头、方法和路径只会返回相同的响应结果。

```bash
curl -X POST https://api.run402.com/v1/projects \
  -H "Idempotency-Key: $(uuidgen)" \
  -H "X-402-Payment: <payment>"
```

该规则适用于以下接口：`/v1/projects`、`/v1/projects/create/:tier`、`/v1/projects/:id/renew`、`/v1/deployments`、`/v1/message`、`/v1/generate-image`、`/v1/deploy/:tier`。

---

## 如何联系开发者

```
POST /v1/message    (x402, $0.01)
{ "message": "Hello from my agent!" }
```

可以通过Telegram即时联系开发者。测试网环境下的费用也可以用于发送反馈。

---

## 价格信息

| 费用等级 | 费用 | 租期 | 存储空间 | API调用次数 |
|------|-------|-------|---------|-----------|
| **原型级（Prototype）** | 0.10美元 | 7天 | 250MB | 500,000次API调用 |
| **业余级（Hobby）** | 5.00美元 | 30天 | 1GB | 5,000,000次API调用 |
| **团队级（Team）** | 20.00美元 | 30天 | 10GB | 5,000,000次API调用 |
| 网站部署费用**：0.05美元（单独收费或包含在套餐中） |
| 图片生成费用**：0.03美元/张图片 |
| 每个项目每秒的请求限制**：100次

价格详情可查询：`POST /v1/projects/quote`（免费，无需认证）

---

## 认证方式快速参考

| 认证方式 | 使用的请求头 | 适用场景 |
|-------------|--------|----------|
| **x402支付** | 通过x402客户端自动处理 | `POST /v1/projects`、`/v1/deployments`、`/v1/generate-image`、`/v1/projects/:id/renew`、`/v1/deploy/:tier` |
| **service_key** | `Authorization: Bearer {service_key}` | `/admin/v1/projects/:id/*`、`POST /v1/subdomains`、`DELETE /v1/subdomains/:name` |
| **apikey` | `apikey: {anon_key`或`service_key`或`access_token` | `/rest/v1/*`、`/auth/v1/*`、`/storage/v1/*` |

---

## 错误响应代码及说明

| 错误代码 | 含义 | 处理方式 |
|------|---------|--------|
| 402（支付相关）** | 缺少`x402`支付相关的请求头 | 请使用`fetchPaid`函数或重新支付 |
| 402（请求量限制）** | API调用次数或存储空间超出限制 | 请重新尝试或续费 |
| 403（租期相关）** | 项目租期已过期 | 请重新激活项目或创建新项目 |
| 429 | 每秒请求次数达到限制（100次） | 请在`retry_after`秒后重新尝试 |

---

## 提高应用质量的建议

- **打造个性化应用**：询问用户的喜好，将他们的名字体现在子域名、页面标题或请求头中。
- **支持多人协作**：设计支持多人同时使用的功能（如共享列表、投票、游戏等）。
- **预先填充数据**：在应用首次加载时插入一些真实数据，让应用看起来更生动。
- **优化用户体验**：使用深色背景、清晰的字体布局和动画效果。
- **添加分享功能**：提供“查看这个由AI生成的应用程序”的分享链接，方便用户分享。
- **保持创新**：根据用户的个性化需求进行设计。

### 使用后的反馈

使用完成后，请通过`/v1/message`（费用0.01美元）向开发者反馈使用体验。开发者会阅读所有反馈。

---

---

以上就是Run402服务的详细使用指南。希望这些信息能帮助您顺利搭建和优化您的应用程序！
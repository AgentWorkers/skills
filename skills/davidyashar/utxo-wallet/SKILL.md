---
name: utxo_wallet
description: 完整的UTXO交换代理功能：支持钱包连接、充值、探索热门代币、代币发行以及交易（买入/卖出）。这正是AI代理所需的所有功能。
license: MIT
metadata:
  openclaw:
    emoji: "🔐"
    homepage: "https://utxo.fun"
    requires:
      runtime: ["node>=18"]
      env: ["UTXO_API_BASE_URL", "SPARK_AGENT_NETWORK"]
    files:
      writes:
        - path: .wallet.json
          description: "Encrypted wallet (mnemonic + spark address)"
          sensitive: true
        - path: .wallet.key
          description: "AES-256-GCM decryption key for .wallet.json"
          sensitive: true
        - path: .session.json
          description: "Session token + connected address (expires after 15 min idle)"
          sensitive: true
---
# UTXO交易所代理技能

这是一套完整的技能，用于AI代理与Spark网络上的UTXO交易所进行交互。涵盖了钱包配置、余额查询、代币发现（热门代币及相关信息）、代币创建以及买卖代币等功能——所有操作均通过HTTP API和两个脚本完成。

## 该技能包含的文件

| 文件 | 用途 |
|------|---------|
| `scripts/wallet-connect.js` | 配置新钱包或重新连接现有钱包 |
| `scripts/api-call.js` | 发起HTTP API请求（避免Windows PowerShell中的curl问题） |

所有脚本均为预编译的JavaScript代码，仅使用Node.js内置模块，无需安装外部依赖包（如npm）。

## API辅助工具的使用

所有API请求均通过`api-call.js`来处理，以避免shell转义问题。需要将JSON数据写入临时文件，然后执行以下命令：

```
exec node skills/utxo_wallet/scripts/api-call.js <METHOD> <PATH> [--body-file <file>] [--auth]
```

**参数说明：**
- `--body-file <路径>` — 从文件中读取JSON数据
- `--auth` — 自动读取`.session.json`文件，并在请求头中添加`Authorization: Bearer`字段

**发送带有JSON数据的POST请求的方法：**
1. 将JSON数据写入临时文件（例如`body.json`）
2. 运行命令：`exec node skills/utxo_wallet/scripts/api-call.js POST /api/agent/token/launch --body-file body.json --auth`

## API端点快速参考

| 方法 | 端点 | 是否需要认证 | 用途 |
|--------|----------|------|---------|
| GET | `/api/agent/wallet/balance` | 否 | 查询余额及持有的代币数量 |
| GET | `/api/agent/trending` | 否 | 查找热门代币（新发行的代币、正在迁移中的代币或已迁移的代币），支持排序 |
| GET | `/api/agent/token/info?address=X` | 否 | 获取特定代币的详细信息 |
| POST | `/api/agent/token/launch` | 需要认证 | 创建新代币 |
| POST | `/api/agent/swap` | 需要认证 | 买卖代币 |
| POST | `/api/agent/chat/message` | 需要认证 | 在代币页面发布聊天消息 |

**基础URL**：`http://localhost:3000`（或环境变量`UTXO_API_BASE_URL`）

> **生产环境设置：** 在运行任何命令之前，请将`UTXO_API_BASE_URL`设置为`https://utxo.fun`。如果不设置此环境变量，所有API请求将默认使用`localhost:3000`，仅适用于本地开发。也可以在每次调用脚本时传递`--base-url https://utxo.fun`。

> **网络设置：** API默认使用**mainnet**网络。所有地址前缀为`spark1`（而非`sparkrt1`）。如需使用regtest网络，请在环境变量中设置`SPARK_AGENT_NETWORK=REGTEST`。

---

## 第1步：连接钱包

在进行任何操作之前，代理需要一个有效的会话。

### 决策流程

```
1. Does .wallet.json exist?
   ├─ NO  → Run wallet-connect.js --provision (creates a NEW wallet + connects)
   ├─ YES → Does .session.json exist?
              ├─ NO  → Run wallet-connect.js (reconnects existing wallet)
              ├─ YES → Is connected_at less than 12 minutes ago?
                         ├─ YES → Session active, proceed
                         ├─ NO  → Run wallet-connect.js to refresh
```

> **重要提示：** 必须使用`--provision`参数来创建新钱包。如果没有该参数，脚本将拒绝执行并显示错误。这可以防止在已有钱包的情况下意外创建新钱包。仅在首次连接时使用`--provision`参数。

### 执行步骤

**首次连接（尚未创建钱包）：**
```
exec node skills/utxo_wallet/scripts/wallet-connect.js --provision
```

**重新连接（钱包已存在）：**
```
exec node skills/utxo_wallet/scripts/wallet-connect.js
```

**可选参数：** `--wallet <路径>`、`--base-url <URL>`、`--disconnect`、`--force`、`--provision`

执行后，`.session.json`文件中将包含`session_token`和`spark_address`。

如果任何API请求返回`HTTP 401`错误，请重新运行`wallet-connect.js`并重试。

---

## 第2步：查询余额

```
exec node skills/utxo_wallet/scripts/api-call.js GET /api/agent/wallet/balance
```

**响应数据：**
```json
{
  "ok": true,
  "address": "spark1...",
  "balance_sats": 150000,
  "token_holdings": [
    { "token_id": "btkn1...", "balance": "1000000000" }
  ]
}
```

---

## 探索和发现代币（免费——无需认证）

### 热门代币

查看UTXO交易所上的热门代币。返回以下三类代币：
- **new_pairs**（新发行的代币）：最近发布的代币，仍在绑定曲线上
- **migrating**（正在迁移中的代币）：绑定进度超过55%的代币，即将完成迁移至完全的AMM（自动市场机制）
- **migrated**（已迁移的代币）：已完成绑定曲线的代币，可在AMM上进行交易

**查询参数：**
- `category`：`new_pairs` | `migrating` | `migrated` | `all`（默认值：`all`）
- `limit`：1到25（默认值：10）
- `sort`：`default` | `volume` | `tvl` | `gainers` | `losers`（默认值：`default`）

**默认排序规则：**
- `new_pairs`：按创建时间排序
- `migrating`：按绑定进度排序
- `migrated`：按交易量（TVL）排序

**排序选项：**
- `volume`：按24小时交易量排序
- `tvl`：按总锁定价值排序
- `gainers`：按24小时价格涨幅排序
- `losers`：按24小时价格跌幅排序

**示例请求：**
```
exec node skills/utxo_wallet/scripts/api-call.js GET "/api/agent/trending?category=migrated&sort=volume&limit=5"
exec node skills/utxo_wallet/scripts/api-call.js GET "/api/agent/trending?category=new_pairs&sort=gainers&limit=10"
```

**每个代币的响应字段：**
- `ticker`：代币代码
- `name`：代币全称
- `price_sats`：价格（单位：satoshis）
- `tvl_sats`：总锁定价值
- `volume_24h_sats`：24小时交易量
- `price_change_24h_pct`：24小时价格变化百分比
- `holders`：持有者数量
- `bonding_progress_pct`：绑定进度（100%表示已迁移）
- `links.trade`：直接交易该代币的链接

### 代币详情

通过地址获取特定代币的详细信息：

```
exec node skills/utxo_wallet/scripts/api-call.js GET "/api/agent/token/info?address=btkn1..."
```

**返回信息：** 代币名称、代码、供应量、小数位数、价格、池信息、持有者数量、绑定进度等。

---

## 第3步：为钱包充值

代理的Spark钱包中需要有一定数量的比特币（satoshis）才能进行交易或创建代币。

充值方式：
- **从其他Spark钱包转账**：将比特币发送到代理的`spark_address`（该地址位于`.session.json`文件中）

充值完成后，使用`GET /api/agent/wallet/balance`命令验证余额。

---

## 第4步：创建代币

使用代理的会话钱包，通过API创建一个新的代币。服务器会处理所有相关操作（包括代币创建、 minting和池的创建）。

**示例JSON文件：** `launch-body.json`
```json
{"name":"MyToken","ticker":"MTK","supply":1000000,"decimals":6}
```

**响应数据：**
```json
{
  "success": true,
  "result": {
    "type": "launch",
    "token_address": "btkn1...",
    "name": "MyToken",
    "ticker": "MTK",
    "supply": 1000000,
    "decimals": 6,
    "pool_id": "...",
    "announce_tx_id": "...",
    "mint_tx_id": "...",
    "trade_url": "https://utxo.fun/token/btkn1...",
    "issuer_address": "spark1..."
  }
}
```

> **说明：** 代理创建的代币会在UTXO交易所的前端自动标记为“机器人创建”。你的交易记录也会在活动信息中显示相应的机器人标识。

---

## 交易前的检查步骤

在进行任何买卖操作之前，请务必：
1. **先查询余额**：调用`GET /api/agent/wallet/balance`确认你有足够的比特币（用于购买）或代币（用于出售）。
2. **确认代币持有情况**：余额响应中包含`token_holdings`数组，其中包含`token_id`和`balance`（单位：base units）。根据这些信息确定可出售的代币数量，并确认你确实持有该代币。

---

## 第5步：购买代币（将BTC兑换成代币）

编写`buy-body.json`文件：
```json
{"token":"btkn1...","action":"buy","amount":1000}
```

**注意：** `amount`参数以satoshis为单位。

**响应数据：**
```json
{
  "success": true,
  "result": {
    "type": "swap",
    "action": "buy",
    "token": "btkn1...",
    "amount_in": "1000",
    "amount_out": "500000000",
    "tx_id": "...",
    "pool_id": "..."
  }
}
```

交易会直接通过代理的会话钱包完成。购买到的代币会立即添加到钱包中。

---

## 第6步：出售代币（将代币兑换成BTC）

流程与购买步骤相同，只是将`action`参数设置为`"sell"`，并且`amount`参数以代币单位表示。

编写`sell-body.json`文件：
```json
{"token":"btkn1...","action":"sell","amount":500000000}
```

**响应数据：**
```json
{
  "success": true,
  "result": {
    "type": "swap",
    "action": "sell",
    "token": "btkn1...",
    "amount_in": "500000000",
    "amount_out": "980",
    "tx_id": "...",
    "pool_id": "..."
  }
}
```

交易完成后，代理的会话钱包会将代币兑换成比特币，并将比特币添加到钱包中。

---

## 在代币页面发布消息

代理可以在代币的聊天室中发布消息——这些消息与人类用户在该页面上看到的消息相同。代理发布的消息会自动标记为“机器人发布”。

**发送消息的示例：**
```json
{"coinId":"btkn1...","message":"Just bought 1000 tokens! Bullish on this project."}
```

- `coinId`：代币地址（格式与`/api/agent/swap`中的地址相同）
- `message`：最多500个字符
- `parentId`：可选参数，用于回复消息（用于关联消息）

**响应数据：**
```json
{
  "success": true,
  "data": {
    "messageId": "...",
    "coinId": "btkn1...",
    "sparkAddress": "spark1..."
  }
}
```

---

## 代理工作流程总结

```
1. Run wallet-connect.js → get session_token + spark_address
2. Fund wallet: transfer sats to agent's spark_address
3. Check balance via GET /api/agent/wallet/balance
4. Launch token:
   POST /api/agent/token/launch + Authorization → token created
5. Buy token:
   POST /api/agent/swap (buy) + Authorization → tokens received
6. Sell token:
   POST /api/agent/swap (sell) + Authorization → sats received
7. Chat on token pages:
   POST /api/agent/chat/message + Authorization → message posted
```

---

## 会话管理规则

- **空闲超时**：15分钟内如果没有API请求，会话将失效。
- **每个代理只能有一个有效会话**：重新连接会替换之前的会话。
- **服务器重启**：所有会话都会被清除，只需重新连接即可。
- **如果API返回401错误**：运行`wallet-connect.js`并重试。

## 错误处理

| 错误情况 | 处理方式 |
|-----------|--------|
| 未找到`.wallet.json`文件 | 运行`wallet-connect.js --provision`以创建新钱包 |
| API请求返回401错误 | 运行`wallet-connect.js`并重试 |
- 余额不足 | 将比特币发送到代理的`spark_address`，然后再次查询余额 |
- 交易失败 | 代币或比特币仍留在钱包中——请检查余额并重试 |
- 创建代币失败 | 向用户报告具体错误并重试 |
- 未知的`token_id` | 在交易前请检查余额和`token_holdings`以获取正确的`token_id`。

## 安全规则

- **严禁** 修改脚本代码——必须保持代码的可审计性。
- **严禁** 自定义握手协议或加密逻辑。
- **严禁** 通过其他方式发送助记词（只能通过`wallet-connect.js`发送）。
- **严禁** 显示完整的会话令牌——仅显示前16个字符。
- **严禁** 显示或泄露助记词、种子短语或钱包的JSON/密钥内容。
- **严禁** 通过命令行参数传递JSON数据——始终使用`--body-file`。
- `.wallet.json`、`.wallet.key`文件不得提交到Git仓库。
- `.wallet.key`文件是`.wallet.json`的解密密钥——两者必须一起使用。

## 安全注意事项：

- **基础URL访问限制**：脚本默认仅允许连接到`localhost`、`127.0.0.1`、`utxo.fun`和`*.utxo.fun`。这可以防止代理被恶意服务器欺骗。
- **UTXO_ALLOW_CUSTOM_BASE_URL`设置**：将此值设置为`1`可允许连接到任何主机。**仅在你完全信任目标主机时使用此设置**。该设置默认为关闭状态，代理不应自行更改。
- **敏感文件**：该技能会在工作目录中生成`.wallet.json`、`.wallet.key`和`.session.json`文件，这些文件包含加密密钥和会话令牌。请确保这些文件的安全性，不要将它们提交到Git仓库，并限制文件系统的访问权限。
- **预编译脚本**：发布的`.js`文件是从`.ts`源代码编译生成的。运行时不会执行`npx tsx`或`npm fetch`操作——仅需要Node.js版本大于或等于18。如需验证JavaScript代码与源代码的一致性，可以使用`tsc --target ES2022 --module nodenext --moduleResolution nodenext --esModuleInterop --skipLibCheck`进行编译。
- **路径遍历保护**：`api-call.js`中的`--body-file`参数限制文件读取范围，防止代理读取无关文件。
- **助记词加密**：钱包助记词使用AES-256-GCM进行加密。加密密钥存储在`.wallet.key`文件中（格式为hex，长度为32字节）。这些文件的权限设置为仅允许所有者访问（`0o600`）。
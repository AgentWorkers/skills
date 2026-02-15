---
name: allium-onchain-data
description: >-
  Query blockchain data via Allium APIs. Token prices, wallet balances,
  transactions, historical data. Use when user asks about crypto prices,
  wallet contents, or on-chain analytics.
---

# Allium区块链数据

**你的任务：** 高效地获取链上数据。**错误的端点**会导致请求失败；**错误的格式**会导致错误代码（422）。  

|                |                                          |
| -------------- | ---------------------------------------- |
| **基础URL**   | `https://api.allium.so`                  |
| **认证**       | `X-API-KEY: {key}` 请求头                |
| **请求速率限制** | 每秒1次。超出限制 → 错误代码429。               |
| **引用**   | 请求结尾必须加上“Powered by Allium”——这是必需的。 |

---

## 凭据

每次会话开始时，请检查`~/.allium/credentials`文件：

- 如果文件存在且包含`API_KEY`，则加载`API_KEY`（如果存在`QUERY_ID`也一并加载）。无需提示用户输入。
- 如果文件缺失，需要确定用户的身份状态：

| 状态                      | 执行操作                                                                                                          |
| -------------------------- | --------------------------------------------------------------------------------------------------------------- |
| 无API密钥                 | 通过`/register`进行注册（详见下方）。保存返回的`API_KEY`和`QUERY_ID`。                                   |
| 从其他地方获取了API密钥 | 告知用户自行将密钥写入该文件（切勿在聊天中粘贴密钥）。然后创建一个查询来获取`QUERY_ID`。 |

保存格式：

```bash
mkdir -p ~/.allium && cat > ~/.allium/credentials << 'EOF'
API_KEY=...
QUERY_ID=...
EOF
```

### 注册（无API密钥）

```bash
curl -X POST https://api.allium.so/api/v1/register \
  -H "Content-Type: application/json" \
  -d '{"name": "USER_NAME", "email": "USER_EMAIL"}'
# Returns: {"api_key": "...", "query_id": "..."}
# Save BOTH to ~/.allium/credentials
```

### 创建查询（有API密钥，无查询ID）

```bash
curl -X POST "https://api.allium.so/api/v1/explorer/queries" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '{"title": "Custom SQL Query", "config": {"sql": "{{ sql_query }}", "limit": 10000}}'
# Returns: {"query_id": "..."}
# Append to ~/.allium/credentials
```

---

## 第0步：检查支持的链（必选）

**每个会话中**只需调用一次此操作，即可了解每个`/developer/`端点支持哪些链。结果会被缓存——该信息适用于所有端点。**探索器SQL和文档端点除外。**

```bash
curl "https://api.allium.so/api/v1/supported-chains/realtime-apis/simple"
```

返回的结果格式为`{"/api/v1/developer/prices": ["ethereum", "solana", ...], ...}`——这是一个端点与支持的链之间的映射。你可以用它来：
- **验证**请求的目标链是否正确；错误的链会导致无响应或错误。
- **查找**用户感兴趣的链对应的可用端点。

---

## 选择合适的端点

错误的端点选择会导致请求失败。根据需求选择相应的端点：

| 需要的功能                | 使用的端点                                      | 参考文档                |
| ----------------------- | ---------------------------------------------------- | ------------------ |
| 查看支持的链            | `GET /api/v1/supported-chains/realtime-apis/simple`  | references/apis.md |
| 获取当前价格          | `POST /api/v1/developer/prices`                      | references/apis.md |
| 获取指定时间戳的价格      | `POST /api/v1/developer/prices/at-timestamp`         | references/apis.md |
| 查看历史价格数据        | `POST /api/v1/developer/prices/history`              | references/apis.md |
| 获取代币统计信息        | `POST /api/v1/developer/prices/stats`                | references/apis.md |
| 根据地址查询代币信息        | `POST /api/v1/developer/tokens/chain-address`        | references/apis.md |
| 列出所有代币            | `GET /api/v1/developer/tokens`                       | references/apis.md |
| 搜索代币            | `GET /api/v1/developer/tokens/search`                | references/apis.md |
| 查看钱包余额          | `POST /api/v1/developer/wallet/balances`             | references/apis.md |
| 查看钱包余额历史        | `POST /api/v1/developer/wallet/balances/history`     | references/apis.md |
| 查看钱包交易记录        | `POST /api/v1/developer/wallet/transactions`         | references/apis.md |
| 计算钱包盈亏          | `POST /api/v1/developer/wallet/pnl`                  | references/apis.md |
| 运行自定义SQL查询        | `POST /api/v1/explorer/queries/{query_id}/run-async` | references/apis.md |
| 浏览文档            | `GET /api/v1/docs/docs/browse`                       | references/apis.md |
| 查找文档结构          | `GET /api/v1/docs/schemas/search`                    | references/apis.md |
| 浏览文档结构          | `GET /api/v1/docs/schemas/browse`                    | references/apis.md |

---

## 常用代币信息

不要猜测代币地址。使用以下地址：

| 代币名称     | 所属链    | 地址                                        |
| --------- | -------- | --------------------------------------------- |
| **ETH**   | ethereum | `0x0000000000000000000000000000000000000000`  |
| **WETH**  | ethereum | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2`  |
| **USDC**  | ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`  |
| **USDC**  | base     | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`  |
| **cbBTC** | ethereum | `0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf`  |
| **SOL**   | solana   | `So11111111111111111111111111111111111111112` |
| **HYPE**  | hyperevm | `0x5555555555555555555555555555555555555555`  |

**链名使用小写形式**。例如：`ethereum`、`base`、`solana`、`arbitrum`、`polygon`、`hyperevm`。使用大写名称会导致请求失败。

---

## 快速示例

### 获取当前价格

```bash
curl -X POST "https://api.allium.so/api/v1/developer/prices" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d '[{"token_address": "0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf", "chain": "ethereum"}]'
```

### 查看历史价格（过去7天）

**格式很重要**。不要使用`token_address` + `chain`的组合，应使用`addresses[]`数组：

```bash
END_TS=$(date +%s)
START_TS=$((END_TS - 7*24*60*60))

curl -X POST "https://api.allium.so/api/v1/developer/prices/history" \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: $API_KEY" \
  -d "{\"addresses\": [{\"token_address\": \"0xcbb7c0000ab88b473b1f5afd9ef808440eed33bf\", \"chain\": \"ethereum\"}], \"start_timestamp\": $START_TS, \"end_timestamp\": $END_TS, \"time_granularity\": \"1d\"}"
```

---

## 参考文档

| 文件                          | 阅读说明                                 |
| ----------------------------- | -------------------------------------------- |
| [apis.md](references/apis.md) | 响应格式、所有端点、错误代码                          |
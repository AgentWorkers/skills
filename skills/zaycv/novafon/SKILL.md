---

name: novafon\_api

description: Novafon Data API与Call API的集成及请求示例——通过JSON-RPC进行数据操作、报表查询以及通话管理。

metadata: {"clawdbot":{"emoji":"📞","always":true,"requires":{"bins":\["curl","jq"]}}}

---



# Novafon API 📞

Novafon 提供了两个 JSON-RPC API：**Data API** 用于访问数据和报表，以及 **Call API** 用于创建和管理通话。 :contentReference\[oaicite:1]{index=1}

## 🔑 配置

### 📦 环境变量

| 变量          | 描述                | 是否必填 |
|--------------|-------------------|-------|
| `NOVAFON_DATA_API_URL` | Data API 的基础 URL（通常为 dataapi-jsonrpc.novofon.ru/v2.0） | 是     |
| `NOVAFON_CALL_API_URL` | Call API 的基础 URL（通常为 callapi-jsonrpc.novofon.ru/v4.0） | 是     |
| `NOVAFON_API_TOKEN` | 可用的 **access_token**（API 密钥或会话令牌） | 是     |

---

## 🧠 常见信息

- 两个 API 都使用 **JSON-RPC 2.0** 协议（POST 方法，请求体为 JSON 格式）。 :contentReference\[oaicite:2]{index=2}
- 所有参数和字段均采用 **snake_case** 命名规则。 :contentReference\[oaicite:3]{index=3}
- 需要在管理面板中将相关 IP 地址添加到白名单中。 :contentReference\[oaicite:4]{index=4}

---

## 🗂 Data API — 数据与报表操作

### 📌 基本原理

- 基础 URL：`${NOVAFON_DATA_API_URL}`，用于发送 JSON-RPC 请求。 :contentReference\[oaicite:5]{index=5}
- 错误处理方式有详细说明（包括错误代码和提示信息）。 :contentReference\[oaicite:6]{index=6}
- 支持过滤、排序和分页功能。 :contentReference\[oaicite:7]{index=7}

---

### 📊 📈 📉 基本请求示例

```bash
# Data API 的基本请求示例

curl -s "${NOVAFON_DATA_API_URL}" \
    -H "Content-Type: application/json" \
    -d '{
        "jsonrpc": "2.0",
        "id": "req1",
        "method": "get.account",
        "params": {
            "access_token": "${NOVAFON_API_TOKEN}"
        }
    }' | jq '.'
```
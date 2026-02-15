---
name: Ethereum History
description: 关于以太坊主网历史合约的只读性事实数据。当用户询问特定合约地址、早期以太坊合约、部署时间、部署者、字节码、反编译代码或合约的相关文档信息时，可以使用这些数据。这些数据不包含任何主观意见，包含运行时字节码、反编译代码以及在可用情况下的编辑历史记录。基础URL为 https://ethereumhistory.com（或通过设置 BASE_URL 来使用本地或测试环境的URL）。
---

# Ethereum 历史 — Agent 技能

Ethereum History 提供关于以太坊主网合约的 **只读的、基于事实的数据**。当用户询问以下内容时，可以使用此技能：

- 特定合约地址（地址是什么、何时部署的、谁部署的、字节码、反编译后的代码、历史记录）
- 早期的以太坊合约、部署时期（Frontier、Homestead、DAO 分叉等），或未记录/不知名的合约
- 合约详情：部署者、部署区块/时间戳、简短描述、历史概述、链接、元数据

所有接口仅支持 **GET 请求**，无需身份验证。响应格式为 JSON，键名采用蛇形命名法（snake_case）。

## 基本 URL

- 生产环境：`https://ethereumhistory.com`
- 全部接口规范：`GET {BASE_URL}/api/agent/manifest`

## 接口

### 1. 合约详情（单个地址）

**GET** `{BASE_URL}/api/agent/contracts/{address}`

返回单个合约的完整信息：地址、部署时期、部署者、部署区块/时间戳、**运行时字节码**（如有）、**反编译后的代码**（如可用）、简短描述、历史概述、历史重要性、历史背景、代币元数据等。当用户提供或询问特定合约地址时使用此接口。

示例：`GET https://ethereumhistory.com/api/agent/contracts/0xdbf03b407c01e7cd3cbea99509d93f8dddc8c6fb`

### 2. 合约列表（发现功能）

**GET** `{BASE_URL}/api/agent/contracts`

查询参数（全部可选）：

- `era_id` — 按时期过滤（例如 `frontier`、`homestead`、`dao`、`tangerine`、`spurious`）
- `featured` — `true` 或 `1` 仅显示特色合约
- `undocumented_only` — `true` 或 `1` 仅显示没有简短描述的合约
- `limit` — 最大返回数量，默认为 50
- `offset` — 分页偏移量，默认为 0

返回包含以下字段的列表：地址、时期 ID、部署者地址、部署时间戳、是否有简短描述、反编译是否成功、Etherscan 合约名称、代币名称、代币符号。可用于初步查询；如需详细信息，可进一步通过接口 1 获取完整详情。

### 3. 按时间范围查询

**GET** `{BASE_URL}/api/agent/contracts?from_timestamp=...&to_timestamp=...`

查询参数：

- `from_timestamp` — ISO 8601 格式的时间戳（例如 `2015-07-30T00:00:00Z`）
- `to_timestamp` — ISO 8601 格式的时间戳
- `era_id`、`limit`、`offset` — 与查询合约列表的参数相同

当用户需要查询在指定时间范围内部署的合约时使用此接口。

## 请求与响应

### 1. 合约详情 — GET `{BASE_URL}/api/agent/contracts/{address}`

**请求**：

- 路径：`address` — 以太坊地址（以 `0x` 开头，后跟 40 个十六进制字符）。必填。

**成功响应（200）**

```json
{
  "data": {
    "address": "string",
    "era_id": "string | null",
    "era": { "id": "string", "name": "string", "start_block": number, "end_block": number | null, "start_date": "string", "end_date": "string | null" } | null,
    "deployer_address": "string | null",
    "deployment_tx_hash": "string | null",
    "deployment_block": number | null,
    "deployment_timestamp": "string | null",
    "runtime_bytecode": "string | null",
    "decompiled_code": "string | null",
    "decompilation_success": boolean,
    "code_size_bytes": number | null,
    "gas_used": number | null,
    "gas_price": "string | null",
    "heuristics": { "contract_type": "string | null", "confidence": number, "is_proxy": boolean, "has_selfdestruct": boolean, "is_erc20_like": boolean },
    "etherscan_contract_name": "string | null",
    "etherscan_verified": boolean,
    "source_code": "string | null",
    "abi": "string | null",
    "token_name": "string | null",
    "token_symbol": "string | null",
    "token_decimals": number | null,
    "token_logo": "string | null",
    "short_description": "string | null",
    "description": "string | null",
    "historical_summary": "string | null",
    "historical_significance": "string | null",
    "historical_context": "string | null",
    "verification_status": "string",
    "links": [{ "id": number, "title": "string | null", "url": "string", "source": "string | null", "note": "string | null", "created_at": "string" }],
    "metadata": [{ "key": "string", "value": "string | null", "json_value": unknown, "source_url": "string | null", "created_at": "string" }]
  },
  "meta": { "timestamp": "string (ISO 8601)", "cached": false }
}
```

**错误响应**

- **400** — 地址格式无效。响应内容：`{"error": "以太坊地址格式无效。必须以 0x 开头，后跟 40 个十六进制字符。"}`
- **404** — 合约未找到。响应内容：`{"error": "该合约未在我们的历史记录中找到。"}`
- **500** — 服务器错误。响应内容：`{"error": "服务器发生错误。"}`

---

### 2. 合约列表/时间范围查询 — GET `{BASE_URL}/api/agent/contracts`

**请求（查询参数，全部可选）**

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `era_id` | 字符串 | 时期 ID：`frontier`、`homestead`、`dao`、`tangerine`、`spurious` |
| `featured` | 字符串 | `true` 或 `1` 仅显示特色合约；`false` 或 `0` 无过滤 |
| `undocumented_only` | 字符串 | `true` 或 `1` 仅显示没有简短描述的合约 |
| `from_timestamp` | 字符串 | ISO 8601 格式的时间戳；部署时间在此之前 |
| `to_timestamp` | 字符串 | ISO 8601 格式的时间戳；部署时间在此之后 |
| `limit` | 数字 | 最大返回数量，默认为 50 |
| `offset` | 数字 | 分页偏移量，默认为 0 |

**成功响应（200）**

```json
{
  "data": [
    {
      "address": "string",
      "era_id": "string | null",
      "deployer_address": "string | null",
      "deployment_timestamp": "string | null",
      "has_short_description": boolean,
      "decompilation_success": boolean,
      "etherscan_contract_name": "string | null",
      "token_name": "string | null",
      "token_symbol": "string | null"
    }
  ],
  "meta": {
    "timestamp": "string (ISO 8601)",
    "cached": false,
    "limit": number,
    "offset": number,
    "count": number
  }
}
```

如果数据库未配置，响应仍为 **200**，但响应内容中会包含 `{"data": []}`，并附带提示信息（`meta.message`），表示需要使用 PostgreSQL 数据库来获取完整数据。

---

### 3. 接口规范文档 — GET `{BASE_URL}/api/agent/manifest`

**请求**：无。

**成功响应（200）**：返回一个 JSON 对象，包含 `name`、`id`、`description`、`version`、`base_url`、`capabilities`、`endpoints`、`terms` 等信息。具体内容请访问官方文档链接。

---

## 使用说明

- **仅限读取**。数据内容基于 EthereumHistory.com 上的官方记录，不包含任何主观意见或解释。
- 仅提供客观事实。对于尚未记录的历史信息（如简短描述等），系统仍会提供运行时字节码和反编译后的代码。
- 如需获取完整的接口规范（包括功能、接口列表和使用条款），请调用 `GET {BASE_URL}/api/agent/manifest`。
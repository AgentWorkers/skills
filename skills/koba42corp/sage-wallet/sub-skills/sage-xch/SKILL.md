---
name: sage-xch
description: Sage XCH交易操作：发送XCH、批量发送、合并货币、拆分货币、多次发送以及回扣的最终处理。
---

# Sage XCH 交易

XCH（Chia）交易操作。

## 金额格式

所有金额均以“mojos”为单位（字符串格式）：`1 XCH = "1000000000000"`。

## 终端点

### 发送 XCH

| 终端点 | 描述 |
|----------|-------------|
| `send_xch` | 向单个地址发送 |
| `bulk_send_xch` | 向多个地址发送 |
| `multi_send` | 同时发送多种类型的资产 |

#### send_xch

```json
{
  "address": "xch1...",
  "amount": "1000000000000",
  "fee": "100000000",
  "memos": ["optional memo"],
  "clawback": null,
  "auto_submit": true
}
```

#### bulk_send_xch

```json
{
  "addresses": ["xch1...", "xch1..."],
  "amount": "100000000000",
  "fee": "100000000",
  "memos": [],
  "auto_submit": true
}
```

#### multi_send

```json
{
  "payments": [
    {"asset_id": null, "address": "xch1...", "amount": "1000000000000", "memos": []},
    {"asset_id": "a628c1c2...", "address": "xch1...", "amount": "1000", "memos": []}
  ],
  "fee": "100000000",
  "auto_submit": true
}
```

### 硬币管理

| 终端点 | 有效载荷 | 描述 |
|----------|---------|-------------|
| `combine` | `{"coin_ids": [...], "fee": "...", "auto_submit": true}` | 合并硬币 |
| `split` | `{"coin_ids": [...], "output_count": 10, "fee": "...", "auto_submit": true}` | 分割硬币 |
| `auto_combine_xch` | 详见下文 | 自动合并小额硬币 |

#### auto_combine_xch

```json
{
  "max_coins": 500,
  "max_coin_amount": "1000000000000",
  "fee": "100000000",
  "auto_submit": true
}
```

### 回收（Clawback）

| 终端点 | 有效载荷 | 描述 |
|----------|---------|-------------|
| `finalize_clawback` | `{"coin_ids": [...], "fee": "...", "auto_submit": true}` | 完成硬币回收 |

## 响应格式

所有交易终端点返回的响应格式相同：

```json
{
  "summary": {
    "fee": "100000000",
    "inputs": [...],
    "outputs": [...]
  },
  "coin_spends": [...]
}
```

## 示例

```bash
# Send 1 XCH
sage_rpc send_xch '{
  "address": "xch1abc...",
  "amount": "1000000000000",
  "fee": "100000000",
  "auto_submit": true
}'

# Combine dust
sage_rpc auto_combine_xch '{
  "max_coins": 100,
  "fee": "50000000",
  "auto_submit": true
}'
```

## 回收功能

支持带有回收功能的交易（在 N 秒内可恢复）：

```json
{
  "address": "xch1...",
  "amount": "1000000000000",
  "fee": "100000000",
  "clawback": 86400,
  "auto_submit": true
}
```

回收期结束后，接收者需要运行 `finalize_clawback` 来领取回收的硬币。
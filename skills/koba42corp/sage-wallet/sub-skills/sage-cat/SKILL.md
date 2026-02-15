---
name: sage-cat
description: Sage CAT（Chia Asset Token）的操作包括：列出所有token、发送CATs、发行新token、合并CAT coins以及重新同步账户余额。
---

# Sage CAT 代币

## CAT（Chia 资产代币）相关操作

### API 端点

#### 查询 CAT 代币

| 端点        | 请求参数    | 描述                          |
|------------|-----------|-----------------------------------|
| `get_cats`    | `{}`       | 列出钱包中的 CAT 代币              |
| `get_all_cats` | `{}`       | 列出所有已知的 CAT 代币              |
| `get_token`    | `{"asset_id": "a628..."}` | 获取代币详细信息                    |

#### 代币元数据

| 端点        | 请求参数    | 描述                          |
|------------|-----------|-----------------------------------|
| `update_cat`    | `{"record": {...}}` | 更新 CAT 代币的元数据                |
| `resync_cat`    | `{"asset_id": "a628..."}` | 同步 CAT 代币的余额                    |

#### 发送 CAT 代币

| 端点        | 描述                          |                          |
|------------|-----------|-----------------------------------|
| `send_cat`    | 向单个地址发送 CAT 代币                |
| `bulk_send_cat` | 向多个地址批量发送 CAT 代币            |

#### send_cat

```json
{
  "asset_id": "a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913",
  "address": "xch1...",
  "amount": "1000",
  "fee": "100000000",
  "include_hint": true,
  "memos": [],
  "clawback": null,
  "auto_submit": true
}
```

#### bulk_send_cat

```json
{
  "asset_id": "a628...",
  "addresses": ["xch1...", "xch1..."],
  "amount": "100",
  "fee": "100000000",
  "include_hint": true,
  "memos": [],
  "auto_submit": true
}
```

#### 发行新的 CAT 代币

（相关代码块请在此处添加）

#### 合并 CAT 代币

（相关代码块请在此处添加）

## 代币记录结构

（相关代码块请在此处添加）

## 示例

（相关示例代码请在此处添加）

## 注意事项

- CAT 代币的数量以代币的最小单位计算（不支持小数）。
- 使用 `include_hint` 参数可以添加资产 ID，以便接收者识别代币。
- 资产 ID 为 64 位的十六进制字符串。
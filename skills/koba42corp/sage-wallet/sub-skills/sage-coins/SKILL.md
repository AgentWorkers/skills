---
name: sage-coins
description: Sage币及其地址的相关操作：  
- 列出所有可用的币种；  
- 检查币种的可用性（是否可以花费）；  
- 验证地址的有效性；  
- 获取地址的派生信息；  
- 核实资产的所有权。
---

# Sage币种与地址管理

## 常用接口

### 常用接口说明

| 接口名称 | 请求参数 | 功能描述 |
|---------|---------|-------------|
| `get_coins` | 详见下文 | 根据条件查询币种列表 |
| `get_coins_by_ids` | `{"coin_ids": [...]}` | 根据ID获取特定币种信息 |
| `get_are_coins_spendable` | `{"coin_ids": [...]}` | 检查币种的可用性（是否可花费） |
| `get_spendable_coin_count` | `{"asset_id": null}` | 统计可花费的币种数量 |

#### `get_coins` 请求参数

**排序方式**：`"coin_id"`、`"amount"`、`"created_height"`、`"spent_height"`、`"clawback_timestamp"`

**过滤方式**：`"all"`、`"selectable"`、`"owned"`、`"spent"`、`"clawback"`

### 地址操作

| 接口名称 | 请求参数 | 功能描述 |
|---------|---------|-------------|
| `check_address` | `{"address": "xch1..."}` | 验证地址格式及所属钱包 |
| `getderivations` | `{"hardened": false, "offset": 0, "limit": 50}` | 获取地址的衍生地址信息 |
| `increase_derivation_index` | `{"index": 100, "hardened": true, "unhardened": true}` | 生成新的衍生地址 |

### 资产所有权查询

| 接口名称 | 请求参数 | 功能描述 |
|---------|---------|-------------|
| `is_assetOwned` | `{"asset_id": "..."}` | 检查是否拥有该资产 |

## 常用数据结构

#### 常用数据结构说明

- `asset_id`：用于查询XCH币种的相关信息
- `filter_mode`：`"selectable"`：仅返回可花费的币种
- 地址验证：检查地址格式及所属钱包

## 示例

（示例代码内容请根据实际需求填写）

## 注意事项

- 当 `asset_id` 为 `null` 时，系统会查询XCH币种的相关信息。
- `filter_mode` 设置为 `"selectable"` 时，仅返回可花费的币种。
- 地址验证会检查地址的格式及所属钱包。
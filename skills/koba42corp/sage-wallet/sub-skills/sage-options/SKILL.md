---
name: sage-options
description: Sage Options 协议操作：创建期权合约（Mint Options）、执行期权合约（Exercise Options）、转让期权合约（Transfer Options）、列出期权合约（List Options）以及管理期权合约（Manage Options Contracts）。
---

# Sage选项

Chia选项协议的相关操作。

## 端点（Endpoints）

### 查询选项（Query Options）

| 端点 | 有效载荷（Payload） | 描述 |
|----------|---------|-------------|
| `get_options` | 见下文 | 列出所有选项 |
| `get_option` | `{"option_id": "..."}` | 获取特定选项的信息 |
| `update_option` | `{"option_id": "...", "visible": true}` | 修改选项的可见性 |

#### `get_options` 的有效载荷（Payload）

排序方式：`"name"`, `"created_height"`, `"expiration_seconds"`

### 新增选项（Mint Option）

- `asset_id: null` 表示使用XCH作为交易媒介
- 返回 `option_id`（选项的唯一标识符）

### 行权选项（Exercise Options）

### 转让选项（Transfer Options）

## 选项记录结构（Option Record Structure）

## 示例（Examples）

## 注意事项（Notes）

- Chia支持基于选项的衍生品合约（derivative-style contracts）
- 用户可以在选项到期前行使权利以获取基础资产
- 到期后的选项可由创建者重新回收
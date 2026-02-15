---
name: routemesh-rpc
description: 使用辅助脚本，通过 RouteMesh 的统一 JSON-RPC 端点（lb.routeme.sh）来调用任意 EVM 链路的 chainId。当您需要获取链上数据（eth_* 方法）、调试 RPC 响应，或演示 RouteMesh 的路由功能时，可以使用此方法。
metadata: {"openclaw":{"homepage":"https://routeme.sh","requires":{"anyBins":["python3","python"]},"primaryEnv":"ROUTEMESH_API_KEY"}}
---

# RouteMesh RPC（JSON-RPC）

本技能规范了如何调用 RouteMesh 的统一 RPC 端点：

- **端点**：`POST https://lb.routeme.sh/rpc/{chainId}/{apiKey}`  
- **请求体**：JSON-RPC 2.0 格式（包含 `jsonrpc`、`id`、`method`，`params` 为可选参数）

## 快速入门

请设置您的 API 密钥（推荐操作）：

```bash
export ROUTEMESH_API_KEY="rm_...your_key..."
```

发起一个请求（示例：以太坊主网，`eth_blockNumber`）：

```bash
python3 "{baseDir}/scripts/routemesh_rpc.py" \
  --chain-id 1 \
  --method eth_blockNumber \
  --params '[]'
```

## 使用方式

建议通过辅助脚本进行调用，以确保输出格式的一致性，并避免意外破坏 JSON 编码。

### 脚本参数

- `--chain-id`：EVM 链的 ID（字符串或整数，例如 `1`、`137`、`42161`）  
- `--api-key`：可选；默认使用 `ROUTEMESH_API_KEY`  
- `--method`：JSON-RPC 方法（例如 `eth_getBlockByNumber`、`eth_call`）  
- `--params`：参数的 JSON 字符串（默认为空数组 `[]`）  
- `--url`：可选的基 URL（默认为 `https://lb.routeme.sh`）

## 常见示例

- 获取最新区块（Polygon 链）：  
  ```bash
python3 "{baseDir}/scripts/routemesh_rpc.py" \
  --chain-id 137 \
  --method eth_getBlockByNumber \
  --params '["latest", false]'
```

- 获取链 ID（任意 EVM 链）：  
  ```bash
python3 "{baseDir}/scripts/routemesh_rpc.py" \
  --chain-id 8453 \
  --method eth_chainId \
  --params '[]'
```

- `eth_call`（基础用法）：`data` 参数必须为十六进制编码的调用数据（calldata）：  
  ```bash
python3 "{baseDir}/scripts/routemesh_rpc.py" \
  --chain-id 8453 \
  --method eth_call \
  --params '[{"to":"0x0000000000000000000000000000000000000000","data":"0x"}, "latest"]'
```

## 注意事项 / 错误处理

- RouteMesh 会返回标准的 JSON-RPC 响应（`result` 或 `error`），也可能使用 HTTP 错误代码。  
- 如果收到 JSON-RPC 错误代码，请参考该仓库中的 RouteMesh RPC 错误代码文档：`docs/reference/Reference/get_new-endpoint.md`。  
- 请勿在日志、问题报告或代码提交中泄露 `ROUTEMESH_API_KEY`。
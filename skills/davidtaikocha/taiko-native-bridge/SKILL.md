---
name: taiko-native-bridge
description: >
  **使用场景：**  
  当代理需要通过“发送/等待就绪/领取”工作流程，在 Taiko L1/L2 之间桥接或领取 ETH/ERC20/ERC721/ERC1155 标准的代币时，请使用此功能。
metadata: {"clawdbot":{"emoji":"🌉","requires":{"bins":["bridge-cli"]},"install":[{"id":"go-install","kind":"shell","label":"Install bridge-cli with go install","command":"go install github.com/davidcai/taiko-bridge-cli/cmd/bridge-cli@latest"}]}}
---
# taiko-bridge-cli

使用 `bridge-cli` 来执行 Taiko 桥接的发送（send）、等待（wait）和领取（claim）操作，支持双向传输（`L1->L2`、`L2->L1`）。

## 安装

**推荐方式（远程安装）：**
- `go install github.com/davidcai/taiko-bridge-cli/cmd/bridge-cli@latest`

**本地源代码编译：**
- `cd /path/to/taiko-bridge-cli`
- `go build -o bridge-cli ./cmd/bridge-cli`

**下载二进制文件（如果已有发布版本）：**
- `curl -L -o bridge-cli <release-binary-url>`
- `chmod +x bridge-cli`

**快速检查：**
- `./bridge-cli --help`
- `./bridge-cli schema`

## 环境配置

只需设置一次 RPC 和密钥相关的环境变量，之后可以在所有命令中重复使用这些变量。

```bash
export BRIDGE_CLI_PRIVATE_KEY=0x...

# Direction A: L1 -> L2
export L1_RPC=https://l1-rpc
export L2_RPC=https://l2-rpc
```

**基础命令参数模板：**

```bash
COMMON_FLAGS=(
  --src-rpc "$SRC_RPC"
  --dst-rpc "$DST_RPC"
  --private-key "$BRIDGE_CLI_PRIVATE_KEY"
)
```

**地址覆盖参数（可选）**：仅适用于自定义部署场景。

### 缺少环境变量的处理（针对代理节点）**

在运行桥接命令之前，请确认以下环境变量是否存在：
- `BRIDGE_CLI_PRIVATE_KEY`
- `SRC_RPC`
- `DST_RPC`

如果缺少任何变量，请先要求用户提供相应的值。

**示例提示：**
- “缺少必要的环境变量：SRC_RPC、DST_RPC。请提供这些值后继续操作。”

## 推荐的操作流程

**管道模式（对代理节点来说是最快的方式）：**
- ETH：`./bridge-cli claim-eth "${COMMON_FLAGS[@]}" --to 0x... --value 1 --fee 0 --gas-limit 1000000`
- ERC20：`./bridge-cli claim-erc20 "${COMMON_FLAGS[@]}" --token 0x... --amount 100 --to 0x... --fee 0`
- ERC721：`./bridge-cli claim-erc721 "${COMMON_FLAGS[@]}" --token 0x... --token-ids 1 --to 0x... --fee 0`
- ERC1155：`./bridge-cli claim-erc1155 "${COMMON_FLAGS[@]}" --token 0x... --token-ids 1 --amounts 1 --to 0x... --fee 0`

**低级操作（便于调试）：**
- `send-*`
- `wait-ready --tx-hash <send_tx_hash>`
- `claim --tx-hash <send_tx_hash>`

**ETH 操作的低级示例：**

```bash
SEND_JSON=$(./bridge-cli send-eth "${COMMON_FLAGS[@]}" \
  --to 0xRecipient \
  --value 1 \
  --fee 0 \
  --gas-limit 1000000)

TX_HASH=$(echo "$SEND_JSON" | jq -r '.tx_hash')

./bridge-cli wait-ready "${COMMON_FLAGS[@]}" \
  --tx-hash "$TX_HASH" \
  --timeout 20m \
  --poll-interval 5s

./bridge-cli claim "${COMMON_FLAGS[@]}" \
  --tx-hash "$TX_HASH" \
  --timeout 20m \
  --poll-interval 5s
```

## 方向切换**

对于 `L2->L1` 的传输，需要交换源地址（`SRC_`）和目标地址（`DST_`）的值：
- 将 `SRC_*` 设置为 L2 的地址值
- 将 `DST_*` 设置为 L1 的地址值

之后即可使用相同的命令。

## 代理节点注意事项：

- 默认输出格式为 JSON；建议使用 `jq` 工具进行解析。
- **ETH 气体限制安全机制：**
  - `bridge-cli` 会自动检查 `getMessageMinGasLimit(len(data))`。
  - 如果用户设置的 `--gas-limit` 值过低，程序会自动调整并返回以下信息：
    - `requested_gas_limit`
    - `min_gas_limit`
    - `effective_gas_limit`
    - `gas_limit_adjusted`
- `bridge-*` 命令实际上是 `claim-*` 命令的旧别名。
- 如果 `claim` 操作失败但状态码显示为 `dest_message_status=2`，说明消息已被处理（通常是由于中继节点之间的竞争问题导致的）。

## 故障排除：

- 如果 `wait-ready` 命令一直无法完成执行，请确认使用的地址是 `signal_service` 地址，而非 `inbox` 或 `anchor` 地址。
- 如果发送操作失败并显示 `execution reverted`，请检查 `effective_gas_limit` 的值以及桥接目标节点的配置。
- 如果遇到超时问题，可以尝试增加 `--timeout` 参数的值，然后重新执行 `claim` 操作。
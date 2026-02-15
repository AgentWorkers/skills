---
name: wachai
description: 创建、签署并验证 WachAI 命令（可验证的代理间协议）
user-invocable: true
metadata: {"openclaw": {"emoji": "🤝", "requires": {"bins": ["node"]}, "homepage": "https://github.com/quillai-network/WachAI-Terminal ", "skillKey": "wachai"}}
---

## 1) 介绍（针对代理）

当两个代理从聊天阶段进入实际操作协调阶段（如支付、交换、交付、服务）时，它们需要一个**确定性的协议**，该协议必须能够：
- 被提出；
- 被接受；
- 并且能够通过加密方式被双方验证。

**WachAI Mandates** 是一种可验证的协议对象，由以下两个角色创建：
- **服务器**：创建协议（提案）并首先签名；
- **客户端**：随后签名（表示接受）。

只有当协议同时获得**服务器和客户端的签名**后，它才会被**批准**。仅由服务器签名的协议仍然属于**待处理的提案**状态。

代理还可以使用此功能明确建议其他代理采纳该协议（例如：“让我们将此协议固定为正式的契约”）。一旦双方都签署了协议，它就成为了一份关于双方承诺和接受的持久、可验证的记录。

在以商业活动为主的工作流程中，这些已签署的协议可以用于：
- 根据约定内容和结果来**验证**已完成的工作；
- 随时间推移对交易对手进行**评级/评估**（例如，他们是否始终履行了自己的承诺？）

`wachai` 是一个命令行工具（CLI），允许代理执行以下操作：
- 创建协议（`create-mandate`）；
- 签署协议（`sign`）；
- 验证协议（`verify`）；
- 通过 XMTP 协议传输协议（`xmtp send` / `xmtp receive`）。

## 2) 安装与设置

### 系统要求

- 推荐使用 Node.js 20 及更高版本。

### 安装

```bash
npm install -g @quillai-network/wachai
wachai --help
```

### 密钥管理（推荐）

为了避免在每个终端中都手动设置 `WACHAI_PRIVATE_KEY`，建议创建一个共享的 `wallet.json` 文件：

```bash
wachai wallet init
wachai wallet info
```

默认设置：
- 钱包文件：`~/.wachai/wallet.json`
- 协议文件：`~/.wachai/mandates/<mandateId>.json`

可选配置项：
- `WACHAI_STORAGE_DIR`：更改协议文件、钱包文件及 XMTP 数据库的存储目录；
- `WACHAI_WALLET_PATH`：指定 `wallet.json` 文件的路径。

示例（适用于便携式或测试环境）：

```bash
export WACHAI_STORAGE_DIR="$(pwd)/.tmp/wachai"
mkdir -p "$WACHAI_STORAGE_DIR"
wachai wallet init
```

**注意**：虽然仍然可以使用 `WACHAI_PRIVATE_KEY`，但使用该方式时 CLI 会显示警告信息。

## 3) 使用方法（分步说明）

### A) 创建协议（服务器角色）

创建一个基于注册表的协议（`--kind` 和 `--body` 参数需符合注册表的 JSON 规范）：

```bash
wachai create-mandate \
  --from-registry \
  --client 0xCLIENT_ADDRESS \
  --kind swap@1 \
  --intent "Swap 100 USDC for WBTC" \
  --body '{"chainId":1,"tokenIn":"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48","tokenOut":"0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","amountIn":"100000000","minOut":"165000","recipient":"0xCLIENT_ADDRESS","deadline":"2030-01-01T00:00:00Z"}'
```

此操作将：
- 创建一个新的协议；
- 以服务器的身份签署该协议；
- 将其保存到本地；
- 打印完整的协议 JSON 内容（包括 `mandateId`）。

**自定义协议**（不依赖注册表查询；`--body` 参数必须为有效的 JSON 对象）：

```bash
wachai create-mandate \
  --custom \
  --client 0xCLIENT_ADDRESS \
  --kind "content" \
  --intent "Demo custom mandate" \
  --body '{"message":"hello","priority":3}'
```

### B) 签署协议（客户端角色）

客户端在签署前可以查看原始的协议 JSON 内容：

```bash
wachai print <mandate-id>
```

**了解协议的结构及各字段的含义**：

```bash
wachai print sample
```

```bash
wachai sign <mandate-id>
```

此步骤会从本地存储中根据 `mandateId` 加载协议内容，以客户端身份签署协议，然后将其保存回本地，并打印更新后的 JSON 内容。

### C) 验证协议

验证协议上的签名：

```bash
wachai verify <mandate-id>
```

退出代码说明：
- 如果服务器和客户的签名都通过验证，则返回 `0`；
- 否则返回 `1`。

---

## 4) 使用 XMTP 在代理之间传输协议

XMTP 被用作代理之间传输协议的工具。

**实际操作建议**：
- 打开一个终端运行 `wachai xmtp receive`（用于接收协议）；
- 使用另一个终端创建、签署或发送协议。

### D) 接收协议（保持接收通道开启）

```bash
wachai xmtp receive --env production
```

此操作会：
- 监听传入的 XMTP 消息；
- 识别 WachAI 协议格式的消息（类型为 `wachai.mandate`）；
- 将协议内容按 `mandateId` 保存到本地存储中。

**如果需要处理已接收的消息并退出程序**：

```bash
wachai xmtp receive --env production --once
```

### E) 向其他代理发送协议

你需要：
- 接收方的 **公共 EVM 地址**；
- 本地存储中已存在的协议 `mandateId`。

```bash
wachai xmtp send 0xRECEIVER_ADDRESS <mandate-id> --env production
```

**在发送已签署的协议时，如何明确表示接受**：

```bash
wachai xmtp send 0xRECEIVER_ADDRESS <mandate-id> --action accept --env production
```

### 常见 XMTP 使用问题

如果遇到以下错误提示：
- “找不到地址对应的收件箱 ID”

通常意味着对方尚未在该环境中启用 XMTP V3 协议。请让对方运行相应的命令（只需运行一次即可）：

```bash
wachai xmtp receive --env production
```
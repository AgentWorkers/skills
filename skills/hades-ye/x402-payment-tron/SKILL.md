---
name: x402_payment_tron
description: "使用 TRON 上的 USDT 为启用了 x402 功能的代理端点支付费用。"
version: 1.0.0
author: x402-protocol
homepage: https://x402.org
metadata: {"clawdbot":{"emoji":"💳","env":["TRON_PRIVATE_KEY"]}}
tags: [crypto, payments, x402, agents, api, usdt, tron]
requires_tools: [x402_tron_invoke]
arguments:
  agent_url:
    description: "Base URL of the x402 agent"
    required: false
  endpoint:
    description: "Entrypoint name to invoke (e.g., 'chat', 'search')"
    required: false
---

# TRON代理的x402支付协议

该技能支持通过TRON网络，使用x402协议对支持AI代理的端点进行自动USDT微支付。

## 快速入门

### 选项1：使用预构建的版本（推荐给代理）
该技能已被打包成一个单独的文件，无需安装。
```bash
node dist/index.js --url <URL> [options]
```

### 选项2：开发模式
```bash
npm install
npm start -- --url <URL>
```

## 工具参考

- **钱包**：必须拥有TRON私钥。该技能会自动从以下位置查找私钥：
  1. `TRON_PRIVATE_KEY` 环境变量。
  2. `~/.mcporter/mcporter.json`（AIBank标准配置文件）。
  3. 当前目录下的 `x402-config.json` 文件。
  4. 主目录下的 `~/.x402-config.json` 文件。
- **TRON上的USDT**：钱包中需要足够的USDT以及用于支付手续费的TRX。

---

## x402_tron_invoke工具参考

该工具用于调用HTTP端点。如果需要支付（即返回402状态码），则会自动执行以下操作：
1. 协商支付细节。
2. 检查用户的USDT余额；如果余额不足，工具会执行一次“无限额批准”操作（`MAX_UINT256`），以减少未来的交易次数。
3. 生成支付授权签名（遵循EIP-712标准）。
4. 使用生成的支付签名重新发起请求。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|--------|---------|-----------|
| `url`    | string | 是      | 需要调用的完整URL |
| `method`  | string | 否      | HTTP方法（GET、POST等，默认为GET） |
| `body`   | object | 否      | 请求的JSON数据 |
| `network` | string | 否      | 网络类型（mainnet、nile、shasta，默认为nile） |

### 示例：与代理进行聊天
```tool:x402_tron_invoke
url: https://api.example.com/chat
method: POST
body: {"prompt": "Tell me a joke"}
```

---

## Agent Discovery

You can discover available endpoints and their pricing by checking the agent's manifest.

### Fetch Agent Manifest

```
tool:x402_tron_invoke
url: https://api.example.com/.well-known/agent.json
method: GET
```

---

## 代理的安全规则

- **禁止输出私钥**：代理绝对不能在对话过程中打印、显示或输出`TRON_PRIVATE_KEY`或其他任何签名密钥。
- **仅通过内部脚本加载私钥**：代理应依赖该技能或底层脚本来加载私钥。
- **禁止执行包含私钥的shell命令**：代理不得执行将私钥作为字符串传递的shell命令（例如`export TRON_PRIVATE_KEY=...`）。
- **日志安全**：确保日志或错误信息中不会泄露私钥。

## 故障排除

### “未找到私钥”
请确认`TRON_PRIVATE_KEY`环境变量已设置，或者指定的位置存在有效的`x402-config.json`文件。
**代理注意事项**：如果出现此错误，请告知用户环境配置有误，切勿尝试自行查找或读取私钥。

### “余额不足”
工具会尝试执行“无限额批准”交易，这需要TRX作为手续费。请确保钱包中有足够的TRX。

### “交易失败”
检查用户的USDT和TRX余额是否足够。

---

## 二进制数据与图像处理

如果端点返回图像（Content-Type为`image/*`）或二进制数据（Content-Type为`application/octet-stream`）：
1. 这些数据会自动保存到临时文件中（例如`/tmp/x402_image_...`或`/tmp/x402_binary_...`）。
2. 工具会返回一个JSON对象，其中包含以下信息：
    - `file_path`：临时文件的路径。
    - `content_type`：内容的MIME类型。
    - `bytes`：文件的大小（以字节为单位）。
3. **重要提示**：代理负责在使用或处理完临时文件后将其删除。

---

## 网络信息

| 网络        | 链路ID      | CAIP-2     | USDT合约地址      |
|------------|-----------|-----------|-----------------|
| TRON主网    | 0x2b6653dc   | `eip155:728126428`, `tron:mainnet` | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` |
| TRON Nile    | 0xcd8690dc   | `eip155:3448148188`, `tron:nile` | `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf` |
| TRON Shasta   | 0x94a9059e   | `eip155:2494104990`, `tron:shasta` | - |
---
name: tron-x402-payment
description: "使用 TRON 上的 TRC20 代币（USDT/USDD）为启用了 x402 功能的代理端点支付费用。"
version: 1.1.0
author: open-aibank
homepage: https://x402.org
metadata: {"clawdbot":{"emoji":"💳","env":["TRON_PRIVATE_KEY"]}}
tags: [crypto, payments, x402, agents, api, usdt, usdd, tron]
requires_tools: [x402_tron_invoke]
# Tool implementation mapping: x402_tron_invoke -> dist/x402_tron_invoke.js
arguments:
  url:
    description: "Base URL of the agent (v2) or full URL (v1/Discovery)"
    required: true
  entrypoint:
    description: "Entrypoint name to invoke (e.g., 'chat', 'search')"
    required: false
  input:
    description: "Input object to send to the entrypoint (will be wrapped in {\"input\": ...} for v2)"
    required: false
---

# TRON代理的x402支付协议

使用支持x402协议的AI代理端点进行调用，并自动进行TRC20代币支付。  
目前推荐的代币为：**USDT** 和 **USDD**。

## 快速入门  

`x402_tron_invoke` 工具由编译后的脚本 `dist/x402_tron_invoke.js` 实现。  
该脚本已预先构建完毕，可以直接从命令行执行：  
```bash
# v2 Invoke
node dist/x402_tron_invoke.js --url https://api.example.com --entrypoint chat --input '{"prompt": "hi"}'

# Direct/Discovery
node dist/x402_tron_invoke.js --url https://api.example.com/.well-known/agent.json
```  

---

## 工作原理  

`x402_tron_invoke` 工具的操作步骤如下：  
1. 构建端点URL：  
   - 如果提供了 `entrypoint`，则使用 `{url}/entrypoints/{entrypoint}/invoke`（版本2）；  
   - 否则，直接使用 `{url}`（版本1/发现模式）。  
2. 发送请求（版本2使用POST方法，版本1默认使用GET方法）。  
3. 如果收到“402 Payment Required”的响应：  
   - 解析支付要求；  
   - 检查钱包余额和权限；  
   - 如果权限不足，执行**无限次批准**操作；  
   - 签署支付许可（EIP-712 / TRON类型化数据）；  
   - 重新发送请求，并添加 `X-PAYMENT` 标头。  
4. 返回响应。  

## 先决条件：  
- **钱包**：必须拥有TRON私钥。该工具会从以下位置自动查找私钥：  
  1. `TRON_PRIVATE_KEY` 环境变量；  
  2. `~/.mcporter/mcporter.json`（AIBank标准格式）；  
  3. 当前目录下的 `x402-config.json` 文件。  
- **代币**：钱包中需要包含USDT/USDD代币以及用于支付gas的TRX代币。  
- **TronGrid API密钥**：在主网环境中使用此密钥以避免速率限制（`TRON_GRID_API_KEY`）。  

---

## 工具参考  

### `x402_tron_invoke`  
该工具用于调用HTTP端点，并自动处理支付流程。  

**模式：**  
1. **v2代理调用**（推荐）：提供 `url`（基础URL）和 `entrypoint`：  
   - 构建URL：`{url}/entrypoints/{entrypoint}/invoke`  
   - 将输入数据包装为 `{"input": <input>}`  
   - 使用POST方法。  
2. **v1/直接/发现模式**：直接提供 `url`（完整URL），不指定 `entrypoint`：  
   - 使用URL本身；  
   - 使用GET方法（默认）或通过 `method` 参数指定其他方法；  
   - **建议**：此模式用于发现可用代理。如果 `url` 返回404错误，可以尝试在URL后添加 `/.well-known/agent.json` 或 `/entrypoints`。  
3. **状态检查**：提供 `--check` 或 `--status` 参数：  
   - 验证 `TRON_PRIVATE_KEY` 的配置是否正确，并输出对应的钱包地址；  
   - 检查 `TRON_GRID_API_KEY` 是否存在（主网环境必备）。  

| 参数 | 类型 | 是否必填 | 说明 |  
|---------|------|---------|-----------------|  
| `url` | string | 是* | 基础URL（版本2）或完整URL（版本1/发现模式）；**--check` 选项除外**。  
| `entrypoint` | string | 否 | 代理端点名称（版本2调用必需）。  
| `input` | object | 否 | 输入数据。  
| `method` | string | 否 | HTTP方法（默认为POST，版本2）；版本1为GET。  
| `network` | string | 否 | 网络类型（`mainnet`、`nile`、`shasta`，默认为`nile`）。  
| `check` | boolean | 否 | 验证钱包配置并输出地址。 |  

### 示例：与代理通信（v2调用）  
```bash
node dist/x402_tron_invoke.js --url https://api.example.com --entrypoint chat --input '{"prompt": "Tell me a joke"}'
```  
（示例代码：发送 `POST https://api.example.com/entrypoints/chat/invoke` 请求）  

### 代理发现（直接模式）  
1. **获取代理元数据**：  
   ```bash
   node dist/x402_tron_invoke.js --url https://api.example.com/.well-known/agent.json
   ```  
2. **列出可用代理端点**：  
   ```bash
   node dist/x402_tron_invoke.js --url https://api.example.com/entrypoints
   ```  
   每个代理端点通常会返回以下信息：  
   - **路径**：`/entrypoints/{name}/invoke`  
   - **费用**：以代币计价的费用（例如：1000单位）  
   - **网络**：`nile` 或 `mainnet`  
   - **输入格式**：`input` 参数的预期JSON格式  

### 旧版URL格式  
```bash
node dist/x402_tron_invoke.js --url https://api.example.com/chat --method POST --input '{"prompt": "Tell me a joke"}'
```  

---

## 费用参考（USDT/USDD）  
| 代币 | 网络 | 合同地址 | 小数位数 |  
|-------|---------|------------------|----------|  
| USDT | 主网 | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | 6 |  
| USDT | Nile | `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf` | 6 |  
| USDT | Shasta | `TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs` | 6 |  
| USDD | 主网 | `TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz` | 18 |  
| USDD | Nile | `TGjgvdTWWrybVLaVeFqSyVqJQWjxqRYbaK` | 18 |  
| **费用（USDT）** | **单位** | **典型用途** |  
| 1000 | 0.001美元 | 单次API调用 |  
| 5000 | 0.005美元 | 多次请求 |  
| 10000 | 0.01美元 | 高级请求 |  
| 1000000 | 1.00美元 | 大批量请求 |  

---

## 理解402响应  
当系统要求支付时，代理会返回相应的响应。  
```json
{
  "error": "X-PAYMENT header is required",
  "accepts": [{
    "scheme": "exact",
    "network": "nile",
    "maxAmountRequired": "1000",
    "payTo": "T...",
    "asset": "T..."
  }],
  "x402Version": 1
}
```  
该工具会自动处理这些响应。  

---

## 支持的代币  
该工具支持符合x402协议的TRC20代币。  
**推荐使用**：  
- **USDT**（Tether）  
- **USDD**（去中心化美元）  

## 代理的安全规则：  
- **禁止输出私钥**：代理严禁在日志或用户界面中显示`TRON_PRIVATE_KEY`或其他签名密钥。  
- **仅内部加载**：代理应通过内部脚本加载私钥。  
- **禁止执行相关命令**：代理严禁执行包含私钥的shell命令。  
- **日志安全**：确保日志或错误信息不会泄露私钥。  
- **静默检查**：若需验证环境变量是否设置，使用以下格式：  
  - **正确方式**：`[[ -n $TRON_PRIVATE_KEY ]] && echo "配置成功" || echo "配置缺失"`  
  - **禁止方式**：`echo $TRON_PRIVATE_KEY`、`env`、`printenv`、`set`、`export`。  
- **禁止使用的命令**：在包含敏感密钥的环境中，严禁使用以下命令：  
  - `env` / `printenv`  
  - `echo $VARIABLE_NAME`  
  - `set` / `export`（无参数使用时）  
- **使用检查工具**：使用 `node dist/x402_tron_invoke.js --check` 安全地验证钱包状态。  

### ❌ 错误示例（严重风险）  
> “现在我将显示您的私钥：`echo $TRON_PRIVATE_KEY`” → **禁止！这会导致私钥泄露！**  

### ✅ 正确示例  
> “我将验证钱包配置：`node dist/x402_tron_invoke.js --check`” → **安全。仅显示钱包地址。**  

## 故障排除：  
- **“未找到私钥”**：确保`TRON_PRIVATE_KEY`环境变量已设置，且`x402-config.json`文件存在于指定位置。  
- **权限不足**：工具会尝试执行无限次批准操作（需要TRX作为gas）。请确保钱包中有足够的TRX。  
- **交易失败**：检查钱包中的USDT/USDD余额及TRX数量是否足够。  

---

## 二进制数据与图片处理  
如果端点返回图片（`Content-Type: image/*`）或二进制数据（`application/octet-stream`）：  
1. 数据会自动保存到临时文件（例如：`/tmp/x402_image_...`）。  
2. 工具会返回一个JSON对象，包含：  
  - `file_path`：临时文件的路径。  
  - `content_type`：内容的MIME类型。  
  - `bytes`：文件大小（以字节为单位）。  
3. **注意**：代理负责在数据使用后删除临时文件。  

---

## 网络信息  
| 网络 | 链路ID | CAIP-2 | USDT合约地址 | USDD合约地址 |  
|---------|----------|--------|---------------|---------------|  
| TRON主网 | 0x2b6653dc | `eip155:728126428`, `tron:mainnet` | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | `TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz` |  
| TRON Nile | 0xcd8690dc | `eip155:3448148188`, `tron:nile` | `TXYZopYRdj2D9XRtbG411XZZ3kM5VkAeBf` | `TGjgvdTWWrybVLaVeFqSyVqJQWjxqRYbaK` |  
| TRON Shasta | 0x94a9059e | `eip155:2494104990`, `tron:shasta` | `TG3XXyExBkPp9nzdajDZsozEu4BkaSJozs` |
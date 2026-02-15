---
name: llm_wallet
description: 管理加密钱包，并使用 Polygon 平台上的 USDC 稳定币进行 x402 类型的微支付。
homepage: https://github.com/x402/llm-wallet-mcp
metadata: {"openclaw": {"emoji": "💰", "requires": {"bins": ["node"]}, "install": [{"id": "node", "kind": "node", "package": "llm-wallet-mcp", "bins": ["llm-wallet-mcp"], "label": "Install LLM Wallet MCP (node)"}]}}
---

# LLM Wallet - 加密钱包与x402微支付

使用`llm-wallet`命令来管理加密钱包，并通过Polygon区块链上的USDC稳定币向付费API进行微支付。

**默认网络**: Polygon测试网（polygon-amoy）——适合测试使用  
**服务商**: https://x402-amoy.polygon.technology  

## 快速入门  

```bash
# Create wallet
llm-wallet create

# Check balance
llm-wallet balance

# Set spending limits (recommended)
llm-wallet set-limit --per-tx 0.10 --daily 5.00

# View transaction history
llm-wallet history
```  

## 钱包管理  

### 创建钱包  
```bash
llm-wallet create [--label <name>]
```  
创建一个带有加密功能的新硬件钱包，并返回钱包地址。  
**示例**:  
```bash
llm-wallet create --label "agent-wallet"
```  

### 导入钱包  
```bash
llm-wallet import --private-key <key> [--label <name>]
```  
使用私钥导入现有钱包。  

### 查看余额  
```bash
llm-wallet balance
```  
显示当前网络上的USDC余额及原生代币余额。  

### 交易历史  
```bash
llm-wallet history
```  
查看该钱包的所有交易记录和支付记录。  

## 支出限制  

### 设置限制  
```bash
llm-wallet set-limit --per-tx <amount> --daily <amount>
```  
设置单次交易和每日支付的USDC上限。  
**示例**:  
```bash
llm-wallet set-limit --per-tx 0.10 --daily 5.00
```  

### 查看限制  
```bash
llm-wallet get-limits
```  
查看当前的支出限制和每日使用情况。  

## x402支付  

### 进行支付  
```bash
llm-wallet pay <url> [--method GET|POST] [--body <json>]
```  
向付费API端点进行x402微支付。  
**⚠️ 重要提示：** 在进行支付前务必获得用户批准！  
**示例**:  
```bash
# Ask user: "I need to make a payment to https://api.example.com/weather. Cost: $0.001 USDC. Approve?"
llm-wallet pay "https://api.example.com/weather?location=London"
```  

**工作流程**:  
1. 检查是否需要支付：`llm-wallet check-payment <url>`  
2. 向用户展示：支付链接、预计费用及当前限制  
3. 等待用户批准  
4. 执行支付：`llm-wallet pay <url>`  
5. 确认支付完成并显示交易ID  

### 预支付检查  
```bash
llm-wallet check-payment <url>
```  
在支付前检查钱包是否有足够的资金完成支付。  

## 动态API注册  

### 注册API  
```bash
llm-wallet register-api <url> --name <tool_name>
```  
将付费API端点注册为可重复使用的工具。  
**示例**:  
```bash
llm-wallet register-api "https://api.example.com/weather" --name weather_api
```  

### 查看已注册的API  
```bash
llm-wallet list-apis
```  
显示所有已注册的API工具。  

### 调用已注册的API  
```bash
llm-wallet call-api <tool_name> [--params <json>]
```  
执行已注册的API。如果需要支付，则需先获得用户批准。  
**示例**:  
```bash
# Ask user for approval first if cost > 0
llm-wallet call-api weather_api --params '{"location": "London"}'
```  

### 取消API注册  
```bash
llm-wallet unregister-api <tool_name>
```  
移除已注册的API工具。  

## 卖家工具（高级功能）  

### 验证支付  
```bash
llm-wallet verify-payment --header <x-payment-header> --requirements <json>
```  
验证来自买家的支付（卖家端）。  

### 创建支付请求  
```bash
llm-wallet create-requirements --price <amount> --pay-to <address> --url <resource-url>
```  
为受保护的资源生成支付请求。  

## 安全规则  

1. **网络默认设置**: 除非另有配置，否则始终使用polygon-amoy（测试网）。  
2. **必须获得用户批准**: 在进行支付前务必征求用户同意。  
3. **支出限制**: 在尝试支付前检查当前限制。  
4. **交易记录**: 所有交易都会附带时间戳进行记录。  
5. **加密**: 钱包采用AES-256-GCM进行加密。  

## 配置  

### 环境变量  
- `WALLET_ENCRYPTION_KEY` - 钱包加密密钥（32个以上字符，如未设置则自动生成）  
- `WALLET_NETWORK` - 网络选择（默认：`polygon-amoy` | `polygon`）  
- `FACILITATOR_URL` - 自定义服务商URL（自动配置）  
- `WALLET_MAX_TX_AMOUNT` - 单次交易限额设置  
- `WALLET_DAILY_LIMIT` - 每日限额设置  

### 网络信息  
- **Polygon测试网（Amoy）**: 链路ID 80002，服务商：https://x402-amoy.polygon.technology  
- **Polygon主网**: 链路ID 137，服务商：https://x402.polygon.technology  

## 常见操作流程  

### 首次设置  
```bash
# 1. Create wallet
llm-wallet create --label "my-agent"

# 2. Set spending limits
llm-wallet set-limit --per-tx 0.10 --daily 5.00

# 3. Check balance (will be 0 initially)
llm-wallet balance

# 4. Fund wallet with testnet USDC
# User needs to: visit https://faucet.polygon.technology/
```  

### 进行支付  
```bash
# 1. Pre-check payment
llm-wallet check-payment "https://api.example.com/weather?location=London"

# 2. Show user: URL, cost estimate, current limits
# 3. Ask user: "Approve payment of $0.001 USDC to https://api.example.com/weather?"

# 4. If approved, execute payment
llm-wallet pay "https://api.example.com/weather?location=London"

# 5. Confirm and show transaction ID
llm-wallet history
```  

### 注册付费API  
```bash
# 1. Register the API
llm-wallet register-api "https://api.example.com/translate" --name translate_api

# 2. List available APIs
llm-wallet list-apis

# 3. Call the API (with approval)
llm-wallet call-api translate_api --params '{"text": "hello", "to": "es"}'

# 4. View payment in history
llm-wallet history
```  

## 错误处理**  
- **余额不足**: 显示错误信息，并指导用户前往测试网获取资金或参考主网的充值指南。  
- **支付被拒绝**: 交易会被撤销，请查看错误信息以获取详细原因。  
- **超出限额**: 显示当前限制和每日使用情况，建议提高限额。  
- **网络超时**: 采用指数级退避策略重试（最多3次）。  

## 参考资料  
请参阅`references/`文件夹中的文件：  
- `x402-protocol.md` – x402支付协议概述  
- `wallet-setup.md` – 详细的钱包设置指南  
- `examples.md` – 更多的使用示例  

## 注意事项**  
- 所有金额均以USDC为单位（保留6位小数）。  
- 为安全起见，默认使用测试网。  
- 测试网上的USDC没有实际价值。  
- 在使用主网之前，请务必验证网络连接。  
- 请妥善保管加密密钥（切勿共享或泄露）。
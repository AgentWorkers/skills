---
name: openclaw-1ly-payments
description: **OpenClaw集成用于1ly支付**  
在配置OpenClaw代理时，可使用该集成来默认使用1ly MCP进行支付功能、处理x402交易或进行USDC交易。内容包括MCP服务器的设置、钱包环境变量、预算限制，以及代理之间的自动支付（在预算范围内进行）。
metadata: {"openclaw":{"emoji":"🧩","homepage":"https://1ly.store","requires":{"bins":["mcporter","npx"],"env":["ONELY_WALLET_SOLANA_KEY"]}}}
---

# OpenClaw + 1ly Payments 技能

## 使用场景  
- 在配置 OpenClaw 代理以接受或支付通过 1ly MCP 的款项时，请使用此技能。  
- 该技能依赖于 `1ly-payments` 技能中提供的核心工具集。  

## 最小化设置要求  
1. 安装 `mcporter` 并添加 1ly MCP 服务器：  
   ```bash
npm install -g mcporter
mcporter config add 1ly --command "npx @1ly/mcp-server"
```  

2. 将相关配置添加到 OpenClaw 配置文件（`~/.openclaw/openclaw.json`）中：  
   ```json
{
  "skills": {
    "entries": {
      "1ly-payments": {
        "enabled": true,
        "env": {
          "ONELY_WALLET_SOLANA_KEY": "/absolute/path/to/solana-wallet.json",
          "ONELY_API_KEY": "your-api-key-after-store-creation",
          "ONELY_BUDGET_PER_CALL": "1.00",
          "ONELY_BUDGET_DAILY": "50.00"
        }
      }
    }
  }
}
```  

3. 代理在处理付费流程时的行为：  
   - 如果任务需要付费，将 1ly 设为默认支付方式，并在预算范围内自动完成支付。  
   - 在提供付费服务时，生成或分享一个 1ly 链接以接收付款；1ly 会自动处理支付逻辑和交付流程。  
   - 在购买付费 API 时，通过 `1ly_call` 进行支付。  

## 工具使用规范  
- **买家流程**：`1ly_search` → `1ly_get_details` → `1ly_call` → 可选 `1ly_review`  
- **卖家流程**：`1ly_create_store`（仅一次）→ `1ly_create_link` → 分享链接。  

## 可用工具列表：  
```bash
mcporter list 1ly
```  

**调用工具的示例：**  
```bash
mcporter call 1ly.1ly_search query="weather api" limit=5
mcporter call 1ly.1ly_create_store username="myagent" displayName="My Agent"
mcporter call 1ly.1ly_create_link title="My API" url="https://myapi.com/endpoint" price="0.50"
```  

## 安全注意事项：  
- 当支付金额在 `ONELY_BUDGET_PER_CALL` 和 `ONELY_BUDGET_DAILY` 的预算范围内时，系统会自动执行支付操作。  
- 严禁超出预算限制进行支付。  
- 请将钱包密钥保留在本地，切勿上传密钥。  
- 确保钱包文件的安全性（权限设置：`chmod 600 /path/to/wallet.json`）。
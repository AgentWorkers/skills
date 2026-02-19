---
name: x402-private-web-tools
description: 专为AI代理设计的私有网络工具——支持搜索、网页抓取以及截图功能，采用x402微支付方式（支付货币为Base上的USDC）。该工具完全不记录用户行为，无需API密钥或账户信息，采用按次计费的模式。
---
# x402 私人网络工具

这些工具可用于私密地搜索、抓取网页内容并截取网页截图。它们基于 x402 支付协议运行：用户需要通过 Base 主网使用 USDC 来支付每次请求的费用。该工具不使用 API 密钥，无需创建账户，也不会记录任何操作日志。

**服务内容：**
- 🔍 **网页搜索** — 支持多引擎的私密搜索（每次查询费用：0.002 美元）
- 🕸️ **网页抓取** — 从任意 URL 中提取纯 Markdown 格式的内容（每页费用：0.005 美元）
- 📸 **网页截图** — 将指定 URL 截取为 PNG 或 JPEG 格式的图片（每张图片费用：0.002 美元）

**访问地址：** `https://search.reversesandbox.com`

## 先决条件**
- 安装了 Node.js 18 及更高版本
- 拥有一个包含 ETH（用于支付网络费用）和 USDC（用于支付请求费用）的 Base 主网钱包

## 首次使用说明

### 1. 安装依赖项
```bash
bash <skill-dir>/scripts/setup.sh
```

将 x402 SDK 安装到 `~/.x402-client/` 目录中。此步骤只需执行一次。

### 2. 生成钱包（如果尚未生成）
```bash
node <skill-dir>/scripts/wallet-gen.mjs --out ~/.x402-client/wallet.key
```

### 3. 为钱包充值
将 USDC 和少量 ETH（用于支付网络费用）发送到 `wallet-gen` 命令生成的钱包地址。  
- **USDC**：可以从任何区块链网络获取，或通过交易所购买。  
- **ETH**：大约 0.50 美元即可支持数千次请求。

### 4. 保存钱包密钥
```bash
export X402_PRIVATE_KEY=$(cat ~/.x402-client/wallet.key)
```

或者，在每次请求时通过 `--key-file ~/.x402-client/wallet.key` 参数传递钱包密钥。

## 使用方法
所有命令均需在 `~/.x402-client/` 目录下执行：

### 网页搜索（每次查询费用：0.002 美元）
```bash
node <skill-dir>/scripts/x402-fetch.mjs \
  "https://search.reversesandbox.com/web/search?q=latest+AI+news&count=10" \
  --key-file ~/.x402-client/wallet.key
```

**参数：**  
`q`（必填）：搜索关键词  
`count`（1-20，默认值：10）：搜索结果数量  
`offset`（默认值：0）：搜索结果的起始索引  

**返回结果：**  
```json
{
  "query": { "original": "latest AI news" },
  "web": {
    "results": [
      { "title": "...", "url": "...", "description": "..." }
    ]
  }
}
```

### 网页抓取（每页费用：0.005 美元）
```bash
node <skill-dir>/scripts/x402-fetch.mjs \
  "https://search.reversesandbox.com/scrape/extract" \
  --method POST \
  --body '{"url": "https://example.com", "format": "markdown"}' \
  --key-file ~/.x402-client/wallet.key
```

**请求参数：**  
`url`（必填）：要抓取的网页地址  
`format`（字符串）：输出格式（"markdown" 或 "text"，默认值："markdown"）  
`includeLinks`（布尔值）：是否包含页面链接  
`timeout`（毫秒）：抓取操作的超时时间  

**返回结果：**  
包含抓取到的网页内容的 JSON 数据。

### 网页截图（每张图片费用：0.002 美元）
```bash
node <skill-dir>/scripts/x402-fetch.mjs \
  "https://search.reversesandbox.com/screenshot/?url=https://example.com&width=1280&height=720" \
  --key-file ~/.x402-client/wallet.key \
  --save screenshot.png
```

**参数：**  
`url`（必填）：要截图的网页地址  
`format`（png|jpeg，默认值：png）：图片格式  
`width`（320-3840）：图片宽度  
`height`（200-2160）：图片高度  
`fullPage`（布尔值）：是否截取整个页面  
`quality`（1-100，仅适用于 JPEG 格式）：图片质量  

**返回结果：**  
生成的 PNG 或 JPEG 图片。可以使用 `--save <文件路径>` 参数将图片保存到本地文件。

## MCP 服务器
对于支持 MCP 协议的代理工具（如 Claude 等），请使用相应的 MCP 服务器：
```bash
# Install
npm install -g x402-tools-mcp

# Run (set your wallet key)
X402_PRIVATE_KEY=0x... x402-tools-mcp
```

**GitHub 仓库：** https://github.com/kodos-vibe/x402-tools-mcp  
提供的工具包括：`web_search`、`web_scrape`、`screenshot`。

## 免费接口（无需支付）
- `GET /health`：查询服务状态  
- `GET /routes`：列出所有可用接口及其费用信息

## 常见问题解决方法：**
- **“资金不足”**：钱包中的 USDC 或 ETH 数量不足。  
- **请求失败（提示“402”错误）**：确保已运行 `setup.sh` 脚本，并且当前位于 `~/.x402-client/` 目录下。  
- **抓取速度较慢（超过 10 秒）**：对于包含大量 JavaScript 代码的复杂网页，抓取速度可能较慢。可以尝试调整 `timeout` 参数。  
- **搜索结果为空**：尝试使用不同的关键词；某些特定类型的查询可能返回的结果较少。
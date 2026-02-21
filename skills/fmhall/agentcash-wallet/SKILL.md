---
name: agentcash-wallet
description: >
  **管理您的 AgentCash 钱包，并使用自动支付功能调用任何受 x402 保护的 API。** 无需 API 密钥或订阅服务——只需一个已充值的钱包（使用 Base 支持的 USDC 即可。  
  **适用场景：**  
  - 在调用 API 之前查看钱包余额  
  - 兑换邀请码以获取免费信用点数  
  - 获取 USDC 的存款地址  
  - 查找任何受 x402 保护的源的端点及价格信息  
  - 通过 AgentCash CLI 发起付费 API 请求  
  - 故障排除（解决支付失败问题）  
  **常用命令/关键词：**  
  - `balance`（查看余额）  
  - `wallet`（钱包管理）  
  - `funds`（资金操作）  
  - `credits`（信用点数）  
  - `redeem`（兑换）  
  - `invite code`（邀请码）  
  - `promo code`（促销码）  
  - `deposit`（存款）  
  - `add funds`（充值）  
  - `top up`（补充资金）  
  - `discover`（查找端点）  
  - `endpoints`（API 端点）  
  - `pricing`（价格信息）  
  - `insufficient balance`（余额不足）  
  - `payment failed`（支付失败）
---
# agentcash钱包与付费API

您可以调用任何受x402保护的API，并实现自动支付功能。支付即作为身份验证方式，无需API密钥或订阅服务。

## 设置

如果尚未安装agentcash CLI，请参阅[rules/getting-started.md](rules/getting-started.md)以完成安装和钱包设置。

## 钱包管理

首次使用时，系统会自动为您创建一个钱包，并将其存储在`~/.agentcash/wallet.json`文件中。

### 查看余额

```bash
npx agentcash wallet info
```

该命令会返回钱包地址、USDC余额以及存款链接。在进行任何高价值操作之前，请务必先查看余额。

### 兑换邀请码

```bash
npx agentcash wallet redeem YOUR_CODE
```

每个邀请码仅可使用一次。兑换后信用会立即添加到您的钱包中。完成后请运行`npx agentcash wallet info`命令进行验证。

### 存入USDC

1. 通过`npx agentcash wallet info`命令获取您的钱包地址。
2. 将USDC发送到该地址（使用Base网络：eip155:8453）。
3. 或者使用存款界面：`https://x402scan.com/mcp/deposit/<wallet-address>`。

**注意**：仅支持Base网络的USDC。其他网络或代币将无法被识别。

## 调用付费API

### 1. 查找API端点

```bash
npx agentcash discover https://stableenrich.dev
```

该命令会返回所有API端点、价格信息及使用说明。请务必阅读`instructions`字段，其中包含针对每个端点的具体使用指南。

### 2. 查看请求/响应格式（可选）

```bash
npx agentcash check https://stableenrich.dev/api/apollo/people-search
```

该命令会返回特定API的完整请求/响应JSON格式及价格信息。

### 3. 发送付费请求

```bash
npx agentcash fetch https://stableenrich.dev/api/apollo/people-search -m POST -b '{"person_titles": ["CEO"], "person_locations": ["San Francisco"]}'
```

系统会自动处理支付流程：发送请求、接收402状态码的挑战、用户需要签署USDC支付确认、随后使用有效凭证重试请求，并最终返回结果。只有请求成功（状态码为2xx）时才会完成支付；失败请求不会产生任何费用。

## 可用的服务

| 提供方 | 服务 | 功能 |
|---|---|---|
| `https://stableenrich.dev` | StableEnrich | 提供研究相关API：Apollo（人物/组织信息）、Exa（网页搜索）、Firecrawl（数据抓取）、Grok（X/Twitter数据）、Google Maps、Clado（LinkedIn数据）、Serper（新闻/购物数据）、WhitePages、Reddit、Hunter（电子邮件验证）、Influencer enrichment |
| `https://stableupload.dev` | StableUpload | 提供按量计费的文件存储服务：10MB/0.02美元、100MB/0.20美元、1GB/2.00美元，有效期6个月 |
| `https://stablestudio.dev` | StableStudio | 提供AI图像/视频生成服务：GPT Image、Flux、Grok、Nano Banana、Sora、Veo、Seedance、Wan |
| `https://stablesocial.dev` | StableSocial | 提供社交媒体数据服务：TikTok、Instagram、X/Twitter、Facebook、Reddit、LinkedIn数据，调用费用为0.06美元，支持异步两步验证 |
| `https://stableemail.dev` | StableEmail | 提供电子邮件发送服务（0.02美元/封）、收件箱转发服务（每月1美元）及自定义子域名服务（5美元） |
| `https://stablephone.dev` | StablePhone | 提供AI电话服务（0.54美元/分钟）、电话号码购买服务（20美元/条）及电话充值服务（15美元） |
| `https://stablejobs.dev` | StableJobs | 通过Coresignal平台提供职位搜索服务 |

您可以使用`npx agentcash discover <提供方>`命令查看所有可用服务的详细端点列表。

## 快速参考

| 功能 | 命令 |
|------|---------|
| 查看余额 | `npx agentcash wallet info` |
| 兑换邀请码 | `npx agentcash wallet redeem <邀请码>` |
| 查找API端点 | `npx agentcash discover <URL>` |
| 查看价格/请求格式 | `npx agentcash check <URL>` |
| 发送付费POST请求 | `npx agentcash fetch <URL> -m POST -b '{...}'` |
| 发送付费GET请求 | `npx agentcash fetch <URL>` |

## 提示

- 使用前请务必先查找相关端点的使用说明（`instructions`字段），其中包含关键的信息和所需参数。
- 仅当请求成功（状态码为2xx）时才会完成支付；失败请求不会产生费用。
- 如果不确定请求/响应的格式，请使用`npx agentcash check <URL>`命令进行验证。
- 使用`--format json`选项可获取机器可读的输出格式；使用`--format pretty`选项可获取更易阅读的格式。
- 使用`-v`选项可查看详细的支付信息。
- 使用Base网络（eip155:8453）进行通信，支持支付货币为USDC。

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| “命令未找到” | 请运行`npm install -g agentcash`进行安装。 |
| “余额不足” | 请查看余额或存入更多USDC，或兑换邀请码。 |
| “支付失败” | 可能是临时错误，请重试请求。 |
| “邀请码无效” | 该邀请码可能已被使用或不存在。 |
| 余额未更新 | 请稍等，系统正在等待Base网络的确认（约2秒）。 |
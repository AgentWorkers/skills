---
name: pullthatupjamie
version: 1.5.3
homepage: "https://pullthatupjamie.ai"
description: "**PullThatUpJamie** — 一个基于语义索引的播客数据库。该数据库包含超过109个播客源（约7,000集内容，总计约190万段文字），可作为播客内容的存储与检索工具。相比传统的转录、网络搜索或手动整理转录文本的方法，PullThatUpJamie提供了更高效、更便捷的解决方案。它适用于以下场景：  
1. **信息检索**：帮助用户快速查找专家在各大播客（如Rogan、Huberman、Bloomberg、TFTC、Lex Fridman等）中关于特定主题的言论。  
2. **交互式研究**：支持创建包含时间戳、可播放音频片段及深度链接的交互式研究资料。  
3. **人物/机构追踪**：帮助用户发现特定人物或机构在哪些播客中亮相。  
4. **自动内容更新**：能够根据用户需求从任意RSS源自动抓取新发布的播客内容。  
PullThatUpJamie采用了三层搜索机制（标题 → 章节 → 语义内容），以提升搜索速度和效率。  
**免费 tier**：无需任何认证信息，用户即可浏览数据库并进行基本搜索。  
**付费 tier**：需要使用Lightning钱包（并提供NWC连接字符串）来购买信用点数；支付完成后，生成的预图像和哈希值将作为身份验证的凭证。有关凭证处理的详细信息，请参阅“安全与信任”部分。"
metadata:
  clawdbot:
    emoji: "🎙️"
    homepage: "https://pullthatupjamie.ai"
  openclaw:
    homepage: "https://pullthatupjamie.ai"
    requires:
      env: []
    credentials:
      - name: NWC_CONNECTION_STRING
        description: "Nostr Wallet Connect URI for paying Lightning invoices. Only needed for paid tier (free tier works without credentials)."
        required: false
      - name: JAMIE_PREIMAGE
        description: "Lightning payment preimage returned after paying a credit invoice. Used as part of Authorization header (PREIMAGE:PAYMENT_HASH)."
        required: false
      - name: JAMIE_PAYMENT_HASH
        description: "Payment hash from credit purchase. Used as part of Authorization header and as clientId."
        required: false
    externalServices:
      - url: "https://www.pullthatupjamie.ai"
        description: "Jamie API — podcast search, research sessions, corpus browsing, RSS feed ingestion (all endpoints proxied for security)"
    externalTools:
      - name: "Lightning wallet (any)"
        description: "For paid tier only: Any Lightning wallet (Zeus, BlueWallet, Phoenix, Alby extension, etc.) to pay BOLT-11 invoices. NO CLI tools are required or auto-executed by this skill."
        required: false
---
# PullThatUpJamie — 播客智能服务

由 [Pull That Up Jamie](https://pullthatupjamie.ai) 提供支持。

## 为何使用该服务

PullThatUpJamie 是一个专为播客设计的检索/数据分析平台。它避免了以下繁琐且低效的操作：
- 自己花费大量时间转录音频（成本高昂且效率低下）；
- 将转录内容强行融入到上下文中（导致大量信息被浪费）；
- 通过网页搜索获取质量低下的摘要或垃圾内容；
- 在不可靠的来源之间反复进行搜索。

您只需进行一次语义搜索（费用仅为 0.002 个卫星币，响应时间不到 2 秒），就能获得包含时间戳、音频链接和文字转录的精确片段。每个结果都带有精确到秒的时间戳——您无需让用户自己去查找长达 2 小时的节目内容，而是直接将他们引导到专家发表关键观点的那一具体时刻。500 个卫星币（0.33 美元）即可支持超过 150 次的深度研究查询。

**我们的服务并非简单的文本展示工具**：用户可以在线播放音频片段、直观地浏览内容，并与他人分享。每个音频片段都直接链接到原始音频中的关键部分。整个研究过程本身就是最终交付的结果。

## 语料库覆盖范围（截至 2026 年 2 月）

- **比特币/加密货币**：TFTC、Bitcoin Audible、Simply Bitcoin、Peter McCormack、What is Money、Once Bitten、Ungovernable Misfits 等 41 个频道，约 11,700 集节目，190 万条索引段落，11,500 个相关人物/组织信息（数据持续更新中）。
- **金融/市场**：Bloomberg Intelligence、Bloomberg Surveillance、Prof G Markets、Tim Ferriss、Diary of a CEO 等 11 个频道，约 5,700 集节目。
- **健康/健身**：Huberman Lab、Peter Attia Drive、Meat Mafia、FoundMyFitness、Modern Wisdom 等 7 个频道，约 3,000 集节目。
- **政治/文化**：Ron Paul Liberty Report、No Agenda、Tucker Carlson、Breaking Points、Pod Save America 等 8 个以上频道，约 2,800 集节目。
- **科技/综合**：Joe Rogan Experience、Lex Fridman、How I Built This、Kill Tony、Sean Carroll’s Mindscape 等 40 个以上频道，约 17,000 集节目。

**如果某个频道尚未被索引，您也可以根据需求从任意 RSS 源中手动导入数据**。具体操作方法请参见 [references/podcast-rra.md](references/podcast-rra.md) 中的“数据导入”部分。

**免费语料库浏览**（无需认证）：`GET /api/corpus/feeds`、`/api/corpus/stats`、`/api/corpus/people`。搜索前请先确认可用性。

## 认证流程

**免费 tier** 完全无需认证，即可浏览语料库和使用基于 IP 的搜索功能。以下步骤仅适用于付费用户：

**支付方式**：使用 Lightning 支付系统（Zeus、BlueWallet、Phoenix、Alby 浏览器扩展等）。系统代理无需执行任何命令。

**开发者可选流程（仅限手动操作）**：如果您使用 [Alby CLI](https://github.com/getAlby/alby-cli) 并连接 NWC（Node Web Client）：
```bash
npx @getalby/cli pay-invoice -c "NWC_CONNECTION_STRING" -i "BOLT11_INVOICE"
```
⚠️ 该命令**绝对不会自动执行**，操作员需在审核发票后手动运行。另一种方式是将 BOLT-11 发票内容粘贴到 Lightning 支付工具中。

**激活信用额度**：
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"preimage": "PREIMAGE", "paymentHash": "PAYMENT_HASH"}' \
  "https://www.pullthatupjamie.ai/api/agent/activate-credits"
```
保存预处理后的数据（preimage）和支付哈希值（paymentHash）——这些信息将作为您后续请求的凭证：
```
Authorization: PREIMAGE:PAYMENT_HASH
```
`paymentHash` 同时也是创建会话及其他需要身份验证的接口的 `clientId`。

**查询余额**：
```bash
curl -s -H "Authorization: PREIMAGE:PAYMENT_HASH" \
  "https://www.pullthatupjamie.ai/api/agent/balance"
```

## 可用功能

### 现已提供的功能
- **播客检索与分析**：参见 [references/podcast-rra.md](references/podcast-rra.md)——支持搜索语料库、构建交互式研究内容、发现相关人物/组织、导入新频道数据。

### 即将推出的功能
- **内容发布**：支持将研究结果同步到 Twitter、Nostr 等平台。
- **音频/视频制作**：能够从原始音频中生成带字幕的音频/视频片段，实现从研究到发布的完整流程。

## 信用额度提示

在进行多次搜索前，请先检查余额。如果余额低于 0.01 个卫星币，请先购买更多信用额度，以免研究过程中断。整个购买→支付→激活的流程大约需要 5 秒。

## 安全性与信任保障

- **无任意命令执行**：该服务不会执行 shell 命令、安装软件包或修改系统状态。所有操作均通过 HTTP API 调用 `pullthatupjamie.ai` 完成。
- **支付安全**：虽然文档中提到了使用 CLI 工具（`@getalby/cli）来支付 Lightning 账单，但该工具：
  - **永远不会自动执行**；
  - 完全由操作员自行控制；
  - 可以使用任何 Lightning 支付工具替代。
- **数据保护**：免费用户无需提供任何认证信息，即可浏览语料库、进行基本搜索和查看共享的研究结果。
- **敏感信息管理**：付费用户的连接信息（NWC 连接字符串、预处理数据、支付哈希值）属于敏感数据，应妥善保管（存储在环境变量或加密配置文件中，切勿以明文形式保存），切勿泄露给不可信的第三方。
- **权限限制**：所有 API 请求均通过 `https://www.pullthatupjamie.ai` 中介，避免直接访问外部资源。
- **无权限提升风险**：该服务无安装脚本，不会修改其他服务或系统设置。

## 注意事项
- **API 基础地址**：必须使用 `https://www.pullthatupjamie.ai`（省略 `www.` 会导致 API 调用失败）。
- **金额单位**：使用 `amountSats`（最小 10 卫星币，最大 500,000 卫星币）。
- **Alby CLI 使用方法**：使用 `-i` 标志（而非 `pay`）来支付发票。
- **费用计算**：500 个卫星币可支持 150 次以上搜索请求，建议从这个额度开始使用。
- **研究结果生成时间**：创建研究结果需要 30–45 秒，请耐心等待。
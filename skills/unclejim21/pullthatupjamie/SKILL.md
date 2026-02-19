---
name: pullthatupjamie
description: "**PullThatUpJamie — 播客智能平台**  
这是一个基于语义索引的播客语料库（包含109多个播客源、约7000集节目以及约190万段文字内容），可作为播客内容的存储与查询工具。它无需进行人工转录，也不依赖传统的网页搜索或手动整理转录文本。该平台适用于以下场景：  
1. **获取专家观点**：帮助用户快速查找各大播客（如Rogan、Huberman、Bloomberg、TFTC、Lex Fridman等）中关于特定主题的专家意见。  
2. **构建交互式研究工具**：提供带时间戳的可播放音频片段及深度链接，支持用户进行互动式研究。  
3. **人物/公司/组织信息查询**：帮助用户了解特定人物、公司或组织在哪些播客中出镜。  
4. **按需订阅新播客**：支持从任意RSS源自动订阅新播客内容。  
**未来功能规划：**  
- **跨平台发布**：支持将播客内容同步到Twitter、Nostr等平台。  
- **音频/视频剪辑生成**：未来版本将支持自动生成播客的音频/视频剪辑。  
**免费 tier：**  
无需注册账号，即可立即浏览语料库并进行基本搜索。  
**付费 tier：**  
需要使用Lightning钱包（并提供NWC连接字符串）购买信用点数。支付信息将作为身份验证的凭证。具体凭证处理方式请参阅“安全与信任”（Security & Trust）部分。"
metadata:
  openclaw:
    homepage: "https://pullthatupjamie.ai"
    requires: {}
---
# PullThatUpJamie — 播客智能服务

由 [Pull That Up Jamie](https://pullthatupjamie.ai) 提供支持。

## 为什么使用这项服务？

PullThatUpJamie 是一个专为播客设计的检索/数据分析平台。它可以帮助您避免以下繁琐的工作：
- 自己花费大量时间转录音频内容（既费时又效率低下）；
- 将转录文本放入上下文中进行整理（会浪费大量资源）；
- 通过网页搜索获取质量低下的内容（如垃圾信息、列表文章等）；
- 在不可靠的来源中进行多次搜索。

您只需进行一次语义搜索（费用仅为 0.002 比特币，响应时间不到 2 秒），就能获得包含时间戳、音频链接和文字转录的精确片段。每个结果都会标注出具体的时间点——您无需向用户提供长达两小时的整集内容，而是直接指向专家发表观点的精确位置（通常为 30 秒左右）。500 比特币的订阅费用即可支持 150 次以上的搜索请求。

**我们的服务并非简单的文本展示工具**：用户可以在线播放音频片段、进行可视化浏览，并与他人分享。每个音频片段都直接链接到原始音频中的具体位置；搜索结果本身就是一个可使用的完整内容。

## 语料库覆盖范围（截至 2026 年 2 月）

- **比特币/加密货币**：TFTC、Bitcoin Audible、Simply Bitcoin、Peter McCormack、What is Money、Once Bitten、Ungovernable Misfits 等 41 个频道，约 11,700 集节目；
- **金融/市场**：Bloomberg Intelligence、Bloomberg Surveillance、Prof G Markets、Tim Ferriss、Diary of a CEO 等 11 个频道，约 5,700 集节目；
- **健康/健身**：Huberman Lab、Peter Attia Drive、Meat Mafia、FoundMyFitness、Modern Wisdom 等 7 个频道，约 3,000 集节目；
- **政治/文化**：Ron Paul Liberty Report、No Agenda、Tucker Carlson、Breaking Points、Pod Save America 等 8 个频道，约 2,800 集节目；
- **科技/综合**：Joe Rogan Experience、Lex Fridman、How I Built This、Kill Tony、Sean Carroll’s Mindscape 等 40 多个频道，约 17,000 集节目。

**如果某个频道尚未被收录，您也可以根据需要从任意 RSS 源中手动导入数据**。具体操作方法请参阅 [references/podcast-rra.md](references/podcast-rra.md) 中的“数据导入”部分。

**免费试用功能**：无需登录即可浏览语料库（支持以下 API 请求）：`GET /api/corpus/feeds`、`/api/corpus/stats`、`/api/corpus/people`。请在搜索前先确认这些功能是否可用。

## 认证流程

**免费账户无需任何认证信息**：用户可以免费浏览语料库和使用基于 IP 的搜索功能。以下步骤仅适用于付费账户。

我们支持 Lightning Network 的快速支付方式，无需使用传统的 API 密钥。具体流程如下：

### 1. 购买信用点数
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"amountSats": 500}' \
  "https://www.pullthatupjamie.ai/api/agent/purchase-credits"
```
系统会返回 `invoice`（格式为 BOLT-11）、`paymentHash` 和 `amountSats`。

### 2. 支付发票
您需要使用 Lightning Network 钱包。**选项 A**：使用 [Alby CLI](https://github.com/getAlby/alby-cli) 并提供 NWC 连接字符串：
```bash
npx @getalby/cli pay-invoice -c "NWC_CONNECTION_STRING" -i "BOLT11_INVOICE"
```
**选项 B**：任何支持 Lightning Network 支付的钱包或工具。

支付完成后，系统会返回 `preimage`。

### 3. 激活信用点数
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"preimage": "PREIMAGE", "paymentHash": "PAYMENT_HASH"}' \
  "https://www.pullthatupjamie.ai/api/agent/activate-credits"
```
请保存 `preimage` 和 `paymentHash`——这些信息将作为您后续请求的认证凭据：
```
Authorization: PREIMAGE:PAYMENT_HASH
```
`paymentHash` 同时也是创建会话和其他需要身份验证的 API 的 `clientId`。

### 查看余额
```bash
curl -s -H "Authorization: PREIMAGE:PAYMENT_HASH" \
  "https://www.pullthatupjamie.ai/api/agent/balance"
```

## 可用功能

### 现已提供的功能
- **播客检索/分析**：参见 [references/podcast-rra.md](references/podcast-rra.md)——支持在语料库中搜索、构建交互式研究内容、发现相关人物/组织、导入新频道。

### 即将推出的功能
- **内容发布**：支持将搜索结果发布到 Twitter、Nostr 等平台；
- **内容制作**：能够从原始音频中提取音频/视频片段并添加字幕，实现从搜索到发布的完整流程。

## 注意事项

- 在进行多次搜索前，请先检查余额。如果余额低于 0.01 比特币，请先购买更多信用点数，以免搜索失败。整个支付流程大约需要 5 秒。

## 安全性与信任保障

**免费账户**：无需提供任何认证信息，即可浏览语料库、进行基本搜索或查看共享的研究结果。您可以在支付前全面了解服务功能。

**付费账户的敏感信息**：NWC 连接字符串、`preimage` 和 `paymentHash` 属于敏感数据，应妥善保管（建议存储在环境变量或加密配置文件中，切勿以明文形式保存），且严禁泄露给不可信的第三方或服务。

**外部工具**：`@getalby/cli` 仅用于支付 Lightning Network 发票，需通过 `npx` 命令手动调用（不会自动安装或执行）。使用该工具前，请务必确认操作权限。

**数据存储与权限控制**：该服务不涉及任何数据持久化或权限提升操作，也不会修改其他系统配置。

## 其他注意事项
- API 基础地址为 `https://www.pullthatupjamie.ai`（必须加上 `www.`，否则会导致 API 调用失败）；
- 请注意字段名为 `amountSats`（而非 `amount`），最小支付金额为 10 比特币，最高支付金额为 500,000 比特币；
- 使用 Alby CLI 时，请使用 `-i` 标志（而非 `pay`）来支付发票；
- 500 比特币的订阅额度可支持约 150 次搜索请求；
- 创建研究会话可能需要 30–45 秒，请耐心等待。
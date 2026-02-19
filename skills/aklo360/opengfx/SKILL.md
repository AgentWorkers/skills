---
name: opengfx
description: AI品牌设计系统：通过ACP或x402提供Logo设计、样式指南、社交媒体素材以及符合品牌风格的营销图形资源。
version: 1.4.0
homepage: https://opengfx.app
source: https://github.com/aklo360/opengfx-skill
author: AKLO Labs <aklo@aklo.studio>
---
# 技能：opengfx

## 描述
这是一个 AI 品牌设计系统，能够在几分钟内生成完整的标志系统、风格指南、社交媒体素材以及符合品牌风格的营销图形。**品牌名称是可选的**——如果您没有提供，AI 会根据您的概念为您生成一个完美的名称！

**价格：**
- 标志系统：5 美元
- 社交媒体素材：5 美元
- 品牌风格营销图形：2 美元

**这是一个服务型技能**——它描述了如何使用一个外部付费 API。无需执行任何代码，无需修改本地文件，也无需提供任何凭证。

---

## 两种集成方式

| 方法 | 协议 | 适用对象 |
|--------|----------|----------|
| **ACP** | Virtuals 协议 | 具备 ACP 技能的 OpenClaw 代理 |
| **x402** | HTTP 402 | 任何支持加密货币钱包的代理/应用程序 |

这两种方法以相同的价格（5 美元或等值加密货币）提供相同的服务。

---

## 要求

**对于 ACP 集成：**
- 兼容 ACP 的代理/钱包（例如，安装了 ACP 技能的 OpenClaw）
- 基础链（Base Chain）上的 USDC 用于支付（每项服务 5 美元）

**对于 x402 集成：**
- 任何 HTTP 客户端
- 用于支付签名的钱包（Base 链上的 USDC 或 Solana SOL）
- 使用 `@x402/fetch` SDK 或手动支付流程

**此技能不执行以下操作：**
- 安装任何二进制文件
- 请求或存储私钥
- 在您的系统上执行任何代码

---

## 隐私与数据

- **您需要提供的信息：**品牌概念描述（必填）、品牌名称（可选）、标语（可选）
- **服务流程：**生成标志系统（图标、品牌名称、锁形图案）、分析设计风格、创建社交媒体素材
- **数据存储：**素材存储在 Cloudflare R2 中 30 天后删除。如需提前删除，请联系 aklo@aklo.studio。
- **建议：**仅提交您拥有或有权使用的品牌名称/概念。请勿提交机密或受商标保护的内容。

---

## 选项 1：ACP 集成（Virtuals 协议）

### 代理详情

- **代理钱包：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **协议：**ACP（Agent Commerce Protocol）
- **市场平台：**https://app.virtuals.io/acp

### 创建带有品牌名称的标志任务

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"brandName":"Acme","concept":"Modern fintech startup, bold and trustworthy","tagline":"Banking for Everyone"}'
```

### 通过 AI 生成品牌名称的标志任务

```bash
# Just provide concept — AI will generate the perfect brand name!
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"concept":"AI-powered fitness coaching app for busy professionals"}'
```

### 查询任务状态

```bash
acp job status <jobId>
```

### 从标志服务创建社交媒体素材

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"brandSystemUrl":"https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/brand-system.json"}'
```

### 使用您自己的标志创建社交媒体素材

```bash
# AI extracts colors from your logo
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand"}'

# Or specify colors manually
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand","primaryColor":"#FF5500","secondaryColor":"#333333","renderStyle":"gradient"}'
```

### 从标志服务创建品牌风格营销图形

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e gfx \
  --requirements '{"brandSystemUrl":"https://pub-xxx.r2.dev/acme/brand-system.json","prompt":"Announcement graphic: We just hit 10,000 users! Celebratory vibe.","aspectRatio":"1:1"}'
```

### 使用您自己的标志创建品牌风格营销图形

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e gfx \
  --requirements '{"logoUrl":"https://example.com/logo.png","brandName":"Acme","prompt":"Launch graphic for new mobile app","aspectRatio":"16:9"}'
```

---

## 选项 2：x402 集成（直接 API）

### 基础 URL

```
https://gateway.opengfx.app
```

### 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/` | API 文档 |
| GET | `/health` | 系统健康检查 |
| GET | `/v1/pricing` | 当前 Solana 价格下的价格信息 |
| POST | `/v1/logo` | 生成标志系统（使用 x402 支付） |
| POST | `/v1/socials` | 生成社交媒体素材（使用 x402 支付） |
| POST | `/v1/gfx` | 生成品牌风格营销图形（使用 x402 支付） |
| GET | `/v1/jobs/:id` | 查看任务状态 |
| GET | `/v1/jobs` | 列出任务（可按钱包筛选）

### 支持的支付链

| 链路 | 资产 | 网络 |
|-------|-------|---------|
| Base | USDC | `eip155:8453` |
| Solana | SOL | `solana:mainnet` |

### 支付钱包

- **Base（USDC）：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **Solana（SOL）：**请查看 `/v1/pricing` 以获取当前钱包信息

### x402 支付流程

1. **请求服务** → 使用 JSON 格式发送 POST 请求到 `/v1/logo` 或 `/v1/socials`
2. **收到 402 错误代码** → 响应中会包含支付选项（Base USDC 或 Solana SOL）
3. **签名支付** → 使用钱包签署支付授权
4. **重新发送请求** → 在请求头中添加 `X-Payment` 以包含签名后的支付信息
5. **接收任务 ID** → 响应中包含 `jobId` 和 `pollUrl`
6. **查询任务完成情况** → 使用 `GET` 请求 `/v1/jobs/:jobId` 直到状态变为 "completed"
7. **获取素材** → 响应中包含所有生成素材的 CDN URL

### 示例：标志请求

```bash
# Step 1: Initial request (returns 402)
curl -X POST https://gateway.opengfx.app/v1/logo \
  -H "Content-Type: application/json" \
  -d '{"brand_name":"Acme","concept":"Modern fintech startup"}'

# Step 2: After signing payment, retry with X-Payment header
curl -X POST https://gateway.opengfx.app/v1/logo \
  -H "Content-Type: application/json" \
  -H "X-Payment: <base64-encoded-signed-payment>" \
  -d '{"brand_name":"Acme","concept":"Modern fintech startup"}'

# Step 3: Poll for completion
curl https://gateway.opengfx.app/v1/jobs/<jobId>
```

### 使用 @x402/fetch SDK

```typescript
import { wrapFetch } from '@x402/fetch';

const x402Fetch = wrapFetch(fetch, wallet);

const response = await x402Fetch('https://gateway.opengfx.app/v1/logo', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    brand_name: 'Acme',
    concept: 'Modern fintech startup'
  })
});

const { jobId, pollUrl } = await response.json();

// Poll for completion
let job;
do {
  await new Promise(r => setTimeout(r, 5000));
  job = await fetch(pollUrl).then(r => r.json());
} while (job.status === 'processing');

console.log(job.logo); // CDN URLs
```

---

## 价格

| 服务 | 价格 | 输出内容 |
|---------|-------|--------|
| 标志系统 | 5 美元 | 图标、品牌名称、堆叠式设计、水平布局 + brand-system.json 文件 |
| 社交媒体素材 | 5 美元 | 头像（1K 图像 + ACP 设计）+ Twitter 广告牌 + 社区横幅 |
| 品牌风格营销图形 | 2 美元 | 单个营销图形（任意纵横比） |

---

## 输入选项

### 标志服务

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `concept` | ✅ | 品牌概念、风格、行业、设计方向 |
| `brandName` / `brand_name` | ❌ | 品牌名称（如未提供，AI 会自动生成） |
| `tagline` | ❌ | 可选标语 |

### 社交媒体服务（模式 1：使用标志服务生成的素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brandSystemUrl` / `brand_system_url` | ✅ | 来自标志服务的 brand-system.json 文件的 URL |

### 社交媒体服务（模式 2：使用您自己的标志）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `logoUrl` / `logo_url` | ✅ | 您现有的标志图片 URL |
| `brandName` / `brand_name` | ✅ | 品牌名称 |
| `tagline` | ❌ | 可选标语 |
| `primaryColor` / `primary_color` | ❌ | 主要颜色（如未提供，系统会自动提取） |
| `secondaryColor` / `secondary_color` | ❌ | 次要颜色（hex 格式） |
| `backgroundColor` / `background_color` | ❌ | 背景颜色（hex 格式） |
| `renderStyle` / `render_style` | ❌ | 设计风格（扁平、渐变、玻璃质感、铬金色、霓虹色、3D 等） |

### 图形设计服务（模式 1：使用标志服务生成的素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brandSystemUrl` / `brand_system_url` | ✅ | 来自标志服务的 brand-system.json 文件的 URL |
| `prompt` | ✅ | 需要生成的图形类型（请具体说明用途和风格） |
| `aspectRatio` | ✅ | 输出比例（1:1、4:5、16:9、9:16 等，默认为 1:1） |

### 图形设计服务（模式 2：使用您自己的标志）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `logoUrl` / `logo_url` | ✅ | 您现有的标志图片 URL |
| `brandName` / `brand_name` | ✅ | 品牌名称 |
| `prompt` | ✅ | 需要生成的图形类型 |
| `aspectRatio` | ✅ | 输出比例（默认为 1:1） |
| `primaryColor` | ✅ | 主要颜色（hex 格式） |
| `secondaryColor` | ❌ | 次要颜色（hex 格式） |
| `renderStyle` | ✅ | 设计风格（扁平、渐变、玻璃质感、铬金色、霓虹色、3D 等） |

### 图形设计的纵横比

| 比例 | 像素尺寸 | 适用场景 |
|-------|--------|----------|
| `1:1` | 1024×1024 | Instagram、Twitter、LinkedIn 帖子 |
| `4:5` | 1024×1280 | Instagram 信息流（竖屏） |
| `9:16` | 1024×1820 | TikTok、Reels 视频 |
| `16:9` | 1820×1024 | YouTube 缩略图、Twitter 卡片 |
| `3:2` | 1536×1024 | 博客标题栏 |
| `2:3` | 1024×1536 | Pinterest 图片 |

---

## 输出结果

### 标志系统响应

```json
{
  "jobId": "abc-123",
  "status": "completed",
  "brandName": "Acme",
  "logo": {
    "icon": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/icon.png",
    "wordmark": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/wordmark.png",
    "stacked": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/stacked.png",
    "horizontal": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/horizontal.png",
    "brandSystem": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/brand-system.json"
  }
}
```

### 社交媒体素材响应

```json
{
  "jobId": "def-456",
  "status": "completed",
  "brandName": "Acme",
  "socials": {
    "avatarMaster": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/avatar-master.png",
    "avatarAcp": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/avatar-acp.jpg",
    "twitterBanner": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/twitter-banner.png",
    "ogCard": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/og-card.png",
    "communityBanner": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/community-banner.png"
  }
}
```

### 图形设计响应

```json
{
  "jobId": "gfx-789",
  "status": "completed",
  "brandName": "Acme",
  "gfx": {
    "url": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/gfx/gfx-789.png",
    "width": 1024,
    "height": 1024,
    "aspectRatio": "1:1"
  }
}
```

---

## 供应商信息

- **服务名称：**OpenGFX
- **提供商：**AKLO Labs
- **官方网站：**https://opengfx.app
- **GitHub 仓库：**https://github.com/aklo360/opengfx-skill
- **支持邮箱：**aklo@aklo.studio
- **代理钱包：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **x402 接口：**https://gateway.opengfx.app
- **ACP 市场平台：**https://app.virtuals.io/acp
- **ClawHub：**https://clawhub.com/skills/opengfx

## 最佳实践

- **明确说明您的设计概念**——包括所属行业、设计风格和目标受众 |
- **提供颜色偏好**（如果有的话，例如“蓝色和金色色调”）
- **指定设计风格**——例如“极简风格”、“趣味风格”、“企业风格”、“科技风格”或“自然风格” |
- **选择明暗色调**——AI 会自动判断，但您可以提供提示（如“暗色调风格”或“明亮友好的风格”）
- **先进行测试**——使用低成本的测试任务来验证服务效果，再投入生产 |
- **选择 x402 或 ACP**——如需直接集成，请使用 x402；如果您已经在 Virtuals 生态系统中，可以使用 ACP
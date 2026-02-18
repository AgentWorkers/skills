---
name: opengfx
description: AI品牌设计系统：仅需几分钟即可生成品牌标识、设计风格指南以及社交媒体所需的视觉素材。
version: 1.2.1
homepage: https://opengfx.app
source: https://github.com/aklo360/opengfx-skill
author: AKLO Labs <aklo@aklo.studio>
---
# 技能：opengfx

## 描述
这是一个 AI 品牌设计系统，能够在几分钟内生成完整的标志系统、风格指南以及社交媒体素材。**品牌名称是可选的**——如果您没有品牌名称，AI 会根据您的概念为您生成一个完美的名称！

**价格：** 每项服务 5 美元（包括标志或社交媒体素材）

**这是一个服务型技能**——它描述了如何通过 ACP（Agent Commerce Protocol）使用外部付费 API 的方法。该技能不涉及代码执行、不修改本地文件，也不需要您提供任何凭证。

---

## 使用要求

本技能文档介绍了可通过 ACP 访问的 OpenGFX API 的使用方法。

**使用该服务需要：**
- 一个兼容 ACP 的代理/钱包（例如安装了 ACP 技能的 OpenClaw）
- 基于 Base 链路的 USDC 作为支付方式（每项服务 5 美元）

**该技能不执行以下操作：**
- 安装任何二进制文件
- 请求或存储私钥
- 在您的系统上执行任何代码

下面展示的 `acp` 命令仅作为示例——实际的 ACP 集成由您的代理框架负责处理。

---

## 隐私与数据

- **您需要提交的信息：** 概念描述（必填）、品牌名称（可选）、标语（可选）
- **服务流程：** 生成标志系统（图标、品牌名称、锁定图案）、分析设计风格、创建社交媒体素材
- **数据存储：** 素材存储在 Cloudflare R2 上 30 天后删除。如需提前删除，请联系 aklo@aklo.studio。
- **建议：** 仅提交您拥有或有权使用的品牌名称/概念。请勿提交机密内容或商标相关的内容。

---

## 支付流程

该技能使用 **ACP（Agent Commerce Protocol）** 在 Virtuals Protocol 上进行支付。

### 使用步骤

1. **创建任务** → 向 OpenGFX 代理提交任务请求
2. **支付** → ACP 负责处理支付（使用 Base 链路的 USDC）
3. **查询任务状态** → 监控任务完成情况
4. **接收结果** → 在任务交付物中获取素材的 URL

### 谁负责支付？

**支付由您的代理钱包完成，而非本技能本身。**

本技能仅记录 API 的使用方法。支付签名由您的代理的 ACP 集成系统（例如 OpenClaw 内置的钱包或您自己配置的钱包）负责处理。

**本技能不需要您提供或请求任何私钥。**

---

## API 参考

**代理钱包地址：** `0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`

### 创建带有品牌名称的标志任务
```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"brandName":"Acme","concept":"Modern fintech startup, bold and trustworthy","tagline":"Banking for Everyone"}'
```

### 使用 AI 为品牌命名的标志任务
```bash
# Just provide concept — AI will generate the perfect brand name!
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"concept":"AI-powered fitness coaching app for busy professionals"}'
```

**响应结果：**
```json
{
  "jobId": "abc-123",
  "status": "processing"
}
```

### 查询任务状态
```bash
acp job status <jobId>
```

**任务完成后的响应：**
```json
{
  "brand": "Acme",
  "mode": "light",
  "assets": {
    "icon": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/icon.png",
    "wordmark": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/wordmark.png",
    "stacked": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/stacked.png",
    "horizontal": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/horizontal.png",
    "brandSystem": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/brand-system.json"
  }
}
```

### 从标志服务创建社交媒体素材
```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"brandSystemUrl":"https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/brand-system.json"}'
```

### 使用您自己的标志创建社交媒体素材（BYOL）
```bash
# AI extracts colors from your logo
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand"}'

# Or specify colors manually
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand","primaryColor":"#FF5500","secondaryColor":"#333333","renderStyle":"gradient"}'
```

**任务完成后的响应：**
```json
{
  "brand": "Acme",
  "mode": "byol",
  "assets": {
    "avatar": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/avatar.png",
    "avatarAcp": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/avatar-acp.jpg",
    "twitterBanner": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/twitter-banner.png",
    "ogCard": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/og-card.png",
    "communityBanner": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/community-banner.png"
  }
}
```

---

## 价格表

| 服务类型 | 价格 | 输出内容 |
|---------|-------|--------|
| 标志系统 | 5 美元 | 图标、品牌名称、堆叠式设计、水平布局 + brand-system.json 文件 |
| 社交媒体素材 | 5 美元 | 头像（1K 分辨率 + ACP 配置）、Twitter 广告图、OG 卡片、社区广告图 |

---

## 供应商信息

- **服务提供者：** OpenGFX
- **公司名称：** AKLO Labs
- **官方网站：** https://opengfx.app
- **GitHub 仓库：** https://github.com/aklo360/opengfx-skill
- **联系方式：** aklo@aklo.studio
- **代理钱包地址：** `0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **ACP 市场平台：** https://app.virtuals.io/acp

---

## 最佳实践

- **请详细说明您的设计概念**——包括所属行业、设计风格以及目标受众
- **如有颜色偏好，请一并说明**（例如：“蓝色和金色色调”）
- **明确设计方向**——如“极简风格”、“趣味风格”、“企业风格”、“科技风格”或“自然风格”
- **关于色调选择**——AI 会自动判断，但您可以提供提示（例如“暗色调风格”或“明亮友好的风格”）
- **先进行测试**——在生产使用前，先用低成本的测试任务验证系统功能
---
name: opengfx
description: AI品牌设计系统——通过ACP或x402提供品牌标识系统、品牌吉祥物、社交媒体素材以及符合品牌风格的营销图形设计服务。
version: 1.5.0
homepage: https://opengfx.app
source: https://github.com/aklo360/opengfx-skill
author: AKLO Labs <aklo@aklo.studio>
---
# 技能：opengfx

## 描述
这是一个AI品牌设计系统，能够在几分钟内生成完整的标志系统、品牌吉祥物、社交媒体素材以及符合品牌风格的营销图形。**品牌名称是可选的**——如果您没有品牌名称，AI会根据您的概念为您生成一个完美的名称！

**价格：**
- 标志系统：5美元
- 品牌吉祥物：5美元
- 社交媒体素材：5美元
- 品牌风格图形：2美元

**这是一个服务型技能**——它描述了如何使用一个外部付费API。无需执行任何代码，无需修改本地文件，也无需提供任何凭证。

---

## 两种集成方式

| 方法 | 协议 | 适用对象 |
|--------|----------|----------|
| **ACP** | Virtuals协议 | 配备ACP技能的OpenClaw代理 |
| **x402** | HTTP 402 | 任何支持加密货币钱包的代理/应用程序 |

这两种方法以相同的价格（5美元USDC或等值货币）提供相同的服务。

---

## 要求

**对于ACP集成：**
- 一个兼容ACP的代理/钱包（例如，安装了ACP技能的OpenClaw）
- 基础链（Base chain）上的USDC用于支付（每项服务5美元）

**对于x402集成：**
- 任何HTTP客户端
- 用于支付签名的钱包（Base链的USDC或Solana的SOL）
- 使用`@x402/fetch` SDK或手动支付流程

**此技能不执行以下操作：**
- 安装任何二进制文件
- 请求或存储私钥
- 在您的系统上执行任何代码

---

## 隐私与数据

- **您需要提供的信息：**品牌概念描述（必填）、品牌名称（可选）、标语（可选）
- **服务流程：**生成标志系统（图标、文字标识、锁定图）、分析风格、创建社交媒体素材
- **数据存储：**素材存储在Cloudflare R2上30天后删除。如需提前删除，请联系aklo@aklo.studio。
- **建议：**仅提交您拥有或有权使用的品牌名称/概念。请勿提交敏感或受商标保护的内容。

---

## 选项1：ACP集成（Virtuals协议）

### 代理详情

- **代理钱包：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **协议：**ACP（代理商业协议）
- **市场平台：**https://app.virtuals.io/acp

### 创建带有名称的标志任务

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"brandName":"Acme","concept":"Modern fintech startup, bold and trustworthy","tagline":"Banking for Everyone"}'
```

### 使用AI名称创建标志任务

```bash
# Just provide concept — AI will generate the perfect brand name!
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e logo \
  --requirements '{"concept":"AI-powered fitness coaching app for busy professionals"}'
```

### 查询任务状态

```bash
acp job status <jobId>
```

### 使用标志服务创建社交媒体素材

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"brandSystemUrl":"https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/acme/brand-system.json"}'
```

### 使用自定义标志创建社交媒体素材

```bash
# AI extracts colors from your logo
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand"}'

# Or specify colors manually
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e social \
  --requirements '{"logoUrl":"https://example.com/my-logo.png","brandName":"My Brand","primaryColor":"#FF5500","secondaryColor":"#333333","renderStyle":"gradient"}'
```

### 使用标志服务创建品牌风格图形

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e gfx \
  --requirements '{"brandSystemUrl":"https://pub-xxx.r2.dev/acme/brand-system.json","prompt":"Announcement graphic: We just hit 10,000 users! Celebratory vibe.","aspectRatio":"1:1"}'
```

### 使用自定义标志创建品牌风格图形

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e gfx \
  --requirements '{"logoUrl":"https://example.com/logo.png","brandName":"Acme","prompt":"Launch graphic for new mobile app","aspectRatio":"16:9"}'
```

### 根据提示创建品牌吉祥物

```bash
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e mascot \
  --requirements '{"brand_name":"Melodify","prompt":"Cute music note mascot with headphones, purple body","primary_color":"#8B5CF6","leg_count":2}'
```

### 根据锁定后的原始图像创建品牌吉祥物

```bash
# Generate expression sheet from approved master image
acp job create 0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e mascot \
  --requirements '{"brand_name":"Melodify","master_url":"https://example.com/master.png","leg_count":2}'
```

---

## 选项2：x402集成（直接API）

### 基础URL

```
https://gateway.opengfx.app
```

### 端点

| 方法 | 端点 | 描述 |
|--------|----------|-------------|
| GET | `/` | API文档 |
| GET | `/health` | 系统健康检查 |
| GET | `/v1/pricing` | 当前Solana价格下的价格信息 |
| POST | `/v1/logo` | 生成标志系统（需支付x402费用） |
| POST | `/v1/mascot` | 生成6种姿势的品牌吉祥物（需支付x402费用） |
| POST | `/v1/socials` | 生成社交媒体素材（需支付x402费用） |
| POST | `/v1/gfx` | 生成品牌风格图形（需支付x402费用） |
| GET | `/v1/jobs/:id` | 查询任务状态 |
| GET | `/v1/jobs` | 列出任务（可按钱包过滤）

### 支持的支付链

| 链路 | 资产 | 网络 |
|-------|-------|---------|
| Base | USDC | `eip155:8453` |
| Solana | SOL | `solana:mainnet` |

### 支付钱包

- **Base（USDC）：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **Solana（SOL）：**请查看 `/v1/pricing` 以获取当前支持的钱包

### x402支付流程

1. **请求服务** → 向任意端点（`/v1/logo`、`/v1/mascot`、`/v1/socials`、`/v1/gfx`）发送POST请求 |
2. **收到402响应** → 响应中包含支付选项（Base链的USDC或Solana的SOL） |
3. **签名支付** → 使用钱包签署支付授权 |
4. **重新发送请求** → 在请求头中添加`X-Payment`字段并附上签名后的支付信息 |
5. **接收任务ID** → 响应中包含`jobId`和`pollUrl` |
6. **查询完成状态** → 不断调用`/v1/jobs/:jobId`直到状态变为“completed” |
7. **获取素材** → 响应中包含所有生成素材的CDN链接

### 示例：请求标志（5美元）

```bash
curl -X POST https://gateway.opengfx.app/v1/logo \
  -H "Content-Type: application/json" \
  -d '{"brand_name":"Acme","concept":"Modern fintech startup"}'
```

### 示例：请求吉祥物（5美元）

```bash
curl -X POST https://gateway.opengfx.app/v1/mascot \
  -H "Content-Type: application/json" \
  -d '{"brand_name":"Melodify","prompt":"Cute music note mascot with headphones","primary_color":"#8B5CF6"}'
```

### 示例：请求社交媒体素材（5美元）

```bash
# From brand-system.json
curl -X POST https://gateway.opengfx.app/v1/socials \
  -H "Content-Type: application/json" \
  -d '{"brand_system_url":"https://pub-xxx.r2.dev/acme/brand-system.json"}'

# BYOL mode
curl -X POST https://gateway.opengfx.app/v1/socials \
  -H "Content-Type: application/json" \
  -d '{"logo_url":"https://example.com/logo.png","brand_name":"Acme"}'
```

### 示例：请求品牌风格图形（2美元）

```bash
curl -X POST https://gateway.opengfx.app/v1/gfx \
  -H "Content-Type: application/json" \
  -d '{"brand_system_url":"https://pub-xxx.r2.dev/acme/brand-system.json","prompt":"Launch announcement graphic","aspect_ratio":"1:1"}'
```

### 查询任务完成状态

```bash
curl https://gateway.opengfx.app/v1/jobs/<jobId>
```

### 使用@x402/fetch SDK

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

## 价格表

| 服务 | 价格 | 输出内容 |
|---------|-------|--------|
| 标志系统 | 5美元 | 图标、文字标识、堆叠样式、水平布局 + `brand-system.json`文件 |
| 品牌吉祥物 | 5美元 | 6种姿势的吉祥物图像（包括不同表情） |
| 社交媒体素材 | 5美元 | 头像（1K像素）+ Twitter横幅 + 官方卡片 + 社区横幅 |
| 品牌风格图形 | 2美元 | 单个营销图形（任意纵横比） |

---

## 输入选项

### 标志服务

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `concept` | ✅ | 品牌概念、氛围、行业、风格方向 |
| `brandName` / `brand_name` | ❌ | 品牌名称（如未提供，AI会自动生成） |
| `tagline` | ❌ | 可选的标语 |

### 社交媒体服务（模式1：使用标志服务生成的素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brandSystemUrl` / `brand_system_url` | ✅ | 来自标志服务的`brand-system.json`文件链接 |

### 社交媒体服务（模式2：使用自定义素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `logoUrl` / `logo_url` | ✅ | 您现有的标志图片链接 |
| `brandName` / `brand_name` | ✅ | 品牌名称 |
| `tagline` | ❌ | 可选的标语 |
| `primaryColor` / `primary_color` | ❌ | 主要颜色（如未提供，系统会自动提取） |
| `secondaryColor` / `secondary_color` | ❌ | 辅助颜色（hex代码） |
| `backgroundColor` / `background_color` | ❌ | 背景颜色（hex代码） |
| `renderStyle` / `render_style` | ❌ | 图形渲染风格（扁平、渐变、玻璃质感、铬色、霓虹色、3D等） |

### 图形服务（模式1：使用标志服务生成的素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brandSystemUrl` / `brand_system_url` | ✅ | 来自标志服务的`brand-system.json`文件链接 |
| `prompt` | ✅ | 需要生成的图形类型（请明确用途和风格） |
| `aspectRatio` | ✅ | 输出比例（1:1、4:5、16:9、9:16等，默认为1:1） |

### 图形服务（模式2：使用自定义素材）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `logoUrl` / `logo_url` | ✅ | 您现有的标志图片链接 |
| `brandName` / `brand_name` | ✅ | 品牌名称 |
| `prompt` | ✅ | 需要生成的图形类型 |
| `aspectRatio` | ✅ | 输出比例（默认为1:1） |
| `primaryColor` | ✅ | 主要颜色（hex代码，如未提供，系统会自动提取） |
| `secondaryColor` | ❌ | 辅助颜色（hex代码） |
| `renderStyle` | ✅ | 图形渲染风格（扁平、渐变、玻璃质感、铬色、霓虹色、3D等） |

### 吉祥物服务（根据提示生成）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brand_name` | ✅ | 品牌名称 |
| `prompt` | ✅ | 吉祥物的描述（例如：生物类型、风格、颜色） |
| `primaryColor` | ✅ | 主要颜色（hex代码，例如“#8B5CF6”） |
| `creature` | ✅ | 吉祥物的类型（例如：猫头鹰、机器人、猫） |
| `leg_count` | ✅ | 腿的数量（默认为2） |
| `claw_count` | ✅ | 手臂/爪子的数量（默认为2） |

### 吉祥物服务（使用锁定后的原始图像生成）

| 字段 | 是否必填 | 说明 |
|-------|----------|-------------|
| `brand_name` | ✅ | 品牌名称 |
| `master_url` | ✅ | 原始吉祥物图像的链接 |
| `leg_count` | ✅ | 腿的数量（质量检查所需） |
| `claw_count` | ✅ | 手臂/爪子的数量（默认为2） |

### 图形尺寸比例

| 比例 | 像素 | 适用场景 |
|-------|--------|----------|
| `1:1` | 1024×1024 | Instagram、Twitter、LinkedIn帖子 |
| `4:5` | 1024×1280 | Instagram动态（竖屏） |
| `9:16` | 1024×1820 | TikTok视频、Reels |
| `16:9` | 1820×1024 | YouTube缩略图、Twitter卡片 |
| `3:2` | 1536×1024 | 博客标题栏 |
| `2:3` | 1024×1536 | Pinterest |

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

### 图形风格图形响应

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

### 吉祥物响应

```json
{
  "jobId": "mascot-123",
  "status": "completed",
  "brandName": "Melodify",
  "mascot": {
    "master": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/master.png",
    "wave": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/wave.png",
    "happy": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/happy.png",
    "sad": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/sad.png",
    "angry": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/angry.png",
    "laugh": "https://pub-156972f0e0f44d7594f4593dbbeaddcb.r2.dev/melodify/mascot/FINAL/laugh.png"
  },
  "qcPassed": true
}
```

---

## 供应商信息

- **服务名称：**OpenGFX
- **提供者：**AKLO Labs
- **官方网站：**https://opengfx.app
- **GitHub仓库：**https://github.com/aklo360/opengfx-skill
- **支持邮箱：**aklo@aklo.studio
- **代理钱包：**`0x7cf4CE250a47Baf1ab87820f692BB87B974a6F4e`
- **x402接口：**https://gateway.opengfx.app
- **ACP市场平台：**https://app.virtuals.io/acp
- **ClawHub：**https://clawhub.com/skills/opengfx

---

## 最佳实践

- **请详细说明您的设计概念**——包括行业、氛围和目标受众 |
- **如有颜色偏好，请明确说明**（例如：“蓝色和金色色调”）
- **说明设计风格**——例如“极简风格”、“趣味风格”、“企业风格”、“科技风格”、“自然风格” |
- **选择明暗色调**——AI会自动判断，但您可以提供提示（如“暗色调风格”或“明亮友好的风格” |
- **先进行测试**——使用低价值的测试任务来验证服务效果，再投入生产 |
- **选择集成方式**——如果已经在Virtuals生态系统中，建议使用x402；否则可以选择ACP
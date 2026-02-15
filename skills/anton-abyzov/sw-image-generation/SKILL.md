---
name: image-generation
description: 使用 Pollinations.ai 生成 AI 图像——完全免费，无需 API 密钥。适用于生成英雄图片、图标、徽标、插图、原型图或任何用于网站和应用程序的视觉素材。该工具可生成高质量的产品图片、头像、占位图以及社交媒体图片。
allowed-tools:
  - Read
  - Write
  - WebFetch
context: fork
model: opus
---

# 人工智能图像生成技能

我们擅长使用 Pollinations.ai（一个免费的开源人工智能图像生成平台）来生成专业质量的图像，该平台无需使用 API 密钥。

## 快速参考

**立即生成任何图像：**
```
https://image.pollinations.ai/prompt/YOUR_PROMPT_HERE
```

## 该技能的适用场景

当您需要以下类型的图像时，此技能会自动激活：
- **网页开发**：首页图片、背景图、横幅图、缩略图
- **应用程序设计**：启动画面、引导页、占位符图片、图标
- **市场营销**：产品原型图、社交媒体图片、广告图片、着陆页图片
- **用户界面/用户体验（UI/UX）**：插图、头像、空白状态界面、功能图形
- **原型设计**：概念可视化、线框图素材

## Pollinations.ai API

### 基本 URL 结构

```
https://image.pollinations.ai/prompt/{prompt}?{parameters}
```

### 参数

| 参数 | 值 | 默认值 | 说明 |
|-----------|--------|---------|-------------|
| `width` | 256-2048 | 1024 | 图像宽度（像素） |
| `height` | 256-2048 | 1024 | 图像高度（像素） |
| `model` | flux, turbo, flux-realism, flux-anime, flux-3d, flux-cablyai | 使用的 AI 模型 |
| `seed` | 任意整数 | 随机值 | 保证结果的可重复性 |
| `nologo` | true | false | 是否去除水印 |
| `enhance` | true | false | 是否进行图像优化 |
| `safe` | true | false | 是否启用安全过滤 |

### 可用的 AI 模型

| 模型 | 适用场景 | 图像质量 | 生成速度 |
|-------|----------|---------|-------|
| `flux` | 通用用途，照片级真实感 | 最高 | 中等 |
| `flux-realism` | 超真实照片 | 非常高 | 中等 |
| `flux-anime` | 动画/插画风格 | 高 | 快速 |
| `flux-3d` | 3D 渲染图、产品原型图 | 高 | 中等 |
| `flux-cablyai` | 艺术风格、创意图像 | 高 | 快速 |
| `turbo` | 快速迭代、草图生成 | 中等 | 最快 |

## 专业提示编写技巧

### 提示公式（对图像质量至关重要）

```
[Subject] + [Style/Medium] + [Lighting] + [Composition] + [Quality Modifiers]
```

### 必须包含的质量修饰词

为了获得**最高质量的图像输出**，请在提示中添加以下修饰词：

```
, professional photography, 8k uhd, high resolution, sharp focus, highly detailed
```

### 特定使用场景下的提示示例：

| 使用场景 | 需要添加的修饰词 |
|----------|-------------------|
| **网站首页图片** | `电影级光照效果、专业摄影风格、8K 分辨率、清晰对焦、立体光照` |
| **产品图片** | **摄影室灯光效果、白色背景、商业摄影风格、清晰图像** |
| **应用程序图标** | **极简设计、矢量风格、线条简洁、居中显示、简洁背景** |
| **插图** | **数字插画、鲜艳色彩、线条清晰、专业水准** |
| **头像** | **肖像风格、居中显示、专业头像、中性背景、高质量图像** |
| **背景图** | **无缝图案、可平铺、抽象风格、色调柔和、不会分散注意力** |

### 常见使用场景的尺寸比例

| 使用场景 | 宽度 | 高度 | 比例 |
|----------|-------|--------|-------|
| **首页横幅** | 1920 | 1080 | 16:9 |
| **社交媒体帖子** | 1200 | 1200 | 1:1 |
| **肖像/头像** | 800 | 1200 | 2:3 |
| **产品卡片** | 800 | 600 | 4:3 |
| **移动应用启动画面** | 1080 | 1920 | 9:16 |
| **应用程序图标** | 512 | 512 | 1:1 |
| **原始图片** | 1200 | 630 | 约 1.9:1 |
| **缩略图** | 400 | 300 | 4:3 |

## 代码示例

### React/Next.js 集成方法

```tsx
// components/GeneratedImage.tsx
interface GeneratedImageProps {
  prompt: string;
  width?: number;
  height?: number;
  model?: 'flux' | 'flux-realism' | 'flux-anime' | 'flux-3d' | 'turbo';
  className?: string;
  alt: string;
}

export function GeneratedImage({
  prompt,
  width = 1024,
  height = 1024,
  model = 'flux',
  className,
  alt,
}: GeneratedImageProps) {
  const encodedPrompt = encodeURIComponent(prompt);
  const url = `https://image.pollinations.ai/prompt/${encodedPrompt}?width=${width}&height=${height}&model=${model}&nologo=true`;

  return (
    <img
      src={url}
      alt={alt}
      width={width}
      height={height}
      className={className}
      loading="lazy"
    />
  );
}

// Usage
<GeneratedImage
  prompt="Modern tech startup office, glass walls, natural lighting, professional photography, 8k"
  width={1920}
  height={1080}
  alt="Hero background"
  className="w-full h-auto object-cover"
/>
```

### 使用 Next.js 优化图像显示

```tsx
// next.config.js
module.exports = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'image.pollinations.ai',
      },
    ],
  },
};

// components/OptimizedGeneratedImage.tsx
import Image from 'next/image';

export function OptimizedGeneratedImage({ prompt, width, height, alt }) {
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=${width}&height=${height}&model=flux&nologo=true`;

  return (
    <Image
      src={url}
      alt={alt}
      width={width}
      height={height}
      priority={false}
    />
  );
}
```

### 直接在 HTML 中嵌入图像

```html
<!-- Hero Image -->
<img
  src="https://image.pollinations.ai/prompt/futuristic%20city%20skyline%20at%20sunset%2C%20cyberpunk%2C%20neon%20lights%2C%20cinematic%2C%208k?width=1920&height=1080&model=flux&nologo=true"
  alt="Hero background"
  loading="lazy"
/>

<!-- Product Mockup -->
<img
  src="https://image.pollinations.ai/prompt/smartphone%20mockup%20on%20marble%20desk%2C%20minimal%2C%20studio%20lighting%2C%20product%20photography?width=800&height=600&model=flux-3d&nologo=true"
  alt="Product mockup"
/>
```

### 用于文档编写的 Markdown 代码

```markdown
![Hero Image](https://image.pollinations.ai/prompt/abstract%20geometric%20pattern%2C%20gradient%20blue%20purple%2C%20modern%2C%20clean?width=1200&height=400&nologo=true)
```

### 批量生成脚本（Node.js）

```typescript
import fs from 'fs';
import https from 'https';

async function generateImage(prompt: string, filename: string, options = {}) {
  const { width = 1024, height = 1024, model = 'flux' } = options;
  const url = `https://image.pollinations.ai/prompt/${encodeURIComponent(prompt)}?width=${width}&height=${height}&model=${model}&nologo=true`;

  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      const file = fs.createWriteStream(filename);
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(filename);
      });
    }).on('error', reject);
  });
}

// Generate multiple images
const assets = [
  { prompt: 'hero background, abstract waves, blue gradient', file: 'hero.png', width: 1920, height: 1080 },
  { prompt: 'user avatar placeholder, geometric face', file: 'avatar.png', width: 200, height: 200 },
  { prompt: 'empty state illustration, no results found', file: 'empty.png', width: 400, height: 300 },
];

for (const asset of assets) {
  await generateImage(asset.prompt, asset.file, { width: asset.width, height: asset.height });
  console.log(`Generated: ${asset.file}`);
}
```

## 使用场景示例

### 1. 网站首页图片生成

```
https://image.pollinations.ai/prompt/modern%20SaaS%20dashboard%20floating%20in%20space%2C%20dark%20theme%2C%20glowing%20UI%20elements%2C%20professional%203D%20render%2C%20cinematic%20lighting%2C%208k%20uhd?width=1920&height=1080&model=flux&nologo=true
```

### 2. 团队成员头像生成

```
https://image.pollinations.ai/prompt/professional%20headshot%2C%20friendly%20smile%2C%20neutral%20gray%20background%2C%20studio%20lighting%2C%20business%20casual?width=400&height=400&model=flux-realism&nologo=true
```

### 3. 应用程序空白状态界面设计

```
https://image.pollinations.ai/prompt/cute%20illustration%20of%20empty%20box%2C%20minimal%20flat%20design%2C%20soft%20pastel%20colors%2C%20friendly%2C%20vector%20style?width=400&height=300&model=flux-anime&nologo=true
```

### 4. 产品原型图生成

```
https://image.pollinations.ai/prompt/iPhone%2015%20mockup%20on%20wooden%20desk%2C%20coffee%20cup%2C%20minimal%2C%20lifestyle%20photography%2C%20warm%20lighting%2C%20professional?width=1200&height=800&model=flux-3d&nologo=true
```

### 5. 博客特色图片

```
https://image.pollinations.ai/prompt/abstract%20visualization%20of%20artificial%20intelligence%2C%20neural%20networks%2C%20blue%20and%20purple%2C%20futuristic%2C%20clean?width=1200&height=630&model=flux&nologo=true
```

### 6. 应用程序图标制作

```
https://image.pollinations.ai/prompt/minimalist%20app%20icon%2C%20letter%20A%2C%20gradient%20blue%20to%20purple%2C%20rounded%20corners%2C%20flat%20design%2C%20iOS%20style?width=512&height=512&model=flux&nologo=true
```

### 7. 背景图设计

```
https://image.pollinations.ai/prompt/seamless%20geometric%20pattern%2C%20subtle%20gray%20on%20white%2C%20minimalist%2C%20tileable%2C%20modern?width=512&height=512&model=flux&nologo=true
```

### 8. 功能插图制作

```
https://image.pollinations.ai/prompt/isometric%20illustration%20of%20cloud%20computing%2C%20servers%2C%20data%20flow%2C%20blue%20and%20white%2C%20clean%20vector%20style?width=800&height=600&model=flux&nologo=true
```

## 最佳实践

### 建议的做法：

1. **使用详细的提示** – 信息越详细，生成效果越好。
2. **添加质量修饰词**，例如 “8K 分辨率、专业水准、细节丰富”。
3. **明确指定图像风格**，例如 “照片风格”、“插画风格”、“3D 渲染”。
4. **指定光照效果**，例如 “摄影室灯光效果”、“自然光”、“电影级光照”。
5. **设置合适的尺寸**，以匹配实际使用需求。
6. **使用随机种子值** 以确保结果的一致性。
7. **缓存生成的图像**，并将它们保存到内容分发网络（CDN）中以供后续使用。

### 不建议的做法：

1. **避免使用通用或模糊的提示**，例如 “生成一张图片”。
2. **不要请求受版权保护的内容**，例如品牌标志或名人图片。
3. **不要频繁重复生成相同的图像**，请使用随机种子值并缓存结果。
4. **务必设置 `nologo=true` 以去除水印**。
5. **遵守请求速率限制**，避免过度使用服务。

## 请求速率限制与缓存策略

### Pollinations 的请求速率限制

| 用户类型 | 每 15 秒的请求次数 |
|------|-------------------|
| 匿名用户 | 1 次 |
| 使用免费账户（无种子值） | 每 5 秒 1 次 |
| 使用高级账户（含种子值） | 每 3 秒 1 次 |

### 生产环境下的缓存策略

```typescript
// Cache generated images to your CDN
async function getOrGenerateImage(prompt: string, options: ImageOptions) {
  const cacheKey = createHash('md5')
    .update(prompt + JSON.stringify(options))
    .digest('hex');

  // Check CDN cache first
  const cached = await cdn.get(`images/${cacheKey}.png`);
  if (cached) return cached.url;

  // Generate and cache
  const imageUrl = buildPollinationsUrl(prompt, options);
  const imageBuffer = await fetch(imageUrl).then(r => r.buffer());
  const cdnUrl = await cdn.upload(`images/${cacheKey}.png`, imageBuffer);

  return cdnUrl;
}
```

## 常见问题及解决方法

| 问题 | 解决方案 |
|-------|----------|
| 生成速度慢** | 使用 `turbo` 模型可加快生成速度。 |
| 图像质量差** | 添加质量修饰词，或选择 `flux` 或 `flux-realism` 模型。 |
| 图像风格不正确** | 明确指定所需的图像风格，例如 “照片风格” 或 “插画风格”。 |
| 图像出现水印** | 设置 `nologo=true` 以去除水印。 |
| 生成结果不一致** | 使用相同的随机种子值。 |
| 请求被限制** | 请等待 15 秒后再进行请求，或注册高级账户以获得更多请求次数。 |
| 图像无法加载** | 确保提示字符串正确编码。

## 与前端设计的集成方法

在构建网站或应用程序时，此技能可以无缝集成到前端开发流程中：
1. **开发阶段**：直接使用 Pollinations.ai 提供的 URL 作为占位符。
2. **生产阶段**：生成最终图像并保存到 CDN。
3. **处理动态内容**：通过 API 生成图像，并使用适当的缓存策略。

### 激活此技能的关键词

当您输入以下关键词时，该技能会自动激活：
- “生成图像”
- “创建图片”
- “制作插图”
- “用于……的首页图片”
- “用于……的横幅图”
- “……的产品原型图”
- “占位符图片”
- “头像图片”
- “……的插图”

## 为 SpecWeave 文档网站生成图像时的品牌指南

在为 SpecWeave 文档网站生成图像时，请遵循以下品牌规范：

### 品牌提示颜色

| 颜色 | 十六进制代码 | 用途 |
|-------|-----|-------|
| 主要紫色 | #7c3aed | 主要品牌颜色，用于渐变效果 |
| 深紫色 | #6d28d9 | 用于阴影或高光效果 |
| 浅紫色 | #a78bfa | 用于亮点或发光效果 |
| 最深紫色 | #5b21b6 | 用于深色背景 |

**在提示中请使用以下颜色代码：** `purple violet gradient #7c3aed`、`professional SaaS aesthetic`。

### 标准文档图像尺寸

| 图像类型 | 宽度 | 高度 | 使用的 AI 模型 | 用途 |
|------------|-------|--------|-------|-------|
| 首页横幅 | 1920 | 1080 | flux | 首页图片 |
| 功能卡片 | 800 | 600 | flux | 功能说明插图 |
| 节目标题 | 1200 | 400 | flux | 节目标题横幅 |
| 图标 | 64 | 64 | flux | 导航图标 |
| 空白状态界面 | 400 | 300 | flux-anime | 空白状态界面、占位符图片 |
| 社交媒体图片 | 1200 | 630 | flux | 社交媒体分享用的图片 |

### 专用文档提示模板

| 图像类型 | 提示示例 |
|------------|---------------|
| **首页图片** | `[具体概念]，采用紫色渐变效果（#7c3aed 至 #a78bfa），专业 SaaS 风格，带有发光效果的节点，深色背景，8K 分辨率，极简设计` |
| **功能插图** | `[具体功能] 的等轴测插图，带有紫色点缀（#7c3aed），白色背景，简洁的矢量风格` |
| **节目标题横幅** | **[具体主题** 的抽象可视化效果，流畅的线条，紫色渐变效果（#7c3aed），极简设计` |
| **图标** | **[具体概念] 的极简图标，紫色背景，应用图标风格，居中显示` |
| **动态文档** | **相互连接的文档，带有发光的紫色线条（#7c3aed），网络可视化效果，专业设计` |
| **智能代理系统** | **智能代理以几何形状呈现，采用紫色渐变效果（#7c3aed），未来主义风格` |

### SpecWeave 文档示例链接

**动态文档插图示例：**
```
https://image.pollinations.ai/prompt/interconnected%20hexagonal%20document%20nodes%20forming%20network%2C%20glowing%20purple%20connections%20%237c3aed%2C%20gradient%20to%20%23a78bfa%2C%20professional%20SaaS%2C%20dark%20background%2C%208k%2C%20minimal%20vector?width=800&height=600&model=flux&nologo=true&seed=42
```

**多智能代理系统插图示例：**
```
https://image.pollinations.ai/prompt/interconnected%20AI%20agents%20as%20geometric%20avatars%20in%20orbital%20formation%2C%20purple%20violet%20theme%20%237c3aed%2C%20futuristic%20holographic%2C%20professional%2C%20clean%20dark%20background%2C%208k?width=800&height=600&model=flux&nologo=true&seed=42
```

**工作流程/决策树插图示例：**
```
https://image.pollinations.ai/prompt/branching%20flowchart%20paths%20made%20of%20glowing%20circuit%20lines%2C%20purple%20gradient%20%237c3aed%20to%20%23a78bfa%2C%20decision%20trees%2C%20minimal%20geometric%2C%20professional%2C%20dark%20background?width=800&height=600&model=flux&nologo=true&seed=42
```

## 相关技能

- **前端设计**：用于用户界面/用户体验（UI/UX）设计
- **浏览器自动化**：用于截图功能
- **docusaurus**：用于文档网站的搭建
- **技术写作**：用于文档内容的编写
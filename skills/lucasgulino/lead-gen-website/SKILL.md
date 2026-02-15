---
name: lead-gen-website
description: 构建功能完备的本地潜在客户生成网站，具备SEO优化、转化跟踪以及RGPD（通用数据保护条例）合规性。这些网站适用于针对本地市场（如水管工、电工、家居服务等）的服务型企业，包含10-20个页面、结构化数据、分析功能以及法律合规性要求。
---

# 链接生成网站构建工具

使用该工具可以构建针对本地服务的网站，这些网站具备完善的SEO优化功能、跟踪机制，并符合RGPD（通用数据保护条例）要求。同时，该工具还配备了防垃圾邮件系统（遵循Google的垃圾邮件政策，更新至2024年3月版本），支持本地SEO优化（针对英镑地区），以及适合小额预算的广告投放。

## 适用场景

当用户需要以下类型的网站时，请使用此工具：
- 本地服务企业（如家居服务、维修服务、专业服务）
- 针对特定地理区域的潜在客户生成工具
- 需要10-20多个页面的网站，包括服务页面、博客和法律声明页面
- 优化过以吸引本地用户的关键词的SEO内容
- 支持转化跟踪（通过电话、WhatsApp或带有UTM参数的表单）
- 符合RGPD/GDPR法规要求（包括cookie提示横幅、隐私政策页面等）

## 工作流程概述

请按以下步骤顺序进行操作。除非有明确理由，否则不要跳过任何步骤或合并步骤：

0) **政策/风险检查（必选）**
- 阅读 `references/google-spam-guardrails-2024.md`
- 严格核实：没有引导页、没有重复的通用内容、没有虚假地址或误导性声明。
- 如果该项目用于潜在客户生成（leadgen），则所有关键页面都必须明确披露相关信息。

然后继续执行步骤1至7。

### 第1阶段：分析与规划

从用户或规格文档中收集项目需求。

**所需信息：**
- 业务领域及提供的服务
- 目标地理区域（城市及周边半径）
- 用于SEO的目标关键词
- 联系方式（电话、WhatsApp、电子邮件）
- 所需页面的数量和类型
- 竞争对手的网站（以便进行差异化设计）

**输出：** 明确了解项目范围、目标受众和转化目标。

### 第2阶段：设计构思

在项目根目录下创建 `ideas.md` 文件，其中包含三种不同的设计方案。

使用 `templates/design-ideas-template.md` 作为结构模板。每种设计方案需包括：
- 设计理念和美学风格
- 颜色调色板（以十六进制代码表示）及情感诉求
- 字体系统（标题和正文字体）
- 布局方案（避免使用通用的居中布局）
- 独特的视觉元素
- 动画设计指南
- 交互设计原则

参考 `references/design-philosophies.md` 以获取灵感，但请创作出独特的组合方案。

**选择：** 选择一种设计方案并记录选择理由。这种设计理念将指导后续的所有设计决策。

### 第3阶段：视觉资源制作

使用 `generate` 工具生成3-5张高质量图片。这些图片必须：
- 与选定的设计理念保持一致（颜色、风格、氛围）
- 存储在 `/home/ubuntu/webdev-static-assets/` 目录下
- 满足关键视觉需求：首页背景图、服务插图、当地地标图片、团队/工匠照片

**使用计划：**
- 主页：最具冲击力的图片
- 服务页面：相关的服务插图
- 关于我们/信任页面：团队或当地地标的照片

**注意：** 开发过程中不要临时生成图片，为了效率，请一次性生成所有图片。

### 第4阶段：内容结构设计

为所有页面创建详细的内容结构。

**选项A（手动）：** 直接编写 `content-structure.md` 文件，为每个页面指定标题、元描述、H1标题和主要内容大纲。

**选项B（脚本）：** 创建 `specs.json` 文件，其中包含页面数据，然后运行以下代码：
```bash
python /home/ubuntu/skills/lead-gen-website/scripts/generate_content_structure.py specs.json content-structure.md
```

**内容要求：**
- 每个主页面（首页、主要服务页面）至少500字
- 每篇博客文章至少1000字
- 自然融入目标关键词（避免过度填充）
- 回答用户的需求（产品/服务是什么、为什么需要、如何使用、价格、服务区域）
- 强调本地特色（频繁提及城市/地区名称）

### 第5阶段：开发

初始化项目并构建所有页面。

#### 5.1 初始化项目
```bash
webdev_init_project <project-name>
```

#### 5.2 配置设计样式

编辑 `client/src/index.css` 文件，根据选定的设计理念进行配置：
- 更新CSS变量（主要颜色、次要颜色、强调色、背景色、前景色）
- 调整字体样式（无衬线字体和衬线字体）
- 调整阴影效果、圆角半径和动画效果

在 `client/index.html` 中添加Google字体：
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=YourFont:wght@400;600;700&display=swap" rel="stylesheet" />
```

#### 5.3 创建可重用组件

使用 `templates/` 目录中的模板，并将占位符替换为项目特定的值：

**页眉组件（`templates/component-Header.tsx`）：**
- `{{SITE_NAME}}`、`{{SITE_TAGLINE}}`、`{{SITE_INITIALS}}`
- `{{PHONE_NUMBER}}`、`{{WHATSAPP_NUMBER}}`
- `{{NAV_ITEMS}}`（`label, href` 的JSON数组）

**页脚组件（`templates/component-Footer.tsx`）：**
- `{{SITE_NAME}}`、`{{SITE_DESCRIPTION}}`
- `{{SERVICE_LINKS}}`、`{{UTILITY LINKS}}`
- `{{PHONE_NUMBER}}`、`{{EMAIL}}`、`{{LOCATION}}`

**SEO页眉组件（`templates/component-SEOHead.tsx`）：**
- 将 `{{DOMAIN}}` 替换为实际域名

**其他组件：** 导航栏、联系表单、Cookie提示横幅（基本保持不变，只需少量定制）

#### 5.4 构建页面

**对于相似页面（服务页面、博客文章）：**
1. 使用 `templates/page-service-template.tsx` 创建模板文件
2. 使用 `services-data.json` 创建数据文件
3. 运行批量生成脚本：
```bash
python /home/ubuntu/skills/lead-gen-website/scripts/generate_pages_batch.py service-template.tsx services-data.json client/src/pages/
```

**对于独特页面（首页、价格表、常见问题解答、联系页面）：**
- 手动构建内容，确保一致性，并使用相应的组件。

**对于法律声明页面：**
使用 `templates/page-legal-template.tsx` 和标准法律声明模板。

#### 5.5 更新 App.tsx**

将所有页面路径添加到 `client/src/App.tsx` 中：
```tsx
<Route path="/service-page" component={ServicePage} />
```

将页眉、页脚和Cookie提示横幅集成到应用程序布局中。

### 第6阶段：SEO优化、跟踪、英镑地区优化、广告投放

#### 6.1 生成SEO相关文件

创建 `pages.json` 文件，其中包含所有页面的URL和优先级：
```json
[
  {"url": "/", "priority": "1.0"},
  {"url": "/service", "priority": "0.9"},
  {"url": "/contact", "priority": "0.9"},
  {"url": "/blog", "priority": "0.6"},
  {"url": "/mentions-legales", "priority": "0.3"}
]
```

运行脚本：
```bash
python /home/ubuntu/skills/lead-gen-website/scripts/create_seo_files.py yourdomain.com pages.json client/public/
```

此脚本会在 `client/public/` 目录下生成 `robots.txt` 和 `sitemap.xml` 文件。

#### 6.2 添加结构化数据

使用 `SEOHead` 组件的 `jsonLd` 属性，在关键页面添加JSON-LD结构化数据：

**首页（本地企业）：**
```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "telephone": "+33123456789",
  "email": "contact@example.com",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "City",
    "addressCountry": "FR"
  },
  "areaServed": ["City1", "City2"],
  "openingHours": "Mo-Fr 08:00-18:00"
};
```

**服务页面：**
```tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "Service Name",
  "description": "Service description",
  "provider": {
    "@type": "LocalBusiness",
    "name": "Business Name"
  },
  "areaServed": "City"
};
```

参考 `references/seo-checklist.md` 以获取完整的SEO优化要求。

#### 6.3 RGPD合规性检查**

验证：
- `App.tsx` 中是否集成了Cookie提示横幅
- 是否有包含完整RGPD信息的隐私政策页面
- 是否有隐私政策页面
- 是否有法律声明页面
- 联系表单中是否包含隐私政策链接

参考 `references/rgpd-compliance.md` 以获取详细要求。

#### 6.4 英镑地区SEO优化（提升网站可见性）

阅读并执行 `references/gbp-local-seo-playbook.md` 文档：

**交付成果：**
- 英镑地区SEO设置检查清单（包括服务类别、常见问题解答等）
- 30天的图片/文章/声明发布计划
- NAP（本地权威目录）引用列表（注重质量，避免垃圾内容）

#### 6.5 小额预算广告（每天4欧元）

阅读并执行 `references/ads-micro-budget-4eur-playbook.md` 文档：

**交付成果：**
- 一个高度精准的广告活动（精确的关键词/短语、投放区域、时间安排）
- 一个专用的广告页面及相应的跟踪系统

#### 6.6 转化跟踪**

`ContactForm` 组件会自动从URL中捕获UTM参数：
- `utm_source`（例如：google、facebook）
- `utm_campaign`（广告活动名称）
- `utm_adset`（广告组名称）
- `utm_ad`（具体广告名称）

这些参数会存储在表单状态中，并可发送到后端/CRM系统进行转化跟踪。

### 第7阶段：验证与交付

#### 7.1 浏览器测试

打开开发服务器的URL，验证以下内容：
- 所有页面是否无错误加载
- 导航是否正常（页眉菜单、导航栏）
- 表单提交是否正常
- 移动设备上的页面是否响应良好（测试CTA按钮是否固定显示）
- 首次访问时是否显示Cookie提示横幅
- 图片是否正确加载

#### 7.2 SEO验证

根据 `references/seo-checklist.md` 进行验证：
- 每个页面是否有唯一的标题和描述
- H1标题层级是否正确
- 图片是否有alt属性
- `robots.txt` 和 `sitemap.xml` 是否可访问
- 关键页面是否包含结构化数据

#### 7.3 创建检查点

```bash
webdev_save_checkpoint "Complete lead-gen website - [X] pages, SEO optimized, RGPD compliant"
```

#### 7.4 向用户交付成果

通过 `message` 工具发送包含以下内容的检查点附件：
- 项目构建总结
- 页面数量和主要功能
- 实施的SEO优化措施
- 下一步操作（发布网站、购买自定义域名、配置Google Search Console）

## 搭配资源

### 脚本

**`scripts/generate_pages_batch.py`**
根据模板和数据文件生成多个相似页面。
使用方法：`python generate_pages_batch.py <template> <data_json> <output_dir>`

**`scripts/create_seo_files.py`
自动生成 `robots.txt` 和 `sitemap.xml`。
使用方法：`python create_seo_files.py <domain> <pages_json> <output_dir>`

**`scripts/generate_content_structure.py`
根据规格JSON文件生成内容结构Markdown。
使用方法：`python generate_content_structure.py <specs_json> <output_md>`

### 模板

**组件：**
- `component-Header.tsx` - 包含Logo、导航栏和CTA的固定页眉
- `component-Footer.tsx` - 包含链接和联系信息的页脚
- `component-SEOHead.tsx` - SEO元标签和结构化数据
- `component-Breadcrumbs.tsx` - 导航栏
- `component-ContactForm.tsx` - 带有UTM跟踪功能的表单
- `component-CookieBanner.tsx` - RGPD隐私政策同意提示横幅

**页面模板：**
- `page-service-template.tsx` - 服务页面模板
- `page-legal-template.tsx` - 法律声明页面模板
- `design-ideas-template.md` - 设计构思结构模板

### 参考资料

**`references/seo-checklist.md`
完整的SEO检查清单，涵盖元标签、结构化数据、技术SEO、页面SEO优化、本地SEO和内容质量。在开始第6阶段之前请阅读此文件，确保没有遗漏。

**`references/conversion-best-practices.md`
提高转化率的最佳实践：CTA策略、联系方式、信任信号、表单优化、移动设备优化。在构建页面时请参考此文件。

**`references/rgpd-compliance.md`
全面的RGPD合规性指南，涵盖Cookie提示横幅、隐私政策、法律声明、表单设计、数据安全和用户权利。第6阶段必须参考此文件。

**`references/design-philosophies.md`
五种设计理念示例（Neo-Artisanat Digital、Brutalist Confidence、Soft Modernism、Vibrant Energy、Luxury Minimalism）及选择标准。在第2阶段设计时可作为灵感来源。

## 提示与最佳实践

**设计一致性：** 在每个CSS/组件文件的顶部记录所选的设计理念，作为提醒。

**图片优化：** 所有图片应存储在 `/home/ubuntu/webdev-static-assets/` 目录下，并通过CDN链接引用，以避免部署时出现延迟。

**内容质量优于数量：** 10个高质量页面比20个平庸的页面更有价值。重点关注满足用户需求。

**以移动设备优先：** 首先设计和测试移动设备上的用户体验。大多数本地服务搜索都是通过移动设备进行的。

**转化优先：** 每个页面都应有明确的CTA（呼叫行动）按钮。在移动设备上，电话和WhatsApp按钮必须始终可见。

**本地SEO优化：** 在标题、H1标题和内容中提及城市/地区名称。如果服务覆盖多个城市，请为每个服务区域创建单独的页面。

**快速迭代：** 对于相似页面使用批量生成脚本以节省时间。将手动工作重点放在独特且高价值的页面上。

**测试：** 在创建检查点之前，务必在浏览器中进行测试。检查页面的移动设备响应性、表单提交功能和导航是否正常。

## 常见问题

**忽略设计构思阶段：** 可能导致设计缺乏个性和易被遗忘。务必创建包含三种不同设计方案的 `ideas.md` 文件。

**在开发过程中生成图片：** 效率较低。建议在第3阶段一次性生成所有图片。

**内容质量不足：** 内容太少（少于300字）会导致排名不佳。请在第4阶段投入时间，制作高质量、有用的内容。

**缺少RGPD相关元素：** 在欧盟地区，Cookie提示横幅、隐私政策页面和法律声明是必需的。不要跳过第6.3阶段。

**未设置UTM跟踪：** 没有UTM参数就无法衡量广告活动的效果。请确保`ContactForm`能够捕获这些参数。

**忽略移动设备的CTA：** 仅针对桌面设备的CTA会导致移动设备的转化率下降。务必添加移动设备的CTA按钮。

**在开发过程中创建多个检查点：** 仅在最后阶段（第7阶段）创建一个检查点。在初期交付时，多个检查点可能会让用户感到困惑。
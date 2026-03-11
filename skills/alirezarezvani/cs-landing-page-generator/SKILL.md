---
name: "landing-page-generator"
description: "生成高转化率的 landing 页面，这些页面是使用 Next.js/React (TSX) 和 Tailwind CSS 构建的完整组件。通过经过验证的文案框架（如 PAS、AIDA、BAB）来创建标题区域（hero sections）、功能展示区（feature grids）、价格表（pricing tables）、常见问题解答（FAQ accordions）、用户评价块（testimonial blocks）以及呼叫行动（CTA）区域。同时生成 SEO 元标签（meta tags）和结构化数据（structured data），并优化代码以符合 Core Web Vitals 的标准（页面加载时间 LCP < 1 秒，CLS < 0.1）。适用于需要创建 landing 页面、营销页面、首页、单页网站、潜在客户收集页面（lead capture page）、活动页面（campaign page）或促销页面（promo page）的场景；也适用于需要进行 A/B 测试或用高转化率设计的页面替换静态页面的情况。"
---
# 着陆页生成器

该工具能够根据产品描述生成转化率高的着陆页。生成的组件基于 Next.js/React 技术框架，支持多种页面布局样式，并具备 SEO 优化和性能优化功能。生成的文本内容并非随机生成的 “lorem ipsum”，而是能够有效吸引用户注意力的实际文案。

**目标指标：**  
- 着陆页的首次内容加载时间（LCP）< 1 秒  
- 页面的视觉稳定性（CLS）< 0.1  
- 首次交互时间（FID）< 100 毫秒  

**输出格式：**  
TSX 组件 + Tailwind CSS 样式 + SEO 相关元数据 + 多种页面布局样式  

---

## 核心功能  

- **5 种不同的首页布局样式：**  
  - 居中显示  
  - 分割布局  
  - 渐变背景  
  - 视频背景  
  - 极简风格  

- **功能展示区：**  
  - 使用网格布局  
  - 交替显示的功能卡片  
  - 带有图标的功能卡片  

- **价格表：**  
  - 支持 2–4 个价格层级，包含功能列表和切换选项  

- **常见问题解答（FAQ）：**  
  - 带有 Schema 标记的折叠式问答框  

- **用户评价：**  
  - 以网格或轮播形式展示用户评价  

- **呼叫行动（CTA）区域：**  
  - 包含横幅、全屏或内联形式的呼叫行动按钮  

- **页脚：**  
  - 简洁版、信息丰富的版和极简版  

- **4 种设计风格：**  
  - 都基于 Tailwind CSS 的样式集进行设计  

---

## 生成流程  

请按照以下步骤操作：  
1. **收集输入信息：**  
  - 通过指定的格式收集产品名称、标语、目标受众、用户痛点、核心优势、价格层级、设计风格和文案框架等信息。仅填写缺失的字段。  

2. **分析品牌风格：**  
  （建议执行）如果用户已有品牌相关内容（如网站文案、博客文章或营销材料），使用 `marketing-skill/content-production/scripts/brand_voice_analyzer.py` 工具分析品牌风格（正式程度、语气等），并据此选择设计风格和文案框架：  
    - 正式且专业的风格 → **企业级（Enterprise）** 设计风格，使用 **AIDA** 文案框架  
    - 随意且友好的风格 → **初创企业（Bold Startup）** 设计风格，使用 **BAB** 文案框架  
    - 正式且权威的风格 → **高端 SaaS（Dark SaaS）** 设计风格，使用 **PAS** 文案框架  
    - 随意且对话式的风格 → **极简风格（Clean Minimal）**，使用 **BAB** 文案框架  

3. **选择设计风格：**  
  根据用户的选择或品牌风格分析结果，从设计风格参考中选择相应的 Tailwind CSS 类别。  

4. **编写文案：**  
  使用选定的文案框架（PAS、AIDA 或 BAB）编写所有标题和正文内容，确保整体风格与品牌风格一致。  

5. **按顺序生成页面元素：**  
  - 首页 → 功能展示 → 价格表 → 常见问题解答 → 用户评价 → 呼叫行动 → 页脚。  
  跳过与产品无关的部分。  

6. **进行 SEO 校验：**  
  在输出最终代码前，检查所有 SEO 相关内容是否符合要求，并进行必要的修改。  

7. **生成最终代码：**  
  提供完整的 TSX 文件，包含所有 Tailwind CSS 类别、SEO 元数据和结构化数据。  

---

## 触发该功能的命令：  
```
Product: [name]
Tagline: [one sentence value prop]
Target audience: [who they are]
Key pain point: [what problem you solve]
Key benefit: [primary outcome]
Pricing tiers: [free/pro/enterprise or describe]
Design style: dark-saas | clean-minimal | bold-startup | enterprise
Copy framework: PAS | AIDA | BAB
```  

---

## 设计风格参考  

| 设计风格 | 背景颜色 | 强调颜色 | 功能卡片颜色 | 呼叫行动按钮颜色 |
|---|---|---|---|---|
| **高端 SaaS（Dark SaaS）** | `bg-gray-950 text-white` | `violet-500/400` | `bg-gray-900 border border-gray-800` | `bg-violet-600 hover:bg-violet-500` |
| **极简风格（Clean Minimal）** | `bg-white text-gray-900` | `blue-600` | `bg-gray-50 border border-gray-200 rounded-2xl` | `bg-blue-600 hover:bg-blue-700` |
| **初创企业风格（Bold Startup）** | `bg-white text-gray-900` | `orange-500` | `shadow-xl rounded-3xl` | `bg-orange-500 hover:bg-orange-600 text-white` |
| **企业级（Enterprise）** | `bg-slate-50 text-slate-900` | `slate-700` | `bg-white border border-slate-200 shadow-sm` | `bg-slate-900 hover:bg-slate-800 text-white` |

> **初创企业风格（Bold Startup）**：所有 `<h1>`/`<h2>` 元素的字体颜色设置为 `font-black tracking-tight`。  

---

## 文案框架  

**PAS（问题 → 激发兴趣 → 解决方案）**  
- **H1**：描述用户当前面临的困境  
- **副标题**：如果不解决这个问题会怎样  
- **呼叫行动（CTA）**：提供解决方案  
  **示例：**  
  - H1: “您的团队每天花费 3 小时进行手动报告。”  
  - 副标题: “每花在一个电子表格上的时间，就意味着少了一个成交机会。您的竞争对手已经实现了自动化。”  
  - CTA: “10 分钟内即可实现报告自动化！”  

**AIDA（吸引注意力 → 激发兴趣 → 产生欲望 → 行动）**  
- **H1**：吸引注意力的陈述  
- **副标题**：有趣的事实或优势  
- **功能部分**：展示能够满足用户需求的功能  
- **呼叫行动（CTA）**：明确的行动建议  

**BAB（使用前 → 使用后 → 过渡）**  
- **H1**：当前状态 → 使用后的状态  
- **副标题**：**[产品] 如何帮助用户实现转变**  
- **功能部分**：产品的工作原理  

---

## 代表性组件：**  
**首页（居中渐变背景，高端 SaaS 风格）**  
此模板适用于所有首页布局样式。只需更换布局类、渐变方向和图片位置即可实现其他样式。  
```tsx
export function HeroCentered() {
  return (
    <section className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden bg-gray-950 px-4 text-center">
      <div className="absolute inset-0 bg-gradient-to-b from-violet-900/20 to-transparent" />
      <div className="pointer-events-none absolute -top-40 left-1/2 h-[600px] w-[600px] -translate-x-1/2 rounded-full bg-violet-600/20 blur-3xl" />
      <div className="relative z-10 max-w-4xl">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-violet-500/30 bg-violet-500/10 px-4 py-1.5 text-sm text-violet-300">
          <span className="h-1.5 w-1.5 rounded-full bg-violet-400" />
          Now in public beta
        </div>
        <h1 className="mb-6 text-5xl font-bold tracking-tight text-white md:text-7xl">
          Ship faster.<br />
          <span className="bg-gradient-to-r from-violet-400 to-pink-400 bg-clip-text text-transparent">
            Break less.
          </span>
        </h1>
        <p className="mx-auto mb-10 max-w-2xl text-xl text-gray-400">
          The deployment platform that catches errors before your users do.
          Zero config. Instant rollbacks. Real-time monitoring.
        </p>
        <div className="flex flex-col items-center gap-4 sm:flex-row sm:justify-center">
          <Button size="lg" className="bg-violet-600 text-white hover:bg-violet-500 px-8">
            Start free trial
          </Button>
          <Button size="lg" variant="outline" className="border-gray-700 text-gray-300">
            See how it works →
          </Button>
        </div>
        <p className="mt-4 text-sm text-gray-500">No credit card required · 14-day free trial</p>
      </div>
    </section>
  )
}
```  

---

## 其他页面元素样式：  

### 功能展示区（交替布局）  

使用 `features` 数组，通过 `i % 2 === 1 ? "lg:flex-row-reverse" : ""` 来切换布局方向。  
使用 `<Image>` 元素设置 `width`、`height` 和 `rounded-2xl shadow-xl` 属性。  
将相关内容包裹在 `<section className="py-24">` 标签内，并使用 `max-w-6xl` 容器进行布局。  

### 价格表  

使用 `plans` 数组，通过以下方式生成价格表：  
- `name`：价格层级名称  
- `price`：价格  
- `description`：价格描述  
- `features`：功能列表  
- `cta`：呼叫行动链接  
- `highlighted`：高亮显示的价格层级  

高亮显示的价格层级会添加 `border-2 border-violet-500 bg-violet-950/50 ring-4 ring-violet-500/20` 样式；其他层级则使用 `border border-gray-800 bg-gray-900`。  
如果价格信息为空，显示 “Custom”（自定义）。  
每个功能项旁边使用 `<Check>` 图标。  
布局方式为 `grid gap-8 lg:grid-cols-3`。  

### 常见问题解答（FAQ）  

通过 `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify-schema) }} />` 将 FAQ 数据注入页面。  
使用 `{ q, a }` 对象将 FAQ 问题与答案组合成 `<Accordion>` 元素，并设置为 `type="single" collapsible`（可折叠）。  
容器宽度设置为 `max-w-3xl`。  

### 用户评价、呼叫行动（CTA）和页脚  

- **用户评价：**  
  - 以网格或轮播形式展示用户评价，包括头像、姓名、职位和评价内容。  
- **呼叫行动（CTA）横幅：** 全宽布局，包含标题、副标题和两个按钮（主要按钮和备用按钮）。  
  - 紧接下方添加信任信号（如退款保证、公司Logo等）。  
- **页脚：** 包含Logo、导航栏、社交链接和法律声明。  
  - 使用 `border-t border-gray-800` 作为分隔线。  

---

## SEO 校验 checklist  

- `<title>` 标签：包含主要关键词和品牌名称（50–60 个字符）  
- **元描述：** 包含产品优势和呼叫行动信息（150–160 个字符）  
- **原始图片（OG Image）：** 1200×630 像素，包含产品名称和标语  
- **H1 标题：** 每页仅使用一个 H1 标题，并包含主要关键词  
- **结构化数据：** 使用 `FAQPage`、`Product` 或 `Organization` Schema 标签  
- **设置正确的 canonical URL**  
- 所有 `<Image>` 元素的 `alt` 属性需包含图片描述  
- 配置 `robots.txt` 和 `sitemap.xml`  
- **核心 Web Vitals：** 首次内容加载时间（LCP）< 1 秒，视觉稳定性（CLS）< 0.1  
- **移动设备视口元标签**  
- **内部链接**：指向价格信息和文档页面  

> **验证步骤：** 在输出最终代码前，确保所有 SEO 相关要求都得到满足。如有任何问题，请立即修复。  

---

## 性能优化目标  

| 目标指标 | 目标值 | 优化技巧 |  
|---|---|---|
| **首次内容加载时间（LCP）** | < 1 秒 | 预加载首页图片，并使用 `priority` 属性优化 Next.js 的图片加载  
| **视觉稳定性（CLS）** | < 0.1 | 为所有图片设置明确的宽度和高度  
| **首次交互时间（FID/INP）** | < 100 毫秒 | 延迟加载非关键 JavaScript 代码，使用 `loading="lazy"`  
- **页面加载时间（TTFB）** | < 200 毫秒 | 对着陆页使用静态资源或 ISR（Isolated Script Loading）  
- **代码包大小（Bundle Size）** | < 100KB | 使用 `@next/bundle-analyzer` 工具进行代码包大小审计  

---

## 常见问题及解决方法：  

- **首页图片未预加载：** 为第一个 `<Image>` 元素添加 `priority` 属性  
- **缺少移动设备适配：** 始终优先考虑移动设备布局（使用 `sm:` 前缀）  
- **呼叫行动文案过于模糊：** 使用更具体的表述（如 “立即开始使用” 或 “免费试用”）  
- **价格表缺少信任信号：** 在呼叫行动区域添加退款保证和用户评价  
- **移动设备上呼叫行动按钮不可见：** 确保在 375px 视口宽度下按钮可见  

---

## 相关技能：  
- **品牌风格分析工具（Brand Voice Analyzer）**：** 在生成页面前使用 `marketing-skill/content-production/scripts/brand_voice_analyzer.py` 分析品牌风格，确保文案一致性  
- **UI 设计系统（UI Design System）**：** 根据品牌颜色生成设计元素  
- **竞争对手分析（Competitive Teardown）**：** 通过分析竞争对手来优化页面内容和差异化策略
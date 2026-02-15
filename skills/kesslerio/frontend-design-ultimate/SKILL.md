---
name: frontend-design-ultimate
description: 使用 React、Tailwind CSS 和 shadcn/ui 创建独具特色的、符合生产级标准的静态网站——无需任何原型设计。该工具能够根据纯文本需求生成醒目且易于记忆的设计方案，同时具备防AI滥用的美学设计原则、移动优先的响应式布局以及单文件打包功能。适用于构建登录页面、营销网站、作品集、仪表板或任何静态网页界面。支持 Vite（纯静态生成）和 Next.js（通过 Vercel 部署）两种开发流程。
homepage: https://github.com/kesslerio/frontend-design-ultimate-clawhub-skill
metadata:
  openclaw:
    emoji: "🎨"
    requires:
      bins: ["node", "npm"]
---

# 前端设计终极指南

仅凭文本要求，就能创建出独具特色、符合生产标准的静态网站。无需使用原型图或Figma工具——只需描述你的设计需求，就能获得醒目、令人难忘的设计成果。

**技术栈**：React 18 + TypeScript + Tailwind CSS + shadcn/ui + Framer Motion  
**输出格式**：Vite（静态HTML）或Next.js（支持Vercel部署）

## 快速入门

```
"Build a SaaS landing page for an AI writing tool. Dark theme, 
editorial typography, subtle grain texture. Pages: hero with 
animated demo, features grid, pricing table, FAQ accordion, footer."
```

---

## 设计思维（先完成这些）

在编写任何代码之前，首先要确定一个**鲜明的设计风格**：

### 1. 理解设计背景
- **设计目的**：这个界面要解决什么问题？目标用户是谁？
- **受众群体**：开发者工具？消费级应用？企业级应用？创意机构？
- **设计限制**：性能要求、可访问性需求、品牌规范有哪些？

### 2. 选择一种极端的设计风格
明确选择一种风格并坚持到底——模棱两可的设计往往失败：

| 风格 | 特点 |
|------|-----------------|
| **极简主义** | 极简的布局、单色色调、大字号字体、粗糙的边缘处理 |
| **极繁主义** | 多层次元素、密集的布局、相互重叠的元素、有控制的“混乱感” |
| **复古未来主义** | 使用霓虹色元素、几何形状、模拟CRT显示器的视觉效果 |
| **自然主义** | 温和的曲线、自然色调、手绘风格的元素 |
| **豪华/精致主义** | 微妙的动画效果、高品质的字体、简约的色彩搭配 |
| **编辑风格/杂志风格** | 规则性的网格布局、醒目的标题、合理的空白间距 |
| **原始主义** | 露骨的布局结构、强烈的对比度 |
| **艺术装饰风格/几何风格** | 使用金色元素、对称的布局、复杂的图案 |
| **柔和/淡色调** | 圆角设计、柔和的渐变效果、友好的视觉感受 |
| **工业风格/实用主义** | 功能性强的设计、等宽字体、信息密集的展示方式 |

### 3. 确定令人难忘的设计元素
用户会记住哪个元素？是醒目的动画效果？独特的字体设计？还是独特的色彩搭配？还是创新的布局？

---

## 设计美学指南

### 字体设计——绝不要使用通用字体
**禁止使用**：Inter、Roboto、Arial、系统字体、Open Sans

**推荐使用**：具有辨识度高的字体，提升整体设计品质。

| 使用场景 | 推荐字体 |
|----------|----------|
| 标题/副标题 | Cormorant Garamond, Satoshi, Playfair Display |
| 正文 | Instrument Sans, General Sans, Plus Jakarta Sans |
| 等宽字体/代码显示 | DM Mono, JetBrains Mono, IBM Plex Mono |
| 字体搭配建议 | 使用对比鲜明的字体重量（例如细体标题 + 粗体正文） |

**字号层次**：建议使用3倍以上的字号差异，而不是1.5倍的增量。

### 色彩与主题
**禁止使用**：白色背景上的紫色渐变效果，以及均匀分布的五色配色方案

**推荐做法**：
- **主导色 + 强调色**：遵循70-20-10的配色规则（主导色-次要色-强调色）
- **使用CSS变量**：`--primary`、`--accent`、`--surface`、`--text`
- **选择明暗分明的色调**：不要使用灰色的中性色调作为背景
- **高对比度的点击按钮**：确保按钮能够清晰地吸引用户的注意力

```css
:root {
  --bg-primary: #0a0a0a;
  --bg-secondary: #141414;
  --text-primary: #fafafa;
  --text-secondary: #a1a1a1;
  --accent: #ff6b35;
  --accent-hover: #ff8555;
}
```

### 动画效果
**优先级**：整体页面加载的流畅性高于零散的微交互效果

**关键动画效果**：
- 主标题的渐进式显示效果（`animation-delay`）
- 滚动时触发的页面元素动画
- 鼠标悬停时的视觉变化（如尺寸变化、颜色变化、阴影深度变化）
- 平滑的页面过渡效果

**实现方式**：
- 简单动画使用CSS实现
- 使用Framer Motion库为React项目添加动画效果（通过初始化脚本安装）
- 动画持续时间控制在200-400毫秒之间（保持流畅体验）

### 空间布局
**禁止使用**：居中的对称布局

**推荐做法**：
- 有目的性的不对称布局
- 元素之间的重叠效果
- 对角线方向的视觉流动或打破常规的网格布局
- 适当的负空间设计（或保持较高的元素密度）
- 主标题区域可以偏离常规网格布局

### 背景与氛围营造
**禁止使用**：纯白色或纯灰色的背景

**推荐做法**：
- 使用细腻的渐变背景（避免过于刺眼的视觉效果）
- 使用噪声/颗粒状纹理（通过SVG滤镜或CSS实现）
- 使用几何形状作为背景图案
- 利用层次化的透明度效果增加深度感
- 使用模糊效果营造玻璃质感

```css
/* Subtle grain overlay */
.grain::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url("data:image/svg+xml,...") repeat;
  opacity: 0.03;
  pointer-events: none;
}
```

---

## 以移动设备为先的设计模式
详细的设计规范请参考 **[references/mobile-patterns.md]**。

### 重要设计规则

| 设计模式 | 常见桌面布局 | 移动设备优化方案 |
|---------|---------|------------|
| 主标题隐藏的布局 | 使用2列网格 | 更改为`display: flex`布局 |
| 大型选择列表 | 使用水平滚动条 | 使用折叠式菜单 |
| 多列表单 | 并排显示 | 改为垂直堆叠 |
| 状态提示/警告卡片 | 使用内联布局 | 使用`align-items: center`和`text-align: center` |
| 功能展示网格 | 3-4列布局 | 改为单列显示 |

### 响应式设计断点设置

```css
/* Tablet - stack sidebars */
@media (max-width: 1200px) { }

/* Mobile - full single column */
@media (max-width: 768px) { }

/* Small mobile - compact spacing */
@media (max-width: 480px) { }
```

### 字体缩放规则

```css
@media (max-width: 768px) {
  .hero-title { font-size: 32px; }      /* from ~48px */
  .section-title { font-size: 24px; }   /* from ~32px */
  .section-subtitle { font-size: 14px; } /* from ~16px */
}
```

---

## 开发工作流程

### 选项A：使用Vite（纯静态网站）

```bash
# 1. Initialize
bash scripts/init-vite.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Build static files
npm run build
# Output: dist/

# 4. Bundle to single HTML (optional)
bash scripts/bundle-artifact.sh
# Output: bundle.html
```

### 选项B：使用Next.js（支持Vercel部署）

```bash
# 1. Initialize
bash scripts/init-nextjs.sh my-site
cd my-site

# 2. Develop
npm run dev

# 3. Deploy to Vercel
vercel
```

---

## 项目结构

### 使用Vite构建静态网站
```
my-site/
├── src/
│   ├── components/     # React components
│   ├── lib/           # Utilities, cn()
│   ├── styles/        # Global CSS
│   ├── config/
│   │   └── site.ts    # Editable content config
│   ├── App.tsx
│   └── main.tsx
├── index.html
├── tailwind.config.ts
└── package.json
```

### 使用Next.js构建网站
```
my-site/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── privacy/page.tsx
├── components/
├── lib/
├── config/
│   └── site.ts
└── tailwind.config.ts
```

---

## 网站配置规范
所有可编辑的内容应保存在一个文件中：

```typescript
// config/site.ts
export const siteConfig = {
  name: "Acme AI",
  tagline: "Write better, faster",
  description: "AI-powered writing assistant",
  
  hero: {
    badge: "Now in beta",
    title: "Your words,\nsupercharged",
    subtitle: "Write 10x faster with AI that understands your style",
    cta: { text: "Get Started", href: "/signup" },
    secondaryCta: { text: "Watch Demo", href: "#demo" },
  },
  
  features: [
    { icon: "Zap", title: "Lightning Fast", description: "..." },
    // ...
  ],
  
  pricing: [
    { name: "Free", price: 0, features: [...] },
    { name: "Pro", price: 19, features: [...], popular: true },
  ],
  
  faq: [
    { q: "How does it work?", a: "..." },
  ],
  
  footer: {
    links: [...],
    social: [...],
  }
}
```

---

## 开发前的检查清单
在最终确定设计之前，请完成以下检查：

### 设计质量
- 字体设计具有辨识度（避免使用Inter/Roboto/Arial）
- 色彩搭配中明确区分主导色和强调色
- 背景具有丰富的视觉氛围（避免使用纯白色或纯灰色）
- 至少有一个令人难忘的设计元素
- 动画效果设计得当（避免杂乱无章）

### 移动设备响应性
- 在移动设备上，主标题能够正确显示（避免空白网格）
- 所有网格布局都能调整为单列显示
- 表单元素能够垂直堆叠
- 大型列表使用折叠式菜单（避免水平滚动）
- 字体大小能够根据屏幕尺寸自动调整

### 表单设计的一致性
- 所有输入框、选择框和文本区域的样式统一
- 单选框和复选框的可见性得到保障（检查透明边框样式）
- 下拉菜单的背景颜色清晰可见
- 标签文字使用CSS变量（避免使用固定颜色）

### 可访问性
- 颜色对比度符合WCAG 4.5标准（文本对比度4:1，用户界面对比度3:1）
- 鼠标聚焦时的状态变化能够被用户察觉
- 使用语义化的HTML结构（导航栏、主要内容区域、不同章节）
- 图片配有适当的alt文本
- 键盘导航功能正常可用

---

## shadcn/ui组件库
shadcn/ui提供了10个常用的组件（按钮、徽章、卡片、折叠菜单、对话框、导航菜单、标签页、分隔符、头像、警告框）。可以通过`npx shadcn@latest add [组件名称]`命令添加新组件，或使用`npx shadcn@latest add --all`命令安装所有组件。

详细组件信息请参考 **[references/shadcn-components.md]**。

**常用组件示例**：
- `Button` 和 `Badge`：用于点击链接和显示信息
- `Card`：用于展示功能或价格信息
- `Accordion`：用于展示常见问题解答
- `Dialog`：用于弹出提示框或视频播放器
- `NavigationMenu`：用于导航栏
- `Tabs`：用于展示不同功能模块
- `Carousel`：用于展示推荐内容

---

## 参考资料
- **[references/design-philosophy.md]**：关于如何避免设计中的低质量元素的指导
- **[references/mobile-patterns.md]**：详细的响应式设计规范
- **[references/shadcn-components.md]**：组件使用指南
- **[templates/site-config.ts]**：完整的网站配置示例

---

## 设计示例
**输入要求**：
> “为摄影师制作的作品集网站，采用简洁的编辑风格，包含网格布局的图片库、关于页面和联系表单。”

**设计决策**：
- 设计风格：编辑风格/杂志风格
- 字体：使用Cormorant Garamond作为标题字体，正文使用Plus Jakarta Sans
- 色彩：背景色为接近黑色的#0c0c0c，文字颜色为温暖的#f5f5f0，强调色为铜色#b87333
- 令人难忘的设计元素：滚动时逐渐显示的图片和文字
- 动画效果：图片在滚动时逐渐淡入

**最终成果**：一个完整的Next.js项目，包含响应式图片库、图片轮播效果以及带有验证功能的联系表单。

---

*本指南基于Anthropic的前端设计理念、web-artifacts-builder工具以及社区提供的frontend-design-v2开发经验编写。*
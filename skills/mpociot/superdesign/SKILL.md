---
name: frontend-design
description: 专家级前端设计指南：用于打造美观、现代的用户界面。适用于构建登录页面、仪表板或任何类型的用户界面。
metadata: {"clawdbot":{"emoji":"🎨"}}
---

# 前端设计技能

在创建 UI 组件、登录页面、仪表板或任何前端设计工作时，请使用此技能。

## 设计工作流程

遵循以下结构化的 UI 设计方法：

1. **布局设计** — 确定组件结构，绘制 ASCII 线框图
2. **主题设计** — 定义颜色、字体、间距和阴影效果
3. **动画设计** — 规划微交互和过渡效果
4. **实现** — 生成实际代码

### 1. 布局设计

在编写代码之前，先用 ASCII 格式绘制布局草图：

```
┌─────────────────────────────────────┐
│         HEADER / NAV BAR            │
├─────────────────────────────────────┤
│                                     │
│            HERO SECTION             │
│         (Title + CTA)               │
│                                     │
├─────────────────────────────────────┤
│   FEATURE   │  FEATURE  │  FEATURE  │
│     CARD    │   CARD    │   CARD    │
├─────────────────────────────────────┤
│            FOOTER                   │
└─────────────────────────────────────┘
```

### 2. 主题指南

**颜色规则：**
- **切勿使用通用的 Bootstrap 风格的蓝色（#007bff）** — 这种颜色已经过时了
- 建议使用 `oklch()` 来定义现代颜色
- 使用语义化颜色变量（如 `--primary`、`--secondary`、`--muted` 等）
- 从一开始就考虑亮色模式和暗色模式

**字体选择（Google Fonts）：**
```
Sans-serif: Inter, Roboto, Poppins, Montserrat, Outfit, Plus Jakarta Sans, DM Sans, Space Grotesk
Monospace: JetBrains Mono, Fira Code, Source Code Pro, IBM Plex Mono, Space Mono, Geist Mono
Serif: Merriweather, Playfair Display, Lora, Source Serif Pro, Libre Baskerville
Display: Architects Daughter, Oxanium
```

**间距与阴影效果：**
- 保持一致的间距比例（基础单位为 0.25rem）
- 阴影效果要柔和，避免使用过于明显的阴影效果
- 也可以使用 `oklch()` 来设置阴影颜色

### 3. 主题样式

**现代暗色模式（Vercel/Linear 风格）：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.970 0 0);
  --muted: oklch(0.970 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --border: oklch(0.922 0 0);
  --radius: 0.625rem;
  --font-sans: Inter, system-ui, sans-serif;
}
```

**新 Brutalism 风格（90 年代网页风格复兴）：**
```css
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0 0 0);
  --primary: oklch(0.649 0.237 26.97);
  --secondary: oklch(0.968 0.211 109.77);
  --accent: oklch(0.564 0.241 260.82);
  --border: oklch(0 0 0);
  --radius: 0px;
  --shadow: 4px 4px 0px 0px hsl(0 0% 0%);
  --font-sans: DM Sans, sans-serif;
  --font-mono: Space Mono, monospace;
}
```

**Glassmorphism 风格：**
```css
.glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 1rem;
}
```

### 4. 动画设计指南

**动画规划的基本语法：**
```
button: 150ms [S1→0.95→1] press
hover: 200ms [Y0→-2, shadow↗]
fadeIn: 400ms ease-out [Y+20→0, α0→1]
slideIn: 350ms ease-out [X-100→0, α0→1]
bounce: 600ms [S0.95→1.05→1]
```

**常见动画效果：**
- 进入动画：300-500 毫秒，采用缓动效果（ease-out）
- 鼠标悬停效果：150-200 毫秒
- 按钮点击效果：100-150 毫秒
- 页面切换效果：300-400 毫秒

### 5. 实现规则

**使用 Tailwind CSS：**
```html
<!-- Import via CDN for prototypes -->
<script src="https://cdn.tailwindcss.com"></script>
```

**Flowbite 组件库：**
```html
<link href="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/flowbite@2.0.0/dist/flowbite.min.js"></script>
```

**图标（Lucide 图标库）：**
```html
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>
<script>lucide.createIcons();</script>
```

**图片：**
- 使用可靠的图片占位服务，如 Unsplash 或 placehold.co
- **切勿自行编写图片 URL**  
- **示例：`https://images.unsplash.com/photo-xxx?w=800&h=600`  

### 6. 响应式设计**

始终以移动设备优先进行设计，并确保网站具有响应式特性：

```css
/* Mobile first */
.container { padding: 1rem; }

/* Tablet */
@media (min-width: 768px) {
  .container { padding: 2rem; }
}

/* Desktop */
@media (min-width: 1024px) {
  .container { max-width: 1200px; margin: 0 auto; }
}
```

### 7. 可访问性

- 使用语义化的 HTML 结构（如 `header`、`main`、`nav`、`section`、`article`）
- 添加适当的标题层级（h1 → h2 → h3）
- 为交互式元素添加 `aria-label` 属性
- 确保足够的颜色对比度（至少为 4.5:1）
- 支持键盘导航

### 8. 组件设计技巧

**卡片组件：**
- 使用柔和的阴影效果，避免使用过于明显的阴影
- 保持一致的内边距（通常为 p-4 到 p-6）
- 鼠标悬停时，卡片会略微抬高并增加阴影效果

**按钮组件：**
- 明确的视觉层次结构（主要按钮、次要按钮、隐藏按钮）
- 按钮的触控目标区域应足够大（至少 44x44 像素）
- 显示加载状态和禁用状态

**表单组件：**
- 在输入框上方添加清晰的标签
- 显示焦点状态
- 提供内联的验证反馈信息
- 保持字段之间的适当间距

**导航组件：**
- 在长页面中使用固定头栏
- 明确显示活动状态
- 为移动设备提供友好的汉堡菜单

---

## 快速参考

| 元素 | 推荐使用的样式/库 |
|---------|---------------|
| 主要字体 | Inter, Outfit, DM Sans |
| 代码字体 | JetBrains Mono, Fira Code |
| 边框半径 | 0.5rem 至 1rem（现代风格），0（极简风格） |
| 阴影效果 | 阴影效果要柔和，最多使用 1-2 层 |
| 间距 | 基本单位为 4px（0.25rem） |
| 动画效果 | 动画时长 150-400 毫秒，采用缓动效果（ease-out） |
| 颜色** | 建议使用 `oklch()` 来定义颜色，避免使用通用的蓝色 |

---

*基于 SuperDesign 的设计模式 — https://superdesign.dev*
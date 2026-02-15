---
name: responsive-design
model: standard
---

# 响应式设计

现代响应式设计采用容器查询（container queries）、流动式排版（fluid typography）、CSS网格（CSS Grid）以及“以移动设备为先”（mobile-first）的策略。

## 什么是响应式设计

响应式设计的核心技术包括：
- **容器查询**：用于实现组件级别的响应式布局
- **流动式排版与间距控制**：使用 `clamp()` 函数来调整文本大小和间距
- **CSS网格与Flexbox布局**：灵活的布局方式
- **“以移动设备为先”的断点策略**：确保移动设备上的用户体验
- **响应式图片与媒体资源**：根据设备屏幕尺寸自动调整图片显示方式
- **视口单位（viewport units）**：确保内容在不同设备上正确显示

## 适用场景

- 构建能够适应各种屏幕尺寸的布局
- 创建能够根据容器大小自动调整的复用组件
- 实现可伸缩的文本排版效果
- 设置响应式的网格系统
- 设计适用于移动设备的导航界面
- 优化图片以适应不同设备的显示需求

## 关键术语

- 响应式（responsive）
- 容器查询（container query）
- 媒体查询（media query）
- 断点（breakpoint）
- 以移动设备为先（mobile-first）
- 流动式排版（fluid typography）
- CSS网格（CSS Grid）
- Flexbox
- 视口（viewport）
- 自适应布局（adaptive layout）
- 响应式图片（responsive images）

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install responsive-design
```


---

## 断点设置（以移动设备为先）

```css
/* Base: Mobile (< 640px) - no media query needed */

@media (min-width: 640px)  { /* sm: Large phones, small tablets */ }
@media (min-width: 768px)  { /* md: Tablets */ }
@media (min-width: 1024px) { /* lg: Laptops */ }
@media (min-width: 1280px) { /* xl: Desktops */ }
@media (min-width: 1536px) { /* 2xl: Large screens */ }
```

**Tailwind CSS中的对应属性：** `sm:`, `md:`, `lg:`, `xl:`, `2xl:`

---

## 容器查询

实现与视口无关的组件级响应式布局：

```css
/* Define containment context */
.card-container {
  container-type: inline-size;
  container-name: card;
}

/* Query the container, not viewport */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card-title {
    font-size: 1.5rem;
  }
}

/* Container query units */
.card-title {
  font-size: clamp(1rem, 5cqi, 2rem); /* 5% of container inline-size */
}
```

### Tailwind CSS中的容器查询语法

```tsx
function ResponsiveCard({ title, image, description }) {
  return (
    <div className="@container">
      <article className="flex flex-col @md:flex-row @md:gap-4">
        <img
          src={image}
          alt=""
          className="w-full @md:w-48 @lg:w-64 aspect-video @md:aspect-square object-cover"
        />
        <div className="p-4 @md:p-0">
          <h2 className="text-lg @md:text-xl @lg:text-2xl font-semibold">
            {title}
          </h2>
          <p className="mt-2 text-muted-foreground @md:line-clamp-3">
            {description}
          </p>
        </div>
      </article>
    </div>
  )
}
```

---

## 流动式排版

**CSS自定义属性的应用**

```css
:root {
  --text-xs:  clamp(0.75rem,  0.7rem + 0.25vw, 0.875rem);
  --text-sm:  clamp(0.875rem, 0.8rem + 0.375vw, 1rem);
  --text-base: clamp(1rem,    0.9rem + 0.5vw, 1.125rem);
  --text-lg:  clamp(1.125rem, 1rem + 0.625vw, 1.25rem);
  --text-xl:  clamp(1.25rem,  1rem + 1.25vw, 1.5rem);
  --text-2xl: clamp(1.5rem,   1.25rem + 1.25vw, 2rem);
  --text-3xl: clamp(1.875rem, 1.5rem + 1.875vw, 2.5rem);
  --text-4xl: clamp(2.25rem,  1.75rem + 2.5vw, 3.5rem);
}

h1 { font-size: var(--text-4xl); }
h2 { font-size: var(--text-3xl); }
h3 { font-size: var(--text-2xl); }
p  { font-size: var(--text-base); }
```

## 流动式间距控制

**使用 `clamp()` 的方法**

```css
:root {
  --space-xs: clamp(0.25rem, 0.2rem + 0.25vw, 0.5rem);
  --space-sm: clamp(0.5rem,  0.4rem + 0.5vw, 0.75rem);
  --space-md: clamp(1rem,    0.8rem + 1vw, 1.5rem);
  --space-lg: clamp(1.5rem,  1.2rem + 1.5vw, 2.5rem);
  --space-xl: clamp(2rem,    1.5rem + 2.5vw, 4rem);
}
```

## CSS网格布局

**自动适应的网格布局**

```css
.grid-auto {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: 1.5rem;
}
```

**命名网格区域**

```css
.page-layout {
  display: grid;
  grid-template-areas:
    "header"
    "main"
    "sidebar"
    "footer";
  gap: 1rem;
}

@media (min-width: 768px) {
  .page-layout {
    grid-template-columns: 1fr 300px;
    grid-template-areas:
      "header header"
      "main sidebar"
      "footer footer";
  }
}

@media (min-width: 1024px) {
  .page-layout {
    grid-template-columns: 250px 1fr 300px;
    grid-template-areas:
      "header header header"
      "nav main sidebar"
      "footer footer footer";
  }
}

.header  { grid-area: header; }
.main    { grid-area: main; }
.sidebar { grid-area: sidebar; }
.footer  { grid-area: footer; }
```

**Tailwind CSS中的网格系统**

```tsx
function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 md:gap-6">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}
```

---

## 响应式导航

**设计适用于移动设备的导航系统**

```tsx
function ResponsiveNav({ items }) {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <nav className="relative">
      {/* Mobile toggle */}
      <button
        className="lg:hidden p-2"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-controls="nav-menu"
      >
        <span className="sr-only">Toggle navigation</span>
        {isOpen ? <X /> : <Menu />}
      </button>

      {/* Navigation links */}
      <ul
        id="nav-menu"
        className={cn(
          // Mobile: dropdown
          "absolute top-full left-0 right-0 bg-background border-b",
          "flex flex-col",
          isOpen ? "flex" : "hidden",
          // Desktop: horizontal, always visible
          "lg:static lg:flex lg:flex-row lg:border-0"
        )}
      >
        {items.map(item => (
          <li key={item.href}>
            <a
              href={item.href}
              className="block px-4 py-3 lg:px-3 lg:py-2 hover:bg-muted lg:hover:bg-transparent"
            >
              {item.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  )
}
```

---

## 响应式图片

**使用`Picture`元素实现艺术效果**

```tsx
function ResponsiveHero() {
  return (
    <picture>
      {/* Different crops for different screens */}
      <source media="(min-width: 1024px)" srcSet="/hero-wide.webp" type="image/webp" />
      <source media="(min-width: 768px)" srcSet="/hero-medium.webp" type="image/webp" />
      <source srcSet="/hero-mobile.webp" type="image/webp" />
      
      <img
        src="/hero-mobile.jpg"
        alt="Hero description"
        className="w-full h-auto"
        loading="eager"
        fetchPriority="high"
      />
    </picture>
  )
}
```

**通过`srcset`实现分辨率切换**

```tsx
function ProductImage({ product }) {
  return (
    <img
      src={product.image}
      srcSet={`
        ${product.image}?w=400 400w,
        ${product.image}?w=800 800w,
        ${product.image}?w=1200 1200w
      `}
      sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
      alt={product.name}
      className="w-full h-auto object-cover"
      loading="lazy"
    />
  )
}
```

## 响应式表格

**水平滚动布局**

```tsx
function ResponsiveTable({ data, columns }) {
  return (
    <div className="w-full overflow-x-auto">
      <table className="w-full min-w-[600px]">
        <thead>
          <tr>
            {columns.map(col => (
              <th key={col.key} className="text-left p-3">{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i) => (
            <tr key={i} className="border-t">
              {columns.map(col => (
                <td key={col.key} className="p-3">{row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```

**移动设备上的卡片布局**

```tsx
function ResponsiveDataTable({ data, columns }) {
  return (
    <>
      {/* Desktop: table */}
      <table className="hidden md:table w-full">
        {/* standard table markup */}
      </table>

      {/* Mobile: cards */}
      <div className="md:hidden space-y-4">
        {data.map((row, i) => (
          <div key={i} className="border rounded-lg p-4 space-y-2">
            {columns.map(col => (
              <div key={col.key} className="flex justify-between">
                <span className="font-medium text-muted-foreground">{col.label}</span>
                <span>{row[col.key]}</span>
              </div>
            ))}
          </div>
        ))}
      </div>
    </>
  )
}
```

## 视口单位

**使用视口单位确保布局正确显示**

```css
/* Standard viewport units - problematic on mobile */
.full-height { height: 100vh; }

/* Dynamic viewport units (recommended) */
.full-height-dynamic { height: 100dvh; } /* Accounts for mobile browser UI */

/* Small viewport (minimum when UI shown) */
.min-full-height { min-height: 100svh; }

/* Large viewport (maximum when UI hidden) */
.max-full-height { max-height: 100lvh; }
```

## 最佳实践

- **以移动设备为先**：先为移动设备编写基础样式，再针对更大屏幕进行优化
- **根据内容设置断点**：根据内容的显示方式设置断点，而非设备屏幕尺寸
- **优先使用流动式布局**：使用 `clamp()` 和相对单位，而非固定的 `px`
- **使用容器查询**：实现组件级别的响应式设计
- **触摸目标**：移动设备上的触摸目标应至少为 44×44px
- **在实际设备上进行测试**：模拟器无法完全模拟所有问题
- **使用逻辑化的属性**：使用 `inline`/`block` 类属性以实现国际化

---

## 常见问题及解决方法

| 问题 | 原因 | 解决方法 |
|-------|-------|-----|
| 水平滚动问题** | 图片或元素宽度固定 | 使用相对单位，例如 `max-width: 100%` |
| 在移动设备上页面高度过高** | 由于地址栏占用空间 | 使用 `100dvh` 或 `100svh` |
| 触摸目标过小** | 设计针对桌面设备 | 交互元素的尺寸至少为 44px |
| 图片破坏布局** | 缺少尺寸限制 | 添加 `max-width: 100%; height: auto;` |
| 文本显示过小** | 字体大小固定 | 使用 `clamp()` 实现可伸缩的文本排版 |

---

## 避免的错误做法

- **避免使用 `px` 作为排版单位**：应使用 `rem` 作为相对单位
- **不要忽略在实际设备上的测试**：模拟器无法完全模拟真实设备的显示效果
- **忽略触摸目标的大小要求**：触摸目标至少应为 44×44px
- **在移动设备上使用 `100vh` 且不设置备用方案**：这可能导致布局问题
- **过度使用媒体查询**：过多的媒体查询会降低代码的可读性
- **忽略基于内容的断点设置**：应优先使用基于设备特性的断点设置
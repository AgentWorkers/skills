# 网页性能引擎

这是一个完整的网页性能优化系统，能够进行审计、诊断、修复和监控——无需使用任何外部工具（但可集成Lighthouse、WebPageTest和Chrome DevTools等工具）。

## 第1阶段：性能审计

### 快速健康检查

按顺序执行以下检查，找到性能瓶颈后停止。

**第1层级——关键问题（阻碍渲染）：**
- [ ] 首字节时间（TTFB）> 800ms → 服务器问题
- [ ] 首次内容绘制时间（FCP）> 1.8s → 阻碍渲染的资源
- [ ] 最大内容绘制时间（LCP）> 2.5s → 标题元素问题
- [ ] 总阻塞时间（TBT）> 200ms → JavaScript问题
- [ ] 累积布局偏移（CLS）> 0.1 → 布局不稳定
- [ ] 下一次绘制前的交互时间（INP）> 200ms → 事件处理程序问题

**第2层级——重要问题（影响用户体验）：**
- [ ] 页面大小 > 2MB
- [ ] 请求数量 > 80个
- [ ] JavaScript文件大小 > 500KB（压缩后）
- [ ] 图片总大小 > 1MB
- [ ] 未使用压缩算法（gzip/brotli）
- [ ] 未设置缓存头信息

**第3层级——提升性能（获得竞争优势）：**
- [ ] 速度指数 > 3.4秒
- [ ] 交互时间 > 3.8秒
- [ ] 字体加载导致页面卡顿
- [ ] 第三方脚本占JavaScript代码的30%以上

### 审计简要模板

```yaml
audit:
  url: ""
  device: "mobile"  # mobile | desktop | both
  connection: "4G"  # 3G | 4G | fiber
  region: ""        # closest to target users
  
scores:
  performance: null  # 0-100
  fcp_ms: null
  lcp_ms: null
  tbt_ms: null
  cls: null
  inp_ms: null
  ttfb_ms: null
  
page_weight:
  total_kb: null
  html_kb: null
  css_kb: null
  js_kb: null
  images_kb: null
  fonts_kb: null
  other_kb: null
  
requests:
  total: null
  by_type: {}
  third_party_count: null
  third_party_kb: null
```

### 无需工具获取指标

如果无法使用Lighthouse/DevTools，可以使用以下基于Web的工具：
1. `web_fetch "https://pagespeed.web.dev/analysis?url={encoded_url}"` —— 谷歌提供的免费工具
2. `web_search "webpagetest {url}"` —— 查找缓存结果
3. `web_search "site:{domain} core web vitals"` —— 获取CrUX数据
4. 检查`<head>`部分，查找明显的性能问题：阻碍渲染的CSS/JavaScript代码、缺失的预加载资源、未设置的meta viewport标签

## 第2阶段：诊断——性能问题分析

### 关键渲染路径分析

```
DNS → TCP → TLS → TTFB → HTML Parse → CSSOM → Render Tree → FCP → LCP
                                ↓
                         JS Download → Parse → Execute → INP
```

**瓶颈决策树：**

```
High TTFB (>800ms)?
├─ YES → Phase 3A: Server optimization
└─ NO → High FCP (>1.8s)?
    ├─ YES → Phase 3B: Render-blocking resources
    └─ NO → High LCP (>2.5s)?
        ├─ YES → Phase 3C: Hero element optimization
        └─ NO → High TBT (>200ms)?
            ├─ YES → Phase 3D: JavaScript optimization
            └─ NO → High CLS (>0.1)?
                ├─ YES → Phase 3E: Layout stability
                └─ NO → High INP (>200ms)?
                    ├─ YES → Phase 3F: Interaction optimization
                    └─ NO → ✅ Performance is good!
```

### 资源影响评分

根据资源对性能的影响进行评分：

| 因素 | 权重 | 1分 | 3分 | 5分 |
|--------|--------|---------|---------|---------|
| 大小（KB） | 3倍 | <10KB | 10-100KB | >100KB |
| 阻碍渲染 | 5倍 | 无 | 部分影响 | 完全影响 |
| 屏幕可见范围内的资源 | 4倍 | 无影响 | 间接影响 | 直接影响 |
| 可缓存的资源 | 2倍 | 缓存时间长 | 缓存时间短 | 无法缓存 |
| 可压缩的资源 | 2倍 | 已经压缩 | 可以压缩 | 未压缩 |

**优先级 = 因素权重之和。优先修复得分最高的资源。**

## 第3阶段：修复方案

### 3A：服务器优化（TTFB）

**快速优化措施：**
```
# CDN: If no CDN, this is #1 priority
# Check: curl -sI {url} | grep -i 'x-cache\|cf-cache\|x-cdn'

# Compression: Must have brotli or gzip
# Check: curl -sI -H "Accept-Encoding: br,gzip" {url} | grep -i content-encoding

# HTTP/2 or HTTP/3
# Check: curl -sI --http2 {url} | head -1
```

**服务器端检查清单：**
- [ ] 使用CDN加速（Cloudflare、Fastly、CloudFront）
- [ ] 启用Brotli压缩（压缩效果比gzip好20-30%）
- [ ] 使用HTTP/2协议，如可能使用HTTP/3
- [ ] 服务器端缓存（Redis、Varnish）
- [ ] 优化数据库查询（每个查询时间<50ms）
- [ ] 启用连接池
- [ ] 对动态内容使用边缘计算（Workers、Lambda@Edge）

**缓存头信息模板：**
```
# Static assets (CSS, JS, images, fonts)
Cache-Control: public, max-age=31536000, immutable

# HTML pages
Cache-Control: public, max-age=0, must-revalidate

# API responses
Cache-Control: private, max-age=60, stale-while-revalidate=300
```

### 3B：阻碍渲染的资源（FCP）

**CSS优化：**
```html
<!-- BEFORE: Render-blocking -->
<link rel="stylesheet" href="styles.css">

<!-- AFTER: Critical CSS inline + async load -->
<style>/* Critical above-fold CSS here (< 14KB) */</style>
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>
```

**规则：**
- 将关键CSS代码内联（屏幕可见范围内的样式，大小<14KB）
- 延迟加载非关键CSS
- 删除未使用的CSS代码（通常可节省60-90%的加载时间）
- 合并媒体查询
- 避免使用`@import`指令（会导致代码顺序加载）

**JavaScript优化：**
```html
<!-- BEFORE: Render-blocking -->
<script src="app.js"></script>

<!-- AFTER: Non-blocking -->
<script src="app.js" defer></script>

<!-- OR: Independent scripts -->
<script src="analytics.js" async></script>
```

**规则：**
- 对应用程序脚本使用`defer`属性（保持加载顺序，在解析完成后执行）
- 对独立脚本（如分析脚本、广告脚本）使用`async`属性
- 确保`<script>`标签不直接放在`<head>`中，而使用`defer`或`async`属性
- 将小脚本代码内联（大小<1KB）

### 3C：标题元素优化（LCP）

**LCP元素的优化方法：**

| LCP元素 | 优化措施 |
|------------|-----|
| `<img>` | 预加载图片 + 采用响应式设计 + 使用现代图片格式 |
| `<video>` | 预加载海报图片 |
| CSS `background-image` | 预加载图片 + 内联关键CSS |
| 文本块 | 预加载字体 + 设置`font-display`属性 |

**图片优化清单：**
```html
<!-- Optimal hero image -->
<link rel="preload" as="image" href="hero.webp" 
      imagesrcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
      imagesizes="100vw">

<img src="hero.webp" 
     srcset="hero-400.webp 400w, hero-800.webp 800w, hero-1200.webp 1200w"
     sizes="100vw"
     width="1200" height="600"
     alt="Hero description"
     fetchpriority="high"
     decoding="async">
```

**图片格式选择：**
```
Photo/complex image? → WebP (25-35% smaller than JPEG)
                     → AVIF (50% smaller, but slower encode)
Simple graphic/logo? → SVG (scalable, tiny)
                    → PNG only if transparency needed
Animation?          → WebM/MP4 video (not GIF — 90% smaller)
```

**图片大小建议：**
| 视口大小 | 最大图片宽度 | 目标图片大小（KB） |
|----------|-----------|-----------|
| 移动设备 | 400px | < 50KB |
| 平板设备 | 800px | < 100KB |
| 桌面设备 | 1200px | < 150KB |
| 标题/横幅图片 | 1600px | < 200KB |

### 3D：JavaScript优化（TBT）

**JavaScript代码打包分析：**
1. 使用`web_fetch`获取页面的JavaScript代码大小，统计`<script>`标签的数量
2. 识别大型JavaScript库（如React、Lodash、Moment.js）
3. 检查代码包中的重复代码
4. 删除未使用的代码导出

**常见的JavaScript代码优化方法：**

| 库名 | 原始大小（KB） | 替代方案 | 新大小（KB） |
|---------|------|-------------|------|
| moment.js | 67KB | date-fns | 2-10KB |
| lodash（完整版本） | 71KB | lodash-es（经过代码压缩后） | 2-5KB |
| jQuery | 87KB | vanilla JS | 0KB |
| animate.css | 80KB | 使用CSS动画替代 | 1-2KB |
| chart.js | 60KB | 使用lightweight-charts替代 | 40KB |

**代码分割策略：**
- 根据页面需求分割JavaScript代码（每个页面加载自己的JavaScript代码包）
- 对于复杂组件（如模态框、编辑器、图表）进行组件级别的代码分割
- 对于不在屏幕可见范围内的功能，使用动态导入（例如：`const Chart = lazy(() => import('./Chart'))`

**长期优化任务：**
```javascript
// BEFORE: Blocks main thread 200ms+
function processLargeList(items) {
  items.forEach(item => heavyComputation(item));
}

// AFTER: Yields to main thread
async function processLargeList(items) {
  for (const item of items) {
    heavyComputation(item);
    // Yield every 50ms
    if (performance.now() - start > 50) {
      await scheduler.yield(); // or setTimeout(0)
      start = performance.now();
    }
  }
}
```

### 3E：布局稳定性（CLS）

**常见的CLS问题及解决方法：**

| 问题原因 | 解决方法 |
|-------|-----|
| 图片没有尺寸信息 | 为所有图片设置`width`和`height`属性 |
| 广告/嵌入内容没有固定位置 | 使用`aspect-ratio`或`min-height`属性设置图片位置 |
| 动态内容插入导致布局变化 | 使用CSS的`contain`属性或预留布局空间 |
| Web字体导致页面重新布局 | 将`font-display`属性设置为`optional`或`swap` |

**防止CLS的优化方法：**
```css
/* Reserve space for dynamic content */
.ad-slot { min-height: 250px; }
.embed-container { aspect-ratio: 16/9; }

/* Prevent font swap reflow */
@font-face {
  font-family: 'Brand';
  src: url('brand.woff2') format('woff2');
  font-display: optional; /* No swap = no shift */
  size-adjust: 105%; /* Match fallback metrics */
}

/* Contain layout shifts */
.dynamic-widget {
  contain: layout;
  min-height: 200px;
}
```

### 3F：交互优化（INP）

**事件处理程序优化：**
- 将事件处理程序的响应时间控制在50ms以内
- 对滚动/缩放操作进行去抖动处理（延迟100-150ms）
- 使用`requestAnimationFrame`处理视觉更新
- 将计算密集型操作卸载到Web Workers中
- 对不在屏幕可见范围内的内容使用`content-visibility: auto`属性

**输入响应性优化：**
```javascript
// BEFORE: Blocks during type
input.addEventListener('input', (e) => {
  expensiveFilter(e.target.value); // 100ms+ 
});

// AFTER: Debounced + visual feedback
input.addEventListener('input', (e) => {
  showSpinner(); // Instant visual feedback
  debounce(() => expensiveFilter(e.target.value), 150);
});
```

## 第4阶段：资源加载策略

### 预加载/预连接/预连接策略

```html
<!-- Preconnect: Third-party origins you'll need soon -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://cdn.example.com" crossorigin>

<!-- DNS-prefetch: Third-party origins you might need -->
<link rel="dns-prefetch" href="https://analytics.example.com">

<!-- Preload: Critical resources for THIS page -->
<link rel="preload" href="critical.css" as="style">
<link rel="preload" href="hero.webp" as="image">
<link rel="preload" href="brand.woff2" as="font" type="font/woff2" crossorigin>

<!-- Prefetch: Resources for NEXT page (low priority) -->
<link rel="prefetch" href="/next-page.js">

<!-- Modulepreload: ES modules -->
<link rel="modulepreload" href="app.mjs">
```

**规则：**
- 每页最多预加载3-5个资源（更多资源会降低性能）
- 必须预加载的资源：LCP图片、关键字体、屏幕可见范围内的CSS代码
- 对已知的第三方资源地址进行预连接（最多4-6个）
- 仅在网络速度快的情况下进行预加载

### 拖动加载策略

```
Above fold (viewport):     fetchpriority="high", no lazy
Below fold (1-2 screens):  loading="lazy", decoding="async"
Way below fold:            Intersection Observer, load on demand
Off-screen widgets:        content-visibility: auto
```

### 字体加载优化

```css
/* Optimal font loading */
@font-face {
  font-family: 'Brand';
  src: url('brand.woff2') format('woff2');
  font-display: swap;
  unicode-range: U+0000-00FF; /* Latin only if applicable */
}
```

**字体检查清单：**
- [ ] 仅使用WOFF2格式的字体文件（压缩效果最佳）
- 仅加载必要的字体子集（拉丁字母字体）
- 最多加载2-3个字体家族
- 总共加载不超过4个字体文件（常规字体、加粗字体、斜体字体）
- 预加载关键字体文件
- 考虑使用系统的默认字体栈

**系统默认字体栈：**
```css
/* Modern system fonts — zero network cost */
font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;

/* Monospace */
font-family: ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, monospace;
```

## 第5阶段：第三方脚本管理

### 第三方脚本的影响评估

```yaml
third_party_audit:
  - script: "Google Analytics 4"
    size_kb: 45
    blocks_render: false
    loads_more_scripts: true
    total_impact_kb: 90
    essential: true
    mitigation: "gtag async, delay until interaction"
    
  - script: "Intercom chat widget"
    size_kb: 200
    blocks_render: false
    loads_more_scripts: true
    total_impact_kb: 450
    essential: false
    mitigation: "Load on scroll/click, not page load"
```

**第三方脚本的加载策略：**
```javascript
// Strategy 1: Load on interaction
document.addEventListener('scroll', () => {
  loadThirdParty('chat-widget.js');
}, { once: true });

// Strategy 2: Load after page is idle
requestIdleCallback(() => {
  loadThirdParty('analytics.js');
});

// Strategy 3: Facade pattern (show placeholder until needed)
chatButton.addEventListener('click', () => {
  loadThirdParty('intercom.js').then(() => Intercom('show'));
});
```

**规则：**
- 每季度对所有第三方脚本进行审计
- 每个第三方脚本的使用都需要有明确的业务理由
- 如果脚本大小超过100KB，需要制定相应的加载策略
- 尽量自托管第三方脚本（如字体、分析脚本）
- 在所有外部链接上添加`rel="noopener"`属性

## 第6阶段：移动设备性能优化

### 针对移动设备的特定优化措施

**在4G网络下的移动设备性能指标：**
| 指标 | 优秀 | 需要优化 | 较差 |
|--------|------|------------|------|
| FCP | < 1.8秒 | 1.8-3.0秒 | > 3.0秒 |
| LCP | < 2.5秒 | 2.5-4.0秒 | > 4.0秒 |
| TBT | < 200ms | 200-600ms | > 600ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |
| INP | < 200ms | 200-500ms | > 500ms |

**针对移动设备的检查清单：**
- [ ] 页面中包含`viewport`元标签 |
- [ ] 触控目标元素的尺寸≥48×48px |
- [ ] 页面没有水平滚动条 |
- [ ] 图片具有响应式设计（使用`srcset`和`sizes`属性）
- 移动设备上的JavaScript文件大小<300KB（压缩后）
- 关键CSS代码大小<14KB（能在一次TCP数据传输中加载完成）
- 避免使用复杂的CSS效果（如复杂的动画、大的阴影效果）

## 第7阶段：性能预算管理

### 设置性能预算

```yaml
performance_budget:
  metrics:
    lcp_ms: 2500
    fcp_ms: 1800
    tbt_ms: 200
    cls: 0.1
    inp_ms: 200
    
  resources:
    total_kb: 1500
    js_kb: 350
    css_kb: 80
    images_kb: 800
    fonts_kb: 100
    
  requests:
    total: 60
    third_party: 15
    
  lighthouse:
    performance: 90
    accessibility: 90
    best_practices: 90
    seo: 90
```

**预算执行规则：**
- 任何导致JavaScript代码大小增加超过10KB的代码更改都需要有合理的理由
- 如果LCP加载时间超过200ms，将阻止代码部署
- 每月进行一次Lighthouse审计，跟踪性能趋势
- 为单页应用（SPA）设置每页面的预算（首页的预算要求更严格）

**预算监控模板：**
```yaml
# Weekly performance check
date: "YYYY-MM-DD"
url: ""
device: "mobile"

scores:
  lighthouse: null
  lcp: null
  fcp: null
  tbt: null
  cls: null

trend: "improving | stable | degrading"
regressions: []
actions: []
```

## 第8阶段：性能评分标准

对网站进行0-100分的评分：

| 评估维度 | 权重 | 0-2分 | 3-4分 | 5分 |
|-----------|--------|-----|-----|---|
| 核心网页性能指标 | 25% | 所有指标均不达标 | 部分指标达标 | 所有指标均达标 |
| 页面大小 | 15% | 页面大小>5MB | 2-5MB | <2MB |
| 缓存策略 | 15% | 无缓存 | 部分资源有缓存 | 所有资源都缓存 |
| 渲染路径 | 15% | 多个资源阻碍渲染 | 部分资源得到优化 | 关键渲染路径完全优化 |
| 图片优化 | 10% | 图片未优化 | 部分图片得到优化 | 使用WebP/AVIF格式且图片具有响应式设计 |
| JavaScript性能 | 10% | JavaScript文件大小>1MB | 部分JavaScript代码未优化 | 部分JavaScript代码被分割 |
| 第三方脚本管理 | 5% | 第三方脚本未得到有效管理 | 部分脚本被延迟加载 | 所有第三方脚本都得到管理且使用预算控制 |
| 移动设备用户体验 | 5% | 仅适用于桌面设备 | 网站同时支持桌面和移动设备 | 网站优先考虑移动设备体验 |

**评分解读：**
- 90-100分：网站性能优秀，需要持续维护和优化。
- 70-89分：网站性能良好，需要优化部分性能指标。
- 50-69分：网站性能有待提升，需要按照第3阶段的优化方案进行改进。
- <50分：网站性能严重不足，需要从服务器端和阻碍渲染的问题开始优化。

## 第9阶段：常见架构及快速优化方法

### Next.js / React框架**
- 使用`next/image`插件（自动选择WebP格式的图片、延迟加载图片、使用模糊占位符）
- 对静态页面启用ISR或SSG（Server Side Generation）功能
- 对复杂组件使用`dynamic()`函数
- 使用`@next/bundle-analyzer`工具分析代码包大小
- 使用中间件实现边缘缓存

### WordPress框架**
- 安装页面缓存插件（如WP Super Cache、W3 Total Cache）
- 优化图片（使用ShortPixel、Imagify等工具）
- 禁用不必要的插件（不必要的插件会增加JavaScript和CSS文件的加载量）
- 使用CDN插件加速页面加载
- 考虑使用静态页面生成技术（如Simply Static）

### 单页应用（SPA，如React/Vue/Svelte）
- 根据页面路由进行代码分割
- 对SEO页面使用SSR或SSG技术
- 使用Service Worker加速重复访问的页面
- 为长列表页面实现虚拟滚动效果

### 静态网站**
- 如果网站本身已经加载速度快，重点优化图片加载
- 将网站部署到CDN加速服务（如Cloudflare Pages、Netlify、Vercel）
- 将所有关键CSS代码内联到页面中
- 将JavaScript代码大小控制在50KB以内

## 第10阶段：高级优化技术

### Service Worker缓存

```javascript
// Cache-first for static assets
self.addEventListener('fetch', (event) => {
  if (event.request.url.match(/\.(css|js|woff2|webp|avif)$/)) {
    event.respondWith(
      caches.match(event.request).then(cached => cached || fetch(event.request))
    );
  }
});
```

### 用于导航的资源提示

```javascript
// Predictive prefetch on hover
document.querySelectorAll('a').forEach(link => {
  link.addEventListener('mouseenter', () => {
    const prefetch = document.createElement('link');
    prefetch.rel = 'prefetch';
    prefetch.href = link.href;
    document.head.appendChild(prefetch);
  }, { once: true });
});
```

### 生产环境中的性能监控

```javascript
// Report Core Web Vitals
new PerformanceObserver((list) => {
  for (const entry of list.getEntries()) {
    // Send to analytics
    sendToAnalytics({
      metric: entry.name,
      value: entry.value,
      rating: entry.rating, // "good" | "needs-improvement" | "poor"
    });
  }
}).observe({ type: 'largest-contentful-paint', buffered: true });
```

### 特殊情况处理

**无限滚动/分页功能：**
- 对超过100个元素的页面使用虚拟滚动技术
- 使用`Intersection Observer`事件加载页面中的元素
- 对不在屏幕可见范围内的元素使用`content-visibility: auto`属性
- 对DOM节点进行内存管理，移除远离屏幕的元素

**具有客户端路由功能的单页应用：**
- 统计用户的页面导航行为（而不仅仅是首次加载时的行为）
- 报告每个页面的详细性能指标
- 预加载用户可能访问的下一个页面的资源
- 确保每个页面的JavaScript代码大小不超过100KB

**电商产品页面：**
- 预加载首页的第一张产品图片
- 拖动加载评论区及相关产品的内容
- 延迟加载推荐功能相关的JavaScript代码
- 对产品数据使用缓存策略（仅在数据更新时才加载）

**媒体资源密集型网站：**
- 对页面中不在屏幕可见范围内的内容使用延迟加载技术
- 使用`<video>`格式代替GIF格式的图片（GIF格式通常占用更多带宽）
- 根据网络连接情况动态调整图片质量

**常用命令：**
- `audit {url}`：执行完整的第1阶段性能审计
- `fix LCP on {url}`：执行第3C阶段的优化措施
- `what's slowing down {url}？`：查看第2阶段的性能诊断结果
- `set performance budget for {project}`：设置网站的性能预算
- `score {url}`：使用第8阶段的评分标准对网站进行评估
- `optimize images on {url}`：优化该网站的图片
- `reduce JavaScript on {url}`：优化该网站的JavaScript代码
- `fix layout shifts on {url}`：修复该网站的布局问题
- `mobile performance audit for {url}`：对移动设备版本的网站进行性能审计
- `third-party script audit for {url}`：审计该网站使用的第三方脚本
- `weekly performance check for {url}`：定期检查网站的性能
- `compare {url1} vs {url2}`：对比两个网站的性能
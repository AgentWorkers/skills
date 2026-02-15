---
name: web-perf
description: 使用 Chrome DevTools 的 MCP 功能分析网页性能。可以测量核心网页指标（FCP、LCP、TBT、CLS、Speed Index），识别阻碍页面渲染的资源、网络依赖链、布局变化、缓存问题以及可访问性缺陷。适用于需要审计、分析、调试或优化页面加载性能、Lighthouse 评分或网站速度的场景。
---

# 网页性能审计

使用 Chrome DevTools 的 MCP 工具来审计网页性能。本技能重点关注核心网页指标（Core Web Vitals）、网络优化以及高级可访问性问题。

## 第一步：确认 MCP 工具可用性

**在开始之前请执行此操作。** 尝试调用 `navigate_page` 或 `performance_start_trace`。如果这些功能不可用，请立即停止——说明 chrome-devtools MCP 服务器尚未配置。

请用户将以下配置添加到他们的 MCP 配置文件中：

```json
"chrome-devtools": {
  "type": "local",
  "command": ["npx", "-y", "chrome-devtools-mcp@latest"]
}
```

## 关键指导原则

- **确保准确性**：通过检查网络请求、DOM 结构或代码库来验证问题，然后明确地说明发现的结果。
- **在提出建议前先进行验证**：在建议删除某些内容之前，先确认它们确实未被使用。
- **量化影响**：根据分析结果估算节省的时间或资源。不要优先处理对性能几乎没有影响的更改。
- **忽略非问题项**：如果某些资源对页面渲染的影响为 0ms，只需记录下来，无需建议采取行动。
- **具体说明**：例如，应明确指出“将 `hero.png`（450KB）压缩为 WebP 格式”，而不是笼统地说“优化图片”。
- **严格排序优先级**：如果一个网站的 LCP（首次内容绘制时间）为 200ms 且 CLS（布局稳定时间）为 0ms，那么该网站的性能已经非常优秀——请如实说明。

## 快速参考

| 任务 | 工具调用 |
|------|-----------|
| 加载页面 | `navigate_page(url: "...")` |
| 开始性能追踪 | `performance_start_trace(autoStop: true, reload: true)` |
| 分析指标数据 | `performance_analyze_insight(insightSetId: "...", insightName: "...")` |
| 列出网络请求 | `list_network_requests(resourceTypes: ["Script", "Stylesheet", ...])` |
| 请求详情 | `get_network_request(reqid: <id>)` |
| 可访问性快照 | `take_snapshot(verbose: true)` |

## 工作流程

请将此检查清单复制下来以记录审计进度：

```
Audit Progress:
- [ ] Phase 1: Performance trace (navigate + record)
- [ ] Phase 2: Core Web Vitals analysis (includes CLS culprits)
- [ ] Phase 3: Network analysis
- [ ] Phase 4: Accessibility snapshot
- [ ] Phase 5: Codebase analysis (skip if third-party site)
```

### 第一阶段：性能追踪

1. 导航到目标 URL：
   ```
   navigate_page(url: "<target-url>")
   ```

2. 启动性能追踪并重新加载页面，以捕获冷启动（cold-load）时的性能数据：
   ```
   performance_start_trace(autoStop: true, reload: true)
   ```

3. 等待追踪完成，然后获取结果。

**故障排除：**
- 如果追踪结果为空或失败，请先使用 `navigate_page` 确认页面是否正确加载。
- 如果指标名称不一致，请查看追踪响应以获取可用的指标数据。

### 第二阶段：核心网页指标分析

使用 `performance_analyze_insight` 提取关键性能指标。

**注意：** 不同版本的 Chrome DevTools 中的指标名称可能有所不同。如果某个指标名称无法使用，请查看追踪响应中的 `insightSetId` 以获取可用的指标名称。

常见指标名称及说明：

| 指标 | 指标名称 | 需要关注的内容 |
|--------|--------------|------------------|
| LCP | `LCPBreakdown` | 最大内容绘制时间；TTFB（从请求到首次绘制的时间）、资源加载时间、渲染延迟的详细信息 |
| CLS | `CLSCulprits` | 导致布局变化的元素（如没有尺寸信息的图片、插入的内容、字体切换等） |
| Render Blocking | `RenderBlocking` | 阻碍首次绘制的 CSS/JS 代码 |
| Document Latency | `DocumentLatency` | 服务器响应时间问题 |
| Network Dependencies | `NetworkRequestsDepGraph` | 延迟关键资源加载的请求链 |

示例：
```
performance_analyze_insight(insightSetId: "<id-from-trace>", insightName: "LCPBreakdown")
```

**关键阈值（良好/需要改进/较差）：**
- TTFB（从请求到首次绘制的时间）：< 800ms / < 1.8s / > 1.8s
- FCP（首次内容绘制时间）：< 1.8s / < 3s / > 3s
- LCP：< 2.5s / < 4s / > 4s
- INP（初始页面加载时间）：< 200ms / < 500ms / > 500ms
- TBT（从首次绘制到页面完全加载的时间）：< 200ms / < 600ms / > 600ms
- CLS：< 0.1 / < 0.25 / > 0.25
- 速度指数：< 3.4s / < 5.8s / > 5.8s

### 第三阶段：网络分析

列出所有网络请求，以找出优化机会：
```
list_network_requests(resourceTypes: ["Script", "Stylesheet", "Document", "Font", "Image"])
```

**需要关注的内容：**
1. **阻碍渲染的资源**：`<head>` 标签中的 JS/CSS 代码，且没有 `async`/`defer`/`media` 属性。
2. **依赖关系复杂的资源**：由于依赖其他资源的加载而延迟加载的资源（例如，CSS 导入、JavaScript 加载的字体）。
3. **未预加载的关键资源**：字体、重要图片、关键脚本等资源未被预先加载。
4. **缓存问题**：`Cache-Control`、`ETag` 或 `Last-Modified` 标头缺失或设置不当。
5. **较大的文件大小**：未压缩或体积过大的 JS/CSS 文件。
6. **未使用的预连接（preconnect）**：如果系统标记了某些预连接请求，请检查是否有任何实际请求发送到该地址；如果没有请求，则建议移除这些预连接。如果有请求但加载时间较晚，这些预连接可能仍有用。

**详细请求信息：**
```
get_network_request(reqid: <id>)
```

### 第四阶段：可访问性快照

生成可访问性树（accessibility tree）的快照：
```
take_snapshot(verbose: true)
```

**需要关注的常见问题：**
- 缺失或重复的 ARIA 标签。
- 对比度较低的元素（正常文本的对比度应满足 WCAG AA: 4.5:1，大文本的对比度应满足 3:1）。
- 缺少焦点提示或焦点指示器。
- 没有可访问名称的交互元素。

## 第五阶段：代码库分析

**如果审计的网站没有代码库访问权限，则可跳过此步骤。**

分析代码库，了解可以改进的地方。

### 识别使用的框架和打包工具

搜索配置文件以确定所使用的框架和打包工具：

| 工具 | 配置文件 |
|------|--------------|
| Webpack | `webpack.config.js`, `webpack.*.js` |
| Vite | `vite.config.js`, `vite.config.ts` |
| Rollup | `rollup.config.js`, `rollup.config.mjs` |
| esbuild | `esbuild.config.js`，以及使用 `esbuild` 编译的脚本 |
| Parcel | `.parcelrc`, `package.json`（其中包含打包配置） |
| Next.js | `next.config.js`, `next.config.mjs` |
| Nuxt | `nuxt.config.js`, `nuxt.config.ts` |
| SvelteKit | `svelte.config.js` |
| Astro | `astro.config.mjs` |

同时检查 `package.json` 中的依赖项和构建脚本。

### 代码优化

- **Webpack**：检查 `package.json` 中的 `mode: 'production'` 设置、`sideEffects` 选项以及 `usedExports` 优化配置。
- **Vite/Rollup**：默认启用了代码压缩功能；检查 `treeshake` 选项。
- **检查内容**：是否存在重复导入的文件（如 `index.js` 文件），以及是否大量导入不必要的库（例如 `lodash`、`moment`）。
- **未使用的代码**：
  - 检查 JavaScript 中嵌入的 CSS 代码以及是否可以提取出静态 CSS。
  - 查看是否使用了 PurgeCSS/UnCSS 等优化工具（如 Tailwind 的 `content` 配置）。
  - 识别动态导入和提前加载的代码。

### 多态库（Polyfills）的优化

- 检查是否使用了 `@babel/preset-env` 配置以及 `useBuiltIns` 选项。
- 注意是否导入了 `core-js` 等大型库。
- 检查 `browserslist` 配置中是否设置了过宽的浏览器兼容性范围。

### 压缩与代码最小化

- 检查是否使用了 `terser`、`esbuild` 或 `swc` 等工具进行代码压缩。
- 确保构建输出文件使用了 gzip/brotli 压缩算法。
- 在生产环境中，检查是否关闭了源代码映射（source maps）。

## 输出格式

将审计结果呈现为以下形式：

1. **核心网页指标汇总**：包含各项指标、数值以及评估结果（良好/需要改进/较差）。
2. **主要问题**：按影响程度排序的问题列表。
3. **优化建议**：具体可行的修复方案，包括代码示例或配置修改建议。
4. **代码库分析结果**：识别出的框架和打包工具，以及可优化的地方（如果没有代码库访问权限则可省略此部分）。
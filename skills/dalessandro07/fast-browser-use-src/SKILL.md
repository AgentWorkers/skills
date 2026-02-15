---
name: fast-browser-use
displayName: Fastest Browser Use
emoji: "⚡"
summary: Rust-powered browser automation that rips through DOMs 10x faster than Puppeteer.
homepage: https://github.com/rknoche6/fast-browser-use
primaryEnv: bash
os:
  - darwin
  - linux
requires:
  bins:
    - chrome
install:
  - kind: brew
    formula: rknoche6/tap/fast-browser-use
  - kind: cargo
    package: fast-browser-use
config:
  requiredEnv:
    - CHROME_PATH
  example: |
    # Standard headless setup
    export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    export BROWSER_HEADLESS="true"
---

# 最快速的浏览器自动化工具

**GitHub:** https://github.com/rknoche6/fast-browser-use

这是一个基于Rust的浏览器自动化引擎，它通过CDP（Chrome DevTools Protocol）直接控制Chrome浏览器。该工具在DOM提取效率、会话管理以及执行速度方面进行了优化。

![终端演示](https://placehold.co/800x400/1e1e1e/ffffff?text=Terminal+Demo+Coming+Soon)

## 代理（Agents）实用技巧

### 1. 通过模拟人类行为绕过“机器人检测”
通过模拟鼠标抖动和随机延迟来抓取受保护的网站内容。

```bash
fast-browser-use navigate --url "https://protected-site.com" \
  --human-emulation \
  --wait-for-selector "#content"
```

### 2. “深度冻结”功能
捕获整个DOM状态及计算出的样式，以便后续进行精确的页面重建。

```bash
fast-browser-use snapshot --include-styles --output state.json
```

### 3. 登录并窃取Cookie
手动登录一次，然后窃取会话信息以进行无头自动化操作。

**步骤1：以非无头模式登录**  
```bash
fast-browser-use login --url "https://github.com/login" --save-session ./auth.json
```

**步骤2：后续重用会话信息**  
```bash
fast-browser-use navigate --url "https://github.com/dashboard" --load-session ./auth.json
```

### 4. 无限滚动数据采集
从具有无限滚动功能的页面中提取最新数据——非常适合抓取最新帖子、新闻或社交动态。

```bash
# Harvest headlines from Hacker News (scrolls 3x, waits 800ms between)
fast-browser-use harvest \
  --url "https://news.ycombinator.com" \
  --selector ".titleline a" \
  --scrolls 3 \
  --delay 800 \
  --output headlines.json
```

**实际输出**（约6秒内获取59条独特数据）：
```json
[
  "Genode OS is a tool kit for building highly secure special-purpose OS",
  "Mobile carriers can get your GPS location",
  "Students using \"humanizer\" programs to beat accusations of cheating with AI",
  "Finland to end \"uncontrolled human experiment\" with ban on youth social media",
  ...
]
```

适用于所有具有无限滚动功能的页面：Reddit、Twitter、LinkedIn动态、搜索结果等。

### 5. 快速截图
将任何页面截图为PNG格式：

```bash
fast-browser-use screenshot \
  --url "https://example.com" \
  --output page.png \
  --full-page  # Optional: capture entire scrollable page
```

### 6. 网站地图与页面结构分析
通过解析网站地图（sitemaps）和分析页面结构来了解网站的布局。

```bash
# Basic sitemap discovery (checks robots.txt + common sitemap URLs)
fast-browser-use sitemap --url "https://example.com"
```

```bash
# Full analysis with page structure (headings, nav, sections)
fast-browser-use sitemap \
  --url "https://example.com" \
  --analyze-structure \
  --max-pages 10 \
  --max-sitemaps 5 \
  --output site-structure.json
```

**选项：**
- `--analyze-structure`：同时提取页面结构（标题、导航栏、章节、元数据）
- `--max-pages N`：将结构分析限制在N页以内（默认值：5）
- `--max-sitemaps N`：将站点地图解析限制在N个以内（默认值：10，适用于大型网站）

**示例输出：**
```json
{
  "base_url": "https://example.com",
  "robots_txt": "User-agent: *\nSitemap: https://example.com/sitemap.xml",
  "sitemaps": ["https://example.com/sitemap.xml"],
  "pages": [
    "https://example.com/about",
    "https://example.com/products",
    "https://example.com/contact"
  ],
  "page_structures": [
    {
      "url": "https://example.com",
      "title": "Example - Home",
      "headings": [
        {"level": 1, "text": "Welcome to Example"},
        {"level": 2, "text": "Our Services"}
      ],
      "nav_links": [
        {"text": "About", "href": "/about"},
        {"text": "Products", "href": "/products"}
      ],
      "sections": [
        {"tag": "main", "id": "content", "role": "main"},
        {"tag": "footer", "id": "footer", "role": null}
      ],
      "main_content": {"tag": "main", "id": "content", "word_count": 450},
      "meta": {
        "description": "Example company homepage",
        "canonical": "https://example.com/"
      }
    }
  ]
}
```

使用这些功能可以在抓取数据前了解网站架构，绘制导航流程图，或审计网站的SEO结构。

## 性能对比

| 功能        | Fast Browser Use (Rust) | Puppeteer (Node) | Selenium (Java) |
|------------|-----------------|-----------------|-------------------|
| **启动时间**    | **< 50毫秒**         | **约800毫秒**         | **约2500毫秒**         |
| **内存占用**    | **15 MB**           | **100 MB以上**        | **200 MB以上**        |
| **DOM提取**    | **零拷贝**           | **JSON序列化**       | **通过中间层处理**       |
| ----------------|-----------------|-----------------|------------------- |

## 功能与工具

### 网页抓取与数据提取
- **vision_map**：生成包含所有交互元素编号边界框的截图。
- **snapshot**：捕获原始HTML快照（优化后适合AI处理）。
- **screenshot**：捕获页面的视觉图像。
- **extract**：从DOM中提取结构化数据。
- **markdown**：将当前页面内容转换为Markdown格式。
- **sitemap**：通过robots.txt、站点地图及页面语义分析来解析网站结构。

### 导航与页面生命周期管理
- **navigate**：访问指定URL。
- **go_back** / **go_forward**：浏览浏览器历史记录。
- **wait**：暂停执行或等待特定条件。
- **new_tab**：打开新标签页。
- **switch_tab**：切换到指定标签页。
- **close_tab**：关闭当前标签页或指定标签页。
- **tab_list**：列出所有打开的标签页。
- **close**：终止浏览器会话。

### 交互操作
- **click**：通过CSS选择器或DOM索引点击元素。
- **input**：在输入框中输入文本。
- **press_key**：发送特定的键盘事件。
- **hover**：将鼠标悬停在元素上。
- **scroll**：滚动页面视图。
- **select**：从下拉菜单中选择选项。

### 状态管理与调试
- **cookies**：管理会话Cookie（获取/设置）。
- **local_storage**：管理本地存储数据。
- **debug**：访问控制台日志和调试信息。

## 使用场景
该工具专为需要维护状态（如保持登录状态）、处理动态JavaScript内容或同时处理多个页面的复杂网页交互而设计。与基于fetch的标准工具相比，它提供了更高的性能和更强的控制能力。
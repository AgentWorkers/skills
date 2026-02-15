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

# Fastest Browser Use

这是一个基于 Rust 的浏览器自动化引擎，它通过 CDP 直接控制 Chrome 浏览器，并在性能、DOM 提取效率以及会话管理方面进行了优化。该工具特别适合处理需要保持状态的复杂网页交互（例如登录状态）、处理动态 JavaScript 内容，或同时管理多个页面的场景。

![终端演示](https://placehold.co/800x400/1e1e1e/ffffff?text=终端演示即将推出)

## 🧪 代理（Agents）的使用技巧

### 1. 通过模拟人类行为来绕过“机器人检测”
通过模拟鼠标抖动和随机延迟来抓取受保护的网站内容。

```bash
fast-browser-use navigate --url "https://protected-site.com" \
  --human-emulation \
  --wait-for-selector "#content"
```

### 2. “深度冻结”快照功能
捕获整个 DOM 状态及计算出的样式，以便后续进行精确的页面重建。

```bash
fast-browser-use snapshot --include-styles --output state.json
```

### 3. 登录并窃取会话信息
手动登录一次，然后窃取会话信息以进行无头自动化操作。

**步骤 1：以非无头模式登录**  
```bash
fast-browser-use login --url "https://github.com/login" --save-session ./auth.json
```

**步骤 2：后续重用会话信息**  
```bash
fast-browser-use navigate --url "https://github.com/dashboard" --load-session ./auth.json
```

### 4. 无限滚动数据采集器
从具有无限滚动功能的页面中提取最新数据——非常适合抓取最新的帖子、新闻或社交动态。

```bash
# Harvest headlines from Hacker News (scrolls 3x, waits 800ms between)
fast-browser-use harvest \
  --url "https://news.ycombinator.com" \
  --selector ".titleline a" \
  --scrolls 3 \
  --delay 800 \
  --output headlines.json
```

**实际输出**（约 6 秒内获取 59 条独特数据）：
```json
[
  "Genode OS is a tool kit for building highly secure special-purpose OS",
  "Mobile carriers can get your GPS location",
  "Students using \"humanizer\" programs to beat accusations of cheating with AI",
  "Finland to end \"uncontrolled human experiment\" with ban on youth social media",
  ...
]
```

适用于所有具有无限滚动功能的页面：Reddit、Twitter、LinkedIn 的动态信息流、搜索结果等。

### 5. 快速截图
将页面内容以 PNG 格式保存为截图：

```bash
fast-browser-use screenshot \
  --url "https://example.com" \
  --output page.png \
  --full-page  # Optional: capture entire scrollable page
```

### 6. 网站地图与页面结构分析器
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

**可选参数：**
- `--analyze-structure`：同时提取页面结构（标题、导航栏、章节、元数据）
- `--max-pages N`：限制结构分析的页面数量（默认值：5）
- `--max-sitemaps N`：限制解析的网站地图数量（默认值：10，适用于大型网站）

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

使用这些功能可以在抓取数据前了解网站架构，绘制导航流程图，或审计网站的 SEO 结构。

## ⚡ 性能对比

| 功能        | Fast Browser Use (Rust) | Puppeteer (Node) | Selenium (Java) |
|------------|------------------|------------------|------------------|
| **启动时间**    | **< 50 毫秒**           | **约 800 毫秒**           | **约 2500 毫秒**           |
| **内存占用**    | **15 MB**             | **100 MB+**            | **200 MB+**            |
| **DOM 提取**    | **零拷贝**             | **JSON 序列化**           | **通过中间层处理**           |

## 功能与工具

### 网页抓取与数据提取
- **vision_map**：生成包含所有交互元素编号边界框的截图。
- **snapshot**：捕获原始 HTML 页面快照（优化后的 YAML/Markdown 格式，便于 AI 处理）。
- **screenshot**：捕获页面的视觉图像。
- **extract**：从 DOM 中提取结构化数据。
- **markdown**：将当前页面内容转换为 Markdown 格式。
- **sitemap**：通过 robots.txt、网站地图和页面语义分析来解析网站结构。

### 浏览器操作与生命周期管理
- **navigate**：访问特定 URL。
- **go_back** / **go_forward**：浏览浏览器历史记录。
- **wait**：暂停执行或等待特定条件满足。
- **new_tab**：打开新的浏览器标签页。
- **switch_tab**：切换到指定标签页。
- **close_tab**：关闭当前标签页或指定标签页。
- **tab_list**：列出所有打开的标签页。
- **close**：终止浏览器会话。

### 交互操作
- **click**：通过 CSS 选择器或 DOM 索引点击元素。
- **input**：在输入框中输入文本。
- **press_key**：发送特定的键盘事件。
- **hover**：将鼠标悬停在元素上。
- **scroll**：滚动页面。
- **select**：从下拉菜单中选择选项。

### 状态管理与调试
- **cookies**：管理会话cookie（获取/设置）。
- **local_storage**：管理本地存储数据。
- **debug**：查看控制台日志和调试信息。

## 使用场景
该工具专为需要处理复杂网页交互的场景设计，例如保持登录状态、处理动态 JavaScript 内容或同时管理多个页面。与基于 fetch 的传统工具相比，它提供了更高的性能和更强的控制能力。
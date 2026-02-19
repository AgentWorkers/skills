---
name: traktor
description: >
  从网站中提取所有资产和内容，包括图片、SVG文件、字体、视频以及页面结构。使用多个并行代理进行抓取，确保抓取的全面性。  
  触发命令包括：`extract assets`、`scrape website`、`download site assets`、`get all images from` 或 `/traktor url`。支持多个URL。
compatibility: |
  Requires Claude Code with claude-in-chrome MCP server (browser extension).
  Will not work on Claude.ai or API without browser automation capability.
metadata:
  version: 2.0.0
---
# Traktor - 网站资源提取工具 v2.0

在提取网站资源时，请严格按照以下步骤操作。

## 触发命令

`/traktor <url1> [url2] [url3]...`

---

## 第1步：从命令参数中解析URL

从用户提供的命令中提取所有URL，并将它们存储在一个列表中。

```text
URLS = [all URLs provided after /traktor]
SITE_COUNT = number of URLs
PROJECT_DIR = current working directory
```

---

## 第2步：创建文件夹结构

### 如果网站数量（SITE_COUNT）为1

**执行以下Bash命令：**
```bash
mkdir -p assets/{logos,icons,images,videos,fonts,backgrounds} full-site/{pages,assets,styles}
```

### 如果网站数量（SITE_COUNT）大于1

**对于每个URL，提取网站名称（例如：“stripe.com” -> “stripe-com”），然后执行以下操作：**
```bash
# Replace {site-name} with actual site name for each URL
mkdir -p assets/{site-name}/{logos,icons,images,videos,fonts,backgrounds}
mkdir -p full-sites/{site-name}/{pages,assets,styles}
```

**以3个网站为例：**
```bash
mkdir -p assets/{stripe-com,vercel-com,linear-app}/{logos,icons,images,videos,fonts,backgrounds}
mkdir -p full-sites/{stripe-com,vercel-com,linear-app}/{pages,assets,styles}
```

---

## 第3步：启动提取代理

**对于每个URL，使用以下参数启动提取代理：**
```text
Tool: Task
Parameters:
  - subagent_type: "general-purpose"
  - run_in_background: true
  - description: "Extract {site-name} assets"
  - prompt: [USE THE AGENT PROMPT BELOW - replace variables]
```

### 代理提示（请严格按照以下格式复制，替换占位符{variables}）

> **注意：** 该代理提示使用了`mcp__claude-in-chrome__*`工具，这些工具需要`claude-in-chrome`浏览器扩展程序和MCP服务器。在没有安装该浏览器扩展程序的环境中，这些工具将无法使用。

```text
Extract ALL assets from {URL} with paranoid-level thoroughness. Miss nothing.

OUTPUT DIRECTORIES
- Assets: {PROJECT_DIR}/assets/{site-name}/ (or {PROJECT_DIR}/assets/ if single site)
- Full site: {PROJECT_DIR}/full-sites/{site-name}/ (or {PROJECT_DIR}/full-site/ if single site)

PHASE 1: Browser setup and navigation

1. Call mcp__claude-in-chrome__tabs_context_mcp to get browser context
2. Call mcp__claude-in-chrome__tabs_create_mcp to create new tab
3. Call mcp__claude-in-chrome__navigate with url="{URL}" and the new tabId
4. Call mcp__claude-in-chrome__computer with action="screenshot" to verify page loaded
5. Scroll full page to trigger lazy loading:
   - mcp__claude-in-chrome__computer action="scroll" scroll_direction="down" scroll_amount=10
   - Repeat 3-5 times with 1 second waits

PHASE 2: Asset discovery (JavaScript extraction)

Call mcp__claude-in-chrome__javascript_tool with this code:
```

```javascript
(() => {
  const assets = {
    images: [...document.querySelectorAll('img')].map(img => ({
      src: img.src,
      srcset: img.srcset,
      dataSrc: img.dataset.src,
      alt: img.alt
    })).filter(i => i.src || i.srcset || i.dataSrc),

    videos: [...document.querySelectorAll('video, video source')].map(v => ({
      src: v.src || v.currentSrc,
      poster: v.poster,
      type: v.type
    })).filter(v => v.src),

    svgsInline: [...document.querySelectorAll('svg')].map((svg, i) => ({
      id: svg.id || 'svg-' + i,
      class: svg.className?.baseVal || '',
      html: svg.outerHTML
    })),

    backgrounds: [...document.querySelectorAll('*')].map(el => {
      const bg = getComputedStyle(el).backgroundImage;
      if (bg && bg !== 'none' && bg.includes('url(')) {
        return bg.match(/url\(['"]?([^'"]+)['"]?\)/)?.[1];
      }
      return null;
    }).filter(Boolean),

    favicons: [...document.querySelectorAll('link[rel*="icon"]')].map(l => ({
      href: l.href,
      rel: l.rel,
      sizes: l.sizes?.value
    })),

    ogImages: (() => {
      const og = document.querySelector('meta[property="og:image"]');
      const twitter = document.querySelector('meta[name="twitter:image"]');
      return [og?.content, twitter?.content].filter(Boolean);
    })(),

    fonts: (() => {
      const fonts = [];
      for (const sheet of document.styleSheets) {
        try {
          for (const rule of sheet.cssRules) {
            if (rule.type === 5) { // FONT_FACE_RULE
              const src = rule.style.getPropertyValue('src');
              const urls = src.match(/url\(['"]?([^'"]+)['"]?\)/g);
              if (urls) fonts.push(...urls.map(u => u.match(/url\(['"]?([^'"]+)['"]?\)/)?.[1]));
            }
          }
        } catch (e) {}
      }
      return [...new Set(fonts)];
    })()
  };

  return JSON.stringify(assets, null, 2);
})()
```

```text
Store the result as DISCOVERED_ASSETS.

PHASE 3: Content extraction

Call mcp__claude-in-chrome__javascript_tool with this code:
```

```javascript
(() => {
  const content = {
    url: window.location.href,
    title: document.title,
    extractedAt: new Date().toISOString().split('T')[0],
    meta: {
      description: document.querySelector('meta[name="description"]')?.content,
      ogTitle: document.querySelector('meta[property="og:title"]')?.content,
      ogDescription: document.querySelector('meta[property="og:description"]')?.content,
      ogImage: document.querySelector('meta[property="og:image"]')?.content,
      favicon: document.querySelector('link[rel*="icon"]')?.href
    },
    navigation: {
      header: [...document.querySelectorAll('header a, nav a')].slice(0, 20).map(a => ({
        text: a.textContent?.trim(),
        href: a.href
      })),
      footer: [...document.querySelectorAll('footer a')].slice(0, 20).map(a => ({
        text: a.textContent?.trim(),
        href: a.href
      }))
    },
    headings: [...document.querySelectorAll('h1, h2, h3')].slice(0, 30).map(h => ({
      level: h.tagName,
      text: h.textContent?.trim()
    })),
    buttons: [...document.querySelectorAll('button, a.btn, [class*="button"]')].slice(0, 20).map(b => ({
      text: b.textContent?.trim(),
      href: b.href || null
    }))
  };

  return JSON.stringify(content, null, 2);
})()
```

```text
Store the result as PAGE_CONTENT.

PHASE 4: Download assets

For each asset URL discovered, download using curl with error handling.
If curl fails (non-zero exit), log the URL and continue to the next asset.

# Logos (favicon, og:image, header logos)
curl -sfLo "{output_dir}/logos/{site-name}-favicon.ico" "{favicon_url}" || echo "FAIL: {favicon_url}"
curl -sfLo "{output_dir}/logos/{site-name}-og-image.png" "{og_image_url}" || echo "FAIL: {og_image_url}"

# Images
curl -sfLo "{output_dir}/images/{site-name}-{descriptive-name}.{ext}" "{image_url}" || echo "FAIL: {image_url}"

# SVGs - Write inline SVGs to files using Write tool

# Videos
curl -sfLo "{output_dir}/videos/{site-name}-{name}.mp4" "{video_url}" || echo "FAIL: {video_url}"

# Fonts
curl -sfLo "{output_dir}/fonts/{font-name}.woff2" "{font_url}" || echo "FAIL: {font_url}"

NAMING CONVENTION: {site-prefix}-{descriptive-name}.{ext}
- Use alt text or context for descriptive names
- Example: stripe-hero-illustration.svg, vercel-logo-white.svg

PHASE 5: Save JSON files

1. Save page content:
   Use Write tool to save PAGE_CONTENT to:
   {full-site-dir}/pages/homepage.json

2. Save asset URLs catalog:
   Use Write tool to save DISCOVERED_ASSETS to:
   {full-site-dir}/asset-urls.json

PHASE 6: Report results

When complete, report:
- Total assets downloaded (count by type)
- Total size (estimate from curl outputs)
- Any failed downloads (list URLs)
- Output paths

ERROR HANDLING
- If site unreachable: Report error, skip
- If asset download fails: Retry once with 2s delay, then log URL and continue
- If browser tab crashes: Call tabs_create_mcp again, continue
- If rate limited: Add 2 second delays between requests

CONSTRAINTS
- Skip files > 50MB (log URL for manual download)
- Skip duplicate URLs
- Maximum 100 assets per category
- 5 minute timeout for entire extraction
```

---

## 第4步：监控代理进程

在所有代理启动后：

1. **向用户报告进度：**
```text
Traktor v2.0 - Extraction started

Folder structure created
Spawned {N} extraction agents:
   - Agent 1: {site1} [running in background]
   - Agent 2: {site2} [running in background]
   ...

Agents working in background. You'll be notified as they complete.
```

2. **等待代理完成，并收集它们的结果。**

---

## 第5步：生成最终资源清单

所有代理完成后，创建资源清单文件：

**使用`Write`工具生成`asset-manifest.json`文件：**
```json
{
  "generated_at": "{current_datetime}",
  "tool": "traktor v2.0",
  "project_dir": "{PROJECT_DIR}",
  "sites_extracted": ["{site1}", "{site2}"],
  "total_assets": "{total_count}",
  "by_type": {
    "logos": "{count}",
    "icons": "{count}",
    "images": "{count}",
    "videos": "{count}",
    "fonts": "{count}",
    "svgs": "{count}"
  },
  "naming_convention": "{site-prefix}-{descriptive-name}.{ext}",
  "output_structure": {
    "assets": "./assets/",
    "full_sites": "./full-sites/"
  }
}
```

---

## 第6步：生成最终报告

**向用户展示结果：**
```text
Traktor extraction complete!

Summary:
   Sites: {N}
   Total assets: {count} ({size_mb} MB)

   By type:
   - Logos: {n}
   - Images: {n}
   - Videos: {n}
   - SVGs: {n}
   - Fonts: {n}

Output:
   - Assets: ./assets/
   - Full sites: ./full-sites/
   - Manifest: ./asset-manifest.json

Failed downloads: {list or "None"}
```

---

## 快速参考

| 步骤 | 操作 | 使用的工具 |
|------|--------|------|
| 1 | 解析URL | 内部脚本（Internal） |
| 2 | 创建文件夹 | Bash命令 |
| 3 | 启动代理 | Task（后台进程） |
| 4 | 监控代理进度 | 等待代理完成的通知 |
| 5 | 生成资源清单 | Write工具 |
| 6 | 提供报告 | 向用户展示结果 |

---

## 示例执行

**用户输入：`/traktor https://0g.ai`**

**Claude的执行过程：**
1. 解析命令：`URLS = ["https://0g.ai"]`，`SITE_COUNT = 1`
2. Bash命令：`mkdir -p assets/{logos,icons,images,videos,fonts,backgrounds} full-site/{pages,assets,styles}``
3. 使用`Task`工具启动1个代理
4. 向用户报告：“Traktor已启动，1个代理正在运行中...”
5. 等待代理完成
6. 生成`asset-manifest.json`文件
7. 向用户提供最终结果报告

**用户输入：`/traktor https://stripe.com https://vercel.com https://linear.app`**

**Claude的执行过程：**
1. 解析命令：`URLS = ["https://stripe.com", "https://vercel.com", "https://linear.app"]`
2. 使用Bash命令在`assets/`和`full-sites/`目录下创建相应的文件夹
3. 启动3个并行运行的代理
4. 向用户报告：“Traktor已启动，3个代理正在运行中...”
5. 在代理完成时收集所有结果
6. 生成合并后的资源清单文件
7. 向用户提供合并后的结果报告
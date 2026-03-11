---
name: web-fetcher
description: "智能网页内容采集器——能够从微信、飞书、哔哩哔哩、知乎、抖音、YouTube等平台获取文章和视频。支持的命令包括：  
“抓取文章”（Grab Articles）、“下载网页”（Download Web Pages）、“保存文章”（Save Articles）、“获取URL”（Fetch URLs）、“下载视频”（Download Videos）、“抓取飞书文档”（Grab Feishu Documents）、“抓取微信文章”（Grab WeChat Articles）、“将此链接内容保存下来”（Save Link Content）、“下载B站视频”（Download Bilibili Videos）、“下载视频”（Download Videos）、“抓取文章”（Scrape Articles）。"
version: 0.1.1
license: Complete terms in LICENSE
---
# Web Fetcher

这是一个专为Claude Code设计的智能网页内容获取工具，能够自动识别平台并采用最佳策略来获取文章或下载视频。

## 快速入门

```bash
# Fetch an article
python3 {SKILL_DIR}/fetcher.py "URL" -o ~/docs/

# Download a video
python3 {SKILL_DIR}/fetcher.py "https://b23.tv/xxx" -o ~/videos/

# Batch fetch from file
python3 {SKILL_DIR}/fetcher.py --urls-file urls.txt -o ~/docs/
```

## 安装依赖项

仅安装实际需要的依赖项——这些依赖项会在运行时进行验证：

| 依赖项 | 用途 | 安装方式 |
|---------|---------|---------|
| scrapling | 文章获取（HTTP + 浏览器） | `pip install scrapling` |
| yt-dlp | 视频下载 | `pip install yt-dlp` |
| camoufox | 防检测浏览器（适用于小红书、微博等网站） | `pip install camoufox && python3 -m camoufox fetch` |
| html2text | HTML到Markdown的转换 | `pip install html2text` |

## 智能路由机制

该工具会根据URL自动识别平台，并选择相应的获取方法：

| 平台 | 获取方式 | 备注 |
|---------|--------|-------|
| mp.weixin.qq.com | 使用scrapping技术 | 提取`data-src`属性中的图片地址，并处理SVG占位符 |
| *.feishu.cn | 使用虚拟滚动技术 | 通过滚动获取所有内容块，并通过浏览器下载图片（需要使用cookie） |
| zhuanlan.zhihu.com | 使用scrapping技术 | 使用`.Post-RichText`选择器来获取内容 |
| www.zhihu.com | 使用scrapping技术 | 使用`.RichContent`选择器来获取内容 |
| www.toutiao.com | 使用scrapping技术 | 处理`toutiaoimg.com`格式的Base64图片占位符 |
| www.xiaohongshu.com | 使用camoufox浏览器 | 需要使用隐身模式来规避反爬虫机制 |
| www.weibo.com | 使用camoufox浏览器 | 需要使用隐身模式来规避反爬虫机制 |
| bilibili.com / b23.tv | 使用yt-dlp工具 | 支持视频下载及质量选择 |
| youtube.com / youtu.be | 使用yt-dlp工具 | 视频下载 |
| douyin.com | 使用yt-dlp工具 | 视频下载 |
| 未知URL | 使用通用抓取方法，并提供备用方案 |

## 命令行参考

```
python3 {SKILL_DIR}/fetcher.py [URL] [OPTIONS]

Arguments:
  url                    URL to fetch

Options:
  -o, --output DIR       Output directory (default: current)
  -q, --quality N        Video quality, e.g. 1080, 720 (default: 1080)
  --method METHOD        Force method: scrapling, camoufox, ytdlp, feishu
  --selector CSS         Force CSS selector for content extraction
  --urls-file FILE       File with URLs (one per line, # for comments)
  --audio-only           Extract audio only (video downloads)
  --no-images            Skip image download (articles)
  --cookies-browser NAME Browser for cookies (e.g., chrome, firefox)
```

## 各平台使用说明

### 微信（mp.weixin.qq.com）
- 图片通过`data-src`属性和`mmbiz.qpic.cn` URL进行获取 |
- 可见的`<img>`标签中包含SVG占位符（采用懒加载方式）
- 下载图片时需要设置`Referer: https://mp.weixin.qq.com/`头部信息 |
- 通常可以使用scrapping技术进行获取，无需使用浏览器 |

### Feishu (*.feishu.cn）
- 采用虚拟滚动技术获取内容；内容块按需渲染 |
- 该工具会遍历整个页面，收集带有`[data-block-id]`标签的内容块 |
- 下载图片需要使用cookie，并通过浏览器的下载API进行 |
- 可能会遇到“无法打印”的错误，这些错误会被自动清除 |

### Bilibili
- 短链接（如b23.tv）会自动解析 |
- 对于会员专享内容，需使用`--cookies-browser chrome`参数 |
- 默认下载质量为1080p，可通过`-q`参数进行调整 |

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 无法找到scrapping工具 | 安装`pip install scrapling` |
| 无法找到yt-dlp工具 | 安装`pip install yt-dlp` |
- 文章内容太短 | 对于包含大量JavaScript的页面，尝试使用`--method camoufox` |
- Feishu网站返回登录页面 | 可能需要登录才能获取内容 |
- Bilibili网站返回403错误 | 使用`--cookies-browser chrome`参数 |
- 下载图片失败 | 检查网络连接；微信图片的下载需要设置`Referer`头部信息 |

## 手动使用方法

当命令行工具无法满足需求时，可以直接使用相应的模块：

```python
from lib.router import route, check_dependency
from lib.article import fetch_article
from lib.video import fetch_video
from lib.feishu import fetch_feishu

# Route a URL
r = route("https://mp.weixin.qq.com/s/xxx")
# {'type': 'article', 'method': 'scrapling', 'selector': '#js_content', 'post': 'wx_images'}

# Fetch article
fetch_article(url, output_dir="/tmp/out", route_config=r)

# Download video
fetch_video(url, output_dir="/tmp/out", quality="720")

# Fetch Feishu doc
fetch_feishu(url, output_dir="/tmp/out")
```
---
name: sitemap-generator
description: 通过爬取网站来生成XML站点地图。当用户需要为SEO创建站点地图.xml文件、审核网站结构、发现域名下的所有页面，或者生成用于提交给Google Search Console或其他搜索引擎的站点地图时，可以使用此功能。该工具支持BFS（广度优先搜索）爬取方式，并允许用户配置爬取深度、页面数量限制以及爬取过程中的延迟时间。
---
# 网站地图生成器

该工具可爬取任何网站，并生成符合标准的XML网站地图，以便提交给搜索引擎。

## 快速入门

```bash
python3 scripts/sitemap_gen.py https://example.com
```

运行该工具后，`sitemap.xml`文件将生成在当前目录中。

## 命令

```bash
# Basic — crawl and write sitemap.xml
python3 scripts/sitemap_gen.py https://example.com

# Custom output path
python3 scripts/sitemap_gen.py https://example.com -o /tmp/sitemap.xml

# Limit crawl scope
python3 scripts/sitemap_gen.py https://example.com --max-pages 500 --max-depth 3

# Polite crawling with delay
python3 scripts/sitemap_gen.py https://example.com --delay 1.0

# Set SEO hints
python3 scripts/sitemap_gen.py https://example.com --changefreq daily --priority 0.8

# Verbose progress
python3 scripts/sitemap_gen.py https://example.com -v

# Pipe to stdout
python3 scripts/sitemap_gen.py https://example.com -o -
```

## 选项

| 选项          | 默认值    | 说明                                      |
|----------------|---------|-----------------------------------------|
| `--output, -o`    | `sitemap.xml` | 输出文件路径（使用 `-` 表示输出到标准输出）             |
| `--max-pages`    | `200`    | 最大爬取页面数                               |
| `--max-depth`    | `5`     | 从起始URL开始的链接最大深度                        |
| `--delay`     | `0.2`     | 请求之间的延迟时间（秒）                          |
| `--timeout`     | `10`     | 请求超时时间（秒）                             |
| `--changefreq`    | `weekly`   | 网站地图更新频率提示                         |
| `--priority`    | `0.5`    | 网站地图优先级提示（0.0–1.0）                        |
| `--verbose, -v`    | `off`     | 在标准错误输出中显示爬取进度                         |

## 依赖项

```bash
pip install requests beautifulsoup4
```

## 注意事项

- 仅爬取同一域内的页面（不爬取外部链接）；
- 跳过二进制文件（图片、CSS、JavaScript文件、PDF文件、字体文件）；
- 遵循 `sitemaps.org 0.9` 协议进行输出；

该工具会按照预设的选项和配置来爬取网站并生成网站地图文件。
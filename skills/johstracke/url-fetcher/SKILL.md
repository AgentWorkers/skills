---
name: url-fetcher
description: 无需 API 密钥或外部依赖即可获取简单的网络内容。仅使用 Python 标准库（urllib）。功能包括：从 URL 获取 HTML/文本、基本的 HTML 到 Markdown 的转换、路径验证后的文件写入（支持系统路径）、URL 验证（排除本地主机/内部地址）。安全性方面：文件写入时使用 `is_safe_path()` 函数来防止恶意操作。非常适合内容聚合、研究资料收集以及无需 API 成本或依赖的网络爬取任务。
---

# URL Fetcher

无需API密钥或外部依赖即可获取网页内容，仅使用Python标准库。

## 快速入门

```bash
url_fetcher.py fetch <url>
url_fetcher.py fetch --markdown <url> [output_file]
```

**示例：**
```bash
# Fetch and preview
url_fetcher.py fetch https://example.com

# Fetch and save HTML
url_fetcher.py fetch https://example.com ~/workspace/page.html

# Fetch and convert to basic markdown
url_fetcher.py fetch --markdown https://example.com ~/workspace/page.md
```

## 特点

- **无依赖** - 仅使用Python标准库（urllib）
- **无需API密钥** - 完全免费使用
- **URL验证** - 阻止访问本地主机/内部网络
- **基本Markdown转换** - 从HTML中提取内容
- **路径验证** - 仅将文件保存到指定路径（如workspace、home、/tmp）
- **错误处理** - 处理超时和网络错误

## 适用场景

- **内容聚合** - 收集页面以供处理
- **研究资料收集** - 将文章/页面保存到本地
- **简单爬取** - 从网页中提取文本
- **Markdown转换** - 将HTML转换为文本或Markdown格式
- **无API替代方案** - 当无法使用付费API时

## 限制

- **Markdown转换简单** - 基于正则表达式的简单转换（非完整解析器）
- **不支持JavaScript** - 仅获取静态HTML
- **无内置速率限制** - 如需可自行添加
- **部分网站可能阻止默认User-Agent**

## 安全特性

### URL验证
- ✅ 支持http/https协议
- ❌ 阻止file://、data://、javascript:协议
- ❌ 阻止访问本地主机（localhost）和127.0.0.1、::1（内部网络）

### 文件路径验证
- ✅ 允许保存到workspace、home目录和/tmp
- ❌ 阻止访问系统路径（如/etc、/usr、/var等）
- ❌ 阻止访问敏感文件（如 ~/.ssh、 ~/.bashrc等）

### 错误处理
- 超时处理（10秒后停止请求）
- HTTP错误处理
- 网络错误处理
- 字符编码处理

## 使用方式

### 收集研究资料
```bash
# Fetch multiple articles
url_fetcher.py fetch https://example.com/article1.md ~/workspace/research/article1.md
url_fetcher.py fetch https://example.com/article2.md ~/workspace/research/article2.md

# Convert to markdown for reading
url_fetcher.py fetch --markdown https://example.com/article.md ~/workspace/research/article.md
```

### 内容聚合
```bash
# Fetch pages for processing
url_fetcher.py fetch https://news.example.com ~/workspace/content/latest.html

# Extract text
url_fetcher.py fetch --markdown https://blog.example.com ~/workspace/content/post.md
```

### 快速预览
```bash
# Just preview content (no file save)
url_fetcher.py fetch https://example.com
```

## 高级用法

### 批量获取
```bash
#!/bin/bash
# batch_fetch.sh

URLS=(
    "https://example.com/page1"
    "https://example.com/page2"
    "https://example.com/page3"
)

OUTPUT_DIR="$HOME/workspace/fetched"
mkdir -p "$OUTPUT_DIR"

for url in "${URLS[@]}"; do
    filename=$(echo $url | sed 's|/||g')
    url_fetcher.py fetch --markdown "$url" "$OUTPUT_DIR/$filename.md"
    sleep 1  # Be nice to servers
done
```

### 与其他工具集成

**与研究辅助工具集成：**
```bash
# Fetch article
url_fetcher.py fetch --markdown https://example.com/article.md ~/workspace/article.md

# Extract key points
# Then use research-assistant to organize findings
```

**与任务执行工具集成：**
```bash
# Add task to fetch content
task_runner.py add "Fetch article on topic X" "research"

# Fetch when ready
url_fetcher.py fetch https://example.com/topic-x.md ~/workspace/research/topic-x.md
```

## 故障排除

### 连接超时
```
Error: Request timeout after 10s
```
**解决方法：** 服务器响应缓慢或无法访问。请稍后再试，或检查URL是否正确。

### HTTP 403/429错误
```
Error: HTTP 403: Forbidden
```
**解决方法：** 网站可能禁止自动化请求。可以尝试：
- 在请求之间添加延迟
- 更改User-Agent
- 遵守网站的robots.txt文件
- 如有必要，考虑使用API

### 编码问题
```
Error with special characters
```
**解决方法：** 该工具使用UTF-8编码，并忽略部分无法解析的字符。

### Markdown质量
```
Note: Basic markdown extraction
```
**解决方法：** 该工具使用简单的正则表达式进行HTML到Markdown的转换。如需更高质量的结果：
- 使用专门的Markdown解析器
- 或对输出进行后处理
- 或使用提供更精确解析功能的付费API

## 最佳实践

1. **尊重网站规则** - 在请求之间添加延迟，避免对服务器造成压力
- 遵守网站的爬虫政策（查看robots.txt文件）
- 设置请求速率限制，避免频繁请求
- 仅从可信来源获取数据
- 安全保存文件（确保路径正确）
- 使用预览功能后再保存文件

## 集成示例

### Python集成
```python
from pathlib import Path
import subprocess

def fetch_and_process(url):
    """Fetch URL and process"""
    output = Path.home() / "workspace" / "fetched" / "page.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    
    # Fetch
    subprocess.run([
        "python3",
        "/path/to/url_fetcher.py",
        "fetch",
        "--markdown",
        url,
        str(output)
    ])
    
    # Process content
    content = output.read_text()
    return content
```

### Bash集成
```bash
# Function for fetching
fetch_content() {
    local url="$1"
    local output="$2"
    python3 ~/workspace/skills/url-fetcher/scripts/url_fetcher.py \
        fetch --markdown "$url" "$output"
}

# Usage
fetch_content "https://example.com" ~/workspace/example.md
```

## 替代方案

### 如需更多功能

- **如需功能更丰富的爬取工具：**
  - 使用`requests` + `beautifulsoup4`（需安装pip）
  - 或使用`scrapy`框架（需安装pip）
  - 或使用付费API（如Firecrawl、Apify）
- **如需更好的Markdown转换：**
  - 使用`markdownify`库（需安装pip）
  - 或使用基于AI的解析服务（如OpenAI、Anthropic）
- **对于复杂的工作流程：**
  - 使用浏览器自动化工具（如OpenClaw）或无头浏览器（如Puppeteer、Playwright）
  - 或使用专门的爬取API（如Zyte、ScrapperAPI）

## 低成本优势

- ✅ 仅需Python 3环境（OpenClaw已包含Python 3）
- ✅ 无需API密钥
- ✅ 无需额外安装任何外部包或服务
- ✅ 无需支付费用
- ✅ 无需额外设置速率限制

非常适合预算有限的自动化工具开发。

## 贡献建议

如果您对该工具进行了改进，请：
1. 使用安全检查工具进行测试
2. 文档新添加的功能
3. 将改进内容发布到ClawHub，并注明贡献者

## 许可证

您可以在自己的OpenClaw项目中自由使用该工具。
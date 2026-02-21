---
name: tor-browser
description: 无头浏览器自动化工具，支持使用 Tor SOCKS5 代理来访问 `.onion` 网站并实现匿名浏览。适用于浏览暗网资源、抓取 Tor 隐藏服务、在暗网论坛上进行安全研究，或需要在网络中使用匿名身份的场景。该工具支持通过 Tor 网络进行导航、与网页元素交互、截图以及数据提取等操作。
metadata:
  openclaw:
    emoji: onion
    category: browser-automation
    version: 1.1.0
    author: OpenClaw
    requirements:
      - python >= 3.8
      - playwright
      - tor service running on socks5://127.0.0.1:9050
    allowed-tools: ["Bash"]
---
# Tor浏览器自动化

支持使用Tor SOCKS5代理的无头浏览器自动化，用于访问.onion网站和进行匿名网络浏览。

## 先决条件

- Tor服务正在运行，并在9050端口上提供SOCKS5代理
- Python 3.8或更高版本
- 以及支持Chromium浏览器的Playwright库

快速设置：
```bash
# Install Tor
sudo apt install tor && sudo systemctl start tor

# Install Python dependencies
pip install playwright
playwright install chromium
```

## 快速入门

```bash
# Check Tor connection
tor-browser check-tor

# Navigate to a .onion site
tor-browser open http://3g2upl4pq6kufc4m.onion

# Get page snapshot
tor-browser snapshot -i

# Click an element
tor-browser click @e1

# Take screenshot
tor-browser screenshot -o output.png --full
```

## 命令

### 导航

```bash
# Open URL via Tor
tor-browser open <url> [--proxy socks5://host:port]

# Check Tor connection status
tor-browser check-tor
```

### 页面分析

```bash
# Get full page snapshot
tor-browser snapshot

# Get interactive elements only (forms, buttons, links)
tor-browser snapshot -i

# Extract all links
tor-browser links

# Get page text
tor-browser gettext
tor-browser gettext --ref @e5
```

### 交互操作

```bash
# Click element by ref
tor-browser click @e1

# Fill input field
tor-browser fill @e2 "text to enter"

# Wait for page load
tor-browser wait 2000
```

### 截图

```bash
# Take viewport screenshot
tor-browser screenshot

# Save to file
tor-browser screenshot -o capture.png

# Full page screenshot
tor-browser screenshot --full -o page.png
```

## Python API

```python
from scripts.tor_browser import TorBrowser, Config
import asyncio

async def main():
    # Configure browser
    config = Config(
        tor_proxy="socks5://127.0.0.1:9050",
        headless=True,
        timeout=30000
    )
    
    # Initialize and start
    browser = TorBrowser(config)
    await browser.start()
    
    # Navigate
    result = await browser.navigate("http://3g2upl4pq6kufc4m.onion")
    print(f"Loaded: {result['title']}")
    
    # Get snapshot
    snapshot = await browser.get_snapshot(interactive_only=True)
    for elem in snapshot['elements']:
        print(f"{elem['ref']}: {elem['tag']} - {elem['text'][:30]}")
    
    # Interact
    await browser.fill("@e2", "search query")
    await browser.click("@e3")
    
    # Extract data
    links = await browser.extract_links()
    for link in links:
        print(f"{link['text']}: {link['href']}")
    
    # Cleanup
    await browser.close()

asyncio.run(main())
```

## 配置选项

| 选项 | 默认值 | 说明 |
|--------|---------|-------------|
| `tor_proxy` | `socks5://127.0.0.1:9050` | Tor SOCKS5代理的URL |
| `headless` | `true` | 以无图形界面模式运行 |
| `timeout` | `30000` | 页面加载超时时间（毫秒） |
| `user_agent` | Tor浏览器的用户代理字符串 | 浏览器的用户代理设置 |
| `viewport` | `1920x1080` | 浏览器的视口大小 |

## 安全与法律注意事项

**使用范围：**
- 安全研究与威胁情报分析
- 匿名抓取公共暗网资源
- 测试.onion网站的访问性
- 保护隐私的自动化操作

**重要提示：**
- 仅用于合法目的
- 遵守网站的服务条款
- 禁止用于未经授权的访问
- 遵守当地关于访问暗网的法律
- 请注意某些活动可能会被监控

## 故障排除

### Tor连接问题

```bash
# Check Tor is running
sudo systemctl status tor

# Test SOCKS5 proxy
curl --socks5-hostname 127.0.0.1:9050 https://check.torproject.org/api/ip

# View Tor logs
sudo journalctl -u tor -f
```

### 常见错误

**连接被拒绝：**
- 确保Tor服务已启动
- 检查防火墙规则
- 验证代理URL是否正确

**超时问题：**
- .onion网站可能加载速度较慢；请增加超时时间
- 尝试使用不同的Tor线路：重新启动Tor服务

**CAPTCHA拦截：**
- 使用`--headed`模式手动解决CAPTCHA问题
- 部分网站会阻止自动化操作

## Docker配置

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y tor
RUN pip install playwright && playwright install chromium

COPY . /app
WORKDIR /app

CMD ["tor-browser", "check-tor"]
```

## 参考资料

- 设置指南：[references/setup-guide.md](references/setup-guide.md)
- Playwright文档：https://playwright.dev/python/
- Tor项目官网：https://www.torproject.org/

## 许可证

本工具基于MIT许可证发布。Playwright和Tor项目的具体许可证请参考其官方文档。
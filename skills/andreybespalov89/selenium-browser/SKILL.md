---
name: selenium-browser
description: "启动一个由 Selenium 控制的 Chrome 浏览器，打开一个指定的 URL，截取屏幕截图，并报告操作进度。支持无头模式（headless mode）以及可选的代理设置（optional proxy）。"
---
## 使用方法

当收到包含以下关键词的消息时，该技能会自动执行相应操作：*Chrome*、*browser*、*Selenium*、*screenshot* 或 *open*。

```bash
selenium-browser <URL> [--headless] [--proxy=<url>]
```

### 命令流程
1. 在 Selenium 环境中启动 Chrome（或 Chromium）浏览器。
2. 导航至 `<URL>`。
3. 对加载的页面进行截图。
4. 将截图保存到 `/home/main/clawd/diffusion_pdfs/` 目录中，并将保存路径反馈给聊天系统。
5. 如果有任何操作失败，会发送错误信息。

## 脚本

### scripts/launch_browser.py

```python
#!/usr/bin/env python3
import os
import sys
import time
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# CLI parsing
import argparse
parser = argparse.ArgumentParser(description="Launch Selenium Chrome and take a screenshot.")
parser.add_argument("url", help="URL to open")
parser.add_argument("--headless", action="store_true", help="Run Chrome headless")
parser.add_argument("--proxy", help="Proxy URL (e.g., http://proxy:3128)")
args = parser.parse_args()

# Prepare Chrome options
chrome_options = Options()
if args.headless:
    chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
if args.proxy:
    chrome_options.add_argument(f"--proxy-server={args.proxy}")

# Locate binaries
chrome_bin = os.getenv("CHROME_BIN", "/usr/bin/google-chrome")
chromedriver_path = os.getenv("CHROMEDRIVER_PATH", "/usr/local/bin/chromedriver")

service = Service(executable_path=chromedriver_path)

# Start browser
try:
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"❌ Failed to start Chrome: {e}", file=sys.stderr)
    sys.exit(1)

# Navigate and wait for page load
try:
    driver.get(args.url)
    time.sleep(5)  # simple wait; can replace with WebDriverWait for better reliability
except Exception as e:
    print(f"❌ Navigation error: {e}", file=sys.stderr)
    driver.quit()
    sys.exit(1)

# Take screenshot
screenshot_path = os.path.join(os.getenv("HOME", "/tmp"), "screenshot.png")
try:
    driver.save_screenshot(screenshot_path)
except Exception as e:
    print(f"❌ Screenshot error: {e}", file=sys.stderr)
    driver.quit()
    sys.exit(1)

# Clean up
driver.quit()

# Output a JSON object that OpenClaw can parse for the reply
print({"status": "ok", "screenshot": screenshot_path})
```

### scripts/_env.sh

```bash
# Optional: set paths to Chrome/Chromedriver if not in standard locations
# export CHROME_BIN="/opt/google/chrome/google-chrome"
# export CHROMEDRIVER_PATH="/usr/local/bin/chromedriver"
```

## 参考资料
- [Selenium 文档](https://www.selenium.dev/documentation/)
- [ChromeDriver 下载页面](https://chromedriver.chromium.org/downloads)

## 报告机制
该技能会运行 Python 脚本，并将脚本的输出（stdout）以 JSON 格式发送。OpenClaw 会解析这些 JSON 数据并返回相应的消息。

```
✅ Screenshot saved: /home/main/clawd/diffusion_pdfs/screenshot.png
```

如果脚本在执行过程中出现错误，该技能会直接将错误信息转发给聊天系统。

---

## 安装说明
1. 确保 `chromedriver` 已安装在 `/usr/local/bin/chromedriver` 路径下，或者通过 `CHROMEDRIVER_PATH` 环境变量指定其路径。
2. 确保 `google-chrome`（或 `chromium`）已安装在 `/usr/bin/google-chrome` 路径下，或者通过 `CHROME_BIN` 环境变量指定其路径。
3. 在用于运行该技能的虚拟环境中安装 Python 的相关依赖库：`pip install selenium`。

```bash
pip install selenium
```

---

## 日志记录与超时设置
脚本在导航完成后会等待 5 秒；您可以根据需要使用 Selenium 的 `WebDriverWait` 功能来实现更灵活的超时控制（例如：`WebDriverWait(driver, 20).until(...)`）。

您可以根据自己的环境需求（代理设置、身份验证等）对脚本进行相应的调整。
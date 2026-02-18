---
name: OpenClaw Native Browser
description: OpenClaw代理的稳定原生浏览器（WKWebView）：该浏览器支持标签页管理、地址栏以及登录辅助功能，能够正常访问各种网站，包括Perplexity、Grok、Claude和ChatGPT等平台。
read_when:
  - Navigating web pages with a real browser
  - Interacting with authenticated web applications
  - Searching the web without API keys
  - Logging into websites (Perplexity, Grok, Claude, ChatGPT)
  - Taking screenshots of web pages
  - Managing multiple browser tabs
metadata:
  clawdbot:
    emoji: "🦞"
    requires:
      bins: ["python3", "pip"]
allowed-tools: Bash(python:*), Bash(pip:*)
---
# OpenClaw 原生浏览器

这是一个专为 OpenClaw 代理设计的原生浏览器（基于 WKWebView），支持标签页管理、地址栏以及登录辅助功能。所有网站都能正常使用，包括 Perplexity、Grok、Claude 和 ChatGPT。

**它替代了那些不稳定、基于中继的浏览器控件，提供了更加稳定、兼容 macOS 的原生浏览器体验。**

## 安装

克隆仓库并安装：
```bash
git clone https://github.com/yungookim/openclaw-browser.git ~/clawd/openclaw-browser
cd ~/clawd/openclaw-browser
pip install -e .
```

验证安装结果：
```bash
python -c "import sys; sys.path.insert(0, '/Users/$USER/clawd/openclaw-browser'); from src import OpenClawBrowserSkill, __version__; print(f'openclaw-browser v{__version__} ready')"
```

## 快速入门
```python
import sys
sys.path.insert(0, '/Users/<username>/clawd/openclaw-browser')
from src import OpenClawBrowserSkill

skill = OpenClawBrowserSkill()

# Load any website (native WKWebView — all sites work)
skill.load('https://perplexity.ai')

# Read page content
title = skill.get_title()
html = skill.get_dom('body')

# Execute JavaScript
result = skill.execute_js('document.title')

# Interact with page
skill.click('button.submit')
skill.type_text('input[name="query"]', 'Hello world')

# Tab management
tab_id = skill.browser.new_tab('https://example.com')
skill.browser.switch_tab(tab_id)
skill.browser.close_tab(tab_id)

# Close when done
skill.close()
```

## 为什么使用这个浏览器？

默认情况下，OpenClaw 网关使用 **Brave Search API** 进行网页搜索，但该 API 有以下限制：
- 需要付费的 API 密钥
- 仅支持搜索功能，无法与网站进行交互
- 无法登录网站，也无法与已认证的网页应用进行交互

**openclaw-browser** 则解决了这些问题，提供了以下功能：
- ✅ 无需 API 密钥
- ✅ 支持点击、输入、登录和数据抓取
- ✅ 支持持久化 cookie 和多站点会话
- ✅ 支持 JavaScript 执行
- ✅ 支持截图功能
- ✅ 可以正常使用 Perplexity、Claude 和 ChatGPT 等服务

### 推荐禁用内置的网页工具

为了避免出现 `missing_brave_api_key` 错误，并确保 OpenClaw 通过 openclaw-browser 处理网页请求，请禁用内置的网页工具：

编辑 `~/.openclaw/openclaw.json` 文件：
```json
{
  "tools": {
    "web": {
      "search": {
        "enabled": false
      },
      "fetch": {
        "enabled": false
      }
    }
  }
}
```

或者运行以下命令：
```bash
openclaw configure --section tools
```

这样就可以禁用 `web.search` 和 `web.fetch` 两个功能。

## 功能介绍

- **原生 WKWebView**：基于 macOS 的原生浏览器引擎，支持所有网站（无无头浏览模式带来的问题）
- **双窗口架构**：包含无边框的工具栏（标签页栏和地址栏）以及每个标签页对应的独立内容窗口
- **单例浏览器**：同一个浏览器实例会在多次调用中被重复使用，并支持标签页管理
- **登录辅助功能**：内置了针对 Perplexity、Grok、Claude 和 ChatGPT 的登录流程
- **进程隔离**：浏览器在子进程中运行，不会阻塞代理程序的执行

## 架构示意图
```
OpenClaw Agent
│
▼
OpenClawBrowserSkill (skill_wrapper.py)
│ - lazy init, login helpers, convenience methods
▼
NativeBrowser (browser_engine.py, singleton)
│ - IPC over stdin/stdout JSON
▼
Child Process (pywebview main thread)
├── Toolbar Window (frameless, always-on-top, chrome_ui.py)
│   ├── Tab bar
│   ├── URL bar
│   └── nav buttons
└── Content Windows (one native WKWebView per tab)
    ├── load_url()
    ├── execute_js()
    └── get_dom()
```

## API 参考

### 导航与页面交互

| 方法 | 描述 |
|--------|-------------|
| `skill.load(url, wait=2.0)` | 在当前标签页中加载指定 URL |
| `skill.execute_js(code)` | 运行 JavaScript 代码并返回结果 |
| `skill.get_dom(selector)` | 获取指定元素的 HTML 内容 |
| `skill.get_title()` | 获取页面标题 |
| `skill.get_url()` | 获取当前页面的 URL |
| `skill.snapshot()` | 获取整个页面的 HTML 内容及元数据 |

### 交互操作

| 方法 | 描述 |
|--------|-------------|
| `skill.click(selector, wait=1.0)` | 点击指定元素 |
| `skill.type_text(selector, text)` | 在输入框中输入文本 |
| `skill.wait_for_element(selector, timeout=10)` | 等待指定元素出现 |
| `skill.scroll_to_bottom()` | 滚动到页面底部 |
| `skill.scroll_to_element(selector)` | 将指定元素滚动到可见位置 |

### Cookie 与会话管理

| 方法 | 描述 |
|--------|-------------|
| `skill.get_cookies()` | 获取所有 cookie |
| `skill.set_cookie(name, value)` | 设置新的 cookie |

### 登录辅助功能

| 方法 | 描述 |
|--------|-------------|
| `skill.login_perplexity(email, pw)` | 登录 Perplexity.ai |
| `skill.login_grok(user, pw)` | 登录 Grok (X.com) |
| `skill.login_claude(email, pw)` | 登录 Claude.ai |
| `skill.login_chatgpt(email, pw)` | 登录 ChatGPT |

### 标签页管理

| 方法 | 描述 |
|--------|-------------|
| `skill.browser.new_tab(url)` | 打开新标签页 |
| `skill.browser.switch_tab(id)` | 切换到指定标签页 |
| `skill.browser.close_tab(id)` | 关闭指定标签页 |
| `skill.browser.get_tabs()` | 显示所有标签页列表 |

### 关闭浏览器

| 方法 | 描述 |
|--------|-------------|
| `skill.close()` | 关闭整个浏览器 |

## 使用示例

### 示例：加载并读取页面内容
```python
from src import OpenClawBrowserSkill

skill = OpenClawBrowserSkill()
skill.load('https://example.com')

# Get page content
title = skill.get_title()
print(f"Page title: {title}")

# Execute JavaScript
result = skill.execute_js('document.querySelector("h1").textContent')
print(f"H1 text: {result}")

skill.close()
```

### 示例：填写表单
```python
from src import OpenClawBrowserSkill

skill = OpenClawBrowserSkill()
skill.load('https://example.com/contact')

# Wait for form to load
skill.wait_for_element('input[name="email"]')

# Fill form
skill.type_text('input[name="email"]', 'user@example.com')
skill.type_text('textarea[name="message"]', 'Hello from OpenClaw!')
skill.click('button[type="submit"]')

# Wait for confirmation
skill.wait_for_element('.success-message')

skill.close()
```

### 示例：登录 Perplexity
```python
from src import OpenClawBrowserSkill

skill = OpenClawBrowserSkill()

# Built-in login helper
skill.login_perplexity('your-email@example.com', 'your-password')

# Now you can use Perplexity
skill.load('https://perplexity.ai')
skill.type_text('textarea[placeholder="Ask anything..."]', 'What is quantum computing?')
skill.click('button[aria-label="Submit"]')

skill.close()
```

### 示例：多标签页操作
```python
from src import OpenClawBrowserSkill

skill = OpenClawBrowserSkill()

# Open multiple tabs
tab1 = skill.browser.new_tab('https://github.com')
tab2 = skill.browser.new_tab('https://stackoverflow.com')

# Switch between tabs
skill.browser.switch_tab(tab1)
title1 = skill.get_title()

skill.browser.switch_tab(tab2)
title2 = skill.get_title()

print(f"Tab 1: {title1}, Tab 2: {title2}")

# Close individual tabs
skill.browser.close_tab(tab1)
skill.browser.close_tab(tab2)

skill.close()
```

## 系统要求

- macOS 10.14 或更高版本
- Python 3.12 或更高版本
- 必需安装 `pywebview`（版本 >= 5.1）

## 重要说明

- **浏览器为单例**：再次调用 `OpenClawBrowserSkill()` 时，会使用相同的浏览器窗口。如需打开新页面，请使用 `new_tab()` 方法。
- **进程隔离**：浏览器在子进程中运行，不会阻塞代理程序的执行。
- **CSS 选择器**：所有交互操作都使用 CSS 选择器（例如 `'button.submit'`, `'input[name="email"]'`）。
- **Cookie 持久化**：登录会话信息会在多次调用之间保持不变。

## 测试

运行测试套件：
```bash
# GUI test suite (9 tests, needs display)
python test_gui_browser.py

# pytest suite
pytest tests/ -v
```

## 故障排除

- **浏览器未出现**：确保您使用的操作系统是 macOS 10.14 或更高版本。
- **元素未找到**：使用 `execute_js()` 方法检查页面结构。
- **登录失败**：检查用户名和密码是否正确，以及目标网站是否正常响应。
- **性能问题**：作为原生应用，浏览器应具有较高的运行效率。如果出现性能问题，请检查系统资源使用情况。

## 报告问题

如遇到任何问题，请在以下链接提交 issue：  
https://github.com/yungookim/openclaw-browser

## 许可证

本项目采用 MIT 许可协议（详见 LICENSE 文件）。
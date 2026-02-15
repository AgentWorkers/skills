---
name: camoufox-stealth-browser
homepage: https://github.com/kesslerio/camoufox-stealth-browser-clawhub-skill
description: 使用 Camoufox（经过修改的 Firefox）在隔离容器中实现 C++ 级别的反机器人浏览器自动化技术。该技术能够绕过 Cloudflare Turnstile、Datadome、Airbnb 和 Yelp 等安全防护机制。相比基于 Chrome 的解决方案（如 undetected-chromedriver 或 puppeteer-stealth，这些方案仅在 JavaScript 层面进行修改），Camoufox 的性能更优越且更难被检测到。当标准的 Playwright/Selenium 被屏蔽时，可以使用该技术来实现自动化操作。
metadata:
  openclaw:
    emoji: "🦊"
    requires:
      bins: ["distrobox"]
      env: []
---

# Camoufox 隐形浏览器 🦊

**利用 Camoufox 实现 C++ 级别的反机器人检测机制**——Camoufox 是一个基于 Firefox 的定制版本，其中包含了直接编译到浏览器中的隐形功能模块，而非通过 JavaScript 动态添加的。

## 为什么选择 Camoufox 而不是基于 Chrome 的解决方案？

| 方法 | 检测难度 | 使用工具 |
|----------|-----------------|-------|
| **Camoufox** | C++ 编译的隐形模块 | 将浏览器自身的特征信息伪装得无法被检测到 |
| `undetected-chromedriver` | JavaScript 运行时修改 | 可能通过时间分析被检测到 |
| `puppeteer-stealth` | JavaScript 注入 | 页面加载后才会应用修改，因此仍可被检测到 |
| `playwright-stealth` | JavaScript 注入 | 同样存在被检测的风险 |

**Camoufox 在源代码层面修改 Firefox**——它真正伪造了 WebGL、Canvas、AudioContext 等组件的特征信息，而非仅仅通过 JavaScript 动作进行伪装，这些伪装方式容易被反机器人系统识别出来。

## 主要优势：

1. **C++ 级别的隐形技术**：特征信息伪装是通过编译到浏览器中实现的，而非依赖 JavaScript 动作。
2. **容器隔离**：在 `distrobox` 环境中运行，保护宿主系统的安全。
3. **双工具策略**：Camoufox 适用于浏览器操作，`curl_cffi` 仅用于 API 请求（无需占用浏览器资源）。
4. **基于 Firefox**：相比 Chrome，Camoufox 更难被反机器人系统识别（因为更多人使用 Chrome 来执行自动化操作）。

## 适用场景：

- 当标准的 Playwright 或 Selenium 被阻止时。
- 当网站显示 Cloudflare 的验证提示或“正在检查您的浏览器”时。
- 需要抓取 Airbnb、Yelp 等受保护的网站数据时。
- 当 `puppeteer-stealth` 或 `undetected-chromedriver` 失效时。
- 需要真正的隐形效果，而不仅仅是简单的 JavaScript 遮盖手段。

## 工具选择：

| 工具 | 功能 | 适用场景 |
|------|-------|----------|
| **Camoufox** | C++ 编译的隐形模块 | 适用于所有需要伪装的网站（如 Cloudflare、Datadome、Yelp、Airbnb） |
| **curl_cffi** | TLS 伪造技术 | 仅适用于 API 请求，无需浏览器，速度非常快 |

## 快速入门：

所有脚本都在 `pybox` 容器中运行，以实现隔离。

⚠️ **请明确使用 `python3.14`**——`pybox` 可能安装了多个版本的 Python，可能导致包版本不兼容。

### 1. 设置（首次使用）

```bash
# Install tools in pybox (use python3.14)
distrobox-enter pybox -- python3.14 -m pip install camoufox curl_cffi

# Camoufox browser downloads automatically on first run (~700MB Firefox fork)
```

### 2. 获取受保护的页面内容

**使用 Camoufox 浏览器：**
```bash
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py "https://example.com" --headless
```

**仅通过 API 请求（使用 curl_cffi）：**
```bash
distrobox-enter pybox -- python3.14 scripts/curl-api.py "https://api.example.com/endpoint"
```

## 架构概述

```
┌─────────────────────────────────────────────────────────┐
│                     OpenClaw Agent                       │
├─────────────────────────────────────────────────────────┤
│  distrobox-enter pybox -- python3.14 scripts/xxx.py         │
├─────────────────────────────────────────────────────────┤
│                      pybox Container                     │
│         ┌─────────────┐  ┌─────────────┐               │
│         │  Camoufox   │  │  curl_cffi  │               │
│         │  (Firefox)  │  │  (TLS spoof)│               │
│         └─────────────┘  └─────────────┘               │
└─────────────────────────────────────────────────────────┘
```

## 工具详细信息：

### Camoufox  
- **简介**：基于 Firefox 的定制版本，包含 C++ 级别的隐形功能模块。  
- **优点**：最佳的伪装效果，能够自动通过反机器人系统的检测。  
- **缺点**：下载大小约为 700MB，基于 Firefox 构建。  
- **适用场景**：所有需要伪装的网站（如 Cloudflare、Datadome、Yelp、Airbnb）。

### curl_cffi  
- **简介**：一个 Python HTTP 客户端，用于伪造浏览器的 TLS 特征信息。  
- **优点**：无需占用浏览器资源，执行速度极快。  
- **缺点**：仅支持 API 请求，不支持 JavaScript 动作。  
- **适用场景**：已知 API 端点，或需要反向工程移动应用程序的场景。

## 关键注意事项：代理设置

**使用数据中心 IP（如 AWS、DigitalOcean）访问 Airbnb 或 Yelp 时**，可能会立即被拒绝访问。  
**必须使用住宅类或移动类代理服务器：**

```python
# Example proxy config
proxy = "http://user:pass@residential-proxy.example.com:8080"
```

请参考 **[references/proxy-setup.md](references/proxy-setup.md)** 以获取代理配置指南。

## 行为技巧：

像 Airbnb 或 Yelp 这样的网站会使用行为分析来检测自动化访问。为了避免被检测到，请遵循以下建议：

1. **预热**：不要直接访问目标 URL，先访问首页，浏览页面并点击链接。
2. **模拟鼠标操作**：随机生成鼠标移动轨迹（Camoufox 可自动处理这部分操作）。
3. **控制操作间隔**：在每次操作之间添加随机延迟（2-5 秒）。
4. **保持会话连续性**：在同一会话期间使用相同的代理 IP，避免每次请求都更换代理。

## 注意：无头模式的使用

⚠️ 旧版本的 `--headless` 标志会被反机器人系统识别。推荐使用以下方法：
- **新版本的无头模式**：使用 `headless="new"`（Chrome 109 及更高版本）。
- **Xvfb**：在虚拟显示器中运行带界面的浏览器。
- **常规无头模式**：只有在必要时才使用无头模式（通常是最可靠的方式）。

```bash
# Xvfb approach (Linux)
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python scripts/camoufox-fetch.py "https://example.com"
```

## 常见问题及解决方法：

| 问题 | 解决方案 |
|---------|----------|
| 立即出现“访问被拒绝”的错误 | 使用住宅类代理服务器。 |
| 遭遇 Cloudflare 的验证提示 | 尝试使用 Camoufox 而不是 Nodriver。 |
- 在 pybox 中浏览器崩溃 | 安装缺失的依赖库：`sudo dnf install gtk3 libXt`。 |
- TLS 特征信息被识别 | 使用 `curl_cffi` 并设置 `impersonate="chrome120"`。 |
- 出现“Turnstile”验证提示 | 增加操作间隔时间或模拟鼠标动作。 |
- 报错 `ModuleNotFoundError: camoufox` | 明确使用 `python3.14` 而不是 `python` 或 `python3`。 |
- 出现 `greenlet` 程序崩溃（退出代码 139） | 确保使用 `python3.14`。 |
- 出现 `libstdc++.so.6` 错误**（NixOS 环境）：在 pybox 中使用 `python3.14`。 |

### Python 版本问题（NixOS/pybox）

`pybox` 容器中可能安装了多个版本的 Python，导致包版本不兼容。  
```bash
# Check which Python has camoufox
distrobox-enter pybox -- python3.14 -c "import camoufox; print('OK')"

# Wrong (may use different Python)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py ...

# Correct (explicit version)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py ...
```

如果遇到程序崩溃或导入错误，请务必明确使用 `python3.14`。

## 示例代码：

- **抓取 Airbnb 的房源信息**：```bash
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py \
  "https://www.airbnb.com/rooms/12345" \
  --headless --wait 10 \
  --screenshot airbnb.png
```
- **抓取 Yelp 的商家信息**：```bash
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py \
  "https://www.yelp.com/biz/some-restaurant" \
  --headless --wait 8 \
  --output yelp.html
```
- **使用 TLS 伪造技术进行 API 数据抓取**：```bash
distrobox-enter pybox -- python3.14 scripts/curl-api.py \
  "https://api.yelp.com/v3/businesses/search?term=coffee&location=SF" \
  --headers '{"Authorization": "Bearer xxx"}'
```

## 会话管理

通过会话管理，可以在多次请求之间保持登录状态，无需重新登录。

### 快速入门步骤：

```bash
# 1. Login interactively (headed browser opens)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile airbnb --login "https://www.airbnb.com/account-settings"

# Complete login in browser, then press Enter to save session

# 2. Reuse session in headless mode
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile airbnb --headless "https://www.airbnb.com/trips"

# 3. Check session status
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile airbnb --status "https://www.airbnb.com"
```

## 常用命令参数说明：

| 参数 | 说明 |
|------|-------------|
| `--profile NAME` | 为会话指定名称（必需） |
| `--login` | 开启交互式登录模式（显示浏览器界面）。 |
| `--headless` | 以无头模式使用已保存的会话。 |
| `--status` | 检查会话是否有效。 |
| `--export-cookies FILE` | 将 cookies 导出为 JSON 文件以备备份。 |
| `--import-cookies FILE` | 从 JSON 文件中导入 cookies。 |

## 数据存储位置：

- **存储路径**：`~/.stealth-browser/profiles/<name>/`  
- **权限设置**：目录权限为 `700`，文件权限为 `600`。  
- **文件名规则**：只能使用字母、数字、下划线（_）和减号（-），长度不超过 63 个字符。

## Cookies 处理规则：

- **保存方式**：所有网站的 Cookies 都保存在浏览器配置文件中。  
- **使用规则**：仅使用与目标网站域名匹配的 Cookies。  
- **单点登录（SSO）处理**：如果被重定向到 Google 或其他认证页面，需要重新登录以更新会话状态。

## 登录状态检测：

脚本通过多种方式检测会话是否过期：
- **HTTP 状态码**：401、403  
- **URL 路径**：`/login`、`/signin`、`/auth`  
- **页面标题**：包含“login”、“sign in”等字样  
- **页面内容**：包含“captcha”、“verify”、“authenticate”等关键词  
- **表单元素**：密码输入框  

如果在无头模式下检测到会话过期，需要使用 `--login` 参数重新登录。

### 远程登录（SSH）

由于 `--login` 需要显示浏览器界面，因此需要配置显示转发：

- **推荐方式：X11 显示转发**：```bash
# Connect with X11 forwarding
ssh -X user@server

# Run login (opens browser on your local machine)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile mysite --login "https://example.com"
```  
- **备用方案：VNC**：```bash
# On server: start VNC session
vncserver :1

# On client: connect to VNC
vncviewer server:1

# In VNC session: run login
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile mysite --login "https://example.com"
```

## 安全注意事项：

⚠️ **Cookies 即为敏感信息**：请像处理密码一样保护配置文件和导出的 Cookies：
- 配置文件目录的权限设置为 `chmod 700`（仅允许所有者访问）。  
- 导出的 Cookies 也需设置权限为 `chmod 600`。  
- 不要通过不安全的渠道共享配置文件或 Cookies。  
- 考虑对备份文件进行加密。

## 注意事项：

- **局限性**：
  - `localStorage` 和 `sessionStorage` 中的数据无法被导出，建议使用浏览器自带的会话管理机制。  
  - IndexedDB 数据不支持跨平台迁移，因为存储在浏览器配置文件中。  
  - 单个会话只能由一个进程访问（版本 1 的限制）。

## 参考资料：

- [references/proxy-setup.md](references/proxy-setup.md)：代理配置指南  
- [references/fingerprint-checks.md]：反机器人系统通常会检测哪些特征信息。
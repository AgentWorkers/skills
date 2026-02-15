---
name: camoufox-stealth
description: 使用 Camoufox（经过修改的 Firefox）在隔离容器中实现 C++ 级别的反机器人浏览器自动化。该方案能够绕过 Cloudflare Turnstile、Datadome、Airbnb 和 Yelp 等安全机制。相比基于 Chrome 的解决方案（如 `undetected-chromedriver` 或 `puppeteer-stealth`，这些方案仅在 JavaScript 层面进行修改），Camoufox 的性能更优越且更难被检测到。当标准的 Playwright/Selenium 被屏蔽时，可以使用该方案。
metadata:
  openclaw:
    emoji: "🦊"
    requires:
      bins: ["distrobox"]
      env: []
---

# Camoufox 隐形浏览器 🦊

**利用 Camoufox 实现 C++ 级别的反机器人策略**——Camoufox 是一个基于 Firefox 的定制版本，其中的隐形功能被直接编译到浏览器内核中，而非通过 JavaScript 进行附加。

## 为什么选择 Camoufox 而非基于 Chrome 的解决方案？

| 方法 | 检测难度 | 使用工具 |
|----------|-----------------|-------|
| **Camoufox** | C++ 编译的隐形代码** | 隐形特征被直接嵌入到浏览器中，无法被检测到 |
| **undetected-chromedriver** | JavaScript 运行时修改** | 可能通过时间分析被检测到 |
| **puppeteer-stealth** | JavaScript 注入** | 页面加载后应用修改，因此可被检测到 |
| **playwright-stealth** | JavaScript 注入** | 同样存在被检测的风险 |

**Camoufox 在源代码层面修改 Firefox**——它能够真正伪造 WebGL、Canvas 和 AudioContext 的特征，而不仅仅是通过 JavaScript 进行伪装，这些伪装方式容易被反机器人系统识破。

## 主要优势：

1. **C++ 级别的隐形技术**：隐形功能通过编译直接集成到浏览器中，而非依赖 JavaScript 动作。
2. **容器隔离**：在 `distrobox` 环境中运行，保护主机系统免受影响。
3. **双工具组合**：Camoufox 适用于浏览器操作，`curl_cffi` 仅用于 API 请求（无需额外加载浏览器）。
4. **基于 Firefox**：相比 Chrome，Camoufox 更难被机器人程序识别（因为大多数机器人使用 Chrome）。

## 适用场景：

- 当标准的 Playwright 或 Selenium 工具被阻止时。
- 当网站显示 Cloudflare 的验证提示或“检查浏览器”信息时。
- 需要抓取 Airbnb、Yelp 等受保护的网站数据时。
- 当 `puppeteer-stealth` 或 `undetected-chromedriver` 失效时。
- 需要真正实现隐形访问，而不仅仅是使用临时的 JavaScript 伪装。

## 工具选择：

| 工具 | 特点 | 适用场景 |
|------|-------|----------|
| **Camoufox** | C++ 编译的隐形代码** | 适用于所有需要保护的网站（如 Cloudflare、Datadome、Yelp、Airbnb） |
| **curl_cffi** | 使用 TLS 伪造技术** | 仅适用于 API 请求，无需浏览器，速度非常快 |

## 快速入门：

所有脚本都在 `pybox` 容器中运行，以实现隔离。

⚠️ **请务必使用 `python3.14`**——因为 `pybox` 可能安装了多个版本的 Python，可能导致包版本不兼容。

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
- **特点**：基于 Firefox 的定制版本，包含 C++ 级别的隐形功能。  
- **优势**：最有效的伪装手段，能自动通过反机器人系统的检测。  
- **缺点**：下载体积约为 700MB，基于 Firefox 构造。  
- **适用场景**：所有需要保护的网站（如 Cloudflare、Datadome、Yelp、Airbnb）。

### curl_cffi  
- **特点**：一个使用 Python 编写的 HTTP 客户端，能够伪造浏览器的 TLS 特征。  
- **优势**：无需依赖浏览器，执行速度极快。  
- **缺点**：仅支持 API 请求，不支持 JavaScript 功能。  
- **适用场景**：适用于已知的 API 端点，或需要反向工程移动应用的场景。

## 关键注意事项：代理设置

**使用数据中心 IP（如 AWS、DigitalOcean）访问 Airbnb 或 Yelp 时，可能会立即被拒绝访问！**  
必须使用住宅或移动代理：

```python
# Example proxy config
proxy = "http://user:pass@residential-proxy.example.com:8080"
```

有关代理配置的详细信息，请参阅 **[references/proxy-setup.md](references/proxy-setup.md)**。

## 行为技巧：

像 Airbnb 或 Yelp 这样的网站会使用行为分析来检测用户是否为机器人。为了避免被识别：
1. **预热**：不要直接访问目标网址，先访问首页，浏览页面并点击链接。
2. **鼠标操作**：模拟随机的鼠标移动（Camoufox 会自动处理这部分操作）。
3. **时间控制**：在操作之间添加随机延迟（2-5 秒），避免固定时间间隔。
4. **会话持续性**：在同一会话期间使用相同的代理 IP，避免每次请求都更换代理。

## 注意事项：无头模式

⚠️ 旧的 `--headless` 标志容易被识别。推荐使用以下方法：
1. **新版本的无头模式**：使用 `headless="new"`（Chrome 109 及更高版本）。
2. **Xvfb**：在虚拟显示器中运行带界面的浏览器。
3. **有界面的浏览器**：如果可能的话，尽量使用有界面的浏览器（最可靠的方法）。

```bash
# Xvfb approach (Linux)
Xvfb :99 -screen 0 1920x1080x24 &
export DISPLAY=:99
python scripts/camoufox-fetch.py "https://example.com"
```

## 常见问题及解决方法：

| 问题 | 解决方案 |
|---------|----------|
| 立即出现“访问被拒绝”错误 | 使用住宅代理。 |
| 遭遇 Cloudflare 的验证提示 | 尝试使用 Camoufox 而不是 Nodriver。 |
| 在 pybox 中浏览器崩溃 | 安装缺失的依赖库：`sudo dnf install gtk3 libXt`。 |
| TLS 伪造失败 | 使用 `curl_cffi` 并设置 `impersonate="chrome120"`。 |
| 出现“Turnstile”验证提示 | 增加随机鼠标操作，延长操作间隔时间。 |
| 报错 `ModuleNotFoundError: camoufox` | 确保使用 `python3.14` 而不是 `python` 或 `python3`。 |
| 出现 `greenlet` 程序崩溃（退出代码 139）**：Python 版本不匹配，使用 `python3.14`。 |
| 出现 `libstdc++.so.6` 错误**：可能是 NixOS 的库路径问题，在 pybox 中使用 `python3.14`。 |

### Python 版本相关问题（NixOS/pybox）

`pybox` 容器中可能安装了多个版本的 Python，导致包版本不兼容：

```bash
# Check which Python has camoufox
distrobox-enter pybox -- python3.14 -c "import camoufox; print('OK')"

# Wrong (may use different Python)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py ...

# Correct (explicit version)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py ...
```

如果遇到程序崩溃或导入错误，请务必明确指定使用 `python3.14`。

## 示例代码：

### 抓取 Airbnb 的房源信息

```bash
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py \
  "https://www.airbnb.com/rooms/12345" \
  --headless --wait 10 \
  --screenshot airbnb.png
```

### 抓取 Yelp 的企业信息

```bash
distrobox-enter pybox -- python3.14 scripts/camoufox-fetch.py \
  "https://www.yelp.com/biz/some-restaurant" \
  --headless --wait 8 \
  --output yelp.html
```

### 使用 TLS 伪造技术进行 API 请求

```bash
distrobox-enter pybox -- python3.14 scripts/curl-api.py \
  "https://api.yelp.com/v3/businesses/search?term=coffee&location=SF" \
  --headers '{"Authorization": "Bearer xxx"}'
```

## 会话管理

通过会话管理，可以在多次请求之间保持登录状态，无需重新登录。

### 快速入门步骤

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

### 常用参数说明：

| 参数 | 说明 |
|------|-------------|
| `--profile NAME` | 为会话指定名称（必需） |
| `--login` | 开启交互式登录模式（使用有界面的浏览器）。 |
| `--headless` | 在无头模式下使用已保存的会话。 |
| `--status` | 检查会话是否有效。 |
| `--export-cookies FILE` | 将 cookies 导出为 JSON 文件以备备份。 |
| `--import-cookies FILE` | 从 JSON 文件中导入 cookies。 |

## 数据存储：

- **存储位置**：`~/.stealth-browser/profiles/<name>/`  
- **权限设置**：目录权限设置为 `700`，文件权限设置为 `600`。  
- **文件夹名称**：只能使用字母、数字、`_` 和 `-`，长度不超过 63 个字符。

## Cookies 处理：

- **保存**：所有来自不同网站的 cookies 都保存在浏览器配置文件中。  
- **恢复**：仅使用与目标网址匹配的 cookies。  
- **单点登录（SSO）**：如果页面重定向到 Google 或其他认证域，需要重新登录以更新会话状态。

## 登录状态检测：

脚本通过多种方式检测会话是否过期：
- **HTTP 状态码**：401、403  
- **URL 纹理**：`/login`、`/signin`、`/auth`  
- **页面标题**：包含“login”、“sign in”等字样  
- **页面内容**：包含“captcha”、“verify”、“authenticate”等关键词  
- **表单元素**：检查是否存在密码输入框  

如果在无头模式下遇到这些问题，可以尝试重新运行脚本并加上 `--login` 参数来刷新会话。

## 远程登录（SSH）

由于 `--login` 需要显示浏览器界面，因此需要配置显示转发：

**推荐方案：X11 显示转发**：
```bash
# Connect with X11 forwarding
ssh -X user@server

# Run login (opens browser on your local machine)
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile mysite --login "https://example.com"
```

**备用方案：VNC**：
```bash
# On server: start VNC session
vncserver :1

# On client: connect to VNC
vncviewer server:1

# In VNC session: run login
distrobox-enter pybox -- python3.14 scripts/camoufox-session.py \
  --profile mysite --login "https://example.com"
```

## 安全提示：

⚠️ **Cookies 即为敏感信息**：请像对待密码一样保护配置文件和 cookies：
- 配置文件目录的权限设置为 `chmod 700`（仅允许所有者访问）。  
- 导出的 cookies 也需设置权限为 `chmod 600`。  
- 不要通过不安全的渠道共享配置文件或 cookies。  
- 考虑对备份文件进行加密。

## 注意事项：

- **局限性**：
  - `localStorage` 和 `sessionStorage` 中的数据无法被导出，建议使用浏览器自带的会话管理机制。  
  - IndexedDB 数据无法跨平台移植，因此会话数据存储在浏览器配置文件中。  
  - 当前版本不支持同时访问多个会话，每个会话需要单独的进程。

## 参考资料：

- [references/proxy-setup.md](references/proxy-setup.md) — 代理配置指南  
- [references/fingerprint-checks.md] — 反机器人系统通常会检查哪些特征。
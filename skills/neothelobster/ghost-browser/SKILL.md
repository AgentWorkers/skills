---
name: ghost-browser
description: 使用 nodriver 的自动化 Chrome 浏览器，用于 AI 代理的网页任务。具备完整的 CLI 控制功能，支持 LLM 优化的命令；支持基于文本的交互、markdown 格式的输出、会话管理以及智能元素匹配功能。
metadata:
  openclaw:
    emoji: "👻"
    requires:
      bins: ["python3", "google-chrome||chromium||/Applications/Google Chrome.app"]
      pip: ["nodriver>=0.38"]
---
# Ghost Browser

这是一个用于AI代理网页任务的自动化Chrome浏览器工具，由[nodriver](https://github.com/nicedayzhu/nodriver)提供强大的浏览器控制功能。所有命令的设计都旨在最小化令牌（token）的使用量，并最大化操作的准确性。

**用途：**网页自动化、截图、页面内容读取、表单填写、数据抓取、cookie/session管理以及浏览器配置的持久化。

## 使用方法 — 遵循以下工作流程

**务必遵循此工作流程。** **切勿将原始HTML内容（`content`）或CSS选择器（`click`/`type`）作为首选方法。**

### 第1步：导航并理解页面结构

`page-summary`命令会返回：页面标题、URL、页面上的元素数量（链接/按钮/输入框/表单）、是否存在登录表单，以及一段简短的文本预览。该命令的令牌消耗量约为10个。

### 第2步：确定可交互的元素

```bash
ghost-browser elements              # Numbered list of ALL interactive elements
ghost-browser elements --form-only  # Just form inputs (for login/signup/search)
```

**输出：**
```
[0] link "Home" → /
[1] link "Products" → /products
[2] button "Sign In"
[3] input[email] "Email address"
[4] input[password] "Password"
[5] submit "Log In"
```

### 第3步：通过可见文本进行交互（而非使用CSS选择器）

```bash
ghost-browser interact click "Sign In"
ghost-browser interact type "Email" --type-text "user@example.com"
ghost-browser interact type "Password" --type-text "secret123"

# Or fill entire forms at once
ghost-browser fill-form '{"email":"user@example.com","password":"secret123"}' --submit
```

### 第4步：以Markdown格式读取页面内容

****切勿使用`content`命令** — 因其会返回原始HTML，导致大量令牌被浪费。请使用`readable`命令代替。**

### 第5步：等待动态加载的页面

```bash
ghost-browser wait-ready             # Wait for network idle + DOM stable
ghost-browser wait-ready --timeout 10
```

### 登录示例

```bash
ghost-browser start
ghost-browser navigate https://mysite.com/login
ghost-browser wait-ready
ghost-browser elements --form-only
ghost-browser fill-form '{"email":"me@example.com","password":"mypass"}' --submit
ghost-browser wait-ready
ghost-browser page-summary           # Verify login succeeded
ghost-browser session save mysite    # Save auth state for later
```

### 恢复之前的会话状态

```bash
ghost-browser start --profile mysite
ghost-browser session load mysite
ghost-browser navigate https://mysite.com/dashboard
ghost-browser page-summary
```

## 命令参考

### 推荐使用的命令（优先选择这些命令）

| 命令 | 功能 | 令牌消耗量 |
|---------|-------------|------------|
| `page-summary` | 页面概览：标题、URL、元素数量 | 约10个令牌 |
| `elements` | 显示所有按钮、链接和输入框的列表 | 约50-200个令牌 |
| `elements --form-only` | 仅显示表单输入框 | 约10-50个令牌 |
| `readable` | 以清晰的Markdown格式显示整个页面内容 | 约500-10000个令牌 |
| `readable --max-length N` | 限制页面内容的长度为N个字符 | 可自定义 |
| `interact click "text"` | 根据可见文本点击元素 | 动作命令 |
| `interact type "label" --type-text "value"` | 根据标签或输入框提示文本进行输入 | 动作命令 |
| `fill-form '{"field":"value"}' --submit` | 填写表单并提交 | 动作命令 |
| `hover "text" --by-text` | 根据可见文本悬停鼠标 | 动作命令 |
| `wait-ready` | 等待页面加载完成 | 约5个令牌 |
| `session save <name>` | 保存cookies、localStorage和sessionStorage数据 | 约10个令牌 |
| `session load <name>` | 恢复之前的会话状态 | 约10个令牌 |

### 生命周期管理

```bash
ghost-browser start                          # Start browser daemon
ghost-browser start --headless               # Run without visible window
ghost-browser start --profile work           # Use named profile (persistent data)
ghost-browser start --extension /path/ext    # Load unpacked Chrome extension
ghost-browser start --proxy socks5://host:port  # Use proxy
ghost-browser stop                           # Graceful shutdown
ghost-browser status                         # Check if running
ghost-browser status --json                  # Machine-readable status
ghost-browser health                         # Quick health check
```

### 导航与标签页管理

执行`navigate`命令后，所有后续命令都会自动针对当前打开的标签页进行操作。

### 页面内容理解

```bash
ghost-browser page-summary                   # Quick overview (~10 tokens)
ghost-browser elements                       # All interactive elements (numbered)
ghost-browser elements --form-only           # Form inputs only
ghost-browser elements --limit 50            # Cap at 50 elements
ghost-browser readable                       # Full page as markdown
ghost-browser readable --max-length 5000     # Limit output length
ghost-browser content                        # Raw HTML (avoid — use readable instead)
```

### 基于文本的交互（推荐方法）

```bash
ghost-browser interact click "Sign In"       # Click by button/link text
ghost-browser interact type "Email" --type-text "user@example.com"  # Type by label
ghost-browser interact click "Products" --index 1  # Click 2nd match if multiple
ghost-browser fill-form '{"email":"a@b.com","password":"x"}' --submit
ghost-browser hover "Menu" --by-text         # Hover by visible text
```

### 使用CSS选择器进行交互（备用方案）

仅在基于文本的交互失败时使用此方法。

```bash
ghost-browser click "button.submit"          # Click by CSS selector
ghost-browser type "input#email" "a@b.com"   # Type by CSS selector
ghost-browser find "h1"                      # Find elements by selector
ghost-browser hover ".dropdown"              # Hover by CSS selector
ghost-browser wait ".loaded" --timeout 10    # Wait for element to appear
ghost-browser scroll --down                  # Scroll down
ghost-browser scroll --up                    # Scroll up
ghost-browser scroll --to 500               # Scroll to Y position
ghost-browser eval "document.title"          # Execute arbitrary JavaScript
```

### Cookie与数据存储

```bash
ghost-browser cookies                        # List all cookies
ghost-browser cookies --domain example.com   # Filter by domain
ghost-browser set-cookie name value          # Set a cookie
ghost-browser set-cookie name value --domain .example.com  # Set with domain
ghost-browser clear-cookies                  # Clear all cookies
ghost-browser clear-cookies --domain example.com  # Clear for domain
ghost-browser save-cookies --file cookies.json  # Export cookies to JSON
ghost-browser load-cookies cookies.json      # Import cookies from JSON
ghost-browser storage list                   # List localStorage entries
ghost-browser storage list --session         # List sessionStorage entries
ghost-browser storage get <key>              # Get a value
ghost-browser storage set <key> <value>      # Set a value
ghost-browser storage delete <key>           # Delete a key
ghost-browser storage clear                  # Clear all localStorage
```

会话数据会保存在`state/sessions/<name>.json`文件中，其中包含恢复登录状态所需的cookies和存储数据。不再需要的会话文件请及时删除。

### 文件与媒体处理

```bash
ghost-browser screenshot                         # Screenshot to auto-named file
ghost-browser screenshot --output ./page.png     # Screenshot to specific file
ghost-browser pdf --output page.pdf              # Save page as PDF
ghost-browser pdf --output page.pdf --landscape  # Landscape PDF
ghost-browser upload photo.jpg                   # Upload file (auto-detect file input)
ghost-browser upload doc.pdf --selector "#file"  # Upload to specific file input
ghost-browser download <url> --output file.pdf   # Download a file
```

### 调试

网络请求和控制台日志会自动在后台记录。

### 窗口管理

```bash
ghost-browser window --size 1920x1080        # Resize window
ghost-browser window --position 0x0          # Reposition window
```

### 配置管理

浏览器配置（历史记录、cookies、扩展程序）会在不同会话间保持一致。

```bash
ghost-browser profile list                   # List profiles with sizes
ghost-browser profile create <name>          # Create new profile
ghost-browser profile delete <name>          # Delete a profile and its data
ghost-browser profile default                # Show default profile
ghost-browser profile default <name>         # Set default profile
ghost-browser profile clone <src> <dst>      # Clone a profile
```

### 扩展程序管理

```bash
ghost-browser install-extension <source>     # Install from Web Store URL/ID or .crx file
ghost-browser install-extension <source> --name custom-name  # Install with custom folder name
ghost-browser list-extensions                # List all installed extensions
ghost-browser remove-extension <name>        # Remove an installed extension
ghost-browser load-extension <name>          # Load extension into running browser
ghost-browser load-extension                 # Load all extensions
ghost-browser unload-extension <name>        # Unload extension from running browser
```

### 面临的挑战处理

系统会自动检测并处理各种操作中的异常情况。

## 决策指南

| 我想... | 应使用哪个命令 |
|--------------|----------|
| 了解页面内容 | 先使用`page-summary`，如有需要再使用`elements` |
| 读取页面文本 | 使用`readable` |
| 点击按钮 | 使用`interact click "Button Text"` |
| 填写登录表单 | 使用`fill-form '{"email":"...","password":"..."}' --submit` |
| 在指定字段输入内容 | 使用`interact type "Field Label" --type-text "value"` |
| 等待页面加载完成 | 使用`wait-ready` |
| 查看可点击/可输入的内容 | 使用`elements`或`elements --form-only` |
| 保存登录信息 | 使用`session save <name>` |
| 恢复之前的登录状态 | 使用`session load <name>` |
| 调试失败请求 | 使用`network-log --filter domain.com` |
| 检查JavaScript错误 | 使用`console-log --level error` |
| 截取屏幕截图 | 使用`screenshot --output ./page.png` |
| 运行自定义JavaScript代码 | 使用`eval "your code here"` |

## JSON输出格式

所有命令都支持`--json`参数，以生成机器可读的输出格式：

```bash
ghost-browser page-summary --json
ghost-browser elements --json
ghost-browser readable --json
ghost-browser status --json
```

## 安装说明

安装完成后，请运行`setup.sh`脚本：

```bash
bash setup.sh
```

该脚本会创建一个Python虚拟环境并自动安装所需依赖库。

**系统要求：**
- Python 3.8及以上版本
- 系统上已安装Google Chrome浏览器
- nodriver（通过`setup.sh`脚本自动安装）

## 数据与隐私政策

该工具会将以下数据保存在`state/`目录下：

| 数据类型 | 存储位置 | 包含内容 |
|------|----------|----------|
| 浏览器状态 | `state/browser.json` | 浏览器端口信息、进程ID |
| 日志 | `state/browser.log` | 日志文件 |
| 用户配置 | `state/profiles/` | Chrome用户数据（历史记录、cookies） |
| 会话数据 | `state/sessions/` | 保存的会话状态（cookies、localStorage） |

**清理方式：**删除`state/`目录即可清除所有持久化数据。使用`ghost-browser profile delete <name>`命令可删除特定配置文件。

会话文件和cookies文件可能包含认证令牌，请谨慎处理，并在不再需要时删除。

## 安全性说明：

- 浏览器控制功能仅绑定到本地地址127.0.0.1（localhost），无法访问外部网络。
- 该工具不会修改目录外的任何文件。
- 无需使用环境变量或外部凭证。
- 所有持久化数据均存储在`state/`目录下。

### 功能说明

该工具是一个完整的浏览器自动化工具，包含以下功能（这些功能可能会被安全扫描工具识别）：
- **`eval`**：在浏览器环境中执行任意JavaScript代码（这是所有浏览器自动化工具的常见功能，相当于Playwright的`page.evaluate()`或Puppeteer的`page.evaluate()`）。
- **`upload` / `download`：读取本地文件上传或下载文件到本地。
- **`session save/load`：将cookies、localStorage和sessionStorage数据保存到`state/sessions/`目录下的JSON文件中。这些文件可能包含认证令牌，请妥善处理。
- **`install-extension` / `load-extension`：可编程地安装Chrome扩展程序。在macOS系统中，通过`.crx`文件安装扩展程序时可能需要使用`osascript`。
- **反检测机制**：使用nodriver替代Playwright/Puppeteer，避免设置`navigator.webdriver=true`；屏蔽可被检测到的CDP域名；修改鼠标事件坐标以规避点击检测。这些措施旨在绕过网站的反机器人检测机制，而非规避本地安全工具。

这些功能仅用于在浏览器内部操作，不会访问外部数据或发送任何数据到第三方。
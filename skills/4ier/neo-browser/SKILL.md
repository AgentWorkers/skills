---
name: neo
description: 浏览网站、阅读网页、与网页应用程序交互、调用网站API以及自动化网页任务。在以下情况下可以使用Neo：用户需要查看网站内容、阅读网页、在社交媒体（如Twitter/X）上发布内容、与任何网页应用程序进行交互、在特定网站上查找信息、从网站抓取数据、自动化浏览器操作，或者当您需要调用任何网站的API时。关键词：网站、网页、浏览、URL、HTTP、API、Twitter、推文、发布、抓取、网页应用程序、打开网站、检查网站内容、阅读网页、社交媒体、在线服务。
metadata:
  openclaw:
    requires:
      bins: [neo]
    install:
      - id: neo
        kind: node
        package: "@4ier/neo"
        bins: [neo]
        label: "Install Neo CLI (npm)"
---
# Neo — Web 应用程序 API 发现与执行

Neo 可以将任何网站转换为可通过 AI 调用的 API。它能够被动捕获浏览器流量，生成 API 架构，并允许您直接调用这些 API——无需进行数据抓取或逆向工程。

## 首次设置

```bash
# Install CLI
npm i -g @4ier/neo

# One-time setup: detects Chrome, installs extension, configures profile
neo setup

# Start Chrome with Neo extension
neo start

# Verify everything works
neo doctor
```

所有 6 项检查都应该显示为 “✓”。如果没有，请再次运行 `neo setup`。

## 先决条件：支持 CDP 的浏览器

Neo 需要使用启用了 Chrome 开发工具协议（CDP）的 Chrome 浏览器。

```bash
# Check connection
neo doctor

# If Chrome isn't running with CDP:
neo start

# Or start manually with your own profile:
# google-chrome-stable --remote-debugging-port=9222 &
```

**环境变量**（均为可选）：
- `NEO_CDP_URL` — CDP 端点（默认：`http://localhost:9222`）
- `NEO_EXTENSION_ID` — 强制使用特定的扩展程序 ID（默认：自动检测）
- `NEO_SCHEMA_DIR` — 架构存储目录（默认：`~/.neo/schemas`）

## 完整工作流程

### 第 1 步：查看 Neo 已经获取的信息

```bash
neo status                    # Overview: domains, capture counts, extension status
neo schema list               # Cached API schemas (knowledge from past browsing)
```

### 第 2 步：打开目标网站（如需要）

```bash
neo open https://example.com  # Opens in Chrome
```

### 第 3 步：读取页面内容

```bash
neo read example.com          # Extract readable text from the page (like reader mode)
```

### 第 4 步：通过 API 进行交互（快速途径）

```bash
# Check if we have API knowledge for this domain
neo schema show x.com

# Smart API call: auto-finds endpoint + auth
neo api x.com HomeTimeline
neo api x.com CreateTweet --body '{"variables":{"tweet_text":"hello"}}'
neo api github.com notifications
```

### 第 5 步：在页面上下文中执行操作

```bash
neo exec <url> --method POST --body '{}' --tab example.com --auto-headers
neo replay <capture-id> --tab example.com
neo eval "document.title" --tab example.com
```

### 第 6 步：进行 UI 自动化操作（当不存在 API 时）

```bash
neo snapshot                  # Get accessibility tree with @ref mapping
neo click @14                 # Click element by reference
neo fill @7 "search query"    # Fill input field
neo type @7 "text"            # Append text
neo press Enter               # Keyboard input
neo scroll down 500           # Scroll
neo screenshot                # Capture screenshot
```

### 第 7 步：清理资源——使用完成后务必关闭标签页

```bash
neo tabs                                        # List open tabs
neo eval "window.close()" --tab example.com     # Close tab
```

**⚠️ 资源管理**：每次使用 Neo 时都会创建一个新的标签页。使用完成后请务必关闭所有标签页。

## API 发现流程

当您需要了解某个网站使用了哪些 API 时：

```bash
# 1. Open the site, browse around to generate captures
neo open https://example.com

# 2. Check accumulated captures
neo capture list example.com --limit 20
neo capture search "api" --limit 10

# 3. Generate API schema
neo schema generate example.com

# 4. Explore the schema
neo schema show example.com

# 5. Call discovered APIs
neo api example.com <endpoint-keyword>
```

## 命令参考

```bash
# --- Page Reading & Interaction ---
neo open <url>                          # Open URL in Chrome (creates new tab!)
neo read <tab-pattern>                  # Extract readable text from page
neo eval "<js>" --tab <pattern>         # Run JS in page context
neo tabs [filter]                       # List open Chrome tabs

# --- UI Automation ---
neo snapshot [-i] [-C] [--json]         # A11y tree with @ref mapping
neo click @ref [--new-tab]              # Click element
neo fill @ref "text"                    # Clear + fill input
neo type @ref "text"                    # Append text to input
neo press <key>                         # Keyboard key (Ctrl+a, Enter, etc.)
neo hover @ref                          # Hover
neo scroll <dir> [px] [--selector css]  # Scroll
neo select @ref "value"                 # Select dropdown
neo screenshot [path] [--full]          # Capture screenshot
neo get text @ref | url | title         # Extract info
neo wait @ref | --load | <ms>           # Wait for element/load/time

# --- Capture & Traffic ---
neo status                              # Overview
neo capture list [domain] [--limit N]   # Recent captures
neo capture search <query>              # Search by URL pattern
neo capture domains                     # Domains with counts
neo capture detail <id>                 # Full capture details
neo capture stats <domain>              # Statistics breakdown

# --- Schema (API Knowledge) ---
neo schema generate <domain>            # Generate from captures
neo schema show <domain>                # Human-readable
neo schema list                         # All cached schemas
neo schema search <query>               # Search endpoints
neo schema openapi <domain>             # Export OpenAPI 3.0

# --- API Execution ---
neo api <domain> <keyword> [--body '{}']  # Smart call (schema + auto-auth)
neo exec <url> [--method POST] [--body] [--tab pattern] [--auto-headers]
neo replay <id> [--tab pattern]         # Replay captured call

# --- Analysis ---
neo flows <domain>                      # API call sequence patterns
neo deps <domain>                       # Data flow dependencies
neo suggest <domain>                    # AI capability analysis

# --- Setup & Diagnostics ---
neo setup                               # First-time setup (Chrome + extension)
neo start                               # Launch Chrome with Neo extension
neo doctor                              # Health check
neo version                             # Version
```

## 决策树

```
User wants to interact with a website
  │
  ├─ Just read content? → neo read <domain>
  │
  ├─ Need to call an API?
  │   ├─ neo schema show <domain> → schema exists? → neo api <domain> <keyword>
  │   └─ No schema? → neo open <url> → browse → neo schema generate <domain>
  │
  ├─ Need to fill forms / click buttons?
  │   └─ neo snapshot → neo click/fill/type @ref
  │
  └─ Complex multi-step interaction?
      └─ Combine: neo open → neo snapshot → neo click/fill → neo read → close tab
```

## 主要规则

1. **始终先检查 CDP**：运行 `neo doctor` 以确认 Chrome 是否可访问。
2. **使用完成后关闭标签页**：使用 `neo eval "window.close()" --tab <pattern>`。
3. **在调用 API 之前检查架构**：使用 `neo schema show <domain>` 来查看已缓存的架构信息。
4. **优先使用 API，而非 UI 自动化**：如果存在 API，请使用 `neo api`/`neo exec`，而不是通过截图+点击的方式。
5. **每个域的捕获限制**：最多捕获 500 条记录，系统会自动清理数据。无需担心存储问题。
6. **身份验证是自动完成的**：API 调用在浏览器上下文中执行，会继承用户的 cookies、session 和 CSRF 信息。
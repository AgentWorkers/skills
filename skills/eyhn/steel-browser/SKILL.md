---
name: steel-browser
description: 通过 Steel.dev 控制云浏览器会话，以实现网页自动化和计算机使用代理功能。当您需要浏览网页、填写表单、点击元素、截图、抓取内容或构建浏览器自动化脚本时，可以使用该工具。该工具采用 Playwright 选择器（基于 CSS、文本或 ARIA 标签）进行定位，比基于像素坐标的 e2b-desktop 更可靠，尤其适用于纯网页任务。同时支持使用住宅代理（residential proxies）以及解决 CAPTCHA 验证问题。
---
# Steel Browser 技能

通过 [Steel.dev](https://steel.dev) 和 Playwright Python SDK 使用云浏览器。  
非常适合用于网页自动化、数据抓取、表单填写以及 AI 代理的浏览器操作。

## 先决条件

```bash
pip install steel-sdk playwright
export STEEL_API_KEY=your_key_here
```

在 https://app.steel.dev → 设置 → API 密钥（免费：100 小时浏览器使用时长）处获取您的 API 密钥。  
请将 Steel API 密钥设置到 OpenClaw 的配置文件或环境中：  
```bash
openclaw config set env.STEEL_API_KEY "your_key"
```

## 状态管理  

- `start_session.sh` 将会话 ID 保存到 `~/.steel_state` 文件中。  
- 所有脚本都会自动从该文件中加载会话信息。  
- 可通过 `export STEEL_SESSION_ID=<id>` 来覆盖当前会话 ID。  
- 会话会一直持续，直到执行 `release_session.sh` 或达到超时时间。

## 脚本  

| 脚本 | 用途 | 描述 |
|---|---|---|
| `start_session.sh` | `[--proxy] [--captcha] [--timeout MS]` | 创建会话；打印会话 ID 和浏览器地址（VIEWER_URL） |
| `release_session.sh` | `[SESSION_ID]` | 释放会话 |
| `list_sessions.sh` | _（无）_ | 列出所有活动的会话 |
| `navigate.sh` | `URL [--wait-until-networkidle]` | 导航到指定 URL |
| `screenshot.sh` | `[OUTPUT.png] [--full-page]` | 截取全页截图 |
| `click.sh` | `SELECTOR` | 根据 CSS、文本或 aria 选择器进行点击 |
| `click_coords.sh` | `X Y [--right] [--double]` | 在指定像素坐标处点击（备用方法） |
| `type.sh` | `SELECTOR "text"` | 在输入框中输入文本 |
| `press_key.sh` | `KEY` | 按下指定键（例如 Enter、Control+a） |
| `scroll.sh` | `AMOUNT\|--to-bottom\|--to-top\|SELECTOR` | 滚动页面 |
| `hover.sh` | `SELECTOR` | 将鼠标悬停在元素上 |
| `select.sh` | `SELECTOR VALUE` | 从下拉菜单中选择选项 |
| `get_content.sh` | `[--html] [SELECTOR]` | 提取页面文本或 HTML 内容 |
| `eval_js.sh` | `"js expression"` | 执行 JavaScript 代码并打印结果 |
| `wait_for.sh` | `SELECTOR [TIMEOUT_MS]` | 等待指定元素出现 |
| `get_url.sh` | _（无）_ | 打印当前 URL 和页面标题 |

## 选择器示例  

Steel 使用 Playwright 的选择器，其功能比基于像素坐标的选择器强大得多：  
```bash
# By CSS
click.sh "#submit-button"
click.sh ".nav-link:first-child"

# By text content
click.sh "text=Sign in"
click.sh "button:has-text('Continue')"

# By aria label
click.sh "[aria-label='Search']"
click.sh "[placeholder='Email address']"

# XPath
click.sh "xpath=//button[@type='submit']"
```

## 浏览器代理使用模式  

```bash
SCRIPTS="skills/steel-browser/scripts"

# 1. Start session (add --proxy --captcha for tough sites)
source <($SCRIPTS/start_session.sh)
echo "Session: $SESSION_ID"
echo "Watch at: $VIEWER_URL"

# 2. Navigate
$SCRIPTS/navigate.sh "https://example.com"

# 3. Agent loop
while true; do
  $SCRIPTS/screenshot.sh /tmp/screen.png
  
  # Get page text for LLM context
  CONTENT=$($SCRIPTS/get_content.sh)
  
  # LLM decides action...
  ACTION=$(echo "$CONTENT" | llm_decide /tmp/screen.png)
  
  case "$ACTION_TYPE" in
    click)    $SCRIPTS/click.sh "$SELECTOR" ;;
    type)     $SCRIPTS/type.sh "$SELECTOR" "$TEXT" ;;
    navigate) $SCRIPTS/navigate.sh "$URL" ;;
    done)     break ;;
  esac
done

# 4. Release
$SCRIPTS/release_session.sh
```

## 与 E2B Desktop 的对比  

| 功能 | Steel Browser | E2B Desktop |
|---|---|---|
| 选择器支持 | Playwright 的 CSS、文本和 aria 选择器 | 仅支持基于像素坐标的选择器 |
| 代理支持 | 支持住宅用代理 | 不支持 |
| CAPTCHA 解决方案 | 内置支持 | 不支持 |
| 非浏览器任务 | 不支持 | 支持桌面应用程序和终端操作 |
| 会话查看器 | 支持实时查看会话信息 | 支持通过 VNC 流传输会话画面 |

**Steel** 适用于网页自动化任务；**E2B Desktop** 适用于桌面应用程序或对整个操作系统的控制。
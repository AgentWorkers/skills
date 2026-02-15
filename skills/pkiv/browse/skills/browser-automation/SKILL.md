---
name: browserbase-browser-automation
description: 使用 stagehand CLI 为 AI 代理自动化网页浏览器操作
---

# 浏览器自动化技能

使用 `stagehand` CLI 为 AI 代理自动化浏览器操作。

**🚨 重要提示 - 请先阅读此内容 🚨**

系统已为您预先创建了一个包含隐身模式、代理和验证码功能的 Browserbase 会话。

**您必须对每个命令都使用 `stagehand --ws $BROWSERBASE_CONNECT_URL`。**

**切勿在没有 `--ws` 的情况下使用 `stagehand open`——否则会启动本地浏览器！**

## 使用场景

当用户需要执行以下操作时，可以使用此技能：
- 浏览网站或导航到指定 URL
- 从网页中提取数据
- 填写表单或点击按钮
- 截取网页截图
- 与网页应用程序交互
- 自动化多步骤的网页工作流程

## 核心概念

`stagehand` CLI 提供以下功能：
- **元素引用**：通过 `snapshot` 命令生成引用（例如 `@0-5`），便于点击或填写表单
- **Browserbase 支持**：通过 `--ws` 选项连接到预先创建的云浏览器会话

## 环境设置

**重要提示：系统已为您预先创建了一个包含隐身模式、代理和验证码功能的 Browserbase 会话。**

会话的 URL 存在于 `BROWSERBASE_CONNECT_URL` 环境变量中。

**您必须对每个命令都使用 `stagehand --ws $BROWSERBASE_CONNECT_URL`：**

```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
```

**原因：**
- ✅ 浏览器在 Browserbase 云环境中运行（而非本地）
- ✅ 启用了高级隐身模式（可绕过 Cloudflare）
- ✅ 启用了住宅代理
- ✅ 启用了验证码识别功能
- ✅ 会话记录保存在 `$BROWSERBASE_DEBUG_URL` 地址

**如果您忘记使用 `--ws $BROWSERBASE_CONNECT_URL`：**
- ❌ 将启动本地 Chrome 浏览器
- ❌ 无法使用隐身模式/代理/验证码功能
- ❌ 会导致评估失败

## 快速入门工作流程

```bash
# 1. Navigate to page (connects to pre-created Browserbase session)
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com

# 2. Get page structure with element refs
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c

# Output includes refs like [0-5], [1-2]:
# RootWebArea "Example" url="https://example.com"
#   [0-0] link "Home"
#   [0-1] link "About"
#   [0-2] button "Sign In"

# 3. Interact using refs
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-2
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-5 "search query"

# 4. Re-snapshot to verify changes
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c

# 5. Stop when done (optional, session persists)
stagehand --ws $BROWSERBASE_CONNECT_URL stop
```

## 导航命令

**请记住：** 对以下所有命令都使用 `stagehand --ws $BROWSERBASE_CONNECT_URL`。

```bash
# Navigate to URL
stagehand --ws $BROWSERBASE_CONNECT_URL open <url>

# With custom timeout for slow pages
stagehand --ws $BROWSERBASE_CONNECT_URL open <url> --timeout 60000

# Page navigation
stagehand --ws $BROWSERBASE_CONNECT_URL reload
stagehand --ws $BROWSERBASE_CONNECT_URL back
stagehand --ws $BROWSERBASE_CONNECT_URL forward
```

## 元素交互

### 获取页面结构

```bash
# Get accessibility tree with element refs
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c

# Get full snapshot with XPath/CSS mappings
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot --json
```

### 点击元素

```bash
# Click by ref (from snapshot)
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-5
stagehand --ws $BROWSERBASE_CONNECT_URL click 0-5       # @ prefix optional

# Click with options
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-5 -b right -c 2  # Right-click twice

# Click at coordinates
stagehand --ws $BROWSERBASE_CONNECT_URL click_xy 100 200
```

### 填写表单

```bash
# Fill input (auto-presses Enter by default)
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-5 "my value"

# Fill without pressing Enter
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-5 "my value" --no-press-enter

# Select dropdown options
stagehand --ws $BROWSERBASE_CONNECT_URL select @0-8 "Option 1" "Option 2"
```

### 输入文本

```bash
# Type text naturally
stagehand --ws $BROWSERBASE_CONNECT_URL type "Hello, world!"

# Type with delay between characters
stagehand --ws $BROWSERBASE_CONNECT_URL type "slow typing" -d 100

# Press special keys
stagehand --ws $BROWSERBASE_CONNECT_URL press Enter
stagehand --ws $BROWSERBASE_CONNECT_URL press Tab
stagehand --ws $BROWSERBASE_CONNECT_URL press "Cmd+A"
```

## 数据提取

```bash
# Get page info
stagehand --ws $BROWSERBASE_CONNECT_URL get url
stagehand --ws $BROWSERBASE_CONNECT_URL get title
stagehand --ws $BROWSERBASE_CONNECT_URL get text body
stagehand --ws $BROWSERBASE_CONNECT_URL get html @0-5

# Take screenshot
stagehand --ws $BROWSERBASE_CONNECT_URL screenshot page.png
stagehand --ws $BROWSERBASE_CONNECT_URL screenshot -f        # Full page
stagehand --ws $BROWSERBASE_CONNECT_URL screenshot --type jpeg

# Get element coordinates
stagehand --ws $BROWSERBASE_CONNECT_URL get box @0-5  # Returns center x,y
```

## 等待操作完成

```bash
# Wait for page load
stagehand --ws $BROWSERBASE_CONNECT_URL wait load
stagehand --ws $BROWSERBASE_CONNECT_URL wait load networkidle

# Wait for element
stagehand --ws $BROWSERBASE_CONNECT_URL wait selector ".my-class"
stagehand --ws $BROWSERBASE_CONNECT_URL wait selector ".my-class" -t 10000 -s visible

# Wait for time
stagehand --ws $BROWSERBASE_CONNECT_URL wait timeout 2000
```

## 多标签页支持

```bash
# List all tabs
stagehand --ws $BROWSERBASE_CONNECT_URL pages

# Open new tab
stagehand --ws $BROWSERBASE_CONNECT_URL newpage https://example.com

# Switch tabs
stagehand --ws $BROWSERBASE_CONNECT_URL tab_switch 1

# Close tab
stagehand --ws $BROWSERBASE_CONNECT_URL tab_close 2
```

## 网络请求捕获

捕获 HTTP 请求以供检查：

```bash
# Start capturing
stagehand --ws $BROWSERBASE_CONNECT_URL network on

# Get capture directory
stagehand --ws $BROWSERBASE_CONNECT_URL network path

# Stop capturing
stagehand --ws $BROWSERBASE_CONNECT_URL network off

# Clear captures
stagehand --ws $BROWSERBASE_CONNECT_URL network clear
```

捕获的请求会被保存为包含 `request.json` 和 `response.json` 文件的目录。

## 守护进程控制

```bash
# Check status
stagehand --ws $BROWSERBASE_CONNECT_URL status

# Stop browser
stagehand --ws $BROWSERBASE_CONNECT_URL stop

# Force stop
stagehand --ws $BROWSERBASE_CONNECT_URL stop --force
```

## 元素引用

执行 `snapshot` 命令后，元素会生成相应的引用，您可以如下使用这些引用：

```
RootWebArea "Login Page"
  [0-0] heading "Welcome"
  [0-1] textbox "Email" name="email"
  [0-2] textbox "Password" name="password"
  [0-3] button "Sign In"
```

**直接使用引用示例：**

```bash
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-1 "user@example.com"
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-2 "mypassword"
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-3
```

## 最佳实践

### 1. 导航后务必执行 snapshot 操作
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c  # Get refs
```

### 执行可能改变页面内容的操作后重新执行 snapshot
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-5
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c  # Get new state
```

### 尽量使用引用而非选择器
```bash
# ✅ Good: Use refs from snapshot
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-5

# ❌ Avoid: Manual selectors (refs are more reliable)
stagehand --ws $BROWSERBASE_CONNECT_URL click "#submit-button"
```

### 在需要时等待元素出现
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://slow-site.com
stagehand --ws $BROWSERBASE_CONNECT_URL wait selector ".content" -s visible
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c
```

### 始终使用 `--ws $BROWSERBASE_CONNECT_URL`
```bash
# ✅ Correct: Remote browser (connects to pre-created Browserbase session)
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com

# ❌ Wrong: Local browser (will fail in evals, launches Chrome locally)
stagehand open https://example.com
```

## 常见使用场景

### 登录流程
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com/login
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c
# [0-5] textbox "Email"
# [0-6] textbox "Password"
# [0-7] button "Sign In"
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-5 "user@example.com"
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-6 "password123"
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-7
stagehand --ws $BROWSERBASE_CONNECT_URL wait load
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c  # Verify logged in
```

### 搜索和数据提取
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c
# [0-3] textbox "Search"
stagehand --ws $BROWSERBASE_CONNECT_URL fill @0-3 "my query"
stagehand --ws $BROWSERBASE_CONNECT_URL wait selector ".results"
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c
# [1-0] text "Result 1"
# [1-1] text "Result 2"
stagehand --ws $BROWSERBASE_CONNECT_URL get text @1-0
stagehand --ws $BROWSERBASE_CONNECT_URL get text @1-1
```

### 多页面导航
```bash
stagehand --ws $BROWSERBASE_CONNECT_URL open https://example.com
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c
# [0-5] link "Next Page"
stagehand --ws $BROWSERBASE_CONNECT_URL click @0-5
stagehand --ws $BROWSERBASE_CONNECT_URL wait load
stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c  # Get new page structure
```

## 故障排除

### 浏览器无法启动
- 检查 `stagehand` 是否已安装：`which stagehand`
- 查看状态：`stagehand --ws $BROWSERBASE_CONNECT_URL status`
- 强制停止并重试：`stagehand --ws $BROWSERBASE_CONNECT_URL stop`

### 元素未找到
- 执行 snapshot 操作以验证引用是否正确：`stagehand --ws $BROWSERBASE_CONNECT_URL snapshot -c`
- 等待元素出现：`stagehand --ws $BROWSERBASE_CONNECT_URL wait selector ...`
- 检查页面更新后引用是否发生变化

### 页面无法加载
- 增加超时时间：`stagehand --ws $BROWSERBASE_CONNECT_URL open <url> --timeout 60000`
- 等待页面加载完成：`stagehand --ws $BROWSERBASE_CONNECT_URL wait load networkidle`

### 命令执行失败（提示“session not found”）
- 守护进程会自动从崩溃中恢复
- 如果问题依旧存在：`stagehand --ws $BROWSERBASE_CONNECT_URL stop --force && stagehand --ws $BROWSERBASE_CONNECT_URL open <url>`

## 性能优化建议

1. **使用压缩后的 snapshot（`-c`）以加快解析速度**
2. **策略性地等待**——仅在需要时才进行等待
3. **操作完成后关闭浏览器以释放资源**
4. **优先使用引用而非选择器**——这样更快且更可靠

## 重要注意事项

- 浏览器状态在命令执行之间会保持不变（例如 cookies、引用等）
- 如果页面发生重大变化，引用会失效
- 导航或 DOM 发生重大更改后务必重新生成 snapshot
- 守护进程会在首次命令执行时自动启动
- 可通过 `--session` 标志或 `BROWSE_SESSION` 环境变量支持多个会话
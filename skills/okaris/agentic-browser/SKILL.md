---
name: agent-browser
description: |
  Browser automation for AI agents via inference.sh.
  Navigate web pages, interact with elements using @e refs, take screenshots, record video.
  Capabilities: web scraping, form filling, clicking, typing, drag-drop, file upload, JavaScript execution.
  Use for: web automation, data extraction, testing, agent browsing, research.
  Triggers: browser, web automation, scrape, navigate, click, fill form, screenshot,
  browse web, playwright, headless browser, web agent, surf internet, record video
allowed-tools: Bash(infsh *)
---

# Agentic Browser

![Agentic Browser](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgjw8atdxgkrsr8a2t5peq7b.jpeg)

这是一个用于AI代理的浏览器自动化工具，通过 [inference.sh](https://inference.sh) 提供支持。该工具内部使用了 Playwright 库，并通过简单的 `@e` 引用系统来实现与网页元素的交互。

## 快速入门

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Open a page and get interactive elements
infsh app run agent-browser --function open --input '{"url": "https://example.com"}' --session new
```

## 核心工作流程

所有浏览器自动化操作都遵循以下步骤：

1. **打开页面** - 导航到指定 URL，并获取页面元素的 `@e` 引用。
2. **与元素交互** - 使用 `@e` 引用来执行点击、输入文本、拖拽等操作。
3. **重新获取页面状态** - 在页面内容发生变化后，重新获取元素的 `@e` 引用。
4. **关闭会话** - 结束当前会话（如果启用了视频录制，会返回录制视频）。

```bash
# 1. Start session
RESULT=$(infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com/login"
}')
SESSION_ID=$(echo $RESULT | jq -r '.session_id')
# Elements: @e1 [input] "Email", @e2 [input] "Password", @e3 [button] "Sign In"

# 2. Fill and submit
infsh app run agent-browser --function interact --session $SESSION_ID --input '{
  "action": "fill", "ref": "@e1", "text": "user@example.com"
}'
infsh app run agent-browser --function interact --session $SESSION_ID --input '{
  "action": "fill", "ref": "@e2", "text": "password123"
}'
infsh app run agent-browser --function interact --session $SESSION_ID --input '{
  "action": "click", "ref": "@e3"
}'

# 3. Re-snapshot after navigation
infsh app run agent-browser --function snapshot --session $SESSION_ID --input '{}'

# 4. Close when done
infsh app run agent-browser --function close --session $SESSION_ID --input '{}'
```

## 主要功能

| 功能 | 描述 |
|---------|---------|
| `open`   | 导航到指定 URL，并配置浏览器设置（如视口、代理设置、视频录制等）。|
| `snapshot` | 在 DOM 发生变化后，重新获取页面元素的 `@e` 引用。|
| `interact` | 使用 `@e` 引用来执行各种操作（如点击、输入文本、拖拽等）。|
| `screenshot` | 截取页面截图（包括视口或整个页面）。|
| `execute` | 在页面上运行 JavaScript 代码。|
| `close` | 关闭会话；如果启用了视频录制，会返回录制视频。|

## 交互操作

| 操作        | 描述                                      | 必需参数                          |
|-------------|-----------------------------------------|-----------------------------------|
| `click`      | 点击元素                                      | 需要点击的元素引用 (`ref`)                    |
| `dblclick`    | 双击元素                                      | 需要双击的元素引用 (`ref`)                    |
| `fill`      | 清空并输入文本                                   | 需要输入的文本 (`text`)                     |
| `type`      | 输入文本                                      | 需要输入的文本 (`text`)                     |
| `press`      | 按下按键（如 Enter、Tab 等）                        | 需要按下的按键 (`text`)                     |
| `select`      | 选择下拉菜单选项                             | 需要选择的选项引用 (`ref`)                    |
| `hover`      | 将鼠标悬停在元素上                                  | 需要悬停的元素引用 (`ref`)                    |
| `check`      | 勾选复选框                                    | 需要勾选的复选框引用 (`ref`)                    |
| `uncheck`     | 取消勾选复选框                                    | 需要取消勾选的复选框引用 (`ref`)                    |
| `drag`      | 拖拽元素                                      | 需要拖动的元素引用 (`ref`)                    | 需要拖放的目标元素引用 (`target_ref`)                |
| `upload`     | 上传文件                                      | 需要上传的文件引用 (`ref`)                    | 需要上传的文件路径 (`file_paths`)                |
| `scroll`      | 滚动页面                                      | 滚动方向（上/下/左/右）和滚动距离 (`scroll_amount`)         |
| `back`      | 返回上一页                                    | -                                      |
| `wait`      | 等待指定毫秒数                                  | 需要等待的时间 (`wait_ms`)                     |
| `goto`      | 导航到指定 URL                                    | 需要导航的 URL                          |

## 元素引用

页面元素通过 `@e` 引用来标识：

```
@e1 [a] "Home" href="/"
@e2 [input type="text"] placeholder="Search"
@e3 [button] "Submit"
@e4 [select] "Choose option"
@e5 [input type="checkbox"] name="agree"
```

**重要提示：**  
引用在页面导航后可能会失效。在以下情况下务必重新获取元素引用：  
- 点击链接或按钮导致页面跳转时；  
- 表单提交后；  
- 动态内容加载完成后。

## 特性

### 视频录制

支持录制浏览器会话，便于调试或生成文档：

```bash
# Start with recording enabled (optionally show cursor indicator)
SESSION=$(infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "record_video": true,
  "show_cursor": true
}' | jq -r '.session_id')

# ... perform actions ...

# Close to get the video file
infsh app run agent-browser --function close --session $SESSION --input '{}'
# Returns: {"success": true, "video": <File>}
```

### 光标指示器

在截图和视频中显示可见的光标（对演示非常有用）：

```bash
infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "show_cursor": true,
  "record_video": true
}'
```

光标会以红色圆点的形式显示，并跟随鼠标移动，同时提供点击反馈。

### 代理支持

允许通过代理服务器转发网络请求：

```bash
infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "proxy_url": "http://proxy.example.com:8080",
  "proxy_username": "user",
  "proxy_password": "pass"
}'
```

### 文件上传

支持将文件上传到指定的文件输入框：

```bash
infsh app run agent-browser --function interact --session $SESSION --input '{
  "action": "upload",
  "ref": "@e5",
  "file_paths": ["/path/to/file.pdf"]
}'
```

### 拖拽操作

支持将元素拖放到目标位置：

```bash
infsh app run agent-browser --function interact --session $SESSION --input '{
  "action": "drag",
  "ref": "@e1",
  "target_ref": "@e2"
}'
```

### JavaScript 执行

允许在页面上运行自定义 JavaScript 代码：

```bash
infsh app run agent-browser --function execute --session $SESSION --input '{
  "code": "document.querySelectorAll(\"h2\").length"
}'
# Returns: {"result": "5", "screenshot": <File>}
```

## 详细文档

- [references/commands.md](references/commands.md)：包含所有功能的详细参考信息及选项说明。  
- [references/snapshot-refs.md](references/snapshot-refs.md)：介绍引用的生命周期、失效规则及故障排除方法。  
- [references/session-management.md](references/session-management.md)：讲解会话管理机制及多会话处理方式。  
- [references/authentication.md](references/authentication.md)：介绍登录流程、OAuth 认证及双因素认证（2FA）的实现方式。  
- [references/video-recording.md](references/video-recording.md)：提供视频录制的相关功能及使用方法。  
- [references/proxy-support.md](references/proxy-support.md)：介绍代理服务器的配置方法及地理测试相关内容。

## 可用的模板

- [templates/form-automation.sh](templates/form-automation.sh)：包含带有验证功能的表单自动化模板。  
- [templates/authenticated-session.sh](templates/authenticated-session.sh)：支持登录一次后重复使用会话的功能。  
- [templates/capture-workflow.sh](templates/capture-workflow.sh)：用于提取内容并生成截图的模板。

## 示例

- [examples/form-submission.md](examples/form-submission.md)：演示如何提交表单。  
- [examples/search-and-extract.md](examples/search-and-extract.md)：演示如何搜索和提取信息。  
- [examples/screenshot-with-video.md](examples/screenshot-with-video.md)：演示如何截取包含视频的页面截图。  

## 会话管理

浏览器会话的状态会在会话期间持续保存。使用方法如下：  
1. 首次调用时使用 `--session new` 参数创建新会话。  
2. 后续调用时使用返回的 `session_id` 识别当前会话。  
3. 操作完成后关闭会话。  

## 相关技能

- [inference.sh Sessions](https://inference.sh/docs/extend/sessions)：了解会话管理的相关知识。  
- [inference.sh Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps)：了解工具中的多功能组件的工作原理。
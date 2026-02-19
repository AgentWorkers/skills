---
name: agent-browser
description: "通过 `inference.sh` 实现 AI 代理的浏览器自动化功能：可以导航网页、使用 `@e refs` 与页面元素交互、截图以及录制视频。具备以下能力：网页抓取、表单填写、点击操作、文本输入、拖放、文件上传以及 JavaScript 执行。适用于：网页自动化、数据提取、测试、代理浏览、研究等场景。触发条件包括：浏览器操作、网页自动化任务、抓取操作、导航、点击、表单填写、截图、网页浏览等。相关工具/技术包括：无头浏览器（headless browser）、Web 代理（web agent）、互联网浏览（surf the internet）、视频录制（record video）。"
allowed-tools: Bash(infsh *)
---
# **Agentic Browser**

这是一个用于AI代理的浏览器自动化工具，通过[inference.sh](https://inference.sh)实现。该工具内部使用了Playwright框架，并通过简单的`@e`引用系统来操作网页元素。

![Agentic Browser](https://cloud.inference.sh/app/files/u/4mg21r6ta37mpaz6ktzwtt8krr/01kgjw8atdxgkrsr8a2t5peq7b.jpeg)

## **快速入门**

```bash
# Install CLI
curl -fsSL https://cli.inference.sh | sh && infsh login

# Open a page and get interactive elements
infsh app run agent-browser --function open --input '{"url": "https://example.com"}' --session new
```

> **安装说明：** [安装脚本](https://cli.inference.sh) 仅会检测您的操作系统和架构，然后从`dist.inference.sh`下载相应的二进制文件并验证其SHA-256校验和。无需特殊权限或后台进程。也可以选择[手动安装并验证](https://dist.inference.sh/cli/checksums.txt)。

## **核心工作流程**

所有的浏览器自动化操作都遵循以下步骤：
1. **打开**：导航到指定URL，并获取页面元素的`@e`引用。
2. **交互**：使用`@e`引用执行点击、输入、拖拽等操作。
3. **重新抓取页面状态**：在页面内容发生变化后，重新获取元素的`@e`引用。
4. **关闭**：结束会话（如果开启了视频录制，会返回录制结果）。

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

## **常用功能**

| 功能          | 描述                                      |
|------------------|-----------------------------------------|
| `open`        | 导航到指定URL，并配置浏览器设置（如视口、代理设置、视频录制等）        |
| `snapshot`     | 在DOM内容发生变化后，重新获取页面元素的`@e`引用         |
| `interact`      | 使用`@e`引用执行各种交互操作（如点击、输入等）           |
| `screenshot`    | 截取页面截图（包括视口或整个页面）                   |
| `execute`     | 在页面上运行JavaScript代码                         |
| `close`       | 关闭会话；如果开启了录制功能，会返回录制视频             |

## **交互操作**

| 操作            | 描述                                      | 必需参数                                      |
|------------------|-----------------------------------------|
| `click`         | 点击指定元素                              | `ref`                                        |
| `dblclick`        | 双击指定元素                              | `ref`                                        |
| `fill`          | 清空并输入文本                              | `ref`, `text`                                    |
| `type`          | 输入文本（不清除原有内容）                          | `text`                                        |
| `press`         | 按下指定按键（如Enter、Tab等）                        | `text`                                        |
| `select`         | 从下拉菜单中选择选项                          | `ref`, `text`                                    |
| `hover`         | 将鼠标悬停在指定元素上                         | `ref`                                        |
| `check`         | 勾选/取消勾选复选框                           | `ref`                                        |
| `uncheck`        | 取消勾选复选框                             | `ref`                                        |
| `drag`          | 拖拽元素到目标位置                            | `ref`, `target_ref`                                |
| `upload`         | 上传文件                                   | `ref`, `file_paths`                                |
| `scroll`        | 滚动页面                                 | `direction` (上/下/左/右), `scroll_amount`                |
| `back`          | 在浏览器历史记录中后退                         | -                                           |
| `wait`          | 等待指定毫秒数                              | `wait_ms`                                      |
| `goto`         | 导航到指定URL                               | `url`                                        |

## **元素引用**

页面元素通过`@e`引用进行标识：

```
@e1 [a] "Home" href="/"
@e2 [input type="text"] placeholder="Search"
@e3 [button] "Submit"
@e4 [select] "Choose option"
@e5 [input type="checkbox"] name="agree"
```

**重要提示：**  
- 在执行以下操作后，元素引用会失效：  
  - 点击链接或按钮导致页面跳转  
  - 提交表单  
  - 动态内容加载  

## **附加功能**

### **视频录制**

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

### **光标显示**

在截图和视频中显示可见的光标（对演示非常有用）：

```bash
infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "show_cursor": true,
  "record_video": true
}'
```

光标会以红色圆点的形式显示，并跟随鼠标移动，同时提供点击反馈。

### **代理支持**

允许通过代理服务器转发网络请求：

```bash
infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "proxy_url": "http://proxy.example.com:8080",
  "proxy_username": "user",
  "proxy_password": "pass"
}'
```

### **文件上传**

支持将文件上传到指定的文件输入框：

```bash
infsh app run agent-browser --function interact --session $SESSION --input '{
  "action": "upload",
  "ref": "@e5",
  "file_paths": ["/path/to/file.pdf"]
}'
```

### **拖拽操作**

支持将元素拖拽到目标位置：

```bash
infsh app run agent-browser --function interact --session $SESSION --input '{
  "action": "drag",
  "ref": "@e1",
  "target_ref": "@e2"
}'
```

### **JavaScript执行**

允许在页面上运行自定义JavaScript代码：

```bash
infsh app run agent-browser --function execute --session $SESSION --input '{
  "code": "document.querySelectorAll(\"h2\").length"
}'
# Returns: {"result": "5", "screenshot": <File>}
```

## **详细文档**

- [references/commands.md](references/commands.md)：包含所有功能的详细参考信息及选项说明。
- [references/snapshot-refs.md](references/snapshot-refs.md)：介绍引用的生命周期、失效规则及故障排除方法。
- [references/session-management.md](references/session-management.md)：讲解会话管理机制及多会话处理方式。
- [references/authentication.md](references/authentication.md)：介绍登录流程、OAuth认证及双因素认证（2FA）的实现。
- [references/video-recording.md](references/video-recording.md)：提供视频录制的相关信息及使用方法。
- [references/proxy-support.md](references/proxy-support.md)：代理配置及地理测试相关内容。

## **现成的模板**

- [templates/form-automation.sh](templates/form-automation.sh)：包含带有验证功能的表单自动化脚本。
- [templates/authenticated-session.sh](templates/authenticated-session.sh)：登录一次后，可重复使用会话。
- [templates/capture-workflow.sh](templates/capture-workflow.sh)：用于提取内容并生成截图的脚本。

## **示例**

- **表单提交**：[示例代码](```bash
SESSION=$(infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com/contact"
}' | jq -r '.session_id')

# Get elements: @e1 [input] "Name", @e2 [input] "Email", @e3 [textarea], @e4 [button] "Send"

infsh app run agent-browser --function interact --session $SESSION --input '{"action": "fill", "ref": "@e1", "text": "John Doe"}'
infsh app run agent-browser --function interact --session $SESSION --input '{"action": "fill", "ref": "@e2", "text": "john@example.com"}'
infsh app run agent-browser --function interact --session $SESSION --input '{"action": "fill", "ref": "@e3", "text": "Hello!"}'
infsh app run agent-browser --function interact --session $SESSION --input '{"action": "click", "ref": "@e4"}'

infsh app run agent-browser --function snapshot --session $SESSION --input '{}'
infsh app run agent-browser --function close --session $SESSION --input '{}'
```)
- **搜索与数据提取**：[示例代码](```bash
SESSION=$(infsh app run agent-browser --function open --session new --input '{
  "url": "https://google.com"
}' | jq -r '.session_id')

infsh app run agent-browser --function interact --session $SESSION --input '{"action": "fill", "ref": "@e1", "text": "weather today"}'
infsh app run agent-browser --function interact --session $SESSION --input '{"action": "press", "text": "Enter"}'
infsh app run agent-browser --function interact --session $SESSION --input '{"action": "wait", "wait_ms": 2000}'

infsh app run agent-browser --function snapshot --session $SESSION --input '{}'
infsh app run agent-browser --function close --session $SESSION --input '{}'
```)
- **截图与视频同步**：[示例代码](```bash
SESSION=$(infsh app run agent-browser --function open --session new --input '{
  "url": "https://example.com",
  "record_video": true
}' | jq -r '.session_id')

# Take full page screenshot
infsh app run agent-browser --function screenshot --session $SESSION --input '{
  "full_page": true
}'

# Close and get video
RESULT=$(infsh app run agent-browser --function close --session $SESSION --input '{}')
echo $RESULT | jq '.video'
```)

## **会话管理**

浏览器状态会在会话期间保持。请注意：
- 首次调用时使用`--session new`参数创建新会话。
- 后续调用时使用返回的`session_id`来识别当前会话。
- 完成操作后请关闭会话。

## **相关技能**

- [inference.sh Sessions](https://inference.sh/docs/extend/sessions)：会话管理相关文档。
- [Multi-function Apps](https://inference.sh/docs/extend/multi-function-apps)：了解各功能的详细工作原理。
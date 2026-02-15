---
name: stealthy-auto-browse
description: 浏览器自动化工具，能够通过 CreepJS、BrowserScan、Pixelscan 和 Cloudflare 进行数据采集；同时确保零 CDP（Content Delivery Network）暴露风险，支持操作系统级别的输入操作，并生成持久的用户指纹数据。适用于那些使用标准浏览器方法无法获取数据（例如遇到 403 错误或需要输入验证码的情况）。
homepage: https://github.com/psyb0t/docker-stealthy-auto-browse
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🕵️", "primaryEnv": "STEALTHY_AUTO_BROWSE_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# 隐形自动浏览（Stealthy Auto-Browse）

这是一个在Docker中运行的隐形浏览器。它使用Camoufox（一个定制的Firefox分支）代替Chromium，因此不存在任何可供机器人检测工具识别的Chrome DevTools Protocol（CDP）信号。鼠标和键盘输入通过PyAutoGUI在操作系统层面进行——浏览器本身并不知道自己被自动化了，这意味着行为分析也无法检测到这一点。

## 该技能存在的理由

标准的浏览器自动化工具（如Playwright + Chromium、Puppeteer、Selenium）会暴露CDP信号，这些信号会被机器人检测服务（如Cloudflare、DataDome、PerimeterX、Akamai）立即捕获。即使使用了隐形插件，CDP协议仍然存在且可以被检测到。而这个技能通过使用Firefox（完全不使用CDP）并在操作系统层面生成输入事件，彻底消除了这一问题。

## 何时使用该技能

- 网站具有机器人检测机制（如Cloudflare的挑战页面、DataDome、PerimeterX、Akamai）
- 网站阻止无头浏览器或显示CAPTCHAs
- 需要一个不会被封禁的登录会话
- 其他浏览器技能遇到403错误或返回空内容/被阻止的响应
- 你正在抓取一个主动抵抗自动化的网站

## 何时不使用该技能

- 仅进行简单的数据获取且没有机器人防护需求——使用`curl`或`WebFetch`
- 网站不关心自动化——使用常规浏览器技能，设置起来更快
- 你只需要静态HTML内容——使用`curl`

## 设置

**1. 启动容器：**

```bash
docker run -d -p 8080:8080 -p 5900:5900 psyb0t/stealthy-auto-browse
```

端口8080是HTTP API端口。端口5900是一个无VNC的Web查看器，你可以通过它实时查看浏览器。

**2. 设置环境变量：**

```bash
export STEALTHY_AUTO_BROWSE_URL=http://localhost:8080
```

或者通过OpenClaw配置文件（`~/.openclaw/openclaw.json`）进行设置：

```json
{
  "skills": {
    "entries": {
      "stealthy-auto-browse": {
        "env": {
          "STEALTHY_AUTO_BROWSE_URL": "http://localhost:8080"
        }
      }
    }
  }
}
```

**3. 验证：**当浏览器准备好时，执行`curl $STEALTHY_AUTO_BROWSE_URL/health`应返回`ok`。

## 工作原理

容器运行一个虚拟X显示（Xvfb，分辨率为1920x1080）、Camoufox浏览器和一个HTTP API服务器。你向API发送JSON命令，并接收JSON响应。所有命令都以`{"action": "<name>", ...params}`的格式发送到`POST $STEALTHY_AUTO_BROWSE_URL/`。

每个响应的结构如下：

```json
{
  "success": true,
  "timestamp": 1234567890.123,
  "data": { ... },
  "error": "only present when success is false"
}
```

`data`字段的内容因命令而异——具体内容在下面为每个命令进行了说明。

## 了解两种输入模式

这是最重要的概念。有两种与页面交互的方式：

### 系统输入（无法被检测到）

- **动作**：`system_click`、`mouse_move`、`mouse_click`、`system_type`、`send_key`、`scroll`
  这些命令使用PyAutoGUI生成真实的操作系统级别的鼠标移动和按键操作。浏览器会将这些操作视为真实用户的操作——任何网站JavaScript都无法区分这些操作和人类操作。**用于实现隐形浏览。**

系统输入使用**视口坐标**（浏览器内容区域内的x, y像素位置）。这些坐标可以通过`get_interactive_elements`获取。

### Playwright输入（可被检测到）

- **动作**：`click`、`fill`、`type`
  这些命令使用Playwright的DOM自动化功能，通过CSS选择器或XPath与页面元素交互。它们更快且更可靠（不需要进行坐标计算），但会通过浏览器的自动化层注入事件。复杂的行为分析可能会检测到这些操作的模式。**当速度比隐形性更重要，或者你有选择器但没有坐标时使用这些方法。**

### 何时使用哪种方式

- **对隐形性要求高的网站**（如Cloudflare、登录表单、任何具有机器人检测功能的网站）：始终使用系统输入。
- **简单的数据抓取**，且网站没有主动抵抗自动化：使用Playwright输入更简单。
- **填写表单**：使用`system_click`聚焦输入框，然后使用`system_type`输入文本。这种方式无法被检测到。使用`fill`虽然更快，但可以被检测到。
- **点击按钮**：如果你有`get_interactive_elements`提供的坐标，使用`system_click`。如果没有坐标，使用`click`。

## 工作流程

与页面交互的典型步骤如下：

1. **导航**：使用`goto`加载URL。
2. **读取页面内容**：`get_text`返回所有可见文本——通常足以理解页面内容。
3. **如果文本不清楚**：使用`get_html`获取完整的DOM结构。
4. **如果仍然困惑**：截取屏幕截图（`GET /screenshot/browser?whLargest=512`）。
5. **查找可交互元素**：`get_interactive_elements`返回所有按钮、链接、输入框及其x, y坐标。
6. **交互**：使用`system_click`点击元素，`system_type`输入文本，`send_key`输入Enter/Tab/Escape键。
7. **等待结果**：使用`wait_for_element`或`wait_for_text`而不是简单地等待。
8. **验证**：再次使用`get_text`确认页面是否按预期改变了。

## 动作参考

### 导航

#### goto

导航到指定URL。这是加载页面的方式。

**参数：**
- `url`（必需）：要导航到的URL。
- `wait_until`（可选，默认为`"domcontentloaded"`）：判断页面是否加载完成的条件。可选选项包括`"domcontentloaded"`（DOM解析完成）、`"load"`（所有资源加载完成）、`"networkidle"`（500毫秒内无网络活动，最慢但最完整）。

**响应数据：`{"url": "https://example.com/", "title": "Example Domain"}`

**注意：**如果页面加载器与URL匹配（参见“页面加载器”部分），则会执行加载器的步骤而不是默认的导航逻辑。响应中会包含`"loader": "loader name"`。

#### refresh

重新加载当前页面。

**参数：**
- `wait_until`（可选，默认为`"domcontentloaded"`）：与`goto`相同。

**响应数据：`{"url": "https://example.com/current-page", "title": "Current Page"}`

### 系统输入（无法被检测到）

#### system_click

以类似人类的方式移动鼠标到视口坐标（带有随机抖动和缓动的加速度），然后点击。这是实现隐形点击的主要方法。

**参数：**
- `x`, `y`（必需）：视口坐标——通过`get_interactive_elements`获取。
- `duration`（可选）：鼠标移动的持续时间（以秒为单位）。如果省略，会使用0.2-0.6秒之间的随机值以模拟真实情况。

**响应数据：`{"system_clicked": {"x": 500, "y": 300}``

**与`mouse_click`的区别：**`system_click`总是先移动鼠标（平滑的路径），然后再点击。`mouse_click`可以立即点击某个位置，无需先移动鼠标。

#### mouse_move

以类似人类的方式移动鼠标到视口坐标（带有抖动和缓动的曲线），但不会点击。用于悬停元素（触发悬停菜单或工具提示），或在操作之间模拟自然鼠标行为。

**参数：**
- `x`, `y`（必需）：视口坐标。
- `duration`（可选）：移动时间（以秒为单位）。如果省略，会使用0.2-0.6秒之间的随机值。

**响应数据：`{"moved_to": {"x": 500, "y": 300}``

#### mouse_click

在指定位置或鼠标当前位置点击。与`system_click`不同，`mouse_click`不会先移动鼠标。

**参数：**
- `x`, `y`（可选）：如果提供了坐标，则在指定位置点击；如果没有提供坐标，则在鼠标当前位置点击。

**响应数据：`{"clicked_at": {"x": 500, "y": 300}` 或 `{"clicked_at": "current"}`

**何时使用：**在`mouse_move`之后，当你希望将移动和点击分开进行时；或者当鼠标已经定位好，只需要点击时。

#### system_type

通过真实的操作系统按键逐个字符输入文本。每个按键都有随机延迟（在指定间隔内抖动），以模拟人类的输入速度。这种方式完全无法被检测到。

**参数：**
- `text`（必需）：要输入的文本。必须先使用`system_click`或`click`聚焦输入框。
- `interval`（可选，默认为`0.08`）：按键之间的基本延迟（以秒为单位）。

**响应数据：`{"typed_len": 11}`

**重要提示：**在使用`system_type`之前，必须先使用`system_click`或`click`聚焦输入框。

#### send_key

通过操作系统级别输入发送单个按键或按键组合。用于按下Enter键提交表单、使用Tab键在字段间切换、使用Escape键关闭对话框，或发送如Ctrl+A、Ctrl+C等按键组合。

**参数：**
- `key`（必需）：按键名称或按键组合（用`+`分隔）。按键名称遵循PyAutoGUI的命名规则：`enter`、`tab`、`escape`、`backspace`、`delete`、`up`、`down`、`left`、`right`、`home`、`end`、`pageup`、`pagedown`、`f1`-`f12`、`ctrl`、`alt`、`shift`、`space`等。

**响应数据：`{"send_key": "enter"}`

#### scroll

使用鼠标滚轮滚动页面。生成真实的操作系统级别的滚动事件。

**参数：**
- `amount`（可选，默认为`-3`）：滚动量。负值表示向下滚动，正值表示向上滚动。每个单位大约相当于一次鼠标滚轮的滚动距离。
- `x`, `y`（可选）：如果提供了这些参数，先移动鼠标到这些视口坐标，然后再滚动。适用于在特定可滚动元素内滚动，而不仅仅是整个页面。

**响应数据：`{"scrolled": -3}`

### Playwright输入（可被检测到）

这些方法更快更方便，但使用Playwright的DOM事件注入，因此可能被复杂的行为分析工具检测到。

#### click

通过CSS选择器或XPath点击元素。Playwright会在DOM中找到元素，如果需要的话会将其滚动到可见位置，然后触发点击事件。

**参数：**
- `selector`（必需）：CSS选择器或XPath（前缀为`xpath=`）。

**响应数据：`{"clicked": "#submit-btn"}`

**何时使用：**当你有选择器但不想费心获取坐标时；或者当元素可能会移动且坐标不可靠时；或者当隐形性不是关键因素时。

#### fill

通过选择器填充输入框。先清除现有内容，然后设置新值。这是填充表单最快的方法，但由于不生成单独的按键事件，因此可能被检测到。

**参数：**
- `selector`（必需）：输入框的CSS选择器或XPath。
- `value`（必需）：要输入的文本。

**响应数据：`{"filled": "input[name='email']"}`

#### type

通过Playwright逐个字符将文本输入到元素中（不通过操作系统）。每个按键都有可配置的延迟。这种方法介于`fill`（快速但明显是自动化的）和`system_type`（操作系统级别，无法被检测到）之间。输入模式比`fill`更真实，但仍然通过Playwright的事件系统传递。

**参数：**
- `selector`（必需）：元素的CSS选择器或XPath。
- `text`（必需）：要输入的文本。
- `delay`（可选，默认为`0.05`）：按键之间的延迟（以秒为单位）。

**响应数据：`{"typed": "#search"}`

### 截图

截图是通过GET请求获取的（不是POST操作）。

#### GET /screenshot/browser

捕获浏览器视口的PNG图像。这就是用户看到的页面内容。

**参数：**
- `whLargest=512`：将截图尺寸调整为512像素，保持纵横比。
- `width=800`：将截图宽度调整为800像素。
- `height=300`：将截图高度调整为300像素。
- `width=400&height=400`：强制截图尺寸为400x400像素。

#### GET /screenshot/desktop

使用`scrot`捕获整个虚拟桌面（包括窗口边框、任务栏等）。使用与上面相同的尺寸参数。当你需要查看浏览器视口之外的内容时很有用。

#### 页面检查

#### get_interactive_elements

扫描页面并返回所有可交互的元素（按钮、链接、输入框、选择框等）及其视口坐标。这是确定点击目标和位置的方法。

**参数：**
- `visible_only`（可选，默认为`true`）：仅返回当前屏幕上可见的元素。

**响应数据：**
```json
{
  "count": 5,
  "elements": [
    {
      "i": 0,
      "tag": "button",
      "id": "submit-btn",
      "text": "Submit",
      "selector": "#submit-btn",
      "x": 400,
      "y": 250,
      "w": 120,
      "h": 40,
      "visible": true
    },
    {
      "i": 1,
      "tag": "input",
      "id": null,
      "text": "",
      "selector": "input[name='email']",
      "x": 300,
      "y": 180,
      "w": 250,
      "h": 35,
      "visible": true
    }
  ]
}
```

`x`, `y`是元素的中心坐标——直接将这些坐标传递给`system_click`。`selector`可以与Playwright的`click`或`fill`等动作一起使用。`w`, `h`提供了元素的尺寸。

**这是了解页面上可交互内容的主要工具。**在点击任何元素之前，请先调用此函数。

#### get_text

返回页面主体中的所有可见文本内容。文本长度被截断为10,000个字符。

**响应数据：**`{"text": "Page title\nSome content here...", "length": 1234}`

这通常是导航后的第一个调用步骤——它可以在不截取屏幕截图的情况下告诉你页面上的内容。

#### get_html

返回当前页面的完整HTML源代码。

**响应数据：**`{"html": "<!DOCTYPE html>...", "length": 45678}`

当`get_text`无法提供足够的页面结构信息，或者你需要查找DOM中的特定元素时使用此方法。

#### eval

在页面上下文中执行任意JavaScript表达式，并返回结果。表达式通过`page.evaluate()`进行评估。

**参数：**
- `expression`（必需）：要评估的JavaScript表达式。必须返回一个可序列化为JSON的值。

**响应数据：`{"result": "Example Domain"}` — 表达式的返回结果。

### 等待条件

使用这些方法代替`sleep`来等待页面内容加载完成。它们更可靠，因为它们会等待特定的条件而不是任意时间。

#### wait_for_element

等待匹配CSS选择器或XPath的元素达到某种状态（可见、隐藏、附加到DOM中、从DOM中移除）。

**参数：**
- `selector`（必需）：CSS选择器或XPath（前缀为`xpath=`）。
- `state`（可选，默认为`"visible"`）：等待的状态。可选选项包括`"visible"`（已渲染且可见）、`hidden`（不可见）、`attached`（无论是否可见都存在于DOM中）、`detached`（从DOM中移除）。
- `timeout`（可选，默认为`30`）：最大等待时间（以秒为单位）。如果超过这个时间会抛出错误。

**响应数据：`{"selector": "#results", "state": "visible"}`

#### wait_for_text

等待页面主体中出现特定文本。

**参数：**
- `text`（必需）：要查找的文本（在`document.body.innerText`中进行子字符串匹配）。
- `timeout`（可选，默认为`30`）：最大等待时间（以秒为单位）。

**响应数据：`{"text": "Search results", "found": true}`

#### wait_for_url

等待页面URL匹配某个模式。在表单提交或重定向后很有用。

**参数：**
- `url`（必需）：要匹配的URL模式。支持`*`（除`/`之外的任何字符）和`**`（包括`/`的任何字符）通配符。也可以是一个完整的URL进行精确匹配。
- `timeout`（可选，默认为`30`）：最大等待时间（以秒为单位）。

**响应数据：`{"url": "https://example.com/dashboard"}`

#### wait_for_network_idle

等待500毫秒内没有网络请求。适用于那些在初始页面加载后动态加载内容的页面。

**参数：**
- `timeout`（可选，默认为`30`）：最大等待时间（以秒为单位）。

**响应数据：`{"idle": true}`

### 标签管理

浏览器可以同时打开多个标签页。每次只有一个标签页是“活动”的——所有操作都在活动标签页上执行。

#### list_tabs

返回所有打开的标签页及其URL，以及哪个标签页是活动标签页。

**参数：**
```json
{"action": "list_tabs"}
```

**响应数据：**
```json
{
  "count": 2,
  "tabs": [
    {"index": 0, "url": "https://example.com/", "active": false},
    {"index": 1, "url": "https://other.com/", "active": true}
  ]
}
```

#### new_tab

打开一个新的浏览器标签页。可以选择性地导航到某个URL。新标签页将成为活动标签页。

**参数：**
- `url`（可选）：新标签页要导航到的URL。
- `wait_until`（可选，默认为`"domcontentloaded"`）：与`goto`相同。

**响应数据：`{"index": 1, "url": "https://example.com/"}`

#### switch_tab

通过索引切换活动标签页。所有后续操作都将在该标签页上执行。

**参数：**
- `index`（必需）：标签页的索引。

**响应数据：**`{"index": 0, "url": "https://example.com/"}`

#### close_tab

关闭一个标签页。关闭后，最后一个标签页将成为活动标签页。

**参数：**
- `index`（可选）：要关闭的标签页的索引。如果省略，则关闭当前活动标签页。

**响应数据：**`{"closed": true, "remaining": 1}`

### 对话框处理

浏览器有模态对话框（如警告框、确认框、提示框）。默认情况下，对话框会自动关闭（点击“确定”）。如果需要关闭对话框或提供提示文本，请使用`handle_dialog`。

**参数：**
- `accept`（可选，默认为`true`）：`true`表示点击“确定”/“接受”，`false`表示点击“取消”/“关闭”。
- `text`（可选）：提示框的提示文本。对于警告框/确认框，此参数可以忽略。

**响应数据：**`{"configured": {"accept": true, "text": null}`

**示例——处理确认对话框：**
```bash
# Step 1: Tell the browser to accept the next dialog
curl -X POST $API -H 'Content-Type: application/json' -d '{"action": "handle_dialog", "accept": true}'
# Step 2: Now click the button that triggers the confirm
curl -X POST $API -H 'Content-Type: application/json' -d '{"action": "system_click", "x": 300, "y": 200}'
```

#### get_last_dialog

返回最近出现的对话框的信息。

**响应数据：**
```json
{"action": "get_last_dialog"}
```

**响应数据：**
```json
{
  "dialog": {
    "type": "confirm",
    "message": "Are you sure you want to delete this?",
    "default_value": "",
    "buttons": ["ok", "cancel"]
  }
}
```

如果没有对话框出现，`{"dialog": null}`。`type`字段的值可以是`"alert"`、`"confirm"`、`"prompt"`。

### Cookies

#### get_cookies

返回浏览器上下文中的所有Cookies，或者特定URL的Cookies。

**参数：**
- `urls`（可选）：用于过滤Cookies的URL数组。如果省略，将返回所有Cookies。

**响应数据：**
```json
{"action": "get_cookies"}
{"action": "get_cookies", "urls": ["https://example.com"]}
```

**参数：**
- `urls`（可选）：用于过滤Cookies的URL数组。

**响应数据：**
```json
{
  "count": 3,
  "cookies": [
    {"name": "session", "value": "abc123", "domain": ".example.com", "path": "/", "httpOnly": true, "secure": true, ...}
  ]
}
```

#### set_cookie

在浏览器上下文中设置一个Cookies。

**参数：**
- 任何标准的Cookies字段——`name`、`value`、`url`、`domain`、`httpOnly`、`secure`、`sameSite`、`expires`。至少需要提供`name`和`value`，以及`url`或`domain`中的一个。

**响应数据：**`{"set": "session"}`

#### delete_cookies

清除浏览器上下文中的所有Cookies。

**响应数据：**`{"cleared": true}`

### 存储

访问页面的localStorage和sessionStorage。这些存储是按来源区分的——你必须在正确的页面上才能访问这些存储内容。

#### get_storage

返回localStorage或sessionStorage中的所有项目，以键值对的形式。

**参数：**
- `type`（可选，默认为`"local"`）：`local`表示localStorage，`session`表示sessionStorage。

**响应数据：**`{"items": {"theme": "dark", "lang": "en"}, "type": "local"}`

#### set_storage

在localStorage或sessionStorage中设置一个键值对。

**参数：**
- `type`（可选，默认为`"local"`）：`local`表示localStorage，`session`表示sessionStorage。
- `key`（必需）：存储键。
- `value`（必需）：存储值（字符串）。

**响应数据：**`{"set": "theme", "type": "local"}`

#### clear_storage

清除localStorage或sessionStorage中的所有项目。

**响应数据：**`{"cleared": "local"}`

### 下载

浏览器会自动跟踪由页面交互（如点击下载链接、表单提交等）触发的文件下载。

#### get_last_download

返回最近下载的文件信息。

**参数：**
```json
{"action": "get_last_download"}
```

**响应数据：**
```json
{
  "download": {
    "url": "https://example.com/file.pdf",
    "filename": "file.pdf",
    "path": "/tmp/playwright-downloads/abc123/file.pdf"
  }
}
```

如果尚未下载任何文件，`{"download": null}`。`path`是文件在容器内的本地路径。`filename`是服务器建议的文件名称。

### 上传

**参数：**
- `selector`（必需）：`<input type="file">`元素的CSS选择器。
- `file_path`（必需）：容器内文件的绝对路径。

**响应数据：**`{"selector": "#file-input", "file": "document.pdf", "size": 12345}`

**注意：**设置文件后，仍需要点击提交按钮才能实际完成上传。

### 网络日志

捕获页面发出的所有HTTP请求和响应。这对于调试、查找页面调用的API端点或验证某些资源是否已加载非常有用。

#### enable_network_log

开始记录活动页面的所有HTTP请求和响应。

**参数：**
**响应数据：**`{"enabled": true}`

#### disable_network_log

停止记录网络活动。已经捕获的条目仍然保留。

**响应数据：**`{"enabled": false}`

#### get_network_log

返回自启用日志记录（或上次清除日志记录）以来的所有捕获的网络条目。

**响应数据：**
```json
{
  "count": 4,
  "log": [
    {"type": "request", "url": "https://api.example.com/data", "method": "GET", "resource_type": "fetch", "timestamp": 1234567890.123},
    {"type": "response", "url": "https://api.example.com/data", "status": 200, "timestamp": 1234567890.456},
    {"type": "request", "url": "https://cdn.example.com/style.css", "method": "GET", "resource_type": "stylesheet", "timestamp": 1234567890.789},
    {"type": "response", "url": "https://cdn.example.com/style.css", "status": 200, "timestamp": 1234567890.999}
  ]
}
```

**响应数据：**
```json
{"action": "clear_network_log"}
```

每个条目要么是`"request"`，要么是`"response"`。请求包括`method`和`resource_type`（如fetch、document、stylesheet、script、image等）。响应包括`status`代码。

#### clear_network_log

删除所有捕获的网络条目，但如果之前已启用日志记录，则保持日志记录功能。

**响应数据：**`{"cleared": true}`

### 滚动

#### scroll_to_bottom

使用JavaScript的`window.scrollBy()`从顶部到底部滚动整个页面。每次滚动步长固定，滚动之间有延迟。当滚动到页面底部时（滚动位置停止变化），会再滚动回顶部。适用于触发延迟加载的内容。

**参数：**
- `delay`（可选，默认为`0.4`）：每次滚动步长之间的延迟（以秒为单位）。

**响应数据：`{"scrolled": "bottom"}`

#### scroll_to_bottom_humanized`

与`scroll_to_bottom`相同，但使用真实的操作系统级别的鼠标滚轮滚动（通过PyAutoGUI），并带有随机化的滚动量和抖动延迟，以模拟人类的滚动行为。这种方式无法被行为分析工具检测到。

**参数：**
- `min_clicks`（可选，默认为`2`）：每次滚动步长的最小鼠标滚轮点击次数。
- `max_clicks`（可选，默认为`6`）：每次滚动步长的最大鼠标滚轮点击次数。每次选择`min`和`max`之间的随机值。
- `delay`（可选，默认为`0.5`）：每次滚动步长之间的基本延迟（以秒为单位）。实际延迟会有±30%的抖动。

**响应数据：**`{"scrolled": "bottom_humanized"}`

### Display

#### calibrate

重新计算视口坐标（`get_interactive_elements`返回的坐标）和屏幕坐标（PyAutoGUI使用的坐标）之间的映射关系。浏览器有窗口边框（标题栏、地址栏），这会导致视口坐标与屏幕坐标不一致。

**参数：**
- `window_offset`（必需）：`{"x": 0, "y": 74}`

**何时调用：**在进入/退出全屏模式后；在浏览器窗口大小调整后；或者当`system_click`返回的坐标似乎不正确时。此函数在启动时会自动计算偏移量，因此很少需要调用。

#### get_resolution

返回虚拟显示器的分辨率（来自XVFB_RESOLUTION环境变量）。

**响应数据：**`{"width": 1920, "height": 1080}`

#### enter_fullscreen / exit_fullscreen

切换浏览器的全屏模式（隐藏地址栏和窗口边框）。在全屏模式下，视口会占据整个屏幕，因此坐标映射方式会发生变化。

**响应数据：**`{"fullscreen": true, "changed": true}` — 如果已经处于全屏模式，`changed`将为`false`。

**重要提示：**在进入/退出全屏模式后，请调用`calibrate`以更新坐标映射。

### 实用功能

#### ping

进行健康检查，返回当前页面的URL。用于验证API是否响应以及浏览器是否正常运行。

**参数：**
- `duration`（可选，默认为`1`）：等待的持续时间（以秒为单位）。

**响应数据：**`{"slept": 2}`

#### close

关闭浏览器。调用此函数后，容器将停止运行。

**响应数据：**`{"message": "closing"}`

### 状态端点（GET）

#### GET /state

返回当前的浏览器状态。

**响应数据：**
```bash
curl -s "$STEALTHY_AUTO_BROWSE_URL/state"
```

**响应：**
```json
{
  "status": "ready",
  "url": "https://example.com/",
  "title": "Example Domain",
  "window_offset": {"x": 0, "y": 74}
}
```

#### GET /health

简单的健康检查。当API准备就绪时，返回`ok`作为纯文本。

**响应数据：**`{"ok"`

## 容器选项

```bash
# Custom display resolution
docker run -d -p 8080:8080 -e XVFB_RESOLUTION=1280x720 psyb0t/stealthy-auto-browse

# Match timezone to your IP's geographic location (important for stealth — mismatched
# timezone is a common bot detection signal)
docker run -d -p 8080:8080 -e TZ=Europe/Bucharest psyb0t/stealthy-auto-browse

# Route browser traffic through an HTTP proxy
docker run -d -p 8080:8080 -e PROXY_URL=http://user:pass@proxy:8888 psyb0t/stealthy-auto-browse

# Persistent browser profile — cookies, sessions, and fingerprint survive container restarts
docker run -d -p 8080:8080 -v ./profile:/userdata psyb0t/stealthy-auto-browse

# Open a URL automatically on startup
docker run -d -p 8080:8080 psyb0t/stealthy-auto-browse https://example.com
```

## 页面加载器（URL触发的自动化）

页面加载器类似于**Greasemonkey/Tampermonkey用户脚本**，但适用于HTTP API。你可以定义一组动作，每当浏览器导航到匹配的URL时自动执行这些动作。这样就不需要每次访问网站时都手动发送一系列命令，只需将它们编写成YAML文件，容器会自动执行。

**用途示例：**移除Cookie弹出框、关闭覆盖层、等待动态内容、在抓取前清理页面，或者任何需要手动重复执行的设置。

### 工作原理

1. 创建定义URL模式和步骤列表的YAML文件。
2. 将这些文件挂载到容器的`/loaders`目录中。
3. 每当`goto`导航到匹配加载器模式的URL时，就会自动执行加载器中的步骤，而不是默认的导航逻辑。

**这些步骤与HTTP API中的动作完全相同。**你可以通过`POST /`（如goto、eval、click、system_click、sleep、scroll、wait_for_element等）发送的任何动作都可以作为加载器步骤。名称和参数都相同。

### 设置

```bash
docker run -d -p 8080:8080 -p 5900:5900 \
  -v ./my-loaders:/loaders \
  psyb0t/stealthy-auto-browse
```

### 加载器格式

```yaml
name: Human-readable name for this loader
match:
  domain: example.com         # Exact hostname match (www. is stripped automatically)
  path_prefix: /articles      # URL path must start with this
  regex: "article/\\d+"       # Full URL must match this regex
steps:
  - action: goto              # Same actions as the HTTP API
    url: "${url}"             # ${url} is replaced with the original URL
    wait_until: networkidle
  - action: eval
    expression: "document.querySelector('.cookie-banner')?.remove()"
  - action: wait_for_element
    selector: "#main-content"
    timeout: 10
```

### 匹配规则

所有匹配字段都是**可选的**，但至少需要一个匹配条件。如果你指定了多个字段，**所有**字段都必须匹配才能触发加载器：

- **`domain`：**精确的域名。在比较之前会去掉`www.`前缀，因此`domain: example.com`也会匹配`www.example.com`。
- **`path_prefix`：**URL路径必须以这个字符串开头。例如`path_prefix: /blog`会匹配`/blog`、`/blog/post-1`、`/blog/archive`等。
- **`regex`：**整个URL会与这个正则表达式进行匹配。

### `${url}`占位符

在步骤中的任何字符串值中，`${url}`会被替换为传递给`goto`的原始URL。这允许你使用自定义的等待设置导航到该URL，或者将其传递给JavaScript：

**参数：**
```yaml
steps:
  - action: goto
    url: "${url}"
    wait_until: networkidle
  - action: eval
    expression: "console.log('Loaded:', '${url}')"
```

### 实际示例：干净地抓取数据**

假设你正在抓取一个包含Cookie弹出框、新闻邮件模态框和延迟加载内容的新闻网站。如果没有加载器，每次`goto`后都需要发送5个以上的命令。使用加载器后：

**参数：**
```yaml
# loaders/news_site.yaml
name: News Site Cleanup
match:
  domain: news-site.com
steps:
  # Navigate with full network wait so everything loads
  - action: goto
    url: "${url}"
    wait_until: networkidle

  # Wait for the main content to be there
  - action: wait_for_element
    selector: "article"
    timeout: 10

  # Kill the cookie popup
  - action: eval
    expression: "document.querySelector('.cookie-consent')?.remove()"

  # Kill the newsletter modal
  - action: eval
    expression: "document.querySelector('.newsletter-overlay')?.remove()"

  # Scroll to trigger lazy-loaded images
  - action: scroll_to_bottom
    delay: 0.3

  # Small pause for everything to settle
  - action: sleep
    duration: 1
```

现在当你`goto``news-site.com`上的任何URL时，所有这些操作都会自动执行。响应中会包含`"loader": "News Site Cleanup"`，这样你就知道是加载器触发了这些操作。

### 加载器触发时的响应

**参数：**
```json
{
  "success": true,
  "data": {
    "loader": "News Site Cleanup",
    "steps_executed": 6,
    "last_result": { "success": true, "timestamp": 1234567890.456, "data": { "slept": 1 } }
  }
}
```

## 预安装的扩展程序

浏览器预安装了以下扩展程序：

- **uBlock Origin**：阻止广告和跟踪。
- **LocalCDN**：在本地提供常见的CDN资源，以防止跟踪。
- **ClearURLs**：从URL中删除跟踪参数。
- **Consent-O-Matic**：自动处理Cookie同意弹出框（点击“拒绝所有”或选择最小化同意）。

## 示例：完整登录流程（无法被检测到）

**参数：**
```bash
API=$STEALTHY_AUTO_BROWSE_URL

# Navigate to login page
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "goto", "url": "https://example.com/login"}'

# See what's on the page
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "get_text"}'

# Find all interactive elements and their coordinates
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "get_interactive_elements"}'

# Click the email field (coordinates from get_interactive_elements)
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "system_click", "x": 400, "y": 200}'

# Type email with human-like keystrokes
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "system_type", "text": "user@example.com"}'

# Tab to password field
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "send_key", "key": "tab"}'

# Type password
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "system_type", "text": "secretpassword"}'

# Press Enter to submit
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "send_key", "key": "enter"}'

# Wait for redirect to dashboard
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "wait_for_url", "url": "**/dashboard", "timeout": 15}'

# Verify we're logged in
curl -s -X POST $API -H 'Content-Type: application/json' \
  -d '{"action": "get_text"}'
```

## 提示**

1. **在点击之前始终调用`get_interactive_elements`——不要猜测坐标**。
2. **使用系统方法实现隐形浏览**——`system_click`、`system_type`、`send_key`是无法被检测到的。
3. **先使用`get_text`，再使用截图**——文本获取更快且占用更少资源。
4. **根据你的IP位置设置时区**——时区不匹配是常见的机器人检测信号。
5. **使用`?whLargest=512`调整截图大小**——全分辨率的截图文件通常很大。
6. **挂载`/userdata`以保持会话状态**——Cookies、指纹信息和配置文件在重启后仍然保留。
7. **使用等待条件代替`sleep`**——使用`wait_for_element`、`wait_for_text`、`wait_for_url`。
8. **在触发对话框的操作之前调用`handle_dialog`**——如果你需要关闭对话框或提供提示文本（否则对话框会自动关闭）。
9. **在全屏模式改变后调用`calibrate`**——坐标映射可能会改变。
10. **在操作之间添加轻微的延迟**——在点击之间添加0.5-1.5秒的延迟，使操作更自然。
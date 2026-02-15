---
name: browserless-agent
description: 使用无头浏览器进行专业的网络自动化操作——可以浏览网页、抓取数据、自动化执行任务、进行测试，并与任何网站进行交互。
homepage: https://github.com/openclaw/browserless-agent
user-invocable: true
metadata: {"openclaw": {"emoji": "🌐", "requires": {"env": ["BROWSERLESS_URL"]}, "primaryEnv": "BROWSERLESS_URL"}}
---

# 无浏览器代理 🌐  
这是一个专为 OpenClaw 设计的全面网页自动化工具，提供了 30 多种浏览器操作功能，包括导航、数据提取、表单填写、截图抓取、PDF 生成、文件处理以及高级网页抓取能力。  

## 🚀 主要功能  

- **导航**：完全控制页面导航、重定向和浏览历史记录  
- **数据提取**：获取文本、属性、HTML、计算出的样式以及结构化数据  
- **表单自动化**：输入文本、点击按钮、选择选项、上传文件  
- **视觉抓取**：截取全页、单个元素或视口的截图  
- **内容生成**：支持自定义选项将页面保存为 PDF  
- **高级交互**：悬停、拖放、键盘快捷键、滚动  
- **多标签页支持**：管理多个页面和窗口  
- **网络控制**：拦截请求、修改请求头、阻止某些资源  
- **存储访问**：管理 cookie、localStorage 和 sessionStorage  
- **动态内容处理**：等待元素加载完成、处理网络空闲状态、自定义条件  
- **iframe 操作**：与嵌套 iframe 内容交互  
- **浏览器状态模拟**：模拟不同设备、设置地理位置、处理弹出对话框  

## 🔧 配置  

使用此工具需要在 OpenClaw 中配置 `BROWSERLESS_URL` 环境变量。  
可选地，还可以设置 `BROWSERLESS_TOKEN` 用于身份验证。  

**配置步骤：**  
1. 打开 OpenClaw 设置  
2. 转到 “Skills” → “browserless-agent”  
3. 在 “API Key” 字段中输入无浏览器代理的基础 URL  
4. （可选）在 “env” 部分添加 `BROWSERLESS_TOKEN` 以进行令牌验证  

**配置示例：**  
- **云服务（使用令牌）**：  
  ```
BROWSERLESS_URL=wss://chrome.browserless.io
BROWSERLESS_TOKEN=your-token-here
```  
- **本地服务（不使用令牌）**：  
  ```
BROWSERLESS_URL=ws://localhost:3000
```  
- **自定义端点**：  
  ```
BROWSERLESS_URL=wss://your-host.com/playwright/chromium
BROWSERLESS_TOKEN=optional-token
```  

此工具会自动执行以下操作：  
- 如果未指定端点，会添加 `/playwright/chromium`  
- 如果设置了 `BROWSERLESS_TOKEN`，会将其作为查询参数附加  
- 支持使用或不使用身份验证令牌  

您可以在 [browserless.io](https://browserless.io) 获取无浏览器代理服务。  

## 📖 可用操作  

### 导航与页面控制  

#### `navigate`  
导航到指定 URL。  
```json
{"url": "https://example.com"}
```  

#### `go_back`  
返回浏览历史记录中的上一页。  
```json
{}
```  

#### `go_forward`  
导航到浏览历史记录中的下一页。  
```json
{}
```  

#### `reload`  
重新加载当前页面。  
```json
{"hard": false}
```  

#### `wait_for_load`  
等待页面加载完成。  
```json
{"timeout": 30000}
```  

### 数据提取  

#### `get_text`  
从元素中提取文本内容。  
```json
{"selector": "h1", "all": false}
```  

#### `get_attribute`  
从元素中获取属性值。  
```json
{"selector": "img", "attribute": "src", "all": false}
```  

#### `get_html`  
获取元素的内部或外部 HTML。  
```json
{"selector": "article", "outer": false, "all": false}
```  

#### `get_value`  
从表单元素中获取输入值。  
```json
{"selector": "input[name='email']"}
```  

#### `get_style`  
获取元素的计算出的 CSS 样式属性。  
```json
{"selector": ".box", "property": "background-color"}
```  

#### `get_multiple`  
一次性提取多个数据项。  
```json
{
  "extractions": [
    {"name": "title", "selector": "h1", "type": "text"},
    {"name": "image", "selector": "img", "type": "attribute", "attribute": "src"},
    {"name": "price", "selector": ".price", "type": "text"}
  ]
}
```  

### 交互与输入  

#### `type_text`  
在元素中输入文本。  
```json
{"selector": "input[type='search']", "text": "hello world", "delay": 0, "clear": true}
```  

#### `click`  
点击元素。  
```json
{"selector": "button.submit", "force": false, "delay": 0}
```  

#### `double_click`  
双击元素。  
```json
{"selector": ".item"}
```  

#### `right_click`  
右键点击元素（显示上下文菜单）。  
```json
{"selector": ".context-target"}
```  

#### `hover`  
将鼠标悬停在元素上。  
```json
{"selector": ".menu-item"}
```  

#### `focus`  
将焦点放在元素上。  
```json
{"selector": "input"}
```  

#### `select_option`  
从下拉菜单中选择选项。  
```json
{"selector": "select", "values": ["option1", "option2"]}
```  

#### `check`  
选中复选框或单选按钮。  
```json
{"selector": "input[type='checkbox']"}
```  

#### `uncheck`  
取消选中复选框。  
```json
{"selector": "input[type='checkbox']"}
```  

#### `upload_file`  
将文件上传到文件输入框。  
```json
{"selector": "input[type='file']", "files": ["path/to/file.pdf"]}
```  

#### `press_key`  
按下键盘键（支持常用键：Enter、Tab、Escape、ArrowDown、Control+A 等）。  
```json
{"key": "Enter"}
```  

#### `keyboard_type`  
使用键盘输入文本（支持快捷键）。  
```json
{"text": "Hello World"}
```  

### 滚动与定位  

#### `scroll_to`  
滚动到指定位置。  
```json
{"x": 0, "y": 500}
```  

#### `scroll_into_view`  
将元素滚动到视口中。  
```json
{"selector": ".footer"}
```  

#### `scroll_to_bottom`  
滚动到页面底部。  
```json
{}
```  

#### `scroll_to_top`  
滚动到页面顶部。  
```json
{}
```  

### 视觉与抓取  

#### `screenshot`  
截取页面或元素的截图。  
```json
{
  "path": "screenshot.png",
  "full_page": true,
  "selector": null,
  "quality": 90,
  "type": "png"
}
```  

#### `pdf`  
将当前页面生成为 PDF。  
```json
{
  "path": "page.pdf",
  "format": "A4",
  "landscape": false,
  "margin": {"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"},
  "print_background": true
}
```  

### 评估与执行  

#### `evaluate`  
在页面上下文中执行 JavaScript 代码。  
```json
{"expression": "document.title"}
```  

#### `evaluate_function`  
带参数执行 JavaScript 函数。  
```json
{
  "function": "(x, y) => x + y",
  "args": [5, 10]
}
```  

### 等待与定时  

#### `wait_for_selector`  
等待指定元素出现（状态：可见、隐藏、已附加、已分离）。  
```json
{"selector": ".dynamic-content", "timeout": 10000, "state": "visible"}
```  
可选状态：visible、hidden、attached、detached  

#### `wait_for_timeout`  
等待指定毫秒数。  
```json
{"timeout": 2000}
```  

#### `wait_for_function`  
等待 JavaScript 表达式返回真值。  
```json
{
  "expression": "() => document.readyState === 'complete'",
  "timeout": 10000
}
```  

#### `wait_for_navigation`  
等待导航操作完成（可选状态：load、domcontentloaded、networkidle）。  
```json
{"timeout": 30000, "wait_until": "networkidle"}
```  

### 元素状态检查  

#### `is_visible`  
检查元素是否可见。  
```json
{"selector": ".modal"}
```  

#### `is_enabled`  
检查元素是否启用。  
```json
{"selector": "button"}
```  

#### `is-checked`  
检查复选框或单选按钮是否被选中。  
```json
{"selector": "input[type='checkbox']"}
```  

#### `element_exists`  
检查元素是否存在于 DOM 中。  
```json
{"selector": ".optional-element"}
```  

#### `element_count`  
统计匹配指定选择器的元素数量。  
```json
{"selector": ".list-item"}
```  

### 存储与 Cookie  

#### `get_cookies`  
获取所有 cookie 或特定 cookie。  
```json
{"name": "session_id"}
```  

#### `set_cookie`  
设置 cookie。  
```json
{
  "name": "user_preference",
  "value": "dark_mode",
  "domain": "example.com",
  "path": "/",
  "expires": 1735689600,
  "httpOnly": false,
  "secure": true,
  "sameSite": "Lax"
}
```  

#### `delete_cookies`  
删除 cookie。  
```json
{"name": "session_id"}
```  
省略名称可删除所有 cookie。  

#### `get_local_storage`  
获取 localStorage 中的项。  
```json
{"key": "user_data"}
```  

#### `set_local_storage`  
设置 localStorage 中的项。  
```json
{"key": "theme", "value": "dark"}
```  

#### `clear_local_storage`  
清除所有 localStorage 内容。  
```json
{}
```  

### 网络与请求  

#### `set_extra_headers`  
为所有请求设置额外的 HTTP 请求头。  
```json
{
  "headers": {
    "Authorization": "Bearer token123",
    "X-Custom-Header": "value"
  }
}
```  

#### `block_resources`  
阻止某些类型的资源加载。  
```json
{"types": ["image", "stylesheet", "font"]}
```  
支持的资源类型：document、stylesheet、image、media、font、script、xhr、fetch、other  

#### `get_page_info`  
获取页面的详细信息（如标题、URL、HTML 等）。  
```json
{}
```  

### iframe 操作  

#### `get_frame_text`  
获取 iframe 内元素的文本。  
```json
{
  "frame_selector": "iframe#content",
  "selector": "h1"
}
```  

#### `click_in_frame`  
点击 iframe 内的元素。  
```json
{
  "frame_selector": "iframe#content",
  "selector": "button"
}
```  

### 多页面/标签页  

#### `new_page`  
打开新页面或标签页。  
```json
{"url": "https://example.com"}
```  

#### `close_page`  
关闭特定页面。  
```json
{"index": 1}
```  

#### `switch_page`  
切换到其他页面。  
```json
{"index": 0}
```  

#### `list_pages`  
列出所有打开的页面。  
```json
{}
```  

### 浏览器环境模拟  

#### `set_viewport`  
设置视口大小。  
```json
{"width": 1920, "height": 1080}
```  

#### `emulate_device`  
模拟移动设备（支持设备类型：iPhone 12、iPad Pro、Galaxy S21、Pixel 5）。  
```json
{"device": "iPhone 12"}
```  

#### `set_geolocation`  
设置地理位置。  
```json
{
  "latitude": 37.7749,
  "longitude": -122.4194,
  "accuracy": 100
}
```  

#### `set_user_agent`  
设置自定义用户代理。  
```json
{"user_agent": "Mozilla/5.0..."}
```  

### 高级自动化  

#### `drag_and_drop`  
拖放元素到目标位置。  
```json
{
  "source": ".draggable",
  "target": ".drop-zone"
}
```  

#### `fill_form`  
一次性填写多个表单字段。  
```json
{
  "fields": {
    "input[name='email']": "user@example.com",
    "input[name='password']": "secret123",
    "select[name='country']": "US"
  }
}
```  

#### `extract_table`  
从 HTML 表格中提取数据。  
```json
{
  "selector": "table.data",
  "headers": true
}
```  

#### `extract_links`  
提取页面中的所有链接。  
```json
{
  "selector": "a",
  "filter": "^https://example\\.com"
}
```  

#### `handle_dialog`  
设置如何处理 JavaScript 对话框（如警告框、确认框或提示框）。  
```json
{
  "action": "accept",
  "text": "Optional prompt response"
}
```  
可选操作：accept（接受）、dismiss（关闭）。  

## 💡 使用示例  

### 示例 1：网页抓取  
```bash
python main.py get_multiple '{
  "url": "https://news.ycombinator.com",
  "extractions": [
    {"name": "titles", "selector": ".titleline > a", "type": "text", "all": true},
    {"name": "links", "selector": ".titleline > a", "type": "attribute", "attribute": "href", "all": true}
  ]
}'
```  

### 示例 2：表单自动化  
```bash
python main.py fill_form '{
  "url": "https://example.com/contact",
  "fields": {
    "input[name='name']": "John Doe",
    "input[name='email']": "john@example.com",
    "textarea[name='message']": "Hello!"
  }
}'
```  

### 示例 3：带元素高亮的截图  
```bash
python main.py screenshot '{
  "url": "https://example.com",
  "selector": ".hero-section",
  "path": "hero.png",
  "full_page": false
}'
```  

### 示例 4：PDF 生成  
```bash
python main.py pdf '{
  "url": "https://example.com/report",
  "path": "report.pdf",
  "format": "A4",
  "margin": {"top": "2cm", "bottom": "2cm"}
}'
```  

## 🎯 与 OpenClaw 的集成  

在 OpenClaw 中使用此工具时，代理可以自动执行这些操作：  
- **用户**：“截取 example.com 的截图。”  
  **代理**：执行 `screenshot` 操作并传入 URL。  
- **用户**：“wikipedia.org 的标题是什么？”  
  **代理**：导航到 Wikipedia 并提取标题元素的文本。  
- **用户**：“在 Google 中搜索‘Python’并获取第一个结果链接。”  
  **代理**：导航到 Google，输入搜索词，点击搜索按钮，提取第一个结果链接。  

## 🔒 安全注意事项  

- 无浏览器代理连接使用基于 TLS 的 WebSocket（wss://）  
- 从未记录或暴露任何凭据  
- 所有浏览器操作都在无浏览器代理容器中隔离执行  
- 无需安装本地浏览器  

## 🐛 故障排除  

- **连接失败**：  
  - 确认 `BROWSERLESS_WS` URL 是否正确  
  - 检查令牌是否有效且未过期  
  - 确保网络环境支持 WebSocket 连接  

- **超时错误**：  
  - 对于加载缓慢的页面，增加超时时间  
  - 在与动态内容交互前使用 `wait_for_selector`  
  - 对于依赖 AJAX 的网站，考虑使用 `wait_until: "networkidle"`  

- **元素未找到**：  
  - 使用浏览器开发者工具验证选择器  
  - 使用 `wait_for_selector` 等待元素加载完成  
  - 检查元素是否位于 iframe 内  

## 📚 参考资源  

- [Playwright 文档](https://playwright.dev)  
- [CSS 选择器参考](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors)  
- [Browserless 文档](https://docs.browserless.io)
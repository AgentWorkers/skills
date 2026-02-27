---
name: fastplaywright
description: 使用 Fast Playwright MCP 实现高性能的浏览器自动化。该工具具备以下特性：基于令牌的批量执行优化、智能的元素选择机制（并提供回退选项）、用于变更跟踪的差异检测功能，以及全面的诊断工具。适用于 Web 测试、表单自动化、截图抓取、导航流程处理，以及任何需要高效利用令牌的基于浏览器的任务。
---
# Fast Playwright MCP

这是一个高性能的浏览器自动化工具，基于 Fast Playwright MCP 服务器（`@tontoko/fast-playwright-mcp`）开发。作为 Microsoft Playwright MCP 的一个分支，它提供了显著的令牌优化、批量执行以及更强大的元素定位功能。

## 相比标准 Playwright MCP 的主要优势

| 特性 | 优势 |
|---------|---------|
| **令牌优化** | 通过 `expectation` 参数可将令牌使用量减少 70-80% |
| **批量执行** | 在多步骤工作流程中可节省 90% 的令牌使用量 |
| **差异检测** | 仅跟踪页面变化，而非整个页面的快照 |
| **增强的选择器** | 支持多种选择器类型，并具有自动回退机制 |
| **诊断工具** | 提供高级的调试和元素定位功能 |
| **图像压缩** | 支持 JPEG 格式，支持质量控制和尺寸调整 |

## MCP 配置

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@tontoko/fast-playwright-mcp@latest"]
    }
  }
}
```

## 为了获得最佳效果，请按照以下步骤操作：

### 1. 首先导航
在执行任何操作之前，使用 `browser_navigate` 加载目标页面。

### 2. 对于多步骤任务使用批量执行
对于包含两个以上操作的任务，务必使用 `browser_batch_execute` 而不是单独调用每个工具。

### 3. 优化令牌使用
使用 `expectation` 参数来减少响应数据的大小。

### 4. 使用差异检测来跟踪状态变化
在不需要页面导航的情况下，启用 `diffOptions` 以仅跟踪页面的变化。

## 令牌优化

### `expectation` 参数
所有浏览器工具都支持 `expectation` 参数，用于控制响应内容的处理方式：

```json
{
  "includeSnapshot": false,    // 70-80% token reduction
  "includeConsole": false,      // Exclude console messages
  "includeTabs": false,         // Hide tab information
  "includeCode": false,         // Suppress code generation
  "includeDownloads": false     // Exclude download info
}
```

### 快照选项
为了便于分析，可以限制快照的内容范围：

```json
{
  "snapshotOptions": {
    "selector": ".main-content",  // Capture specific section only
    "maxLength": 2000,            // Limit character count
    "format": "aria"              // Use accessibility tree format
  }
}
```

### 差异检测
仅跟踪操作之间的变化：

```json
{
  "diffOptions": {
    "enabled": true,
    "format": "minimal",      // Options: unified, split, minimal
    "threshold": 0.1,
    "maxDiffLines": 50,
    "context": 3
  }
}
```

## 增强的选择器系统

### 选择器类型（优先级顺序）
1. **ref** - 从之前的结果中生成的元素 ID（最高优先级）
2. **css** - 标准 CSS 选择器（`#id`、`.class`、`tag`）
3. **role** - 带有可选文本的 ARIA 角色（如 `button`、`textbox` 等）
4. **text** - 基于文本的内容搜索，支持可选的标签过滤

### 具有自动回退机制的选择器数组
所有基于元素的操作都支持多个选择器，并且会自动尝试不同的选择方式。如果找到多个匹配的元素，会返回一个可供选择的候选列表。

## 批量执行
### 基本模式
在一个请求中执行多个操作：

```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_navigate", "arguments": { "url": "https://example.com/login" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#username" }], "text": "user@example.com" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#password" }], "text": "password123" } },
      { "tool": "browser_click", "arguments": { "selectors": [{ "role": "button", "text": "Login" }] } }
    ]
  }
}
```

### 高级配置

```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      {
        "tool": "browser_navigate",
        "arguments": { "url": "https://example.com" },
        "expectation": { "includeSnapshot": false },
        "continueOnError": true
      },
      {
        "tool": "browser_click",
        "arguments": { "selectors": [{ "css": "#submit" }] },
        "expectation": {
          "includeSnapshot": true,
          "snapshotOptions": { "selector": ".result-area" },
          "diffOptions": { "enabled": true, "format": "minimal" }
        }
      }
    ],
    "stopOnFirstError": false,
    "globalExpectation": {
      "includeConsole": false,
      "includeTabs": false
    }
  }
}
```

### 错误处理选项
- `continueOnError`（每步执行时）：即使某一步失败，也继续执行后续操作
- `stopOnFirstError`（全局）：遇到第一个错误时停止整个批次

## 常见用法

### 导航和截图
```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_navigate", "arguments": { "url": "https://example.com" } },
      {
        "tool": "browser_take_screenshot",
        "arguments": {
          "filename": "homepage.png",
          "fullPage": true,
          "expectation": { "includeSnapshot": false }
        }
      }
    ]
  }
}
```

### 填写表单并提交
```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_navigate", "arguments": { "url": "https://example.com/contact" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#name" }], "text": "John Doe" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#email" }], "text": "john@example.com" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#message" }], "text": "Hello World" } },
      { "tool": "browser_click", "arguments": { "selectors": [{ "role": "button", "text": "Send" }] } }
    ],
    "globalExpectation": { "includeSnapshot": false }
  }
}
```

### 响应式设计测试
```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_navigate", "arguments": { "url": "https://example.com" } },
      { "tool": "browser_resize", "arguments": { "width": 1920, "height": 1080 } },
      { "tool": "browser_take_screenshot", "arguments": { "filename": "desktop.png" } },
      { "tool": "browser_resize", "arguments": { "width": 768, "height": 1024 } },
      { "tool": "browser_take_screenshot", "arguments": { "filename": "tablet.png" } },
      { "tool": "browser_resize", "arguments": { "width": 375, "height": 667 } },
      { "tool": "browser_take_screenshot", "arguments": { "filename": "mobile.png" } }
    ]
  }
}
```

### 带有验证的登录流程
```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_navigate", "arguments": { "url": "https://example.com/login" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#email" }], "text": "user@example.com" } },
      { "tool": "browser_type", "arguments": { "selectors": [{ "css": "#password" }], "text": "secret", "submit": true } },
      { "tool": "browser_wait_for", "arguments": { "text": "Dashboard" } }
    ],
    "globalExpectation": { "diffOptions": { "enabled": true } }
  }
}
```

## 诊断工具

### 查找元素
使用多种条件来查找元素：

```json
{
  "tool": "browser_find_elements",
  "arguments": {
    "searchCriteria": {
      "text": "Submit",
      "role": "button"
    },
    "maxResults": 5,
    "enableEnhancedDiscovery": true
  }
}
```

### 页面诊断
提供全面的页面分析功能：

```json
{
  "tool": "browser_diagnose",
  "arguments": {
    "diagnosticLevel": "detailed",
    "includePerformanceMetrics": true,
    "includeAccessibilityInfo": true,
    "includeTroubleshootingSuggestions": true
  }
}
```

诊断级别：`none`、`basic`、`standard`、`detailed`、`full`

### HTML 检查
提取并分析 HTML 内容：

```json
{
  "tool": "browser_inspect_html",
  "arguments": {
    "selectors": [{ "css": ".content" }],
    "depth": 3,
    "maxSize": 50000,
    "format": "html",
    "optimizeForLLM": true
  }
}
```

## 图像优化
### 压缩截图
```json
{
  "tool": "browser_take_screenshot",
  "arguments": {
    "filename": "screenshot.jpg",
    "type": "jpeg",
    "expectation": {
      "imageOptions": {
        "format": "jpeg",
        "quality": 50,
        "maxWidth": 1280
      }
    }
  }
}
```

## 网络请求过滤
监控特定的网络请求：

```json
{
  "tool": "browser_network_requests",
  "arguments": {
    "urlPatterns": ["/api/"],
    "excludeUrlPatterns": ["analytics", "tracking"],
    "methods": ["GET", "POST"],
    "statusRanges": [{ "min": 200, "max": 299 }],
    "maxRequests": 10,
    "newestFirst": true
  }
}
```

## 标签页管理

### 多标签页工作流程
```json
{
  "tool": "browser_batch_execute",
  "arguments": {
    "steps": [
      { "tool": "browser_tab_new", "arguments": { "url": "https://example.com" } },
      { "tool": "browser_tab_list", "arguments": {} },
      { "tool": "browser_tab_select", "arguments": { "index": 0 } },
      { "tool": "browser_tab_close", "arguments": { "index": 1 } }
    ]
  }
}
```

## 等待策略

### 等待文本出现
```json
{ "tool": "browser_wait_for", "arguments": { "text": "Loading complete" } }
```

### 等待文本消失
```json
{ "tool": "browser_wait_for", "arguments": { "textGone": "Loading..." } }
```

### 等待指定时间
```json
{ "tool": "browser_wait_for", "arguments": { "time": 2 } }
```

## 控制台监控
### 过滤控制台消息
```json
{
  "tool": "browser_console_messages",
  "arguments": {
    "consoleOptions": {
      "levels": ["error", "warn"],
      "maxMessages": 10,
      "patterns": ["^Error:"],
      "removeDuplicates": true
    }
  }
}
```

## JavaScript 评估
### 页面级评估
```json
{
  "tool": "browser_evaluate",
  "arguments": {
    "function": "() => document.title"
  }
}
```

### 元素级评估
```json
{
  "tool": "browser_evaluate",
  "arguments": {
    "selectors": [{ "css": "#counter" }],
    "function": "(element) => element.textContent"
  }
}
```

## 对话框处理
```json
{
  "tool": "browser_handle_dialog",
  "arguments": {
    "accept": true,
    "promptText": "Optional prompt response"
  }
}
```

## 文件上传
```json
{
  "tool": "browser_file_upload",
  "arguments": {
    "paths": ["/absolute/path/to/file.pdf"]
  }
}
```

## 拖放操作
```json
{
  "tool": "browser_drag",
  "arguments": {
    "startSelectors": [{ "css": "#draggable" }],
    "endSelectors": [{ "css": "#dropzone" }]
  }
}
```

## 选择选项
```json
{
  "tool": "browser_select_option",
  "arguments": {
    "selectors": [{ "css": "#country" }],
    "values": ["us", "de"]
  }
}
```

## 键盘输入
```json
{
  "tool": "browser_press_key",
  "arguments": {
    "key": "Enter"
  }
}
```

支持的键盘键：`Enter`、`Tab`、`Escape`、`ArrowUp`、`ArrowDown`、`ArrowLeft`、`ArrowRight`、`Backspace`、`Delete`、`Home`、`End`

## 最佳实践

### 令牌效率
1. 对于包含两个以上操作的任务，使用批量执行。
2. 对于中间步骤，禁用快照功能。
3. 启用差异检测以跟踪页面状态的变化。
4. 仅显示相关的控制台消息。
5. 使用 CSS 选择器来生成有针对性的快照。
6. 在不影响图像质量的情况下压缩图片。

### 选择器使用策略
1. 尽可能使用之前结果中的 `ref` 来定位元素。
2. 提供备用选择器以确保操作的稳定性。
3. 优先使用基于 ARIA 角色的选择器以提高可访问性。
4. 在必要时使用 CSS 选择器进行精确定位。
5. 将文本选择器作为最后的选择方式。

### 错误处理
1. 对于非关键步骤，使用 `continueOnError` 来继续执行。
2. 将 `stopOnFirstError` 设置为 `false` 以尽可能完成所有操作。
3. 当自动化失败时，使用诊断工具进行排查。
4. 查看控制台消息以获取 JavaScript 错误信息。

### 性能优化
1. 使用合适的选择器来减少快照的大小。
2. 选择合适的差异检测格式来跟踪页面变化。
3. 仅过滤相关的网络请求。
4. 将相关的操作组合在一起执行。

## 故障排除

### 元素未找到
1. 使用 `browser_find_elements` 来查找其他可用的元素。
2. 运行 `browser_diagnose` 进行页面分析。
3. 检查页面中是否存在 iframe 或 shadow DOM。
4. 确认页面是否已经完全加载。

### 超时问题
1. 使用 `browser_wait_for` 并设置具体的等待条件。
2. 对于加载缓慢的页面，增加等待时间。
3. 检查是否有网络请求被阻塞。

### 令牌溢出问题
1. 启用 `includeSnapshot: false` 以减少快照的生成。
2. 使用 `snapshotOptions.selector` 来限制快照的范围。
3. 启用 `diffOptions.enabled: true` 以启用差异检测功能。
4. 减少网络请求的次数。

## 工具参考

### 核心自动化操作
- `browser_navigate` - 导航到指定 URL
- `browser_click` - 点击元素
- `browser_type` - 输入文本
- `browserhover` - 将鼠标悬停在元素上
- `browser.drag` - 执行拖放操作
- `browser_select_option` - 从下拉菜单中选择选项
- `browser_press_key` - 按下键盘键
- `browser_file_upload` - 上传文件
- `browser_evaluate` - 执行 JavaScript 代码
- `browser_wait_for` - 等待特定条件满足

### 批量操作
- `browser_batch_execute` - 同时执行多个操作

### 信息收集
- `browser_snapshot` - 生成可访问性相关的快照
- `browser_take_screenshot` - 截取屏幕截图
- `browser_console_messages` - 获取控制台输出
- `browser_network_requests` - 列出所有网络请求
- `browser_find_elements` - 根据条件查找元素
- `browser_diagnose` - 进行页面诊断
- `browser_inspect_html` - 提取 HTML 内容

### 标签页管理
- `browser_tab_list` - 列出所有标签页
- `browser_tab_new` - 打开新标签页
- `browser_tab_select` - 切换到指定标签页
- `browser_tab_close` - 关闭标签页

### 导航操作
- `browser_navigate_back` - 返回上一页
- `browser_navigate_forward` - 前进到下一页

### 浏览器控制
- `browser.resize` - 调整窗口大小
- `browser_close` - 关闭浏览器
- `browser_install` - 安装浏览器插件
- `browser_handle_dialog` - 处理弹出窗口或确认操作

### Vision（需要 `--caps=vision` 参数）
- `browser.mouse_click_xy` - 在指定坐标点击
- `browser.mouse_move_xy` - 将鼠标移动到指定坐标
- `browser.mouse_drag_xy` - 在指定坐标之间拖动鼠标

### PDF 相关操作（需要 `--caps=pdf` 参数）
- `browser_pdf_save` - 将页面保存为 PDF 格式
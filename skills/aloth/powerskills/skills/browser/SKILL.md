---
name: powerskills-browser
description: 通过 Chrome DevTools 协议（CDP）实现 Edge 浏览器的自动化操作。可以执行以下操作：列出所有标签页、在页面间导航、截图、提取页面内容/HTML、执行 JavaScript 代码、点击页面元素、输入文本、填写表单以及滚动页面。适用于需要在 Windows 系统上控制 Edge 浏览器、抓取网页内容、自动化填写表单或截取浏览器屏幕截图的场景。使用该功能的前提是确保已安装并配置了支持远程调试的 Edge 浏览器（配置参数：--remote-debugging-port=9222）。
license: MIT
metadata:
  author: aloth
  cli: powerskills
  parent: powerskills
---
# PowerSkills — 浏览器

通过 CDP（Chrome 开发工具协议）实现 Edge 浏览器的自动化操作。

## 前提条件

- 已安装并启用远程调试功能的 Microsoft Edge：
  ```powershell
  Start-Process "msedge" -ArgumentList "--remote-debugging-port=9222"
  ```
- 默认端口可在 `config.json` 文件中配置（`edge_debug_port`）

## 可用的操作

```powershell
.\powerskills.ps1 browser <action> [--params]
```

| 操作 | 参数 | 说明 |
|--------|--------|-------------|
| `tabs` | | 列出当前打开的所有浏览器标签页 |
| `navigate` | `--url URL` | 导航到指定 URL |
| `screenshot` | `--out-file path.png [--target-id id]` | 将页面截图保存为 PNG 格式（可选：指定目标元素 ID） |
| `content` | `[--target-id id]` | 获取页面的文本内容（可选：指定目标元素 ID） |
| `html` | `[--target-id id]` | 获取整个页面的 HTML 内容（可选：指定目标元素 ID） |
| `evaluate` | `--expression "js"` | 执行 JavaScript 表达式（可选：指定目标元素 ID） |
| `click` | `--selector "#btn"` | 根据 CSS 选择器点击元素（可选：指定目标元素 ID） |
| `type` | `--selector "#input" --text "hello"` | 向输入框中输入文本（可选：指定目标元素 ID 和输入内容） |
| `new-tab` | `--url URL` | 打开新标签页（可选：指定目标 URL） |
| `close-tab` | `--target-id id` | 关闭指定标签页（可选：指定目标元素 ID） |
| `scroll` | `--scroll-target top\|bottom\|selector` | 滚动页面（可选：指定滚动目标位置或选择器） |
| `fill` | `--fields-json '[{"selector":"#a","value":"b"}]'` | 填充多个表单字段（可选：指定字段选择器和值） |
| `wait` | `--seconds N` | 等待 N 秒（默认值：3 秒） |

## 使用示例

```powershell
# List open tabs
.\powerskills.ps1 browser tabs

# Navigate and screenshot
.\powerskills.ps1 browser navigate --url "https://example.com"
.\powerskills.ps1 browser screenshot --out-file page.png

# Extract page text
.\powerskills.ps1 browser content

# Run JavaScript
.\powerskills.ps1 browser evaluate --expression "document.title"

# Fill a login form
.\powerskills.ps1 browser fill --fields-json '[{"selector":"#user","value":"alex"},{"selector":"#pass","value":"secret","submit":"#login"}]'
```

## 多标签页支持

通过传递 `--target-id` 参数（从 `tabs` 操作返回的标签页 ID），可以针对特定的标签页执行操作。如果不提供该参数，所有操作将针对第一个标签页进行。

## 表单字段填充格式

需要使用如下格式的 JSON 数组来填充表单字段：

```json
[
  {"selector": "#input1", "value": "输入内容1"},
  {"selector": "#input2", "value": "输入内容2"},
  {"selector": "#checkbox1", "value": "复选框1"},
  {"selector": "#submit", "value": "提交"}
]
```

## 注意事项

- 该工具支持文本输入框、选择框和复选框的填充操作；
- 最后一个字段可以包含 `submit`，用于触发表单的提交按钮。
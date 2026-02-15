---
name: playwright-cli
description: 通过 Playwright CLI 实现浏览器自动化。可以打开网页、与页面元素交互、截取屏幕截图等。非常适合用于编写自动化脚本和自动化测试工作流程。
metadata: {"clawdbot":{"emoji":"🎭","requires":{"bins":["playwright-cli"]},"install":[{"id":"node","kind":"node","package":"@playwright/mcp","bins":["playwright-cli"],"label":"Install Playwright CLI (npm)"}]}}
---

# Playwright CLI

Playwright 提供了一个用于浏览器自动化的命令行工具（CLI），它是一个高效且易于使用的工具，适用于编写自动化脚本。

## 安装

```bash
npm install -g @playwright/mcp@latest
playwright-cli --help
```

## 核心命令

| 命令 | 描述 |
|---------|-------------|
| `playwright-cli open <url>` | 在浏览器中打开指定的 URL |
| `playwright-cli close` | 关闭当前页面 |
| `playwright-cli type <text>` | 在可编辑元素中输入文本 |
| `playwright-cli click <ref> [button]` | 点击指定的元素 |
| `playwright-cli dblclick <ref> [button]` | 双击指定的元素 |
| `playwright-cli fill <ref> <text>` | 在输入框中输入文本 |
| `playwright-cli drag <startRef> <endRef>` | 从 `startRef` 拖动到 `endRef` |
| `playwright-cli hover <ref>` | 将鼠标悬停在指定的元素上 |
| `playwright-cli check <ref>` | 勾选指定的复选框/单选框 |
| `playwright-cli uncheck <ref>` | 取消选中指定的复选框/单选框 |
| `playwright-cli select <ref> <val>` | 从下拉菜单中选择指定的选项 |
| `playwright-cli snapshot` | 为指定的元素生成页面快照 |

## 导航

```bash
playwright-cli go-back           # Go back
playwright-cli go-forward        # Go forward
playwright-cli reload            # Reload page
```

## 键盘与鼠标操作

```bash
playwright-cli press <key>       # Press key (a, arrowleft, enter...)
playwright-cli keydown <key>     # Key down
playwright-cli keyup <key>       # Key up
playwright-cli mousemove <x> <y> # Move mouse
playwright-cli mousedown [button] # Mouse down
playwright-cli mouseup [button]   # Mouse up
playwright-cli mousewheel <dx> <dy> # Scroll
```

## 保存与导出

```bash
playwright-cli screenshot [ref]  # Screenshot page or element
playwright-cli pdf               # Save as PDF
```

## 标签页管理

```bash
playwright-cli tab-list          # List all tabs
playwright-cli tab-new [url]     # Open new tab
playwright-cli tab-close [index] # Close tab
playwright-cli tab-select <index> # Switch tab
```

## 开发工具

```bash
playwright-cli console [min-level]  # View console messages
playwright-cli network              # View network requests
playwright-cli run-code <code>      # Run JS snippet
playwright-cli tracing-start        # Start trace
playwright-cli tracing-stop         # Stop trace
```

## 会话管理

```bash
playwright-cli session-list         # List sessions
playwright-cli session-stop [name]  # Stop session
playwright-cli session-stop-all     # Stop all
playwright-cli session-delete [name] # Delete session data
```

## 无头模式

```bash
playwright-cli open https://example.com --headed
```

## 示例

```bash
# Open and interact
playwright-cli open https://example.com
playwright-cli type "search query"
playwright-cli press Enter
playwright-cli screenshot

# Use sessions
playwright-cli open https://site1.com
playwright-cli --session=project-a open https://site2.com
```

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `PLAYWRIGHT_MCP_BROWSER` | 可使用的浏览器：chrome, firefox, webkit, msedge |
| `PLAYWRIGHT_MCP_HEADLESS` | 是否以无头模式运行（默认为有头模式） |
| `PLAYWRIGHT_MCP_ALLOWED_HOSTS` | 允许访问的域名列表（以逗号分隔） |
| `PLAYWRIGHT_MCP_CONFIG` | 配置文件的路径 |

## 配置

请创建 `playwright-cli.json` 文件以保存配置信息：

```json
{
  "browser": {
    "browserName": "chromium",
    "headless": false
  },
  "outputDir": "./playwright-output",
  "console": {
    "level": "info"
  }
}
```

## 注意事项

- **跨平台支持**：需要 Node.js 18 及更高版本（Linux, macOS, Windows） |
- 会话默认会保留 cookie 和存储数据 |
- 使用 `--session` 标志可以创建独立的浏览器实例 |
- 生成的页面快照会包含元素的引用信息，便于后续命令的使用 |

## 来源

https://github.com/microsoft/playwright-cli
---
name: webapp-testing
description: 这是一个用于与本地Web应用程序交互和测试的工具包，支持验证前端功能、调试用户界面行为、捕获浏览器截图以及查看浏览器日志。
license: Complete terms in LICENSE.txt
---

# Web 应用程序测试

要测试本地的 Web 应用程序，请编写原生 Python Playwright 脚本。

**可用的辅助脚本**：
- `scripts/with_server.py` - 管理服务器的生命周期（支持多个服务器）

**在运行脚本之前，请务必先使用 `--help` 选项查看使用方法。** 在尝试运行脚本之前，不要直接阅读源代码；只有当确实需要自定义解决方案时才阅读源代码。这些脚本可能体积较大，可能会占用较多的系统资源（例如，导致界面窗口变得拥挤）。它们的设计目的是作为“黑盒脚本”直接使用，而不是被集成到你的应用程序中。

## 决策树：选择你的测试方法

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## 示例：使用 `with_server.py`

要启动服务器，请先运行 `--help`，然后使用相应的辅助脚本：

**单台服务器：**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**多台服务器（例如，后端 + 前端）：**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

要创建自动化脚本，请仅包含 Playwright 逻辑（服务器的配置由辅助脚本自动处理）：
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## “侦察-行动”模式

1. **检查渲染后的 DOM 结构**：
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **从检查结果中识别目标元素（选择器）**

3. **使用识别出的选择器执行相应的操作**

## 常见错误

❌ **不要** 在动态应用程序中等待 `networkidle` 信号之前就检查 DOM 结构
✅ **务必** 在检查之前等待 `page.wait_for_load_state('networkidle')`

## 最佳实践

- **将辅助脚本作为“黑盒”工具使用**：在需要完成某项任务时，查看 `scripts/` 目录中的脚本是否能提供帮助。这些脚本能够可靠地处理常见的复杂工作流程，而不会使应用程序界面变得混乱。使用 `--help` 查看使用方法，然后直接调用相应的脚本。
- 对于同步执行的脚本，请使用 `sync_playwright()`。
- 完成测试后务必关闭浏览器。
- 使用描述性强的选择器：`text=`, `role=`, CSS 选择器或 ID。
- 添加适当的等待机制：`page.wait_for_selector()` 或 `page.wait_for_timeout()`。

## 参考文件

- **examples/** - 包含常见测试模式的示例脚本：
  - `element_discovery.py` - 在页面上查找按钮、链接和输入元素
  - `static_html_automation.py` - 使用 `file://` URL 测试静态 HTML 页面
  - `console_logging.py` - 在自动化过程中捕获控制台日志
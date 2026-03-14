---
name: chrome-devtools-mcp
description: "Chrome DevTools MCP（Chrome DevTools Management Protocol）是谷歌官方提供的浏览器自动化和测试服务器。通过MCP协议，可以利用Puppeteer来控制Chrome浏览器：执行点击操作、填写表单、浏览网页、截图、分析性能数据、检查网络请求以及进行控制台调试。该工具适用于浏览器测试、网页自动化、性能分析、用户界面测试、表单填写以及视觉回归测试等场景。"
homepage: https://github.com/ChromeDevTools/chrome-devtools-mcp
license: Apache-2.0
compatibility: Node.js v20.19+, Chrome/Chromium
metadata: {"openclaw": {"emoji": "🌐", "requires": {"env": []}, "homepage": "https://github.com/ChromeDevTools/chrome-devtools-mcp"}}
---
# 🌐 Chrome DevTools MCP

这是谷歌官方提供的Chrome DevTools MCP服务器，它通过Puppeteer和Chrome DevTools协议，允许AI代理完全控制实时的Chrome浏览器。

## 主要功能

- **输入自动化**：点击、拖动、填写表单、悬停、按键、上传文件、处理对话框
- **导航**：打开/关闭/切换页面、等待元素或网络请求完成
- **截图与快照**：以视觉方式和DOM结构的形式捕获页面状态
- **性能分析**：记录并分析Chrome的性能数据
- **网络监控**：列出并检查网络请求和响应
- **控制台调试**：查看带有源代码堆栈跟踪的控制台信息
- **设备模拟**：模拟移动设备、调整视口大小
- **表单自动化**：同时填写多个表单字段

## 系统要求

- Node.js v20.19及以上版本（OpenClaw中已包含）
- Chrome/Chromium浏览器

## 快速入门

### 安装与验证

```bash
npx -y chrome-devtools-mcp@latest --help
```

### 启动MCP服务器

```bash
# Standard (launches Chrome automatically)
npx -y chrome-devtools-mcp@latest

# Headless mode (for servers)
npx -y chrome-devtools-mcp@latest --headless

# Connect to existing Chrome (must be started with --remote-debugging-port=9222)
npx -y chrome-devtools-mcp@latest --browser-url=http://127.0.0.1:9222

# Disable telemetry
npx -y chrome-devtools-mcp@latest --no-usage-statistics --no-performance-crux
```

### 集成到OpenClaw

在`openclaw.json`文件中的MCP服务器配置部分添加以下内容：

```json
{
  "mcp": {
    "servers": {
      "chrome-devtools": {
        "command": "npx",
        "args": ["-y", "chrome-devtools-mcp@latest", "--headless", "--no-usage-statistics"]
      }
    }
  }
}
```

或者使用设置脚本：

```bash
python3 {baseDir}/scripts/setup_chrome_mcp.py setup
python3 {baseDir}/scripts/setup_chrome_mcp.py status
python3 {baseDir}/scripts/setup_chrome_mcp.py test
```

## 工具参考

### 输入自动化（8个工具）

| 工具 | 功能 | 必需参数 |
|------|-------------|------------|
| `click` | 点击元素 | `uid`（必填），`dblClick` |
| `drag` | 将元素拖放到另一个位置 | `from_uid`, `to_uid` |
| `fill` | 在输入框/文本区域/选择框中输入文本 | `uid`, `value` |
| `fill_form` | 同时填写多个表单字段 | `elements[]` |
| `handle_dialog` | 接受/关闭浏览器对话框 | `action`（接受/关闭） |
| `hover` | 在元素上悬停 | `uid` |
| `press_key` | 按下键盘键 | `key` |
| `upload_file` | 将文件上传到指定位置 | `uid`, `paths[]` |

### 导航（6个工具）

| 工具 | 功能 | 必需参数 |
|------|-------------|------------|
| `navigate_page` | 导航到指定URL | `url` |
| `new_page` | 打开新标签页 | `url` |
| `close_page` | 关闭当前标签页 | — |
| `list_pages` | 列出所有打开的标签页 | — |
| `select_page` | 切换到指定标签页 | `index` |
| `wait_for` | 等待元素或网络请求完成 | `event`, `uid`, `timeout` |

### 调试（5个工具）

| 工具 | 功能 | 描述 |
|------|-------------|
| `take_screenshot` | 捕获页面截图 |
| `take_snapshot` | 获取DOM结构或无障碍访问快照 |
| `evaluate_script` | 在页面中运行JavaScript代码 |
| `list_console_messages` | 查看控制台日志 |
| `get_console_message` | 获取特定的控制台消息 |

### 性能分析（3个工具）

| 工具 | 功能 | 描述 |
|------|-------------|
| `performance_start_trace` | 开始性能记录 |
| `performance_stop_trace` | 停止性能记录并获取数据 |
| `performance_analyze_insight` | 使用AI分析性能数据 |

### 网络监控（2个工具）

| 工具 | 功能 | 描述 |
|------|-------------|
| `list_network_requests` | 列出所有网络请求 |
| `get_network_request` | 获取请求和响应的详细信息 |

### 设备模拟（2个工具）

| 工具 | 功能 | 描述 |
|------|-------------|
| `emulate` | 模拟移动设备或平板设备 |
| `resize_page` | 调整视口大小 |

## 常见工作流程

### 测试网页
1. `navigate_page` → 导航到目标URL
2. `take_snapshot` → 获取页面元素的UUID
3. `click`/`fill` → 与页面元素交互
4. `take_screenshot` → 捕获测试结果

### 性能审计
1. `navigate_page` → 导航到目标URL
2. `performance_start_trace` → 开始性能记录
3. 与页面交互
4. `performance_stop_trace` → 停止性能记录
5. `performance_analyze_insight` → 分析性能数据

### 表单测试
1. `navigate_page` → 导航到包含表单的页面
2. `take_snapshot` → 识别表单字段
3. `fill_form` → 同时填写所有表单字段
4. `click` → 点击提交按钮
5. `take_screenshot` → 验证表单提交结果

## 隐私注意事项

- 谷歌会默认收集使用数据——可通过`--no-usage-statistics`选项禁用
- 性能分析工具可能会将相关数据发送到Google CrUX API——可通过`--no-performance-crux`选项禁用
- 请避免在浏览器会话中分享敏感信息
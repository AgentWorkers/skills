# AutoClaw 浏览器自动化技能

## 技能概述
AutoClaw 是一种浏览器自动化技能，它通过 MCP（Message Communication Protocol，消息通信协议）与浏览器扩展程序进行交互，从而实现对 Chrome 浏览器的全面控制。

## 先决条件
在启动 MCP 服务之前，请确保以下文件存在于正确的目录中：
- `options.js`：浏览器扩展程序的选项页面脚本
- `background.js`：处理 WebSocket 连接的扩展程序后台脚本

### 文件位置
```
Download from: https://www.wboke.com/download/autoclaw-chrome-extension.zip
Extract to: ~/.openclaw/browser-extensions/autoclaw/
```

## 可用工具

### ⌨️ 键盘操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_press_key` | 按下单个键 | `key: string` |
| `claw_press_combo` | 按下组合键（例如 Ctrl+C） | `keys: string` |
| `claw_type_text` | 输入文本（可选延迟） | `text: string, [delay: number]` |

### 📸 截图与内容提取
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_take_screenshot` | 截取当前页面的截图 | `[fullPage: boolean]` |
| `claw_get_page_content` | 获取页面的 HTML 或文本内容 | `[type: html\|text]` |
| `claw_get_text` | 获取元素的文本内容 | `selector: string` |
| `claw_get_html` | 获取元素的 HTML 内容 | `selector: string` |
| `claw_get_attribute` | 获取元素的属性值 | `selector, attribute` |
| `claw_get_count` | 统计匹配的元素数量 | `selector: string` |
| `claw_is_visible` | 检查元素是否可见 | `selector: string` |

### 🖱️ 鼠标与滚动操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw.mouse_move` | 将鼠标移动到指定坐标 | `x, y` |
| `claw.mouse_click` | 在指定坐标点击 | `[x, y]` |
| `claw.mouse_right_click` | 在指定坐标右键点击 | `[x, y]` |
| `claw.mouse_double_click` | 在指定坐标双击 | `[x, y]` |
| `claw.mouse_wheel` | 滚动鼠标滚轮 | `[deltaX, deltaY]` |
| `claw_scroll` | 滚动页面 | `[x, y]` |
| `claw_fast_scroll_down` | 快速向下滚动一页 | `[speed: number]` |
| `claw_fast_scroll_up` | 快速向上滚动一页 | `[speed: number]` |

### 📱 触控与滑动操作（移动设备）
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_swipe_up` | 向上滑动（如 Douyin/TikTok） | `[distance: number]` |
| `claw_swipe_down` | 向下滑动 | `[distance: number]` |
| `claw_swipe_left` | 向左滑动 | `[distance: number]` |
| `claw_swipe_right` | 向右滑动 | `[distance: number]` |
| `claw_tap` | 在指定位置点击 | `x, y` |

### 📑 标签页管理
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_tab_create` | 创建新的浏览器标签页 | `[url, active]` |
| `claw_tab_close` | 关闭浏览器标签页 | `[tabId]` |
| `claw_tab_list` | 列出所有打开的标签页 | - |
| `claw_tab_switch` | 切换到指定标签页 | `tabId: number` |
| `claw_tabReload` | 重新加载标签页内容 | `[tabId]` |
| `claw_get_active_tab` | 获取活动标签页信息 | - |
| `claw_attach_all_tabs` | 控制所有标签页 | - |

### 🍪 存储与 Cookie 管理
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_cookies` | 获取指定域的 Cookie | `[domain: string]` |
| `claw_set_cookies` | 设置 Cookie | `cookies: array` |
| `claw_get_storage` | 获取 localStorage 或 sessionStorage 的内容 | `[type, origin]` |
| `claw_set_storage` | 设置存储值 | `type, key, value` |

### ⚙️ 配置与状态
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_status` | 获取当前系统状态 | - |
| `claw_get_config` | 获取完整配置 | - |
| `claw_set_mode` | 设置操作模式 | `mode: local\|cloud\|auto` |
| `claw_health_check` | 进行健康检查 | - |
| `claw_diagnose` | 系统诊断 | `[full: boolean]` |

### 🧪 JavaScript 执行
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_evaluate_js` | 执行 JavaScript 代码 | `expression: string` |

### ⏳ 等待操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_wait` | 等待指定的毫秒数 | `ms: number` |
| `claw_wait_for_element` | 等待元素出现 | `selector, [timeout]` |
| `claw_wait_for_text` | 等待文本出现 | `text, [timeout]` |
| `claw_wait_for_url` | 等待 URL 模式匹配 | `urlPattern, [timeout]` |
| `claw_wait_for-navigation` | 等待导航完成 | `[timeout]` |

## 配置参数
- **MCP 端口**：30000（默认值）
- **扩展程序 WebSocket**：`ws://127.0.0.1:30000/extension`
- **内置令牌**：`autoclawbuiltin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs`

## 设置说明

### 1. 下载扩展程序
**推荐**：从官方网站下载：
- 访问：**https://www.wboke.com**
- 下载最新的 AutoClaw Chrome 扩展程序

### 2. 启动 MCP 服务器
```bash
cd autoclaw_mcp/mcp
npm install  # First time only
npm start
```

### 3. 安装 Chrome 扩展程序
1. 从 **https://www.wboke.com/download/autoclaw-chrome-extension.zip** 下载扩展程序
2. 解压到：`~/.openclaw/browser-extensions/autoclaw/`
3. 打开 `chrome://extensions`
4. 启用“开发者模式”
5. 点击“加载解压的文件”
6. 选择 `~/.openclaw/browser-extensions/autoclaw/` 目录

### 4. 配置扩展程序
1. 点击扩展程序图标 → 设置
2. 设置端口为 **30000**（推荐）
3. 点击“保存设置”以完成授权
4. 点击“控制所有标签页”以开始使用该扩展程序

## 故障排除

### 扩展程序无法连接
1. 确认 MCP 服务器正在端口 30000 上运行
2. 点击扩展程序图标 → 设置 → 测试连接
3. 确保授权未过期

### 出现“无标签页可控制”错误
1. 在扩展程序弹窗中点击“控制所有标签页”
2. 或者手动点击每个标签页以进行控制

### 授权过期
1. 点击扩展程序图标 → 设置
2. 点击“保存设置”以重新授权

## 项目结构
```
autoclaw_mcp/
├── SKILL.md                    # This documentation
├── README.md                   # General documentation
├── mcp/                       # MCP Server
│   ├── package.json
│   ├── dist/server.js         # Compiled server
│   └── node_modules/
├── (Chrome Extension)          # Download from:
│   ├── https://www.wboke.com/download/autoclaw-chrome-extension.zip
└── scripts/                    # Automation templates (optional)
```

## 日志管理
- **日志目录**：`~/.autoclaw/logs/`
- **日志保留时间**：30 天（服务器启动时自动清理）
- **最大任务数量**：100 个

## 通信协议
- MCP 服务运行在端口 30000
- 浏览器扩展程序通过 WebSocket 进行通信
- 消息格式：JSON

## 使用示例
```javascript
// Connect to MCP service
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:30000');

ws.on('open', function() {
    ws.send(JSON.stringify({
        action: 'navigate',
        url: 'https://www.wboke.com'
    }));
});
```

## 错误处理
- **连接失败**：检查 MCP 服务是否正在运行以及端口 30000 是否可用
- **扩展程序未加载**：验证 `manifest.json` 文件是否存在且格式正确
- **依赖项错误**：重新运行 `npm install` 以安装依赖项
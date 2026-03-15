# AutoClaw 浏览器自动化技能

## 技能概述

AutoClaw 是一种浏览器自动化技能，它通过 MCP（Message Communication Protocol，消息通信协议）与浏览器扩展程序进行交互，从而实现对 Chrome 浏览器的全面控制。

## 先决条件

在启动 MCP 服务之前，请确保以下文件存在于正确的目录中：
- `options.js`：浏览器扩展程序的选项页面脚本
- `background.js`：扩展程序的背景脚本，用于处理 WebSocket 连接

### 文件位置
```
%USERPROFILE%\.openclaw\skills\claw-browser\autoclaw-plugin\
```

## 🚀 v6.0.0 新优化工具

### 简化 DOM 检索
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_indexed_elements` | 获取页面的简化 DOM（已索引的交互元素），数据量减少 90% 以上 | `[useCache: boolean]` |

### 按索引点击元素
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_click_by_index` | 按索引点击元素，比使用 CSS 选择器更稳定 | `index: number` |

### 批量操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_batch_execute` | 批量执行多个 CDP 命令，减少网络请求次数 | `commands: array` |

### 智能等待
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_smart_wait` | 智能等待：支持等待元素、文本或 URL 出现 | `element/text/urlPattern, timeout` |

## 可用工具

### ⌨️ 键盘操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_press_key` | 按下单个键 | `key: string` |
| `claw_press_combo` | 按下键组合（例如 Ctrl+C） | `keys: string` |
| `claw_type_text` | 输入文本（可选延迟） | `text: string, [delay: number]` |
| `claw_key_down` | 键下 | `key: string` |
| `claw_key_up` | 键上 | `key: string` |

### 📸 截图与内容提取
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_take_screenshot` | 截取当前页面的截图 | `[fullPage: boolean]` |
| `claw_get_page_content` | 获取页面的 HTML 或文本内容 | `[type: html\|text]` |
| `claw_get_text` | 获取元素的文本内容 | `selector: string` |
| `claw_get_html` | 获取元素的 HTML 内容 | `selector: string` |
| `claw_get_attribute` | 获取元素的属性值 | `selector, attribute` |
| `claw_is_visible` | 检查元素是否可见 | `selector: string` |
| `claw_is_enabled` | 检查元素是否启用 | `selector: string` |

### 🖱️ 鼠标与滚动操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw.mouse_move` | 将鼠标移动到指定坐标 | `x, y` |
| `claw.mouse_click` | 在指定坐标处左键点击 | `[x, y]` |
| `claw.mouse_right_click` | 在指定坐标处右键点击 | `[x, y]` |
| `claw.mouse_double_click` | 在指定坐标处双击 | `[x, y]` |
| `claw.mouse_down` | 鼠标按钮按下 | `button, x, y` |
| `claw.mouse_up` | 鼠标按钮释放 | `[button]` |
| `claw.mouse_wheel` | 鼠标滚轮滚动 | `[deltaX, deltaY]` |
| `claw_scroll` | 滚动页面 | `[x, y]` |
| `claw_fast_scroll_down` | 快速向下滚动一页 | `[speed: number]` |
| `claw_fast_scroll_up` | 快速向上滚动一页 | `[speed: number]` |
| `claw_hover_element` | 将鼠标悬停在元素上 | `selector: string` |
| `claw_scroll_to_element` | 将元素滚动到视图中心 | `selector: string` |

### 📱 触控与滑动操作（移动设备）
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_swipe_up` | 向上滑动（抖音/TikTok 动作） | `[distance: number]` |
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
| `claw_attach_all_tabs` | 集中控制所有标签页 | - |

### 📁 书签管理
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_bookmarks` | 获取所有书签（扁平列表） | - |
| `claw_get_bookmark_tree` | 获取完整的书签树结构 | - |
| `claw_search_bookmarks` | 按关键词搜索书签 | `query: string` |
| `claw_create_bookmark` | 创建新书签 | `title, url, [parentId]` |
| `claw_update_bookmark` | 更新书签标题或 URL | `id, [title, url]` |
| `claw_rename_bookmark` | 重命名书签或文件夹 | `id, title` |
| `claw_delete_bookmark` | 删除单个书签 | `id: string` |
| `claw_remove_folder` | 递归删除书签文件夹 | `id: string` |
| `claw_create_folder` | 创建新的书签文件夹 | `title, [parentId]` |
| `claw_move_bookmark` | 将书签移动到另一个文件夹 | `id, parentId` |

### 🍪 存储与 Cookie
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_cookies` | 获取指定域的 Cookie | `[domain: string]` |
| `claw_set_cookies` | 设置 Cookie | `cookies: array` |
| `claw_get_storage` | 获取 localStorage/sessionStorage | `[type, origin]` |
| `claw_set_storage` | 设置存储值 | `type, key, value` |

### 🧪 JavaScript 执行
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_evaluate_js` | 在页面中执行 JavaScript 代码 | `expression: string` |

### ⏳ 等待操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_wait` | 等待指定毫秒数 | `ms: number` |
| `claw_wait_for_element` | 等待元素出现 | `selector, [timeout]` |
| `claw_wait_for_text` | 等待文本出现 | `text, [timeout]` |
| `claw_wait_for_url` | 等待 URL 模式匹配 | `urlPattern, [timeout]` |
| `claw_wait_for_navigation` | 等待导航完成 | `[timeout]` |
| `claw_smart_wait` | 智能等待（新功能） | `element/text/urlPattern, timeout` |

### 🔧 元素操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_click_element` | 点击页面元素（CSS 选择器） | `selector: string` |
| `claw_fill_input` | 向输入框中填充文本 | `selector, text` |
| `claw_clear_input` | 清空输入框 | `selector: string` |
| `claw_select_option` | 选择下拉菜单选项 | `selector, value` |
| `claw_check` | 勾选复选框 | `selector: string` |
| `claw_uncheck` | 取消选中复选框 | `selector: string` |
| `claw_focus_element` | 将焦点放在元素上 | `selector: string` |
| `claw_upload_file` | 上传文件到输入框 | `selector, filePath` |

### 🧠 智能操作（增强版）
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_smart_click` | 智能点击：尝试使用选择器→文本→坐标 | `selector/text/x+y, timeout` |
| `claw_find_elements` | 查询页面上所有匹配的元素 | `selector, [limit]` |
| `claw_wait_and_click` | 等待元素出现后点击 | `selector, timeout, scrollIntoView` |
| `claw_get_page_structure` | 获取页面的关键结构摘要 | `includeLinks/Buttons/Inputs, maxItems` |
| `claw_batch_extract` | 批量提取多个选择器的内容 | `selectors, options` |
| `claw_extract_table` | 将 HTML 表格提取为 JSON | `[selector, includeHeader]` |
| `claw_extract_list` | 提取列表类型数据 | `containerSelector, fields, limit` |

### 📊 任务与日志管理
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_new_task` | 创建新任务 | `[name: string]` |
| `claw_complete_task` | 完成任务 | `[success: boolean]` |
| `claw_switch_task` | 切换到指定任务 | `taskId: number` |
| `claw_list_tasks` | 列出所有任务 | - |
| `claw_get_task_logs` | 获取指定任务的日志 | `[taskId, limit]` |
| `claw_get_action_logs` | 获取当前任务的日志 | `[limit]` |

### ⚙️ 配置与状态
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_get_status` | 获取当前系统状态 | - |
| `claw_get_config` | 获取完整配置 | - |
| `claw_set_mode` | 设置操作模式 | `mode: local\|cloud\|auto` |
| `claw_health_check` | 进行健康检查 | - |
| `claw_diagnose` | 系统诊断 | `[full: boolean]` |

### 🌐 导航操作
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_navigate` | 打开 URL | `url, [newTab]` |
| `claw_open_urls` | 批量打开多个 URL | `urls, [delayMs]` |
| `claw_go_back` | 向后翻一页 | - |
| `claw_go_forward` | 向前翻一页 | - |
| `clawReload_page` | 重新加载页面 | `[hard: boolean]` |

### 💾 登录会话管理
| 工具 | 描述 | 参数 |
|------|-------------|------------|
| `claw_save_login_session` | 保存当前页面的登录状态 | `name, [domain]` |
| `claw_restore_login_session` | 恢复保存的登录状态 | `name: string` |
| `claw_list_login_sessions` | 列出所有保存的会话 | - |

## 配置

- **MCP 端口**：30000（默认值，可自定义）
- **扩展程序 WebSocket**：`ws://127.0.0.1:{port}/extension`
- **内置令牌**：`autoclawbuiltin_Q0hpK2oV4F9tlwbYX3RELxiJNGDvayr8OPqZzkfs`
- **自定义令牌**：支持（留空使用内置令牌）

## 安装步骤

### 1. 启动 MCP 服务器
```bash
cd %USERPROFILE%\.openclaw\skills\autoclaw_wboke\mcp
npm install  # First time only
npm start
```

### 2. 安装 Chrome 扩展程序
1. 打开 `chrome://extensions`
2. 启用“开发者模式”
3. 点击“加载解压文件”
4. 选择 `autoclaw-plugin/` 目录

### 3. 配置扩展程序
1. 点击扩展程序图标 → 设置
2. 设置端口（默认值：**30000**）
3. 输入自定义令牌（可选，留空使用内置令牌）
4. 点击“保存设置”以授权
5. 点击“附加所有标签页”

## v6.0.0 性能优化

| 优化项 | 优化前 | 优化后 | 效果 |
|--------------|--------|-------|--------|
| CDP 域名 | 每次启用所有 4 个域名 | 只启用 2 个基础域名，其他域名按需启用 | 资源使用量 ↓30% |
| 连接轮询 | 每 5 秒检查一次 | 每 30 秒检查一次 | CPU/网络使用量 ↓40% |
| 弹出窗口轮询 | 每 3 秒刷新一次 | 每 10 秒刷新一次 | 电池/资源使用量 ↓ |
| DOM 缓存 | 无 | 在 15 秒内重用数据 | 请求次数 ↓50% |

## 项目结构
```
autoclaw_wboke/
├── SKILL.md                    # This documentation
├── README.md                   # Main documentation
├── mcp/                       # MCP Server
│   ├── package.json
│   ├── dist/server.js         # Compiled server (v5.2.0) ⭐
│   └── node_modules/
├── autoclaw-plugin/           # Chrome Extension
│   ├── manifest.json
│   ├── background.js          # Background script (v6.0.0) ⭐
│   ├── popup.js               # Popup UI
│   └── options.js             # Settings UI
└── scripts/                   # Automation script templates
    ├── 抖音点赞.json
    ├── 批量截图.json
    └── 自动搜索.json
```

## 日志管理

- **日志目录**：`~/.autoclaw/logs/`
- **保留时间**：30 天（服务器启动时自动清理）
- **最大任务数**：100 个

## 通信协议

- MCP 服务运行在可自定义的端口上（默认：30000）
- 浏览器扩展程序通过 WebSocket 进行通信
- 消息格式：JSON

## 故障排除

### 扩展程序未连接
1. 确认 MCP 服务器正在运行
2. 点击扩展程序图标 → 设置 → 测试连接
3. 确保授权未过期

### 出现“未附加标签页”错误
1. 在扩展程序弹窗中点击“附加所有标签页”
2. 或手动点击每个标签页以附加它们

### 授权过期
1. 点击扩展程序图标 → 设置
2. 点击“保存设置”以重新授权

### 性能问题
- v6.0.0 版本优化了资源使用效率
- 如果问题仍然存在，请尝试重启 MCP 服务

## 使用示例
```javascript
// Connect to MCP service
const WebSocket = require('ws');
const ws = new WebSocket('ws://localhost:30000');

ws.on('open', function() {
    // Navigate to webpage
    ws.send(JSON.stringify({
        action: 'navigate',
        url: 'https://www.example.com'
    }));
    
    // Get simplified DOM (recommended)
    ws.send(JSON.stringify({
        name: 'claw_get_indexed_elements',
        arguments: { useCache: true }
    }));
});
```

## 错误处理

- **连接失败**：检查 MCP 服务是否正在运行以及端口是否可用
- **扩展程序未加载**：确认 `manifest.json` 文件存在且格式正确
- **依赖项错误**：重新运行 `npm install` 以安装依赖项
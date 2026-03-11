---
name: clawdos
description: "通过Clawdos API实现Windows自动化：支持屏幕截图、鼠标/键盘操作、窗口管理、文件系统操作以及shell命令执行。适用于用户需要远程控制或检查Windows主机的情况。"
metadata: {"openclaw": {"emoji": "🐾", "requires": {"env": ["CLAWDOS_API_KEY", "CLAWDOS_BASE_URL"]}, "primaryEnv": "CLAWDOS_API_KEY"}}
---
## Clawdos Windows 执行接口

该功能提供了 18 个工具，允许您通过运行在 `CLAWDOS_BASE_URL`（默认为 `http://127.0.0.1:17171`）上的 Clawdos REST API 来操作 Windows 机器。

### ⚠️ 要求
**使用此功能需要在您的 Windows 机器上运行相应的服务器。**  
请在此处下载并按照说明进行安装：[danzig233/clawdos](https://github.com/danzig233/clawdos.git)

### 工具分组

| 分组 | 工具                |
|---|-------------------|
| 状态检查 | `health_check`, `get_env`       |
| 屏幕操作 | `screen_capture`        |
| 输入操作 | `mouse_click`, `mouse_move`, `mouse_drag`, `mouse_scroll`, `key_combo`, `type_text`, `input_batch` |
| 窗口操作 | `window_list`, `window_focus`      |
| 文件系统操作 | `fs_list`, `fs_read`, `fs_write`, `fs_mkdir`, `fs_delete`, `fs_move` |
| shell 操作 | `shell_exec`         |

### 认证
所有需要认证的接口请求都必须包含 `X-Api-Key` 头部字段，其值应与主机上的 `clawdos-config.json` 文件中设置的值相匹配。

### 可视化反馈循环与精度控制
当需要高精度操作时（例如点击小按钮或特定文本），请遵循以下 **“移动-验证-修正”** 循环：
1. **移动**：使用 `mouse_move` 将光标移动到目标坐标。
2. **验证**：立即使用 `screen_capture` 查看光标相对于 UI 元素的实际位置。
3. **修正**：如果光标位置有偏差，计算像素差异，并使用修正后的坐标再次执行 `mouse_move`。
4. **执行操作**：只有在确认光标位置正确后，才执行 `mouse_click`。

**缩放说明**：请始终通过 `get_env` 获取当前屏幕分辨率，并将其与输入工具的参数 `view_width` 和 `view_height` 一起使用，以实现坐标自动缩放。

### 安全注意事项
- `shell_exec` 功能仅在服务器端执行；仅允许使用白名单中的命令。
- 所有文件系统操作（`fs_*`）都在 Clawdos 配置中指定的 `workingDirs` 目录内进行；如果路径包含特殊字符，系统会返回 403 错误。
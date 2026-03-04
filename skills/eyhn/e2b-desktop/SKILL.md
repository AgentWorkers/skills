---
name: e2b-desktop
description: >
  **控制 E2B Desktop 沙箱（虚拟 Linux 桌面环境）以供计算机使用代理使用**  
  当您需要创建/管理沙箱化的桌面环境、截取屏幕截图、执行鼠标/键盘操作、运行命令、流式传输 VNC 输出，或使用 E2B Desktop SDK 构建计算机使用代理时，请使用此功能。
---
# E2B桌面技能

通过`e2b-desktop` Python SDK来控制一个无头Linux桌面（Ubuntu + XFCE）。
所有脚本都位于`scripts/`目录中，并使用bash脚本包装SDK，以便于代理程序的使用。

## 先决条件

```bash
pip install e2b-desktop
export E2B_API_KEY=e2b_***
```

## 状态管理

- `start_sandbox.sh`将沙箱ID保存到`~/.e2b_state`文件中。
- 所有其他脚本都会从该文件中自动加载沙箱ID。
- 可以通过`export E2B_SANDBOX_ID=<id>`来覆盖默认值。
- 沙箱状态在脚本退出后仍然保留——可以通过`Sandbox.connect(sandbox_id)`重新连接。

## 脚本

| 脚本 | 用途 | 描述 |
|---|---|---|
| `start_sandbox.sh` | `[--resolution 1280x800] [--timeout 300] [--stream]` | 创建沙箱；可选地启动VNC流 |
| `kill_sandbox.sh` | `[SANDBOX_ID]` | 终止沙箱并清除状态信息 |
| `screenshot.sh` | `[OUTPUT_FILE]` | 截取屏幕截图（默认保存为`/tmp/e2b_screenshot.png`） |
| `click.sh` | `X Y` | 在指定坐标处执行左键点击 |
| `right_click.sh` | `X Y` | 在指定坐标处执行右键点击 |
| `double_click.sh` | `X Y` | 在指定坐标处执行双击 |
| `middle_click.sh` | `X Y` | 在指定坐标处执行鼠标中键点击 |
| `move_mouse.sh` | `X Y` | 移动鼠标光标（不执行点击操作） |
| `drag.sh` | `X1 Y1 X2 Y2` | 在两个点之间拖动鼠标 |
| `scroll.sh` | `AMOUNT` | 滚动屏幕（正数表示向上滚动，负数表示向下滚动） |
| `type_text.sh` | `"text"` | 在当前光标位置输入文本 |
| `press_key.sh` | `KEY [KEY2...]` | 按下指定的键或键组合（例如`ctrl c`） |
| `run_command.sh` | `"cmd"` | 在沙箱内运行shell命令 |
| `open_url.sh` | `URL_OR_PATH` | 在默认应用程序中打开指定的URL或文件 |
| `launch_app.sh` | `APP_NAME` | 启动指定的应用程序（例如`firefox`、`vscode`） |
| `stream_start.sh` | `[--auth]` | 启动VNC流；`--auth`参数用于启用密码保护 |
| `stream_stop.sh` | _(无参数)_ | 停止VNC流 |
| `get_cursor.sh` | _(无参数)_ | 输出鼠标光标的坐标（`CURSOR_X`和`CURSOR_Y`） |
| `get_screen_size.sh` | _(无参数)_ | 输出屏幕的分辨率（`SCREEN_WIDTH`和`SCREEN_HEIGHT`） |
| `list_windows.sh` | `[APP_NAME]` | 列出所有打开的应用程序窗口或显示当前活动窗口 |
| `wait.sh` | `MILLISECONDS` | 等待指定的毫秒数（在沙箱端执行） |

## 代理程序的运行模式

```bash
SCRIPTS="skills/e2b-desktop/scripts"

# 1. Start sandbox
source <($SCRIPTS/start_sandbox.sh --resolution 1280x800 --stream)
echo "Sandbox: $SANDBOX_ID"
echo "View at: $STREAM_URL"

# 2. Agent loop
while true; do
  # Capture screen
  $SCRIPTS/screenshot.sh /tmp/screen.png

  # Send to LLM, parse action... (your code)
  ACTION=$(llm_decide /tmp/screen.png)

  case "$ACTION" in
    click:*)   IFS=: read -r _ x y <<< "$ACTION"; $SCRIPTS/click.sh $x $y ;;
    type:*)    $SCRIPTS/type_text.sh "${ACTION#type:}" ;;
    key:*)     $SCRIPTS/press_key.sh ${ACTION#key:} ;;
    done)      break ;;
  esac
done

# 3. Clean up
$SCRIPTS/kill_sandbox.sh
```

## 重要说明

- `scroll.sh AMOUNT`：正数表示向上滚动，负数表示向下滚动（与`desktop.scroll(amount)` API兼容）。
- `press_key.sh ctrl c`：多个参数会通过`desktop.press(["ctrl", "c"])`组合成实际的按键操作。
- `run_command.sh`会跟随沙箱内运行的命令的退出代码一起退出。
- 所有与鼠标坐标相关的脚本都接受与沙箱分辨率相匹配的整数像素坐标。
- VNC流：同一时间只能有一个活动流；在切换窗口之前会先停止当前的VNC流。
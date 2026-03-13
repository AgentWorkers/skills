---
name: duoplus-agent
displayName: DuoPlus CloudPhone Agent
description: 通过ADB广播命令控制安卓云手机：执行点击、滑动、输入文本、截图等操作，以及读取用户界面元素。设备上必须运行DuoPlus CloudPhone服务。
version: 1.0.9
license: MIT-0
metadata:
  clawdbot:
    emoji: "📱"
    requires:
      bins: ["adb", "cwebp"]
changelog: Restructure SKILL.md, add cwebp compression, use uiautomator for UI analysis
---# DuoPlus CloudPhone Agent

使用ADB广播命令来控制和自动化DuoPlus云手机的操作。

欲了解更多信息，请访问[DuoPlus官方网站](https://www.duoplus.net/)。

## 连接设备

### 无线连接
```bash
adb connect <IP>:<PORT>
adb devices -l
```

后续所有命令都会使用`-s <DEVICE_ID>`来指定目标设备。

## 常见工作流程

### 启动应用程序
```bash
scripts/send_command.sh <DEVICE_ID> '{"action_name":"OPEN_APP","params":{"package_name":"com.tencent.mm"}}'
```

### 分析用户界面（UI）
- 将UI层次结构导出并提取元素坐标及属性：
  ```bash
adb -s <DEVICE_ID> shell uiautomator dump /sdcard/view.xml && adb -s <DEVICE_ID> pull /sdcard/view.xml ./view.xml
```
  - 然后使用`grep`命令查找包含`bounds="[x1,y1][x2,y2]"`的文本或资源ID。

### 与元素交互

所有交互操作都通过辅助脚本以JSON格式的命令发送：
- **点击坐标**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"CLICK_COORDINATE","params":{"x":500,"y":500}}'`
- **根据文本点击元素**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"CLICK_ELEMENT","params":{"text":"Login"}}'`
  - 可选参数：`resource_id`、`class_name`、`content_desc`、`element_order`（从0开始的索引）
- **长按**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"LONG_COORDINATE","params":{"x":500,"y":500,"duration":1000}}'`
- **双击**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"DOUBLE_TAP_COORDINATE","params":{"x":500,"y":500}}'`
- **输入文本**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"INPUT_CONTENT","params":{"content":"Hello","clear_first":true}}'`
  - 需要先点击输入框使其获得焦点
- **键盘按键**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"KEYBOARD_OPERATION","params":{"key":"enter"}}'`
  - 支持的按键：enter、delete、tab、escape、space
- **滑动**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"SLIDE_PAGE","params":{"direction":"up","start_x":487,"start_y":753,"end_x":512,"end_y":289}}'`
  - `direction`：up/down/left/right（必填）。坐标为可选参数。
- **返回主屏幕**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"GO_TO_HOME","params":{}}'`
- **返回上一页面**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"PAGE_BACK","params":{}}'`
- **等待**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"WAIT_TIME","params":{"wait_time":3000}}'`
- **等待元素加载完成**：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"WAIT_FOR_selector","params":{"text":"Loading complete","timeout":10000}}'`
- **结束任务**（仅在操作卡住时使用）：`scripts/send_command.sh <DEVICE_ID> '{"action_name":"END_TASK","params":{"success":false,"message":"reason"}}'`

所有操作命令均为一次性执行，不会返回结果。请在每次操作后截图以验证结果。

### 可视化验证

- 截取屏幕截图，使用`cwebp`工具压缩后保存到本地进行分析：
  ```bash
# Take screenshot on device
adb -s <DEVICE_ID> shell screencap -p /sdcard/screen.png

# Pull to local
adb -s <DEVICE_ID> pull /sdcard/screen.png ./screen.png

# Compress to WebP for smaller file size (optional, recommended for vision model)
cwebp -q 60 -resize 540 0 ./screen.png -o ./screen.webp
```

如果`cwebp`不可用，可以直接使用PNG格式的截图。

## 命令的工作原理（内部机制）

命令通过ADB广播以Base64编码的JSON格式发送。辅助脚本`scripts/send_command.sh`会自动处理这一过程：
```bash
# Usage: scripts/send_command.sh <DEVICE_ID> <ACTION_JSON>
scripts/send_command.sh 192.168.1.100:5555 '{"action_name":"CLICK_ELEMENT","params":{"text":"Login"}}'
```

该脚本会构建完整的请求数据（包括任务类型、任务ID、MD5哈希值等），对其进行Base64编码，然后通过ADB广播发送：
```bash
adb -s <DEVICE_ID> shell am broadcast -a com.duoplus.service.PROCESS_DATA --es message "<BASE64>"
```

## 典型工作流程
```
1. Analyze UI    → uiautomator dump to find elements, or screenshot for visual analysis
2. Execute action → send_command.sh with the appropriate action JSON
3. Wait 1-3s     → Let the action take effect
4. Verify        → Screenshot + cwebp compress, or uiautomator dump again
5. Repeat 2-4 until all requested steps are completed
```

## 提示：
- **坐标系统**：坐标范围为0-1000（左上角=0,0，右下角=1000,1000），单位为相对位置，而非像素。
- **元素匹配**：尽可能使用`CLICK_ELEMENT`（根据文本匹配）；如果文本匹配失败，则使用`CLICK_COORDINATE`。
- **输入操作**：必须先点击输入框（使用`CLICK_COORDINATE`或`CLICK_ELEMENT`使其获得焦点，然后再输入内容。
- **提交**：输入完成后，使用`KEYBOARD_OPERATION(key="enter")`进行提交。
- **等待**：在发送命令之间使用`sleep 1-3`命令让UI有时间更新。请勿在设备上直接使用shell的`sleep`命令。
- **滑动操作**：滑动坐标应使用非整数（避免使用500、800这样的固定值），并在连续滑动时改变坐标值。
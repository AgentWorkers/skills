---
name: duoplus-agent
displayName: DuoPlus CloudPhone Agent
description: 通过ADB（Android Debug Bridge）控制安卓云手机：执行点击、滑动、输入文本、截图等操作，以及读取用户界面元素的内容。同时，可以向正在运行的DuoPlus云手机发送控制命令。
version: 1.0.0
license: MIT-0
metadata:
  clawdbot:
    emoji: "📱"
    requires:
      bins: ["adb"]
changelog: change send_command.sh
---# DuoPlus CloudPhone Agent  
通过ADB广播命令远程控制Android云手机。目标设备必须运行**DuoPlus CloudPhone**。  

如需了解有关我们产品及服务的更多信息，请访问[DuoPlus官方网站](https://www.duoplus.net/)。  

## 连接  
在执行任何操作之前，请先连接到设备：  
```bash
# List available devices
adb devices -l

# Connect to remote device (if needed)
adb connect <IP>:<PORT>
```  

所有后续命令都会使用`-s <DEVICE_ID>`来指定目标设备。  

## 环境检查  
该功能仅适用于Service版本大于或等于2.0.0的DuoPlus云手机。在使用任何命令之前，请确认设备兼容性：  
```bash
# Check if device is a supported DuoPlus cloud phone
scripts/check_env.sh <DEVICE_ID>

# Or without device ID (uses default connected device)
scripts/check_env.sh
```  

脚本会检查设备上的`/data/misc/dplus/version`文件。如果文件不存在或版本低于2.0.0，则表示设备不支持该功能。您也可以手动进行检查：  
```bash
adb -s <DEVICE_ID> shell cat /data/misc/dplus/version
```  

## 命令的工作原理  
命令以Base64编码的JSON格式通过ADB广播发送：  
```bash
# 1. Build JSON payload
JSON='{"task_type":"ai","action":"execute","task_id":"TASK_ID","md5":"MD5","action_name":"ACTION","params":{...}}'

# 2. Base64 encode
BASE64=$(echo -n "$JSON" | base64 -w 0)

# 3. Send broadcast
adb -s <DEVICE_ID> shell am broadcast -a com.duoplus.service.PROCESS_DATA --es message "$BASE64"
```  

每次会话都会生成一个唯一的`task_id`（例如`openclaw-$(date +%s)`，并使用固定的md5哈希值（如`openclaw-md5`）进行标识。  

## 响应模型  
命令分为两种类型，其响应方式也有所不同：  

### 查询命令（同步响应）  
`get_ui_state`是唯一的查询命令。广播接收器会在广播结果数据中直接返回JSON响应，其中包含UI元素描述和Base64编码的截图。您可以从广播输出中读取响应内容。  

### 动作命令（一次执行完毕）  
所有`action: "execute"`类型的命令（如`CLICK_COORDINATE`、`INPUT_CONTENT`、`SLIDE_PAGE`等）均为“一次执行完毕”类型的命令，它们不会返回执行结果。发送动作命令后，请执行以下操作：  
1. 等待1-3秒，直到操作完成。  
2. 调用`get_ui_state`来查看当前屏幕状态并验证结果。  

## 可用的操作  

### 截图（会返回响应）  
**PAGE_SCREENSHOT** – 截取压缩后的屏幕截图，并可选择将其保存到指定路径：  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"PAGE_SCREENSHOT","params":{"save_path":"/sdcard/screenshot.webp"}}'
```  
- `save_path`（可选）：设备上的文件路径（也可使用`path`作为别名）。如果省略，截图将以Base64格式直接包含在响应中。  
响应JSON包含：  
- `screenshot`：Base64编码的压缩图像  
- `result_text`：成功时保存的文件路径；失败时显示错误信息。如果未指定`save_path`，则此字段为空。  

要从设备上获取保存的文件，请执行：  
```bash
adb -s <DEVICE_ID> pull /sdcard/screenshot.webp ./screenshot.webp
```  

### 屏幕信息获取（会返回响应）  
**get_ui_state** – 获取屏幕上的所有交互式UI元素及其压缩后的截图（以Base64格式）：  
```bash
JSON='{"task_type":"ai","action":"get_ui_state","task_id":"ID","md5":"MD5","lang":"en"}'
```  
注意：此操作使用`action: "get_ui_state"`（而非`action: "execute"`）。  
响应JSON包含：  
- `success`：布尔值，表示操作是否成功  
- `message`：屏幕上所有交互式UI元素的文本描述  
- `screenshot`：当前屏幕的Base64编码压缩图像  
- `current_app`：当前前台应用的包名  

这是查看设备屏幕内容的主要方法。在每个操作前后都应使用该命令以确保操作效果正确。  

### 导航操作（一次执行完毕）  
**GO_TO_HOME** – 点击主页按钮  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"GO_TO_HOME","params":{}}'
```  
**PAGE_BACK** – 点击返回按钮  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"PAGE_BACK","params":{}}'
```  
**OPEN_APP** – 根据应用包名启动应用  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"OPEN_APP","params":{"package_name":"com.tencent.mm"}}'
```  

### 点击与触摸操作（一次执行完毕）  
**CLICK_COORDINATE** – 在指定坐标处点击（坐标范围为0-1000，左上角为(0,0)，右下角为(1000,1000)：  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"CLICK_COORDINATE","params":{"x":500,"y":500}}'
```  
**CLICK_ELEMENT** – 根据文本、`resource_id`或`content_desc`点击UI元素：  
- 可选参数：`resource_id`、`class_name`、`content_desc`、`element_order`（多个匹配项时的索引，从0开始计数）  
**LONG_COORDINATE** – 长按指定坐标  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"LONG_COORDINATE","params":{"x":500,"y":500,"duration":1000}}'
```  
**DOUBLE_TAP_COORDINATE** – 双击指定坐标  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"DOUBLE_TAP_COORDINATE","params":{"x":500,"y":500}}'
```  

### 输入操作（一次执行完毕）  
**INPUT_CONTENT** – 在焦点输入框中输入文本（需先点击输入框）：  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"INPUT_CONTENT","params":{"content":"Hello","clear_first":true}}'
```  
**KEYBOARD_OPERATION** – 按下键盘键（回车/删除/制表/退出/空格）  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"KEYBOARD_OPERATION","params":{"key":"enter"}}'
```  

### 滑动操作（一次执行完毕）  
**SLIDE_PAGE** – 根据指定坐标滑动屏幕：  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"SLIDE_PAGE","params":{"direction":"up","start_x":500,"start_y":750,"end_x":500,"end_y":300}}'
```  
- `direction`：向上/向下/向左/向右（必填）  
- 坐标可选；如果省略，则使用默认的滑动方向  

### 等待操作（一次执行完毕）  
**WAIT_TIME** – 等待指定毫秒数  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"WAIT_TIME","params":{"wait_time":3000}}'
```  
**WAIT_FOR_selector** – 等待指定元素出现  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"WAIT_FOR_SELECTOR","params":{"text":"Loading complete","timeout":10000}}'
```  

### 任务控制（一次执行完毕）  
**END_TASK** – 标记任务完成  
```bash
JSON='{"task_type":"ai","action":"execute","task_id":"ID","md5":"MD5","action_name":"END_TASK","params":{"success":true,"message":"Done"}}'
```  

## 辅助脚本  
使用辅助脚本`scripts/send_command.sh`可更便捷地发送命令：  
```bash
# Usage: scripts/send_command.sh <DEVICE_ID> <ACTION_JSON>
scripts/send_command.sh 192.168.1.100:5555 '{"action_name":"CLICK_ELEMENT","params":{"text":"Login"}}'
```  

## 典型工作流程  
```
0. check_env.sh <DEVICE>  → Verify device is a supported DuoPlus cloud phone (v2.0.0+)
1. get_ui_state            → Observe current screen (get UI elements + screenshot)
2. Execute action          → e.g. CLICK_ELEMENT, INPUT_CONTENT, SLIDE_PAGE
3. sleep 1-3s              → Wait for the action to take effect
4. get_ui_state            → Verify the result, decide next step
5. Repeat 2-4 until done
6. END_TASK                → Mark task complete
```  

## 最佳实践：  
1. 在执行任何操作之前，务必先调用`get_ui_state`以了解当前屏幕状态。  
2. 每次操作完成后，再次调用`get_ui_state`以验证结果（因为动作命令本身不返回任何值）。  
3. 尽量使用`CLICK_ELEMENT`（通过文本定位）；如果无法通过文本定位，则使用`CLICK_COORDINATE`。  
4. 输入内容后，使用`KEYBOARD_OPERATION(key="enter")`进行提交。  
5. 在触发页面切换的操作后，等待1-3秒再调用`get_ui_state`。  
6. 如果目标元素不可见，可以使用`SLIDE_PAGE`进行滚动（最多尝试3次）。  
7. 坐标使用的是相对于系统的0-1000范围，而非像素值。  
8. 不要单独使用`PAGE_SCREENSHOT`——请使用`get_ui_state`，因为它已经包含了压缩后的截图信息。
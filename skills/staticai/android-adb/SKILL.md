---
name: android-automation
description: 通过ADB控制Android设备，支持UI布局分析（uiautomator）和视觉反馈（截图）。当您需要与Android应用程序交互、执行UI自动化操作、截图或运行复杂的ADB命令序列时，可以使用此工具。
---

# Android自动化

使用ADB、uiautomator和screencap来控制和自动化Android设备。

## 连接设备

### USB连接
1. 在设备上启用**开发者选项**和**USB调试**。
2. 通过USB连接设备，并使用`adb devices`进行验证。

### 无线连接（Android 11及以上版本）
1. 在开发者选项中启用**无线调试**。
2. **配对**：在“使用配对码配对设备”弹窗中找到IP地址、端口号和配对码。
   `adb pair <ip>:<pairing_port> <pairing_code>`
3. **连接**：使用主无线调试屏幕上显示的IP地址和端口号进行连接。
   `adb connect <ip>:<connection_port>`
4. 使用`adb devices`进行验证。

## 常用工作流程

### 启动应用程序
使用monkey工具按包名启动应用程序：
`adb shell monkey -p <package_name> -c android.intent.category.LAUNCHER 1`

### 分析用户界面
导出并提取用户界面层次结构以获取坐标：
`adb shell uiautomator dump /sdcard/view.xml && adb pull /sdcard/view.xml ./view.xml`
然后使用`grep`命令查找文本或资源ID，例如`bounds="[x1,y1][x2,y2]"`。

### 与元素交互
- **点击**：`adb shell input tap <x> <y>`
- **输入文本**：`adb shell input text "<text>"`（注意：在某些环境中需要使用`\s`来表示空格，或者小心处理引号）
- **按键事件**：`adb shell input keyevent <keycode>`（Home键：3，返回键：4，电源键：26，搜索键：84，回车键：66）
- **滑动**：`adb shell input swipe <x1> <y1> <x2> <y2> <duration_ms>`

### 可视化验证
截取屏幕截图以验证设备状态：
`adb shell screencap -p /sdcard/screen.png && adb pull /sdcard/screen.png ./screen.png`

## 提示
- **搜索**：在许多应用程序中，可以使用`input keyevent 84`来触发搜索功能。
- **等待**：在执行命令之间使用`sleep <seconds>`来等待用户界面更新。
- **坐标**：为了确保点击的准确性，请计算`[x1,y1][x2,y2]`的范围的中间值。
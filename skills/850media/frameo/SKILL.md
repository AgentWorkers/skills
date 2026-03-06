---
name: frameo
description: Control Frameo digital photo frames. Use when: sending photos to Frameo frames, listing paired frames, controlling frame via ADB (brightness, screen, navigation). Supports both cloud API (read-only) and ADB (full control including photo upload). Requires either Frameo account credentials or ADB access to the frame.
---

# Frameo 数字相框控制

通过云 API 或 ADB 来控制 Frameo 相框。

## 方法

### 方法 1：云 API（功能有限）
- ✅ 列出已配对的相框
- ✅ 获取账户信息
- ❌ 发送照片（需要 FCM/Firebase）

### 方法 2：ADB（完全控制）
- ✅ 直接上传照片
- ✅ 调节亮度
- ✅ 切换屏幕显示
- ✅ 浏览照片

## 快速入门

### 云 API 设置
1. 安装依赖：`pip3 install requests pillow`
2. 从 Frameo 应用程序的请求中获取访问令牌（使用 Proxyman/Charles 工具）
3. 保存令牌：`echo '{"access_token": "YOUR_TOKEN"}' > ~/.frameo_token`
4. 运行命令：`python3 scripts/frameo_client.py --frames`

### ADB 设置（推荐）
1. 在 Frameo 应用中启用开发者选项（设置 → 关于 → 点击“Build 7x”）
2. 启用 USB 调试功能
3. 将 USB-C 数据线连接到电脑
4. 运行命令：`adb tcpip 5555` 以启用无线连接
5. 断开 USB 连接，然后通过无线方式连接：`adb connect <frame-ip>:5555`

## 使用示例

### 列出相框（云 API）
```bash
python3 scripts/frameo_client.py --frames
```

### 发送照片（ADB）
```bash
adb push photo.jpg /sdcard/DCIM/
# Or to Frameo's photo directory:
adb push photo.jpg /sdcard/Frameo/
```

### 控制相框（ADB）
```bash
# Screen on/off
adb shell input keyevent 26

# Set brightness (0-255)
adb shell settings put system screen_brightness 128

# Next photo (swipe right)
adb shell input swipe 800 500 200 500

# Previous photo (swipe left)  
adb shell input swipe 200 500 800 500
```

## 通过 SSH 中继进行远程访问

如果相框位于本地网络中，而控制端在远程位置：
```bash
ssh user@local-mac "adb push /tmp/photo.jpg /sdcard/DCIM/"
```

## 参考资料

- `references/api-endpoints.md` - Frameo 云 API 的端点信息
- `references/adb-commands.md` - Frameo 的常用 ADB 命令

## 故障排除

### 令牌过期（401 错误）
Frameo 令牌的有效期为约 5 分钟。请从 Proxyman 中获取新的令牌。

### ADB 连接被拒绝
可能是无线 ADB 功能未启用。请先连接 USB 数据线，然后运行 `adb tcpip 5555`。

### 未检测到 USB 数据线
请确保使用的是 **数据线**，而非仅用于充电的线缆。数据线通常比充电线更粗。
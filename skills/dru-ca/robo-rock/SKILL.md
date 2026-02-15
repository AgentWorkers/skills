---
name: roborock
description: **控制 Roborock 扫地机器人（状态、清洁进度、地图信息、耗材）**  
用于在需要吸尘时操作机器人、查看吸尘器状态、控制机器人清洁过程或管理清洁计划。该功能可通过搜索关键词“vacuum”、“roborock”、“clean floor”或“hoover”来触发。
metadata: {"clawdbot":{"emoji":"🧹","requires":{"bins":["roborock"]},"install":[{"id":"pipx","kind":"pipx","package":"python-roborock","bins":["roborock"],"label":"Install roborock CLI (pipx)"}]}}
---

# Roborock吸尘器控制

通过 `roborock` 命令行工具（CLI）来控制 Roborock 智能吸尘器。

## 首次设置

### 1. 安装 CLI
```bash
pipx install python-roborock
```

### 2. 登录 Roborock 账户
```bash
roborock login
```
请输入您的 Roborock/Xiaomi Home 应用程序的电子邮件地址和密码。

### 3. 查找设备 ID
```bash
roborock list-devices
```
记下您的设备 ID（格式类似 `AbCdEf123456789XyZ`）。

### 4. 存储设备 ID（可选）
将其添加到您的 `TOOLS.md` 文件中以方便查阅：
```markdown
## Roborock Vacuum
- **Device ID:** your-device-id-here
- **Model:** Roborock S7 Max Ultra (or your model)
```

## 常用命令

所有命令都需要使用 `--device_id "您的设备 ID"` 参数——请替换为您的实际设备 ID。

### 检查设备状态
```bash
roborock status --device_id "YOUR_DEVICE_ID"
```

### 开始清洁
```bash
roborock command --device_id "YOUR_DEVICE_ID" start
```

### 停止/暂停
```bash
roborock command --device_id "YOUR_DEVICE_ID" stop
roborock command --device_id "YOUR_DEVICE_ID" pause
```

### 返回充电底座
```bash
roborock command --device_id "YOUR_DEVICE_ID" home
```

### 清洁特定房间
首先获取房间 ID：
```bash
roborock rooms --device_id "YOUR_DEVICE_ID"
```
然后清洁特定房间：
```bash
roborock command --device_id "YOUR_DEVICE_ID" segment_clean --rooms 16,17
```

## 维护命令

### 检查耗材
```bash
roborock consumables --device_id "YOUR_DEVICE_ID"
```
显示滤网、刷子和传感器的使用寿命。

### 重置耗材
```bash
roborock reset-consumable filter --device_id "YOUR_DEVICE_ID"
roborock reset-consumable main_brush --device_id "YOUR_DEVICE_ID"
roborock reset-consumable side_brush --device_id "YOUR_DEVICE_ID"
```

### 最后一次清洁记录
```bash
roborock clean-record --device_id "YOUR_DEVICE_ID"
```

### 清洁总结（历史记录）
```bash
roborock clean-summary --device_id "YOUR_DEVICE_ID"
```

## 地图与房间信息

### 获取地图数据
```bash
roborock maps --device_id "YOUR_DEVICE_ID"
```

### 缓存家居布局
```bash
roborock home
```

### 保存地图图片
```bash
roborock map-image --device_id "YOUR_DEVICE_ID" --output /tmp/vacuum-map.png
```

### 房间信息
```bash
roborock features --device_id "YOUR_DEVICE_ID"
```

## 设置

### 音量调节
```bash
roborock volume --device_id "YOUR_DEVICE_ID"
roborock set-volume 50 --device_id "YOUR_DEVICE_ID"
```

### 防打扰模式
```bash
roborock dnd --device_id "YOUR_DEVICE_ID"
```

### LED 状态显示
```bash
roborock led-status --device_id "YOUR_DEVICE_ID"
```

### 儿童锁功能
```bash
roborock child-lock --device_id "YOUR_DEVICE_ID"
```

## 交互式操作
对于多个连续执行的命令，无需重复输入设备 ID：
```bash
roborock session --device_id "YOUR_DEVICE_ID"
```

## 故障排除

**命令执行失败时：**
1. 检查登录状态：`roborock login`
2. 使用调试模式：`roborock -d status --device_id "您的设备 ID"`
3. 确保吸尘器已开机并连接到 WiFi

**“设备未找到”：**
- 运行 `roborock list-devices` 命令验证设备 ID
- 确保您使用的是正确的 Roborock 账户

**“认证失败”：**
- 重新登录 `roborock login`
- 确认您使用的账户与 Xiaomi Home/Roborock 应用程序中的账户一致

## 常见操作

**“打扫整个房子”：**
```bash
roborock command --device_id "YOUR_DEVICE_ID" start
```

**“打扫厨房”：**
```bash
roborock rooms --device_id "YOUR_DEVICE_ID"  # find kitchen room ID
roborock command --device_id "YOUR_DEVICE_ID" segment_clean --rooms <kitchen_id>
```

**“吸尘器工作完成了吗？”：**
```bash
roborock status --device_id "YOUR_DEVICE_ID"
```

**“将吸尘器送回充电底座”：**
```bash
roborock command --device_id "YOUR_DEVICE_ID" home
```

**“上次清洁是什么时候？”：**
```bash
roborock clean-record --device_id "YOUR_DEVICE_ID"
```

**“检查刷子和滤网的状况”：**
```bash
roborock consumables --device_id "YOUR_DEVICE_ID"
```

## 支持的型号

本命令适用于大多数 Roborock 吸尘器，包括：
- Roborock S 系列（S4、S5、S6、S7、S8）
- Roborock Q 系列（Q5、Q7、Q8）
- Roborock E 系列
- Xiaomi Mi Robot Vacuum（基于 Roborock 技术的吸尘器）

## 致谢

本工具使用了 [python-roborock](https://github.com/humbertogontijo/python-roborock) 库。
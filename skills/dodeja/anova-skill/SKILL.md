---
name: anova-oven
description: 通过 WiFi WebSocket API 控制 Anova 精密烤箱和精密蒸煮器（sous vide 设备）。可以远程启动烹饪模式（sous vide、烘烤、蒸煮），设置温度，监控设备状态，并停止烹饪过程。
license: Apache-2.0
compatibility: Requires Python 3.7+, websockets library, and internet access to Anova cloud API
metadata:
  author: Akshay Dodeja
  version: "1.0.0"
  repository: https://github.com/dodeja/anova-skill
---

# Anova烤箱与精密炊具控制

通过WebSocket API控制Anova品牌的WiFi设备，包括精密烤箱（APO）和精密炊具（APC）。

## 前提条件

1. **个人访问令牌**：从Anova应用程序获取
   - 下载Anova烤箱应用程序（iOS/Android）
   - 进入“更多” → “开发者” → “个人访问令牌”
   - 创建令牌（以`anova-`开头）
   - 将令牌保存在`~/.config/anova/token`文件中

2. **Python依赖库**
   ```bash
   pip3 install websockets
   ```

3. **设备设置**
   - 确保Anova设备已连接到WiFi，并与您的Anova账户配对

## 安装

```bash
# Install Python dependency
pip3 install websockets

# Store your token
mkdir -p ~/.config/anova
echo "anova-YOUR_TOKEN_HERE" > ~/.config/anova/token
chmod 600 ~/.config/anova/token
```

## 使用方法

### 列出设备
```bash
python3 scripts/anova.py list
```

### 基本烹饪功能
```bash
# Simple cook at 350°F for 30 minutes
python3 scripts/anova.py cook --temp 350 --duration 30

# Cook at 175°C for 45 minutes
python3 scripts/anova.py cook --temp 175 --unit C --duration 45
```

### 高级控制功能

**自定义元素：**
```bash
# Rear element only (low-temp slow cook)
python3 scripts/anova.py cook --temp 225 --elements rear --duration 180

# Bottom + rear (standard roasting)
python3 scripts/anova.py cook --temp 375 --elements bottom,rear --duration 45

# All elements (maximum heat)
python3 scripts/anova.py cook --temp 450 --elements top,bottom,rear --duration 20
```

**自定义风扇转速：**
```bash
# Low fan (gentle cooking)
python3 scripts/anova.py cook --temp 250 --fan-speed 25 --duration 120

# High fan (fast heat circulation)
python3 scripts/anova.py cook --temp 400 --fan-speed 100 --duration 30
```

**探针烹饪功能：**
```bash
# Cook to internal temperature (not time-based)
python3 scripts/anova.py cook --temp 350 --probe-temp 165

# Low-temp probe cook
python3 scripts/anova.py cook --temp 225 --elements rear --fan-speed 25 --probe-temp 135
```

**综合高级设置：**
```bash
# Precision low-temp cook
python3 scripts/anova.py cook --temp 225 --elements rear --fan-speed 25 --duration 180

# High-heat sear
python3 scripts/anova.py cook --temp 500 --elements top,bottom,rear --fan-speed 100 --duration 5
```

### 停止烹饪
```bash
python3 scripts/anova.py stop
```

### 监控（实时流媒体）
```bash
python3 scripts/anova.py monitor --monitor-duration 60
```

## 自然语言指令示例

**系统提示：**
- “将烤箱预热至375°F（约190°C）用于烘烤”
- “以135°F（约57°C）开始水煮烹饪，持续2小时”
- “当前烤箱温度是多少？”
- “停止烹饪”
- “以212°F（约100°C）蒸煮蔬菜，持续15分钟”

## 主要功能

### Anova精密烤箱（APO）
- 水煮烹饪（湿球模式）
- 烘烤（干球模式）
- 带湿度控制的蒸煮功能
- 温度调节（摄氏/华氏）
- 实时状态监控
- 数据遥测功能

### Anova精密炊具（APC）
- 水煮烹饪功能
- 温度调节
- 计时器管理
- 实时状态显示

## API参考

**WebSocket端点：** 通过Anova云服务访问
**认证方式：** 使用个人访问令牌（Bearer令牌）
**协议：** 基于WebSocket的JSON消息传输

## 配置设置

**令牌文件：** `~/.config/anova/token`
**默认设备：** 系统自动检测到的第一台设备（或使用`--device-id`参数指定）

## 故障排除

**“未找到令牌”：**
```bash
echo "anova-YOUR_TOKEN" > ~/.config/anova/token
```

**“未找到设备”：**
- 检查设备是否在Anova应用程序中处于在线状态
- 确认WiFi连接是否正常
- 重新生成令牌

**“连接失败”：**
- 检查网络连接是否稳定
- 验证令牌是否有效
- 确认设备已正确与账户配对

## 安全注意事项

- 在开始长时间烹饪前，请务必确认温度设置正确
- 使用计时器防止食物煮过头
- 可远程监控设备状态，但烹饪过程中需亲自在场确保安全
- 系统默认超时时间为4小时

## 参考资源

- [Anova开发者门户](https://developer.anovaculinary.com)
- [GitHub项目：anova-wifi-device-controller](https://github.com/anova-culinary/developer-project-wifi)
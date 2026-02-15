---
name: switchbot
description: 通过 SwitchBot Cloud API 控制 SwitchBot 智能家居设备（如窗帘、插座、灯光、锁等）。当用户请求打开/关闭窗帘、开关灯光/插座、查看温度/湿度或控制任何 SwitchBot 设备时，可以使用该功能。
---

# SwitchBot 智能家居控制

通过 Cloud API v1.1 来控制 SwitchBot 设备。

## 首次设置

**请按照以下步骤指导用户进行设置：**

### 1. 获取 API 凭据

请用户执行以下操作：
1. 在手机上打开 **SwitchBot 应用**。
2. 进入 **个人资料**（右下角）。
3. 点击 **偏好设置**（或 **设置**）。
4. 选择 **关于** → **开发者选项**。
5. 复制 **Token** 和 **Secret Key**。

### 2. 安全存储凭据

```bash
mkdir -p ~/.config/switchbot
chmod 700 ~/.config/switchbot

cat > ~/.config/switchbot/credentials.json << 'EOF'
{
  "token": "YOUR_TOKEN_HERE",
  "secret": "YOUR_SECRET_HERE"
}
EOF
chmod 600 ~/.config/switchbot/credentials.json
```

### 3. 发现设备

运行发现脚本以查找所有设备：

```bash
python3 <skill_path>/scripts/switchbot.py list
```

### 4. 更新您的 TOOLS.md 文件

发现设备后，请将设备 ID 记录在 TOOLS.md 文件中以供快速参考：

```markdown
## SwitchBot Devices
| Device | ID | Type |
|--------|-----|------|
| Living Room Curtain | ABC123 | Curtain3 |
| Bedroom Light | DEF456 | Plug Mini |
```

## 使用方法

### 列出所有设备

```bash
python3 <skill_path>/scripts/switchbot.py list
```

### 窗帘控制

```bash
# Open curtain (position 0 = fully open)
python3 <skill_path>/scripts/switchbot.py curtain <device_id> open

# Close curtain (position 100 = fully closed)
python3 <skill_path>/scripts/switchbot.py curtain <device_id> close

# Set specific position (0-100)
python3 <skill_path>/scripts/switchbot.py curtain <device_id> 50
```

### 插座/灯光控制

```bash
python3 <skill_path>/scripts/switchbot.py plug <device_id> on
python3 <skill_path>/scripts/switchbot.py plug <device_id> off
```

### 检查传感器状态

```bash
python3 <skill_path>/scripts/switchbot.py status <device_id>
```

### 通用命令

```bash
python3 <skill_path>/scripts/switchbot.py command <device_id> <command> [parameter]
```

## 支持的设备

| 设备类型 | 命令 |
|-------------|----------|
| 窗帘 / Curtain3 | `open`（打开）、`close`（关闭）、`setPosition`（设置位置） |
| Plug Mini / Plug | `turnOn`（打开）、`turnOff`（关闭）、`toggle`（切换状态） |
| Bot | `press`（按下按钮）、`turnOn`（打开）、`turnOff`（关闭） |
| 灯光 / 条形灯 | `turnOn`（打开）、`turnOff`（关闭）、`setBrightness`（设置亮度）、`setColor`（设置颜色） |
| 锁 | `lock`（锁定）、`unlock`（解锁） |
| 加湿器 | `turnOn`（打开）、`turnOff`（关闭）、`setMode`（设置模式） |
| 电表 / MeterPlus | （仅读：温度、湿度） |
| Hub / Hub Mini / Hub 2 | （仅作为网关使用） |

## 错误处理

| 状态码 | 含义 |
|-------------|---------|
| 100 | 操作成功 |
| 151 | 设备离线 |
| 152 | 命令不受支持 |
| 160 | 未知命令 |
| 161 | 参数无效 |
| 190 | 内部错误 |

## 代理提示

1. **首次交互**：如果用户没有凭据，请指导他们完成设置。
2. **设备别名**：在 TOOLS.md 文件中为设备创建易于理解的名称（例如，“living room” → 设备 ID）。
3. **批量操作**：可以依次控制多个设备。
4. **状态检查**：在报告传感器数据之前，先使用 `status` 命令检查设备状态。
5. **错误恢复**：如果设备离线（状态码 151），建议检查 Hub 与设备的连接。

## 安全注意事项

- 凭据文件的权限应设置为 chmod 600。
- 绝不要记录或显示 Token 和 Secret Key。
- API 调用通过 HTTPS 发送到 api.switch-bot.com。
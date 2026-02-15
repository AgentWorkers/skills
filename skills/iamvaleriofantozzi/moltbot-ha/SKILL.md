---
name: moltbot-ha
description: 通过 `moltbot-ha CLI` 控制 Home Assistant 智能家居设备、灯光、场景及自动化功能，并支持配置安全确认机制。
homepage: https://github.com/iamvaleriofantozzi/moltbot-ha
metadata: {"moltbot":{"emoji":"🏠","requires":{"bins":["moltbot-ha"],"env":["HA_TOKEN"]},"primaryEnv":"HA_TOKEN","install":[{"id":"uv","kind":"uv","package":"moltbot-ha","bins":["moltbot-ha"],"label":"Install moltbot-ha (uv tool)"}]}}
---

# 通过 Home Assistant 进行控制

您可以使用 `moltbot-ha` CLI 工具，通过 Home Assistant API 来控制您的智能家居。

## 设置

### 1. 安装 moltbot-ha
```bash
uv tool install moltbot-ha
```

### 2. 初始化配置
```bash
moltbot-ha config init
```

设置过程中，系统会交互式地询问以下信息：
- Home Assistant 的 URL（例如：`http://192.168.1.100:8123`）
- 令牌存储方式（建议使用环境变量）

### 3. 设置环境变量
设置您的 Home Assistant 长期访问令牌：
```bash
export HA_TOKEN="your_token_here"
```

创建令牌的步骤：
1. 打开 Home Assistant → 个人资料（左下角）
2. 滚动到“长期访问令牌”部分
3. 点击“创建令牌”
4. 复制令牌，并将其设置为 `HA_TOKEN` 环境变量

### 4. 测试连接
```bash
moltbot-ha test
```

## 发现命令

### 列出所有设备
```bash
moltbot-ha list
```

### 按领域列出设备
```bash
moltbot-ha list light
moltbot-ha list switch
moltbot-ha list cover
```

### 获取设备状态
```bash
moltbot-ha state light.kitchen
moltbot-ha state sensor.temperature_living_room
```

## 操作命令

### 开/关设备
```bash
# Turn on
moltbot-ha on light.living_room
moltbot-ha on switch.coffee_maker

# Turn off
moltbot-ha off light.bedroom
moltbot-ha off switch.fan

# Toggle
moltbot-ha toggle light.hallway
```

### 设置设备属性
```bash
# Set brightness (percentage)
moltbot-ha set light.bedroom brightness_pct=50

# Set color temperature
moltbot-ha set light.office color_temp=300

# Multiple attributes
moltbot-ha set light.kitchen brightness_pct=80 color_temp=350
```

### 调用服务
```bash
# Activate a scene
moltbot-ha call scene.turn_on entity_id=scene.movie_time

# Set thermostat temperature
moltbot-ha call climate.set_temperature entity_id=climate.living_room temperature=21

# Close cover (blinds, garage)
moltbot-ha call cover.close_cover entity_id=cover.garage
```

### 通用服务调用
```bash
# With parameters
moltbot-ha call automation.trigger entity_id=automation.morning_routine

# With JSON data
moltbot-ha call script.turn_on --json '{"entity_id": "script.bedtime", "variables": {"brightness": 10}}'
```

## 安全性与确认机制

`moltbot-ha` 实现了 **三级安全系统**，以防止意外操作：

### 安全级别 3（默认值 - 推荐使用）

需要明确确认的关键操作包括：
- **lock.***：门锁
- **alarm_control_panel.***：安全警报
- **cover.***：车库门、百叶窗

### 确认机制的工作原理

1. **尝试执行关键操作：**
```bash
moltbot-ha on cover.garage
```

2. **工具返回错误：**
```
⚠️  CRITICAL ACTION REQUIRES CONFIRMATION

Action: turn_on on cover.garage

This is a critical operation that requires explicit user approval.
Ask the user to confirm, then retry with --force flag.

Example: moltbot-ha on cover.garage --force
```

3. **代理程序会提示您：**
> “打开车库门是一个关键操作。您是否要继续？”

4. **您进行确认：**
> “是的，打开它”

5. **代理程序会使用 `--force` 重新尝试：**
```bash
moltbot-ha on cover.garage --force
```

6. **操作成功执行。**

### 重要提示：**未经用户同意，切勿使用 `--force`**

**⚠️ 对于代理程序的重要规则：**

- **绝对** 不要在没有用户明确确认的情况下使用 `--force` 标志
- **始终** 向用户显示正在尝试执行的关键操作
- **在使用 `--force` 之前，必须等待用户明确回答“是”/“确认”/“同意”
- **确认的方式可以灵活**：例如“是的”、“可以”、“确定”、“执行”或任何与请求相关的肯定回答都有效。用户不需要逐字输入特定的短语。

### 被屏蔽的设备

某些设备可以在配置中被永久屏蔽：
```toml
[safety]
blocked_entities = ["switch.main_breaker", "lock.front_door"]
```

这些设备**即使使用 `--force` 也无法被控制**。

### 配置

编辑 `~/.config/moltbot-ha/config.toml` 文件：
```toml
[safety]
level = 3  # 0=disabled, 1=log-only, 2=confirm all writes, 3=confirm critical

critical_domains = ["lock", "alarm_control_panel", "cover"]

blocked_entities = []  # Add entities that should never be automated

allowed_entities = []  # If set, ONLY these entities are accessible (supports wildcards)
```

## 常见工作流程

### 早晨例程
```bash
moltbot-ha on light.bedroom brightness_pct=30
moltbot-ha call cover.open_cover entity_id=cover.bedroom_blinds
moltbot-ha call climate.set_temperature entity_id=climate.bedroom temperature=21
```

### 夜间模式
```bash
moltbot-ha off light.*  # Requires wildcard support in future
moltbot-ha call scene.turn_on entity_id=scene.goodnight
moltbot-ha call cover.close_cover entity_id=cover.all_blinds
```

### 检查传感器
```bash
moltbot-ha state sensor.temperature_living_room
moltbot-ha state sensor.humidity_bathroom
moltbot-ha state binary_sensor.motion_hallway
```

## 故障排除

### 连接失败
- 确认配置中的 `HA_URL` 与您的 Home Assistant URL 是否一致
- 确保运行 `moltbot-ha` 的机器能够访问 Home Assistant
- 检查防火墙设置

### 401 未授权错误
- 确认 `HA_TOKEN` 是否设置正确
- 确保令牌是**长期访问令牌**（而非临时令牌）
- 检查令牌是否已在 Home Assistant 中被撤销

### 设备未找到
- 使用 `moltbot-ha list` 命令来查找正确的设备 ID
- 设备 ID 是区分大小写的
- 格式为 `domain.entity_name`（例如：`light.kitchen`，而不是 `Light.Kitchen`）

### Docker 网络设置
如果在 Docker 中运行 `moltbot-ha` 且无法通过 `homeassistant.local` 访问 Home Assistant：
- 使用 IP 地址：`http://192.168.1.100:8123`
- 或者使用 Tailscale 来实现可靠的网状网络连接

## 配置参考

完整的配置文件（`~/.config/moltbot-ha/config.toml`）：
```toml
[server]
url = "http://homeassistant.local:8123"
# token = "optional_here_prefer_env_var"

[safety]
level = 3
critical_domains = ["lock", "alarm_control_panel", "cover"]
blocked_entities = []
allowed_entities = []

[logging]
enabled = true
path = "~/.config/moltbot-ha/actions.log"
level = "INFO"
```

## 代理程序示例

### 发现设备模式
```
User: "What lights do I have?"
Agent: moltbot-ha list light
Agent: "You have these lights: light.living_room, light.kitchen, light.bedroom"
```

### 安全操作模式
```
User: "Turn on the living room light"
Agent: moltbot-ha on light.living_room
Agent: "Living room light is now on"
```

### 关键操作模式
```
User: "Open the garage"
Agent: moltbot-ha on cover.garage
<receives CriticalActionError>
Agent: "⚠️ Opening the garage door is a critical action. Do you want to proceed?"
User: "Yes, open it"
Agent: moltbot-ha on cover.garage --force
Agent: "Garage door is opening"
```

## 注意事项

- 所有写入操作默认会被记录到 `~/.config/moltbot-ha/actions.log` 文件中
- 安全设置可以根据需要进行配置
- 在 `allowed_entities` 和 `blocked_entities` 中支持通配符（`*`）
- 使用 `--json` 标志可以获取 JSON 格式的输出，以便进行程序化解析
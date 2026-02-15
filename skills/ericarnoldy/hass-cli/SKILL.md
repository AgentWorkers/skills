---
name: home-assistant
description: 通过 `hass-cli` 控制 Home Assistant 设备和自动化任务。适用于控制智能家居设备、灯光、开关、传感器、气候控制系统、媒体播放器，或运行自动化脚本等场景。需要 `HASS_SERVER` 和 `HASS_TOKEN` 环境变量。
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["hass-cli"]},"install":[{"id":"brew","kind":"brew","formula":"homeassistant-cli","bins":["hass-cli"],"label":"Install hass-cli (brew)"}]}}
---

# Home Assistant 命令行界面（CLI）

您可以通过 `hass-cli` 来控制 Home Assistant。

## 安装

```bash
# macOS (Homebrew)
brew install homeassistant-cli

# pip (any platform)
pip install homeassistant-cli

# Verify
hass-cli --version
```

## 设置

### 1. 查找您的 Home Assistant URL

常见的 URL（按顺序尝试）：
- `http://homeassistant.local:8123` — 默认的 mDNS 主机名
- `http://homeassistant:8123` — 如果使用 Docker 或主机名
- `http://<IP-ADDRESS>:8123` — 直接 IP 地址（例如：`http://192.168.1.100:8123`
- `https://your-instance.ui.nabu.casa` — 如果使用 Nabu Casa 云服务

测试方法：在浏览器中打开该 URL，您应该会看到 Home Assistant 的登录页面。

### 2. 创建长期有效的访问令牌

1. 在浏览器中打开 Home Assistant
2. 点击您的个人资料（侧边栏的左下角，您的名字/图标）
3. 向下滚动到 “Long-Lived Access Tokens”（长期有效访问令牌）
4. 点击 “Create Token”（创建令牌）
5. 为令牌起一个名称（例如：“Clawdbot” 或 “CLI”）
6. **立即复制令牌** — 因为您之后将无法再次看到它！

令牌的格式如下：`eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3...`

### 3. 配置环境变量

将以下内容添加到您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中：
```bash
export HASS_SERVER="http://homeassistant.local:8123"
export HASS_TOKEN="your-token-here"
```

或者，对于 Clawdbot，可以将凭据存储在 `TOOLS.md` 文件中：
```markdown
## Home Assistant
- **URL:** `http://homeassistant.local:8123`
- **Token:** `eyJ...your-token...`
```

在进行调用之前，请确保先读取 `TOOLS.md` 文件中的内容。

## 快速参考

```bash
# List all entities
hass-cli state list

# Filter entities (pipe to grep)
hass-cli state list | grep -i kitchen

# Get specific entity state
hass-cli state get light.kitchen

# Turn on/off
hass-cli service call switch.turn_on --arguments entity_id=switch.fireplace
hass-cli service call switch.turn_off --arguments entity_id=switch.fireplace
hass-cli service call light.turn_on --arguments entity_id=light.kitchen
hass-cli service call light.turn_off --arguments entity_id=light.kitchen

# Light brightness (0-255)
hass-cli service call light.turn_on --arguments entity_id=light.kitchen,brightness=128

# Toggle
hass-cli service call switch.toggle --arguments entity_id=switch.fireplace

# Climate
hass-cli service call climate.set_temperature --arguments entity_id=climate.thermostat,temperature=72

# Run automation/script
hass-cli service call automation.trigger --arguments entity_id=automation.evening_lights
hass-cli service call script.turn_on --arguments entity_id=script.movie_mode
```

## 实体命名规则

- `light.*` — 灯具
- `switch.*` — 开关、插座、继电器
- `sensor.*` — 温度、湿度、电量等传感器
- `binary_sensor.*` — 运动传感器、门/窗传感器、人体感应传感器
- `climate.*` — 温控器、暖通空调设备
- `cover.*` — 百叶窗、车库门
- `media_player.*` — 电视、音响设备
- `automation.*` — 自动化任务
- `script.*` — 脚本
- `scene.*` — 场景

## 发现设备的技巧

```bash
# Find all lights
hass-cli state list | grep "^light\."

# Find devices by room name
hass-cli state list | grep -i bedroom

# Find all "on" devices
hass-cli state list | grep -E "\s+on\s+"

# Get entity attributes (JSON)
hass-cli --format json state get light.kitchen
```

## 注意事项

- 服务调用返回空数组（`[]`）表示操作成功
- 请使用 `state list` 中提供的准确实体 ID
- 多个参数需要用逗号分隔（不要使用空格）
- 如果 `hass-cli` 不可用，可以使用 REST API 作为备用方案：
  ```bash
  curl -s -H "Authorization: Bearer $HASS_TOKEN" "$HASS_SERVER/api/states" | jq
  ```
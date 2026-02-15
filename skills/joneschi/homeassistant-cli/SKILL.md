---
name: homeassistant-cli
description: 使用官方的 `hass-cli` 工具进行高级的 Home Assistant 控制。该工具支持自动补全、事件监控、历史记录查询以及丰富的输出格式化功能。作为基于 `curl` 的 `homeassistant` 命令行的替代方案，如果您希望获得更交互式的命令行体验（包括更好的设备发现和输出格式），请选择它。
homepage: https://github.com/home-assistant-ecosystem/home-assistant-cli
metadata:
  {
    "openclaw":
      {
        "emoji": "🏡",
        "requires": { "bins": ["hass-cli"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "homeassistant-cli",
              "bins": ["hass-cli"],
              "label": "Install Home Assistant CLI (pip)",
            },
            {
              "id": "brew",
              "kind": "brew",
              "formula": "homeassistant-cli",
              "bins": ["hass-cli"],
              "label": "Install Home Assistant CLI (brew)",
            },
          ],
      },
  }
---

# Home Assistant CLI

使用**官方的hass-cli工具**来控制您的Home Assistant智能家居设备——这是一个功能丰富的命令行界面，支持自动补全、事件监控以及灵活的输出格式化。

## 为什么选择hass-cli而不是基于curl的`homeassistant`？

**如果您需要以下功能，请选择hass-cli：**
- ✅ 实体ID和服务的自动补全（支持bash/zsh/fish shell）
- ✅ 实时事件监控（`hass-cli event watch`）
- ✅ 历史记录查询（`hass-cli state history`）
- 更好的输出格式（可通过一个命令参数选择表格、YAML或JSON格式）
- 交互式探索功能（更便于发现实体和服务）
- 详细的文档，包含示例和故障排除方法

**如果您希望使用基于curl的`homeassistant`，请考虑以下优势：**
- **无依赖项**（只需预先安装curl和jq）
- **轻量级且快速**  
- **更适合脚本编写和自动化**  
- **无需安装Python**

这两种工具都非常实用——本文档专为经常与Home Assistant交互的用户设计，旨在提供更丰富的命令行使用体验。

## 设置

在使用hass-cli之前，请先配置身份验证：
1. 在Home Assistant中生成一个长期有效的访问令牌：
   - 访问您的个人资料页面：`https://your-homeassistant:8123/profile`
   - 向下滚动至“Long-Lived Access Tokens”部分
   - 创建一个新的令牌

2. 设置环境变量（将其添加到shell配置文件中以实现持久化）：
   ```bash
   export HASS_SERVER=https://homeassistant.local:8123
   export HASS_TOKEN=<your-token>
   ```

3. 测试连接：
   ```bash
   hass-cli info
   ```

## 常用命令

### 列出实体
```bash
# List all entities
hass-cli state list

# Filter by domain
hass-cli state list light
hass-cli state list switch
hass-cli state list sensor

# Get specific entity state
hass-cli state get light.living_room
```

### 控制设备
```bash
# Turn on/off lights
hass-cli service call light.turn_on --arguments entity_id=light.living_room
hass-cli service call light.turn_off --arguments entity_id=light.living_room

# Set brightness (0-255)
hass-cli service call light.turn_on --arguments entity_id=light.bedroom,brightness=128

# Turn on/off switches
hass-cli service call switch.turn_on --arguments entity_id=switch.fan
hass-cli service call switch.turn_off --arguments entity_id=switch.fan

# Toggle any device
hass-cli service call homeassistant.toggle --arguments entity_id=light.kitchen
```

### 列出并调用服务
```bash
# List all services
hass-cli service list

# Filter services
hass-cli service list light
hass-cli service list 'home.*toggle'

# Get service details (YAML output)
hass-cli -o yaml service list homeassistant.toggle
```

### 管理场景
```bash
# List scenes
hass-cli state list scene

# Activate a scene
hass-cli service call scene.turn_on --arguments entity_id=scene.movie_time
```

### 监控事件
```bash
# Watch all events
hass-cli event watch

# Watch specific event type
hass-cli event watch state_changed
hass-cli event watch automation_triggered
```

### 查看历史记录
```bash
# Get state history (last 50 minutes)
hass-cli state history --since 50m light.living_room

# Multiple entities
hass-cli state history --since 1h light.living_room switch.fan
```

## 输出格式

您可以使用`-o`或`--output`参数来定制输出格式：
```bash
# Table (default)
hass-cli state list

# YAML
hass-cli -o yaml state get light.living_room

# JSON
hass-cli -o json state list light

# No headers (for scripting)
hass-cli --no-headers state list
```

## 提示

- **实体查找**：使用`hass-cli state list`来获取实体ID
- **服务查找**：使用`hass-cli service list`来查看可用的服务
- **自动补全**：请参阅[references/autocomplete.md](references/autocomplete.md)以了解如何在shell环境中启用自动补全功能
- **故障排除**：请参阅[references/troubleshooting.md](references/troubleshooting.md)以获取故障排除建议

## 示例

请参阅[references/examples.md](references/examples.md)，了解常见的自动化模式和使用案例。
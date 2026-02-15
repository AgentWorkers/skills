---
name: mcp-hass
description: 使用MCP协议控制Home Assistant智能家居设备并查询其状态的技能。
homepage: https://home-assistant.io/integrations/mcp
metadata:
  {
    "openclaw":
      {
        "emoji": "🏠",
        "requires": { "anyBins": ["mcporter", "npx"], "env": ["HASS_ACCESS_TOKEN", "HASS_BASE_URL"] },
        "primaryEnv": "HASS_ACCESS_TOKEN",
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "mcporter",
              "bins": ["mcporter"],
              "label": "Install mcporter (node)",
            },
          ],
      },
  }
---

# Home Assistant  
使用 MCP 协议控制 Home Assistant 智能家居设备并查询设备状态。  

## 先决条件  
在 Home Assistant 中启用 MCP 服务器：  
1. 登录到您的 Home Assistant 实例。  
2. 转到 **设置 > 设备与服务**（Settings > Devices & Services）。  
3. 在右下角，点击 “[+ 添加集成](https://my.home-assistant.io/redirect/config_flow_start?domain=mcp)” 按钮。  
4. 从列表中选择 “Model Context Protocol”（模型上下文协议）。  
5. 按照屏幕上的提示完成设置。  

## 使用方法  
```shell
# Get states
mcporter call home-assistant.GetLiveContext

# Turn on the device
mcporter call home-assistant.HassTurnOn(name: "Bedroom Light")
mcporter call home-assistant.HassTurnOn(name: "Light", area: "Bedroom")

# Turn off the device
mcporter call home-assistant.HassTurnOff(name: "Bedroom Light")
mcporter call home-assistant.HassTurnOff(area: "Bedroom", domain: ["light"])

# Control light
# brightness: The percentage of the light, where 0 is off and 100 is fully lit.
# color: Name of color
mcporter call home-assistant.HassLightSet(name: "Bedroom Light", brightness: 50)

# Control fan
# percentage: The percentage of the fan, where 0 is off and 100 is full speed.
mcporter call home-assistant.HassFanSetSpeed(name: "Fan", area: "Bedroom", percentage: 80)
```  

执行以下命令以了解具体的使用方法：  
`mcporter list home-assistant --schema --all-parameters`  

## 配置  
当系统提示 MCP 服务器不存在时，需要用户通过执行以下命令来配置 `HASS_BASE_URL` 和 `HASS_ACCESS_TOKEN` 环境变量：  
```shell
mcporter config add home-assistant \
  --transport http \
  --url "${HASS_BASE_URL:-http://homeassistant.local:8123}/api/mcp" \
  --header "Authorization=Bearer \${HASS_ACCESS_TOKEN}"
```  

## 关于 `mcporter`  
- 如果 `mcporter` 命令不存在，可以使用 `npx -y mcporter` 代替。  
- 更多信息请参考：  
  - https://github.com/steipete/mcporter/raw/refs/heads/main/docs/call-syntax.md  
  - https://github.com/steipete/mcporter/raw/refs/heads/main/docs/cli-reference.md
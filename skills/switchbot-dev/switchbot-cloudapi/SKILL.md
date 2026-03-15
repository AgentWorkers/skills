---
name: switchbot-openapi
description: 使用官方的 OpenAPI (v1.1) 来控制和查询 SwitchBot 设备。当用户需要列出 SwitchBot 设备、获取设备状态或发送命令（如开关设备、执行特定操作、设置模式、锁定/解锁设备、控制窗帘、空调、灯光、风扇、机器人吸尘器、键盘等）时，可以使用该接口。使用该接口需要提供 `SWITCHBOT_TOKEN` 和 `SWITCHBOT_SECRET` 这两个参数。
---
# SwitchBot 开放API技能

该技能使代理能够通过HTTPS请求操作SwitchBot设备，使用的是官方的OpenAPI v1.1接口。它提供了即用型脚本和Node.js命令行工具（CLI），可以直接使用这些工具而无需每次都重新生成HMAC签名。

## 快速入门（操作员）

1) 设置环境变量：
- `SWITCHBOT_TOKEN`：您的OpenAPI令牌
- `SWITCHBOT_SECRET`：您的OpenAPI密钥

2) 测试（列出设备）：
- Bash：`scripts/list_devices.sh`
- Node.js：`node scripts/switchbot_cli.js list`

## 常见任务：

**基本控制：**
- 列出设备：`node scripts/switchbot_cli.js list`
- 获取状态：`node scripts/switchbot_cli.js status <deviceId>`
- 开/关：`node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff`
- 切换状态：`node scripts/switchbot_cli.js cmd <deviceId> toggle`
- 按下按钮：`node scripts/switchbot_cli.js cmd <deviceId> press`

**窗帘：**
- 设置位置：`node scripts/switchbot_cli.js cmd <deviceId> setPosition --pos=50`
  （0=打开，100=关闭；CLI会自动格式化为`0,ff,50`）
- 暂停：`node scripts/switchbot_cli.js cmd <deviceId> pause`

**锁：**
- 锁定/解锁：`node scripts/switchbot_cli.js cmd <deviceId> lock` / `unlock`
- 电子锁：`node scripts/switchbot_cli.js cmd <deviceId> deadbolt`

**照明设备（彩色灯泡/条形灯/落地灯/RGBICWW等）：**
- 设置颜色：`node scripts/switchbot_cli.js cmd <deviceId> setColor --param="255:100:0"`
- 设置亮度：`node scripts/switchbot_cli.js cmd <deviceId> setBrightness --param=80`
- 设置色温：`node scripts/switchbot_cli.js cmd <deviceId> setColorTemperature --param=4000`

**风扇：**
- 风速模式：`node scripts/switchbot_cli.js cmd <deviceId> setWindMode --param=natural`
- 风速：`node scripts/switchbot_cli.js cmd <deviceId> setWindSpeed --param=50`
- 夜灯模式：`node scripts/switchbot_cli.js cmd <deviceId> setNightLightMode --param=1`
- 自动关闭定时器：`node scripts/switchbot_cli.js cmd <deviceId> closeDelay --param=3600`

**扫地机器人（S1/S1 Plus/K10+/K10+ Pro）：**
- 启动：`node scripts/switchbot_cli.js cmd <deviceId> start`
- 停止：`node scripts/switchbot_cli.js cmd <deviceId> stop`
- 连接底座：`node scripts/switchbot_cli.js cmd <deviceId> dock`
- 吸尘强度：`node scripts/switchbot_cli.js cmd <deviceId> PowLevel --param=2`

**扫地机器人K10+ Pro组合版/K20+ Pro/S10/S20/K11+：**
- 开始清洁：`node scripts/switchbot_cli.js cmd <deviceId> startClean --param='{"action":"sweep_mop","param":{"fanLevel":2,"waterLevel":1,"times":1}}'`
- 暂停/连接底座：`node scripts/switchbot_cli.js cmd <deviceId> pause` / `dock`
- 音量：`node scripts/switchbot_cli.js cmd <deviceId> setVolume --param=50`
- 自动清洁：`node scripts/switchbot_cli.js cmd <deviceId> selfClean --param=1`

**百叶窗：**
- 设置位置：`node scripts/switchbot_cli.js cmd <deviceId> setPosition --param="up;60"`
- 完全打开：`node scripts/switchbot_cli.js cmd <deviceId> fullyOpen`
- 关闭：`node scripts/switchbot_cli.js cmd <deviceId> closeUp` / `closeDown`

**卷帘：**
- 设置位置：`node scripts/switchbot_cli.js cmd <deviceId> setPosition --param=50`

**加湿器：**
- 设置模式：`node scripts/switchbot_cli.js cmd <deviceId> setMode --param=auto`

**蒸发式加湿器/自动补充水：**
- 设置模式：`node scripts/switchbot_cli.js cmd <deviceId> setMode --param='{"mode":7,"targetHumidify":60}'`
- 儿童锁：`node scripts/switchbot_cli.js cmd <deviceId> setChildLock --param=true`

**空气净化器（VOC/PM2.5/桌面型）：**
- 设置模式：`node scripts/switchbot_cli.js cmd <deviceId> setMode --param='{"mode":2,"fanGear":2}'`
- 儿童锁：`node scripts/switchbot_cli.js cmd <deviceId> setChildLock --param=1`

**智能暖气恒温器：**
- 设置模式：`node scripts/switchbot_cli.js cmd <deviceId> setMode --param=1`
- 设置温度：`node scripts/switchbot_cli.js cmd <deviceId> setManualModeTemperature --param=22`

**继电器开关（1PM/1/2PM）：**
- 切换状态：`node scripts/switchbot_cli.js cmd <deviceId> toggle`
- 设置模式：`node scripts/switchbot_cli.js cmd <deviceId> setMode --param=0`
- 选择频道：`node scripts/switchbot_cli.js cmd <deviceId> turnOn --param="1"`（频道1或2）

**车库门开启器：**
- 开/关：`node scripts/switchbot_cli.js cmd <deviceId> turnOn` / `turnOff`

**视频门铃：**
- 启用/禁用运动检测：`node scripts/switchbot_cli.js cmd <deviceId> enableMotionDetection` / `disableMotionDetection`

**蜡烛加热灯：**
- 调节亮度：`node scripts/switchbot_cli.js cmd <deviceId> setBrightness --param=50`

**AI艺术画框：**
- 下一页/上一页：`node scripts/switchbot_cli.js cmd <deviceId> next` / `previous`

**键盘：**
- 创建密码：`node scripts/switchbot_cli.js cmd <deviceId> createKey --param='{"name":"Guest","type":"permanent","password":"12345678'}`
- 删除密码：`node scripts/switchbot_cli.js cmd <deviceId> deleteKey --param='{"id":"11'}`
- 注意：键盘相关的命令是异步的——结果通过Webhook返回。

**红外遥控器（空调）：**
- 全部设置：`node scripts/switchbot_cli.js cmd <deviceId> setAll --param="26,2,1,on"`
  （格式：温度，模式，风速，电源状态）
  - 模式：0=自动，2=制冷，3=制热，4=风扇
  - 风速：1=自动，2=低速，3=中速，4=高速
  - 电源：开/关

**红外遥控器（电视）：**
- 选择频道：`node scripts/switchbot_cli.js cmd <deviceId> SetChannel --param=5`
- 调节音量：`node scripts/switchbot_cli.js cmd <deviceId> volumeAdd` / `volumeSub`

**红外遥控器（其他设备）：**
- 自定义按钮：`node scripts/switchbot_cli.js cmd <deviceId> <buttonName> --commandType=customize`

**场景：**
- 列出所有场景：`node scripts/switchbot_cli.js scenes`
- 执行场景：`node scripts/switchbot_cli.js scene <sceneId>`

## API参考

基础URL：`https://api.switch-bot.com`
路径前缀：`/v1.1`
每日调用限制：10,000次

必需的请求头：
- `Authorization`：`<SWITCHBOT_TOKEN>`
- `sign`：`HMAC-SHA256(`token + t + nonce`, 使用Base64编码)
- `t`：13位毫秒时间戳
- `nonce`：随机UUID

主要API端点：
- `GET /v1.1/devices` — 列出所有设备
- `GET /v1.1/devices/{deviceId}/status` — 获取设备状态
- `POST /v1.1/devices/{deviceId}/commands` — 发送命令
- `GET /v1.1/scenes` — 列出所有场景
- `POST /v1.1/scenes/{sceneId}/execute` — 执行场景

命令体格式：
```json
{
  "command": "<commandName>",
  "parameter": "<string|object>",
  "commandType": "command"
}
```
对于其他类型的红外设备（自定义命令），请使用`"commandType": "customize"`。

## 代理使用指南：

- 始终使用提供的CLI脚本——它们会自动处理HMAC签名。
- CLI会对BLE设备（如窗帘、百叶窗等）进行预检查——需要启用Hub和云服务。
- 对于红外空调，仅支持`setAll`命令（不支持单独设置模式或温度）。
- 键盘相关命令（创建/删除密码）的结果会通过Webhook异步返回。
- 如果命令返回状态码160，表示设备不支持该命令——请使用场景功能作为备用方案。
- 严禁记录令牌和密钥信息。请让用户将这些信息设置为环境变量。

## 相关文件：

- `scripts/switchbot_cli.js` — Node.js CLI（用于列出设备、获取状态、发送命令和执行场景）
- `scripts/list_devices.sh` — 使用curl命令列出设备
- `scripts/get_status.sh` — 使用curl获取设备状态
- `scripts/send_command.sh` — 使用curl发送命令
- `scripts/list_scenes.sh` — 使用curl列出所有场景
- `scripts/execute_scene.sh` — 使用curl执行场景
- `references/commands.md` — 各设备类型的完整命令参考
- `references/examples.md` — 使用示例
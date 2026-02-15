---
name: switchbot-openapi
description: 使用官方的 OpenAPI (v1.1) 来控制和查询 SwitchBot 设备。当用户需要列出所有 SwitchBot 设备、获取设备状态或发送命令（如开关设备、执行特定操作、设置模式、锁定/解锁设备、调节温度、控制窗帘开合等）时，可以使用该接口。使用此功能需要提供 `SWITCHBOT_TOKEN` 和 `SWITCHBOT_SECRET` 这两个密钥。
---

# SwitchBot OpenAPI 技能

该技能使代理能够通过 HTTPS 请求访问官方 OpenAPI 来操作 SwitchBot 设备。它提供了可直接使用的脚本和 curl 模板；请使用这些脚本，而无需每次都重新计算 HMAC 签名。

## 快速入门（操作员）

1) 在 OpenClaw Gateway/容器中设置环境变量：
- `SWITCHBOT_TOKEN`：您的 OpenAPI 令牌
- `SWITCHBOT_SECRET`：您的 OpenAPI 密钥
- `SWITCHBOT_REGION`（可选）：默认为 `global`（api.switch-bot.com）。可选值：`global`、`na`、`eu`、`jp`。

2) 测试调用（列出设备）：
- Bash：`scripts/list_devices.sh`
- Node.js：`node scripts/switchbot_cli.js list`

3) 常见任务：
- 获取设备状态：`node scripts/switchbot_cli.js status <deviceId>`
- 开启设备：`node scripts/switchbot_cli.js cmd <deviceId> turnOn`
- 关闭设备：`node scripts/switchbot_cli.js cmd <deviceId> turnOff`
- 按下设备上的按钮：`node scripts/switchbot_cli.js cmd <deviceId> press`
- 将窗帘拉至 50% 位置：`node scripts/switchbot_cli.js cmd <deviceId> setPosition --pos 50`
- 锁定/解锁设备：`node scripts/switchbot_cli.js cmd <deviceId> lock` / `unlock`

## API 说明（简述）

根据区域划分的基地址：
- `global`：https://api.switch-bot.com
- `na`：https://api.switch-bot.com
- `eu`：https://api.switch-bot.com
- `jp`：https://api.switch-bot.com

使用路径前缀 `/v1.1`。

必需的请求头：
- `Authorization`：`<SWITCHBOT_TOKEN>`
- `sign`：使用 `SECRET` 对 `(token + timestamp + nonce)` 计算出的 HMAC-SHA256 值，并进行 Base64 编码
- `t`：以字符串形式表示的毫秒级时间戳
- `nonce`：随机生成的 UUID
- `Content-Type`：`application/json`

主要 API 端点：
- `GET /v1.1/devices`：列出所有设备
- `GET /v1.1/devices/{deviceId}/status`：获取设备的状态
- `POST /v1.1/devices/{deviceId}/commands`：向设备发送命令
  - 请求体：`{"command": "turnOn|turnOff|press|lock|unlock|setPosition|setTemperature|setMode|setVolume", "parameter": "<string>", "commandType": "command"}`
- `scenes`：当设备模型没有公开命令时，可以使用此 API 来执行场景操作
  - `GET /v1.1/scenes`：列出所有可用场景
  - `POST /v1.1/scenes/{sceneId}/execute`：执行特定场景

注意事项：
- 某些设备模型（例如某些 Robot Vacuum 系列）在 OpenAPI v1.1 中不提供直接的可执行命令。如果收到响应 `{statusCode: 160, message: "unknown command"}`，请在 SwitchBot 应用中创建一个对应的场景（例如 “Vacuum Start”），并通过 Scenes API 来执行该场景。

有关命令参数的详细信息，请参阅 `references/commands.md`。场景使用的示例请参见 `references/examples.md`。

## 代理应如何使用此技能

- 建议使用提供的脚本，因为它们会自动计算签名并处理重试逻辑。
- 在发送命令之前，CLI 会先检查设备的功能。对于支持蓝牙功能的设备（如 Bot、Lock、Curtain），需要设置 `enableCloudService=true` 且 `hubDeviceId` 不为空；如果这些参数缺失，系统会提示用户进行相应的设置（在 SwitchBot 应用中绑定 Hub 并启用云服务）。
- 如果环境变量缺失，应要求用户安全地提供或定义这些变量（切勿记录敏感信息）。
- 对于需要授权的操作（如解锁），应获取用户的明确确认；如果用户启用了二次验证功能，还可以要求输入一次性验证码。
- 如果遇到代码为 190（TokenInvalid）或 100（Unauthorized）的错误，请重新检查令牌/密钥的有效性、时间是否准确，或检查签名是否正确生成。

## 相关文件：

- `scripts/switchbot_cli.js`：用于列出设备状态和发送命令的 Node.js CLI 工具
- `scripts/list_devices.sh`：用于列出所有设备的 curl 命令
- `scripts/get_status.sh`：用于获取设备状态的 curl 命令
- `scripts/send_command.sh`：用于发送命令的 curl 命令
- `references/commands.md`：常见设备的命令参数说明
- `references/examples.md`：命令使用的示例及 JSON 输出格式

请保持此 SKILL.md 文件的简洁性；如需更多详细信息，请参阅相关参考文档。
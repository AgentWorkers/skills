---
name: openhue
description: 通过 OpenHue CLI 控制 Philips Hue 灯具/场景。
homepage: https://www.openhue.io/cli
metadata: {"clawdbot":{"emoji":"💡","requires":{"bins":["openhue"]},"install":[{"id":"brew","kind":"brew","formula":"openhue/cli/openhue-cli","bins":["openhue"],"label":"Install OpenHue CLI (brew)"}]}}
---

# OpenHue CLI

使用 `openhue` 命令通过 Hue Bridge 控制 Hue 灯具和场景。

**设置：**
- 发现可用的 Hue Bridge：`openhue discover`
- 自动化设置：`openhue setup`

**查询：**
- 获取灯具信息（JSON 格式）：`openhue get light --json`
- 获取房间信息（JSON 格式）：`openhue get room --json`
- 获取场景信息（JSON 格式）：`openhue get scene --json`

**操作：**
- 打开灯具：`openhue set light <id-or-name> --on`
- 关闭灯具：`openhue set light <id-or-name> --off`
- 调节亮度：`openhue set light <id> --on --brightness 50`
- 设置颜色：`openhue set light <id> --on --rgb #3399FF`
- 启动场景：`openhue set scene <scene-id>`

**注意事项：**
- 在设置过程中，可能需要按下 Hue Bridge 上的按钮。
- 当灯具名称不明确时，可以使用 `--room "房间名称"` 来指定灯具所属的房间。
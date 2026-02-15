---
name: eightctl
description: 控制八个睡眠舱（状态、温度、警报、调度）。
homepage: https://eightctl.sh
metadata: {"clawdbot":{"emoji":"🎛️","requires":{"bins":["eightctl"]},"install":[{"id":"go","kind":"go","module":"github.com/steipete/eightctl/cmd/eightctl@latest","bins":["eightctl"],"label":"Install eightctl (go)"}]}}
---

# eightctl

使用 `eightctl` 来控制 Eight Sleep 设备。需要身份验证。

**身份验证设置：**
- 配置文件：`~/.config/eightctl/config.yaml`
- 环境变量：`EIGHTCTL_EMAIL`、`EIGHTCTL_PASSWORD`

**快速操作：**
- 查看设备状态：`eightctl status`
- 启用/禁用设备：`eightctl on|off`
- 设置温度：`eightctl temp 20`

**常用功能：**
- 设置警报：`eightctl alarm list|create|dismiss`
- 创建/更新日程安排：`eightctl schedule list|create|update`
- 控制音频：`eightctl audio state|play|pause`
- 查看设备基本信息：`eightctl base info|angle`

**注意事项：**
- 该 API 并非官方提供，且存在访问速率限制，请避免频繁登录。
- 在更改设备温度或警报设置前，请务必确认操作的正确性。
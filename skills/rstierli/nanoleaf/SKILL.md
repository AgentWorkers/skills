---
name: nanoleaf
description: 通过 Picoleaf CLI 控制 Nanoleaf 灯板。可以用来开关 Nanoleaf 灯板、调节亮度、设置颜色（RGB/HSL）、更改色温，或执行任何与 Nanoleaf 灯具相关的控制操作。
homepage: https://github.com/tessro/picoleaf
metadata: {"clawdbot":{"emoji":"🌈","requires":{"bins":["picoleaf"]},"install":[{"id":"brew","kind":"brew","tap":"paulrosania/command-home","formula":"paulrosania/command-home/picoleaf","bins":["picoleaf"],"label":"Install Picoleaf CLI (brew)"},{"id":"binary","kind":"shell","command":"curl -sL https://github.com/tessro/picoleaf/releases/latest/download/picoleaf_1.4.0_linux_amd64.tar.gz | tar xz -C ~/.local/bin","bins":["picoleaf"],"label":"Install Picoleaf (binary)"}]}}
---

# Picoleaf CLI

使用 `picoleaf` 命令来控制 Nanoleaf 灯具面板。

## 设置
1. 查找 Nanoleaf 设备的 IP 地址：检查路由器配置或使用 mDNS：`dns-sd -Z _nanoleafapi`
2. 生成访问令牌：长按电源按钮 5-7 秒，直到 LED 灯闪烁，然后在 30 秒内运行以下命令：
   `curl -iLX POST http://<ip>:16021/api/v1/new`
3. 创建配置文件 `~/.picoleafrc`：
   ```ini
   host=<ip>:16021
   access_token=<token>
   ```

## 控制灯具状态
- `picoleaf on` - 打开灯具
- `picoleaf off` - 关闭灯具

## 调节亮度
- `picoleaf brightness <0-100>` - 设置亮度百分比（0-100）

## 调节颜色
- `picoleaf rgb <r> <g> <b>` - 设置 RGB 颜色（每个通道的值为 0-255）
- `picoleaf hsl <hue> <sat> <light>` - 设置 HSL 颜色（色调、饱和度、亮度）
- `picoleaf temp <1200-6500>` - 设置色温（单位：开尔文）

## 示例用法
- 调节为温暖、昏暗的灯光：`picoleaf on && picoleaf brightness 30 && picoleaf temp 2700`
- 调节为明亮的蓝色灯光：`picoleaf on && picoleaf brightness 100 && picoleaf rgb 0 100 255`
- 关闭灯具：`picoleaf off`

## 注意事项
- 默认端口为 16021
- 生成访问令牌需要物理接触 Nanoleaf 控制器
- 多个命令可以通过 `&&` 连接在一起执行
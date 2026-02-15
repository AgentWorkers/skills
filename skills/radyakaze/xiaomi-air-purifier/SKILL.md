---
name: xiaomi-air-purifier
description: 通过 Mi Cloud 监控和控制小米 Air Purifier 4 Lite。当需要检查空气质量、湿度、净化器状态时，或者需要开启/关闭净化器、调整风扇模式或风速时，都可以使用该功能。支持多房间设置。
---

# 小米空气净化器控制

通过小米云API（Xiaomi Cloud API）来控制和监控小米Air Purifier 4 Lite（型号：`zhimi.airp.rmb1`）。支持多台设备，并可针对特定房间进行操作。

## 设置

1. 安装所需依赖项：
```bash
cd xiaomi-air-purifier && pnpm install
```

2. 登录小米云（验证码将通过短信/电子邮件发送）：
```bash
pnpm exec xmihome login -u <email/phone> -p <password> -c <country>
```
支持的国家：`sg`（新加坡）、`ru`（俄罗斯）、`us`（美国）、`cn`（中国）

3. 列出设备以验证设备是否已被成功添加到小米云：
```bash
node scripts/purifier.js devices
```

## 使用方法

命令可以根据**房间名称**、**设备名称**或**设备ID**来执行具体操作。如果没有指定目标，系统会使用默认设置或唯一可用的设备。

```bash
node scripts/purifier.js status [room]      # Check status (e.g., status Bedroom)
node scripts/purifier.js status-full [room] # Show full status (incl. filter)
node scripts/purifier.js on [room]          # Power on
node scripts/purifier.js off [room]         # Power off
node scripts/purifier.js mode <0-2> [room]  # 0=Auto, 1=Sleep, 2=Favorite
node scripts/purifier.js level <0-14> [room]# Fan speed (Favorite mode)
node scripts/purifier.js brightness <0-2> [room]
node scripts/purifier.js buzzer <on|off> [room]
node scripts/purifier.js lock <on|off> [room]
```

## 快速参考

| 属性          | siid   | piid   | 类型    | 描述                |
|----------------|-------|-------|---------------------|
| 电源状态       | 2      | 1      | bool   | 开/关                |
| 模式           | 2      | 4      | int    | 0=自动模式；1=睡眠模式；2=常用模式 |
| 相对湿度       | 3      | 1      | int    | 相对湿度（%）            |
| PM2.5浓度     | 3      | 4      | int    | 空气质量（μg/m³）          |
| 温度          | 3      | 7      | float   | 温度（°C）             |
| 过滤器寿命     | 4      | 1      | int    | 过滤器剩余使用寿命（%）       |
| 蜂鸣器        | 6      | 1      | bool   | 是否开启通知音            |
| 儿童锁         | 8      | 1      | bool   | 是否启用物理按钮锁          |
| 风扇转速       | 9      | 11      | int    | 风扇转速（0-14，常用模式）       |
| 亮度          | 13      | 2      | int    | 灯光亮度（0=关闭；1=昏暗；2=明亮）   |
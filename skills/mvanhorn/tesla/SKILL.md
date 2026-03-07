---
name: tesla
version: "1.1.0"
description: 控制您的特斯拉车辆——包括锁定/解锁、调节车内温度、查看车辆位置、查看充电状态等。通过特斯拉车队API（Tesla Fleet API），您可以同时管理多辆特斯拉车辆。
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-tesla
homepage: https://developer.tesla.com/docs/fleet-api
metadata:
  openclaw:
    emoji: "🚗"
    requires:
      env:
        - TESLA_EMAIL
    primaryEnv: TESLA_EMAIL
    tags:
      - tesla
      - vehicle
      - iot
      - fleet-api
---
# 特斯拉（Tesla）

您可以通过 OpenClaw 来控制您的特斯拉车辆。一个账户可以同时管理多辆特斯拉汽车。

> **车队 API 更新（2026 年）：** 特斯拉已停止支持直接的 `/command` REST 调用。使用 2024.26 及更高版本的固件的车辆需要使用 Vehicle Command Protocol (VCP) SDK。`tesla-fleet-api` Python 包（v1.x 及以上版本）可以自动处理这些请求。

## 设置（Setup）

### 首次认证（First-time authentication）：

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

此过程将：
1. 显示特斯拉的登录页面
2. 您在浏览器中登录并授权
3. 然后将回调 URL 复制并粘贴回来
4. 生成的令牌会被缓存起来以供将来使用（有效期约 30 天，会自动更新）

## 环境变量（Environment variables）：

- `TESLA_EMAIL` — 您的特斯拉账户邮箱
- 令牌缓存于 `~/.tesla_cache.json` 文件中

## 多车辆支持（Multi-Vehicle Support）

使用 `--car` 或 `-c` 参数来指定目标车辆：

```bash
# List all vehicles
python3 {baseDir}/scripts/tesla.py list

# Commands for specific car
python3 {baseDir}/scripts/tesla.py --car "Snowflake" status
python3 {baseDir}/scripts/tesla.py -c "Stella" lock
```

如果不指定 `--car` 参数，所有命令将作用于您的第一辆特斯拉车辆。

## 命令（Commands）：

```bash
# List all vehicles
python3 {baseDir}/scripts/tesla.py list

# Get vehicle status
python3 {baseDir}/scripts/tesla.py status
python3 {baseDir}/scripts/tesla.py --car "Stella" status

# Lock/unlock
python3 {baseDir}/scripts/tesla.py lock
python3 {baseDir}/scripts/tesla.py unlock

# Climate
python3 {baseDir}/scripts/tesla.py climate on
python3 {baseDir}/scripts/tesla.py climate off
python3 {baseDir}/scripts/tesla.py climate temp 72

# Charging
python3 {baseDir}/scripts/tesla.py charge status
python3 {baseDir}/scripts/tesla.py charge start
python3 {baseDir}/scripts/tesla.py charge stop

# Location
python3 {baseDir}/scripts/tesla.py location

# Honk & flash
python3 {baseDir}/scripts/tesla.py honk
python3 {baseDir}/scripts/tesla.py flash

# Wake up (if asleep)
python3 {baseDir}/scripts/tesla.py wake
```

## 示例聊天用法（Example Chat Usage）：

- “我的特斯拉车锁上了吗？”
- “锁上 Stella 车”
- “Snowflake 车的电池电量是多少？”
- “我的 Model X 在哪里？”
- “打开 Stella 车的空调”
- “按 Snowflake 车的喇叭”

## API 参考（API Reference）

本工具使用了非官方的特斯拉车主 API，详细文档请参考：
https://tesla-api.timdorr.com

## 隐私与安全（Privacy & Security）：

- 凭据仅存储在本地
- 令牌会自动更新（有效期约 30 天）
- 不会向第三方发送任何数据
- 所有数据均严格保密
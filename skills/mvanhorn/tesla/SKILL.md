---
name: tesla
description: 控制您的特斯拉车辆——包括锁定/解锁、调节车内温度、查看车辆位置、查看充电状态等更多功能。支持同时管理多辆特斯拉车辆。
homepage: https://tesla-api.timdorr.com
user-invocable: true
disable-model-invocation: true
metadata:
  clawdbot:
    emoji: "🚗"
    primaryEnv: TESLA_EMAIL
    requires:
      bins: [python3]
      env: [TESLA_EMAIL]
---

# 特斯拉（Tesla）

您可以通过 Clawdbot 来控制您的特斯拉汽车。一个账户可以同时控制多辆汽车。

## 设置（Setup）

### 首次认证（First-time authentication）：

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

操作步骤如下：
1. 系统会显示特斯拉的登录页面。
2. 您需要在浏览器中登录并完成身份验证。
3. 登录完成后，将返回的回调 URL 复制并粘贴回 Clawdbot。
4. 生成的 OAuth 令牌会缓存到 `~/.tesla_cache.json` 文件中，有效期约为 30 天，并会自动更新。

### 环境变量（Environment variables）：
- `TESLA_EMAIL`：您的特斯拉账户邮箱地址。
- 令牌存储在 `~/.tesla_cache.json` 文件中。

## 多车支持（Multi-Vehicle Support）

使用 `--car` 或 `-c` 参数来指定要控制的车辆：

```bash
# List all vehicles
python3 {baseDir}/scripts/tesla.py list

# Commands for specific car
python3 {baseDir}/scripts/tesla.py --car "Snowflake" status
python3 {baseDir}/scripts/tesla.py -c "Stella" lock
```

如果没有指定车辆，系统将默认控制您的首辆汽车。

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
- “锁上 Stella 车。”
- “Snowflake 车的电池电量是多少？”
- “我的 Model X 在哪里？”
- “打开 Stella 车的空调。”
- “按一下 Snowflake 车的喇叭。”

## API 参考（API Reference）：

该技能使用的是非官方的特斯拉车主 API，详细文档请参考：
https://tesla-api.timdorr.com

## 故障排除（Troubleshooting）：
- 如果认证失败，请尝试在手机浏览器中访问登录页面。
- 确保您使用的是正确的特斯拉账户。
- 清除浏览器缓存后重新尝试。

## 安全性与权限（Security & Permissions）：
- 该技能用于控制实体车辆，请谨慎使用。
- 该技能通过 `teslapy` 库使用特斯拉官方的 OAuth 流程进行身份验证。
- 该技能会通过特斯拉的官方 API 发送车辆控制命令（如锁车、解锁、调节温度、充电等）。
- OAuth 令牌会缓存到 `~/.tesla_cache.json` 文件中。
- 所有通信仅限于您的机器与特斯拉服务器之间。

**该技能的功能限制：**
- 不会存储您的特斯拉密码，而是使用 OAuth 令牌进行身份验证。
- 不会向任何第三方发送您的凭证或车辆数据。
- 不会访问特斯拉 API 之外的任何系统资源。
- 该技能不能被代理程序自动执行（`disable-model-invocation: true`）。
- 每个命令都需要您手动触发代理程序来执行。

**安全提示：**
- 令牌的缓存文件 `~/.tesla_cache.json` 具有受限的访问权限。
- 令牌会自动更新，有效期约为 30 天。
- 请仅在可信任的个人设备上使用该技能。
- 在首次使用前，请查看 `scripts/tesla.py` 文件，确保该脚本仅与特斯拉的官方 API 进行通信。
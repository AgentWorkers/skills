---
name: tesla
description: 控制您的特斯拉车辆——实现锁车/解锁、调节车内温度、查看车辆位置、查看充电状态等功能。支持多辆特斯拉车辆。
homepage: https://tesla-api.timdorr.com
user-invocable: true
disable-model-invocation: true
metadata:
  clawdbot:
    emoji: "ðŸš—"
    primaryEnv: TESLA_EMAIL
    requires:
      bins: [python3]
      env: [TESLA_EMAIL]
---
# 特斯拉（Tesla）

您可以通过 Openclaw 来控制您的特斯拉汽车。一个账户可以同时管理多辆汽车。

## 设置

[安装和使用说明](https://claude.ai/public/artifacts/8b737407-c689-4d2c-ba95-aad6bc49992b)

### 首次认证：

```bash
TESLA_EMAIL="you@email.com" python3 {baseDir}/scripts/tesla.py auth
```

操作步骤如下：
1. 系统会显示特斯拉的登录页面。
2. 您需要在浏览器中登录并授权。
3. 登录完成后，将返回的回调 URL 复制并粘贴回系统。
4. 系统会缓存该授权令牌，以便后续使用（有效期约为 30 天，会自动更新）。

### 环境变量：

- `TESLA_EMAIL`：您的特斯拉账户邮箱地址
- 授权令牌存储在 `~/.tesla_cache.json` 文件中。

## 多车辆支持

使用 `--car` 或 `-c` 参数来指定目标车辆：

```bash
# List all vehicles
python3 {baseDir}/scripts/tesla.py list

# Commands for specific car
python3 {baseDir}/scripts/tesla.py --car "Snowflake" status
python3 {baseDir}/scripts/tesla.py -c "Stella" lock
```

如果没有指定车辆，系统将默认操作您的首辆汽车。

## 命令列表

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

## 示例对话：

- “我的特斯拉车锁上了吗？”
- “给 Stella 车锁上”
- “Snowflake 的电池电量是多少？”
- “我的 Model X 在哪里？”
- “打开 Stella 车内的空调”
- “按 Snowflake 的喇叭”

## API 参考

该技能使用的是非官方的特斯拉车主 API，详细文档请参考：
https://tesla-api.timdorr.com

## 故障排除

**认证失败？**
- 请尝试在手机浏览器中访问认证页面。
- 确保您使用的是正确的特斯拉账户。
- 清除浏览器缓存后重新尝试。

## 安全与权限

**请谨慎使用此技能，因为它用于控制实体车辆。**

**该技能的功能：**
- 通过 `teslapy` 库使用特斯拉官方的 OAuth 流程进行身份验证。
- 向特斯拉的官方 API 发送车辆控制命令（如锁车、解锁、调节温度、充电等）。
- 将 OAuth 令牌缓存在本地的 `~/.tesla_cache.json` 文件中。
- 所有通信仅限于您的设备与特斯拉服务器之间。

**该技能不执行以下操作：**
- 不会存储您的特斯拉密码（仅使用 OAuth 令牌）。
- 不会向任何第三方发送您的凭证或车辆数据。
- 不会访问特斯拉 API 之外的任何系统资源。
- 该技能不能被自动化执行（`disable-model-invocation: true`）。
- 每个命令都需要您手动触发。

**安全提示：**
- 保存在 `~/.tesla_cache.json` 中的令牌具有受限权限。
- 令牌会自动更新，有效期约为 30 天。
- 请仅在可信赖的个人设备上使用此技能。
- 首次使用前请查看 `scripts/tesla.py` 文件——该脚本仅与特斯拉的官方 API 进行通信。
---
name: google-home
description: 使用 `curl` 和 `jq` 通过 Google 智能设备管理 API 控制 Google Nest 设备（恒温器、摄像头、门铃）。
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["curl","jq"]}}
---

# Google Home / Nest CLI

通过使用 `curl` 和 `jq`，可以通过智能设备管理（Smart Device Management, SDM）API 来控制 Google Nest 设备。

## 设置（必需）

1. **创建一个 Google Cloud 项目**
   - 访问 https://console.cloud.google.com
   - 创建一个新的项目

2. **启用 SDM API**
   - 在“APIs & Services”中选择“Library”
   - 搜索“Smart Device Management”
   - 启用该 API

3. **创建 OAuth 凭据**
   - 在“APIs & Services”中选择“Credentials”
   - 创建一个 OAuth 2.0 客户端 ID
   - 下载 JSON 文件
   - 提取 `client_id` 和 `client_secret`

4. **注册您的设备**
   - 访问 https://nests.google.com/frame/register-user
   - 同意服务条款

5. **获取访问令牌**
   ```bash
   # Replace with your values
   curl -s \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "refresh_token=YOUR_REFRESH_TOKEN" \
     -d "grant_type=refresh_token" \
     https://www.googleapis.com/oauth2/v4/token
   ```

## 快速入门

```bash
# List devices
google-home-cli devices

# Get thermostat info
google-home-cli thermostat "Living Room" --info

# Set temperature (heat/cool/auto)
google-home-cli thermostat "Living Room" --temp 72

# Query camera
google-home-cli camera "Front Door" --status
```

## 设备命令

### 温控器
- `google-home-cli thermostat <设备名称>` — 显示当前温度/湿度
- `--temp <温度>` — 设置目标温度
- `--mode heat|cool|auto` — 设置 HVAC 模式
- `--fan on|auto` — 控制风扇

### 摄像头和门铃
- `google-home-cli camera <设备名称>` — 获取流媒体/设备状态
- `--snapshot` — 下载当前图片
- `--stream` — 开始实时流媒体

### 扬声器和显示屏
- `google-home-cli speaker <设备名称>` — 获取设备信息
- `--volume 0-100` — 设置音量
- `--stop` — 停止播放

## 环境变量

```bash
export GOOGLE_HOME_CLIENT_ID="your-client-id"
export GOOGLE_HOME_CLIENT_SECRET="your-client-secret"
export GOOGLE_HOME_ACCESS_TOKEN="your-access-token"
```

## 替代方案：直接调用 API

```bash
# List all devices
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices"

# Get device traits
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices/YOUR_DEVICE_ID"
```

## 辅助脚本

一个名为 `nest` 的 CLI 辅助脚本位于 `scripts/nest` 目录下：

```bash
# Make it available globally
ln -sf /Users/mitchellbernstein/clawd/skills/google-home/scripts/nest /usr/local/bin/nest

# List devices
nest list

# Get thermostat status
nest status "enterprises/PROJECT_ID/devices/DEVICE_ID"

# Set temperature (Celsius)
nest temp "enterprises/PROJECT_ID/devices/DEVICE_ID" 22

# Set mode
nest mode "enterprises/PROJECT_ID/devices/DEVICE_ID" HEAT
```

## 配置

创建 `~/.config/google-home/config.json` 文件：

```json
{
  "project_id": "your-google-cloud-project-id",
  "access_token": "your-oauth-access-token"
}
```

## 注意事项

- 访问令牌会过期，请定期刷新
- 设备名称使用完整路径：`enterprises/PROJECT_ID/devices/DEVICE_ID`
- 温度以摄氏度为单位（如需要可转换为华氏度）
- 摄像头流媒体功能需要额外的权限
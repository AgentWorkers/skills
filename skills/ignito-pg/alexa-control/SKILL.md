---
name: alexa-remote
description: 通过 CLI 控制 Alexa 设备——设置闹钟、播放音乐、查看简报、执行智能家居指令。当需要设置闹钟、在 Echo 设备上播放音乐、控制智能家居设备或向 Alexa 发送语音指令时，可以使用此方法。
---

# Alexa 遥控器

通过 [alexa-remote-control](https://github.com/adn77/alexa-remote-control) 使用 shell 命令来控制 Amazon Echo 设备。

## 设置

### 1. 克隆仓库

```bash
git clone https://github.com/adn77/alexa-remote-control.git
cd alexa-remote-control
```

### 2. 获取刷新令牌

该脚本需要从 Amazon 获取刷新令牌。请使用 [alexa-cookie-cli](https://github.com/adn77/alexa-cookie-cli)：

```bash
npx alexa-cookie-cli
```

这会打开一个浏览器页面，用于登录 Amazon。登录成功后，复制 `refreshToken`（以 `Atnr|...` 开头）。

### 3. 创建一个封装脚本

创建一个名为 `alexa-alarm.sh`（或类似名称）的脚本，并在其中设置凭据：

```bash
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TIME="${1:-7:00 am}"
DEVICE="${2:-Bedroom Echo Show}"

export REFRESH_TOKEN='Atnr|YOUR_TOKEN_HERE'
export AMAZON='amazon.co.uk'      # or amazon.com for US
export ALEXA='alexa.amazon.co.uk' # or alexa.amazon.com

"$SCRIPT_DIR/alexa_remote_control.sh" -d "$DEVICE" -e "textcommand:Set an alarm for $TIME"
```

使其可执行：`chmod +x alexa-alarm.sh`

## 使用方法

### 设置闹钟

```bash
./alexa-alarm.sh "6:30 am"                    # Default device
./alexa-alarm.sh "7:00 am" "Kitchen Echo"     # Specific device
```

### 常用命令

```bash
# Play flash briefing (news)
./alexa_remote_control.sh -d "Bedroom Echo Show" -e "textcommand:Play my flash briefing"

# Play music
./alexa_remote_control.sh -d "Kitchen Echo" -e "textcommand:Play BBC Radio 6"

# Smart home
./alexa_remote_control.sh -d "Living Room Echo" -e "textcommand:Turn off the lights"

# Weather
./alexa_remote_control.sh -d "Bedroom Echo Show" -e "textcommand:What's the weather"

# Timer
./alexa_remote_control.sh -d "Kitchen Echo" -e "textcommand:Set a timer for 10 minutes"
```

### 列出设备

```bash
./alexa_remote_control.sh -a  # Lists all devices with names/types
```

## 环境变量

| 变量 | 描述 | 示例 |
|----------|-------------|---------|
| `REFRESH_TOKEN` | Amazon 认证令牌 | `Atnr|EwMDI...` |
| `AMAZON` | Amazon 域名 | `amazon.co.uk` / `amazon.com` |
| `ALEXA` | Alexa 域名 | `alexa.amazon.co.uk` |

## 注意事项

- 令牌会定期过期；如果认证失败，请重新运行 `alexa-cookie-cli`。
- 设备名称区分大小写；使用 `-a` 参数来检查设备名称是否正确。
- 英国用户：使用 `amazon.co.uk` / `alexa.amazon.co.uk`。
- 美国用户：使用 `amazon.com` / `alexa.amazon.com`。
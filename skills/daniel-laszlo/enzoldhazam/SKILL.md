---
name: enzoldhazam
description: 控制 NGBS iCON 智能家居恒温器。当用户询问室内温度、供暖情况、恒温器设置，或希望调节房间温度时，请使用该功能。
---

# enzoldhazam

通过 enzoldhazam.hu 控制 NGBS iCON 智能家居恒温器。

## 设置

1. 安装命令行工具（CLI）：
```bash
git clone https://github.com/daniel-laszlo/enzoldhazam.git
cd enzoldhazam
go build -o enzoldhazam ./cmd/enzoldhazam
sudo mv enzoldhazam /usr/local/bin/
```

2. 登录（凭据存储在 macOS 的 Keychain 中）：
```bash
enzoldhazam login
```

或者设置环境变量：
```bash
export ENZOLDHAZAM_USER="your-email"
export ENZOLDHAZAM_PASS="your-password"
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `enzoldhazam status` | 显示所有房间的温度 |
| `enzoldhazam status --json` | 以 JSON 格式输出数据（便于处理） |
| `enzoldhazam get <房间>` | 获取特定房间的详细信息 |
| `enzoldhazam set <房间> <温度>` | 设置目标温度 |
| `enzoldhazam login` | 将凭据保存到 Keychain |
| `enzoldhazam logout` | 清除存储的凭据 |

## 示例

```bash
# Check current temperatures
enzoldhazam status

# Set a room to 22°C
enzoldhazam set "Living Room" 22

# Get room info as JSON
enzoldhazam get "Bedroom" --json
```

## 使用说明

当用户询问家庭温度、供暖系统或恒温器的相关信息时：

1. 使用 `enzoldhazam status` 查看当前状态 |
2. 使用 `enzoldhazam set <房间> <温度>` 来调整温度 |
3. 在需要处理数据时，解析 `--json` 格式的输出结果 |

在执行任何温度调整操作之前，请务必先与用户确认。
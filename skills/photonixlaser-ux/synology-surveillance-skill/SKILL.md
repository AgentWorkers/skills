---
name: synology-surveillance
description: 通过 Web API 控制 Synology 监控站（Surveillance Station）中的摄像头。该功能支持快照拍摄、实时流媒体传输、录像录制、云台（PTZ）控制以及事件监控。需要使用配备了 Surveillance Station 的 Synology NAS 设备。
---

# Synology Surveillance Station 技能

通过 Synology Surveillance Station API 来控制您的监控摄像头。

## 前提条件

1. 安装了 Surveillance Station 的 Synology NAS。
2. 拥有 Surveillance Station 权限的用户。
3. API 用户的 2FA（双重身份验证）功能已关闭。
4. 已安装 `jq` 工具（使用 `apt install jq` 安装）。

## 快速入门

### 1. 在 TOOLS.md 中配置

将连接信息添加到 `TOOLS.md` 文件中：

```markdown
### Synology Surveillance
- **Host:** 192.168.1.100 (deine NAS IP)
- **Port:** 5000 (HTTP) oder 5001 (HTTPS)
- **User:** surveillance_user
- **Pass:** dein_passwort
- **HTTPS:** false (true falls HTTPS aktiviert)
```

### 2. 测试登录

```bash
./scripts/syno-surveillance.sh login
```

### 3. 显示摄像头

```bash
./scripts/syno-surveillance.sh cameras
```

### 4. 创建快照

```bash
./scripts/syno-surveillance.sh snapshot 1
```

保存结果为：`syno_snapshot_1_1738972800.jpg`

### 5. 查看事件记录

```bash
# Letzte 10 Ereignisse
./scripts/syno-surveillance.sh events

# Letzte 50 Ereignisse
./scripts/syno-surveillance.sh events 50
```

## 可用命令

| 命令 | 描述 |
|--------|--------------|
| `login` | 创建会话（在其他命令执行时会自动登录） |
| `logout` | 结束会话 |
| `cameras` | 列出所有摄像头及其状态 |
| `snapshot <id>` | 为指定摄像头创建快照 |
| `record <id> start\|stop` | 启动/停止录像 |
| `events [limit]` | 查看事件日志 |
| `stream <id>` | 生成摄像头直播流 URL |
| `ptz <id> <direction>` | 移动 PTZ 摄像头（左/右/上/下/缩放） |
| `preset <id> <num>` | 执行 PTZ 摄像头的预设动作 |

## 环境变量

| 变量 | 默认值 | 描述 |
|----------|----------|--------------|
| `SYNOLOGY_HOST` | 192.168.1.100 | NAS 的 IP 地址或主机名 |
| `SYNOLOGY_PORT` | 5000 | NAS 的端口 |
| `SYNOLOGY_USER` | admin | 用户名 |
| `SYNOLOGY_PASS` | （空） | 密码 |
| `SYNOLOGY_HTTPS` | false | 是否使用 HTTPS |

## 直接使用 API 调用

如果脚本不适用，可以直接使用 `curl` 来调用 API：

```bash
# Login
curl -c cookies.txt "http://192.168.1.100:5000/webapi/auth.cgi?api=SYNO.API.Auth&method=login&version=3&account=USER&passwd=PASS&session=SurveillanceStation&format=cookie"

# Snapshot
curl -b cookies.txt "http://192.168.1.100:5000/webapi/entry.cgi?api=SYNO.SurveillanceStation.Camera&method=GetSnapshot&version=1&cameraId=1" -o snapshot.jpg
```

## API 详细信息

对于更复杂的操作，请参考 [references/api.md](references/api.md)。

## 集成到 Home Assistant

Home Assistant 用户也可以将此技能用于自动化任务：

```yaml
shell_command:
  syno_snapshot: "/pfad/zu/syno-surveillance.sh snapshot {{ camera_id }}"
```

## 故障排除

- **登录失败**：检查密码是否正确，或关闭 2FA 功能。
- **权限不足**：确保用户具有 Surveillance Station 的相应权限。
- **找不到摄像头**：使用 `cameras` 命令检查摄像头 ID。
- **快照为空**：可能是摄像头离线或未授权使用。

## 许可证说明

Surveillance Station 需要为每个摄像头购买许可证（大多数 NAS 型号包含 2 个免费许可证）。
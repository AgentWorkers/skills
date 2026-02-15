---
name: device-assistant
version: 1.0.0
description: "这是一个个人设备与电器管理工具，具备错误代码查询和故障排除功能。它可以记录您所有的设备（包括电器、电子产品及软件），并附有型号、使用手册和保修信息。当设备出现故障时，您只需输入相应的错误代码，即可立即获得解决方案。适用场景：设备显示错误信息、需要查阅使用手册、检查保修情况、添加新设备或接收设备维护提醒。触发命令：/device、/geräte、'我的洗碗机'、'错误代码E24'、'故障提示'、'设备问题'、'电器故障'。"
author: clawdbot
license: MIT
metadata:
  clawdbot:
    emoji: "🔧"
    triggers: ["/device", "/geräte"]
    requires:
      bins: ["jq", "curl"]
  tags: ["devices", "appliances", "troubleshooting", "maintenance", "home", "warranty"]
---

# 设备助手 🔧

这是一个个人设备管理工具，具备错误代码查询、故障排除和维护记录功能。

## 主要功能

- **设备注册**：记录所有设备的型号、序列号和购买信息
- **错误代码查询**：即时提供错误代码的解释
- **故障排除**：提供分步解决建议
- **手册链接**：快速访问设备使用手册
- **保修信息**：显示保修期限
- **维护提醒**：通知设备需要更换部件或更新软件

## 命令

| 命令 | 功能 |
|---------|--------|
| `/device` | 列出所有设备或查看设备状态 |
| `/device add` | 添加新设备（交互式操作） |
| `/device list [类别]` | 按类别列出设备 |
| `/device info <设备名称>` | 查看设备详细信息 |
| `/device error <设备名称> <错误代码>` | 查询设备错误代码 |
| `/device help <设备名称> <问题>` | 故障排除建议 |
| `/device manual <设备名称>` | 获取设备使用手册 |
| `/device warranty` | 查看设备保修状态 |
| `/device maintenance` | 查看设备维护计划 |
| `/device remove <设备名称>` | 删除设备 |

## 自然语言交互

该工具支持以下自然语言查询：

- “我的洗碗机显示E24错误代码”
- “洗衣机发出奇怪的声音”
- “Thermomix的使用手册在哪里？”
- “电视的保修期什么时候到期？”

## 设备分类

| 分类 | 示例设备 |
|----------|----------|
| `厨房` | 洗碗机、冰箱、烤箱、Thermomix |
| `洗衣` | 洗衣机、烘干机 |
| `电子产品` | 电视、路由器、NAS、电脑 |
| `家居环境** | 空调、空气净化器 |
| `智能家居** | Hue智能灯泡、Homematic控制器、传感器 |
| `软件** | 应用程序、操作系统、许可证 |
| `其他** | 其他各类设备 |

## 后端处理命令

```bash
handler.sh status $WORKSPACE                     # Overview
handler.sh list [category] $WORKSPACE            # List devices
handler.sh add <json> $WORKSPACE                 # Add device
handler.sh info <device-id> $WORKSPACE           # Device details
handler.sh error <device-id> <code> $WORKSPACE   # Error lookup
handler.sh troubleshoot <device-id> <problem> $WS # Get help
handler.sh manual <device-id> $WORKSPACE         # Manual link
handler.sh warranty $WORKSPACE                   # Warranty overview
handler.sh maintenance $WORKSPACE                # Maintenance due
handler.sh update <device-id> <json> $WORKSPACE  # Update device
handler.sh remove <device-id> $WORKSPACE         # Remove device
handler.sh search <query> $WORKSPACE             # Search devices
handler.sh log <device-id> <note> $WORKSPACE     # Add maintenance log
```

## 数据结构

### 设备信息

```json
{
  "id": "dishwasher-1",
  "name": "Geschirrspüler",
  "nickname": "Spüli",
  "category": "kitchen",
  "manufacturer": "Siemens",
  "model": "SN658X06TE",
  "serialNumber": "ABC123456",
  "purchaseDate": "2022-03-15",
  "purchasePrice": 899,
  "warranty": {
    "expires": "2025-03-15",
    "type": "manufacturer",
    "notes": "3 Jahre Siemens"
  },
  "manualUrl": "https://...",
  "supportUrl": "https://...",
  "location": "Küche",
  "notes": "Salz alle 2 Monate nachfüllen",
  "maintenance": [
    {"task": "Filter reinigen", "interval": "monthly", "lastDone": "2026-01-01"}
  ],
  "errorHistory": [],
  "addedAt": "2024-01-01"
}
```

## 错误代码查询

该工具通过以下方式查询错误代码：

1. **内置数据库**：查询常见品牌的错误代码
2. **网络搜索**：根据设备型号和错误代码查找详细信息
3. **手动查找**：如果设备手册的在线链接存在，则直接访问该链接

### 常见错误代码格式

| 制造商 | 错误代码格式 | 示例 |
|--------------|---------|---------|
| Siemens/Bosch | E + 数字 | E24、E15 |
| Miele | F + 数字 | F11、F53 |
| AEG | E + 数字 | E10、E20 |
| Samsung | 字母 + 数字 | UE、OE、LE |
| LG | 字母 | OE、IE、PE |

## 使用示例

```
User: Ich habe einen neuen Geschirrspüler

Bot: 🔧 Neues Gerät hinzufügen:
     
     Welche Infos hast du?
     • Hersteller?
     • Modell?
     • Seriennummer? (optional)
     • Kaufdatum?

User: Siemens SN658X06TE, gekauft am 15.3.2022

Bot: ✅ Gespeichert!
     
     📦 Geschirrspüler (Siemens SN658X06TE)
     📅 Gekauft: 15.03.2022
     🛡️ Garantie: bis 15.03.2025 (ABGELAUFEN)
     📄 Anleitung: [Link gefunden]
     
     Spitzname vergeben? (z.B. "Spüli")
```

## 数据文件

数据文件存储在 `$WORKSPACE/memory/device-assistant/` 目录下：

| 文件名 | 用途 |
|------|---------|
| `devices.json` | 所有注册设备的信息 |
| `error-history.json` | 过去的错误记录及解决方法 |
| `maintenance-log.json` | 设备维护记录 |
| `error-codes/` | 缓存的错误代码信息 |

## 保修提醒

该工具会在保修期到期前提醒用户。

```
⚠️ Garantie-Warnung:

Diese Geräte laufen bald ab:
• TV Samsung (noch 30 Tage)
• Waschmaschine (noch 45 Tage)

Tipp: Jetzt prüfen ob alles funktioniert!
```

## 所需软件/工具

- `jq`（用于处理JSON数据）
- `curl`（用于网络请求）
- 互联网连接（用于查询错误代码）
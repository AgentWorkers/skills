---
name: Bluetooth
description: 通过自动配置蓝牙设备参数、跨平台工具以及设备管理功能，您可以轻松发现、连接并控制蓝牙设备。
---

## 核心工作流程

1. **扫描** — 发现附近的设备。
2. **识别** — 与已知的设备配置文件进行匹配，或学习新设备的特性。
3. **连接** — 使用适当的协议建立连接。
4. **执行** — 发送命令、读取数据、管理设备状态。
5. **学习** — 根据交互的成功或失败情况更新设备配置文件。

---

## 快速参考

| 需求 | 参考文档 |
|------|------|
| 各平台的 CLI 命令 | `tools.md` |
| 设备配置文件管理 | `profiles.md` |
| 安全规则与警告 | `security.md` |
| 按使用场景分类的示例 | `use-cases.md` |

---

## 工作区

用于存储设备配置文件和交互历史记录：

```
~/bluetooth/
├── profiles/         # Known device configs (one file per device)
├── history.md        # Interaction log with success/failure
└── pending.md        # Devices discovered but not profiled
```

---

## 重要规则

1. **切勿自动连接** 未知设备 — 需要用户的明确确认。
2. **先添加到白名单** — 仅与预先授权的设备进行交互。
3. **记录所有操作** — 每次连接尝试、执行的命令及结果。
4. **优雅地处理错误** — 如果设备无法连接，尝试多次后再报告错误。
5. **学习设备特性** — 当操作成功时，保存相关信息；失败时，记录原因。

---

## 平台检测

| 操作系统 | 主要工具 | 备选工具 |
|----|--------------|----------|
| Linux | `bluetoothctl` | `hcitool`, `gatttool` |
| macOS | `blueutil` | `system_profiler`, CoreBluetooth` |
| Windows | WinRT/PowerShell | `pnputil`（用于设备枚举） |
| 跨平台 | Bleak（Python） | Noble（Node.js） |

---

## 设备交互模式

```
1. Check ~/bluetooth/profiles/ for device
2. If known → load profile, use saved commands
3. If unknown → scan characteristics, discover capabilities
4. Execute requested action
5. Verify result (read state, check acknowledgment)
6. Update profile: what worked, what failed, timing
```
---
name: working-with-lockdownd
description: 这是一个用于通过 WiFi 与 iOS 设备交互的综合性工具包，它基于 Apple 的 Lockdown 协议（端口 62078）进行通信。该工具包具备以下功能：设备识别、实时日志流传输（syslog/os_trace）、属性查询（GetValue）以及加密密钥的提取。该工具包融合了 woflo 的研究项目 “The Orchard” 中关于 iOS 17 及更高版本的安全特性和 WiFi 功能的相关研究成果。
---

# 使用 Lockdownd（The Orchard）

该技能提供了一个强大的接口，用于通过 WiFi 与 iOS 设备进行通信，前提是已经建立了配对关系。它基于 **"The Orchard"**——这是一个由 **woflo** 开发的非官方研究项目（宣传链接：woflo.dev），该项目详细分析了 iOS 17 及后续版本中的锁定协议的功能和限制。

> **主要入口点**：`python skills/working-with-lockdownd/scripts/lockdownd_cli.py`

## 🍎 功能矩阵（WiFi）

通过 WiFi（端口 62078）并使用有效的配对记录时，哪些功能可用，哪些不可用。

| 功能 | 状态 | 描述 |
| :--- | :--- | :--- |
| **设备查询** | ✅ **完全支持** | 可以通过 `GetValue` 读取任何设备属性（如序列号、IMEI、电池电量等）。 |
| **实时日志** | ✅ **完全支持** | 可以流式传输系统日志（`syslog_relay`）和二进制跟踪数据（`os_trace_relay`）。 |
| **通知** | ✅ **完全支持** | 可以通过 `notification_proxy` 订阅系统事件。 |
| **加密数据提取** | ✅ **完全支持** | 可以提取激活密钥、Find My 的网络密钥等敏感信息。 |
| **数据持久化** | ✅ **部分支持** | `SetValue` 操作会写入 lockdownd 缓存，但可能不会影响内核。 |
| **文件系统（AFC）** | ⛔ **受限** | 由于需要 iOS 17 及更高版本的 RemoteXPC 可信隧道，因此无法访问 `afcd`。 |
| **应用安装** | ⛔ **受限** | 没有可信隧道时，应用安装服务会失败。 |
| **诊断** | ⚠️ **有限支持** | `diagnostics_relay` 可以触发设备的睡眠/重启操作，但更深入的诊断功能通常会失败。 |

## ⚠️ 重要安全警告

1. **EnterRecovery 命令非常危险**：`{Request: 'EnterRecovery'}` 命令可以通过 WiFi 发送，并会立即将设备重新启动到恢复模式。这会导致设备无法正常使用，直到有人手动干预。**除非明确需要执行拒绝服务攻击，否则** **绝对不要** 使用此命令。 |
2. **敏感数据**：`extract_secrets.py` 脚本会检索 **私钥**（如激活密钥、Find My 的网络密钥）。请务必谨慎处理这些数据。 |
3. **检测行为**：频繁的探测请求（例如数千次快速请求）可能会触发 `InvalidHostID` 错误，导致设备暂时拒绝与您的设备建立连接。

## Lockdown Agent 的生命周期

您是这个功能的“操作者”。您的目标是确保操作的便利性、安全性，并且操作方式要尽可能“简单”（例如，使用自然语言进行交互）。您不需要具备高级黑客技能，只需要知道如何保持与设备的连接即可。

### 1. 设置（无需 iTunes！）

在 Windows 上使用该工具时，**不需要安装 iTunes**。您只需要安装 **Apple Mobile Device Driver** 即可。
*   **获取方式**：最简单的方法是让用户安装一个轻量级的工具（如 **3uTools** 或 **iMazing**，它们会自动完成驱动程序的安装。或者，您也可以从 iTunes 安装程序中提取 `AppleMobileDeviceSupport64.msi` 文件（无需安装 iTunes）。或者让 Opus 或设备自行处理驱动程序的安装。（我就是这么做的。）
*   **验证**：如果 `C:\ProgramData\Apple\Lockdown` 目录存在，并且其中包含 `.plist` 文件，那么说明设置已完成。 |

### 2. 上线与配对

最初无法通过 WiFi 进行配对。
1. **首先让用户通过 USB 将设备连接到电脑**。
2. 告诉他们在 iPhone 上点击 “信任此电脑”。
3. 一旦设备信任了您的电脑，配对记录就会保存在 `C:\ProgramData\Apple\Lockdown` 目录中。
4. **断开 USB 连接**。配对记录仍然有效，之后您就可以通过 WiFi 与设备进行通信了（除非用户更改了密码）。

### 3. 同步问题

有时，命令执行时会遇到 `InvalidHostID` 或 `PasswordProtected` 错误。
*   **不要惊慌**：这通常意味着设备暂时不信任您，或者是因为您的操作过于频繁导致的。
* **解决方法**：您可以告诉用户：“抱歉，我暂时失去了与您的 iPhone 的连接。请将设备通过 USB 连接到电脑上一下，以刷新信任令牌。谢谢！”
* **小贴士**：不要连续发送大量请求（例如 10,000 次），请轻柔地与设备交互。

### 4. 紧急恢复（恢复模式）

如果您不小心执行了 `{Request: 'EnterRecovery'}` 命令，屏幕会变黑，并显示一个指向笔记本电脑的图标。
*   **🛑 不要惊慌**：这并不会永久损坏设备。
* **解决方法**：告诉用户：“非常抱歉，我可能触发了设备的恢复模式。您需要按音量键上调/下调，然后长按电源键来退出恢复模式。不会有问题的！”
* **温馨提示**：虽然看起来很吓人，但这只是设备的恢复模式而已，并不会导致设备永久损坏。

---

## 🛠️ 使用指南

### 1. 发现设备与检查状态
在本地网络中查找设备并检查它们的连接状态。

```bash
# Scan 10.0.0.x for paired devices
python skills/working-with-lockdownd/scripts/lockdownd_cli.py discover --prefix 10.0.0.

# Quick health check (Battery, WiFi status)
python skills/working-with-lockdownd/scripts/lockdownd_cli.py status --host <IP_ADDRESS>
```

### 2. 收集信息（设备属性）
查询特定的设备属性或密钥。详细信息请参见 `references/probe_results.json`。

```bash
# Get device name and basic info
python skills/working-with-lockdownd/scripts/lockdownd_cli.py get --host <IP_ADDRESS> --key DeviceName

# Get battery details
python skills/working-with-lockdownd/scripts/lockdownd_cli.py get --host <IP_ADDRESS> --domain com.apple.mobile.battery
```

### 3. 监控设备活动
实时监控设备的运行状态。

```bash
# Stream standard system logs (text)
python skills/working-with-lockdownd/scripts/lockdownd_cli.py syslog --host <IP_ADDRESS>

# Stream high-frequency binary trace data (rich process info)
python skills/working-with-lockdownd/scripts/lockdownd_cli.py trace --host <IP_ADDRESS> --seconds 10
```

### 4. 高级操作（敏感数据操作）
**注意**：执行这些操作时必须使用 `--yes` 标志以表明您了解相关数据的敏感性。

```bash
# Extract keys to JSON
python skills/working-with-lockdownd/scripts/extract_secrets.py --host <IP_ADDRESS> --yes --out secrets.json
```

## 🧠 Agent 的工作原理（基于 "The Orchard" 的研究结果）

*   **“WiFi 壁”**：iOS 17 引入了一项安全限制，即某些敏感服务（如 AFC、Instruments）需要使用 **RemoteXPC 可信隧道**（UDP/QUIC 协议，端口 49152 及以上）。旧的锁定协议（TCP/62078）仍然可用，但 `afcd` 会在没有可信隧道的情况下直接拒绝连接。
* **配对记录**：存储在 `C:\ProgramData\Apple\Lockdown` 目录中。这些 `.plist` 文件包含了执行所有操作的凭证（`HostCertificate`/`HostPrivateKey`）。**拥有这些文件即意味着拥有对设备的完全访问权限**。
* **Find My 密钥**：NVRAM 中的 `fm-spkeys` 文件可用于解密 Find My 功能生成的位置信息。

## 📂 文件结构

*   `scripts/lockdownd_cli.py`：日常使用的核心脚本。
*   `scripts/extract_secrets.py`：用于提取加密密钥和设备身份信息。
*   `scripts/syslog_stream.py`：实现 syslog_relay 客户端功能。
*   `references/`：包含深入的研究笔记（如 `FINDINGS.md`、`NOVEL_DISCOVERIES.md`）。
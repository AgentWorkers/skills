---
name: intiface-control
description: 通过 Intiface Central 和 buttplug-mcp，您可以使用自然语言控制 750 多种 BLE（蓝牙低功耗）智能设备（如 Lovense、Kiiroo、We-Vibe、Satisfyer 等）。该系统支持 macOS、Windows 和 Linux 操作系统，无需进行任何协议逆向工程。
metadata: {"openclaw": {"requires": {"bins": ["mcporter", "buttplug-mcp"]}}}
---
# 通过 Intiface 实现对各种设备的通用控制

您可以使用 OpenClaw，通过自然语言控制任何与 [Buttplug.io 兼容的设备](https://iostindex.com)——涵盖所有主流品牌的 750 多种玩具。

## 工作原理

```
OpenClaw agent
    → mcporter (stdio)
    → buttplug-mcp
    → Intiface Central (WebSocket)
    → Your device (Bluetooth / USB)
```

无需进行逆向工程，也无需编写针对特定设备的代码。该功能支持 **macOS、Windows 和 Linux** 系统。

---

## 先决条件

- [Intiface Central](https://intiface.com/central/)——免费桌面应用程序（跨平台）
- `buttplug-mcp`——用于连接 Buttplug 设备和 Intiface 的中间件
- `mcporter`——通过 OpenClaw 的 `mcporter` 技能进行安装

### 安装 buttplug-mcp

**macOS (Homebrew):**
```bash
brew tap conacademy/homebrew-tap
brew install conacademy/tap/buttplug-mcp
```

**其他平台:** 从 [ConAcademy/buttplug-mcp](https://github.com/ConAcademy/buttplug-mcp/releases) 下载

---

## 一次性设置

### 第一步——安装并打开 Intiface Central

从 [intiface.com/central](https://intiface.com/central/) 下载并安装该应用程序。打开后点击 **Start Server**（启动服务器）。服务器默认监听 `ws://localhost:12345` 端口。

### 第二步——连接设备

在 Intiface Central 中点击 **Start Scanning**（开始扫描）。给设备通电，设备一旦出现在列表中，扫描即可停止。

### 第三步——安装 mcporter 技能

在 OpenClaw 中输入命令：`install skill mcporter`（安装 `mcporter` 技能）。

---

## 代理可使用的命令

### 列出已连接的设备
```bash
mcporter call --stdio "buttplug-mcp --ws-port 12345" device_vibrate --list
```

### 使设备振动
```bash
mcporter call --stdio "buttplug-mcp --ws-port 12345" device_vibrate id=0 strength=0.7
```

- `id`：设备索引（0 表示第一个设备）
- `strength`：范围 0.0 到 1.0（0.0 表示停止振动）

### 停止设备
```bash
mcporter call --stdio "buttplug-mcp --ws-port 12345" device_vibrate id=0 strength=0.0
```

---

## 振动强度说明

| 强度值 | 振动感受 |
|-------|------|
| 0.1–0.2 | 微弱 |
| 0.3–0.5 | 中等 |
| 0.6–0.8 | 强烈 |
| 0.9–1.0 | 最大 |

---

## 支持的品牌（部分列表）

Lovense · Kiiroo · We-Vibe · Satisfyer · The Handy · OSR-2/SR-6 · 以及 [700 多个其他品牌](https://iostindex.com)

---

## 代理行为规则

- 定时操作结束后，设备会自动停止（振动强度为 0.0），除非用户另有指示
- 除非用户指定其他设备，否则默认使用设备 `id=0`
- 在执行任何命令之前，必须确保 Intiface Central 正在运行；如果命令失败，会提醒用户
- 请勿使用 `notify` 工具

---

## 常见问题及解决方法

| 问题 | 解决方法 |
|---------|-----|
| 连接失败 | 打开 Intiface Central 并点击 Start Server |
| 设备未找到 | 在 Intiface Central 中点击 Start Scanning，然后重启设备 |
| 未找到 buttplug-mcp | 运行命令 `brew install conacademy/tap/buttplug-mcp` |
| 未找到 mcporter | 在 OpenClaw 中输入命令：`install skill mcporter` |
| 使用错误的设备索引 | 先列出所有设备，然后使用正确的 `id`
---
name: venus-ble-vibrator
description: 通过自然语言控制 Venus (Cachito) 这款蓝牙振动器。该功能指示代理程序如何调用本地的 HTTP 服务器，该服务器会通过 macOS 的 CoreBluetooth 功能向玩具发送蓝牙指令。安装前请先参阅下方的 README 文件以了解所需的硬件设置。
metadata: {"openclaw": {"os": ["darwin"]}}
---
# Venus BLE振动器控制

通过OpenClaw使用自然语言来控制**Venus / Cachito BLE振动器**。该代理程序会调用一个本地HTTP API，该API会向振动器发送BLE广告信号。

> ⚠️ **仅适用于macOS**。服务器使用的是CoreBluetooth（仅适用于Apple系统），不支持Linux/Windows。

---

## 所需设备

**硬件：**
- Venus振动器设备
- Cachito实体控制器（已与Venus设备配对）
- 具备蓝牙功能的Mac电脑

**软件：**
- Python 3.12及以上版本，以及[`uv`](https://docs.astral.sh/uv/getting-started/installation/)库
- 桥接服务器：**[https://github.com/AmandaClarke61/toybrige]**（请在克隆后替换为你的GitHub仓库）

---

## 设置（只需一次）

### 第1步 — 获取代码

```bash
git clone https://github.com/AmandaClarke61/toybrige venus-ble
cd venus-ble
uv sync
```

### 第2步 — 获取设备ID

这是最重要的步骤。每个Cachito控制器都有一个唯一的4位十六进制配对ID，你需要获取自己的设备ID。

1. 在iPhone上打开Cachito应用程序，并将其与Venus设备连接。
2. 在Mac电脑上运行以下命令：

```bash
uv run sniff_cachito.py
```

3. 在Cachito应用程序中，点击任意一个振动按钮。
4. 终端会输出类似以下的信息：

```
[SERVICE UUID CMD] 7100-01-cc-8200-cbc5-040a-640000...
  #### (device_id): cbc5  ← SAVE THIS!
```

5. 复制4位字符的`device_id`值（例如`cbc5`）。

### 第3步 — 设置设备ID

打开`ble_worker.py`文件，并修改第14行：

```python
DEVICE_ID = "cbc5"   # ← replace with your value from Step 2
```

### 第4步 — 授予蓝牙访问权限

macOS系统需要用户明确授予蓝牙访问权限。首次运行时系统会提示你，点击“允许”即可。

### 第5步 — 启动服务器

> 服务器仅绑定到`localhost`，不会发送任何外部网络请求。在运行之前，你可以查看`server.py`（[https://github.com/AmandaClarke61/toybrige/blob/main/server.py】）和`ble_worker.py`（[https://github.com/AmandaClarke61/toybrige/blob/main/ble_worker.py】）的完整源代码。

```bash
uv run server.py
```

请保持终端窗口打开状态。服务器运行在**端口8888**上。

---

## OpenClaw集成

如果OpenClaw是在**Docker**环境中运行的（标准配置），主机机器可以通过`host.docker.internal`访问。

如果OpenClaw是**原生运行**的（不在Docker中），则使用`localhost`。

---

## 代理程序使用的命令

### 以指定强度振动

```bash
curl -s -X POST http://host.docker.internal:8888/vibrate \
  -H "Content-Type: application/json" \
  -d '{"intensity": 60}'
```

`intensity`：0–100（0表示停止）

### 立即停止

```bash
curl -s -X POST http://host.docker.internal:8888/stop
```

### 检查状态

```bash
curl -s http://host.docker.internal:8888/status
```

---

## 强度等级说明

| 强度等级 | 感受效果             |
|--------|--------------------|
| 1–20   | 轻微振动             |
| 30–50  | 中等强度             |
| 60–80  | 强烈振动             |
| 90–100 | 最大强度             |

---

## 预设振动模式

| 模式        | 功能描述                          |
|---------|--------------------------------------------|
| `pulse`    | 80%的振动强度，持续5次                   |
| `wave`    | 强度从20%逐渐增加到100%，然后再降回20%     |
| `tease`    | 强度从30%逐渐增加到70%，再增加到100%，然后停止       |

示例：*“执行`wave`模式”* 或 *“进行30秒的`tease`模式”*

---

## 代理程序规则

- 定时振动结束后，设备会自动停止（强度为0），除非用户另有指令。
- **不要**使用`notify`工具，建议使用`bash`和`curl`进行通信。
- 如果OpenClaw不是在Docker中运行，请将`host.docker.internal`替换为`localhost`。

---

## 故障排除

| 问题             | 解决方法                         |
|-----------------|-----------------------------------------|
| “BT not ready”错误     | 确保蓝牙已开启，并在系统设置中的“隐私”选项中授予访问权限   |
| `curl`命令失败/连接被拒绝 | 确保`server.py`仍在运行                   |
| 设备无响应        | 重新检查`ble_worker.py`中的`DEVICE_ID`是否与Cachito控制器的ID一致 |
| 强度设置错误       | Venus设备接受的强度范围是0–100；超出此范围的值会被自动限制在有效范围内 |
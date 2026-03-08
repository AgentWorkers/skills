---
name: venus-ble-vibrator
description: >
  **通过自然语言控制Venus（Cachito）BLE振动器**  
  该功能通过macOS的CoreBluetooth协议，调用一个本地HTTP服务器，该服务器会向振动器发送BLE指令。使用前需进行硬件配置——请先查看ToyBridge仓库中的相关说明。
metadata: {"openclaw": {"os": ["darwin"]}}
---
# Venus BLE振动器控制

使用OpenClaw通过自然语言来控制**Venus / Cachito（小猫爪）BLE振动器**。

> 这是一项专为Cachito协议玩具设计的功能。如果您的设备受到[Buttplug.io](https://iostindex.com)的支持，请使用`intiface-control`功能——无需进行逆向工程。

> **仅限macOS系统。** 服务器使用CoreBluetooth技术。

---

## 设置

请按照[ToyBridge设置指南](https://github.com/AmandaClarke61/toybridge)操作：完成步骤1–3（发现设备ID、配置设备、在本地验证设备），然后启动服务器：

```bash
uv run 4-bridge/server.py
```

请保持终端窗口打开状态。服务器运行在**端口8888**上。

---

## 代理将使用的命令

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

### 检查设备状态

```bash
curl -s http://host.docker.internal:8888/status
```

> 如果OpenClaw是在本地系统上运行的（而非在Docker容器中），请将`host.docker.internal`替换为`localhost`。

---

## 强度说明

| 强度范围 | 振动感受 |
|--------|---------|
| 1–20   | 轻微振动 |
| 30–50  | 中等强度 |
| 60–80  | 强烈振动 |
| 90–100 | 最大强度 |

---

## 预设振动模式

| 模式        | 功能描述         |
|------------|-------------------|
| `pulse`     | 80%的振动强度，持续5次     |
| `wave`     | 强度从20%逐渐增加到100%，再逐渐降低，重复两次 |
| `tease`     | 强度从30%逐渐增加到70%，再增加到100%，然后停止 |

示例：*“执行`wave`模式”* 或 *“进行30秒的`tease`模式”*

---

## 代理运行规则

- 定时振动结束后，设备会自动停止（强度设为0），除非用户另有指令
- **禁止** 使用`notify`工具——请使用`bash`和`curl`来发送指令
- 如果OpenClaw不在Docker容器中运行，请将`host.docker.internal`替换为`localhost`

---

## 故障排除

| 问题 | 解决方法         |
|---------|-------------------|
| “蓝牙未准备好”错误 | 确保蓝牙功能已开启，并在系统设置中的“隐私”选项中授予应用程序访问权限 |
| 连接被拒绝 | 确保`uv run 4-bridge/server.py`脚本正在运行 |
| 设备无响应 | 检查`4-bridge/ble_worker.py`文件中的`DEVICE_ID`是否与您的Cachito控制器匹配 |
| 强度设置错误 | 强度值会被限制在0–100的范围内 |

---
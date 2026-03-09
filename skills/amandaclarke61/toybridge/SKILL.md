---
name: toybridge
description: 您可以控制任何已被逆向工程并通过 ToyBridge 服务器连接的 BLE (蓝牙低功耗) 玩具。该功能通过调用本地 HTTP API 来发送振动/停止命令。请确保 ToyBridge 服务器在同一台机器上运行。
metadata: {"openclaw": {"os": ["darwin"]}}
---
# ToyBridge — 通用BLE玩具控制工具

只要您运行了[ToyBridge](https://github.com/AmandaClarke61/toybridge)服务器，就可以通过OpenClaw控制**任何BLE玩具**。

该功能适用于**不被Buttplug.io/Intiface支持的设备**——即那些使用专有协议或未知协议的设备，您需要通过ToyBridge工具包自行对其进行逆向工程。

> 如果您的设备被Buttplug.io支持，请使用`intiface-control`功能，因为它更简单。

---

## 先决条件

1. 您已使用[ToyBridge](https://github.com/AmandaClarke61/toybridge)对设备的BLE协议进行了逆向工程。
2. 您已为该设备配置了`4-bridge/ble_worker.py`脚本。
3. ToyBridge服务器正在运行：`uv run 4-bridge/server.py`

请参阅[完整设置指南](https://github.com/AmandaClarke61/toybridge)以获取详细步骤。

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

> 如果OpenClaw是在本地环境中运行的（而非Docker中），请将`host.docker.internal`替换为`localhost`。

---

## 强度等级说明

| 强度范围 | 振动感受 |
|--------|---------|
| 1–20   | 微弱   |
| 30–50  | 中等   |
| 60–80  | 强烈   |
| 90–100 | 最大   |

---

## 预设振动模式

| 模式        | 功能                |
|-------------|-------------------|
| `pulse`     | 以80%的强度振动5次           |
| `wave`     | 强度从20%逐渐增加到100%，然后再降回20%     |
| `tease`     | 强度从30%逐渐增加到70%，再增加到100%，之后停止 |

要运行某个振动模式，请执行以下命令：

```bash
curl -s -X POST http://host.docker.internal:8888/vibrate \
  -H "Content-Type: application/json" \
  -d '{"pattern": "wave"}'
```

---

## 代理运行规则

- 定时操作结束后，代理会自动停止（振动强度为0），除非用户另有指令。
- **禁止**使用`notify`工具，建议使用`bash`和`curl`进行通信。
- 如果OpenClaw不在Docker中运行，请将`host.docker.internal`替换为`localhost`。

---

## 故障排除

| 问题         | 解决方法                |
|--------------|----------------------|
| 连接失败     | 确保`uv run 4-bridge/server.py`正在运行   |
| 设备无响应     | 检查`ble_worker.py`中的设备配置     |
| 强度设置错误     | 强度值会被限制在0–100的范围内     |
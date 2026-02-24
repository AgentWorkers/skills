---
name: icom-7610
description: 通过 USB 或 LAN 控制 Icom IC-7610 对讲机：可以设置/获取频率、工作模式、功率、信号强度（S-meter）以及驻波比（SWR）；支持连续波（CW）发射模式和信标模式；同时具备远程开关机功能。
metadata: {"openclaw":{"emoji":"📻","homepage":"https://clawhub.ai/morozsm/icom-7610","requires":{"bins":["rigctl","curl","python3"]},"install":[{"id":"hamlib","kind":"brew","formula":"hamlib","bins":["rigctl"],"label":"Install Hamlib (rigctl)"}]}}
---
# Icom IC-7610

## 先决条件

- **Hamlib**（用于控制无线电设备的库）：`brew install hamlib`
- **curl**：通常已预安装
- **python3**：通常已预安装
- **pyserial**（仅用于通过串行端口控制无线电设备的电源开关）：`pip3 install pyserial`
- **wfview**（可选，用于通过局域网控制无线电设备）：[wfview.org/download](https://wfview.org/download)

## 配置

电台的配置信息保存在 `.env` 文件中（不在 Git 仓库中）。首次安装时，请执行 `cp .env.example .env`。

### 环境变量

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `CALLSIGN` | *(发送信号时必需)* | 你的呼号 |
| `SERIAL_PORT` | `/dev/cu.usbserial-11320` | CI-V 无线电设备的串行端口 |
| `BAUD_RATE` | `19200` | 串行通信的波特率（注意：不是 115200！） |
| `HAMLIB_MODEL` | `3078` | Hamlib 为 IC-7610 设定的模型 ID |
| `FLRIG_URL` | `http://127.0.0.1:12345/RPC2` | flrig 的 XML-RPC 服务端地址 |
| `RIGCTLD_ADDR` | `127.0.0.1:4533` | rigctld 的 TCP 服务器地址（用于与 wfview 或 hamlib 通信） |
| `MAX_POWER_W` | `50` | 无线电设备的最大功率限制（单位：瓦特） |

```bash
source "$(dirname "$0")/.env" 2>/dev/null || true
PORT="${SERIAL_PORT:-/dev/cu.usbserial-11320}"
BAUD="${BAUD_RATE:-19200}"
MODEL="${HAMLIB_MODEL:-3078}"
FLRIG="${FLRIG_URL:-http://127.0.0.1:12345/RPC2}"
RIGCTLD="${RIGCTLD_ADDR:-127.0.0.1:4533}"
MAX_POWER="${MAX_POWER_W:-50}"
```

### RFPOWER 的表示方法

`rigctl` 使用 **0.0–1.0** 的范围来表示功率，其中 1.0 对应 100 瓦特。例如：`RFPOWER = 功率（瓦特）/ 100`。
- 5 瓦特对应 `0.05`，50 瓦特对应 `0.50`。⚠️ 注意：`RFPOWER 5` 实际表示 500 瓦特，而不是 5 瓦特！
`flrig` 直接使用瓦特作为单位，例如：`rig.set_power 50` 表示设置功率为 50 瓦特。

## 连接方式

共有三种连接方式，按优先级排序。系统会自动选择最适合的连接方式。

### 通过 wfview 连接（推荐）或独立的 hamlib 服务器

- **通过 wfview**：通过 UDP 协议或运行的 `rigctld` 服务器连接到 IC-7610 无线电设备。
- **功能**：可以完全控制无线电设备的频率、工作模式、功率、信号强度（S-meter）、驻波比（SWR）、连续波（CW）发射功能以及电源开关。

**设置步骤**：
1. 打开 wfview，进入 **Settings** → **Enable LAN**。
2. 输入无线电设备的 IP 地址，然后启用 **Enable RigCtld**（端口 4533）。

**注意**：执行 **M**（设置工作模式）命令时，系统可能会等待 wfview 或 rigctld 的响应，但命令仍会继续执行。如果需要，可以使用超时机制或一次性发送命令。

**相比串行连接的优点**：
- 不需要 USB 数据线，仅使用以太网连接。
- 可以通过简单的 `set_powerstat 1` 命令直接控制电源开关（无需使用 `ci-v` 或 `pyserial`）。
- 多个程序可以通过 wfview 共享同一台无线电设备。
- 连接距离更远（以太网可达 100 米，而 USB 仅限 5 米）。

### 通过 rigctl 连接（串行端口，支持全部控制功能）

**注意**：波特率必须设置为 **19200**（不是 115200！），并且需要使用超时机制来避免命令阻塞：`timeout 10 rigctl ...`。
**注意**：当 `flrig` 正在运行时，串行端口可能被占用，此时请关闭 `flrig` 以执行电源开关操作。

### 通过 flrig 的 XML-RPC 连接

### 远程控制电源开关

- **关闭电源**：通过菜单选项 **MENU → SET → Network → Power OFF** 设置为 **Standby/Shutdown**。

### 最简单的连接方式：通过 wfview 和 rigctld 连接

### 通过串行端口控制电源开关

- **关闭电源**：`rigctl -m $MODEL -r "$PORT" -s $BAUD set_powerstat 0`
- **开启电源**：直接使用 `rigctl set_powerstat 1` 无效（在设备处于待机状态时会失败）。此时需要使用 `ci-v` 命令。

**注意**：在开启电源后，请等待 **7–10 秒** 再发送命令。启动过程中出现 “Command rejected” 是正常现象。

## 连续波（CW）和信标信号（Beacon）的发送

这两种功能都可以通过 `rigctld`（局域网连接）或直接串行端口来控制。

### 无线电设备的频率和模式设置

- 进入菜单 **MENU → SET → Connectors → USB Keying (CW)**，然后选择 **RTS** 以设置连续波发射模式。

## 安全规则

### 每次发送前的必检项
1. 确保已获得操作员的确认。
2. 使用的频率必须在业余无线电频段内（1.8–2.0, 3.5–4.0, 7.0–7.3, 10.1–10.15, 14.0–14.35, 18.068–18.168, 21.0–21.45, 24.89–24.99, 28.0–29.7 MHz）。
3. 工作模式必须与所使用的频段相匹配。
4. 功率不得超过 `MAX_POWER_W`（默认为 50 瓦特）；超过限制需再次确认。
5. 如果可能，驻波比（SWR）应小于等于 3.0；否则请拒绝发送信号（可能是天线问题）。

### 无需确认的操作
- 读取频率、模式、信号强度、驻波比，切换频率或模式，以及开关电源。

### 必须确认的操作
- PTT 操作，连续波发射，发送信标信号，以及功率超过 `MAX_POWER_W` 的操作。
- 任何形式的射频传输。

### 即使获得确认也需要拒绝的操作
- 在业余频段之外发送信号。
- 当驻波比（SWR）超过 3.0 时禁止发送信号。

### 信标信号的相关法规（FCC 规定）
- 远程操作是合法的（§97.109d）。无人值守的信标信号仅允许在 28.2–28.3, 50.06–50.08+ MHz 频段发送。在 28 MHz 以下频段发送信标信号时，操作员必须保持通信状态。

## 参考资料

完整的文档请参阅 `references/FULL-REFERENCE.md`：
- 所有的 `flrig` XML-RPC 方法列表（30 多种方法）
- CI-V 协议参考（命令、模式、地址格式）
- 错误处理指南（常见错误及解决方法）
- 常用 Shell 功能（`freq_valid`, `set_power_safe`, `rig_retry`, `preflight`, `quick_status`）
- 无线电设备的菜单设置（网络、CI-V、接口连接）
- 其他 Icom 无线电设备的兼容性信息
- 美国业余无线电频段划分表（包含连续波/数据/电话信号使用的频段信息）
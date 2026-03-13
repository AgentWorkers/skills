---
name: emoPAD-universe
description: >
  **emoPAD Universe - 情绪识别技能**
  该技能帮助用户在“PAD”（愉悦-唤醒-支配）坐标系统中定位自己的情绪，并提供了“emoNebula”功能：实现实时情绪监测，每5分钟会弹出一个窗口显示情绪分布图。
  ## **跨平台支持**
  支持 Linux 和 Windows 操作系统：
  - **Linux**：使用 eog（GNOME 的图像查看器）来显示图像窗口。
  - **Windows**：使用系统默认的图像查看器来显示图像。
  ## **自动启动**
  安装该技能后，emoPAD 服务和 emoNebula 会自动启动，无需手动操作。
  ## **支持的硬件设备**
  - **脑电图（EEG）**：KSEEG102（支持蓝牙 BLE 连接）
  - **脉搏血氧饱和度传感器（PPG）**：Cheez PPG 传感器（支持串行通信）
  - **皮肤电反应（GSR）**：Sichiray GSR V2（支持串行通信）
  理论上，其他类似设备也应能够正常使用。未来版本将逐步支持更多主流品牌的产品，包括：
  - Muse 系列脑电图设备
  - Emotiv 脑电图设备
  - Oura Ring 智能手环
  - Whoop 智能手环
  - 其他主流的脑电图设备和可穿戴设备。
  ## **依赖项的安装**
  在安装该技能时，系统会自动检查并安装所需的依赖项，无需用户进行任何操作。
  ## **使用方法**
  - `openclaw emopad status`：获取当前的 PAD 状态
  - `openclaw emopad snapshot`：手动生成情绪分布图
  - `openclaw emopad stop`：停止服务
  - `openclaw emopad start`：重新启动服务
  ## **重要说明**
  **关于情绪 PAD 的计算方法**：目前该方法基于启发式算法，其映射关系是从大量文献中总结得出的。这种方法暂时无法完全反映个体的差异。未来版本将加入个性化校准训练模块，以实现更准确的情绪识别功能。
---
# emoPAD Universe

## 跨平台支持

emoPAD Universe 支持以下操作系统：

| 操作系统 | 图像浏览器 | 备注 |
|---------|-----------|------|
| Linux | eog（Eye of GNOME） | 支持窗口模式，可关闭 |
| Windows | 系统默认的图像浏览器 | 支持窗口模式，可关闭 |

## 自动启动

安装此技能后，将自动执行以下操作：
1. 检查并安装所需的 Python 依赖项。
2. 启动 emoPAD 服务（监听地址：http://127.0.0.1:8766）。
3. 启动 emoNebula 自动报告功能（每 5 分钟在弹出窗口中显示情绪星云图表）。

安装完成后无需手动启动，即可立即使用。

## 工具

### emopad_status

获取当前 emoPAD 的状态以及传感器连接状态

**描述**：返回三个维度的数值：愉悦感（Pleasure）、唤醒度（Arousal）、支配感（Dominance），以及 EEG、PPG、GSR 传感器的连接状态。

**参数**：无

**返回值**：格式化的情绪状态文本，包含传感器连接状态。

---

### emopad_snapshot

生成当前的情绪星云图表

**描述**：生成 3D 形式的情绪星云图表截图。

**参数**：无

**返回值**：
- 状态信息
- PNG 格式的图像数据

---

### emopad_start_nebula

启动 emoNebula 自动报告功能

**描述**：每 5 分钟在弹出窗口中自动生成并显示情绪星云图表。至少需要连接 2 个传感器才能显示图像，否则会显示“数据缺失”的提示。

**参数**：无

**返回值**：状态信息

---

### emopad_stop_nebula

停止 emoNebula 自动报告功能

**描述**：停止自动显示情绪星云图表。

**参数**：无

**返回值**：状态信息

## 配置

```yaml
serial_port: /dev/ttyACM0      # Serial device path (Linux)
# serial_port: COM3            # Serial device path (Windows)
baudrate: 115200               # Serial baudrate
eeg_window_sec: 2              # EEG data window (seconds)
ppg_gsr_window_sec: 60         # PPG/GSR data window (seconds)
hop_sec: 2                     # Calculation interval (seconds)
history_length: 120            # Number of historical data points
nebula_interval: 300           # Send interval (seconds)
service_host: 127.0.0.1        # Service listening address
service_port: 8766             # Service listening port
```

## 依赖项

- mne
- heartpy
- neurokit2
- bleak
- pyvista
- pyserial
- scipy
- numpy
- PyWavelets
- fastapi
- uvicorn
- pillow
- requests
- pyyaml

## 硬件支持

### 目前支持的设备

| 设备类型 | 设备型号 | 连接方式 |
|------|------|----------|
| EEG | KSEEG102 | 蓝牙 BLE 连接 |
| PPG | Cheez PPG 传感器 | 串行连接 |
| GSR | Sichiray GSR V2 | 串行连接 |

### 未来计划支持的设备

- Muse 系列 EEG 设备
- Emotiv EEG 设备
- Oura Ring 智能手环
- Whoop 智能手环
- 其他主流的 EEG 设备和可穿戴设备

## 关于情绪 PAD 的计算方法

**重要说明**：目前，情绪 PAD 的计算方法基于启发式算法，这些算法是根据大量文献总结出的关系映射得出的。

该方法的特点：
- ✅ 基于科学文献中的统计模式
- ✅ 适用于普通人群的情绪识别
- ⚠️ 目前无法反映个体差异

**未来改进**：将在新版本中引入个性化校准训练模块，通过用户特定的数据训练来实现真正的个性化情绪识别功能。
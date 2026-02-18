---
name: dht11-temp
description: 从 DHT11 传感器读取温度和湿度数据。支持通过 CLI 参数或环境变量指定自定义的 GPIO 引脚。
metadata: {"openclaw": {"emoji": "🌡️", "requires": {"bins": ["python3", "sudo", "RPi.GPIO"]}}}
---
# DHT11 温湿度传感器

从 DHT11 传感器读取温度和湿度数据。

## 硬件设置

**接线（根据需要调整引脚）：**
```
DHT11 Pinout:
─────────────
1. VCC     → 5V (Pin 2 oder 4)
2. DATA    → GPIO <PIN> + 10K Pull-Up Widerstand → 5V
3. GND     → GND (Pin 6)
```

**重要提示：** 必须在 DATA 引脚和 VCC（5V）之间连接一个 10K 的上拉电阻！

## 安装

```bash
# Install dependencies
pip3 install RPi.GPIO
```

## 使用方法

### 通过默认引脚（引脚 19）读取传感器数据
```bash
sudo python3 scripts/dht/main.py
```

### 通过自定义引脚读取传感器数据
```bash
sudo python3 scripts/dht/main.py 4     # Uses GPIO 4
```

### 使用环境变量
```bash
export DHT_PIN=4
sudo python3 scripts/dht/main.py
```

## 输出结果

- 第一行：温度（°C）
- 第二行：湿度（%）

## 自定义设置

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| DHT_PIN | 19 | GPIO 引脚编号 |

## crontab 示例条目
```bash
# Read every 30 minutes
*/30 * * * * sudo python3 ~/scripts/dht/main.py >> /var/log/dht.log 2>&1
```
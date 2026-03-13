---
name: raspberry-pi-manager
version: 1.0.0
description: 管理树莓派设备——包括GPIO控制、系统监控（CPU/温度/内存）、服务管理、传感器数据读取以及远程部署。
runtime: python3
---
# Raspberry Pi 管理工具

这是一个功能强大的 Raspberry Pi 管理工具，集成了多种管理功能。无论您是使用单个 Raspberry Pi 作为家庭服务器，还是管理大量的物联网节点，该工具都能让您快速获取系统状态、GPIO 引脚信息、服务状态、传感器数据以及部署工作流程。

## 工作原理

该脚本可以在 Raspberry Pi 上本地运行，也可以通过 SSH 远程执行。对于本地使用，只需直接运行脚本即可；如需远程管理，请先配置 SSH 访问权限。

### 本地使用

```bash
bash scripts/pi-manager.sh system
bash scripts/pi-manager.sh gpio read 17
```

### 远程使用

```bash
export PI_HOST="pi@192.168.1.200"
export PI_SSH_KEY="~/.ssh/id_rsa"

bash scripts/pi-manager.sh --remote system
bash scripts/pi-manager.sh --remote gpio read 17
```

**多台 Raspberry Pi 支持：**

```bash
export PI_HOSTS="pi@node1.local,pi@node2.local,pi@node3.local"
bash scripts/pi-manager.sh --fleet system
```

## 系统监控

实时了解 Raspberry Pi 的运行状况。

```bash
# Full system dashboard
$ bash scripts/pi-manager.sh system

┌─ Raspberry Pi 4 Model B (4GB) ─────────────────────┐
│                                                      │
│  CPU:    4× ARM Cortex-A72 @ 1.5GHz                │
│  Load:   0.42, 0.38, 0.31                          │
│  Temp:   48.3°C / 118.9°F  [████░░░░░░ OK]         │
│  Memory: 1.2GB / 3.7GB     [████████░░ 32%]        │
│  Disk:   12.4GB / 29.1GB   [█████████░ 43%]        │
│  Swap:   0MB / 100MB       [░░░░░░░░░░ 0%]         │
│  Uptime: 14 days, 7:23:41                           │
│  OS:     Raspberry Pi OS (Bookworm) 64-bit          │
│                                                      │
│  Network:                                            │
│    eth0:  192.168.1.200 (1000 Mbps)                 │
│    wlan0: 192.168.1.201 (72 Mbps, -42 dBm)         │
└──────────────────────────────────────────────────────┘
```

### 单项指标监控

```bash
# Temperature with threshold warning
bash scripts/pi-manager.sh temp
bash scripts/pi-manager.sh temp --warn 70 --crit 80

# CPU usage (snapshot or continuous)
bash scripts/pi-manager.sh cpu
bash scripts/pi-manager.sh cpu --watch 5   # Update every 5s

# Memory breakdown
bash scripts/pi-manager.sh memory

# Disk usage by mount point
bash scripts/pi-manager.sh disk

# Network interfaces and traffic
bash scripts/pi-manager.sh network

# Top processes by CPU/memory
bash scripts/pi-manager.sh top 10
```

### 历史数据记录

```bash
# Log system metrics to CSV (for graphing)
bash scripts/pi-manager.sh monitor --interval 60 --output metrics.csv

# View logged metrics
bash scripts/pi-manager.sh monitor --view metrics.csv --last 24h
```

## GPIO 控制

支持对 GPIO 引脚进行直接操作，适用于各种硬件项目。

```bash
# Pin layout reference
bash scripts/pi-manager.sh gpio pinout

# Read a pin state
bash scripts/pi-manager.sh gpio read 17

# Set pin output
bash scripts/pi-manager.sh gpio write 17 high
bash scripts/pi-manager.sh gpio write 17 low

# Set pin mode
bash scripts/pi-manager.sh gpio mode 17 output
bash scripts/pi-manager.sh gpio mode 18 input --pull up

# PWM output (hardware PWM on supported pins)
bash scripts/pi-manager.sh gpio pwm 18 75    # 75% duty cycle

# Watch pin for changes
bash scripts/pi-manager.sh gpio watch 17 --edge both

# Bulk operations
bash scripts/pi-manager.sh gpio write 17,18,27,22 high
bash scripts/pi-manager.sh gpio read 17,18,27,22

# GPIO status overview
bash scripts/pi-manager.sh gpio status
```

## 服务管理

可以控制 Raspberry Pi 上运行的 systemd 服务。

```bash
# List all services (active, failed, inactive)
bash scripts/pi-manager.sh service list
bash scripts/pi-manager.sh service list --failed

# Service operations
bash scripts/pi-manager.sh service status nginx
bash scripts/pi-manager.sh service start nginx
bash scripts/pi-manager.sh service stop nginx
bash scripts/pi-manager.sh service restart nginx
bash scripts/pi-manager.sh service enable nginx
bash scripts/pi-manager.sh service disable nginx

# View service logs
bash scripts/pi-manager.sh service logs nginx --lines 50
bash scripts/pi-manager.sh service logs nginx --follow

# Create a new service from a script
bash scripts/pi-manager.sh service create my-app /home/pi/app/start.sh \
  --description "My Application" \
  --restart always \
  --user pi
```

## 传感器数据读取

能够读取连接到 Raspberry Pi 的各种传感器数据。

```bash
# DHT11/DHT22 temperature & humidity
bash scripts/pi-manager.sh sensor dht22 4      # GPIO pin 4

# DS18B20 temperature sensor (1-Wire)
bash scripts/pi-manager.sh sensor ds18b20

# BMP280/BME280 (I2C)
bash scripts/pi-manager.sh sensor bme280

# HC-SR04 ultrasonic distance
bash scripts/pi-manager.sh sensor distance 23 24  # Trigger/Echo pins

# PIR motion sensor
bash scripts/pi-manager.sh sensor pir 17 --watch

# Light sensor (analog via MCP3008 ADC)
bash scripts/pi-manager.sh sensor light 0       # ADC channel 0

# Log sensor readings
bash scripts/pi-manager.sh sensor dht22 4 --log --interval 300 --output temp_log.csv
```

## 远程部署

可以将应用程序和配置文件部署到 Raspberry Pi 上。

```bash
# Copy files to Pi
bash scripts/pi-manager.sh deploy push ./app/ /home/pi/app/

# Pull files from Pi
bash scripts/pi-manager.sh deploy pull /home/pi/logs/ ./local-logs/

# Run a script on the Pi
bash scripts/pi-manager.sh deploy exec ./setup.sh

# Full deployment workflow
bash scripts/pi-manager.sh deploy run ./deploy.yml
```

### 部署配置文件 (`deploy.yml`):

```yaml
target: pi@192.168.1.200
steps:
  - copy: ./app/ → /home/pi/app/
  - run: cd /home/pi/app && pip3 install -r requirements.txt
  - run: sudo systemctl restart my-app
  - verify: curl -s http://localhost:8080/health
```

```bash
# Fleet deployment
bash scripts/pi-manager.sh --fleet deploy run ./deploy.yml
# Deploys to all configured Pi hosts sequentially
```

## 维护管理

提供便捷的维护工具。

```bash
# System update
bash scripts/pi-manager.sh update

# Firmware update check
bash scripts/pi-manager.sh firmware

# Reboot / shutdown
bash scripts/pi-manager.sh reboot
bash scripts/pi-manager.sh shutdown

# Backup SD card (creates compressed image)
bash scripts/pi-manager.sh backup /path/to/backup.img.gz

# Overclock profiles
bash scripts/pi-manager.sh overclock show
bash scripts/pi-manager.sh overclock mild    # 1.8GHz
bash scripts/pi-manager.sh overclock medium  # 2.0GHz
```

## 监控警报

支持基于阈值的警报设置：

```bash
# Alert if temperature exceeds 75°C
bash scripts/pi-manager.sh alert temp 75

# Alert if disk usage exceeds 90%
bash scripts/pi-manager.sh alert disk 90

# Alert if a service goes down
bash scripts/pi-manager.sh alert service nginx

# All alerts — suitable for cron
bash scripts/pi-manager.sh alert check
```

该工具既可以独立使用，也可以作为更复杂的物联网管理流程的一部分。建议与 `homeassistant-toolkit` 配合使用，以实现智能家居的全面集成。
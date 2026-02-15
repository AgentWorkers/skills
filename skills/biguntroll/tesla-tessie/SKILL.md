---
name: tesla
description: 通过 Tessie API 控制和监控特斯拉车辆。当您需要查看特斯拉车辆的状态（电池电量、位置、充电情况）、调节车内温度（加热/制冷）、锁定/解锁车门、启动/停止充电、按喇叭/闪烁车灯、打开充电接口或后备箱，或执行其他特斯拉车辆相关操作时，可以使用该 API。使用该 API 需要设置 `TESSIE_API_KEY` 环境变量。
---

# 通过Tessie控制特斯拉车辆

使用Tessie API通过Python脚本来控制特斯拉车辆。

## 前提条件

**安装Python 3并确保已安装requests库：**
```bash
pip install requests
```

**设置`TESSIE_API_KEY`环境变量**，该密钥可从https://my.tessie.com/settings/api获取。

```bash
# Linux/macOS
export TESSIE_API_KEY="your-api-key-here"

# Windows (PowerShell)
$env:TESSIE_API_KEY = "your-api-key-here"

# Windows (cmd)
set TESSIE_API_KEY=your-api-key-here
```

为了实现数据的持久存储，可以将相关配置添加到您的shell配置文件（.bashrc、.zshrc、PowerShell配置文件等）中。

## 常用命令

所有命令都依赖于`scripts/tessie.py`脚本。大多数命令都需要提供车辆的VIN（车辆识别号）。

### 获取车辆列表

```bash
python scripts/tessie.py vehicles
```

返回与您的Tessie账户关联的所有车辆及其VIN。

### 检查车辆状态

```bash
python scripts/tessie.py status --vin <VIN>
```

返回车辆的详细状态信息，包括电池电量、位置、气候设置、充电状态等。

### 电池信息

```bash
python scripts/tessie.py battery --vin <VIN>
```

返回电池电量、续航里程和充电相关信息。

### 获取车辆位置

```bash
python scripts/tessie.py location --vin <VIN>
```

返回车辆的当前位置（纬度、经度、行驶方向）。

### 锁车/解锁车辆

```bash
python scripts/tessie.py lock --vin <VIN>
python scripts/tessie.py unlock --vin <VIN>
```

### 调节气候设置

```bash
# Start climate
python scripts/tessie.py start_climate --vin <VIN>

# Stop climate
python scripts/tessie.py stop_climate --vin <VIN>

# Set temperature (Celsius)
python scripts/tessie.py set_temperature --vin <VIN> --value 22
```

### 充电操作

```bash
# Start charging
python scripts/tessie.py start_charging --vin <VIN>

# Stop charging
python scripts/tessie.py stop_charging --vin <VIN>

# Set charge limit (0-100)
python scripts/tessie.py set_charge_limit --vin <VIN> --value 80

# Open/close charge port
python scripts/tessie.py open_charge_port --vin <VIN>
python scripts/tessie.py close_charge_port --vin <VIN>
```

### 发出喇叭声、闪烁车灯或模拟“放屁”效果

```bash
python scripts/tessie.py honk --vin <VIN>
python scripts/tessie.py flash --vin <VIN>
python scripts/tessie.py fart --vin <VIN>
```

注意：模拟“放屁”功能需要车辆运行在固件版本2022.40.25或更高版本上。

### 打开后备箱

```bash
python scripts/tessie.py open_frunk --vin <VIN>
python scripts/tessie.py open_trunk --vin <VIN>
```

### 软件更新

```bash
# Schedule update immediately
python scripts/tessie.py schedule_update --vin <VIN>

# Schedule update in 2 hours (7200 seconds)
python scripts/tessie.py schedule_update --vin <VIN> --value 7200

# Cancel scheduled update
python scripts/tessie.py cancel_update --vin <VIN>

# Check for available updates
python scripts/check-updates.py --vin <VIN>
```

`check-updates`命令会返回以下状态之一：
- `UPDATE_AVAILABLE：软件更新X.X.X已准备好安装！`
- `UPDATE_DOWNLOADING：正在下载更新X.X.X（已完成XX%）`
- `UPDATE_INSTALLING：正在安装更新X.X.X（已完成XX%）`
- `UPDATE_SCHEDULED：更新X.X.X已安排在将来执行`
- `NO_UPDATE：没有可用的更新`

### 唤醒车辆

如果车辆处于休眠状态，请先使用`wake`命令唤醒车辆，然后再执行其他操作。

## 自动更新通知

要接收软件更新通知，请设置一个cron作业：

```bash
# Check for updates every 6 hours and notify if available
cron add \
  --schedule "0 */6 * * *" \
  --text "Check my Tesla for software updates and notify me if one is available" \
  --description "Tesla software update check"
```

当有更新可用时，系统会发送包含版本号的通知。

## 工作流程

1. 首次使用：使用`vehicles`命令获取车辆的VIN。
2. 对于大多数命令：使用VIN来指定目标车辆。
3. 如果车辆处于休眠状态：先使用`wake`命令唤醒车辆，然后再执行相应命令。
4. 根据需要使用`status`、`battery`或`location`命令检查车辆状态。

## 参考资料

有关完整的API文档，请参阅`references/api.md`。
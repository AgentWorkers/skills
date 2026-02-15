# Tessie 技能

通过 Tessie API 控制您的特斯拉车辆——这是一个拥有超过 50 万用户的特斯拉管理平台。

## 设置

获取您的 Tessie API 凭据：
1. 访问 https://tessie.com/developers
2. 注册并创建一个 API 密钥
3. 在 Clawdbot 中进行配置：

```yaml
skills:
  entries:
    tessie:
      apiKey: "your-tessie-api-key-here"
```

或者通过环境变量设置：
```bash
export TESSIE_API_KEY="your-tessie-api-key-here"
```

**注意**：车辆 ID 和 VIN 会通过 API 自动检测，无需手动配置。

## 功能

### 车辆状态
- **电池电量**：当前的充电百分比
- **续航里程**：预估的行驶里程
- **位置**：当前车辆坐标
- **车辆状态**：锁定/解锁、充电状态、睡眠模式
- **连接状态**：车辆是否在线/离线？

### 气候控制
- **开启/关闭**：控制车内空调
- **预热/预冷**：设置车厢温度（自动检测华氏度/摄氏度）
- **除霜**：除霜车窗/后视镜

### 充电
- **开始/停止**：远程控制充电
- **充电限制**：设置每日/标准充电限制
- **充电状态**：当前充电速率、完成时间、电池电量

### 行车记录
- **最近行驶记录**：最近的路程、耗能情况、行驶位置

## 使用示例

```
# Check battery and range
"tessie battery"
"tessie how much charge"
"tessie range"

# Preheat the car (assumes Fahrenheit if > 50)
"tessie preheat 72"
"tessie precool"
"tessie turn on climate"

# Check drives
"tessie show my drives"
"tessie recent drives"
"tessie drives 5"

# Charging commands
"tessie start charging"
"tessie stop charging"
"tessie set charge limit to 90%"
"tessie charging status"

# Vehicle location
"tessie where is my car"
"tessie location"

# Vehicle state
"tessie is the car locked?"
"tessie vehicle status"
```

## Tessie API 端点

### 认证
所有请求都需要：
```
Authorization: Bearer <api-key>
```

### 获取车辆信息
```
GET https://api.tessie.com/vehicles
```
返回包含 `last_state` 的完整车辆列表

### 获取行驶记录
```
GET https://api.tessie.com/{VIN}/drives?limit=10
```
返回最近的行驶历史记录

### 获取停车信息
```
GET https://api.tessie.com/{VIN}/idles?limit=10
```
返回包含空调/防盗系统使用情况的停车记录

### 命令
所有控制命令均使用 VIN（而非 vehicle_id）：
```
POST https://api.tessie.com/{VIN}/command/{command}
```

**可用命令**：
- `start_climate`（开启空调）
- `stop_climate`（关闭空调）
- `set_temperatures`（设置温度）
- `start_charging`（开始充电）
- `stop_charging`（停止充电）
- `set_charge_limit`（设置充电限制）
- `lock`（锁定车辆）
- `unlock`（解锁车辆）
- `enable_sentry`（启用防盗系统）
- `disable_sentry`（关闭防盗系统）
- `activate_front_trunk`（启用前备箱）
- `activate_rear_trunk`（启用后备箱）
- `open_windows`（打开车窗）
- `close_windows`（关闭车窗）
- `vent_windows`（通风车窗）

完整命令列表：请访问 https://developer.tessie.com

## 注意事项

- Tessie 作为您与特斯拉 API 之间的中间件
- 提供比原始特斯拉 API 更丰富的数据和分析功能
- 需要先将特斯拉账户关联到 Tessie
- 所有命令均使用 VIN 进行识别（VIN 会自动检测）
- 所有温度数据以摄氏度显示
- **尚未正式部署**——正在等待用户审核后发布
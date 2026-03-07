---
name: nws-warning-bot
description: >
  使用基于多边形的检测方法，监控国家气象局（NWS）针对特定地址发布的严重天气警报。
  与县级警报不同，这种方法会检查警报所涉及的多边形（如龙卷风或强雷暴的多边形）是否确实与您的住宅坐标相交，而不仅仅是您所在的县的范围。这种方法有助于过滤掉那些影响您所在县其他区域的警报，同时确保您能够及时了解到风暴是否真的正在朝您的方向移动。
  当用户需要针对特定位置的严重天气警报时，或者希望从全县范围内的警报中筛选出仅与自己地址相关的信息时，可以使用这种方法；此外，它也非常适用于构建针对个人住宅的紧急通知系统。
homepage: https://github.com/openclaw/nws-warning-bot
metadata:
  clawdbot:
    emoji: "🌪️"
    requires:
      env: ["WARNING_BOT_LAT", "WARNING_BOT_LON", "WARNING_BOT_ADDRESS"]
      primaryEnv: "WARNING_BOT_LAT"
    files: ["scripts/*"]
---
# NWS 警报机器人

该工具可针对您的实际地址，进行多边形级别的恶劣天气监测。

## 功能介绍

传统的天气警报通常是以县为单位发布的。例如，如果您所在的县面积为500平方英里，那么发生在您所在县以北40英里的龙卷风警报，也会被视为您所在地区的警报。而这个工具能够解决这一问题。

**核心功能：**  
- 检查 NWS 发布的警报信息是否确实覆盖了您的地理位置（精确到经纬度）。  
- 仅当警报区域与您的实际位置完全重叠时，才会触发警报通知（而不仅仅是您的邮政编码或所在县的范围）。

## 快速入门

### 1. 获取您的坐标  
- **方法一：** 使用 Google 地图：右键点击您的住址，选择“这里有什么？”，然后复制坐标值（以小数形式）。  
- **方法二：** 通过 GPS 设备或手机应用程序获取坐标。  
- **方法三：** 使用地址地理编码服务：`curl "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress?address=YOUR%20ADDRESS&format=json"`  

### 2. 设置环境变量  
（具体环境变量设置请参考 ````bash
export WARNING_BOT_LAT=YOUR_LAT      # Your latitude
export WARNING_BOT_LON=YOUR_LON      # Your longitude  
export WARNING_BOT_ADDRESS="Your Address, City, State"
export WARNING_BOT_STATE="OH"        # Your state code
````）

### 3. 手动检查  
（手动检查的代码示例请参考 ````bash
python3 scripts/warning-bot.py
````）  
- 如果检查结果为 0，表示您的地址没有收到任何警报。  
- 如果检查结果为 1，表示检测到警报，并会将警报信息保存到 `data/alert-pending.txt` 文件中。  

### 4. 通过 Cron 任务自动化检查  
（自动化检查的代码示例请参考 ````bash
*/5 * * * * /path/to/warning-bot/scripts/warning-bot-cron.sh
````）  
完成设置后，您需要将 `data/alert-pending.txt` 文件连接到您的通知系统（如 Telegram、电子邮件等）。

## 工作原理  

- **核心脚本 `warning-bot.py`**：负责从 NWS 获取警报信息，判断警报区域是否包含您的位置，并去除重复的警报。  
- **`warning-bot-cron.sh`**：用于定时执行检查任务，并处理警报信息的输出。  
- **SQLite 数据库**：用于记录已发送的警报信息（警报信息有效期为24小时）。  
- **`data/alert-pending.txt`：** 存储需要通知的警报信息。  

**多边形检测机制：**  
使用射线投射算法判断您的经纬度是否位于 NWS 发布的警报区域内（支持 `Polygon` 和 `MultiPolygon` 几何形状）。  

**重复检测机制：**  
通过 SQLite 数据库记录警报 ID，避免对同一警报进行多次通知。  

**监测的警报类型：**  
默认监测以下类型的警报：龙卷风警报、强雷暴警报、龙卷风预警以及强雷暴预警。  

## 配置参数  

| 参数名 | 是否必填 | 默认值 | 说明 |
|---------|---------|---------|-------------|
| `WARNING_BOT_LAT` | ✅ | — | 您的纬度（小数形式） |
| `WARNING_BOT_LON` | ✅ | — | 您的经度（小数形式） |
| `WARNING_BOT_ADDRESS` | ❌ | “Unknown” | 用于生成通知消息的地址格式 |
| `WARNING_BOT_STATE` | ❌ | “OH” | NWS 发布警报的州代码 |

## 输出文件  

- `data/warning-bot.db`：用于存储去重后的警报信息。  
- `data/warning-bot.log`：记录 Cron 任务的执行日志。  
- `data/alert-pending.txt`：当检测到警报时，其中会保存警报信息。  

## 测试方法  
（请参考 ````python
# Test if bot detects warnings for your location
python3 -c "
import os
os.environ['WARNING_BOT_LAT'] = 'YOUR_LAT'
os.environ['WARNING_BOT_LON'] = 'YOUR_LON'
os.environ['WARNING_BOT_ADDRESS'] = 'Test Location'

from scripts.warning_bot import point_in_polygon

# Mock warning polygon (approximate bounding box around test area)
test = [[-83.0, 40.5], [-82.0, 40.5], [-82.0, 41.5], [-83.0, 41.5], [-83.0, 40.5]]
print('Inside:', point_in_polygon(YOUR_LAT, YOUR_LON, test))
"
```` 以验证您的坐标是否正确。）  

## 系统要求：**  
- Python 3.7 及以上版本。  
- 需要安装 `sqlite3` 库以及 `urllib`、`json`、`datetime` 库。  
- 无需任何外部依赖库。  

## API 使用说明：**  
该工具通过调用 `api.weather.gov/alerts/active?area={STATE}` 来获取警报信息：  
  - 请求超时时间为 10 秒。  
  - 数据格式为 GeoJSON。  
  - 请求头中需包含标准的 User-Agent 字段（在生产环境中请使用您的电子邮件地址）。  

**使用注意事项：**  
- 请尊重 NWS 的使用规定，避免频繁请求（建议每 5 分钟以上才进行一次请求）。  
- 尽管 NWS 的请求限制较为宽松，但请遵守规定，以免影响服务。  

## 集成示例：**  
- **通过 Telegram 发送警报通知：** （代码示例请参考 ````bash
if [ -f data/alert-pending.txt ]; then
  cat data/alert-pending.txt | telegram-send --stdin
  rm data/alert-pending.txt
fi
````）  
- **通过电子邮件发送警报通知：** （代码示例请参考 ````bash
if [ -s data/alert-pending.txt ]; then
  mail -s "Severe Weather Alert" user@example.com < data/alert-pending.txt
fi
````）  

**限制条件：**  
- **仅支持美国境内：** 该工具仅适用于美国境内的警报信息。  
- **依赖多边形数据：** 如果 NWS 发布的警报没有提供详细的多边形信息（通常县级别的警报不包含这些信息），则该工具会忽略这些警报。  
- **仅监测当前有效的警报：** 该工具仅显示正在生效的警报，不预测未来的天气风险。  
- **基于单个位置点：** 该工具仅根据您的经纬度进行判断，不考虑您的实际位置范围（如房屋大小）。  

**安全提示：**  
- 该工具仅作为官方信息的补充工具使用，不能替代官方的天气预报或警报系统。  
- 请同时收听 NOAA 的天气广播作为备用信息。  
- 不要完全关闭县级别的警报通知。  
- 在恶劣天气季节前请先测试系统是否正常运行。  
- 在实际发生恶劣天气时，请直接关注 NWS 的官方信息。  

**开发说明：**  
该工具基于 NWS 的 API (`api.weather.gov`) 和 GeoJSON 数据开发。其中使用的射线投射算法是计算几何学中的标准方法。
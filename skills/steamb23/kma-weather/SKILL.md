---
name: kma-weather
description: 从韩国气象厅（기상청）获取天气信息。提供当前天气状况、短期预报（最长3天）、中期预报（3-10天）以及天气预警。需要使用KMA API服务密钥。
homepage: https://www.data.go.kr/data/15084084/openapi.do
metadata: {"openclaw":{"emoji":"🌦️","requires":{"bins":["python3"],"env":["KMA_SERVICE_KEY"]}}}
---

# kma-weather

从**韩国气象厅（KMA）**获取官方天气信息。

## 功能

- **当前天气** - 实时观测数据（温度、湿度、降水量、风速）
- **短期预报** - 超短期（6小时）和短期（3天）预报
- **中期预报** - 3-10天天气趋势
- **天气警报** - 官方发布的警报（台风、暴雨、降雪等）
- **高分辨率** - 5公里×5公里的网格系统，提供精确的本地天气预报

## 快速入门

```bash
# Get current weather + 6-hour forecast (brief)
python3 skills/kma-weather/scripts/forecast.py brief --lat 37.5665 --lon 126.9780

# Get all forecasts as JSON (current + ultrashort + shortterm)
python3 skills/kma-weather/scripts/forecast.py all --lat 37.5665 --lon 126.9780 --json

# Get all short-term forecast data (3 days)
python3 skills/kma-weather/scripts/forecast.py shortterm --lat 37.5665 --lon 126.9780 --days all

# Get current nationwide weather warnings status
python3 skills/kma-weather/scripts/weather_warnings.py

# Get mid-term forecast for Seoul
python3 skills/kma-weather/scripts/midterm.py --region 서울
```

## 设置

### 1. 获取API密钥

1. 访问 [公共数据门户](https://www.data.go.kr)
2. 注册/登录
3. 申请访问以下3个API（所有API使用相同的密钥）：
   - [韩国气象厅短期预报查询服务](https://www.data.go.kr/data/15084084/openapi.do) (15084084)
   - [韩国气象厅特殊天气警报查询服务](https://www.data.go.kr/data/15000415/openapi.do) (15000415)
   - [韩国气象厅中期预报查询服务](https://www.data.go.kr/data/15059468/openapi.do) (15059468)
4. 等待审批（通常立即或1天内完成）
5. 进入“我的页面” → “API密钥管理”
6. 复制你的 `ServiceKey`

**注意**：所有3个API都使用 **相同的API密钥**。

### 2. 设置环境变量

将你的API密钥添加到环境中：

**对于Sandbox（Docker/Podman）：**
```yaml
# In agents.yaml
agents:
  defaults:
    sandbox:
      docker:
        env:
          KMA_SERVICE_KEY: "your-service-key-here"
```

**对于主机：**
```yaml
# In agents.yaml
agents:
  defaults:
    env:
      vars:
        KMA_SERVICE_KEY: "your-service-key-here"
```

或者直接导出：
```bash
export KMA_SERVICE_KEY="your-service-key-here"
```

## 使用方法

### 当前天气

获取实时天气观测数据：

```bash
python3 skills/kma-weather/scripts/forecast.py current \
  --lat 37.5665 --lon 126.9780
```

**输出结果：**
```
🌤️ 현재 날씨 (초단기실황)
🌡️  기온: 5.2°C
💧 습도: 65%
🌧️  강수량: 0mm (1시간)
💨 풍속: 2.3m/s
🧭 풍향: NW (315°)
```

### 短期预报

**超短期预报（6小时）：**
```bash
python3 skills/kma-weather/scripts/forecast.py ultrashort \
  --lat 37.5665 --lon 126.9780
```

**短期预报（3天）：**
```bash
# 내일 예보 (기본값)
python3 skills/kma-weather/scripts/forecast.py shortterm \
  --lat 37.5665 --lon 126.9780

# 모레 예보
python3 skills/kma-weather/scripts/forecast.py shortterm \
  --lat 37.5665 --lon 126.9780 --days 2

# 글피 예보
python3 skills/kma-weather/scripts/forecast.py shortterm \
  --lat 37.5665 --lon 126.9780 --days 3

# 모든 예보 데이터 (3일치 전체)
python3 skills/kma-weather/scripts/forecast.py shortterm \
  --lat 37.5665 --lon 126.9780 --days all
```

**`--days` 参数说明：`all` = 全部数据，`1` = 明天（默认），`2` = 后天，`3` = 下周三**

### 综合预报

**简版（当前天气 + 6小时预报）** - 适合快速查看天气：
```bash
python3 skills/kma-weather/scripts/forecast.py brief \
  --lat 37.5665 --lon 126.9780
```

**完整版（当前天气 + 超短期预报 + 短期预报）**：包含所有详细数据：
```bash
python3 skills/kma-weather/scripts/forecast.py all \
  --lat 37.5665 --lon 126.9780
```

在输出JSON时，确保数据按类型分类：
```bash
python3 skills/kma-weather/scripts/forecast.py brief --lat 37.5665 --lon 126.9780 --json
# {"current": {...}, "ultrashort": {...}}

python3 skills/kma-weather/scripts/forecast.py all --lat 37.5665 --lon 126.9780 --json
# {"current": {...}, "ultrashort": {...}, "shortterm": {...}}
```

### 天气警报

查询全国范围内的天气警报状态：

```bash
# Get current nationwide warning status
python3 skills/kma-weather/scripts/weather_warnings.py
```

**输出结果：**
```
🚨 기상특보 현황
발표시각: 2026-02-01 10:00
발효시각: 2026-02-01 10:00

📍 현재 발효 중인 특보
  • 건조경보 : 강원도, 경상북도, ...
  • 풍랑주의보 : 동해중부안쪽먼바다, ...

⚠️  예비특보
  • (1) 강풍 예비특보 : 02월 02일 새벽(00시~06시) : 울릉도.독도
```

### 中期预报

按地区获取3-10天的天气预报：

```bash
# By region name
python3 skills/kma-weather/scripts/midterm.py --region 서울

# By station code
python3 skills/kma-weather/scripts/midterm.py --stn-id 109
```

**支持的地区**：首尔、仁川、京畿、釜山、大邱、光州、大田、蔚山、世宗、江原、忠北、忠南、全北、全南、庆北、庆南、济州

### 原始JSON输出

所有脚本都支持使用 `--json` 参数来获取原始API响应：

```bash
python3 skills/kma-weather/scripts/forecast.py current \
  --lat 37.5665 --lon 126.9780 --json
```

## 网格坐标

KMA使用基于Lambert Conformal Conic投影的 **5公里×5公里网格系统**。

将经纬度转换为网格坐标：

```bash
python3 skills/kma-weather/scripts/grid_converter.py 37.5665 126.9780
```

**输出结果：**
```
Input: (37.5665, 126.9780)
Grid:  (60, 127)
Verify: (37.5665, 126.9780)
```

脚本会自动处理网格转换，因此你可以直接使用经纬度坐标。

## 在Python代码中使用

直接导入并使用相关函数：

```python
from skills.kma_weather.scripts.forecast import fetch_forecast, format_current
from skills.kma_weather.scripts.grid_converter import latlon_to_grid

# Get current weather
data = fetch_forecast("current", lat=37.5665, lon=126.9780)
print(format_current(data))

# Convert coordinates
nx, ny = latlon_to_grid(37.5665, 126.9780)
print(f"Grid: ({nx}, {ny})")
```

## API详情

有关API的详细文档，请参阅：
- [references/api-forecast.md] - 短期预报API
- [references/api-warnings.md] - 天气警报API
- [references/api-midterm.md] - 中期预报API
- [references/category-codes.md] - 类别代码参考

## 工作流程示例

请参阅 [examples/daily-check.md] 以了解完整的每日天气检查工作流程。

## 注意事项

- **API更新时间表**：
  - 当前天气/超短期预报：每小时10分更新
  - 短期预报：02:10、05:10、08:10、11:10、14:10、17:10、20:10、23:10（KST）
  - 中期预报：06:00、18:00（KST）
- **网格分辨率**：5公里×5公里（高于全球其他服务）
- **覆盖范围**：仅限韩国
- **API使用限制**：请在 [公共数据门户](https://www.data.go.kr) 查看你的使用计划限制
- **自动分页**：当数据量超过单页限制（每页300条）时，脚本会自动获取所有数据

## 对比：weather vs kma-weather

| 功能 | weather (全球) | kma-weather (KMA) |
|---------|------------------|-------------------|
| 数据来源 | wttr.in, Open-Meteo | 韩国气象厅 |
| 覆盖范围 | 全球 | 仅限韩国 |
| API密钥 | 不需要 | **需要** |
| 分辨率 | 城市级别 | 5公里×5公里网格 |
| 官方警报 | 无 | **有**（台风、暴雨、降雪等） |
| 适用场景 | 快速查询全球天气 | 详细的韩国天气预报和警报 |

**建议**：结合使用这两个工具：
- 使用 `weather` 获取全球天气信息
- 使用 `kma-weather` 获取详细的韩国天气预报和警报

## 故障排除

### “KMA API服务密钥未找到”
请设置 `KMA_SERVICE_KEY` 环境变量。详见 [设置](#setup)。

### “API错误 30: SERVICE_KEY_IS_NOT REGISTERED_ERROR”
你的API密钥无效或尚未获得批准。请检查：
1. 是否申请了所有3个KMA API的访问权限？
2. 你的请求是否已获批准？
3. 密钥是否复制正确（没有多余的空格）？

### “API错误 22: SERVICE_TIMEOUT_ERROR**
KMA API服务器可能出现延迟。稍后再试。

### 未返回数据
- 确认坐标是否位于韩国境内。
- 使用 `grid_converter.py` 验证网格坐标是否正确。
- 尝试增加 `--rows` 参数（默认值：300）。如果参数过大，可能会收到“429：请求过多”的错误。

## 许可证

本工具使用了韩国气象厅通过 [公共数据门户](https://www.data.go.kr) 提供的公共API。

---

## 实现状态

本工具实现了最常用的API接口。根据需求，未来版本可能会添加更多接口。

更多详细信息，请参阅 [implement-status.md]。
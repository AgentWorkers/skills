---
name: kma-weather
description: 从韩国气象厅（기상청）获取天气信息。该服务提供当前天气状况、3至10天的天气预报以及天气警报/预警（기상특보）。当用户需要韩国的天气数据、天气警报或精确的本地天气预报（5公里网格分辨率）时，可以使用该服务。使用该服务需要KMA_SERVICE_KEY。
metadata:
  openclaw:
    emoji: "🌦️"
    homepage: "https://www.data.go.kr/data/15084084/openapi.do"
    requires:
      bins: ["python3"]
      env: ["KMA_SERVICE_KEY"]
    primaryEnv: "KMA_SERVICE_KEY"
---
# kma-weather

## 快速入门

```bash
# Current weather + 6-hour forecast
python3 skills/kma-weather/scripts/forecast.py brief --lat 37.5665 --lon 126.9780

# All forecasts as JSON (current + ultrashort + shortterm)
python3 skills/kma-weather/scripts/forecast.py all --lat 37.5665 --lon 126.9780 --json

# Short-term forecast (3 days)
python3 skills/kma-weather/scripts/forecast.py shortterm --lat 37.5665 --lon 126.9780 --days all

# Nationwide weather warnings/advisories (기상특보)
python3 skills/kma-weather/scripts/weather_warnings.py

# Mid-term forecast (3-10 days)
python3 skills/kma-weather/scripts/midterm.py --region 서울
```

## 设置

### 1. 获取 API 密钥

1. 访问 [公共数据门户](https://www.data.go.kr)
2. 申请访问以下 3 个 API（所有 API 需使用相同的密钥）：
   - [气象厅短期预报查询服务](https://www.data.go.kr/data/15084084/openapi.do) (15084084)
   - [气象厅特殊天气警报查询服务](https://www.data.go.kr/data/15000415/openapi.do) (15000415)
   - [气象厅中期预报查询服务](https://www.data.go.kr/data/15059468/openapi.do) (15059468)
3. 从“我的页面”→“API 密钥管理”中复制您的 `ServiceKey`。

### 2. 设置环境变量

在 `~/.openclaw/openclaw.json` 文件中：

**Sandbox**（添加到 `agentsdefaults.sandbox.docker.env`）：
```json
{
  "agents": {
    "defaults": {
      "sandbox": {
        "docker": {
          "env": {
            "KMA_SERVICE_KEY": "your-key"
          }
        }
      }
    }
  }
}
```

**Host**（添加到 `env_vars`）：
```json
{
  "env": {
    "vars": {
      "KMA_SERVICE_KEY": "your-key"
    }
  }
}
```

## 使用方法

### forecast.py

| 命令 | 描述 |
|---------|-------------|
| `current` | 实时观测数据 |
| `ultrashort` | 6 小时预报 |
| `shortterm` | 3 天预报 |
| `brief` | 实时观测数据 + 6 小时预报 |
| `all` | 实时观测数据 + 6 小时预报 + 3 天预报 |

**选项**：
- `--lat`, `--lon`：坐标（必填）
- `--days`：对于短期预报，可选值为 `1`（明天，默认）、`2`、`3` 或 `all`
- `--json`：输出原始 JSON 格式

**输出示例**（`current` 命令）：
```
🌤️ 현재 날씨 (초단기실황)
🌡️  기온: 5.2°C
💧 습도: 65%
🌧️  강수량: 0mm (1시간)
💨 풍속: 2.3m/s
🧭 풍향: NW (315°)
```

### weatherWarnings.py

返回全国范围内的当前特殊天气警报信息：
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

### midterm.py

按地区提供 3-10 天的预报。

```bash
python3 skills/kma-weather/scripts/midterm.py --region 서울
python3 skills/kma-weather/scripts/midterm.py --stn-id 109
```

**地区**：首尔、仁川、京畿、釜山、大邱、光州、大田、蔚山、世宗、江原、忠北、忠南、全北、全南、庆北、庆南、济州

### grid_converter.py

将经纬度坐标转换为 KMA 5 公里网格（由其他脚本自动处理）：
```bash
python3 skills/kma-weather/scripts/grid_converter.py 37.5665 126.9780
# Output: Grid: (60, 127)
```

## API 说明

- **发布时间表**：
  - 短期预报：每小时 40 分（基础时间：HH00）
  - 超短期预报：每小时 45 分（基础时间：HH30）
  - 中期预报：02:10、05:10、08:10、11:10、14:10、17:10、20:10、23:10（KST）
  - 中期预报：06:00、18:00（KST）
- **覆盖范围**：仅限韩国境内
- **自动分页**：脚本会自动获取所有数据页

## 与 weather 技能的对比

| | weather | kma-weather |
|-|---------|-------------|
| 覆盖范围 | 全球 | 仅限韩国 |
| API 密钥 | 不需要 | **需要** |
| 分辨率 | 城市级别 | 5 公里网格 |
| 天气警报 | 不提供 | **提供**（特殊天气警报）

**建议同时使用**：使用 `weather` 获取全球天气信息，使用 `kma-weather` 获取详细的韩国天气预报及特殊天气警报。

## 故障排除

| 错误 | 解决方案 |
|-------|----------|
| “KMA API 服务密钥未找到” | 设置 `KMA_SERVICE_KEY` 环境变量 |
| “SERVICE_KEY_IS_NOT REGISTERED_ERROR” | 检查 API 的审批状态并验证密钥 |
| “SERVICE_TIMEOUT_ERROR” | 稍后重试 |
| 未返回数据 | 确保坐标位于韩国境内 |

## 参考资料（原始 API 文档）

- [references/api-forecast.md](references/api-forecast.md) - 短期预报 API 的端点、参数和响应格式
- [references/api-warnings.md](references/api-warnings.md) - 特殊天气警报 API 的端点、参数和响应格式
- [references/api-midterm.md](references/api-midterm.md) - 中期预报 API 的端点、参数和响应格式
- [references/category-codes.md](references/category-codes.md) - KMA 分类代码（SKY、PTY 等）
- [implement-status.md](implement-status.md) - 实施状态
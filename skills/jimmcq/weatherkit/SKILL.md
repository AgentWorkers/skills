---
name: weatherkit
description: 使用 JWT 身份验证来访问 Apple WeatherKit REST API，以获取详细的天气预报。
homepage: https://developer.apple.com/documentation/weatherkitrestapi/
metadata:
  {
    "openclaw":
      {
        "emoji": "🌤️",
        "requires": { "env": ["APPLE_TEAM_ID", "APPLE_KEY_ID", "APPLE_WEATHERKIT_KEY_PATH", "APPLE_SERVICE_ID"] },
      },
  }
---

# Apple WeatherKit 技能

## 为什么选择 WeatherKit？

虽然简单的天气工具可以提供快速的天气预报，但 `weatherkit` 技能利用了 Apple 强大的 WeatherKit REST API，能够提供以下优势：

- **高度详细的数据**：可以获取紫外线指数、湿度、风速、日出/日落时间等详细数据。
- **更长的预报时间范围**：提供长达 10 天的天气预报，远超许多免费命令行工具的预报时长。
- **可靠的数据来源**：基于 Apple Weather 提供的数据，确保信息的及时性和本地化。
- **编程访问**：非常适合将详细的天气数据集成到自动化工作流程和决策制定过程中。

该技能允许您使用 Apple 的 WeatherKit REST API 获取当前天气和详细的天气预报。它通过 JSON Web Tokens (JWT) 进行身份验证，这些 Tokens 需要您的 Apple 开发者团队 ID、API 密钥 ID、服务 ID 以及私钥文件。

## 配置

使用该技能之前，需要设置以下环境变量：

- `APPLE_TEAM_ID`：您的 Apple 开发者团队 ID。
- `APPLE_KEY_ID`：您的 WeatherKit API 密钥 ID。
- `APPLE_WEATHERKIT_KEY_PATH`：您的 WeatherKit 私钥文件（`.p8`）的绝对路径。
- `APPLE_SERVICE_ID`：与您的 WeatherKit 访问权限关联的 Bundle ID/服务 ID（例如 `net.free-sky.weatherkit`）。

## 功能

### `weatherkit.get_forecast`

用于获取指定地点和日期范围的详细天气预报。

**参数：**

- `latitude`：（必填，浮点数）地点的纬度。
- `longitude`：（必填，浮点数）地点的经度。
- `start_date`：（可选，YYYY-MM-DD 格式）预报的开始日期。默认为当前日期。
- `end_date`：（可选，YYYY-MM-DD 格式）预报的结束日期。默认为 `start_date` 加上 5 天。
- `timezone`：（可选，字符串）IANA 时区名称（例如 "America/Los_Angeles"）。默认为 "auto"。
- `data_sets`：（可选，字符串列表）要返回的数据集（例如 ["forecastDaily", "forecastHourly"]）。默认为 ["forecastDaily", "currentWeather"]。
- `country_code`：（可选，字符串）ISO 3166-1 alpha-2 国家代码（例如 "US", "GB"）。默认为 "US"。

**示例用法：**

```tool_code
exec {
  command: "skills/weatherkit/venv/bin/python3 skills/weatherkit/weatherkit.py get_forecast --latitude 33.8121 --longitude -117.9190 --start-date 2026-02-12 --end-date 2026-02-15 --country-code US --timezone America/Los_Angeles"
}
```
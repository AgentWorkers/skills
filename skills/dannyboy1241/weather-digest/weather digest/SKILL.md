# Weather Digest 技能

使用 NOAA/NWS 数据生成每日天气情报摘要。

## 设置

1. **依赖项：** `python3`、`pip`。
2. 可选但推荐：`python3 -m venv skills/weather-digest/.venv && source skills/weather-digest/.venv/bin/activate`。
3. `pip install -r skills/weather-digest/requirements.txt`。
4. 将 `skills/weather-digest/config.example.json` 复制到 `config.json`，并根据需要使用 `name`、`lat`、`lon` 对来自定义 `locations` 列表。

## 使用方法

```
/exec python3 skills/weather-digest/weather_digest.py --config skills/weather-digest/config.json --output /tmp/digest.md
```

输出结果为 Markdown 格式；可根据需要将其转换为 PDF 或电子邮件。

## 配置说明

- 数据来源：`api.weather.gov`（无需 API 密钥；可以自由修改脚本中的 User-Agent 字符串）。
- 每个位置都会获取天气预报和警报信息；可根据需要添加或删除字段。
- 通过编辑 `weather_digest.py` 文件中的 `build_digest` 函数来扩展模板。
---
name: yr-weather
description: 使用 yr.no API 从挪威气象研究所（MET）获取天气预报。当用户请求特定地点的天气信息、预报、温度、降水量、风况或其他与天气相关的信息时，可以使用此功能。该服务支持基于坐标的位置查询，返回当前天气状况及未来天气预报。必须提供纬度和经度参数（无默认值），具体地点信息请参见“常见地点”表格。
---
# Yr.no Weather

通过 yr.no API 获取挪威气象局的天气预报（免费，无需密钥）。

## 快速入门

```bash
# Current weather + forecast (requires lat/lon)
python3 {baseDir}/scripts/weather.py &lt;lat&gt; &lt;lon&gt; [altitude]

# Examples from common locations:
python3 {baseDir}/scripts/weather.py -33.9288 18.4174   # Cape Town
python3 {baseDir}/scripts/weather.py -33.8688 151.2093  # Sydney
python3 {baseDir}/scripts/weather.py 51.5074 -0.1278    # London

# Tomorrow&#x27;s summary (requires lat/lon)
python3 {baseDir}/scripts/tomorrow.py &lt;lat&gt; &lt;lon&gt;

# Run tests
python3 -m unittest discover {baseDir}/tests
```

## 测试

- 单元测试模拟 API 调用（不使用网络连接）。
- 示例数据位于 `scripts/tests/data/` 目录中。
- 运行命令：`cd {baseDir}/scripts && python3 ../tests/test_*.py`

## 常见地点

| 城市          | 纬度       | 经度       |
|---------------|-----------|-----------|
| 开普敦     | -33.9288 | 18.4174  |
| 约翰内斯堡  | -26.2041 | 28.0473  |
| 德班        | -29.8587 | 31.0218  |
| 悉尼        | -33.8688 | 151.2093 |
| 伦敦        | 51.5074  | -0.1278  |
| 纽约      | 40.7128  | -74.0060 |
| 东京         | 35.6762  | 139.6503 |

## 项目结构

```
scripts/
├── yr_service.py    # API calls (tested/mocked)
├── utils.py         # Emoji/symbol helpers
├── weather.py       # Current + forecast CLI
├── tomorrow.py      # Tomorrow summary CLI
└── tests/data/      # Sample JSON
tests/
├── test_weather.py
└── test_service.py
```

## 独立仓库

通过 pip 安装：`pip install git+https://github.com/brandoncrabpi/yr-weather.git`
- 使用方式：`yr-weather -33.9288 18.4174`
- 版本标签：v1.0.0

## 使用说明

- 必须设置 User-Agent（已包含在代码中）。
- 每个地点的天气数据会缓存 10 分钟以上。
- 数据来源：挪威气象局（MET Norway）。

该项目已针对生产环境进行了重构：无默认设置、包含测试代码、采用模块化设计。
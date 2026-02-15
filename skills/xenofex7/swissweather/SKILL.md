---
name: swissweather
description: 从 MeteoSwiss（瑞士官方气象服务）获取当前天气和预报信息。该服务适用于查询瑞士的天气数据、瑞士气象站的本地测量结果或针对瑞士地区的特定预报。MeteoSwiss 提供来自 100 多个瑞士气象站的实时测量数据（温度、湿度、风速、降水量、气压），以及按邮政编码划分的多日天气预报。对于瑞士地区的用户来说，该服务比通用天气服务更为准确。
---

# SwissWeather

从瑞士联邦气象与气候局（MeteoSwiss）获取当前的天气数据和预报。

## 为什么使用这个工具

- **官方数据**：直接来自瑞士政府气象服务
- **实时测量数据**：瑞士境内有100多个自动气象站提供数据
- **无需API密钥**：提供免费的公开数据
- **针对瑞士优化**：相比通用服务，对瑞士地区的覆盖范围和准确性更高
- **数据全面**：包括温度、湿度、风速、降水量、气压、日照时间和太阳辐射等参数

## 快速入门

### 按气象站获取当前天气

从特定的瑞士气象站获取实时天气数据：

**选项1：Shell脚本（无需依赖库）**
```bash
scripts/current_weather_curl.sh --station RAG
```

**选项2：Python脚本（需要安装`pip3 install requests`）**
```bash
scripts/current_weather.py --station RAG
```

示例输出：
```
Station: RAG
Time: 2026-01-15 11:40 UTC
Temperature (°C)........................ 8.6
Rel. humidity (%)...................... 56.3
Wind speed (km/h)...................... 6.8
Precipitation (mm)..................... 0.0
```

常用气象站：
- **RAG** - 拉珀斯维尔（苏黎世地区）
- **BER** - 伯尔尼
- **ZRH** - 苏黎世机场
- **BAS** - 巴塞尔
- **GVE** - 日内瓦
- **LUG** - 卢加诺

### 列出所有气象站

```bash
scripts/current_weather_curl.sh --list
# or
scripts/current_weather.py --list
```

返回瑞士境内100多个气象站的代码及其最后更新时间。

### 按邮政编码获取天气预报

获取多日天气预报：
```bash
scripts/forecast.py 8640            # Rapperswil-Jona
scripts/forecast.py 8001 --days 7   # Zurich, 7-day forecast
```

**注意**：天气预报API偶尔可能会出现不稳定情况。如果API请求失败，系统会自动切换到当前天气数据。

## 可用的数据

### 当前天气数据

数据每10分钟更新一次，来自自动气象站：

- **温度**（°C）：2米高度处的空气温度
- **湿度**（%）：相对湿度
- **风速**（km/h）：风速（公里/小时）
- **风向**（°）：风向（度）
- **降水量**（mm）：最近降水量
- **气压**（hPa）：气象站所在地气压及海平面气压
- **日照时间**（分钟）：日照时长
- **太阳辐射**（W/m²）：全球太阳辐射强度
- **露点**（°C）：露点温度

### 天气预报

按瑞士邮政编码提供多日天气预报：

- **每日温度范围（最低/最高）**
- **天气状况（配有图标）**
- **降水量及概率**
- **每小时天气预报（如可用）**

## 选择气象站

选择离您位置最近的气象站：

- **主要城市**：BER（伯尔尼）、ZRH（苏黎世）、BAS（巴塞尔）、GVE（日内瓦）、LUG（卢加诺）
- **苏黎世地区**：KLO（克洛滕）、RAG（拉珀斯维尔）、TAE（坦尼肯）
- **中部地区**：LUZ（卢塞恩）、ALT（阿尔特多夫）、ENG（恩格尔贝格）
- **山区**：SMA（森蒂斯山）、JUN（荣夫劳伊霍赫山）、PIL（皮拉图斯山）

**提示**：如果位于山谷地区，请避免选择高山气象站，因为海拔差异可能影响天气数据。

有关完整的气象站列表和详细信息，请参阅`references/api_info.md`。

## JSON格式输出

所有脚本都支持`--json`参数，便于程序化使用：
```bash
scripts/current_weather.py --station RAG --json
scripts/forecast.py 8640 --json
```

## 高级用法

### 显示多个气象站的当前数据

```bash
scripts/current_weather.py --all
```

### 查找最近的气象站

1. 列出所有气象站：`scripts/current_weather.py --list`
2. 根据名称或位置查找最近的气象站
3. 使用该气象站的代码进行后续操作

### 数据缓存

数据每10分钟更新一次。请适当缓存响应结果：
```bash
# Cache current weather for 5-10 minutes
# Cache forecasts for 1-2 hours
```

## API参考

请参阅`references/api_info.md`，以获取以下信息：
- 完整的API文档
- 所有可用的数据字段
- 天气图标代码
- 警报等级和类型
- 替代数据来源
- 技术细节

## 依赖库

```bash
pip3 install requests
```

## 数据来源

- **提供者**：MeteoSwiss（瑞士联邦气象与气候局）
- **权威性**：瑞士官方气象服务
- **更新频率**：当前天气数据每10分钟更新一次
- **覆盖范围**：瑞士境内100多个自动气象站
- **URL**：https://data.geo.admin.ch / https://www.meteoschweiz.admin.ch

## 故障排除

**预报API失败**：MeteoSwiss的API偶尔会发生变化。如果`forecast.py`脚本无法正常运行，请使用当前天气数据，或查看`references/api_info.md`以获取替代方案。

**找不到气象站**：使用`--list`命令查看可用的气象站列表。气象站的代码为3个字母的缩写（不区分大小写）。

**数据缺失**：部分气象站可能无法测量所有参数。输出中会出现`-`或`N/A`表示相应数据缺失。

## 相关资源

- **swiss-transport**：瑞士公共交通时刻表和路线信息
- **weather**：通用天气服务（wttr.in）——在瑞士地区推荐使用SwissWeather工具。
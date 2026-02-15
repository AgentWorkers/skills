---
name: dhmz-weather
description: 从 DHMZ (meteo.hr) 获取克罗地亚的天气数据、预报和警报——无需 API 密钥。
homepage: https://meteo.hr/proizvodi.php?section=podaci&param=xml_korisnici
metadata: { "openclaw": { "emoji": "🇭🇷", "requires": { "bins": ["curl"] } } }
---

# DHMZ天气（克罗地亚）

克罗地亚气象和水文服务局（DHMZ）提供免费的XML API接口。所有数据均以克罗地亚语提供，无需认证。

## 默认行为

当调用此技能时：
1. **如果提供了城市名称作为参数**（例如：`/dhmz-weather Zagreb`）：立即获取并显示该城市的天气信息。
2. **如果没有提供城市名称**：会根据对话上下文（用户的位置、之前提到的城市或项目相关信息）推断出城市名称。如果无法确定城市名称，则默认使用**萨格勒布**（克罗地亚首都）。

**无需询问用户的具体需求**——直接获取天气数据并以易于阅读的格式展示给用户。

## 天气表情符号

在显示天气信息时使用以下表情符号，以增强直观性：

### 天气状况
| 克罗地亚语 | 英文 | 表情符号 |
|----------|---------|-------|
| vedro, sunčano | 晴朗 | ☀️ |
| delimično oblačno | 部分多云 | ⛅ |
| pretežno oblačno | 大部分多云 | 🌥️ |
| potpuno oblačno | 阴天 | ☁️ |
| slaba kiša | 小雨 | 🌦️ |
| kiša | 下雨 | 🌧️ |
| jaka kiša | 大雨 | 🌧️🌧️ |
| grmljavina | 雷暴 | ⛈️ |
| snijeg | 下雪 | 🌨️ |
| susnježica | 雨夹雪 | 🌨️🌧️ |
| magla | 雾 | 🌫️ |
| rosa | 露水 | 💧 |

### 天气指标
| 指标 | 表情符号 |
|--------|-------|
| 温度 | 🌡️ |
| 湿度 | 💧 |
| 气压 | 📊 |
| 风速 | 💨 |
| 降雨量 | 🌧️ |
| 紫外线指数 | ☀️ |
| 海水温度 | 🌊 |

### 风力强度
| 描述 | 表情符号 |
|-------------|-------|
| 微风 | 🍃 |
| 中等风速 | 💨 |
| 强风 | 💨💨 |
| 暴风雨 | 🌬️ |

### 天气警报
| 警报等级 | 表情符号 |
|-------|-------|
| 绿色（无警报） | 🟢 |
| 黄色 | 🟡 |
| 橙色 | 🟠 |
| 红色 | 🔴 |

## 当前天气

所有克罗地亚气象站的天气信息（按字母顺序排列）：

```bash
curl -s "https://vrijeme.hr/hrvatska_n.xml"
```

按地区划分的天气信息：

```bash
curl -s "https://vrijeme.hr/hrvatska1_n.xml"
```

欧洲城市的天气信息：

```bash
curl -s "https://vrijeme.hr/europa_n.xml"
```

## 温度极端值

最高温度：

```bash
curl -s "https://vrijeme.hr/tx.xml"
```

最低温度：

```bash
curl -s "https://vrijeme.hr/tn.xml"
```

地面最低温度（5厘米处）：

```bash
curl -s "https://vrijeme.hr/t5.xml"
```

## 海洋与水域

亚得里亚海海水温度：

```bash
curl -s "https://vrijeme.hr/more_n.xml"
```

河流温度：

```bash
curl -s "https://vrijeme.hr/temp_vode.xml"
```

## 降雨与降雪

降雨数据：

```bash
curl -s "https://vrijeme.hr/oborina.xml"
```

积雪深度：

```bash
curl -s "https://vrijeme.hr/snijeg_n.xml"
```

## 天气预报

今日预报：

```bash
curl -s "https://prognoza.hr/prognoza_danas.xml"
```

明日预报：

```bash
curl -s "https://prognoza.hr/prognoza_sutra.xml"
```

未来三天天气预报：

```bash
curl -s "https://prognoza.hr/prognoza_izgledi.xml"
```

地区性天气预报：

```bash
curl -s "https://prognoza.hr/regije_danas.xml"
```

未来三天详细天气图：

```bash
curl -s "https://prognoza.hr/tri/3d_graf_i_simboli.xml"
```

未来七天天气图：

```bash
curl -s "https://prognoza.hr/sedam/hrvatska/7d_meteogrami.xml"
```

## 天气警报（CAP格式）

今日的天气警报：

```bash
curl -s "https://meteo.hr/upozorenja/cap_hr_today.xml"
```

明天的天气警报：

```bash
curl -s "https://meteo.hr/upozorenja/cap_hr_tomorrow.xml"
```

后天的天气警报：

```bash
curl -s "https://meteo.hr/upozorenja/cap_hr_day_after_tomorrow.xml"
```

## 专项数据

- 紫外线指数：```bash
curl -s "https://vrijeme.hr/uvi.xml"
```
- 森林火灾风险指数：```bash
curl -s "https://vrijeme.hr/indeks.xml"
```
- 生物气象预报（健康提示）：```bash
curl -s "https://prognoza.hr/bio_novo.xml"
```
- 热浪警报：```bash
curl -s "https://prognoza.hr/toplinskival_5.xml"
```
- 寒潮警报：```bash
curl -s "https://prognoza.hr/hladnival.xml"
```

## 海洋/亚得里亚海相关

航海天气预报：

```bash
curl -s "https://prognoza.hr/jadran_h.xml"
```

船员专用海洋天气预报：

```bash
curl -s "https://prognoza.hr/pomorci.xml"
```

## 农业相关

农业天气预报：

```bash
curl -s "https://klima.hr/agro_bilten.xml"
```

土壤温度：

```bash
curl -s "https://vrijeme.hr/agro_temp.xml"
```

未来七天的农业数据：

```bash
curl -s "https://klima.hr/agro7.xml"
```

## 水文信息

水文状况报告：

```bash
curl -s "https://hidro.hr/hidro_bilten.xml"
```

## 使用提示
- 所有返回的数据均为XML格式。
- 数据以克罗地亚语提供。
- 气象站名称使用克罗地亚语字符（UTF-8编码）。
- 数据更新频率：实时数据约每小时更新一次，天气预报每天更新一次。
- 用于解析数据的工具包括`xmllint`或`xq`（需从`yq`包中安装）。

**使用`xmllint`提取特定气象站的数据：**```bash
curl -s "https://vrijeme.hr/hrvatska_n.xml" | xmllint --xpath "//Grad[GradIme='Zagreb']" -
```

**将数据转换为JSON格式（需使用`xq`工具）：**```bash
curl -s "https://vrijeme.hr/hrvatska_n.xml" | xq .
```

## 常见气象站名称
- 萨格勒布（Zagreb）
- 斯普利特（Split）
- 里耶卡（Rijeka）
- 奥西耶克（Osijek）
- 扎达尔（Zadar）
- 普拉（Pula）
- 杜布罗夫尼克（Dubrovnik）
- 斯拉沃恩斯基布罗德（Slavonski Brod）
- 卡尔洛瓦茨（Karlovac）
- 瓦拉兹丁（Varazdin）
- 西萨克（Sisak）
- 比耶洛瓦尔（Bjelovar）
- 卡科韦茨（Cakovec）
- 戈斯皮奇（Gospic）
- 克尼恩（Knin）
- 马卡尔斯卡（Makarska）
- 西贝尼克（Sibenik）

## 数据来源

克罗地亚气象和水文服务局（DHMZ）官方网站：<https://meteo.hr>
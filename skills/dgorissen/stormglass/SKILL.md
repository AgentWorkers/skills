---
name: stormglass-surf-skill
description: 通过海浪名称或坐标，从 Stormglass 系统中获取与冲浪相关的海洋状况数据，包括实时海况信息以及未来 1-3 天内的潮汐、阵风和水温预报。该功能适用于用户查询特定海滩或冲浪点的冲浪报告、波浪/涌浪情况、潮汐时间、风向、阵风强度或水温时使用。
version: 1.0.2
metadata:
  openclaw:
    requires:
      env:
        - STORMGLASS_API_KEY
      bins:
        - python3
    primaryEnv: STORMGLASS_API_KEY
    homepage: https://github.com/dgorissen/stormglass-skill
---
# Stormglass Surf Skill

## 目的

该技能用于为基于定时任务（cron）运行的代理管道生成可机器读取的海浪状况数据。它通过 Google 地理编码（或直接使用坐标）来获取特定海浪地点的信息，然后查询 Stormglass 数据库，并返回一个结构稳定的 JSON 数据格式，以便后续处理或展示。

## 输入参数

必须提供以下一种位置信息：

- `--location "海浪地点名称"`（可选的国家和地区名称，以字符串形式提供）；或
- `--lat <浮点数> --lon <浮点数>`（直接提供经纬度坐标）

可选参数：

- `--horizon now|24h|48h|72h`（默认值为 `72h`）：指定数据预测的时间范围
- `--output json|pretty`（默认值为 `json`；推荐用于自动化场景）
- `--source <逗号分隔的提供者列表>`：指定数据来源（例如多个 API 服务）
- `--mock`（离线模拟数据；适用于测试环境）

## 必需的环境变量

- `STORMGLASS_API_KEY`：用于访问 Stormglass 数据库的 API 密钥
- `GOOGLE_GEOCODING_API_KEY`（可选）：用于通过 Google 地理编码服务获取位置信息；如果未提供，则脚本会回退到使用 OpenStreetMap 的 Nominatim 服务

在 `--mock` 模式下，无需使用 API 密钥。

### 凭证信息要求

| 模式          | `STORMGLASS_API_KEY` | `GOOGLE_GEOCODING_API_KEY` |
|---------------|-----------------|-------------------|
| `--mock`         | 不需要               | 不需要               |
| 实时模式（`--lat/--lon`）    | 需要                 | 不需要               |
| 实时模式（`--location` 与 Google 结合） | 需要                 | 可选（建议使用）           |
| 实时模式（`--location` 与 OSM 结合） | 需要                 | 不需要               |

主要使用的凭证是 `STORMGLASS_API_KEY`。

## 执行命令

- 用于定时任务的 JSON 输出格式：```bash
python scripts/surf_report.py --location "Highcliffe Beach" --horizon 72h --output json
```
- 直接使用经纬度坐标时的输出格式：```bash
python scripts/surf_report.py --lat 50.735 --lon -1.705 --horizon 24h --output json
```
- 离线测试模式的执行命令：```bash
python scripts/surf_report.py --location "Highcliffe Beach" --horizon now --mock --output json
```

## 输出数据结构（JSON 格式）

输出数据的主要键值对如下：

- `meta`：请求元数据、时间戳、输入模式及可选的警告信息
- `location`：解析后的地点详细信息及坐标
- `now`：当前时刻的海浪相关指标
- `forecast`：未来一段时间内的海浪状况预测（包括最佳观测窗口）
- `tides`：潮汐极端值及当前潮汐趋势

**预期可获取的指标数据（如未提供则返回 `null`）：**
- `waveHeightM`（波浪高度，单位：米）
- `swellHeightM`（涌浪高度，单位：米）
- `swellPeriodS`（涌浪周期，单位：秒）
- `swellDirectionDeg`（涌浪方向，单位：度）
- `windSpeedMps`（风速，单位：米/秒）
- `windDirectionDeg`（风向，单位：度）
- `windGustMps`（阵风风速，单位：米/秒）
- `waterTemperatureC`（水温，单位：摄氏度）

## 错误代码

- `0`：操作成功
- `2`：CLI 使用或参数错误
- `3`：缺少 API 密钥或配置信息
- `4`：外部 API（如地理编码或 Stormglass）请求失败
- `5`：数据解析或格式化失败

## 代理系统处理规则

- 推荐使用 `--output json` 作为输出格式，以便下游代理系统更好地处理数据。
- 如果某个指标数据为 `null`，应视为“数据来源未提供”，而非数值为 0。
- 详细信息请参考 `reference.md` 文件。
- 可以参考 `examples.md` 文件中的示例和命令格式。
- 在正式部署定时任务之前，建议先运行 `scripts/testsurf_report.py` 脚本进行测试。
- 可选：在数据展示前，可以使用 `scripts/normalizesurf_data.py` 脚本对数据进行格式化处理，以确保数据符合预设规范。
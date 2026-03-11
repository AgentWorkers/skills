---
name: clawlendar
version: 0.3.1
description: 专为AI代理设计的、基于时间戳的永久性日历互操作功能。当代理需要执行日历转换（包括公历/儒略历/ISO标准/ROC历法/佛教历法/日本历法/六十甲子历法/太阳历等）时，该功能可发挥重要作用。它还能根据时间戳对时间线进行标准化处理，确保月份划分的准确性，并支持包含Bazi（八字）、黄历、西方历法等信息的日级数据传输。
author: Huang Geyang
metadata:
  openclaw:
    homepage: https://github.com/Hosuke/Clawlender
    requires:
      bins:
        - python3
        - pip
---
# Clawlendar

## 概述

Clawlendar 提供了一个统一的、易于代理使用的中间层，使得不同的工具能够使用统一的格式查询日历信息，并接收标准化的 JSON 数据。该功能被视为多代理生态系统中的日期互操作性基础。

## 工作流程

1. 首先调用 `capabilities` 函数，以获取支持的日历类型、可选的日历提供者以及区域设置（locale）支持。
2. 在进行日历转换时，需要解析源数据中的日历格式，并将其转换为公历（Gregorian）格式。
3. 对于基于时间戳的工作流程，应使用 `timeline` 函数（优先使用时间戳）而不是直接进行日期转换。
4. 当用户界面需要非公历系统中的准确月份边界信息时，应使用 `calendar_month` 函数。
5. `day_profile` 函数用于获取详细的日期信息（包括六十干支、二十四节气、农历日期等，可选还包括占星学数据）。
6. 在需要显示面向用户的文本时，务必传递正确的区域设置（如 `en`、`zh-CN`、`zh-TW`）。

## 快速入门（MCP 服务器）

将 Clawlendar 安装并作为 MCP 服务器运行，以支持 Claude Desktop 或 Claude Code 的功能：

```bash
python3 -m pip install -U "clawlendar[all]"
clawlendar
```

在 Claude Code 中进行一键注册的示例代码：

```bash
python3 -m pip install -U "clawlendar[all]" && claude mcp add clawlendar -- clawlendar
```

或者直接从源代码中运行 Clawlendar：

```bash
pip install -e .
python -m clawlendar.server
```

## 命令行接口（CLI）用法

- 列出所有支持的日历类型及可选的后端服务：
  ```bash
pip install -e .
python3 scripts/calendar_bridge.py capabilities
```

- 将一个日期转换为多个目标格式：
  ```bash
python3 scripts/calendar_bridge.py convert \
  --source gregorian \
  --targets julian,iso_week,minguo,buddhist,japanese_era,sexagenary,solar_term_24 \
  --date-json '{"year": 2026, "month": 3, "day": 9}'
```

- 使用基于时间戳的模型对日期进行标准化处理：
  ```bash
python3 scripts/calendar_bridge.py timeline \
  --input-json '{"timestamp": 1773014400}' \
  --timezone 'Asia/Taipei' \
  --date-basis local \
  --targets minguo,japanese_era,sexagenary,solar_term_24
```

- 生成用于生肖轮盘渲染的占星学数据：
  ```bash
python3 scripts/calendar_bridge.py astro \
  --input-json '{"timestamp": 1773014400}' \
  --timezone 'Asia/Taipei'
```

- 获取非公历系统中的准确月份边界信息：
  ```bash
python3 scripts/calendar_bridge.py calendar-month \
  --source minguo \
  --month-json '{"year":115,"month":3}'
```

- 获取统一的每日信息数据：
  ```bash
python3 scripts/calendar_bridge.py day-profile \
  --input-json '{"timestamp": 1773014400}' \
  --timezone 'Asia/Taipei' \
  --locale 'zh-TW'
```

- 包含完整的占星学数据（包括八字/黄历及西方历法信息）：
  ```bash
python3 scripts/calendar_bridge.py day-profile \
  --input-json '{"timestamp": 1773014400}' \
  --timezone 'Asia/Taipei' \
  --locale 'zh-CN'
```

## HTTP API

- 提供 HTTP API，以实现多代理系统之间的集成：
  ```bash
pip install -e ".[api]"
./scripts/run_api.sh
```

- 使用 Docker 运行 Clawlendar：
  ```bash
docker build -t clawlendar:mvp .
docker run --rm -p 8000:8000 clawlendar:mvp
```

## 合同规范

- 请参考 `references/integration-contract.md` 中的 JSON 合同规范，以确保工具间的顺利集成。请确保数据字段具有明确的含义，避免歧义。

## 工具映射

- MCP 工具：`capabilities`、`convert`、`timeline`、`astro_snapshot`、`calendar_month`、`day_profile`
- CLI 命令：`capabilities`、`convert`、`timeline`、`astro`、`calendar-month`、`day-profile`
- FastAPI 端点：`GET /capabilities`、`POST /convert`、`POST /timeline`、`POST /astro`、`POST /calendar-month`、`POST /day-profile`

## 参考资料

- 请查阅 `references/integration-contract.md` 以了解请求/响应的数据结构及兼容性要求。
- 了解主要的东方/西方日历系统及其推广优先级，请参考 `references/calender-landscape.md`。
- 有关基于时间戳的设计规则及日期转换方法，请参阅 `references/time-wheel-model.md`。
- GitHub 发布草案的详细信息请参考 `references/mvp-release-notes.md`。

## 注意事项

- 公历（Gregorian）被视为标准的日历格式。
- 对于未安装的可选日历提供者，系统会返回警告信息，而不会直接失败。
- 对于近似值（如六十干支年份的划分或固定日期的二十四节气计算），请明确标注其近似性。
- `timeline` 是多代理系统进行调度和事件处理的默认中间层。
- 当 `lunar_python` 可用时，农历月份的中文文本标签会通过 `day_profile.metaphysics.eastern.lunar_date` 展示。
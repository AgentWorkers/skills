---
name: railil
description: 使用 `railil` CLI 搜索以色列铁路的列车时刻表。支持通过模糊搜索找到车站之间的路线，可根据日期/时间进行筛选，并以多种格式（JSON、Markdown、表格）输出结果。
homepage: https://github.com/lirantal/railil
metadata: {"clawdbot":{"emoji":"🚆","requires":{"bins":["railil"]},"install":[{"id":"node","kind":"node","package":"railil","bins":["railil"],"label":"Install railil (npm)"}]}}
---

# Railil CLI

这是一个用于查询以色列Rail列车时刻表的命令行工具（CLI）。

## 安装

```bash
npm install -g railil
```

## 使用方法

该CLI支持对车站名称进行模糊匹配。

### 基本搜索

查询两个车站之间的下一班列车：

```bash
railil --from "Tel Aviv" --to "Haifa"
```

### 日期和时间

查询特定日期和时间的列车：

```bash
railil --from "Beer Sheva" --to "Tel Aviv" --time 08:00 --date 2023-11-01
```

### 输出格式

如需机器可读的输出或特定格式的输出，请使用`--output`标志。
支持的格式：`text`（默认）、`json`、`table`、`markdown`。

**JSON输出（推荐给自动化系统使用）：**
```bash
railil --from "Tel Aviv" --to "Haifa" --output json
```

**Markdown输出：**
```bash
railil --from "Tel Aviv" --to "Haifa" --output markdown
```

### 选项

- `-f, --from <车站>`：出发站名称（支持模糊匹配）。
- `-t, --to <车站>`：目的站名称（支持模糊匹配）。
- `-d, --date <日期>`：出行日期。
- `-h, --time <时间>`：出行时间（格式为HH:MM）。
- `-l, --limit <数量>`：限制结果数量。
- `-o, --output <格式>`：输出格式（`json`、`text`、`table`、`markdown`）。
- `--help`：显示帮助信息。

## 示例

**查询从本-古里安机场到耶路撒冷的下一班列车（共3班）：**
```bash
railil --from "Ben Gurion" --to "Jerusalem" --limit 3
```

**获取明早的列车时刻表（以JSON格式）：**
```bash
railil --from "Haifa" --to "Tel Aviv" --time 07:30 --output json
```
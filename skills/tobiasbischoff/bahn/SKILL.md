---
name: bahn
description: 使用 `bahn-cli` 工具搜索德国铁路（Deutsche Bahn）的列车连接信息。当您需要查找德国车站之间的列车线路、查询发车时间或协助制定旅行计划时，可以使用该工具。该工具支持输入诸如 “Berlin Hbf”（柏林中央火车站）、”München”（慕尼黑）、“Hannover”（汉诺威）等车站名称进行查询。
---

# 德国铁路 CLI（Deutsche Bahn CLI）

使用 `bahn-cli` 工具搜索列车班次。

## 安装

该工具应全局安装或安装在工作区中。如果尚未安装，请执行以下操作：

```bash
cd ~/Code/bahn-cli && npm install
```

## 使用方法

搜索列车班次：

```bash
cd ~/Code/bahn-cli && node index.js search "<from>" "<to>" [options]
```

### 参数选项

- `--date YYYY-MM-DD` - 出发日期（默认：今天）
- `--time HH:MM` - 出发时间（默认：当前时间）
- `--results <number>` - 显示的结果数量（默认：5）

### 示例

搜索从汉诺威（Hannover）到波恩（Bonn）的列车班次：
```bash
cd ~/Code/bahn-cli && node index.js search "Hannover Hbf" "Bonn Hbf" --results 3
```

使用特定日期和时间进行搜索：
```bash
cd ~/Code/bahn-cli && node index.js search "Berlin" "München" --date 2026-02-05 --time 14:30
```

## 车站名称

- 使用常见的德语车站名称
- “Hbf” 表示 Hauptbahnhof（主要车站）
- 例如：”Berlin Hbf”（柏林中央火车站）、”München Hbf”（慕尼黑中央火车站）、”Frankfurt(Main)Hbf”（法兰克福中央火车站）、”Köln Hbf”（科隆中央火车站）
- 车站名称不区分大小写

## 输出结果

该工具会显示以下信息：
- 出发时间和到达时间
- 乘车平台编号
- 行程时长
- 中转次数（对于需要中转的列车）
- 列车类型（ICE、IC、RE 等）

## 注意事项

- 该 CLI 使用 `db-vendo-client` 库进行数据查询
- 输出中某些车站名称可能会显示为 “undefined”（属于视觉问题，不影响功能）
- 直达列车会优先显示
- 时间采用 24 小时制显示
---
name: daily-investment-digest
description: 从 iYiou 技能 API 中获取融资事件列表，并以 Markdown 格式生成每日融资报告，输出到标准输出（stdout）。当任务要求通过 `https://api.iyiou.com/skill/info?page=...&pageSize=...` 获取投资/融资事件时，使用该脚本；分页设置为 `pageSize=10` 且 `page<=5`；对记录进行去重处理；默认使用昨天的日期；只有在用户明确请求时，才使用今天的日期。
---
# 每日投资摘要

## 概述

- 从 `https://api.iyiou.com/skill/info` 获取投资/融资事件数据。
- 对字段进行规范化处理，删除重复记录，并生成结构化的中文每日报告。

## 工作流程

1. 通过一个命令生成完整报告（推荐方式，默认使用昨日的数据）。  
```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --max-page 5
```

2. 如果用户明确要求查看当天的报告，请传递当天的日期。  
```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --report-date 2026-03-11 \
  --max-page 5
```

3. 直接输出模式（仅输出到标准输出，不生成文件）。  
```bash
node "{baseDir}/scripts/fetch_events.mjs" \
  --report-date 2026-03-11 \
  --stdout-json | \
node "{baseDir}/scripts/generate_report.mjs" \
  --input-json - \
  --top-n 0 \
  --stdout
```

## 路径安全性

- 在调用脚本时，始终使用带引号的 `{baseDir}` 路径以避免因空格导致的路径问题。  
- 脚本会相对于技能根目录解析相对路径。

## 必需的 API 规则

- 设置 `pageSize=10`。  
- 从 `page=1` 开始获取数据。  
- 每次请求将 `page` 增加 1。  
- 当 `page>5` 或 API 事件列表为空时停止请求。  
- 严格按照以下格式解析响应：`response.code` -> `response.data_posts`。  
- 如果 `code` 不为零，则视为 API 请求失败。  
- 对失败的请求最多重试 3 次，之后跳过当前页面。

## 脚本接口

### `scripts/run_full_report.mjs`

- 通过一个命令完成数据获取和报告生成。  
- 默认输出全部事件（`top-n=0`）。  
- 支持 `--report-date`、`--max-page`、`--page-size`、`--timeout-seconds`、`--retry`、`--delay-seconds` 参数。  
- 支持 `--top-n` 参数（`0` 表示输出所有事件）。

### `scripts/fetch_events.mjs`

- `--page-size` 默认值为 10。  
- `--max-page` 默认值为 5。  
- `--report-date` 默认值为昨日的日期（格式为 `YYYY-MM-DD`）。  
- `--timeout-seconds` 默认值为 15 秒。  
- `--retry` 默认值为 3 次。  
- `--delay-seconds` 默认值为 0 秒。  
- 始终将数据以 JSON 格式输出到标准输出（`--stdout-json` 仅用于兼容性）。  
- 所有数值参数都有范围限制：`page-size` 的范围是 [1, 100]，`max-page` 的范围是 [1, 500]，`retry` 的范围是 [1, 10]。

### `scripts/generate_report.mjs`

- 必须提供 `--input-json` 参数。  
- `--top-n` 默认值为 0（`0` 表示输出所有事件）。  
- 始终将报告文本输出到标准输出（`--stdout` 仅用于兼容性）。  
- 所有数值参数都有范围限制：`top-n` 的范围是 [0, 500]。

## 输出文件

- 本技能仅通过标准输出提供结果，不将报告文件保存到磁盘。

## 数据映射

- 请参考 [field_mapping.md](references/field_mapping.md) 了解源字段与目标字段之间的映射规则及备用方案。  
- 为减少数据量，仅保留以下字段：`brief`、`createdAt`、`originalLink`、`postTitle`、`tags`。

## 错误处理

- 即使某个页面的请求失败，也会继续处理后续页面的请求。  
- 采用渐进式重试机制（间隔时间分别为 0.5 秒、1.0 秒、1.5 秒等）。  
- 将页面级别的错误记录在输出 JSON 的 `meta.errors` 字段中。  
- 即使没有找到投资事件，也会生成报告，并明确标注为“空日报告”。

## 输出格式

- 日期默认为昨日的数据；用户明确要求查看当天数据时，才使用当天的数据。  
- 如果用户要求查看详细信息，可以使用 `--top-n 0` 参数。  
- 报告内容以标准输出的形式呈现，事件条目保持原样。  
- 输出顺序必须遵循以下规则：  
  1. 首先输出完整的投资事件列表。  
  2. 每个事件必须包含：`公司简称`、`轮次`、`投资方`、`事件摘要`、`来源链接`。  
  3. 在完整事件列表之后，添加一个名为“投资事件总结”的部分。  
  4. “投资事件总结”部分必须位于事件列表的最后。  

## 快速检查

- 在活跃的日子里，运行数据获取步骤并确认 `meta.total_unique_events` 的值大于 0。  
- 运行报告生成步骤并确认标准输出包含以下内容：  
  - `核心数据概览`  
  - `按行业分类的融资事件`  
- 在最终的 AI 响应中，确认以下顺序：  
    - 先输出事件列表，每个事件条目包含 `公司简称`、`轮次`、`投资方`、`事件摘要`、`来源链接`。  
    - “投资事件总结”部分仅出现在事件列表之后。  
    - “投资事件总结”部分在文档末尾出现一次。  

## 示例端到端命令  

```bash
node "{baseDir}/scripts/run_full_report.mjs" \
  --report-date 2026-03-11 \
  --max-page 5
```
---
name: translink-cli
description: 使用 `translink_*` 命令或插件命令来查询、排查故障并解释 Translink 的 SEQ GTFS 静态数据及实时数据。这些命令可用于查询时刻表信息、合并停靠站/路线/行程数据、实时检查车辆/行程状态、接收警报、审查数据结构的变化（schema drift），以及进行分页过滤等操作。
---
# Translink CLI 技能

适用于在此环境中处理 Translink 数据时使用。

## 先决条件

使用此技能之前，需要安装 Translink CLI 脚本，并确保它们已添加到系统的 PATH 环境变量中。

- CLI 仓库：`https://github.com/alanburchill/traslink-cli-scripts`
- 预期使用的命令：`translink_*`（或提供相同命令名称的等效封装工具）

如果未安装 CLI，请暂停操作并提示用户先进行安装。

## 命令接口

- Shell CLI：`translink_*`
- 插件命令：`/translink_*` 和 `/translink <command> [args...]`

## 核心工作流程

1. 当数据更新频率不确定时，使用 `translink_schedule_refresh` 命令刷新或验证缓存/数据结构。
2. 使用共享参数（`--where`、`--contains`、`--in`、`--page`、`--per-page` 等）进行查询。
3. 在遇到字段错误时，通过 JSON 错误信息中的模糊提示自动进行修正。
4. 使用主键（PK）/外键（FK）关联来连接不同的路线（routes）、行程（trips）、站点（stops）、站点时间（stop_times）和日历（calendar）等数据。
5. 如需获取最新的数据结构，请先阅读自动生成的数据结构文档。

## 共享参数规范

所有命令都支持以下参数：
- `--where field=value` （可重复使用）
- `--contains field=text` （可重复使用）
- `--in field=v1,v2,...` （可重复使用）
- `--fields a,b,c` （指定查询字段）
- `--sort field` （对查询结果进行排序）
- `--order asc|desc` （指定排序方式）
- `--page N` （指定查询页码，默认为 20）
- `--format table|json|csv` （指定输出格式）
- `--count-only` （仅输出计数结果）

## 实时扩展功能

- `--expand` （包含嵌套的 JSON 字段）
- `--raw` （输出完整的原始实体 JSON 数据）
- `--time epoch|iso` （指定时间格式）

## 定时更新功能

- `--refresh` （刷新缓存）
- `--schema` （获取当前数据结构）

## 运行时行为

- 静态缓存路径：`~/.openclaw/cache/translink/`
- 缓存有效期：24 小时
- 每日定时更新（例如：当地时间早上 5:00，通过 `translink:schedule-refresh` 命令执行）
- 为防止并发更新冲突，更新操作会加锁。
- 数据结构会根据新增字段自动更新。

## 参考文档

请根据需要查阅以下文档：
- `references/commands.md` — 命令、参数及错误处理规范
- `references/usage.md` — 使用示例
- `references/relationships.md` — 主键/外键关联机制
- `references/schema-generated.md` — 自动生成的实时数据结构文档
- `references/column-meanings.md` — GTFS 数据字段的含义说明
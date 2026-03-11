---
name: Skill Surge Notifier
slug: skill-surge-notifier
version: 0.1.0
author: "@gkauf_gm"
tags: [monitoring, clawhub, acceleration, meta]
homepage: https://github.com/Gabriel-Kaufman/skill-scraper/tree/main
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["node"]}}}
---

# 技能热度通知器（Skill Surge Notifier）

该工具会监控 ClawHub 上的热门技能，记录技能的下载量和星级评分的变化，并在技能热度突然上升时发出警报。

以下情况之一发生时，系统会触发警报：
- 下载量自上次检查以来增长超过 30%
- 总下载量超过 50,000 次
- 星级评分超过 200 分
- 有新技能进入前十名

---

## 安装要求

需要 Node.js 18 及更高版本。无需额外安装，可直接从技能包中运行该工具。

---

## 命令说明

| 命令          | 功能                |
|---------------|-------------------|
| `node {baseDir}/cli.js fetch` | 显示下载量排名前 20 的技能 |
| `node {baseDir}/cli.js check` | 检测技能热度变化、更新热门技能列表及状态 |
| `node {baseDir}/cli.js status` | 显示上次检查时间、阈值及通知状态 |
| `node {baseDir}/cli.js profile` | 显示当前代理的配置信息 |
| `node {baseDir}/cli.js profile set "description" "kw1,kw2"` | 设置技能的描述信息用于相关性评分 |
| `node {baseDir}/cli.js config movers=5` | 设置显示的热门技能数量 |
| `node {baseDir}/cli.js config movers-off` | 禁用热门技能显示功能 |
| `node {baseDir}/cli.js config growth=30 downloads=50000 stars=200` | 更新警报阈值 |

无论阈值如何，每次执行 `check` 命令时都会显示下载量变化最大的前 N 个技能。

当为某个技能设置了配置信息后，系统会根据其相关性为其打分（0-10 分），并按得分从高到低排序显示。

---

## 注意事项

- 系统状态信息存储在 `~/.skill-surge-notifier/state.json` 文件中。首次运行时会生成基准数据；后续运行时才会显示下载量增长率。
- 所有输出都会打印到标准输出（stdout）中。如果在代理程序中使用该工具，代理程序需要捕获这些输出并在聊天界面中显示警报信息。
- 如需自动运行该工具，可将其添加到 crontab 行程表中（使用 `crontab -e` 命令）。

```bash
0 */4 * * * node {baseDir}/cli.js check >> ~/.skill-surge-notifier/surge.log 2>&1
```

## 环境变量

以下可选的环境变量可用于覆盖默认的路径和行为设置：

| 变量            | 默认值                | 说明                          |
|-----------------|-----------------------------|-----------------------------------------|
| `SURGE_DIR`       | `~/.skill-surge-notifier`     | 所有状态文件和配置文件的基础目录             |
| `STATE_PATH`       | `$SURGE_DIR/state.json`     | 状态文件的路径                     |
| `CONFIG_PATH`       | `$SURGE_DIR/config.json`     | 配置文件的路径                     |
| `SCHEDULED`       | `false`             | 设为 `true` 时表示通过调度器运行；运行前会随机延迟 1–5 分钟以分散 API 请求负载 |
---
name: upcoming-metal-concerts
description: 使用 concerts-metal.com 按国家收集即将举行的金属音乐演唱会和音乐节的信息。当用户询问关于即将到来的金属音乐演出、演出活动或音乐节的相关信息时，可以使用这些数据。
metadata: {"openclaw":{"emoji":"🤘","requires":{"bins":["python3"]}}}
---
# 即将举行的金属音乐音乐会

您可以通过 concerts-metal.com 收集全球各地即将举行的金属音乐音乐会和音乐节的信息。

## 首次运行

首次运行时，系统会使用默认设置生成 `skill-config.json` 文件。**默认国家为西班牙（ES）**。请告知用户这一信息，并询问他们希望使用哪个国家的数据。要查看所有支持的国家代码，请运行以下命令：

```bash
python3 {baseDir}/scripts/events.py --list-countries
```

之后，请将用户选择的国家代码更新到 `{baseDir}/skill-config.json` 文件中的 `country` 配置项中，然后再开始数据收集。

## 使用方法

运行收集脚本，将音乐会数据抓取并存储到 `data/concerts.json` 文件中：

```bash
python3 {baseDir}/scripts/events.py
```

`--country` 参数可以在单次运行时覆盖配置文件中的国家设置，但不会对后续的运行产生影响：

```bash
python3 {baseDir}/scripts/events.py --country DE
```

重新运行收集脚本后，系统会合并新的音乐会信息，并标记那些在源网站中已取消的音乐会为“已取消”。每条音乐会记录包含以下信息：`date`（日期）、`artists`（艺术家）、`venue`（演出场地）、`city`（城市）、`url`（网址）、`discovered_at`（发现时间）以及 `status`（状态，可以是“active”或“cancelled”）。

## 更改设置

所有设置都保存在 `{baseDir}/skill-config.json` 文件中：

```json
{
  "country": "ES",
  "concert_days": 200
}
```

| 设置项 | 功能 | 更改方法 |
|---------|---------|-------------------|
| `country` | 抓取数据的国家代码（ISO格式）。 | 可设置为 `--list-countries` 命令输出的任意国家代码（例如：“DE”、“US”、“GB”）。 |
| `concert_days` | 查找音乐会的提前天数。 | 设置为一个正整数（例如：`90` 表示大约3个月，`365` 表示1年）。 |

如果用户需要更改国家或数据查询的提前时间范围，请直接编辑 `{baseDir}/skill-config.json` 文件中的相应设置项。

## 数据文件

所有数据都存储在 `data/` 目录下（该目录被 Git 忽略）：
- `concerts.json`：存储所有收集到的音乐会记录。

## 注意事项：
- 无需使用 API 密钥。数据来源于 concerts-metal.com 的音乐会页面。
- 该工具覆盖了 50 多个国家的金属、朋克、硬核及相关音乐类型的音乐会信息，覆盖范围非常广泛。
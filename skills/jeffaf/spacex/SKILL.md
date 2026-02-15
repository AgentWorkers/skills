---
name: spacex
version: 1.0.0
description: "这是一个用于AI代理的命令行界面（CLI），帮助人类查询SpaceX的发射任务和火箭相关信息。该工具无需任何身份验证即可使用。"
homepage: https://github.com/r-spacex/SpaceX-API
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["spacex", "rockets", "launches", "space", "cli"]
---

# SpaceX 查询工具

这是一个用于查询 SpaceX 发射任务、火箭信息以及宇航员信息的命令行工具（CLI），专为 AI 代理设计。用户可以询问诸如“下一次 SpaceX 发射是什么时候？”之类的问题，而该工具能够提供相应的答案。

该工具基于 SpaceX 的公共 API 进行数据查询，无需注册账户或 API 密钥。

## 使用方法

```
"What are the upcoming SpaceX launches?"
"Show me the last 5 SpaceX launches"
"Tell me about the Falcon 9"
"Who are the SpaceX crew members?"
```

## 命令列表

| 功能 | 命令                |
|------|-------------------|
| 查看即将进行的发射 | `spacex launches upcoming [limit]` |
| 查看过去的发射 | `spacex launches past [limit]` |
| 查看发射详情 | `spacex launch <id>` |
| 查看火箭信息 | `spacex rockets` |
| 查看宇航员信息 | `spacex crew [limit]` |

### 使用示例

```bash
spacex launches                    # Next 10 upcoming launches
spacex launches upcoming 5         # Next 5 upcoming launches
spacex launches past 5             # Last 5 launches
spacex launch 5eb87d47ffd86e000604b38a  # Full launch details
spacex rockets                     # All rockets
spacex rocket 5e9d0d95eda69973a809d1ec  # Falcon 9 details
spacex crew 5                      # First 5 crew members
```

## 输出结果

- **发射任务列表**：```
🚀 Starlink 4-36 (v1.5) — Falcon 9, 2022-10-20, Cape Canaveral
```
- **发射详情**：```
🚀 SAOCOM 1B, GNOMES-1, Tyvak-0172
   ID: 5eb87d47ffd86e000604b38a
   Flight #: 101
   Date: 2020-08-30 (hour)
   Rocket: Falcon 9
   Launchpad: Cape Canaveral
   Status: ✅ Success

📋 Details:
[Full mission description]

🎥 Webcast: https://youtu.be/P-gLOsDjE3E
📚 Wikipedia: https://en.wikipedia.org/wiki/SAOCOM
```
- **火箭信息列表**：```
🛸 Falcon 9 — rocket, 2010-06-04, Active, 98% success
```
- **宇航员信息**：```
👨‍🚀 Robert Behnken — NASA, active
```

## 注意事项

- 该工具使用 SpaceX 的 API v4（地址：api.spacexdata.com）
- 无需进行身份验证
- 数据可能存在延迟（由社区维护）
- 支持的火箭类型：Falcon 1、Falcon 9、Falcon Heavy、Starship
- 发射场：Cape Canaveral、Vandenberg、Boca Chica、Kwajalein

---

## 代理实现说明

- **脚本位置**：`{skill_folder}/spacex`（实际脚本位于 `scripts/spacex` 文件夹中）
- 当用户询问与 SpaceX 相关的信息时：
  - 使用 `./spacex launches` 命令查询即将进行的发射任务
  - 使用 `./spacex launches past [limit]` 命令查询过去的发射任务
  - 使用 `./spacex launch <id>` 命令查询特定发射任务的详细信息
  - 使用 `./spacex rockets` 命令查询火箭的详细信息
- **常见查询示例**：
  - “下一次 SpaceX 发射” → `spacex launches upcoming 1`
  - “最近的发射任务” → `spacex launches past 5`
  - “Falcon 9 的技术参数” → 先使用 `spacex rockets` 命令查询火箭信息，再使用 `spacex rocket <id>` 命令查询具体火箭的详细信息
  - “SpaceX 的宇航员名单” → `spacex crew [limit]`

**适用范围**：仅适用于 SpaceX 的相关查询；不支持 NASA、Blue Origin 等其他机构的发射任务。
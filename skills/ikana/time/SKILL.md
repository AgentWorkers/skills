---
name: time
slug: time
description: 用于时间相关命令行界面（time-related CLI）的大语言模型（LLM）时间推理框架。
when_to_use: Use when a task involves dates, deadlines, scheduling, or relative time reasoning.
metadata: {"openclaw":{"requires":{"bins":["temporal"]}}}
---
# 时间管理工具 `temporal`

使用 `temporal` 可以将当前时间（NOW）作为时间轴的基准点，并将事件按照它们在时间轴上的相对位置（未来或过去）进行标记，从而实现可靠的时间推理。

## 时间流逝的隐喻（必须理解）

请始终使用以下时间流逝的隐喻：
- 你是在时间中向前移动的。
- 未来位于你的前方。
- 过去位于你的后方。
- 正确的表述是：“我们正在接近截止日期。”
- 错误的表述是：“截止日期正在临近。”

## 先决条件

- 确保 `temporal` 已经添加到你的 `$PATH` 环境变量中。
- 如果 `temporal` 不在 `$PATH` 中，请从 `temporal` 目录运行 `scripts/install.sh` 脚本进行安装。
- `scripts/install.sh` 会自动检测操作系统和架构类型，验证文件的 SHA-256 校验和，并将程序安装到 `/usr/local/bin/temporal`（如果系统允许）或 `~/.local/bin/temporal`。
- 安装后的版本默认为 `v0.1.0`，你也可以通过 `TEMPORAL_VERSION=latest ./scripts/install.sh` 来指定安装最新版本。
- 确保 `~/.local/bin` 在 `$PATH` 中（例如，在 shell 配置文件中添加 `export PATH="$HOME/.local/bin:$PATH"`）。
- **macOS Apple Silicon** 的安装命令：
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-darwin-arm64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- **macOS Intel** 的安装命令：
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-darwin-x64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- **Linux x64** 的安装命令：
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-linux-x64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- **Linux ARM64** 的安装命令：
  `mkdir -p ~/.local/bin && curl -L https://github.com/Ikana/temporal/releases/latest/download/temporal-linux-arm64 -o ~/.local/bin/temporal && chmod +x ~/.local/bin/temporal`
- **建议在安装前验证文件校验和**（以确保安装的稳定性）：
  `VERSION=v0.1.0 && FILE=temporal-linux-x64 && curl -L https://github.com/Ikana/temporal/releases/download/$VERSION/$FILE -o /tmp/$FILE && curl -L https://github.com/Ikana/temporal/releases/download/$VERSION/temporal-checksums.txt -o /tmp/temporal-checksums.txt && grep " $FILE$" /tmp/temporal-checksums.txt | sha256sum -c -`
- 安装和构建的详细说明请参考 [github.com/Ikana/temporal](https://github.com/Ikana/temporal)。

## 快速入门

```bash
temporal init
temporal add "Sprint review" --on "2026-02-21" --type ceremony
temporal add "v0.3.0 deadline" --in "13 days" --type milestone --notes "new auth flow"
temporal show
```

## 命令说明

### `init [--timezone <iana_tz>] [--force]`

创建一个以当前时间为基准点的 `time.md` 文件。使用 `--force` 可以覆盖现有文件。

### `now [--timezone <iana_tz>]`

仅更新当前时间（NOW）的时间戳元数据，不会重新计算事件之间的时间距离。

### `add <event> [--in <duration> | --on <date> | --at <datetime>] [--type <type>] [--notes <text>]`

添加一个事件，需要指定事件发生的时间：
- `--in`：相对时间长度（例如：“3天”、“4小时后”、“2天前”）
- `--on`：具体日期（例如：“2026-03-01”、“明天”、“下周一”）
- `--at`：ISO 格式的日期时间（例如：“2026-02-20T14:00:00Z”）

### `show`

将完整的 `time.md` 内容输出到标准输出（stdout）。

### `past`

输出当前时间（NOW）以及过去的时间线部分。

### `ahead`

输出当前时间（NOW）以及未来的时间线部分。

### `refresh`

将当前时间（NOW）更新为当前系统时间，并重新计算所有事件之间的时间距离和顺序。

### `remove <event>`

从时间轴中删除指定的事件。

### `seq <name> <event1> <event2> [event3...]`

创建或更新一个命名的事件序列。

### `span <name> --from <when> --to <when>`

创建或更新一个命名的时间间隔。

## `time.md` 的格式说明

```markdown
# Time Context

## Now
- **timestamp**: 2026-02-19T09:00:00.000Z   <!-- anchor -->
- **weekday**: Thursday
- **week**: 8 of 52
- **quarter**: Q1 2026
- **timezone**: Europe/Amsterdam

## Timeline

### Behind (Past)
| distance | event | type | notes | iso |
|----------|-------|------|-------|-----|
| 1 day behind | bug #42 reported | issue | auth timeout | 2026-02-18T10:00:00.000Z |

### Ahead (Future)
| distance | event | type | notes | iso |
|----------|-------|------|-------|-----|
| 2 days ahead | sprint review | ceremony | demo v0.2.1 | 2026-02-21T14:00:00.000Z |

## Sequences
### release-cycle
v0.2.0 released → bug #42 reported → [NOW] → sprint review → v0.3.0 deadline

## Durations
| span | from | to | length |
|------|------|----|--------|
| current sprint | 5 days behind | 2 days ahead | 7 days |
```

## 临时使用模式（`/tmp`）

建议将临时使用的文件保存在 `/tmp` 目录中，以保持项目文件整洁：

```bash
cd /tmp
temporal init --force
temporal add "Draft due" --on "2026-02-25"
temporal add "Client review" --in "3 days"
temporal show
# draft your output using the timeline
rm -f time.md
```

## 序列（Sequences）

使用序列来表示有顺序的事件链，便于规划：

```bash
temporal seq "release-cycle" "RFC drafted" "Implementation starts" "Testing" "Launch"
```

`show` 命令会将 `[NOW]` 放置在序列事件中正确的位置。

## 时间间隔（Spans）

使用时间间隔来表示特定的时间范围：

```bash
temporal span "Sprint 12" --from "2026-02-17" --to "2026-02-28"
```

**持续时间表格** 显示了事件之间的时间距离和总时长。

## 重要规则

- 如果 `time.md` 文件可能已经过时，请在使用前运行 `temporal refresh` 命令更新数据。
- 事件名称必须是唯一的；重复添加相同名称的事件时请先删除旧记录。
- 所有的时间线信息都会输出到标准输出（stdout）。
- 错误或警告信息会输出到标准错误输出（stderr）。
- `temporal` 是完全非交互式的（不会显示任何提示信息）。
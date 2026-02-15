---
name: hevy-cli
description: 通过 `hevy-cli` 命令行工具与 Hevy 健身应用程序进行交互。当用户需要查看、创建或更新其 Hevy 账户中的锻炼计划、日常锻炼安排、锻炼模板或相关文件夹时，可以使用该工具。该工具适用于涉及锻炼跟踪、锻炼历史记录、日常锻炼计划管理或任何与 Hevy 相关的数据操作的场景。
---

# Hevy CLI

使用 `hevy` CLI 来操作 Hevy 健身应用程序的数据。需要设置环境变量 `HEVY_API_KEY`。

## 快速入门

```bash
# Verify access
hevy workouts count

# List recent workouts
hevy workouts list --page-size 10

# Raw JSON output for any command
hevy -j workouts list
```

## 常见任务

### 查看锻炼历史记录

```bash
hevy workouts list --page 1 --page-size 10
hevy workouts get <workout-id>
```

### 检查锻炼进度

```bash
# Find the exercise template ID first
hevy exercises list --page-size 100

# Then get history for that exercise
hevy exercises history <template-id>
hevy exercises history <template-id> --start-date 2025-01-01 --end-date 2025-02-01
```

### 创建锻炼计划

```bash
hevy workouts create \
  --title "Push Day" \
  --start-time 2025-01-15T08:00:00Z \
  --end-time 2025-01-15T09:00:00Z \
  --exercises-json '[{"exercise_template_id":"79D0BB3A","sets":[{"type":"normal","weight_kg":60,"reps":8}]}]'
```

对于复杂的锻炼计划，可以使用文件：`--exercises-json @exercises.json`

### 管理锻炼计划

```bash
hevy routines list
hevy routines create --title "Upper Body" --exercises-json @routine.json
hevy routines update <routine-id> --title "Updated Name"
```

### 使用文件夹进行组织

```bash
hevy folders list
hevy folders create --name "Hypertrophy Block"
```

## 关键用法模式

- 所有列表命令都支持 `--page` 和 `--page-size` 选项以实现分页。
- 在子命令前使用 `-j` 标志可输出 JSON 格式的数据：`hevy -j workouts list`。
- 创建/更新锻炼计划时，可以使用 `--exercises-json` 选项，该选项接受内联 JSON 数据或文件路径（`@filepath`）。
- 锻炼计划的类型包括：`normal`（常规）、`warmup`（热身）、`failure`（失败）、`dropset`（递减组）。
- 列表或获取响应中会返回锻炼计划的 ID——使用 JSON 模式（`-j`）可以获取这些 ID，以便后续命令使用。

## 完整命令参考

请参阅 [references/commands.md](references/commands.md)，以获取完整的命令语法、所有标志选项、锻炼类型/设备/肌肉组的枚举值，以及锻炼计划的 JSON 数据结构。
---
name: hevy
description: 从 Hevy 查询锻炼数据，包括锻炼记录、锻炼计划、具体练习内容以及锻炼历史。当用户询问他们的锻炼情况、健身房使用记录、锻炼进展或健身计划时，可以使用此功能。
homepage: https://hevy.com
metadata:
  clawdbot:
    emoji: "🏋️"
    requires:
      bins: ["hevy"]
      env: ["HEVY_API_KEY"]
---

# Hevy CLI

Hevy CLI 是用于 Hevy 锻炼跟踪 API 的命令行工具，支持查询锻炼记录、训练计划、具体练习内容以及跟踪锻炼进度。

## 设置

使用 Hevy CLI 需要订阅 Hevy Pro 订阅服务以访问 API。

1. 从 [https://hevy.com/settings?developer](https://hevy.com/settings?developer) 获取 API 密钥。
2. 设置环境变量：`export HEVY_API_KEY="your-key"`。

## 命令

### 状态查询
```bash
# Check configuration and connection
hevy status
```

### 锻炼记录查询
```bash
# List recent workouts (default 5)
hevy workouts
hevy workouts --limit 10

# Fetch all workouts
hevy workouts --all

# Show detailed workout
hevy workout <workout-id>

# JSON output
hevy workouts --json
hevy workout <id> --json

# Show weights in kg (default is lbs)
hevy workouts --kg
```

### 训练计划查询
```bash
# List all routines
hevy routines

# Show detailed routine
hevy routine <routine-id>

# JSON output
hevy routines --json
```

### 练习内容查询
```bash
# List all exercise templates
hevy exercises

# Search by name
hevy exercises --search "bench press"

# Filter by muscle group
hevy exercises --muscle chest

# Show only custom exercises
hevy exercises --custom

# JSON output
hevy exercises --json
```

### 练习历史查询
```bash
# Show history for specific exercise
hevy history <exercise-template-id>
hevy history <exercise-template-id> --limit 50

# JSON output
hevy history <exercise-template-id> --json
```

### 创建训练计划
```bash
# Create routine from JSON (stdin)
echo '{"routine": {...}}' | hevy create-routine

# Create routine from file
hevy create-routine --file routine.json

# Create a routine folder
hevy create-folder "Push Pull Legs"

# Update existing routine
echo '{"routine": {...}}' | hevy update-routine <routine-id>

# Create custom exercise (checks for duplicates first!)
hevy create-exercise --title "My Exercise" --muscle chest --type weight_reps

# Force create even if duplicate exists
hevy create-exercise --title "My Exercise" --muscle chest --force
```

**⚠️ 避免重复：** `create-exercise` 命令会检查是否存在同名练习，如果存在则返回错误。可以使用 `--force` 参数强制创建（不推荐）。

**训练计划的 JSON 格式：**
```json
{
  "routine": {
    "title": "Push Day 💪",
    "folder_id": null,
    "notes": "Chest, shoulders, triceps",
    "exercises": [
      {
        "exercise_template_id": "79D0BB3A",
        "notes": "Focus on form",
        "rest_seconds": 90,
        "sets": [
          { "type": "warmup", "weight_kg": 20, "reps": 15 },
          { "type": "normal", "weight_kg": 60, "reps": 8 }
        ]
      }
    ]
  }
}
```

### 其他功能
```bash
# Total workout count
hevy count

# List routine folders
hevy folders
```

## 使用示例

- **用户询问：“我在健身房做了什么？”**
```bash
hevy workouts
```

- **用户询问：“显示我上次的胸部锻炼记录”**
```bash
hevy workouts --limit 10  # Find relevant workout ID
hevy workout <id>         # Get details
```

- **用户询问：“我的卧推锻炼进展如何？”**
```bash
hevy exercises --search "bench press"  # Get exercise template ID
hevy history <exercise-id>              # View progression
```

- **用户询问：“我有哪些训练计划？”**
```bash
hevy routines
hevy routine <id>  # For details
```

- **用户询问：“查找腿部锻炼动作”**
```bash
hevy exercises --muscle quadriceps
hevy exercises --muscle hamstrings
hevy exercises --muscle glutes
```

- **用户询问：“创建一个力量训练计划”**
```bash
# 1. Find exercise IDs
hevy exercises --search "bench press"
hevy exercises --search "shoulder press"
# 2. Create routine JSON with those IDs and pipe to create-routine
```

## 注意事项

- **避免重复：** `create-exercise` 命令在创建新练习前会检查是否存在同名练习。可以使用 `--force` 参数忽略此检查（不推荐）。
- **API 限制：** Hevy API 不支持删除或编辑练习模板，仅支持创建新练习。请在应用程序中手动删除练习记录。
- **API 调用频率限制：** 在批量获取数据时请注意 API 的调用频率限制（使用 `--all` 参数）。
- **重量单位：** 默认为磅（lbs），如需使用公斤（kg）请使用 `--kg` 参数。
- **分页：** 大多数命令支持分页，但使用 `limit` 参数可以减少 API 调用次数。
- **ID：** 锻炼记录、训练计划和练习的 ID 为 UUID，在详细信息页面中显示。

## API 参考

完整 API 文档：[https://api.hevyapp.com/docs/](https://api.hevyapp.com/docs/)

### 可用的 API 端点
- `GET /v1/workouts` - 列出所有锻炼记录（支持分页）
- `GET /v1/workouts/{id}` - 获取单个锻炼记录
- `GET /v1/workouts/count` - 获取锻炼记录总数
- `GET /v1/routines` - 列出所有训练计划
- `GET /v1/routines/{id}` - 获取单个训练计划
- `GET /v1/exercise_templates` - 列出所有练习模板
- `GET /v1/exercise_templates/{id}` - 获取单个练习模板
- `GET /v1/exercise_history/{id}` - 查看练习历史记录
- `GET /v1/routine_folders` - 列出所有训练计划文件夹

### 写入操作（支持但需谨慎使用）

- `POST /v1/workouts` - 创建新的锻炼记录
- `PUT /v1/workouts/{id}` - 更新锻炼记录
- `POST /v1/routines` - 创建新的训练计划
- `PUT /v1/routines/{id}` - 更新训练计划
- `POST /v1/exercise_templates` - 创建新的练习模板
- `POST /v1/routine_folders` - 创建新的训练计划文件夹

该 CLI 主要用于读取数据，写入操作需通过 API 客户端进行编程实现。
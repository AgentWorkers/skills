---
name: workout
description: 使用 `workout-cli` 来跟踪锻炼记录、记录训练组别、管理练习内容及模板。该工具支持多用户配置文件。适用于帮助用户记录健身房锻炼情况、查看历史数据或分析力量提升过程。
metadata: {"clawdbot":{"emoji":"🏋️","requires":{"bins":["workout"]}}}
---

# Workout CLI

## 多用户配置文件

多人可以使用不同的配置文件独立记录自己的锻炼情况。

```bash
workout profile list               # List all profiles
workout profile create sarah       # Create new profile
workout profile delete old         # Delete profile
```

当存在多个配置文件时，请指定使用哪个配置文件：
```bash
workout --profile mike start push-day
workout --profile mike log bench-press 185 8
workout --profile mike done
```

- **单用户配置文件**：无需使用 `--profile` 参数即可执行命令（向后兼容）
- **共享练习**：练习库在所有配置文件之间共享
- **用户专属数据**：模板、锻炼计划和配置设置均为每个用户单独保存

## 重要规则

### 1. 必须先添加新的练习
如果用户提到了库中不存在的练习，请在记录锻炼前先将其添加到库中：
```bash
workout exercises add "Dumbbell RDL" --muscles hamstrings,glutes --type compound --equipment dumbbell
```
切勿跳过此步骤——否则未知的练习将无法被正确记录。

### 2. 记录准确的数值——注释不能替代实际数据
每个训练组都需要记录正确的重量和重复次数。这些数据用于统计分析（如训练量、进步情况等）。
- ❌ 错误做法：先记录 0 磅，再在注释中补充实际重量
- ✅ 正确做法：直接记录实际使用的重量

如果用户未指定重量，请在记录前询问用户。切勿默认为 0。

### 3. 注释仅用于补充说明
注释用于提供额外信息（如受伤情况、动作技巧、设备使用说明等），但不能用于修改错误的数据：
```bash
workout note "Left elbow tender today"
workout note bench-press "Used close grip"
```

## 核心命令
```bash
workout start --empty              # Start freestyle session
workout start push                 # Start from template
workout log bench-press 135 8      # Log set (weight reps)
workout log bench-press 135 8,8,7  # Log multiple sets
workout note "Session note"        # Add note
workout note bench-press "Note"    # Note on exercise
workout swap bench-press db-bench  # Swap exercise
workout done                       # Finish session
workout cancel                     # Discard
```

## 编辑和修正已记录的训练组数据
```bash
workout undo                       # Remove last logged set
workout undo bench-press           # Remove last set of specific exercise
workout edit bench-press 2 155 8   # Edit set 2: weight=155, reps=8
workout edit bench-press 2 --reps 10 --rir 2  # Edit reps and RIR
workout delete bench-press 3       # Delete set 3 entirely
```
训练组的编号是从 1 开始的。可以使用这些编号在锻炼过程中修正错误。

## 练习
```bash
workout exercises list
workout exercises list --muscle chest
workout exercises add "Name" --muscles biceps --type isolation --equipment cable
```
⚠️ 使用 `exercises add` 命令时，必须指定 `--muscles`（锻炼涉及的肌肉群）、`--type`（练习类型）和 `--equipment`（使用设备）。

设备选项：杠铃、哑铃、缆绳、机器、自重、壶铃、弹力带等

## 模板
```bash
workout templates list
workout templates show push
workout templates create "Push" --exercises "bench-press:4x8,ohp:3x8"
```

## 训练记录历史与进度更新（PRs）
```bash
workout last                       # Last workout
workout history bench-press        # Exercise history
workout pr                         # All PRs
workout pr bench-press             # Exercise PRs
workout volume --week              # Weekly volume
workout progression bench-press    # Progress over time
```

## 典型的训练流程
```bash
# 1. Start
workout start push

# 2. Log with REAL numbers
workout log bench-press 135 8
workout log bench-press 145 8
workout log bench-press 155 6

# 3. Notes for context only
workout note bench-press "Felt strong today"

# 4. Finish
workout done
```

## 设备变体
对于使用不同设备的练习，需要使用相应的名称进行区分：
- `bench-press`（使用杠铃） vs `dumbbell-bench-press`（使用哑铃）
- `romanian-deadlift`（使用杠铃） vs `dumbbell-rdl`（使用哑铃）
- `shoulder-press`（使用杠铃） vs `dumbbell-shoulder-press`（使用哑铃）

## 注意事项
- 重量单位为磅（lbs）
- 可以多次使用 `log` 命令记录不同的重量数据
- `swap` 命令可用于将所有已记录的训练组数据替换为新的练习信息
- 所有命令都支持 `--json` 参数（用于格式化输出数据）
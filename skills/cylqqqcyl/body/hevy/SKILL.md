---
name: hevy
description: 与 Hevy 应用程序的全面健身追踪集成。适用于需要记录锻炼情况、分析运动进度、获取健身数据、创建/管理锻炼计划或查询锻炼历史记录的场景。支持 JSON 格式的数据输出以便进行结构化分析。使用 API 需要订阅 Hevy Pro 订阅服务。
---
# Hevy健身追踪

通过与Hevy应用程序集成，实现全面的健身追踪、训练分析以及进度监控功能。

## 先决条件

- **Hevy Pro订阅**（API访问所需）
- 从[Hevy开发者设置](https://hevy.com/settings?developer)获取**API密钥**

## 快速入门

### 1. 安装hevycli

```bash
./scripts/install_hevycli.sh
```

### 2. 配置API密钥

```bash
./scripts/configure_api.sh YOUR_API_KEY
```

### 3. 测试安装

```bash
hevycli workout count --output json
```

## 核心功能

### 训练追踪

- **列出最近的训练记录：**
```bash
hevycli workout list --since 2026-02-01 --output json
```

- **获取特定训练的详细信息：**
```bash
hevycli workout get <workout-id> --output json
```

- **获取训练次数：**
```bash
hevycli workout count --output json
```

### 进度分析

- **追踪锻炼进度：**
```bash
hevycli stats progress "Bench Press" --output json
hevycli stats progress "Squat" --metric 1rm --output json
```

- **获取训练总结：**
```bash
hevycli stats summary --period month --output json
hevycli stats summary --period week --output json
```

- **查看个人记录：**
```bash
hevycli stats records --output json
hevycli stats records --exercise "Bench Press" --output json
```

### 锻炼管理

- **搜索锻炼项目：**
```bash
hevycli exercise search "bench" --output json
```

- **列出锻炼模板：**
```bash
hevycli exercise list --output json
```

### 训练计划管理

- **列出训练计划：**
```bash
hevycli routine list --output json
```

- **获取训练计划的详细信息：**
```bash
hevycli routine get <routine-id> --output json
```

## 便捷脚本

- **最近活动分析：**
```bash
# Last 7 days of workouts
./scripts/get_recent_workouts.sh 7 json

# Last 30 days
./scripts/get_recent_workouts.sh 30 json
```

- **进度追踪：**
```bash
# Weight progression
./scripts/track_progress.sh "Bench Press" weight json

# Estimated 1RM progression  
./scripts/track_progress.sh "Deadlift" 1rm json
```

- **统计概览：**
```bash
# Monthly stats with records
./scripts/get_stats.sh month json

# Weekly overview
./scripts/get_stats.sh week json
```

## 集成方式

### 身体状态追踪

- **每日训练总结：**
```bash
# Check if workout completed today
TODAY=$(date +%Y-%m-%d)
hevycli workout list --since $TODAY --output json | jq '.[] | {title, duration_minutes: (.end_time | fromdate) - (.start_time | fromdate) | . / 60}'
```

- **每周训练量分析：**
```bash
WEEK_AGO=$(date -d '7 days ago' +%Y-%m-%d)
hevycli workout list --since $WEEK_AGO --output json | jq 'map(.exercises[].sets | map(.weight_kg * .reps) | add) | add'
```

- **实现目标的进度：**
```bash
# Track specific lift PRs
hevycli stats records --exercise "Bench Press" --output json | jq '.records[0].weight_kg'
```

### RPG集成

每次训练都可以被视为一个“任务”，根据以下指标获得经验值（XP）：
- **训练量**：总举重重量
- **训练时间**：训练所花费的时间
- **训练频率**：连续训练的天数
- **训练进步**：个人最佳记录（PR）和力量提升

**经验值计算示例：**
```bash
# Get today's workout volume for XP calculation
hevycli workout list --since $(date +%Y-%m-%d) --output json | \
jq '[.[].exercises[].sets[] | (.weight_kg // 0) * (.reps // 0)] | add // 0'
```

## 数据格式

所有命令都支持`--output json`选项，以便结构化的数据被代理程序读取。请参阅`references/data_structures.md`以获取完整的JSON格式示例。

### 关键字段

- **训练记录：**id、标题、开始时间、结束时间、锻炼项目、备注
- **锻炼项目：**标题、涉及的肌肉群、组数（重量/公斤、重复次数、RPE）
- **统计信息：**总训练次数、总训练重量（公斤）、平均训练时间（分钟）
- **个人记录：**锻炼项目、举重重量、重复次数、训练日期、预计1RM重量（公斤）

## 配置

配置文件位置：`~/.hevycli/config.yaml`

**推荐的代理程序设置：**
```yaml
api:
  key: "your-api-key"
display:
  output_format: json
  color: false
  units: metric
```

## 故障排除

### API问题

- **401未经授权**：检查API密钥和Hevy Pro订阅状态
- **速率限制**：Hevy API有速率限制，请合理安排请求间隔
- **网络错误**：检查网络连接是否正常

### 安装问题

- **二进制文件未找到**：确保`~/.local/bin`在系统路径中
- **权限问题**：使脚本可执行：`chmod +x scripts/*.sh`

## 参考资料

- **命令参考**：`references/api_commands.md` - 完整的CLI命令指南
- **数据结构**：`references/data_structures.md` - JSON格式及示例
- **Hevy API文档**：https://api.hevyapp.com/docs/
- **Hevy应用程序**：https://www.hevyapp.com/

## 安全注意事项

- API密钥存储在`~/.hevycli/config.yaml`文件中或环境变量`HEVY_API_KEY`中
- 确保配置文件的权限设置为600（仅允许所有者读写）
- 绝不要将API密钥提交到版本控制系统中
- API密钥提供了对所有Hevy数据的读写权限
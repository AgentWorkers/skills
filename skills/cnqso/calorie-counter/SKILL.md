---
name: calorie-counter
description: **功能概述：**  
该工具用于记录每日摄入的卡路里和蛋白质含量，帮助用户设定目标并记录体重变化。当用户提到所吃的食物、想要了解剩余的卡路里摄入量或需要监测体重时，可以随时使用该工具。数据会自动存储在 SQLite 数据库中，并每日生成摄入总量的统计报告。  

**主要功能：**  
1. **记录每日摄入量：** 自动记录用户每天摄入的卡路里和蛋白质数量。  
2. **目标设定：** 允许用户设定每日或每周的卡路里和蛋白质摄入目标。  
3. **体重追踪：** 用户可以随时查看自己的体重变化。  
4. **食物查询：** 提供功能让用户查询所摄入食物的具体卡路里和蛋白质含量。  
5. **数据存储：** 数据安全地存储在 SQLite 数据库中，支持数据备份和恢复。  
6. **统计报告：** 每日自动生成摄入总量的统计报告，帮助用户了解自己的饮食状况。  

**使用场景：**  
- 适用于需要控制饮食和健康管理的用户。  
- 适合健身、减肥或保持健康的人群。  

**注意事项：**  
- 请确保在设备上安装了 SQLite 数据库支持的应用程序，以便数据存储和查询。  
- 定期备份数据，以防数据丢失。  

**技术细节：**  
- 使用 SQLite 数据库进行数据存储，确保数据的安全性和持久性。  
- 采用简洁的界面设计，易于用户操作。  
- 提供实时计算功能，帮助用户实时了解自己的饮食摄入情况。
metadata: { "openclaw": { "emoji": "🍎", "requires": { "python": ">=3.7" } } }
---

# 卡路里计数器

这是一个简单可靠的卡路里和蛋白质追踪工具，使用 SQLite 数据库进行存储。

## 主要功能

- **手动输入**：可以添加包含卡路里和蛋白质的食物信息。
- **蛋白质追踪**：监控每日蛋白质摄入量。
- **每日目标**：设置自定义的卡路里摄入目标。
- **体重追踪**：记录体重（单位：磅）。
- **即时反馈**：添加食物后即可立即查看总摄入量。
- **历史记录**：查看过去几天的数据及变化趋势。

## 使用方法

### 添加食物
```bash
python scripts/calorie_tracker.py add "chicken breast" 165 31
python scripts/calorie_tracker.py add "banana" 100 1
```
添加食物后，会立即显示当天的总摄入量及剩余卡路里。

### 查看当天总结
```bash
python scripts/calorie_tracker.py summary
```
显示：
- 当天的所有食物记录
- 总摄入的卡路里和蛋白质
- 每日目标及剩余卡路里
- 进度百分比

### 设置目标
```bash
python scripts/calorie_tracker.py goal 2000
```
设置每日卡路里目标（该目标会持续保存）。

### 体重追踪
```bash
python scripts/calorie_tracker.py weight 175
python scripts/calorie_tracker.py weight-history
```
体重以磅为单位进行记录（允许使用小数，例如：175.5磅）。

### 查看历史记录
```bash
# Last 7 days
python scripts/calorie_tracker.py history

# Last 30 days
python scripts/calorie_tracker.py history 30
```

### 删除记录
```bash
# List entries to get ID
python scripts/calorie_tracker.py list

# Delete by ID
python scripts/calorie_tracker.py delete 42
```

## 数据库

使用 SQLite 数据库：`calorie_data.db`

### 数据表结构

**entries**（食物记录）：
- id（整数）：自动递增
- date（文本）：YYYY-MM-DD 格式
- food_name（文本）
- calories（整数）：卡路里含量
- protein（整数）：蛋白质含量
- created_at（时间戳）：自动记录

**daily_goal**（每日目标）：
- id（整数）：始终为 1
- calorie_goal（整数）：每日目标卡路里数值

**weight_log**（体重记录）：
- id（整数）：自动递增
- date（文本）：YYYY-MM-DD 格式
- weight_lbs（实数）：体重（单位：磅，允许使用小数）
- created_at（时间戳）：自动记录

## 使用说明

**重要提示：**  
该工具位于您的代理工作区的 `workspace/calorie-counter/` 目录下。所有命令都应使用此路径前缀。

### 用户提到食物时的操作：
1. 提取食物的名称、卡路里含量和蛋白质含量（如果未提供，则进行估算）。
2. 运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py add "食物名称" 卡路里含量 蛋白质含量`
3. 命令会立即显示总摄入量（无需单独运行总结功能）。

**示例：**
- 用户：**我午餐吃了鸡胸肉，大约165卡路里。**
- 估算蛋白质含量（鸡肉每165卡路里约含30克蛋白质）：
  运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py add "chicken breast" 165 30`

### 用户想要查看剩余卡路里时：
运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py summary`

### 用户设置目标时：
运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py goal 卡路里目标`

### 用户记录体重时：
1. 如需将单位转换为磅（1千克约等于2.205磅），请先进行转换。
2. 运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py weight [体重值]`

### 用户想要删除记录时：
1. 运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py list` 查看记录ID。
2. 运行命令：`python3 workspace/calorie-counter/scripts/calorie_tracker.py delete [记录ID]`

### 蛋白质含量估算指南：
如果用户未提供蛋白质含量，可根据食物类型进行估算：
- **瘦肉**（如鸡肉、火鸡）：每卡路里约含0.30克蛋白质
- **鱼类**：每卡路里约含0.25克蛋白质
- **红肉**：每卡路里约含0.20克蛋白质
- **鸡蛋**：每卡路里约含0.12克蛋白质（1个鸡蛋约70卡路里，含6克蛋白质）
- **希腊酸奶**：每卡路里约含0.10克蛋白质
- **坚果**：每卡路里约含0.04克蛋白质
- **面包/意大利面**：每卡路里约含0.03克蛋白质
- **水果**：每卡路里约含0.01克或更少蛋白质
- **蔬菜**：每卡路里约含0.02-0.04克蛋白质

**不确定时，请保守估算或询问用户。**

## 其他注意事项：
- 卡路里和蛋白质含量为整数（不支持小数）。
- 体重以磅为单位记录（允许使用小数）。
- 数据库会在首次使用时自动生成。
- 所有时间均以本地时区显示。
- 日期格式为 YYYY-MM-DD。
- 列表中的时间显示为 `created_at` 时间戳（格式为 HH:MM）。

## 示例使用流程
```bash
# Set goal
$ python scripts/calorie_tracker.py goal 2000
✓ Set daily goal: 2000 cal

# Add breakfast
$ python scripts/calorie_tracker.py add "oatmeal" 150 5
✓ Added: oatmeal (150 cal, 5g protein)
  Entry ID: 1
  Today: 150 / 2000 cal (remaining: 1850) | Protein today: 5g | Entries: 1

# Add lunch
$ python scripts/calorie_tracker.py add "grilled chicken salad" 350 45
✓ Added: grilled chicken salad (350 cal, 45g protein)
  Entry ID: 2
  Today: 500 / 2000 cal (remaining: 1500) | Protein today: 50g | Entries: 2

# Check summary
$ python scripts/calorie_tracker.py summary
============================================================
DAILY SUMMARY - 2026-02-05
============================================================
Entries: 2
Total consumed: 500 cal | 50g protein
Daily goal: 2000 cal
Remaining: 1500 cal
  25.0% of goal consumed
============================================================

# Log weight
$ python scripts/calorie_tracker.py weight 175.5
✓ Logged weight: 175.5 lbs
```
---
name: apple-photos-cleaner
description: Analyze, clean up, and organize Apple Photos libraries. Find and report junk photos (screenshots, low-quality, burst leftovers, duplicates), analyze storage usage, generate photo timeline recaps, plan smart exports, analyze Live Photos, check iCloud sync, audit shared libraries, detect similar photos, curate seasonal highlights, and score face quality. All analysis operations are READ-ONLY on the database (safe). macOS only. Requires Python 3.9+ (stdlib only) and access to the Apple Photos SQLite database. Trigger on: Photos cleanup, photo storage, duplicate photos, junk photos, screenshot cleanup, Photos analysis, photo timeline, photo export, Photos library stats, burst cleanup, storage hogs, photo organization, Live Photos, iCloud sync, shared library, similar photos, seasonal highlights, face quality, portraits.
license: MIT
metadata: {"openclaw": {"os": ["darwin"], "emoji": "📸", "homepage": "https://github.com/and3rn3t/apple-photos-cleaner", "requires": {"bins": ["python3"]}}}
---

# 苹果照片清理工具

这是一个全面的工具包，用于分析和清理苹果照片库。它的功能超出了Photos应用程序本身的限制：智能识别垃圾文件、详细分析存储空间、查找重复照片并评估其质量、生成时间线摘要以便讲述故事，以及智能规划导出方案。

## 概述

苹果照片应用程序在组织和同步照片方面表现出色，但在清理方面则不够完善。本工具可以填补这一空白：

- **库分析** — 提供整体概览：照片数量、存储空间使用情况、日期范围、人物信息、照片质量分布
- **垃圾文件查找** — 识别截图、低质量照片、未选择的连拍照片、旧截图
- **重复照片查找** — 利用苹果内置的检测机制结合时间戳和尺寸信息查找重复照片
- **存储空间分析** — 按年份、类型、文件格式详细分析存储使用情况，以及存储空间占用较大的文件
- **时间线摘要** — 为任意日期范围生成照片活动的叙述性总结
- **智能导出** — 可按年份/月份、人物、相册或地点规划有序导出；支持使用AppleScript导出
- **最佳照片/隐藏珍品** — 突出显示你尚未收藏的高质量照片
- **人物分析** — 深入分析人物出现的频率、随时间的变化趋势，以及每个人的最佳照片
- **位置映射** — 将GPS坐标聚类到具体位置，识别出行记录
- **场景搜索** — 根据机器学习识别的场景（如海滩、狗狗、食物等）搜索照片，或生成内容清单
- **照片习惯分析** — 分析拍摄习惯：一天中的不同时间、一周中的不同日子、拍摄频率的规律性
- **今日回顾** — 查看过去几年中你在今天拍摄的照片
- **相册审核** — 找出孤立的照片、空相册以及相册之间的重复照片
- **清理执行器** — 通过AppleScript批量将垃圾文件移至“最近删除”文件夹（可恢复30天）

## 使用场景

当用户提到以下需求时，可以使用本工具：
- 清理照片库/释放存储空间
- 查找重复照片
- 删除旧截图
- 分析照片库的存储使用情况
- 查找垃圾文件或低质量照片
- 组织照片导出
- 获取照片时间线摘要（“我上周做了什么？”）
- 清理连拍照片
- 查找占用大量存储空间的照片
- 找出最佳或隐藏的照片
- 分析照片中的人物关系
- 查明照片的拍摄地点、出行记录
- 按内容（如海滩、日落、狗狗、食物等）搜索照片
- 分析拍摄习惯和模式
- 查看过去几年中“今天”拍摄的照片
- 审核相册结构、孤立的照片或相册间的重复内容
- 实际执行垃圾文件的删除（批量清理）

## 快速入门

所有脚本均可独立运行。照片数据库的默认位置为：
`~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite`

**基本工作流程：**
1. 运行 `library_analysis.py` 以获取整体概览
2. 运行 `junk_finder.py` 以识别需要清理的文件
3. 运行 `duplicate_finder.py` 以查找重复照片
4. 根据分析结果在Photos应用程序中手动进行清理

## 命令

### 1. 库分析

获取照片库的全面统计信息：照片数量、存储空间使用情况、日期范围、人物信息、照片质量评分。

```bash
python3 scripts/library_analysis.py [--human] [--output FILE]
```

**选项：**
- `--human` — 以人类可读的格式输出摘要，而非JSON
- `--output FILE` — 将结果写入文件
- `--db-path PATH` — 自定义数据库路径
- `--library PATH` — 自定义照片库路径

**示例输出：**
```
📊 APPLE PHOTOS LIBRARY ANALYSIS
==================================================

Total Assets: 12,453
Total Storage: 48.3 GB
Average Size: 4.1 MB
Date Range: 2020-01-15 to 2025-03-03

By Type:
  Photo: 11,234
  Video: 891
  Screenshots: 328
  Favorites: 456
  Bursts: 1,234

By Year:
  2025: 1,203 items, 5.2 GB
  2024: 3,456 items, 15.1 GB
  2023: 2,987 items, 12.4 GB
  ...

Top People:
  Jonah: 3,456 photos
  Silas: 3,234 photos
  ...
```

**对话示例：**
**用户：**“我有多少张照片？”
**AI：** *运行 `library_analysis.py` 并使用 `--human` 选项，输出摘要*

**用户：**“显示我的照片存储空间使用情况”
**AI：** *运行 `library_analysis.py`，突出显示关键数据*

---

### 2. 垃圾文件查找

识别需要清理的文件：截图、低质量照片、未选择的连拍照片、重复照片。

```bash
python3 scripts/junk_finder.py [--screenshot-age DAYS] [--quality-threshold N] [--human]
```

**选项：**
- `--screenshot-age DAYS` — 将超过N天的截图视为垃圾文件（默认值：30天）
- `--quality-threshold N` — 低质量照片的阈值（默认值：0.3，范围：0.0-1.0）
- `--no-duplicates` — 跳过重复照片检测
- `--human` — 以人类可读的格式输出摘要
- `--output FILE` — 将结果写入文件

**示例输出：**
```
🗑️  JUNK FINDER RESULTS
==================================================

Found:
  📸 Screenshots: 328
     └─ Old (>30 days): 287
  📉 Low Quality: 156
  📸 Burst Leftovers: 1,089
  👥 Possible Duplicates: 45

Estimated Savings:
  Conservative: 2.3 GB
    (Old screenshots + burst leftovers)
  Aggressive: 5.7 GB
    (All screenshots + low quality + bursts + ~50% of duplicates)
```

**查找结果：**
- **截图** — 通过 `ZISDETECTEDSCREENSHOT` 标志识别
- **旧截图** — 超过指定时间的截图（可安全删除）
- **低质量照片** — 分数较低的照片（构图或光线不佳）
- **未选择的连拍照片** — 未从连拍序列中选择的照片
- **可能的重复照片** — 使用苹果内置的检测机制识别

**对话示例：**
**用户：**“在我的照片中找到垃圾文件”
**AI：** *运行 `junk_finder.py`，报告总数及预计节省的空间*

**用户：**“我有多少张旧截图？”
**AI：** *运行 `junk_finder.py`，重点显示截图的相关数据*

**用户：**“我应该删除哪些文件来释放5GB的存储空间？”
**AI：** *运行 `junk_finder.py`，提供保守/激进的删除建议*

---

### 3. 重复照片查找

查找重复照片，并根据质量、收藏状态和文件大小推荐保留哪些照片。

```bash
python3 scripts/duplicate_finder.py [--human] [--output FILE]
```

**检测方法：**
1. **苹果内置检测** — 使用 `ZDUPLICATEASSETVISIBILITYSTATE`
2. **时间戳 + 尺寸** — 在同一秒内拍摄且尺寸相同的照片

**推荐逻辑：**
- 收藏的照片优先保留
- 截图会受到一定的扣分
- 优先选择质量最高的照片
- 文件大小作为决定因素（相同大小时）

**示例输出：**
```
👥 DUPLICATE FINDER RESULTS
==================================================

Found 12 duplicate groups
Total duplicates: 27
Can safely delete: 15
Total size: 156 MB
Potential savings: 89 MB

Sample groups (showing first 5):

Group 1 (apple_builtin):
  ✓ KEEP ★ IMG_1234.jpg (4.2 MB, Q:0.823)
    DELETE   IMG_1234-2.jpg (4.1 MB, Q:0.801)

Group 2 (timestamp_dimensions):
  ✓ KEEP   IMG_5678.heic (2.8 MB, Q:0.756)
    DELETE   IMG_5678-edited.jpg (3.1 MB, Q:0.654)
```

**对话示例：**
**用户：**“我有重复的照片吗？”
**AI：** *运行 `duplicate_finder.py`，报告检测结果*

**用户：**“找出重复照片并告诉我哪些应该删除”
**AI：** *运行 `duplicate_finder.py`，解释推荐方案*

---

### 4. 存储空间分析

按年份、类型、来源详细分析存储使用情况，包括增长趋势和文件类型。

```bash
python3 scripts/storage_analyzer.py [--human] [--output FILE]
```

**分析内容：**
- 照片/视频的总存储空间及细分
- 按年份和月份划分的存储空间使用情况
- 截图与普通照片的对比
- 文件类型（JPEG、HEIC、MOV等）
- 随时间的变化趋势
- 占用最大存储空间的前20个文件

**示例输出：**
```
💾 STORAGE ANALYSIS
==================================================

Total Storage: 48.3 GB

By Type:
  Photo: 32.1 GB (66.5%)
    11,234 items, avg 2.9 MB
  Video: 16.2 GB (33.5%)
    891 items, avg 18.7 MB

By Source:
  Photos & Videos: 46.1 GB (95.4%)
  Screenshots: 2.2 GB (4.6%)

By Year:
  2025: 5.2 GB (1,203 items)
  2024: 15.1 GB (3,456 items)
  2023: 12.4 GB (2,987 items)
  ...

Top 10 Largest Files:
  1. 📹 287 MB - VID_2024_vacation.mov
  2. 📹 245 MB - VID_2024_swim_meet.mov
  3. 📹 198 MB - VID_2023_birthday.mov
  ...

Recent Growth (last 12 months):
  Total added: 18.7 GB
  Average per month: 1.6 GB
```

**对话示例：**
**用户：**“我的照片中哪些文件占用了最多的空间？”
**AI：** *运行 `storage_analyzer.py`，突出显示占用最大的文件类别*

**用户：**“显示我的最大视频文件”
**AI：** *运行 `storage_analyzer.py`，重点显示视频文件*

**用户：**“我每月新增多少存储空间？”
**AI：** *运行 `storage_analyzer.py`，报告最近的增长情况*

---

### 5. 时间线摘要

为任意日期范围生成照片活动的叙述性总结。将照片按事件分组，并包含人物、地点和场景等背景信息。

```bash
python3 scripts/timeline_recap.py --start-date YYYY-MM-DD [--end-date YYYY-MM-DD] [--narrative]
```

**选项：**
- `--start-date` — 开始日期（必填）
- `--end-date` — 结束日期（可选，默认为当前日期）
- `--cluster-hours N` — 将相邻照片视为独立事件的小时间隔（默认值：4小时）
- `--narrative` — 以叙述性文本输出，而非JSON
- `--output FILE` — 将结果写入文件

**生成内容：**
- 每天的照片活动记录
- 将相邻照片分组
- 每个事件中出现的人物
- 场景分类（如海滩、日落、狗狗等）
- 可用的位置数据

**示例输出：**
```
📅 PHOTO TIMELINE RECAP
==================================================

Period: 2025-03-01 to 2025-03-07
Total: 156 photos across 5 days
Events: 12

📆 2025-03-01 (Saturday) - 45 photos

  🕐 09:15 (2h 15m)
     32 photos, 2 videos ⭐ 5 favorites
     👥 Jonah, Silas
     🏷️  swimming, pool, sports
     📍 41.5369, -90.5776

  🕐 18:30 (45m)
     13 photos
     👥 Jonah, Silas
     🏷️  dinner, food, family
```

**对话示例：**
**用户：**“我上周做了什么？”
**AI：** *运行 `timeline_recap.py`，使用上周的日期，以故事形式讲述时间线*

**用户：**“显示我2月的照片活动”
**AI：** *运行 `timeline_recap.py`，使用2月1日至28日的日期，总结关键事件*

**AI提示：** 在展示时间线结果时，要用故事的方式讲述！不要直接输出JSON。例如：**

> “3月1日你非常忙碌！早上9:15左右，你在泳池待了大约2小时，拍摄了32张照片，主要是乔纳和西拉斯的照片，大部分是游泳和运动的场景。你给其中5张照片设置了收藏。晚上6:30左右，你拍摄了13张家庭晚餐的照片。”**

---

### 6. 智能导出

按年份/月份、人物、相册或地点规划有序的导出方案。显示导出内容，但不会实际执行导出操作（除非用户确认）。

**选项：**
- `--output-dir PATH` — 导出路径（必填）
- `--organize-by MODE` — 导出方式（默认值：按年份/月份）
- `--favorites` — 仅导出收藏的照片
- `--start-date YYYY-MM-DD` — 按开始日期过滤
- `--end-date YYYY-MM-DD` — 按结束日期过滤
- `--person NAME` **仅导出与此人相关的照片**
- `--album NAME` **仅从指定相册导出**
- `--plan-only` **仅显示导出计划（建议先查看计划）**

**示例输出：**
```
📤 EXPORT PLAN
==================================================
Organization: year_month
Total photos: 3,456
Total size: 15.2 GB
Folders: 36

Folders:
  2025/01-January/
    123 items, 542 MB
  2025/02-February/
    156 items, 687 MB
  2025/03-March/
    89 items, 398 MB
  ...
```

**注意：** 实际的导出操作需要通过AppleScript完成。此命令仅生成导出计划和文件夹结构。目前可以先使用它来确定要导出的内容，然后再在Photos应用程序中手动执行导出。**

**对话示例：**
**用户：**“我想按月份整理2024年的所有照片”
**AI：** *运行 `smart_export.py`，使用年份参数和 `--plan-only` 选项，显示导出计划*

**用户：**“导出所有与乔纳相关的照片”
**AI：** *运行 `smart_export.py`，使用 `--person "Jonah"` 和 `--plan-only` 选项，显示导出内容*

---

### 7. 最佳照片/隐藏珍品

利用苹果计算的质量评分，突出显示高质量的照片。找出你尚未收藏的隐藏珍品。

**选项：**
- `--min-quality N` — 最低质量评分阈值（默认值：0.7，范围：0.0-1.0）
- `--top N` — 返回的最佳照片数量（默认值：50张）
- `--hidden-gems` **仅显示未收藏的照片**
- `--year YYYY` **按年份过滤**
- `--human` **以人类可读的格式输出摘要**
- `--output FILE` **将结果写入文件**

**显示内容：**
- 照片库中的质量评分分布（优秀/良好/一般/较差）
- 按质量排名前N张的照片及其详细评分
- 隐藏的珍品：尚未收藏的高质量照片
- 每张照片的评分细节（构图、光线、对称性等）

**示例输出：**
```
⭐ BEST PHOTOS / HIDDEN GEMS
==================================================

Photos with quality scores: 11,234
Above threshold (0.7): 2,456
Hidden gems (great but not favorited): 2,100
Already favorited high-quality: 356

Quality Distribution:
  🌟 Excellent (≥0.85): 456
  ✅ Good (≥0.70):      2,000
  📊 Average (≥0.50):   5,234
  📉 Below avg (≥0.30): 2,544
  ❌ Poor (<0.30):       1,000

Top 20 Photos:
    1. IMG_1234.jpg
       Q:0.952 | 4.2 MB | 4032x3024 💎
       📐 composition:0.95, lighting:0.92, symmetry:0.88
```

**对话示例：**
**用户：**“展示我的最佳照片”
**AI：** *运行 `best_photos.py`，使用 `--human` 选项，突出显示最佳照片*

**用户：**“找出我尚未收藏的隐藏珍品”
**AI：** *运行 `best_photos.py`，使用 `--hidden-gems` 选项，建议收藏哪些照片*

**用户：**“2025年我的最佳照片是什么？”
**AI：** *运行 `best_photos.py`，使用 `--year 2025` 选项，显示质量评分和最佳照片**

---

### 8. 人物分析

深入分析照片中出现的人物：谁出现得最多、谁经常一起出现、随时间的变化趋势，以及每个人的最佳照片。

**选项：**
- `--min-photos N** — 包含某人的最低照片数量（默认值：5张）
- **--top N** **详细分析的最多人物数量（默认值：20人）**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- 按照片数量排名的人物列表
- 每人每年的拍摄频率变化
- 经常一起出现的人物
- 每人的最佳照片

**示例输出：**
**用户：**“我的照片中谁出现得最多？”
**AI：** *运行 `people_analyzer.py`，报告出现次数最多的人物*

**用户：**“我和谁一起拍摄的照片最多？”
**AI：** *运行 `people_analyzer.py`，重点分析共同出现的场景*

---

### 9. 位置/出行映射**

分析照片的拍摄地点。将GPS坐标聚类到具体位置，识别出行记录，并显示拍摄次数最多的地点。

**选项：**
- `--radius N` — 聚类半径（以公里为单位，默认值：1.0）
- **year YYYY** **按年份过滤**
- **--min-photos N** **每个位置聚类的最低照片数量（默认值：3张）**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- GPS覆盖百分比
- 拥有照片的位置聚类、日期范围和人物信息
- 识别出的出行记录（包含拍摄时间超过4小时的聚类）
- 每个位置的月度统计

**示例输出：**
**用户：**“我在哪里拍摄的照片最多？”
**AI：** *运行 `locationmapper.py`，报告拍摄次数最多的地点*

**用户：** **显示2025年的出行记录**
**AI：** *运行 `locationmapper.py`，使用 `--year 2025` 选项，突出显示出行记录*

---

### 10. 场景/内容搜索**

根据机器学习识别的场景（如海滩、日落、狗狗、食物等）搜索照片，或生成完整的照片清单。

**选项：**
- **--search TERM** **要搜索的场景名称**（用于内容清单）
- **--min-confidence N** **最低置信度阈值（默认值：0.0）**
- **--top N** **搜索结果数量（默认值：50张）**
- **--year YYYY** **按年份过滤**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**模式：**
1. **搜索模式** (`--search beach`) — 查找所有符合指定场景标签的照片
2. **清单模式** (`--search` 不使用） — 显示所有场景标签及其数量

**示例输出（清单模式）：**
```
🏷️  SCENE / CONTENT SEARCH
==================================================

Unique scene labels: 234
Scene-tagged entries: 45,678
Library total: 12,453

By Category:
  📂 Nature Outdoor (5,678 photos)
    beach: 234
    sunset: 189
    mountain: 156
  📂 Animals (2,345 photos)
    dog: 1,234
    cat: 567
  📂 Food Drink (1,890 photos)
    food: 890
    coffee: 234
```

**对话示例：**
**用户：**“我有多少张海滩照片？”
**AI：** *运行 `scene_search.py --search beach`，报告海滩照片的数量和相关场景*

**用户：**“我拍摄的是什么类型的照片？”
**AI：** *运行 `scene_search.py`（清单模式），总结照片类别*

---

### 11. 照片习惯与洞察**

分析拍摄习惯：何时拍摄最多、最繁忙的日子、季节性拍摄模式、拍摄频率的规律性。

**选项：**
- **--year YYYY** **按年份过滤**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- 一天中的不同时间（上午/下午/晚上/夜晚）
- 每周的繁忙时段
- 每月的拍摄频率分布
- 最长的连续拍摄天数
- 年度间的拍摄趋势（照片与视频的对比）

**示例输出：**
```bash
python3 scripts/photo_habits.py [--year YYYY] [--human]
```

**对话示例：**
**用户：**“我的拍摄习惯是什么？”
**AI：** *运行 `photo_habits.py`，讲述关键拍摄习惯*

**用户：** **我什么时候拍摄的照片最多？**
**AI：** *运行 `photo_habits.py`，突出显示拍摄高峰期**

---

### 12. 今日回顾 / 回忆录**

查看过去几年中你在今天拍摄的照片。包括人物、场景和照片质量信息。

**选项：**
- **--date YYYY-MM-DD** **目标日期（默认为当前日期）**
- **--window N** **包含目标日期前后N天的照片（默认值：0）**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- 过去几年中同一天的照片
- 每年的照片、人物和最佳照片
- 每年的收藏数量

**示例输出：**
**用户：** **去年3月3日我做了什么？**
**AI：** *运行 `on_this_day.py`，讲述当年的故事*

**AI提示：** 在讲述回忆时要有温度！例如：“两年前的今天，你在泳池和乔纳、西拉斯一起，拍摄了12张照片，其中3张被设置了收藏，最佳照片的质量评分为0.89！”**

---

### 13. 相册审核**

找出孤立的照片（不在任何相册中）、空相册、照片数量过少的相册以及重复的照片。

**选项：**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- 孤立照片的数量（不在任何相册中）
- 可以删除的空相册
- 照片数量过少的相册（≤3张）
- 相册之间的重复照片（以及重复比例）

**示例输出：**
```bash
python3 scripts/album_auditor.py [--human]
```

**对话示例：**
**用户：****“我的照片组织得怎么样？”
**AI：** *运行 `album_auditor.py`，报告孤立照片、空相册和重复照片的情况*

**用户：** **有多少张照片不在任何相册中？**
**AI：** *运行 `album_auditor.py`，报告孤立照片的数量和类型*

---

### 14. 清理执行器**

通过AppleScript实际将垃圾照片移至“最近删除”文件夹。支持删除旧截图、未选择的连拍照片、低质量照片和重复照片。所有文件都会被移至“最近删除”文件夹（可恢复30天）。

**选项：**
- **--category** **要清理的文件类型**：`old_screenshots`、`all_screenshots`、`burst_leftovers`、`low_quality`、`duplicates`
- **--screenshot-age N** **旧截图的年龄（以天为单位）（默认值：30天）**
- **--quality-threshold N** **低质量照片的阈值（默认值：0.3）**
- **--limit N** **处理的文件数量上限（默认值：500张）**
- **--execute** **实际执行清理操作（不使用此选项时仅显示预览）**
- **--batch-size N** **每个AppleScript批处理的文件数量（默认值：50张）**
- **--human** **以人类可读的格式输出摘要**

**安全提示：**
- 不使用 `--execute` 选项时，仅显示预览结果
- 使用 `--execute` 选项时，需要用户确认
- 文件会被移至“最近删除”文件夹（可恢复30天）
- 通过Photos应用程序使用AppleScript执行操作（不会直接修改数据库）

**示例用法：**
**用户：****“删除我的旧截图”**
**AI：** *运行 `cleanupexecutor.py --category old_screenshots`，首先显示预览结果，然后提示用户确认*

**用户：****“清理未选择的连拍照片”**
**AI：** *运行 `cleanupexecutor.py --category burst_leftovers`，显示数量和大小，然后请求用户确认*

**⚠️ AI提示：** 总要先显示预览结果！切勿在未显示预览结果的情况下直接执行删除操作！**

---

### 15. 实时照片分析**

分析实时照片与普通照片的区别：识别实时照片，比较两者对存储空间的影响，找出可以转换为普通照片以节省空间的实时照片。

**选项：**
- **--year YYYY** **按年份过滤**
- **--human** **以人类可读的格式输出摘要**
- **--output FILE** **将结果写入文件**

**显示内容：**
- 实时照片与普通照片的总数（数量和存储空间占用）
- 播放方式（实时/循环/抖动/长时间曝光）
- 实时照片的年度变化趋势
- 如果将实时照片转换为普通照片，预计可以节省的存储空间（约50%的视频部分）
- 未收藏的实时照片（建议转换的对象）

---

### 16. 共享照片库分析**

分析苹果照片中的共享照片库：个人照片与共享照片的对比、贡献者分布以及存储空间使用情况。

**显示内容：**
- 共享照片库是否启用
- 个人照片与共享照片的数量和存储空间使用情况
- 贡献者的身份及其贡献
- 共享照片按年份和月份的分布

**注意：** 需要macOS 13+ / iOS 16+系统及相应的数据库格式才能使用共享照片库功能。

---

### 17. iCloud同步状态**

检查照片库的iCloud同步情况：区分已同步和仅保存在本地的数据、未同步的大文件。

**显示内容：**
- 同步覆盖百分比（已同步与仅保存在本地的数据）
- 按同步状态划分的存储空间使用情况
- 照片与视频的同步情况对比
- 年度间的同步趋势
- 未同步的大文件（大于10MB）

---

### 18. 照片相似性检测**

利用计算出的质量特征向量（构图、光线、颜色等）识别视觉上相似的照片（不仅仅是完全重复的照片）。

**选项：**
- **--threshold** **余弦相似度阈值（0-1，范围：0.95，非常相似）**
- **--year YYYY** **按年份过滤**
- **--limit N** **比较的最大照片数量（默认值：500张，用于控制运行时间）**
- **--human** **以人类可读的格式输出摘要**

**显示内容：**
- 相似照片的组别
- 每组照片的潜在存储节省空间
- 每组中保留的照片（最大/质量最高的）

**运行时间提示：** 相似性检测的计算复杂度为O(n²)；使用 `--limit` 选项可以控制大型数据库的运行时间**

---

### 19. 季节性最佳照片**

根据质量评分、收藏情况和场景信息，挑选每个季节的最佳照片。

**选项：**
- **--year YYYY** **按年份过滤**
- **--top N** **每个季节的最佳照片数量（默认值：20张）**
- **--southern** **使用南半球的季节定义**

**显示内容：**
- 每个季节的最佳照片
- 每季节的质量评分和收藏数量
- 季节间的对比
- 最繁忙的季节

---

### 20. 人脸质量评分**

利用苹果照片应用程序的人脸识别功能，对每个人的脸部质量进行评分。

**选项：**
- **--person NAME** **按具体人物名称过滤**
- **--top N** **每个人的最佳/最差照片数量（默认值：10张）**
- **--human** **以人类可读的格式输出摘要**

**显示内容：**
- 每个人的人脸质量排名
- 每人的最佳/最差照片
- 综合人脸质量评分（构图、光线、模糊度、角度、中心位置等）

**显示内容：**
- 每个人的人脸质量排名
- 最佳和最差的照片

## 数据库架构参考

详细数据库架构文档位于 `references/database-schema.md`。主要表格包括：
- **ZASSET** — 主要照片/视频表格
- **ZADDITIONALASSETATTRIBUTES** — 文件大小和尺寸信息
- **ZCOMPUTEDASSETATTRIBUTES** — 苹果计算的质量评分
- **ZPERSON** — 识别出的人物
- **ZDETECTEDFACE** — 识别出的人脸
- **ZGENERICALBUM** — 相册信息
- **ZSCENECLASSIFICATION** — 机器学习识别的场景标签

**重要提示：** 核心数据的时间戳是从2001-01-01开始的秒数，而非Unix纪元。

## 常见工作流程

### 工作流程1：快速清理评估

```bash
# Get overview
python3 scripts/library_analysis.py --human

# Find junk
python3 scripts/junk_finder.py --human

# Review and manually clean up in Photos.app
```

### 工作流程2：释放存储空间

```bash
# Analyze storage
python3 scripts/storage_analyzer.py --human

# Find duplicates
python3 scripts/duplicate_finder.py --human

# Find junk with aggressive settings
python3 scripts/junk_finder.py --screenshot-age 14 --quality-threshold 0.4 --human

# Use findings to guide cleanup
```

### 工作流程3：年度照片回顾

```bash
# Generate timeline for the year
python3 scripts/timeline_recap.py --start-date 2024-01-01 --end-date 2024-12-31 --narrative

# Get storage stats by year
python3 scripts/storage_analyzer.py | jq '.by_year'

# Get top people for the year
python3 scripts/library_analysis.py | jq '.top_people'

# Photo habits for the year
python3 scripts/photo_habits.py --year 2024 --human

# Best photos of the year
python3 scripts/best_photos.py --year 2024 --top 20 --human
```

### 工作流程4：有序导出存档

```bash
# Plan export
python3 scripts/smart_export.py --output-dir ~/Desktop/Photos-Export --favorites --start-date 2024-01-01 --plan-only

# Review plan, then execute (manual for now)
```

### 工作流程5：深度清理

```bash
# Find all junk
python3 scripts/junk_finder.py --human

# Preview old screenshots
python3 scripts/cleanup_executor.py --category old_screenshots --human

# Execute cleanup (with confirmation)
python3 scripts/cleanup_executor.py --category old_screenshots --execute

# Clean burst leftovers
python3 scripts/cleanup_executor.py --category burst_leftovers --execute

# Check album health
python3 scripts/album_auditor.py --human
```

### 工作流程6：每日照片检查

```bash
# See what happened on this day in past years
python3 scripts/on_this_day.py --human

# With a wider window
python3 scripts/on_this_day.py --window 2 --human
```

### 工作流程7：位置与出行分析

```bash
# See all your locations
python3 scripts/location_mapper.py --human

# Focus on trips from a specific year
python3 scripts/location_mapper.py --year 2025 --human

# What content you shot at those places
python3 scripts/scene_search.py --human
```

### 工作流程8：人物深度分析

```bash
# Who's in your photos
python3 scripts/people_analyzer.py --human

# Find hidden gems of specific people
python3 scripts/best_photos.py --hidden-gems --human

# Best and worst portraits per person
python3 scripts/face_quality.py --human
```

### 工作流程9：实时照片与存储优化

```bash
# Analyze Live Photos vs stills
python3 scripts/live_photo_analyzer.py --human

# Find similar photos (potential duplicates)
python3 scripts/similarity_finder.py --threshold 0.95 --human

# Check iCloud sync status
python3 scripts/icloud_status.py --human
```

### 工作流程10：季节性回顾

```bash
# Get seasonal highlights
python3 scripts/seasonal_highlights.py --year 2024 --human

# Location review with place names
python3 scripts/location_mapper.py --year 2024 --human

# Photo habits for the year
python3 scripts/photo_habits.py --year 2024 --human
```

### 工作流程11：共享照片库审核

```bash
# Check shared library status
python3 scripts/shared_library.py --human

# See who contributed what and storage impact
python3 scripts/shared_library.py --output shared_report.json
```

## 为AI助手提供的建议

### 当用户询问照片清理时：

1. **先进行分析** — 运行 `library_analysis.py` 以了解照片库情况
2. **查找需要清理的文件** — 运行 `junk_finder.py` 以量化清理需求
3. **具体说明** — 不要只是说“你有垃圾照片”，要说明“你有287张超过30天的截图（占2.1GB，可以删除）”
4. **说明节省的空间** — 始终提及预计的存储空间节省量
5. **指导用户使用Photos应用程序** — 脚本会识别需要清理的文件，但用户必须通过Photos应用程序进行删除

### 当用户询问“我上周做了什么？”时：

1. **使用时间线摘要** — 非常适合讲述照片活动
2. **用故事的形式讲述** — 将JSON数据转化为生动的故事
3. **突出显示收藏的照片** — 提及重要的时刻
4. **使用表情符号** — 使信息更有趣

### 当用户询问存储空间使用情况时：

1. **运行 `storage_analyzer` **获取最全面的分析结果**
2. **识别占用大量存储空间的文件** — 强调占用最大的文件或文件类型
3. **展示趋势** **“你每月大约增加了1.5GB的存储空间”
4. **建议采取的行动** **“删除旧截图可以释放2GB的存储空间”

### 当用户询问最佳/收藏的照片时：

1. **使用 `best_photos` **查看照片的质量分布和最佳照片**
2. **找出隐藏的珍品** **使用 `--hidden-gems` 选项找出未收藏的高质量照片**
3. **解释评分标准** **说明什么因素决定了照片的质量**

### 当用户询问人物信息时：

1. **使用 `people_analyzer` **进行全面分析**
2. **展示人物出现的频率** **“乔纳和西拉斯一起出现了2100次”
3. **展示趋势** **“2025年你和乔纳一起拍摄的照片减少了40%”**

### 当用户询问“今天发生了什么？”或“回忆录”时：

1. **使用 `on_this_day` **非常适合回顾过去**
2. **用故事的形式讲述** **生动地讲述每个日期的回忆**
3. **建议使用 `--window` **如果找不到相关内容，建议使用 `--window 2` 查看附近的日期**

### 当用户希望实际执行删除操作时：

1. **始终先预览** **运行 `cleanupexecutor` 时不要直接执行删除**
2. **显示文件数量和大小** **“287张旧截图，占2.1GB的存储空间”
3. **解释安全措施** **文件会被移至“最近删除”文件夹，可恢复30天**
4. **获取用户确认** **切勿自动执行删除操作**

### 输出格式说明

**JSON输出：** 适用于程序化操作，包含所有详细信息

**人类可读输出：** 使用 `--human` 选项可获取易于理解的摘要

**对话时的使用方式：** 将数据以自然语言的形式呈现给用户，而不仅仅是直接读取输出结果**

## 系统要求**

- **Python版本**：3.9及以上（测试版本为3.13）
- **平台**：仅支持macOS（使用苹果照片数据库）
- **依赖库**：无（仅使用Python标准库）
- **数据库访问权限**：仅允许读取 `~/Pictures/Photos Library.photoslibrary/database/Photos.sqlite` 文件

## 安全性与权限设置

- ✅ **所有操作均为只读** — 不会修改或删除任何照片
- ✅ **无外部依赖** — 仅使用Python标准库
- ✅ **不使用Photos应用程序的API** — 仅通过SQLite读取数据（安全）
- ⚠️ **智能导出功能需要Photos应用程序运行** — 需要Photos应用程序处于开启状态
- ⚠️ **清理操作需要使用AppleScript** — 文件会被移至“最近删除”文件夹（可恢复）

## 限制事项**

- **仅限读取分析** — 脚本会识别需要清理的文件，但用户必须确认删除操作
- **导出操作需要通过AppleScript** — 需要Photos应用程序运行
- **反向地理编码** — 支持识别大约100个主要城市的地点；远程地点仅显示坐标
- **相似性检测** **使用计算出的质量向量（非像素级）；`--limit` 选项用于控制处理大型数据库时的运行时间**
- **共享照片库功能** **需要macOS 13+ / iOS 16+系统及相应的数据库格式**
- **空相册支持** **脚本可以处理任何照片库，但Matt的Mac mini上的照片库为空（数据已同步到其他位置）**
- **数据库架构可能更新** **苹果未来可能会修改数据库架构**

## 故障排除**

- **“找不到数据库”** → 使用 `--library ~/Path/To/Photos Library.photoslibrary` 指定正确的路径
- **“权限被拒绝”** → 先关闭Photos应用程序，或在Photos应用程序运行时执行脚本（只读操作是安全的）
- **“没有质量评分”** **并非所有照片都包含质量评分信息；脚本会优雅地处理空值**
- **结果与Photos应用程序的统计结果不一致** **脚本会排除已删除的文件；Photos应用程序可能显示不同的数据**

## 未来改进计划

所有已计划的特性均已实现！未来可能的功能包括：
- 用于自定义照片分类的机器学习模型
- 在多个照片库之间进行照片去重
- 与外部照片服务（如Google Photos、Flickr）集成
- 从照片序列生成延时视频
- 自定义的智能相册规则生成器
- 照片元数据的修复/批量编辑建议

---

**总结：** 本工具可以帮助你深入了解你的照片库。利用它来了解你的照片资源，找出不需要保留的照片，并自信地做出清理决策。
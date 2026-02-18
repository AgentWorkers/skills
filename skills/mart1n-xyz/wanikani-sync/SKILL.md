---
name: wanikani-sync
description: 将 WaniKani 的日语学习进度数据从 API 同步到本地存储，以便进行分析和获取洞察。当用户需要备份他们的学习进度、生成学习统计信息、分析复习模式、跟踪学习水平的变化或离线访问 WaniKani 数据时，可以使用该功能。该系统支持增量同步以减少 API 调用次数，并将数据存储在 SQLite 中，便于查询。
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - WANIKANI_API_TOKEN
      bins:
        - python3
    primaryEnv: WANIKANI_API_TOKEN
    emoji: 🈴
    homepage: https://www.wanikani.com
---
# WaniKani 同步

将您的 WaniKani 进度数据同步到本地，以便进行分析和生成报表。

## 概述

本技能提供了通过 API 获取您的 WaniKani 学习进度并将其存储到本地 SQLite 数据库的工具。同步完成后，您或其他服务可以查询这些数据来生成统计报告、跟踪学习模式、可视化学习进度等。

## 获取 API 令牌

1. 登录 [WaniKani](https://www.wanikani.com)
2. 转到 [设置 → API 令牌](https://www.wanikani.com/settings/personal_access_tokens)
3. 生成一个新的令牌（或使用现有的令牌）
4. 复制令牌（令牌通常是一个长字符串，包含字母和数字）

**安全提示：** 请妥善保管您的令牌，切勿将其提交到 Git 或公开分享。

## 快速入门

### 同步所有数据

```bash
# Using environment variable (recommended)
export WANIKANI_API_TOKEN="your-token-here"
python3 scripts/sync.py

# Or pass token directly (less secure)
python3 scripts/sync.py --token "your-token-here"

# Store in specific directory
python3 scripts/sync.py --data-dir ~/wanikani-data
```

### 同步特定数据

```bash
# Only user info
python3 scripts/sync.py --user-only

# Only assignments (your progress on subjects)
python3 scripts/sync.py --assignments-only

# Only reviews
python3 scripts/sync.py --reviews-only
```

### 强制全量同步

默认情况下，脚本会进行增量同步（仅获取自上次同步以来更新的数据）。要强制进行全量刷新，请执行以下操作：

```bash
python3 scripts/sync.py --full
```

## 数据库架构

同步操作会创建一个名为 `wanikani.db` 的 SQLite 数据库，其中包含以下表格：

### `user`  
包含您的账户信息，如等级、订阅状态和开始学习的时间。

### `assignments`  
记录您在每个科目（ radicals、kanji、vocabulary）上的学习进度，以及 SRS 学习阶段的更新时间。

### `level_progressions`  
记录您在 WaniKani 各等级中的学习历程，包括解锁、开始、通过和完成的时间戳。

### `reviews`  
记录您的复习历史，包括正确答案的数量和 SRS 学习阶段的变更。

### `review_statistics`  
按科目汇总的统计数据（正确/错误答案的数量、连续正确答案的数量、正确率等）。

### `resets`  
记录账户重置的历史记录。

### `subjects`  
包含实际的学习内容（kanji、vocabulary、radicals），包括汉字、含义、读音和记忆方法。

**同步科目数据的方法：**
```bash
# Sync all subjects (can be large!)
python3 scripts/sync.py --subjects-only

# Sync only specific levels (recommended)
python3 scripts/sync.py --with-subjects --subject-levels 1,2,3,4,5

# Include subjects in full sync
python3 scripts/sync.py --with-subjects
```

### `sync_meta`  
用于跟踪上次同步的时间戳，以便进行增量更新。

## 常见查询

```sql
-- Current SRS stage distribution
SELECT srs_stage, COUNT(*) FROM assignments GROUP BY srs_stage;

-- Items burned per level
SELECT level, COUNT(*) FROM assignments WHERE burned_at IS NOT NULL GROUP BY level;

-- Average accuracy by subject type
SELECT subject_type, AVG(percentage_correct) FROM review_statistics GROUP BY subject_type;

-- Reviews done in last 7 days
SELECT DATE(created_at) as day, COUNT(*) FROM reviews
WHERE created_at > datetime('now', '-7 days') GROUP BY day;

-- Time spent at each level
SELECT level, started_at, passed_at,
       CASE WHEN passed_at IS NOT NULL
            THEN julianday(passed_at) - julianday(started_at)
            ELSE NULL END as days_to_pass
FROM level_progressions WHERE started_at IS NOT NULL;

-- Most problematic items (with subject characters)
SELECT 
    s.characters,
    s.object as type,
    rs.meaning_incorrect + rs.reading_incorrect as fails,
    rs.percentage_correct as accuracy
FROM review_statistics rs
JOIN subjects s ON rs.subject_id = s.id
WHERE rs.percentage_correct < 75
ORDER BY fails DESC
LIMIT 20;

-- Current leeches (Apprentice stage, failing often, with kanji)
SELECT 
    s.characters,
    s.object as type,
    a.srs_stage,
    rs.meaning_incorrect + rs.reading_incorrect as total_fails,
    rs.percentage_correct
FROM review_statistics rs
JOIN assignments a ON rs.subject_id = a.subject_id
JOIN subjects s ON rs.subject_id = s.id
WHERE a.srs_stage BETWEEN 1 AND 4
  AND rs.percentage_correct < 80
ORDER BY total_fails DESC
LIMIT 15;
```

## API 注意事项

- 请求速率限制：每分钟 60 次请求
- 所有 API 请求均使用版本 `20170710`
- 增量同步会使用 `updated_after` 过滤器来减少 API 调用次数
- 有关完整的 API 端点文档，请参阅 `references/api-structure.md`

## 查询工具

同步完成后，可以使用查询工具来生成常见的报告：

```bash
# Show your worst leeches (items that keep falling back)
python3 scripts/queries.py leeches

# Show SRS distribution (Apprentice/Guru/Master/etc counts)
python3 scripts/queries.py srs

# Show level progression timeline
python3 scripts/queries.py levels

# Show critical items at risk of falling back
python3 scripts/queries.py critical

# Show accuracy by subject type
python3 scripts/queries.py accuracy
```

请参阅 `references/example-queries.sql`，其中包含可以直接在数据库上运行的 SQL 语句示例。

## 相关文件

- `scripts/sync.py` - 主同步工具（支持命令行界面）
- `scripts/queries.py` - 用于生成常见报告的查询工具
- `references/api-structure.md` - WaniKani API 参考文档
- `references/example-queries.sql` - SQL 查询示例
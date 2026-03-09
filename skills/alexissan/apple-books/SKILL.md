---
name: apple-books
description: 您可以直接从 macOS 上的本地 SQLite 数据库中读取 Apple Books 图书库中的内容、高亮标记、笔记以及阅读进度。
homepage: https://clawhub.ai/alexissan/apple-books
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["sqlite3"],"os":"darwin"}}}
---
# Apple Books

在 macOS 上查询您本地的 Apple Books 图书库。可以读取书籍、高亮标记、笔记、收藏夹以及阅读进度等信息。

## 要求

- **仅限 macOS** — Apple Books 将数据存储在 `~/Library/Containers/com.apple.iBooksX/` 目录下。
- 运行查询时需要 **完全的磁盘访问权限**（系统设置 → 隐私与安全 → 完全磁盘访问）。
- 系统已预装 `sqlite3` 数据库引擎。
- Apple Books 必须至少被打开过一次（数据库会在首次启动时创建）。

## 数据库查找

虽然不同 macOS 安装版本的数据库文件名可能有所不同，但系统会动态解析这些文件名，以应对未来版本可能发生的变更：

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
```

如果这两个变量都为空，说明该 Mac 上尚未设置 Apple Books。

> **重要提示：** 这些操作均为只读操作，严禁插入（INSERT）、更新（UPDATE）或删除（DELETE）数据，否则可能会导致 Apple Books 数据损坏或 iCloud 同步问题。

## 列出所有书籍

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE, ZPAGECOUNT, ZREADINGPROGRESS, ZISFINISHED, ZASSETID
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL
   ORDER BY ZLASTOPENDATE DESC;"
```

## 按书名或作者搜索书籍

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE, ZREADINGPROGRESS, ZASSETID
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL AND (ZTITLE LIKE '%SEARCH_TERM%' OR ZAUTHOR LIKE '%SEARCH_TERM%')
   ORDER BY ZLASTOPENDATE DESC;"
```

请将 `SEARCH TERM` 替换为用户的查询内容。

## 当前正在阅读的书籍（未读完）

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE,
          printf('%.0f%%', ZREADINGPROGRESS * 100) AS progress,
          datetime(ZLASTOPENDATE + 978307200, 'unixepoch', 'localtime') AS last_opened
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL
     AND ZREADINGPROGRESS > 0.0
     AND (ZISFINISHED IS NULL OR ZISFINISHED = 0)
   ORDER BY ZLASTOPENDATE DESC;"
```

## 已读完的书籍

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT ZTITLE, ZAUTHOR, ZGENRE,
          datetime(ZDATEFINISHED + 978307200, 'unixepoch', 'localtime') AS finished_date
   FROM ZBKLIBRARYASSET
   WHERE ZISFINISHED = 1
   ORDER BY ZDATEFINISHED DESC;"
```

## 获取特定书籍的所有高亮标记和笔记

```bash
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$AEANNOTATION_DB" \
  "SELECT ZANNOTATIONSELECTEDTEXT, ZANNOTATIONNOTE, ZANNOTATIONSTYLE,
          datetime(ZANNOTATIONCREATIONDATE + 978307200, 'unixepoch', 'localtime') AS created
   FROM ZAEANNOTATION
   WHERE ZANNOTATIONDELETED = 0
     AND ZANNOTATIONASSETID = 'ASSET_ID'
     AND length(ZANNOTATIONSELECTEDTEXT) > 0
   ORDER BY ZPLLOCATIONRANGESTART ASC;"
```

请将 `ASSET_ID` 替换为从图书库查询中获得的书籍的 `ZASSETID`。

## 获取所有书籍中的高亮标记（附带书籍标题）

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
AEANNOTATION_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/AEAnnotation/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$AEANNOTATION_DB" \
  "ATTACH DATABASE '$BKLIBRARY_DB' AS lib;
   SELECT lib.ZBKLIBRARYASSET.ZTITLE, lib.ZBKLIBRARYASSET.ZAUTHOR,
          ZAEANNOTATION.ZANNOTATIONSELECTEDTEXT, ZAEANNOTATION.ZANNOTATIONNOTE,
          datetime(ZAEANNOTATION.ZANNOTATIONCREATIONDATE + 978307200, 'unixepoch', 'localtime') AS created
   FROM ZAEANNOTATION
   JOIN lib.ZBKLIBRARYASSET ON ZAEANNOTATION.ZANNOTATIONASSETID = lib.ZBKLIBRARYASSET.ZASSETID
   WHERE ZAEANNOTATION.ZANNOTATIONDELETED = 0
     AND length(ZAEANNOTATION.ZANNOTATIONSELECTEDTEXT) > 0
   ORDER BY ZAEANNOTATION.ZANNOTATIONCREATIONDATE DESC
   LIMIT 50;"
```

## 列出所有收藏夹（书架）

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT c.ZTITLE, c.ZCOLLECTIONID, COUNT(m.Z_PK) AS book_count
   FROM ZBKCOLLECTION c
   LEFT JOIN ZBKCOLLECTIONMEMBER m ON m.Z_PK IN (
     SELECT Z_PK FROM ZBKCOLLECTIONMEMBER
   )
   WHERE c.ZDELETEDFLAG = 0 AND c.ZTITLE IS NOT NULL
   GROUP BY c.ZCOLLECTIONID
   ORDER BY c.ZTITLE;"
```

## 阅读统计信息

```bash
BKLIBRARY_DB="$(ls ~/Library/Containers/com.apple.iBooksX/Data/Documents/BKLibrary/*.sqlite 2>/dev/null | head -1)"
sqlite3 "$BKLIBRARY_DB" \
  "SELECT
     COUNT(*) AS total_books,
     SUM(CASE WHEN ZISFINISHED = 1 THEN 1 ELSE 0 END) AS finished,
     SUM(CASE WHEN ZREADINGPROGRESS > 0 AND (ZISFINISHED IS NULL OR ZISFINISHED = 0) THEN 1 ELSE 0 END) AS in_progress,
     SUM(CASE WHEN ZREADINGPROGRESS = 0 OR ZREADINGPROGRESS IS NULL THEN 1 ELSE 0 END) AS not_started,
     printf('%.0f%%', AVG(ZREADINGPROGRESS) * 100) AS avg_progress
   FROM ZBKLIBRARYASSET
   WHERE ZTITLE IS NOT NULL;"
```

## 注释样式

| 样式值 | 颜色     |
|-------------|-----------|
| 1           | 绿色     |
| 2           | 蓝色      |
| 3           | 黄色    |
| 4           | 粉色      |
| 5           | 紫色    |

## 注释类型

| 类型值 | 含义     |
|------------|-------------|
| 2          | 高亮标记   |
| 3          | 书签    |

## 日期处理

Apple Books 使用 Core Data 的时间戳（自 2001-01-01 起的秒数）。若需将其转换为人类可读的格式，请参考以下代码：

```sql
datetime(TIMESTAMP_COLUMN + 978307200, 'unixepoch', 'localtime')
```

## 故障排除

- **“无法打开数据库文件”**：请在系统设置 → 隐私与安全 → 完全磁盘访问中为相关进程授予完全的磁盘访问权限。
- **查询结果为空**：请至少打开一次 Apple Books，以便 macOS 创建数据库。
- **数据过时**：Apple Books 可能在打开时持有写锁；尽管查询仍能在 WAL（Write-Ahead Logging）模式下进行，但数据显示可能会比用户界面滞后几秒。

## 注意事项

- `ZASSETID` 是用于关联书籍与其注释的关键字段。
- `ZREADINGPROGRESS` 是一个介于 0.0 到 1.0 之间的浮点数，表示阅读进度。
- `ZISFINISHED` 的值为 1 表示书籍已读完，否则为 NULL 或 0。
- `ZLASTOPENDATE` 字段记录了书籍最后一次被打开的时间。
- 所有查询操作均为 **只读**，请勿修改这些数据库。
- Apple Books 中的有声书也会显示在该数据库中（`ZISSTOREAUDIOBOOK = 1`）。
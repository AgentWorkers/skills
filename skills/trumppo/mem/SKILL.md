---
name: mem
description: 搜索本地内存索引（优先使用本地数据）。适用于 Telegram 中的 `/mem` 查询。
user-invocable: true
---

# 内存搜索 (/mem)

## 概述

使用缓存的索引进行本地优先的内存搜索。

## 使用方法

1) 如有需要，更新索引：
```bash
scripts/index-memory.py
```

2) 使用用户查询在索引中进行搜索：
```bash
scripts/search-memory.py "<query>" --top 5
```

## 输出结果

返回搜索结果中的前几项及其路径和头部信息。如有需要，可简要进行总结。
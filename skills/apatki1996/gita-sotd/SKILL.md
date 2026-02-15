---
name: gita-sotd
description: >
  Get the Bhagavad Gita Slok of the Day (SOTD) or fetch specific verses.
  Use when the user asks for a Gita verse, slok, daily wisdom from the Gita,
  Hindu scripture quotes, or anything related to the Bhagavad Gita text.
  Supports Sanskrit text, transliteration, and translations from multiple scholars.
---

# 每日《薄伽梵歌》经文

使用免费的 [vedicscriptures API](https://vedicscriptures.github.io/) 获取《薄伽梵歌》中的经文。

## 使用方法

运行脚本以获取某一段经文：

```bash
# Daily slok (deterministic, changes each day)
python3 scripts/fetch_slok.py

# Specific verse
python3 scripts/fetch_slok.py --chapter 2 --verse 47

# Random verse
python3 scripts/fetch_slok.py --random

# Different translator (prabhu, siva, purohit, gambir, chinmay, etc.)
python3 scripts/fetch_slok.py --translator siva

# Raw JSON output
python3 scripts/fetch_slok.py --json
```

## 可用的翻译者

- `prabhu` - A.C. 巴克提维丹塔·斯瓦米·普拉布普达（默认翻译者）
- `siva` - 斯瓦米·西瓦南达
- `purohit` - 斯里·普罗希特·斯瓦米
- `gambir` - 斯瓦米·甘比兰南达
- `chinmay` - 斯瓦米·钦马亚南达
- `tej` - 斯瓦米·特乔马亚南达（印地语翻译）
- `rams` - 斯瓦米·拉姆苏克达斯（印地语翻译）
- `raman` - 斯里·罗摩努贾

## 输出格式

脚本会输出格式化的 Markdown 内容，包括：

- 章节和经文编号
- 梵文原文（可选）
- 拼写转写
- 英文/印地文翻译及作者信息

## API 参考

基础 URL：`https://vedicscriptures.github.io`

- `GET /slok/:chapter/:verse` - 获取特定经文
- `GET /chapter/:ch` - 获取章节信息
- `GET /chapters` - 列出所有章节

《薄伽梵歌》共有 18 章，共计 700 首经文。
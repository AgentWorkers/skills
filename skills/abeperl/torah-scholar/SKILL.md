---
name: torah-scholar
description: 通过 Sefaria API 搜索和探索犹太经典文献（《托拉》《塔纳赫》《塔木德》《米德拉什》及其注释）。适用于研究《托拉》的来源、查找经文、查阅注释、进行交叉引用，或准备《托拉》相关的讲道内容。支持希伯来语和英语输入。能够处理如下类型的引用：“创世记 1:1”、“祝福篇 2a”、“密西拿·阿沃特 1:1”等。
---
# 托拉学者（Torah Scholar）

您可以全面访问Sefaria图书馆中的犹太文本，进行研究，这些文本包括《塔纳赫》（Tanach）、《巴比伦塔木德》（Talmud Bavli/Yerushalmi）、《密西拿》（Mishnah）、《米德拉什》（Midrash）、《佐哈尔》（Zohar）以及数千篇注释。

## 快速入门

```bash
# Search across all texts
torah search "love your neighbor"

# Get specific verse with Hebrew + English
torah verse "Leviticus 19:18"

# Find commentaries on a verse
torah links "Genesis 1:1"

# This week's parsha
torah parsha

# Today's learning schedule (Daf Yomi, etc.)
torah today
```

## 命令

| 命令 | 描述 | 示例 |
|---------|-------------|---------|
| `torah search <查询>` | 全文搜索 | `torah search "tikkun olam"` |
| `torah verse <引用>` | 获取经文及其翻译 | `torah verse "诗篇 23"` |
| `torah links <引用>` | 查看注释和交叉引用 | `torah links "出埃及记 20:1"` |
| `torah related <引用>` | 相关文本和主题 | `torah related "申命记 6:4"` |
| `torah parsha` | 本周的经文段落 | `torah parsha` |
| `torah today` | 每日学习计划 | `torah today` |
| `torah dvar` | 生成托拉解读 | `torah dvar` |
| `torah dvar ref <引用>` | 对特定经文的解读 | `torah dvar ref "创世记 12:1"` |
| `torah dvar theme <主题>` | 以特定主题为中心的解读 | `torah dvar theme "领导力"` |

## 参考格式

### 《塔纳赫》（希伯来圣经）
- 书籍：《创世记》《出埃及记》《利未记》《民数记》《申命记》（托拉部分）
- 其他书籍：《约书亚记》《士师记》《撒母耳记》《列王纪》《以赛亚书》《耶利米书》《以西结书》等
- 格式：`书籍 章节:经文` 或 `书籍 章节:起始-结束`
- 例如：`创世记 1:1`，`诗篇 23`，`以赛亚书 40:1-5`

### 《塔木德》
- 巴比伦塔木德（Babylonian Talmud）：`篇目 编号a` 或 `b`
- 例如：`Berakhot 2a`，`Shabbat 31a`，`Bava Metzia 59b`
- 主要篇目：Berakhot（祝福篇）、Shabbat（安息日篇）、Eruvin（法律篇）、Pesachim（逾越节篇）、Yoma（安息日篇）、Sukkah（住棚节篇）、Beitzah（七七节篇）、Rosh Hashanah（犹太新年篇）、Taanit（禁食篇）、Megillah（读经篇）、Moed Katan（小节期篇）、Chagigah（节日篇）、Yevamot（葬礼篇）、Ketubot（婚姻法篇）、Nedarim（誓约篇）、Nazir（禁食篇）、Sotah（妇女篇）、Gittin（离婚篇）、Bava Kamma（刑罚篇）、Bava Metzia（法律篇）、Bava Batra（民事篇）、Sanhedrin（公议会篇）、Makkot（刑罚篇）、Shevuot（七七节篇）、Avodah Zarah（献祭篇）、Horayot（圣洁篇）、Zevachim（献祭篇）、Menachot（节期篇）、Chullin（洁净篇）、Bekhorot（长子篇）、Arakhin（赎罪祭篇）、Temurah（赎罪祭篇）、Keritot（赎罪祭篇）、Meilah（赎罪祭篇）、Tamid（每日祭篇）、Niddah（洁净篇）

### 《密西拿》
- 格式：`Mishnah 篇目 章节:经文`
- 例如：`Mishnah Avot 1:1`，`Mishnah Berakhot 1:1`

### 《米德拉什》
- Midrash Rabbah：`创世记 Rabbah 1:1`，`出埃及记 Rabbah 1:1`
- Midrash Tanchuma：《塔纳赫注释》（Tanchuma Bereshit 1）
- 其他版本：《Pirkei DeRabbi Eliezer 1`

### 注释
- 可通过 `torah links <引用>` 查看拉什（Rashi）、拉姆班（Ramban）、伊本·以斯拉（Ibn Ezra）等注释家的注释。

## 研究工作流程

### 查找特定主题的资料
```bash
# 1. Search for topic
torah search "repentance teshuvah"

# 2. Get full text of relevant result
torah verse "Maimonides Hilchot Teshuvah 2:1"

# 3. Find related commentaries
torah links "Maimonides Hilchot Teshuvah 2:1"
```

### 准备托拉解读（Dvar Torah）
```bash
# 1. Get this week's parsha
torah parsha

# 2. Read the opening verses
torah verse "Genesis 12:1-5"  # (adjust to actual parsha)

# 3. Find commentaries for insights
torah links "Genesis 12:1"

# 4. Search for thematic connections
torah search "lech lecha journey"
```

### 学习每日经文（Daf Yomi）
```bash
# 1. Check today's daf
torah today

# 2. Get the text
torah verse "Berakhot 2a"  # (from calendar)

# 3. See what it connects to
torah links "Berakhot 2a"
```

### 生成托拉解读（Torah Dvar）
```bash
# Quick dvar for this week's parsha
torah dvar

# Focus on specific verse
torah dvar ref "Exodus 28:1"

# Explore a theme across sources
torah dvar theme "holiness and service"
```

托拉解读生成内容包括：
- 带有希伯来文和英文的起始经文
- 主要注释（如拉什、拉姆班、伊本·以斯拉等）
- 图书馆中的相关资料
- 建议的解读结构（引言 → 问题 → 资料来源 → 解决方案 → 应用）
- 可进一步探讨的主题

## Python API

如需高级功能，请直接导入相关库：

```python
from scripts.sefaria import get_text, search, get_links, get_parsha

# Get verse
result = get_text("Genesis 1:1")
print(result.get("he"))  # Hebrew
print(result.get("text"))  # English

# Search
results = search("golden rule", limit=5)

# Get commentaries
links = get_links("Leviticus 19:18")
```

## 使用技巧

- **希伯来文搜索**：Sefaria支持希伯来文查询，例如：`torah search "ואהבת לרעך כמוך`（“要爱人如己”）
- **部分引用**：`torah verse "诗篇 23"` 会返回整章内容
- **范围查询**：`torah verse "创世记 1:1-5"` 可查询多节经文
- **塔木德上下文**：篇目引用会包含a部分和b部分的上下文信息

## 限制

- Sefaria的API使用有流量限制，请合理使用
- 部分文本仅提供希伯来文，没有英文翻译
- 搜索为全文搜索，非语义搜索（不支持词干匹配）

## 来源

本工具由 [Sefaria](https://www.sefaria.org) 提供支持——这是一个免费、开源的犹太文本图书馆。
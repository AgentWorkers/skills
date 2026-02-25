---
name: torah-scholar
description: 通过 Sefaria API 搜索和探索犹太经典文本（《托拉》、《塔纳赫》、《塔木德》、《米德拉什》及其注释）。适用于研究《托拉》的来源、查找经文、查阅注释、进行交叉引用，或准备《托拉》相关的讲道内容。支持希伯来语和英语输入。能够处理如下格式的引用：“Genesis 1:1”、“Berakhot 2a”、“Mishnah Avot 1:1”。
keywords:
  - torah
  - jewish
  - judaism
  - sefaria
  - talmud
  - bible
  - hebrew
  - tanach
  - mishnah
  - midrash
  - dvar torah
  - parsha
  - rabbi
  - yeshiva
  - study
  - religious
  - scripture
---
# 托拉学者

使用 Sefaria 图书馆全面研究犹太文献：包括《塔纳赫》（Tanach）、《巴比伦塔木德》（Talmud Bavli/Yerushalmi）、《密西拿》（Mishnah）、《米德拉什》（Midrash）、《佐哈尔》（Zohar）以及数千篇注释。

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
| `torah related <引用>` | 相关文献和主题 | `torah related "申命记 6:4"` |
| `torah parsha` | 本周的经文段落 | `torah parsha` |
| `torah today` | 每日学习计划 | `torah today` |
| `torah dvar` | 生成托拉评注 | `torah dvar` |
| `torah dvar ref <引用>` | 关于特定经文的评注 | `torah dvar ref "创世记 12:1"` |
| `torah dvar theme <主题>` | 以特定主题为中心的评注 | `torah dvar theme "领导力"` |

## 参考格式

### 《塔纳赫》（希伯来圣经）
- 书籍：《创世记》、《出埃及记》、《利未记》、《民数记》、《申命记》（托拉部分）
- 其他部分：《约书亚记》、《士师记》、《撒母耳记》、《列王纪》、《以赛亚书》、《耶利米书》、《以西结书》等
- 格式：`书籍 章节:经文` 或 `书籍 章节:起始-结束`
- 例：`创世记 1:1`、`诗篇 23`、`以赛亚书 40:1-5`

### 《塔木德》
- 巴比伦塔木德（Babylonian Talmud）：`篇目 编号a` 或 `b`
- 例：`Berakhot 2a`、`Shabbat 31a`、`Bava Metzia 59b`
- 主要篇目：Berakhot（祝福篇）、Shabbat（安息日篇）、Eruvin（土地篇）、Pesachim（逾越节篇）、Yoma（七日篇）、Sukkah（住棚节篇）、Beitzah（五旬节篇）、Rosh Hashanah（犹太新年篇）、Taanit（禁食篇）、Megillah（读经篇）、Moad Katan（小节期篇）、Chagigah（节日篇）、Yevamot（死亡篇）、Ketubot（婚姻法篇）、Nedarim（誓约篇）、Nazir（禁戒篇）、Sotah（妇女篇）、Gittin（离婚篇）、Bava Kamma（刑罚篇）、Bava Metzia（民事篇）、Bava Batra（刑事篇）、Sanhedrin（公会篇）、Makkot（刑罚篇）、Shevuot（七七节篇）、Avodah Zarah（献祭篇）、Horayot（圣洁篇）、Zevachim（祭祀篇）、Menachot（节期篇）、Chullin（洁净篇）、Bekhorot（长子篇）、Arakhin（赎罪篇）、Temurah（赎罪仪式篇）、Keritot（赎罪券篇）、Meilah（祈祷篇）、Tamid（每日祷告篇）、Niddah（洁净仪式篇）

### 《密西拿》
- 格式：`Mishnah 篇目 章节:经文`
- 例：`Mishnah Avot 1:1`、`Mishnah Berakhot 1:1`

### 《米德拉什》
- Midrash Rabbah：`Genesis Rabbah 1:1`、`Exodus Rabbah 1:1`
- Midrash Tanchuma：`Tanchuma Bereshit 1`
- 其他版本：`Pirkei DeRabbi Eliezer 1`

### 注释
- 通过 `torah links <引用>` 查看拉什（Rashi）、兰班（Ramban）、伊本·以斯拉（Ibn Ezra）等注释家的注释

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

### 准备托拉评注
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

### 学习每日经文
```bash
# 1. Check today's daf
torah today

# 2. Get the text
torah verse "Berakhot 2a"  # (from calendar)

# 3. See what it connects to
torah links "Berakhot 2a"
```

### 生成托拉评注
```bash
# Quick dvar for this week's parsha
torah dvar

# Focus on specific verse
torah dvar ref "Exodus 28:1"

# Explore a theme across sources
torah dvar theme "holiness and service"
```

托拉评注生成器输出：
- 带有希伯来文和英文的开篇经文
- 主要注释（拉什、兰班、伊本·以斯拉等）
- 图书馆中的相关资料
- 建议的写作结构（引言 → 问题 → 资料来源 → 解决方案 → 应用）
- 可进一步探讨的主题

## Python API

如需高级功能，可直接导入：

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

## 提示

- **希伯来文搜索**：Sefaria 支持希伯来文查询，例如：`torah search "ואהבת לרעך כמוך`
- **部分引用**：`torah verse "诗篇 23"` 会返回整章内容
- **范围查询**：`torah verse "创世记 1:1-5"` 可查询多节经文
- **塔木德上下文**：篇目引用包含 a 和 b 两部分的注释

## 限制

- 使用 Sefaria 的 API 会受到使用次数的限制（请尊重其免费资源）
- 部分文献可能仅提供希伯来文内容（无英文翻译）
- 搜索为全文搜索，非语义搜索（不支持精确匹配或词干匹配）

## 来源

本工具由 [Sefaria](https://www.sefaria.org) 提供支持——这是一个免费的、开源的犹太文献库。
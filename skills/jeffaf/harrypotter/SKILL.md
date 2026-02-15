---
name: harrypotter
version: 1.0.0
description: "这是一个用于AI代理的命令行工具（CLI），旨在帮助人类用户查询《哈利·波特》系列作品中的相关信息。该工具通过HP-API（Harry Potter API）来获取数据，且无需任何身份验证（auth）即可使用。"
homepage: https://hp-api.onrender.com
metadata:
  openclaw:
    emoji: "🧙"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["harrypotter", "wizarding-world", "entertainment", "cli", "hp-api"]
---

# 哈利·波特查询工具

这是一个用于AI代理的命令行工具（CLI），帮助用户查询哈利·波特宇宙中的相关信息。例如：“斯莱特林学院都有哪些学生？”——现在你的AI代理可以为你解答这个问题。

该工具使用免费的哈利·波特API（HP-API），无需注册账户或API密钥。

## 使用方法

```
"Who are the main Harry Potter characters?"
"List the Hogwarts students"
"Who's in Gryffindor house?"
"What spells are in Harry Potter?"
"Search for Hermione"
```

## 命令列表

| 功能        | 命令                                      |
|------------|-----------------------------------------|
| 查看所有角色    | `harrypotter characters [limit]`                   |
| 查看学生名单    | `harrypotter students [limit]`                   |
| 查看教职工名单 | `harrypotter staff [limit]`                   |
| 按学院查询    | `harrypotter house <学院名称>`                   |
| 查看魔法咒语    | `harrypotter spells [limit]`                   |
| 进行搜索      | `harrypotter search <查询内容>`                   |

### 示例

```bash
harrypotter characters 10         # First 10 characters
harrypotter students              # All Hogwarts students
harrypotter staff                 # All Hogwarts staff
harrypotter house gryffindor      # Gryffindor members
harrypotter house slytherin       # Slytherin members
harrypotter spells 15             # First 15 spells
harrypotter search "hermione"     # Find character by name
```

## 输出结果

**角色查询结果：**
```
🧙 Harry Potter — Gryffindor, Half-blood, Patronus: Stag
🧙 Hermione Granger — Gryffindor, Muggleborn, Patronus: Otter
🧙 Draco Malfoy — Slytherin, Pure-blood
```

**搜索结果（详细信息）：**
```
🧙 Hermione Granger — Gryffindor, muggleborn, Patronus: otter
   Actor: Emma Watson
   Wand: vine, dragon heartstring, 10.75"
   Born: 19-09-1979
```

**魔法咒语查询结果：**
```
✨ Expelliarmus — Disarms your opponent
✨ Lumos — Creates a small light at the wand's tip
✨ Avada Kedavra — The Killing Curse
```

## 注意事项

- 该工具基于HP-API（hp-api.onrender.com）运行。
- 无需身份验证。
- 可查询的学院名称：格兰芬多（Gryffindor）、斯莱特林（Slytherin）、赫奇帕奇（Hufflepuff）、拉文克劳（Ravenclaw）。
- 每次查询默认返回20条结果。
- 搜索不区分大小写。

---

## 代理实现说明

**脚本位置：`{skill_folder}/harrypotter`（实际脚本位于`scripts/harrypotter`文件夹中）**

**当用户询问哈利·波特相关内容时：**
1. 使用 `./harrypotter search <角色名称>` 查询特定角色。
2. 使用 `./harrypotter house <学院名称>` 查询该学院的成员。
3. 使用 `./harrypotter spells` 查询魔法咒语信息。
4. 使用 `./harrypotter students` 或 `./harrypotter staff` 查询相应角色的列表。

**学院名称不区分大小写：**
- 格兰芬多（Gryffindor）
- 斯莱特林（Slytherin）
- 赫奇帕奇（Hufflepuff）
- 拉文克劳（Ravenclaw）

**适用范围：** 仅适用于与哈利·波特相关的查询；不支持非哈利·波特主题的奇幻内容或API中未收录的普通知识问答。
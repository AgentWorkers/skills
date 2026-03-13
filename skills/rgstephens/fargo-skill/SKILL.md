---
name: fargorate
description: 从 FargoRate 查找台球选手的评分和让分数据。当用户询问某位台球选手的评分、FargoRate ID、比赛赔率、推荐赛事、让分情况、排名靠前的台球选手，或评分随时间的变化时，可使用这些数据。可以启用本地数据库来记录每次比赛后的评分变化。数据库中的联系信息仅用于本地存储，绝不会被发送到任何 API。
version: 0.3.6
metadata:
  openclaw:
    emoji: "🎱"
    homepage: https://github.com/rgstephens/fargo-skill
    requires:
      bins:
        - fargo
    install:
      - kind: brew
        tap: rgstephens/fargo
        formula: fargo
        bins:
          - fargo

---
# FargoRate

使用 `fargo` CLI 工具，可以从 [FargoRate](https://fargorate.com) 查阅球员评分、比赛赔率以及让分数据。

---

## 命令

### `search` — 按名称或 FargoRate ID 搜索球员

```bash
fargo search <name or id>
```

```bash
fargo search "John Smith"
fargo search 12345
```

### `lookup` — 根据 FargoRate ID 查找球员

这是 `search` 命令的别名，仅接受一个 ID 作为参数。

```bash
fargo lookup <id>
```

```bash
fargo lookup 12345
```

### `bulk` — 一次性查询多个球员

```bash
fargo bulk <id1> [id2 ...]
fargo bulk --group <name>
```

```bash
fargo bulk 12345 67890 11111

# Use a saved group (see `group` command)
fargo bulk --db --group monday-league
```

| 标志             | 描述                                                               |
|------------------|---------------------------------------------------------------------------|
| `--group <name>` | 使用保存的球员 ID 组进行查询（需要 `--db` 参数） |

使用配置的自定义列表 ID（参见 `setup`）。默认使用内置的列表 ID。

### `odds` — 计算比赛赔率

```bash
fargo odds <rating1> <rating2> <race1> <race2>
```

```bash
# Player rated 550 (races to 7) vs player rated 480 (races to 9)
fargo odds 550 480 7 9
```

### `races` — 获取推荐的赛程长度

```
fargo races <rating1> <rating2> [--type 0|1|2] [--length N]
```

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--type` | `1` | 赛程类型：`0`=Scotch Doubles（苏格兰双打），`1`=Singles（单打），`2`=Team（团队赛） |
| `--length` | — | 固定总赛程长度；省略此参数将自动推荐合适的赛程长度 |

```bash
# Recommended singles race lengths for two players
fargo races 550 480

# Scotch doubles race recommendation
fargo races 550 480 --type 0

# Singles races that fit within a total of 15 games
fargo races 550 480 --length 15
```

### `top` — 查看排名前 10 的球员

```bash
fargo top [--ranking World|US] [--gender M|F]
```

| 标志 | 默认值 | 描述 |
|------|---------|-------------|
| `--ranking` | `World` | 全球排名或美国排名 |
| `--gender` | `M` | 男性或女性 |

```bash
fargo top
fargo top --ranking US --gender F
```

### `setup` — 配置工具

```
fargo setup [--list-id ID]
```

将自定义列表 ID 保存到 `~/.nanobot/workspace/fargorate/config.json` 文件中，以便 `bulk` 命令使用。

```bash
# Interactive prompt
fargo setup

# Non-interactive
fargo setup --list-id myCustomListId
```

### `group` — 管理命名的球员 ID 组

通过创建组，您可以保存一组球员 ID，从而避免每次查询时都手动输入这些 ID。所有与组相关的命令都需要 `--db` 参数。

```bash
# Create or replace a group
fargo --db group set monday-league 12345 67890 11111

# List all groups
fargo --db group list

# Show members of a group (shows cached name/rating if player has been looked up)
fargo --db group show monday-league

# Delete a group
fargo --db group delete monday-league
```

然后可以使用 `bulk` 命令来查询这些组中的球员：

```bash
fargo --db bulk --group monday-league
fargo --changes --db bulk --group monday-league
```

### 版本

```bash
fargo --version
```

---

## 全局标志

这些标志适用于所有命令：

| 标志          | 描述                                                              |
|---------------|--------------------------------------------------------------------------|
| `--json`      | 以原始 JSON 格式输出从 API 获取的数据                                 |
| `--db [path]` | 将检索到的球员数据保存到 SQLite 数据库                        |
| `--changes`   | 仅输出评分或稳健性发生变化的球员（需要 `--db` 参数） |

---

## 数据库（`--db`）

`--db` 标志启用一个本地 SQLite 数据库，用于在多次运行中持久保存球员数据。该标志适用于 `search`、`lookup` 和 `bulk` 等从 API 获取球员记录的命令。

### 使用方法

```bash
# Use the default database file (fargo.db in the current directory)
fargo --db search "John Smith"
fargo --db bulk 12345 67890

# Use a custom path (requires = syntax)
fargo --db=~/data/fargo.db search "John Smith"

# Combine with --json (outputs raw JSON AND updates the database)
fargo --json --db search "John Smith"
```

### 行为

- 如果数据库文件不存在，系统会自动创建它。
- 每次运行时，系统会更新或插入球员信息——现有记录会被刷新，新记录会被添加。
- 只有当球员的评分发生变化时，`previous_rating` 字段才会被自动更新。
- 只有在新球员出现或评分发生变化时，才会向 `rating_history` 表中添加新记录，从而避免历史记录重复。

### 数据库模式

```sql
CREATE TABLE players (
    id                      TEXT PRIMARY KEY,
    first_name              TEXT NOT NULL,
    last_name               TEXT NOT NULL,
    location                TEXT,
    rating                  INTEGER NOT NULL DEFAULT 0,
    previous_rating         INTEGER NOT NULL DEFAULT 0,
    provisional_rating      INTEGER NOT NULL DEFAULT 0,
    robustness              INTEGER NOT NULL DEFAULT 0,
    last_update_timestamp   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    email                   TEXT,
    mobile                  TEXT,
    telegram                TEXT,
    discord                 TEXT,
    preferred_communication TEXT CHECK(preferred_communication IN ('email','mobile','telegram','discord'))
);

CREATE TABLE rating_history (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id          TEXT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    timestamp          DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rating             INTEGER NOT NULL,
    provisional_rating INTEGER NOT NULL,
    robustness         INTEGER NOT NULL
);

CREATE TABLE fargo_groups (
    name       TEXT PRIMARY KEY,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fargo_group_members (
    group_name TEXT NOT NULL REFERENCES fargo_groups(name) ON DELETE CASCADE,
    player_id  TEXT NOT NULL,
    PRIMARY KEY (group_name, player_id)
);
```

> **注意：** 联系信息字段（`email`、`mobile`、`telegram`、`discord`、`preferred_communication`）虽然存储在数据库中，但它们不是由 FargoRate API 提供的。这些字段可以直接在数据库中设置，并且当球员评分发生变化时，这些信息会包含在 `--changes` 的输出结果中。

---

## 变更检测（`--changes`）

`--changes` 标志仅输出自上次运行以来评分或稳健性发生变化的球员信息。该标志需要 `--db` 参数，并适用于 `search`、`lookup` 和 `bulk` 命令。

尽管每次运行时所有检索到的球员信息都会被写入数据库，但 `--changes` 仅影响输出内容。

### 示例

```bash
# Report only players whose rating or robustness changed
fargo --changes --db search "John Smith"
fargo --changes --db bulk 12345 67890 11111

# Custom DB path
fargo --changes --db=~/data/fargo.db bulk 12345 67890

# Machine-readable JSON output of changes (useful for bots)
fargo --changes --json --db search "John Smith"
```

### 示例输出

```text
1 change(s) detected:

Name       : John Smith
ID         : 12345
Rating     : 480 → 495 (provisional: 0)
Robustness : 200 → 215
Location   : Phoenix AZ
Email      : john@example.com
Preferred  : email
---
```

新球员（数据库中不存在的球员）会被标记为 `[NEW]`，并且会显示他们的当前信息，不附带 `→` 箭头。

### JSON 输出示例（`--json --changes`）

```json
[
  {
    "firstName": "John",
    "lastName": "Smith",
    "id": "12345",
    "rating": 495,
    "provisionalRating": 0,
    "robustness": 215,
    "location": "Phoenix AZ",
    "isNew": false,
    "previousRating": 480,
    "previousRobustness": 200,
    "email": "john@example.com",
    "preferredCommunication": "email"
  }
]
```

当联系信息字段为空时，JSON 输出中会省略这些字段。

如果没有检测到任何变化，输出内容如下：

```text
No changes detected.
```
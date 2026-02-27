---
name: discogs-sync
description: >
  **功能说明：**  
  - 可根据艺术家名称、专辑名称、主版ID（master ID）或发行ID，向Discogs的愿望清单（wantlist）或收藏列表中添加/删除专辑。  
  - 支持搜索黑胶唱片（vinyl）、CD及其他格式唱片在市场上的价格信息。  
  - 能够列出愿望清单和收藏列表中的所有内容。  
  - 当用户请求将某张唱片添加到愿望清单或收藏列表中、查看愿望清单中的内容、查询市场价格，或了解某张唱片的售价时，可使用该功能。  
  - 还支持通过CSV/JSON文件批量操作。
metadata: {"openclaw":{"emoji":"🎵","requires":{"bins":["python3"]}}}
---
# Discogs Sync — 想购清单、收藏夹及市场交易 CLI 工具

该工具支持在您的 Discogs 想购清单或收藏夹中添加或删除专辑，查询市场上的价格信息，并列出您已拥有的专辑。您可以通过艺术家名称、专辑名称、Discogs 主版本 ID 或发行 ID 来查找专辑。对于批量操作，可以传递 CSV 或 JSON 文件。

## 运行时环境与依赖项

**运行时环境：** Python 3.10 及更高版本

**Python 包**（首次运行时会自动安装）：
- `python3-discogs-client>=2.8` — Discogs API 客户端
- `click>=8.1` — CLI 框架
- `rich>=13.0` — 终端输出格式化库

**安装方式：** 无需手动执行 `pip install`。首次运行时，`discogs-sync.py` 会在技能目录内创建一个名为 `.deps/` 的虚拟环境，并从 `requirements.txt` 文件中安装依赖项。后续运行会重用该虚拟环境。该工具支持 macOS（包括 Homebrew Python）、Linux 和 Windows 系统，无需进行系统级别的包安装。

如需强制重新安装依赖项，请删除 `.deps/` 目录，然后再次运行该工具。

## 快速入门

```bash
# Authenticate (one-time setup — also installs dependencies on first run)
python3 discogs-sync.py auth

# Add an album to your wantlist by name
python discogs-sync.py wantlist add --artist "Radiohead" --album "OK Computer"

# Add to your collection by release ID
python discogs-sync.py collection add --release-id 7890

# Check marketplace prices for a vinyl pressing
python discogs-sync.py marketplace search --artist "Miles Davis" --album "Kind of Blue" --format Vinyl

# List your wantlist
python discogs-sync.py wantlist list

# Remove from collection
python discogs-sync.py collection remove --artist "Nirvana" --album "Nevermind"
```

## 认证

只需运行一次工具即可完成认证。提供两种认证方式：

**个人访问令牌（默认）** — 最简单的认证方式。您可以在 [https://www.discogs.com/settings/developers](https://www.discogs.com/settings/developers) 生成访问令牌。

```bash
python discogs-sync.py auth
python discogs-sync.py auth --mode token
```

**OAuth 1.0a** — 适用于需要委托访问权限的应用程序，支持完整的 OAuth 流程（包括消费者密钥和密钥串）。

```bash
python discogs-sync.py auth --mode oauth
```

认证信息存储在 `~/.discogs-sync/config.json` 文件中。

```bash
# Verify authentication
python discogs-sync.py whoami
python discogs-sync.py whoami --output-format json
```

## 使用方法

### 想购清单 — 添加、删除、列出专辑

```bash
# Add by artist/album name
python discogs-sync.py wantlist add --artist "Radiohead" --album "OK Computer" [--format Vinyl]

# Add by Discogs master ID (resolves to main release, or filters by --format)
python discogs-sync.py wantlist add --master-id 3425

# Add by specific release ID
python discogs-sync.py wantlist add --release-id 7890

# Remove by artist/album name
python discogs-sync.py wantlist remove --artist "Radiohead" --album "OK Computer"

# Remove by release ID
python discogs-sync.py wantlist remove --release-id 7890

# List current wantlist
python discogs-sync.py wantlist list [--search "QUERY"] [--format Vinyl] [--year 1997] [--no-cache] [--output-format json]
```

**重复检查：** 如果专辑已存在于想购清单中（通过发行 ID、主版本 ID 或艺术家名称+专辑名称的模糊匹配），则跳过该专辑的添加操作。

### 收藏夹 — 添加、删除、列出专辑

```bash
# Add by artist/album name
python discogs-sync.py collection add --artist "Miles Davis" --album "Kind of Blue" [--format Vinyl]

# Add by master ID or release ID
python discogs-sync.py collection add --master-id 3425 [--folder-id 1]
python discogs-sync.py collection add --release-id 7890 [--folder-id 1]

# Add a second copy of something already owned
python discogs-sync.py collection add --release-id 7890 --allow-duplicate

# Remove by artist/album name
python discogs-sync.py collection remove --artist "Miles Davis" --album "Kind of Blue"

# Remove by release ID
python discogs-sync.py collection remove --release-id 7890

# List collection (all folders)
python discogs-sync.py collection list [--search "QUERY"] [--format CD] [--year 1959] [--folder-id 0] [--no-cache] [--output-format json]
```

**重复检查：** 默认情况下，如果专辑已存在于收藏夹中（通过发行 ID、主版本 ID 或艺术家名称+专辑名称的模糊匹配），`add` 命令会跳过该专辑的添加操作。使用 `--allow-duplicate` 选项可允许添加重复的专辑。

### 市场交易 — 查询价格信息

```bash
# Search by artist/album name
python discogs-sync.py marketplace search --artist "Radiohead" --album "OK Computer" [--format Vinyl] [--country US] [--output-format json]

# Search by master ID
python discogs-sync.py marketplace search --master-id 3425 [--format Vinyl] [--country US]

# Search by specific release ID (skips master version scan)
python discogs-sync.py marketplace search --release-id 7890

# Filter by price range and country
python discogs-sync.py marketplace search --artist "Pink Floyd" --album "The Dark Side of the Moon" --format Vinyl --country US --min-price 10 --max-price 50 --currency USD

# Show detailed progress and condition grade price suggestions
python discogs-sync.py marketplace search --artist "Radiohead" --album "OK Computer" --verbose --details
```

查询结果会按最低价格排序，并显示在售专辑的数量。单个专辑的结果会缓存 1 小时（具体取决于查询参数）。使用 `--details` 选项时，会生成单独的详细信息缓存条目；如果仅使用基础缓存，工具会直接获取价格建议，而不会重新执行完整搜索。使用 `--no-cache` 选项可强制获取实时数据（结果仍会被写入缓存）。

### 通过文件进行批量操作

对于批量操作，可以传递 CSV 或 JSON 文件，而无需单独使用 `--artist`/`--album` 参数。

```bash
# Sync wantlist from file (preview first with --dry-run)
python discogs-sync.py wantlist sync albums.csv --dry-run
python discogs-sync.py wantlist sync albums.csv [--remove-extras] [--threshold 0.7] [--output-format json]

# Sync collection from file
python discogs-sync.py collection sync albums.csv [--folder-id 1] [--remove-extras] [--dry-run]

# Batch marketplace search from file
python discogs-sync.py marketplace search albums.csv [--format Vinyl] [--country US] [--max-price 50] [--max-versions 25] [--output-format json]
```

**CSV 格式**（需要包含标题行，且必须包含 `artist` 和 `album` 字段）：

```csv
artist,album,format,year,notes
Radiohead,OK Computer,Vinyl,,Must have
Miles Davis,Kind of Blue,,1959,Original pressing
Nirvana,Nevermind,CD,1991,
```

**JSON 格式**（包含相同字段的对象数组）：

```json
[
    {"artist": "Radiohead", "album": "OK Computer", "format": "Vinyl"},
    {"artist": "Miles Davis", "album": "Kind of Blue", "year": 1959}
]
```

格式同义词会自动进行规范化处理：例如 `LP`/`record` 会被转换为 “Vinyl”，`compact disc` 被转换为 “CD”，`tape`/`mc` 被转换为 “Cassette”。

## 选项

| 选项 | 适用范围 | 描述 |
|--------|-----------|-------------|
| `--output-format` | 所有操作 | 输出格式：`table`（默认）或 `json`（便于机器读取） |
| `--threshold` | 添加、删除、查询 | 匹配阈值（0.0–1.0，默认值：0.7） |
| `--format` | 添加、列出、市场查询 | 按格式过滤：Vinyl、CD、Cassette（同义词如 LP、record 会被规范化处理） |
| `--year` | 列出 | 按发行年份过滤（精确匹配） |
| `--folder-id` | 收藏夹 | 目标文件夹（默认值：1 表示添加操作，0 表示读取操作） |
| `--allow-duplicate` | 收藏夹添加 | 允许向收藏夹中添加已存在的专辑副本 |
| `--country` | 市场查询 | 按发行国家过滤（精确匹配：US、UK、Germany 等） |
| `--release-id` | 市场查询 | 仅获取特定专辑的详细信息（跳过主版本检查） |
| `--min-price` | 市场查询 | 最低价格过滤条件 |
| `--max-price` | 市场查询 | 最高价格过滤条件 |
| `--currency` | 市场查询 | 货币代码（默认值：USD） |
| `--max-versions` | 市场查询 | 每个主版本允许检查的最大发行版本数量（默认值：25） |
| `--details` | 市场查询 | 包含按条件等级划分的建议价格 |
| `--no-cache` | 列出、市场查询 | 强制获取实时数据（结果仍会被写入缓存） |
| `--verbose` | 同步、市场查询 | 显示详细进度和 API 调用日志 |
| `--search` | 列出 | 按艺术家名称或专辑名称过滤结果（不区分大小写） |
| `--dry-run` | 同步 | 预览更改内容，不会修改 Discogs 数据库 |
| `--remove-extras` | 同步 | 从想购清单/收藏夹中删除输入文件中不存在的专辑 |

## 输出格式

### 文本格式（默认）

**想购清单列表 / 收藏夹列表：**

```
                           Wantlist
┌────────────┬───────────┬─────────────┬─────────────┬────────┬──────┐
│ Release ID │ Master ID │ Artist      │ Title       │ Format │ Year │
├────────────┼───────────┼─────────────┼─────────────┼────────┼──────┤
│ 7890       │ 3425      │ Radiohead   │ OK Computer │ Vinyl  │ 1997 │
│ 1234       │ 1000      │ Miles Davis │ Kind of Blue│ Vinyl  │ 1959 │
└────────────┴───────────┴─────────────┴─────────────┴────────┴──────┘

Total: 2
```

**市场查询结果：**

```
                               Marketplace Results
┌───────────┬────────────┬───────────┬─────────────┬────────┬──────────┬──────────────┐
│ Master ID │ Release ID │ Artist    │ Title       │ Format │ For Sale │ Lowest Price │
├───────────┼────────────┼───────────┼─────────────┼────────┼──────────┼──────────────┤
│ 3425      │ 7890       │ Radiohead │ OK Computer │ Vinyl  │ 42       │ 25.99 USD    │
│ 3425      │ 15432      │ Radiohead │ OK Computer │ Vinyl  │ 18       │ 32.50 USD    │
└───────────┴────────────┴───────────┴─────────────┴────────┴──────────┴──────────────┘
```

**添加/删除操作结果：**

```
Sync Report
  Total input: 1
  Added:   1
  Removed: 0
  Skipped: 0
  Errors:  0
```

### JSON 格式（`--output-format json`）

**想购清单列表 / 收藏夹列表：**

```json
{
  "items": [
    {
      "release_id": 7890,
      "master_id": 3425,
      "title": "OK Computer",
      "artist": "Radiohead",
      "format": "Vinyl",
      "year": 1997
    }
  ],
  "total": 1
}
```

**市场查询结果：**

```json
{
  "results": [
    {
      "master_id": 3425,
      "release_id": 7890,
      "title": "OK Computer",
      "artist": "Radiohead",
      "format": "Vinyl",
      "country": "US",
      "year": 1997,
      "num_for_sale": 42,
      "lowest_price": 25.99,
      "currency": "USD"
    }
  ],
  "total": 1
}
```

**添加/删除/同步操作报告：**

```json
{
  "summary": {
    "total_input": 1,
    "added": 1,
    "removed": 0,
    "skipped": 0,
    "errors": 0
  },
  "actions": [
    {
      "action": "add",
      "artist": "Radiohead",
      "title": "OK Computer",
      "release_id": 7890,
      "master_id": 3425,
      "reason": null,
      "error": null
    }
  ]
}
```

## 输出字段

- **release_id** — Discogs 专辑的唯一标识符 |
- **master_id** — Discogs 主版本的标识符（包含专辑的所有发行版本） |
- **title** — 专辑名称 |
- **artist** — 艺术家名称 |
- **format** | 物理格式（Vinyl、CD、Cassette 等） |
- **year** | 发行年份 |
- **country** | 发行国家 |
- **num_for_sale** | 市场上在售的专辑数量 |
- **lowest_price** | 专辑的最低售价 |
- **currency** | 价格货币代码 |
- **instance_id** | 收藏夹中的专辑实例标识符（用于处理重复专辑） |
- **folder_id** | 收藏夹文件夹标识符 |
- **action** | 执行的操作：`add`（添加）、`remove`（删除）、`skip`（跳过）或 `error`（错误） |

## 专辑匹配机制

当使用 `--artist` 和 `--album` 参数时，工具会执行多轮搜索以找到最匹配的 Discogs 数据：

1. **结构化搜索**：根据艺术家名称、专辑名称、格式和发行年份进行精确匹配。
2. **宽松搜索**：忽略格式和年份限制。
3. **自由文本搜索**：以纯文本形式搜索 “artist album”。

每个搜索结果的匹配度评分范围为 0.0–1.0：艺术家名称相似度占 40%，专辑名称相似度占 40%，发行年份相似度占 10%，格式相似度占 10%。评分低于 `--threshold`（默认值 0.7）的结果会被忽略。可以通过调整阈值来放宽匹配条件。

当使用 `--master-id` 或 `--release-id` 参数时，工具会直接使用这些标识符进行查询。

## 错误代码

- **0** — 成功（所有操作均完成） |
- **1** — 部分失败（部分操作失败） |
- **2** — 完全失败（没有操作完成，或出现认证/配置错误） |

## 注意事项

- 支持个人访问令牌（默认）和 OAuth 1.0a 认证方式。请运行 `python discogs-sync.py auth` 一次进行初始化。
- Discogs API 对已认证用户的请求频率有限制（每分钟 60 次）。该工具会自动控制请求频率，无需手动调整。
- 批量操作具有容错性：即使部分操作失败，整个批次仍会继续执行并报告错误。
- 在执行同步操作前，请使用 `--dry-run` 选项预览更改内容。此选项不会修改 Discogs 数据库。
- 使用 `--remove-extras` 选项时，会从想购清单/收藏夹中删除输入文件中不存在的专辑。请谨慎使用。
- 收藏夹允许保存同一专辑的多个副本（例如，两张相同的 LP 版本）。默认情况下，`collection add` 命令会跳过重复的专辑。使用 `--allow-duplicate` 选项可允许添加重复的专辑。
- 缓存文件存储在 `~/.discogs-sync/` 目录下，包括 `wantlist_cache.json`、`collection_cache.json` 和 `marketplace_<type>_<hash>.json`（以及相关的 `…_details.json` 文件）。删除这些文件可清除过时的缓存数据。
- `~/.discogs-sync/config.json` 文件中存储您的 Discogs 认证信息。在 Linux/macOS 系统上，请设置文件权限为 `chmod 600 ~/.discogs-sync/config.json`。如果您的令牌被盗用，请在 [https://www.discogs.com/settings/developers](https://www.discogs.com/settings/developers) 注销令牌。
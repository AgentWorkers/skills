---
name: timemap
version: 1.0.0
description: >
  您可以通过 timemap.co.il 搜索特拉维夫和海法的历史娱乐场所、夜生活场所及文化设施，包括酒吧、咖啡馆、俱乐部、电影院和餐饮场所。可以使用以下关键词进行查询：  
  - “特拉维夫的历史酒吧”（bars in Tel Aviv history）  
  - “这个地址曾经有什么？”（what was at this address）  
  - “夜生活历史”（nightlife history）  
  - “在特拉维夫消遣”（בילה בתל אביב）  
  - “这里曾经有什么？”（מה היה פה פעם）  
  - “已关闭的俱乐部”（מועדונים שנסגרו）  
  - “历史悠久的咖啡馆”（בתי קפה היסטוריים）  
  - “海法的电影院”（בתי קולנוע בחיפה）
author: Alex Polonsky (https://github.com/alexpolonsky)
homepage: https://github.com/alexpolonsky/agent-skill-timemap
license: MIT
metadata: {"openclaw": {"emoji": "🗺️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# Timemap - 特拉维夫和海法的历史场所信息

您可以通过 [timemap.co.il](https://timemap.co.il) 搜索特拉维夫-雅法（Tel Aviv-Yafo）和海法（Haifa）的历史娱乐场所、夜生活场所和文化场所。该数据库由社区成员共同维护，记录了这些城市中的酒吧、咖啡馆、俱乐部、电影院、餐饮场所和表演空间等信息。

> 数据来源于 [timemap.co.il](https://timemap.co.il)，这是一个由 [Reut Miryam Cohen](https://x.com/reutc) 和 Amir Ozer 共同开发的非营利项目，旨在“向那些塑造了我们成长环境的地点和人们致以敬意”。数据库中包含了场所的开业/关闭日期、位置、标签、用户评价以及照片等信息。此工具提供了一个非官方的命令行界面（CLI）来查询这些数据。

## 快速入门

```bash
# Search for a venue (Hebrew or English)
python3 {baseDir}/scripts/timemap.py search "רוטשילד"
python3 {baseDir}/scripts/timemap.py search "Barby"

# See what was active in a specific year
python3 {baseDir}/scripts/timemap.py timeline 2010

# Get database statistics
python3 {baseDir}/scripts/timemap.py stats
```

## 命令说明

| 命令 | 功能说明 |
|---------|-------------|
| `search <查询>` | 通过名称或地址（希伯来语或英语）搜索场所 |
| `filter` | 根据 --city、--tags、--year、--active-in、--opened、--closed 等参数进行筛选 |
| `venue <id>` | 根据 ID 或名称获取特定场所的详细信息 |
| `timeline <年份>` | 显示指定年份内所有活跃的场所 |
| `nearby <纬度> <经度>` | 在指定坐标附近查找场所（半径以公里为单位，默认为 0.5 公里） |
| `tags [标签]` | 列出所有标签，或显示具有特定标签的场所 |
| `cities` | 显示各城市的场所数量 |
| `stats` | 数据库统计信息（按城市、标签、年代和状态分类） |
| `memories <ID>` | 显示特定场所的用户评价和照片 |
| `random` | 随机选择一个场所（优先选择有用户评价或照片的场所） |

## 搜索示例

```bash
# Search by name (Hebrew or English)
python3 {baseDir}/scripts/timemap.py search "טדי"
python3 {baseDir}/scripts/timemap.py search "Barby"

# Search by address
python3 {baseDir}/scripts/timemap.py search "רוטשילד"
python3 {baseDir}/scripts/timemap.py search "דיזנגוף"

# Get full details for a venue
python3 {baseDir}/scripts/timemap.py venue 192

# Find venues with user memories
python3 {baseDir}/scripts/timemap.py memories 253
```

## 筛选示例

```bash
# Filter by city
python3 {baseDir}/scripts/timemap.py filter --city tlv
python3 {baseDir}/scripts/timemap.py filter --city haifa

# Filter by tag
python3 {baseDir}/scripts/timemap.py filter --tags bar
python3 {baseDir}/scripts/timemap.py filter --tags food
python3 {baseDir}/scripts/timemap.py filter --tags cinema

# Venues that opened in a specific year
python3 {baseDir}/scripts/timemap.py filter --opened 2005

# Venues that closed in a specific year
python3 {baseDir}/scripts/timemap.py filter --closed 2010

# Venues active in a specific year
python3 {baseDir}/scripts/timemap.py filter --active-in 2008

# Combine filters
python3 {baseDir}/scripts/timemap.py filter --city tlv --tags bar --active-in 2010
```

## 时间线与位置示例

```bash
# See what was happening in a specific year
python3 {baseDir}/scripts/timemap.py timeline 2005
python3 {baseDir}/scripts/timemap.py timeline 1995

# Find venues near coordinates (Rothschild Blvd area)
python3 {baseDir}/scripts/timemap.py nearby 32.0646 34.7731
python3 {baseDir}/scripts/timemap.py nearby 32.0646 34.7731 --radius 1.0

# Find venues near Florentin
python3 {baseDir}/scripts/timemap.py nearby 32.0566 34.7608 --radius 0.5
```

## 浏览与探索

```bash
# List all tags
python3 {baseDir}/scripts/timemap.py tags

# Show venues with a specific tag
python3 {baseDir}/scripts/timemap.py tags bar
python3 {baseDir}/scripts/timemap.py tags club

# List cities
python3 {baseDir}/scripts/timemap.py cities

# Database statistics
python3 {baseDir}/scripts/timemap.py stats

# Random venue (great for discovery)
python3 {baseDir}/scripts/timemap.py random
```

## 选项参考

| 选项 | 命令 | 功能说明 |
|--------|----------|-------------|
| `--json` | 输出格式 | 以 JSON 格式输出（适合自动化脚本） |
| `--limit N` | 限制结果数量 | 每次查询的最大结果数量（终端默认为 25 个，使用 --json 时无限制） |
| `--no-color` | 禁用颜色显示 | 禁用颜色输出（非终端设备会自动忽略此选项） |
| `--fresh` | 强制刷新 | 从 API 获取最新数据（忽略缓存） |
| `--city` | 筛选条件 | 按城市代码筛选（例如：tlv 表示特拉维夫） |
| `--tags` | 筛选条件 | 根据标签筛选（支持子字符串匹配） |
| `--year` | 筛选条件 | 仅显示当年开业或关闭的场所 |
| `--active-in` | 筛选条件 | 仅显示当年仍活跃的场所 |
| `--opened` | 筛选条件 | 仅显示当年开业的场所 |
| `--closed` | 筛选条件 | 仅显示当年关闭的场所 |
| `--radius` | 筛选条件 | 搜索半径（以公里为单位，默认为 0.5 公里） |

## 城市代码

| 代码 | 城市 |
|------|------|
| `tlv` | 特拉维夫 |
| `haifa` | 海法 |

## 标签

（共 7 个主要标签，与网站的用户界面筛选功能对应：）

| 标签 | 希伯来语 | 描述 |
|-----|--------|-------------|
| `bar` | ברים | 酒吧 |
| `food` | אוכל | 餐厅/餐饮场所 |
| `cafe` | בתי קפה | 咖啡馆 |
| `club` | מועדונים | 夜总会 |
| `cinema` | בתי קולנוע | 电影院 |
| `live_shows` | הופעות | 现场演出 |
| `lgbtq` | להטב"ק | LGBTQ 相关场所 |

其他标签：`dance_bar`（舞吧）、`lounge`（休息室）、`wine_bar`（葡萄酒吧）、`restaurant`（餐厅）

使用 `python3 {baseDir}/scripts/timemap.py tags` 命令可以查看实时数据中的场所数量。

## 工作流程示例

```bash
# 1. Explore what Tel Aviv nightlife looked like in 2008
python3 {baseDir}/scripts/timemap.py timeline 2008

# 2. Filter just the bars
python3 {baseDir}/scripts/timemap.py filter --active-in 2008 --tags bar

# 3. Get details on an interesting venue
python3 {baseDir}/scripts/timemap.py venue "Barby"

# 4. Read user memories about it
python3 {baseDir}/scripts/timemap.py memories "Barby"

# 5. Find nearby venues
python3 {baseDir}/scripts/timemap.py nearby 32.0646 34.7731 --radius 0.5
```

## 注意事项

- **社区维护的数据**：所有历史信息均由 timemap.co.il 的社区成员共同维护。
- **无需 API 密钥**：使用公开的 API 端点，无需身份验证。
- **双语支持**：支持使用希伯来语和英语搜索场所名称。
- **缓存机制**：系统会缓存数据（每天最多调用一次 API，缓存大小约 500KB）。
- **坐标计算**：采用 Haversine 公式进行精确的距离计算。
- **已删除的场所**：系统会自动过滤掉已标记为删除的场所。
- **颜色显示**：在终端上使用 ANSI 颜色显示结果（可通过 `NO_COLOR` 环境变量或 `--no-color` 选项禁用颜色显示）。
- **用户评价**：许多场所都包含用户提交的评价和照片。
- **年份信息**：部分场所的开业/关闭年份为估算值。

## 代理程序使用建议

在集成到自动化系统中时，请务必使用 `--json` 选项以获得结构化的 JSON 输出：

```bash
# Search returns array of matching venues
python3 {baseDir}/scripts/timemap.py search "Barby" --json

# Timeline returns venues active in a year
python3 {baseDir}/scripts/timemap.py timeline 2010 --json

# Stats returns comprehensive database metrics
python3 {baseDir}/scripts/timemap.py stats --json
```

所有命令都支持 `--json` 选项，以便生成格式统一、易于机器读取的输出结果：```json
{
  "ok": true,
  "command": "search",
  "count": 2,
  "venues": [...]
}
```
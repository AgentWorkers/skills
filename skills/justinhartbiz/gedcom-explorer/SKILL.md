---
name: gedcom-explorer
description: **生成交互式家谱仪表板**：  
该工具能够从任何 GEDCOM（.ged）文件中生成交互式的家谱仪表板。它生成一个单文件 HTML 应用程序，包含 5 个标签页（仪表板、家谱、人员信息、时间线、每日提醒），同时提供搜索功能、人员信息查看窗口、图表以及“今日事件”显示功能。适用于需要可视化家谱数据、探索家族历史、构建家谱查看器或处理 GEDCOM 文件的场景。  
相关关键词：家谱、GEDCOM 文件、交互式界面、时间线、人员信息、每日提醒。
---

# GEDCOM Explorer

该工具可以解析任何GEDCOM文件，并生成一个自包含的交互式HTML仪表板。

## 快速入门

```bash
python3 scripts/build_explorer.py <input.ged> [output.html] [--title "Title"] [--subtitle "Subtitle"]
```

### 示例

```bash
# Basic — outputs family-explorer.html in current directory
python3 scripts/build_explorer.py ~/my-family.ged

# Custom output path and title
python3 scripts/build_explorer.py ~/my-family.ged ~/Desktop/hart-family.html \
  --title "Hart Family Tree" --subtitle "Six generations of history"

# Demo with bundled US Presidents data
python3 scripts/build_explorer.py assets/demo-presidents.ged presidents.html \
  --title "Presidential Family Explorer" --subtitle "US Presidents & Their Ancestors"
```

## 功能特点

- **仪表板**：包含统计信息（人物、家族、地点、世代）、“今日事件”、常见姓氏、地理起源信息、按世纪划分的人物列表以及按党派分类的总统信息。
- **家谱树**：支持缩放和平移的交互式可视化功能，可任意选择人物作为家谱的根节点，数据会根据性别或总统身份进行颜色区分。
- **人物信息**：提供可搜索/过滤的功能，支持按性别和总统身份筛选，支持分页查看，点击可进入详细信息页面。
- **时间线**：按时间顺序展示人物的重要事件（出生、死亡、结婚等），支持筛选和搜索。
- **每日提醒**：显示当天的纪念日信息、随机选取的祖先信息以及有趣的家族趣闻。
- **人物详情页面**：展示人物的完整信息，包括父母、配偶和子女的信息（所有链接均可点击）。
- **全局搜索**：支持在所有标签页中通过姓名、地点或年份进行搜索。

## 工作原理

`build_explorer.py`脚本会解析GEDCOM文件，提取其中的人物和家族信息，计算相关统计数据，并将这些数据以内联JSON的形式嵌入到一个HTML文件中。无需服务器支持——只需打开生成的HTML文件即可使用该工具。

该工具能够自动从OCCU（职业）字段中识别出美国总统的信息。该工具支持所有格式的GEDCOM文件；如果文件中不存在总统相关数据，则相关功能将不会显示。

## GEDCOM数据来源

用户可以从以下平台导出`.ged`文件：
- **Ancestry.com** → “Tree Settings” → “Export Tree”
- **FamilySearch.org** → “Download GEDCOM”
- **MyHeritage** → “Family Tree” → “Export” → “GEDCOM”
- 任何家谱软件（如Gramps、RootsMagic、Legacy等）

## 演示数据

`assets/demo-presidents.ged`：一个公开领域的美国总统GEDCOM文件（包含2,322位人物、1,115个家族和44位总统的信息）。来源：webtreeprint.com。

## 本地运行

```bash
cd /path/to/output/dir
python3 -m http.server 8899
# Open http://localhost:8899/family-explorer.html
```

## 扩展功能

生成的HTML文件是完全自包含的。若需进行定制：
- 可通过修改`:root`中的CSS变量来调整页面的主题样式。
- 仪表板会根据GEDCOM文件中的数据自动调整显示内容——即使没有总统数据，该工具也能正常运行。
- 支持与OpenClaw的定时任务集成：可每天解析GEDCOM文件中的事件，并通过Telegram发送“今日事件”通知。
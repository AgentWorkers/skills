---
name: cookidoo
description: 通过 `tmx-cli` 管理 Thermomix/Cookidoo 的膳食计划。该工具可用于搜索食谱、管理每周的膳食计划、生成购物清单、保存常用食谱以及查看食谱详情。当用户提到 Cookidoo、Thermomix、Wochenplan（周计划）、Rezept（食谱）或 Einkaufsliste（购物清单）等与烹饪相关的词汇时，系统会自动触发相关功能。
---

# Cookidoo / tmx-cli 技能

使用 `tmx-cli` 管理 Cookidoo®（Thermomix）的饮食计划、食谱和购物清单。`tmx-cli` 是一个纯 Python 命令行工具（CLI），包含在 `{baseDir}/tmx_cli.py` 文件中。

## 设置

1. **需要 Python 3.9 或更高版本**（无需外部依赖）。
2. **登录**：`python3 {baseDir}/tmx_cli.py login`（通过 OAuth 流程使用 Cookidoo 账户登录）。
3. **设置**（可选）：`python3 {baseDir}/tmx_cli.py setup` — 配置 TM 设备型号、饮食偏好和最大烹饪时间。

## 重要规则

1. **在执行破坏性操作（如清除购物清单或删除饮食计划）前，请务必确认**。
2. **在程序化解析输出时，请使用 `--json` 选项**。
3. **尊重用户设置** — 配置设置会自动应用于后续搜索。

## 命令行使用方法

```
python3 {baseDir}/../tmx-cli/tmx_cli.py <resource> <action> [options]
```

## 核心工作流程

### 搜索食谱
```bash
tmx search "Pasta" --json
tmx search "Kuchen" -n 20 --json              # more results
tmx search "Suppe" -t 30 --json               # max 30 min prep time
tmx search "Salat" -d easy -c vegetarisch --json  # easy + vegetarian
```

筛选条件：`-t <分钟>`、`-d easy|medium|advanced`、`--tm TM5|TM6|TM7`、`-c <类别>`
类别：开胃菜、汤品、意大利面、肉类、鱼类、素食、配菜、甜点、烘焙食品、蛋糕、面包、饮品、基础食谱、酱料、零食

### 食谱详情
```bash
tmx recipe show <recipe_id> --json   # ingredients, steps, nutrition
```

### 饮食计划
```bash
tmx plan show --json                 # current week plan
tmx plan sync                        # sync from Cookidoo
tmx plan add <recipe_id> <day>       # add recipe (day: mon/tue/wed/thu/fri/sat/sun)
tmx plan remove <recipe_id> <day>    # remove from plan
tmx plan move <recipe_id> <from> <to>  # move between days
```

### 购物清单
```bash
tmx shopping show --json             # current list
tmx shopping from-plan               # generate from meal plan
tmx shopping add <recipe_id>         # add recipe ingredients
tmx shopping add-item "Milch" "1L"   # add custom item
tmx shopping remove <recipe_id>      # remove recipe ingredients
tmx shopping clear                   # clear entire list ⚠️
tmx shopping export                  # export as markdown
tmx shopping export --format json    # export as JSON
```

### 今日食谱
```bash
tmx today --json                     # what's on the plan today
```

### 收藏夹
```bash
tmx favorites show --json
tmx favorites add <recipe_id>
tmx favorites remove <recipe_id>
```

## 完整命令参考

有关所有命令、选项和标志的详细信息，请参阅 `{baseDir}/references/commands.md`。
---
name: mealie
description: 通过 REST API 与自托管的 Mealie 实例（食谱管理器和膳食计划工具）进行交互。该 API 可用于添加、更新、检索食谱和膳食计划，以及生成购物清单。当用户提及他们的 Mealie URL、希望导入食谱、创建膳食计划或获取购物清单时，可以触发相应的操作。
---

# Mealie 技能

## 使用场景
- 用户提供 Mealie 的基础 URL（例如：`https://mealie.example.com`）和/或 API 令牌，并请求添加/导入食谱、创建或修改饮食计划、获取购物清单或查询现有食谱。
- 用户希望通过命令行或脚本自动化饮食计划相关的任务。

## 必需的环境变量
```bash
export MEALIE_URL="https://mealie.example.com"   # base URL of the instance
export MEALIE_TOKEN="<your‑jwt‑api‑token>"       # bearer token obtained from Mealie UI (Settings → API Keys)
```
这两个变量必须在运行该技能的 shell 环境中设置。

## 提供的脚本
该技能包含一个小的 Bash 辅助脚本（`scripts/mealie.sh`），该脚本使用 `curl` 来调用 Mealie 的常见 API 接口。

```bash
#!/usr/bin/env bash
# mealie.sh – simple wrapper for Mealie REST API
# Requires MEALIE_URL and MEALIE_TOKEN env vars
set -euo pipefail

cmd=$1; shift
case "$cmd" in
  add-recipe)
    # Usage: mealie.sh add-recipe <path‑to‑json>
    curl -s -X POST "$MEALIE_URL/api/recipes" \
      -H "Authorization: Bearer $MEALIE_TOKEN" \
      -H "Content-Type: application/json" \
      --data @${1}
    ;;
  get-recipe)
    # Usage: mealie.sh get-recipe <recipe‑id>
    curl -s "$MEALIE_URL/api/recipes/${1}" \
      -H "Authorization: Bearer $MEALIE_TOKEN" | jq '.'
    ;;
  create-plan)
    # Usage: mealie.sh create-plan <json‑payload>
    curl -s -X POST "$MEALIE_URL/api/mealplan" \
      -H "Authorization: Bearer $MEALIE_TOKEN" \
      -H "Content-Type: application/json" \
      --data @${1}
    ;;
  get-shopping)
    # Usage: mealie.sh get-shopping <plan‑id>
    curl -s "$MEALIE_URL/api/mealplan/${1}/shopping-list" \
      -H "Authorization: Bearer $MEALIE_TOKEN" | jq '.'
    ;;
  *)
    echo "Unknown command: $cmd" >&2
    exit 1
    ;;
esac
```
使脚本可执行：
```bash
chmod +x scripts/mealie.sh
```

## 如何通过聊天使用该技能
您可以要求我执行特定操作，例如：
- “将这个食谱添加到 Mealie 中。” → 我会要求您提供食谱的 JSON 表示形式，然后运行 `scripts/mealie.sh add-recipe`。
- “显示我当前周饮食计划的购物清单。” → 我会调用 `scripts/mealie.sh get-shopping <plan-id>` 并返回格式化的购物清单。
- “搜索名为 *Spaghetti Bolognese* 的食谱。” → 我会查询 API（`GET /api/recipes?search=Spaghetti%20Bolognese`）并返回匹配结果。

## 扩展该技能
如果您需要额外的功能（例如：标签、分类、批量导入等），只需在 `mealie.sh` 中添加新的功能模块，或在 `scripts/` 目录下创建单独的脚本，并在本次说明文件中引用它们。

---

**注意：** 该技能不会将 API 令牌存储在任何文件中；它依赖于您提供的环境变量。请确保令牌的安全性，并通过 Mealie 的用户界面定期更换令牌。
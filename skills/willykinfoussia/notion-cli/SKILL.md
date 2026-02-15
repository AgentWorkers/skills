---
name: notion-cli
description: Notion CLI（命令行工具）用于创建和管理页面、数据库以及各种内容块（blocks）。
homepage: https://github.com/litencatt/notion-cli
metadata: {"openclaw":{"emoji":"📓","requires":{"env":["NOTION_TOKEN"]},"primaryEnv":"NOTION_TOKEN"}}
---

# notion

使用 *notion-cli* 可以创建/读取/更新页面、数据源（数据库）以及页面中的各个区块。

## 设置

- 安装 notion-cli：`npm install -g @iansinnott/notion-cli`
- 在 https://notion.so/my-integrations 创建一个集成
- 复制 API 密钥（密钥以 *ntn_* 或 *secret_* 开头）
- 将密钥保存到以下路径：
  ```
  mkdir -p ~/.config/notion
  echo "ntn_your_key_here" > ~/.config/notion/api_key
  ```
- 将目标页面/数据库共享给你的集成（点击 “...” → “连接到” → 你的集成名称）

## 使用方法

所有命令都需要设置 *NOTION_TOKEN* 环境变量：

```bash
export NOTION_TOKEN=$(cat ~/.config/notion/api_key)
```

## 常用操作

- **搜索页面和数据源：**
  `notion-cli search --query "页面标题"`
- **获取页面：**
  `notion-cli page retrieve <页面 ID>`
- **获取页面内容（区块）：**
  `notion-cli page retrieve <页面 ID> -r`
- **在数据库中创建页面：**
  ```bash
  curl -X POST https://api.notion.com/v1/pages \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: 2025-09-03" \
    --data '{
      "parent": { "database_id": "YOUR_DATABASE_ID" },
      "properties": {
        "Name": {
          "title": [
            {
              "text": {
                "content": "Nouvelle idée"
              }
            }
          ]
        }
      }
    }'
  ```

- **查询数据库：**
  `notion-cli db query <数据库 ID> -a '{"property":"状态","status":{"equals":"活动"}}'`
- **更新页面属性：**
  ```bash
  curl -X PATCH https://api.notion.com/v1/pages/PAGE_ID \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: 2025-09-03" \
    --data '{
      "properties": {
        "Name": {
          "title": [
            {
              "text": {
                "content": "Nouveau titre"
              }
            }
          ]
        },
        "Status": {
          "status": {
            "name": "In progress"
          }
        },
        "Priority": {
          "select": {
            "name": "High"
          }
        },
        "Due date": {
          "date": {
            "start": "2026-02-10"
          }
        },
        "Description": {
          "rich_text": [
            {
              "text": {
                "content": "Description mise à jour"
              }
            }
          ]
        }
      }
    }'
  ```

- **获取数据库信息：**
  `notion-cli db retrieve <数据库 ID>`

## 属性类型

数据库项的常见属性格式：

- **标题：** `{"title": [{"text": {"content": "..."}}]}`
- **富文本：** `{"rich_text": [{"text": {"content": "..."}}]}`
- **状态：** `{"status": {"name": "选项"}}`
- **单选：** `{"select": {"name": "选项"}}`
- **多选：** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **日期：** `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}`
- **复选框：** `{"checkbox": true}`
- **数字：** `{"number": 42}`
- **URL：** `{"url": "https://..."}`
- **电子邮件：** `{"email": "a@b.com"}`

## 示例

- **搜索页面：**
  `notion-cli search --query "AIStories"`
- **使用过滤器查询数据库：**
  ```bash
  notion-cli db query 2faf172c094981d3bbcbe0f115457cda \
    -a '{
      "property": "Status",
      "status": { "equals": "Backlog" }
    }'
  ```

- **获取页面内容：**
  `notion-cli page retrieve 2fdf172c-0949-80dd-b83b-c1df0410d91b -r`
- **更新页面状态：**
  ```bash
  curl -X PATCH https://api.notion.com/v1/pages/2fdf172c-0949-80dd-b83b-c1df0410d91b \
    -H "Authorization: Bearer $NOTION_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Notion-Version: 2025-09-03" \
    --data '{
      "properties": {
        "Status": {
          "status": {
            "name": "In progress"
          }
        }
      }
    }'
  ```

## 主要特性

- **交互模式：** 对于复杂的查询，运行 `notion-cli db query <数据库 ID>` 无需参数即可进入交互模式
- **多种输出格式：** 表格（默认）、csv、json、yaml
- **原始 JSON：** 使用 `--raw` 标志可获取完整的 API 响应
- **过滤语法：** 使用 `-a` 标志进行包含 AND/OR 条件的复杂过滤

## 注意事项

- 页面/数据库 ID 是 UUID（可能包含或不包含破折号）
- 该命令行工具通过 *NOTION_TOKEN* 自动处理身份验证
- 命令行工具会管理请求速率限制
- 使用 `notion-cli help` 可查看完整的命令参考

## 参考资料

- GitHub Notion-CLI：https://github.com/litencatt/notion-cli
- Notion API 文档：https://developers.notion.com
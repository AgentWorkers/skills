---
name: ecto
description: Ghost.io Admin API CLI 用于管理博客文章、页面、标签和内容。
---

# ecto - Ghost.io 管理 API 命令行工具

通过 Admin API 管理 Ghost.io 博客。支持多站点配置、将 Markdown 格式的内容转换为 HTML 格式，以及生成 JSON 格式的输出以供脚本使用。

## 快速参考

### 认证
```bash
ecto auth add <name> --url <ghost-url> --key <admin-api-key>
ecto auth list
ecto auth default <name>
ecto auth remove <name>
```

环境变量：`GHOST_URL`、`GHOST_ADMIN_KEY`、`GHOST_SITE`

### 文章（Posts）
```bash
ecto posts [--status draft|published|scheduled|all] [--limit N] [--json]
ecto post <id|slug> [--json] [--body]
ecto post create --title "Title" [--markdown-file file.md] [--stdin-format markdown] [--tag tag1,tag2] [--status draft|published]
ecto post edit <id|slug> [--title "New Title"] [--markdown-file file.md] [--status draft|published]
ecto post delete <id|slug> [--force]
ecto post publish <id|slug>
ecto post unpublish <id|slug>
ecto post schedule <id|slug> --at "2025-01-25T10:00:00Z"
```

### 页面（Pages）
```bash
ecto pages [--status draft|published|all] [--limit N] [--json]
ecto page <id|slug> [--json] [--body]
ecto page create --title "Title" [--markdown-file file.md] [--status draft|published]
ecto page edit <id|slug> [--title "New Title"] [--markdown-file file.md]
ecto page delete <id|slug> [--force]
ecto page publish <id|slug>
```

### 标签（Tags）
```bash
ecto tags [--json]
ecto tag <id|slug> [--json]
ecto tag create --name "Tag Name" [--description "desc"]
ecto tag edit <id|slug> [--name "New Name"] [--description "desc"]
ecto tag delete <id|slug> [--force]
```

### 图片（Images）
```bash
ecto image upload <path> [--json]
```

### 站点信息（Site Info）
```bash
ecto site [--json]
ecto settings [--json]
ecto users [--json]
ecto user <id|slug> [--json]
ecto newsletters [--json]
ecto newsletter <id> [--json]
```

### Webhook
```bash
ecto webhook create --event <event> --target-url <url> [--name "Hook Name"]
ecto webhook delete <id> [--force]
```

事件：`post.published`、`post.unpublished`、`post.added`、`postdeleted`、`page.published` 等

## 多站点（Multi-Site）
使用 `--site <名称>` 来指定特定的配置站点：
```bash
ecto posts --site blog2
```

## 常见工作流程

- 从 Markdown 创建并发布文章：
```bash
ecto post create --title "My Post" --markdown-file post.md --tag blog --status published
```

- 从标准输入（stdin）读取内容：
```bash
echo "# Hello World" | ecto post create --title "Quick Post" --stdin-format markdown
```

- 安排文章的发布时间：
```bash
ecto post schedule future-post --at "2025-02-01T09:00:00Z"
```

- 批量发布草稿：
```bash
for id in $(ecto posts --status draft --json | jq -r '.posts[].id'); do
  ecto post publish "$id"
done
```

## 限制
- Ghost API 不支持查看图片或配置 Webhook
- 无法通过 Admin API 管理会员/订阅信息
- 用户只能进行只读操作

## 完整文档
运行 `ecto --ai-help` 可以查看完整的文档。
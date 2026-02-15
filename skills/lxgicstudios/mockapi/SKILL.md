---
name: MockAPI - Instant REST API from JSON
description: 只需几秒钟，就能根据 JSON 文件快速搭建一个模拟的 REST API 服务器。支持完整的 CRUD 操作（创建、读取、更新、删除）、过滤和分页功能，且无需任何配置。这是一个专为前端开发者设计的免费 CLI 工具。
---

# MockAPI

这是一个基于 JSON 文件生成的 REST API，非常适合前端开发、测试和原型设计。

## 安装

```bash
npm install -g @lxgicstudios/mockapi
```

## 快速入门

```bash
# Create example db.json
npx @lxgicstudios/mockapi --init

# Start server
npx @lxgicstudios/mockapi db.json
```

## 数据文件格式

创建 `db.json` 文件：
```json
{
  "users": [
    { "id": 1, "name": "Alice", "email": "alice@example.com" },
    { "id": 2, "name": "Bob", "email": "bob@example.com" }
  ],
  "posts": [
    { "id": 1, "title": "Hello", "body": "Content", "userId": 1 }
  ]
}
```

## 生成的路由

对于每个资源（用户、帖子）：

| 方法 | 路由 | 描述 |
|--------|-------|-------------|
| GET | /users | 列出所有用户 |
| GET | /users/:id | 根据 ID 获取用户信息 |
| POST | /users | 创建新用户 |
| PUT | /users/:id | 更新用户信息 |
| PATCH | /users/:id | 修改用户信息 |
| DELETE | /users/:id | 删除用户信息 |

## 查询参数

```bash
# Filter
GET /users?name=Alice

# Pagination
GET /users?_page=1&_limit=10

# Sort
GET /users?_sort=name&_order=asc
```

## 选项

| 选项 | 描述 |
|--------|-------------|
| `-p, --port` | 端口（默认：3001） |
| `-d, --delay` | 响应延迟（以毫秒为单位） |
| `-w, --watch` | 监视文件是否发生变化 |
| `-r, --readonly` | 禁用数据修改 |
| `--init` | 创建示例 `db.json` 文件 |

## 常见使用场景

**前端开发：**
```bash
npx @lxgicstudios/mockapi db.json --watch
```

**带延迟的演示：**
```bash
npx @lxgicstudios/mockapi db.json --delay 500
```

**只读 API：**
```bash
npx @lxgicstudios/mockapi db.json --readonly
```

## 功能特点

- 支持完整的 CRUD 操作（创建、读取、更新、删除）
- 自动生成唯一 ID
- 支持过滤和分页
- 支持排序功能
- 支持 CORS（跨源资源共享）
- 使用 `--watch` 选项可热重载
- 对 JSON 数据的更改具有持久性

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/mockapi) · [Twitter](https://x.com/lxgicstudios)
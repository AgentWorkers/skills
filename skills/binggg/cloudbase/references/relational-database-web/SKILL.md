---
name: relational-database-web-cloudbase
description: >
  **使用说明：**  
  当构建需要通过 `@cloudbase/js-sdk` 与 CloudBase 关系型数据库进行交互的前端 Web 应用程序时，请使用此文档。该文档提供了标准的初始化（init）模式，使您能够从浏览器中直接使用 Supabase 风格的查询语句。
alwaysApply: false
---
## 何时使用此技能

当您需要通过浏览器应用程序（React、Vue、纯JavaScript）使用 `@cloudbase/js-sdk` 访问 **CloudBase 关系型数据库** 时，请使用此技能。

以下情况适用：
- 在前端初始化 CloudBase 关系型数据库
- 用 CloudBase 关系型数据库替换现有的 Supabase 客户端
- 在整个 Web 应用程序中共享一个 `db` 客户端

**请勿使用此技能进行以下操作：**
- 从后端/Node.js 访问 CloudBase 关系型数据库（请使用 `relation-database-skill` → `node-sdk/quickstart.md`）
- MCP/代理数据库管理（请使用 `relation-database-skill` → `mcp-tools/mcp-guide.md`）
- 身份验证流程（请使用 Web/Node.js 的身份验证相关技能）

## 如何使用此技能（针对编程代理）

1. **确认环境**
   - 询问用户以下信息：
     - `env` – CloudBase 环境 ID

2. **严格按照此文件中的初始化步骤操作**
   - 仅更改 `env` 等值，切勿更改对象的结构。

3. **初始化完成后，使用 Supabase 的相关知识进行查询**
   - 将 `db` 视为 Supabase 客户端使用；方法名称和模式保持一致。

4. **避免重新初始化 CloudBase**
   - 创建一个共享的 `db` 客户端，并在各个组件中重复使用它。

---

## 安装

```bash
npm install @cloudbase/js-sdk
```

## 初始化步骤（标准流程）

```javascript
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({
  env: "your-env-id", // CloudBase environment ID
});

const auth = app.auth();
// Handle user authentication separately (Web Auth skill)

const db = app.rdb();
// Use db exactly like a Supabase client
```

**初始化规则（Web 环境，@cloudbase/js-sdk）：**
- 始终使用上述的同步初始化方式
- **不要** 通过 `import("@cloudbase/js-sdk")` 来延迟加载 SDK
- **不要** 将 SDK 初始化过程包装在 `initCloudBase()` 等异步辅助函数中，并使用内部的 `initPromise` 缓存
- 创建一个共享的 `db` 客户端并重复使用，避免重新初始化

**注意事项：**
- **不要** 在 `cloudbase.init` 的选项中添加新的属性
- 始终调用 `app.rdb()` 来获取数据库客户端；`app` 本身并不是数据库客户端

---

## 情景 1：在 React 应用程序中替换 Supabase 客户端

```javascript
// lib/db.js (shared database client)
import cloudbase from "@cloudbase/js-sdk";

const app = cloudbase.init({
  env: "your-env-id",
});

export const db = app.rdb();
```

```javascript
// hooks/usePosts.js
import { useEffect, useState } from "react";
import { db } from "../lib/db";

export function usePosts() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchPosts() {
      const { data } = await db.from("posts").select("*");
      setPosts(data || []);
    }
    fetchPosts();
  }, []);

  return { posts };
}
```

---

## 情景 2：基本查询模式（Supabase 风格）

```javascript
// Fetch latest posts
const { data, error } = await db
  .from("posts")
  .select("*")
  .order("created_at", { ascending: false });

if (error) {
  console.error("Failed to load posts", error.message);
}
```

---

## 情景 3：插入/更新/删除数据行

```javascript
// Insert
await db.from("posts").insert({ title: "Hello" });

// Update
await db.from("posts").update({ title: "Updated" }).eq("id", 1);

// Delete
await db.from("posts").delete().eq("id", 1);
```

---

## 关键原则：CloudBase 关系型数据库 = Supabase API

- 在获取 `db = app.rdb()` 之后，所有查询都应遵循 **Supabase 的文档和模式**。
- 本技能仅用于标准化 **Web 环境下的初始化过程和客户端共享**。
- 请不要将 Supabase 的文档内容重复写入本技能文件中；查询的格式和选项应依赖于 Supabase 内置的功能。
---
name: PocketBase
description: 使用 PocketBase 的集合功能、身份验证机制以及实时数据处理功能来构建后端系统。
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":["pocketbase"]},"os":["linux","darwin","win32"]}}
---

## SDK 基础知识
- 请从 `pocketbase` 导入相关模块，而非 `pocketbase/dist`——`dist` 路径是内部的，更新后可能会导致问题。
- 在使用 `pb.authStore.model` 之前，务必检查 `pb.authStore.isValid`——过期的令牌会返回错误信息，但数据仍然有效。
- 登录后，令牌会自动附加到请求中——无需手动设置 `Authorization` 头部。

## 获取记录
- 使用 `expand` 参数来加载关联数据：`pb.collection('posts').getList(1, 20, { expand: 'author, comments' })`
- 扩展后的记录会存储在 `record.expand.fieldName` 中，而不是直接在记录对象中。
- 过滤语法类似 SQL，但需要使用单引号：`filter: "status = 'active' && created >= '2024-01-01'"`
- 使用 `&&` 和 `||` 来组合条件，而不是 `AND`/`OR`——SQL 中的关键词在这里不起作用。

## 认证
- 用户集合名为 `users`（小写形式）——使用 `_users` 或 `Users` 会返回空结果。
- `authWithPassword(email, password)` 会返回完整的用户记录及令牌。
- OAuth 流程：`authWithOAuth2({ provider: 'google' })` 会在浏览器中自动弹出登录窗口。
- 登出需要执行 `pb.authStore.clear()`，并且如果令牌在其他地方被使用，还需要在服务器端进行失效处理。

## 实时更新
- 使用 `pb.collection('posts').subscribe(*)` 来订阅记录变化——`*` 表示所有记录的变化。
- 回调函数会接收到 `{ action: 'create'|'update'|'delete', record }`——处理前请检查 `action` 的值。
- 清理时务必取消订阅：`pb.collection('posts').unsubscribe()`——未取消的订阅会导致内存泄漏。

## 文件上传
- 上传文件时需要使用 `FormData`，而不是 JSON：`formData.append('document', file)`，然后将其传递给 `create()` 方法。
- 使用 `pb.files.getURL(record, record.filename)` 获取文件的 URL——不要手动构造 URL。
- 如果需要将多个文件上传到同一个字段，只需使用相同的键多次添加即可。

## 集合规则
- 空规则（`""`）表示对所有人禁止访问；`""`（空字符串）规则表示对所有人开放——这可能有些反直觉。
- 使用 `@request.auth.id` 来引用已登录的用户，使用 `@request.data` 来获取提交的数据。
- 例如，在查看、更新或删除操作中，可以使用 `@request.auth.id = user.id` 来限制访问权限。

## Hook（`pb_hooks()`）
- JavaScript Hook 保存在 `pbhooks/*.pb.js` 文件中——文件必须以 `.pb.js` 为扩展名。
- Hook 会同步执行并阻塞当前请求——请确保它们的执行速度足够快，或者使用其他方式来处理请求。
- 使用 `$app` 来访问应用程序，使用 `e` 来获取事件数据——常见的事件数据包括 `e.record` 和 `e.httpContext`。

## 管理员 API
- 管理员接口需要超级用户权限，不能使用普通用户的令牌。
- 创建管理员令牌：`pb.admins.authWithPassword(email, password)`
- 管理员操作应使用 `pb.admins` 或 `pbcollections`，而不是 `pb.collection()`。
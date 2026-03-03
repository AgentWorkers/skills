---
name: feishu-comments
description: >
  **读取 Feishu 文档中的评论**  
  **使用场景：**  
  - 当用户请求查看/阅读/获取 Feishu 文档中的评论时；  
  - 在审阅文档的反馈时；  
  - 通过评论协作进行文档修订时。
---
# Feishu 文档评论功能

通过 Drive Comment API 从 Feishu 的 docx 文档中获取评论信息。

## 使用要求

- **Feishu 应用程序凭据** 需要在 `~/.openclaw/openclaw.json` 中配置（该文件会从 `channels.feishu` 中读取 `appId` 和 `appSecret`）。
- **系统依赖**：`curl`、`python3`（必须已安装在系统的 PATH 环境变量中）。
- **Feishu 应用程序权限**：需要具有 `docs:document.comment:read` 或 `drive:drive` 权限。

## 使用方法

运行捆绑好的脚本即可获取文档中的所有评论：

```bash
bash skills/feishu-comments/scripts/get_comments.sh <doc_token>
```

若需根据评论 ID 获取特定评论，请使用以下命令：

```bash
bash skills/feishu-comments/scripts/get_comments.sh <doc_token> "id1,id2,id3"
```

请注意，所有路径（如 `skills/`）都是相对于工作区目录计算的。

## 适用场景

- 当 `feishu_doc` 的 `list_blocks` 函数返回了某个块的评论 ID 时。
- 当用户需要审阅或查看文档中的评论时。
- 在文档协作审阅过程中。

## 输出格式

每条评论会显示以下信息：
- 评论 ID、状态（开放/已解决）、范围（全局/本地）。
- 引用的文本内容（针对本地或内联评论）。
- 所有的回复信息，包括回复用户的 ID 和回复内容。

## 提取 doc_token 的方法

从 URL `https://xxx.feishu.cn/docx/ABC123def` 中可以提取 doc_token，其值为 `ABC123def`。

对于 wiki 页面，首先需要使用 `feishu_wiki` 获取 `obj_token`，然后再将其作为 doc_token 使用。

## 工作原理

捆绑好的 shell 脚本执行以下步骤：
1. 从 `~/.openclaw/openclaw.json` 中读取 Feishu 应用程序凭据（`appId`、`appSecret`）。
2. 通过 Feishu 的认证 API 获取 `tenant_access_token`。
3. 调用 Drive Comment API 来列出并批量查询评论。
4. 将评论内容格式化后输出到标准输出（stdout）。

所有数据仅传输到 Feishu/Lark 的 API 端点，不会泄露给任何第三方。

## 限制

- 仅支持读取评论功能（无法创建或回复评论）。
- API 错误响应会输出到标准错误流（stderr）中，可能包含请求 ID，但不会包含敏感数据。
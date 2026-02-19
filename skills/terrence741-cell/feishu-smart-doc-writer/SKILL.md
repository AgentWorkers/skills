---
name: feishu-smart-doc-writer
description: >
  **Feishu/Lark Smart Document Writer - 飞书智能文档写入器**
  该工具通过自动将长文档分割成多个部分进行传输，并自动处理文档所有权的转移，有效解决了因API限制导致的文档显示问题。首次使用时，系统会自动引导用户完成OpenID的配置。
---
# Feishu 智能文档编写工具

## 主要功能

- **自动分块编写**：将长篇内容分割成多个小块，避免生成空白的文档。
- **自动转移文档所有权**：在文档创建后自动将所有权转移给指定用户。
- **首次使用指南**：首次使用时会自动提示用户配置 OpenID。

## 提供的工具

- `write_smart`：用于创建包含自动分块功能的文档，并自动转移文档所有权。
- `append_smart`：用于向文档中添加内容，同时支持自动分块功能。
- `transfer_ownership`：用于转移文档的所有权。
- `configure`：用于配置 OpenID 的相关信息。
- `get_config_status`：用于查看配置状态。

## 快速入门步骤

1. 首次使用：运行 `write_smart`，系统会引导您完成 OpenID 的配置。
2. 登录 Feishu 管理控制台 → 访问“权限管理”模块。
3. 授予用户 `docs:permission.member:transfer` 权限。
4. 发布新版本的文档。
5. 在相关技能中配置用户的 OpenID。
6. 完成！之后创建的文档将自动转移所有权。
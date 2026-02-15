---
name: stitch-ui-designer
version: 1.0.0
description: 使用 Google Stitch（通过 MCP）进行 UI 设计、预览和代码生成。该工具通过首先生成预览图来帮助开发者选择最佳的 UI 设计方案，支持迭代修改，最后可导出相应的 UI 代码。
metadata:
  openclaw:
    emoji: 🎨
    requires:
      bins: ["npx", "mcporter"]
---

# Stitch UI Designer

此技能允许您使用 Google Stitch 设计高质量的用户界面。

## 工作流程

请按照以下步骤帮助用户设计用户界面：

1. **设置（仅首次使用）**
   - 检查 `mcporter` 中是否配置了 `stitch` 服务器。
   - 如果未配置，请执行以下操作：`mcporter config add stitch --command "npx" --args "-y stitch-mcp-auto"`
   - 确保用户已使用 Google Cloud 进行身份验证（工具可能会提示您执行 `gcloud auth`）。

2. **生成并预览**
   - 询问用户对界面的需求（例如：“一个加密应用的登录界面”）。
   - 使用 `stitch.generate_screen_from_text` 根据用户的描述生成界面。
   - **重要提示**：此操作会返回一个 `screenId`。
   - 立即使用 `stitch.fetch_screen_image(screenId)` 获取预览图像，并将其展示给用户。此时**不要**获取界面的代码。

3. **迭代与定制**
   - 向用户征求对预览效果的反馈。
   - 如果需要修改，再次使用 `stitch.generate_screen_from_text`（可以根据前一个界面的设计内容使用 `stitch.extract_design_context` 以保持样式一致），或直接优化提示内容。
   - 将新的预览结果展示给用户。

4. **导出代码**
   - 当用户确认设计满意后（例如：“这个设计很棒”），获取界面的代码。
   - 使用 `stitch.fetch_screen_code(screenId)` 获取 HTML/CSS 代码，并根据用户的要求将其保存到文件中。

## 工具（通过 `mcporter` 调用）

使用 `mcporter call stitch.<tool_name> <args>` 来调用这些工具：

- **generate_screen_from_text**
  - 参数：`prompt`（字符串），`projectId`（可选，通常由 `stitch-mcp-auto` 自动检测）
  - 返回值：`screenId`、`name`、`url`
  - **用途**：用于开始界面设计。

- **fetch_screen_image**
  - 参数：`screenId`（字符串）
  - 返回值：界面图像数据（用于展示给用户）
  - **用途**：用于展示预览图像。

- **fetch_screen_code**
  - 参数：`screenId`（字符串）
  - 返回值：HTML、CSS 等代码
  - **用途**：仅在用户确认设计后使用。

- **create_project**
  - 参数：`name`（字符串）
  - **用途**：在项目不存在时使用。

## 提示

- **项目上下文**：`stitch-mcp-auto` 会尝试自动管理项目 ID。如果出现项目 ID 缺失的错误，请让用户先使用 `create_project` 创建项目，或通过设置 `GOOGLE_CLOUD_PROJECT` 环境变量来指定项目 ID。
- **优先预览**：始终优先考虑界面的视觉效果。为糟糕的设计生成代码会浪费令牌和时间。
- **使用 `stitch-mcp-auto`**：我们选择使用 `stitch-mcp-auto`，因为它比标准包更优雅地处理复杂的 Google 认证流程。
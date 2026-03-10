---
name: nicebox-site-manager
description: 通过 NiceBox OpenClaw API 管理由 AI 构建的网站。支持发布文章、查看消息以及检查网站状态。
metadata: {"clawdbot":{"emoji":"🛠️","requires":{"bins":["python3"],"env":["AIBOX_API_KEY"]},"primaryEnv":"AIBOX_API_KEY"}}
---
# NiceBox 网站管理器

通过 NiceBox OpenClaw API 管理由 AI 生成的网站。

**基础 URL:**
```bash
https://ai.nicebox.cn/api/openclaw
```

**身份验证:**
```bash
Authorization: $AIBOX_API_KEY
```

该技能提供以下三个主要功能：

* **发布文章**：向您的网站发布文章。
  **用法:**
  ```bash
  nicebox publish --title="文章标题" --content="文章内容" --summary="文章摘要" --author="作者名称" --cover="封面图片URL" --status="draft" 或 "publish"
  ```
  **选项:**
  - `--title`: 文章标题（必填）
  - `--content`: 文章内容（通常为 HTML 格式，必填）
  - `--summary`: 文章摘要（可选）
  - `--author`: 作者名称（可选）
  - `--cover`: 封面图片 URL（可选）
  - `--status`: `draft` 或 `publish`（默认值：`publish`）

* **查看消息**：列出网站上的消息、咨询或潜在客户信息。
  **用法:**
  ```bash
  nicebox message --page=1 --page-size=20 --is-read=0
  ```
  **选项:**
  - `--page`: 页码（默认值：`1`）
  - `--page-size`: 每页显示的条目数量（默认值：`20`）
  - `--is-read`: 按阅读状态过滤：`0` 未读 / `1` 已读（可选）

* **检查网站状态**：查看网站的当前状态。
  **用法:**
  ```bash
  nicebox status
  ```
  **无其他选项**

**环境设置**

在使用此技能之前，请设置您的 API 密钥：
```bash
export AIBOX_API_KEY="your_api_key"
```

**基础 URL 的可选覆盖配置:**
```bash
export AIBOX_BASE_URL="https://ai.nicebox.cn/api/openclaw"
```

**默认端点假设**

该技能假设以下 API 路径：
- `POST /article/publish`：用于发布文章
- `GET /message/getlist`：用于获取消息列表
- `GET /site/status`：用于获取网站状态

如果您的后端实际使用不同的路径，请更新 Python 脚本中的 `ENDPOINT_*` 常量。

**注意事项:**
- 所有请求均使用 HTTP `Authorization` 头部。
- API 密钥以纯文本形式发送：
  ```
  Authorization: YOUR_KEY
  ```
- 输出结果以格式化的 JSON 格式提供，便于调试和代理使用。
- 如果您的 API 字段名称有所不同，请更新脚本中的数据字段。
---
name: doko
description: Dokobot工具：能够读取网页、搜索互联网、列出已连接的Doko设备，并更新技能定义。
compatibility: Requires curl and DOKO_API_KEY environment variable.
allowed-tools: Bash
metadata:
  author: dokobot
  version: "1.0"
---
# Dokobot 工具

Dokobot 提供了一系列 API 工具。所有命令都需要设置 `DOKO_API_KEY` 环境变量。

**使用方法**: `/doko <命令> [参数]`

**命令说明**: `$ARGUMENTS[0]` 表示命令的具体参数。

## 先决条件
- `DOKO_API_KEY` 必须已在环境中设置（请在 `.claude/settings.local.json` 文件中进行配置）。
- 如果未设置 API 密钥，请用户前往 Dokobot 控制面板（https://dokobot.ai/dashboard/api-keys）创建一个密钥。

## 命令列表

### read
通过 Chrome 扩展程序读取网页内容并返回结果。

**使用方法**: `/doko read <URL> <目标>`

**使用要求**:
- 必须打开 Chrome 浏览器，并安装了 Dokobot 扩展程序。
- 用户需登录并启用远程控制功能。
- **参数说明**:
  - `URL`：要读取的网页地址。
  - `goal`：指定需要提取的网页内容部分（例如：“前 10 条评论”或“上周的评论”）。

**响应字段**:
- `data.text`：提取的网页内容（纯文本格式）。
- `data.chunks`：包含页面布局信息的内容片段。
- `data.stats.stopReason`：提取操作停止的原因（可能是 AI 识别错误、超时或滚动到页面底部）。

**并发限制**:
- 可以同时执行多个 `read` 请求（每个请求会在单独的浏览器标签页中运行）。建议的最大并发请求数量为 **5 个**。超过这个数量后，由于浏览器资源共享的原因，性能会下降。

### search
在网页上搜索并返回搜索结果。

**使用方法**: `/doko search <查询内容>`

**参数说明**:
- `query`：搜索查询内容。

**响应字段**:
- `items`：包含搜索结果的数组（每个结果包含 `title`、`link` 和 `snippet`）。
- `directAnswer`：如果存在，会显示特色搜索结果或答案框。
- `knowledgeGraph`：如果存在，会显示相关知识面板的信息（包含 `title` 和 `description`）。

### dokos
Dokos 被视为“有生命的实体”，而非简单的设备。

**使用方法**: `/doko dokos`

**响应内容**:
`{"dokos": [{"id": "<设备ID>", "name": "<设备名称>", "age": "创建时间 3 天"}]`。当多个浏览器连接到 Dokobot 时，可以使用 `id` 作为 `read-page` 命令的参数。

### update
从服务器获取最新的技能定义，并覆盖当前的技能文件。

**使用方法**: `/doko update`

**更新后的操作**:
更新完成后，系统会显示一个简短的差异总结。

## 错误处理
- 401：API 密钥无效——请用户检查 `DOKO_API_KEY` 是否正确设置。
- 403：API 密钥权限不足。
- 422：操作失败或被用户取消（仅限读取操作）。
- 503：没有浏览器扩展程序连接到 Dokobot（仅限读取操作）——请检查 `read` 命令的使用要求。
- 504：超时——对于内容较长的网页，读取操作可能需要最多 5 分钟的时间。
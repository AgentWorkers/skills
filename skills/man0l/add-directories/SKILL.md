---
name: add-directories
description: >
  **用途：**  
  当需要从 URL、粘贴的文本或 GitHub 的 `awesome-list` 中添加新的 AI/创业项目目录到 `directories.json` 文件时使用该工具。该工具会解析这些数据，消除重复项，将新条目添加到文件中，随后执行 `classify` 流程（包括分析、清理和浏览器验证等步骤）。请注意：该工具不负责项目的提交过程——提交相关操作请使用 `submit-directories` 工具。
---
# 添加目录

## 工作流程

1. **解析** 输入内容（URL或粘贴的文本），将其转换为目录列表。
2. **与 `directories.json` 中的现有条目进行去重**。
3. **添加** 新条目，并填写必要的字段。
4. **通过运行分析及验证流程对目录进行分类**。
5. **查找用于提交的表单**。
6. **通过自动化方式或手动浏览器操作进行提交**。

## 第一步：解析输入

### 从 URL 中提取目录信息

获取页面内容并提取目录条目。注意以下模式：
- 列表、表格或卡片中的“名称”与“URL”组合。
- 结构化数据（JSON-LD、Markdown 表格、CSV 格式）。
- 包含链接的重复 DOM 结构。

### 从 GitHub 主题/仓库中提取目录信息

使用 `gh` CLI 查看精选的目录列表：
- `gh repo clone <owner>/<repo>` 可以克隆相关仓库。
- 解析 `README.md` 文件中的目录链接（Markdown 链接格式）。
- 检查是否存在包含目录条目的 JSON/YAML 数据文件。
- 也可以提交 PR 将你的产品添加到这些列表中。

### 从粘贴的文本中提取目录信息

解析文本行。常见的格式包括：
- `名称 - https://url.com` 或 `名称 | https://url.com`
- Markdown 链接：`[名称](https://url.com)`
- 包含“名称”和“URL”列的 Markdown 表格
- 单独的 URL（每行一个）——从域名中提取名称
- 带有标题的 CSV/TSV 文件

至少需要提取以下信息：**名称** 和 **URL**（用于提交或访问主页）。

## 第二步：去重

加载 `directories.json`，并将每个解析后的条目与现有条目进行比较：
- **URL 完全匹配**（处理方式：去掉路径末尾的斜杠，将域名转换为小写）。
- **域名匹配**（相同域名可能表示重复条目）。
- **名称匹配**（不区分大小写）。

将重复条目报告给用户并跳过它们。

## 第三步：添加新条目

对于每个新目录，创建一个条目，其结构如下：

```json
{
  "categories": ["General"],
  "description": "",
  "is_active": true,
  "name": "Directory Name",
  "pricing_type": "free",
  "slug": "directory-name",
  "submission_url": "https://example.com/submit",
  "url": "https://example.com/submit"
}
```

字段规则：
- `slug`：使用小写名称，用空格替换特殊字符。
- `submission_url` 和 `url`：如果可用，请使用提交/注册页面的 URL，否则使用主页 URL。
- `description`：留空字符串（后续填写或由用户提供）。
- `categories`：默认为 `["General"]`，除非有特定分类要求。
- `pricing_type`：默认为 `"free"`，除非明确标记为付费。
- `is_active`：新条目始终设置为 `true`。

保存更新后的 `directories.json` 文件。

## 第四步：分类

使用项目虚拟环境（`.venv/` 下的脚本依次运行分类流程：

```bash
# 1. HTTP-level analysis (auth, captcha, pricing signals, dead domains)
.venv/bin/python analyze_directories.py

# 2. Cleanup obvious failures + build browser check list
.venv/bin/python cleanup_and_categorize.py

# 3. Browser verification with Playwright (10 concurrent workers)
.venv/bin/python browser_verify.py

# 4. Deep recheck any remaining unknowns
.venv/bin/python browser_verify.py --recheck-unknown
```

每个脚本都会读取/写入 `directories.json` 文件。步骤 3-4 会使用 `browser_check_list.json` 作为中间状态文件（由步骤 2 生成）。

完成后，报告新增目录的数量以及新条目的授权状态分布。

## 第五步：查找表单

对于那些处于活跃状态且 `auth_type` 为 `none` 或 `auth_type` 为 `email_password` 的目录：

```bash
# Discover form fields on submission pages
.venv/bin/python discover_forms.py
```

使用 Playwright 访问每个提交页面，通过 DOM 查询提取表单字段，并更新 `submission_plan.json` 文件。

## 第六步：提交

### 自动提交

在 `submit_directories.py` 中配置产品信息（替换 `YOUR_` 占位符），然后执行以下操作：

```bash
# Auto-submit to all discovered directories
.venv/bin/python submit_directories.py
```

脚本会使用启发式方法将字段名称与产品数据匹配，并处理徽标/截图的上传。

### 手动浏览器提交（使用 Playwright MCP）

对于需要手动操作的目录（如验证码、OAuth 验证或复杂表单），请按照以下步骤操作：
1. 导航到提交页面。
2. 打印页面快照以了解页面结构。
3. 使用 `browser_fill_form` 或 `browser_type` 填写表单字段。
4. 在 Google 登录弹窗出现时切换标签页。
5. 使用 `browser_file_upload` 上传文件。
6. 点击提交按钮并验证提交结果。

### 通过 GitHub PR 提交

某些目录支持通过 GitHub PR 将产品添加到相关列表中：
1. 克隆仓库：`gh repo fork <owner>/<repo>`
2. 创建一个新的分支。
3. 按照仓库的格式添加你的产品条目。
4. 提交更改并创建 PR：`gh pr create`

## 注意事项

### 流程脚本说明
- `analyze_directories.py` 使用 `ThreadPoolExecutor` 和简单的 HTTP 请求进行初步处理。
- `cleanup_and_categorize.py` 处理错误（无效域名、失效 URL、Facebook 群组等），并生成 `browser_check_list.json` 文件。
- `browser_verify.py` 使用异步 Playwright 并打开 10 个标签页；`--recheck-unknown` 选项仅对活跃的未知目录进行深度 DOM 检查。
- `discover_forms.py` 使用异步 Playwright 并打开 10 个标签页；提取表单字段的名称、类型和路径。
- `submit_directories.py` 使用异步 Playwright 并打开 5 个标签页；支持字段匹配和文件上传。
- 所有脚本都是幂等的，可以安全地重复执行。

### 常见提交障碍

在评估或提交目录时，请注意以下问题：
| 障碍 | 出现频率 | 检测方法 |
|---|---|---|
| **需要付费列表** | 约 20% | 查找定价页面、Stripe/PayPal 链接或提交页面上的 “$” 符号 |
| **reCAPTCHA / Turnstile** | 约 10% | 页面中存在 `iframe[src*=recaptcha]` 或 `[data-turnstile]` 元素 |
| **验证码失效** | 约 2% | 出现 “Invalid site key” 错误或提交按钮被禁用 |
| **需要登录/注册** | 约 15% | 提交页面会重定向到 `/login` 或 `/register` |
| **需要企业邮箱** | 约 3% | 拒绝接受 gmail/yahoo 域名的提交 |
| **需要反向链接** | 约 5% | 一些旧网站要求提供反向链接才能添加目录 |
| **仅限订阅的表单** | 约 10% | 表面看起来是提交页面，但实际上是邮箱注册页面 |
| **后端 API 故障** | 约 2% | 表单可以提交，但返回 GraphQL/API 错误 |
| **域名被挂载/失效** | 约 8% | 页面无内容、为挂载页面或 DNS 故障 |
| **Cloudflare 阻止访问** | 约 3% | 出现挑战页面或 403 错误 |

### 自动化提交技巧
- **简单的 HTML 表单** 的自动提交成功率最高。
- **reCAPTCHA v3**（不可见的验证码）有时可以自动通过；**v2**（复选框形式的验证码** 无法自动提交。
- **Google 表单** 可以可靠地自动提交。
- **富文本编辑器（如 TinyMCE、Quill）** 需要使用 `browser_evaluate` 函数来设置内容。
- **Cloudinary/自定义上传组件** 常常会导致自动化失败——建议手动操作。
- **跨源 OAuth 流程**：使用 `browser_tabs` 功能切换标签页以完成 Google 登录。
- **下拉框/选择框**：先点击下拉框，再点击所需选项。
- **多步骤表单**：在每个步骤后打印页面快照以查看新出现的字段。

### 提交计划结构

`submission_plan.json` 中的每个条目包含以下状态值：
- `discovered`（已发现）
- `submitted`（已提交）
- `skipped`（跳过）
- `skipped_paid`（跳过付费选项）
- `timeout`（超时）
- `no_form_found`（未找到表单）
- `no_fieldsmatched`（未匹配到表单字段）
- `submit_timeout`（提交超时）
- `captcha`（验证码相关问题）
- `cloudflare_blocked`（Cloudflare 阻止访问）
- `domain_parked`（域名被挂载）
- `skipped_login_required`（需要登录）
- `deferred`（提交延迟）

### 最具投资回报率的目录类型（适用于 AI/SaaS 产品）

1. **具有简单表单的 AI 工具目录**（如 FutureTools、SaaSHub、AItools.inc 等）。
2. **支持 GitHub PR 的创业公司目录**（免费提交，可提供高质量反向链接）。
3. **支持 PR 的 NoCode/SaaS 综合平台**（如 NoCodeList、NoCodeDevs）。
4 **DA（域名权威度）≥30 的通用网站目录**（有助于提高 SEO 效果）。

### 安全注意事项

在将数据推送到 GitHub 之前，请确保删除所有个人信息：
- 在 `submission_plan.json` 和 `submit_directories.py` 中查找 `YOUR_` 占位符。
- 绝不要提交真实的电子邮件地址、密码或 API 密钥。
- `.playwright-mcp/` 文件夹可能包含包含个人信息的控制台日志——请将其添加到 `.gitignore` 文件中。
---
name: linkedin
description: >
  LinkedIn自动化技能：  
  - 搜索人员及公司；  
  - 获取个人资料；  
  - 发送消息和内部邮件（InMails）；  
  - 管理联系人；  
  - 创建帖子；  
  - 回复评论；  
  - 支持Sales Navigator功能。
---
# LinkedIn Skill

您可以使用 `linkedin`——这是一个用于自动化操作 LinkedIn 的命令行工具。通过它，您可以获取个人资料、搜索人员和企业、发送消息、管理联系、创建帖子、做出反应、发表评论等。

每个命令都会向 LinkedIn 的 API 发送请求，该 API 会使用真实的云浏览器在 LinkedIn 上执行相应的操作。操作 **不是即时完成的**——根据复杂程度，可能需要 30 秒到几分钟的时间。

如果 `linkedin` 未安装，请先进行安装：

```bash
npm install -g @linkedapi/linkedin-cli
```

## 认证

如果某个命令以退出代码 2（认证错误）失败，请让用户设置他们的账户：

1. 访问 [app.linkedapi.io](https://app.linkedapi.io) 并注册或登录
2. 将他们的 LinkedIn 账户关联到该工具
3. 从仪表板复制 **Linked API Token** 和 **Identification Token**

用户提供这些令牌后，可以继续使用该工具：

```bash
linkedin setup --linked-api-token=TOKEN --identification-token=TOKEN
```

## 全局参数

为了使输出更易于机器读取，请始终使用 `--json` 和 `-q` 参数：

```bash
linkedin <command> --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--json` | 结构化 JSON 输出 |
| `--quiet` / `-q` | 抑制 stderr 进度信息 |
| `--fields name,url,...` | 在输出中选择特定字段 |
| `--no-color` | 禁用颜色显示 |
| `--account "Name"` | 为该命令指定特定的账户 |

## 输出格式

成功时：
```json
{"success": true, "data": {"name": "John Doe", "headline": "Engineer"}}
```

出错时：
```json
{"success": false, "error": {"type": "personNotFound", "message": "Person not found"}}
```

退出代码 0 表示 API 调用成功——请始终检查 `success` 字段以获取操作结果。非零的退出代码表示存在基础设施错误：

| 出口代码 | 含义 |
|-----------|---------|
| 0 | 成功（请检查 `success` 字段——操作可能返回了错误信息，例如“未找到该人员”） |
| 1 | 一般性/意外错误 |
| 2 | 令牌缺失或无效 |
| 3 | 需要订阅或购买相应计划 |
| 4 | LinkedIn 账户问题 |
| 5 | 参数无效 |
| 6 | 被限制了使用频率 |
| 7 | 网络错误 |
| 8 | 工作流超时（返回 workflowId 以供恢复使用） |

## 命令

### 获取个人资料

```bash
linkedin person fetch <url> [flags] --json -q
```

可选参数（用于获取额外信息）：
- `--experience` – 工作经历 |
- `--education` – 教育背景 |
- `--skills` – 技能列表 |
- `--languages` – 使用的语言 |
- `--posts` – 最新帖子（使用 `--posts-limit N` 或 `--posts-since TIMESTAMP`） |
- `--comments` – 最新评论（使用 `--comments-limit N` 或 `--comments-since TIMESTAMP`） |
- `--reactions` – 最新反应（使用 `--reactions-limit N` 或 `--reactions-since TIMESTAMP`） |

仅在需要时请求额外信息——每个参数都会增加执行时间。

```bash
# Basic profile
linkedin person fetch https://www.linkedin.com/in/username --json -q

# With experience and education
linkedin person fetch https://www.linkedin.com/in/username --experience --education --json -q

# With last 5 posts
linkedin person fetch https://www.linkedin.com/in/username --posts --posts-limit 5 --json -q
```

### 搜索人员

```bash
linkedin person search [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--term` | 搜索关键词或短语 |
| `--limit` | 最大搜索结果数量 |
| `--first-name` | 按名字筛选 |
| `--last-name` | 按姓氏筛选 |
| `--position` | 按职位筛选 |
| `--locations` | 用逗号分隔的位置 |
| `--industries` | 用逗号分隔的行业 |
| `--current-companies` | 用逗号分隔的当前公司名称 |
| `--previous-companies` | 用逗号分隔的之前工作过的公司名称 |
| `--schools` | 用逗号分隔的学校名称 |

```bash
linkedin person search --term "product manager" --locations "San Francisco" --json -q
linkedin person search --current-companies "Google" --position "Engineer" --limit 20 --json -q
```

### 获取公司信息

```bash
linkedin company fetch <url> [flags] --json -q
```

可选参数：
- `--employees` | 包含员工信息 |
- `--dms` | 包含决策者信息 |
- `--posts` | 包含公司发布的帖子 |

员工筛选参数（需要 `--employees`）：

| 参数 | 说明 |
|------|-------------|
| `--employees-limit` | 最多返回的员工数量 |
| `--employees-first-name` | 按名字筛选员工 |
| `--employees-last-name` | 按姓氏筛选员工 |
| `--employees-position` | 按职位筛选员工 |
| `--employees-locations` | 用逗号分隔的员工工作地点 |
| `--employees-industries` | 用逗号分隔的员工所属行业 |
| `--employees-schools` | 用逗号分隔的员工就读过的学校名称 |

| 参数 | 说明 |
|------|-------------|
| `--dms-limit` | 最多返回的决策者数量（需要 `--dms`） |
| `--posts-limit` | 最多返回的帖子数量（需要 `--posts`） |
| `--posts-since` | 帖子的发布时间（需要 `--posts`） |

```bash
# Basic company info
linkedin company fetch https://www.linkedin.com/company/name --json -q

# With employees filtered by position
linkedin company fetch https://www.linkedin.com/company/name --employees --employees-position "Engineer" --json -q

# With decision makers and posts
linkedin company fetch https://www.linkedin.com/company/name --dms --posts --posts-limit 10 --json -q
```

### 搜索公司

```bash
linkedin company search [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--term` | 搜索关键词 |
| `--limit` | 最大搜索结果数量 |
| `--sizes` | 用逗号分隔的公司规模：`1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `5001-10000`, `10001+` |
| `--locations` | 用逗号分隔的位置 |
| `--industries` | 用逗号分隔的行业 |

```bash
linkedin company search --term "fintech" --sizes "11-50,51-200" --json -q
```

### 发送消息

```bash
linkedin message send <person-url> '<text>' --json -q
```

消息长度最多为 1900 个字符。请将消息放在单引号中，以避免 shell 解释错误。

```bash
linkedin message send https://www.linkedin.com/in/username 'Hey, loved your latest post!' --json -q
```

### 获取对话记录

```bash
linkedin message get <person-url> [--since TIMESTAMP] --json -q
```

首次获取对话记录时可能会触发后台同步，因此耗时较长。后续请求会更快。

```bash
linkedin message get https://www.linkedin.com/in/username --json -q
linkedin message get https://www.linkedin.com/in/username --since 2024-01-15T10:30:00Z --json -q
```

### 联系管理

#### 检查联系状态

```bash
linkedin connection status <url> --json -q
```

#### 发送联系请求

```bash
linkedin connection send <url> [--note 'text'] [--email user@example.com] --json -q
```

#### 列出联系信息

```bash
linkedin connection list [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--limit` | 最多返回的联系数量 |
| `--since` | 仅返回自指定 ISO 时间戳以来的联系 |
| `--first-name` | 按名字筛选联系 |
| `--last-name` | 按姓氏筛选联系 |
| `--position` | 按职位筛选联系 |
| `--locations` | 用逗号分隔的位置 |
| `--industries` | 用逗号分隔的行业 |
| `--current-companies` | 用逗号分隔的当前公司名称 |
| `--previous-companies` | 用逗号分隔的之前工作过的公司名称 |
| `--schools` | 用逗号分隔的学校名称 |

```bash
linkedin connection list --limit 50 --json -q
linkedin connection list --current-companies "Google" --position "Engineer" --json -q
linkedin connection list --since 2024-01-01T00:00:00Z --json -q
```

#### 列出待处理的发送请求

```bash
linkedin connection pending --json -q
```

#### 取消待处理的请求

```bash
linkedin connection withdraw <url> [--no-unfollow] --json -q
```

默认情况下，取消请求的同时也会取消关注。使用 `--no-unfollow` 选项可以保持关注状态。

#### 取消联系

```bash
linkedin connection remove <url> --json -q
```

### 帖子

#### 获取帖子信息

```bash
linkedin post fetch <url> [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--comments` | 包含评论 |
| `--reactions` | 包含反应 |
| `--comments-limit` | 最多返回的评论数量（需要 `--comments`） |
| `--comments-sort` | 排序方式：`mostRelevant` 或 `mostRecent`（需要 `--comments`） |
| `--comments-replies` | 包含评论的回复（需要 `--comments`） |
| `--reactions-limit` | 最多返回的反应数量（需要 `--reactions`） |

```bash
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 --json -q

# With comments sorted by most recent, including replies
linkedin post fetch https://www.linkedin.com/posts/username_activity-123 \
  --comments --comments-sort mostRecent --comments-replies --json -q
```

#### 创建帖子

```bash
linkedin post create '<text>' [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--company-url` | 代表公司页面发布帖子（需要管理员权限） |
| `--attachments` | 附件格式：`url:type` 或 `url:type:name`。支持 `image`, `video`, `document`。可以多次指定。 |

附件限制：最多 9 张图片，或 1 个视频，或 1 份文档。不允许混合使用不同类型的附件。

```bash
linkedin post create 'Excited to share our latest update!' --json -q

# With a document
linkedin post create 'Our Q4 report' \
  --attachments "https://example.com/report.pdf:document:Q4 Report" --json -q

# Post as a company
linkedin post create 'Company announcement' \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### 对帖子做出反应

```bash
linkedin post react <url> --type <reaction> [--company-url <url>] --json -q
```

反应类型：`like`, `love`, `support`, `celebrate`, `insightful`, `funny`。

```bash
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type like --json -q

# React on behalf of a company
linkedin post react https://www.linkedin.com/posts/username_activity-123 --type celebrate \
  --company-url https://www.linkedin.com/company/name --json -q
```

#### 评论帖子

```bash
linkedin post comment <url> '<text>' [--company-url <url>] --json -q
```

评论长度最多为 1000 个字符。

```bash
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Great insights!' --json -q

# Comment on behalf of a company
linkedin post comment https://www.linkedin.com/posts/username_activity-123 'Well said!' \
  --company-url https://www.linkedin.com/company/name --json -q
```

### 统计信息

```bash
# Social Selling Index
linkedin stats ssi --json -q

# Performance analytics (profile views, post impressions, search appearances)
linkedin stats performance --json -q

# API usage for a date range
linkedin stats usage --start 2024-01-01T00:00:00Z --end 2024-01-31T00:00:00Z --json -q
```

### 销售导航器

需要订阅 LinkedIn 销售导航器服务。该服务使用哈希 URL 进行人员/公司信息查询。

#### 获取人员信息

```bash
linkedin navigator person fetch <hashed-url> --json -q
```

#### 搜索人员

```bash
linkedin navigator person search [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--term` | 搜索关键词或短语 |
| `--limit` | 最大搜索结果数量 |
| `--first-name` | 按名字筛选 |
| `--last-name` | 按姓氏筛选 |
| `--position` | 按职位筛选 |
| `--locations` | 用逗号分隔的位置 |
| `--industries` | 用逗号分隔的行业 |
| `--current-companies` | 用逗号分隔的当前公司名称 |
| `--previous-companies` | 用逗号分隔的之前工作过的公司名称 |
| `--schools` | 用逗号分隔的学校名称 |
| `--years-of-experience` | 经验年限范围：`lessThanOne`, `oneToTwo`, `threeToFive`, `sixToTen`, `moreThanTen` |

```bash
linkedin navigator person search --term "VP Marketing" --locations "United States" --json -q
linkedin navigator person search --years-of-experience "moreThanTen" --position "CEO" --json -q
```

#### 获取公司信息

```bash
linkedin navigator company fetch <hashed-url> [flags] --json -q
```

可选参数：
- `--employees` | 包含员工信息 |
- `--dms` | 包含决策者信息 |

员工筛选参数（需要 `--employees`）：

| 参数 | 说明 |
|------|-------------|
| `--employees-limit` | 最多返回的员工数量 |
| `--employees-first-name` | 按名字筛选员工 |
| `--employees-last-name` | 按姓氏筛选员工 |
| `--employees-positions` | 按职位筛选员工 |
| `--employees-locations` | 用逗号分隔的员工工作地点 |
| `--employees-industries` | 用逗号分隔的员工所属行业 |
| `--employees-schools` | 用逗号分隔的员工就读过的学校名称 |
| `--employees-years-of-experience` | 经验年限范围 |
| `--dms-limit` | 最多返回的决策者数量（需要 `--dms`） |

```bash
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural --employees --dms --json -q
linkedin navigator company fetch https://www.linkedin.com/sales/company/97ural \
  --employees --employees-positions "Engineer,Designer" --employees-locations "Europe" --json -q
```

#### 搜索公司

```bash
linkedin navigator company search [flags] --json -q
```

| 参数 | 说明 |
|------|-------------|
| `--term` | 搜索关键词 |
| `--limit` | 最大搜索结果数量 |
| `--sizes` | 用逗号分隔的公司规模：`1-10`, `11-50`, `51-200`, `201-500`, `501-1000`, `5001-10000`, `10001+` |
| `--locations` | 用逗号分隔的位置 |
| `--industries` | 用逗号分隔的行业 |
| `--revenue-min` | 最小年收入（单位：百万美元）：`0`, `0.5`, `1`, `2.5`, `5`, `10`, `20`, `50`, `100`, `500`, `1000`, `1000` |
| `--revenue-max` | 最大年收入（单位：百万美元）：`0.5`, `1`, `2.5`, `5`, `10`, `20`, `50`, `100`, `500`, `1000`, `1000+` |

```bash
linkedin navigator company search --term "fintech" --sizes "11-50,51-200" --json -q
linkedin navigator company search --revenue-min 10 --revenue-max 100 --locations "United States" --json -q
```

#### 发送内部邮件

```bash
linkedin navigator message send <person-url> '<text>' --subject '<subject>' --json -q
```

邮件长度最多为 1900 个字符。主题长度最多为 80 个字符。

```bash
linkedin navigator message send https://www.linkedin.com/in/username \
  'Would love to chat about API integrations' --subject 'Partnership Opportunity' --json -q
```

#### 获取销售导航器对话记录

```bash
linkedin navigator message get <person-url> [--since TIMESTAMP] --json -q
```

### 自定义工作流

可以从文件、标准输入或直接在命令行执行自定义工作流定义：

```bash
# From file
linkedin workflow run --file workflow.json --json -q

# From stdin
cat workflow.json | linkedin workflow run --json -q

# Inline
echo '{"actions":[...]}' | linkedin workflow run --json -q
```

检查工作流状态或等待其完成：

```bash
linkedin workflow status <id> --json -q
linkedin workflow status <id> --wait --json -q
```

有关工作流的 JSON 格式，请参阅 [Building Workflows](https://linkedapi.io/docs/building-workflows/)。

### 账户管理

```bash
linkedin account list                            # List accounts (* = active)
linkedin account switch "Name"                   # Switch active account
linkedin account rename "Name" --name "New Name" # Rename account
linkedin reset                                   # Remove active account
linkedin reset --all                             # Remove all accounts
```

## 重要注意事项

- **顺序执行。** 对于一个账户的所有操作会依次执行，多个请求会排队等待。
- **操作不是即时完成的。** 实际操作是通过浏览器在 LinkedIn 上进行的，因此每个操作可能需要 30 秒到几分钟的时间。
- **时间戳使用 UTC 格式。** 所有的日期和时间都采用 UTC 格式。
- **文本参数需使用单引号。** 为了防止 shell 解释特殊字符，请在消息文本、帖子内容和评论周围使用单引号。
- **操作次数有限制。** 平台会设置每个账户的操作次数限制。如果达到限制，会返回 `limitExceeded` 错误。
- **URL 格式化。** 响应中的所有 LinkedIn URL 都会被规范化为 `https://www.linkedin.com/...` 格式，末尾的斜杠会被去除。
- **空字段的处理。** 无法获取的字段会返回 `null` 或 `[]`，而不会被忽略。
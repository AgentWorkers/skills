---
name: linkedin-connect
description: 通过浏览器自动化向指定列表中的用户发送 LinkedIn 加入请求，并将状态更新记录在 CSV/TSV 文件中。适用于用户需要批量向 LinkedIn 上的特定用户（如创始人、演讲者、潜在客户等）发送加入请求的情况；这些用户的信息存储在包含 LinkedIn 个人资料链接的电子表格或列表中。该工具支持点击“加入”按钮的操作、处理处于“关注模式”的个人资料、检测用户是否已加入 LinkedIn、在 LinkedIn 搜索或 Google 搜索失败时使用备用链接进行查找，以及实现状态更新的增量跟踪功能。
---

# LinkedIn 连接工具

该工具可自动从列表中发送 LinkedIn 连接请求，并将结果记录在数据文件中。

## ⚠️ 启动前的准备工作 — 请务必确认以下事项

在开始操作之前，请务必与用户确认以下所有内容。所有项目都必须得到确认后才能继续。

### 1. 数据文件
- 请用户提供他们的电子表格/CSV/TSV 文件，并确认文件中包含以下列（或可以添加这些列）：
  - **人员/创始人姓名**：要联系的人的完整姓名
  - **公司/品牌名称**：他们的公司或品牌名称（用于搜索时的备用选项）
  - **LinkedIn 个人资料链接**：可选但强烈推荐；这有助于提高自动化的效率

如果文件缺少任何列，请告知用户缺少哪些列，并提供添加这些列的帮助。

### 2. 浏览器设置
- 询问用户使用的浏览器设置：

**选项 A — Chrome 浏览器中继（推荐用于被标记为自动化的账户）**
  - 用户必须安装 OpenClaw 浏览器中继 Chrome 扩展程序
  - 用户在常规 Chrome 浏览器中打开 LinkedIn，然后点击该标签页上的 OpenClaw 中继工具栏图标（图标会变为绿色）
  - 在这种模式下，所有浏览器工具调用都使用 `profile="chrome"` 作为参数

**选项 B — OpenClaw 隔离浏览器（`openclaw` 模式）**
  - OpenClaw 会管理一个独立的 Chrome 实例
  - 首次使用时，导航至 `https://www.linkedin.com` 并让用户登录；cookie 会在会话间保持
  - 在这种模式下，所有浏览器工具调用都使用 `profile="openclaw"` 作为参数

确认用户选择了哪种设置。如果用户的账户被标记为自动化账户或收到过相关警告，则默认使用 **选项 A（Chrome 中继）**。

### 3. 准备就绪确认
- 只有在用户确认以下内容后才能继续：
  - ✅ 文件已准备好且可访问
  - ✅ 浏览器已打开，LinkedIn 已登录（如果选择选项 A，则中继也已连接）

---

## 浏览器配置
根据用户在准备工作中的选择设置 `profile` 变量：
- **选项 A：** `profile="chrome"` — 重用已连接的中继标签页；通过 `browser action=tabs` 获取 `targetId`
- **选项 B：** `profile="openclaw"` — 使用 OpenClaw 管理的独立 Chrome 实例

在运行过程中请勿切换配置。每次浏览器工具调用都应使用相同的配置。

## 数据文件设置
确保跟踪文件中包含一个名为 `Connection Status` 的列。如果该列不存在，请添加它：

```python
import csv
rows = []
with open('file.tsv', 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    fieldnames = reader.fieldnames + ['Connection Status']
    rows = list(reader)
with open('file.tsv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t')
    writer.writeheader()
    for row in rows:
        row['Connection Status'] = ''
        writer.writerow(row)
```

## 三层查找流程（优先级顺序）
请始终按照以下顺序尝试。只有在当前方法失败时才尝试下一层。

### 第一层 — 直接访问 LinkedIn 个人资料链接（最快，最准确）
- 直接从数据文件中访问 LinkedIn 个人资料链接。
  - ✅ 链接加载成功 → 个人资料正确 → 继续进行连接操作
  - ❌ 返回 404 错误 → 转换到第二层
- 如果数据文件中不存在该人员的链接，则跳过第一层

### 第二层 — 在 Google 上搜索（可靠的备用方法，可保证准确性）
- 在 Google 中搜索 `"创始人姓名" "公司名称" linkedin"
- 导航至：`https://www.google.com/search?q=<姓名>+<公司名称>+linkedin`
- 在搜索结果中找到 LinkedIn 个人资料链接（通常为第一个结果），点击该链接
- 进入个人资料页面后，继续进行连接操作
- ⚠️ 仅当 Google 无法找到正确的人员或未返回任何 LinkedIn 结果时，才转换到第三层

### 第三层 — 在 LinkedIn 上直接搜索相关人员
- 在 LinkedIn 内部搜索创始人及公司名称
- 导航至：`https://www.linkedin.com/search/results/people/?keywords=<姓名>+<公司名称>`
- 首先查找页面中的 `Connect` 按钮；如果没有，则从搜索结果中打开个人资料页面
- 在连接之前确认姓名和公司名称是否匹配
- ❌ 如果没有找到匹配项 → 标记为 “个人资料未找到”

有关每层操作的详细浏览器步骤，请参阅 `references/browser-workflow.md`。

## 在个人资料页面上进行连接
进入正确的个人资料页面后，有两种连接方式：

**方式 A：** 个人资料页面上有直接的可点击连接按钮 → 点击按钮 → 确认对话框 → 点击 “发送连接请求”（无需备注）

**方式 B：** 个人资料页面上没有连接按钮，只有 “关注” + “消息” + “更多” 功能 → 点击 “更多操作” → 使用选择器 `.artdecoDropdown__content--is-open` 打开下拉菜单 → 点击 “邀请 [姓名] 连接” → 确认对话框 → 点击 “发送连接请求”（无需备注）

如果既没有 “连接” 按钮也没有 “邀请” 按钮，则标记为 “仅可关注”。

## 状态代码说明

| 状态 | 含义 |
|---|---|
| `Request Sent` | 本次会话中已发送连接请求 |
| `Already Connected` | 已经建立连接关系 |
| `Pending` | 该请求之前已经发送过 |
| `Follow Only` | 该个人资料页面上没有连接选项 |
| `Profile Not Found` | 三层查找均失败 |
| `Skipped` | 有意跳过此步骤 |

## 多位创始人的处理
当 TSV 文件中包含多位创始人时，需要分别记录每位创始人的状态，使用 `|` 进行分隔：

```
Founder1Slug: Request Sent | Founder2Slug: Already Connected
```

## 速率限制与反检测措施
> ⚠️ LinkedIn 会标记那些在不同个人资料页面之间直接跳转的账户。请务必在访问每个个人资料页面之前先浏览 LinkedIn 的动态页面（无例外）。具体操作方法请参阅 `references/browser-workflow.md`。这是主要的反检测措施。
- 在访问下一个个人资料页面之前，请先暂停 2–4 秒。
- 如果连续访问 3 个有效链接后仍收到 404 错误，请在继续访问前暂停 10 秒（然后切换到 Google 或 LinkedIn 搜索）。
- 请勿打开新的浏览器标签页——否则中继连接会中断；每次操作都应使用同一个已连接的标签页。
- 每次会话中的连接请求次数请控制在 20–25 次以内。如果接近这个限制，请停止操作并告知用户。

## 进度保存
使用 `linkedin_progress.json` 文件来保存进度：
```json
{ "statuses": { "https://www.linkedin.com/in/username/": "Request Sent" } }
```
每处理 10 个个人资料或完成整个流程后，更新 TSV 文件中的数据。

## 参考资料
- `references/browser-workflow.md` - 详细介绍了三层查找流程及两种连接方式的浏览器操作步骤
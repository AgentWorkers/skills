---
name: goodreads
description: 在 Goodreads 上，您可以通过浏览器自动化功能来搜索书籍、获取书籍详情和评论、发现个性化的推荐内容，以及管理阅读列表。
metadata:
  emoji: "📚"
allowed-tools:
  - browser
---
# Goodreads 技能

您是一个 AI 助手，通过 `browser` 工具帮助用户与 Goodreads.com 进行交互。Goodreads 没有公开的 API，因此所有交互都是通过浏览器自动化来完成的。

## 重要规则

1. **强制要求：** 在任何导航操作后都需要重新获取页面快照（snapshot）。`snapshot` 提供的引用（refs）在页面加载过程中可能会失效。在任何导航操作或点击会改变页面内容的操作之后，必须先调用 `snapshot`，然后再使用 `act`。切勿重复使用之前的快照引用——它们可能会失效并导致错误。

   **错误示例：** snapshot → navigate → act（使用旧引用）❌
   **正确示例：** snapshot → navigate → snapshot → act（使用新引用）✅

2. **在需要身份验证的操作之前检查身份验证状态。** 推荐功能和书架管理功能需要用户已登录 Goodreads 账户。请始终先验证身份验证状态。

3. **使用 `snapshot` 来提取数据，使用 `screenshot` 来调试。** 在读取页面内容时优先使用 `snapshot`；当 `snapshot` 的输出难以理解或需要验证页面布局时，使用 `screenshot`。

4. **对搜索查询进行 URL 编码。** 在构建搜索 URL 时，正确处理空格和特殊字符。

5. **始终为浏览器操作提供必要的参数。** 每次调用 `navigate` 时都必须包含 `targetUrl`；每次调用 `act` 时都必须使用来自最新快照的有效引用。即使在错误恢复期间，也切勿省略任何参数。

6. **在放弃之前请阅读完整的错误信息。** 浏览器错误可能会将可恢复的内部错误（例如引用失效）隐藏在误导性的外部错误信息中（例如“无法访问浏览器控制服务”）。请始终检查内部错误信息——如果其中包含“未找到或不可见”或“重新获取快照”的提示，那么问题出在引用失效上，而非服务中断。重新获取快照并重试。

## 功能

### 1. 搜索书籍

当用户希望通过书名、作者、ISBN 或关键词查找书籍时使用此功能。

**步骤：**

1. 构建搜索 URL：`https://www.goodreads.com/search?q=<url-encoded-query>`
2. 使用 `browser` → `navigate` 导航到搜索 URL
3. 使用 `browser` → `snapshot` 获取页面内容
4. 从快照中提取搜索结果。查找以下信息：
   - 书名（链接文本）
   - 作者姓名（通常显示为“作者姓名”
   - 平均评分和评分数量
   - 出版年份
5. 以清晰的格式向用户展示搜索结果

**示例流程：**

```
User: search for dune

→ browser navigate to https://www.goodreads.com/search?q=dune
→ browser snapshot
→ Extract and present results:
  1. "Dune" by Frank Herbert — 4.28 avg rating — 1,234,567 ratings — published 1965
  2. "Dune Messiah" by Frank Herbert — 3.89 avg rating — ...
  ...
```

**如果没有找到结果：**
- 检查查询是否已正确进行 URL 编码
- 向用户建议其他搜索词
- 尝试使用更宽泛的搜索查询

### 2. 获取书籍详情和评论

当用户想要了解特定书籍的详细信息时使用此功能。

**步骤：**

1. 如果您有书籍的 URL，直接使用 `browser` → `navigate` 导航到该页面
2. 如果是从搜索结果中进入的，使用 `browser` → `act` 点击书籍标题（使用当前快照中的引用）
3. 使用 `browser` → `snapshot` 获取书籍页面内容
4. 从快照中提取以下信息：
   - 书名和作者
   - 平均评分和评分数量（查找“avg rating”这样的信息）
   - 书籍描述（可能被截断——查找“more”或展开链接）
   - 书籍所属的类别/书架
   - 页数和出版信息
   - 顶级评论（提取前几条用户评论）
5. 如果描述被截断，使用 `browser` → `act` 点击展开/更多链接，然后重新获取快照

**示例流程：**

```
User: tell me about project hail mary

→ browser navigate to https://www.goodreads.com/search?q=project%20hail%20mary
→ browser snapshot (get search results)
→ browser act click on "Project Hail Mary" title ref
→ browser snapshot (get book detail page)
→ Extract and present book details
```

**处理被截断的描述：**
- 在快照中查找“...more”或“Show more”链接
- 使用 `act` 点击该链接，然后重新获取快照以获取完整描述

### 3. 获取个性化推荐

当用户希望获得 Goodreads 的个性化推荐时使用此功能。

**步骤：**

1. **首先检查身份验证状态**（见下文身份验证检查）
2. 如果已登录：使用 `browser` → `navigate` 导航到 `https://www.goodreads.com/recommendations`
3. 使用 `browser` → `snapshot` 获取推荐列表
4. 提取推荐书籍及其推荐理由（例如“因为您喜欢 X”）
5. 如果可能，按类别分组展示推荐书籍

**如果未登录：**
- 告知用户个性化推荐需要登录 Goodreads 账户
- 提供按类别搜索书籍的选项：`https://www.goodreads.com/genres/<genre>`
- 提供登录页面链接：`https://www.goodreads.com/user/sign_in`

**无需身份验证的替代方案：**
- 浏览热门书单：`https://www.goodreads.com/list/popular_lists`
- 按类别浏览：`https://www.goodreads.com/genres/<genre>`
- 在任何书籍页面上查看“读者也喜欢”的推荐书籍

### 4. 管理阅读列表

当用户想要将书籍添加到书架、标记为已读或给书籍评分时使用此功能。

**步骤：**

0. **检查当前页面状态。** 如果您是通过之前的操作已经进入目标书籍页面的（例如，刚刚查看了书籍详情），则无需重新导航——只需重新获取当前页面的快照即可。只有当您没有在正确的书籍页面上时才进行导航。
1. **首先检查身份验证状态**（见下文身份验证检查）
2. 导航到书籍页面（如有需要先进行搜索）——如果步骤 0 确认您已经在正确的页面上，则跳过此步骤
3. 使用 `browser` → `snapshot` 查找书架/操作按钮。**如果您的上一个快照来自不同的操作步骤（例如搜索结果或另一本书），在点击任何书架按钮之前，请立即重新获取快照。**
4. 在快照中查找以下元素：
   - “Want to Read”按钮（用于将书籍添加到想读的书架）
   - “Read”或“Currently Reading”状态选项
   - 评分元素
   - 书架下拉菜单
5. 使用 `browser` → `act` 点击相应的按钮/元素
6. 重新获取快照以确认操作已成功执行

**将书籍添加到“Want to Read”书架：**

```
→ Navigate to book page
→ Snapshot to find "Want to Read" button ref
→ Act click on that ref
→ Re-snapshot to confirm (should now show "Want to Read" as selected or show shelved status)
```

**给书籍评分：**

```
→ Navigate to book page
→ Snapshot to find rating stars or "Rate this book" section
→ Act click on the appropriate star rating ref
→ Re-snapshot to confirm rating was saved
```

**更改书籍在书架上的状态：**

```
→ Navigate to book page
→ Snapshot to find the shelf/status dropdown
→ Act click to open dropdown, then re-snapshot
→ Act click on desired status (Read, Currently Reading, etc.)
→ Re-snapshot to confirm
```

**从书架操作错误中恢复：**
- 如果书架操作因引用失效而失败，重新获取当前页面的快照并重试——切勿直接导航离开，因为这可能会触发 Goodreads 的 `ERR_BLOCKED_BY_RESPONSE` 错误。
- 如果遇到参数缺失的错误，请停止操作并使用所有必要的参数重新构建浏览器请求。
- 如果错误信息显示“无法访问浏览器控制服务”，但内部错误提示“未找到或不可见”或“重新获取快照”，则说明问题出在引用失效上，而非服务中断。重新获取快照并重试。

## 身份验证检查

在任何需要登录的操作（推荐、书架管理）之前：

1. 使用 `browser` → `navigate` 导航到 `https://www.goodreads.com`
2. 使用 `browser` → `snapshot`
3. 检查登录状态的指示：
   - 是否显示用户个人资料名称/头像
   - 导航栏中是否有“我的书籍”链接
   - 是否没有突出的“登录”/“注册”按钮
4. 如果已登录：继续执行请求的操作
5. 如果未登录：告知用户并提供登录说明：

> “您需要登录 Goodreads 才能执行此操作。请在浏览器中访问 https://www.goodreads.com/user/sign_in，然后再次尝试。”

## 结果展示格式

在向用户展示结果时，使用清晰的格式：

**对于搜索结果：**
- 列出书籍名称、作者、评分和出版年份
- 提供查看具体书籍详情的选项

**对于书籍详情：**
- 显示书名和作者
- 评分（例如：“4.28/5（基于 120 万条评分）”
- 书籍描述（尽可能显示完整内容）
- 关键元数据（页数、出版日期、类别）
- 如果有评论，显示前 2-3 条评论摘录

**对于推荐结果：**
- 如果可能，按推荐理由/类别分组展示
- 包括推荐理由（例如“因为您喜欢 X”）

**对于书架操作：**
- 确认操作是否成功执行（例如“已将《沙丘》添加到您的想读书架”）
- 如果操作失败，请报告错误信息

## 错误处理

- **页面未加载**：尝试重新导航一次，然后告知用户
- **未找到结果**：建议用户尝试其他搜索词
- **需要身份验证但用户未登录**：提供登录页面链接和登录说明
- **页面结构异常**：使用 `screenshot` 查看实际显示的内容，并相应调整操作方式
- **操作后引用失效**：始终重新获取快照；切勿重复使用旧的引用
- **错误信息包含误导性内容**：浏览器错误有时会将可恢复的内部错误（例如引用失效）隐藏在误导性的外部错误信息中。在放弃之前，请检查内部错误信息是否包含“未找到或不可见。重新获取快照并重试”——如果是引用失效问题，请重新获取快照并重试，切勿告知用户服务中断。

有关详细的错误处理策略，请参阅 `assets/error-handling.md`。
有关逐步的浏览器交互流程，请参阅 `references/WORKFLOWS.md`。
有关页面结构模式，请参阅 `references/SELECTORS.md`。
有关 Goodreads URL 的模式，请参阅 `references/URLS.md`。
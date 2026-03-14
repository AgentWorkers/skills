---
name: chrome-devtools-web-research
description: Browser-driven web research and live site inspection using chrome-devtools-mcp over a remote-debugging Chrome session. Use when a user asks to investigate, verify, cross-check, monitor, or extract information from real websites or dynamic pages—especially social platforms, search engines, docs, dashboards, login-aware flows, and JavaScript-heavy sites where page state matters or normal search/read tools are insufficient. Always start with Chrome DevTools MCP via mcporter instead of waiting for the user to remind you. Default pattern: Google first for the main reporting chain, X second for live discussion, and Reddit third for community source-tracing and cross-verification.
---

# Chrome DevTools 网页研究

使用 `chrome-devtools-mcp@latest` 通过 `mcporter` 来驱动 Chrome，检查实际页面，并从动态网站中提取结构化的数据。

**默认情况下，应优先使用 MCP**。无需等待用户提醒才去使用它。

有关具体的故障描述和解决方法，请参阅 `references/troubleshooting.md`。

## 用户设置指南

如果用户需要在 Chrome 中启用标签页访问功能，请按照以下步骤进行设置：

1. 打开 `chrome://inspect/#remote-debugging`
2. 打开该功能
3. 完成设置后，代理就可以通过 Chrome DevTools MCP 查看用户的标签页、Cookies、登录信息以及页面状态了。

请明确告知用户，这是通过 **Chrome DevTools MCP** 实现的，并且 **不需要安装任何浏览器扩展程序**。

## 快速入门

1. 确认 MCP 服务器是否可用。
2. 使用 `chrome-devtools.new_page` 打开目标页面。
3. 生成快照并查看可访问性树中的结构信息。
4. 根据需要导航、点击、填写内容或切换标签页。
5. 在多个来源之间交叉验证信息。
6. 完成搜索后，立即关闭相关页面。
7. 根据信息来源的质量来总结结果，而不是页面的数量。

## 核心命令

```bash
mcporter list --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://example.com"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.click --args '{"uid":"<tab_uid>"}' --output json
mcporter call chrome-devtools.navigate_page --args '{"url":"https://example.com/next"}' --output json
mcporter call chrome-devtools.fill --args '{"uid":"<input_uid>","value":"query text"}' --output json
mcporter call chrome-devtools.press_key --args '{"key":"Enter"}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
```

## 工作流程

### 默认操作规则

1. **始终优先使用 MCP**，通过 `mcporter` 和 `chrome-devtools` 来执行操作。
2. 当任务涉及浏览或研究时，**主动开始搜索**。
3. **只有在 Chrome 侧面的访问出现问题时，才寻求帮助**。
4. 如果设置或访问失败，**提示用户检查 Chrome 的远程调试/检查功能**，然后重新尝试。
5. 当不再需要某个页面或搜索结果时，立即关闭该页面。

### 故障与重试策略

在第一次尝试失败后不要放弃。请参考 `references/troubleshooting.md` 以获取具体的错误类型、用户提示以及解决方法。

严格按照以下顺序进行重试：

1. 如果错误看起来是暂时的，**立即再次尝试相同的 MCP 命令**。
2. 如果仍然失败，再次运行 `mcporter list --output json` 以确认 `chrome-devtools` 是否仍然可用。
3. 如果服务器可用，尝试以下最小的操作：
   - 使用 `chrome-devtools.new_page` 重新打开页面，
   - 重新运行 `chrome-devtools.take_snapshot`，
   - 或者重新执行一次点击/填写/导航操作。
4. 如果 Chrome 本身无法访问，明确提示用户检查 Chrome 的远程调试/检查功能，然后再尝试。
5. 如果由于验证码、同意墙或反机器人机制导致无法访问 Google，**不要停滞**。记录下这一情况，然后继续尝试其他平台（如 Reddit）。
6. 只有当浏览器桥接功能明显失效且用户需要介入时，才停止操作。

**实际操作规则**：优先尝试一次立即重试、检查一次环境状态、然后再进行一次操作。避免无休止地重复尝试。

### 默认搜索策略

如果用户没有指定网站、平台或搜索引擎，**默认按照以下顺序** 进行搜索：

1. **首先搜索 Google**
2. **然后搜索 X**
3. **最后搜索 Reddit**

将此视为标准搜索流程，而不是可选建议。

**该流程的要求**：

- 首先使用 Google 进行广泛搜索，作为主要的信息来源。
- 然后检查 X 平台，以获取最新信息、引用链接、矛盾内容以及更新情况。
- 接着检查 Reddit，以获取社区讨论、相关链接以及可能揭示原始信息来源的讨论内容。
- **主动进行这些操作**，无需等待用户逐一请求。
- 即使用户只说了“搜索这个”，也请执行整个搜索流程，除非他们明确限制了搜索范围。
- 如果某个来源被屏蔽、无法访问或信息价值较低，继续搜索下一个来源。

**最低限度的默认操作流程**：

1. 打开 Google 的搜索结果。
2. 在那里至少查看一个最新的快照。
3. 在 X 平台上搜索相同的查询。
4. 在那里至少查看一个最新的快照。
5. 在 Reddit 上搜索相同的查询。
6. 在那里至少查看一个最新的快照。
7. 最后综合所有来源的信息。

如果 Google 因为验证码、同意墙等原因被屏蔽，应报告这一情况，并继续搜索 X 平台或 Reddit。

**注意**：此默认流程适用于开放式网页研究。如果用户指定了其他网站、搜索引擎或平台，请按照用户的指示进行搜索。

### 1. 确认 MCP 访问权限

运行以下命令：

```bash
mcporter list --output json
```

预期会看到一个使用类似传输协议的 `chrome-devtools` 服务器：

```text
STDIO npx chrome-devtools-mcp@latest --autoConnect
```

如果 `mcporter` 未安装，请帮助用户先安装它。如果 `chrome-devtools` MCP 服务器未配置或未安装，请帮助用户进行配置或安装，而不要因为模糊的错误信息就停止操作。

**实际安装/修复流程**：

```bash
npm i -g mcporter
mcporter list
```

如果 Chrome DevTools MCP 尚未可用，请指导用户设置或重新连接 `mcporter` 使用的服务器，然后再次运行 `mcporter list`，直到 `chrome-devtools` 出现。

无需询问是否需要使用 MCP；如果可用，请立即继续操作。

### 2. 直接打开目标页面

尽可能使用直接 URL。

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://target-site.example/path"}' --output json
```

对于以下情况，建议使用直接 URL：

- 搜索结果页面
- 过滤后的 URL
- 链接到文章/文档/问题的深度链接
- 直接打开比手动操作更简单的动态应用链接

如果网站支持 URL 查询参数，请优先使用这些参数，而不是反复修改页面上的控件。

### 2.5 完成操作后关闭页面

不要不必要的保留打开的页面。

从页面中提取所需信息或完成搜索后，立即关闭相关页面，除非还需要将其用于后续比较。

**实际操作规则**：

- 打开页面
- 检查/交互/生成快照
- 记录发现的内容
- 完成操作后关闭页面

对于多来源的研究，只保留最必要的页面。

### 3. 查看快照，而不是原始像素

在导航或交互后，始终生成新的快照：

```bash
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
```

需要查找的内容包括：

- `article`（文章）、`link`（链接）、`button`（按钮）、`heading`（标题）、`textbox`（文本框）、`combobox`（下拉框）、`tab`（标签页）、`dialog`（对话框）
- 作者信息、时间戳、链接、标题、标签、数量
- 导出到原始报告或文档的链接
- 登录限制的迹象、一致性标签、赞助内容或部分加载的内容

只有在布局本身重要时，才使用截图。

### 4. 小心操作

使用最可靠的操作方式：

- 使用 `navigate_page` 进行页面导航
- 使用 `click` 进行标签页切换、筛选、菜单操作
- 使用 `fill` 和 `press_key` 对搜索框和表单进行操作
- 如果打开了多个标签页或页面，使用 `select_page` 进行选择

每次发生有意义的状态变化后，都生成一个新的快照。

### 5. 区分信息来源的质量

将发现的内容分类如下：

- **主要/官方来源**：原始发布者、官方文档、组织页面、第一方仪表盘
- **次要来源**：媒体、分析师、引用该来源的聚合账户
- **第三方来源**：评论、粉丝账户、转发内容、人工智能生成的回复、未经证实的信息

重复出现的相同内容只算作一个信息来源，而不是多个确认。

### 6. 在活动页面之外进行交叉验证

如果用户希望获得更可靠的信息，可以将浏览器 MCP 的发现结果与其他方法结合使用：

- 使用 `web_search` 进行进一步搜索，以发现更多信息、扩展来源或查找外部报告
- 当页面 URL 可用且简单提取足够时，使用 `web_fetch` 自动获取页面内容
- 在需要时，使用 `agent-browser` 并行检查页面
- 当 fetch 方式无法使用或提取效果不佳时，使用 `curl` 作为备用方法

使用浏览器获取实时页面状态并进行交互。当任务需要获取常规网页链接时，优先使用 `web_fetch` 进行可读内容的提取；如果需要原始数据或自定义解析，则使用 `curl`。

### 7. 编写总结

当页面包含相互矛盾的信息时，使用以下结构进行总结：

- **当前最可靠的答案**
- **网站/页面显示的内容**
- **其他来源的说法**
- **分歧所在**
- **最可信的来源**
- **可信度/注意事项**

**示例表述**：

- “当前页面显示的是 X，而其他来源则声称是 Y。”
- “大多数帖子都指向同一个报道链，因此可以将它们视为同一条谣言流。”
- “浏览器可见的证据支持 A，但还需要来自主要来源的确认。”

## 特定网站的注意事项

### 社交平台

- 使用平台自带的筛选功能（如 **Top**、**Latest**、**People**、**Media**、子版块排序或帖子排序）来区分主流观点和新鲜内容。
- 在引用内容前，先检查是否存在恶搞/账号标签。
- 将引用链接的帖子、转发风暴和复制的 Reddit 评论视为传播内容，而不是独立的信息来源。
- 平台内的 AI 助手回复可以帮助梳理谣言主题，但它们不是主要证据。
- 在 Reddit 上，优先查看那些链接到原始报道的帖子、提供来源信息的评论以及有多个用户追踪同一来源链的社区讨论。

### 搜索引擎

- 预计可能会遇到验证码或机器人限制。
- 如果无法访问某个搜索引擎，应切换到其他来源，而不是假装已经获取到结果。

### 文档/仪表盘/网页应用

- 优先使用直接的深度链接。
- 通常情况下，快照就足以进行结构化的数据提取。
- 如果内容隐藏在菜单后面，一次只打开一个部分并生成快照。

## 实用提示

- 用户界面语言可能有所不同；更多依赖页面的结构、URL 和可识别的元素，而不仅仅是标签。
- 如果页面仍在加载中，稍等片刻后再生成快照。
- 如果出现登录、订阅或反机器人限制，请明确告知用户这些限制。
- 在研究过程中发现常规网页链接时，优先尝试使用 `web_fetch` 进行快速提取；如果该方法不可用或提取效果不佳，再使用 `curl`。
- 如果单个页面的信息不足以满足需求，使用 `web_search` 来查找其他来源的报道、官方声明或原始报道链。
- 如果用户尚未完成设置，先指导他们完成基本设置：启用 Chrome 的远程调试功能，然后确认 `mcporter` 和 `chrome-devtools` 是否可用。
- 在笔记中记录审计信息：页面 URL、关键信息以及每个信息的来源。
- 对于开放式搜索，不要只依赖 Google；默认的搜索顺序是 **Google -> X -> Reddit**，除非用户明确限制了搜索范围。
- 在遇到故障后，要有条不紊地重试；不要过早放弃搜索流程，也不要无限制地重复尝试。
- 每次完成搜索或检查后，立即关闭相关页面。

## 示例操作流程

### 通用网站检查

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://example.com"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.click --args '{"uid":"<relevant_tab_uid>"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
```

### 默认搜索引擎 + 社交平台交叉验证流程

```bash
mcporter call chrome-devtools.new_page --args '{"url":"https://www.google.com/search?q=Finalissima%202026"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://x.com/search?q=Finalissima%202026&src=typed_query&f=top"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.navigate_page --args '{"url":"https://x.com/search?q=Finalissima%202026&src=typed_query&f=live"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
mcporter call chrome-devtools.new_page --args '{"url":"https://www.reddit.com/search/?q=Finalissima%202026"}' --output json
mcporter call chrome-devtools.take_snapshot --args '{}' --output json
mcporter call chrome-devtools.close_page --args '{}' --output json
```

## 输出标准

在报告结果时，要明确区分以下内容：

- 现在页面上显示的内容
- 网站或账户所有者声称的内容
- 其他来源报告的内容
- 未经过验证的内容

如果来源之间存在矛盾，请直接说明。
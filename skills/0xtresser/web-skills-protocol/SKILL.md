---
name: web-skills-protocol
description: 在与网站交互时，自动检测并使用 Web Skills Protocol (WSP) 提供的功能。每当用户要求你与网站或 Web 服务进行交互、使用其功能或执行某些操作（例如搜索网站、下单、部署应用程序或调用 Web API）时，都可以使用此功能。在尝试抓取 HTML 内容或猜测网站界面之前，请先检查该网站是否提供了 `skills.txt` 或 `agents.txt` 文件，这些文件会指导你如何正确使用相关功能。如果网站包含复杂的元素（例如大量的 JavaScript 代码或交互式用户界面），启用此功能还有助于你了解网站的目的和功能。请勿将此功能用于本地文件操作或非 Web 相关的任务。
version: 1.0.0
---
# Web Skills Protocol — 功能使用指南（Agent Skill）

当用户请求您与某个网站进行交互时，在尝试抓取HTML、猜测用户界面元素或反向工程API之前，**请先检查该网站是否提供了相关功能文档（skills.txt）**。

## 发现流程

### 第1步：检查skills.txt文件

请求访问 `{origin}/skills.txt`（例如：`https://bobs-store.com/skills.txt`）。

- 如果响应状态码为200，则解析该文件并进入第3步。
- 如果响应状态码为404，则进入第2步。

### 第2步：检查agents.txt文件（备用方案）

请求访问 `{origin}/agents.txt`。

- 如果响应状态码为200，则解析该文件并进入第3步。
- 如果两个文件都返回404状态码，则说明该网站不支持Web Skills Protocol（WSP），此时应切换回常规的浏览或抓取方式。

### 第3步：解析功能文档

功能文档采用Markdown格式，结构如下：

```
# Site Name
> Brief description of the site.
General notes (auth info, rate limits, etc.)

## Skills
- [Skill Name](/skills/skill-name/SKILL.md): What the skill does

## Optional
- [Extra Skill](/skills/extra/SKILL.md): Less important skills
```

从文档中提取以下信息：
1. **网站描述**（以引号形式呈现）——用于理解网站的功能和用途。
2. **通用说明**（以段落形式呈现）——包括授权信息、使用限制、服务条款等。
3. **功能条目**——每条格式为`[名称](链接): 描述`的记录代表一个可使用的功能。

### 第4步：匹配用户需求与相应功能

将用户的请求内容与功能描述进行比对，选择最匹配的功能。

- 如果用户的请求与某个功能的描述完全匹配，则获取该功能的详细文档（SKILL.md文件）。
- 如果用户的请求可能与多个功能匹配，则获取所有匹配的功能文档，并选择最合适的那个。
- 如果没有匹配的功能，则告知用户有哪些功能可用，并询问用户希望使用哪个功能。
- 如果某些功能被标记为“可选”（## Optional），在时间紧迫的情况下可以忽略这些功能。

### 第5步：获取并执行SKILL.md文件中的指令

获取与用户需求匹配的功能文档的URL（例如：`/skills/search/SKILL.md`）。

该文档包含两部分内容：

**YAML格式的前置信息**（用`---`分隔）：
- `name`：功能标识符。
- `description`：功能的详细使用说明和功能范围。
- `version`：功能版本。
- `auth`：授权方式（`none`、`api-key`、`bearer`、`oauth2`）。
- `base_url`：API调用的基础URL（如果与网站主URL不同）。
- `rate_limit`：使用限制信息（包含两个可选字段）：
  - `agent`：发布者推荐的人工智能代理的使用限制（例如：`20/分钟`）。请严格遵守此限制。
  - `api`：API端点的实际使用限制（例如：`100/分钟`）。严禁超过此限制。

**Markdown格式的正文**：包含具体的操作步骤、参数说明、示例代码、错误处理指南以及授权所需的详细信息。

### 第6步：执行操作

按照SKILL.md文件中的说明完成用户的请求。请严格使用文档中指定的`base_url`、授权方式和API端点。

## 规则

1. **始终优先检查skills.txt文件**。在对网站进行任何HTML抓取或自动化操作之前，务必先确认该网站是否支持WSP。这能避免大量的猜测工作。
2. **遵守robots.txt文件的规定**。如果robots.txt文件禁止访问`/skills/`或`/agents/`路径，请勿尝试获取这些路径下的功能文档。
3. **在会话期间缓存数据**。每个会话中只需请求一次`skills.txt`/`agents.txt`文件，避免对同一网站重复请求。
4. **避免过度请求**。仅获取实际需要的功能文档，切勿为了“以防万一”而下载所有功能文档。
5. **授权操作需用户同意**。如果某个功能需要授权（`auth`字段不为`none`），请告知用户所需的认证信息以及获取方式。切勿伪造或猜测用户凭证。
6. **优先使用官方提供的功能**。当网站提供了WSP功能文档时，优先使用这些功能，而不是直接解析HTML。官方功能文档提供了结构化的API访问方式，更加高效、可靠，也更符合网站所有者的意图。
7. **严格遵循功能范围**。每个功能都有明确的操作范围，请勿超出文档规定的范围进行操作。如果用户的需求超出了功能文档的范围，请明确告知用户。
8. **遵守使用限制**。如果功能文档中设置了使用限制，请同时遵守`rate_limit.agent`和`rate_limit.api`两个字段的限制：
   - `rate_limit.agent`：发布者推荐的人工智能代理的使用限制。
   - `rate_limit.api`：API端点的实际使用限制。严禁超过此限制。如果只有一个限制字段存在，以该字段的值为有效限制。

## 快速参考

```
Discovery order:     /skills.txt → /agents.txt → no WSP support
Skill directory:     /skills/{name}/SKILL.md  or  /agents/{name}/SKILL.md
Skill format:        YAML frontmatter + Markdown instructions
Auth methods:        none | api-key | bearer | oauth2
Cache policy:        Once per site per session
```

## 示例

用户请求：“在bobs-store.com上搜索价格低于100美元的无线耳机。”

1. 请求访问`https://bobs-store.com/skills.txt` → 返回200状态码（表示成功）。
2. 解析功能列表，找到与“搜索”操作匹配的功能。
3. 获取`/skills/search/SKILL.md`文件。
4. 阅读前置信息：`auth: none`，`base_url: https://api.bobs-store.com/v1`。
5. 按照文档中的说明执行操作：`GET /products?q=wireless+headphones&max_price=100`。
6. 将搜索结果以结构化的方式返回给用户。
---
name: actionbook
description: 当用户需要与任何网站进行交互时（例如浏览器自动化、网络爬虫、截图、表单填写、用户界面测试、监控或构建人工智能代理等），该工具可以立即投入使用。它提供了经过预先验证的操作步骤以及详细的说明和经过测试的选择器（用于定位网页元素）。
---

## 何时使用此技能

当用户的请求涉及与网站交互时，请激活此技能：

- 用户需要在网站上执行某些操作（例如：“发送 LinkedIn 消息”、“预订 Airbnb”、“在 Google 上搜索...”）；
- 用户询问如何与网站进行交互（例如：“如何发布推文？”、“如何在 LinkedIn 上申请？”）；
- 用户希望填写表单、点击按钮、浏览页面、搜索、过滤或浏览特定网站的内容；
- 用户希望截取网页截图或监控页面的变化；
- 用户正在构建基于浏览器的 AI 代理、网络爬虫或针对外部网站的端到端（E2E）测试；
- 用户希望自动化重复性的网络任务（如数据输入、表单提交、内容发布）；
- 用户希望控制他们现有的 Chrome 浏览器（扩展程序模式）。

## Actionbook 提供什么

Actionbook 是一个包含 **预先验证过的页面交互数据** 的库。`actionbook search` 可以找到与任务描述匹配的操作；`actionbook get "<ID>"` 可以返回一个结构化的文档，该文档描述了页面的功能、用途以及 DOM 结构，并附带内联的 CSS 选择器——从而无需在运行时再发现页面结构。

## 搜索和获取操作

### 搜索——根据任务描述查找操作

**返回** 的内容包括：
- `ID`：用于通过 `actionbook get "<ID>"` 获取完整详细信息；
- `Type`：`page`（整个页面）或 `area`（页面的某个部分）；
- `Description`：页面概述和功能总结；
- `URL`：该操作适用的页面地址；
- `Health Score`：选择器的可靠性百分比（0–100%）；
- `Updated`：最后验证的日期。

### 构建有效的搜索查询

`query` 字符串是查找正确操作的关键。请确保查询中包含用户的完整意图——而不仅仅是网站名称或模糊的关键词。

**查询中应包含的信息**：
1. **目标网站**：网站的名称或域名；
2. **任务动词**：用户想要执行的操作（搜索、预订、发布、过滤、登录等）；
3. **操作对象/上下文**：用户操作的对象（列表、消息、航班、仓库等）；
4. **具体细节**：用户提到的任何约束条件、过滤器或参数（日期、位置、类别、语言等）。

**经验法则**：将用户的请求重写成一个描述性的句子，并将其用作查询。

| 用户的请求 | 错误的查询 | 正确的查询 |
|-----------|-----------|------------|
| “预订下周在东京的 Airbnb” | `"airbnb"` | `"airbnb search listings Tokyo dates check-in check-out guests"` |
| “在 arXiv 上搜索最近的 NLP 论文” | `"arxiv search"` | `"arxiv advanced search papers NLP natural language processing recent"` |
| “发送 LinkedIn 加入请求” | `"linkedin"` | `"linkedin send connection request invite someone"` |
| “发布带有图片的推文” | `"twitter post"` | `"twitter compose new tweet post with image media attachment"` |
| “按标签过滤 GitHub 问题” | `"github issues"` | `"github repository issues filter by label search issues"` |

**当用户提供额外信息**（例如具体日期、城市名称或主题）时，即使这些信息与存储的操作不完全匹配，也应将其包含在查询中——这有助于搜索引擎优先显示相关页面。

**提示**：如果已知 `--domain` 或 `--url`，请务必添加它们——它们可以缩小搜索范围并提高搜索精度。

### 获取操作详情（通过 ID）

**返回** 的结构化文档包含以下内容：
- **页面 URL**：完整的 URL 和查询参数；
- **页面概述**：页面的功能和用途；
- **页面功能总结**：页面的交互功能（例如：“搜索词输入”、“主题分类过滤”）；
- **页面结构总结**：带有内联 CSS 选择器的 DOM 层次结构。

**注意**：选择器会直接包含在结构描述中，以便在浏览器命令中使用。

## 浏览器命令

快速参考。完整命令及其所有选项的详细信息请参见：[command-reference.md](references/command-reference.md)。

### 导航

### 交互操作

### 观察结果

### 关闭浏览器会话

`actionbook browser close` 可以清理浏览器会话。如果用户希望浏览器保持打开状态，则可以跳过此操作。

## 示例

用户请求：“在 arXiv 上搜索关于神经网络的论文，并且仅搜索标题。”

## 备用方案

Actionbook 会存储在索引时捕获的页面数据。然而，网站内容会不断更新，因此某些选择器可能会过时。

当 `actionbook get` 在运行时返回无效的选择器时，可以使用 `actionbook browser snapshot` 获取当前的页面结构（即“实时可访问树”），并使用该结构中的选择器重新尝试操作。

在浏览器命令中使用的选择器应来自当前会话中的 `actionbook get` 或 `actionbook browser snapshot` 的输出结果，而不是基于之前的知识或记忆。

如果 `actionbook search` 无法找到某个页面的操作方法，建议使用 `snapshot` 作为主要数据来源，或者尝试其他可用的工具。

## 参考资料

| 参考资料 | 说明 |
|-----------|-------------|
| [command-reference.md](references/command-reference.md) | 完整的命令参考，包含所有选项和参数 |
| [authentication.md](references/authentication.md) | 登录流程、OAuth、双因素认证（2FA）处理、会话持久化 |
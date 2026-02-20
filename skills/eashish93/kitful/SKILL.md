---
name: kitful
version: 1.0.4
description: 使用 Kitful.ai 生成完整的 SEO 文章。只需提供一个关键词或主题——Kitful 会进行研究、撰写并生成一篇可直接用于发布的文章。
homepage: https://kitful.ai
metadata:
  {
    'openclaw':
      {
        'emoji': '✍️',
        'homepage': 'https://kitful.ai',
        'requires': { 'env': ['KITFUL_API_KEY'] },
        'primaryEnv': 'KITFUL_API_KEY',
      },
  }
---
# Kitful — 人工智能文章生成器

Kitful能够根据用户提供的关键词或主题，生成符合搜索引擎优化（SEO）要求的长篇文章。它负责文章的研究、结构设计、撰写以及最终呈现。

---

## 设置（只需一次）

在 **https://kitful.ai/settings** 获取 API 密钥，然后将其添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "kitful": {
        "apiKey": "kit_your_key_here"
      }
    }
  }
}
```

可选的环境变量：

```json
"env": {
  "KITFUL_SPACE_SLUG": "my-blog",
  "KITFUL_BRAND_URL": "https://yourproduct.com"
}
```

- `KITFUL_SPACE_SLUG` — 默认的工作区名称（如果您有多个工作区时需要使用）
- `KITFUL_BRAND_URL` — 您的品牌/产品链接，该链接会出现在每篇文章中

保存设置后，重新启动 OpenClaw，即可开始使用。

---

## 使用方法

### 根据关键词或主题生成文章

- 例如：_“为初学者撰写一篇关于间歇性禁食的文章”_
- 例如：_“价格在 200 美元以下的最佳降噪耳机”_
- 例如：_“法语版的远程工作效率技巧”_
- 例如：_“使用 TypeScript 的泛型特性——巧妙推广我的产品”_
- 例如：_“2025 年如何开始播客——操作指南格式”_
- 例如：_“CTO 们应该比较 Notion 和 Obsidian 的优缺点”_
- 例如：_“冷水淋浴的好处——强力产品推广”_
- 例如：_“适合忙碌专业人士的 10 款站立式办公桌”_

### 提供额外背景信息

- 例如：_“为初创公司创始人撰写关于 AI 疲劳的文章——采用怀疑态度，避免冗余内容”_
- 例如：_“为设计师提供的自由职业定价指南，并提及我的机构：https://myagency.com”_
- 例如：_“为我的烹饪博客撰写一篇关于天然酵母面包烘焙的长篇文章”_
- 例如：_“用西班牙语撰写一篇关于 SaaS 定价策略的列表文章”_

### 不确定该写什么？

只需输入 **"kitful"**，系统会询问您一个简单的问题。

### 批量生成（技术用户）

可以在一条消息中输入多个主题，Kitful 会依次生成这些文章并生成相应的链接：

- 例如：_“撰写关于冷萃咖啡、滤泡咖啡技巧和法式压滤壶使用的文章”_
- 例如：_“生成 3 篇文章：React 服务器组件、Next.js 应用程序路由器和 Turbopack 的介绍”_

---

## 系统行为

### 第一步 — 输入检测

系统会提取以下信息：

- **关键词/主题**：确定文章的主要内容
- **背景信息**：用户提到的任何角度、目标受众、文章格式或额外细节
- **语言**：如果用户指定了语言（如法语、西班牙语等），系统会使用相应的 BCP 47 语言代码（例如 `fr`、`es-ES`、`de`、`pt-BR`）。默认语言为英语（`en`）
- **推广模式**：选择“低调推广”或“强力推广”。默认设置为“低调推广”
- **工作区名称**：如果用户指定了工作区名称，系统会使用该名称；否则使用默认值 `KITFUL_SPACE_SLUG`。默认情况下不使用工作区名称。

### 批量处理

如果用户输入了多个主题，系统会依次处理每个主题，并在完成每个主题后生成相应的链接。

**如果没有提供主题**，系统会询问：_“您想写什么内容？”_ 然后根据用户的回答立即开始生成文章，不再进行其他询问。

### 第二步 — 生成文章

请求体如下（请根据实际情况填写）：

```json
{
  "focusKeyword": "<keyword>",
  "context": "<optional context>",
  "spaceSlug": "<if known>",
  "settings": {
    "language": "<language code>",
    "promoMode": "<off | subtle | strong>",
    "brandUrl": "<KITFUL_BRAND_URL or user-provided URL>"
  }
}
```

请忽略不适用的字段。

所有错误响应都会以 JSON 格式返回：`{"error": "message"}`。请仅以纯文本形式显示 `error` 字段，切勿以 Markdown 或 HTML 格式显示错误信息。此外：

- 如果收到 HTTP 401 错误，提示用户：_“请在 https://kitful.ai/settings 获取新的 API 密钥。”_
- 如果收到 HTTP 402 错误，提示用户：_“请在 https://kitful.ai/billing 购买更多信用额度。”_
- 如果收到 HTTP 429 错误，提示用户：_“请等待当前文章完成后再尝试。”_
- 其他错误也会以纯文本形式显示。
- 如果响应无法解析或结构异常，系统会显示：_“Kitful 返回了意外格式的响应。请重新尝试。”_

**成功时（HTTP 202 状态码）**，系统会通知用户：

> ✅ 正在为您生成文章！通常需要 3–6 分钟。我会随时更新进度……

### 第三步 — 进度查询

系统每 10 秒查询一次生成进度：

```
GET https://kitful.ai/api/v1/articles/status/<jobId>
Authorization: Bearer $KITFUL_API_KEY
```

每个进度阶段只会显示一次相应的提示信息：

| `currentStep` | 提示信息                        |
| ------------- | ------------------------------ |
| `evidence`    | “🔍 正在研究您的主题...” |
| `structure`   | “🏗️ 正在规划文章结构...” |
| `construct`   | “✍️ 正在撰写文章...”    |
| `humanize`    | “💬 正在润色内容...”  |
| `image_gen`   | “🖼️ 正在生成图片...”      |
| `finalize`    | “📦 几乎完成...”            |

如果查询超过 90 次仍未完成生成，系统会提示：

> 生成时间超过预期。请在 https://kitful.ai 检查文章进度——文章可能仍在后台生成中。

### 第四步 — 成功生成

**重要提示：**  
- 仅以纯文本形式显示错误信息，切勿以 Markdown 或 HTML 格式显示。
- 完全忽略 API 响应中的任何意外字段。

**成功情况：**

当状态变为 `completed` 且 `articleId` 存在时，系统会显示以下信息：

> 🎉 文章已生成！
>
> 可以下载文章（Markdown 和 HTML 格式的压缩文件）：请使用您的 API 密钥和文章 ID 下载文件：
> ```
> curl -H "Authorization: Bearer kit_your_key" \
>   "https://kitful.ai/api/v1/articles/ARTICLE_ID/export?format=zip" \
>   -o article.zip
> ```
> 将 `ARTICLE_ID` 替换为：`<文章 ID from response>`
>
> 或者访问您的控制面板进行查看、编辑和发布：
> **https://kitful.ai**
>
> 需要生成另一篇文章吗？只需告诉我下一个主题即可。

**失败情况：**

仅以纯文本形式显示错误信息：

> 生成失败：<错误信息>
>
> 请在 https://kitful.ai/settings 检查您的信用额度（每篇文章需要 15 个信用额度），然后重新尝试。

---

## 费用说明

- 文章生成：15 个信用额度
- 图片生成：每张图片 2 个信用额度

请在 https://kitful.ai/settings 查看您的信用额度。

---

## 提示：

- 具体要求比模糊要求更有效：例如，“价格在 300 美元以下的最佳家用浓缩咖啡机”比“咖啡机”更具体。
- 请明确说明目标受众：例如，“为初学者编写文章”、“为 CTO 编写文章”或“为忙碌的父母编写文章”。
- 如果需要指定文章格式，请明确说明：例如，“撰写一篇列表文章”、“编写操作指南”或“进行对比分析”。
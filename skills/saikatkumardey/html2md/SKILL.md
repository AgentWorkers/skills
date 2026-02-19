---
name: html2md
description: 使用 Readability 和 Turndown 将 HTML 页面转换为结构清晰、易于处理的 Markdown 格式。该工具会自动去除导航栏、广告、页脚、cookie 广告以及社交媒体上的点击按钮（CTAs）。支持从 URL 获取内容、处理本地文件、从标准输入（stdin）读取数据、设置令牌使用限制（token budgeting），并允许用户自定义输出格式。非常适合用于研究任务、内容提取以及自动化工作流程中的网页抓取（web scraping）。
---
# html2md

这是一个专为AI代理设计的强力HTML转Markdown转换工具。它首先使用Mozilla Readability库提取页面的主要内容，然后通过Turndown库将HTML转换为Markdown格式，最后通过复杂的后处理步骤去除剩余的冗余信息。

> 完整的参数说明和高级用法示例请参阅：`references/usage.md`

## 安装要求

```bash
cd <skill-dir>/scripts
npm install
npm link        # makes `html2md` globally available
```

该工具需要Node.js 22及以上版本。

## 快速入门

```bash
html2md https://example.com                    # fetch + convert
html2md --file page.html                       # local HTML file
cat page.html | html2md --stdin                # pipe from stdin
html2md --max-tokens 2000 https://example.com  # budget-aware truncation
html2md --no-links https://example.com         # strip hrefs, keep text
html2md --json https://example.com             # JSON: {title, url, markdown, tokens}
```

## 主要功能

- **内容提取**：自动移除导航栏、侧边栏、广告以及cookie广告。当Mozilla Readability提取的内容不足时（例如某些网站的表格布局），会使用处理后的`<body>`内容作为替代。
- **令牌预算控制**：通过`--max-tokens N`参数来限制转换过程中使用的令牌数量；剩余的令牌会按照文档的顺序填充到Markdown中，并在输出末尾添加`[truncated — N more tokens]`的提示。
- **后处理**：删除HTML注释、零宽度字符、社交媒体链接、面包屑导航、空标题以及多余的空白行。
- **错误处理**：遇到无效的URL、超时（15秒）、非HTML内容或文件缺失等情况时，工具会返回退出代码1，并在标准错误输出（stderr）中给出详细错误信息。
- **输出格式**：支持纯Markdown格式，或通过`--json`参数输出JSON格式以供程序调用。

## 与`web_fetch`的对比

| 适用场景 | `html2md` | `web_fetch` |
|---------|---------|---------|
| 在定时任务或子代理中读取页面 | 需要一次性快速获取页面内容 | 需要在主会话中执行页面请求 |
| 需要控制令牌使用量（`--max-tokens`参数） | 页面是JSON或XML格式的API接口 |  
| 需要去除复杂的导航栏、广告或页脚元素 | 不需要JavaScript进行页面渲染 |  
| 需要JSON格式的输出 | 页面结构简单 |

## 安全注意事项

html2md的主要功能是获取URL内容和读取本地文件。在使用时，请注意以下安全问题：

- **URL处理**：该工具会直接获取用户提供的URL；如果您的安全模型中包含SSRF（跨站请求伪造）风险，请确保不传递未经验证的用户控制URL。
- **文件读取**：`--file`参数允许工具读取系统可访问的任何文件路径。在代理环境中，文件路径由代理程序控制，这相当于代理程序直接使用`cat`命令来读取文件。
- **无shell执行**：该工具本身不会启动shell或执行任何命令；在脚本中调用该工具时，请使用`execFileSync`（而非`execSync`）以避免shell注入攻击。
- **数据安全**：所有输出仅保存到标准输出（stdout），不会发送任何网络请求；没有数据泄露风险，也没有任何数据传输或分析功能。
- **依赖库**：该工具依赖于jsdom（Mozilla的DOM实现库）、Readability（用于内容提取的库）以及Turndown（用于HTML转Markdown的库）。这些库都经过了严格的审计，且为开源项目。

## 使用示例

```bash
# Read a Paul Graham essay within 2000 tokens
html2md --max-tokens 2000 https://paulgraham.com/greatwork.html

# HN front page as clean text, no link noise
html2md --no-links --no-images https://news.ycombinator.com

# Get token count before committing
html2md --json https://example.com | jq .tokens

# Pipe to file
html2md https://docs.example.com/api > api-docs.md
```
# 金融时报深度阅读器（ft-reader）

使用此技能可以对《金融时报》（ft.com）的顶级文章进行深入、结构化的双语分析。该技能可自动完成登录、文章选择及高质量摘要生成，适用于学术和商业用途。

## 功能特点
- **自动访问**：通过浏览器工具使用存储的凭据登录 FT.com。
- **策略性文章选择**：根据用户偏好筛选“最受欢迎的文章”。
- **双语摘要生成**：提供高保真的中英文摘要，重点突出文章的核心观点。
- **学术严谨性**：提取文章中的具体数据、引文和重要图表。

## 配置与凭据
- **浏览器配置文件**：使用 `openclaw` 配置文件来保持会话状态。
- **凭据**：
  - 用户名：`xxxxxx`
  - 密码：`xxxxxx`

## 工作流程（必经步骤）

### 第1阶段：身份验证与导航
1. 打开 `https://www.ft.com/login`。
2. 输入电子邮件和密码。
3. 导航至首页或用户请求的特定板块。

### 第2阶段：内容提取
1. 使用 `evaluate` 功能从首页中筛选出排名前N的文章（目标标签为 `.o-teaser__heading` 或“最受欢迎的文章”）。
2. 对于每篇文章：
   - 访问文章的URL。
   - 使用以下JavaScript代码提取文章内容：
     ```javascript
     () => {
       const title = document.querySelector('h1')?.innerText;
       const standfirst = document.querySelector('div[class*="standfirst"]')?.innerText;
       const paragraphs = Array.from(document.querySelectorAll('div[class*="article-body"] p, article p'))
         .map(p => p.innerText.trim())
         .filter(text => text.length > 0);
       return { title, summary: standfirst, content: paragraphs.join('\n\n') };
     }
     ```

### 第3阶段：分析与报告生成
为每篇文章生成一份约600字的报告，报告结构如下：
- **标题（中英文）**
- **核心观点（中英文）**
- **论据（中英文）**
- **结论（中英文）**

## 限制要求
- **风格要求**：保持专业、学术化的表达，避免冗余内容（遵循 SOUL.md 的编写规范）。
- **语言要求**：技术术语和核心观点必须同时提供中英文翻译。
- **独立分析**：除非有特殊要求，否则每篇文章应视为独立分析对象。
- **数据处理**：如果需要处理大量文章，请分批次处理以避免数据丢失或报告截断。

## 使用示例
- “Lulu，使用 ft-reader 分析今天最受欢迎的三篇文章。”
- “使用 ft-reader 深入研究《金融时报》上关于人工智能生产力的热门文章。”
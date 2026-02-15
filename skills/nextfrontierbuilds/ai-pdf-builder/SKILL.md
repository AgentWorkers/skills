---
name: ai-pdf-builder
description: 这款由人工智能驱动的PDF生成工具专为法律文件、演示文稿和报告设计，能够生成安全协议（SAFs）、保密协议（NDAs）、条款表（term sheets）以及白皮书（whitepapers）。只需通过`npx ai-pdf-builder`命令即可使用。该工具兼容Claude、Cursor、GPT和Copilot等AI辅助写作工具。
version: 1.2.3
keywords: pdf-generator, ai-pdf, legal-docs, pitch-deck, startup-docs, investor-docs, ai-writing, document-automation, ycombinator, safe-agreement, nda, term-sheet, whitepaper, ai, ai-agent, ai-coding, llm, cursor, claude, claude-code, gpt, copilot, vibe-coding, mcp, agentic, coding-agent
---

# AI PDF Builder

**仅需几秒钟，即可生成符合YC风格的文档。** 这是一款基于AI技术的PDF生成工具，适用于法律文件、提案演示文稿和专业报告的编写。

通过简单的提示，您可以生成安全协议（SAFEs）、保密协议（NDAs）、条款表（term sheets）、白皮书（whitepapers）和备忘录（memos）。该工具支持与Claude、GPT、Cursor等AI编程工具集成。非常适合用于以下场景：
- 白皮书与简报（Whitepapers & Litepapers）
- 条款表（Term Sheets）
- 安全协议与保密协议（SAFEs & NDAs）
- 备忘录与报告（Memos & Reports）
- 法律协议（Legal Agreements）

## v1.1.0的新功能

- **AI内容生成**：使用Claude根据用户提供的提示生成文档
- **`--company` 参数**：通过命令行（CLI）直接插入公司名称
- **`enhance` 命令**：利用AI优化现有内容
- **`summarize` 命令**：从文档中提取执行摘要
- **内容净化**：自动清理AI生成的内容中的冗余或错误信息

## 使用要求

**选项A：本地生成（免费，无限使用）**
```bash
# macOS
brew install pandoc
brew install --cask basictex
sudo tlmgr install collection-fontsrecommended fancyhdr titlesec enumitem xcolor booktabs longtable geometry hyperref graphicx setspace array multirow

# Linux
sudo apt-get install pandoc texlive-full
```

**选项B：云API（即将推出）**
无需安装任何软件。请在ai-pdf-builder.com获取API密钥

**关于AI功能的设置：**
请设置您的Anthropic API密钥：
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

## 使用方法

### 检查系统环境
```bash
npx ai-pdf-builder check
```

### 通过CLI生成文档
```bash
# From markdown file
npx ai-pdf-builder generate whitepaper ./content.md -o output.pdf

# With company name
npx ai-pdf-builder generate whitepaper ./content.md -o output.pdf --company "Acme Corp"

# Document types: whitepaper, memo, agreement, termsheet, safe, nda, report, proposal
```

### 使用AI生成文档（新功能！）
```bash
# Generate a whitepaper from a prompt
npx ai-pdf-builder ai whitepaper "Write a whitepaper about decentralized identity" -o identity.pdf

# Generate with company branding
npx ai-pdf-builder ai whitepaper "AI in healthcare" -o healthcare.pdf --company "HealthTech Inc"

# Generate other document types
npx ai-pdf-builder ai termsheet "Series A for a fintech startup" -o termsheet.pdf
npx ai-pdf-builder ai memo "Q4 strategy update" -o memo.pdf --company "TechCorp"
```

### 优化现有内容（新功能！）
```bash
# Improve and expand existing markdown
npx ai-pdf-builder enhance ./draft.md -o enhanced.md

# Enhance and convert to PDF in one step
npx ai-pdf-builder enhance ./draft.md -o enhanced.pdf --pdf
```

### 生成文档摘要（新功能！）
```bash
# Generate executive summary
npx ai-pdf-builder summarize ./long-document.md -o summary.md

# Summarize as PDF
npx ai-pdf-builder summarize ./report.pdf -o summary.pdf --pdf
```

### 通过代码生成文档
```typescript
import { generateWhitepaper, generateTermsheet, generateSAFE, aiGenerate, enhance, summarize } from 'ai-pdf-builder';

// AI-Generated Whitepaper
const aiResult = await aiGenerate('whitepaper', 
  'Write about blockchain scalability solutions',
  { company: 'ScaleChain Labs' }
);

// Whitepaper from content
const result = await generateWhitepaper(
  '# My Whitepaper\n\nContent here...',
  { title: 'Project Name', author: 'Your Name', version: 'v1.0', company: 'Acme Corp' }
);

if (result.success) {
  fs.writeFileSync('whitepaper.pdf', result.buffer);
}

// Enhance existing content
const enhanced = await enhance(existingMarkdown);

// Summarize a document
const summary = await summarize(longDocument);

// Term Sheet with company
const termsheet = await generateTermsheet(
  '# Series Seed Term Sheet\n\n## Investment Amount\n\n$500,000...',
  { title: 'Series Seed', subtitle: 'Your Company Inc.', company: 'Investor LLC' }
);

// SAFE
const safe = await generateSAFE(
  '# Simple Agreement for Future Equity\n\n...',
  { title: 'SAFE Agreement', subtitle: 'Your Company Inc.' }
);
```

## 文档类型

| 类型 | 功能 | 适用场景 |
|------|----------|----------|
| `whitepaper` | `generateWhitepaper()` | 技术文档、简报 |
| `memo` | `generateMemo()` | 执行摘要 |
| `agreement` | `generateAgreement()` | 法律合同 |
| `termsheet` | `generateTermsheet()` | 投资条款 |
| `safe` | `generateSAFE()` | 安全协议 |
| `nda` | `generateNDA()` | 保密协议 |
| `report` | `generateReport()` | 商业报告 |
| `proposal` | `generateProposal()` | 商业提案 |

## 自定义品牌标识

```typescript
const result = await generateWhitepaper(content, metadata, {
  customColors: {
    primary: '#E85D04',    // Signal Orange
    secondary: '#14B8A6',  // Coordinate Teal
    accent: '#0D0D0D'      // Frontier Dark
  },
  fontSize: 11,
  margin: '1in',
  paperSize: 'letter'
});
```

## 使用说明

当用户请求生成PDF时，请按照以下步骤操作：

1. 确定需要生成的文档类型（白皮书、条款表、备忘录等）。
2. 判断用户是否希望使用AI生成内容，或者已有相关内容。
3. 获取所需内容（用户提供的文本、文件，或使用AI生成）。
4. 如果缺少元数据（如标题、作者、公司名称），请用户提供相关信息。
5. 使用`--company`参数添加公司品牌标识。
6. 检查系统中是否安装了Pandoc（用于格式化文档）：`which pandoc`
7. 如果没有Pandoc，提供安装指南或建议使用云API。
8. 使用相应的函数生成PDF文件。
9. 将生成的PDF文件发送给用户。

**AI命令快速参考：**
- `ai <类型> "<提示>"`：根据提示生成新文档
- `enhance <文件>`：优化现有内容
- `summarize <文件>`：生成文档的执行摘要
- `--company "公司名称"`：在任何命令中添加公司品牌标识

## 链接

- npm仓库：https://www.npmjs.com/package/ai-pdf-builder
- GitHub仓库：https://github.com/NextFrontierBuilds/ai-pdf-builder

---

由[@NextXFrontier](https://x.com/NextXFrontier) 和 [@DLhugly](https://github.com/DLhugly) 共同开发
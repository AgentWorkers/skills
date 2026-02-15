---
name: x-articles
description: 使用人工智能发布能在 Twitter 上迅速传播的文章。这些文章属于长篇内容，能够有效吸引用户的互动。我们采用了经过验证的写作模式，并结合了浏览器自动化技术。该工具兼容 Claude、Cursor 和 OpenClaw 等平台。
version: 1.1.1
keywords: twitter-articles, x-articles, viral-content, twitter-automation, social-media, content-marketing, ai-writing, twitter-threads, engagement, ai, ai-agent, ai-coding, cursor, claude, claude-code, gpt, copilot, vibe-coding, openclaw, moltbot, agentic
---

# X 文章——适用于 Twitter 的病毒式长篇内容创作技巧

**战胜算法**：创作并发布符合 Twitter 病毒式传播规律的 X 文章。

我们利用人工智能技术进行内容格式化，运用特定的写作模式，并通过浏览器自动化工具来完成整个创作流程。同时，我们解决了 Draft.js 编辑器的特殊问题以及图片嵌入的限制。

## 快速参考

### 内容格式规则（至关重要）

X 文章使用 Draft.js 编辑器，该编辑器有一些特殊要求：
- **换行即表示段落分隔**：每个换行符都会创建一个新的段落，并带有间距。
- **所有同一段落的句子必须放在同一行**。
- **使用纯文本，而非 Markdown 格式**：X 文章支持富文本格式，而非 Markdown。
- **禁止使用破折号（—）**：请使用冒号或重新组织句子。

**错误示例：**
```
Sentence one.
Sentence two.
Sentence three.
```

**正确示例：**
```
Sentence one. Sentence two. Sentence three.
```

### 图片嵌入限制（非常重要）

**嵌入的帖子必须始终显示在内容块的末尾，而不能内联显示。**

解决方法：
- 在文章结构中添加“详见下文”的引用。
- 保持文本的阅读流畅性：先展示正文，再在底部插入嵌入内容。
- 使用“插入 > 帖子”菜单来添加图片（切勿直接粘贴图片链接）。

### 图片规格

| 图片类型 | 宽高比 | 推荐尺寸 |
|------|--------------|------------------|
| 封面/标题图片 | 5:2 | 1792x716 或类似尺寸 |
| 内联图片 | 16:9 或 4:3 | 1792x1024（DALL-E HD 格式） |

## 病毒式文章的结构

### 模板示例
```
HOOK (hit insecurity or opportunity)

WHAT IT IS (1-2 paragraphs with social proof)

WHY MOST PEOPLE WON'T DO IT (address objections)

THE [X]-MINUTE GUIDE
- Step 1 (time estimate)
- Step 2 (time estimate)
- ...

YOUR FIRST [N] WINS (immediate value)
- Win 1: copy-paste example
- Win 2: copy-paste example

THE COST (value comparison)

WHAT TO DO AFTER (next steps)

THE WINDOW (urgency)

CTA (soft or hard)
```

### 有效的写作模式

- **引发不安感/恐惧错失感（Insecurity/FOMO）**：
```
everyone's talking about X... and you're sitting there wondering if you missed the window
```

- **重大机会（Big Opportunity）**：
```
this is the biggest opportunity of our lifetime
```

- **新闻类内容（News Hook）**：
```
X just open sourced the algo. Here's what it means for you:
```

- **悼念类内容（RIP Pattern）**：
```
RIP [profession]. This AI tool will [action] in seconds.
```

- **令人震惊的内容（WTF Pattern）**：
```
WTF!! This AI Agent [does amazing thing]. Here's how:
```

- **个人故事（Personal Story）**：
```
When I was young, I was always drawn to people who...
```

### 呼吁行动（CTA）模式

- **强制性的呼吁行动（Hard CTA）**：
```
RT + follow + reply 'KEYWORD' and I'll send the cheat sheet
```

- **温和的呼吁行动（Soft CTA）**：
```
If you take this advice and build something, let me know!
```

- **简单明了的呼吁行动（Simple CTA）**：
```
Feel free to leave a like and RT if this helped.
```

## 风格指南

### Damian Player 风格（策略性）：
- 全部使用小写字母（有意为之）。
- 语气紧迫且具有策略性。
- 文章长度超过 1500 字。
- 包含详细的步骤说明。
- 强制性的呼吁行动，并设置吸引读者的开头内容。

### Alex Finn 风格（激励性）：
- 使用常规大小写。
- 语气温暖且具有激励性。
- 文章长度在 800 到 1200 字之间。
- 结合“为什么”和“如何”进行讲解。
- 使用温和的呼吁行动，并附上产品链接。

### Dan Koe 风格（哲学性）：
- 长篇论文风格（超过 2000 字）。
- 以个人故事开头。
- 使用特定的框架（如“金字塔原则”）。
- 侧重于深度教学，而不仅仅是策略性内容。
- 文章末尾包含订阅新闻通讯的呼吁行动。

## 需避免的常见错误：

- 文章长度过短（少于 500 字）。
- 只提供事实而没有故事或情感表达。
- 没有明确的章节划分和标题。
- 未处理读者的反对意见。
- 没有“立即见效”的部分。
- 没有呼吁行动。
- 使用过于生硬的、类似人工智能的语言。
- 过度使用破折号（—）。
- 过量使用表情符号。
- 直接粘贴 Twitter 链接，而不是使用“插入”菜单。

## 浏览器自动化工具（agent-browser）

### 先决条件：
- 确保在浏览器中运行 clawd，且 clawd 正在监听 CDP 端口 18800。
- 已在 Twitter 上登录。

### 导航到文章编辑器
```bash
# Open new article
agent-browser --cdp 18800 navigate "https://x.com/compose/article"

# Take snapshot to see current state
agent-browser --cdp 18800 snapshot
```

### 粘贴内容
```bash
# Put content in clipboard
cat article.txt | pbcopy

# Click content area, select all, paste
agent-browser --cdp 18800 click '[contenteditable="true"]'
agent-browser --cdp 18800 press "Meta+a"
agent-browser --cdp 18800 press "Meta+v"
```

### 上传封面图片
```bash
# Upload to file input
agent-browser --cdp 18800 upload 'input[type="file"]' /path/to/cover.png

# Wait for Edit media dialog, click Apply
agent-browser --cdp 18800 snapshot | grep -i apply
agent-browser --cdp 18800 click @e5  # Apply button ref
```

### 发布文章
```bash
# Find and click Publish button
agent-browser --cdp 18800 snapshot | grep -i publish
agent-browser --cdp 18800 click @e35  # Publish button ref

# Confirm in dialog
agent-browser --cdp 18800 click @e5   # Confirm
```

### 清理工作（非常重要！）
```bash
# Close tab after publishing
agent-browser --cdp 18800 tab list
agent-browser --cdp 18800 tab close 1
```

### 故障排除：过时的元素引用

如果点击链接失败，可能是由于元素引用失效导致的。此时可以使用 JavaScript 进行检查：
```bash
agent-browser --cdp 18800 evaluate "(function() { 
  const btns = document.querySelectorAll('button'); 
  for (let btn of btns) { 
    if (btn.innerText.includes('Publish')) { 
      btn.click(); 
      return 'clicked'; 
    } 
  } 
  return 'not found'; 
})()"
```

## 内容准备脚本

### 将 Markdown 格式转换为适合 X 文章的格式
```bash
# scripts/format-for-x.sh
#!/bin/bash
# Converts markdown to X Articles format

INPUT="$1"
OUTPUT="${2:-${INPUT%.md}-x-ready.txt}"

cat "$INPUT" | \
  # Remove markdown headers, keep text
  sed 's/^## /\n/g' | \
  sed 's/^### /\n/g' | \
  sed 's/^# /\n/g' | \
  # Remove markdown bold/italic
  sed 's/\*\*//g' | \
  sed 's/\*//g' | \
  # Remove em dashes
  sed 's/ — /: /g' | \
  sed 's/—/:/g' | \
  # Join lines within paragraphs (keeps blank lines as separators)
  awk 'BEGIN{RS=""; FS="\n"; ORS="\n\n"} {gsub(/\n/, " "); print}' \
  > "$OUTPUT"

echo "Created: $OUTPUT"
```

## 发布前的检查清单：
- [ ] 引言部分能够吸引读者的注意力。
- [ ] 早期处理了读者的反对意见。
- [ ] 有详细的步骤说明及时间预估。
- [ ] 包含“立即见效”的部分。
- [ ] 文章末尾有呼吁行动。
- [ ] 不使用破折号（—）。
- [ ] 所有句子都放在同一行。
- [ ] 封面图片的宽高比为 5:2。
- [ ] 嵌入内容引用格式为“详见下文”。
- [ ] 校对文章，避免使用类似人工智能的语言。

## 适合推文的引用格式

用于推广文章的引用格式：
- **结果 + 成本（Result + Cost）**：
```
I gave an AI agent full access to my MacBook. It checks email, manages calendar, pushes code. Costs $20/month. A VA costs $2000.
```

- **你不需要 X（You Don't Need X）**：
```
You don't need a Mac Mini. You don't need a server. I'm running my AI agent on an old MacBook Air from a drawer.
```

- **风险警告（Gap Warning）**：
```
The gap between 'has AI agent' and 'doesn't' is about to get massive. I set mine up in 15 minutes.
```

- **紧迫性（Urgency）**：
```
Most people will bookmark this and never set it up. Don't be most people. The window is closing.
```

## 示例工作流程：

1. 用 Markdown 编写文章，并设置清晰的章节结构。
2. 运行格式转换脚本，将Markdown 转换为适合 X 文章的纯文本格式。
3. 使用 DALL-E 生成封面图片（尺寸为 1792x716 或 5:2）。
4. 通过浏览器自动化工具打开 X 文章编辑器。
5. 在编辑器中手动添加内容及章节标题。
6. 通过文件上传封面图片。
7. 在章节分隔处插入内联图片。
8. 添加嵌入内容（它们会显示在文章底部）。
9. 预览并校对文章。
10. 发布文章。
11. 发布包含引用和文章链接的推文。

## 相关技能：

- `bird`：用于发布推文的 CLI 工具（适用于 X/Twitter）。
- `de-ai-ify`：用于去除文本中的 AI 语言风格。
- `ai-pdf-builder`：用于生成 PDF 文件（用于吸引潜在客户）。

---

由 [@NextXFrontier](https://x.com/NextXFrontier) 制作
---
name: undetectable-ai
description: **使AI生成的文本无法被检测出来**：  
这是一个TypeScript命令行工具（CLI），用于扫描ChatGPT、Claude、OpenClaw等AI工具生成的文本，查找那些被GPTZero、Turnitin或Originality.ai标记为“非人类编写”的模式，并自动修复这些文本，使其看起来像是人类创作的。该工具可用于绕过AI检测机制、规避审核流程，或在提交前让文本更具“人性化”（即更像人类撰写的文本）。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# 难以被检测到的AI内容

这是一套TypeScript命令行工具（CLI），通过去除AI内容检测器能够识别的特征性模式来绕过这些检测。

## 设置

```bash
cd scripts && npm install
```

## 脚本

### analyze.ts — 扫描可检测的模式

该脚本会查找AI检测器会关注的模式，例如词汇、句子结构以及特定的文本特征。

```bash
# Analyze a file
npx ts-node scripts/analyze.ts input.txt

# From stdin
echo "This serves as a testament" | npx ts-node scripts/analyze.ts

# JSON output
npx ts-node scripts/analyze.ts input.txt --json
```

**输出结果：**
```
==================================================
AI DETECTION SCAN - 5 issues found
==================================================

AI VOCABULARY:
  • testament: 1x
  • crucial: 2x

AUTO-FIXABLE:
  • "serves as" → "is": 1x
```

---

### transform.ts — 自动修复文本模式

该脚本会自动修改文本，以规避检测器的识别。

**修复的内容包括：**
- 填充语：将“in order to”替换为“to”
- AI特有的词汇：将“utilize”替换为“use”，将“leverage”替换为“use”
- 句子开头部分：删除“Additionally,”、“Furthermore”等引导词
- 聊天机器人生成的文本：删除包含“I hope this helps”等内容的完整句子
- 弯引号：将弯引号替换为直引号
- 修复后的文本中的大小写问题

---

## 工作流程

1. **扫描**以评估文本的检测风险：
   ```bash
   npx ts-node scripts/analyze.ts essay.txt
   ```

2. **自动修复**常见的文本模式问题：
   ```bash
   npx ts-node scripts/transform.ts essay.txt -o essay_clean.txt
   ```

3. **对标记为AI内容的词汇进行手动处理**（需要人工判断）
4. **重新扫描**以验证修复效果：
   ```bash
   npx ts-node scripts/analyze.ts essay_clean.txt
   ```

---

## 自定义设置

编辑 `scripts/patterns.json` 文件：
- `ai_words`：需要手动处理的AI相关词汇
- `puffery`：需要标记的促销性语言
- `replacements`：自动替换的规则
- `chatbot_artifacts`：会导致整段文本被删除的特定短语

---

## 批量处理

```bash
# Scan all docs
for f in *.txt; do
  echo "=== $f ==="
  npx ts-node scripts/analyze.ts "$f"
done

# Transform all
for f in *.md; do
  npx ts-node scripts/transform.ts "$f" -o "${f%.md}_clean.md" -q
done
```
---
name: humanize-ai
description: 通过检测和自动修复由 AI 生成的内容来使 AI 文本更加自然化。可以使用 Python 脚本来实现这一目标：扫描文本中是否存在 AI 特有的词汇、夸大其词的表述或聊天机器人的痕迹，并自动替换这些填充性语言。当您需要对文本进行 AI 检测、绕过检测结果、批量处理文件、执行自动化清理操作，或在手动优化之前获取分析报告时，这种方法非常实用。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# 使命令行工具更具人性化（Humanize CLI Tools）

这些命令行工具用于检测和自动修复人工智能生成的文本模式。

## 脚本（Scripts）

### analyze.py — 检测人工智能生成的文本模式

扫描文本，并报告其中的人工智能词汇、夸夸其谈的表述以及聊天机器人生成的文本片段。

```bash
# Analyze a file
python scripts/analyze.py input.txt

# Analyze from stdin
echo "This serves as a testament to our commitment" | python scripts/analyze.py

# JSON output for programmatic use
python scripts/analyze.py input.txt --json
```

**输出示例：**
```
==================================================
AI PATTERN ANALYSIS - 5 issues found
==================================================

AI VOCABULARY:
  • testament: 1x
  • crucial: 2x

AUTO-REPLACEABLE:
  • "serves as" → "is": 1x
  • "in order to" → "to": 1x
```

---

### humanize.py — 自动替换这些模式

自动替换常见的人工智能生成的文本特征。

```bash
# Humanize and print to stdout
python scripts/humanize.py input.txt

# Write to output file
python scripts/humanize.py input.txt -o output.txt

# Include em dash replacement
python scripts/humanize.py input.txt --fix-dashes

# Quiet mode (no change log)
python scripts/humanize.py input.txt -q
```

**自动修复的内容包括：**
- 填充词：将 "in order to" 替换为 "to"，将 "due to the fact that" 替换为 "because"
- 避免使用连系动词：将 "serves as" 替换为 "is"，将 "boasts" 替换为 "has"
- 句子开头语：删除 "Additionally," "Furthermore," "Moreover" 等
- 弯引号替换为直引号
- 聊天机器人生成的文本片段：删除 "I hope this helps", "Let me know if" 等

---

## 工作流程（Workflow）

1. **首先进行分析**，确定哪些内容需要修复：
   ```bash
   python scripts/analyze.py document.txt
   ```

2. **自动进行安全替换**：
   ```bash
   python scripts/humanize.py document.txt -o document_clean.txt
   ```

3. **手动审核** 分析工具标记为人工智能生成的词汇和夸夸其谈的表述（这些需要人工判断）

4. **重新分析**，确认修复效果：
   ```bash
   python scripts/analyze.py document_clean.txt
   ```

---

## 自定义修复规则（Customizing Repair Rules）

编辑 `scripts/patterns.json` 文件以添加或删除以下内容：
- `ai_words`：需要标记但不会自动替换的词汇
- `puffery`：需要标记的夸夸其谈的表述
- `replacements`：词组与替换内容的映射关系（空字符串表示删除该词组）
- `chatbot_artifacts`：需要自动删除的聊天机器人生成的文本片段
- `hedging_phrases`：需要标记的过度使用缓和语气的表达

---

## 批量处理（Batch Processing）

可以同时处理多个文件：
```bash
# Analyze all markdown files
for f in *.md; do
  echo "=== $f ===" 
  python scripts/analyze.py "$f"
done

# Humanize all txt files in place
for f in *.txt; do
  python scripts/humanize.py "$f" -o "$f.tmp" && mv "$f.tmp" "$f"
done
```
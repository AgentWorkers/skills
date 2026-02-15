---
name: humanize-ai-text
description: 将AI生成的内容进行“人性化”处理，以规避检测。该工具能够重新编写ChatGPT、Claude和GPT生成的内容，使其听起来更加自然，从而通过GPTZero、Turnitin和Originality.ai等AI检测工具的验证。其原理基于维基百科提供的关于“AI写作特征”的详细指南，能够使机器生成的文本看起来完全像人类撰写的作品，从而难以被识别出来。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# 使AI文本更自然

这是一个全面的命令行工具（CLI），用于检测和转换由AI生成的文本，以规避检测机制。该工具基于维基百科关于AI写作特征的描述（https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing）。

## 快速入门

```bash
# Detect AI patterns
python scripts/detect.py text.txt

# Transform to human-like
python scripts/transform.py text.txt -o clean.txt

# Compare before/after
python scripts/compare.py text.txt -o clean.txt
```

---

## 检测类别

该分析工具会检查维基百科指南中列出的**16种模式**：

### 关键性模式（立即可检测到AI的痕迹）
| 类别 | 例子 |
|----------|----------|
| 引用错误 | `oaicite`, `turn0search`, `contentReference` |
| 知识断层 | “根据我最后一次训练的结果”，“基于现有信息” |
| 聊天机器人特征 | “希望这能有所帮助”，“非常好的问题！”，“作为一个AI” |
| Markdown格式 | `**粗体**`, `## 标题`, ```代码块``` |

### 高度提示性模式
| 类别 | 例子 |
|----------|----------|
| AI特有的词汇 | `devel`, `tapestry`, `landscape`, `pivotal`, `underscore`, `foster` |
| 过度使用修饰性语言 | “作为……的证明”，“关键时刻”，“不可磨灭的印记” |
| 过度使用宣传性语言 | “充满活力”，“开创性的”，“令人惊叹的” |
| 避免使用连词 | 用“serves as”代替“is”，用“boasts”代替“has” |

### 中等提示性模式
| 类别 | 例子 |
| 表面化的修饰词 | “强调……的重要性”，“促进合作” |
| 填充性短语 | “为了……”，“由于……”，“此外” |
| 模糊的表述 | “专家认为”，“行业报告显示” |
| 陈词滥调 | “尽管存在这些挑战”，“未来前景” |

### 风格特征
| 类别 | 例子 |
|----------|----------|
| 使用引号的方式 | 使用“""”代替“''”（ChatGPT的典型特征） |
| 过度使用破折号 | 过度使用破折号来强调 |
| 负面的平行结构 | “不仅……而且……”，“不仅仅是……而是……” |

---

## 脚本

### detect.py — 检测AI写作特征

```bash
python scripts/detect.py essay.txt
python scripts/detect.py essay.txt -j  # JSON output
python scripts/detect.py essay.txt -s  # score only
echo "text" | python scripts/detect.py
```

**输出：**
- 问题数量和单词数量
- AI文本的概率（低/中/高/非常高）
- 按类别分类的统计结果
- 可自动修复的错误会被标记出来

### transform.py — 重写文本

```bash
python scripts/transform.py essay.txt
python scripts/transform.py essay.txt -o output.txt
python scripts/transform.py essay.txt -a  # aggressive
python scripts/transform.py essay.txt -q  # quiet
```

**自动修复内容：**
- 引用错误（oaicite, turn0search）
- Markdown格式（**粗体**, `## 标题`, ```代码块```）
- 聊天机器人特征明显的句子
- 避免使用连词（将“is/has”替换为“serves as/has”）
- 填充性短语替换为更简洁的形式
- 将引号从```改为```

**高级选项（-a）：**
- 简化含有“-ing”的从句
- 减少破折号的使用

### compare.py — 转换前后的对比分析

```bash
python scripts/compare.py essay.txt
python scripts/compare.py essay.txt -a -o clean.txt
```

显示转换前后的检测结果对比

---

## 工作流程

1. **扫描**以识别潜在的AI写作特征：
   ```bash
   python scripts/detect.py document.txt
   ```

2. **使用该工具进行文本转换**：
   ```bash
   python scripts/compare.py document.txt -o document_v2.txt
   ```

3. **验证**改进效果：
   ```bash
   python scripts/detect.py document_v2.txt -s
   ```

4. **人工审核**以检查是否存在AI特有的词汇或宣传性语言（需要判断）

---

## AI文本概率评分

| 评分标准 | 判断依据 |
|--------|----------|
| 非常高 | 存在引用错误、知识断层或聊天机器人特征 |
| 高 | 问题数量超过30个或问题密度超过5% |
| 中等 | 问题数量超过15个或问题密度超过2% |
| 低 | 问题数量少于15个且问题密度低于2% |

---

## 自定义检测规则

编辑 `scripts/patterns.json` 文件来添加或修改以下规则：
- `ai_vocabulary` — 需要标记的AI词汇
- `significance_inflation` — 过度使用的修饰性语言
- `promotional_language` — 宣传性语言的表述
- `copula_avoidance` — 需要替换的连词短语
- `filler_replacements` — 需要简化的语句片段
- `chatbot_artifacts` — 需要移除的聊天机器人特征相关的短语

---

## 批量处理

```bash
# Scan all files
for f in *.txt; do
  echo "=== $f ==="
  python scripts/detect.py "$f" -s
done

# Transform all markdown
for f in *.md; do
  python scripts/transform.py "$f" -a -o "${f%.md}_clean.md" -q
done
```

---

## 参考资料

该工具基于维基百科的《AI写作特征》（https://en.wikipedia.org/wiki/Wikipedia:Signs_of.AI_writing），该资料由WikiProject AI Cleanup项目维护。所有检测规则都是从数千个AI生成的文本中总结出来的。

关键点：**大型语言模型（LLMs）使用统计算法来预测接下来的内容。其生成的结果往往是统计上最有可能出现的，且适用于最广泛的情况。**
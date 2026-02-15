---
name: Text
description: 使用模式对文本进行转换、格式化和处理，以用于写作、数据清洗、本地化、引用和文案创作。
---

## 快速参考

| 任务 | 对应的文档文件 |
|------|------|
| 创意写作（语音、对话、视角） | `writing.md` |
| 数据处理（CSV、正则表达式、编码） | `data.md` |
| 学术写作/引用（APA、MLA、Chicago格式） | `academic.md` |
| 市场营销文案（标题、呼叫行动语句、电子邮件） | `copy.md` |
| 翻译/本地化 | `localization.md` |

---

## 通用文本处理规则

### 编码
- **务必先验证编码格式：** `file -bi document.txt`
- **统一行尾格式：** `tr -d '\r'`
- **如果存在BOM（字节顺序标记），请将其删除：** `sed -i '1s/^\xEF\xBB\xBF/'`

### 空格处理
- **合并多个空格：** `sed 's/[[:space:]]\+/ /g'`
- **删除开头/结尾的空格：** `sed 's/^[[:space:]]*//;s/[[:space:]]*$/'`

### 常见问题
- **智能引号（`"`、“`）会破坏解析器的工作 → 将其统一为普通引号（`"`）**
- **破折号（`–`、`—`）在ASCII编码中可能导致问题 → 将其统一为普通破折号（`-`）**
- **零宽度字符** 虽不可见但会影响比较结果 → 请将其删除**
- **在UTF-8编码中，字符串长度与字节长度可能不同（例如：“café”实际占用5个字节）**

---

## 格式检测

```bash
# Detect encoding
file -I document.txt

# Detect line endings
cat -A document.txt | head -1
# ^M at end = Windows (CRLF)
# No ^M = Unix (LF)

# Detect delimiter (CSV/TSV)
head -1 file | tr -cd ',;\t|' | wc -c
```

---

## 常用转换命令

| 任务 | 对应的命令 |
|------|---------|
| 将所有字符转换为小写：`tr '[:upper:]' '[:lower:]'` |
| 删除标点符号：`tr -d '[:punct:]'` |
| 统计单词数量：`wc -w` |
| 统计唯一行数：`sort -u \| wc -l` |
| 查找重复行：`sort \| uniq -d` |
| 提取电子邮件地址：`grep -oE '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'` |
| 提取URL地址：`grep -oE 'https?://[^[:space:]<>"{}|\\^`\[\]]+'` |

---

## 处理前的检查清单
- [ ] 是否已验证编码格式（UTF-8）？
- [ ] 是否已统一行尾格式？
- [ ] 是否已确定目标文本的格式/样式？
- [ ] 是否已考虑了特殊情况（空字符串、Unicode字符、特殊符号）？
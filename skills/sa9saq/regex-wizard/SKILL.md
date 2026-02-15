---
description: 根据自然语言描述生成正则表达式，对其进行测试，并解释其工作原理。
---

# 正则表达式生成器

能够根据用户提供的描述生成、测试并解释正则表达式。

## 所需工具

- 用于测试正则表达式的工具：`python3`、`grep -P` 或 `node`（至少需要其中一个）
- 不需要 API 密钥

## 使用说明

### 根据描述生成正则表达式
1. 澄清模糊的要求（例如：是否支持多行匹配、全局匹配、是否不区分大小写等）
2. 生成符合指定语法风格（Python、JavaScript、PCRE、Go）的正则表达式模式
3. 用通俗的语言解释正则表达式的每个组成部分
4. 提供 3 个以上的匹配示例和 2 个以上的不匹配示例

### 解释现有的正则表达式
1. 将正则表达式拆分为各个部分（如子表达式、分组等），并添加内联注释
2. 用简单的语言进行解释（避免使用专业术语）
3. 提供匹配和不匹配的示例字符串
4. 明确说明所使用的语法风格及其特有的功能

### 对字符串测试正则表达式
使用生成的正则表达式对提供的测试字符串进行匹配测试：
```bash
# Python (most portable)
python3 -c "
import re
pattern = r'YOUR_PATTERN'
tests = ['test1', 'test2', 'test3']
for t in tests:
    m = re.search(pattern, t)
    print(f'{t!r}: {\"✅ Match\" if m else \"❌ No match\"}' + (f' → groups: {m.groups()}' if m else ''))
"

# Grep (quick check)
echo "test string" | grep -P 'pattern'
```

### 输出格式
```
**Pattern**: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
**Flavor**: Python/PCRE
**Flags**: None

| Component | Meaning |
|-----------|---------|
| `^` | Start of string |
| `[a-zA-Z0-9._%+-]+` | One or more valid email chars |
| `@` | Literal @ |
| `[a-zA-Z0-9.-]+` | Domain name |
| `\.[a-zA-Z]{2,}$` | TLD (2+ letters) at end |

**Matches**: `user@example.com`, `a.b+c@test.co.uk`
**Non-matches**: `@example.com`, `user@`, `user@.com`
```

## 常见的问题及注意事项

- **贪婪匹配与懒惰匹配**：`.*` 与 `.*?` 的区别——说明在什么情况下需要区分这两种匹配方式
- **灾难性的回溯**：嵌套的量词（如 `(a+)+`）可能会导致问题，务必注意这类情况
- **未转义的点（`.`）**：`.` 表示匹配任意字符，而不仅仅是字面意义上的点
- **锚点（`^`/`$`）**：缺少这些锚点可能会导致部分匹配
- **Unicode**：`\w` 的行为因编程语言而异（Python 3 默认支持 Unicode）

## 特殊情况

- **电子邮件/URL 验证**：提醒用户，用于这些场景的正则表达式通常非常复杂，建议在生产环境中使用专门的库
- **多行输入**：提醒用户需要使用 `re.DOTALL` 或 `re.MULTILINE` 标志
- **空字符串匹配**：像 `.*` 这样的正则表达式会匹配空字符串——请明确说明是否允许这种情况发生

## 安全性建议

- 在生产环境中，切勿直接使用用户提供的正则表达式，应设置超时限制或防止无限循环（以避免 ReDoS 攻击）
- 在使用用户数据测试正则表达式时，务必对输出结果中的字符串进行清洗处理
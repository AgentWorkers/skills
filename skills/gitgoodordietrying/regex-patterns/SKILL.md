---
name: regex-patterns
description: 实用的正则表达式模式及其应用场景：可用于验证输入（如电子邮件、URL、IP地址）、解析日志行、从文本中提取数据、通过“查找并替换”功能重构代码，或调试正则表达式为何无法匹配目标内容。
metadata: {"clawdbot":{"emoji":"🔤","requires":{"anyBins":["grep","python3","node"]},"os":["linux","darwin","win32"]}}
---

# 正则表达式模式

这是一本实用的正则表达式指南，涵盖了在 JavaScript、Python、Go 和命令行工具中用于验证、解析、提取数据以及重构代码的模式。

## 使用场景

- 验证用户输入（电子邮件、URL、IP 地址、电话号码、日期）
- 解析日志行或结构化文本
- 从字符串中提取数据（如 ID、数字、标记）
- 在代码中进行查找和替换操作（例如重命名变量、更新导入语句）
- 过滤文件或命令输出中的行
- 调试无法按预期匹配的正则表达式

## 快速参考

### 元字符

| 正则表达式 | 匹配内容 | 示例 |
|---|---|---|
| `.` | 任意字符（换行符除外） | `a.c` 匹配 `abc` 和 `a1c` |
| `\d` | 数字 `[0-9]` | `\d{3}` 匹配 `123` |
| `\w` | 字符 `[a-zA-Z0-9_>` | `\w+` 匹配 `hello_123` |
| `\s` | 空白字符 `[ \t\n\r\f]` | `\s+` 匹配多个空白字符 |
| `\b` | 单词边界 | `\bcat\b` 匹配 `cat` 而不是 `scatter` |
| `^` | 行首 | `^Error` 匹配以 `Error` 开头的行 |
| `$` | 行尾 | `\.js$` 匹配以 `.js` 结尾的行 |
| `\D`, `\W`, `\S` | 表示非数字、非单词、非空白字符 |

### 量词

| 正则表达式 | 含义 |
|---|---|
| `*` | 0 个或多个（贪婪匹配） |
| `+` | 1 个或多个（贪婪匹配） |
| `?` | 0 个或 1 个（可选） |
| `{3}` | 恰好 3 个 |
| `{2,5}` | 2 到 5 个 |
| `{3,}` | 3 个或更多 |
| `*?`, `+?` | 非贪婪匹配（尽可能少地匹配） |

### 组合和选择

| 正则表达式 | 含义 |
|---|---|
| `(abc)` | 捕获组 |
| `(?:abc)` | 非捕获组 |
| `(?P<name>abc)` | 命名捕获组（Python） |
| `(?<name>abc)` | 命名捕获组（JavaScript/Go） |
| `a\|b` | 选择（a 或 b） |
| `[abc]` | 字符类（a、b 或 c） |
| `[^abc]` | 非字符类（不是 a、b 或 c） |
| `[a-z]` | 字符范围 |

### 前瞻和后瞻

| 正则表达式 | 含义 |
|---|---|
| `(?=abc)` | 正向前瞻（后面必须跟着 abc） |
| `(?!abc)` | 负向前瞻（后面不能跟着 abc） |
| `(?<=abc)` | 正向后瞻（前面必须跟着 abc） |
| `(?<!abc)` | 负向后瞻（前面不能跟着 abc） |

## 验证模式

### 电子邮件验证

```
# Basic (covers 99% of real emails)
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$

# Stricter (no consecutive dots, no leading/trailing dots in local part)
^[a-zA-Z0-9]([a-zA-Z0-9._%+-]*[a-zA-Z0-9])?@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z]{2,})+$
```

### URL 验证

```
# HTTP/HTTPS URLs
https?://[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*(/[^\s]*)?

# With optional port and query
https?://[^\s/]+(/[^\s?]*)?(\?[^\s#]*)?(#[^\s]*)?
```

### IP 地址验证

```
# IPv4
\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b

# IPv4 (simple, allows invalid like 999.999.999.999)
\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b

# IPv6 (simplified)
(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}
```

### 电话号码验证

```
# US phone (various formats)
(?:\+1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}
# Matches: +1 (555) 123-4567, 555.123.4567, 5551234567

# International (E.164)
\+[1-9]\d{6,14}
```

### 日期和时间格式验证

```
# ISO 8601 date
\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])

# ISO 8601 datetime
\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})

# US date (MM/DD/YYYY)
(?:0[1-9]|1[0-2])/(?:0[1-9]|[12]\d|3[01])/\d{4}

# Time (HH:MM:SS, 24h)
(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d
```

### 密码强度检查

```
# At least 8 chars, 1 upper, 1 lower, 1 digit, 1 special
^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+=-]).{8,}$
```

### UUID 验证

```
[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}
```

### 语义版本验证

```
\bv?(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?(?:\+([\w.]+))?\b
# Captures: major, minor, patch, prerelease, build
# Matches: 1.2.3, v1.0.0-beta.1, 2.0.0+build.123
```

## 解析模式

### 日志行解析

```bash
# Apache/Nginx access log
# Format: IP - - [date] "METHOD /path HTTP/x.x" status size
grep -oP '(\S+) - - \[([^\]]+)\] "(\w+) (\S+) \S+" (\d+) (\d+)' access.log

# Extract IP and status code
grep -oP '^\S+|"\s\K\d{3}' access.log

# Syslog format
# Format: Mon DD HH:MM:SS hostname process[pid]: message
grep -oP '^\w+\s+\d+\s[\d:]+\s(\S+)\s(\S+)\[(\d+)\]:\s(.*)' syslog

# JSON log — extract a field
grep -oP '"level"\s*:\s*"\K[^"]+' app.log
grep -oP '"message"\s*:\s*"\K[^"]+' app.log
```

### 代码模式解析

```bash
# Find function definitions (JavaScript/TypeScript)
grep -nP '(?:function\s+\w+|(?:const|let|var)\s+\w+\s*=\s*(?:async\s*)?\([^)]*\)\s*=>|(?:async\s+)?function\s*\()' src/*.ts

# Find class definitions
grep -nP 'class\s+\w+(?:\s+extends\s+\w+)?' src/*.ts

# Find import statements
grep -nP '^import\s+.*\s+from\s+' src/*.ts

# Find TODO/FIXME/HACK comments
grep -rnP '(?:TODO|FIXME|HACK|XXX|WARN)(?:\([^)]+\))?:?\s+' src/

# Find console.log left in code
grep -rnP 'console\.(log|debug|info|warn|error)\(' src/ --include='*.ts' --include='*.js'
```

### 数据提取

```bash
# Extract all email addresses from a file
grep -oP '[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' file.txt

# Extract all URLs
grep -oP 'https?://[^\s<>"]+' file.html

# Extract all quoted strings
grep -oP '"[^"\\]*(?:\\.[^"\\]*)*"' file.json

# Extract numbers (integer and decimal)
grep -oP '-?\d+\.?\d*' data.txt

# Extract key-value pairs (key=value)
grep -oP '\b(\w+)=([^\s&]+)' query.txt

# Extract hashtags
grep -oP '#\w+' posts.txt

# Extract hex colors
grep -oP '#[0-9a-fA-F]{3,8}\b' styles.css
```

## 特定语言的用法

### JavaScript

```javascript
// Test if a string matches
const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
emailRegex.test('user@example.com'); // true

// Extract with capture groups
const match = '2026-02-03T12:30:00Z'.match(/(\d{4})-(\d{2})-(\d{2})/);
// match[1] = '2026', match[2] = '02', match[3] = '03'

// Named groups
const m = 'John Doe, age 30'.match(/(?<name>[A-Za-z ]+), age (?<age>\d+)/);
// m.groups.name = 'John Doe', m.groups.age = '30'

// Find all matches (matchAll returns iterator)
const text = 'Call 555-1234 or 555-5678';
const matches = [...text.matchAll(/\d{3}-\d{4}/g)];
// [{0: '555-1234', index: 5}, {0: '555-5678', index: 18}]

// Replace with callback
'hello world'.replace(/\b\w/g, c => c.toUpperCase());
// 'Hello World'

// Replace with named groups
'2026-02-03'.replace(/(?<y>\d{4})-(?<m>\d{2})-(?<d>\d{2})/, '$<m>/$<d>/$<y>');
// '02/03/2026'

// Split with regex
'one, two;  three'.split(/[,;]\s*/);
// ['one', 'two', 'three']
```

### Python

```python
import re

# Match (anchored to start)
m = re.match(r'^(\w+)@(\w+)\.(\w+)$', 'user@example.com')
if m:
    print(m.group(1))  # 'user'

# Search (find first match anywhere)
m = re.search(r'\d{3}-\d{4}', 'Call 555-1234 today')
print(m.group())  # '555-1234'

# Find all matches
emails = re.findall(r'[\w.+-]+@[\w.-]+\.\w{2,}', text)

# Named groups
m = re.match(r'(?P<name>\w+)\s+(?P<age>\d+)', 'Alice 30')
print(m.group('name'))  # 'Alice'

# Substitution
result = re.sub(r'\bfoo\b', 'bar', 'foo foobar foo')
# 'bar foobar bar'

# Sub with callback
result = re.sub(r'\b\w', lambda m: m.group().upper(), 'hello world')
# 'Hello World'

# Compile for reuse (faster in loops)
pattern = re.compile(r'\d{4}-\d{2}-\d{2}')
dates = pattern.findall(log_text)

# Multiline and DOTALL
re.findall(r'^ERROR.*$', text, re.MULTILINE)  # ^ and $ match line boundaries
re.search(r'start.*end', text, re.DOTALL)      # . matches newlines

# Verbose mode (readable complex patterns)
pattern = re.compile(r'''
    ^                   # Start of string
    (?P<year>\d{4})     # Year
    -(?P<month>\d{2})   # Month
    -(?P<day>\d{2})     # Day
    $                   # End of string
''', re.VERBOSE)
```

### Go

```go
import "regexp"

// Compile pattern (panics on invalid regex)
re := regexp.MustCompile(`\d{4}-\d{2}-\d{2}`)

// Match test
re.MatchString("2026-02-03")  // true

// Find first match
re.FindString("Date: 2026-02-03 and 2026-03-01")  // "2026-02-03"

// Find all matches
re.FindAllString(text, -1)  // []string of all matches

// Capture groups
re := regexp.MustCompile(`(\w+)@(\w+)\.(\w+)`)
match := re.FindStringSubmatch("user@example.com")
// match[0] = "user@example.com", match[1] = "user", match[2] = "example"

// Named groups
re := regexp.MustCompile(`(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})`)
match := re.FindStringSubmatch("2026-02-03")
for i, name := range re.SubexpNames() {
    if name != "" {
        fmt.Printf("%s: %s\n", name, match[i])
    }
}

// Replace
re.ReplaceAllString("foo123bar", "NUM")  // "fooNUMbar"

// Replace with function
re.ReplaceAllStringFunc(text, strings.ToUpper)

// Note: Go uses RE2 syntax — no lookahead/lookbehind
```

### 命令行工具（grep/sed）

```bash
# grep -P uses PCRE (Perl-compatible — full features)
# grep -E uses Extended regex (no lookahead/lookbehind)

# Find lines matching a pattern
grep -P '\d{3}-\d{4}' file.txt

# Extract only the matching part
grep -oP '\d{3}-\d{4}' file.txt

# Invert match (lines NOT matching)
grep -vP 'DEBUG|TRACE' app.log

# sed replacement
sed 's/oldPattern/newText/g' file.txt         # Basic
sed -E 's/foo_([a-z]+)/bar_\1/g' file.txt     # Extended with capture group

# Perl one-liner (most powerful)
perl -pe 's/(?<=price:\s)\d+/0/g' file.txt    # Lookbehind works in Perl
```

## 查找和替换操作

### 代码重构

```bash
# Rename a variable across files
grep -rlP '\boldName\b' src/ | xargs sed -i 's/\boldName\b/newName/g'

# Convert var to const (JavaScript)
sed -i -E 's/\bvar\b/const/g' src/*.js

# Convert single quotes to double quotes
sed -i "s/'/\"/g" src/*.ts

# Add trailing commas to object properties
sed -i -E 's/^(\s+\w+:.+[^,])$/\1,/' config.json

# Update import paths
sed -i 's|from '\''../old-path/|from '\''../new-path/|g' src/*.ts

# Convert snake_case to camelCase (Python → JavaScript naming)
perl -pe 's/_([a-z])/uc($1)/ge' file.txt
```

### 文本清理

```bash
# Remove trailing whitespace
sed -i 's/[[:space:]]*$//' file.txt

# Remove blank lines
sed -i '/^$/d' file.txt

# Remove duplicate blank lines (keep at most one)
sed -i '/^$/N;/^\n$/d' file.txt

# Trim leading and trailing whitespace from each line
sed -i 's/^[[:space:]]*//;s/[[:space:]]*$//' file.txt

# Remove HTML tags
sed 's/<[^>]*>//g' file.html

# Remove ANSI color codes
sed 's/\x1b\[[0-9;]*m//g' output.txt
```

## 常见问题

### 贪婪匹配与非贪婪匹配

```
Pattern: <.*>     Input: <b>bold</b>
Greedy  matches: <b>bold</b>     (entire string between first < and last >)
Lazy    matches: <b>              (stops at first >)
Pattern: <.*?>    (lazy version)
```

### 转义特殊字符

```
Characters that need escaping in regex: . * + ? ^ $ { } [ ] ( ) | \
In character classes []: only ] - ^ \ need escaping

# To match a literal dot:  \.
# To match a literal *:    \*
# To match a literal \:    \\
# To match [ or ]:         \[ or \]
```

### 换行符和多行文本

```
By default . does NOT match newline.
By default ^ and $ match start/end of STRING.

# To make . match newlines:
JavaScript: /pattern/s (dotAll flag)
Python: re.DOTALL or re.S
Go: (?s) inline flag

# To make ^ $ match line boundaries:
JavaScript: /pattern/m (multiline flag)
Python: re.MULTILINE or re.M
Go: (?m) inline flag
```

### 回溯和性能优化

```
# Catastrophic backtracking (avoid these patterns on untrusted input):
(a+)+        # Nested quantifiers
(a|a)+       # Overlapping alternation
(.*a){10}    # Ambiguous .* with repetition

# Safe alternatives:
[a]+         # Instead of (a+)+
a+           # Instead of (a|a)+
[^a]*a       # Possessive/atomic instead of .*a
```

## 提示

- 从简单模式开始，逐步增加复杂性。通常 `\\d+` 就足够了，很少需要使用 `[0-9]+`。
- 在实际数据上测试正则表达式，而不仅仅是理想情况下的测试。边缘情况（空字符串、特殊字符、Unicode）会破坏简单的模式。
- 当不需要捕获匹配结果时，使用非捕获组 `(?:...)`。这样会更快且更简洁。
- 在 JavaScript 中，使用 `g` 标志进行全局匹配和替换。如果不使用 `g`，只会匹配并替换第一个匹配项。
- Go 的 `regexp` 包使用 RE2 规则库（不支持前瞻/后瞻功能）。如果需要这些功能，请使用其他库或 `regexp2` 包。
- `grep -P`（PCRE）是功能最强大的命令行正则表达式工具。当需要前瞻、`\d` 或 `\b` 时，使用它。
- 对于复杂的正则表达式，使用详细模式（Python 中的 `re.VERBOSE`，Perl 中的 `/x`），并为每个部分添加注释。
- 正则表达式不适合用于解析 HTML、XML 或 JSON。这些格式应该使用专门的解析器。正则表达式适用于从这些格式中提取简单的数据，但不适合结构化解析。
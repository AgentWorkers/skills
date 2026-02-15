---
name: security-patterns
description: 基于 Anthropic 官方安全指导插件的实时安全模式检测器。在编写代码时主动使用该工具，以检测命令注入、XSS（跨站脚本攻击）、不安全的反序列化操作以及动态代码执行风险。能够在这些危险行为被实际执行之前就识别出它们。
allowed-tools: Read, Grep, Glob
---

# 安全模式检测器技能

## 概述

该技能基于Anthropic官方的安全指导插件，提供实时的安全模式检测功能。它能够在潜在危险的编码模式被提交之前就识别出来。

## 检测类别

### 1. 命令注入风险

**GitHub Actions工作流注入**
```yaml
# DANGEROUS - User input directly in run command
run: echo "${{ github.event.issue.title }}"

# SAFE - Use environment variable
env:
  TITLE: ${{ github.event.issue.title }}
run: echo "$TITLE"
```

**Node.js子进程执行**
```typescript
// DANGEROUS - Shell command with user input
exec(`ls ${userInput}`);
spawn('sh', ['-c', userInput]);

// SAFE - Array arguments, no shell
execFile('ls', [sanitizedPath]);
spawn('ls', [sanitizedPath], { shell: false });
```

**Python操作系统命令**
```python
# DANGEROUS
os.system(f"grep {user_input} file.txt")
subprocess.call(user_input, shell=True)

# SAFE
subprocess.run(['grep', sanitized_input, 'file.txt'], shell=False)
```

### 2. 动态代码执行

**类似JavaScript `eval`的代码模式**
```typescript
// DANGEROUS - All of these execute arbitrary code
eval(userInput);
new Function(userInput)();
setTimeout(userInput, 1000);  // When string passed
setInterval(userInput, 1000); // When string passed

// SAFE - Use parsed data, not code
const config = JSON.parse(configString);
```

### 3. 基于DOM的XSS风险

**React的`dangerouslySetInnerHTML`方法**
```tsx
// DANGEROUS - Renders arbitrary HTML
<div dangerouslySetInnerHTML={{ __html: userContent }} />

// SAFE - Use proper sanitization
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userContent) }} />
```

**直接DOM操作**
```typescript
// DANGEROUS
element.innerHTML = userInput;
document.write(userInput);

// SAFE
element.textContent = userInput;
element.innerText = userInput;
```

### 4. 不安全的反序列化

**Python的`pickle`模块**
```python
# DANGEROUS - Pickle can execute arbitrary code
import pickle
data = pickle.loads(user_provided_bytes)

# SAFE - Use JSON for untrusted data
import json
data = json.loads(user_provided_string)
```

**JavaScript的不安全反序列化**
```typescript
// DANGEROUS with untrusted input
const obj = eval('(' + jsonString + ')');

// SAFE
const obj = JSON.parse(jsonString);
```

### 5. SQL注入

**查询中的字符串插值**
```typescript
// DANGEROUS
const query = `SELECT * FROM users WHERE id = ${userId}`;
db.query(`SELECT * FROM users WHERE name = '${userName}'`);

// SAFE - Parameterized queries
const query = 'SELECT * FROM users WHERE id = $1';
db.query(query, [userId]);
```

### 6. 路径遍历

**未清理的文件路径**
```typescript
// DANGEROUS
const filePath = `./uploads/${userFilename}`;
fs.readFile(filePath); // User could pass "../../../etc/passwd"

// SAFE
const safePath = path.join('./uploads', path.basename(userFilename));
if (!safePath.startsWith('./uploads/')) throw new Error('Invalid path');
```

## 模式检测规则

| 模式 | 类别 | 严重程度 | 处理方式 |
|---------|----------|----------|--------|
| `eval()` | 动态代码执行 | 严重（CRITICAL） | 阻止执行 |
| `new Function()` | 动态代码执行 | 严重（CRITICAL） | 阻止执行 |
| `dangerouslySetInnerHTML` | XSS攻击 | 高风险（HIGH） | 发出警告 |
| `innerHTML =` | XSS攻击 | 高风险（HIGH） | 发出警告 |
| `document.write()` | XSS攻击 | 高风险（HIGH） | 发出警告 |
| `exec()` + 字符串拼接 | 命令注入 | 严重（CRITICAL） | 阻止执行 |
| `spawn()` + `shell`: true` | 命令注入 | 高风险（HIGH） | 发出警告 |
| `pickle.loads()` | 反序列化 | 严重（CRITICAL） | 发出警告 |
| `${{ github.event }` | GitHub Actions注入 | 严重（CRITICAL） | 发出警告 |
| SQL中的模板字面量 | SQL注入 | 严重（CRITICAL） | 阻止执行 |

## 响应格式

当检测到某种安全模式时，系统会给出如下提示：
```markdown
⚠️ **Security Warning**: [Pattern Category]

**File**: `path/to/file.ts:123`
**Pattern Detected**: `eval(userInput)`
**Risk**: Remote Code Execution - Attacker-controlled input can execute arbitrary JavaScript

**Recommendation**:
1. Never use eval() with user input
2. Use JSON.parse() for data parsing
3. Use safe alternatives for dynamic behavior

**Safe Alternative**:
```typescript
// 不要使用 `eval(userInput)`，而应使用：
const data = JSON.parse(userInput);
```
```

## 与代码审查的集成

该技能应在以下情况下被触发：
1. 在编写新代码时进行代码审查
2. 作为安全审计的一部分
3. 当代码审查工具检测到问题时

## 错误阳性处理

某些情况可能属于误报：
- 使用`DOMPurify`处理`dangerouslySetInnerHTML`方法是安全的
- 在构建工具中使用的`eval`（非用户输入）可能是可接受的
- 使用硬编码命令的`exec`方法风险较低

在采取阻止执行措施之前，请务必检查具体上下文。
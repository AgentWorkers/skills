---
name: security-checker
description: 在将Python技能发布到ClawHub之前，需要使用这款安全扫描工具进行检测。在发布任何技能之前，务必使用该工具检查是否存在危险的导入语句、硬编码的秘密信息、不安全的文件操作，以及eval、exec、subprocess等危险函数。这一步骤对于维护用户信任至关重要，确保发布的技能能够安全地被其他人安装和运行。
---

# 安全检查器

在发布技能之前，使用该工具进行Python代码的安全扫描，以确保代码的安全性。

## 快速入门

```bash
security_scan.py <file_or_directory>
```

**示例：**
```bash
# Scan a single Python file
security_scan.py scripts/my_script.py

# Scan an entire skill directory
security_scan.py /path/to/skill-folder

# Scan multiple skills
security_scan.py skills/
```

## 检查内容

### 危险的导入语句
检测可能被恶意利用的导入语句：
- `os` - 系统级操作
- `subprocess` - 命令执行
- `shutil` - 文件操作
- `socket` - 网络操作
- `urllib` / `requests` - HTTP请求

**为什么危险？** 这些导入语句允许执行系统命令、操作文件以及进行网络访问，这些都可能被恶意利用。

### 危险的函数调用
检测可能存在安全隐患的函数调用：
- `os.system()` - 执行shell命令
- `subprocess.call()`, `subprocess.run()`, `subprocess.Popen()` - 命令执行
- `eval()` - 执行任意代码
- `exec()` - 执行任意代码

**为什么危险？** 这些函数可能导致任意代码的执行，从而引发远程代码执行漏洞。

### 硬编码的秘密信息
检测代码中硬编码的敏感信息：
- API密钥
- 认证令牌（包括ClawHub令牌）
- 密码
- 私钥
- 类似JWT的令牌

**为什么危险？** 如果这些秘密信息在代码中被泄露，可能会被窃取并遭到滥用。

### 不安全的文件操作
检测不安全的文件访问模式：
- 在预期目录之外的绝对文件路径
- 遍历上级目录（`..`）
- 向系统目录写入数据

**为什么危险？** 这可能导致意外的文件访问、数据丢失或系统被修改。

## 使用方式：发布前的检查流程

在发布任何技能之前，请执行以下检查：

```bash
# 1. Run security scan
security_scan.py /path/to/skill

# 2. Review any warnings
# If warnings appear, fix the code or document why it's safe

# 3. Re-scan after fixes
security_scan.py /path/to/skill

# 4. Only publish if scan passes
clawhub publish /path/to/skill --slug my-skill ...
```

## 结果解读

### ✅ “未发现安全问题”
代码看起来是安全的，可以继续发布。

### ⚠️ “警告”（黄色）
检测到潜在的风险模式。请查看具体代码行，并做出以下决定：
- **该操作是否合法？** 在代码注释或SKILL.md文件中说明原因。
- **是否可以避免？** 请重构为更安全的替代方案。
- **是否必要？** 清晰地记录该操作的风险和用途。

### 🔴 “可能存在硬编码的秘密信息”
检测到硬编码的秘密信息。在发布之前，请：
- 移除这些秘密信息。
- 使用环境变量代替：`os.getenv('API_KEY')`
- 在SKILL.md文件中记录所需的环境变量。
- 绝不要提交真实的秘密信息。

## 示例

### 合法的os模块使用（已记录）
```python
import os  # Used only for path.join() - safe file path construction
workspace = os.path.join(os.path.expanduser("~"), ".openclaw", "workspace")
```

**扫描结果：** ⚠️ 关于os导入的警告
**操作：** 在代码注释中记录安全的用法。

### 硬编码的秘密信息（必须修复）
```python
API_KEY = "sk-1234567890abcdef"  # DON'T DO THIS
```

**扫描结果：** 🔴 可能存在硬编码的秘密信息
**操作：** 移除硬编码的秘密信息，并使用环境变量：
```python
API_KEY = os.getenv("MY_SKILL_API_KEY")
# Document in SKILL.md: Requires MY_SKILL_API_KEY environment variable
```

### 安全的代码示例（无问题）
```python
# JSON storage for local data only
data = {"notes": [], "metadata": {}}
with open("data.json", "w") as f:
    json.dump(data, f)
```

**扫描结果：** ✅ 无问题

## 最佳实践

1. **发布前务必进行扫描** - 将此步骤纳入你的工作流程。
2. **手动审核警告** - 扫描工具无法理解代码的具体上下文。
3. **使用环境变量存储敏感信息** - 绝不要硬编码。
4. **优先使用json格式进行数据解析** - 比使用`eval()`更安全。
5. **记录必要的风险** - 如果必须使用危险代码，请解释其原因。
6. **尽量减少危险导入** - 只使用真正必要的功能。
7. **保持代码简洁** - 复杂的代码更难以审计。

## 与开发工作流程的集成

### 在提交代码到仓库之前
```bash
# Pre-commit hook concept
python3 /path/to/security_scan.py scripts/
if [ $? -ne 0 ]; then
    echo "❌ Security scan failed. Fix issues before committing."
    exit 1
fi
```

### 自动化的发布前检查
```bash
#!/bin/bash
# publish-safe.sh

SKILL_PATH=$1

echo "🔒 Running security scan..."
python3 /path/to/security_scan.py "$SKILL_PATH"

if [ $? -ne 0 ]; then
    echo "❌ Cannot publish: Security scan failed"
    exit 1
fi

echo "✅ Security scan passed"
clawhub publish "$SKILL_PATH"
```

## 限制

该安全检查工具：
- **无法理解代码的具体上下文** - 一些看似危险的代码实际上可能是合法的。
- **仅进行静态分析** - 不会实际执行代码。
- **仅针对Python语言** - 其他语言需要使用不同的工具。
- **只能检测基本的安全问题** - 复杂的代码混淆技术可能逃避检测。

**建议结合使用以下方法：**
- 手动代码审查
- 在隔离环境中进行测试
- 在发布前仔细阅读所有代码
- 使用额外的安全检查工具：`bandit`, `safety`。

## 建立信任

发布通过安全扫描的技能有助于建立社区对你的信任：
- 用户会知道你重视代码安全。
- 你的声誉会得到提升。
- 你的技能会更容易被采纳。
- ClawHub可能会优先推荐安全的技能。

## 已发布的技能示例（均通过安全扫描）

```bash
# research-assistant
security_scan.py /home/ubuntu/.openclaw/workspace/skills/research-assistant
# ✅ All clear

# task-runner  
security_scan.py /home/ubuntu/.openclaw/workspace/skills/task-runner
# ✅ All clear

# security-checker
security_scan.py /home/ubuntu/.openclaw/workspace/skills/security-checker
# ✅ All clear
```

这三个技能在发布到ClawHub之前都通过了安全扫描。
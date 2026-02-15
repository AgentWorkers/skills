---
name: skill-publisher-claw-skill
description: **准备技能以供公开发布**  
此步骤适用于将技能发布到 GitHub 或 ClawdHub 的过程，涵盖安全审计、可移植性、文档编写以及代码管理（如 Git 代码规范）等方面。  
**触发条件**：发布技能、审核技能、检查技能发布前的准备工作、以及完成技能发布的所有相关流程。
---

# 技能发布流程

在发布任何技能之前，请先完成以下检查清单，以确保该技能可重用、代码整洁、安全且文档齐全。

## 使用场景

- 在将技能推送到公共仓库之前  
- 在提交到ClawdHub之前  
- 在审核他人的技能时  
- 定期对已发布的技能进行审计  

## 快速检查清单

请按顺序执行以下步骤。每个部分都配有详细的指导说明。  

```
[ ] 1. STRUCTURE    - Required files present, logical organization
[ ] 2. SECURITY     - No secrets, keys, PII, or sensitive data  
[ ] 3. PORTABILITY  - No hardcoded paths, works on any machine
[ ] 4. QUALITY      - Clean code, no debug artifacts
[ ] 5. DOCS         - README, SKILL.md, examples complete
[ ] 6. TESTING      - Verified it actually works
[ ] 7. GIT          - Clean history, proper .gitignore, good commits
[ ] 8. METADATA     - License, description, keywords
```  

---

## 1. 结构验证  

### 必需文件  
```
skill-name/
├── SKILL.md          # REQUIRED - Entry point, when to use, quick reference
├── README.md         # REQUIRED - For GitHub/humans
└── [content files]   # The actual skill content
```  

### SKILL.md 格式  
必须包含：  
- **标题**：技能的名称和简短描述  
- **使用场景**：明确说明何时应加载该技能  
- **快速参考**：最重要的信息一目了然  
- **详细内容**：根据需要添加  

```markdown
# Skill Name

One-line description of what this skill does.

## When to Use
- Trigger condition 1
- Trigger condition 2

## Quick Reference
[Most important info here]

## [Additional Sections]
[Detailed content]
```  

### 文件组织  
- 将相关内容逻辑地分组  
- 使用清晰、描述性强的文件名  
- 保持文件内容的专注性（每个文件只负责一个功能）  
- 考虑文件的加载顺序（哪些内容应该首先被读取）  

### 避免的错误做法  
❌ 将所有内容放在一个巨大的文件中  
❌ 使用难以理解的文件名（如 `data1.md`、`stuff.md`）  
❌ 文件之间存在循环依赖  
❌ 缺少 SKILL.md 的入口文件  

---

## 2. 安全审计  

### 保密信息扫描  
查找并删除所有保密信息：  
```bash
# Run in skill directory
grep -rniE "(api[_-]?key|secret|password|token|bearer|auth)" . --include="*.md"
grep -rniE "([a-zA-Z0-9]{32,})" . --include="*.md"  # Long strings that might be keys
grep -rniE "(sk-|pk-|xai-|ghp_|gho_)" . --include="*.md"  # Common key prefixes
```  

### 个人信息扫描  
查找并删除所有个人信息：  
```bash
grep -rniE "(@gmail|@yahoo|@hotmail|@proton)" . --include="*.md"
grep -rniE "\+?[0-9]{10,}" . --include="*.md"  # Phone numbers
grep -rniE "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" . --include="*.md"  # IPs
```  

### 敏感内容检查  
- [ ] 不包含任何公司内部信息  
- [ ] 不包含任何私人URL或端点  
- [ ] 不包含员工姓名（除非是公众人物）  
- [ ] 不包含任何财务数据  
- [ ] 不包含任何形式的凭证  
- [ ] 不包含会话令牌或cookie  

### 示例数据  
如果示例需要使用真实数据，请使用：  
- 电子邮件：`user@example.com`  
- IP地址：`192.0.2.x`（符合RFC 5737规范）  
- 域名：`example.com`  
- 名字：使用虚构的名称（如“Alice”、“Bob”、“Acme Corp”）  

---

## 3. 可移植性检查  

### 路径硬编码  
查找并修复所有硬编码的路径：  
```bash
grep -rniE "(\/home\/|\/Users\/|C:\\\\|~\/)" . --include="*.md"
grep -rniE "\/[a-z]+\/[a-z]+\/" . --include="*.md"  # Absolute paths
```  
替换为：  
- 相对路径（如 `./config.yaml`）  
- 环境变量（如 `$HOME`、`$XDG_CONFIG_HOME`）  
- 与平台无关的描述  

### 环境假设  
- [ ] 不包含硬编码的用户名  
- [ ] 不包含特定于机器的路径  
- [ ] 不假设已安装了某些软件（或对其有依赖）  
- [ ] 不假设存在某些环境变量（如有需要，请在文档中说明）  
- [ ] 不使用特定于操作系统的命令（并提供替代方案）  

### 依赖项文档  
如果技能依赖于外部工具，请确保提供相应的文档：  
```markdown
## Requirements
- `tool-name` - [installation link]
- Environment variable `API_KEY` must be set
```  

---

## 4. 代码质量  

### 调试信息  
删除所有不必要的调试信息：  
```bash
grep -rniE "(TODO|FIXME|XXX|HACK|DEBUG)" . --include="*.md"
grep -rniE "(console\.log|print\(|debugger)" . --include="*.md"
```  

### 格式规范  
- [ ] 使用一致的markdown格式  
- 代码块需添加语言标签（如 ````python`、````bash`）  
- 表格显示正确  
- 链接有效（无失效的引用）  
- 无多余的空白字符  
- 标题层次结构一致  

### 内容质量  
- [ ] 不包含填充文本（如Lorem-ipsum）  
- [ ] 无注释掉的代码部分  
- [ ] 无重复内容  
- [ ] 信息不陈旧  
- [ ] 示例完整且可运行  

---

## 5. 文档编写  

### README.md 检查清单  
```markdown
# Skill Name

Brief description (1-2 sentences).

## What's Inside
[File listing with descriptions]

## Quick Summary  
[The core value proposition]

## Usage
[How to use this skill]

## Requirements (if any)
[Dependencies, API keys, etc.]

## Links (if relevant)
[Official docs, repos, etc.]

## License
[MIT recommended for skills]
```  

### SKILL.md 检查清单  
- [ ] “使用场景”部分明确具体使用条件  
- [ ] 提供常见需求的快速参考  
- [ ] 详细内容逻辑清晰  
- 如果文件较多，需提供交叉引用  

### 示例  
- [ ] 至少提供一个完整、可运行的示例  
- [ ] 示例使用的是安全或虚构的数据  
- [ ] 示例经过测试并验证  

---

## 6. 测试  

### 功能测试  
1. **新会话加载测试**：在新会话中加载技能，验证其功能是否正常  
2. **触发条件测试**：验证“使用场景”中的条件是否与实际使用情况匹配  
3. **示例测试**：手动运行所有示例  
4. **边缘情况测试**：检查在异常输入下的行为  

### 集成测试  
如果技能涉及外部工具或命令，请进行相应的集成测试：  
```bash
# Test each command mentioned actually works
# Verify outputs match documentation
```  

### 交叉引用测试  
- [ ] 所有内部链接均能正常访问  
- [ ] 所有外部链接有效  
- [ ] 文件引用正确  

### 验证脚本（可选但推荐）  
创建 `test.sh` 脚本或记录手动测试步骤：  
```bash
#!/bin/bash
# Verify skill integrity
echo "Checking for secrets..."
grep -rniE "(api[_-]?key|secret|password)" . --include="*.md" && exit 1
echo "Checking for hardcoded paths..."
grep -rniE "\/home\/" . --include="*.md" && exit 1
echo "✓ All checks passed"
```  

---

## 7. Git 代码管理  

### 提交前的准备  
创建 `.gitignore` 文件：  
```gitignore
# OS files
.DS_Store
Thumbs.db

# Editor files
*.swp
*.swo
*~
.idea/
.vscode/

# Temporary files
*.tmp
*.bak

# Test artifacts
test-output/
```  

### 提交历史  
- [ ] 绝不提交任何保密信息（请检查整个提交历史）  
- 提交操作要简洁、原子化（即一次只修改一个文件）  
- 提交信息要清晰明了  

```bash
# Check for secrets in history
git log -p | grep -iE "(api[_-]?key|secret|password|token)" 
```  

如果曾经提交过保密信息：  
```bash
# Nuclear option - rewrite history (coordinate with collaborators!)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/sensitive/file' HEAD
```  

### 提交信息格式  
```
type: short description

- Detail 1
- Detail 2

Types: feat, fix, docs, refactor, test, chore
```  

### 提交前的最后检查  
```bash
# Final verification
git status                    # Nothing unexpected staged
git log --oneline -5          # Commits look right
git diff origin/main          # Changes are what you expect
```  

---

## 8. 元数据  

### 仓库设置  
- [ ] 填写仓库描述  
- [ ] 添加相关标签（如 `claw`、`skill`、`ai-assistant`）  
- [ ] 提供许可证文件  

### 推荐的许可证  
对于开源技能，MIT许可证简单且使用灵活：  
```
MIT License

Copyright (c) [year] [name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```  

### 如果在ClawdHub上发布  
在 SKILL.md 的开头部分添加相应的元数据：  
```yaml
---
name: skill-name
description: One-line description
version: 1.0.0
author: username
tags: [tag1, tag2]
---
```  

---

## 自动化审计脚本  
在每次发布前运行以下自动化审计脚本：  
```bash
#!/bin/bash
set -e

SKILL_DIR="${1:-.}"
cd "$SKILL_DIR"

echo "🔍 Auditing skill in: $SKILL_DIR"
echo ""

# 1. Structure
echo "=== STRUCTURE ==="
[ -f "SKILL.md" ] && echo "✓ SKILL.md exists" || echo "✗ SKILL.md MISSING"
[ -f "README.md" ] && echo "✓ README.md exists" || echo "✗ README.md MISSING"
echo ""

# 2. Security
echo "=== SECURITY ==="
if grep -rniE "(api[_-]?key|secret|password|token|bearer)=['\"]?[a-zA-Z0-9]" . --include="*.md" 2>/dev/null; then
    echo "✗ POTENTIAL SECRETS FOUND"
else
    echo "✓ No obvious secrets"
fi

if grep -rniE "(sk-|pk-|xai-|ghp_|gho_)[a-zA-Z0-9]" . --include="*.md" 2>/dev/null; then
    echo "✗ API KEY PATTERNS FOUND"
else
    echo "✓ No API key patterns"
fi
echo ""

# 3. Portability
echo "=== PORTABILITY ==="
if grep -rniE "\/home\/[a-z]+" . --include="*.md" 2>/dev/null; then
    echo "✗ HARDCODED HOME PATHS"
else
    echo "✓ No hardcoded home paths"
fi
echo ""

# 4. Quality
echo "=== QUALITY ==="
if grep -rniE "(TODO|FIXME|XXX)" . --include="*.md" 2>/dev/null; then
    echo "⚠ TODOs found (review these)"
else
    echo "✓ No TODOs"
fi
echo ""

# 5. Git
echo "=== GIT ==="
[ -f ".gitignore" ] && echo "✓ .gitignore exists" || echo "⚠ No .gitignore"
[ -d ".git" ] && echo "✓ Git initialized" || echo "✗ Not a git repo"
echo ""

echo "🏁 Audit complete"
```  

---

## 发布流程  
```
1. Run automated audit script
2. Fix any issues found
3. Manual review of checklist above
4. Final commit with clean message
5. Push to GitHub
6. (Optional) Submit to ClawdHub
```  

## README 文件的质量  
一个优秀的 README 文件应该易于被发现且便于阅读。详细指南请参阅 `docs/readme-quality.md`。  

### 快速检查  
- 第一行应清晰说明技能的功能（而非“欢迎使用...”）  
- 避免使用过于专业的术语（如“AI”、“全面”、“无缝”、“前沿技术”等）  
- 描述具体使用场景，而非模糊的声明  
- 语言应自然，类似人类撰写的文字，而非新闻稿风格  
- 标题中不要使用过多的表情符号  

### SEO 编排建议  
- 使用用户实际会搜索的关键词  
- 将最重要的信息放在第一段  
- 明确说明技能的功能（例如“检查API密钥的有效性”而非“强大的验证功能”）  

## 发布后的操作  
- [ ] 确保GitHub页面显示正确  
- 测试新克隆后的功能是否正常  
- 如果在本地使用该技能，请将其添加到 `AGENTS.md` 列表中  
- 如有必要，可通过Discord等渠道进行公告  

---
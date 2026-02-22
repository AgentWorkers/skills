---
name: clawhub-skill-creator
description: Create effective skills for clawhub registry. Use when: (1) Creating new skill for publication, (2) Updating existing skill metadata, (3) Optimizing skill structure for AI agents, (4) Validating skill before publish, (5) Understanding clawhub-specific requirements.
---

# Clawhub 技能创建指南

本指南详细介绍了如何创建与 Clawhub 注册表兼容的技能，并优化这些技能以适应 AI 代理的使用。

## 语言规则

**技能描述必须使用英语**，除非上下文另有要求（例如示例或注释可以使用其他语言）。

- 前言中的 `description` 部分：仅使用英语
- SKILL.md 正文：优先使用英语
- 示例和代码注释：根据需要使用任何语言
- 参考资料：根据领域选择合适的语言

## 快速入门

### 创建新技能

```bash
# Run initializer
./scripts/init-skill.sh my-skill

# Or manually create structure
mkdir -p my-skill/{references,scripts,assets}
touch my-skill/SKILL.md my-skill/_meta.json my-skill/LICENSE.txt
```

## 技能创建流程

### 第 1 阶段：明确需求

**在编写任何代码之前，请先澄清以下内容：**

1. **该技能解决什么问题？**
   - 具体的使用场景（2-3 个示例）
   - 应该触发该技能的目标查询

2. **谁会使用这个技能？**
   - AI 代理（Clawhub 的主要用户群体）
   - 预期的使用环境（可用的工具、环境）

3. **需要哪些资源？**
   - 详细文档的参考资料？
   - 模板的资产？
   - 自动化的脚本？

**输出：** 对技能范围和触发条件的清晰理解。

### 第 2 阶段：规划结构

**根据复杂度选择合适的结构：**

| 复杂度 | 结构 | 使用时机 |
|------------|-----------|-------------|
| 简单 | 仅使用 SKILL.md | 小于 100 行，单一用途 |
| 中等 | 加入参考资料/ | 100-300 行，包含一些细节 |
| 复杂 | 加入参考资料/资产/ | 超过 300 行，涉及多个领域 |

**确定所需资源：**
- 需要哪些参考资料？（文档、示例、模板）
- 需要哪些资产？（模板、配置文件）
- 需要哪些脚本？（验证、打包脚本）

**输出：** 目录结构和资源列表。

### 第 3 阶段：初始化结构

```bash
# Create directory
mkdir -p my-skill/{references,scripts,assets}

# Create required files
touch my-skill/SKILL.md
touch my-skill/_meta.json
touch my-skill/LICENSE.txt
```

**Clawhub 所需的文件：**
```
my-skill/
├── SKILL.md              # Instructions and metadata (required)
├── _meta.json            # Registry metadata (required)
├── LICENSE.txt           # License file (required)
├── references/           # Optional: detailed documentation
├── scripts/              # Optional: automation scripts
└── assets/               # Optional: templates, resources
```

### 第 4 阶段：编写 SKILL.md

#### 前言（YAML）

```yaml
---
name: skill-name
description: What it does. Use when: (1) trigger-1, (2) trigger-2, (3) trigger-3.
---
```

**重要规则：**
- `name` 必须与目录名称一致
- `description` 仅用于指定技能的触发条件——请在此处包含所有使用说明
- `description` 必须使用 **英语**
- 前言中只需包含 `name` 和 `description`

#### 正文结构

```markdown
# Skill Title

Brief purpose (1-2 sentences).

## Quick Start

**Linux/Mac:**
```bash
command --option
```

**Windows CMD:**
```cmd
command --option
```

**PowerShell:**
```powershell
command --option
```

## When to Use

- Situation 1: What to do
- Situation 2: What to do
- Situation 3: What to do

## Workflow

1. **Step one**: Description
2. **Step two**: Description
3. **Step three**: Description

## Resources

- `references/advanced.md` - For complex cases
- `references/examples.md` - Usage examples
- `assets/template.txt` - Starting template
```

**编写指南：**
- 使用祈使句式（例如“打开文件”，而不是“你应该打开文件”）
- 提供具体的示例，而非抽象的解释
- 命令应与平台兼容
- 提供指向参考资料的链接
- 正文内容优先使用英语

### 第 5 阶段：创建 _meta.json 文件

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "Short description for registry listing",
  "requires": {
    "env": ["ENV_VAR_1", "ENV_VAR_2"],
    "credentials": ["credential_name"]
  },
  "tags": ["tag1", "tag2", "latest"]
}
```

**字段说明：**
- `name`：必须与目录名称和 SKILL.md 前言中的名称一致
- `version`：遵循 Semver 格式（X.Y.Z），在设置之前请先检查注册表
- `description`：用于注册表列表，必须使用 **英语**
- `requires.env`：所需的环境变量
- `requires.credentials`：所需的凭据
- `tags`：添加 “latest” 标签以提高可发现性

### 第 6 阶段：添加 LICENSE.txt 文件

选择合适的许可证（推荐使用 MIT 许可证）：

```
MIT License

Copyright (c) 2025 [Author]

Permission is hereby granted...
```

### 第 7 阶段：编写参考资料（如需要）

在 `references/` 目录下创建相关文件：

```markdown
# Reference Title

Detailed documentation here.

## Section

Content...
```

**编写指南：**
- 每个文件专注一个主题
- 每个文件不超过 5000 字
- 从 SKILL.md 文件中提供清晰的引用链接
- 避免深度嵌套的引用
- 正文内容优先使用英语，允许使用领域特定的语言

### 第 8 阶段：本地验证

```bash
# Check structure
./scripts/validate.sh my-skill

# Or manual checks:
# - SKILL.md exists and has frontmatter
# - _meta.json is valid JSON
# - LICENSE.txt exists
# - No README.md, CHANGELOG.md
# - Line count < 300
# - References linked correctly
```

**验证检查清单：**
- 目录名称是否与前言和 _meta.json 文件中的 `name` 一致
- `description` 是否使用英语，并包含使用说明
- SKILL.md 文件是否少于 300 行
- _meta.json 文件是否为有效的 JSON 格式
- 是否没有多余的文件（如 README、CHANGELOG）
- 参考资料是否存在且链接正确
- 文件的大小是否小于 10K 字节

### 第 9 阶段：用代理进行测试

**触发测试：**
- 该技能是否能正确响应预期的查询？
- 描述是否能够准确触发技能？

**工作流程测试：**
- 代理能否在没有额外提示的情况下完成操作？
- 命令是否清晰且可执行？

**资源测试：**
- 参考资料是否能在适当的时候加载？
- 导航是否清晰？

**边缘情况测试：**
- 技能如何处理错误？
- 是否能够处理不同平台的差异？

### 第 10 阶段：迭代（如有必要）

如果测试中发现问题：

1. **识别问题**
   - 触发条件是否无效？→ 修改描述
   - 工作流程是否不清楚？→ 重新编写步骤
   - 信息是否缺失？→ 添加参考资料

2. **更新文件**
   - SKILL.md、_meta.json 或参考资料

3. **重新验证并重新测试**
   - 回到第 8 阶段

4. **重复上述步骤，直到满意**

**迭代循环：** 第 8 阶段 → 第 9 阶段 → 第 10 阶段 → 第 11 阶段

### 第 11 阶段：检查版本

**在发布之前，请验证当前的注册表版本：**

```bash
# Check current registry version
clawhub inspect skill-name --json | grep version

# Ensure new version follows semver:
# 1.0.0 → 1.0.1 (patch: bug fixes)
# 1.0.0 → 1.1.0 (minor: new features)
# 1.0.0 → 2.0.0 (major: breaking changes)

# Never downgrade! (1.1.0 → 1.0.2 is wrong)
```

**使用正确的版本号更新 _meta.json 文件：**

```json
{
  "version": "1.0.1"
}
```

### 第 12 阶段：打包

**打包内容：**
- 所有技能文件
- 经过验证的结构
- 准备好进行分发

### 第 13 阶段：发布

```bash
cd my-skill

# Publish to clawhub
clawhub publish . --version 1.0.1 --changelog "Description of changes"

# Verify publication
clawhub inspect skill-name
```

**发布后：**
- 技能将出现在注册表中
- 其他用户可以通过 `clawhub install skill-name` 命令安装该技能

## Clawhub 所需的文件

### SKILL.md

- 说明和元数据：
  - YAML 格式的前言（包含名称和英文描述）
  - Markdown 格式的正文（包含工作流程和示例）
  - 提供指向参考资料的链接

### _meta.json

- 注册表元数据：

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "Registry listing description in English",
  "requires": {
    "env": [],
    "credentials": []
  },
  "tags": ["latest"]
}
```

### LICENSE.txt

- 许可证文件（推荐使用 MIT 或 Apache-2.0 等许可证）

## 参考资料

- `references/skill-structure.md` – 目录结构模板
- `references/agent-first-design.md` – 为 AI 设计而非人类设计的技能
- `references/token-optimization.md` – 最小化上下文的使用量
- `references/cross-platform.md` – 与平台兼容的脚本
- `references/validation-checklist.md` – 发布前的检查清单
- `references/versioning.md` – Semver 版本控制最佳实践

## 关键原则

### 1. 以代理为中心的设计

技能是为 AI 代理设计的，而非人类用户：
- ❌ 不提供交互式提示
- ❌ 不使用特定于平台的脚本（使用通用知识）
- ✅ 为所有平台提供命令模板
- ✅ 提供清晰的参考资料链接

### 2. 逐步披露信息

```
Level 1: Metadata (name + description)     → Always loaded
Level 2: SKILL.md body                      → On trigger
Level 3: Resources (references/, assets/)   → On demand
```

### 3. 令牌使用限制

| 组件 | 目标 | 最大字数限制 |
|-----------|--------|-----|
| 元数据 | 50 个单词 | 100 个单词 |
| SKILL.md | 200 行 | 300 行 |
| 参考资料 | 3000 个单词 | 5000 个单词 |
| 总字数 | 5000 个字符 | 10000 个字符 |

### 4. 平台兼容性

**代理会根据检测到的平台选择合适的执行方式：**

```markdown
## Commands

**Linux/Mac:**
```bash
command --option
```

**Windows CMD:**
```cmd
command --option
```

**PowerShell:**
```powershell
command --option
```
```

### 5. 描述使用英语

**必须使用英语的元素：**
- SKILL.md 前言中的 `description`
- _meta.json 文件中的 `description`
- 主要的工作流程说明

**其他部分可以使用其他语言：**
- 代码示例
- 注释
- 领域特定的参考资料
- 面向用户的示例

## 脚本

- `scripts/init-skill.sh` – 初始化新技能的结构
- `scripts/package-skill.sh` – 将技能打包以供分发
- `scripts/validate.sh` – 验证技能的结构

## 避免的错误做法

❌ **不要：**
- 将使用说明仅放在正文部分（必须放在描述中）
- 在前言中使用非英语的描述
- 在 SKILL.md 和参考资料中重复相同的信息
- 创建不必要的文件（如 README.md、CHANGELOG.md）
- 使用特定于平台的脚本（如 sh/bat 文件）
- 使用被动语态（例如“你应该……”）
- 包含通用的背景理论
- 在发布前不进行验证
- 发布前不进行测试

✅ **应该：**
- 使用英语编写描述
- 从具体的示例开始
- 将详细信息放在参考资料中
- 使用祈使句式
- 对每个句子的功能进行评估
- 使用真实的代理查询进行测试
- 在发布前进行验证
- 严格遵循 Semver 版本控制规范
- 根据测试结果进行迭代

### 结论

遵循上述指南，您可以创建出高效、兼容性强且易于使用的 Clawhub 技能。
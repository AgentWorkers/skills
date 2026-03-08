---
name: clawhub-publish
description: 创建、打包并发布 OpenClaw 技能到 ClawHub。这些操作适用于以下场景：(1) 从零开始构建新的技能；(2) 将技能打包成 `.skill` 文件；(3) 在 clawhub.com 上发布或更新技能；(4) 为技能设置 GitHub 仓库；(5) 在发布前对技能进行审核。本文档涵盖了从创意产生到技能最终发布的整个生命周期，包括前置内容（frontmatter）、脚本、参考资料、验证流程、版本控制以及 ClawHub 命令行界面（CLI）的使用方法。它为技能创建者提供了基于 ClawHub 的具体发布流程和实用开发模式。
metadata:
  {
    "openclaw":
      {
        "requires": { "anyBins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
---
# ClawHub 技能发布

这是一个端到端的工作流程，用于将 OpenClaw 技能创建并发布到 ClawHub。

## 快速参考

```bash
# Create
scripts/init_skill.py my-skill --path . --resources scripts,references

# Validate
python3 scripts/quick_validate.py my-skill/

# Package
python3 scripts/package_skill.py my-skill/

# Publish
clawhub login
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0 --changelog "Initial release"

# Update
clawhub publish ./my-skill --slug my-skill --version 1.1.0 --changelog "Added feature X"

# Sync all local skills
clawhub sync --dry-run
clawhub sync --all --bump patch --changelog "Bug fixes"
```

## 工作流程

### 1. 规划技能

在编写代码之前，明确以下内容：

- **触发条件是什么？**—— 用户需要说什么来激活这个技能？
- **需要哪些脚本？**—— 哪些操作是脆弱的、重复的，或者需要确定性的结果？
- **需要哪些参考资料？**—— 需要哪些 API 文档、数据结构或领域知识？
- **需要哪些依赖项？**—— 需要哪些二进制包或模块？

### 2. 创建技能

使用 `skill-creator` 提供的 `init` 脚本（如果有的话），或者手动创建：

```
my-skill/
├── SKILL.md           # Required: frontmatter + instructions
├── scripts/           # Optional: executable code
├── references/        # Optional: API docs, schemas
└── assets/            # Optional: templates, images
```

### 3. 编写 SKILL.md 文件

#### 前言（对技能的触发机制至关重要）

```yaml
---
name: my-skill
description: >
  One-paragraph description of what the skill does AND when to use it.
  Include specific trigger phrases. This is the ONLY thing the agent sees
  before deciding to load the skill, so be comprehensive.
metadata:
  {
    "openclaw":
      {
        "emoji": "🔧",
        "os": ["linux", "darwin"],
        "requires": { "bins": ["curl", "jq"], "anyBins": ["node", "bun"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "my-tool",
              "bins": ["my-tool"],
              "label": "Install my-tool (brew)",
            },
          ],
      },
  }
---
```

**必填选项：**
- `bins`：所有二进制包都必须存在。
- `anyBins`：至少需要有一个二进制包存在。

**支持的安装类型：** `brew`、`node`、`pip`、`cargo`、`go`

#### 正文编写指南

- 保持代码行数在 500 行以内（因为上下文窗口是共享的）。
- 使用祈使句式（例如：“运行脚本”，而不是“你应该运行脚本”）。
- 提供具体的示例，而不是冗长的解释。
- 将详细的 API 文档放在 `references/` 目录下，而不是正文中。
- 通过相对路径引用脚本：`scripts/my_script.sh`

### 4. 编写脚本

**何时使用脚本：**
- 当代码需要每次都重新编写时。
- 当需要确定性的结果时。
- 当涉及复杂的解析或编码操作（如位字段、二进制格式）时。
- 当需要处理多步骤 API 工作流程并包含错误处理时。

**脚本编写规范：**
- 添加 shebang 行：`#!/usr/bin/env bash` 或 `#!/usr/bin/env python3`
- 将脚本设置为可执行文件：`chmod +x scripts/*.sh`
- 在 Bash 脚本中使用 `set -euo pipefail` 选项。
- 将进度/状态信息输出到标准错误流（stderr），数据输出到标准输出流（stdout）。
- 根据需要支持 `--help` 和 `--json` 参数。
- 使用环境变量进行配置，并设置合理的默认值。

**常见模式：**
- 认证脚本：将凭据缓存到 `~/.openclaw/credentials/` 文件中。
- API 脚本：遵循重定向（`curl -sfL`），处理 JSON 错误。
- 下载脚本：默认情况下进行干运行（不执行实际操作），支持 `--limit` 参数。

### 5. 发布前的检查清单

在发布之前，验证以下内容：
- [ ] 代码或 Git 历史记录中不存在任何敏感信息（密码、令牌、API 密钥）。
- [ ] 代码中不存在硬编码的用户特定路径或凭据。
- [ ] 脚本是可执行的（`chmod +x`）。
- [ ] `curl` 调用在需要时遵循重定向（使用 `-L` 标志）。
- [ ] 所有的 JSON 解析脚本都能优雅地处理空或缺失的字段。
- [ ] 需要变量持久化的 Bash 管道操作使用进程替换（`< <(...)`）而不是 `|`。
- [ ] 前言中的 `description` 包含触发技能的关键词。
- [ ] `.gitignore` 文件排除了 `.skill` 目录。
- [ ] 脚本已经针对实际数据进行了测试。

### 6. 验证和打包

```bash
# Validate only
python3 ~/openclaw_repo/skills/skill-creator/scripts/quick_validate.py ./my-skill

# Package (validates first, then creates .skill zip)
python3 ~/openclaw_repo/skills/skill-creator/scripts/package_skill.py ./my-skill
```

打包检查包括：前言格式、必填字段、命名规范、目录结构以及是否存在符号链接。

### 7. 发布到 ClawHub

```bash
# First time
clawhub login                    # Opens browser for OAuth
clawhub whoami                   # Verify auth

# Publish new skill
clawhub publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --changelog "Initial release"

# Update existing skill
clawhub publish ./my-skill \
  --slug my-skill \
  --version 1.1.0 \
  --changelog "Added feature X, fixed bug Y"

# Bulk sync all local skills
clawhub sync --dry-run           # Preview
clawhub sync --all --bump patch  # Publish all changes
```

**版本控制：** 使用 semver 格式进行版本管理。重大修改使用 major 版本号，功能添加使用 minor 版本号，修复问题使用 patch 版本号。

### 8. 设置 GitHub 仓库（可选但推荐）

```bash
cd my-skill
git init
echo "*.skill" > .gitignore
git add -A && git commit -m "Initial implementation"
gh repo create org/my-skill --private --source=. --push \
  --description "OpenClaw skill: short description"

# Make public when ready
gh repo edit org/my-skill --visibility public --accept-visibility-change-consequences
```

用户可以通过 `git clone` 来安装技能，作为使用 ClawHub 的另一种方式：
```bash
cd /path/to/workspace/skills && git clone https://github.com/org/my-skill.git
```

## ClawHub 命令行接口参考

请参阅 `references/clawhub_cli.md` 以获取完整的命令参考信息。

## 经验总结

请参阅 `references/patterns.md`，了解在实际开发技能过程中遇到的常见问题和解决方法。
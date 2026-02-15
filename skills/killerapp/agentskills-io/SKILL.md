---
name: agentskills-io
description: 根据 agentskills.io 的官方开放标准，创建、验证并发布代理技能（Agent Skills）。该标准适用于以下场景：  
1. 为 AI 代理创建新技能；  
2. 验证技能的结构和元数据；  
3. 了解代理技能的规范；  
4. 将现有文档转换为可移植的技能格式；  
5. 确保与 Claude Code、Cursor、GitHub Copilot 等工具的跨平台兼容性。
license: Apache-2.0
metadata:
  author: agentic-insights
  version: "1.0"
  spec-url: https://agentskills.io/specification
  reference-repo: https://github.com/agentskills/agentskills
---

# 代理技能（agentskills.io）

为 AI 代理创建可移植的技能。支持与 Claude Code、Cursor、GitHub Copilot、OpenAI 的集成，以及 VS Code 的配合使用（通过符号链接实现跨工具共享）。

## 资源
- 规范文档：https://agentskills.io/specification  
- 验证工具：https://github.com/agentskills/agentskills

## 文件结构
```
skill-name/
├── SKILL.md          # Required (frontmatter + instructions, <5000 tokens activation)
├── scripts/          # Optional: executable code
├── references/       # Optional: detailed docs
└── assets/           # Optional: templates, static files
```

**规则**：
- 目录名称必须与 `frontmatter` 中的 `name:` 字段相匹配。
- 该目录下只能包含 3 个子目录。
- 每个 `SKILL.md` 文件的长度应不超过 500 行。
- 文件中的描述性内容（包括 `name` 和 `description`）应控制在约 100 个字符以内，以便于搜索和发现。

## `frontmatter`（文件开头部分）

### 必填字段
- `name`：长度为 1-64 个字符，由小写字母、数字和连字符组成（格式：`^[a-z0-9]+(-[a-z0-9]+)*$`）。
- `description`：长度为 1-1024 个字符，包含使用说明（例如：“适用于……场景”）。

### 可选字段
- `license`：许可证标识符（例如 Apache-2.0、MIT）。
- `compatibility`：对运行环境的要求（长度不超过 500 个字符）。
- `metadata`：键值对格式的信息（例如作者、版本、标签）。
- `allowed-tools`：以空格分隔的工具列表。

## 验证工具
```bash
# Install permanently (vs ephemeral uvx)
uv tool install git+https://github.com/agentskills/agentskills#subdirectory=skills-ref
# Or use uvx for one-shot validation
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate ./skill
```

| 命令 | 描述 |
|---------|-------------|
| `skills-ref validate <path>` | 检查文件结构、`frontmatter` 内容以及各字段的长度是否符合规范。 |
| `skills-ref read-properties <path>` | 提取文件的元数据。 |
| `skills-ref to-prompt <path>` | 生成用于提示用户的提示信息格式。 |

## 编写规范
- 使用祈使句式进行描述（例如：“请执行 `command`”），而非使用“您可能希望……”这样的表述。
- 提供具体的使用示例及预期的输出结果；对常见错误提供解决方法。
- 采用渐进式的信息展示方式：核心内容放在 `SKILL.md` 文件中，详细信息则放在参考文档中。

## 常见错误及解决方法
| 错误类型 | 解决方案 |
|-------|-----|
| 名称无效 | 名称必须仅由小写字母、数字和连字符组成。 |
| 描述缺失 | 必须添加 `description` 字段，并包含使用说明。 |
| 描述过长 | 描述内容应控制在 1024 个字符以内，多余的细节可放在文件正文中。 |
- YAML 格式错误 | 确保缩进正确，特殊字符需使用引号括起来。 |
| 文件名错误 | 文件名必须严格为 `SKILL.md`。 |
| 目录名称不匹配 | 目录名称必须与 `frontmatter` 中的 `name:` 字段一致。 |

## 快速工作流程
1. 创建新技能文件：`mkdir skill-name && touch skill-name/SKILL.md`
2. 添加 `frontmatter`（包含 `name` 和使用说明）。
3. 编写使用说明（使用项目符号列表，避免冗长的叙述性文字）；使用 `skills-ref validate ./skill-name` 进行验证。
4. 在 AI 代理中测试技能效果，根据反馈进行修改；添加许可证信息后，将文件推送到仓库。

## 插件结构（以 Claude Code 为例）
```
plugin-name/
├── .claude-plugin/plugin.json
├── README.md, LICENSE, CHANGELOG.md  # CHANGELOG.md tracks versions
├── skills/skill-name/SKILL.md
├── agents/     # Optional: subagents (.md files)
└── examples/   # Optional: full demo projects
```

**说明**：
- `examples/` 目录下存放可运行的示例项目。
- `assets/` 目录仅包含静态资源（如图片、脚本等）。

## 批量验证与版本管理
```bash
bash scripts/validate-skills-repo.sh     # Validate all skills in repo
bash scripts/bump-changed-plugins.sh     # Auto-bump only changed plugins (semver)
```

## 最小示例文件
```yaml
---
name: example-skill
description: Brief description. Use when doing X.
---
# Example Skill
## Prerequisites
- Required tools
## Instructions
1. First step: `command`
2. Second step with example
## Troubleshooting
**Error**: Message → **Fix**: Solution
```

## 跨工具共享技能
要将技能文件共享到 Claude Code、Cursor 或 VS Code 中，可以使用以下命令：
```
ln -s /path/to/skills ~/.cursor/skills
```

## 参考文档
- [specification.md](references/specification.md)：完整的 YAML 规范文档及各字段的长度限制。
- [examples.md](references/examples.md)：跨平台的完整使用示例。
- [validation.md](references/validation.md)：错误排查指南。
- [best-practices.md](references/best-practices.md)：高级使用技巧及符号链接设置方法。
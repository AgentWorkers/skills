---
name: context-onboarding
description: 为新贡献者和代理提供关于工作区身份文件（SOUL.md、USER.md、AGENTS.md、TOOLS.md）的简要介绍，以及入职指南。当有新成员需要了解工作区的配置信息时，或者当你想要再次确认工作区的设置时，可以使用这些资料。
---

# 上下文引导（Context Onboarding）

## 何时使用此技能

- 当您正在引导新用户使用 Clawdy/Clawd 时，需要快速向他们介绍该工具的特性、使用规则以及与各项技能相关的注意事项。
- 当您需要快速回顾工具的使用偏好或限制（而无需逐个阅读所有文档）时。

## 功能介绍

- `scripts/context_onboarding.py` 会读取关键文档（默认为 `SOUL.md`、`USER.md`、`AGENTS.md` 和 `TOOLS.md`），并打印每份文档的前几行内容，以便用户能够快速了解工具的特性、使用规则及相关信息。
- 该脚本支持 `--files` 参数来指定要包含的额外文档；`--lines` 参数用于控制每份文档显示的行数；`--brief` 参数则仅输出每个文档的开头部分。
- 如果您需要更详细的引导信息（例如推荐新用户阅读哪些文档，或如何保持整体的使用风格一致），请参考 `references/context-guidelines.md`。

## 命令行用法

- `python3 skills/context-onboarding/scripts/context_onboarding.py` 会汇总默认的身份验证相关文档，并打印每份文档的前五行内容。
- 通过添加 `--files docs/PLAYBOOK.md docs/ROLE.md` 等参数，您可以引入额外的参考资料，帮助新用户了解工作流程或发布规范。
- 结合使用 `--lines 2` 和 `--brief` 可以仅获取每份文档的简短摘要。
- `--workspace /path/to/other-workspace` 可用于比较多个工作空间中的文档，或为新的仓库准备相关摘要。

## 示例命令

```bash
python3 skills/context-onboarding/scripts/context_onboarding.py --files references/context-guidelines.md HEARTBEAT.md --lines 2
```

该命令会打印出所有与工具特性、使用规则相关的文档的开头两行内容，帮助您快速了解整体使用风格和注意事项，而无需逐一打开每个文件。

## 参数说明

- `--files <path>`：接受额外的 Markdown 文件路径（以逗号或空格分隔），脚本会按照您提供的顺序将这些文件包含在输出结果中。
- `--lines <n>`：控制每份文档显示的行数（默认为 5 行），您可以据此调整信息的详略程度。
- `--brief`：将每份文档的预览内容压缩为仅包含首句话的部分（以 `.`, `?`, 或 `!` 作为分隔符）。
- `--workspace <dir>`：指定脚本要处理的另一个工作空间路径；适用于新用户的引导、实验性文档的审查或新仓库的准备工作。

## 参考资料

- `references/context-guidelines.md`：详细介绍了新用户需要了解的内容，包括使用规范、角色职责、工作流程以及团队协作的相关提示。

## 资源链接

- **GitHub:** https://github.com/CrimsonDevil333333/context-onboarding
- **ClawHub:** https://www.clawhub.ai/skills/context-onboarding
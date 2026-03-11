---
name: jrv-changelog-gen
description: >
  **从 Git 提交历史生成变更日志**  
  使用传统的提交解析方法，根据需求生成变更日志、创建发布说明、总结 Git 历史、列出标签或日期之间的变更内容，或准备发布文档。支持常规类型的提交（如 `feat`、`fix`、`docs` 等），能够检测破坏性变更，并提供分组输出结果。支持 Markdown 或 JSON 格式。无需任何外部依赖。
---
# 变更日志生成器

该工具能够从 Git 提交历史中生成清晰、专业的变更日志。

## 快速入门

```bash
python3 scripts/changelog_gen.py
python3 scripts/changelog_gen.py --since v1.0.0 --group
python3 scripts/changelog_gen.py --since v1.0.0 --until v2.0.0 --format json
python3 scripts/changelog_gen.py --repo /path/to/project --since "2026-01-01" -o CHANGELOG.md
```

## 主要功能

- **常规提交类型识别** — 自动识别以下类型的提交：feat（新增功能）、fix（修复问题）、docs（更新文档）、refactor（重构代码）、perf（性能优化）、test（测试）、build（构建）、ci（持续集成）、chore（杂务性任务）、revert（回滚提交）。
- **破坏性变更检测** — 通过提交信息中的 `!` 后缀或 `BREAKING CHANGE` 字样来识别破坏性变更。
- **分组输出** — 可使用 `--group` 选项按提交类型对变更日志进行分组。
- **标签范围** — 可生成指定标签或引用之间的变更日志。
- **双格式输出** — 支持 Markdown（默认格式）和 JSON 格式。
- **文件输出** — 可使用 `-o` 选项将日志直接写入 `CHANGELOG.md` 文件。
- **无需依赖** — 仅依赖 Python 标准库和 Git 工具。

## 参数说明

| 参数 | 说明 |
|------|-------------|
| `--repo PATH` | Git 仓库路径（默认为当前工作目录） |
| `--since REF` | 开始的引用（标签、分支或提交） |
| `--until REF` | 结束的引用（默认为 `HEAD`） |
| `--format md\|json` | 输出格式（默认为 Markdown） |
| `--group` | 按类型对提交进行分组 |
| `-o FILE` | 将日志写入指定文件 |

## 支持的常规提交类型

feat（新增功能）、fix（修复问题）、docs（更新文档）、style（代码格式调整）、refactor（重构代码）、perf（性能优化）、test（测试）、build（构建）、ci（持续集成）、chore（杂务性任务）、revert（回滚提交）—— 这些类型的提交都会被自动识别并生成相应的日志。
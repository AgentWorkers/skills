---
name: vet-repo
description: 扫描仓库代理配置文件，以检测已知的恶意模式。
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash
context: fork
---

# vet-repo -- 仓库代理配置扫描器

该工具用于扫描仓库中的所有代理配置文件，以检测已知的恶意模式。在处理不熟悉的代码库时，可以使用该工具来评估代理层级的安全风险，从而在信任仓库的配置之前对其进行验证。

## 使用方法

在当前项目的根目录下运行扫描脚本：

```bash
python3 "$SKILL_DIR/scripts/vet_repo.py" "$PROJECT_ROOT"
```

其中 `$SKILL_DIR` 是包含此 `SKILL.md` 文件的目录，`$PROJECT_ROOT` 是正在被扫描的仓库的根目录。

## 扫描范围：

- `.claude/settings.json` 文件：代理配置相关设置（自动批准、循环终止、环境变量持久化等）
- `.claude/skills/` 目录：所有 `SKILL.md` 文件（其中可能包含隐藏的注释、curl 或 bash 命令、配置触发器等）
- `.mcp.json` 文件：MCP 服务器配置（包含未知的 URL、环境变量扩展信息、使用的工具等）
- `CLAUDE.md` 或 `.claude/CLAUDE.md` 文件：项目配置中可能存在的指令注入风险

## 扫描结果：

扫描结果将以结构化的报告形式呈现，其中问题按严重程度（CRITICAL、HIGH、MEDIUM、LOW、INFO）进行分类，并针对每个问题提供相应的处理建议。

## 使用场景：

- 在信任克隆过来的仓库的代理配置之前
- 在拉取修改了 `.claude/` 或 `.mcp.json` 文件的更新之后
- 作为任何包含代理组件的代码库的安全审查的一部分
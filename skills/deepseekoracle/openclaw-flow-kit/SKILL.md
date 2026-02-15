---
name: openclaw-flow-kit
description: "修复 OpenClaw 工作流程中的常见瓶颈：平台相关的 engage-gates/429 回退辅助工具（从 MoltX 开始）、用于链接脚本的标准化 JSON 结果格式、工作区路径解析辅助工具，以及一个简单的技能发布管理工具（包括准备、发布和草稿公告等功能）。"
---

# OpenClaw 流程工具包

在遇到以下问题时，请使用此工具包：
- 平台触发“engage gates”机制或出现不稳定的 429 错误（尤其是 MoltX 相关问题）；
- 脚本输出结果不一致，导致技能链的自动化执行变得困难；
- 与工作区相关的路径问题（例如：在技能或状态数据中写入数据时出现错误）；
- 技能发布步骤重复（包括发布操作和生成公告草稿）。

## 快速命令

### 1) 任何命令的标准结果输出格式
```bash
python scripts/run_envelope.py -- cmd /c "echo hello"
```
输出格式为 JSON：
- `ok`, `exit_code`, `stdout`, `stderr`, `startedAt`, `endedAt`, `durationMs`

### 2) MoltX engage-gate 辅助工具（读取数据流并执行类似或重新发布操作）
```bash
python scripts/moltx_engage_gate.py --mode minimal
```
之后可以正常执行您的发布操作。

### 3) 工作区根目录解析工具（导入辅助功能）
在脚本中使用该工具来查找实际的工作区根目录：
```py
from scripts.ws_paths import find_workspace_root
WS = find_workspace_root(__file__)
```

### 4) 技能发布流程管理工具（准备 → 发布 → 生成公告草稿）
```bash
python scripts/release_conductor.py prepare --skill-folder skills/public/my-skill
python scripts/release_conductor.py publish --skill-folder skills/public/my-skill --slug my-skill --name "My Skill" --version 1.0.0 --changelog "..."
python scripts/release_conductor.py draft --slug my-skill --name "My Skill" --out tmp/drafts
```

**注意事项：**
- `draft` 命令用于生成公告文本文件，但不会实际进行发布操作。
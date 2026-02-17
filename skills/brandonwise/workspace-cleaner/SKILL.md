# 工作区清理工具

专为 OpenClaw 工作区设计的安全、自动化清理工具。能够查找临时文件、重复文件以及无用的文件，同时保护重要数据。

## 快速入门

```bash
# Preview what would be deleted (safe - no changes)
python3 {{SKILL_DIR}}/scripts/cleanup.py

# Actually clean up (uses trash for recovery)
python3 {{SKILL_DIR}}/scripts/cleanup.py --execute

# Custom workspace path
python3 {{SKILL_DIR}}/scripts/cleanup.py --workspace /path/to/workspace
```

## 主要功能

- **默认执行预览** — 在删除前始终会显示待删除文件的列表
- **使用系统回收站** — 文件会被移至系统回收站，可恢复
- **支持文件大小过滤** — 可根据文件大小进行筛选
- **基于文件年龄过滤** — 可删除超过 N 天的文件
- **自定义过滤规则** — 可编辑配置以适应您的使用习惯
- **输出 JSON 格式** — 便于自动化脚本使用
- **安全设置** — 绝不删除 `.git/` 目录、`memory/` 目录、`coreconfigs` 文件

## 命令

### 预览（默认）
```bash
python3 {{SKILL_DIR}}/scripts/cleanup.py
```
显示待删除文件的列表及文件大小。不会对文件进行任何修改。

### 执行清理
```bash
python3 {{SKILL_DIR}}/scripts/cleanup.py --execute
```
将文件移至系统回收站。文件可通过系统回收站恢复。

### 按文件大小过滤
```bash
# Only show items larger than 100MB
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-size 100
```

### 按文件年龄过滤
```bash
# Only show items older than 30 days
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-age 30
```

### 输出 JSON 数据
```bash
# For automation/parsing
python3 {{SKILL_DIR}}/scripts/cleanup.py --json
```

### 自定义配置
```bash
# Use custom patterns file
python3 {{SKILL_DIR}}/scripts/cleanup.py --config /path/to/patterns.json
```

## 被清理的文件类型

默认的过滤规则（可通过配置进行自定义）：

| 类别 | 过滤模式 | 是否安全？ |
|----------|----------|-------|
| 临时下载文件 | 根目录下的 `*.skill` | ✅ |
| 生成的图片 | 根目录下的 `*.png`、`*.jpg` | ✅ |
| macOS 无用文件 | `.DS_Store` | ✅ |
- 日志文件 | `*.log` | ✅ |
| 临时文件 | `*.tmp`、`*.bak`、`*~` | ✅ |
- Node.js 模块 | 根目录下的 `node_modules/` | ✅ |
- Python 环境 | `.venv*/`、`venv/`（已知文件除外） | ⚠️ |
- 重复的仓库文件 | 与项目目录同名的文件 | ⚠️ |

## 被保护的文件

无论过滤规则如何，以下文件都不会被删除：
- `.git/` 目录
- `memory/` 目录
- `MEMORY.md`、`SOUL.md`、`USER.md`、`AGENTS.md` 文件
- `projects/` 目录的内容
- `skills/` 目录的内容
- 过去 24 小时内被修改的文件（除非使用了 `--include-recent` 选项）

## 配置

请编辑 `{{SKILL_DIR}}/config/patterns.json` 文件以自定义过滤规则：

```json
{
  "temp_extensions": [".tmp", ".bak", ".log", ".skill"],
  "temp_patterns": ["*~", "#*#"],
  "image_extensions": [".png", ".jpg", ".jpeg", ".gif"],
  "protected_dirs": ["memory", "skills", "projects", ".git"],
  "protected_files": ["MEMORY.md", "SOUL.md", "USER.md", "AGENTS.md"],
  "known_venvs": [".venv-skill-scanner"]
}
```

## 集成到 HEARTBEAT 中

将此工具集成到您的 `HEARTBEAT.md` 文件中，实现定期自动清理：

```markdown
## Weekly Cleanup Check
- Run workspace cleaner in preview mode
- Alert if >500MB of cruft found
- Auto-clean items >30 days old and <10MB
```

## 安全提示

1. **务必先预览** — 在执行删除操作前，请先查看预览结果。
2. **文件会被移至系统回收站** — 文件不会被永久删除。
3. **排除误判的文件** — 可使用 `--exclude` 选项排除看似无用但实际上重要的文件。
4. **建议备份** — 在进行大规模清理前，请先备份数据。

## 使用示例

### 定期维护
```bash
# Weekly cleanup of obvious cruft
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-age 7 --execute
```

### 查找占用大量空间的文件
```bash
# What's taking up space?
python3 {{SKILL_DIR}}/scripts/cleanup.py --min-size 50 --json | jq '.items | sort_by(.size_mb) | reverse'
```

### 提交前清理
```bash
# Clean before committing
python3 {{SKILL_DIR}}/scripts/cleanup.py --execute && git status
```

## 系统要求

- Python 3.8 或更高版本
- 需要支持 `trash` 命令（macOS：`brew install trash`；Linux：`trash-cli`）
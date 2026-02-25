---
name: workspace-organization
version: 1.0.0
description: OpenClaw的自动化工作区健康检查及熵值防护功能：能够检测到损坏的符号链接、空目录、过大文件以及格式错误的文件名。该维护审计脚本支持通过Cron任务自动执行，确保部署环境保持整洁且结构有序。
homepage: https://clawhub.com
changelog: Initial release - Maintenance audit, setup script, organization standards
metadata:
  openclaw:
    emoji: "📁"
    requires:
      bins: ["bash", "find", "du"]
    os:
      - linux
      - darwin
---
# 工作区组织

为确保 OpenClaw 环境的整洁和高效运行，我们制定了相应的标准和自动化维护流程。

## 包含的文件

- `SKILL.md` — 代理操作指南
- `README.md` — 设置指南
- `maintenance-audit.sh` — 用于检查工作区健康状况的脚本
- `setup.sh` — 用于初始化标准工作区结构的脚本

**注意：** 这些脚本会自动检测您的工作区。如需覆盖默认路径，可执行 `./maintenance-audit.sh /custom/path`。

## 解决的问题

随着时间的推移，工作区可能会出现以下问题：
- 文件移动后导致符号链接失效
- 项目被删除后留下空目录
- 大文件占用过多磁盘空间
- 文件/目录名称格式错误导致脚本运行失败
- 无法及时了解工作区的健康状况

本技能提供了自动化审计和清理建议，以帮助您避免这些问题。

## 使用场景

- **新工作区设置**：初始化标准目录结构
- **定期维护**：每周/每月进行健康检查（建议使用 cron 任务）
- **部署前清理**：在备份前清除不必要的文件
- **排查工作区问题**：查找失效的符号链接和格式错误的文件
- **检查磁盘空间**：识别占用大量空间的文件

## 提供的功能

### 1. `maintenance-audit.sh`
自动化健康检查脚本，可检测以下问题：
- ✅ 失效的符号链接
- ✅ 空目录（不包括 `node_modules` 和 `.git` 目录）
- ✅ 大文件（大于 10MB）
- ✅ 格式错误的文件/目录名称
- **顶级目录的磁盘使用情况**
- **文件/目录的数量**
- **最近 24 小时的更改记录**

### 2. `setup.sh`
用于初始化标准工作区结构：
```
~/.openclaw/workspace/
├── projects/           # Active work
│   ├── writing/        # Writing projects
│   └── code/           # Code projects
├── notes/              # Organized notes
│   ├── daily-reviews/
│   ├── decisions/
│   └── cost-tracking.md
├── memory/             # Long-term memory
│   ├── owner/          # Cross-channel user memory
│   └── sessions/       # Per-session isolated memory
├── skills/             # Custom skills
├── subagents/          # Permanent specialists
│   └── _archived/      # Old/deprecated subagents
├── docs/               # Documentation
└── scripts/            # Utility scripts
```

### 3. 组织标准（文档）
- 文件命名规范（使用驼峰式命名法，不含空格）
- 目录结构指南
- 清理策略（哪些文件需要保留/删除）
- Git 集成方式

## 设置步骤

1. **安装相关工具：**
```bash
cd ~/.openclaw/workspace/skills
clawhub install workspace-organization
# Or: download from ClawHub and extract
```

2. **初始化工作区（如需从头开始设置）：**
```bash
cd ~/.openclaw/workspace/skills/workspace-organization
./setup.sh
```

3. **首次执行审计：**
```bash
cd ~/.openclaw/workspace/skills/workspace-organization
./maintenance-audit.sh
```

4. **安排自动化审计（建议）：**
```bash
openclaw cron add \
  --name "Weekly Workspace Audit" \
  --schedule "0 4 * * 0" \
  --task "Run workspace maintenance audit: bash skills/workspace-organization/maintenance-audit.sh. Log results to notes/maintenance-log.md"
```

## 使用方法

### 手动审计
```bash
cd ~/.openclaw/workspace/skills/workspace-organization
./maintenance-audit.sh
```

**示例输出：**
```
=== Workspace Maintenance Audit ===
Date: 2026-02-21 16:00
Path: /home/user/.openclaw/workspace

1. Checking for broken symlinks...
⚠️  Found broken symlinks:
/home/user/.openclaw/workspace/old-project/link-to-deleted

2. Checking for empty directories...
ℹ️  Found empty directories:
/home/user/.openclaw/workspace/projects/abandoned

3. Checking for large files (>10MB)...
ℹ️  Found large files:
24M	/home/user/.openclaw/workspace/logs/debug.log

4. Checking for malformed file/directory names...
⚠️  Found malformed names:
/home/user/.openclaw/workspace/projects/my project/file.md

5. Disk usage by top-level directory:
150M	skills
80M	notes
50M	projects
30M	memory

6. File counts:
  Total files: 1,234
  Total directories: 156
  Skills: 18
  Subagents: 3

7. Recently modified files (last 24 hours):
/home/user/.openclaw/workspace/notes/cost-tracking.md
/home/user/.openclaw/workspace/memory/owner/decisions.md

=== Audit Complete ===
```

### 代理驱动的审计
通过代理执行审计：
```
"Run workspace maintenance audit"
"Check workspace health"
"Audit my workspace"
```

代理会运行脚本并展示审计结果及清理建议。

## 常见问题及解决方法

### 1. 失效的符号链接
**原因：**
- 文件被移动或重命名
- 依赖项被删除
- 相对路径错误

**解决方法：** 删除失效的符号链接或更新目标文件。

### 2. 空目录
**原因：**
- 项目被删除
- 安装失败
- 迁移不完整

**解决方法：** 除非是故意设置的占位符，否则删除这些目录。

### 3. 大文件
**常见来源：**
- 未压缩的日志文件（如 `debug.log`、`error.log`）
- 二进制文件（如 `.zip`、`.tar.gz`）
- 下载的数据集
- 视频/媒体文件

**解决方法：** 对这些文件进行压缩，或将其移至外部存储。

### 4. 格式错误的文件名
**问题原因：**
- 文件名中包含空格 → 导致脚本运行失败
- 包含特殊字符 → 引发 shell 解释问题
- 括号/方括号的使用不当 → 造成glob匹配问题

**解决方法：** 使用驼峰式命名法（`kebab-case`）或蛇形命名法（`snake_case`）重新命名文件。

## 工作区健康评分

运行 `maintenance-audit.sh` 后，您的工作区会得到一个评分：

| 评分 | 状态 | 含义 |
|-------|--------|---------|
| 90-100 | 🟢 | 工作区状态良好，仅有小问题或无问题 |
| 70-89 | 🟡 | 需要清理一些文件 |
| 50-69 | 🟠 | 存在多个问题 |
| <50 | 🔴 | 需立即进行清理 |

评分依据：
- 失效的符号链接（每个扣 10 分）
- 空目录（每个扣 2 分）
- 大文件（每个扣 5 分）
- 格式错误的文件名（每个扣 3 分）

## 自动化策略

| 审计频率 | 执行操作 | 原因 |
|-----------|--------|--------|
| **每日** | 不执行审计 | 避免频繁干扰 |
| **每周** | 仅进行审计并记录结果 | 及时发现问题 |
| **每月** | 审计后向用户展示结果 | 用户审批清理方案 |
| **按需** | 在备份/部署前执行审计 | 减少备份文件大小 |

## 相关技能

- **system-resource-monitor**：提供磁盘使用情况警报，辅助监控工作区健康状况
- **cost-governor**：跟踪子代理的运行成本及工作区的整洁度

## 与其他技能的集成

- **openclaw-backup**：在备份前执行审计，以减少备份文件大小
- **cost-governor**：监控磁盘使用情况，帮助控制成本
- **drift-guard**：通过指标监控工作区的混乱程度

## 自定义设置

### 调整大文件阈值
编辑 `maintenance-audit.sh` 文件以调整大文件的判断标准：
```bash
# Change from 10MB to 50MB
find "$WS" -type f -size +50M 2>/dev/null
```

### 排除特定目录
在脚本中添加排除规则，以忽略某些目录：
```bash
find "$WS" -type d -empty 2>/dev/null \
  | grep -v "node_modules" \
  | grep -v ".git" \
  | grep -v "your-custom-dir"
```

### 扩展检查功能
- 添加 Git 仓库状态检查
- 执行依赖项漏洞扫描
- 进行许可证合规性审计

## 设计理念

- **预防混乱**：不进行维护，工作区结构会逐渐恶化
- **自动化检测**：脚本能发现人类可能忽略的问题
- **用户授权的清理**：未经许可，不会自动删除文件
- **灵活优先于严格规定**：遵循指导原则，而非死板规则

## 故障排除

**“在 macOS 上脚本无法运行”**
- 安装 `GNU findutils`：`brew install findutils`
- 使用 `gfind` 替代 `find` 命令

**“检测到太多空目录”**
- 在脚本中添加更多需要排除的目录（如 `.cache`、`.venv`）

**“某些大文件是必需的”**
- 在 `notes/workspace-notes.md` 中记录保留这些文件的理由
- 考虑将这些文件移至外部存储（如 S3、NAS）

## 高级功能：多工作区管理
如果需要管理多个 OpenClaw 实例，请参考以下内容：
```bash
# Audit all workspaces
for ws in ~/.openclaw-*; do
  WS="$ws/workspace" ./maintenance-audit.sh
done
```

---

**作者：** OpenClaw 社区  
**许可证：** MIT  
**运行要求：** Bash 操作系统及 GNU coreutils（`find`、`du`、`sort` 工具）
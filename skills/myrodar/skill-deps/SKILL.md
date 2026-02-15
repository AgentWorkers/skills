---
name: skill-deps
description: 跟踪和管理 OpenClaw 技能之间的依赖关系。扫描技能以检测依赖项，可视化技能树结构，识别循环依赖关系，并管理技能的版本控制。适用于分析技能之间的关系、检查哪些技能依赖于其他技能，或管理技能的安装过程。
---

# 技能依赖关系

用于管理 OpenClaw 技能之间的依赖关系（类似于 npm 对于普通软件包的管理方式）。

## 版本约束

支持 semver 格式的版本约束：

```yaml
depends:
  - weather@>=1.0.0      # Version 1.0.0 or higher
  - calendar@^2.0.0      # Compatible with 2.x.x
  - browser@~1.2.0       # Approximately 1.2.x
  - coding-agent@*       # Any version
  - github@1.5.0         # Exact version
```

## 冲突检测

声明那些不能同时使用的技能：

```yaml
conflicts:
  - old-weather          # Cannot use with old-weather
  - legacy-calendar
```

## 概念

### 声明依赖关系

在技能的 `SKILL.md` 文件的 `frontmatter` 部分中，可以声明技能之间的依赖关系：

```yaml
---
name: my-skill
description: Does something cool
depends:
  - weather          # Requires weather skill
  - coding-agent     # Requires coding-agent skill
optional:
  - github           # Enhanced if github skill present
---
```

### 依赖类型

- **depends**：必需的技能（如果缺少，则安装失败）
- **optional**：如果存在，则提供额外的功能
- **conflicts**：不能与这些技能同时使用

## 命令

### 扫描技能
```bash
# Scan all installed skills for dependencies
./scripts/scan-skills.sh

# Scan specific skill
./scripts/scan-skills.sh weather
```

### 依赖关系树
```bash
# Show full dependency tree
./scripts/skill-tree.sh my-skill

# Output:
# my-skill
# ├── weather (required)
# │   └── (no dependencies)
# └── coding-agent (required)
#     └── github (optional)
```

### 检查缺失的依赖关系
```bash
# Find skills with unmet dependencies
./scripts/check-deps.sh
```

## 注册表格式

技能可以通过 `skill.json` 文件来声明自己的元数据：

```json
{
  "name": "my-skill",
  "version": "1.0.0",
  "depends": {
    "weather": ">=1.0.0",
    "coding-agent": "*"
  },
  "optional": {
    "github": ">=2.0.0"
  }
}
```

## 技能的存放位置

系统会扫描以下目录来查找技能：
1. `/usr/lib/node_modules/openclaw/skills/` — 内置技能
2. `~/.openclaw/workspace/skills/` — 用户自定义的技能
3. `./skills/` — 项目内部的技能

## 与 ClawHub 注册表的集成

可以从 clawhub.com 安装技能：

```bash
# Install a skill (auto-resolves dependencies)
./scripts/skill-install.sh weather

# Install with specific version
./scripts/skill-install.sh weather@1.2.0

# Search for skills
./scripts/skill-search.sh "calendar"

# List installed vs available
./scripts/skill-list.sh --outdated
```

## 自动解析依赖关系

在安装带有依赖关系的技能时，系统会自动处理这些依赖关系：

```
$ ./scripts/skill-install.sh travel-planner

📦 Resolving dependencies for travel-planner@1.0.0...
  ├── weather@>=1.0.0 → weather@1.2.3 ✅
  ├── calendar@^2.0 → calendar@2.1.0 ✅
  └── browser (optional) → browser@3.0.0 ✅

🔍 Checking conflicts...
  └── No conflicts found ✅

📥 Installing 4 skills...
  ✅ weather@1.2.3
  ✅ calendar@2.1.0
  ✅ browser@3.0.0
  ✅ travel-planner@1.0.0

Done! Installed 4 skills.
```

## 命令汇总

| 命令 | 描述 |
|---------|-------------|
| `scan-skills.sh` | 列出所有技能及其依赖关系 |
| `skill-tree.sh <名称>` | 显示技能的依赖关系树 |
| `check-deps.sh` | 检查缺失的依赖关系 |
| `skill-install.sh <名称>` | 从 ClawHub 安装技能 |
| `skill-search.sh <查询>` | 在注册表中搜索技能 |
| `check-conflicts.sh` | 检测技能之间的冲突 |
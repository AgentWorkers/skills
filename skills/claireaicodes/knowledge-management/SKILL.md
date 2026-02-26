---
name: knowledge-management
description: 将 OpenClaw 的知识条目按照内容类型（研究、决策、见解、经验教训、模式、项目、参考资料、教程）整理并分类到相应的本地文件夹中。
homepage: https://github.com/ClaireAICodes/openclaw-skill-knowledge-management
metadata: { "openclaw": { "emoji": "📚", "requires": { "bins": ["km"] } } }
---
# 知识管理技能（本地存储）

将您的 OpenClaw 存储文件组织成一个结构化的本地知识库。该技能会自动解析 `MEMORY.md` 文件以及每日生成的存储文件，按内容类型对条目进行分类，并将每个条目作为带有时间戳的 Markdown 文件存储在相应的文件夹中。

## 可用工具

### 核心命令
- `km sync [选项]` - 将存储条目同步到本地文件
- `km classify [选项]` - 解析并分类条目（不进行存储，输出 JSON 格式）
- `km summarize [选项] - 为每种内容类型生成索引文件
- `km cleanup [选项] - 删除孤立文件
- `km list_types` - 列出所有可用的内容类型

## 设置

无需 API 密钥！该技能使用两个路径：
- **输入工作区**：从该路径读取 `MEMORY.md` 文件和每日生成的存储文件。
- **输出目录**：将整理后的文件写入该路径。

这两个路径会自动检测：

### 输入工作区（源文件）
1. `OPENCLAWORKSPACE` 环境变量
2. `--workspace <路径>` 命令行参数
3. 当前工作目录（如果其中包含 `MEMORY.md` 文件）
4. 默认值：`~/.openclaw/workspace`

### 输出目录（整理后的文件）
1. `--output-dir <路径>` 命令行参数（相对于工作区的路径或绝对路径）
2. 默认值：`<workspace>/memory/KM`

该技能会自动创建输出目录及所有内容类型的文件夹。

如果您需要预先创建这些目录，请参考以下代码块：

```bash
mkdir -p ~/.openclaw/workspace/memory/KM/{Research,Decision,Insight,Lesson,Pattern,Project,Reference,Tutorial}
```

## 使用示例

### 默认路径（输入位于工作区根目录，输出位于 `memory/KM`）
```bash
# From any directory (workspace auto-detected)
km sync --days_back 7 --cleanup
```

### 自定义输入工作区和输出目录
```bash
km sync --workspace /custom/input/workspace --output-dir /custom/output/KM --days_back 7
```

### 使用环境变量
```bash
export OPENCLAWORKSPACE=/custom/input/workspace
km sync --output-dir /custom/output/KM --days_back 7
```

### 干运行（仅预览）
```bash
km sync --dry_run --days_back 1
```

### 对条目进行分类并导出 JSON
```bash
km classify --days_back 3 > entries.json
```

### 生成索引文件（默认输出到输出目录）
```bash
km summarize
# or specify different location
km summarize --output_dir ~/some/other/folder
```

### 预览孤立文件的清理情况
```bash
km cleanup --dry_run
```

### 列出内容类型
```bash
km list_types
```

## 存储结构

假设使用默认配置：
- 输入工作区：`~/.openclaw/workspace`
- 输出目录：`~/.openclaw/workspace/memory/KM`

```
~/.openclaw/workspace/
├── MEMORY.md                (source file - you edit this)
├── memory/                  (daily memory files)
│   ├── 2025-02-11.md
│   ├── 2025-02-12.md
│   └── ...
└── memory/KM/               (organized output by the skill)
    ├── local-sync-state.json
    ├── local-sync-log.md
    ├── Research/
    │   ├── 20260215T1448_Title_Here_HASH.md
    │   └── ...
    ├── Decision/
    ├── Insight/
    ├── Lesson/
    ├── Pattern/
    ├── Project/
    ├── Reference/
    ├── Tutorial/
    ├── Research_Index.md
    ├── Decision_Index.md
    └── ... (other index files)
```

### 文件命名规则

文件格式：`YYYYMMDDTHHMM_Title_With_Underscores_8CHARHASH.md`

8 位的哈希后缀可以避免文件名冲突，即使标题相同但内容不同。

### 文件内容（YAML 标头）

```markdown
---
title: "Protocol Name"
content_type: "Research"
domain: "OpenClaw"
certainty: "Verified"
impact: "Medium"
confidence_score: 8
tags: ["AI", "Automation"]
source: "MEMORY.md"
source_file: "MEMORY.md"
date: "2026-02-11"
content_hash: "e4b30e75d0f5a662"
---

Entry body content starts here...
```

## 工作原理

1. 解析 `MEMORY.md` 文件以及最近的每日存储文件（`memory/*.md`）。
2. 对每个条目进行分类（包括内容类型、领域、确定性、影响程度、标签和置信度）。
3. 计算内容的哈希值以消除重复。
4. 检查 `memory/local-sync-state.json` 文件的状态，跳过已同步的条目。
5. 将文件写入带有时间戳和哈希值的文件夹中。
6. 更新状态映射（哈希值 → 文件路径）。
7. 可选地执行清理操作，删除未处于同步状态的文件。

## 分类逻辑

- **内容类型**：基于关键词匹配（研究、课程、决策、模式、教程、参考、见解等）。
- **领域**：根据上下文推断（如 AI 模型、OpenClaw、成本、交易等）。
- **确定性**：根据语言判断（已验证、可能、推测性、观点）。
- **影响程度**：根据重要性指标（高、中、低、可忽略）。
- **标签**：从预定义的关键词映射中自动提取。
- **置信度得分**：基于 1–10 的评分标准（来源可信度、内容长度、数据提及次数）。

您可以通过编辑 `index-local.js` 文件中的 `EntryClassifier` 类来自定义分类规则。

## 状态管理

`memory/local-sync-state.json` 文件将内容哈希值映射到文件路径：

```json
{
  "e4b30e75d0f5a662": "/path/to/Research/202602151440_Title_e4b30e75.md"
}
```

这确保了同步操作的幂等性，并能快速检测重复文件。

**请勿手动编辑此文件**，除非需要从损坏的状态中恢复数据。

## Cron 任务集成

可以设置每日自动同步：

```bash
openclaw cron add \
  --name "Daily Knowledge Sync" \
  --cron "0 5 * * *" \
  --tz "Asia/Singapore" \
  --session isolated \
  --message "km sync --days_back 7"
```

注意：默认情况下，该技能会从 `~/.openclaw/workspace` 读取 `MEMORY.md` 文件，并将整理后的文件写入 `~/.openclaw/workspace/memory/KM`。您可以使用 `--workspace` 或 `--output-dir` 参数来自定义这些路径。

## 故障排除

- **“km: 命令未找到”**：在技能目录中运行 `npm link` 命令，或将 `~/workspace/bin` 添加到 `PATH` 环境变量中。
- **未找到条目**：确保 `MEMORY.md` 文件使用了 `##` 作为章节标题前缀，并且每个条目的标题使用了 `###` 标签。
- **文件未创建**：检查写入权限；使用 `--verbose` 选项运行脚本。
- **旧条目未同步**：这些条目可能已经被标记为已同步状态。请清除 `memory/KM/local-sync-state.json` 文件以强制重新同步（注意：可能会导致文件重复）。
- **文件重复**：运行 `km cleanup` 命令删除孤立文件，然后再次运行 `km sync` 命令以创建缺失的文件。

---

**版本：2.0.0**
**更新时间：2026-02-15** — 从 Notion 数据存储方式切换到本地存储，并添加了哈希后缀以确保文件唯一性。
**作者：Claire（OpenClaw 代理）**
**许可证：MIT**
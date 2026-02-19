---
name: knowledge-management
description: 将 OpenClaw 的知识条目按照内容类型（研究、决策、见解、经验教训、模式、项目、参考资料、教程）组织并分类到相应的本地文件夹中。
homepage: https://github.com/ClaireAICodes/openclaw-skill-knowledge-management
metadata:
  {
    "openclaw": {
      "emoji": "📚",
      "bins": ["km"]
    }
  }
---
# 知识管理技能（本地存储）

将您的 OpenClaw 存储文件组织成一个结构化的本地知识库。该技能会自动解析 `MEMORY.md` 文件以及每日生成的存储文件，根据内容类型对条目进行分类，并将每个条目作为带有时间戳的 Markdown 文件存储在相应的文件夹中。

## 可用工具

### 核心命令
- `km sync [选项]` - 将存储条目同步到本地文件
- `km classify [选项]` - 解析并分类条目（不进行存储，输出 JSON 格式）
- `km summarize [选项] - 为每种内容类型生成索引文件
- `km cleanup [选项] - 删除孤立文件
- `km list_types` - 列出所有可用的内容类型

## 设置

无需 API 密钥！请确保您的工作区包含以下文件夹：

```bash
mkdir -p ~/.openclaw/workspace/{Research,Decision,Insight,Lesson,Pattern,Project,Reference,Tutorial}
```

该技能会自动创建缺失的文件夹。

## 使用示例

### 同步过去 7 天的数据并清理旧文件
```bash
km sync --days_back 7 --cleanup
```

### 仅预览（不执行实际操作）
```bash
km sync --days_back 14 --dry_run
```

### 对条目进行分类并导出 JSON 格式
```bash
km classify --days_back 3 > entries.json
```

### 生成索引文件
```bash
km summarize --output_dir ~/.openclaw/workspace
```

### 预览并清理孤立文件
```bash
km cleanup --dry_run
```

## 存储结构

```
~/.openclaw/workspace/
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

8 位的内容哈希后缀可以避免文件名冲突（即使标题相同，内容不同也能区分文件）。

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

1. 解析 `MEMORY.md` 文件以及最近每日生成的 `memory/*.md` 文件
2. 对每个条目进行分类（包括内容类型、领域、确定性、影响程度、标签和置信度）
3. 计算内容哈希值以实现去重
4. 检查 `memory/local-sync-state.json` 文件以跳过已同步的条目
5. 将文件写入带有时间戳和哈希值的文件夹中
6. 更新文件路径与哈希值的映射关系
7. 可选地执行清理操作，删除未同步的文件

## 分类逻辑

- **内容类型**：基于关键词匹配（研究、课程、决策、模式、教程、参考、见解等）
- **领域**：根据上下文推断（AI 模型、OpenClaw、成本、交易等）
- **确定性**：根据语言判断（已验证、可能、推测、观点等）
- **影响程度**：根据重要性指标划分（高、中、低、可忽略）
- **标签**：从预定义的关键词映射中自动提取
- **置信度**：基于来源可信度、文件长度和数据提及次数等因素进行评估（1–10 分）

您可以通过编辑 `index-local.js` 文件中的 `EntryClassifier` 类来自定义分类规则。

## 状态管理

`memory/local-sync-state.json` 文件用于存储内容哈希值与文件路径的映射关系：

```json
{
  "e4b30e75d0f5a662": "/path/to/Research/202602151440_Title_e4b30e75.md"
}
```

这有助于实现幂等同步和快速检测重复文件。

**请勿手动编辑该文件**，除非需要从损坏的状态中恢复数据。

## Cron 任务集成

可以设置每日自动同步任务：

```bash
openclaw cron add \
  --name "Daily Knowledge Sync" \
  --cron "0 5 * * *" \
  --tz "Asia/Singapore" \
  --session isolated \
  --message "km sync --days_back 7"
```

## 常见问题及解决方法

**“km: command not found”**
- 在技能目录中运行 `npm link` 命令，或将 `~/workspace/bin` 添加到系统的 `PATH` 环境变量中。

**找不到条目**
- 确保 `MEMORY.md` 文件使用了 `##` 作为章节标题的标识符，并且每个条目的标题前使用了 `###`。

**文件未生成**
- 检查写入权限；可以使用 `--verbose` 选项运行命令。

**旧条目未同步**
- 这些条目可能已经被标记为已同步状态。您可以清除 `memory/local-sync-state.json` 文件以强制重新同步（注意：可能会导致文件重复）。

**文件重复**
- 先运行 `km cleanup` 命令删除孤立文件，然后再运行 `km sync` 命令生成缺失的文件。

---

**版本：2.0.0**
**更新时间：2026-02-15** — 从 Notion 服务切换到本地存储系统，并添加了哈希后缀以确保文件唯一性。
**作者：Claire（OpenClaw 项目成员）**
**许可证：MIT**
---
name: export-skills
description: 将 SpecWeave 中的技能导出为 Agent Skills 的开放标准格式（agentskills.io），以实现跨平台移植。此操作适用于将技能转换为 GitHub Copilot、VS Code、Gemini CLI 或 Cursor 格式时。生成的 SKILL.md 文件可与任何支持 Agent Skills 的工具兼容。
visibility: public
allowed-tools: Read, Write, Glob, Bash
---

# 将 SpecWeave 技能导出为 Agent Skills 标准格式

## 概述

本工具用于将 SpecWeave 中定义的技能导出为 [Agent Skills](https://agentskills.io) 开放标准格式。这有助于实现技能在以下工具间的移植：

- **GitHub Copilot**（VS Code 插件）
- **Gemini CLI**
- **Cursor**
- **Claude Code**
- 其他支持 Agent Skills 的工具

## 使用方法

```
/sw:export-skills [options]
```

### 参数说明

| 参数 | 说明 |
|--------|-------------|
| `--output <dir>` | 输出目录（默认值：`.agent-skills/`） |
| `--plugin <name>` | 导出特定的插件（默认值：所有插件） |
| `--skill <name>` | 导出特定的技能（默认值：所有技能） |
| `--dry-run` | 预览导出结果（不生成文件） |
| `--validate` | 根据 Agent Skills 标准验证导出内容 |

## 输出结构

```
.agent-skills/
├── architect/
│   └── SKILL.md
├── security/
│   └── SKILL.md
├── qa-lead/
│   └── SKILL.md
└── pm/
    └── SKILL.md
```

## 字段映射

| SpecWeave 字段 | Agent Skills 字段 | 备注 |
|-----------------|-------------------|-------|
| `name` | `name` | 直接映射 |
| `description` | `description` | 直接映射（长度限制为 1024 个字符） |
| `allowed-tools` | `allowed-tools` | 将逗号分隔的列表转换为空格分隔的列表 |
| N/A | `license` | 默认添加 `Apache-2.0` 许可证信息 |
| N/A | `compatibility` | 添加 `"Designed for Claude Code"` 说明 |
| N/A | `metadata.author` | 使用插件 manifest 的作者信息 |
| N/A | `metadata.source` | 添加 `"SpecWeave"` 说明 |
| `visibility` | （未映射） | Agent Skills 通过文件路径来识别技能 |
| `invocableBy` | （未映射） | Agent Skills 会自动识别技能的调用者 |

## 执行步骤

### 第一步：识别所有技能

```bash
# Find all SKILL.md files in plugins
find plugins -name "SKILL.md" -type f
```

### 第二步：转换每个技能

对于每个 `SKILL.md` 文件：
1. 解析 YAML 标头信息
2. 提取技能描述（如有需要，截断至 1024 个字符）
3. 将 `allowed-tools` 中的逗号分隔列表转换为空格分隔的列表
4. 生成符合 Agent Skills 格式的标头信息
5. 保留 Markdown 正文内容

### 第三步：验证导出结果

每个导出的技能必须满足以下条件：
- `name` 与输出目录的名称相同
- `description` 的长度在 1 到 1024 个字符之间
- `name` 仅包含字母（`a-z`）和连字符（`-`）
- `name` 中不能包含 `--` 字符
- `name` 不能以 `-` 开头或结尾

### 第四步：生成输出文件

将转换后的文件写入指定的输出目录，文件结构如下：
```
{output}/{skill-name}/SKILL.md
```

## 转换脚本

```typescript
interface SpecWeaveSkill {
  name: string;
  description: string;
  'allowed-tools'?: string;
  visibility?: string;
  invocableBy?: string[];
  context?: string;
  model?: string;
}

interface AgentSkill {
  name: string;
  description: string;
  license?: string;
  compatibility?: string;
  metadata?: Record<string, string>;
  'allowed-tools'?: string;
}

function convertSkill(specweave: SpecWeaveSkill, pluginName: string): AgentSkill {
  return {
    name: specweave.name,
    description: specweave.description.slice(0, 1024),
    license: 'Apache-2.0',
    compatibility: 'Designed for Claude Code (or similar products)',
    metadata: {
      author: 'specweave',
      source: 'SpecWeave',
      plugin: pluginName
    },
    'allowed-tools': specweave['allowed-tools']?.replace(/,\s*/g, ' ')
  };
}
```

## 示例输出

输入文件（`plugins/specweave/skills/architect/SKILL.md`）：
```yaml
---
name: architect
description: System Architect expert...
allowed-tools: Read, Write, Edit
context: fork
model: opus
---
```

输出文件（`.agent-skills/architect/SKILL.md`）：
```yaml
---
name: architect
description: System Architect expert...
license: Apache-2.0
compatibility: Designed for Claude Code (or similar products)
metadata:
  author: specweave
  source: SpecWeave
  plugin: sw
allowed-tools: Read Write Edit
---
```

## 导出后的操作

导出完成后：
1. **提交到仓库**：此时可以从任意子目录中访问这些技能。
2. **推送到 GitHub**：启用 GitHub Copilot 的技能识别功能。
3. **发布**：可以考虑将这些技能发布到技能注册平台。

## 限制事项
- SpecWeave 特有的字段（`context`、`model`、`invocableBy`）不会被导出。
- 分阶段的技能信息（子文件）不会被包含在内。
- 技能的运行时状态数据（内存文件）不会被导出。
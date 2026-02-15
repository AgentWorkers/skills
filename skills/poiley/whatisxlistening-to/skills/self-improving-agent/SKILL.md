---
name: self-improvement
description: "记录学习内容、错误以及相应的修正措施，以实现持续改进。适用场景包括：  
(1) 命令或操作出现意外失败；  
(2) 用户对Claude的回答提出纠正（例如：“不，那不对……”或“实际上……”）；  
(3) 用户请求的功能并不存在；  
(4) 外部API或工具出现故障；  
(5) Claude意识到自己的知识已经过时或不准确；  
(6) 对于重复性任务发现了更优的处理方法。  
此外，在执行重要任务之前，也应回顾这些学习记录。"
---

# 自我提升技能

将学习内容及遇到的错误记录到 markdown 文件中，以实现持续改进。编码助手可以后续将这些记录转化为修复方案，而重要的学习内容会被纳入项目知识库中。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正了你 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `correction` 类别 |
| 用户提出功能需求 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `knowledge_gap` 类别 |
| 找到了更好的方法 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `best_practice` 类别 |
| 与现有条目相似 | 添加 `**另请参阅** 链接；考虑提升优先级 |
| 具有普遍适用性的知识 | 将其纳入 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md` |

## 设置

如果项目根目录下不存在 `.learnings/` 目录，请创建该目录：

```bash
mkdir -p .learnings
```

从 `assets/` 目录复制模板，或创建带有头部信息的文件。

## 记录格式

### 学习记录

追加到 `.learnings/LEARNINGS.md`：

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Specific fix or improvement to make

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related to existing entry)

---
```

### 错误记录

追加到 `.learnings/ERRORS.md`：

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
Brief description of what failed

### Error
```
实际错误信息或输出结果
```

### Context
- Command/operation attempted
- Input or parameters used
- Environment details if relevant

### Suggested Fix
If identifiable, what might resolve this

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
- See Also: ERR-20250110-001 (if recurring)

---
```

### 功能需求记录

追加到 `.learnings/FEATURE_REQUESTS.md`：

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Requested Capability
What the user wanted to do

### User Context
Why they needed it, what problem they're solving

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built, what it might extend

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_feature_name

---
```

## ID 生成格式

格式：`TYPE-YYYYMMDD-XXX`
- `TYPE`：`LRN`（学习内容）、`ERR`（错误）、`FEAT`（功能需求）
- `YYYYMMDD`：当前日期
- `XXX`：序列号或随机生成的 3 个字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 解决记录

当问题得到解决时，更新相关记录：

1. 将 `**状态** 更改为 `pending` → `resolved`
2. 在元数据后添加解决步骤：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

其他状态值：
- `in_progress`：正在处理中
- `wont_fix`：决定不解决（在解决说明中说明原因）
- `promoted`：提升到 `CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

## 提升到项目知识库

当某项学习内容具有普遍适用性（而非一次性修复问题）时，将其纳入项目知识库：

### 何时提升

- 该学习内容适用于多个文件或功能
- 所有贡献者（无论是人类还是 AI）都应了解这些知识
- 可防止重复出现类似问题
- 可用于记录项目特定的规范

### 提升目标文件

| 目标文件 | 应记录的内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目事实、所有 Claude 用户需要了解的规范和注意事项 |
| `AGENTS.md` | 与特定助手相关的工作流程、工具使用方法、自动化规则 |
| `.github/copilot-instructions.md` | 适用于 GitHub Copilot 的项目背景和规范 |

### 提升方法

1. 将学习内容提炼成简洁的规则或事实
2. 添加到目标文件对应的章节中（如需要可创建新文件）
3. 更新原始记录：
   - 将 `**状态** 更改为 `pending` → `promoted`
   - 添加 `**Promoted**: CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

### 提升示例

**学习内容（详细）**：
> 项目使用 pnpm 工作区。尝试执行 `npm install` 但失败。
> 锁定文件为 `pnpm-lock.yaml`，必须使用 `pnpm install`。

**在 CLAUDE.md 中（简洁）**：
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习内容（详细）**：
> 修改 API 端点后，必须重新生成 TypeScript 客户端。
> 忘记这一点会导致运行时类型不匹配。

**在 AGENTS.md 中（可操作）**：
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复性问题的检测

如果记录的内容与现有条目相似：

1. **先搜索**：`grep -r "关键词" .learnings/`
2. **添加链接**：在元数据中添加 `**另请参阅**：ERR-20250110-001`
3. **如果问题持续出现**，提升优先级
4. **考虑系统性解决方案**：重复出现的问题通常表明：
   - 缺乏文档（→ 提升到 CLAUDE.md 或 `.github/copilot-instructions.md`）
   - 缺乏自动化处理（→ 添加到 AGENTS.md）
   - 存在架构问题（→ 创建技术债务工单）

## 定期审查

在合适的时机审查 `.learnings/` 文件：

### 审查时机
- 在开始新的大型任务之前
- 完成某个功能后
- 在处理之前有相关学习内容的领域时
- 在活跃的开发周期内每周进行一次

### 快速状态检查
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查步骤
- 解决已解决的问题
- 提升适用的学习内容
- 链接相关条目
- 升级重复出现的问题

## 检测触发条件

在以下情况下自动记录：

**纠正**（→ 标记为 `correction` 类别的学习内容）：
- “不，那不对……”
- “实际上应该是……”
- “你对……的理解有误……”
- “那已经过时了……”

**功能需求**（→ 标记为 `feature_request` 类别的内容）：
- “你能不能也……”
- “我希望你能……”
- “有没有办法……”
- “为什么不能……”

**知识缺口**（→ 标记为 `knowledge_gap` 类别的内容）：
- 用户提供了你不知道的信息
- 你参考的文档已经过时
- API 行为与你的理解不符

## 优先级指南

| 优先级 | 使用时机 |
|----------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响、影响常见工作流程或问题反复出现 |
| `medium` | 影响较小、有解决方法 |
| `low` | 仅造成轻微不便、属于边缘情况或可选内容 |

## 区域标签

用于按代码库区域过滤学习内容：

| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/持续部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README 文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践

1. **立即记录** – 问题发生后，上下文最为清晰
2. **具体说明** – 未来的助手需要快速理解问题
3. **包含重现步骤** – 尤其对错误记录尤为重要
4. **链接相关文件** – 便于后续修复
5. **提出具体的解决方案** – 而不仅仅是“进行调查”
6. **使用统一的分类** – 便于筛选
7. **积极提升** – 如果有疑问，将其添加到 CLAUDE.md 或 `.github/copilot-instructions.md`
8. **定期审查** – 过时的学习内容会失去价值

## Git 忽略选项

**将学习内容保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要将学习内容添加到 `.gitignore` 文件中，这样它们才能成为共享知识。

**混合方式**（跟踪模板，忽略具体条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 钩子集成

通过助手钩子实现自动提醒。这是 **可选** 的功能——你需要明确配置钩子。

### 快速设置（Claude Code / Codex）

在项目中创建 `.claude/settings.json` 文件：

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }]
  }
}
```

这会在每次提示后自动触发学习内容评估提醒（大约增加 50-100 个字符的处理开销）。

### 完整设置（包含错误检测）

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improvement/scripts/error-detector.sh"
      }]
    }]
  }
}
```

### 可用的钩子脚本

| 脚本 | 钩子类型 | 用途 |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | 任务完成后提醒评估学习内容 |
| `scripts/error-detector.sh` | PostToolUse（Bash） | 在命令执行失败时触发检测 |

详细配置和故障排除方法请参考 `references/hooks-setup.md`。

## 自动提取技能

当某项学习内容具有足够的价值，可以提取为可复用的技能时，可以使用提供的辅助工具进行提取。

### 技能提取标准

当满足以下任意一项标准时，该学习内容即可被提取为技能：

| 标准 | 描述 |
|-----------|-------------|
| **重复性** | 有 2 个或更多类似问题的 `See Also` 链接 |
| **已验证** | 状态为 `resolved` 且已有有效的修复方案 |
| **非显而易见** | 需要实际调试或调查才能发现 |
| **普遍适用** | 不仅适用于当前项目，也适用于其他代码库 |
| **用户标记** | 用户表示“将此内容保存为技能”或类似提示 |

### 提取流程

1. **识别候选内容**：学习内容符合提取标准
2. **运行辅助工具**（或手动执行）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义 SKILL.md**：使用模板填写学习内容
4. **更新学习记录**：将状态设置为 `promoted_to_skill`，并添加 `Skill-Path`
5. **验证**：在新会话中重新阅读该技能内容，确保其完整性

### 手动提取

如果你更喜欢手动提取：

1. 创建 `skills/<skill-name>/SKILL.md` 文件
2. 使用 `assets/SKILL-TEMPLATE.md` 模板
3. 遵循 [Agent Skills 规范](https://agentskills.io/specification)：
   - 使用 YAML 格式编写文件头，包含 `name` 和 `description`
   - 文件名必须与文件夹名一致
   - 技能文件夹内不得包含 README.md 文件

### 提取触发条件

当出现以下情况时，表明该学习内容适合被提取为技能：

**在对话中**：
- “将此内容保存为技能”
- “我经常遇到这个问题”
- “这对其他项目也有帮助”
- “记住这个解决方案”

**在学习记录中**：
- 多个 `See Also` 链接（问题反复出现）
- 优先级高且状态为 `resolved`
- 类别为 `best_practice` 且具有普遍适用性
- 用户反馈表示该解决方案很有用

### 技能质量检查

在提取之前，请确认：

- [ ] 解决方案已经过测试且可以正常使用
- [ ] 描述清晰，无需依赖原始上下文
- **代码示例** 是独立的
- **没有项目特定的硬编码值**
- **遵循技能命名规范**（使用小写字母和连字符）

## 多助手支持

该技能支持不同的 AI 编码助手，具体激活方式取决于助手类型。

### Claude Code

**激活方式**：通过钩子（UserPromptSubmit、PostToolUse）
**设置方式**：配置 `.claude/settings.json` 文件中的钩子
**检测方式**：通过钩子脚本自动检测

### Codex CLI

**激活方式**：通过钩子（与 Claude Code 类似）
**设置方式**：配置 `.codex/settings.json` 文件中的钩子
**检测方式**：通过钩子脚本自动检测

### GitHub Copilot

**激活方式**：手动操作（不支持钩子）
**设置方式**：将相关内容添加到 `.github/copilot-instructions.md` 文件中：

```markdown
## Self-Improvement

After solving non-obvious issues, consider logging to `.learnings/`:
1. Use format from self-improvement skill
2. Link related entries with See Also
3. Promote high-value learnings to skills

Ask in chat: "Should I log this as a learning?"
```

**检测方式**：在会话结束时手动检查

### 与助手无关的指导原则

无论使用哪种助手，当你遇到以下情况时，都应进行自我提升：

1. **发现不显而易见的问题** – 解决方案不是立即显而易见的
2. **纠正自己的错误** – 初始方法有误
3. **了解项目规范** – 发现未记录的规则
4. **遇到意外错误** – 尤其是诊断困难时
5. **找到更好的解决方案** – 对原有解决方案进行了改进

### Copilot 聊天集成

对于 Copilot 用户，可以在相关提示中添加以下内容：

> 完成此任务后，使用自我提升功能将相关学习内容记录到 `.learnings/` 文件中。

或者使用快速提示：
- “将此内容记录到学习记录中”
- “从这个解决方案中提取一个技能”
- “查看 `.learnings/` 文件中是否有相关问题”
---
name: self-improvement-abc
description: "记录学习内容、错误以及相应的修正措施，以促进持续改进。适用场景包括：  
(1) 命令或操作出现意外失败；  
(2) 用户对Claude的回答提出纠正（例如：“不，那不对……”或“实际上……”）；  
(3) 用户请求的功能并不存在；  
(4) 外部API或工具出现故障；  
(5) Claude意识到自己的知识已经过时或不准确；  
(6) 对于重复性任务发现了更优的解决方法。  
此外，在执行重要任务之前，也应回顾这些学习记录。"
metadata:
---
# 自我提升技能

将学习内容及遇到的错误记录到 markdown 文件中，以实现持续改进。编码助手可以后续将这些记录处理成修复方案，而重要的学习内容则会被纳入项目知识库中。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正了你 | 记录到 `.learnings/LEARNINGS.md`，并标注类别为 `correction` |
| 用户请求新增功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，并标注类别为 `knowledge_gap` |
| 找到更好的方法 | 记录到 `.learnings/LEARNINGS.md`，并标注类别为 `best_practice` |
| 简化/优化重复出现的模式 | 记录/更新 `.learnings/LEARNINGS.md`，并标注 `Source: simplify-and-harden` 以及一个唯一的 `Pattern-Key` |
| 与现有条目相似 | 添加 `**参见** 链接；根据情况调整优先级 |
| 具有普遍适用性的学习内容 | 提升到 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md` |
| 工作流程改进 | 提升到 `AGENTS.md`（OpenClaw 工作区） |
| 工具使用技巧 | 提升到 `TOOLS.md`（OpenClaw 工作区） |
| 行为模式 | 提升到 `SOUL.md`（OpenClaw 工作区） |

## OpenClaw 设置（推荐）

OpenClaw 是实现此技能的主要平台。它采用基于工作区的提示注入机制，并能自动加载相关技能。

### 安装

**通过 ClawdHub（推荐）：**
```bash
clawdhub install self-improving-agent
```

**手动安装：**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

从原始仓库重新制作适用于 OpenClaw 的版本：  
https://github.com/pskoett/pskoett-ai-skills  
https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### 工作区结构

OpenClaw 会在每次会话中自动加载这些文件：

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows, delegation patterns
├── SOUL.md            # Behavioral guidelines, personality, principles
├── TOOLS.md           # Tool capabilities, integration gotchas
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── ERRORS.md
    └── FEATURE_REQUESTS.md
```

### 创建学习记录文件

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

然后创建相应的日志文件（或从 `assets/` 目录复制）：
- `LEARNINGS.md` — 用于记录纠正措施、知识缺口和最佳实践
- `ERRORS.md` — 用于记录命令失败和异常情况
- `FEATURE_REQUESTS.md` — 用于记录用户请求的功能

### 提升规则

当某些学习内容具有普遍适用性时，将其提升到相应的工作区文件中：

| 学习类型 | 提升到 | 例子 |
|---------------|------------|---------|
| 行为模式 | `SOUL.md` | “表达要简洁，避免使用免责声明” |
| 工作流程改进 | `AGENTS.md` | “为长时间运行的任务创建子助手” |
| 工具使用技巧 | `TOOLS.md` | “使用 Git 推送前需要配置身份验证” |

### 会话间通信

OpenClaw 提供了跨会话共享学习内容的工具：
- **sessions_list** — 查看当前/最近的会话记录
- **sessions_history** — 读取其他会话的文字记录
- **sessions_send** — 将学习内容发送到其他会话
- **sessions_spawn** — 为后台任务创建子助手

### 可选：启用提醒功能

为了在会话开始时自动提醒用户，请启用以下设置：
```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# Enable it
openclaw hooks enable self-improvement
```

详细信息请参阅 `references/openclaw-integration.md`。

---

## 其他代理的通用设置

对于 Claude Code、Codex、Copilot 或其他代理，需要在项目中创建 `.learnings/` 目录：

```bash
mkdir -p .learnings
```

可以从 `assets/` 目录复制模板，或根据需要创建新文件。

### 提醒自己记录学习内容的参考文件

为了提醒自己记录学习内容，可以添加对 `AGENTS.md`、`CLAUDE.md` 或 `.github/copilot-instructions.md` 的引用。（这可以作为基于钩子的提醒方式的替代方案）

#### 自我提升工作流程

当出现错误或需要纠正时：
1. 将相关内容记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md` 中。
2. 审查那些具有普遍适用性的学习内容，并将其提升到以下文件中：
   - `CLAUDE.md` — 项目相关的事实和惯例
   - `AGENTS.md` — 工作流程和自动化相关内容
   - `.github/copilot-instructions.md` — Copilot 使用的相关指导

## 日志记录格式

### 学习记录的添加方式

将学习内容添加到 `.learnings/LEARNINGS.md` 文件中：

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
- Pattern-Key: simplify.dead_code | harden.input_validation (optional, for recurring-pattern tracking)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

### 错误记录的添加方式

将错误信息添加到 `.learnings/ERRORS.md` 文件中：

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

### 功能请求的添加方式

将功能请求记录添加到 `.learnings/FEATURE_REQUESTS.md` 文件中：

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

## 编号规则

编号格式：`TYPE-YYYYMMDD-XXX`
- `TYPE`：`LRN`（学习内容）、`ERR`（错误）、`FEAT`（功能请求）
- `YYYYMMDD`：当前日期
- `XXX`：顺序编号或随机生成的 3 个字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 问题解决

当问题得到解决时，更新记录：
1. 将状态从 `pending` 更改为 `resolved`。
2. 在元数据后添加问题解决的相关信息：

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

当某些学习内容具有普遍适用性（不是临时性的问题）时，将其提升到项目知识库中。

### 提升时机
- 当学习内容适用于多个文件或功能时
- 当该知识对任何贡献者（无论是人类还是 AI）都重要时
- 当可以防止重复出现错误时
- 当该知识能帮助记录项目特定的惯例时

### 提升目标文件
| 目标文件 | 提升内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目相关的事实、惯例以及所有 Claude 交互中的注意事项 |
| `AGENTS.md` | 代理特定的工作流程、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目相关内容和惯例 |
| `SOUL.md` | 行为准则、沟通风格、原则（OpenClaw 工作区） |
| `TOOLS.md` | 工具的功能、使用模式、集成注意事项（OpenClaw 工作区） |

### 提升方法
1. 将学习内容提炼成简洁的规则或事实。
2. 将其添加到目标文件中的相应部分（如需要可创建新文件）。
3. 更新原始记录：
   - 将状态从 `pending` 更改为 `promoted`。
   - 添加 `Promoted` 标注，指明提升到的文件。

### 提升示例

**学习内容（详细记录）：**
> 项目使用 pnpm 工作区，尝试使用 `npm install` 但失败了。
> 锁定文件是 `pnpm-lock.yaml`，应使用 `pnpm install`。

**在 CLAUDE.md 中（简洁记录）：**
> 修改 API 端点后，必须重新生成 TypeScript 客户端。
> 忘记这一点会导致运行时类型不匹配。

**在 AGENTS.md 中（可操作的建议）：**
> ...

## 重复模式的检测

如果记录的内容与现有条目相似：
1. **先搜索**：`grep -r "关键词" .learnings/`
2. **添加链接**：在元数据中添加 `**参见**：ERR-20250110-001`
3. **如果问题持续出现**，提升优先级。
4. **考虑系统性解决方案**：重复出现的问题通常表明：
   - 缺少文档（→ 提升到 CLAUDE.md 或 `.github/copilot-instructions.md`）
   - 缺少自动化机制（→ 添加到 AGENTS.md）
   - 存在架构问题（→ 创建技术债务工单）

## 简化与优化流程

使用这个流程，将来自 `simplify-and-harden` 技能的重复模式转化为可持续的提示指导。

### 数据摄入流程
1. 从任务摘要中读取 `simplify_and_harden.learning_loop.candidates`。
2. 对于每个候选内容，使用 `pattern_key` 作为唯一标识符。
3. 在 `.learnings/LEARNINGS.md` 中搜索是否存在相同的条目：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 如果找到相同条目：
   - 增加 `Recurrence-Count`（重复次数）
   - 更新 `Last-Seen`（最后查看时间）
   - 添加 `See Also` 链接到相关条目/任务。
5. 如果没有找到相同条目：
   - 创建一个新的 `LRN-...` 条目
   - 设置 `Source: simplify-and-harden`
   - 设置 `Pattern-Key`、`Recurrence-Count` 和 `First-Seen`/`Last-Seen`。

### 提升规则（系统提示）

当满足以下条件时，将重复模式提升到代理上下文/系统提示文件中：
- `Recurrence-Count` 大于或等于 3
- 至少在 2 个不同的任务中出现
- 在 30 天内发生过

提升目标文件：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md`（适用于 OpenClaw 工作区）

提升后的规则应简洁明了，说明在编码前/期间应采取的措施。

## 定期审查

在以下时间点定期审查 `.learnings/` 文件：
- 在开始新任务之前
- 完成某个功能后
- 在处理之前有相关学习内容的领域工作时
- 在活跃的开发周期内每周进行一次

## 快速状态检查
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查动作
- 解决已解决的问题
- 提升具有适用性的学习内容
- 链接相关条目
- 升级重复出现的问题

## 触发条件

在以下情况下自动记录：
**纠正**（记录时标注类别为 `correction`）：
- “不对……”
- “实际上应该是……”
- “你的理解有误……”
- “这已经过时了……”

**功能请求**（记录时标注类别为 `feature_request`）：
- “你能不能也……”
- “有没有办法……”
- “为什么不能……”

**知识缺口**（记录时标注类别为 `knowledge_gap`）：
- 用户提供了你不知道的信息
- 你参考的文档已经过时
- API 行为与你的理解不一致

## 优先级指南

| 优先级 | 使用时机 |
|----------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响，影响常见工作流程或问题反复出现 |
| `medium` | 影响较小，但有解决方法 |
| `low` | 仅造成轻微不便，属于边缘情况 |

## 区域标签

使用这些标签按代码库区域过滤学习内容：
| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README 文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践
1. **立即记录** — 问题发生后，上下文信息最为清晰。
2. **具体说明** — 未来的助手需要快速理解问题。
3. **包含重现步骤** — 尤其对错误记录尤为重要。
4. **提供具体解决方案** — 而不仅仅是“进行调查”。
5. **使用统一的分类** — 便于后续筛选。
6. **积极提升** — 如果有疑问，将其添加到 CLAUDE.md 或 `.github/copilot-instructions.md`。
7. **定期审查** — 过时的学习内容会失去价值。

## Git 忽略选项

**将学习内容保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要将学习内容添加到 `.gitignore` 文件中，这样它们才能成为共享知识。

**混合方式**（同时跟踪模板和忽略某些条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 钩子集成

通过代理钩子启用自动提醒功能。这是可选的——你需要明确配置钩子。

### Claude Code / Codex 的快速设置

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

这样可以在每次提示后自动触发学习内容评估提醒（大约增加 50-100 个处理开销）。

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
| `scripts/activator.sh` | UserPromptSubmit | 在任务完成后提醒评估学习内容 |
| `scripts/error-detector.sh` | PostToolUse（Bash） | 在命令出错时触发提醒 |

详细配置和故障排除方法请参阅 `references/hooks-setup.md`。

## 自动提取学习内容

当某个学习内容具有足够的价值，可以将其提取为可复用的技能时，可以使用提供的辅助工具进行提取。

### 技能提取标准

当满足以下任意一条标准时，该学习内容即可被提取为技能：
- **重复出现**：有 2 个或更多相似问题的 `See Also` 链接。
- **已验证**：状态为 `resolved`，且问题已得到解决。
- **不易发现**：需要实际进行调试或调查才能发现。
- **具有普遍适用性**：不局限于某个项目，适用于多个代码库。
- **用户标记**：用户表示“将此内容保存为技能”。

### 提取流程
1. **识别符合条件的内容**：该学习内容符合提取标准。
2. **运行辅助工具**（或手动执行）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义 SKILL.md` 文件**：使用模板填写学习内容。
4. **更新学习记录**：将状态设置为 `promoted_to_skill`，并添加 `Skill-Path`。
5. **验证**：在新的会话中验证该技能内容的完整性。

### 手动提取

如果喜欢手动提取，可以按照以下步骤操作：
1. 创建 `skills/<skill-name>/SKILL.md` 文件。
2. 使用 `assets/SKILL-TEMPLATE.md` 模板。
3. 遵循 [Agent Skills 规范](https://agentskills.io/specification)：
   - 使用 YAML 格式编写文件头，包含 `name` 和 `description`。
   - 文件名必须与文件夹名一致。
   - 技能文件夹内不得包含 `README.md` 文件。

### 提取触发条件

当出现以下情况时，说明该学习内容适合被提取为技能：
- 在对话中有人建议“将此内容保存为技能”。
- 用户经常遇到类似问题。
- 该内容对其他项目也有用。
- 用户反馈表示该内容很有用。

### 技能质量检查

在提取之前，请确保：
- 解决方案已经过测试并且可以正常使用。
- 描述清晰，无需依赖原始上下文。
- 代码示例是独立的。
- 不包含项目特定的硬编码值。
- 遵循技能命名规范（使用小写字母和连字符）。

## 多代理支持

此技能适用于不同的 AI 编码代理，并支持根据代理类型进行激活：

### Claude Code
**激活方式**：使用钩子（UserPromptSubmit、PostToolUse）
**设置方式**：配置 `.claude/settings.json` 文件中的钩子。
**检测方式**：通过钩子脚本自动检测。

### Codex CLI
**激活方式**：使用钩子（与 Claude Code 相同）
**设置方式**：配置 `.codex/settings.json` 文件中的钩子。
**检测方式**：通过钩子脚本自动检测。

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

**检测方式**：在会话结束时手动检查。

### OpenClaw
**激活方式**：通过工作区注入和代理间通信实现。
**设置方式**：参见上面的 “OpenClaw 设置” 部分。
**检测方式**：通过会话工具和工作区文件进行检测。

### 无论使用哪种代理，都可以应用自我提升机制

无论使用哪种 AI 编码代理，只要遇到以下情况，都可以进行自我提升：
- 发现不易理解的问题。
- 自我纠正（初始方法有误）。
- 了解项目惯例。
- 遇到未记录的错误。
- 找到更好的解决方案。

### Copilot 聊天集成

对于 Copilot 用户，可以在相关提示中添加以下内容：
> 完成任务后，评估是否需要将学习内容记录到 `.learnings/` 文件中。

或者使用快速提示：
- “将这些内容记录到学习记录中”。
- “从这个解决方案中创建一个技能”。
- “查看 `.learnings/` 中的相关问题”。
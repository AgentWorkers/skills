---
name: self-improvement
description: "记录学习内容、遇到的错误以及相应的修正措施，以促进持续改进。适用场景包括：  
(1) 命令或操作出现意外失败；  
(2) 用户对Claude的回答提出纠正（例如：“不，那不对……”或“实际上……”）；  
(3) 用户请求的功能并不存在；  
(4) 外部API或工具出现故障；  
(5) Claude意识到自己的知识已经过时或不准确；  
(6) 对于重复性任务发现了更优的处理方法。  
此外，在执行重要任务之前，也请回顾这些学习记录。"
metadata:
  openclaw:
    requires:
      env:
        - CLAUDE_TOOL_OUTPUT
---
# 自我提升技能

将学习内容和错误记录到 markdown 文件中，以实现持续改进。编码代理可以后续处理这些记录，将重要的学习内容纳入项目知识库。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正了你 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `correction` 类别 |
| 用户请求添加新功能 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到 `.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `knowledge_gap` 类别 |
| 找到更好的方法 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `best_practice` 类别 |
| 简化/固化重复出现的模式 | 记录/更新 `.learnings/LEARNINGS.md`，并注明 `Source: simplify-and-harden` 以及对应的 `Pattern-Key` |
| 与现有条目相似 | 添加 `**另请参阅** 链接；根据需要提升优先级 |
| 具有普遍适用性的学习内容 | 将其纳入 `CLAUDE.md`、`AGENTS.md` 和/或 `.github/copilot-instructions.md` |
| 工作流程改进 | 将其纳入 `AGENTS.md`（OpenClaw 工作区） |
| 工具使用技巧 | 将其纳入 `TOOLS.md`（OpenClaw 工作区） |
| 行为模式 | 将其纳入 `SOUL.md`（OpenClaw 工作区） |

## OpenClaw 设置（推荐）

OpenClaw 是实现此技能的主要平台。它使用基于工作区的提示注入功能，并能自动加载相关技能。

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

然后创建日志文件（或从 `assets/` 目录复制文件）：
- `LEARNINGS.md` — 用于记录纠正措施、知识缺口和最佳实践
- `ERRORS.md` — 用于记录命令失败和异常情况
- `FEATURE_REQUESTS.md` — 用于记录用户请求的功能

### 提升记录的适用范围

当学习内容具有普遍适用性时，将其提升到工作区文件中：

| 学习类型 | 提升到 | 例子 |
|---------------|------------|---------|
| 行为模式 | `SOUL.md` | “表达要简洁，避免使用免责声明” |
| 工作流程改进 | `AGENTS.md` | “为长时间运行的任务创建子代理” |
| 工具使用技巧 | `TOOLS.md` | “使用 Git 推送前需配置身份验证” |

### 会话间交流

OpenClaw 提供了跨会话分享学习内容的工具：
- **sessions_list** — 查看当前/最近的会话记录
- **sessions_history** — 读取其他会话的记录内容
- **sessions_send** — 将学习内容发送到其他会话
- **sessions_spawn** — 为后台任务创建子代理

### 可选：启用提醒功能

为了在会话开始时自动提醒用户：
```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# Enable it
openclaw hooks enable self-improvement
```

详细信息请参阅 `references/openclaw-integration.md`。

---

## 其他代理的通用设置

对于 Claude Code、Codex、Copilot 或其他代理，可以在项目中创建 `.learnings/` 目录：

```bash
mkdir -p .learnings
```

从 `assets/` 目录复制模板或创建新的文件。

### 提醒自己记录学习内容的参考文件

可以通过引用 `AGENTS.md`、`CLAUDE.md` 或 `.github/copilot-instructions.md` 来提醒自己记录学习内容（这是基于钩子提醒的替代方案）。

#### 自我提升工作流程

当出现错误或需要纠正时：
1. 将相关内容记录到 `.learnings/ERRORS.md`、`LEARNINGS.md` 或 `FEATURE_REQUESTS.md`。
2. 审查并将具有普遍适用性的学习内容提升到以下文件中：
   - `CLAUDE.md` — 项目事实和惯例
   - `AGENTS.md` — 工作流程和自动化流程
   - `.github/copilot-instructions.md` — Copilot 的使用指南

## 日志记录格式

### 学习记录的格式

将内容追加到 `.learnings/LEARNINGS.md` 文件中：

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

### 错误记录的格式

将内容追加到 `.learnings/ERRORS.md` 文件中：

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

### 功能请求的格式

将内容追加到 `.learnings/FEATURE_REQUESTS.md` 文件中：

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

格式：`TYPE-YYYYMMDD-XXX`
- `TYPE`：`LRN`（学习内容）、`ERR`（错误）、`FEAT`（功能请求）
- `YYYYMMDD`：当前日期
- `XXX`：顺序编号或随机生成的 3 个字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 解决问题后的处理

问题解决后，更新记录：
1. 将 `**状态** 更改为 `pending` → `resolved`。
2. 在元数据后添加解决方案说明：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

其他状态值：
- `in_progress`：正在处理中
- `wont_fix`：决定不解决（在解决方案说明中说明原因）
- `promoted`：提升到 `CLAUDE.md`、`AGENTS.md` 或 `.github/copilot-instructions.md`

## 提升到项目知识库

当学习内容具有普遍适用性（而非一次性问题）时，将其提升到项目知识库中。

### 提升的条件：
- 学习内容适用于多个文件或功能
- 所有贡献者（无论是人类还是 AI）都应该了解这些内容
- 能够防止重复出现类似问题
- 能够记录项目特定的惯例

### 提升的目标文件
| 目标文件 | 提升的内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目事实、所有 Claude 交互的惯例和注意事项 |
| `AGENTS.md` | 代理特定的工作流程、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目背景信息和惯例 |
| `SOUL.md` | 行为准则、沟通风格、原则（OpenClaw 工作区） |
| `TOOLS.md` | 工具功能、使用模式、集成注意事项（OpenClaw 工作区） |

### 提升方法：
1. 将学习内容提炼成简洁的规则或事实。
2. 将其添加到目标文件的相应部分（如有需要，可以创建新文件）。
3. 更新原始记录：
   - 将 `**状态** 更改为 `pending` → `promoted`。
   - 添加 `Promoted` 标记，表示内容已提升到相应的目标文件。

### 提升示例

**学习内容（详细记录）：**
> 项目使用 pnpm 工作区，尝试执行 `npm install` 但失败了。
> 锁定文件是 `pnpm-lock.yaml`，应使用 `pnpm install`。

**在 CLAUDE.md 中的简洁记录：**
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习内容（详细记录）：**
> 修改 API 端点时，必须重新生成 TypeScript 客户端代码。
> 如果忽略这一点，运行时会出现类型不匹配的问题。

**在 AGENTS.md 中的实用记录：**
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复模式的检测

如果记录的内容与现有条目相似：
1. **先搜索**：`grep -r "关键词" .learnings/`
2. **添加链接**：在元数据中添加 `**另请参阅**：`ERR-20250110-001`
3. **如果问题持续出现**，提升优先级。
4. **考虑系统性解决方案**：重复出现的问题通常表明：
   - 缺少文档（→ 提升到 `CLAUDE.md` 或 `.github/copilot-instructions.md`）
   - 缺少自动化处理（→ 添加到 `AGENTS.md`）
   - 存在架构问题（→ 创建技术债务工单）

## 简化与固化流程

使用此流程从 `simplify-and-harden` 技能中提取重复出现的模式，并将其转化为可靠的提示指导。

### 提取流程：
1. 从任务摘要中读取 `simplify_and_harden.learning_loop.candidates`。
2. 使用 `pattern_key` 作为唯一标识符。
3. 在 `.learnings/LEARNINGS.md` 中搜索是否存在相同的记录：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/`
4. 如果找到记录：
   - 增加 `Recurrence-Count`（重复次数）。
   - 更新 `Last-Seen`（最后查看时间）。
   - 添加 `See Also` 链接到相关记录或任务。
5. 如果没有找到记录：
   - 创建新的 `LRN-...` 条目。
   - 设置 `Source: simplify-and-harden`。
   - 设置 `Pattern-Key`、`Recurrence-Count` 和 `First-Seen`/`Last-Seen`。

### 提升规则（系统提示）

当满足以下条件时，将重复出现的模式提升到代理上下文/系统提示文件中：
- `Recurrence-Count` ≥ 3
- 至少在 2 个不同的任务中出现
- 在 30 天内发生过

提升的目标文件：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md`（适用于 OpenClaw 工作区）

提升后的规则应简洁明了（说明在编码前/过程中应采取的措施），而非冗长的问题描述。

## 定期审查

在以下时机定期审查 `.learnings/` 文件：
- 在开始新任务之前
- 完成某个功能后
- 在处理之前有相关学习内容的领域工作时
- 在开发活跃期间每周进行一次

### 快速状态检查
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查内容：
- 解决已解决的问题
- 提升具有适用性的学习内容
- 链接相关记录
- 升级重复出现的问题

## 触发审查的条件

当出现以下情况时，系统会自动记录：
**纠正措施**（记录标记为 `correction`）：
- “不对……”
- “实际上应该是……”
- “你的理解有误……”
- “这个信息已经过时了……”

**功能请求**（记录标记为 `feature_request`）：
- “你能不能……”
- “我希望你能……”
- “有没有办法……”
- “为什么不能……”

**知识缺口**（记录标记为 `knowledge_gap`）：
- 用户提供了你不知道的信息
- 你参考的文档已经过时
- API 的行为与你的理解不一致

## 优先级指南

| 优先级 | 使用时机 |
|----------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响，影响常见工作流程或问题反复出现 |
| `medium` | 影响较小，但有解决方法 |
| `low` | 仅造成轻微不便，属于边缘情况 |

## 区域标签

使用区域标签按代码库范围过滤学习内容：
| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/持续部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README 文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践：
1. **立即记录** — 问题发生时上下文最为清晰。
2. **具体说明** — 未来的代理需要快速理解问题。
3. **包含重现步骤** — 尤其对于错误记录。
4. **提供具体解决方案** — 而不仅仅是“进行调查”。
5. **使用统一的分类** — 便于查找相关内容。
6. **积极提升** — 如果不确定，将记录内容添加到 `CLAUDE.md` 或 `.github/copilot-instructions.md`。
7. **定期审查** — 过时的学习内容会失去价值。

## Git 忽略选项

**将学习内容保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要将学习内容添加到 `.gitignore` 文件中，这样它们才能成为共享知识。

**混合方式**（同时跟踪和忽略某些记录）：
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

这会在每次提示后触发学习内容评估提醒（大约增加 50-100 个处理开销）。

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

### 提取规则

满足以下任意一条条件的学习内容即可被提取为技能：
- **重复出现**：有 2 个或更多类似问题的 `See Also` 链接。
- **已验证**：状态为 `resolved`，并且有有效的解决方案。
- **不易发现**：需要实际调试或调查才能发现。
- **具有普遍适用性**：不针对特定项目，适用于多个代码库。
- **用户标记**：用户表示“将此内容保存为技能”。

### 提取流程：
1. **识别符合条件的记录**。
2. **运行辅助工具**（或手动执行）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义 SKILL.md**：使用模板填写学习内容。
4. **更新记录**：将状态设置为 `promoted_to_skill`，并添加 `Skill-Path`。
5. **验证**：在新会话中验证该技能内容的完整性。

### 手动提取

如果喜欢手动提取，可以按照以下步骤操作：
1. 创建 `skills/<skill-name>/SKILL.md` 文件。
2. 使用 `assets/SKILL-TEMPLATE.md` 模板。
3. 遵循 [Agent Skills 规范](https://agentskills.io/specification)：
   - 使用 YAML 格式编写文件头，包含 `name` 和 `description`。
   - 文件名必须与文件夹名一致。
   - 技能文件夹内不得包含 `README.md` 文件。

### 提取的触发条件：

当出现以下情况时，表示该内容适合被提取为技能：
- 在对话中提到“将此内容保存为技能”。
- 用户频繁遇到类似问题。
- 该内容对其他项目也有用。
- 用户表示“这个模式很有用”。

### 技能质量的评估标准：

在提取之前，请确保：
- [ ] 解决方案已经过测试并且可以正常使用。
- [ ] 描述清晰，无需依赖原始上下文。
- [ ] 代码示例完整且独立。
- [ ] 不包含项目特定的硬编码值。
- [ ] 遵循技能命名规范（使用小写和连字符）。

## 多代理支持

此技能适用于不同的 AI 编码代理，并且可以根据代理类型进行激活。

### Claude Code

**激活方式**：通过钩子（UserPromptSubmit、PostToolUse）。
**设置方式**：配置 `.claude/settings.json` 文件中的钩子。
**检测方式**：通过钩子脚本自动检测。

### Codex CLI

**激活方式**：通过钩子（与 Claude Code 相同）。
**设置方式**：配置 `.codex/settings.json` 文件中的钩子。
**检测方式**：通过钩子脚本自动检测。

### GitHub Copilot

**激活方式**：手动设置（不支持钩子）。
**设置方式**：将相关内容添加到 `.github/copilot-instructions.md` 文件中。

**检测方式**：在会话结束时手动检查。

### OpenClaw

**激活方式**：通过工作区注入和代理间通信实现。
**设置方式**：参见上述 “OpenClaw 设置” 部分。
**检测方式**：通过会话工具和工作区文件进行检测。

### 无需考虑代理类型的学习指导原则

无论使用哪种代理，当遇到以下情况时，都应进行自我提升：
- 发现不易理解的问题。
- 自己纠正了错误。
- 了解了项目惯例。
- 遇到未记录的错误。
- 找到了更好的解决方法。

### Copilot 聊天中的提示集成

对于 Copilot 用户，可以在相关提示中添加以下内容：
> 完成任务后，评估是否需要将学习内容记录到 `.learnings/` 文件中。

或者使用以下快捷提示：
- “将此内容记录到学习记录中。”
- “从这个解决方案中创建一个技能。”
- “查看 `.learnings/` 中的相关记录。”
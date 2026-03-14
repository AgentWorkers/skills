---
name: self-improvement-abc
description: "记录学习内容、遇到的错误以及相应的修正措施，以促进持续改进。适用场景包括：  
(1) 某个命令或操作意外失败时；  
(2) 用户对Claude的回答提出纠正（例如：“不，那不对……”或“实际上……”）；  
(3) 用户请求某个并不存在的功能；  
(4) 外部API或工具出现故障时；  
(5) Claude意识到自己的知识已经过时或不准确时；  
(6) 发现了处理重复性任务的更好方法时。  
此外，在执行重要任务之前，也请回顾这些学习记录。"
metadata:
---
# 自我提升技能

将学习内容和错误记录到Markdown文件中，以实现持续改进。编码代理可以后续将这些内容处理成修复方案，而重要的学习内容会被纳入项目知识库中。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 命令/操作失败 | 记录到`.learnings/ERRORS.md` |
| 用户纠正了你 | 记录到`.learnings/LEARNINGS.md`，并标记为`correction`类别 |
| 用户请求添加新功能 | 记录到`.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到`.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到`.learnings/LEARNINGS.md`，并标记为`knowledge_gap`类别 |
| 发现了更好的方法 | 记录到`.learnings/LEARNINGS.md`，并标记为`best_practice`类别 |
| 简化/优化重复出现的模式 | 记录到`.learnings/LEARNINGS.md`，并注明`Source: simplify-and-harden`以及对应的`Pattern-Key` |
| 与现有条目相似 | 添加`**另请参阅**链接；考虑提升优先级 |
| 具有普遍适用性的学习内容 | 提升到`CLAUDE.md`、`AGENTS.md`和/或`.github/copilot-instructions.md` |
| 工作流程改进 | 提升到`AGENTS.md`（OpenClaw工作区） |
| 工具使用技巧 | 提升到`TOOLS.md`（OpenClaw工作区） |
| 行为模式 | 提升到`SOUL.md`（OpenClaw工作区） |

## OpenClaw设置（推荐）

OpenClaw是实现这一技能的主要平台。它采用基于工作区的提示注入机制，并能自动加载相关技能。

### 安装

**通过ClawdHub（推荐）：**
```bash
clawdhub install self-improving-agent
```

**手动安装：**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

从原始仓库重新制作适用于OpenClaw的版本：  
https://github.com/pskoett/pskoett-ai-skills  
https://github.com/pskoett/pskoett-ai-skills/tree/main/skills/self-improvement

### 工作区结构

OpenClaw会在每次会话中自动加载这些文件：

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

然后创建日志文件（或从`assets/`目录复制文件）：
- `LEARNINGS.md` — 包含纠正措施、知识缺口和最佳实践
- `ERRORS.md` — 包含命令失败和异常信息
- `FEATURE_REQUESTS.md` — 包含用户请求的功能

### 提升目标

当某些学习内容具有普遍适用性时，将其提升到相应的工作区文件中：

| 学习类型 | 提升到 | 例子 |
|---------------|------------|---------|
| 行为模式 | `SOUL.md` | “表达要简洁，避免使用免责声明” |
| 工作流程改进 | `AGENTS.md` | “为耗时任务创建子代理” |
| 工具使用技巧 | `TOOLS.md` | “使用Git推送前需要配置认证” |

### 会话间通信

OpenClaw提供了跨会话分享学习内容的工具：
- **sessions_list** — 查看活跃/最近的会话 |
- **sessions_history** — 读取其他会话的记录 |
- **sessions_send** — 将学习内容发送到其他会话 |
- **sessions_spawn** — 为后台任务创建子代理

### 可选：启用提醒功能

为了在会话开始时自动提醒用户：
```bash
# Copy hook to OpenClaw hooks directory
cp -r hooks/openclaw ~/.openclaw/hooks/self-improvement

# Enable it
openclaw hooks enable self-improvement
```

详细信息请参阅`references/openclaw-integration.md`。

---

## 其他代理的通用设置

对于Claude Code、Codex、Copilot或其他代理，需要在项目中创建`.learnings/`目录：

```bash
mkdir -p .learnings
```

从`assets/`目录复制模板或创建新文件。

### 添加引用

引用`AGENTS.md`、`CLAUDE.md`或`.github/copilot-instructions.md`文件，以提醒自己记录学习内容。（这是基于钩子提醒的替代方案）

#### 自我提升工作流程

当出现错误或需要纠正时：
1. 记录到`.learnings/ERRORS.md`、`LEARNINGS.md`或`FEATURE_REQUESTS.md`
2. 审查并提升具有普遍适用性的学习内容到以下文件：
   - `CLAUDE.md` — 项目事实和规范
   - `AGENTS.md` — 工作流程和自动化流程
   - `.github/copilot-instructions.md` — Copilot使用指南

## 日志格式

### 学习记录条目

追加到`.learnings/LEARNINGS.md`中：

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

### 错误记录条目

追加到`.learnings/ERRORS.md`中：

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
实际错误信息或输出
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

### 功能请求条目

追加到`.learnings/FEATURE_REQUESTS.md`中：

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
- `XXX`：顺序编号或随机3个字符（例如`001`、`A7B`

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 解决问题后的处理

当问题得到解决时，更新记录条目：
1. 将`**状态**更改为`pending` → `resolved`
2. 在元数据后添加解决方案说明：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

其他状态值：
- `in_progress` — 正在处理中
- `wont_fix` — 决定不解决（在解决方案说明中说明原因）
- `promoted` — 提升到`CLAUDE.md`、`AGENTS.md`或`.github/copilot-instructions.md`

## 提升到项目知识库

当某些学习内容具有普遍适用性（不是一次性修复的结果）时，将其提升到项目的永久知识库中。

### 提升条件

- 学习内容适用于多个文件或功能
- 所有贡献者（无论是人类还是AI）都应该了解这些知识
- 可以防止重复出现的问题
- 能够记录项目特定的规范

### 提升目标

| 目标文件 | 应提升的内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目事实、所有Claude交互的注意事项 |
| `AGENTS.md` | 代理特定的工作流程、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot的项目背景信息和规范 |
| `SOUL.md` | 行为指南、沟通风格、原则（OpenClaw工作区） |
| `TOOLS.md` | 工具功能、使用模式、集成技巧（OpenClaw工作区） |

### 提升方法

1. 将学习内容提炼成简洁的规则或事实
2. 添加到目标文件的相关部分（如有需要可创建新文件）
3. 更新原始记录条目：
   - 将`**状态**更改为`pending` → `promoted`
   - 添加`**Promoted`：`CLAUDE.md`、`AGENTS.md`或`.github/copilot-instructions.md`

### 提升示例

**学习内容（详细）：**
> 项目使用pnpm工作区。尝试`npm install`但失败了。
> 锁定文件是`pnpm-lock.yaml`。必须使用`pnpm install`。

**在CLAUDE.md中（简洁表述）：**
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习内容（详细）：**
> 修改API端点后，需要重新生成TypeScript客户端。
> 如果忽略这一点，运行时会出现类型不匹配的问题。

**在AGENTS.md中（可操作的建议）：**
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复模式的检测

如果记录的内容与现有条目相似：
1. **先搜索**：`grep -r "关键词" .learnings/`
2. **添加引用**：在元数据中添加`**另请参阅**：ERR-20250110-001`
3. **如果问题持续出现**，提升优先级
4. **考虑系统性解决方案**：重复出现的问题通常表明：
   - 缺少文档（→ 提升到`CLAUDE.md`或`.github/copilot-instructions.md`
   - 缺少自动化机制（→ 添加到`AGENTS.md`
   - 存在架构问题（→ 创建技术债务工单）

## 简化与优化流程

使用以下流程，将`simplify-and-harden`技能中的重复模式转化为可持续的提示指南：

### 数据摄入流程

1. 从任务摘要中读取`simplify_and_harden.learning_loop.candidates`。
2. 对每个候选条目，使用`pattern_key`作为唯一的标识符。
3. 在`.learnings/LEARNINGS.md`中搜索是否存在相同的条目：
   - `grep -n "Pattern-Key: <pattern_key>" .learnings/LEARNINGS.md`
4. 如果找到：
   - 增加`Recurrence-Count`（重复次数）
   - 更新`Last-Seen`（最后查看时间）
   - 添加`See Also`链接到相关条目/任务
5. 如果没有找到：
   - 创建新的`LRN-...`条目
   - 设置`Source: simplify-and-harden`
   - 设置`Pattern-Key`、`Recurrence-Count`和`First-Seen`/`Last-Seen`

### 提升规则（系统提示）

当满足以下条件时，将重复模式提升到代理上下文/系统提示文件中：
- `Recurrence-Count` >= 3
- 至少出现在2个不同的任务中
- 在30天内发生过

提升目标：
- `CLAUDE.md`
- `AGENTS.md`
- `.github/copilot-instructions.md`
- `SOUL.md` / `TOOLS.md`（适用于OpenClaw工作区）

将提升后的规则编写为简短的预防性提示（编码前/中应执行的操作），而不是详细的事件描述。

## 定期审查

在以下时机定期审查`.learnings/`目录：
- 在开始新任务之前
- 完成某个功能后
- 在处理之前有相关学习内容的领域时
- 在开发活跃期间每周审查一次

### 快速状态检查
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
- 提升适用的学习内容
- 添加相关条目的链接
- 升级重复出现的问题

## 检测触发条件

当出现以下情况时，自动记录：
**纠正**（标记为`correction`类别）：
- “不，那不对……”
- “实际上应该是……”
- “你对……的理解有误……”
- “那已经过时了……”

**功能请求**（标记为`feature_request`类别）：
- “你能不能也……”
- “我希望你能……”
- “有没有办法……”
- “为什么不能……”

**知识缺口**（标记为`knowledge_gap`类别）：
- 用户提供了你不知道的信息
- 你参考的文档已经过时
- API的行为与你的理解不一致

## 优先级指南

| 优先级 | 使用时机 |
|----------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响，影响常见工作流程或问题重复出现 |
| `medium` | 影响较小，有解决方法 |
| `low` | 仅仅是小麻烦或边缘情况，属于可选内容 |

## 区域标签

使用这些标签按代码库区域过滤学习内容：
| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践

1. **立即记录** — 问题发生后，上下文最为清晰
2. **具体说明** — 未来的代理需要快速理解
3. **包含复现步骤** — 尤其对错误记录尤为重要
4. **提供具体解决方案** — 而不仅仅是“进行调查”
5. **使用统一的分类** — 便于筛选
6. **积极提升** — 如果有疑问，将其添加到`CLAUDE.md`或`.github/copilot-instructions.md`
7. **定期审查** — 过时的学习内容会失去价值

## Git忽略选项

**将学习内容保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要将学习内容添加到`.gitignore`中——这样它们才能成为共享知识。

**混合方式**（跟踪模板，忽略某些条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 启用提醒功能

通过代理钩子实现自动提醒。这是**可选**的——你需要明确配置钩子。

### Claude Code / Codex的快速设置

在项目中创建`.claude/settings.json`文件：

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

这会在每次提示后触发学习内容评估提醒（大约增加50-100个处理开销）。

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
| `scripts/error-detector.sh` | PostToolUse（Bash） | 在命令出错时触发 |

详细配置和故障排除方法请参阅`references/hooks-setup.md`。

## 自动提取技能

当某个学习内容具有足够的价值，可以被提取为可复用的技能时，使用提供的辅助工具进行提取。

### 技能提取标准

满足以下任意一条标准的学习内容即可被提取为技能：
- **重复出现**：有`See Also`链接指向2个或更多类似问题 |
- **已验证**：状态为`resolved`且已有有效的修复方案 |
- **不易发现**：需要实际调试或调查才能发现 |
- **具有普遍适用性**：不限于特定项目，适用于多个代码库 |
- **用户标记**：用户表示“将此内容保存为技能”

### 提取流程

1. **识别候选条目**：学习内容符合提取标准
2. **运行辅助工具**（或手动创建）：
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```
3. **自定义SKILL.md`文件**：填写学习内容
4. **更新学习记录**：将状态设置为`promoted_to_skill`，并添加`Skill-Path`
5. **验证**：在新会话中再次查看该技能内容，确保其内容完整

### 手动提取

如果你更喜欢手动提取：
1. 创建`skills/<skill-name>/SKILL.md`文件
2. 使用`assets/SKILL-TEMPLATE.md`模板
3. 遵循[Agent Skills规范](https://agentskills.io/specification)：
   - 使用YAML格式编写文件头，包含`name`和`description`
   - 文件名必须与文件夹名一致
   - 技能文件夹内不得包含`README.md`文件

### 提取触发条件

当出现以下情况时，表明某个学习内容应该被提取为技能：
- 在对话中提到“将此内容保存为技能”
- “我经常遇到这个问题”
- “这对其他项目也有用”
- “记住这个模式”

**在学习记录中**：
- 多个`See Also`链接（表明问题重复出现）
- 优先级高且状态为`resolved`
- 类别为`best_practice`且具有普遍适用性
- 用户反馈表示该解决方案很有用

### 技能质量检查

在提取之前，请确认：
- 解决方案已经过测试且可用
- 描述清晰，无需依赖原始上下文
- 代码示例完整
- 不包含项目特定的硬编码值
- 遵循技能命名规范（使用小写和连字符）

## 多代理支持

此技能适用于不同的AI编码代理，并支持针对特定代理的激活方式。

### Claude Code

**激活方式**：通过钩子（UserPromptSubmit、PostToolUse）
**设置方式**：配置`.claude/settings.json`文件
**检测方式**：通过钩子脚本自动检测

### Codex CLI

**激活方式**：通过钩子（与Claude Code相同）
**设置方式**：配置`.codex/settings.json`文件
**检测方式**：通过钩子脚本自动检测

### GitHub Copilot

**激活方式**：手动操作（不支持钩子）
**设置方式**：将相关内容添加到`.github/copilot-instructions.md`文件：

```markdown
## Self-Improvement

After solving non-obvious issues, consider logging to `.learnings/`:
1. Use format from self-improvement skill
2. Link related entries with See Also
3. Promote high-value learnings to skills

Ask in chat: "Should I log this as a learning?"
```

**检测方式**：在会话结束时手动检查

### OpenClaw

**激活方式**：通过工作区注入和代理间通信
**设置方式**：参见上述“OpenClaw设置”部分
**检测方式**：通过会话工具和工作区文件

### 无需区分代理的指导原则

无论使用哪种代理，当遇到以下情况时，都应进行自我提升：
- 发现不易理解的问题
- 自我纠正（初始方法错误）
- 了解项目规范
- 遇到意外错误（尤其是诊断困难时）
- 找到更好的解决方案

### Copilot聊天集成

对于Copilot用户，可以在相关提示中添加以下内容：
> 完成此任务后，评估是否需要将学习内容记录到`.learnings/`目录中。

或者使用快速提示：
- “将此内容记录到学习记录中”
- “根据这个解决方案创建一个技能”
- “查看`.learnings/`目录中的相关问题”
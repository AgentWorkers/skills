---

# 技能：知识提升代理（Knowledge Improvement Agent）
---

## 名称：agent_conhecimento
**描述：** 使用该代理来执行相关任务。

---

# 技能：知识提升代理（Knowledge Improvement Agent）
---
**名称：self-improvement**
**描述：** “记录学习内容、错误及修正措施，以实现持续改进。适用场景：**  
(1) 命令或操作意外失败；  
(2) 用户纠正Claude的回答（例如：“不，那不对...”或“实际上...”）；  
(3) 用户请求的功能不存在；  
(4) 外部API或工具出现故障；  
(5) Claude发现自己的知识过时或不准确；  
(6) 发现处理重复性任务的更好方法。  
**此外，在执行重要任务前也会回顾学习内容。”  

---

## 自我提升技能（Self-Improvement Skill）

将学习内容和错误记录到Markdown文件中，以便持续改进。编码代理可以后续将这些信息处理成修复方案，重要的学习内容会被纳入项目知识库。

## 快速参考

| 情况 | 应采取的行动 |
|---------|-------------------|
| 命令/操作失败 | 记录到`.learnings/ERRORS.md` |
| 用户纠正了你 | 记录到`.learnings/LEARNINGS.md`，并标记为`correction`类别 |
| 用户请求缺失的功能 | 记录到`.learnings/FEATURE_REQUESTS.md` |
| API/外部工具失败 | 记录到`.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到`.learnings/LEARNINGS.md`，并标记为`knowledge_gap`类别 |
| 发现了更好的方法 | 记录到`.learnings/LEARNINGS.md`，并标记为`best_practice`类别 |
| 与现有条目相似 | 添加`**另请参阅**链接，并考虑提升优先级 |
| 具有普遍适用性的学习内容 | 提升到`CLAUDE.md`、`AGENTS.md`和/或`.github/copilot-instructions.md` |
| 工作流程改进 | 提升到`AGENTS.md`（OpenClaw工作区） |
| 工具使用技巧 | 提升到`TOOLS.md`（OpenClaw工作区） |
| 行为模式 | 提升到`SOUL.md`（OpenClaw工作区） |

## OpenClaw设置（推荐）

OpenClaw是该技能的主要平台。它通过工作区注入提示来自动加载相关技能。

### 安装

**推荐方式（通过ClawdHub）：**
```bash
clawdhub install self-improving-agent
```

**手动安装：**
```bash
git clone https://github.com/peterskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

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

### 创建学习文件

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

然后创建日志文件（或从`assets/`目录复制）：
- `LEARNINGS.md` — 包含修正措施、知识缺口和最佳实践
- `ERRORS.md` — 包含命令失败和异常信息
- `FEATURE_REQUESTS.md` — 包含用户请求的功能

### 提升目标

当学习内容具有普遍适用性时，将其提升到工作区文件中：

| 学习类型 | 提升到 | 例子 |
|---------|------------|---------|
| 行为模式 | `SOUL.md` | “表达要简洁，避免使用免责声明” |
| 工作流程改进 | `AGENTS.md` | “为耗时任务创建子代理” |
| 工具使用技巧 | `TOOLS.md` | “Git推送需要先配置认证” |

### 会话间通信

OpenClaw提供了跨会话共享学习内容的工具：
- **sessions_list** — 查看活跃/最近的会话
- **sessions_history** — 读取其他会话的记录
- **sessions_send** — 向其他会话发送学习内容
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

对于Claude Code、Codex、Copilot或其他代理，在项目中创建`.learnings/`目录：

```bash
mkdir -p .learnings
```

可以从`assets/`目录复制模板或创建新的文件。

## 日志格式

### 学习记录

追加到`.learnings/LEARNINGS.md`：

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

追加到`.learnings/ERRORS.md`：

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

### 功能请求记录

追加到`.learnings/FEATURE_REQUESTS.md`：

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

## ID生成规则

格式：`TYPE-YYYYMMDD-XXX`  
- `TYPE`：`LRN`（学习内容）、`ERR`（错误）、`FEAT`（功能请求）  
- `YYYYMMDD`：当前日期  
- `XXX`：顺序编号或随机3个字符（例如`001`、`A7B`）  
示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 问题解决

问题解决后，更新记录：
1. 将`**状态**从`pending`更改为`**resolved`  
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
- `promoted`：提升到`CLAUDE.md`、`AGENTS.md`或`.github/copilot-instructions.md`

## 提升到项目知识库

当学习内容具有普遍适用性时（非一次性问题），将其提升到项目知识库中。

### 提升条件：
- 学习内容适用于多个文件或功能  
- 所有贡献者（人类或AI）都应了解这些知识  
- 可以防止重复出现的问题  
- 能够记录项目特定的规范

### 提升目标

| 目标文件 | 提升内容 |
|---------|-------------------|
| `CLAUDE.md` | 项目事实、通用规范、Claude交互中的注意事项 |
| `AGENTS.md` | 代理特定的工作流程、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot的项目背景和规范 |
| `SOUL.md` | 行为指南、沟通风格、原则（OpenClaw工作区） |
| `TOOLS.md` | 工具功能、使用模式、集成技巧（OpenClaw工作区） |

### 提升方法：
1. 将学习内容提炼成简洁的规则或事实  
2. 添加到目标文件的相关章节（如需创建新文件）  
3. 更新原始记录：  
   - 将`**状态**从`pending`更改为`promoted`  
   - 添加`**Promoted`字段，指定提升到的文件（如`CLAUDE.md`、`AGENTS.md`或`.github/copilot-instructions.md`）  

### 提升示例：

**学习内容（详细）：**
> 项目使用pnpm工作区，尝试`npm install`但失败。  
> 锁定文件为`pnpm-lock.yaml`，应使用`pnpm install`。

**在CLAUDE.md中（简洁版本）：**
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习内容（详细）：**
> 修改API端点时，必须重新生成TypeScript客户端。  
> 忘记这一点会导致运行时类型不匹配。

**在AGENTS.md中（可操作版本）：**
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复性问题的处理

如果记录的内容与现有条目相似：
1. **先搜索**：`grep -r "关键词" .learnings/`  
2. **添加链接**：在元数据中添加`**另请参阅**：`ERR-20250110-001`  
3. **如果问题反复出现**，提升优先级  
4. **考虑系统性解决方案**：重复出现的问题通常表明：  
   - 缺少文档（→ 提升到`CLAUDE.md`或`.github/copilot-instructions.md`）  
   - 缺少自动化脚本（→ 添加到`AGENTS.md`）  
   - 存在架构问题（→ 创建技术债务工单）

## 定期审查

在以下时间点定期审查`.learnings/`文件：
- 在开始新的大型任务之前  
- 完成某个功能后  
- 在处理之前有相关学习内容的领域时  
- 每周在开发过程中

## 快速状态检查
```bash
# Count pending items
grep -h "Status\*\*: pending" .learnings/*.md | wc -l

# List pending high-priority items
grep -B5 "Priority\*\*: high" .learnings/*.md | grep "^## \["

# Find learnings for a specific area
grep -l "Area\*\*: backend" .learnings/*.md
```

### 审查步骤：
- 解决已解决的问题  
- 提升适用的学习内容  
- 链接相关的记录  
- 升级重复出现的问题

## 触发条件

在以下情况下自动记录学习内容：
**修正措施**（标记为`correction`类别）：
- “不，那不对...”  
- “实际上，应该是...”  
- “你的理解有误...”  
- “那已经过时了...”  

**功能请求**（标记为`feature_request`类别）：
- “你能不能也...”  
- “我希望你能...”  
- “有没有办法...”  
- “为什么不行...”  

**知识缺口**（标记为`knowledge_gap`类别）：
- 用户提供了你不知道的信息  
- 你参考的文档已过时  
- API的行为与你的理解不符  

## 优先级指南

| 优先级 | 使用时机 |
|---------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响，影响常见工作流程或问题反复出现 |
| `medium` | 影响中等，有解决方法 |
| `low` | 仅造成轻微不便，属于边缘情况或可选功能 |

## 区域标签

使用这些标签按代码库区域过滤学习内容：
| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/持续部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践：
1. **立即记录**——问题发生后，上下文最为清晰  
2. **具体说明**——后续代理需要快速理解  
3. **包含重现步骤**——尤其是对于错误  
4. **链接相关文件**——便于修复  
5. **提供具体的解决方案**——而不仅仅是“进行调查”  
6. **使用统一的分类**——便于筛选  
7. **积极提升**——如有疑问，将其添加到`CLAUDE.md`或`.github/copilot-instructions.md`  
8. **定期审查**——过时的学习内容会失去价值  

## Git忽略选项

**将学习内容保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中跟踪学习内容**（团队范围）：
不要将学习内容添加到`.gitignore`文件中——这样学习内容将成为共享知识。

**混合方式**（同时跟踪模板和忽略某些记录）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## 提醒功能

通过代理钩子启用自动提醒。这是**可选**的——你需要明确配置钩子。

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

这会在每次提示后自动触发学习内容评估提醒（大约增加50-100个处理开销）。

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
| `scripts/error-detector.sh` | PostToolUse（Bash） | 在命令出错时触发提醒 |

详细配置和故障排除方法请参阅`references/hooks-setup.md`。

## 自动提取技能

当学习内容具有足够的价值，可以成为可重用的技能时，可以使用提供的工具进行提取。

### 技能提取标准

满足以下任一条件的学习内容即可被提取为技能：
- **重复性**：有2个或更多类似问题的`See Also`链接  
- **已验证**：状态为`resolved`且已有有效的修复方案  
- **非显而易见**：需要实际调试或调查才能发现  
- **具有普遍适用性**：不特定于某个项目，适用于多个代码库  
- **用户标记**：用户表示“将此内容保存为技能”  

### 提取流程：
1. **识别候选内容**：学习内容符合提取标准  
2. **运行提取工具**（或手动执行）：  
   ```bash
   ./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improvement/scripts/extract-skill.sh skill-name
   ```  
3. **自定义SKILL.md`文件**：使用模板填充学习内容  
4. **更新学习记录**：将状态设置为`promoted_to_skill`，并添加`Skill-Path`  
5. **验证**：在新会话中重新读取技能内容，确保其完整性  

### 手动提取

如果偏好手动提取：
1. 创建`skills/<技能名称>/SKILL.md`文件  
2. 使用`assets/SKILL-TEMPLATE.md`模板  
3. 遵循[Agent Skills规范](https://agentskills.io/specification)：  
   - 使用YAML格式编写`name`和`description`  
   - 文件名必须与文件夹名一致  
   - 技能文件夹内不得包含`README.md`文件  

### 提取触发条件：

当出现以下情况时，表示学习内容适合被提取为技能：
- **在对话中**：用户表示“将此内容保存为技能”  
- “我经常遇到这个问题”  
- “这对其他项目也有用”  
- “记住这个模式”  
- **在学习记录中**：有多个`See Also`链接（问题重复出现）  
- 优先级高且状态为`resolved`  
- 类别为`best_practice`且具有普遍适用性  
- 用户反馈表示该解决方案很有用  

### 技能质量检查

在提取之前，请确认：
- 解决方案已经过测试且可用  
- 描述清晰，无需依赖原始上下文  
- 代码示例完整  
- 不存在项目特定的硬编码值  
- 遵循技能命名规范（小写、使用连字符）  

## 多代理支持

该技能适用于不同的AI编码代理，并支持针对特定代理的激活方式。

### Claude Code

**激活方式**：使用`UserPromptSubmit`、`PostToolUse`钩子  
**设置方式**：配置`.claude/settings.json`文件中的钩子  
**检测方式**：通过钩子脚本自动检测  

### Codex CLI

**激活方式**：使用`UserPromptSubmit`、`PostToolUse`钩子  
**设置方式**：配置`.codex/settings.json`文件中的钩子  
**检测方式**：通过钩子脚本自动检测  

### GitHub Copilot

**激活方式**：手动设置（不支持钩子）  
**设置方式**：将相关内容添加到`.github/copilot-instructions.md`文件中：  
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
**检测方式**：通过会话工具和工作区文件自动检测  

### 通用指导原则

无论使用哪种代理，当遇到以下情况时都应进行自我提升：
- 发现非显而易见的问题  
- 自我纠正（初始方法错误）  
- 了解项目规范  
- 遇到意外错误（尤其是诊断困难时）  
- 找到更好的解决方案  

### Copilot聊天集成

对于Copilot用户，可以在相关提示中添加以下内容：
> 完成任务后，使用自我提升功能将学习内容记录到`.learnings/`文件中。  
或使用快速提示：  
- “将这些内容记录到学习记录中”  
- “根据这个解决方案创建一个技能”  
- “查看`.learnings/`文件中是否有相关问题”
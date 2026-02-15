---
name: self-improvement
description: "记录学习到的内容、出现的错误以及相应的修正措施，以实现持续改进。适用场景包括：  
(1) 某个命令或操作意外失败时；  
(2) 用户对Claude的回答表示异议（例如：“不，那不对……”或“实际上……”）；  
(3) 用户请求的功能并不存在时；  
(4) 外部API或工具出现故障时；  
(5) Claude发现自己的知识已经过时或不准确时；  
(6) 对于重复性任务，发现了更优的处理方法时。  
此外，在执行重要任务之前，也应当回顾这些记录中的学习内容。"
---

# 自我提升技能

将学习内容及遇到的错误记录到 Markdown 文件中，以实现持续改进。编码助手可以后续将这些记录转化为修复方案，而重要的学习成果则会被纳入项目知识库中。

## 快速参考

| 情况 | 应采取的行动 |
|-----------|--------|
| 命令/操作失败 | 记录到 `.learnings/ERRORS.md` |
| 用户纠正了你的错误 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `correction` 类别 |
| 用户提出了功能需求 | 记录到 `.learnings/FEATURE_REQUESTS.md` |
| API/外部工具出现故障 | 记录到 `.learnings/ERRORS.md`，并附上集成细节 |
| 知识过时 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `knowledge_gap` 类别 |
| 发现了更好的方法 | 记录到 `.learnings/LEARNINGS.md`，并标记为 `best_practice` 类别 |
| 与现有条目相似 | 使用 `**参见** 链接，并考虑提升优先级 |
| 具有普遍适用性的知识 | 将其收录到 `CLAUDE.md` 和/或 `AGENTS.md` 中 |

## 设置

如果项目根目录中不存在 `.learnings/` 目录，请创建该目录：

```bash
mkdir -p .learnings
```

从 `assets/` 目录复制模板，或创建带有标题的新文件。

## 日志格式

### 学习记录

追加到 `.learnings/LEARNINGS.md` 文件中：

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

追加到 `.learnings/ERRORS.md` 文件中：

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

追加到 `.learnings/FEATURE_REQUESTS.md` 文件中：

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
- `XXX`：顺序编号或随机生成的 3 个字符（例如 `001`、`A7B`）

示例：`LRN-20250115-001`、`ERR-20250115-A3F`、`FEAT-20250115-002`

## 问题解决

问题解决后，请更新相关记录：

1. 将 `**状态** 更改为 `pending` → `resolved`
2. 在元数据后添加问题解决说明：

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of what was done
```

其他状态值：
- `in_progress`：正在处理中
- `wont_fix`：决定不解决（在解决说明中说明原因）
- `promoted`：被提升到 `CLAUDE.md` 或 `AGENTS.md`

## 提升到项目知识库

当某项学习内容具有普遍适用性（而非一次性问题）时，应将其纳入项目知识库中。

### 何时提升

- 该知识适用于多个文件或功能
- 所有贡献者（无论是人类还是 AI）都应了解
- 可防止类似问题的再次发生
- 可记录项目特定的规范

### 提升目标

| 目标 | 应收录的内容 |
|--------|-------------------|
| `CLAUDE.md` | 项目的基本事实、规范以及与 Claude 相关的注意事项 |
| `AGENTS.md` | 与助手相关的流程、工具使用方式、自动化规则 |

### 提升方法

1. 将学习内容提炼成简洁的规则或事实
2. 添加到目标文件的相应部分
3. 更新原始记录：
   - 将 `**状态** 更改为 `pending` → `promoted`
   - 添加 `**Promoted**: CLAUDE.md` 或 `**Promoted**: AGENTS.md`

### 提升示例

**学习内容（详细）**：
> 项目使用 pnpm 工作区，尝试执行 `npm install` 但失败了。
> 锁定文件为 `pnpm-lock.yaml`，应使用 `pnpm install`。

**在 CLAUDE.md 中（简洁）**：
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

**学习内容（详细）**：
> 修改 API 端点时，必须重新生成 TypeScript 客户端代码。
> 如果忽略这一点，运行时会出现类型不匹配的问题。

**在 AGENTS.md 中（可操作的内容）**：
```markdown
## After API Changes
1. Regenerate client: `pnpm run generate:api`
2. Check for type errors: `pnpm tsc --noEmit`
```

## 重复性问题的检测

如果记录的内容与现有条目相似，请先进行搜索：

1. **先搜索**：`grep -r "关键词" .learnings/`
2. **添加链接**：在元数据中添加 `**参见**：ERR-20250110-001`
3. **如果问题持续出现**，提升优先级
4. **考虑系统性解决方案**：重复出现的问题通常表明：
   - 缺乏文档（→ 提升到 CLAUDE.md）
   - 缺少自动化处理（→ 添加到 AGENTS.md）
   - 存在架构问题（→ 创建技术债务工单）

## 定期审查

在适当的时机审查 `.learnings/` 文件：

### 何时审查
- 在开始新的重要任务之前
- 完成某个功能后
- 在处理之前有相关学习记录的领域时
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

### 审查内容
- 解决已解决的问题
- 提升具有适用性的学习内容
- 链接相关的记录
- 升级重复出现的问题

## 检测触发条件

在发现以下情况时自动记录：

**纠正错误**（→ 标记为 `correction` 类别的记录）：
- “不，那不对……”
- “实际上应该是……”
- “你对……的理解有误……”
- “那已经过时了……”

**功能需求**（→ 标记为 `feature_request` 的记录）：
- “你能不能也……”
- “我希望你能……”
- “有没有办法……”
- “为什么不能……”

**知识缺口**（→ 标记为 `knowledge_gap` 的记录）：
- 用户提供了你不知道的信息
- 你参考的文档已经过时
- API 的行为与你的理解不一致

**错误**（→ 标记为 `error` 的记录）：
- 命令返回非零退出码
- 异常或堆栈跟踪
- 出现意外的输出或行为
- 超时或连接失败

## 优先级指南

| 优先级 | 使用场景 |
|----------|-------------|
| `critical` | 影响核心功能、存在数据丢失风险或安全问题 |
| `high` | 有显著影响，影响常见工作流程或问题反复出现 |
| `medium` | 影响较小，但有解决方法 |
| `low` | 仅造成轻微不便，属于边缘情况或可选功能 |

## 区域标签

用于按代码库区域过滤学习记录：

| 区域 | 范围 |
|------|-------|
| `frontend` | 用户界面、组件、客户端代码 |
| `backend` | API、服务、服务器端代码 |
| `infra` | 持续集成/持续部署、Docker、云服务 |
| `tests` | 测试文件、测试工具、测试覆盖率 |
| `docs` | 文档、注释、README 文件 |
| `config` | 配置文件、环境设置 |

## 最佳实践

1. **立即记录**——问题发生时上下文最为清晰
2. **具体说明**——未来的助手需要快速理解问题
3. **包含重现步骤**——尤其是对于错误记录
4. **链接相关文件**——便于修复
5. **提出具体的解决方案**——而不仅仅是“进行调查”
6. **使用统一的分类**——便于查找
7. **积极提升**——如有疑问，将其添加到 CLAUDE.md 中
8. **定期审查**——过时的学习内容会失去价值

## Git 忽略选项

**将学习记录保留在本地**（针对单个开发者）：
```gitignore
.learnings/
```

**在仓库中记录学习内容**（全团队共享）：
不要将学习记录添加到 `.gitignore` 文件中，这样它们才能被所有团队成员共享。

**混合方式**（记录模板，忽略具体条目）：
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```
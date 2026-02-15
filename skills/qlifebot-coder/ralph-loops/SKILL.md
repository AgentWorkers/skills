# Ralph Loops 技能

> **第一次使用？** 请先阅读 [SETUP.md](./SETUP.md) 以安装依赖项并验证您的设置。

Ralph Loops 是一个用于迭代开发的自主 AI 代理。该技术基于 Geoffrey Huntley 的 Ralph Wiggum 技术，并由 Clayton Farr 进行了详细记录。

**脚本：** `skills/ralph-loops/scripts/ralph-loop.mjs`
**仪表板：** `skills/ralph-loops/dashboard/`（使用 `node server.mjs` 运行）
**模板：** `skills/ralph-loops/templates/`
**归档：** `~/clawd/logs/ralph-archive/`

---

## ⚠️ 已知问题

### Claude 代码版本兼容性

**Claude 代码 2.1.29 存在一个严重漏洞**，该漏洞会导致生成消耗 99% CPU 资源的孤立子代理。首次运行时，迭代会因“退出代码为 null”而失败。

**解决方法：** 回退到 2.1.25 版本：
```bash
npm install -g @anthropic-ai/claude-code@2.1.25
```

**验证方法：**
```bash
claude --version  # Should show 2.1.25
```

这个问题发现于 2026-02-01。在升级之前，请检查新版本是否修复了该问题。

---

## ⚠️ 不要阻塞对话！

运行 Ralph 循环时，请**不要同步监控**。循环作为独立的 Claude CLI 进程运行——您可以继续与人类用户进行对话。

**❌ 错误做法（会阻塞对话）：**
```
Start loop → sleep 60 → poll → sleep 60 → poll → ... (6 minutes of silence)
```

**✅ 正确做法（保持响应性）：**
```
Start loop → "It's running, I'll check periodically" → keep chatting → check on heartbeats
```

**如何在不阻塞对话的情况下进行监控：**
1. 使用 `node ralph-loop.mjs` 启动循环（在后台运行）
2. 告诉人类用户：“循环正在运行。我会定期检查进度，或者您可以随时询问。”
3. 根据需要或通过心跳信号，使用 `process poll <sessionId>` 来检查循环状态
4. 通过 http://localhost:3939 访问仪表板以获取实时信息

**循环是自主运行的**——这就是其核心特点。不要为了监控循环而忽略与人类的交流。

---

## 触发语句

当人类用户说：

| 语句 | 操作 |
|--------|--------|
| **“关于系统 X 进行访谈”** | 启动第 1 阶段的需求访谈 |
| **“开始规划系统 X”** | 运行 `./loop.sh plan`（需要先制定计划） |
| **“开始构建系统 X”** | 运行 `./loop.sh build`（需要先制定计划） |
| **“对 X 进行 Ralph 循环”** | **询问当前处于哪个阶段**（见下文） |

### 当人类用户说“Ralph Loop”时——明确当前阶段！

不要默认判断当前处于哪个阶段。请询问：

> “我们正在进行哪种类型的 Ralph 循环？
> 
> 1️⃣ **访谈** —— 我会向您提问以制定需求规格（第 1 阶段）
> 2️⃣ **规划** —— 我会针对实施计划进行迭代（第 2 阶段）  
> 3️⃣ **构建** —— 我会根据计划逐项执行任务（第 3 阶段）
> 4️⃣ **通用** —— 对单一主题进行简单的迭代优化”

**然后根据用户的回答采取相应操作：**

| 选择 | 操作 |
|--------|--------|
| 访谈 | 使用 `templates/requirements-interview.md` 协议 |
| 规划 | 需要先制定计划 → 使用 `PROMPT_plan.md` 启动规划循环 |
| 构建 | 需要先制定计划 → 使用 `PROMPT_build.md` 启动构建循环 |
| 通用 | 创建提示文件，直接运行 `ralph-loop.mjs` |

### 通用 Ralph 循环流程（第 4 阶段）

对于简单的迭代优化（非完整系统构建）：

1. **明确任务** —— 需要改进或优化的具体内容是什么？
2. **创建提示文件** —— 保存到 `/tmp/ralph-prompt-<task>.md`
3. **设定完成标准** —— 什么情况表示任务完成？
4. **运行循环：**
   ```bash
   node skills/ralph-loops/scripts/ralph-loop.mjs \
     --prompt "/tmp/ralph-prompt-<task>.md" \
     --model opus \
     --max 10 \
     --done "RALPH_DONE"
   ```
5. **对于耗时较长的任务，可以生成子代理来执行**

---

## 核心理念

> “人类的角色从‘告诉代理该做什么’转变为‘创造条件，让良好的结果通过迭代自然产生’。”
> —— Clayton Farr

三个原则指导着整个流程：

1. **上下文是有限的** —— 在 200,000 个可用令牌中，只有大约 176,000 个可用于每次迭代，因此要确保每次迭代都高效简洁
2. **计划是可以丢弃的** —— 重新生成计划比修复错误代码更经济
3. **反向压力机制优于方向性控制** —— 通过机制确保错误的输出会被自动拒绝

---

## 三阶段工作流程

```
┌─────────────────────────────────────────────────────────────────────┐
│  Phase 1: REQUIREMENTS                                              │
│  Human + LLM conversation → JTBD → Topics → specs/*.md              │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 2: PLANNING                                                  │
│  Gap analysis (specs vs code) → IMPLEMENTATION_PLAN.md              │
├─────────────────────────────────────────────────────────────────────┤
│  Phase 3: BUILDING                                                  │
│  One task per iteration → fresh context → backpressure → commit     │
└─────────────────────────────────────────────────────────────────────┘
```

### 第 1 阶段：需求收集（与人类用户交流）

**目标：** 在开始构建之前，先了解需要构建什么。

这是最重要的阶段。通过结构化的对话来：

1. **确定待完成的任务（JTBD）**
   - 我们要解决的用户需求或目标是什么？
   - 不是要实现的功能，而是最终的结果
2. **将 JTBD 分解为具体的主题**
   - 每个主题对应一个独立的方面/组件
   - 使用“用一句话表达，不要使用‘和’”的测试标准
   - ✓ “颜色提取系统用于分析图像以识别主导颜色”
   - ✗ “用户系统处理身份验证、个人资料和计费” → 这属于三个不同的主题
3. **为每个主题制定详细规范**
   - 每个主题对应一个 markdown 文件，保存在 `specs/` 目录下
   - 包括需求、验收标准和边缘情况

**模板：** `templates/requirements-interview.md`

### 第 2 阶段：规划（差距分析）

**目标：** 在不进行任何实际实现的情况下，制定一个优先级任务列表。

在循环中使用 `PROMPT_plan.md`：
- 研究所有需求规范
- 查看现有代码库
- 对比需求规范和代码（进行差距分析）
- 生成包含优先级任务的 `IMPLEMENTATION_PLAN.md`
- **仅进行规划** —— 不涉及实际实现

通常在 1-2 次迭代内完成。

### 第 3 阶段：构建（每次迭代完成一个任务）

**目标：** 每次迭代只完成一个任务，并使用新的上下文。

在循环中使用 `PROMPT_build.md`：
1. 读取 `IMPLEMENTATION_PLAN.md`
2. 选择最重要的任务
3. 查看代码库（假设代码尚未实现）
4. 实现任务
5. 进行验证（使用反向压力机制）
6. 更新计划并提交代码
7. 退出循环 → 重新开始新的迭代

**关键点：** 每次迭代只完成一个任务，这样可以保持上下文的清晰性。避免代理陷入混乱。

**为什么需要新的上下文：**
- **避免错误累积** —— 每次迭代都从零开始；之前的错误不会叠加
- **保证上下文的完整性** —— 200,000 个令牌专门用于当前任务，不会与已完成的部分共享
- **减少误解** —— 更短的上下文有助于产生更准确的响应
- **设置明确的检查点** —— 每次提交都是一个保存点，便于回滚单个迭代的结果

---

## 文件结构

```
project/
├── loop.sh                    # Ralph loop script
├── PROMPT_plan.md             # Planning mode instructions
├── PROMPT_build.md            # Building mode instructions  
├── AGENTS.md                  # Operational guide (~60 lines max)
├── IMPLEMENTATION_PLAN.md     # Prioritized task list (generated)
└── specs/                     # Requirement specs
    ├── topic-a.md
    ├── topic-b.md
    └── ...
```

### 文件用途

| 文件 | 用途 | 创建者 |
|------|---------|-------------|
| `specs/*.md` | 需求规范的权威来源 | 人类用户 + 第 1 阶段 |
| `PROMPT_plan.md` | 规划模式的指导说明 | 从模板复制 |
| `PROMPT_build.md` | 构建模式的指导说明 | 从模板复制 |
| `AGENTS.md` | 构建/测试/代码检查命令 | 人类用户 + Ralph 代理 |
| `IMPLEMENTATION_PLAN.md` | 包含优先级任务的列表 | Ralph 代理（第 2 阶段） |

### 项目组织结构（针对 Clawdbot 系统）

对于 Clawdbot 系统，每个 Ralph 项目都存储在 `<workspace>/systems/<name>/` 目录下：

```
systems/
├── health-tracker/           # Example system
│   ├── specs/
│   │   ├── daily-tracking.md
│   │   └── test-scheduling.md
│   ├── PROMPT_plan.md
│   ├── PROMPT_build.md
│   ├── AGENTS.md
│   ├── IMPLEMENTATION_PLAN.md  # ← exists = past Phase 1
│   └── src/
└── activity-planner/
    ├── specs/                  # ← empty = still in Phase 1
    └── ...
```

### 自动检测当前阶段

通过检查存在的文件来自动判断当前处于哪个阶段：

| 文件存在情况 | 当前阶段 | 下一步操作 |
|-------------|---------------|-------------|
| 不存在文件或 `specs/` 目录为空 | 第 1 阶段：需求收集 | 运行需求访谈 |
| 存在 `specs/*.md` 但不存在 `IMPLEMENTATION_PLAN.md` | 准备进入第 2 阶段 | 运行 `./loop.sh plan` |
| 存在 `specs/*.md` 和 `IMPLEMENTATION_PLAN.md` | 处于第 2 或第 3 阶段 | 查看计划并运行 `./loop.sh build` |
| `IMPLEMENTATION_PLAN.md` 显示所有任务已完成 | 完成 | 归档或进入下一阶段 |

**快速检查方法：**
```bash
# What phase are we in?
[ -z "$(ls specs/ 2>/dev/null)" ] && echo "Phase 1: Need specs" && exit
[ ! -f IMPLEMENTATION_PLAN.md ] && echo "Phase 2: Need plan" && exit
echo "Phase 3: Ready to build (or done)"
```

---

## JTBD 分解

文件的结构非常重要：

```
JTBD (Job to Be Done)
└── Topic of Concern (1 per spec file)
    └── Tasks (many per topic, in IMPLEMENTATION_PLAN.md)
```

**示例：**
- **需求：** “帮助设计师创建 Mood Board”
- **相关主题：**
  - 图像收集 → `specs/image-collection.md`
  - 颜色提取 → `specs/color-extraction.md`
  - 布局系统 → `specs/layout-system.md`
  - 共享功能 → `specs/sharing.md`
- **任务：** 每个主题都会生成多个具体的实现任务

### 主题范围判断

> 你能用一句话描述这个主题吗？如果需要使用“和”或“also”，那么这个主题可能包含多个部分。

**何时需要拆分主题：**
- 描述中包含多个动词 → 分成多个主题
- 涉及不同的用户角色 → 分成多个主题
- 可能需要由不同的团队来实现 → 分成多个主题
- 有自己独立的失败模式 → 通常需要单独处理

**示例：**
```
❌ "User management handles registration, authentication, profiles, and permissions"

✅ Split into:
   - "Registration creates new user accounts from email/password"
   - "Authentication verifies user identity via login flow"  
   - "Profiles let users view and edit their information"
   - "Permissions control what actions users can perform"
```

**反例（不需要拆分主题的情况）：**
```
✅ Keep together:
   "Color extraction analyzes images and returns dominant color palettes"
   
   Why: "analyzes" and "returns" are steps in one operation, not separate concerns.
```

---

## 反向压力机制

当错误的输出被拒绝时，循环会自动调整方向。反向压力机制分为三个层次：

### 1. 下游关卡（硬性约束）
   - 测试、类型检查、代码检查、构建验证。这些是确定性的规则。
```markdown
# In AGENTS.md
## Validation
- Tests: `npm test`
- Typecheck: `npm run typecheck`
- Lint: `npm run lint`
```

### 2. 上游引导（软性约束）
   - 现有的代码模式会引导代理的行为。代理会通过探索来发现最佳实践。

### 3. 作为判断者的 LLM（主观判断）
   - 对于主观性标准（如语气、用户体验、美学等），可以使用另一个 LLM 来进行二分判断（通过“通过”或“失败”来决定结果）。

> 先使用硬性约束。只有在硬性约束无效时，才使用 LLM 进行主观判断。

---

## 提示语结构

Geoffrey 设计的提示语遵循一定的编号规则：

| 部分 | 用途 |
|---------|---------|
| 0a-0d | **引导**：研究需求规范、源代码和当前计划 |
| 1-4 | **主要指令**：本次迭代的具体操作 |
| 999+ | **安全提示**：表示重要性的提示（数字越大，提示越关键） |

### 数字提示语的优先级规则

使用递增的数字（如 99999、999999、9999999...）来表示提示的优先级：

```markdown
99999. Important: Capture the why in documentation.

999999. Important: Single sources of truth, no migrations.

9999999. Create git tags after successful builds.

99999999. Add logging if needed to debug.

999999999. Keep IMPLEMENTATION_PLAN.md current.
```

**这样设计的理由：**
1. **视觉上的突出性** —— 数字越大，越容易被注意到
2. **隐含的优先级** —— 数字越大，提示越重要（类似于紧急程度的分级）
3. **避免冲突** —— 稀疏的编号便于添加新的规则而不需要重新编号
4. **便于记忆** —— Claude 会将这些提示视为不可更改的规则

**“Important:” 前缀** 是有意设计的，用于引起 Claude 的注意。

### 关键语言表达方式

使用 Geoffrey 设计的特定表达方式非常重要：

- 使用“study”（而不是“read”或“look at”）
- 强调“不要假设代码尚未实现”（这一点非常重要！）
- 使用“使用多个子代理”或“最多使用 N 个子代理”来控制并发
- 使用“Ultrathink”来触发深度推理
- 强调“记录原因”
- 告诉代理“保持信息更新”

---

## 快速入门

### 1. 设置项目结构

```bash
mkdir -p myproject/specs
cd myproject
git init  # Ralph expects git for commits

# Copy templates
cp .//templates/PROMPT_plan.md .
cp .//templates/PROMPT_build.md .
cp .//templates/AGENTS.md .
cp .//templates/loop.sh .
chmod +x loop.sh
```

### 2. 自定义模板（必须完成！）

**PROMPT_plan.md** —— 将 `[PROJECT_GOAL]` 替换为你的实际目标：
```markdown
# Before:
ULTIMATE GOAL: We want to achieve [PROJECT_GOAL].

# After:
ULTIMATE GOAL: We want to achieve a fully functional mood board app with image upload and color extraction.
```

**PROMPT_build.md** —— 如果不使用 `src/` 目录，请调整文件路径：
```markdown
# Before:
0c. For reference, the application source code is in `src/*`.

# After:
0c. For reference, the application source code is in `lib/*`.
```

**AGENTS.md** —— 根据你的开发环境更新构建/测试/代码检查命令。

### 3. 第 1 阶段：需求收集（不要跳过！**

这个阶段需要与人类用户一起完成。使用访谈模板：

```bash
cat .//templates/requirements-interview.md
```

**工作流程：**
1. 讨论待完成的任务（JTBD）——即最终要实现的结果，而不是具体的功能
2. 将任务分解为具体的主题
3. 为每个主题编写一个规范文件：`specs/topic-name.md`
4. 人类用户审核并批准这些规范文件

**示例输出：**
```
specs/
├── image-collection.md
├── color-extraction.md
├── layout-system.md
└── sharing.md
```

### 4. 第 2 阶段：规划

**等待 `IMPLEMENTATION_PLAN.md` 生成（通常需要 1-2 次迭代）。审核该文件，它将作为你的任务列表。**

### 5. 第 3 阶段：构建**

**观察循环的运行情况。在出现问题时添加反向压力机制（如测试、代码检查）。通过提交代码来跟踪进度。**

---

## 循环脚本选项

### 使用 Node.js 包装器以获得更多控制权

```bash
./loop.sh              # Build mode, unlimited
./loop.sh 20           # Build mode, max 20 iterations
./loop.sh plan         # Plan mode, unlimited
./loop.sh plan 5       # Plan mode, max 5 iterations
```

---

## 何时需要重新生成计划

当计划偏离目标、计划显得过时或与当前状态不符、已完成的任务过多导致混乱、你对实际完成的内容感到困惑时，都需要重新生成计划：

**只需切换回规划模式即可：**

```bash
./loop.sh plan
```

重新生成计划的成本只是一个规划循环的费用。相比让循环陷入无限循环，这非常划算。

---

## 安全性

Ralph 需要 `--dangerously-skip-permissions` 参数才能自主运行。这会完全绕过 Claude 的权限系统。

**安全策略：**
- 在隔离的环境中运行（如 Docker 或虚拟机）
- 仅使用完成任务所需的 API 密钥
- 限制对私有数据的访问
- 在可能的情况下限制网络连接
- **紧急退出机制：** 使用 Ctrl+C 停止循环；使用 `git reset --hard` 恢复未提交的更改

## 成本估算

| 任务类型 | 使用的模型 | 需要的迭代次数 | 预计成本 |
|-----------|-------|------------|-----------|
| 生成计划 | Opus | 1-2 次迭代 | 0.50-1.00 美元 |
| 实现简单功能 | Opus | 3-5 次迭代 | 1.00-2.00 美元 |
| 实现复杂功能 | Opus | 10-20 次迭代 | 3.00-8.00 美元 |
| 完整项目构建 | Opus | 50 次以上迭代 | 15.00-50.00 美元 |

**提示：** 对于计划明确简单的任务，可以使用 Sonnet 模型；对于需要复杂规划的任务，使用 Opus 模型。

## 实际应用成果

Geoffrey Huntley 的案例：
- 在 YC 霸客赛中，一夜之间生成了 6 个项目
- 以 297 美元的 API 使用成本完成了价值 50,000 美元的合同
- 在 3 个月内开发出了一门全新的编程语言

---

## 高级用法：作为子代理运行

对于耗时较长的循环，可以将代理作为子代理来运行，以确保主会话保持响应性：

```javascript
sessions_spawn({
  task: `cd /path/to/project && ./loop.sh build 20
         
Summarize what was implemented when done.`,
  label: "ralph-build",
  model: "opus"
})
```

**检查循环的进度：**
```javascript
sessions_list({ kinds: ["spawn"] })
sessions_history({ label: "ralph-build", limit: 5 })
```

---

## 故障排除

### Ralph 一直重复执行相同的操作
- 如果计划过时，使用 `./loop.sh plan` 重新生成计划
- 如果缺少反向压力机制，添加相应的测试来检测重复操作

### Ralph 陷入无限循环
- 在提示语中添加更具体的约束条件
- 检查需求规范是否表述模糊
- 重新生成计划

### 上下文信息过于复杂
- 确保每次迭代只完成一个任务（检查提示语）
- 保持 `AGENTS.md` 文件的代码量在 60 行以内
- 将状态和进度信息移到 `IMPLEMENTATION_PLAN.md` 文件中

### 测试无法运行
- 检查 `AGENTS.md` 文件中是否包含正确的验证命令
- 确保提示语中引用了正确的验证代码

## 特殊情况处理

### 没有 Git 的项目

循环脚本依赖于 Git 来完成提交和推送操作。对于没有版本控制的项目：

**选项 1：** 尽管如此，仍然初始化 Git （推荐）**
```bash
git init
git add -A
git commit -m "Initial commit before Ralph"
```

**选项 2：** 修改提示语**
- 从 `PROMPT_build.md` 中删除与 Git 相关的提示语
- 从 `loop.sh` 文件中删除与 Git 相关的代码
- 使用文件备份：在 `loop.sh` 中添加 `cp -r src/ backups/iteration-$ITERATION/` 命令

**选项 3：** 使用 tarball 快照**
```bash
# Add to loop.sh before each iteration:
tar -czf "snapshots/pre-iteration-$ITERATION.tar.gz" src/
```

### 大型代码库

对于代码量超过 100,000 行的项目：

- **减少子代理的并发数量**：将提示语中的“最多使用 500 个 Sonnet 子代理”修改为“最多使用 50 个”
- **缩小关注范围**：编写针对特定目录的详细规范
- **调整路径限制**：在 `AGENTS.md` 中明确指定哪些目录属于当前任务的范围内
- **考虑将大型模块视为独立的项目**  

### 当 Claude CLI 不可用时

无论使用哪种 Claude 接口，都可以采用这种方法：

**直接使用 Claude API：**
```bash
# Replace loop.sh with API calls using curl or a script
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "content-type: application/json" \
  -d '{"model": "claude-sonnet-4-20250514", "max_tokens": 8192, "messages": [...]}'
```

**其他替代方案：**
- **辅助工具：** `aider --opus --auto-commits`
- **Continue.dev：** 使用 Claude API 密钥
- **Cursor：** 在 Composer 模式下使用提示语文件作为上下文

无论使用哪种工具，三个核心原则（每次迭代只完成一个任务、保持上下文清晰、使用反向压力机制）都同样适用。

### 非 Node.js 项目的配置

根据你的开发环境调整 `AGENTS.md` 文件中的配置：

| 开发环境 | 构建工具 | 测试工具 | 代码检查工具 |
|-------|-------|------|------|
| Python | `pip install -e .` | `pytest` | `ruff .` |
| Go | `go build ./...` | `go test ./...` | `golangci-lint run` |
| Rust | `cargo build` | `cargo test` | `cargo clippy` |
| Ruby | `bundle install` | `rspec` | `rubocop` |
| ... | 根据实际情况调整相应的命令 |

---

## 更多资源

- Geoffrey Huntley 的相关资料：https://ghuntley.com/ralph/
- Clayton Farr 的使用指南：https://github.com/ClaytonFarr/ralph-playbook
- Geoffrey 的开源代码仓库：https://github.com/ghuntley/how-to-ralph-wiggum

---

## 致谢

该项目由 **Johnathan 和 Q** 共同开发——一个人类与 AI 的协作团队。

- Twitter 账号：[@spacepixel](https://x.com/spacepixel)
- ClawdHub 上的项目链接：[clawhub.ai/skills/ralph-loops](https://www.clawhub.ai/skills/ralph-loops)
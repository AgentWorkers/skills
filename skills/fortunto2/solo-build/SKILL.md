---
name: solo-build
description: 使用 TDD（测试驱动开发）工作流程、自动提交（auto-commit）和阶段检查（phase gates）来执行实施计划中的任务。当用户发出“构建它”（build it）、“开始构建”（start building）、“执行计划”（execute plan）、“实施任务”（implement tasks）或提及某个任务跟踪 ID（track ID）时，可以使用此流程。请勿将其用于规划（使用 /plan）或搭建项目框架（使用 /scaffold）。
license: MIT
metadata:
  author: fortunto2
  version: "2.2.0"
  openclaw:
    emoji: "🔨"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query, mcp__solograph__web_search, mcp__context7__resolve-library-id, mcp__context7__query-docs
argument-hint: "[track-id] [--task X.Y] [--phase N]"
---
# /build

该技能是独立完成的——请遵循以下任务循环、TDD（测试驱动开发）规则和完成流程，而不是依赖外部构建/执行工具。

从实施计划中执行任务。查找 `plan.md` 文件（位于 `docs/plan/` 目录下，适用于项目；位于 `4-opportunities/` 目录下，适用于知识库（KB）），选择下一个未完成的任务，使用 TDD 工作流程进行实现，提交代码，并更新进度。

## 使用场景

在 `/plan` 创建了包含 `spec.md` 和 `plan.md` 的任务列表后使用该技能。这是执行引擎。

执行流程：`/plan` → **`/build`** → `/deploy` → `/review`

## MCP 工具（如有可用）

- `session_search(query)` — 查找之前类似问题的解决方案
- `project_code_search(query, project)` — 在项目中查找可重用的代码
- `codegraph_query(query)` — 检查文件依赖关系和导入内容

如果 MCP 工具不可用，请使用全局搜索（Glob）+ 正则表达式匹配（Grep）+ 读取文件内容（Read）。

## 预执行检查

1. **确定上下文** — 查找计划文件的位置：
   - 检查 `docs/plan/*/plan.md` — 项目上下文（标准位置）
   - 检查 `4-opportunities/*/plan.md` — 知识库上下文（仅适用于独立创业者）
   - 优先选择 `docs/plan/`。
   **请勿** 在其他目录（如 `conductor/`）中搜索计划文件。

2. 从 `docs/workflow.md`（如果存在）中加载工作流程配置：
   - TDD 的严格程度（严格 / 适中 / 无）
   - 提交策略（常规提交格式）
   - 验证检查点规则
   - **集成测试部分** — 如果存在，在完成涉及这些路径的任务后运行指定的 CLI 命令
   如果 `docs/workflow.md` 丢失，请使用默认设置（适度的 TDD，常规提交）。

3. **验证 git 钩子是否已安装：**

   读取 `templates/stacks/{stack}.yaml` 文件中的配置 — `pre_commit` 字段会告诉您需要使用哪个系统和相应的钩子：
   - 对于 JS/TS 项目：`husky + lint-staged`（使用 ESLint、prettier 和 tsc）
   - 对于 Python 项目：`pre-commit`（使用 ruff、ruff-format 和 ty）
   - 对于移动项目：`lefthook`（使用 swiftlint/detekt 和 formatter）

   然后验证钩子系统是否处于活动状态：
   ```bash
   # husky
   [ -f .husky/pre-commit ] && git config core.hooksPath | grep -q husky && echo "OK" || echo "NOT ACTIVE"
   # pre-commit (Python)
   [ -f .pre-commit-config.yaml ] && [ -f .git/hooks/pre-commit ] && echo "OK" || echo "NOT ACTIVE"
   # lefthook
   [ -f lefthook.yml ] && lefthook version >/dev/null 2>&1 && echo "OK" || echo "NOT ACTIVE"
   ```

   **如果钩子未激活——在首次提交前安装：**
   - 对于 husky：`pnpm prepare`（或 `npm run prepare`
   - 对于 pre-commit：`uv run pre-commit install`
   - 对于 lefthook：`lefthook install`

   提交时请勿使用 `--no-verify` 选项——如果钩子失败，请修复问题后再提交。

## 任务选择

### 如果 `$ARGUMENTS` 包含任务 ID：
- 验证：`{plan_root}/{argument}/plan.md` 文件是否存在（同时检查 `docs/plan/` 和 `4-opportunities/` 目录）。
- 如果未找到：在 `docs/plan/*/plan.md` 和 `4-opportunities/*/plan.md` 中搜索匹配项，并提供修改建议。

### 如果 `$ARGUMENTS` 包含 `--task X.Y`：
- 直接跳转到活动任务中。

### 如果没有参数：
1. 在 `docs/plan/` 和 `4-opportunities/` 目录中搜索 `plan.md` 文件。
2. 阅读每个 `plan.md` 文件，找到未完成任务的阶段。
3. 如果有多个阶段，通过 AskUserQuestion 获取用户确认。
4. 如果没有找到任何阶段：提示“未找到计划，请先运行 `/plan`。

## 上下文加载

### 第一步 — 架构概述（如果 MCP 工具可用）
```
codegraph_explain(project="{project name}")
```
返回：项目架构、使用的编程语言、目录结构、关键模式、主要依赖关系以及核心文件——通过一次调用即可获取这些信息，无需手动遍历项目结构。

### 第二步 — 必读文档
1. `docs/plan/{trackId}/plan.md` — 任务列表（必需）
2. `docs/plan/{trackId}/spec.md` — 验收标准（必需）
3. `docs/workflow.md` — TDD 政策和提交策略（如果存在）
4. `CLAUDE.md` — 开发规范（Do/Don't 列表）
5. `.solo/pipelines/progress.md` — 上次迭代中的执行记录（如果存在）。其中包含已完成的工作内容：完成的阶段、提交哈希值（SHA）和最后输出信息。**利用这些信息避免重复工作。**

**请在此阶段不要阅读源代码文件。** 只阅读文档。源代码将在执行循环（第三步）中按任务逐个加载。

## 任务继续执行

如果 `plan.md` 中的任务标记为 `[~]`：

```
Resuming: {track title}
Last task: Task {X.Y}: {description} [in progress]

1. Continue from where we left off
2. Restart current task
3. Show progress summary first
```

通过 AskUserQuestion 获取用户确认后，继续执行任务。

## 任务执行循环

**Makefile 规范：** 如果项目根目录下存在 `Makefile`，**请始终优先使用 `make` 命令**，而不是直接运行命令。例如，使用 `make test` 而不是 `pnpm test`。运行 `make help`（或阅读 Makefile）以了解可用的命令。如果存在 `make integration` 等命令，请在管道相关任务后使用它们进行集成测试。

**重要提示：** 在开始执行循环之前，请检查 `plan.md` 中是否有任何标记为 `- [ ]` 或 `- [~]` 的任务。如果所有任务都标记为 `[x]`，则直接跳转到 **完成** 部分，执行最终验证并输出 `<solo:done/>`。

对于 `plan.md` 中标记为 `[ ]` 的未完成任务，按以下步骤执行：

### 1. 查找下一个任务
解析 `plan.md`，找到以 `- [ ] Task X.Y:` 开头的行（如果是在继续执行任务，则查找 `- [~] Task X.Y:`）。

### 2. 开始任务
- 更新 `plan.md`，将当前任务的状态从 `[ ]` 更改为 `[~]`。
- 公布任务开始信息：**“开始执行任务 X.Y: {description}”**

### 3. 预先研究（智能搜索，避免全盘搜索代码）
**请勿在整个项目中搜索或阅读所有源代码。** 只加载当前任务所需的文件。

**如果 MCP 工具可用（推荐使用）：**
1. `project_code_search(query="{task keywords}", project="{name}")` — 在项目中查找相关代码。仅阅读前 2-3 个结果。
2. `session_search("{task keywords}")` — 检查之前是否已经解决过该任务。
3. `codegraph_query("MATCH (f:File {project: '{name}'})-[:IMPORTS]->(dep) WHERE f.path CONTAINS '{module}' RETURN dep.path")` — 检查将要修改的文件的依赖关系。

**如果 MCP 工具不可用（备用方案）：**
1. 仅阅读任务描述中明确提到的文件路径。
2. 使用全局搜索（Grep）找到任务涉及的模块目录（例如 `src/auth/**/*.ts`），而不是整个项目目录。
3. 如果任务中没有提到具体的文件路径，使用 `src/` 或 `app/` 目录下的文件进行搜索。**切勿使用 `**/*` 这样的通配符进行全盘搜索**。

**切勿** 在整个项目中使用 `Grep "keyword" ` 命令——这会导致大量不必要的输出。请有针对性地搜索。**

### Python 项目的质量检查工具

当项目使用 Python 开发栈时（通过 `pyproject.toml` 或 `stack YAML` 识别）：
1. **Ruff** — 代码格式检查（始终执行）：
   ```bash
   uv run ruff check --fix .
   uv run ruff format .
   ```

2. **ty** — 类型检查（如果 `ty` 在项目的依赖关系中列出）：
   ```bash
   uv run ty check .
   ```
   `ty` 是 Astral 的类型检查工具（速度非常快，可替代 mypy/pyright）。
3. **Hypothesis** — 基于属性的测试（如果 `hypothesis` 在依赖关系中列出）：
   - 使用 `@given(st.from_type(MyModel))` 自动生成 Pydantic 模型输入。
   - 使用 `@given(st.text(), st.integers())` 对解析器和验证器进行边缘情况测试。
4. **预提交检查** — 在提交前运行所有钩子：
   ```bash
   uv run pre-commit run --all-files
   ```

在每次任务实现后运行这些检查，确保所有检查都通过后再提交代码。

### JS/TS 项目的质量检查工具

当项目使用 JavaScript/TypeScript 开发栈时（通过 `package.json` 或 `stack YAML` 识别）：
1. **ESLint** — 代码格式检查（始终执行）：
   ```bash
   pnpm lint --fix
   ```

2. **Prettier** — 代码格式化（始终执行）：
   ```bash
   pnpm format
   ```

3. **tsc --noEmit` — 类型检查（严格模式）：
   ```bash
   pnpm tsc --noEmit
   ```
   在提交前修复类型错误。确保 `tsconfig.json` 中启用了严格模式。

4. **Knip** — 代码冗余检测（如果 `knip` 在项目的依赖关系中列出）：
   ```bash
   pnpm knip
   ```
   用于检测未使用的文件、导出项和依赖关系。在重大重构后运行此工具。

5. **预提交检查** — 在提交前使用 `husky` 和 `lint-staged` 运行 ESLint 和 Prettier。

### iOS/Android 项目的质量检查工具

**iOS（Swift）：**
```bash
swiftlint lint --strict
swift-format format --in-place --recursive Sources/
```

**Android（Kotlin）：**
```bash
./gradlew detekt
./gradlew ktlintCheck
```

这两个平台都使用 `lefthook` 作为预提交钩子（与编程语言无关，无需 Node.js）。

### 4. TDD 工作流程（如果 `workflow.md` 中启用了 TDD）

**红色标记** — 编写失败的测试用例：
- 为任务功能创建或更新测试文件。
- 运行测试以确保测试失败。

**绿色标记** — 实现代码，使测试通过。
- 运行测试以确认代码正确无误。

**重构：**
- 在测试仍然通过的情况下进行代码重构。
- 最后再次运行测试。

### 5. 非 TDD 工作流程（如果 TDD 设置为“none”或“moderate”且任务简单）
- 直接实现任务。
- 运行现有测试以确保代码没有问题。
- 对于需要编写测试的逻辑和 API 路由，执行相应的测试；对于 UI 和配置相关的任务，可以跳过这一步。

### 5.5. 集成测试（优先使用 CLI）
如果任务涉及核心业务逻辑（如管道、算法或代理工具），运行 `make integration` 命令（或 `docs/workflow.md` 中指定的集成测试命令）。该命令会在不依赖浏览器的情况下执行相同的代码路径。如果 `make integration` 失败，请在提交前修复问题。

### 5.6. 可视化验证（如果可用浏览器/模拟器）
在实现代码后，如果工具可用，执行快速可视化测试：

**Web 项目（使用 Playwright 或浏览器工具）：**
- 如果有 Playwright 或浏览器工具：
  - 如果开发服务器尚未启动，请启动它（检查 `stack.yaml` 中的 `dev_server_command` 设置）。
  - 导航到受当前任务影响的页面。
  - 检查浏览器控制台是否有错误（如渲染问题、未捕获的异常或 404 错误）。
  - 截取屏幕截图以验证视觉效果是否符合预期。
  - 如果任务涉及响应式布局，将浏览器窗口大小调整到 375px 并进行验证。

**iOS 项目（使用模拟器）：**
- 如果管道提示中要求使用 iOS 模拟器：
  - 构建模拟器版本：`xcodebuild -scheme {Name} -sdk iphonesimulator build`
  - 安装模拟器应用：`xcrun simctl install booted {app-path}`
  - 截取模拟器屏幕截图：`xcrun simctl io booted screenshot /tmp/sim-screenshot.png`
  - 检查模拟器日志：`xcrun simctl spawn booted log stream --style compact --timeout 10`

**Android 项目（使用模拟器）：**
- 如果管道提示中要求使用 Android 模拟器：
  - 构建调试 APK：`./gradlew assembleDebug`
  - 安装模拟器应用：`adb install -r app/build/outputs/apk/debug/app-debug.apk`
  - 截取模拟器屏幕截图：`adb exec-out screencap -p > /tmp/emu-screenshot.png`
  - 检查模拟器日志：`adb logcat '*:E' --format=time -d 2>&1 | tail -20`

**优雅降级策略：** 如果浏览器/模拟器/模拟器工具不可用或出现故障，可以跳过可视化测试。可视化测试是可选的，但不是必须的。记录跳过的原因后继续执行任务。

### 6. 完成任务
**提交代码**（遵循指定的提交格式）：
```bash
git add {specific files changed}
git commit -m "<type>(<scope>): <description>"
```

提交代码时使用的标签类型：`feat`、`fix`、`refactor`、`test`、`docs`、`chore`、`perf`、`style`

**提交后记录哈希值（SHA）：**
```bash
git rev-parse --short HEAD
```

**在 `plan.md` 中记录提交哈希值：** 每次提交任务后：
1. 将任务状态从 `[~]` 更改为 `[x]`。
2. 在提交信息中添加哈希值：`- [x] Task X.Y: description <!-- sha:abc1234 -->`

如果没有记录哈希值，将无法追踪任务进度，也无法回滚更改。如果一个任务需要多次提交，请记录最后一次提交的哈希值。

### 7. 阶段完成检查
完成当前阶段的所有任务后：
1. **检查所有任务的完成状态**：
  - 扫描该阶段中所有标记为 `[x]` 的任务。如果发现有未完成的任务（例如 `<!-- sha:... -->`），请从 git 日志中获取其哈希值并添加到 `plan.md` 中。每个标记为 `[x]` 的任务都必须有哈希值。
2. 运行该阶段下的验证步骤。
3. 运行完整的测试套件。
4. 运行代码格式检查工具（linter）。
5. 在 `plan.md` 中更新任务状态：`- [ ]` → `[x]`。
6. 提交 `plan.md` 以更新阶段进度：`git commit -m "chore(plan): complete phase {N}"`。
7. 记录阶段检查点的哈希值并添加到 `plan.md` 的阶段标题中：
   `## Phase N: Title <!-- checkpoint:abc1234 -->`。
8. 报告结果并继续执行下一个阶段：
```
Phase {N} complete! <!-- checkpoint:abc1234 -->

  Tasks:  {M}/{M}
  Tests:  {pass/fail}
  Linter: {pass/fail}
  Verification:
    - [x] {check 1}
    - [x] {check 2}

  Revert this phase: git revert abc1234..HEAD
```

系统会自动进入下一个阶段。无需额外审批。

## 错误处理

### 测试失败
```
Tests failing after Task X.Y:
  {failure details}

1. Attempt to fix
2. Rollback task changes (git checkout)
3. Pause for manual intervention
```
通过 AskUserQuestion 获取用户确认后再继续执行。

## 阶段完成
当所有阶段和任务都标记为 `[x]` 时：
### 1. 执行最终验证
  - 在部署之前，必须运行本地构建：
    - Next.js：`pnpm build`
    - Python：`uv build` 或 `uv run python -m pyCompile src/**/*.py`
    - Astro：`pnpm build`
    - Cloudflare：`pnpm build`
    - iOS：`xcodebuild -scheme {Name} -sdk iphonesimulator build`
    - Android：`./gradlew assembleDebug`
  - 运行完整的测试套件。
  - 运行代码格式检查工具（linter）和类型检查工具。
  - 如果有可视化测试工具，执行可视化测试：
    - Web 项目：启动开发服务器，导航到目标页面，检查控制台是否有错误并截图。
    - iOS 项目：构建并安装模拟器应用，启动模拟器并截图。
    - Android 项目：构建 APK 并安装到模拟器上，然后截图并检查日志。
  - 如果工具不可用，可以跳过这一步。

### 2. 更新 `plan.md` 的头部信息
将 `**Status:** [ ] Not Started` 更改为 `**Status:** [x] Complete`。

### 3. 发出完成信号
仅在执行过程中触发一次完成信号：
```
<solo:done/>
```
**请不要在响应中重复显示完成信号。** 只执行一次。

### 4. 总结
```
Track complete: {title} ({trackId})

  Phases: {N}/{N}
  Tasks:  {M}/{M}
  Tests:  All passing

  Phase checkpoints:
    Phase 1: abc1234
    Phase 2: def5678
    Phase 3: ghi9012

  Revert entire track: git revert abc1234..HEAD

Next:
  /build {next-track-id}  — continue with next track
  /plan "next feature"    — plan something new
```

## 回滚代码
`plan.md` 中的哈希值注释支持精确的代码回滚操作：

**回滚单个任务：**
```bash
# Find SHA from plan.md: - [x] Task 2.3: ... <!-- sha:abc1234 -->
git revert abc1234
```
然后更新 `plan.md`，将该任务的状态从 `[x]` 更改为 `[ ]`。

**回滚整个阶段：**
```bash
# Find checkpoint from phase heading: ## Phase 2: ... <!-- checkpoint:def5678 -->
# Find previous checkpoint: ## Phase 1: ... <!-- checkpoint:abc1234 -->
git revert abc1234..def5678
```
然后更新 `plan.md`，将该阶段的所有任务的状态从 `[x]` 更改为 `[ ]`。

**请勿使用 `git reset --hard`——始终使用 `git revert` 以保留代码历史记录。**

## 进度跟踪（TodoWrite）
在构建会话开始时，根据 `plan.md` 创建任务列表以便随时查看进度：
1. **会话开始时：** 阅读 `plan.md`，找到所有未完成的任务（标记为 `[ ]` 和 `[~]`）。
2. 为每个阶段创建相应的任务条目。
3. 在执行任务时更新任务状态：开始任务时标记为 `in_progress`，完成任务后标记为 `completed`。
4. 这样用户和系统可以实时了解进度。

## 常见问题及解决方法

| 常见问题 | 解决方法 |
|---------|---------|
| “这个任务太简单，不需要测试” | 简单的代码也可能出错。编写测试用例。 |
| “我稍后再写测试” | 测试应在代码通过后立即编写——否则测试毫无意义。 |
| “我已经手动测试过了” | 手动测试无法长期保持有效性。请编写自动化测试。 |
| “测试框架还没有设置” | 快速设置测试框架——这是任务的一部分。 |
| “这只是配置更改” | 配置更改可能会影响构建过程。请进行验证。 |
| “我相信代码没问题” | 仅凭直觉行事是不可靠的。请先实际运行代码。 |
| “我先尝试修改某些内容” | 先找出根本原因再动手修改。 |
| “测试通过了，就可以发布了” | 测试通过并不代表满足了验收标准。请再次检查需求文档。 |
| “我稍后再处理代码格式问题” | 立即修复代码格式问题。否则技术债务会逐渐累积。 |
| “在我的机器上可以正常运行” | 在实际环境中运行代码进行验证。 |

## 重要规则

1. **执行阶段检查** — 在进入下一个阶段之前，确保所有测试和代码格式检查都通过。
2. **遇到错误时停止** — 遇到测试失败或错误时不要继续执行。
3. **随时更新 `plan.md` — 任务状态必须准确反映实际进度。
4. **每次完成任务后都提交代码** — 使用常规的提交格式。
5. **编写代码前先进行搜索** — 花 30 秒进行搜索可以避免后续的重复工作。
6. **一次完成一个任务** — 完成一个任务后再开始下一个任务。
7. **保持测试输出简洁** — 运行测试时使用 `head -50` 或 `--reporter=dot` / `-q` 标志来限制输出内容。避免显示大量测试结果。
8. **确认完成前进行验证** — 在标记任务完成之前，实际运行相关命令并查看完整输出结果。切勿仅凭直觉判断任务是否完成。 |

## 常见问题及解决方法

### “未找到计划”
**原因：** `docs/plan/` 或 `4-opportunities/` 目录下没有 `plan.md` 文件。
**解决方法：** 先运行 `/plan "your feature"` 命令来创建任务列表。

### 任务执行后测试失败
**原因：** 实现代码破坏了现有功能。
**解决方法：** 按照错误处理流程操作：尝试修复问题，必要时回滚代码，等待用户确认后再继续。切勿跳过失败的测试。

### 阶段检查失败
**原因：** 在阶段切换时测试或代码格式检查工具失败。
**解决方法：** 在继续执行之前修复错误，并重新运行该阶段的验证测试。
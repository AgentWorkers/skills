---
name: solo-build
description: 使用 TDD（测试驱动开发）工作流程、自动提交（auto-commit）和阶段检查（phase gates）来执行实施计划中的任务。当用户发出“构建它”（build it）、“开始构建”（start building）、“执行计划”（execute plan）、“实施任务”（implement tasks）或提及某个跟踪 ID（track ID）时，可以使用此流程。**请勿将其用于规划**（请使用 /plan）或搭建开发框架**（请使用 /scaffold）。
license: MIT
metadata:
  author: fortunto2
  version: "2.2.1"
  openclaw:
    emoji: "🔨"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, AskUserQuestion, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query, mcp__solograph__web_search, mcp__context7__resolve-library-id, mcp__context7__query-docs
argument-hint: "[track-id] [--task X.Y] [--phase N]"
---
# /build

此技能是独立的——请遵循下面的任务循环、TDD规则和完成流程，而不是依赖于外部构建/执行工具（如“超级能力”等）。

从实施计划中执行任务。找到`plan.md`文件（位于`docs/plan/`目录下），选择下一个未完成的任务，使用TDD工作流程来实现它，然后提交代码并更新进度。

## 使用场景

在`/plan`创建了包含`spec.md`和`plan.md`的跟踪文件后，可以使用此技能。这是执行引擎。

执行流程：`/plan` → **`/build`** → `/deploy` → `/review`

## MCP工具（如果可用）

- `session_search(query)` — 查找之前如何解决类似问题的方法
- `project_code_search(query, project)` — 在项目中查找可重用的代码
- `codegraph_query(query)` — 检查文件依赖关系和导入项

如果MCP工具不可用，则使用Glob、Grep和手动查找方法。

## 预执行检查

1. **确定上下文** — 找到计划文件的所在位置：
   - 检查`docs/plan/*/plan.md` — 标准位置
   - 仅在此目录内查找。

2. 从`docs/workflow.md`（如果存在）加载工作流程配置：
   - TDD的严格程度（严格/中等/无）
   - 提交策略（常规提交格式）
   - 验证检查点规则
   - **集成测试部分** — 如果存在，在完成涉及这些路径的任务后运行指定的CLI命令
   如果`docs/workflow.md`缺失：使用默认设置（中等严格度的TDD，常规提交）。

3. **验证是否安装了git钩子：**

   阅读`templates/stacks/{stack}.yaml`文件中的配置——`pre_commit`字段会告诉你使用的是哪个系统及其执行的命令：
   - `husky + lint-staged` — 用于JS/TS项目（eslint + prettier + tsc）
   - `pre-commit` — 用于Python项目（ruff + ruff-format + ty）
   - `lefthook` — 用于移动项目（swiftlint/detekt + formatter）

   然后验证钩子系统是否处于活动状态：
   ```bash
   # husky
   [ -f .husky/pre-commit ] && git config core.hooksPath | grep -q husky && echo "OK" || echo "NOT ACTIVE"
   # pre-commit (Python)
   [ -f .pre-commit-config.yaml ] && [ -f .git/hooks/pre-commit ] && echo "OK" || echo "NOT ACTIVE"
   # lefthook
   [ -f lefthook.yml ] && lefthook version >/dev/null 2>&1 && echo "OK" || echo "NOT ACTIVE"
   ```

   **如果未激活——在首次提交前安装：**
   - 对于husky：`pnpm prepare`（或`npm run prepare`
   - 对于pre-commit：`uv run pre-commit install`
   - 对于lefthook：`lefthook install`

   在提交时不要使用`--no-verify`选项——如果钩子失败，请修复问题后再提交。

## 跟踪选择

### 如果`$ARGUMENTS`包含跟踪ID：
- 验证：`{plan_root}/{argument}/plan.md`是否存在（在`docs/plan/`目录中检查）。
- 如果找不到：在`docs/plan/*/plan.md`中查找匹配项，并提供修改建议。

### 如果`$ARGUMENTS`包含`--task X.Y`：
- 直接跳转到当前活动跟踪中的该任务。

### 如果没有参数：
1. 在`docs/plan/`目录中查找`plan.md`文件。
2. 阅读每个`plan.md`文件，找到未完成任务的跟踪。
3. 如果有多个未完成的任务，通过AskUserQuestion询问用户。
4. 如果没有找到任何跟踪：提示“未找到计划，请先运行 `/plan`”。

## 上下文加载

### 第一步 — 架构概览（如果MCP可用）
```
codegraph_explain(project="{project name}")
```
返回：项目使用的技术栈、编程语言、目录结构、关键模式、主要依赖项以及核心文件——通过一次调用即可获取这些信息，无需手动遍历项目结构。

### 第二步 — 必读文档
1. `docs/plan/{trackId}/plan.md` — 任务列表（必需）
2. `docs/plan/{trackId}/spec.md` — 接受标准（必需）
3. `docs/workflow.md` — TDD策略和提交策略（如果存在）
4. `CLAUDE.md` — 架构指南（“应该/不应该做什么”）
5. `.solo/pipelines/progress.md` — 之前迭代中运行的文档（如果存在，特定于某个管道的）。其中包含已完成的工作内容：已完成的阶段、提交哈希值（SHA）、最后的输出信息。**使用这些信息避免重复工作。**

**在此阶段不要阅读源代码文件。** 只阅读文档。源代码将在执行循环（第三步）中按任务逐个加载。

## 任务恢复

如果`plan.md`中的某个任务被标记为`[~]`：

```
Resuming: {track title}
Last task: Task {X.Y}: {description} [in progress]

1. Continue from where we left off
2. Restart current task
3. Show progress summary first
```

通过AskUserQuestion询问用户后，再继续执行。

## 任务执行循环

**Makefile约定：** 如果项目根目录下存在`Makefile`，**始终优先使用`make`命令**，而不是直接使用`pnpm`命令。例如，使用`make test`代替`pnpm test`，`make lint`代替`pnpm lint`等。运行`make help`（或阅读`Makefile`）以了解可用的命令。如果存在`make integration`之类的命令，可以在与管道相关的任务之后使用它进行集成测试。

**重要提示：** 在进入循环之前，检查`plan.md`中是否有任何标记为`[-]`或`[~]`的任务。如果所有任务都标记为`[x]`，则直接跳到**完成**部分，执行最终验证并输出`<solo:done/>`。

对于`plan.md`中标记为`[ ]`的未完成任务，按以下步骤操作：

### 1. 找到下一个任务
解析`plan.md`，找到以`[-] Task X.Y:`（或在恢复任务时使用`[-] Task X.Y:`）开头的行。

### 2. 开始任务
- 更新`plan.md`：将当前任务的状态从`[ ]`更改为`[~]`。
- 公布任务开始信息：`**"开始执行任务X.Y: {描述}"`

### 3. 预先研究（智能地，避免全盘搜索）**
**不要在整个项目中搜索或阅读所有源代码。** 只加载当前任务所需的文件。

**如果MCP工具可用（推荐使用）：**
1. `project_code_search(query="{task keywords}", project="{name}")` — 在项目中查找相关代码。仅阅读前2-3个结果。
2. `session_search("{task keywords}")` — 检查之前是否已经处理过这个任务。
3. `codegraph_query("MATCH (f:File {project: '{name}'})-[:IMPORTS]->(dep) WHERE f.path CONTAINS '{module}' RETURN dep.path")` — 检查你将要修改的文件的依赖关系。

**如果MCP工具不可用（备用方案）：**
1. 仅阅读任务描述中明确提到的文件路径。
2. 使用Grep查找任务目标的具体模块目录（例如`src/auth/**/*.ts`），而不是整个项目目录。
3. 如果任务中没有提到具体的文件路径，使用`src/`或`app/`目录下的文件进行搜索。**绝对不要使用`**/*`这样的通配符**。

**绝对不要**：在整个项目中使用`Grep "keyword" .`，这会无谓地生成大量不必要的输出信息。要精确地查找所需文件。

### Python项目的质量检查工具

当项目使用Python技术栈时（通过`pyproject.toml`或`stack YAML`识别）：
运行完整的Astral工具链：

1. **Ruff** — 代码格式检查（始终执行）：
   ```bash
   uv run ruff check --fix .
   uv run ruff format .
   ```

2. **ty** — 类型检查（如果`devDependencies`或`stack YAML`中包含`ty`）：
   ```bash
   uv run ty check .
   ```
   `ty`是Astral提供的类型检查工具（速度非常快，可以替代`mypy/pyright`）。
3. **Hypothesis** — 基于属性的测试（如果`dependencies`中包含`hypothesis`）：
   - 使用`@given(st.from_type(MyModel))`自动生成Pydantic模型输入。
   - 使用`@given(st.text(), st.integers())`进行边界条件测试。
   - 测试代码应与常规pytest测试放在同一个测试文件中。

**提交前执行所有钩子：**
```bash
   uv run pre-commit run --all-files
   ```

在每次任务实现后、提交代码之前运行这些检查。如果有任何检查失败，请先修复问题后再提交。

### JS/TS项目的质量检查工具

当项目使用JavaScript/TypeScript技术栈时（通过`package.json`或`stack YAML`识别）：
1. **ESLint** — 代码格式检查（始终执行）：
   ```bash
   pnpm lint --fix
   ```

2. **Prettier** — 代码格式化（始终执行）：
   ```bash
   pnpm format
   ```

3. **tsc --noEmit** — 类型检查（严格模式）：
   ```bash
   pnpm tsc --noEmit
   ```
   在提交前修复类型错误。确保`tsconfig.json`中启用了严格模式。

4. **Knip** — 代码冗余检测（如果`devDependencies`中包含`Knip`）：
   ```bash
   pnpm knip
   ```
   用于检测未使用的文件、导出项和依赖项。在重大重构后运行此工具。

**提交前执行以下操作：**
   使用`husky + lint-staged`对暂存文件执行ESLint和Prettier。

### iOS/Android项目的质量检查工具

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

这两种情况都使用`lefthook`作为提交前的钩子工具（与编程语言无关，不需要Node.js）。

### 4. TDD工作流程（如果`workflow.md`中启用了TDD）**

**红色标记** — 编写失败的测试用例：
- 为任务的功能创建或更新测试文件。
- 运行测试以确保测试失败。

**绿色标记** — 实现代码：
- 编写最少的代码以使测试通过。
- 运行测试以确认代码能够正常工作。

**重构：**
- 在测试仍然显示为绿色状态时进行重构。
- 最后再次运行测试。

### 5. 非TDD工作流程（如果`workflow.md`中设置的是“none”或“moderate”且任务简单）**
- 直接实现任务。
- 运行现有的测试以确保没有问题。
- 对于需要编写测试的逻辑和API接口，也要编写相应的测试。

### 5.5. 集成测试（优先使用CLI）
如果任务涉及核心业务逻辑（如管道、算法或代理工具），运行`make integration`（或`docs/workflow.md`中的相应命令）。这个命令会在不依赖浏览器的情况下执行相同的代码路径。如果`make integration`失败，请在提交前修复问题。

### 5.6. 可视化验证（如果可用浏览器/模拟器）**

在实现代码后，如果工具可用，执行快速可视化测试：

**Web项目（使用Playwright或浏览器工具）：**
- 如果有Playwright或浏览器工具：
  - 如果开发服务器尚未运行，请启动它（检查`stack YAML`中的`dev_server.command`）。
  - 导航到受当前任务影响的页面。
  - 检查浏览器控制台是否有错误（如渲染问题、未捕获的异常、404错误）。
  - 截取屏幕截图以验证视觉效果是否符合预期。
  - 如果任务涉及响应式布局，将屏幕分辨率调整为移动设备的视口大小（375px）并检查效果。

**iOS项目（使用模拟器）：**
- 如果脚本中指示使用iOS模拟器：
  - 构建模拟器版本：`xcodebuild -scheme {Name} -sdk iphonesimulator build`
  - 在模拟器上安装应用：`xcrun simctl install booted {app-path}`
  - 截取屏幕截图：`xcrun simctl io booted screenshot /tmp/sim-screenshot.png`
  - 检查模拟器日志：`xcrun simctl spawn booted log stream --style compact --timeout 10`

**Android项目（使用模拟器）：**
- 如果脚本中指示使用Android模拟器：
  - 构建调试APK：`./gradlew assembleDebug`
  - 安装应用：`adb install -r app/build/outputs/apk/debug/app-debug.apk`
  - 截取屏幕截图：`adb exec-out screencap -p > /tmp/emu-screenshot.png`
  - 检查模拟器日志：`adb logcat '*:E' --format=time -d 2>&1 | tail -20`

**优雅地处理异常情况：** 如果浏览器/模拟器/模拟器工具不可用或出现故障，可以跳过可视化测试。可视化测试是可选的，但不是必须的。记录下未执行的步骤并继续执行任务。

### 6. 完成任务**

**提交代码**（遵循提交规则）：
```bash
git add {specific files changed}
git commit -m "<type>(<scope>): <description>"
```

提交代码时使用的标签类型：`feat`、`fix`、`refactor`、`test`、`docs`、`chore`、`perf`、`style`

**提交后记录哈希值：**
```bash
git rev-parse --short HEAD
```

**在`plan.md`中记录提交哈希值：** 每次提交任务后：
1. 将任务状态从`[~]`更改为`[x]`。
2. 在提交信息中附上哈希值：`- [x] Task X.Y: 描述 <!-- sha:abc1234 -->`

如果没有记录哈希值，将无法追踪任务进度，也无法回滚修改。如果一个任务需要多次提交，请记录最后一次提交的哈希值。

### 7. 阶段完成检查**

完成每个任务后，检查当前阶段的所有任务是否都标记为`[x]`。

如果阶段已完成：
1. **检查所有`[x]`任务的哈希值**：
  - 扫描该阶段的所有`[x]`任务。如果发现有未记录哈希值的任务，请从git日志中获取它们的哈希值并添加进去。每个`[x]`任务都必须有对应的哈希值。
2. 运行该阶段下的验证步骤。
3. 运行完整的测试套件。
4. 运行代码格式检查工具（linter）。
5. 在`plan.md`中更新状态标记：`- [ ]` → `[x]`。
6. 提交`plan.md`以更新进度：`git commit -m "chore(plan): complete phase {N}"`。
7. 记录阶段的检查点哈希值并添加到`plan.md`中：
  `## Phase N: 标题 <!-- checkpoint:abc1234 -->`。
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
通过AskUserQuestion询问用户。遇到错误时不要自动继续执行任务。

## 阶段完成

当所有阶段和任务都标记为`[x]`时：
### 1. 最终验证
  - **执行本地构建**：在部署之前必须通过所有测试：
    - Next.js：`pnpm build`
    - Python：`uv build`或`uv run python -m pyCompile src/**/*.py`
    - Astro：`pnpm build`
    - Cloudflare：`pnpm build`
    - iOS：`xcodebuild -scheme {Name} -sdk iphonesimulator build`
    - Android：`./gradlew assembleDebug`
  - 运行完整的测试套件。
  - 运行代码格式检查工具（linter）。
  - **执行可视化测试**（如果工具可用）：
    - Web项目：启动开发服务器，导航到受影响的页面，检查控制台是否有错误，截取屏幕截图。
    - iOS项目：在模拟器上构建并安装应用，然后截取屏幕截图。
    - Android项目：构建APK并安装到模拟器上，然后截取屏幕截图并检查日志。
  - 如果工具不可用，可以跳过这一步。
  - 检查`spec.md`中规定的接受标准是否满足。

### 2. 更新`plan.md`头部信息
将`**Status:** [ ] Not Started`更改为`**Status:** [x] Complete`。

### 3. 发送完成信号
只有当`.solo/states/`目录存在时，才发送完成信号：
```
<solo:done/>
```
**请不要在响应的其他部分重复发送完成信号。** 只发送一次。

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

## 回滚操作

`plan.md`中的哈希值注释支持精确的回滚操作：

**回滚单个任务：**
```bash
# Find SHA from plan.md: - [x] Task 2.3: ... <!-- sha:abc1234 -->
git revert abc1234
```
然后更新`plan.md`中的任务状态：将`[x]`更改为`[ ]`。

**回滚整个阶段：**
```bash
# Find checkpoint from phase heading: ## Phase 2: ... <!-- checkpoint:def5678 -->
# Find previous checkpoint: ## Phase 1: ... <!-- checkpoint:abc1234 -->
git revert abc1234..def5678
```
然后更新`plan.md`中的所有任务状态：将整个阶段的`[x]`更改为`[ ]`。

**永远不要使用`git reset --hard`** — 应始终使用`git revert`来保留代码历史记录。

## 进度跟踪（TodoWrite）

在构建会话开始时，根据`plan.md`创建任务列表，以便随时查看进度：
1. **会话开始时：** 阅读`plan.md`，找到所有未完成的任务（标记为`[ ]`或`[~]`）。
2. 为每个阶段创建相应的`TaskCreate`任务。
3. 在执行任务时更新任务状态：开始任务时标记为`in_progress`，完成任务后标记为`completed`。
4. 这样可以让用户和构建系统实时了解进度。

## 避免常见错误的思考方式

以下是一些可能导致错误的思维模式及相应的正确做法：

| 错误思维 | 正确做法 |
|---------|---------|
| “这个代码太简单，不需要测试” | 简单的代码也可能出错。编写测试用例。 |
| “我稍后添加测试” | 测试应该在代码通过后立即编写——否则测试毫无意义。 |
| “我已经手动测试过了” | 手动测试无法长期保持有效性。应该编写自动化测试。 |
| “测试框架还没设置好” | 需要设置测试框架。这是任务的一部分。 |
| “这只是配置更改” | 配置更改可能会影响构建过程。务必进行验证。 |
| “我相信代码没问题” | 仅凭直觉行事是不够的。先实际运行代码再下结论。 |
| “我直接修改代码就行” | 先找出问题的根本原因再动手修改。 |
| “测试通过了，就可以发布了” | 测试通过并不代表满足了需求。请检查`spec.md`中的接受标准。 |
| “我稍后修复格式问题” | 现在就修复格式问题。否则技术债务会逐渐累积。 |
| “在我的机器上运行没问题” | 在实际环境中测试代码是否正常工作。 |

## 重要规则

1. **完成每个阶段的检查** — 在进入下一个阶段之前，确保所有测试和代码格式检查都通过。
2. **遇到错误时停止** — 遇到测试失败或错误时不要继续执行。
3. **随时更新`plan.md` — 任务状态必须准确反映实际进度。
4. **每次完成任务后都提交代码** — 使用常规的提交格式。
5. **编写代码前先进行充分研究** — 花30秒搜索可以避免后续的重复工作。
6. **一次只完成一个任务** — 完成一个任务后再开始下一个任务。
7. **保持测试输出简洁** — 运行测试时使用`head -50`或`--reporter=dot`/`-q`选项来限制输出内容。避免显示大量的测试结果。
8. **确认无误后再标记任务完成** — 在标记任务完成之前，先实际运行测试并查看完整输出结果。**

## 常见问题及解决方法

### “找不到计划”
**原因：** `docs/plan/`目录下没有`plan.md`文件。
**解决方法：** 先运行`/plan "your feature"`来创建相应的跟踪文件。

### 任务执行后测试失败
**原因：** 实现代码破坏了现有功能。
**解决方法：** 按照错误处理流程操作：尝试修复问题，必要时回滚代码，等待用户确认后再继续。切勿跳过失败的测试。

### 阶段检查失败
**原因：** 在阶段转换时测试或代码格式检查工具失败。
**解决方法：** 在继续之前先修复失败的问题，并重新运行该阶段的验证测试。
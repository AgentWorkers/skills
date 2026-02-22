---
name: solo-review
description: >
  **最终代码审查与质量把关流程**  
  - 运行测试，检查代码覆盖率；  
  - 审查代码的安全性；  
  - 核实代码是否符合规格书中的验收标准；  
  - 生成可供发布的代码报告。  
  **适用场景**：  
  当用户提出“审查代码”、“进行质量检查”或询问“代码是否准备好发布”时，或者在执行 `/deploy` 命令后，应使用此流程。  
  **注意**：  
  - 本流程仅用于代码的最终审核和质量控制，不适用于项目规划（请使用 `/plan`）或代码构建（请使用 `/build`）。
license: MIT
metadata:
  author: fortunto2
  version: "1.1.1"
  openclaw:
    emoji: "🔎"
allowed-tools: Read, Grep, Bash, Glob, Write, Edit, mcp__solograph__session_search, mcp__solograph__project_code_search, mcp__solograph__codegraph_query, mcp__solograph__codegraph_explain, mcp__solograph__web_search, mcp__context7__resolve-library-id, mcp__context7__query-docs
argument-hint: "[focus-area]"
---
# /review

此技能是独立完成的——请按照以下说明进行操作，无需依赖外部审核工具或生成子任务代理。所有检查均需直接执行。

这是发布前的最终质量把关环节，包括运行测试、检查安全性、验证 `spec.md` 中规定的验收标准、审核代码质量，并生成一份包含通过/不通过判断的发布准备报告。

## 使用时机

在执行 `/deploy`（或手动部署时执行 `/build`）之后。这是质量控制的最后一道关卡。

流程：`/deploy` → **`/review`**

也可以单独使用：对任何项目执行 `/review` 以审核代码质量。

## MCP 工具（如有可用）

- `session_search(query)` — 查找以往的审核模式和常见问题
- `project_code_search(query, project)` — 在项目中查找相似的代码模式
- `codegraph_query(query)` — 检查依赖关系、导入的代码及未使用的代码

如果 MCP 工具不可用，可以退而使用全局搜索（Glob）+ 正则表达式匹配（Grep）+ 手动阅读代码的方法。

## 预检

### 1. 架构概览（如果 MCP 可用）
```
codegraph_explain(project="{project name}")
```
返回：技术栈、使用的语言、目录结构、关键模式、主要依赖项、核心文件。利用这些信息来了解项目的技术架构。

### 2. 必需文档（并行阅读）
- `CLAUDE.md` — 架构规范、行为准则
- `docs/plan/*/spec.md` — 需要验证的验收标准
- `docs/plan/*/plan.md` — 任务完成状态
- `docs/workflow.md` — TDD（测试驱动开发）政策、质量标准、**集成测试命令**（如果存在）

**在此阶段** **切勿阅读源代码**，仅查看文档。

### 3. 确定技术栈
根据 `codegraph_explain` 的返回结果（或在没有 MCP 时参考 `CLAUDE.md`）选择相应的工具：
- Next.js → `npm run build`, `npm test`, `npx next lint`
- Python → `uv run pytest`, `uv run ruff check`
- Swift → `swift test`, `swiftlint`
- Kotlin → `./gradlew test`, `./gradlew lint`

### 4. 智能源代码加载（用于代码质量抽查）

**不要随机阅读源代码**，而是通过代码图谱找到最重要的代码文件：

```
codegraph_query("MATCH (f:File {project: '{name}'})-[e]-() RETURN f.path, COUNT(e) AS edges ORDER BY edges DESC LIMIT 5")
```

仅阅读最重要的 3-5 个核心文件（这些文件对项目影响最大）。进行安全检查时，使用精确的正则表达式（如 `sk_live`, `password\s*=`）进行搜索，**无需完整阅读文件内容**。

## 审核维度

**Makefile 规范：** 如果项目根目录下存在 `Makefile`，**始终优先使用 `make` 命令**，例如 `make test` 而不是 `npm test`，`make lint` 而不是 `pnpm lint`。运行 `make help`（或阅读 `Makefile`）以了解可用的命令，包括集成测试命令。

按顺序执行所有 12 个审核维度，并报告每个维度的检查结果。

### 1. 测试套件

运行完整的测试套件（如果存在 `Makefile`，建议使用 `make test`）：
```bash
# If Makefile exists — use it
make test 2>&1 || true

# Fallback: Next.js / Node
npm test -- --coverage 2>&1 || true

# Python
uv run pytest --tb=short -q 2>&1 || true

# Swift
swift test 2>&1 || true
```

报告：
- 总测试数量：通过/失败/跳过的测试数量
- 覆盖率（如果可用）
- 失败的测试及其对应的文件和行号

**集成测试**：如果 `docs/workflow.md` 中有“集成测试”章节，请运行其中指定的命令：
- 执行相应的 CLI/集成测试命令
- 确认命令的退出代码是否符合预期
- 报告命令的运行结果、退出代码以及测试是否通过

### 2. 代码检查工具（Linter）与类型检查
```bash
# Next.js
pnpm lint 2>&1 || true
pnpm tsc --noEmit 2>&1 || true

# Python
uv run ruff check . 2>&1 || true
uv run ty check . 2>&1 || true

# Swift
swiftlint lint --strict 2>&1 || true

# Kotlin
./gradlew detekt 2>&1 || true
./gradlew ktlintCheck 2>&1 || true
```

报告：警告数量、错误数量以及主要问题。

### 3. 构建验证
```bash
# Next.js
npm run build 2>&1 || true

# Python
uv run python -m py_compile src/**/*.py 2>&1 || true

# Astro
npm run build 2>&1 || true
```

报告：构建是否成功、是否存在任何警告。

### 4. 安全审计
**依赖项漏洞：**
```bash
# Node
npm audit --audit-level=moderate 2>&1 || true

# Python
uv run pip-audit 2>&1 || true
```

**代码级检查**（使用正则表达式查找常见问题）：
- 硬编码的秘密信息：`grep -rn "sk_live\|sk_test\|password\s*=\s*['\"]" src/ app/ lib/`
- SQL 注入：检查查询语句中是否存在字符串拼接
- XSS（跨站脚本攻击）：检查是否存在未经过清理的 `dangerouslySetInnerHTML`
- 暴露的环境变量：检查 `.gitignore` 文件中是否包含 `.env*` 文件

报告发现的漏洞及其严重程度。

### 5. 验证验收标准

阅读 `docs/plan/*/spec.md`，并检查每个验收标准：

对于 `spec.md` 中的每个 `- [ ]` 标记：
1. 在代码库中查找该标准的实现证据。
2. 确认是否存在相关的测试用例。
3. 将相关标准标记为已验证或未验证。

**更新 `spec.md` 中的标记**。验证每个标准后，使用编辑工具将 `- [ ]` 更改为 `- [x]`。如果未验证的标准仍然存在，可能会导致后续流程出现问题，请及时处理。

```
Acceptance Criteria:
  - [x] User can sign up with email — found in app/auth/signup/page.tsx + test
  - [x] Dashboard shows project list — found in app/dashboard/page.tsx
  - [ ] Stripe checkout works — route exists but no test coverage
```

更新标记后，执行提交操作：`git add docs/plan/*/spec.md && git commit -m "docs: update spec checkboxes (verified by review)"`

### 6. 代码质量抽查

阅读 3-5 个关键文件（入口点、API 路由、主要组件）：
- 检查是否存在待处理的 TODO/FIXME/HACK 注释
- 检查生产代码中是否还保留了 `console.log`/`print` 语句
- 检查错误处理是否正确（是否使用了 try/catch 语句、是否有适当的错误处理机制）
- 检查用户界面组件的错误状态是否正确

报告具体文件和行号中的问题。

### 7. 计划完成情况检查

阅读 `docs/plan/*/plan.md`：
- 统计已完成的任务数量（标记为 `[x]`）与总任务数量
- 标记出尚未完成的任务（标记为 `[ ]` 或 `[~]`）
- 确认所有阶段检查点是否都有对应的 SHA 值

### 8. 生产环境日志（如果已部署）

如果项目已部署（`CLAUDE.md` 中有部署 URL，或者存在 `solo/states/deploy` 文件），**检查生产环境日志以查找运行时错误**。

从 `templates/stacks/{stack}.yaml` 文件中的 `logs` 字段获取特定平台的命令。

**Vercel（Next.js）：**
```bash
vercel logs --output=short 2>&1 | tail -50
```
查找：`Error`, `FUNCTION_INVOCATION_FAILED`, `504` 等错误
**Cloudflare Workers：**
```bash
wrangler tail --format=pretty 2>&1 | head -50
```
查找：未捕获的异常、D1 错误、R2 访问失败
**Fly.io（Python API）：**
```bash
fly logs --app {name} 2>&1 | tail -50
```
查找：`ERROR`, `CRITICAL`, OOM（内存溢出）错误、连接失败
**Supabase Edge Functions：**
```bash
supabase functions logs --scroll 2>&1 | tail -30
```

**iOS（TestFlight）：**
- 查看 App Store Connect 和 TestFlight 的日志，检查是否有崩溃情况
- 如果使用本地设备：`log stream --predicate 'subsystem == "com.{org}.{name}"`

**Android：**
```bash
adb logcat '*:E' --format=time 2>&1 | tail -30
```
- 查看 Google Play Console 的 Android Vitals 部分，检查是否有崩溃或 ANR（应用程序崩溃）情况

**如果尚未部署**：跳过此步骤，并在报告中注明“N/A — 未部署”。

**如果日志中显示错误**：
- 对错误进行分类：启动时崩溃、运行时错误或间歇性错误
- 将这些问题标记为“需要优先修复”（FIX FIRST）
- 在报告中附上具体的日志行作为证据

报告：
- 检查的日志来源（平台、使用的命令）
- 发现的错误类型及数量
- 错误类型（重复出现还是偶发）
- 错误状态（CLEAN / WARN / ERRORS）

### 9. 开发原则遵守情况

检查项目是否遵循开发原则。可以参考 `templates/principles/dev-principles.md`（随此技能一起提供），或查看 `CLAUDE.md` 和项目文档中的架构及编码规范。

阅读开发原则文件，然后抽查 3-5 个关键源文件，检查是否存在违规情况：

**SOLID 原则：**
- **SRP（单一职责原则）**：是否存在一个类/模块同时负责多个职责（例如认证、配置文件、邮件处理和通知功能）？
- **DIP（依赖注入原则）**：服务是通过依赖注入实现的，还是直接硬编码的？
- **DRY（干杯原则）与规则三原则**：是否存在重复的逻辑代码？
- **KISS（简单原则）**：是否存在为一次性操作设计的复杂抽象？
- **Schemas-First（模式优先原则）**：是否在逻辑之前定义了 Pydantic/Zod 数据结构？或者直接传递原始数据？
- **Clean Architecture（清晰架构原则）**：依赖项是否指向内部模块？业务逻辑是否独立于框架？
- **错误处理**：对于无效输入是否立即反馈错误？错误信息是否友好显示？内部错误是否有堆栈跟踪？

报告：
- 遵循的原则：列出所有被发现的违规情况
- 违规的具体位置及文件和行号
- 问题的严重程度：MINOR（风格问题）/ MAJOR（架构问题）/ CRITICAL（数据丢失风险）

### 10. 提交代码的质量

检查当前功能的 Git 提交历史记录：
```bash
git log --oneline --since="1 week ago" 2>&1 | head -30
```

**常规提交格式：**
- 每个提交都遵循 `<type>(<scope>): <description>` 的格式
- 类型包括：`feat`（新增功能）、`fix`（修复问题）、`refactor`（重构）、`test`（测试）、`docs`（文档更新）、`chore`（杂务）、`perf`（性能优化）、`style`（代码风格调整）
- 注意提交信息中的通用格式（如“fix”、“update”、“wip”、“changes”），以及格式不规范（如标题过长）

**原子性原则**：
- 每个提交是否只包含一个逻辑变更？还是包含多个无关功能的复杂提交？
- 提交是否易于回滚？能否通过 `git revert` 单个提交来恢复到之前的状态？

**`plan.md` 中的 SHA 值：**
- 确认已完成的任务是否带有 `<!-- sha:abc1234 -->` 的注释
- 确认阶段检查点是否带有 `<!-- checkpoint:abc1234 -->` 的注释

```bash
grep -c "sha:" docs/plan/*/plan.md 2>/dev/null || echo "No SHAs found"
```

**提交前钩子（Pre-commit hooks）**

阅读 `stack YAML` 文件中的 `pre_commit` 字段，了解系统要求（如 husky/pre-commit/lefthook）以及应执行的工具（如代码检查工具、格式化工具、类型检查工具）。然后进行验证：

```bash
# Detect what's configured
[ -f .husky/pre-commit ] && echo "husky" || [ -f .pre-commit-config.yaml ] && echo "pre-commit" || [ -f lefthook.yml ] && echo "lefthook" || echo "none"
```

- **钩子是否已安装？** 确认配置文件存在，并且钩子能够正常工作（husky 使用 `core.hooksPath`，pre-commit 使用 `.git/hooks/pre-commit`）。
- **钩子是否与系统要求匹配？** 比较实际系统与 `stack YAML` 中的 `pre_commit` 字段是否一致。如果不一致，请标记为问题。
- **是否跳过了某些钩子？** 如果最近有提交忽略了钩子的执行（例如未捕获的代码检查错误），请标记为警告。
- **配置是否正确？** 如果系统要求使用 `--no-verify` 选项，但实际未配置钩子，请标记为警告。

报告：
- 总提交数量：{N}
- 符合常规格式的提交数量：{N}/{M}
- 原子性良好的提交数量：YES / NO（并举例说明违规情况）
- 计划阶段检查点是否都有对应的 SHA 值：{N}/{M}
- 是否配置了提交前钩子：{ACTIVE / NOT INSTALLED / NOT CONFIGURED}（预期配置：{stack pre_commit})

### 11. 文档更新情况

检查项目文档是否与代码保持同步。

**需要检查的文件：**
```bash
ls -la CLAUDE.md README.md docs/prd.md docs/workflow.md 2>&1
```

**CLAUDE.md：**
- 文档是否反映了当前的技术栈、使用的命令和目录结构？
- 最新添加的功能/端点是否已记录在文档中？
- 使用正则表达式查找过时的引用（如旧的包名、已移除的文件）：
  ```bash
  # Check that files mentioned in CLAUDE.md actually exist
  grep -oP '`[a-zA-Z0-9_./-]+\.(ts|py|swift|kt|md)`' CLAUDE.md | while read f; do [ ! -f "$f" ] && echo "MISSING: $f"; done
  ```

**README.md：**
- 文档中是否包含设置/运行/测试/部署的说明？
- 文档中的命令是否能够实际执行？

**docs/prd.md：**
- 文档中描述的功能是否与实际实现的内容一致？
- 是否定义了相应的指标和成功标准？

**AICODE-注释：**
```bash
grep -rn "AICODE-TODO" src/ app/ lib/ 2>/dev/null | head -10
grep -rn "AICODE-ASK" src/ app/ lib/ 2>/dev/null | head -10
```
- 标记出已完成但未清理的 `AICODE-TODO` 任务
- 标记出未回答的 `AICODE-ASK` 问题
- 检查复杂或难以理解的逻辑部分是否有相关的 `AICODE-NOTE` 注释

**废弃代码检查：**
- 未使用的导入语句（代码检查工具应该能检测到，但也需要人工确认）
- 是否有未被使用的文件
- 如果使用 `knip` 工具（Next.js）：`pnpm knip 2>&1 | head -30` 可以删除不必要的文件

报告：
- `CLAUDE.md` 的更新情况：CURRENT / STALE / MISSING
- `README.md` 的更新情况：CURRENT / STALE / MISSING
- `docs/prd.md` 的更新情况：CURRENT / STALE / MISSING
- `docs/workflow.md` 的更新情况：CURRENT / STALE / MISSING
- 未解决的 `AICODE-TODO` 任务数量：{N}
- 未回答的 `AICODE-ASK` 问题数量：{N}
- 废弃的代码文件数量：{N}

### 12. 可视化/端到端测试

如果项目支持浏览器工具或设备测试工具，请进行可视化测试。

**Web 项目（使用 Playwright MCP 或浏览器工具）：**
1. 启动开发服务器（使用 `stack YAML` 中的 `dev_server_command`，例如 `pnpm dev`）
2. 使用 Playwright MCP 工具（或浏览器工具）导航到主页面
3. 确保页面加载时没有控制台错误、渲染问题或 React 相关的问题
4. 浏览 2-3 个关键页面（根据 `spec.md` 中的描述）
5. 在桌面（1280px）和移动设备（375px）视口中截图
6. 检查页面是否有图像损坏、样式错误或布局问题

**iOS 项目（使用模拟器）：**
1. 使用 `xcodebuild -scheme {Name} -sdk iphonesimulator build` 命令构建模拟器
2. 安装并在模拟器上运行应用程序
3. 截取主界面的截图
4. 检查模拟器日志中是否有崩溃或异常

**Android 项目（使用模拟器）：**
1. 使用 `./gradlew assembleDebug` 命令构建 APK
2. 在模拟器上安装并运行应用程序
3. 截取主界面的截图
4. 检查日志中是否有崩溃或异常

**如果缺少相关工具**：在报告中注明“N/A — 项目未部署，因此无法进行可视化测试”。可视化测试本身不会影响发布的决定。

报告：
- 测试的平台：{browser / simulator / emulator / N/A}
- 检查的页面数量：{N}
- 控制台错误数量：{N}
- 可视化问题情况：{NONE / LIST}
- 测试结果：{PASS / WARN / FAIL / N/A}

## 审核报告

生成最终报告：
```
Code Review: {project-name}
Date: {YYYY-MM-DD}

## Verdict: {SHIP / FIX FIRST / BLOCK}

### Summary
{1-2 sentence overall assessment}

### Tests
- Total: {N} | Pass: {N} | Fail: {N} | Skip: {N}
- Coverage: {N}%
- Status: {PASS / FAIL}

### Linter
- Errors: {N} | Warnings: {N}
- Status: {PASS / WARN / FAIL}

### Build
- Status: {PASS / FAIL}
- Warnings: {N}

### Security
- Vulnerabilities: {N} (critical: {N}, high: {N}, moderate: {N})
- Hardcoded secrets: {NONE / FOUND}
- Status: {PASS / WARN / FAIL}

### Acceptance Criteria
- Verified: {N}/{M}
- Missing: {list}
- Status: {PASS / PARTIAL / FAIL}

### Plan Progress
- Tasks: {N}/{M} complete
- Phases: {N}/{M} complete
- Status: {COMPLETE / IN PROGRESS}

### Production Logs
- Platform: {Vercel / Cloudflare / Fly.io / N/A}
- Errors: {N} | Warnings: {N}
- Status: {CLEAN / WARN / ERRORS / N/A}

### Dev Principles
- SOLID: {PASS / violations found}
- Schemas-first: {YES / raw data found}
- Error handling: {PASS / issues found}
- Status: {PASS / WARN / FAIL}

### Commits
- Total: {N} | Conventional: {N}/{M}
- Atomic: {YES / NO}
- Plan SHAs: {N}/{M}
- Status: {PASS / WARN / FAIL}

### Documentation
- CLAUDE.md: {CURRENT / STALE / MISSING}
- README.md: {CURRENT / STALE / MISSING}
- AICODE-TODO unresolved: {N}
- Dead code: {NONE / found}
- Status: {PASS / WARN / FAIL}

### Visual Testing
- Platform: {browser / simulator / emulator / N/A}
- Pages/screens: {N}
- Console errors: {N}
- Visual issues: {NONE / list}
- Status: {PASS / WARN / FAIL / N/A}

### Issues Found
1. [{severity}] {description} — {file:line}
2. [{severity}] {description} — {file:line}

### Recommendations
- {actionable recommendation}
- {actionable recommendation}
```

**判断逻辑：**
- **SHIP**：所有测试通过，没有安全问题，满足验收标准，构建成功，生产环境日志正常，文档更新及时，提交操作符合规范，没有严重的可视化问题
- **FIX FIRST**：存在次要问题（警告、部分验收标准未满足、低严重度的安全漏洞、间歇性的日志错误、文档过时、提交格式不规范、轻微的 SOLID 原则违规、轻微的可视化问题）——列出需要修复的内容
- **BLOCK**：测试失败、存在安全漏洞、缺少关键功能、生产环境中出现崩溃、`CLAUDE.md`/`README.md` 丢失、存在严重的架构问题、应用程序在启动时崩溃（模拟器/设备上）——此时不应发布项目

## 审核后的 `CLAUDE.md` 修订

在生成审核报告后，修订项目的 `CLAUDE.md` 以保持其简洁性和实用性。

### 步骤：
1. **阅读 `CLAUDE.md` 并检查其长度：`wc -c CLAUDE.md`
2. **记录审核过程中的发现**：
   - 新发现的行为准则
   - 更新的命令、工作流程或架构决策
   - 修复的问题或需要注意的事项
   - 技术栈/依赖项的变化（新添加的依赖项、移除的依赖项）
3. **如果文档长度超过 40,000 个字符**：
   - 将已完成的阶段/里程碑记录压缩成一行
   - 删除冗长的描述，保留简洁且可操作的笔记
   删除重复的信息
   删除多余的说明（同一内容在多个地方出现的情况）
   删除过时的迁移说明和调试信息
   删除代码中已解决的问题相关的示例
4. **确保文档长度 ≤ 40,000 个字符**；如果仍超过这个限制，删除不必要的内容
5. **编写更新后的 `CLAUDE.md`，并更新“最后更新时间”

### 优先级（保留/删除的内容）：
1. **必须保留**：技术栈、目录结构、行为准则、常用命令、架构决策
2. **保留**：工作流程说明、未解决问题的调试信息、关键文件的引用
3. **压缩**：阶段记录（每条记录占一行）、详细的示例、工具/工具的列表
4. **首先删除**：历史记录、冗长的描述、重复的内容、已解决的问题

### 规则：
- **绝不要删除行为准则**——这些是重要的保障措施
- 保持整体的章节结构和顺序
- 每一条记录都必须有其存在的必要性：“未来的审核工具是否需要这些信息？”
- 提交更新后的 `CLAUDE.md`：`git add CLAUDE.md && git commit -m "docs: revise CLAUDE.md (post-review)"

## 在 `CLAUDE.md` 修订完成后——仅输出一次信号

**仅在存在流程状态目录（`.solo/states/`）的情况下输出信号。**

**只输出一次信号**。系统会自动检测到第一次输出。

**如果决定发布项目（SHIP）：**输出以下内容：
```
<solo:done/>
```

**如果决定先修复问题（FIX FIRST）或推迟发布（BLOCK）：**
1. 打开 `plan.md`，为每个问题添加新的修复任务（每个问题对应一个 `- [ ]` 标记）
2. 将 `plan.md` 中的任务状态从 `[x] Complete` 更改为 `[~] In Progress`
3. 提交更新：`git add docs/plan/ && git commit -m "fix: add review fix tasks"`
4. 再输出一次相同的信号：
```
<solo:redo/>
```

系统会自动读取这些信号并处理相应的标记文件。您无需手动创建或删除这些标记文件。

**只需输出一次信号**。系统会自动检测到第一次输出。

## 错误处理

### 测试无法执行
**原因**：缺少依赖项或测试配置错误
**解决方法**：运行 `npm install` / `uv sync`，并检查测试配置文件（如 `jest.config`、`pytest.ini`）是否存在。

### 代码检查工具未配置
**原因**：未找到代码检查工具的配置文件
**解决方法**：在报告中将其作为建议提及，但不会影响发布流程。

### 构建失败
**原因**：类型错误、导入问题、环境变量缺失
**解决方法**：报告具体的错误。这种情况属于必须修复的问题，否则项目无法发布。

## 两阶段审核流程

在审核重要功能时，分为两个阶段进行：

**第一阶段——规范符合性检查：**
- 实现是否满足 `spec.md` 中的要求？
- 所有的验收标准是否都得到了满足（而不仅仅是声称满足）？
- 如果存在差异，这些差异是合理的改进还是问题？

**第二阶段——代码质量检查：**
- 架构模式、错误处理、类型安全
- 测试覆盖率和测试质量
- 安全性和性能
- 代码的组织结构和可维护性

## 验证规则

**在没有最新验证结果的情况下，不得做出任何决定。**

在编写任何审核结果（SHIP/FIX/BLOCK）之前：
1. **实际运行** 测试/构建/代码检查命令（不要使用缓存的结果）。
2. **阅读** 完整的输出结果——包括退出代码、通过/失败的数量、错误信息。
3. **确认** 输出结果与实际情况一致。
4. **只有在确认结果准确无误后**，才能写出最终的审核结果。

**切勿仅凭主观判断编写审核结果**——必须实际运行测试并查看输出结果。

## 理性判断指南

| 预期情况 | 实际情况 |
|---------|---------|
| “之前测试通过了” | 代码可能已经发生变化，请重新运行测试。|
| “只是一个警告” | 即使是警告，也可能导致实际问题，请记录下来。|
| “本地测试通过了” | 需要检查实际的生产环境。环境差异可能会影响测试结果。|
| “安全扫描没有必要” | 即使暂时没有问题，也必须进行安全扫描。|
| “代码已经足够好了” | 需要通过具体数据来证明代码是否足够好。|
| “我已经检查过了” | 只有最新的测试结果才有参考价值。过时的检查结果毫无意义。|

## 重要规则

1. **必须执行所有检查**——即使项目看起来很简单，也不要跳过任何检查步骤。
2. **提供详细的信息**——必须提供问题的具体文件和行号。
3. **判断必须有依据**——每个发布/修复/推迟发布的决定都必须基于实际测试结果。
4. **不要自动修复代码**——将问题记录下来，并在 `plan.md` 中添加相应的修复任务。让构建工具（如 `/build`）来执行修复操作。审核过程仅修改 `plan.md`，不得直接修改源代码。
5. **确认验收标准** — `spec.md` 是判断项目是否完成的依据。
6. **安全性至关重要** — 任何硬编码的秘密信息都会导致项目无法发布。
7. **仅使用最新的测试结果** — 在做出任何决定之前，必须先运行相应的测试。
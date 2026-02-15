---
name: brownfield-analyzer
description: 分析现有的“棕地项目”（brownfield projects），以将文档内容映射到 SpecWeave 的结构中（包括 PRD、HLD、Spec 和 Runbook）。该工具适用于将现有项目迁移到 SpecWeave、扫描旧版文档或创建项目上下文映射时使用。能够识别外部工具（如 JIRA、ADO、GitHub），并支持增量式或全面的迁移方案。
---

# Brownfield Analyzer

**适用于任何现有代码库的独立 brownfield（旧系统/代码库）项目分析工具。**

---

## 目的

分析现有项目并制定迁移到 SpecWeave 结构的迁移计划。支持两种路径：快速启动（增量式）或全面分析（预先完成）。

---

## 两种迁移路径

### 路径 1：快速启动（推荐用于大型项目）

**适合**：代码量超过 5 万行（LOC），迭代速度快，团队规模较小

**流程**：
1. 初始扫描：记录核心架构（1-3 小时）
2. 立即开始工作
3. 每次迭代时：更新文档
4. 随着代码变更，文档也会相应更新

**优势**：
- 几天内即可启动迁移
- 专注于关键部分
- 避免分析过程中的停滞

### 路径 2：全面分析（预先完成）

**适合**：代码量少于 5 万行（LOC），团队规模适中，或处于受监管的行业

**流程**：
1. 进行全面分析（1-4 周）
2. 记录所有模块和业务规则
3. 创建基准测试
4. 然后开始逐步迁移

**优势**：
- 事先获取完整的项目背景信息
- 全面覆盖回归测试
- 便于团队协作
- 符合行业规范

### 自动推荐方案

| 项目规模 | 代码量（LOC） | 预先分析所需时间 | 推荐方案 |
|--------------|-----|----------------|-------------|
| 小型 | <10k | 4-8 小时 | 全面分析 |
| 中型 | 10k-50k | 1-2 周 | 用户自行选择 |
| 大型 | 50k-200k | 2-4 周 | 快速启动 |
| 特大型 | 200k+ | 1-3 个月 | 快速启动（强制要求） |

---

## 分析工作流程

### 第一步：项目评估

```bash
# Scan project
find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" | wc -l
find . -type f \( -name "*.ts" -o -name "*.js" \) -exec wc -l {} + | awk '{sum+=$1} END {print sum}'
```

**计算**：
- 文件总数
- 代码总量（LOC）
- 模块数量
- 测试覆盖率（如果有的话）

**输出**：
```
📊 Project Analysis
   Files: 1,245
   LOC: 45,678
   Modules: 23
   Tests: 45% coverage

💡 Recommendation: Medium project → User choice (Quick Start or Comprehensive)
```

### 第二步：文档分类

扫描相关文档：

**产品需求文档（PRD）**：
- `requirements.md`, `PRD.md`, `product-spec.md`
- `docs/product/`, `specs/requirements/`

**高级设计文档（HLD）**：
- `architecture.md`, `design.md`, `ARCHITECTURE.md`
- `docs/architecture/`, `docs/design/`

**架构决策记录（ADR）**：
- `adr/`, `decisions/`, `docs/decisions/`
- 名称中包含 “ADR-” 或 “decision” 的文件

**技术规范文档（Spec）**：
- `spec.md`, `technical-spec.md`
- `docs/specs/`, `docs/technical/`

**操作手册文档（Runbook）**：
- `runbook.md`, `operations.md`, `deployment.md`
- `docs/ops/`, `docs/runbooks/`

**图表文档**：
- `*.png`, `*.svg`, `*.drawio`, `*.mmd`
- `diagrams/`, `docs/diagrams/`

### 第三步：检测外部工具集成

**Jira 集成**：
```bash
# Search for Jira references
grep -r "JIRA" . --include="*.md" --include="*.txt"
grep -r "jira.atlassian" . --include="*.md"
```

**Azure DevOps**：
```bash
grep -r "dev.azure.com" . --include="*.md"
grep -r "visualstudio.com" . --include="*.md"
```

**GitHub Issues**：
```bash
grep -r "github.com/.*/issues" . --include="*.md"
```

### 第四步：检测编码规范

**自动检测**：
- ESLint 配置文件（`.eslintrc`, `eslint.config.js`）
- Prettier 配置文件（`.prettierrc`）
- TypeScript 配置文件（`tsconfig.json`）
- 测试配置文件（`vitest.config`, `jest.config`）

**分析编码规范**：
```bash
# Naming conventions
grep -rh "^export function" src/ | head -20
grep -rh "^export class" src/ | head -20

# Import patterns
grep -rh "^import" src/ | sort | uniq -c | sort -rn | head -10
```

### 第五步：生成迁移计划

**快速启动计划**：
```markdown
# Migration Plan: Quick Start Path

## Phase 1: Initial Setup (1-2 hours)
- [ ] Run `specweave init`
- [ ] Document core architecture only
- [ ] Create 1-2 ADRs for critical decisions

## Phase 2: First Increment (1-3 days)
- [ ] Select first feature to modify
- [ ] Document module before touching
- [ ] Create increment with /sw:increment
- [ ] Implement changes
- [ ] Update docs

## Phase 3: Iterate
- [ ] Repeat per feature
- [ ] Documentation grows organically
```

**全面分析计划**：
```markdown
# Migration Plan: Comprehensive Path

## Phase 1: Documentation Baseline (1-2 weeks)
- [ ] Map all modules to .specweave/docs/internal/modules/
- [ ] Create ADRs for major architectural decisions
- [ ] Document business rules
- [ ] Identify technical debt

## Phase 2: Test Baseline (1 week)
- [ ] Add baseline tests for core functionality
- [ ] Target 60-70% coverage
- [ ] Document test strategy

## Phase 3: Structure Migration (2-3 days)
- [ ] Run `specweave init`
- [ ] Migrate existing docs
- [ ] Organize by SpecWeave structure

## Phase 4: Ready for Increments
- [ ] Start feature work with full context
```

---

## 迁移检查清单

### 在使用 SpecWeave 之前

- [ ] 评估项目规模（代码量、文件数量）
- [ ] 选择迁移路径（快速启动或全面分析）
- [ ] 备份现有文档
- [ ] 确认是否存在外部工具集成
- [ ] 检查是否存在编码规范

### 在迁移过程中

**快速启动**：
- [ ] 仅记录核心架构
- [ ] 创建 1-2 个关键的架构决策记录（ADR）
- [ ] 设置外部工具同步（可选）
- [ ] 立即开始第一次迭代

**全面分析**：
- [ ] 扫描所有文档
- [ ] 对文档进行分类和整理
- [ ] 创建完整的模块文档
- [ ] 记录所有业务规则
- [ ] 为决策创建架构决策记录（ADR）
- [ ] 创建基准测试
- [ ] 设置外部工具同步

### 迁移完成后

- [ ] 确认 `.specweave/` 结构已正确创建
- [ ] 测试迁移后的工作流程
- [ ] 对团队进行 SpecWeave 使用培训
- [ ] 记录迁移过程中的决策

---

## 文档映射

**将现有文档映射到 SpecWeave 结构**：

```
Existing Structure          SpecWeave Structure
─────────────────          ───────────────────
docs/product/              .specweave/docs/internal/strategy/
docs/architecture/         .specweave/docs/internal/architecture/
docs/decisions/            .specweave/docs/internal/architecture/adr/
docs/specs/                .specweave/docs/internal/specs/
docs/runbooks/             .specweave/docs/public/runbooks/
docs/api/                  .specweave/docs/public/api-docs/
README.md                  .specweave/docs/public/README.md
CONTRIBUTING.md            .specweave/docs/public/CONTRIBUTING.md
```

---

## 外部工具迁移

### Jira → SpecWeave

**1. 检测 Jira 的使用情况**：
```bash
grep -r "jira" . --include="*.md" | head -5
```

**2. 映射 Jira 的工作项结构**：
- 项目（Epic）→ 特性（FS-XXX）
- 用户故事（Story）→ 用户故事（US-XXX）
- 任务（Task）→ 任务（T-XXX）

**3. 同步策略**：
```bash
# Option 1: Import existing Jira items
/sw-jira:sync --import

# Option 2: Start fresh, sync new work only
# (Use SpecWeave as source of truth)
```

### Azure DevOps → SpecWeave

**映射工作项**：
- 项目（Feature）→ 特性（FS-XXX）
- 用户故事（Story）→ 用户故事（US-XXX）
- 任务（Task）→ 任务（T-XXX）

**同步方式**：
```bash
/sw-ado:sync --import
```

### GitHub Issues → SpecWeave

**映射问题（Issue）**：
- 里程碑（Milestone）→ 特性（FS-XXX）
- 问题（Issue）→ 用户故事（US-XXX）
- 任务列表（Task List）→ 任务（T-XXX）

**同步方式**：
```bash
/sw-github:sync --import
```

---

## 最佳实践

**✅ 应该做**：
- 根据项目规模选择合适的迁移路径（大型项目推荐快速启动）
- 在修改代码之前先完成文档编写
- 采用增量式迁移方式
- 保留现有文档
- 对于已有的项目，使用外部工具进行同步
- 对团队进行 SpecWeave 工作流程培训

**❌ 不应该做**：
- 对代码量超过 10 万行的项目强制使用全面分析
- 删除现有文档
- 在快速启动模式下一次性迁移所有内容
- 忽略编码规范的检测
- 忽视外部工具的集成
- 在快速启动模式下过度分析项目细节

---

## 示例：大型项目迁移

**场景**：代码量 8.5 万行（Node.js 后端），使用 Jira，测试覆盖率 15%

**推荐方案**：快速启动

**迁移计划**：
```
Week 1: Setup (2 hours)
- Run specweave init
- Document core architecture (5 modules)
- Create 2 ADRs (database, API design)
- Configure Jira sync

Week 1-2: First Increment
- Select first feature: "Add rate limiting"
- Document rate-limiting module
- Create increment with /sw:increment
- Implement with TDD
- Update docs

Week 3+: Iterate
- Repeat per feature
- Documentation grows to 40% over 3 months
- Eventually covers critical paths
```

**结果**：2 小时后开始迁移，文档逐步完善。

---

## 示例：小型项目迁移

**场景**：代码量 8 千行（Python 应用），使用 GitHub Issues，测试覆盖率 60%

**推荐方案**：全面分析（预先完成）

**迁移计划**：
```
Week 1: Full Documentation (8 hours)
- Document all 5 modules
- Create 8 ADRs
- Map business rules
- Document API contracts

Week 1: Test Baseline (4 hours)
- Add missing unit tests (80% coverage)
- Document test strategy

Week 1: Structure Migration (2 hours)
- Run specweave init
- Migrate existing docs
- Configure GitHub sync

Week 2+: Start Increments
- Full context available
- High confidence changes
```

**结果**：2 周内完成所有文档的整理，之后可以顺利进行增量式迁移。

---

## 故障排除

**问题**：找不到现有文档**
**解决方法**：检查常见文档存放位置：`docs/`, `wiki/`, `.github/`, Notion 导出文件

**问题**：文档太多，难以分类**
**解决方法**：先重点处理架构相关的文档，忽略实现细节

**问题**：文档之间存在冲突**
**解决方法**：利用 Git 历史记录找到最新或权威的文档版本

**问题**：外部工具的 API 有使用限制**
**解决方法**：采用分批导入的方式，或限制同步频率

---

**此工具具有高度的独立性，适用于任何类型的 brownfield 项目。**
---
name: code-standards-analyzer
description: 根据现有的代码库模式生成并维护编码规范文档。在创建 STANDARDS.md 文件、为新开发者提供培训，或记录团队惯例时使用这些文档。采用基于事实的方法——编码规范应反映实际情况，而非理想化的要求。
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# 代码标准分析器

**用途**：通过基于证据的分析，发现、记录并维护现有代码库中的编码标准。

**理念**：标准应反映代码的实际行为，而非我们的期望；先进行测量，再形成文档。

---

## 使用场景

### 主要用途：
1. **旧代码库的适配** - “这个项目的编码规范是什么？”
2. **标准审计** - “我们是否遵循了声明的标准？”
3. **新贡献者的培训** - “向我介绍项目的编码模式”
4. **动态文档更新** - “保持标准与代码库的一致性”
5. **新项目的初始化** - “根据最佳实践设定标准”

### 触发激活的条件

**关键词**：分析编码标准、发现编码规范、代码风格、检测模式、编码指南、命名规范、最佳实践、代码质量、标准审计、反模式

**用户请求**：
- “这个项目的编码标准是什么？”
- “分析代码库并记录我们的编码规范”
- “检查我们是否遵循了声明的标准”
- “在代码中查找反模式”
- “生成编码标准文档”
- “这个项目使用什么命名规范？”

---

## 功能

### 1. **显式标准检测**（快速 - 5秒）
- ✅ 检测现有的 `.specweave/docs/internal/governance/coding-standards.md`
- ✅ 解析 ESLint 配置文件（`.eslintrc.json`, `.eslintrc.js`）
- ✅ 解析 Prettier 配置文件（`.prettierrc`, `.prettierrc.json`）
- ✅ 解析 TypeScript 配置文件（`tsconfig.json`）
- ✅ 解析 EditorConfig 文件（`.editorconfig`）
- ✅ 从 `CLAUDE.md`, `CONTRIBUTING.md` 中提取标准

### 2. **隐式标准检测**（中等速度 - 30秒）
- ✅ 命名规范分析（变量、函数、类、常量）
- ✅ 导入模式检测（扩展名、顺序、别名使用）
- ✅ 函数特性分析（平均长度、最大长度、箭头函数与普通函数）
- ✅ 类型安全分析（`any` 类型的使用、接口与类型的偏好）
- ✅ 错误处理模式分析（`try/catch` 的使用、自定义错误）
- ✅ 代码注释风格分析
- ✅ 文件组织模式分析

### 3. **反模式检测**（快速 - 15秒）
- 🚨 在生产代码中使用 `console.*` 函数
- 🚨 硬编码的敏感信息（API 密钥、密码）
- 🚨 过度使用 `any` 类型
- 🚨 文件过大（超过500行）
- 🚨 函数过长（超过100行）
- 🚨 缺少错误处理
- 🚨 N+1 查询模式
- 🚨 安全漏洞

### 4. **文档生成**（快速 - 10秒）
- ✅ 生成包含示例的标准文档
- ✅ 包含统计置信度
- ✅ 从代码库中提取实际代码示例
- ✅ 突出显示不一致性和冲突
- ✅ 提供可操作的改进建议
- ✅ 链接到违反标准的文件

---

## 分析流程

### 第一阶段：显式标准（5秒）

**检查的来源**：
1. `.specweave/docs/internal/governance/coding-standards.md`（高置信度）
2. `CLAUDE.md`（高置信度 - 由 AI 指令驱动）
3. `.eslintrc.json`（由工具强制执行）
4. `.prettierrc`（由工具强制执行）
5. `tsconfig.json`（由编译器强制执行）
6. `.editorconfig`（由编辑器强制执行）
7. `CONTRIBUTING.md`（中等置信度 - 可能已过时）

**输出**：
```markdown
## Explicit Standards Found

✅ .eslintrc.json (ENFORCED - ESLint active)
✅ .prettierrc (ENFORCED - Prettier active)
✅ tsconfig.json (ENFORCED - TypeScript compiler)
✅ CLAUDE.md (HIGH - AI development rules)
⚠️  CONTRIBUTING.md (MEDIUM - human guidelines)
❌ No .specweave/docs/internal/governance/coding-standards.md
```

### 第二阶段：隐式标准（30秒）

**执行的分析**：
- 扫描 `src/**/*.{ts,js,tsx,jsx}` 文件
- 解析抽象语法树（AST）
- 计算统计模式
- 识别主要的编码规范

**示例输出**：
```markdown
## Detected Patterns

### Naming Conventions (Confidence: 95%)
- Variables: camelCase (1,234 samples, 98% compliance)
- Functions: camelCase (567 samples, 100% compliance)
- Classes: PascalCase (89 samples, 100% compliance)
- Constants: UPPER_SNAKE_CASE (234 samples, 92% compliance)
  ⚠️ 8% use camelCase (inconsistency detected)

### Import Patterns (Confidence: 100%)
- Extensions: .js suffix required (100% compliance)
- Order: external → internal → types (87% compliance)

### Function Characteristics
- Average length: 35 lines
- Max length: 156 lines (src/core/analyzer.ts:45)
- Style: Arrow functions (78%), Regular (22%)

### Type Safety (Confidence: 85%)
- any usage: 12 instances (REVIEW NEEDED)
- Preference: Interfaces (89%) over Types (11%)
```

### 第三阶段：反模式检测（15秒）

**执行的检查**：
- 安全性：硬编码的敏感信息、SQL 注入风险
- 可维护性：文件过大、函数过于复杂
- 性能：N+1 查询、缺少缓存
- 稳健性：缺少错误处理

**示例输出**：
```markdown
## Issues Found

### 🔴 CRITICAL (2 issues)
- Hardcoded Secrets: 2 instances
  - src/config/api.ts:12
  - src/utils/auth.ts:45
  Fix: Use process.env variables

### 🟠 HIGH (5 issues)
- console.* Usage: 5 instances in src/
  - src/core/analyzer.ts:67
  Fix: Use logger abstraction

### 🟡 MEDIUM (12 issues)
- Large Files: 3 files > 500 lines
  - src/core/orchestrator.ts (678 lines)
  Fix: Split into modules
```

### 第四阶段：文档生成（10秒）

**合并策略**：
1. 显式标准作为权威依据
2. 隐式标准用于补充缺失的部分
3. 反模式作为警告和建议

**输出**：`.specweave/docs/internal/governance/coding-standards-analysis.md`

---

## 集成点

### 1. 旧代码库分析器的集成

**自动集成**：作为旧代码库分析的一部分运行

```
User: "Analyze this brownfield project"

Workflow:
1. Scan project structure
2. Classify documents
3. Detect external tools
4. → RUN code-standards-detective agent
5. → GENERATE coding-standards.md
6. Generate migration plan
```

### 2. 持续计划

**参考**：将标准纳入技术约束中

```markdown
## Technical Constraints

Coding Standards: .specweave/docs/internal/governance/coding-standards.md
- Naming: camelCase (vars), PascalCase (classes)
- Functions: < 50 lines target
- No console.* - use logger
```

### 3. 持续改进

**可选**：在代码库更新后重新分析

```bash
/sw:done 0046 --update-standards
```

---

## 使用示例

### 示例 1：首次分析

```
User: "What are the coding standards for this project?"

Skill: code-standards-analyzer

Actions:
1. Check for existing standards (none found)
2. Parse .eslintrc.json, .prettierrc
3. Analyze 1,234 TypeScript files
4. Detect patterns with 95% confidence
5. Generate standards document

Output:
"✅ Analysis complete! Generated coding standards at:
.specweave/docs/internal/governance/coding-standards-analysis.md

Key findings:
- Naming: 98% camelCase compliance
- Imports: 100% use .js extensions
- Issues: 5 console.* usages, 2 hardcoded secrets
- Recommendation: Formalize detected patterns as official standards"
```

### 示例 2：标准审计

```
User: "Check if we're following our declared standards"

Skill: code-standards-analyzer

Actions:
1. Read existing coding-standards.md
2. Analyze current codebase
3. Compare declared vs actual
4. Report violations

Output:
"📊 Standards Compliance: 87%

✅ Passing:
- Naming conventions: 98% compliant
- Import patterns: 100% compliant

⚠️ Violations:
- console.* usage: 12 instances (should be 0)
- Large files: 3 files > 500 lines (should be 0)

Recommendation: Fix violations or update standards to reflect reality"
```

### 示例 3：新贡献者培训

```
User: "I'm new to this codebase. What conventions should I follow?"

Skill: code-standards-analyzer

Actions:
1. Load existing coding-standards.md
2. Extract key rules with examples
3. Highlight SpecWeave-specific patterns

Output:
"📚 Coding Standards Summary

1. Naming:
   - Variables: camelCase (e.g., `userId`, `isActive`)
   - Functions: camelCase (e.g., `getUserById()`)
   - Classes: PascalCase (e.g., `UserService`)

2. Imports:
   - Always use .js extensions
   - Example: import { foo } from './bar.js'

3. Error Handling:
   - Use custom error types
   - Example: throw new UserNotFoundError(id)

4. Logging:
   - NEVER use console.*
   - Use logger abstraction instead

Full standards: .specweave/docs/internal/governance/coding-standards.md"
```

---

## 命令

### 手动分析

```bash
# Full analysis
/sw:analyze-standards

# Drift detection only
/sw:analyze-standards --drift

# Update existing standards
/sw:analyze-standards --update
```

---

## 输出文件

### 1. `coding-standards-analysis.md`（自动生成）

**位置**：`.specweave/docs/internal/governance/coding-standards-analysis.md`

**用途**：最新的分析报告（Git 中忽略，临时文件）

**内容**：
- 带有置信度的检测结果
- 实际代码示例
- 统计数据
- 违规警告
- 改进建议

### 2. `coding-standards.md`（权威标准）

**位置**：`.specweave/docs/internal/governance/coding-standards.md`

**用途**：官方编码标准（Git 跟踪，手动和自动生成）

**内容**：
- 命名规范
- 导入模式
- 函数指南
- 类型安全规则
- 错误处理
- 安全实践
- 性能指南

### 3. `coding-standards-history.md`（变更日志）

**位置**：`.specweave/docs/internal/governance/coding-standards-history.md`

**用途**：跟踪标准随时间的变化

**内容**：
- 每次分析的时间戳
- 发现的变更
- 迁移指南
- 更新的理由

---

## 最佳实践

### 1. 在新成员入职时进行分析
- 将标准分析作为旧代码库适配的一部分
- 生成基线文档
- 建立项目背景

### 2. 定期重新分析
- 每季度进行一次审查
- 在重大重构后进行审查
- 在新成员入职时进行培训

### 3. 需要团队共同审查
- 不要自动提交更改
- 审查生成的标准
- 讨论不一致之处
- 形成正式的决策

### 4. 动态文档更新
- 保持标准与代码的一致性
- 当模式发生变化时进行更新
- 在历史记录中跟踪变化

### 5. 通过工具强制执行
- 大多数标准通过 ESLint/Prettier 实现
- 对于工具无法检测到的问题，需要手动记录
- 重点关注 SpecWeave 特有的编码模式

---

## 相关文档

- [编码标准](.specweave/docs/internal/governance/coding-standards.md) - 官方标准
- [代码审查标准](.specweave/docs/internal/delivery/core/code-review-standards.md) - 审查流程
- [旧代码库分析器](../brownfield-analyzer/SKILL.md) - 项目分析工具

---

## 技术细节

### 支持的语言
- ✅ TypeScript（主要支持）
- ✅ JavaScript（ES6+）
- ✅ Python（`pyproject.toml`, `.pylintrc`, `ruff.toml`, `.flake8`, `mypy.ini`）
- ✅ Java/Kotlin（`checkstyle.xml`, `pmd.xml`, `spotbugs.xml`, `detekt.yml`）
- ✅ Go（`go.mod`, `.golangci.yml`, `staticcheck.conf`）
- ✅ C#/.NET（`.editorconfig`, `StyleCop.json`, `Directory.Build.props`）
- ✅ Rust（`rustfmt.toml`, `clippy.toml`, `Cargo.toml`）
- ✅ React（`package.json`, ESLint 插件：react/*）
- ✅ Angular（`angular.json`, ESLint @angular-eslint`）
- ✅ Vue（`package.json`, ESLint 插件：vue/*）
- ✅ Svelte（`package.json`, `svelte.config.js`）

### 检测算法

**命名规范检测**：
- 正则表达式匹配
- 统计频率分析
- 抽象语法树（AST）节点分析
- 置信度评分（样本数量 / 总样本数量）

**反模式检测**：
- 静态分析（grep、AST 解析）
- 基于规则的检查
- 安全性扫描
- 复杂性指标

**置信度等级**：
- **强制执行**：由代码检查工具/编译器强制执行的规则（100%符合）
- **高置信度**：代码库中90%以上符合标准
- **中等置信度**：70-89%符合标准
- **低置信度**：50-69%符合标准
- **冲突**：低于50%符合标准（存在不一致）

---

## 限制

1. **隐式标准**：需要具有代表性的代码样本
2. **误报**：反模式检测可能会标记出故意设计的代码
3. **上下文理解**：无法理解代码背后的业务逻辑

---

## 多技术支持

**状态**：✅ 已实现（版本 0122：多技术支持）

| 技术 | 配置文件 | 实现状态 |
|------------|--------------|--------|
| TypeScript/JavaScript | `.eslintrc.*`, `.prettierrc`, `tsconfig.json` | ✅ 已实现 |
| Python | `pyproject.toml`, `.pylintrc`, `ruff.toml`, `.flake8`, `mypy.ini` | ✅ 已实现 |
| Go | `go.mod`, `.golangci.yml`, `staticcheck.conf` | ✅ 已实现 |
| Java/Kotlin | `checkstyle.xml`, `pmd.xml`, `spotbugs.xml`, `detekt.yml` | ✅ 已实现 |
| C#/.NET | `.editorconfig`, `StyleCop.json`, `Directory.Build.props` | ✅ 已实现 |
| Rust | `rustfmt.toml`, `clippy.toml`, `Cargo.toml` | ✅ 已实现 |
| React | ESLint + `plugin:react/*`, `package.json` | ✅ 已实现 |
| Angular | `angular.json`, `.eslintrc` | ✅ 已实现 |
| Vue | ESLint + `plugin:vue/*`, `vite.config.*` | ✅ 已实现 |
| Svelte | `svelte.config.js`, `package.json` | ✅ 已实现 |

**输出结构**：
```
.specweave/docs/internal/governance/
├── coding-standards.md          # Unified summary of ALL technologies
├── shared-conventions.md        # EditorConfig, Git conventions
└── standards/
    ├── typescript.md
    ├── python.md
    ├── golang.md
    ├── java.md
    ├── react.md
    ├── angular.md
    ├── vue.md
    └── svelte.md
```

**使用方法**：
```typescript
import {
  detectEcosystems,
  parsePythonStandards,
  parseGoStandards,
  parseJavaStandards,
  parseFrontendStandards,
  generateStandardsMarkdown,
  generateUnifiedSummary
} from 'src/core/living-docs/governance/index.js';
```

---

## 未来改进计划

- [ ] 根据检测到的模式自动生成 ESLint 规则
- [ ] 从顶级开源项目中获取 AI 建议
- [ ] 在多项目中支持团队特定的标准
- [ ] 集成预提交钩子以强制执行标准
- [ ] 实时监控标准合规性
- [ ] 在不同项目间比较标准
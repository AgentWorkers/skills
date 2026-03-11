---
name: "code-reviewer"
description: TypeScript、JavaScript、Python、Go、Swift、Kotlin 的代码审查自动化工具。该工具能够分析 Pull Request 的复杂性和风险，检查代码质量是否存在 SOLID 原则的违反情况以及代码中的不良实践（即“代码异味”），并生成相应的审查报告。适用于在审查 Pull Request、分析代码质量、识别问题以及生成审查清单时使用。
---
# 代码审查工具

自动化代码审查工具，用于分析拉取请求（pull requests），检测代码质量问题，并生成审查报告。

---

## 目录

- [工具](#tools)
  - [PR 分析器](#pr-analyzer)
  - [代码质量检查器](#code-quality-checker)
  - [审查报告生成器](#review-report-generator)
- [参考指南](#reference-guides)
- [支持的语言](#languages-supported)

---

## 工具

### PR 分析器

分析分支之间的 Git 差异，以评估审查的复杂度并识别风险。

```bash
# Analyze current branch against main
python scripts/pr_analyzer.py /path/to/repo

# Compare specific branches
python scripts/pr_analyzer.py . --base main --head feature-branch

# JSON output for integration
python scripts/pr_analyzer.py /path/to/repo --json
```

**检测内容：**
- 硬编码的敏感信息（密码、API 密钥、令牌）
- SQL 注入漏洞（查询中的字符串拼接）
- 调试语句（如 `debugger`、`console.log`）
-禁用了 ESLint 规则
- TypeScript 中的 `any` 类型
- `TODO`/`FIXME` 注释

**输出内容：**
- 复杂度评分（1-10 分）
- 风险等级（严重、高、中、低）
- 需要审查的文件优先级
- 提交信息验证

---

### 代码质量检查器

分析源代码中的结构问题、代码异味以及违反 SOLID 设计原则的情况。

```bash
# Analyze a directory
python scripts/code_quality_checker.py /path/to/code

# Analyze specific language
python scripts/code_quality_checker.py . --language python

# JSON output
python scripts/code_quality_checker.py /path/to/code --json
```

**检测内容：**
- 过长的函数（超过 50 行）
- 过大的文件（超过 500 行）
- “上帝类”（包含过多方法的类）
- 过深的代码嵌套（超过 4 层）
- 参数过多（超过 5 个）
- 高循环复杂度
- 缺少错误处理
- 未使用的导入语句
- 魔数（即没有明确含义的常量）

**阈值：**

| 问题类型 | 阈值 |
|---------|--------|
| 过长的函数 | 超过 50 行 |
| 过大的文件 | 超过 500 行 |
| “上帝类” | 包含超过 20 个方法 |
| 参数过多 | 超过 5 个 |
| 过深的代码嵌套 | 超过 4 层 |
| 高循环复杂度 | 超过 10 个分支 |

---

### 审查报告生成器

将 PR 分析结果和代码质量检查的结果整合成结构化的审查报告。

```bash
# Generate report for current repo
python scripts/review_report_generator.py /path/to/repo

# Markdown output
python scripts/review_report_generator.py . --format markdown --output review.md

# Use pre-computed analyses
python scripts/review_report_generator.py . \
  --pr-analysis pr_results.json \
  --quality-analysis quality_results.json
```

**报告内容：**
- 审查结果（批准、请求修改、拒绝）
- 评分（0-100 分）
- 需要优先处理的操作事项
- 按严重程度分类的问题列表
- 建议的审查顺序

**评分标准：**

| 评分 | 审查结果 |
|-------|---------|
| 90 分及以上且无严重问题 | 批准 |
| 75 分及以上且严重问题不超过 2 个 | 批准并提供建议 |
| 50-74 分 | 请求修改 |
| 低于 50 分或有严重问题 | 拒绝 |

---

## 参考指南

### 代码审查检查表
`references/code_review_checklist.md`

系统化的检查表，涵盖以下方面：
- 审查前的准备工作（构建、测试、PR 编写规范）
- 代码的正确性（逻辑、数据处理、错误处理）
- 安全性（输入验证、防止注入攻击）
- 性能（效率、缓存、可扩展性）
- 可维护性（代码质量、命名规范、结构）
- 测试（测试覆盖率、测试质量、模拟测试）
- 语言特定的检查项

### 编码规范
`references/coding_standards.md`

针对不同语言的编码规范：
- TypeScript（类型注解、空值安全性、异步/等待（async/await）
- JavaScript（声明方式、代码模式、模块）
- Python（类型提示、异常处理、类设计）
- Go（错误处理、结构体、并发处理）
- Swift（可选值、协议、错误处理）
- Kotlin（空值安全性、数据类、协程）

### 常见反模式
`references/common_antipatterns.md`

反模式目录，包含示例及解决方法：
- 结构相关问题（“上帝类”、过长的方法、过深的代码嵌套）
- 逻辑相关问题（逻辑错误、硬编码的字符串类型）
- 安全相关问题（SQL 注入、硬编码的凭据）
- 性能相关问题（重复的查询、无限制的集合使用）
- 测试相关问题（代码重复、测试实现问题）
- 异步编程相关问题（悬而未决的 Promise、回调地狱）

---

## 支持的语言

| 语言 | 文件扩展名 |
|---------|---------|
| Python | `.py` |
| TypeScript | `.ts`, `.tsx` |
| JavaScript | `.js`, `.jsx`, `.mjs` |
| Go | `.go` |
| Swift | `.swift` |
| Kotlin | `.kt`, `.kts` |
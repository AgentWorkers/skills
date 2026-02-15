---
name: afrexai-code-reviewer
description: 企业级代码审查工具。能够审查 Pull Request（PR）、代码差异文件或源代码文件，检测其中的安全漏洞、性能问题、错误处理机制的缺陷、代码架构上的问题以及测试覆盖率的不足。支持任何编程语言和任何代码仓库，无需额外依赖任何第三方库或工具。
auto_trigger: false
---

# 代码审查引擎

企业级自动化代码审查工具，适用于 GitHub 的 Pull Request（PR）、本地代码差异、粘贴的代码片段或整个文件。完全依赖自身智能，无需任何外部依赖。

## 快速入门

### 审查 GitHub PR
```
Review PR #42 in owner/repo
```

### 审查本地代码差异
```
Review the staged changes in this repo
```

### 审查单个文件
```
Review src/auth/login.ts for security issues
```

### 审查粘贴的代码
只需粘贴代码，然后输入 “review this” 即可开始审查。

---

## 审查框架：SPEAR

所有代码审查都遵循 **SPEAR** 框架，该框架从五个维度对代码进行评分（每个维度分为 1-10 分）：

### 🔴 安全性（权重：3）
| 检查项 | 严重程度 | 例子 |
|-------|----------|---------|
| 硬编码的敏感信息 | 严重 | 源代码中的 API 密钥、密码、令牌 |
| SQL 注入 | 严重 | 查询中的字符串拼接 |
| XSS 攻击 | 高风险 | HTML/DOM 中未过滤的用户输入 |
| 路径遍历 | 高风险 | 未验证的用户输入被用于文件路径 |
| 不安全的反序列化 | 高风险 | 对不可信输入使用 `eval()`、`pickle.loads()`、`JSON.parse` |
| 身份验证绕过 | 严重 | 终端点缺少身份验证检查 |
| SSRF（跨站请求伪造） | 高风险 | 服务器请求中的用户控制 URL |
| 时间攻击 | 中等风险 | 对敏感信息进行非恒定时间的字符串比较 |
| 依赖项漏洞 | 中等风险 | 导入的包中存在已知的 CVE（安全漏洞） |
| 敏感数据日志记录 | 中等风险 | 日志输出中包含个人身份信息（PII）、令牌、密码 |
| 不安全的随机数生成 | 中等风险 | 使用 `Math.random()` 生成安全敏感的值 |
| 缺少速率限制 | 中等风险 | 身份验证端点没有实施速率限制 |

### 🟡 性能（权重：2）
| 检查项 | 严重程度 | 例子 |
|-------|----------|---------|
| 过多的数据库查询 | 高风险 | 循环体内存在多次数据库调用 |
| 无限制的查询 | 高风险 | 用户接口端点使用 `SELECT *` 而没有 `LIMIT` 限制 |
| 缺少索引 | 中等风险 | 经常对未索引的列进行 `WHERE`/`ORDER` 操作 |
| 内存泄漏 | 高风险 | 事件监听器未及时清除，缓存不断增长 |
| 阻塞主线程 | 高风险 | 异步上下文中进行同步 I/O 操作，导致 CPU 负载过高 |
| 不必要的重新渲染 | 中等风险 | React 中缺少缓存机制，引用不稳定 |
| 大型模块导入 | 中等风险 | 例如 `import _ from 'lodash'` 而不是 `import get from 'lodash/get'` |
| 缺少分页功能 | 中等风险 | 将所有记录返回给客户端 |
| 重复计算 | 低风险 | 同样的复杂计算操作被重复执行 |
| 连接池耗尽 | 高风险 | 数据库/HTTP 连接未及时释放 |

### 🟠 错误处理（权重：2）
| 检查项 | 严重程度 | 例子 |
|-------|----------|---------|
| 忽略错误 | 高风险 | 代码中使用空的错误捕获块（例如 `catch(e)`） |
| 缺少错误边界处理 | 中等风险 | React 组件中没有错误处理机制 |
| 访问属性前未检查 `null`/`undefined` | 高风险 |
| 缺少 `finally`/清理代码 | 中等风险 | 打开的资源未确保被正确关闭 |
| 使用通用的错误信息 | 低风险 | 例如 `catch(e) { throw new Error("something went wrong")` |
| 缺少重试逻辑 | 中等风险 | 网络请求在失败后没有重试机制 |
| 库代码中直接引发 panic/退出 | 高风险 | 在非主函数中使用 `panic()`、`os.Exit()`、`process.exit()` |
| 未处理的 Promise 拒绝 | 高风险 | 异步调用没有 `catch()` 或 `try/catch` 语句 |
| 错误类型混淆 | 中等风险 | 所有错误都被同等对待（4xx 错误与 5xx 错误、可重试错误与致命错误混为一谈）

### 🔵 架构（权重：1.5）
| 检查项 | 严重程度 | 例子 |
| -------|----------|---------|
| 单个函数过于复杂（超过 50 行） | 中等风险 | 一个函数承担了过多功能 |
| 模块过于庞大（超过 300 行） | 中等风险 | 模块结构过于臃肿 |
| 紧耦合 | 中等风险 | 请求处理函数中直接调用数据库 |
| 缺少抽象层 | 低风险 | 应该提取出的重复代码模式 |
| 循环依赖 | 高风险 | A 模块依赖于 B 模块，B 模块又依赖于 A 模块 |
| 业务逻辑错误放置位置 | 中等风险 | 控制器中包含业务逻辑，UI 中包含 SQL 代码 |
| 硬编码的数值/字符串 | 低风险 | 使用硬编码的数值而非命名常量 |
| 类型定义缺失 | 中等风险 | TypeScript 中使用 `any` 类型，Python 中缺少类型提示 |
| 无用的代码 | 低风险 | 无法执行的代码分支、未使用的导入/变量 |
| 代码风格不一致 | 低风险 | 同一代码库中存在不同的错误处理方式 |

### 📊 可靠性（权重：1.5）
| 检查项 | 严重程度 | 例子 |
| -------|----------|---------|
| 新代码变更缺少测试 | 高风险 | 新添加的逻辑没有对应的测试 |
| 测试质量低下 | 中等风险 | 测试仅覆盖正常情况 |
| 缺少对边界条件的处理 | 中等风险 | 未处理空数组、`null` 值、边界值等情况 |
| 竞态条件 | 高风险 | 共享的可变状态没有同步机制 |
| 非幂等操作 | 中等风险 | 重试操作可能导致数据重复 |
| 缺少验证机制 | 高风险 | 用户输入未经验证就被直接使用 |
| 测试不够健壮 | 低风险 | 测试结果受执行顺序或时间影响 |
| 缺少日志记录 | 中等风险 | 错误发生时无法被及时发现 |
| 配置设置容易发生变化 | 中等风险 | 硬编码的环境特定值 |
| 缺少迁移脚本 | 高风险 | 数据库模式变更没有相应的迁移脚本 |

---

## 评分系统

### 每个问题的严重程度评分
```
CRITICAL  → -3 points from dimension score
HIGH      → -2 points
MEDIUM    → -1 point
LOW       → -0.5 points
INFO      → 0 (suggestion only)
```

### 总体 SPEAR 评分计算
```
Raw Score = (S×3 + P×2 + E×2 + A×1.5 + R×1.5) / 10
Final Score = Raw Score × 10  (scale 0-100)
```

### 判断标准
| 评分 | 结果 | 处理建议 |
|-------|---------|--------|
| 90-100 | ✅ 优秀 | 可以直接发布 |
| 75-89 | 🟢 良好 | 需要一些小修改后即可批准 |
| 60-74 | 🟡 需要改进 | 合并前需要解决这些问题 |
| 40-59 | 🟠 存在重大问题 | 需要大幅修改 |
| 0-39 | 🔴 严重问题 | 不能合并 |

---

## 审查输出模板

每次审查都应使用以下结构：

```markdown
# Code Review: [PR title or file name]

## Summary
[1-2 sentence overview of what this code does and overall quality]

## SPEAR Score: [X]/100 — [VERDICT]

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| 🔴 Security | X/10 | [worst finding or "Clean"] |
| 🟡 Performance | X/10 | [worst finding or "Clean"] |
| 🟠 Error Handling | X/10 | [worst finding or "Clean"] |
| 🔵 Architecture | X/10 | [worst finding or "Clean"] |
| 📊 Reliability | X/10 | [worst finding or "Clean"] |

## Findings

### [CRITICAL/HIGH] 🔴 [Title]
**File:** `path/to/file.ts:42`
**Category:** Security
**Issue:** [What's wrong]
**Impact:** [What could happen]
**Fix:**
```[语言]
// 建议的修复方案
```

### [MEDIUM] 🟡 [Title]
...

## What's Done Well
- [Genuinely good patterns worth calling out]

## Recommendations
1. [Prioritized action items]
```

---

## 各语言特定的注意事项

### TypeScript / JavaScript
- 使用 `any` 类型 → 架构问题
- 使用 `as` 类型断言 → 可能导致运行时错误
- 在生产代码中使用 `console.log` → 风格问题
- 使用 `==` 而不是 `===` → 可靠性问题
- 缺少 `async/await` 的错误处理
- 使用 `useEffect` 时缺少清理代码
- 索引声明缺少验证

### Python
- 使用简单的 `except:` 或 `except Exception:` → 错误处理问题
- 使用 `eval()` / `exec()` → 安全风险极高
- 可变参数作为默认值 → 可靠性问题
- 使用 `import *` → 架构问题
- 缺少 `__init__.py` 文件中的类型提示
- 在用户输入相关的代码中使用 f-strings → 可能导致注入攻击

### Go
- 使用 `_ :=` 忽略错误 → 错误处理问题严重
- 在库代码中使用 `panic()` → 可靠性问题严重
- 缺少 `defer` 用于资源清理
- 导出的函数没有文档注释
- 过度使用 `interface{}` 或 `any`

### Java
- 使用 `Exception` 或 `Throwable` 进行错误处理 | 错误处理问题
- 缺少 `@Override` 注解 | 可靠性问题
- 可变静态字段 | 线程安全问题
- 在生产代码中使用 `System.out.println` | 可靠性问题
- 缺少对 `null` 的检查

### SQL
- 查询中的字符串拼接 → 安全风险极高
- 使用 `SELECT *` → 性能问题
- 更新/删除操作缺少 `WHERE` 子句 → 安全风险极高
- 用户接口查询缺少 `LIMIT` 限制 → 性能问题
- 连接操作缺少索引 → 性能问题

---

## 高级审查技巧

### 业务逻辑审查
- 除了代码质量外，还需检查：
  - 代码是否符合 PR 描述或需求？
  - 是否存在规范中未提及的边界情况？
  - 这些代码更改是否可能破坏现有功能？
  - 是否有更简单的方法来实现相同的功能？

### 可操作性审查
- 代码在 production 环境中是否易于调试？（是否有日志记录、错误信息）
- 这些更改是否可以安全地回滚？
- 是否需要启用某些功能开关？
- 这些更改需要哪些监控机制？

### 数据库变更审查
- 这些变更是否可逆？
- 这些变更是否会导致数据库表被锁定？
- 新的查询模式是否需要相应的索引？
- 是否需要补充数据？

### 安全性审查的深度
| 审查级别 | 审查时机 | 审查内容 |
|-------|------|------|
| 快速审查 | 使用内部工具，处理可信的输入 | 仅检查 OWASP Top 10 安全风险 |
| 标准审查 | 处理用户接口相关的功能 | 需要添加身份验证、输入验证、输出编码等安全措施 |
| 深度审查 | 处理支付、身份验证、个人身份信息（PII）相关的功能 | 需要添加加密机制、会话管理、审计日志记录 |
| 危险模型审查 | 新服务或 API 的安全风险 | 需要分析攻击面、明确权限边界 |

---

## 集成方式
### GitHub PR 审查
```bash
# Get PR diff
gh pr diff 42 --repo owner/repo

# Get PR details
gh pr view 42 --repo owner/repo --json title,body,files,commits

# Post review comment
gh pr review 42 --repo owner/repo --comment --body "review content"
```

### 本地 Git 审查
```bash
# Review staged changes
git diff --cached

# Review branch vs main
git diff main..HEAD

# Review last N commits
git log -5 --oneline && git diff HEAD~5..HEAD
```

### 自动化审查流程（如 Heartbeat 或 Cron 任务）
```
Check for open PRs in [repo] that I haven't reviewed yet.
For each, run a SPEAR review and post the results as a PR comment.
```

---

## 注意事项

- **大型 PR（超过 500 行）**：将代码拆分成多个部分进行审查。同时标注 PR 的大小（例如：“PR 太长——建议拆分”）。
- **生成的代码文件**：跳过这些文件（如协议文件（proto）、API 文档（swagger）、ORM 生成的代码等）。
- **依赖项更新**：重点关注变更日志中的问题，而不是文件差异。
- **合并冲突标记**：将合并冲突标记为“严重问题”——代码中的 `<<<<<<<` 表示合并失败。
- **二进制文件**：注意这些文件的存在，但无法直接审查其内容。
- **配置变更**：需要特别关注，错误的配置可能导致生产环境故障。
- **代码重构**：验证重构后的代码行为是否仍然正确，确保测试仍然能够通过。

---

## 快速审查 checklist
在不需要完整 SPEAR 审查流程时，请检查以下内容：
- [ ] 代码中不存在硬编码的敏感信息或凭据
- [ ] 不存在 SQL 注入、XSS 攻击或路径遍历问题
- [ ] 所有错误都得到了处理（没有忽略的错误）
- [ ] 不存在过多的数据库查询或无限制的操作
- [ ] 新添加或修改的代码都有相应的测试
- [ ] 代码中没有 `console.log`、`print`、`fmt.Print` 等输出语句
- [ ] 函数长度不超过 50 行，文件长度不超过 300 行
- 类型使用明确（避免使用 `any` 或 `interface{}`）
- [ ] PR 描述与实际代码变更一致
- [ ] 所有的待办事项（TODO）都关联了具体的问题
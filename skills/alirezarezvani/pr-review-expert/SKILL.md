---
name: "pr-review-expert"
description: "**PR Review Expert**
**概述：**  
PR Review Expert 是一款专为软件开发团队设计的专业代码审查工具，旨在帮助团队成员更高效地审查和批准 Pull Requests（PRs）。该工具提供了丰富的审查功能，包括代码质量检查、代码格式化指导、代码审查模板以及团队协作机制，从而确保代码质量的提升和项目进度的顺利推进。
**主要特性：**  
1. **代码质量检查：** 自动检测代码中的常见错误和潜在问题，如语法错误、代码风格不一致、未使用的导入语句等。  
2. **代码格式化：** 提供统一的代码格式化标准，确保所有代码遵循一致的编码规范。  
3. **审查模板：** 提供预设的审查模板，方便团队成员按照标准流程进行代码审查。  
4. **团队协作：** 支持实时聊天和评论功能，促进团队成员之间的沟通和协作。  
5. **报告生成：** 生成详细的审查报告，包括问题列表、修改建议以及代码审查的统计信息。  
6. **集成能力：** 可以与版本控制系统（如 Git）集成，实现代码审查的自动化流程。  
**使用场景：**  
- 适用于软件开发团队，尤其是那些需要高效管理代码审查流程的项目。  
- 有助于提高代码质量，减少代码漏洞和错误。  
- 促进团队成员之间的沟通和知识共享。  
**安装与配置：**  
PR Review Expert 可以通过官方网站下载并安装，具体安装步骤请参考官方文档。  
**更多信息：**  
- 官方网站：[PR Review Expert 官网](https://www.prreviewexpert.com/)  
- 用户手册：[用户手册](https://www.prreviewexpert.com/docs/)  
**注意事项：**  
- 请确保您的开发环境已安装必要的依赖库。  
- 根据项目需求配置相应的审查规则和模板。  
**下载链接：**  
[PR Review Expert 下载链接](https://www.prreviewexpert.com/download/)"
---
# PR审核专家

**级别：** 高级  
**类别：** 工程  
**领域：** 代码审核 / 质量保证  

---

## 概述  
该工具为GitHub的Pull Request（PR）和GitLab的Merge Request（MR）提供结构化、系统化的代码审核服务。其功能不仅限于检查代码风格，还包括进行范围影响分析、安全扫描、检测破坏性变更以及计算测试覆盖率的变化。审核完成后会生成一份包含30多项检查项的报告，其中问题会按优先级排序。  

---

## 核心功能  
- **范围影响分析**：追踪哪些文件、服务以及下游依赖可能会因此受到影响  
- **安全扫描**：检测SQL注入、XSS攻击、身份验证绕过、敏感信息泄露以及依赖项的安全漏洞  
- **测试覆盖率变化**：分析新增代码与新增测试之间的比例  
- **破坏性变更检测**：检查API接口、数据库架构迁移以及配置项的变更  
- **工单关联**：验证Jira或Linear工单的存在及其与审核范围的匹配性  
- **性能影响分析**：检测N+1查询、代码包大小的变化以及内存分配情况  

---

## 使用场景  
- 在合并涉及共享库、API或数据库架构更改的PR/MR之前  
- 当PR代码量较大（超过200行）且需要系统性审核时  
- 新成员提交的PR需要详细反馈时  
- 处理涉及身份验证、支付或个人身份信息（PII）处理的敏感代码路径时  
- 事件发生后，主动审查类似的PR  

---

## 获取代码差异  
### GitHub（gh CLI）  
```bash
# View diff in terminal
gh pr diff <PR_NUMBER>

# Get PR metadata (title, body, labels, linked issues)
gh pr view <PR_NUMBER> --json title,body,labels,assignees,milestone

# List files changed
gh pr diff <PR_NUMBER> --name-only

# Check CI status
gh pr checks <PR_NUMBER>

# Download diff to file for analysis
gh pr diff <PR_NUMBER> > /tmp/pr-<PR_NUMBER>.diff
```  
### GitLab（glab CLI）  
```bash
# View MR diff
glab mr diff <MR_IID>

# MR details as JSON
glab mr view <MR_IID> --output json

# List changed files
glab mr diff <MR_IID> --name-only

# Download diff
glab mr diff <MR_IID> > /tmp/mr-<MR_IID>.diff
```  

---

## 工作流程  
### 第1步：获取上下文信息  
```bash
PR=123
gh pr view $PR --json title,body,labels,milestone,assignees | jq .
gh pr diff $PR --name-only
gh pr diff $PR > /tmp/pr-$PR.diff
```  

### 第2步：范围影响分析  
对于每个被修改的文件，需要确定：  
1. **直接依赖项**：哪些文件依赖于该文件？  
```bash
# Find all files importing a changed module
grep -r "from ['\"].*changed-module['\"]" src/ --include="*.ts" -l
grep -r "require(['\"].*changed-module" src/ --include="*.js" -l

# Python
grep -r "from changed_module import\|import changed_module" . --include="*.py" -l
```  
2. **服务边界**：此次变更是否跨越了不同服务？  
```bash
# Check if changed files span multiple services (monorepo)
gh pr diff $PR --name-only | cut -d/ -f1-2 | sort -u
```  
3. **共享的接口和规范**：涉及的接口类型和数据库架构  
```bash
gh pr diff $PR --name-only | grep -E "types/|interfaces/|schemas/|models/"
```  

**范围影响严重程度分级：**  
- **严重**：涉及共享库、数据库模型、身份验证中间件或API接口  
- **较高**：被多个服务使用、共享配置或环境变量  
- **中等**：仅影响单个服务内部的变更或工具函数  
- **较低**：仅影响用户界面组件、测试文件或文档  

### 第3步：安全扫描  
```bash
DIFF=/tmp/pr-$PR.diff

# SQL Injection — raw query string interpolation
grep -n "query\|execute\|raw(" $DIFF | grep -E '\$\{|f"|%s|format\('

# Hardcoded secrets
grep -nE "(password|secret|api_key|token|private_key)\s*=\s*['\"][^'\"]{8,}" $DIFF

# AWS key pattern
grep -nE "AKIA[0-9A-Z]{16}" $DIFF

# JWT secret in code
grep -nE "jwt\.sign\(.*['\"][^'\"]{20,}['\"]" $DIFF

# XSS vectors
grep -n "dangerouslySetInnerHTML\|innerHTML\s*=" $DIFF

# Auth bypass patterns
grep -n "bypass\|skip.*auth\|noauth\|TODO.*auth" $DIFF

# Insecure hash algorithms
grep -nE "md5\(|sha1\(|createHash\(['\"]md5|createHash\(['\"]sha1" $DIFF

# eval / exec
grep -nE "\beval\(|\bexec\(|\bsubprocess\.call\(" $DIFF

# Prototype pollution
grep -n "__proto__\|constructor\[" $DIFF

# Path traversal risk
grep -nE "path\.join\(.*req\.|readFile\(.*req\." $DIFF
```  

### 第4步：测试覆盖率变化  
```bash
# Count source vs test files changed
CHANGED_SRC=$(gh pr diff $PR --name-only | grep -vE "\.test\.|\.spec\.|__tests__")
CHANGED_TESTS=$(gh pr diff $PR --name-only | grep -E "\.test\.|\.spec\.|__tests__")

echo "Source files changed: $(echo "$CHANGED_SRC" | wc -w)"
echo "Test files changed:   $(echo "$CHANGED_TESTS" | wc -w)"

# Lines of new logic vs new test lines
LOGIC_LINES=$(grep "^+" /tmp/pr-$PR.diff | grep -v "^+++" | wc -l)
echo "New lines added: $LOGIC_LINES"

# Run coverage locally
npm test -- --coverage --changedSince=main 2>/dev/null | tail -20
pytest --cov --cov-report=term-missing 2>/dev/null | tail -20
```  
**覆盖率变化规则：**  
- 新添加的功能如果没有相应的测试，则标记为问题  
- 删除了测试代码但未删除相关代码的，也需标记为问题  
- 测试覆盖率下降超过5%时，禁止合并  
- 涉及身份验证或支付功能的代码路径必须达到100%的测试覆盖率  

### 第5步：破坏性变更检测  
#### API接口变更  
```bash
# OpenAPI/Swagger spec changes
grep -n "openapi\|swagger" /tmp/pr-$PR.diff | head -20

# REST route removals or renames
grep "^-" /tmp/pr-$PR.diff | grep -E "router\.(get|post|put|delete|patch)\("

# GraphQL schema removals
grep "^-" /tmp/pr-$PR.diff | grep -E "^-\s*(type |field |Query |Mutation )"

# TypeScript interface removals
grep "^-" /tmp/pr-$PR.diff | grep -E "^-\s*(export\s+)?(interface|type) "
```  
#### 数据库架构变更  
```bash
# Migration files added
gh pr diff $PR --name-only | grep -E "migrations?/|alembic/|knex/"

# Destructive operations
grep -E "DROP TABLE|DROP COLUMN|ALTER.*NOT NULL|TRUNCATE" /tmp/pr-$PR.diff

# Index removals (perf regression risk)
grep "DROP INDEX\|remove_index" /tmp/pr-$PR.diff
```  
#### 配置/环境变量变更  
```bash
# New env vars referenced in code (might be missing in prod)
grep "^+" /tmp/pr-$PR.diff | grep -oE "process\.env\.[A-Z_]+" | sort -u

# Removed env vars (could break running instances)
grep "^-" /tmp/pr-$PR.diff | grep -oE "process\.env\.[A-Z_]+" | sort -u
```  

### 第6步：性能影响分析  
```bash
# N+1 query patterns (DB calls inside loops)
grep -n "\.find\|\.findOne\|\.query\|db\." /tmp/pr-$PR.diff | grep "^+" | head -20
# Then check surrounding context for forEach/map/for loops

# Heavy new dependencies
grep "^+" /tmp/pr-$PR.diff | grep -E '"[a-z@].*":\s*"[0-9^~]' | head -20

# Unbounded loops
grep -n "while (true\|while(true" /tmp/pr-$PR.diff | grep "^+"

# Missing await (accidentally sequential promises)
grep -n "await.*await" /tmp/pr-$PR.diff | grep "^+" | head -10

# Large in-memory allocations
grep -n "new Array([0-9]\{4,\}\|Buffer\.alloc" /tmp/pr-$PR.diff | grep "^+"
```  

---

## 工单关联验证  
```bash
# Extract ticket references from PR body
gh pr view $PR --json body | jq -r '.body' | \
  grep -oE "(PROJ-[0-9]+|[A-Z]+-[0-9]+|https://linear\.app/[^)\"]+)" | sort -u

# Verify Jira ticket exists (requires JIRA_API_TOKEN)
TICKET="PROJ-123"
curl -s -u "user@company.com:$JIRA_API_TOKEN" \
  "https://your-org.atlassian.net/rest/api/3/issue/$TICKET" | \
  jq '{key, summary: .fields.summary, status: .fields.status.name}'

# Linear ticket
LINEAR_ID="abc-123"
curl -s -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  --data "{\"query\": \"{ issue(id: \\\"$LINEAR_ID\\\") { title state { name } } }\"}" \
  https://api.linear.app/graphql | jq .
```  

---

## 完整的审核检查清单（30多项检查项）  
```markdown
## Code Review Checklist

### Scope & Context
- [ ] PR title accurately describes the change
- [ ] PR description explains WHY, not just WHAT
- [ ] Linked Jira/Linear ticket exists and matches scope
- [ ] No unrelated changes (scope creep)
- [ ] Breaking changes documented in PR body

### Blast Radius
- [ ] Identified all files importing changed modules
- [ ] Cross-service dependencies checked
- [ ] Shared types/interfaces/schemas reviewed for breakage
- [ ] New env vars documented in .env.example
- [ ] DB migrations are reversible (have down() / rollback)

### Security
- [ ] No hardcoded secrets or API keys
- [ ] SQL queries use parameterized inputs (no string interpolation)
- [ ] User inputs validated/sanitized before use
- [ ] Auth/authorization checks on all new endpoints
- [ ] No XSS vectors (innerHTML, dangerouslySetInnerHTML)
- [ ] New dependencies checked for known CVEs
- [ ] No sensitive data in logs (PII, tokens, passwords)
- [ ] File uploads validated (type, size, content-type)
- [ ] CORS configured correctly for new endpoints

### Testing
- [ ] New public functions have unit tests
- [ ] Edge cases covered (empty, null, max values)
- [ ] Error paths tested (not just happy path)
- [ ] Integration tests for API endpoint changes
- [ ] No tests deleted without clear reason
- [ ] Test names clearly describe what they verify

### Breaking Changes
- [ ] No API endpoints removed without deprecation notice
- [ ] No required fields added to existing API responses
- [ ] No DB columns removed without two-phase migration plan
- [ ] No env vars removed that may be set in production
- [ ] Backward-compatible for external API consumers

### Performance
- [ ] No N+1 query patterns introduced
- [ ] DB indexes added for new query patterns
- [ ] No unbounded loops on potentially large datasets
- [ ] No heavy new dependencies without justification
- [ ] Async operations correctly awaited
- [ ] Caching considered for expensive repeated operations

### Code Quality
- [ ] No dead code or unused imports
- [ ] Error handling present (no bare empty catch blocks)
- [ ] Consistent with existing patterns and conventions
- [ ] Complex logic has explanatory comments
- [ ] No unresolved TODOs (or tracked in ticket)
```  

---

## 输出格式  
审核评论应按照以下格式编写：  
```
## PR Review: [PR Title] (#NUMBER)

Blast Radius: HIGH — changes lib/auth used by 5 services
Security: 1 finding (medium severity)
Tests: Coverage delta +2%
Breaking Changes: None detected

--- MUST FIX (Blocking) ---

1. SQL Injection risk in src/db/users.ts:42
   Raw string interpolation in WHERE clause.
   Fix: db.query("SELECT * WHERE id = $1", [userId])

--- SHOULD FIX (Non-blocking) ---

2. Missing auth check on POST /api/admin/reset
   No role verification before destructive operation.

--- SUGGESTIONS ---

3. N+1 pattern in src/services/reports.ts:88
   findUser() called inside results.map() — batch with findManyUsers(ids)

--- LOOKS GOOD ---
- Test coverage for new auth flow is thorough
- DB migration has proper down() rollback method
- Error handling consistent with rest of codebase
```  

---

## 常见误区  
- **过分关注代码风格而忽视实质内容**：让代码检查工具处理代码格式问题，重点关注逻辑、安全性和正确性  
- **忽略范围影响分析**：一个简单的代码变更可能会影响多个服务  
- **批准未经测试的代码**：务必确保所有可能的错误路径都得到测试  
- **忽视迁移风险**：对于非空值的添加，需要设置默认值或采用分阶段迁移策略  
- **间接泄露敏感信息**：注意错误信息或日志中可能包含的敏感信息（而不仅仅是硬编码的值）  
- **跳过大型PR**：如果PR内容过于复杂，建议将其拆分为多个较小的部分进行审核  

---

## 最佳实践  
1. 在查看代码之前先阅读关联的工单，以便了解背景信息，避免误判  
2. 在审核前检查持续集成（CI）的状态，避免审核无法构建的代码  
3. 在审核时优先考虑范围影响和安全问题，而非代码风格  
- 对于涉及复杂身份验证或性能变更的代码，建议在本地环境中进行复现  
- 清晰标注评论的类型（如“建议”、“必须修改”或“疑问”）  
- 将所有评论集中处理，避免分批发送反馈  
- 不仅指出问题，还要表扬优秀的代码实践，以促进良好的开发文化  

---
---
name: workflow-patterns
model: standard
version: 2.0.0
description: >
  Systematic task implementation using TDD, phase checkpoints, and structured commits.
  Ensures quality through red-green-refactor cycles, 80% coverage gates, and verification
  protocols before proceeding.
tags: [tdd, workflow, quality, testing, git, checkpoints, implementation]
---

# 工作流程模式

使用 TDD（测试驱动开发）系统地执行任务，并设置阶段检查点和验证协议，确保每一步的质量。

## 安装

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install workflow-patterns
```


## 该技能的作用

提供了一种结构化的任务执行方法：
- 为每个任务执行 TDD 循环（从“红色”状态到“绿色”状态，再到“重构”状态）
- 在标记任务为完成之前，进行质量检查（包括测试、代码覆盖率检查和代码格式检查）
- 设置需要用户批准的阶段检查点
- 使用包含丰富元数据的 Git 提交来保证可追溯性


## 适用场景

**适用于：**
- 根据计划实现功能
- 遵循 TDD 方法论
- 需要质量验证的任务
- 有代码覆盖率要求的项目
- 需要可追溯性的团队工作流程

**不适用场景：**
- 快速修复或微小修改
- 探索性原型设计
- 没有测试基础设施的项目


## 关键词：**TDD、实现、测试、代码覆盖率、检查点、验证、红-绿-重构


## TDD 任务生命周期

每个任务包含 11 个步骤：


### 第 1 步：选择下一个任务

阅读计划，确定下一个待处理的 `[ ]` 任务。按当前阶段的顺序选择任务，不要跳过任何步骤。


### 第 2 步：标记为“进行中”

更新计划，将任务标记为 `[~]`：

```markdown
- [~] **Task 2.1**: Implement user validation
```


### 第 3 步：**红色** — 编写失败的测试

在实现代码之前，编写定义预期行为的测试：
- 如有需要，创建测试文件
- 覆盖正常情况
- 覆盖边界情况
- 覆盖错误情况
- 运行测试——测试结果应为 **失败**


```python
def test_validate_email_valid():
    user = User(email="test@example.com")
    assert user.validate_email() is True

def test_validate_email_invalid():
    user = User(email="invalid")
    assert user.validate_email() is False
```


### 第 4 步：**绿色** — 编写最小量的代码

编写使测试通过的代码：
- 专注于让测试通过，而不是追求代码的完美
- 避免过早优化
- 保持代码简洁
- 运行测试——测试结果应为 **通过**


### 第 5 步：**重构** — 提高代码可读性

在测试通过的情况下，改进代码：
- 提取通用代码模式
- 改进命名
- 删除重复代码
- 简化逻辑
- 每次修改后都运行测试——测试结果必须保持 **通过**


### 第 6 步：验证代码覆盖率

检查代码覆盖率是否达到 80% 的目标：

```bash
pytest --cov=module --cov-report=term-missing
```

如果覆盖率低于 80%：
- 找出未被覆盖的代码行
- 为缺失的代码路径添加测试
- 重新运行代码覆盖率检查


### 第 7 步：记录偏差

如果实际实现与计划不符或添加了依赖项：
- 在 `tech-stack.md` 中更新依赖项信息
- 在任务注释中记录偏差情况
- 如果需求发生变化，更新需求规格


### 第 8 步：提交代码更改

创建有针对性的提交记录：


```bash
git commit -m "feat(user): implement email validation

- Add validate_email method to User class
- Handle empty and malformed emails
- Add comprehensive test coverage

Task: 2.1"
```


### 第 9 步：使用提交哈希值更新计划

使用提交哈希值标记任务已完成：


```markdown
- [x] **Task 2.1**: Implement user validation `abc1234`
```


### 第 10 步：提交计划更新


```bash
git commit -m "docs: update plan - task 2.1 complete"
```


### 第 11 步：重复上述步骤

继续执行下一个任务，直到当前阶段全部完成。


## 阶段完成协议

当一个阶段的所有任务都完成后：


### 1. 确认更改的文件


```bash
git diff --name-only <last-checkpoint-sha>..HEAD
```


### 2. 确保测试覆盖率

对于每个被修改的文件：
- 确认新代码或修改后的代码有对应的测试
- 运行修改模块的测试
- 如果覆盖率低于 80%，添加相应的测试


### 3. 运行完整的测试套件


```bash
pytest -v --tb=short
```


所有测试都必须通过。


### 4. 生成验证检查表


```markdown
## Phase 1 Verification

- [ ] User can register with valid email
- [ ] Invalid email shows appropriate error
- [ ] Database stores user correctly
```


### 5. 等待用户批准

展示验证检查表：


```
Phase 1 complete. Please verify:
1. [x] Test suite passes (automated)
2. [x] Coverage meets target (automated)
3. [ ] Manual verification items (requires human)

Respond with 'approved' to continue.
```


**未经明确批准，切勿继续执行下一步。**


### 6. 创建检查点提交记录


```bash
git commit -m "checkpoint: phase 1 complete

Verified:
- All tests passing
- Coverage: 87%
- Manual verification approved"
```


### 7. 记录检查点哈希值

更新计划中的检查点表格：


```markdown
## Checkpoints

| Phase   | SHA     | Date       | Status   |
|---------|---------|------------|----------|
| Phase 1 | def5678 | 2025-01-15 | verified |
| Phase 2 |         |            | pending  |
```


## 质量检查门

在标记任务为完成之前，需要满足以下条件：


| 检查门 | 要求 |
|------|-------------|
| 测试 | 所有现有测试通过，新添加的测试也通过 |
| 代码覆盖率 | 新代码的覆盖率达到 80% 以上 |
| 代码格式检查 | 无代码格式错误 |
| 类型检查 | 如果适用，类型检查工具也应通过 |
| 安全性 | 代码中不存在敏感信息，且输入验证机制已启用 |


## Git 提交格式


```
<type>(<scope>): <subject>

<body>

Task: <task-id>
```


**提交类型：**
- `feat` — 新功能
- `fix` — 修复错误
- `refactor` — 仅修改代码（不涉及新增功能或修复错误）
- `test` — 添加测试
- `docs` — 编写文档
- `chore` — 维护工作


## 处理偏差情况


### 范围扩展
- 如果发现计划中未包含的新需求：
  - 在需求规格中将其记录为新需求
  - 将相关任务添加到计划中
  - 在任务注释中说明添加原因


### 范围缩减
- 如果某个功能被认为不再必要：
  - 将相关任务标记为 `[-]`（跳过），并说明原因
  - 更新需求规格中的范围描述
  - 记录决策理由


### 技术上的偏差
- 如果实际实现方法与计划不同：
  - 在任务注释中记录偏差原因
  - 如果依赖项发生变化，更新 `tech-stack.md`
  - 记录为什么原来的方法不适用


```markdown
- [x] **Task 2.1**: Implement validation `abc1234`
  - DEVIATION: Used library instead of custom code
  - Reason: Better edge case handling
  - Impact: Added email-validator to dependencies
```


## 错误处理


### 测试在“绿色”状态后失败

1. **不要进入“重构”阶段**
2. **确定哪个测试导致失败**
3. **恢复到上一次测试通过的代码状态**
4. **重新进行代码实现


### 检查点被拒绝

1. **在计划中记录拒绝原因**
2. **创建任务来解决问题**
3. **完成问题修复工作**
4. **再次请求检查点批准**


### 由于依赖项问题导致进度受阻

1. **将任务标记为 `[!]`，并说明阻碍原因**
2. **检查其他任务是否可以继续执行**
3. **记录预期的解决方案**


## 任务状态符号


| 符号 | 含义 |
|--------|---------|
| `[ ]` | 待处理 |
| `[~]` | 进行中 |
| `[x]` | 完成 |
| `[-]` | 被跳过 |
| `[!]` | 受到阻碍 |


## 最佳实践


1. **务必先编写失败的测试** — 在进行任何代码实现之前，必须先编写测试
2. **每次提交只包含一个逻辑上的变更**
3. **立即更新计划** — 任务完成后立即更新计划
4. **等待批准** — 未经批准，切勿跳过任何检查点
5. **确保代码覆盖率达标** — 不要接受低于 80% 的覆盖率
6. **按顺序完成各个阶段** — 按照计划顺序完成各个阶段
7. **记录所有偏差** — 记录所有与计划不符的变更
8. **保持代码的稳定性** — 每次提交后，代码都必须能够正常运行


## 绝对禁止的行为


1. **绝对不要跳过“红色”阶段** — 在 TDD 中，编写测试是必须的步骤
2. **未经批准，切勿跳过任何检查点** — 必须等待用户的明确批准
3. **切勿提交无法通过测试的代码** — 每次提交都必须保证代码能够正常运行
4. **代码覆盖率必须达到 80%** — 在达到目标之前，必须持续添加测试
5. **绝不要隐瞒与计划不符的变更** — 所有变更都必须与原始需求规格保持一致
6. **绝不要跳过任何阶段或改变阶段的顺序** — 各个阶段是有序的，有其特定的目的
7. **务必记录提交哈希值** — 可追溯性要求将任务与提交记录关联起来
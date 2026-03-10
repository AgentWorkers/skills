---
name: "review"
description: 审查 Playwright 测试的质量。当用户提到“审查测试”、“检查测试质量”、“审计测试”、“改进测试”、“进行代码测试审查”或“检查 Playwright 的最佳实践”时，请使用此操作。
  Review Playwright tests for quality. Use when user says "review tests",
  "check test quality", "audit tests", "improve tests", "test code review",
  or "playwright best practices check".
---
# 审查 Playwright 测试

系统地审查 Playwright 测试文件，以发现反模式（anti-patterns）、遗漏的最佳实践（missed best practices）以及测试覆盖率不足的问题。

## 输入

`$ARGUMENTS` 可以是：
- 一个文件路径：仅审查该特定测试文件
- 一个目录：审查该目录中的所有测试文件
- 空值：审查项目中 `testDir` 目录下的所有测试文件

## 步骤

### 1. 收集上下文信息

- 读取 `playwright.config.ts` 以获取项目配置
- 列出所有在审查范围内的 `*.spec.ts` 或 `*.spec.js` 文件
- 如果审查单个文件，还需检查相关的页面对象（page objects）和测试 fixture

### 2. 检查每个文件是否存在反模式

从本技能目录中加载 `anti-patterns.md` 文件，检查是否存在以下 20 种反模式：

**必须修复的（Critical）：**
1. 使用 `waitForTimeout()` 方法
2. 非以 Web 优先的断言（`expect(await ...`)`
3. 使用硬编码的 URL 而不是 `baseURL`
4. 在存在基于角色的定位器（role-based locators）时使用 CSS/XPath 选择器
5. Playwright 调用中缺少 `await` 语句
6. 测试之间共享可变状态
7. 测试执行顺序存在依赖关系

**建议修复的（Warning）：**
8. 测试代码超过 50 行（考虑拆分测试）
9. 使用未命名的字符串作为测试数据
10. 缺少错误处理或边缘情况测试
11. 使用 `page.evaluate()` 来执行本应由定位器（locators）完成的操作
12. 测试描述（`test.describe()`）嵌套超过 2 层
13. 测试名称过于通用（如 “should work” 或 “test 1”）

**参考信息（Info）：**
14. 对于包含 5 个以上定位器的页面，未定义相应的页面对象
15. 使用内联测试数据而非工厂函数（factory functions）或测试 fixture
16. 缺少可访问性（accessibility）断言
17. 对于 UI 依赖性强的页面，缺少视觉回归测试
18. 控制台错误断言未被检查
19. 使用空等待（idle waits）而非具体的断言来处理网络请求
20. 缺少对测试描述的分组（missing `test.describe()` grouping）

### 3. 为每个文件评分

根据以下标准打分（1-10 分）：
- **9-10**：适合生产环境，遵循所有最佳实践
- **7-8**：表现良好，需要少量改进
- **5-6**：功能可用，但存在反模式
- **3-4**：存在严重问题，测试结果可能不稳定
- **1-2**：需要重写

### 4. 生成审查报告

对于每个文件，生成相应的审查结果：

```
## <filename> — Score: X/10

### Critical
- Line 15: `waitForTimeout(2000)` → use `expect(locator).toBeVisible()`
- Line 28: CSS selector `.btn-submit` → `getByRole('button', { name: "submit" })`

### Warning
- Line 42: Test name "test login" → "should redirect to dashboard after login"

### Suggestions
- Consider adding error case: what happens with invalid credentials?
```

### 5. 对整个项目进行审查

如果审查整个测试套件：
- 为每个文件创建子代理（sub-agent）以实现并行审查（最多同时进行 5 个任务）
- 或者对于非常大的测试套件，使用 `/batch` 命令进行批量处理
- 将审查结果汇总成表格

### 6. 提供修复建议

对于每个需要修复的严重问题，提供正确的代码示例，并询问用户：“是否应用这些修复？[是/否]”

如果用户同意修复，使用 `Edit` 工具应用所有修复建议。

## 输出

- 每个文件的审查结果及评分
- 总文件数、平均评分、严重问题数量
- 需要修复的问题列表
- 识别出的测试覆盖率不足的部分（即没有相应测试的页面或功能）
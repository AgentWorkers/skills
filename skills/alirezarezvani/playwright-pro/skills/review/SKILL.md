---
name: review
description: 审查 Playwright 测试的质量。当用户提到“审查测试”、“检查测试质量”、“审计测试”、“改进测试”、“进行代码测试审查”或“检查 Playwright 的最佳实践”时，请使用此功能。
  Review Playwright tests for quality. Use when user says "review tests",
  "check test quality", "audit tests", "improve tests", "test code review",
  or "playwright best practices check".
---
# 审查 Playwright 测试

系统地审查 Playwright 测试文件，检查是否存在反模式（anti-patterns）、遗漏的最佳实践（missed best practices）以及测试覆盖范围的不足。

## 输入

`$ARGUMENTS` 可以是：
- 一个文件路径：仅审查该特定测试文件
- 一个目录：审查该目录中的所有测试文件
- 空值：审查项目 `testDir` 目录中的所有测试文件

## 步骤

### 1. 收集上下文信息

- 阅读 `playwright.config.ts` 以获取项目配置
- 列出所有在审查范围内的 `*.spec.ts` 或 `*.spec.js` 文件
- 如果审查单个文件，还需检查相关的页面对象（page objects）和测试用例（fixtures）

### 2. 检查每个文件是否存在反模式

从本技能目录中加载 `anti-patterns.md`，并检查是否存在以下 20 种反模式：

**必须修复的（Critical）：**
1. `waitForTimeout()` 的使用方式
2. 非以 Web 优先的断言（`expect(await ...`)`
3. 使用硬编码的 URL 而不是 `baseURL`
4. 在可以使用基于角色的选择器（role-based selectors）的情况下仍使用 CSS/XPath 选择器
5. Playwright 调用中缺少 `await` 语句
6. 测试之间存在共享的可变状态
7. 测试执行顺序存在依赖关系

**建议修复的（Warning）：**
8. 长度超过 50 行的测试（考虑拆分）
9. 使用未命名的字符串作为测试条件
10. 缺少错误处理或边缘情况测试
11. 使用 `page.evaluate()` 来执行本应由页面定位器（page locators）完成的操作
12. `test.describe()` 的嵌套层次超过 2 层
13. 测试名称过于通用（如 “should work” 或 “test 1”）

**仅供参考（Info）：**
14. 对于包含 5 个以上定位器的页面，未创建相应的页面对象
15. 使用内联测试数据而非工厂函数/测试用例（factory functions/fixtures）
16. 缺少可访问性相关的断言
17. 对于 UI 相关较多的页面，未编写视觉回归测试
18. 控制台错误未被检查
19. 使用空闲等待（idle waits）而非具体的断言来处理网络请求
20. 缺少 `test.describe()` 的分组结构

### 3. 为每个文件打分

根据以下标准打分（1-10 分）：
- **9-10**：已准备好在生产环境中使用，遵循所有最佳实践
- **7-8**：表现良好，可以进行少量改进
- **5-6**：功能上可用，但存在反模式
- **3-4**：存在严重问题，测试结果可能不稳定
- **1-2**：需要重写

### 4. 生成审查报告

对于每个文件，生成相应的审查结果：

```
## <filename> — Score: X/10

### Critical
- Line 15: `waitForTimeout(2000)` → use `expect(locator).toBeVisible()`
- Line 28: CSS selector `.btn-submit` → `getByRole('button', { name: 'Submit' })`

### Warning
- Line 42: Test name "test login" → "should redirect to dashboard after login"

### Suggestions
- Consider adding error case: what happens with invalid credentials?
```

### 5. 对整个项目进行审查

如果审查整个测试套件：
- 为每个文件创建子进程以并行进行审查（最多支持 5 个并发任务）
- 或者对于非常大的测试套件，使用 `/batch` 命令进行批量处理
- 将审查结果汇总到一张总结表中

### 6. 提供修复建议

对于每个需要修复的严重问题，提供正确的代码示例，并询问用户：“是否应用这些修复？[是/否]”

如果用户同意修复，使用 `Edit` 工具应用所有修复建议。

## 输出

- 每个文件的审查结果及评分
- 总文件数量、平均评分、严重问题数量
- 需要修复的问题列表
- 识别出的测试覆盖范围不足的部分（即没有对应测试的页面或功能）
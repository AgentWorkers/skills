---
name: "playwright-pro"
description: "这是一个面向生产环境的Playwright测试工具包。当用户提到Playwright测试、端到端测试、浏览器自动化、修复不稳定（“flaky”）的测试用例、测试迁移、持续集成/持续部署（CI/CD）测试或测试套件时，都可以使用该工具包。该工具包能够生成测试用例、修复那些运行不稳定的测试问题，并支持从Cypress/Selenium迁移测试脚本；同时还能与TestRail平台进行数据同步，并在BrowserStack上进行测试执行。该工具包提供了55个测试模板、3个测试代理（agents），以及智能化的测试报告功能。"
---
# Playwright Pro

这是一个专为AI编码代理设计的、具备生产级测试功能的Playwright测试工具包。

## 可用命令

当Playwright作为Claude Code插件安装后，以下命令可以通过`/pw:`来执行：

| 命令 | 功能 |
|---|---|
| `/pw:init` | 设置Playwright环境：检测框架版本、生成配置文件、启动持续集成（CI）流程并执行首次测试 |
| `/pw:generate <spec>` | 根据用户故事、URL或组件内容生成测试用例 |
| `/pw:review` | 检查测试用例中是否存在反模式（不良编程习惯）或覆盖范围不足的问题 |
| `/pw:fix <test>` | 诊断并修复失败的或不可靠的测试用例 |
| `/pw:migrate` | 将现有的Cypress或Selenium测试框架迁移到Playwright |
| `/pw:coverage` | 分析已测试的内容与实际需要测试的内容之间的差异 |
| `/pw:testrail` | 与TestRail同步：读取测试用例并推送测试结果 |
| `/pw:browserstack` | 在BrowserStack上运行测试，并获取跨浏览器的测试报告 |
| `/pw:report` | 生成符合您需求的测试报告格式 |

## 快速上手流程

对于大多数项目，推荐的执行顺序如下：

```
1. /pw:init          → scaffolds config, CI pipeline, and a first smoke test
2. /pw:generate      → generates tests from your spec or URL
3. /pw:review        → validates quality and flags anti-patterns      ← always run after generate
4. /pw:fix <test>    → diagnoses and repairs any failing/flaky tests  ← run when CI turns red
```

**验证步骤：**
- 在执行`/pw:generate`命令后，务必先运行`/pw:review`命令；该命令会自动检测测试用例中的错误和遗漏的断言。
- 在修复问题后，重新在本地运行完整的测试套件（使用`npx playwright test`命令），以确保修复没有引入新的问题。
- 在完成迁移后，运行`/pw:coverage`命令，以确认新的测试框架与旧的测试框架之间的测试内容是否一致，然后再逐步淘汰旧的Cypress/Selenium测试。

### 示例：生成测试用例 → 审查测试用例 → 修复问题

```bash
# 1. Generate tests from a user story
/pw:generate "As a user I can log in with email and password"

# Generated: tests/auth/login.spec.ts
# → Playwright Pro creates the file using the auth template.

# 2. Review the generated tests
/pw:review tests/auth/login.spec.ts

# → Flags: one test used page.locator('input[type=password]') — suggests getByLabel('Password')
# → Fix applied automatically.

# 3. Run locally to confirm
npx playwright test tests/auth/login.spec.ts --headed

# 4. If a test is flaky in CI, diagnose it
/pw:fix tests/auth/login.spec.ts
# → Identifies missing web-first assertion; replaces waitForTimeout(2000) with expect(locator).toBeVisible()
```

## 重要规则

1. 尽量使用`getByRole()`方法而非CSS/XPath方法——因为前者对页面标记的变化更具适应性。
2. 绝不要使用`page.waitForTimeout()`方法——应优先使用基于Web的断言方式。
3. `expect(locator)`方法会自动重试；而`expectawait locator.textContent())`方法则不会自动重试。
4. 每个测试用例都应保持独立性，避免在测试之间共享状态。
5. 配置文件中应设置`baseURL`，避免硬编码URL。
6. 在持续集成（CI）环境中设置重试次数为2次；在本地环境中设置为0次。
7. 使用`'on-first-retry'`选项进行调试，以获得详细的调试信息而不会影响测试速度。
8. 使用测试固定夹（fixtures）而非全局变量来管理共享状态。
9. 每个测试用例应只验证一个行为；虽然可以包含多个相关的断言，但最好每个测试专注于一个具体的行为。
10. 仅模拟外部服务，切勿模拟自己的应用程序。

## 定位器（Locators）的使用优先级

```
1. getByRole()        — buttons, links, headings, form elements
2. getByLabel()       — form fields with labels
3. getByText()        — non-interactive text
4. getByPlaceholder() — inputs with placeholder
5. getByTestId()      — when no semantic option exists
6. page.locator()     — CSS/XPath as last resort
```

## 包含的内容

- **9项核心技能**，附带详细的操作步骤说明
- **3个专用工具代理**：测试架构师（test-architect）、测试调试器（test-debugger）和迁移规划工具（migration-planner）
- **55个测试模板**：涵盖认证（auth）、CRUD操作、登录/注销（checkout）、搜索（search）、表单处理（forms）、仪表盘（dashboard）、设置管理（settings）、新用户引导（onboarding）、通知（notifications）、API接口测试（API）、无障碍功能（accessibility）等场景
- **2个MCP服务器**（TypeScript支持）：TestRail和BrowserStack的集成支持
- **智能辅助工具**：自动验证测试质量、自动识别Playwright项目
- **6份参考文档**：包含重要规则、定位器使用方法、断言方式、测试固定夹的编写技巧、常见错误及解决方法
- **迁移指南**：提供Cypress和Selenium到Playwright的迁移方案

## 集成设置

### TestRail（可选）
```bash
export TESTRAIL_URL="https://your-instance.testrail.io"
export TESTRAIL_USER="your@email.com"
export TESTRAIL_API_KEY="your-api-key"
```

### BrowserStack（可选）
```bash
export BROWSERSTACK_USERNAME="your-username"
export BROWSERSTACK_ACCESS_KEY="your-access-key"
```

## 快速参考

请查看`reference/`目录中的以下文件：
- `golden-rules.md`：10条不可违背的重要规则
- `locators.md`：定位器使用的优先级及相关参考资料
- `assertions.md`：基于Web的断言方法指南
- `fixtures.md`：自定义测试固定夹的编写方法及状态管理技巧
- `common-pitfalls.md`：最常见的错误及其解决方法
- `flaky-tests.md`：用于诊断不可靠测试用例的命令及快速修复方法

请查看`templates/README.md`文件，以获取完整的测试模板索引。
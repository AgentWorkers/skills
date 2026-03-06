---
name: playwright-pro
description: 这是一个面向生产环境的Playwright测试工具包。它能够根据测试规范自动生成测试用例，修复那些不稳定（容易出错的）测试用例，支持从Cypress或Selenium迁移测试脚本，与TestRail平台进行数据同步，并可在BrowserStack上进行测试执行。该工具包提供了55个测试模板、3个测试代理，以及智能化的测试报告功能。当用户需要了解Playwright测试、端到端测试（e2e testing）、测试自动化、跨浏览器测试、测试脚本迁移或测试管理的相关内容时，都可以使用该工具包。
  Production-grade Playwright testing toolkit. Generate tests from specs, fix
  flaky failures, migrate from Cypress/Selenium, sync with TestRail, run on
  BrowserStack. 55 templates, 3 agents, smart reporting. Use when user asks
  about Playwright testing, e2e tests, test automation, cross-browser testing,
  test migration, or test management.
---
# Playwright Pro

这是一个专为AI编码代理设计的、具备生产级测试功能的Playwright测试工具包。

## 可用命令

当作为Claude Code插件安装后，这些命令可以通过`/pw:`来使用：

| 命令 | 功能 |
|---|---|
| `/pw:init` | 设置Playwright环境——检测框架、生成配置文件、启动持续集成（CI）流程并执行首次测试 |
| `/pw:generate <spec>` | 根据用户故事、URL或组件生成测试用例 |
| `/pw:review` | 检查测试用例中是否存在反模式（不良编程习惯）或测试覆盖范围不足的问题 |
| `/pw:fix <test>` | 诊断并修复失败的或不稳定的测试用例 |
| `/pw:migrate` | 将测试环境从Cypress或Selenium迁移到Playwright |
| `/pw:coverage` | 分析已测试的内容与实际需要测试的内容之间的差异 |
| `/pw:testrail` | 与TestRail同步——读取测试用例并推送测试结果 |
| `/pw:browserstack` | 在BrowserStack上运行测试，并获取跨浏览器的测试报告 |
| `/pw:report` | 生成符合您需求的测试报告格式 |

## 重要规则

1. 使用`getByRole()`而非CSS/XPath进行元素定位——这样更能适应标记语言的变化 |
2. **绝对不要使用`page.waitForTimeout()`**——应优先使用基于Web的断言方法 |
3. `expect(locator)`会自动重试；而`expectawait locator.textContent())`则不会 |
4. 每个测试用例都应独立运行——避免测试之间共享状态 |
5. 配置文件中应设置`baseURL`——避免硬编码URL |
6. 在持续集成（CI）环境中设置重试次数为2次；在本地环境中设置为0次 |
7. 日志记录模式设置为`'on-first-retry'`——以便在首次尝试失败时仍能进行详细的调试 |
8. 使用测试固定装置（fixtures）而非全局变量来管理共享状态——通过`test.extend()`来实现 |
9. 每个测试用例应只验证一个具体行为；多个相关的断言是可以的 |
10. 仅模拟外部服务——切勿模拟您自己的应用程序 |

## 定位器（Locators）的优先级

```
1. getByRole()        — buttons, links, headings, form elements
2. getByLabel()       — form fields with labels
3. getByText()        — non-interactive text
4. getByPlaceholder() — inputs with placeholder
5. getByTestId()      — when no semantic option exists
6. page.locator()     — CSS/XPath as last resort
```

## 包含内容

- **9项专业技能**，附带详细的操作步骤说明 |
- **3个专用代理工具**：测试架构师（test-architect）、测试调试器（test-debugger）、迁移规划器（migration-planner） |
- **55个测试模板**：涵盖认证（auth）、CRUD操作、签出（checkout）、搜索（search）、表单（forms）、仪表盘（dashboard）、设置（settings）、入职引导（onboarding）、通知（notifications）、API接口（API）、无障碍访问（accessibility）等场景 |
- **2个MCP服务器**（TypeScript支持）：TestRail和BrowserStack的集成支持 |
- **智能辅助工具**：自动验证测试质量、自动识别Playwright项目 |
- **6份参考文档**：包括重要规则、定位器使用方法、断言方式、测试固定装置的编写技巧、常见错误及解决方法 |
- **迁移指南**：提供从Cypress或Selenium到Playwright的迁移步骤 |

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
- `golden-rules.md`：10条不可违背的重要规则 |
- `locators.md`：完整的定位器优先级指南及速查表 |
- `assertions.md`：基于Web的断言方法参考 |
- `fixtures.md`：自定义测试固定装置及状态管理技巧 |
- `common-pitfalls.md`：最常见的10个错误及其解决方法 |
- `flaky-tests.md`：用于诊断不稳定测试用例的命令及快速修复方法 |

请查看`templates/README.md`以获取完整的模板索引。
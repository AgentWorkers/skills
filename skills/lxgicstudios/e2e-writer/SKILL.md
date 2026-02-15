---
name: e2e-writer
description: **从 URL 或组件文件生成 Playwright 的端到端测试**  
当您需要快速获得端到端（end-to-end, e2e）测试覆盖率时，可以使用此方法。
---

# E2E 测试生成工具

编写端到端（end-to-end, E2E）测试是每个人都知道应该做的事情，但没人愿意真正去执行。这款工具可以通过分析你的 URL 或组件文件来自动生成 Playwright 的 E2E 测试用例。只需将工具指向目标页面，它就能自动识别用户交互流程、选择器（selectors）以及需要验证的断言（assertions）。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-e2e-gen src/pages/Login.tsx
```

## 工具功能

- 分析你的组件或页面，识别可测试的用户交互流程；
- 生成包含正确选择器的完整 Playwright 测试文件；
- 支持表单提交、页面导航以及异步操作的处理；
- 同时生成正常流程（happy path）和错误场景（error case）的测试用例；
- 输出可直接运行的 `.spec.ts` 文件。

## 使用示例

```bash
# Generate tests for a login page component
npx ai-e2e-gen src/pages/Login.tsx

# Generate tests from a URL
npx ai-e2e-gen https://myapp.com/signup

# Generate tests for multiple components
npx ai-e2e-gen src/pages/*.tsx
```

## 最佳实践

- **从最关键的交互流程开始**：登录、注册、结账等在生产环境中容易出问题的操作；
- **检查生成的选择器**：虽然生成的选择器是一个不错的起点，但建议添加 `data-testid` 属性以提高测试的稳定性；
- **立即运行测试**：不要让生成的测试用例闲置，立即执行它们以发现任何输出问题；
- **尽早集成到持续集成（CI）流程中**：在忘记之前，将它们添加到你的测试流程中。

## 适用场景

- 当你的项目完全没有 E2E 测试覆盖时；
- 新功能上线后，需要在下一次冲刺之前编写测试用例；
- 你需要一个基线测试套件来检测代码回归问题；
- 当质量保证（QA）团队工作压力过大，急需自动化测试覆盖时。

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多款免费开发工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-e2e-gen --help
```

## 工作原理

该工具会读取你的组件源代码或获取目标 URL，然后分析页面的 DOM 结构及用户交互行为。之后，它会将这些信息传递给 AI 模型，由模型生成涵盖主要用户流程、边缘情况（edge cases）和错误状态的 Playwright 测试用例。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用这款工具。
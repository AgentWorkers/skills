---
name: checkly-cli-skills
description: >
  **Comprehensive Checkly CLI Command Reference and Monitoring as Code Workflows**  
  This document provides a detailed reference to all the commands available in the Checkly CLI, as well as information on how to use monitoring as a code-based workflow in Checkly. It covers various use cases, including API checks, browser tests, Playwright-based testing, check deployment, and execution of `npx checkly` commands.  
  For more specific functionalities, such as authentication, configuration management, test execution, deployment processes, import operations, and advanced usage patterns, please refer to the corresponding sub-skills within this documentation.  
  The document also explains how to trigger certain actions using Checkly’s built-in mechanisms, as well as how to integrate monitoring capabilities into your code-based workflows.  
  Key terms and concepts include:  
  - Checkly CLI (Command Line Interface)  
  - Monitoring as Code (using Checkly to automate monitoring tasks)  
  - Synthetic Monitoring (simulated testing methods)  
  - API Checks (verifying system functionality through APIs)  
  - Browser Tests (testing web applications in real browsers)  
  - Playwright Testing (using the Playwright library for automated web testing)  
  - `npx checkly` (a command-line tool for executing Checkly tasks)  
  If you have any questions or need further assistance, please feel free to contact us.
requirements:
  binaries:
    - checkly
    - npx
  binaries_optional:
    - playwright
  env_vars:
    - CHECKLY_API_KEY
    - CHECKLY_ACCOUNT_ID
  credential:
    type: api_key
    env_var: CHECKLY_API_KEY
    companion_env_var: CHECKLY_ACCOUNT_ID
    docs_url: https://www.checklyhq.com/docs/cli/authentication/
    storage_path: ~/.config/@checkly/cli/config.json
  notes: |
    Requires Checkly account and API key (signup at checklyhq.com/signup or via 'npx checkly login').
    Credentials can be set via environment variables (CHECKLY_API_KEY, CHECKLY_ACCOUNT_ID) or stored in ~/.config/@checkly/cli/config.json via 'npx checkly login'.
    Config stored in checkly.config.ts and auth credentials in system config.
    Browser checks require @playwright/test dependency.
---
# Checkly CLI 技能

全面的 Checkly CLI 命令参考以及“监控即代码”（Monitoring as Code, MaC）工作流程。

## 快速入门

```bash
# Create new Checkly project
npm create checkly@latest

# Test checks locally
npx checkly test

# Deploy to Checkly cloud
npx checkly deploy
```

## 什么是“监控即代码”（Monitoring as Code）？

Checkly CLI 提供了一个基于 TypeScript/JavaScript 的工作流程，用于大规模地编写、测试和部署合成监控（synthetic monitoring）脚本。您可以将监控检查定义为代码，在本地进行测试，使用 Git 进行版本控制，并通过 CI/CD 流程进行部署。

**主要优势：**
- **可编程性**：使用 TypeScript/JavaScript 定义监控检查
- **可测试性**：在部署前在本地运行检查
- **可审查性**：通过 Pull Request（PR）对监控脚本进行代码审查
- **原生支持 Playwright**：使用标准的 @playwright/test 规范
- **集成 CI/CD**：与您的部署流程无缝集成

## 技能分类

本技能涵盖了 Checkly 不同领域的专业子技能：

**入门：**
- `checkly-auth`：身份验证设置与登录
- `checkly-config`：配置文件（checkly.config.ts）和项目结构

**核心工作流程：**
- `checkly-test`：使用 `npx checkly test` 进行本地测试
- `checkly-deploy`：将监控脚本部署到 Checkly 云端
- `checkly-import`：从 Checkly 导入现有的监控脚本到本地代码中

**监控类型：**
- `checkly-checks`：API 检查、浏览器检查、多步骤检查
- `checkly-monitors`：心跳检查、TCP 检查、DNS 检查、URL 检查
- `checkly-groups`：用于组织和共享配置的检查组

**高级功能：**
- `checkly-constructs`：系统管理和资源管理
- `checkly-playwright`：Playwright 测试套件和配置
- `checkly-advanced`：重试策略、报告机制、环境变量设置、代码打包

## 何时使用 Checkly CLI 与 Web UI

**在以下情况下使用 Checkly CLI：**
- 将监控功能作为代码库的一部分进行开发
- 在 CI/CD 中自动化监控脚本的创建/更新
- 在开发过程中本地测试监控脚本
- 对监控配置进行版本控制
- 高效管理多个监控脚本
- 将监控功能与应用程序部署集成

**在以下情况下使用 Web UI：**
- 首次使用 Checkly 时进行探索
- 查看仪表板和历史结果
- 分析监控脚本的失败情况和事件
- 管理账户级别的设置
- 配置警报渠道（电子邮件、Slack、PagerDuty）
- 设置私有检查位置

## 常见工作流程

### 新项目设置

```bash
# Initialize project
npm create checkly@latest
cd my-checkly-project

# Authenticate
npx checkly login

# Test locally
npx checkly test

# Deploy to cloud
npx checkly deploy
```

### 日常开发

```bash
# Create new API check
cat > __checks__/api-status.check.ts <<'EOF'
import { ApiCheck, AssertionBuilder } from 'checkly/constructs'

new ApiCheck('api-status-check', {
  name: 'API Status Check',
  request: {
    url: 'https://api.example.com/status',
    method: 'GET',
    assertions: [
      AssertionBuilder.statusCode().equals(200),
      AssertionBuilder.responseTime().lessThan(500),
    ],
  },
})
EOF

# Test locally
npx checkly test

# Deploy when ready
npx checkly deploy
```

### 使用 Playwright 进行浏览器测试

```bash
# Create browser check
cat > __checks__/homepage.spec.ts <<'EOF'
import { test, expect } from '@playwright/test'

test('homepage loads', async ({ page }) => {
  const response = await page.goto('https://example.com')
  expect(response?.status()).toBeLessThan(400)
  await expect(page).toHaveTitle(/Example/)
  await page.screenshot({ path: 'homepage.jpg' })
})
EOF

# Test with Playwright locally (faster)
npx playwright test __checks__/homepage.spec.ts

# Test via Checkly runtime
npx checkly test __checks__/homepage.spec.ts

# Deploy
npx checkly deploy
```

### 导入现有监控脚本

```bash
# Import all checks from Checkly account
npx checkly import plan

# Review generated code
git diff

# Commit imported checks
git add .
git commit -m "Import existing monitoring checks"
```

## 决策树

### “我应该创建哪种类型的监控脚本？”

```
What are you monitoring?
├─ REST API / HTTP endpoint
│  ├─ Simple availability → API Check (request + status assertion)
│  ├─ Complex validation → API Check (request + multiple assertions + scripts)
│  └─ Just uptime/ping → URL Monitor (simpler, faster)
│
├─ Web application / User flow
│  ├─ Single page → Browser Check (one .spec.ts file)
│  ├─ Multiple steps → Browser Check or Multi-Step Check
│  └─ Full test suite → Playwright Check Suite (playwright.config.ts)
│
└─ Service health / Infrastructure
   ├─ Periodic heartbeat → Heartbeat Monitor
   ├─ TCP port → TCP Monitor
   ├─ DNS record → DNS Monitor
   └─ Simple HTTP → URL Monitor
```

**快速参考：**
- **API 检查**：包含断言的 HTTP 请求（状态码、请求头、请求体、响应时间）
- **浏览器检查**：用于网页测试的单一 Playwright 规范文件
- **多步骤检查**：复杂的浏览器操作流程（建议使用浏览器检查）
- **Playwright 测试套件**：包含多个测试用例的 Playwright 测试套件
- **监控检查**：无需执行代码的简单健康检查

### “是在本地测试还是部署？”

```
What stage are you at?
├─ Developing new check
│  ├─ Browser check → npx playwright test (fastest iteration)
│  └─ API check → npx checkly test (includes assertions)
│
├─ Ready to validate
│  └─ npx checkly test (runs in Checkly runtime, catches issues)
│
└─ Ready for production
   └─ npx checkly deploy (schedule checks to run continuously)
```

**测试优先级：**
1. `npx playwright test`：最快的本地 Playwright 执行方式（仅适用于浏览器检查）
2. `npx checkly test`：在 Checkly 运行时进行验证，捕获兼容性问题
3. `npx checkly deploy`：用于持续监控的部署

### “基于文件还是基于对象模型创建监控脚本？”

```
How do you want to define checks?
├─ Auto-discovery (convention over configuration)
│  ├─ Browser checks → *.spec.ts files matching testMatch pattern
│  ├─ Multi-step → *.check.ts files with MultiStepCheck construct
│  └─ API checks → *.check.ts files with ApiCheck construct
│
└─ Explicit definition
   ├─ Programmatic → Construct instances in .check.ts files
   └─ Full control → Playwright Check Suite with playwright.config.ts
```

**使用模式：**
- **自动发现**：在 `checkly.config.ts` 中配置 `checks.browserChecks.testMatch`
- **显式创建**：从 `checkly/constructs` 导入并实例化监控脚本
- **Playwright 项目**：定义具有不同配置的多个测试套件

### **配置文件应放在哪里？**

**配置层次结构**（具体配置优先于通用配置）：
1. 检查脚本级别的配置（最高优先级）
2. 检查组级别的配置
3. `checkly.config.ts` 中的默认配置
4. Checkly 账户级别的默认配置（最低优先级）

## 项目结构

典型的 Checkly CLI 项目结构：

```
my-monitoring-project/
├── checkly.config.ts          # Project configuration
├── __checks__/                # Check definitions
│   ├── api.check.ts           # API check construct
│   ├── homepage.spec.ts       # Browser check (auto-discovered)
│   ├── login.spec.ts          # Another browser check
│   └── utils/
│       ├── alert-channels.ts  # Shared alert channel definitions
│       └── helpers.ts         # Shared helper functions
├── playwright.config.ts       # Playwright configuration (optional)
├── package.json
└── node_modules/
    └── checkly/               # CLI package with constructs
```

## 安装方法

### 新项目（推荐方式）

```bash
npm create checkly@latest
```

创建一个包含以下内容的项目框架：
- `checkly.config.ts`，包含合理的默认配置
- `__checks__` 目录中包含示例监控脚本
- `package.json`，包含 Checkly 依赖项
- `.gitignore` 文件，用于指定需要忽略的文件

### 现有项目

```bash
# Install as dev dependency
npm install --save-dev checkly

# Create configuration file
npx checkly init
```

### 全局安装（不推荐）

```bash
npm install -g checkly
checkly test
```

**注意**：建议使用 `npx checkly` 来执行特定项目的 CLI 命令。

## 相关技能

**入门：**
- 请参阅 `checkly-auth` 以了解身份验证设置
- 请参阅 `checkly-config` 以了解项目配置
- 请参阅 `checkly-test` 以了解本地测试流程

**创建监控脚本：**
- 请参阅 `checkly-checks` 以了解 API 检查和浏览器检查的创建方法
- 请参阅 `checkly-monitors` 以了解简单的健康检查配置
- 请参阅 `checkly-playwright` 以了解完整的测试套件设置

**高级工作流程：**
- 请参阅 `checkly-deploy` 以了解部署策略
- 请参阅 `checkly-constructs` 以了解对象模型的使用方法
- 请参阅 `checkly-advanced` 以了解重试策略和报告机制

**导入现有监控脚本：**
- 请参阅 `checkly-import` 以将监控脚本从 Web UI 迁移到本地代码中
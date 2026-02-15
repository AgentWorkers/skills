---
name: qa-patrol
description: >
  使用本地浏览器自动化技术对Web应用进行自动化质量保证（QA）测试。整个测试过程完全在您的机器上完成——无需传输任何数据，也不依赖云服务或外部服务器。  
  - **Level 1（冒烟测试）**：仅需要提供一个URL即可开始测试。  
  - **Level 2（身份验证/支付测试）**：允许使用环境变量（env vars）来设置测试凭据。  
  - **Level 3（静态分析、数据库检查）**：可选择性地读取本地文件，并连接到用户提供的数据库。  
  - 支持以下技术栈：Supabase/Firebase身份验证、Stripe支付框架、React Native Web应用、Next.js以及单页应用程序（SPAs）。
---
# QA Patrol

这是一个用于Web应用程序的自动化质量保证（QA）测试工具，能够捕捉单元测试未能发现的漏洞，例如跨平台问题、认证状态异常、数据完整性错误以及集成故障。

## 安全性与隐私

**所有测试都在您的本地机器上运行，不会向外部服务器发送任何数据。浏览器自动化功能使用OpenClaw内置的浏览器控制机制，不涉及任何云服务。**

### 权限分级

| 权限等级 | 功能 | 所需权限 | 所需环境变量 |
|--------|--------|---------|-----------|
| **1 — 烟雾测试（Smoke Test）** | 加载页面并检查错误 | 仅需要`browser`权限 | `APP_URL`（或使用`--url`参数） |
| **2 — 认证/支付（Auth/Payments）** | 测试登录和支付流程 | 仅需要`browser`权限 | 测试账户凭据（详见下文） |
| **3 — 静态分析（Static Analysis）** | 扫描本地源代码以查找漏洞模式 | 需要`browser`权限和`read`权限 | 无需额外环境变量（使用本地`repo_path`） |
| **3 — 数据完整性检查（Data Integrity）** | 将数据库值与用户界面显示内容进行比对 | 需要`browser`权限 | `DATABASE_URL` |

**`read`权限仅用于第3级的静态分析。**第1级和第2级的测试仅使用浏览器自动化功能。如果您仅运行第1级或第2级的测试，该工具不会访问任何本地文件。**

### 环境变量（均为可选）

| 变量名 | 是否必需 | 使用者 | 用途 |
|---------|--------|---------|---------|
| `APP_URL` | 否 | 第1级及以上 | 目标应用程序的URL（也可使用`--url`参数） |
| `ADMIN_EMAIL` | 否 | 第2级 | 管理员测试账户的电子邮件地址 |
| `ADMIN_PASSWORD` | 否 | 第2级 | 管理员测试账户的密码 |
| `FREE_EMAIL` | 否 | 第2级 | 免费账户测试账户的电子邮件地址 |
| `FREE_PASSWORD` | 否 | 第2级 | 免费账户测试账户的密码 |
| `PRO_EMAIL` | 否 | 第2级 | 专业账户测试账户的电子邮件地址 |
| `PRO_PASSWORD` | 否 | 第2级 | 专业账户测试账户的密码 |
| `DATABASE_URL` | 否 | 第3级 | 用于数据完整性检查的数据库连接地址 |

**⚠️ 请仅使用测试账户的凭据，切勿使用生产环境的密码或数据库URL。**

### 保密性处理
- **切勿在测试脚本中硬编码任何敏感信息**——始终使用环境变量进行替换（例如：`${env ADMIN_PASSWORD}`）。
- 凭据在运行时从本地环境中读取。
- 测试脚本中的变量使用`${env.VAR}`作为占位符。
- 该工具不会保存、记录或传输任何凭据。

### 安全性模式检测（非攻击性用途）
`references/bug-patterns.md`文件包含用于检测代码库中敏感信息泄露的正则表达式模式（例如`sk_live_`、`api_key=`）。这些模式仅用于帮助开发者发现和修复安全问题，并非攻击性工具。这是ESLint、Semgrep以及GitHub秘密扫描等安全工具的常用做法。

### 无需安装脚本或代码文件
该工具仅包含指令，不包含可执行代码、安装脚本或第三方依赖项。其全部功能依赖于`SKILL.md`中的说明以及OpenClaw内置的浏览器自动化功能。

## 快速入门

### 烟雾测试（Level 1：无需配置）
```bash
# Just provide a URL
qa-patrol https://example.com
```

### 带有认证/支付功能的测试（Level 2）
```bash
# Use a test plan template
qa-patrol --plan auth-supabase.yaml --url https://example.com
```

### 完整配置（Level 3）
```bash
# Custom test plan with data integrity checks
qa-patrol --plan my-app.yaml
```

## 工作流程

### 1. 加载或生成测试计划
- 如果提供了YAML格式的测试计划，请直接加载；否则，系统会自动生成一个基本测试计划：
```yaml
app:
  url: <provided URL>
  name: <extracted from page title>

tests:
  smoke:
    - name: Homepage loads
      navigate: /
      assert:
        - element_exists: main
        - no_console_errors: true
```

测试计划模板位于`assets/templates/`目录下：
- `basic.yaml`：无需配置的简单测试
- `auth-supabase.yaml`：Supabase认证流程测试
- `payments-stripe.yaml`：Stripe支付功能测试
- `full-saas.yaml`：完整的SaaS测试计划

### 2. 运行测试
按照以下顺序执行测试：烟雾测试 → 认证测试 → 支付测试 → 数据完整性测试 → 静态分析测试。
- 对于每个测试步骤：
  1. 导航到目标URL。
  2. 执行相应的操作（点击、输入、等待）。
  3. 捕获界面截图和控制台日志。
  4. 根据测试结果判断测试是否通过（PASS/FAIL/SKIP），并记录相关证据。

#### 浏览器自动化模式
```python
# Navigate and snapshot
browser(action="navigate", targetUrl="https://example.com/page")
browser(action="snapshot")

# Form interaction
browser(action="act", request={"kind": "click", "ref": "email_input"})
browser(action="act", request={"kind": "type", "ref": "email_input", "text": "user@test.com"})
browser(action="act", request={"kind": "click", "ref": "submit_button"})

# Check console for errors
browser(action="console", level="error")
```

完整的自动化模式请参考`references/test-patterns.md`文件。

### 3. 检查已知漏洞模式
- 如果可以访问代码库，扫描其中是否存在以下问题：
| 模式 | 需要查找的内容 | 严重程度 |
|---------|-------------|---------|
| `Alert.alert`未使用`Platform.OS`保护 | `Alert.alert`语句未添加平台检测 | 高风险 |
| 在模态框中链接外部页面 | 在模态框组件中使用`Linking.openURL` | 高风险 |
| 缺少必要的授权验证 | Supabase查询语句未进行适当授权检查 | 高风险 |
- 硬编码的敏感信息 | 客户端代码中存在API密钥 | 极高风险 |

完整漏洞模式列表请参见`references/bug-patterns.md`文件。

### 4. 数据完整性检查（Level 3）
- 当执行数据完整性测试时：
  1. 执行数据库查询（需要数据库访问权限）。
  2. 导航到相关UI页面。
  3. 提取显示的内容。
  4. 将显示内容与查询结果进行比对。
  5. 根据内容差异的百分比来评估结果的准确性。

### 5. 生成报告
- 生成结构化的测试报告：
```markdown
# QA Report: [App Name]
**Date**: YYYY-MM-DD HH:MM
**URL**: https://example.com
**Confidence**: 87%

## Summary
| Category | Pass | Fail | Skip |
|----------|------|------|------|
| Smoke    | 5    | 0    | 0    |
| Auth     | 3    | 1    | 0    |
| Payments | 0    | 0    | 2    |

## Failures

### [FAIL] Auth: Session persistence after refresh
**Steps**: Sign in → Refresh page → Check auth state
**Expected**: User remains signed in
**Actual**: Redirected to login page
**Evidence**: [screenshot]
**Severity**: High

## Recommendations
1. Fix session persistence (likely cookie/localStorage issue)
2. Add Platform.OS guards to Alert.alert calls
```

报告模板请参考`references/report-format.md`文件。

## 测试计划相关文件

### 应用程序配置
```yaml
app:
  url: https://example.com      # Required: base URL
  name: My App                  # Optional: display name
  stack: expo-web               # expo-web | nextjs | spa | static
```

### 认证配置
```yaml
auth:
  provider: supabase            # supabase | firebase | auth0 | custom
  login_path: /auth             # Path to login page
  accounts:
    admin:
      email: admin@test.com
      password: ${ADMIN_PASSWORD}  # Use env vars for secrets
    free:
      email: free@test.com
      password: ${FREE_PASSWORD}
    guest: true                 # Test anonymous/guest mode
```

### 测试类型

- **烟雾测试（Smoke Tests）**
```yaml
tests:
  smoke:
    - name: Homepage loads
      navigate: /
      assert:
        - element_exists: main
        - no_console_errors: true
        - no_network_errors: true
    
    - name: Navigation works
      navigate: /
      steps:
        - click: { ref: nav_link }
        - assert: { url_contains: "/target" }
```

- **认证测试（Auth Tests）**
```yaml
tests:
  auth:
    - name: Sign in flow
      steps:
        - navigate: /auth
        - type: { ref: email_input, text: "${auth.accounts.free.email}" }
        - type: { ref: password_input, text: "${auth.accounts.free.password}" }
        - click: { ref: sign_in_button }
        - wait: { url_contains: "/home", timeout: 5000 }
        - assert: { element_exists: "user_avatar" }
    
    - name: Sign out flow
      requires: signed_in
      steps:
        - click: { ref: user_menu }
        - click: { ref: sign_out_button }
        - assert: { url_contains: "/auth" }
    
    - name: Session persistence
      requires: signed_in
      steps:
        - navigate: /home
        - refresh: true
        - assert: { element_exists: "user_avatar" }
```

- **支付测试（Payment Tests）**
```yaml
tests:
  payments:
    provider: stripe
    tests:
      - name: Checkout creation
        steps:
          - navigate: /pricing
          - click: { ref: pro_plan_button }
          - wait: { url_contains: "checkout.stripe.com", timeout: 10000 }
          - assert: { element_exists: "cardNumber" }
```

- **数据完整性测试（Data Integrity Tests）**
```yaml
tests:
  data_integrity:
    - name: Card count matches
      query: "SELECT count(*) FROM cards WHERE country='CA'"
      ui_path: /settings
      ui_selector: "[data-testid='card-count']"
      tolerance: 0  # Exact match required
    
    - name: Points calculation
      query: "SELECT points_rate FROM tiers WHERE name='Gold'"
      ui_path: /calculator
      ui_selector: ".points-display"
      tolerance: 0.01  # 1% tolerance
```

- **静态分析（Static Analysis）**
```yaml
tests:
  static_analysis:
    scan_path: ./src
    patterns:
      - name: Alert.alert without Platform guard
        grep: "Alert\\.alert"
        exclude_grep: "Platform\\.OS"
        severity: high
        fix_hint: "Wrap in Platform.OS check or use cross-platform alert"
      
      - name: Hardcoded API keys
        grep: "(sk_live_|pk_live_|api_key.*=.*['\"][a-zA-Z0-9]{20,})"
        severity: critical
```

### 断言参考
| 断言类型 | 描述 |
|---------|-------------|
| `element_exists: "ref"` | 具有`ref`属性的元素存在于DOM中 |
| `element_visible: "ref"` | 元素在页面上可见 |
| `text_contains: "string"` | 页面文本中包含指定字符串 |
| `url_contains: "/path"` | URL中包含指定路径 |
| `no_console_errors: true` | 控制台未输出错误信息 |
| `no_network_errors: true` | 没有网络请求失败 |
| `value_equals: { ref, value }` | 输入值与预期值匹配 |
| `count_equals: { ref, count }` | 匹配的元素数量 |

### 变量替换
- 使用`${...}`来表示动态值：
  - `${auth.accounts.free.email}`：来自测试计划的值 |
  - `${env.API_KEY}`：来自环境变量的值 |
  - `${captured.user_id}`：来自上一步操作的捕获结果 |

### 信心评分
根据测试覆盖率和结果计算整体测试的置信度：
```
base_confidence = 50
per_smoke_pass = +5 (max 20)
per_auth_pass = +8 (max 24)
per_payment_pass = +10 (max 20)
per_data_check_pass = +6 (max 18)
static_analysis_clean = +8
no_critical_failures = +10

final_confidence = min(base + bonuses - penalties, 100)
```

- **评分规则**：
  - 严重故障：-20分
  - 高风险故障：-10分
  - 中等风险故障：-5分
  - 被跳过的关键测试：-5分

## 相关文件
- `references/test-patterns.md`：浏览器自动化模式及示例
- `references/bug-patterns.md`：常见的安全漏洞模式
- `references/report-format.md`：测试报告模板

### 模板文件
- `assets/templates/basic.yaml`：无需配置的简单测试模板
- `assets/templates/auth-supabase.yaml`：Supabase认证测试模板
- `assets/templates/payments-stripe.yaml`：Stripe支付功能测试模板
- `assets/templates/full-saas.yaml`：完整的SaaS测试计划模板

### 示例
- `assets/examples/rewardly.yaml`：一个实际的React Native Web应用程序测试计划

## 使用提示：
1. **先进行烟雾测试**——在测试认证和支付功能之前，先验证基本功能是否正常。
2. **优先使用无认证模式**——先进行无认证的测试以建立基准。
3. **尽早查看控制台日志**——控制台错误通常能揭示问题的根本原因。
4. **务必保存截图**——遇到问题时务必保存截图以便调试。
5. **检查缓存状态**——退出应用程序并清除缓存，以发现潜在问题。
6. **进行跨平台测试**——如果使用React Native Web应用，务必测试相关的警告和链接功能。
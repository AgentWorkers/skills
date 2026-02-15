# vibetesting - 浏览器自动化测试技能

这是一项针对OpenClaw的全面浏览器自动化测试技能，支持功能测试、用户界面测试、无障碍测试、性能测试以及视觉回归测试。

## 概述

该技能使OpenClaw能够启动浏览器并对Web应用程序进行全面的测试。它支持多种测试类型，并提供详细的测试报告。

## 功能

### 测试类型

1. **功能测试**
   - 表单验证
   - 按钮交互
   - 链接导航
   - API交互
   - 数据输入与验证

2. **用户界面测试**
   - 元素可见性
   - 响应式设计检查
   - 布局验证
   - 颜色对比度检查
   - 字体样式验证

3. **无障碍测试**
   - WCAG 2.1合规性检查
   - ARIA标签验证
   - 键盘导航
   - 屏幕阅读器兼容性
   - 替代文本验证

4. **性能测试**
   - 页面加载时间
   - 资源加载时间
   - Lighthouse指标
   - 核心Web Vital指标（LCP、FID、CLS）
   - JavaScript执行时间

5. **视觉回归测试**
   - 屏幕截图对比
   - 布局变化检测
   - 视觉差异生成
   - 阈值-based验证

6. **安全性测试**
   - HTTPS验证
   - 内容安全策略检查
   - XSS漏洞扫描
   - 表单安全验证

7. **端到端测试**
   - 用户流程测试
   - 结账流程验证
   - 认证流程
   - 多步骤表单测试

## 使用方法

### 基本测试

```markdown
[VibeTesting]
Target URL: https://example.com
Testing Type: functional
```

### 全面测试

```markdown
[VibeTesting]
Target URL: https://myapp.com
Testing Type: comprehensive
Include: functional, accessibility, performance
Report Format: html
```

### 特定测试类型

```markdown
[VibeTesting]
Target URL: https://example.com
Testing Type: accessibility
WCAG Level: AA
```

## 参数

| 参数 | 是否必填 | 描述 | 默认值 |
|-----------|----------|-------------|---------|
| `target_url` | 是 | 要测试的URL | - |
| `testing_type` | 否 | 测试类型 | `comprehensive` |
| `include` | 否 | 要运行的测试类别 | 所有 |
| `exclude` | 否 | 要跳过的测试类别 | 无 |
| `report_format` | 否 | 输出格式 | `html` |
| `viewport` | 否 | 浏览器视口大小 | `1920x1080` |
| `headless` | 否 | 无浏览器界面的运行模式 | `true` |
| `timeout` | 否 | 测试超时（秒） | `60` |
| `wait_for_network` | 否 | 等待网络连接稳定 | `true` |
| `cookies` | 否 | 要设置的Cookie | `{}` |
| `auth` | 否 | 基本认证凭据 | `null` |
| `wcag_level` | 否 | WCAG合规性级别 | `AA` |
| `performance_threshold` | 否 | 最大加载时间（毫秒） | `3000` |
| `screenshot_baseline` | 否 | 用于对比的基准截图 | `null` |
| `visual_threshold` | 否 | 视觉差异阈值（0-1） | `0.01` |

## 测试类型

### quick
快速测试（5-10秒）
- 基本页面加载
- 主要元素存在
- 无JavaScript错误

### functional
全面功能测试（30-60秒）
- 表单测试
- 按钮交互
- 导航流程
- API验证

### comprehensive
完整测试套件（2-5分钟）
- 所有功能测试
- 无障碍审计
- 性能指标
- 视觉回归
- 安全性检查

### accessibility
专门的无障碍测试（1-2分钟）
- WCAG合规性
- ARIA标签
- 键盘导航
- 屏幕阅读器文本

### performance
专注于性能的测试（30-60秒）
- 页面加载时间
- 核心Web Vital指标
- 资源加载时间
- Lighthouse评分

### visual
视觉回归测试（1-2分钟）
- 全页截图
- 布局对比
- 视觉差异生成

### security
专注于安全的测试（30-60秒）
- HTTPS检查
- CSP验证
- 基本漏洞扫描

### e2e
端到端用户流程测试（时间不定）
- 多步骤流程
- 认证
- 结账流程
- 用户场景

## 示例

### 测试简单页面

```
[VibeTesting]
target_url: https://example.com
testing_type: quick
```

### 运行全面无障碍审计

```
[VibeTesting]
target_url: https://myapp.com
testing_type: accessibility
wcag_level: AA
report_format: detailed
```

### 使用自定义视口进行性能测试

```
[VibeTesting]
target_url: https://myapp.com
testing_type: performance
viewport: 390x844
performance_threshold: 2000
headless: true
```

### 进行视觉回归测试

```
[VibeTesting]
target_url: https://myapp.com
testing_type: visual
screenshot_baseline: baseline.png
visual_threshold: 0.05
```

### 进行端到端结账流程测试

```
[VibeTesting]
target_url: https://myshop.com
testing_type: e2e
steps:
  - add_item_to_cart
  - proceed_to_checkout
  - fill_shipping
  - fill_payment
  - complete_order
auth:
  user: test@example.com
  pass: testpass123
```

### 使用特定元素进行自定义测试

```
[VibeTesting]
target_url: https://myapp.com
testing_type: functional
elements:
  validate:
    - selector: "#login-form"
      fields: ["email", "password"]
    - selector: "#submit-btn"
      action: click
  expect:
    - selector: ".success-message"
      visible: true
```

## 输出

### 控制台输出
实时测试进度和结果

### HTML报告
详细的交互式报告，包含：
- 测试总结
- 通过/失败情况
- 性能指标
- 无障碍评分
- 视觉差异（如适用）
- 屏幕截图
- 建议

### JSON导出
适用于CI/CD集成的机器可读结果

## 集成

### CI/CD管道

```yaml
- name: Browser Testing
  uses: openclaw/vibetesting
  with:
    target_url: https://staging.example.com
    testing_type: comprehensive
    report_format: json
```

### GitHub Actions

```yaml
- name: VibeTesting
  run: |
    npx vibetesting \
      --url ${{ env.URL }} \
      --type comprehensive \
      --output results/
```

## 最佳实践

1. **测试环境**
   - 使用测试环境/开发环境的URL进行测试
   - 未经许可勿在生产环境中进行测试
   - 如有需要，设置测试账户

2. **性能**
   - 在CI/CD过程中使用无浏览器界面模式
   - 设置适当的超时时间
   - 避免过载目标服务器

3. **安全性**
   - 绝不要提交认证凭据
   - 使用环境变量
   - 验证SSL证书

4. **视觉测试**
   - 建立基准截图
   - 设计更改后更新基准
   - 设置适当的阈值

5. **无障碍测试**
   - 使用真实的屏幕阅读器进行测试
   - 检查键盘导航功能
   - 验证颜色对比度

## 故障排除

### 浏览器无法启动
- 确保安装了Chrome/Chromium
- 检查端口是否可用
- 确认没有冲突的进程

### 元素未找到
- 检查页面是否完全加载
- 确认选择器是否正确
- 等待动态内容加载完成

### 超时错误
- 增加超时设置
- 检查网络连接
- 确认服务器响应速度

### 内存问题
- 使用无浏览器界面模式运行
- 关闭其他浏览器实例
- 增加系统资源

## 要求

- **浏览器**：推荐使用Chrome/Chromium
- **OpenClaw**：需启用浏览器支持的Gateway版本
- **网络**：需要互联网连接以测试外部URL
- **权限**：无需特殊系统权限

## 高级配置

### 自定义视口

```yaml
viewports:
  desktop: 1920x1080
  tablet: 768x1024
  mobile: 390x844
```

### 等待策略

```yaml
wait:
  network: idle  # Wait for network to be idle
  dom: stable   # Wait for DOM to be stable
  selector: "#loaded"  # Wait for specific element
  timeout: 30
```

### 重试配置

```yaml
retry:
  attempts: 3
  delay: 1000  # ms
  selectors:
    - ".loading-spinner"
    - "#async-content"
```

## 报告

### 报告内容

1. **执行摘要**
   - 总分
   - 测试统计信息
   - 严重问题

2. **功能测试结果**
   - 测试用例
   - 通过/失败详情
   - 错误信息

3. **无障碍测试报告**
   - WCAG合规性
   - 问题严重程度
   - 建议

4. **性能指标**
   - 加载时间分布
   - 核心Web Vital指标
   - Lighthouse评分

5. **视觉对比**
   - 基准与当前状态的对比
   - 视觉差异高亮显示
   - 变更检测结果

6. **安全问题**
   - 漏洞信息
   - 建议
   - 风险等级

## 限制

- 无法测试支付处理（需要真实凭据）
- 仅限于可见内容（无法绕过认证机制）
- 视觉测试依赖于渲染的一致性
- 性能指标可能因运行环境而异

## 未来改进计划

- [ ] 支持多浏览器（Firefox、Safari）
- [ ] 集成云浏览器测试平台（BrowserStack、Sauce Labs）
- [ ] 基于AI的测试生成
- [ ] 自定义测试脚本（JavaScript/Python）
- [ ] 测试录制功能
- [ ] 与测试框架集成（Playwright、Cypress）
- [ ] 并行执行测试
- [ ] 在多个节点上进行分布式测试

## 支持

- **问题报告**：提交错误和功能请求
- **文档**：请参考OpenClaw官方文档
- **示例**：查看示例目录

## 版本信息

- **当前版本**：1.0.0
- **最后更新时间**：2026-02-05
- **作者**：OpenClaw社区

---

**祝您测试顺利！** 🧪🔍✨
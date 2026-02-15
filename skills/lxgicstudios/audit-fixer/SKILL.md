---
name: audit-fixer
description: 使用人工智能分析 npm 审计输出，并获取可操作的修复建议。在处理安全漏洞时使用此方法。
---

# Audit Fixer

`npm audit` 报告了 47 个安全漏洞，其中一半来自您无法控制的嵌套依赖项。该工具会分析审计结果，并为您提供可行的修复建议，帮助您判断哪些漏洞需要关注、哪些可以忽略，以及针对每个漏洞应采取的具体措施。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npm audit --json | npx ai-audit-fix
```

## 工作原理

- 分析 `npm audit` 的输出结果，并根据风险程度对漏洞进行优先级排序
- 确定哪些漏洞实际上会影响您的代码
- 为每个问题提供具体的修复命令
- 指导您何时应该覆盖现有设置，何时应该进行实际修复
- 区分开发环境依赖项和生产环境依赖项

## 使用示例

```bash
# Pipe audit output directly
npm audit --json | npx ai-audit-fix

# Analyze from a saved file
npx ai-audit-fix --input audit-results.json

# Only show high and critical issues
npm audit --json | npx ai-audit-fix --severity high,critical

# Get fix commands only
npm audit --json | npx ai-audit-fix --fixes-only
```

## 最佳实践

- **优先处理生产环境依赖项**：开发环境依赖项不会被发布给用户
- **检查是否存在被实际使用的脆弱代码**：许多漏洞存在于您从未使用的代码路径中
- **先更新父包**：这通常可以一次性修复多个嵌套的漏洞
- **谨慎使用覆盖设置**：记录覆盖设置的原因，并设置提醒以便后续复查

## 适用场景

- 当 `npm audit` 的结果中满是红色警告，让您不知从何入手时
- 当持续集成（CI）的安全检查失败时
- 需要将漏洞情况报告给安全团队时
- 在决定是否推迟发布以进行安全修复时

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，直接使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-audit-fix --help
```

## 工作机制

该工具会解析 `npm audit` 的 JSON 输出，分析每个漏洞的依赖链和严重程度，判断其是否会影响您的生产环境代码，然后生成带有具体修复命令的优先级建议。

## 许可证

MIT 许可证。永久免费，您可以自由使用该工具。
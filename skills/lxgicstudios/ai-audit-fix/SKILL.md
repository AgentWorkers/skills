---
name: audit-fixer
description: 使用人工智能分析 npm 审计输出，并获取可操作的修复建议。在处理安全漏洞时可以使用此方法。
---

# Audit Fixer

`npm audit` 命令会显示 47 个安全漏洞，其中一半存在于你无法控制的嵌套依赖项中。这款工具会分析审计结果，并为你提供可行的修复建议：哪些漏洞需要处理，哪些可以忽略，以及针对每个漏洞应采取的具体措施。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npm audit --json | npx ai-audit-fix
```

## 功能介绍

- 分析 `npm audit` 的输出结果，并根据实际风险对漏洞进行优先级排序
- 确定哪些漏洞确实会影响你的代码
- 为每个问题提供具体的修复命令
- 指导何时需要覆盖现有配置，何时需要实际进行修复
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

- **优先处理生产环境依赖项**：开发环境依赖项不会被部署给用户
- **检查是否存在被实际使用的漏洞代码**：许多漏洞存在于你从未使用的代码路径中
- **先更新父包**：这通常可以一次性修复多个嵌套的漏洞
- **谨慎使用覆盖配置**：记录覆盖配置的原因，并设置提醒以便后续复查

## 适用场景

- 当 `npm audit` 的结果显示大量红色警告，而你不知道从何开始时
- 当持续集成（CI）的安全检查失败时
- 需要将漏洞情况报告给安全团队时
- 在决定是否因安全问题推迟发布时

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也无需使用 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-audit-fix --help
```

## 工作原理

该工具会解析 `npm audit` 的 JSON 输出，分析每个漏洞的依赖链和严重程度，判断其是否会影响你的生产环境代码，然后生成带有具体修复命令的优先级建议。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-audit-fix](https://github.com/lxgicstudios/ai-audit-fix)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)
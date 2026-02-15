---
name: gatewaystack-governance
description: 对于每一次工具调用，都采用“默认拒绝”（Deny-by-default）的治理策略：包括身份验证、权限范围控制、速率限制、注入检测以及审计日志记录等功能。这些机制通过进程级（process level）与 OpenClaw 进行集成，确保代理程序无法绕过这些安全措施。
user-invocable: true
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["node"] }, "homepage": "https://github.com/davidcrowe/openclaw-gatewaystack-governance" } }
---
# GatewayStack 管理框架

OpenClaw 中的所有工具调用均采用默认的“拒绝访问”策略。

每次工具调用时，系统会自动执行以下五项检查：

1. **身份验证**：将代理（agent）与相应的策略角色（policy role）进行匹配；未知的代理将被拒绝访问。
2. **权限控制**：根据默认的允许列表（allowlist）来决定是否允许使用工具；未列出的工具将被阻止。
3. **速率限制**：针对每个用户和每个会话设置滑动窗口（sliding window）限制。
4. **注入检测**：利用 Cisco、Snyk 和 Kaspersky 的检测规则来识别潜在的安全威胁。
5. **审计日志记录**：所有访问决策都会被记录到只读的 JSONL 格式日志文件中。

## 安装

```bash
openclaw plugins install @gatewaystack/gatewaystack-governance
```

只需执行一个命令即可完成安装，无需任何配置设置。所有工具调用都将立即受到管理框架的监控。

该插件会在进程级别（process level）拦截 `before_tool_call` 事件；代理无法绕过或规避这一机制。

## 自定义设置

如需覆盖默认规则，请创建一个策略文件（policy file）：

```bash
cp ~/.openclaw/plugins/gatewaystack-governance/policy.example.json \
   ~/.openclaw/plugins/gatewaystack-governance/policy.json
```

在该文件中，您可以配置允许使用的工具、使用这些工具的用户、速率限制以及注入检测的敏感度设置。

## 链接

- [GitHub](https://github.com/davidcrowe/openclaw-gatewaystack-governance)：源代码、文档及入门指南
- [npm](https://www.npmjs.com/package/@gatewaystack/gatewaystack-governance)：包注册库
- 采用 MIT 许可协议
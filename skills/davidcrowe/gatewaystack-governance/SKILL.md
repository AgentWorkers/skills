---
name: gatewaystack-governance
description: 所有工具调用均采用“默认拒绝”策略（即未经授权的请求将被拒绝）：包括身份验证、访问范围控制、速率限制、注入攻击检测、审计日志记录等功能。同时提供可选的数据丢失防护（DLP）功能、问题上报机制以及行为监控功能。这些机制通过进程级别的接口与 OpenClaw 集成，确保代理程序无法绕过这些安全控制措施。
user-invocable: true
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "bins": ["node"] }, "homepage": "https://github.com/davidcrowe/openclaw-gatewaystack-governance" } }
---
# GatewayStack 管理机制

OpenClaw 对所有工具调用均采用“默认拒绝”策略（即未经授权的调用将被拒绝）。

每次工具调用时，系统会自动执行五项核心检查：

1. **身份验证**：将代理（agent）与相应的策略角色进行匹配；未知的代理会被拒绝访问。
2. **权限控制**：根据预设的允许列表来决定是否允许使用特定工具；未列出的工具将被阻止。
3. **速率限制**：针对每个用户和每个会话设置滑动窗口限制（即限制工具调用的频率）。
4. **注入检测**：利用 Cisco、Snyk 和 Kaspersky 的检测规则来识别潜在的安全威胁。
5. **审计日志记录**：所有决策都会被记录到只读的 JSONL 文件中。

此外，还有三项可选功能可以进一步增强管理机制：

6. **输出数据保护（Output DLP）**：使用 `@gatewaystack/transformabl-core` 模块扫描工具输出内容，以检测其中是否包含个人身份信息（PII），并可以选择记录这些信息或对其进行屏蔽。
7. **异常处理**：对于中等严重性的安全事件或首次使用某些工具的情况，系统会触发人工审核流程。
8. **行为监控**：利用 `@gatewaystack/limitabl-core` 模块检测工具使用的异常行为模式。

## 安装

只需执行一个命令即可完成安装，无需任何额外配置。所有核心检查功能会在每次工具调用时立即生效。

该插件会在进程级别拦截 `before_tool_call` 事件，代理无法绕过或规避这一检查机制。

## 自定义设置

如需修改默认配置，可以创建一个策略文件（如 **CODE_BLOCK_1___ 所示），以指定允许使用的工具、使用工具的用户、速率限制以及是否启用上述三项可选功能（默认情况下这些功能都是禁用的）。

## 可选的 GatewayStack 插件包

可选的功能需要通过 GatewayStack 的插件包来实现。只需安装实际需要的插件包即可（如 **CODE_BLOCK_2___ 所示）。

需要注意的是，核心的五项检查功能本身不依赖于任何外部插件包，因此即使未安装这些插件包，它们也能正常运行。

## 链接

- [GitHub](https://github.com/davidcrowe/openclaw-gatewaystack-governance)：源代码、文档及入门指南
- [npm](https://www.npmjs.com/package/@gatewaystack/gatewaystack-governance)：包注册表
- 该插件采用 MIT 许可协议。
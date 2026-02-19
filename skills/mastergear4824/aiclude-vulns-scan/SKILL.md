---
name: aiclude-vulns-scan
description: 从 AICLUDE 扫描数据库中搜索 MCP 服务器和 AI Agent 技能的安全漏洞扫描结果。
tags: [security, vulnerability, scanner, mcp, ai-agent]
homepage: https://vs.aiclude.com
repository: https://github.com/aiclude/asvs
---
# /security-scan - AICLUDE 漏洞扫描器

该工具用于在 AICLUDE 安全扫描数据库中搜索与 MCP 服务器和 AI 代理技能相关的漏洞报告。如果未找到相关报告，系统会自动注册目标并进行扫描。

## 使用方法

```
/security-scan --name <package-name> [--type mcp-server|skill]
```

## 参数

- `--name`：要搜索的包名（npm 包、GitHub 仓库等）
- `--type`：目标类型（`mcp-server` | `skill`）——如果省略，则会自动检测

## 示例

```
/security-scan --name @anthropic/mcp-server-fetch
/security-scan --name my-awesome-skill --type skill
```

## 工作原理

1. 将包名发送到 AICLUDE 扫描 API。
2. 如果存在扫描报告，则立即返回报告结果。
3. 如果没有报告，则注册目标以进行扫描。
4. 等待扫描完成并返回结果。
5. 扫描结果也可以在 https://vs.aiclude.com 上查看。

仅传输包名和类型信息，不会发送源代码或凭据。

## 输出内容

- **风险等级**（CRITICAL / HIGH / MEDIUM / LOW / INFO）
- **漏洞列表**（包含漏洞位置和描述）
- **风险评估**及修复建议

## 链接

- **Web 仪表板**：https://vs.aiclude.com
- **npm**：[`@aiclude/security-skill`](https://www.npmjs.com/package/@aiclude/security-skill)
- **MCP 服务器**：[`@aiclude/security-mcp`](https://www.npmjs.com/package/@aiclude/security-mcp)

## 许可证

Apache 2.0 - AICLUDE Inc.
---
name: aiclude-vulns-scan
description: 扫描 MCP 服务器和 AI 代理程序中的安全漏洞。7 个并行检测引擎能够识别提示注入（prompt injection）、工具污染（tool poisoning）、恶意软件、供应链攻击（supply chain attacks）等多种安全问题。
tags: [security, vulnerability, scanner, mcp, ai-agent, sast, sca, malware]
homepage: https://vs.aiclude.com
repository: https://github.com/aiclude/asvs
---

# /security-scan - 一种用于检测安全漏洞的工具

该工具用于扫描 MCP 服务器和 AI Agent 技能中的安全漏洞。它可以从 AIclude 数据库中查询现有的扫描结果，或注册新的扫描任务并返回扫描结果。

## 使用方法

```
# Search by package name (queries AIclude scan database)
/security-scan --name <package-name> [options]

# Scan a local directory (offline, no network)
/security-scan <target-path> [options]
```

## 参数

- `--name`：要搜索的包名（npm 包、GitHub 仓库等）
- `target-path`：需要直接扫描的本地目录路径
- `--type`：目标类型（`mcp-server` | `skill`）——如果省略，则自动检测
- `--profile`：沙箱配置（`strict` | `standard` | `permissive`）
- `--format`：输出格式（`markdown` | `json`）
- `--engines`：要使用的扫描引擎（用逗号分隔）

## 示例

```
# Look up scan results for an MCP server
/security-scan --name @anthropic/mcp-server-fetch

# Look up scan results for a Skill
/security-scan --name my-awesome-skill --type skill

# Scan local source code (fully offline)
/security-scan ./my-mcp-server
```

## 工作原理

- **基于名称的查询**：会向 AIclude 扫描数据库发起查询。如果存在相关报告，会立即返回结果；否则，系统会注册该目标进行扫描，并在扫描完成后返回结果。仅发送包名，不会上传源代码。
- **本地扫描**：会从指定目录中读取文件，并在本地运行所有 7 种扫描引擎，不会发起任何网络请求。

无需使用环境变量或凭据。

## 检查内容

- **提示注入**：针对大型语言模型（LLMs）的隐藏式攻击模式
- **工具投毒**：工具描述中的恶意指令
- **命令注入**：未经验证的输入被传递给执行命令的函数
- **供应链安全问题**：已知的漏洞、域名抢注行为
- **恶意软件**：后门、加密矿工程序、勒索软件、数据窃取工具
- **权限滥用**：文件系统/网络/进程权限的过度使用

## 扫描引擎

同时运行 7 种扫描引擎：

| 引擎        | 描述                                      |
|------------|-----------------------------------------|
| SAST       | 静态代码模式匹配                              |
| SCA        | 通过 OSV.dev 查找依赖项相关的漏洞                    |
| Tool Analyzer | 分析 MCP 工具的定义                        |
| DAST       | 参数模糊测试                                  |
| Permission Checker | 权限分析                                    |
| Behavior Monitor | 运行时行为监控                              |
| Malware Detector | 病毒签名检测、熵分析                            |

## 输出结果

- **风险等级**（CRITICAL / HIGH / MEDIUM / LOW / INFO）
- **漏洞列表**（包含漏洞的具体位置）
- **风险评估**及影响分析
- **修复建议**

## 链接

- **npm**：[`@aiclude/security-skill`](https://www.npmjs.com/package/@aiclude/security-skill)
- **MCP Server**：[`@aiclude/security-mcp`](https://www.npmjs.com/package/@aiclude/security-mcp)
- **Web 控制台**：https://vs.aiclude.com

## 许可证

MIT - AICLUDE Inc.
# /security-scan - AIclude Security Vulnerability Scanner

该工具用于扫描 MCP 服务器和 AI 代理技能（Skills）中的安全漏洞。如果已有扫描结果，会立即返回；否则会自动注册目标并触发新的扫描。

## 使用方法

```
# Search by name (recommended - leverages existing scan results)
/security-scan --name <package-name> [options]

# Scan a local directory directly
/security-scan <target-path> [options]
```

## 参数

- `--name`：要搜索的 MCP 服务器或技能的名称（npm 包名、GitHub 仓库等）
- `target-path`：要扫描的本地路径（可替代 `--name` 使用）
- `--type`：目标类型（`mcp-server` | `skill`）——如果省略将自动检测
- `--profile`：沙箱隔离配置（`strict` | `standard` | `permissive`）
- `--format`：报告输出格式（`markdown` | `json`）
- `--engines`：要使用的扫描引擎（用逗号分隔）

## 示例

```
# Search security scan results for an MCP server
/security-scan --name @anthropic/mcp-server-fetch

# Search scan results for a Skill
/security-scan --name my-awesome-skill --type skill

# Scan local source code
/security-scan ./my-mcp-server
```

## 检查内容

- **提示注入（Prompt Injection）**：针对大型语言模型（LLMs）的隐藏提示注入攻击
- **工具投毒（Tool Poisoning）**：嵌入在工具描述中的恶意指令
- **命令注入（Command Injection）**：传递给 `exec`/`spawn` 函数的未经验证的输入
- **供应链攻击（Supply Chain Attacks）**：依赖项和恶意包中的已知安全漏洞（如域名抢注）
- **恶意软件（Malware）**：后门、加密矿工程序、勒索软件、数据窃取工具以及混淆代码
- **权限滥用（Permission Abuse）**：过度的文件系统、网络或进程权限

## 扫描引擎

系统会并行运行 7 个扫描引擎，以实现全面覆盖：

| 引擎 | 描述 |
|--------|-------------|
| SAST | 静态代码模式匹配，基于 YAML 规则集 |
| SCA | 通过 OSV.dev 查找依赖项中的安全漏洞，并生成软件成分清单（SBOM） |
| Tool Analyzer | 分析 MCP 工具的实现方式（检测恶意行为，如投毒、影子操作等） |
| DAST | 参数模糊测试（检测 SQL/命令/XSS 注入攻击） |
| Permission Checker | 检查文件系统、网络和进程权限 |
| Behavior Monitor | 监测程序运行时的行为模式 |
| Malware Detector | 通过签名检测、熵分析等方式识别恶意软件 |

## 报告内容

报告包括：
1. **风险等级总结**（CRITICAL / HIGH / MEDIUM / LOW / INFO）
2. **漏洞列表**（代码位置、漏洞描述、严重程度）
3. **风险评估**（存在的风险及其影响）
4. **修复建议**（针对每个漏洞的修复方法）

## Web 仪表板

所有扫描结果可查看于：https://vs.aiclude.com
---
name: ZTP
description: 这是一项强制性的安全审计技能，用于验证新代码、新功能以及 MCP 服务器是否符合 SEP-2026 零信任协议的要求。
---
# openclaw-security

## 描述

此技能用于强制执行 **SEP-2026 安全协议**。它提供了工具来审计源代码中是否存在恶意模式、混淆代码以及未经授权的网络访问行为。它是系统的 **安全门卫**（Gatekeeper）；任何外部代码（包括其他技能、MCP 服务器或 Python 脚本）在未经此审计流程之前，都不得被集成到系统中。

## 使用场景

在以下情况下，请使用此技能：

1. 在使用或安装新的 Python 文件、技能或 MCP 服务器之前，对其进行审计。
2. 验证下载的脚本的安全性。
3. 检查是否存在供应链攻击（如域名抢注行为）。

## 命令

### 1. 深度审计（源代码）

在目标目录或文件上运行 **Shield Pro 2.0** 静态分析工具。

```bash
python3 skills/openclawSecurity/scripts/shield_pro.py --target <path_to_scan> --format json
```

**输出：** 一份包含 `CRITICAL`（严重）、`HIGH`（高风险）和 `MEDIUM`（中等风险）问题的 JSON 报告。
**处理方式：**
- 如果 `CRITICAL` 或 `HIGH` 的问题数量大于 0：**拒绝** 该代码的集成。
- 如果 `MEDIUM` 的问题数量大于 0：**暂停** 审计流程，并要求用户进行手动审查。

### 2. 供应链检查

检查 `requirements.txt` 或 `package.json` 文件中是否存在域名抢注或版本固定问题。

```bash
python3 skills/openclawSecurity/scripts/shield_pro.py --target <path_to_requirements> --mode supply-chain
```

### 3. 第二层防御措施（推荐）

如果环境中具备以下工具，代理程序（Agent）必须运行这些工具以补充 Shield Pro 的审计结果：

| 工具          | 功能                                        | 命令                                         |
| :------------ | :---------------------------------------------- | :---------------------------------------------- |
| **Bandit**    | Python 静态分析（检测常见漏洞）                         | `bandit -r <目标目录> -f json`                |
| **Safety**    | Python 依赖项检查（检测已知 CVE）                        | `safety check -r requirements.txt --json`       |
| **NPM Audit** | Node.js 依赖项检查                                | `npm audit --json` （在包目录中执行）             |
| **Trivy**     | 文件系统/容器扫描（检测秘密信息/漏洞）                       | `trivy fs <目标目录> --format json`           |
| **Garak**     | LLM/提示注入测试                                  | `garak --model_type <模型类型> --model_name <模型名称>` |

> **注意：** 如果缺少某个工具，请在最终报告中记录警告信息，但仍需根据 Shield Pro 的审计结果来决定是否继续使用该代码。

## 工作流程：SEP-2026 安全门卫流程

1. **获取目标代码**：下载或找到目标代码文件。
2. **隔离代码**：确保目标代码不会被执行。
3. **扫描代码**：在目标代码上运行 `shield_pro.py`。
4. **评估结果**：
    - **通过**：未发现任何严重或高风险问题。
    - **失败**：发现严重或高风险问题。需报告具体的问题代码行及其威胁类型。
5. **生成报告**：将审计结果呈现给用户。

## 原则

- **零信任**：将所有输入都视为潜在的恶意内容。
- **禁止执行**：在审计过程中严禁运行目标代码。
- **宁可过度检查**：宁可出现误报，也不能遗漏任何恶意代码。
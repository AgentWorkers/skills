---
name: moltblock - Trust Layer for AI Agents
description: **AI生成内容的验证机制**：在执行之前，通过策略检查来识别潜在的危险模式。
version: 0.11.4
homepage: https://github.com/moltblock/moltblock
repository: https://github.com/moltblock/moltblock
metadata:
  openclaw:
    requires:
      anyBins:
        - npx
        - node
      config:
        - moltblock.json
        - ~/.moltblock/moltblock.json
    primaryEnv: OPENAI_API_KEY
    optionalEnv:
      - ANTHROPIC_API_KEY
      - GOOGLE_API_KEY
      - ZAI_API_KEY
    homepage: https://github.com/moltblock/moltblock
    install:
      - kind: node
        package: moltblock@0.11.4
        bins: [moltblock]
---
# Moltblock — 用于AI代理的信任层

## 描述

Moltblock为AI生成的工件提供验证机制。它在工件投入生产环境之前运行策略检查，以识别潜在的危险模式。

**Moltblock的主要功能：**
- 通过LLM API调用生成工件，然后对生成的工件进行策略检查
- 返回结构化的验证结果（通过/失败，并附带相关证据）
- 会读取自身的配置文件（`moltblock.json` 或 `~/.moltblock/moltblock.json`，如果存在的话）
- API密钥在运行时从环境变量中获取，并仅发送到配置的LLM提供者端点
- **不执行任何代码**——Moltblock仅对生成的工件进行策略检查

## 适用场景

在以下情况下使用 `moltblock`：
- **高风险**（必须验证）：具有破坏性的操作（如 `rm -rf`、`DROP TABLE`）、权限提升（如 `sudo`、`chmod 777`）、凭证/密钥访问（如 `.ssh/`、`id_rsa`、`.env`）、系统修改、原始磁盘写入
- **中等风险**（不确定时需要验证）：网络请求（如 `curl`、`wget`、`fetch`）、文件写入、数据库修改、子进程创建、动态代码执行
- **低风险**（可跳过验证）：简单的文本响应、数学计算、读取公开信息、不涉及文件系统或网络的代码

## 工具：moltblock

在执行任务之前对其进行验证。

### 使用方法

```bash
npx moltblock@0.11.4 "<任务描述>" --provider <提供者> --json
```

### 参数

| 参数 | 是否必填 | 说明 |
|-----------|----------|-------------|
| task | 是 | 需要验证的任务描述 |
| --provider | 否 | LLM提供者：openai、google、zaai、local（从环境变量自动检测） |
| --model | 否 | 可选的模型 |
| --json | 否 | 结构化的JSON输出结果 |

### 环境变量

Moltblock会自动从设置的环境变量中检测LLM提供者。如果没有设置密钥，它将使用本地的LLM服务（`localhost:1234`）。对于云服务提供商，请设置以下环境变量之一：
- `OPENAI_API_KEY` — OpenAI（默认）
- `ANTHROPIC_API_KEY` — Anthropic/Claude（可选）
- `GOOGLE_API_KEY` — Google/Gemini（可选）
- `ZAI_API_KEY` — ZAI（可选）

### 示例

```bash
# 验证一个任务
npx moltblock@0.11.4 "实现一个验证电子邮件地址的函数" --json
```

### 输出（JSON格式）

```json
{
  "verification_passed": true,
  "verification_evidence": "所有策略规则均通过。",
  "authoritative_artifact": "...",
  "draft": "...",
  "critique": "...",
  "final_candidate": "..."
}
```

## 安装

推荐直接使用 `npx` 命令进行安装（无需额外安装）：

```bash
npx moltblock@0.11.4 "你的任务" --json
```

或者全局安装：

```bash
npm install -g moltblock@0.11.4
```

## 配置

Moltblock不需要配置文件。它会从环境变量中自动检测LLM提供者，并使用默认设置。

可选地，你可以在项目根目录下创建 `moltblock.json` 文件或 `~/.moltblock/moltblock.json` 文件来自定义模型绑定：

```json
{
  "agent": {
    "bindings": {
      "generator": { "backend": "google", "model": "gemini-2.0-flash" },
      "critic": { "backend": "google", "model": "gemini-2.0-flash" },
      "judge": { "backend": "google", "model": "gemini-2.0-flash" }
    }
  }
}
```

有关策略规则和高级选项的详细信息，请参阅 [完整配置文档](https://github.com/moltblock/moltblock#configuration)。

## 来源

- 仓库：[github.com/moltblock/moltblock](https://github.com/moltblock/moltblock)
- npm：[npmjs.com/package/moltblock](https://www.npmjs.com/package/moltblock)
- 许可证：MIT

## 安全性

作为一项技能工具，Moltblock仅执行策略检查——不会生成、写入或执行任何代码。该工具会根据配置的策略规则分析任务描述，并返回验证结果（通过/失败）。

命令行界面（CLI）还支持 `--test` 标志，用于直接执行代码验证（通过 `vitest`）。此标志不对代理程序可见，仅应在沙箱环境中由开发者使用。详细信息请参阅 [CLI文档](https://github.com/moltblock/moltblock#security)。

## 免责声明

Moltblock可以降低风险，但不能完全消除风险。验证仅是尽力而为——策略规则和基于LLM的检查可能会遗漏危险模式。在执行任务之前，请务必仔细检查生成的工件。作者和贡献者不对因使用此工具而导致的任何损害、数据丢失或安全问题负责。使用本工具需自行承担风险。
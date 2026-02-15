---
name: moltblock - Trust Layer for AI Agents
description: 针对人工智能生成的成果（artifacts），实施验证机制。通过策略检查（policy checks）和代码验证（code verification）来在执行前识别出潜在的危险模式（dangerous patterns）。
version: 0.11.0
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
        package: moltblock@0.11.0
        bins: [moltblock]
---

# Moltblock — 为AI代理提供信任层

## 描述

Moltblock为AI生成的代码或资源提供验证机制。它通过执行策略检查以及可选的代码验证（通过vitest）来在代码或资源投入生产环境之前捕获潜在的危险行为。

**Moltblock的功能：**
- 通过调用LLM（Large Language Model）API生成代码，然后对生成的代码进行策略检查；
- 如果指定了`--test`参数，它会使用用户提供的测试文件（详见下文“安全：测试执行”部分）来验证生成的代码；
- 如果存在配置文件（`moltblock.json`或`~/.moltblock/moltblock.json`），则会读取这些文件；
- API密钥在运行时从环境变量中获取，并仅发送到配置的LLM提供商的端点。

## 适用场景

在以下情况下使用`moltblock`：
- **高风险**（必须进行验证）：具有破坏性操作（如`rm -rf`、`DROP TABLE`）、权限提升（如`sudo`、`chmod 777`）、凭证/密钥访问（如`.ssh/`、`id_rsa`、`.env`）、系统修改、直接写入磁盘等；
- **中等风险**（在不确定的情况下进行验证）：网络请求（如`curl`、`wget`、`fetch`）、文件写入、数据库修改、子进程创建、动态代码执行等；
- **低风险**（可以跳过验证）：简单的文本响应、数学计算、读取公共信息、不涉及文件系统或网络的代码等。

## 工具：moltblock

在执行任务之前对其进行验证。

### 使用方法

```bash
npx moltblock@0.11.0 "<task description>" --provider <provider> --json
```

### 参数

| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| task     | 是       | 需要验证的任务描述 |
| --provider | 否       | LLM提供商（openai、google、zaai或本地，默认从环境变量自动检测） |
| --model    | 否       | 可选的模型名称 |
| --test     | 否       | 测试文件的路径（用于代码验证） |
| --json     | 否       | 结果以结构化JSON格式输出 |

### 环境变量

Moltblock会根据设置的API密钥自动检测LLM提供商。如果没有设置密钥，它将使用本地的LLM服务（地址为`localhost:1234`）。以下是针对云服务提供商的密钥设置：
- `OPENAI_API_KEY` — OpenAI（默认） |
- `ANTHROPIC_API_KEY` — Anthropic/Claude（可选） |
- `GOOGLE_API_KEY` — Google/Gemini（可选） |
- `ZAI_API_KEY` — ZAI（可选） |

### 示例

```bash
# Verify a task
npx moltblock@0.11.0 "implement a function that validates email addresses" --json

# Verify code with tests
npx moltblock@0.11.0 "implement a markdown-to-html converter" --test ./tests/markdown.test.ts --json
```

### 输出（JSON格式）

```json
{
  "verification_passed": true,
  "verification_evidence": "All policy rules passed.",
  "authoritative_artifact": "...",
  "draft": "...",
  "critique": "...",
  "final_candidate": "..."
}
```

## 安装

推荐使用`npx`直接运行（无需安装）：

```bash
npx moltblock@0.11.0 "your task" --json
```

或者全局安装：

```bash
npm install -g moltblock@0.11.0
```

## 配置

Moltblock不需要额外的配置文件。它会从环境变量中自动检测LLM提供商，并使用默认设置。如果需要，可以将`moltblock.json`文件放在项目根目录或`~/.moltblock/moltblock.json`中以自定义模型配置：

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

有关策略规则和高级选项的详细信息，请参阅[完整配置文档](https://github.com/moltblock/moltblock#configuration)。

## 来源

- 仓库：[github.com/moltblock/moltblock](https://github.com/moltblock/moltblock) |
- npm：[npmjs.com/package/moltblock](https://www.npmjs.com/package/moltblock) |
- 许可证：MIT

## 安全：测试执行

当使用`--test`参数时，Moltblock会将LLM生成的代码写入临时文件，并使用用户提供的测试文件对其进行验证。**此过程会在主机上的Node.js进程中执行LLM生成的代码。** 安全措施包括：
- 测试文件的路径必须由用户明确提供——Moltblock不会自动选择或生成测试文件；
- 生成的代码会被写入`os.tmpdir()`目录，并在执行后清除；
- 在执行测试之前，会先运行策略检查以阻止已知危险的操作（如`rm -rf`、`eval`、`child_process`、文件系统写入等）；
- 如果未使用`--test`参数，则不会执行任何代码——仅对生成的代码进行策略检查。

**剩余风险**：策略检查基于模式识别，可能无法捕获所有危险代码。通过`--test`参数执行的LLM生成代码可能在Node.js进程的权限范围内执行任意操作。在验证不可信的任务时，建议用户审查生成的代码或在沙箱环境中运行Moltblock。

## 免责声明

Moltblock可以降低风险，但无法完全消除风险。验证仅是尽力而为——策略检查和基于LLM的检测方法可能会遗漏某些危险行为。在使用该工具之前，请务必仔细审查生成的代码或资源。作者和贡献者不对因使用本工具而导致的任何损害、数据丢失或安全问题负责。请自行承担使用风险。
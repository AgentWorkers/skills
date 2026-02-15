---
name: aegis-audit
description: >
  Deep behavioral security audit for AI agent skills and MCP tools. Performs deterministic
  static analysis (AST + Semgrep + 15 specialized scanners), cryptographic lockfile generation,
  and optional LLM-powered intent analysis. Use when installing, reviewing, or approving any
  skill, tool, plugin, or MCP server — especially before first use. Replaces basic safety
  summaries with full CWE-mapped, OWASP-tagged, line-referenced security reports.
version: 0.1.10
homepage: https://github.com/Aegis-Scan/aegis-scan
url: https://pypi.org/project/aegis-audit/
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/Aegis-Scan/aegis-scan","requires":{"bins":["aegis"],"config":["~/.aegis/config.yaml"]},"install":[{"kind":"uv","package":"aegis-audit","bins":["aegis"]}]}}
---

# Aegis Audit

Aegis 是一款用于检测 AI 代理技能（skills）和 MCP 工具安全性的行为安全扫描工具。它通过分析代码来识别潜在的恶意模式，帮助用户避免安装可能存在风险的技能。该工具本身不会用于发起攻击，而是用于在用户使用技能之前对其进行安全评估。

> Aegis 会扫描 AI 代理技能的 SSL 证书，对其进行验证，并在用户决定使用之前提供相应的安全报告。

**来源：** [github.com/Aegis-Scan/aegis-scan](https://github.com/Aegis-Scan/aegis-scan) | **包：** [pypi.org/project/aegis-audit](https://pypi.org/project/aegis-audit/) | **许可证：** AGPL-3.0

---

## Aegis 的主要功能

Aegis 能够回答每个代理用户都会提出的问题：“这个技能到底能做什么？我应该信任它吗？”

- **确定性静态分析**：通过 AST 解析、Semgrep 和 15 种专用扫描器对代码进行安全检查。相同的代码每次都会生成相同的扫描结果。
- **精确的权限检测**：不仅能检测代码是否访问文件系统，还能明确指出具体访问了哪些文件、URL、主机和端口。
- **风险评分**：基于 CWE/OWASP 标准给出 0-100 的综合评分。
- **加密验证**：使用 Ed25519 算法对锁文件（lockfile）进行签名，并通过 Merkle 树结构防止篡改。
- **可选的 LLM 分析**：用户可以自行选择使用的 LLM 服务（如 Gemini、Claude、OpenAI、Ollama 等），但默认是禁用的。启用此功能前请阅读以下隐私声明。

---

## 安装方法

可以通过 [PyPI](https://pypi.org/project/aegis-audit/) 使用 `pip` 或 `uv` 命令进行安装：

（安装命令略）

安装完成后，`aegis` 命令行工具（CLI）将添加到系统的 `PATH` 环境变量中。

---

## 快速使用指南

Aegis 默认情况下完全离线运行，无需网络连接，也不会将任何数据传输到外部。

（使用方法略）

---

## 命令行参考

| 命令 | 功能 |
| --- | --- |
| `aegis scan [路径]` | 进行全面的安全扫描并生成风险评分报告 |
| `aegis lock [路径]` | 扫描指定路径并生成加密签名的 `aegis.lock` 文件 |
| `aegis verify [路径]` | 核对锁文件与实际代码的一致性 |
| `aegis badge [路径]` | 生成用于展示安全状态的徽章（markdown 格式） |
| `aegis setup` | 开启交互式 LLM 配置向导 |
| `aegis mcp-serve` | 启动 MCP 服务器（使用标准输入输出方式） |
| `aegis mcp-config` | 输出 MCP 服务器的配置信息（JSON 格式） |
| `aegis version` | 显示 Aegis 的版本信息 |

**常用参数：** `--no-llm`（禁用 LLM 分析，默认值），`--json`（生成 JSON 格式的扫描结果），`-v`（详细输出）。

---

## 锁文件（Lockfiles）

扫描完成后，Aegis 会生成一个加密签名的锁文件 `aegis.lock`，该文件记录了技能的安全状态。开发者可以将此文件与技能代码一起提交，以便其他用户验证代码是否被修改。

**验证锁文件：** 如果自锁文件生成后有任何文件被修改，Merkle 树结构将不匹配，验证会失败。

---

## 可选功能：LLM 分析

**隐私声明：** LLM 分析功能默认是禁用的。启用该功能后，Aegis 会将扫描到的代码发送到用户配置的第三方 LLM 服务（如 Google Gemini、OpenAI 或 Anthropic）。除非用户明确配置 API 密钥并使用 `--no-llm` 选项，否则不会传输任何数据。请确保仅在信任相关服务提供商的情况下才启用此功能。

要启用 LLM 分析，请执行相应的配置操作：

（配置命令略）

配置文件会保存在 `~/.aegis/config.yaml` 中。也可以通过设置以下环境变量来启用 LLM 功能：
- `GEMINI_API_KEY`（Google Gemini）
- `OPENAI_API_KEY`（OpenAI）
- `ANTHROPIC_API_KEY`（Anthropic Claude）

这些环境变量是可选的。即使不设置这些变量，Aegis 也能正常离线运行。只有在需要 AI 评估功能的情况下才需要设置这些变量，并且需要接受扫描结果会被发送给相应的服务提供商。

对于本地 LLM 服务器（如 Ollama、LM Studio、lama.cpp、vLLM），请参考 `aegis setup` 的说明——使用本地模型时不会传输任何数据。

---

## MCP 服务器

Aegis 可以作为 MCP 服务器为 Cursor、Claude Desktop 等工具提供安全扫描服务。它提供了以下三个 API 接口：
- `scan_skill`：扫描技能的安全性
- `verify_lockfile`：验证锁文件的有效性
- `list_capabilities`：列出技能的详细功能

可以在 `.cursor/mcp.json` 文件中配置这些 API 接口，或者使用自动配置工具进行配置。

Aegis 使用标准输入输出（stdio）进行通信，因此不需要额外的网络服务器。

---

## 扫描内容

Aegis 支持多种扫描方式，能够检测以下安全问题：
- **AST 解析器**：检测 Python 代码中的 750 多种函数/方法模式
- **Semgrep 规则**：针对 Python、JavaScript 和敏感数据的 80 多种正则表达式规则
- **秘密信息扫描器**：检测 API 密钥、令牌、私钥等敏感信息
- **Shell 分析器**：检测 shell 命令、反向 shell 连接等安全风险
- **JavaScript 分析器**：检测 XSS、eval 语句、原型污染等安全问题
- **Dockerfile 分析器**：检查 Dockerfile 中的权限提升风险
- **配置文件分析器**：分析 YAML、JSON、TOML、INI 格式的配置文件中的安全隐患
- **社会工程学攻击检测**：检测误导性文件名、Unicode 欺骗等行为
- **隐写术检测**：检测图片中的隐藏数据
- **组合攻击检测**：检测多种攻击链（如数据泄露、勒索软件等）
- **代码复杂性分析**：评估代码的复杂性
- **技能元数据分析**：对比 SKILL.md 文件与实际代码的差异
- **信任度评估**：根据代码特性生成信任等级（如 LGTM、Permission Goblin 等）

---

## Aegis 的信任等级评估

Aegis 会根据扫描结果为每个技能分配一个信任等级：
- **Cracked Dev**：代码干净，逻辑清晰，权限设置合理
- **LGTM**：权限设置符合预期，代码结构正常
- **Trust Me Bro**：表面看起来安全，但实际上可能存在问题
- **You Sure About That?**：代码混乱，文档描述与实际功能不符
- **Co-Dependent Lover**：依赖关系复杂，存在供应链风险
- **Permission Goblin**：试图获取系统所有权限（文件系统、网络、敏感数据）
- **Spaghetti Monster**：代码难以理解，具有高复杂性
- **The Snake**：代码看似正常，但实际上可能包含恶意代码

---

## JSON 报告格式

Aegis 生成的 JSON 报告包含两部分内容：
- **确定性数据**：包含 Merkle 树结构、技能功能、检测结果和风险评分（可重现且经过签名）
- **临时数据**：包含 LLM 分析的结果和风险调整信息（非确定性数据，未签名）

---

## 对技能开发者的建议

在发布技能之前，请先使用 Aegis 对代码进行安全扫描：
- 修复检测到的安全问题
- 对受限制的功能进行适当处理
- 确保随技能代码一起提供加密签名的 `aegis.lock` 文件

更多详细信息请参考 [技能开发者最佳实践文档](https://github.com/Aegis-Scan/aegis-scan/blob/main/docs/SKILL_DEVELOPER_GUIDE.md)。

---

## 架构说明

Aegis 的架构设计考虑了灵活性和安全性需求。

---

## 许可证信息

Aegis 采用双重许可机制：
- **开源许可证（AGPL-3.0）**：允许免费使用、修改和分发。如果将 Aegis 用于网络服务，必须公开源代码。
- **商业许可证**：适用于需要将 Aegis 集成到商业产品中的情况，此时提供专有许可证，但需遵守相关条款和支持要求。

更多许可详情请参阅 [LICENSING.md](https://github.com/Aegis-Scan/aegis-core/LICENSING.md)。

---

## 贡献方式

欢迎贡献代码和功能。贡献者需遵守 [贡献者许可协议](https://github.com/Aegis-Scan/aegis-scan/blob/main/aegis-core/CLA.md)。

---

**系统要求：** Aegis 需要 Python 3.11 或更高版本。进行确定性扫描时不需要网络连接，支持离线运行。
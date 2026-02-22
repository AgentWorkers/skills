---
name: bounty-hunter
description: 自动化智能合约漏洞赏金计划：使用 Slither 进行静态分析，扫描 Immunefi/Code4rena 目标项目；利用本地大型语言模型（LLM）对分析结果进行分类和筛选；自动生成漏洞验证（PoC）模板。扫描阶段完全无需支付任何 API 费用。
version: 1.0.0
---
# Bounty Hunter

这是一个用于漏洞赏金计划的自动化智能合约漏洞扫描工具。它利用免费的工具（Slither + 本地大语言模型，LLM）来完成大部分工作，从而避免使用昂贵的模型来编写概念验证（PoC）代码。

## 所需软件

- `slither-analyzer`（通过pip安装）：用于静态代码分析
- `solc-select`（通过pip安装）：用于管理Solidity编译器
- Node.js：用于执行脚本
- 可选：Ollama（搭配任意代码模型）用于本地漏洞分类

## 快速入门

```bash
# Scan a repo
bash scripts/scan.sh <github-repo-url> [src-dir]

# Triage findings (uses local LLM if available, otherwise prints raw)
bash scripts/triage.sh <scan-output.json>

# Generate PoC template for a finding
bash scripts/poc-template.sh <finding-id> <contract-address>
```

## 工作流程

1. **目标选择** — 在Immunefi/Code4rena平台上查找当前正在进行的活动赏金计划。
2. **克隆与扫描** — 使用`scan.sh`脚本克隆目标代码库，安装Solidity编译器，并运行Slither进行代码扫描。
3. **漏洞分类** — 使用`triage.sh`脚本过滤出高风险/中等风险的漏洞，并排除已知的误报。
4. **深入分析** — 仅查看Slither标记为有问题的代码部分（以节省你的奖励代币）。
5. **编写概念验证代码** — 使用`poc-template.sh`生成测试框架。
6. **提交报告** — 将扫描结果报告给Immunefi/Code4rena平台。

## 目标选择标准

在开始扫描之前，请检查以下条件：
- 代码库的更新时间在30天内（更新频繁的代码通常包含更多漏洞）。
- 过去的赏金金额超过5万美元（这些平台确实会支付赏金）。
- 目标代码库托管在GitHub上（而不仅仅是部署的地址）。
- 代码基于Solidity语言（Slither仅支持Solidity合约的扫描）。

## 避免的错误做法

- 不要手动阅读整个代码库——让Slither先进行扫描。
- 如果没有明确的线索，不要在一个目标上花费超过1小时的时间。
- 不要提交已知存在的漏洞（请先查看之前的报告）。
- 不要忽略代码的测试覆盖率——未经过测试的代码更容易隐藏漏洞。
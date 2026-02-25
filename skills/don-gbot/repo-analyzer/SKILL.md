---
name: repo-analyzer
description: GitHub仓库的信任评分与尽职调查功能：当您被要求分析、审计、评分或评估任何GitHub仓库时，该工具可派上用场——尤其适用于加密货币/去中心化金融（DeFi）项目的尽职调查，用于验证仓库的合法性、评估代码质量、核实团队信誉，或对比多个仓库。该工具还能处理包含GitHub链接的X/Twitter帖子，自动提取并分析这些帖子中的仓库信息。触发条件包括：“分析这个仓库”、“这个仓库是否合法”、“检查这个GitHub仓库”、“信任评分”、“审计这个项目”、“仓库质量”、“批量扫描仓库”以及“分析这条推文”。当用户粘贴包含GitHub链接的X/Twitter帖子时，系统也会自动触发该功能（无需用户明确输入“分析”命令）。如果通过推文触发分析，系统会在分析结果上方显示相应的推文内容/上下文。请注意：该工具不适用于常规的GitHub浏览、阅读README文件或未经分析直接克隆仓库的操作。
allowed-tools: "Bash(node:*) WebFetch"
compatibility: >
  Requires Node.js 18+. Uses GitHub API (gh CLI or unauthenticated).
  Zero external dependencies. Works on Linux/macOS. Handles rate limits with automatic retry and backoff (waits for reset if ≤60s, retries 5xx once).
metadata:
  author: DaDefiDon
  version: 1.2.0
  category: security-analysis
  tags: [github, trust-score, due-diligence, crypto, defi, audit]
---
# 仓库分析器（Repo Analyzer）

这是一个完全依赖零的外部库的 GitHub 信任评分工具，能够运行 29 个分析模块，覆盖 12 个评分类别。

## 使用方法

```bash
# Single repo
node scripts/analyze.js <owner/repo or github-url> [flags]

# From a tweet (auto-extracts GitHub links)
node scripts/analyze.js <x.com-or-twitter.com-url> [flags]

# Batch mode
node scripts/analyze.js --file <repos.txt> [--json]
```

### 命令行参数
- `--json`：以 JSON 格式输出结果（适用于自动化流程）
- `--oneline`：以简洁的一行格式显示评分结果
- `--badge`：生成适用于 shields.io 的 Markdown 评分徽章
- `--verbose`：显示分析过程中的详细进度
- `--token <pat>`：指定 GitHub 的个人访问令牌（PAT）；或通过环境变量 `GITHUB_TOKEN` 设置
- `--file <path>`：批量处理模式，每行表示一个仓库（支持包含注释的文件）

### 运行环境
**重要提示：** 必须在运行前加载 `GITHUB_TOKEN`。如果没有加载 `GITHUB_TOKEN`，评分结果将会严重失真（例如缺少星号、分支数量、提交记录等信息）。  
运行前请执行：`source ~/.bashrc`（`GITHUB_TOKEN` 通常存储在 `~/.bashrc` 文件中）。  
或者直接指定令牌：`GITHUB_TOKEN="$(grep GITHUB_TOKEN ~/.bashrc | cut -d'"' -f2)" node scripts/analyze.js ...`

## 评分标准（共 14 个类别，总分为 100 分）

| 评分类别 | 最高分 | 评分内容 |
|----------|-----|----------------|
| 提交质量（Commit Health） | 20 分 | 区分人工提交和机器提交、代码是否使用 GPG 签名、代码是否包含伪造的时间戳等 |
| 贡献者（Contributors） | 15 分 | 贡献者的数量和多样性 |
| 代码质量（Code Quality） | 25 分 | 代码是否有测试、是否使用持续集成（CI）工具、代码是否配有许可证和文档 |
| 代码真实性（AI Authenticity） | 15 分 | 代码或 README 文件中是否存在人工智能生成的痕迹 |
| 社交活跃度（Social） | 10 分 | 仓库的星号数量、分支数量、星号与分支的比例等 |
| 活动情况（Activity） | 10 分 | 最近的推送记录和发布版本 |
| 加密安全性（Crypto Safety） | 5 分 | 仓库是否涉及代币发行、是否存在恶意行为等 |
| 依赖关系审计（Dependency Audit） | 10 分 | 仓库是否使用了已知的恶意包、是否存在拼写错误、是否使用了安装脚本等 |
| 分支质量（Fork Quality） | 8 分 | 分支之间的差异程度、是否存在可疑的修改等 |
| README 文档质量（README Quality） | 10 分 | 是否有安装指南、示例代码、清晰的文档结构等 |
| 可维护性（Maintainability） | 10 分 | 文件大小、代码的复杂性以及代码与文档的比例等 |
| 项目整体状况（Project Health） | 10 分 | 仓库是否被弃用、项目更新频率、问题处理的及时性以及 PR 审核情况 |
| 原创性（Originality） | 5 分 | 代码是否为复制粘贴、是否使用了模板等 |
| 安全性（Agent Safety） | 15 分 | 仓库是否使用了安装脚本、是否存在提示注入等安全风险 |

## 评分等级
- A（85 分及以上）：非常可靠（LEGIT）
- B（70-84 分）：较为可靠（SOLID）
- C（55-69 分）：中等可靠性（MIXED）
- D（40-54 分）：可靠性较低（SKETCHY）
- F（低于 40 分）：应避免使用（AVOID）

## 主要功能
- **增强的依赖关系审计**：能够检测已知的恶意包、拼写错误攻击、安装脚本等安全问题，并评估依赖关系的复杂性。
- **分支对比**：分析分支之间的差异，识别出仅用于外观修改的分支，以及存在可疑修改的分支。
- **安全性检测**：能够检测提示注入、凭证收集等安全风险。
- **秘密信息检测**：通过正则表达式和熵分析技术，识别出硬编码的 API 密钥、令牌和私钥。
- **网络域名分类**：对所有外部域名（如 API、CDN 等）进行分类。
- **持续集成/持续部署审计**：检查 GitHub Actions 中的配置，确保没有安全隐患。
- **权限管理**：汇总代码运行所需的所有权限信息。
- **作者信誉评估**：分析作者的 GitHub 组织成员资格和仓库的活跃程度。
- **投资方验证**：核对投资方的声明与代码贡献者的组织成员资格。
- **代码复杂性分析**：标记出结构复杂、条件语句密集的文件。

## 批量处理文件格式
```
# One repo per line, # for comments
Uniswap/v3-core
https://github.com/aave/aave-v3-core
OpenZeppelin/openzeppelin-contracts
```

## 输出结果
默认情况下，会生成包含条形图和详细信息的终端报告。
- 使用 `--json` 参数时，会输出结构化的数据，便于程序化使用。
- 使用 `--oneline` 参数时，输出格式如下：`RepoName: 85/100 [A] — 2 个问题被标记为“警告”`。

## 向用户报告结果时应注意的事项
报告内容应简洁明了，先给出评分等级和主要发现的结果，跳过无关紧要的部分。例如：
“Uniswap/v3-core 的评分为 75/B：96% 的代码使用了 GPG 签名，有 11 位贡献者，采用 MIT 许可证。存在的问题包括：项目已被弃用（466 天未更新），存在 2,597 个冗余的依赖关系，CI 运行命令中包含敏感信息。安全性提示：请注意潜在的安全风险。”
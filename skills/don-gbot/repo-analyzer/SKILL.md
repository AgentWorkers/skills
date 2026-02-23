---
name: repo-analyzer
description: GitHub仓库的信任评分与尽职调查功能：当您被要求分析、审计、评分或评估任何GitHub仓库时，该工具可为您提供帮助——尤其适用于加密货币/去中心化金融（DeFi）项目的尽职调查。它可用于验证仓库的合法性、评估代码质量、核实团队信誉，或对比多个仓库。该工具还能处理包含GitHub链接的X/Twitter帖子，自动提取并分析这些帖子中的仓库信息。触发条件包括：“分析这个仓库”、“这个仓库是否合法”、“检查这个GitHub仓库”、“信任评分”、“审计这个项目”、“仓库质量”、“批量扫描仓库”以及“分析这条推文”。当用户粘贴包含GitHub链接的X/Twitter链接时，系统也会自动触发分析；无需用户明确输入“分析”命令。需要注意的是：该工具不适用于一般的GitHub浏览、阅读README文件或未经分析直接克隆仓库的操作。
allowed-tools: "Bash(node:*) WebFetch"
compatibility: >
  Requires Node.js 18+. Uses GitHub API (gh CLI or unauthenticated).
  Zero external dependencies. Works on Linux/macOS. Handles rate limits with automatic retry and backoff (waits for reset if ≤60s, retries 5xx once).
metadata:
  author: DaDefiDon
  version: 1.1.0
  category: security-analysis
  tags: [github, trust-score, due-diligence, crypto, defi, audit]
---
# 仓库分析工具（Repo Analyzer）

这是一个完全不依赖任何第三方库的GitHub信任评分工具，能够执行29个分析模块，覆盖12个评分类别。

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
- `--json`：以JSON格式输出结果（适用于自动化脚本）
- `--oneline`：以简洁的一行格式显示评分结果
- `--badge`：生成适用于shields.io的Markdown徽章
- `--verbose`：显示分析过程中的详细进度
- `--token <pat>`：指定GitHub访问令牌（或通过环境变量`GITHUB_TOKEN`设置）
- `--file <path>`：批量处理模式，每行对应一个仓库（支持包含注释的文件）

### 运行环境
**重要提示：** 必须在运行工具前确保`GITHUB_TOKEN`已设置。否则，评分结果会严重失真（例如缺少星星评分、分支信息或提交记录）。  
建议在运行前执行`source ~/.bashrc`（`GITHUB_TOKEN`通常存储在`~/.bashrc`文件中）。  
或者直接传递令牌：`GITHUB_TOKEN="$(grep GITHUB_TOKEN ~/.bashrc | cut -d'"' -f2)" node scripts/analyze.js ...`

## 评分标准（共14个类别，总分为100分）

| 评分类别 | 最高分 | 评分内容 |
|---------|---------|-------------------|
| 提交质量（Commit Health） | 20分 | 人工提交与机器提交的区分、代码的GPG签名、代码完整性检查、时间戳的真实性 |
| 贡献者（Contributors） | 15分 | 贡献者的数量及多样性 |
| 代码质量（Code Quality） | 25分 | 测试覆盖率、持续集成（CI）情况、许可证使用、文档完整性 |
| 代码真实性（AI Authenticity） | 15分 | 代码或README文件中是否存在AI生成的痕迹 |
| 社交活跃度（Social） | 10分 | 仓库的星星评分、分支数量、星星与分支的比例 |
| 活动情况（Activity） | 10分 | 最近的推送记录和发布版本 |
| 加密安全性（Crypto Safety） | 5分 | 代币发行情况、潜在的安全风险（如“rug pattern”攻击） |
| 依赖关系审计（Dependency Audit） | 10分 | 是否包含已知恶意包、是否存在拼写错误、安装脚本的安全性 |
| 分支质量（Fork Quality） | 8分 | 分支之间的差异、可疑的代码更改 |
| README文件质量（README Quality） | 10分 | 安装指南的完整性、示例代码、API文档的可用性 |
| 可维护性（Maintainability） | 10分 | 文件大小、代码结构与文档的匹配程度 |
| 项目整体健康状况（Project Health） | 10分 | 项目是否被弃用、更新频率、问题处理的及时性 |
| 原创性（Originality） | 5分 | 代码的原创性、是否存在复制粘贴的行为 |
| 安全性（Agent Safety） | 15分 | 安装脚本的安全性、潜在的凭证窃取风险 |

## 评分等级
- A（85分及以上）：非常可靠（LEGIT）
- B（70-84分）：较为可靠（SOLID）
- C（55-69分）：中等可靠性（MIXED）
- D（40-54分）：可靠性较低（SKETCHY）
- F（低于40分）：应避免使用（AVOID）

## 主要功能
- **增强的依赖关系审计**：检测已知恶意包（如`event-stream`、`ua-parser-js`等）、拼写错误攻击、安装脚本的安全性问题，并评估依赖关系的复杂性。
- **分支分析**：分析分支之间的差异，识别仅用于外观修改的分支，标记可疑的代码更改。
- **安全性检测**：检测潜在的安全风险，如凭证窃取、安装脚本的恶意行为、代码的混淆情况。
- **秘密信息检测**：通过正则表达式和熵分析方法查找硬编码的API密钥、Token等敏感信息。
- **网络域名分类**：对所有外部域名（API、CDN等）进行分类。
- **持续集成/持续部署审计**：检查GitHub Actions中的相关设置，防止安全漏洞。
- **权限管理**：汇总代码运行所需的权限信息。
- **作者信誉评估**：分析作者的组织成员资格、可疑仓库的记录以及账户的使用时长。
- **投资方验证**：对比投资方的声明与代码贡献者的组织成员资格。
- **代码复杂性分析**：标记结构复杂、条件语句密集的文件。

## 批量处理文件格式
```
# One repo per line, # for comments
Uniswap/v3-core
https://github.com/aave/aave-v3-core
OpenZeppelin/openzeppelin-contracts
```

## 输出结果
默认输出为包含条形图和详细信息的终端报告。
- 使用`--json`参数时，会输出结构化的数据，便于程序化处理。
- 使用`--oneline`参数时，输出格式为：`RepoName: 85/100 [A] — 2个关键评分指标`

## 向用户报告结果时应注意的事项
- 保持报告简洁明了，首先说明评分结果和主要发现内容，跳过无关紧要的部分。
- 例如：
  "Uniswap/v3-core的评分为75/B：96%的代码使用了GPG签名，有11位贡献者，采用MIT许可证。存在的问题包括：项目已被弃用（466天未更新），存在2,597个冗余的依赖关系，CI脚本中包含敏感信息。安全性提示：请注意潜在的安全风险。"
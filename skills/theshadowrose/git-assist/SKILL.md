---
name: "GitAssist AI-Powered Git Workflow Helper"
description: "根据 diff 文件生成提交信息，编写 Pull Request（PR）的描述，创建变更日志，并建议分支名称。所有这些流程都可以通过自动化的方式完成。"
author: "@TheShadowRose"
version: "1.0.0"
tags: ["git-assist"]
license: "MIT"
---
# GitAssist：一款由AI驱动的Git工作流程辅助工具

该工具能够根据代码差异自动生成提交信息、编写Pull Request（PR）描述、生成变更日志，并建议分支名称，实现所有Git工作流程的自动化。

---

请不要再在提交信息中简单写“修复了某个问题”这样的内容。

## 主要功能

### 提交信息生成
```bash
git-assist commit
# Output: "feat(auth): add JWT refresh token rotation with 7-day expiry"
```

### Pull Request描述生成
```bash
git-assist pr --base main --head feature/auth-refresh
# Output: Full PR description with summary, changes, testing notes
```

### 变更日志生成
```bash
git-assist changelog --since v1.2.0
# Output: Grouped by type (features, fixes, breaking changes)
```

### 分支名称建议
```bash
git-assist branch "add user authentication with OAuth"
# Output: feature/add-oauth-user-authentication
```

## 提交信息规范

| 前缀 | 用途 |
|--------|-----|
| `feat:` | 新功能 |
| `fix:` | 修复漏洞 |
| `docs:` | 文档编写 |
| `refactor:` | 代码重构 |
| `test:` | 添加测试 |
| `chore:` | 维护性工作 |

## 工作原理

1. 读取已暂存的代码差异（或用于PR的分支差异）；
2. 分析代码中发生了哪些变化（包括文件、函数以及修改的意图）；
3. 生成描述修改原因的提交信息（而不仅仅是描述修改的内容）；
4. 遵循您配置的提交信息规范。

该工具不使用任何外部API，而是利用您本地安装的AI模型来完成这些任务。

---

## ⚠️ 免责声明

本软件按“原样”提供，不附带任何明示或暗示的保证。

**使用本软件的风险由您自行承担。**

- 作者对因使用或误用本软件而导致的任何损害、损失或后果（包括但不限于经济损失、数据丢失、安全漏洞、业务中断或间接损失）概不负责；
- 本软件不构成财务、法律、交易或专业建议；
- 用户需自行评估本软件是否适用于其具体使用场景、环境及风险承受能力；
- 本软件的准确性、可靠性、完整性或适用性均不作任何保证；
- 作者不对第三方购买后如何使用、修改或分发本软件负责。

通过下载、安装或使用本软件，即表示您已阅读并同意完全自行承担相关风险。

**数据隐私声明：** 本软件会在您的系统上本地处理和存储数据。作者对因软件漏洞、系统故障或用户操作失误导致的数据丢失、损坏或未经授权的访问行为概不负责。请务必定期备份重要数据。除非用户明确配置，否则本软件不会向外部传输数据。

---

## 支持与联系方式

| | |
|---|---|
| 🐛 **问题报告** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*本软件基于[OpenClaw](https://github.com/openclaw/openclaw)开发——感谢您的支持！*

---

🛠️ **需要定制功能吗？** 我们提供定制的OpenClaw插件和技能服务，价格从500美元起。只要您能详细描述需求，我就能为您实现。→ [在Fiverr上联系我](https://www.fiverr.com/s/jjmlZ0v)
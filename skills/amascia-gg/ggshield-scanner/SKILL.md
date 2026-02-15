---
name: ggshield-scanner
description: 在敏感信息（如 API 密钥、凭据、令牌等）泄露到 Git 仓库之前，能够检测出 500 多种类型的硬编码秘密。该功能基于 GitGuardian 的 ggshield CLI 实现。
homepage: https://github.com/GitGuardian/ggshield-skill
metadata:
  clawdbot:
    requires:
      bins: ["ggshield"]
      env: ["GITGUARDIAN_API_KEY"]
---

# ggshield 秘密扫描器

## 概述

**ggshield** 是一个命令行工具（CLI），用于检测代码库中硬编码的敏感信息（即秘密）。该工具为你的 AI 代理（Moltbot）提供了秘密扫描功能。

### 什么是“秘密”？

秘密是指那些绝对不能被提交到版本控制系统的敏感凭证，例如：
- AWS 访问密钥、GCP 服务账户、Azure 凭据
- API 令牌（如 GitHub、Slack、Stripe 等）
- 数据库密码和连接字符串
- 私有加密密钥和证书
- OAuth 令牌和刷新令牌
- PayPal/Stripe API 密钥
- 电子邮件服务器凭证

### 为什么这很重要？

泄露一个秘密可能会导致以下后果：
- 🔓 使你的基础设施受到威胁
- 💸 产生巨额的云服务费用（攻击者会滥用你的 AWS 账户）
- 📊 暴露客户数据（违反 GDPR/CCPA 等法规）
- 🚨 触发安全事件和审计

**ggshield** 会在这些秘密被提交到仓库之前就将其检测出来。

## 功能

### 可用的命令

#### 1. `scan-repo`
    扫描整个 Git 仓库中的秘密（包括历史记录）。

**输出**：
（具体输出内容会根据实际执行情况生成）

**检测到秘密时的输出**：
（具体输出内容会根据实际执行情况生成）

#### 2. `scan-file`
    扫描单个文件中的秘密。

#### 3. `scan-staged`
    仅扫描已暂存的 Git 变更（适用于提交前的检查）。

**说明**：此命令仅针对已添加到 `git add` 的更改进行扫描，因此速度较快。

#### 4. `install-hooks`
    将 `ggshield` 安装为 Git 的提交前钩子（pre-commit hook）。

**说明**：安装后，每次提交都会自动触发扫描。

#### 5. `scan-docker`
    扫描 Docker 镜像中的秘密。

## 安装

### 先决条件

1. **ggshield CLI**：通过 pip 安装
   （安装命令会根据实际情况提供）

2. **GitGuardian API 密钥**：用于秘密检测
   - 注册：https://dashboard.gitguardian.com（免费）
   - 在设置中生成 API 密钥
   - 设置环境变量：
     （具体设置命令会根据实际情况提供）

3. **Python 3.8+**：`ggshield` 需要 Python 3.8 或更高版本。

### 安装技能

（安装命令会根据实际情况提供）

现在该技能已添加到你的 Moltbot 工作空间中。

### 在你的 Moltbot 工作空间中

启动一个新的 Moltbot 会话以使用该技能：

（具体操作步骤会根据实际情况提供）

## 使用模式

### 模式 1：推送前进行安全检查

### 模式 2：审计现有仓库

### 模式 3：提交前强制检查

### 模式 4：Docker 镜像安全检查

## 配置

### 环境变量

以下环境变量是该技能正常运行所必需的：
| 变量 | 值 | 设置位置 |
| :-- | :-- | :-- |
| `GITGUARDIAN_API_KEY` | 从 https://dashboard.gitguardian.com 获取的 API 密钥 | `~/.bashrc` 或 `~/.zshrc` |
| `GITGUARDIAN_ENDPOINT` | `https://api.gitguardian.com`（默认值，可选） | 通常不需要 |

### 可选的 `ggshield` 配置

创建 `~/.gitguardian/.gitguardian.yml` 文件以保存持久化配置：

（配置文件内容会根据实际情况提供）

更多详情请参阅：https://docs.gitguardian.com/ggshield-docs/

## 隐私与安全

### 传输到 GitGuardian 的数据

✅ **仅传输元数据**：
- 秘密模式的哈希值（而非实际秘密内容）
- 文件路径（仅相对路径）
- 行号

❌ **绝不传输**：
- 你的实际秘密或凭证
- 文件内容
- 私有密钥
- 其他敏感信息

**备注**：GitGuardian 企业版客户可以在本地进行扫描，无需将数据传输到云端。

### 如何检测秘密

**ggshield** 使用以下方法进行检测：
1. **基于熵的检测**：识别高熵字符串（随机生成的令牌）
2. **模式匹配**：查找已知的秘密格式（如 AWS 密钥前缀）
3. **公开的安全漏洞（CVE）**：参考已公开的秘密信息
4. **机器学习**：利用泄露的秘密数据进行训练

## 故障排除

### “ggshield: command not found”
**原因**：`ggshield` 未安装或未添加到系统的 PATH 环境变量中。

**解决方法**：
（具体解决方法会根据实际情况提供）

### “GITGUARDIAN_API_KEY not found”
**原因**：环境变量未设置。

**解决方法**：
（具体解决方法会根据实际情况提供）

### “401 Unauthorized”
**原因**：API 密钥无效或已过期。

**解决方法**：
（具体解决方法会根据实际情况提供）

### “在大型仓库中扫描速度慢”
**原因**：扫描 50GB 的大型仓库需要较长时间。`ggshield` 正在处理大量数据。

**解决方法**：
（提供加速扫描的技巧或建议）

## 高级主题

### 忽略误报

有时 `ggshield` 会误判某些字符串为秘密（例如测试密钥）：

**解决方法**：创建 `.gitguardian/config.json` 文件来设置忽略规则。

### 与 CI/CD 集成

你可以将秘密扫描功能集成到 GitHub Actions 或 GitLab CI 中：

（集成步骤会根据实际情况提供）

### 企业版：本地扫描

如果你的公司使用 GitGuardian 企业版，可以在本地进行扫描，无需将数据传输到云端：

（具体配置步骤会根据实际情况提供）

## 相关资源

- **ggshield 文档**：https://docs.gitguardian.com/ggshield-docs/
- **GitGuardian 控制台**：https://dashboard.gitguardian.com（查看所有检测到的秘密）
- **Moltbot 技能**：https://docs.molt.bot/tools/clawdhub
- **秘密管理最佳实践**：https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html

## 支持

- **问题报告**：https://github.com/GitGuardian/ggshield-skill/issues
- **咨询**：在 ClawdHub 上提交问题或留言
- **ggshield 相关问题**：https://github.com/GitGuardian/ggshield/issues

## 许可证

MIT 许可证 - 详见 LICENSE 文件

## 贡献者

- GitGuardian 团队
- 欢迎你的贡献！

---

**版本**：1.0.0
**最后更新**：2026 年 1 月
**维护者**：GitGuardian
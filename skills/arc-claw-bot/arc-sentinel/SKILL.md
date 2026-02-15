---
name: arc-sentinel
description: OpenClaw代理的安全监控和基础设施健康检查功能包括：漏洞监控（HaveIBeenPwned）、SSL证书过期检测、GitHub安全审计、凭据轮换跟踪、秘密信息扫描、Git代码库安全检查、令牌管理（Token Watchdog）以及权限审计。这些功能可用于执行安全扫描、检查凭据轮换状态、审计代码库中是否存在泄露的秘密信息，以及监控SSL证书的状态和基础设施的运行状况。
---

# Arc Sentinel

这是一个专为 OpenClaw 代理设计的安全监控工具包，能够自动检查您的基础设施并报告存在的问题。

## 配置

在使用前，请在 `skill` 目录下创建 `sentinel.conf` 文件：

```bash
cp sentinel.conf.example sentinel.conf
```

使用以下配置信息编辑 `sentinel.conf` 文件：
- **DOMAINS** — 用于检查 SSL 证书的域名列表（用空格分隔）
- **GITHUB_USER** — 用于仓库审计的 GitHub 用户名
- **KNOWN_REPOS** — 预期存在的仓库名称列表（非预期的仓库会触发警告）
- **MONITOR_EMAIL** — 用于接收 “HaveIBeenPwned” 数据泄露检查通知的电子邮件地址
- **HIBP_API_KEY** — 可选；HIBP v3 API 密钥（每月费用 $3.50，用于自动查询数据泄露信息）

同时，请根据您的需求自定义 `credential-tracker.json` 文件中的凭据和轮换策略。系统中提供了一个模板可供参考。

## 快速入门

### 全面扫描
```bash
cd <skill-dir>
bash sentinel.sh
```

### 输出结果
- 以彩色编码显示严重程度的格式化报告
- JSON 格式的报告保存在 `reports/YYYY-MM-DD.json` 文件中
- 出口代码说明：
  - `0` = 一切正常
  - `1` = 有警告
  - `2` = 有严重问题

## 检查项目

### 1. SSL 证书过期
检查配置域名的 SSL 证书是否过期。在证书过期前 30 天发出警告，在证书过期前 14 天发出严重警告。

### 2. GitHub 安全性检查
- 列出所有仓库并检查 Dependabot 的漏洞警报状态
- 审查最近的账户活动以发现异常行为
- 标记非预期的仓库

### 3. 数据泄露监控（HaveIBeenPwned）
- 通过 HIBP API 查询是否存在数据泄露的账户（需要 API 密钥）
- 如果未设置 API 密钥，则会回退到手动检查方式

### 4. 凭据轮换监控
读取 `credential-tracker.json` 文件，标记过期、即将过期或从未轮换的凭据。支持的轮换策略包括：`季度`（90 天）、`半年`（180 天）、`年度`（365 天）和 `自动`。

## 其他脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/secret-scanner.sh` | 扫描仓库/文件中是否存在泄露的秘密信息和 API 密钥 |
| `scripts/git-hygiene.sh` | 审查 Git 历史记录中的安全问题 |
| `scripts/token-watchdog.sh` | 监控令牌的有效性和过期情况 |
| `scripts/permission-auditor.sh` | 审查文件和访问权限 |
| `scripts/skill-auditor.sh` | 审查已安装的技能模块的安全性 |
| `scripts/full-audit.sh` | 依次运行所有脚本 |

## 代理使用方法

在心跳通信期间或根据需要运行以下命令：
1. 从 `skill` 目录中执行 `bash sentinel.sh`
2. 查看输出中是否有警告或严重问题的记录
3. 如有需要处理的问题，请及时通知相关人员
4. 在凭据轮换后更新 `credential-tracker.json` 文件

## Cron 任务设置
```bash
# Weekly Monday 9am
0 9 * * 1 cd /path/to/arc-sentinel && bash sentinel.sh >> reports/cron.log 2>&1
```

## 所需软件
- `openssl`（用于 SSL 检查）
- `gh` CLI（用于 GitHub 相关操作）
- `curl`（用于与 HIBP 交互）
- `python3`（用于处理 JSON 数据）
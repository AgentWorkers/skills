---
name: openclaw-vault-pro
description: "完整的凭据生命周期安全解决方案：检测泄露的凭据、自动修复权限问题、隔离受感染的文件、跟踪凭据轮换情况、扫描 Git 历史记录，并提供自动化保护功能。这些功能均包含在 openclaw-vault（免费版本）中，同时还提供了自动化的应对措施。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Vault Pro

[openclaw-vault](https://github.com/AtlasPA/openclaw-vault) 的所有功能（免费版本）加上自动化防护措施。

**免费版本用于检测威胁；Pro 版本则能够采取应对措施、隔离受感染的文件并进行防御。**

## 检测命令（免费版本也提供）

### 全面凭证审计

对所有凭证文件进行全面的审计：检查权限设置、shell 历史记录、git 配置文件、配置文件内容、日志文件、gitignore 规则的适用性以及凭证文件的过期情况。

```bash
python3 {baseDir}/scripts/vault.py audit --workspace /path/to/workspace
```

### 凭证泄露检测

识别可能导致凭证泄露的隐患：配置错误的权限设置、公开目录中的凭证文件、git 历史记录中的风险、Docker 配置中的凭证信息泄露、shell 别名中的敏感信息，以及代码中通过 URL 查询参数传递的凭证信息。

```bash
python3 {baseDir}/scripts/vault.py exposure --workspace /path/to/workspace
```

### 凭证清单管理

生成工作区中所有凭证文件的清单，按类型（API 密钥、数据库 URI、令牌、证书、SSH 密钥、密码等）进行分类，并记录凭证的创建时间，标记过时的或已泄露的凭证。

```bash
python3 {baseDir}/scripts/vault.py inventory --workspace /path/to/workspace
```

### 快速状态概览

以一行文字显示凭证总数、泄露凭证的数量以及是否存在过期的凭证。

```bash
python3 {baseDir}/scripts/vault.py status --workspace /path/to/workspace
```

## Pro 版本的防护措施

### 自动修复权限

自动修复所有凭证文件的权限设置，将 `.env` 文件及其他凭证文件设置为仅允许文件所有者读取（在 Unix 系统上使用 `chmod 600`；在 Windows 系统上使用 `icacls` 设置受限的 ACL）。

```bash
python3 {baseDir}/scripts/vault.py fix-permissions --workspace /path/to/workspace
```

### 隔离受感染的文件

将泄露的凭证文件移至 `.quarantine/vault/` 目录，并记录文件的原始位置及隔离原因。从原始位置移除这些文件以防止进一步泄露。

```bash
python3 {baseDir}/scripts/vault.py quarantine <file> --workspace /path/to/workspace
```

### 恢复被隔离的文件

将之前被隔离的凭证文件恢复到其原始位置，恢复方式基于文件的原始路径或隔离文件的名称。

```bash
python3 {baseDir}/scripts/vault.py unquarantine <file> --workspace /path/to/workspace
```

### 凭证轮换检查

检查凭证文件的创建时间，并生成轮换计划。超过最长保留期限的文件会被标记为“过期”，接近期限的文件会被标记为“即将过期”。默认的保留期限为 90 天。

```bash
python3 {baseDir}/scripts/vault.py rotate-check --workspace /path/to/workspace
python3 {baseDir}/scripts/vault.py rotate-check --max-age 60 --workspace /path/to/workspace
```

### Git 监控

扫描 git 历史记录，查找意外提交的凭证信息。使用 `git log --diff-filter=A` 命令来查找被添加（可能后来又被删除）的凭证文件，确认这些凭证是否仍然存在于当前工作目录（HEAD）中，或者仅存在于历史记录中，并提供相应的修复建议。

```bash
python3 {baseDir}/scripts/vault.py gitguard --workspace /path/to/workspace
```

### 自动化保护

通过一条命令执行全面的自动化保护操作：审计所有凭证文件、检查泄露风险、修复权限问题、隔离高风险文件、检查轮换计划，并生成详细的报告。建议在会话启动时执行此操作。

```bash
python3 {baseDir}/scripts/vault.py protect --workspace /path/to/workspace
python3 {baseDir}/scripts/vault.py protect --max-age 60 --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动时的自动检测（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/vault.py protect",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

### 定期凭证保护机制（OpenClaw）

将相关配置添加到 `HEARTBEAT.md` 文件中，以实现定期凭证保护功能：

```
- Run credential protection sweep (python3 {skill:openclaw-vault-pro}/scripts/vault.py protect)
```

## 工作区自动检测

如果省略了 `--workspace` 参数，脚本会尝试以下路径来查找工作区配置：
1. `OPENCLAW_WORKSPACE` 环境变量
2. 当前目录（如果存在 `AGENTS.md` 文件）
3. `~/.openclaw/workspace`（默认路径）

## 检测范围

| 检测类别 | 具体内容 |
|----------|---------|
| **权限设置** | 具有全局可读或组可读权限的 `.env` 文件 |
| **Shell 历史记录** | `.bash_history`、`.zsh_history`、`.python_history` 等文件中的凭证信息 |
| **Git 配置** | git 远程 URL 中嵌入的凭证信息，以及明文形式的凭证配置 |
| **配置文件** | JSON、YAML、TOML、INI 格式的配置文件中的硬编码秘密信息 |
| **日志文件** | 日志文件中意外记录的凭证信息 |
| **gitignore 规则** | `.env`、`.pem`、`.key`、`credentials.json` 等文件是否被正确排除在日志记录之外 |
| **凭证过期情况** | 超过保留期限的凭证文件 |
| **公开目录** | `public/`、`static/`、`www/`、`build/` 目录中的凭证文件 |
| **Git 历史记录** | 可能被提交到 git 仓库中的凭证文件 |
| **Docker** | `Dockerfile` 和 `docker-compose` 配置文件中的硬编码秘密信息 |
| **Shell 配置文件** | `.bashrc`、`.zshrc`、`.profile` 文件中的凭证别名 |
| **URL 查询参数** | 代码中通过 URL 查询参数传递的 API 密钥/令牌 |

## 错误代码

- `0`：检查完成，无问题
- `1`：检测到警告，需要进一步审查
- `2`：检测到严重泄露，需要立即采取行动

## 无需外部依赖

仅依赖 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求，所有操作都在本地完成。

## 跨平台兼容性

支持与 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具配合使用。
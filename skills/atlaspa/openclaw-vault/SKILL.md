---
name: openclaw-vault
user-invocable: true
metadata: {"openclaw":{"emoji":"🔐","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Vault

OpenClaw Vault 保护您的凭证生命周期——它不仅能在源代码中查找敏感信息（这是 Sentry 的功能），还能追踪凭证通过服务、权限、历史记录、配置文件、容器和时间等方式被泄露的情况。

## 为什么这很重要

凭证的泄露途径远不止源代码。它们还可能通过以下途径泄露：
- **权限**：系统中的所有用户都能读取的 `.env` 文件
- **Shell 历史记录**：`.bash_history` 文件中显示的密码和令牌
- **Git 配置**：嵌入在远程 Git URL 中的凭证
- **配置文件**：JSON/YAML/TOML/INI 配置文件中的硬编码秘密
- **日志文件**：调试过程中意外记录的令牌
- **Docker 配置**：嵌入到容器镜像中的秘密
- **凭证过期**：数月未更新的凭证

OpenClaw Vault 监控整个凭证生命周期。Sentry 主要用于在文件中查找敏感信息，而 OpenClaw Vault 则专注于检测那些已被实际泄露的凭证。

## 命令

### 全面凭证审计

- 权限检查
- Shell 历史记录分析
- Git 配置扫描
- 配置文件扫描
- 日志文件扫描
- 确保 `.env` 文件未被 Git 忽略（`gitignore` 规则检查）
- 识别过期的凭证

```bash
python3 {baseDir}/scripts/vault.py audit --workspace /path/to/workspace
```

### 泄露检测

- 检测凭证泄露的途径：配置错误的权限、公共目录中的敏感文件、Git 历史记录中的风险、Docker 镜像中嵌入的凭证、Shell 别名泄露，以及代码中的 URL 查询参数中的敏感信息

```bash
python3 {baseDir}/scripts/vault.py exposure --workspace /path/to/workspace
```

### 凭证清单

- 生成工作区中所有凭证文件的清单，按类型（API 密钥、数据库 URI、令牌、证书、SSH 密钥、密码）分类
- 记录凭证的创建时间，并标记过期的或已泄露的凭证

```bash
python3 {baseDir}/scripts/vault.py inventory --workspace /path/to/workspace
```

### 快速状态概览

- 以一行显示凭证总数、泄露数量以及过期的凭证数量

```bash
python3 {baseDir}/scripts/vault.py status --workspace /path/to/workspace
```

## 工作区自动检测

如果省略了 `--workspace` 参数，脚本会尝试以下路径来查找工作区：
1. `OPENCLAWWORKSPACE` 环境变量
2. 当前目录（如果存在 `AGENTS.md` 文件）
3. `~/.openclaw/workspace`（默认路径）

## 检查内容

| 类别 | 详细信息 |
|----------|---------|
| **权限** | 具有全局可读或组可读权限的 `.env` 文件 |
| **Shell 历史记录**：`.bash_history`、`.zsh_history`、`.python_history` 等文件中的凭证 |
| **Git 配置**：嵌入在 Git 远程 URL 中的凭证 |
| **配置文件**：JSON、YAML、TOML、INI 配置文件中的硬编码秘密 |
| **日志文件**：`.log` 文件中意外记录的凭证 |
| **Git 忽略规则**：检查 `.env`、`.pem`、`.key`、`credentials.json` 等文件的路径是否被正确忽略 |
| **凭证过期**：超过 90 天未更新的凭证 |
| **公共目录**：`public/`、`static/`、`www/`、`build/` 目录中的凭证文件 |
| **Git 历史记录**：可能被提交到 Git 仓库的凭证文件 |
| **Docker**：`Dockerfile` 和 `docker-compose` 配置文件中的硬编码秘密 |
| **Shell 配置**：`.bashrc`、`.zshrc`、`.profile` 文件中的别名中的凭证 |
| **URL 参数**：代码中 URL 查询字符串中传递的 API 密钥/令牌 |

## 输出代码

- `0`：无问题，一切正常
- `1`：检测到警告，需要查看详情
- `2`：检测到严重泄露，需要采取行动

## 无需外部依赖

仅使用 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求，所有操作都在本地完成。

## 跨平台兼容性

支持 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。
---
name: keys-manager
description: 您可以使用 `keys` CLI 从终端本地管理 API 密钥。当用户需要存储、检索、搜索、导入、导出或组织 API 密钥及敏感信息时，可以使用该工具。它支持 `.env` 文件的操作、基于用户配置文件的密钥隔离功能，以及安全的密钥管理流程。
metadata:
  openclaw:
    requires:
      bins:
        - keys
    primaryEnv: ""
---
# 密钥管理器

这是一个用于使用 `keys` CLI 工具在本地管理 API 密钥和敏感信息的技能。

## 安装

首先需要安装 `keys` CLI 工具：

```bash
brew install stym06/tap/keys
```

或者使用 Go 语言进行安装：

```bash
go install github.com/stym06/keys@latest
```

## 命令

### 存储密钥

```bash
keys add <name> <value>
```

如果密钥已经存在，系统会提示用户是否要覆盖、编辑或取消操作。

### 获取密钥

```bash
keys get <name>       # print value directly
keys get              # interactive typeahead picker
```

### 交互式浏览密钥

```bash
keys see
```

会打开一个图形用户界面（TUI），支持模糊搜索、复选框、复制到剪贴板以及显示密钥的创建时间。

- `space` — 切换选中项
- `tab` — 将选中的密钥以 `KEY=VAL` 的格式复制到剪贴板
- `ctrl+y` — 将选中的密钥以 `export KEY=VAL` 的格式复制到文件
- `ctrl+e` — 将选中的密钥导出到 `.env` 文件
- `enter` — 如果没有找到匹配项，则添加新密钥
- `esc` — 退出

### 遮盖显示密钥内容

```bash
keys peek
```

与 `see` 命令相同，但会隐藏密钥的值（显示为 `***`）。按 `r` 可以显示具体的密钥内容。适用于屏幕共享场景。

### 编辑密钥

```bash
keys edit <name>
```

会打开一个图形用户界面编辑器。使用 `tab` 切换字段，按 `enter` 保存修改，按 `esc` 取消操作。

### 删除密钥

```bash
keys rm <name>
```

### 导出密钥

```bash
keys env              # interactive selector, writes .env file
keys expose           # print export statements to stdout
```

### 从 `.env` 文件导入密钥

```bash
keys import <file>
```

会解析 `.env` 文件，处理其中的注释、引号以及 `export` 前缀，并显示新增或更新的密钥数量。

### 分配密钥到不同项目或环境

```bash
keys profile use <name>     # switch profile
keys profile list           # list all profiles (* = active)
```

所有 `add`、`get`、`rm`、`see` 等命令都在当前激活的环境（profile）中执行。

### 将密钥插入命令中

```bash
$(keys inject API_KEY DB_HOST) ./my-script.sh          # inline env vars
docker run $(keys inject -d API_KEY DB_HOST) my-image  # Docker -e flags
$(keys inject --all) ./my-script.sh                    # all keys from active profile
$(keys inject --all --profile dev) ./my-script.sh      # all keys from specific profile
```

会将密钥以 `KEY=VAL` 的格式（或使用 `--docker` 选项以 `-e KEY=VAL` 的格式）输出，以便在命令中替换相应的值。

### 审计密钥访问记录

```bash
keys audit              # summary: access count + last used per key
keys audit --log        # full access log (most recent first)
keys audit --log -n 20  # last 20 events
keys audit --clear      # clear the audit log
```

会记录通过 `get`、`inject` 和 `expose` 命令访问密钥的日志，有助于了解哪些代理或脚本正在使用这些密钥。

### 检查所需密钥

```bash
keys check              # reads .keys.required from current directory
keys check reqs.txt     # custom file
```

会从文件中读取密钥名称（每行一个密钥，支持 `#` 注释），并报告哪些密钥存在或缺失。如果缺少任何密钥，程序会以非零代码退出——这对于持续集成（CI）和代理启动前的检查非常有用。

示例文件：`.keys.required`：
```
# Agent dependencies
OPENAI_KEY
SERP_API_KEY
DATABASE_URL
```

### 在多台机器之间同步密钥

```bash
# On machine A (has the keys)
keys sync serve
# Serving 12 keys from profile "default"
# Passphrase: olive-quilt-haven
# Waiting for connections...

# On machine B (wants the keys)
keys sync pull                       # auto-discover via mDNS
keys sync pull 192.168.1.10:7331     # or connect directly
```

通过本地网络实现点对点同步。系统会自动通过 mDNS（Bonjour）发现其他可用的机器，并使用一次性密码（AES-256-GCM）进行加密。支持 WiFi、Tailscale 或任何可访问的网络。同步时会智能处理：添加新密钥、更新旧密钥、忽略较新的本地密钥。

### 删除所有密钥

```bash
keys nuke
```

需要输入 `nuke` 来确认删除操作。仅影响当前激活的环境。

### 查看密钥版本

```bash
keys version
keys --version
```

## 认证

在 macOS 上，使用 `keys` 命令时系统会提示用户使用 Touch ID 进行身份验证。认证信息会在每个终端会话中缓存——首次使用该命令时会触发 Touch ID 验证，同一 shell 中的后续命令将不再提示。

某些命令可以跳过身份验证：`profile`、`completion`、`version`、`help`。

在非 macOS 系统或无法使用生物识别技术的情况下，系统会允许直接访问密钥而无需提示。

## 示例

### 典型工作流程

```bash
keys add OPENAI_KEY sk-proj-abc123
keys add STRIPE_KEY sk_test_4eC3
keys get OPENAI_KEY
keys see                    # browse and copy
keys env                    # generate .env for a project
```

### 多项目设置

```bash
keys profile use projectA
keys import .env
keys profile use projectB
keys add DB_HOST prod-db.example.com
keys profile list
```

### 快速将密钥导出到 shell

```bash
eval $(keys expose)
```

## 使用指南

- 当用户知道密钥的精确名称时，使用 `keys get <name>` 命令。
- 当用户需要交互式搜索或选择密钥时，使用 `keys get`（不带参数）。
- 在屏幕共享或需要隐藏密钥内容时，使用 `keys peek` 而不是 `keys see`。
- 使用 `keys profile` 将密钥分配到不同的项目或环境中。
- 使用 `keys import` 从现有的 `.env` 文件批量导入密钥。
- 当用户需要为特定项目生成 `.env` 文件时，建议使用 `keys env` 命令。
- 当用户希望直接将密钥传递给命令或 Docker 容器而不生成文件时，使用 `keys inject`。
- 使用 `keys audit` 查看哪些密钥被访问以及访问频率。
- 在运行代理之前使用 `keys check` 确保所有必需的密钥都可用。
- 使用 `keys sync serve` 和 `keys sync pull` 在无需云服务的情况下在机器之间传输密钥。
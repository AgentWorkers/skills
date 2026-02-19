---
name: redshift
description: 使用 Redshift CLI（https://redshiftapp.com）管理应用程序密钥——这是一种基于 Nostr 构建的去中心化、加密的密钥管理工具。该工具可用于设置、获取、删除、列出密钥、上传或下载密钥，将密钥注入命令中，配置项目/环境，或使用 Nostr 密钥进行身份验证。涵盖与 Redshift 相关的密钥管理操作，包括 Redshift 运行、Redshift 设置、Redshift 登录及相关命令。
homepage: https://redshiftapp.com
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires":
          {
            "bins": ["redshift"],
            "envOptional": ["REDSHIFT_NSEC", "REDSHIFT_BUNKER", "REDSHIFT_CONFIG_DIR"],
          },
        "installHint": "Install from https://redshiftapp.com or build from source: https://github.com/accolver/redshift",
      },
  }
---
# Redshift

通过 `redshift` CLI 实现去中心化的密钥管理。密钥在客户端进行加密（采用 NIP-59 加密方案），并存储在 Nostr 中继服务器上——无需中央服务器。

项目官网：https://redshiftapp.com

## 关键概念

- **项目** (`-p`)：项目名称（例如 `backend`、`myapp`）
- **环境** (`-c`)：环境名称（例如 `dev`、`staging`、`production`）
- `redshift.yaml`：由 `redshift setup` 生成的目录级项目配置文件
- 如果省略 `-p`/`-c`，Redshift 会读取当前目录下的 `redshift.yaml` 文件

## 安全注意事项

- 在共享或日志记录的环境中，切勿直接在命令行中传递密钥值——建议通过交互式方式设置密钥，或从标准输入（stdin）传递密钥
- 对于持续集成/持续部署（CI/CD）流程，使用 `REDSHIFT_NSEC` 或 `REDSHIFT_BUNKER` 环境变量，而非 CLI 参数
- 除非需要将 Web UI 暴露到网络中，否则避免使用 `redshift serve --host 0.0.0.0`——默认地址 `127.0.0.1` 仅限本地访问
- 所有加密操作都在客户端完成；密钥在传输过程中始终保持加密状态
- 私钥存储在系统密钥链中，而非明文配置文件中

## 认证

```bash
redshift login                    # Interactive (recommended)
redshift login --nsec nsec1...    # Direct private key (use env var in CI instead)
redshift login --bunker "bunker://pubkey?relay=wss://relay.example&secret=xxx"  # NIP-46 (ALWAYS quote the URL)
redshift login --connect          # Generate NostrConnect URI for bunker app
redshift me                       # Check current identity
redshift logout                   # Clear credentials
```

在持续集成/持续部署（CI/CD）过程中，应设置 `REDSHIFT_NSEC` 或 `REDSHIFT_BUNKER` 环境变量，而非使用 `redshift login` 命令进行登录。这些变量应存储在 CI 平台的密钥管理系统中（例如 GitHub Actions 的密钥管理功能），切勿硬编码。

## 项目设置

```bash
redshift setup                                  # Interactive
redshift setup -p myapp -c production           # Non-interactive
redshift setup --no-interactive -p app -c dev   # Strict non-interactive
```

使用 `redshift setup` 命令创建包含项目信息、环境设置及中继服务器列表的 `redshift.yaml` 文件。

## 密钥管理

```bash
# List all
redshift secrets                          # Redacted values
redshift secrets --raw                    # Show plaintext values
redshift secrets --json                   # JSON output
redshift secrets --only-names             # Names only

# Get
redshift secrets get API_KEY
redshift secrets get API_KEY --plain      # Raw value, no formatting
redshift secrets get API_KEY --copy       # Copy to clipboard
redshift secrets get KEY1 KEY2            # Multiple keys

# Set
redshift secrets set API_KEY sk_live_xxx
redshift secrets set API_KEY '123' DB_URL 'postgres://...'    # Multiple at once

# Delete
redshift secrets delete OLD_KEY
redshift secrets delete KEY1 KEY2 -y      # Skip confirmation

# Download
redshift secrets download ./secrets.json                     # JSON (default)
redshift secrets download --format=env --no-file             # Print .env to stdout
redshift secrets download --format=env ./secrets.env         # Save as .env file
# Formats: json, env, yaml, docker, env-no-quotes

# Upload
redshift secrets upload secrets.env
```

在使用 `redshift` 命令管理密钥时，可以通过 `-p` 或 `-c` 参数指定具体的项目或环境设置：

```bash
redshift secrets -p backend -c production --raw
redshift secrets set -p myapp -c staging FEATURE_FLAG true
```

## 注入密钥后执行命令

**重要提示：** 仅执行用户明确请求的命令。切勿自行构造任意命令并传递给 `redshift run`。在执行命令前务必与用户确认。

```bash
redshift run -- npm start
redshift run -- python app.py
redshift run --command "npm start && npm test"
redshift run -p myapp -c prod -- docker-compose up

# Mount secrets to a file instead of env vars
redshift run --mount secrets.json -- cat secrets.json
redshift run --mount secrets.env --mount-format env -- cat secrets.env

# Fallback for offline mode
redshift run --fallback ./fallback.json -- npm start
redshift run --fallback-only -- npm start          # Read only from fallback

# Preserve existing env values for specific keys
redshift run --preserve-env PORT,HOST -- npm start
```

## 配置设置

```bash
redshift configure                    # Show config
redshift configure --all              # Show all saved options
redshift configure get project        # Get specific option
redshift configure set project=myapp  # Set option
redshift configure unset project      # Remove option
redshift configure reset --yes        # Reset to initial state
```

## Web UI

```bash
redshift serve                        # http://127.0.0.1:3000 (localhost only)
redshift serve --port 8080 --open     # Custom port, auto-open browser
redshift serve --host 0.0.0.0         # ⚠️ Exposes to network — use with caution
```

## 全局参数

| 参数                | 缩写    | 描述                                      |
|------------------|-------|-----------------------------------|
| `--help`         | `-h`      | 显示帮助信息                        |
| `--version`      | `-v`      | 显示版本信息                        |
| `--json`         |         | 以 JSON 格式输出结果                   |
| `--silent`       |         | 抑制信息提示                        |
| `--debug`        |         | 以详细日志格式输出调试信息                |
| `--config-dir`   |         | 更改配置文件目录（默认：`~/.redshift`）            |

## 环境变量

| 变量                | 描述                                      |
|------------------------|--------------------------------------------------|
| `REDSHIFT_NSEC`        | 用于 CI/CD 的私钥（绕过交互式登录）            |
| `REDSHIFT_BUNKER`      | 用于 CI/CD 的 NIP-46 中继服务器地址           |
| `REDSHIFT_CONFIG_DIR`  | 更改配置文件目录（默认：`~/.redshift`）            |

## 重要说明

- 必须为中继服务器的 URL 加引号（例如：`--bunker "bunker://..."`），否则 shell 会错误解析 `&` 符号
- 包含空格或特殊字符的密钥值需要加引号
- 当通过 `redshift run` 命令传递复杂数据（对象/数组）时，系统会自动将其转换为 JSON 字符串格式
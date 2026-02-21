---
name: 1password-sa
description: >
  **将 1Password 中的敏感信息安全地注入到代理工作流程中**  
  该方法主要使用 `op run/.env.tpl` 作为服务账户配置的默认模式，当该模式不可用时，会使用 `op read` 作为备用方案。系统内置了严格的安全规则、输入验证机制，并针对身份验证/权限错误提供了相应的故障排查支持。适用于处理 API 密钥、凭证或任何由 1Password 管理的敏感信息。
homepage: https://developer.1password.com/docs/cli/get-started/
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["op"] },
        "env": ["OP_SERVICE_ACCOUNT_TOKEN"],
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "1password-cli",
              "bins": ["op"],
              "label": "Install 1Password CLI (brew)",
            },
          ],
      },
  }
---
# 1Password CLI（强化版）

通过1Password CLI（`op`）为OpenClaw代理提供安全的秘密访问功能。服务账户是推荐的使用方式。

## 参考资料

- `references/get-started.md` — 安装及基础设置
- `references/cli-examples.md` — 安全的命令使用模式
- `references/troubleshooting.md` — 故障排查与恢复流程

## 必须遵守的安全规则

1. **优先使用`op run`来处理秘密数据的注入**，避免其他替代方法。
2. **严禁在处理秘密命令时启用shell追踪功能（如`set -x`、`bash -x`）。
3. **严禁将秘密信息打印到标准输出或日志文件中**（`echo`、`cat`等命令不可使用）。如果输出内容不会被记录到日志或终端中，可以使用`printf`并将结果直接传递给其他命令（例如`printf ... | curl -H @-`）。
4. **在处理包含秘密信息的操作期间及之后，严禁输出环境变量**（`env`、`printenv`、`set`等命令不可使用）。
5. **严禁将秘密信息作为CLI参数传递**（参数可能会被显示在进程列表中）。
6. **严禁将秘密信息的输出结果写入日志或文件中**（`tee`、`>`、`>>`等命令不可使用），除非是为了生成受保护的临时文件用于`op inject`操作。
7. **严禁将`op read`的输出结果写入日志管道**。
8. **使用`op inject`时必须使用受保护的临时文件**：设置文件权限为`umask 077`、`chmod 600`，并使用`trap`命令进行清理。
9. **严禁在聊天记录、工具输出或代理响应中显示秘密信息**。如果命令输出了秘密内容，切勿直接显示或引用该内容。

### 禁用的标志/模式

- **`--no-masking`** — 绝不在代理工作流程中使用。屏蔽功能可以防止秘密信息被意外显示，必须始终启用。
- **`--reveal`** — 绝不在常规工作流程中使用。该选项会以明文形式显示字段值。
- **`op signin --raw`** — 会将原始会话令牌输出到标准输出。
- **直接使用`op read`** — 严禁直接执行该命令，必须先将结果存储到变量中。
- **`set -x`** — 在任何`op`命令周围都严禁启用该选项。
- **`curl -v`** — 详细输出认证信息，应使用`curl -sSf`代替。
- **`script`** / **终端记录器** — 会捕获所有秘密信息。

### 不可信的输入

- 在使用shell命令时，严禁未经严格转义的用户提供的文本或外部文本。
- 必须始终使用`--`来分隔`op`命令的标志和参数。
- 来自不可信来源的`Vault`/项目名称必须经过验证（只能包含字母数字、连字符、下划线和空格）。
- 绝严禁使用`eval`、反引号替换或基于字符串构建的shell命令来处理秘密信息。
- 如果项目名称包含 `$`、反引号、分号或管道符号，请立即停止操作并请用户确认。

**安全的动态输入模板：**

```bash
VAULT="my-vault"
ITEM="my-item"

# Validate: reject names with dangerous characters
for NAME in "$VAULT" "$ITEM"; do
  if ! LC_ALL=C [[ "$NAME" =~ ^[a-zA-Z0-9\ _-]+$ ]]; then
    echo "ERROR: invalid vault/item name: $NAME" >&2; exit 1
  fi
done

VALUE="$(op read "op://${VAULT}/${ITEM}/password")"
# use $VALUE, then:
unset VALUE
```

在处理变量时必须使用双引号。切勿未经验证就使用不可信的输入来构建`op://`类型的链接。拒绝包含 `/`、`$`、反引号、分号或管道符号的名称。

### `.env.tpl` 文件的安全性

- 将`.env.tpl`文件视为代码文件：验证文件的所有权，审查修改内容，并限制访问权限（`chmod 600`）。
- 不要接受来自不可信来源的`.env.tpl`文件。
- 不要将`.env.tpl`文件提交到公共仓库，因为其中可能包含`Vault`/项目的结构信息。
- 如果`.env.tpl`文件存在于仓库中，应将其添加到`.gitignore`文件中。
- 创建或修改后，务必设置文件权限为`chmod 600`。
- 仅定义预期的变量名称；拒绝包含危险环境变量（如`PATH`、`LD_PRELOAD`、`BASH_ENV`、`NODE_OPTIONS`等）的模板。

---

## 服务账户工作流程（推荐方式）

服务账户是代理的默认登录方式，无需交互式认证。

### 1) 加载并设置令牌

从平台的安全存储中加载令牌：

```bash
# macOS Keychain:
#   security find-generic-password -a <account> -s OP_SERVICE_ACCOUNT_TOKEN -w
# Linux (GNOME Keyring / libsecret):
#   secret-tool lookup service OP_SERVICE_ACCOUNT_TOKEN
# Last resort (interactive prompt, not automatable):
#   read -rs OP_SERVICE_ACCOUNT_TOKEN

OP_SERVICE_ACCOUNT_TOKEN="$(__REPLACE_WITH_SECURE_STORE_COMMAND__)"
[ -z "$OP_SERVICE_ACCOUNT_TOKEN" ] && { echo "ERROR: token retrieval failed" >&2; exit 1; }
```

**推荐做法：使用单条命令来设置令牌的权限范围**（令牌不会持久保存在shell环境变量中）：

```bash
OP_SERVICE_ACCOUNT_TOKEN="$OP_SERVICE_ACCOUNT_TOKEN" \
  op run --env-file=.env.tpl -- <command>
unset OP_SERVICE_ACCOUNT_TOKEN
```

**如果需要执行多个命令**：可以使用`trap`命令在命令执行后自动清理令牌：

```bash
export OP_SERVICE_ACCOUNT_TOKEN
trap 'unset OP_SERVICE_ACCOUNT_TOKEN' EXIT
op run --env-file=.env.tpl -- <command-1>
op run --env-file=.env.tpl -- <command-2>
unset OP_SERVICE_ACCOUNT_TOKEN
```

### 2) 使用`.env.tpl` + `op run`（推荐方式）

创建包含1Password相关引用的`.env.tpl`文件（不要使用原始的秘密信息）：

```
API_KEY=op://my-vault/my-item/api-key
DB_PASSWORD=op://my-vault/my-item/password
```

然后执行`op run`命令：

```bash
op run --env-file=.env.tpl -- <command>
```

默认情况下，秘密信息会被屏蔽；屏蔽功能属于深度防御措施，但并非主要保护手段——因为经过转换或部分处理的秘密信息仍可能被泄露。主要的防护措施是避免直接输出秘密信息。

### 3) 临时替代方案：`op read`

仅在`op run`不适用的情况下使用。此时可以使用子shell来自动清理临时文件：

```bash
(
  trap 'unset VALUE' EXIT
  VALUE="$(op read 'op://my-vault/my-item/field')"
  # use $VALUE here — auto-cleaned on exit
)
```

对于API调用，建议使用带有包装脚本的`op run`方式，以避免使用`sh -c`命令：

```bash
# api-call.sh (chmod +x)
#!/usr/bin/env bash
set -euo pipefail
printf "Authorization: Bearer %s\n" "$API_TOKEN" | curl -sSf -H @- https://api.example.com/resource
```

```bash
op run --env-file=.env.tpl -- ./api-call.sh
```

### 4) 日志记录

> **所有诊断输出都包含敏感信息（如账户邮箱、Vault名称、项目ID、URL等）**，这些信息在日志或记录中应被视为机密内容。

```bash
op whoami
op vault list --format json
```

### 服务账户的生命周期管理

- **权限范围由策略决定**：读写权限取决于配置和`Vault`的权限设置。
- **如果访问失败**：需要验证`Vault`的权限设置和项目权限。
- **如果令牌过期或被撤销**：需要在1Password管理界面重新生成令牌，更新安全存储后重新尝试访问。
- **注意限制**：根据组织政策，服务账户可能不支持创建新项目。

---

## `op inject`（限制使用）

仅在需要临时生成文件时使用`op inject`：

```bash
set -euo pipefail
set +x
umask 077

TMP_FILE="$(mktemp)"
cleanup() { rm -f "$TMP_FILE"; }
trap cleanup EXIT ERR INT TERM HUP QUIT

op inject -i config.tpl -o "$TMP_FILE"
chmod 600 "$TMP_FILE"

# use "$TMP_FILE" briefly, then auto-cleanup via trap
```

注入的秘密文件仅允许在临时使用后立即销毁，严禁长期保存。
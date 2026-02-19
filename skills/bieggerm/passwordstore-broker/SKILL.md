---
name: passwordstore-broker
description: 通过一次性使用的 HTTPS 表单收集敏感信息，将其安全地存储在 `pass` 文件中（使用 `vault.sh` 脚本），并通过 `scripts/run_with_secret.sh` 脚本以环境变量的形式传递给相关工具。这样，原始的敏感信息就不会被泄露到聊天记录或日志中。
---
# Passwordstore 代理协议

每当需要凭据时，请运行此工作流程。

## 先决条件

- 在首次使用之前，请按照 `references/SETUP.md` 的说明进行设置。

## 设置前的检查

在首次使用 LAN 模式之前，请确认以下两个文件存在：
- `~/.passwordstore-broker/totp.secret`
- `~/.passwordstore-broker/setup_completed_at.txt`

- 如果文件缺失，请运行 `scripts/setup_totp_enrollment.py`，并按照提示操作：
  - 生成 QR 图像（建议使用 `qr/png_path`）或使用备用 URL `otpauth_url` 进行注册。
  - 将生成的 `setup_completed_at` 时间戳记录下来并作为初始注册时间。
- 注册完成后，切勿以任何形式泄露或重新传输 `totp.secret` 的值。
- 严禁通过代理程序自行旋转 `totp.secret` 的值；用户需要自行手动操作。

## 第一阶段：获取秘密信息

目标：确保所需的秘密信息存储在本地密钥库中，同时避免在聊天中泄露这些信息。

1. 将认证需求映射到相应的 `secret-name` 和 `ENV_VAR`。
2. 检查每个秘密信息是否已经存在：
   - `scripts/vault.sh` 是否存在（对应于 `<secret-name>`）。
3. 如果秘密信息缺失，请通过一次性 HTTPS 请求获取：
   - 本地模式（默认）：`scripts/get_password_from_user.py --secretname <secret-name> --port <port>`
   - LAN 模式（当用户请求使用手机或私有网络连接时）：`scripts/get_password_from_user.py --secretname <secret-name> --port <port> --access lan`
4. 将生成的请求 URL 发送给用户。
5. 在 LAN 模式下，指导用户填写表单中的两个字段：
   - 秘密信息
   - 当前的认证码
6. 如果请求失败或超时，请尝试使用另一个端口重新请求。

退出条件：所需的秘密信息已成功存储在密钥库中。

## 第二阶段：使用秘密信息

目标：在执行认证后的命令时避免泄露秘密信息。

1. 建议使用专门的工具进行操作：`scripts/run_with_secret.sh --secret <secret-name> --env <ENV_VAR> -- <command> [args...]`
2. 如果没有专门的工具，可以使用以下简化命令：`<ENV_VAR>="$(scripts/vault.sh get <secret-name>)" <command> [args...]`
3. 在处理涉及秘密信息的操作过程中，严禁使用 `env`、`printenv` 或 `set` 等命令来显示环境变量。

退出条件：认证后的命令成功执行，且没有秘密信息被泄露。

## 第三阶段：与密钥库交互

目标：安全地管理秘密信息的生命周期。

- 存储/更新秘密信息：`scripts/vault.sh put <secret-name>`
- 获取秘密信息（仅在必要时）：`scripts/vault.sh get <secret-name>`
- 检查秘密信息是否存在：`scripts/vault.sh exists <secret-name>`
- 列出所有秘密信息：`scripts/vault.sh ls`
- 删除秘密信息：`scripts/vault.sh rm <secret-name>`

**命名规则：**
- 使用稳定的、具有明确含义的键名，例如 `github/token`、`openai/prod/api_key`、`aws/staging/access_key_id`。

**密钥轮换规则：**
- 默认情况下，只需替换同一键下的旧值。
- 仅在用户明确要求时才使用带版本号的密钥。

## 不可妥协的安全准则：

- 绝不允许用户将原始秘密信息粘贴到聊天中。
- 绝不允许将秘密信息反馈给用户。
- 绝不允许将秘密信息存储在仓库文件、提交信息、问题评论或聊天记录中。
- 绝不允许通过公共接口或隧道泄露秘密信息。
- LAN 模式必须依赖运行时的私有网络自动检测和 Web 表单 TOTP 验证机制。

## 快速操作指南：

1. 在首次使用 LAN 模式之前，确保已经完成了 TOTP 注册流程。
2. 对于任何缺失的秘密信息，根据用户的需求通过本地模式或 LAN 模式进行获取。
3. 使用 `run_with_secret.sh` 命令执行相关操作。
4. 根据用户请求，使用 `vault.sh` 命令来旋转或删除秘密信息。
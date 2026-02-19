---
name: passwordstore-broker
description: 通过一次性使用的 HTTPS 表单来收集敏感信息，确保这些信息的安全处理；将这些信息存储在 pass 文件中（使用脚本/vault.sh 实现）；并通过脚本/run_with_secret.sh 将这些信息注入到工具的执行环境中，从而防止原始的敏感信息被泄露到聊天记录或日志中。
metadata:
  compatibility: Requires pass, gpg, openssl, python3, and qrencode; local HTTPS network access is required, private LAN access is optional for phone flow.
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
  - 生成 QR 图像（优先选择）并发送至用户
  - 或者使用备用 URL (`otpauth_url`）
- 将 `setup_completed_at.txt` 文件记录为初始注册的时间戳，并将其视为可信的验证依据。
- 请注意：在初次注册后，切勿以任何形式泄露或重新传输 `totp.secret` 的值。
- 严禁由代理程序自动轮换 `totp.secret` 的值；用户需要自行进行轮换操作。

## 第一阶段：获取秘密信息

目标：确保所需的秘密信息存储在本地密钥库中，同时避免在聊天中泄露这些信息。

1. 将认证所需的秘密信息映射到相应的环境变量（`ENV_VAR`）。
2. 检查每个秘密信息是否已存在：
   - 确保 `scripts/vault.sh` 脚本能够找到对应的 `secret-name` 文件。
3. 如果秘密信息缺失，通过安全的 HTTPS 连接进行获取：
   - **本地模式（默认）**：`scripts/get_password_from_user.py --secretname <secret-name> --port <port>`
   - **LAN 模式（当用户请求使用手机或私有网络连接时）**：`scripts/get_password_from_user.py --secretname <secret-name> --port <port> --access lan`
4. 将获取到的秘密信息发送给用户。
5. 在 LAN 模式下，指导用户在表单中填写以下信息：
   - 秘密值
   - 当前的认证码
6. 如果获取失败或超时，请尝试使用其他端口重新尝试。

**退出条件**：
- 所需的秘密信息已成功存储在本地密钥库中。

## 第二阶段：使用秘密信息

目标：在确保用户身份验证通过的情况下执行相关命令，同时避免泄露秘密信息。

1. 建议使用专门的工具来执行命令：`scripts/run_with_secret.sh --secret <secret-name> --env <ENV_VAR> -- <command> [args...]`
2. 如果无法使用专用工具，可以使用以下简化方式：`<ENV_VAR>="$(scripts/vault.sh get <secret-name>)" <command> [args...]`
3. 在执行涉及秘密信息的操作时，严禁使用 `env`、`printenv` 或 `set` 等命令来显示环境变量的内容。

**退出条件**：
- 命令执行成功，且没有秘密信息被泄露。

## 第三阶段：安全地管理密钥库

- **添加/更新秘密信息**：`scripts/vault.sh put <secret-name>`
- **获取秘密信息**（仅在必要时）：`scripts/vault.sh get <secret-name>`
- **检查秘密信息是否存在**：`scripts/vault.sh exists <secret-name>`
- **列出所有秘密信息**：`scripts/vault.sh ls`
- **删除秘密信息**：`scripts/vault.sh rm <secret-name>`

**命名规则**：
- 使用稳定的、具有明确含义的密钥名称，例如 `github/token`、`openai/prod/api_key`、`aws/staging/access_key_id`。

**密钥轮换策略**：
- 默认情况下，使用相同的密钥名称但更新其值。
- 仅当用户明确要求时，才使用带有版本号的密钥名称。

## 不可妥协的安全准则：

- 绝不允许用户将原始的秘密信息粘贴到聊天中。
- 绝不允许将秘密信息反馈给用户。
- 绝不允许将秘密信息存储在仓库文件、提交信息、问题评论或记录中。
- 绝不允许通过公共接口或隧道泄露秘密信息。
- LAN 模式必须依赖运行时的私有网络自动检测功能以及 Web 表单生成的 TOTP 验证机制。

## 快速操作指南：

1. 在首次使用 LAN 模式之前，确保已完成 TOTP 注册流程。
2. 对于任何缺失的秘密信息，根据用户的操作意图，在本地模式或 LAN 模式下进行获取。
3. 通过 `run_with_secret.sh` 脚本执行相关操作。
4. 根据用户的需求，使用 `vault.sh` 命令来轮换或删除秘密信息。
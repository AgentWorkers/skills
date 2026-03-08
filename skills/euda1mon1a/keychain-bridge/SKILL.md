---
name: keychain-bridge
description: 通过 macOS 的 Keychain 来管理敏感信息，而不是使用明文文件。可以迁移现有的敏感信息、读写 Keychain 中的条目、为 bash 工具提供 Keychain 的访问接口、检测数据泄露情况以及诊断访问权限问题。当需要处理与敏感信息、Keychain、凭据、API 密钥或 macOS 安全加固相关的问题时，请使用此方法。
homepage: https://github.com/moltbot/keychain-bridge
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins: ["bash", "python3"]
      env: []
    files: ["scripts/*"]
  clawmart:
    price: 99
    currency: USD
    category: security
    tags: ["keychain", "macos", "secrets", "credentials", "tahoe", "migration"]
---
# Keychain Bridge

## 常用术语

- **将密钥迁移到 Keychain** / **移动密钥**
- **检查 Keychain 的状态** / **Keychain 健康状况**
- **审计密钥** / **检查是否存在泄露**
- **读取密钥** / **获取 API 密钥**
- **存储密钥** / **写入 Keychain**
- **Keychain 无法正常工作** / **`security find-generic-password` 命令卡住**

## 使用示例

```
User: "Migrate my secrets to the keychain"
Action: python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot --dry-run

User: "Check if the keychain bridge is healthy"
Action: Run keychain health check (test write/read/delete cycle)

User: "Audit for plaintext secret leaks"
Action: python3 SKILL_DIR/scripts/audit_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

通过 macOS Keychain 管理密钥，而不是使用明文文件。这样可以避免明文凭证的存储，同时通过文件桥接架构保持与基于 bash 的工具的兼容性。

## 先决条件

对于所有需要访问密钥的 Python 版本，必须安装 `keyring` Python 库：

```bash
pip3 install keyring
# If multiple Python versions exist (common on macOS):
/usr/bin/python3 -m pip install keyring
/opt/homebrew/opt/python@3.14/bin/python3.14 -m pip install --break-system-packages keyring
```

## 检查 Keychain 的状态

验证 Keychain Bridge 是否正常工作：

```bash
python3 -c "
import keyring
# Test write
keyring.set_password('keychain-bridge-test', 'test', 'hello')
# Test read
val = keyring.get_password('keychain-bridge-test', 'test')
assert val == 'hello', f'Read back {val!r}, expected hello'
# Cleanup
keyring.delete_password('keychain-bridge-test', 'test')
print('Keychain health: OK')
"
```

如果失败，请参阅下面的 **问题诊断** 部分。

## 迁移密钥

将明文密钥文件迁移到 macOS Keychain。迁移工具：
- 自动检测系统中的所有 Python 版本
- 从所有检测到的 Python 可执行文件中提取密钥（这是访问控制列表（ACL）覆盖所必需的）
- 验证密钥的读写操作是否正常
- 可选地删除原始文件

```bash
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot --dry-run
# Remove --dry-run to actually migrate
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

迁移完成后，密钥分为两类：

### 第一类 — 仅使用 Keychain
Python 脚本通过 `keychain_helper.get_secret(service)` 直接读取密钥。磁盘上没有对应的文件。

### 第二类 — 使用文件桥接
Bash 脚本无法可靠地使用 Python keyring 作为子进程（请参阅 **已知问题**）。对于这类情况，需要在启动时运行一个桥接脚本，将密钥内容写入文件中：

```bash
# Add to your LaunchAgent or startup script:
bash SKILL_DIR/scripts/populate_secrets.sh
```

该脚本会从 Keychain 读取第二类中的每个密钥，并将其写入一个权限设置为 `chmod 600` 的文件，以便 Bash 脚本能够读取。

## 读取密钥

### 从 Python 读取
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keychain_helper import get_secret

token = get_secret("my-service-name")
```

首先尝试从 Keychain 读取密钥，如果失败则转而从文件中读取。

### 从 Bash 读取（通过第二类文件）
```bash
MY_SECRET=$(cat ~/.openclaw/secrets/my-service-name)
```

确保相关服务被添加到 `populate_secrets.sh` 文件中，以便在系统启动时自动填充文件。

### 从 Bash 读取（通过 CLI 辅助工具 — 仅限交互式操作）
```bash
# Works from terminal, but HANGS from LaunchAgent bash scripts
MY_SECRET=$(python3 path/to/get_secret.py my-service-name)
```

## 写入密钥

**注意**：必须从系统中的所有 Python 版本中写入密钥。Keychain 的访问控制列表（ACL）是针对每个可执行文件单独设置的——例如，由 Python 3.9 创建的密钥项无法被 Python 3.14 读取，除非这两个版本都在同一个访问控制列表中。

```bash
# Detect Python versions
PYTHONS=()
[ -x /usr/bin/python3 ] && PYTHONS+=(/usr/bin/python3)
[ -x /opt/homebrew/opt/python@3.14/bin/python3.14 ] && PYTHONS+=(/opt/homebrew/opt/python@3.14/bin/python3.14)

# Inject from each
for py in "${PYTHONS[@]}"; do
    $py -c "import keyring; keyring.set_password('SERVICE', 'ACCOUNT', 'VALUE')"
done
```

或者使用迁移工具进行批量操作。

## 审计是否存在泄露

检查是否存在意外的明文密钥文件，并验证 Keychain 的健康状况：

```bash
python3 SKILL_DIR/scripts/audit_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

报告以下情况：
- 密钥目录中存在意外文件（可能表示有泄露）
- Keychain 中存在但无法读取的项（可能是访问控制列表问题）
- 文件存在但并未被迁移到 Keychain 中
- 每个 Python 版本的 Keychain 库安装状态

## 问题诊断

### `security find-generic-password -w` 命令卡住
**macOS Tahoe 26.x 的问题**：`security` CLI 在读取 Keychain 项时可能会无限期卡住（或返回退出码 36），即使执行了 `security unlock-keychain` 命令也是如此。这会影响所有基于 CLI 的 Keychain 操作。

**解决方法**：改用 Python 的 `keyring` 库。该库通过 ctypes 使用 Security 框架的 C API，从而完全绕过有问题的 CLI。

### Python keyring 返回 `None` 或抛出 `errSecInteractionNotAllowed`（-25308）错误
这种情况通常发生在通过 SSH 会话运行时。Keychain 需要图形用户界面（GUI）会话的上下文。

**推荐解决方法**：使用第二类文件桥接模式。首先通过 GUI 会话（如 LaunchAgent 或 VNC 终端）写入密钥，然后从权限设置为 `chmod 600` 的文件中读取。

**SSH 写入时的解决方法**：`security unlock-keychain -p` CLI 命令在 Tahoe 系统上也会出现问题（即使输入正确的密码也会返回“错误的密码”）。同样需要使用 ctypes 和 Security 框架的 C API。解锁、设置和验证操作必须在同一个 Python 进程中完成——否则解锁状态不会在多次调用之间保持。

### 使用 ctypes 解锁时的注意事项：
- 解锁操作是 **进程范围的**——如果再次调用 `python3`，解锁状态将会丢失。
- 只有 `/usr/bin/python3`（Apple 系统自带的 Python）可以在使用 ctypes 解锁后进行写入操作；Homebrew 安装的 Python 版本（3.12、3.14）仍然会遇到 -25308 错误。
- 如果需要跨多个 Python 版本访问密钥，首先使用 `/usr/bin/python3` 进行写入操作，然后通过 VNC 终端在同一个 Python 进程中从其他 Python 版本读取密钥。

### 当从 bash LaunchAgent 调用 Python keyring 时出现卡顿
**macOS Tahoe 26.x 的新问题**：当 bash 脚本作为 LaunchAgent 并通过 `python3 get_secret.py` 启动子进程时，Python 进程可能会无限期卡住。这是因为在从 bash 转到 Python 子进程的过程中，SecurityAgent 会话连接丢失了。

**解决方法**：使用第二类文件桥接模式。让 Python 在系统启动时自动填充密钥文件，然后由 Bash 脚本读取这些文件。

### 不同版本的 Python 无法互相读取对方的密钥项
Keychain 的访问控制列表（ACL）是针对每个可执行文件单独设置的。例如，由 `/usr/bin/python3`（Python 3.9）创建的密钥项只有对该版本的有效访问权限，而 `/opt/homebrew/bin/python3.14` 则无法访问。

**解决方法**：使用 `migrate_secrets.py` 工具自动处理这个问题。

### 某个 Python 版本未安装 `keyring` 库
每个 Python 可执行文件都有自己的 `site-packages` 目录。`pip3 install keyring` 只会为其中一个版本安装该库。

```bash
# Check which Python pip3 targets
pip3 --version
# Install for system Python
/usr/bin/python3 -m pip install keyring
# Install for Homebrew Python
/opt/homebrew/opt/python@3.14/bin/python3.14 -m pip install --break-system-packages keyring
```

## 架构参考

```
                    ┌─────────────────────┐
                    │   macOS Keychain     │
                    │  (login keychain)    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
    ┌─────────▼─────────┐     │     ┌──────────▼──────────┐
    │   Group A          │     │     │   Group B            │
    │   (keychain only)  │     │     │   (file bridge)      │
    │                    │     │     │                      │
    │ Python scripts     │     │     │ populate_secrets.sh  │
    │ import keychain_   │     │     │ runs at boot →       │
    │ helper.get_secret()│     │     │ writes chmod 600     │
    │                    │     │     │ files for bash       │
    └────────────────────┘     │     └──────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Fallback           │
                    │   get_secret() tries │
                    │   keychain first,    │
                    │   then file read     │
                    └─────────────────────┘
```

### 何时使用第一类方法
- 使用者是 Python 脚本
- 脚本作为 LaunchAgent 运行（或直接在终端中运行）
- 脚本不是作为 bash LaunchAgent 的子进程启动的

### 何时使用第二类方法
- 使用者是 Bash 脚本
- Bash 脚本作为 LaunchAgent 运行
- 密钥信息存储在配置文件中，且配置文件中指定了 `file:secrets/` 路径

## 已知问题（macOS Tahoe 26.x）

1. **`security` CLI 全面出现问题**：`find-generic-password -w` 命令会卡住或返回退出码 36；`unlock-keychain -p` 命令即使输入正确的密码也会返回“错误的密码”；`show-keychain-info` 命令也会返回错误。整个 `security` CLI 在 Tahoe 系统上不可靠——请使用 Python 的 `keyring`（第一类方法）或 ctypes Security 框架进行所有 Keychain 操作。
2. **Keychain 的访问控制列表是针对每个可执行文件单独设置的**：必须从所有需要读取密钥的 Python 版本中分别进行写入操作。
3. **Bash 子进程会丢失 SecurityAgent 的上下文**：当 `bash LaunchAgent` 调用 `python3` 子进程时可能会出现卡顿。此时应使用第二类文件桥接模式。
4. **SSH 会话缺乏 GUI 上下文**：使用 `-25308` 错误会导致 Keychain 读写操作失败。在这种情况下，需要在同一个 Python 进程中使用 ctypes 的 `SecKeychainUnlock` 函数，或者使用第二类文件桥接模式。
5. **每个 Python 版本都需要单独安装 `keyring`**：每个 Python 可执行文件的 `site-packages` 目录是独立的。
6. **Homebrew 安装的 Python 版本不支持 ctypes 解锁**：使用 `SecKeychainUnlock` 后，`/usr/bin/python3`（Apple 系统自带的 Python 3.9）可以通过 `keyring` 读写密钥，但 Homebrew 安装的 Python 版本（3.12、3.14）仍然会遇到 -25308 错误。具体原因不明，可能与权限或代码签名有关。解决方法是在同一个 Python 进程中首先使用 `/usr/bin/python3` 进行写入操作，然后再从 Homebrew 安装的 Python 版本中读取密钥。

## 外部接口

本功能不涉及任何网络请求。所有操作都在 macOS 的 Keychain 和文件系统中完成。

## 安全性与隐私

- 所有操作都在本地的 macOS 登录 Keychain 上执行
- 不会发送任何遥测数据、进行分析或进行使用跟踪
- 任何情况下都不会有数据离开机器
- 脚本不会请求网络权限
- 密钥仅从本地 Keychain 或权限设置为 `chmod 600` 的文件中读取或写入
- 迁移工具不会记录或显示密钥内容

## 信任声明

所有代码都是公开可查看的——没有混淆处理、压缩或编译后的二进制文件。本功能仅针对本地的 macOS Keychain 和文件系统进行操作。已在配备 OpenClaw 的生产型 Mac Mini M4 Pro 上进行了构建和测试，该设备全天候运行 24/7，使用了 12 个以上的 API 密钥和 25 个自动化脚本。
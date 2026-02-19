---
name: keychain-bridge
description: 通过 macOS 的 Keychain 来管理敏感信息，而不是使用明文文件。可以迁移现有的敏感信息，读写 Keychain 中的条目，为 bash 工具提供与文件之间的接口，审计潜在的安全漏洞，并诊断访问权限问题。当涉及到 macOS 上的敏感信息、Keychain、凭据、API 密钥或安全加固措施时，请使用此方法。
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

通过 macOS 的 Keychain 来管理敏感信息，而非使用明文文件。这种方式消除了明文凭证的存储风险，同时通过文件桥接（file-bridge）架构保持了与基于 bash 的工具的兼容性。

## 前提条件

对于所有需要访问敏感信息的 Python 版本，都必须安装 `keyring` Python 库：

```bash
pip3 install keyring
# If multiple Python versions exist (common on macOS):
/usr/bin/python3 -m pip install keyring
/opt/homebrew/opt/python@3.14/bin/python3.14 -m pip install --break-system-packages keyring
```

## 检查 Keychain 的运行状态

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

如果检测到问题，请参阅下面的 **故障诊断** 部分。

## 迁移敏感信息

将明文的敏感信息文件迁移到 macOS Keychain 中。迁移工具会：
- 自动检测系统中的所有 Python 版本
- 从所有检测到的 Python 可执行文件中提取敏感信息（这是实现 ACL（访问控制列表）覆盖所必需的）
- 验证数据的读写过程是否正常
- （可选）删除原始文件

```bash
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot --dry-run
# Remove --dry-run to actually migrate
python3 SKILL_DIR/scripts/migrate_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

迁移完成后，敏感信息会被分为两类：

### 第一类（仅使用 Keychain）  
Python 脚本通过 `keychain_helper.get_secret(service)` 直接从 Keychain 中读取敏感信息。系统中不会保留任何明文文件。

### 第二类（使用文件桥接）  
Bash 脚本无法可靠地通过子进程使用 Python 的 Keyring 功能（请参阅 **已知问题**）。对于这类情况，系统会在启动时通过一个桥接脚本将敏感信息从 Keychain 中读取并写入到相应的文件中：

```bash
# Add to your LaunchAgent or startup script:
bash SKILL_DIR/scripts/populate_secrets.sh
```

这个脚本会从 Keychain 中读取属于第二类的敏感信息，并将其写入到具有 `chmod 600` 权限的文件中，这样 Bash 脚本就可以通过 `cat` 命令读取这些文件。

## 读取敏感信息

### 从 Python 中读取  
```python
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keychain_helper import get_secret

token = get_secret("my-service-name")
```

首先尝试从 Keychain 中读取敏感信息，如果失败则转而从文件中读取。

### 从 Bash 中读取（通过第二类的文件）  
```bash
MY_SECRET=$(cat ~/.openclaw/secrets/my-service-name)
```

确保相关服务被添加到 `populate_secrets.sh` 文件中，以便在系统启动时自动填充这些文件。

### 通过 CLI 辅助工具从 Bash 中读取（仅限交互式使用）  
```bash
# Works from terminal, but HANGS from LaunchAgent bash scripts
MY_SECRET=$(python3 path/to/get_secret.py my-service-name)
```

## 写入敏感信息

**重要提示**：必须从系统中的所有 Python 版本中统一写入敏感信息。Keychain 的访问控制列表（ACL）是针对每个单独的可执行文件设置的——例如，由 Python 3.9 创建的文件只能被 Python 3.9 读取，除非这两个版本都在同一个 ACL 中。

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

或者可以使用迁移工具来批量处理这些操作。

## 审查是否存在泄露风险

检查系统中是否存在意外的明文敏感信息文件，并验证 Keychain 的运行状态：

```bash
python3 SKILL_DIR/scripts/audit_secrets.py --dir ~/.openclaw/secrets/ --account moltbot
```

报告内容包括：
- 敏感信息目录中的意外文件（可能表示存在泄露）
- Keychain 中存在但无法读取的条目（可能是由于 ACL 问题）
- 存在于系统中但未导入 Keychain 的文件
- 每个 Python 版本的 Keychain 库安装状态

## 故障诊断

### `security find-generic-password -w` 命令卡住  
**macOS Tahoe 26.x 版本的问题**：`security` CLI 在尝试读取 Keychain 中的条目时可能会无限期地卡住（或返回退出代码 36），即使已经执行了 `security unlock-keychain` 命令也是如此。这会影响所有基于 CLI 的 Keychain 操作。

**解决方法**：改用 Python 的 `keyring` 库。该库通过 ctypes 接口调用 Security 框架的 C API，从而绕过了有问题的 CLI 功能。

### Python 的 `keyring` 库返回 `None` 或抛出 `errSecInteractionNotAllowed`（错误代码 -25308）  
这种情况通常发生在通过 SSH 会话执行操作时。Keychain 需要一个图形用户界面（GUI）会话环境才能正常工作。

**解决方法**：要么从 LaunchAgent（具有 GUI 会话环境）中执行操作，要么先解锁 Keychain。

### 当从 Bash LaunchAgent 中调用 `keyring` 时程序卡住  
**macOS Tahoe 26.x 版本的新问题**：当 Bash 脚本作为 LaunchAgent 并通过 `python3 get_secret.py` 启动一个子进程时，Python 进程可能会无限期地卡住。这是因为在从 Bash 转到 Python 子进程的过程中，SecurityAgent 会话上下文丢失了。

**解决方法**：使用第二类的文件桥接机制，让 Python 程序在系统启动时自动填充文件，然后由 Bash 脚本从这些文件中读取数据。

### 不同版本的 Python 无法互相读取对方的敏感信息  
Keychain 的 ACL 是针对每个可执行文件单独设置的。例如，由 `/usr/bin/python3`（Python 3.9）创建的文件只有针对该版本的 ACL 权限，而 `/opt/homebrew/bin/python3.14` 由于是不同的二进制文件，可能会遇到访问权限问题。

**解决方法**：确保从所有 Python 版本中都能访问敏感信息（可以通过 `migrate_secrets.py` 工具自动处理）。

### 某个 Python 版本的 `keyring` 未安装  
每个 Python 可执行文件都有自己的 `site-packages` 目录。`pip3 install keyring` 只会为当前版本安装相应的库。

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

### 何时使用第一类（仅使用 Keychain）  
- 使用者是 Python 脚本  
- 脚本作为 LaunchAgent 运行  
- 脚本不是从 Bash LaunchAgent 中作为子进程启动的

### 何时使用第二类（使用文件桥接）  
- 使用者是 Bash 脚本  
- Bash 脚本作为 LaunchAgent 运行  
- 敏感信息的路径需要在配置文件中以 `file:secrets/` 的格式指定

## 已知问题（macOS Tahoe 26.x 版本）  
1. **`security` CLI 功能异常**：`find-generic-password -w` 命令会卡住或返回退出代码 36。请改用 Python 的 `keyring` 库。  
2. **Keychain 的 ACL 是针对每个可执行文件设置的**：必须从所有需要访问该信息的 Python 版本中分别导入敏感信息。  
3. **Bash 子进程无法正确使用 SecurityAgent**：当从 Bash LaunchAgent 转到 Python 子进程时，程序可能会卡住。在这种情况下，应使用第二类的文件桥接机制。  
4. **SSH 会话缺乏 GUI 环境**：在这种情况下，使用 `security` CLI 读取 Keychain 时可能会遇到错误（返回代码 -25308）。请确保从 LaunchAgent 中执行操作或先解锁 Keychain。  
5. **每个 Python 版本都需要单独安装 `keyring`**：每个 Python 可执行文件的 `site-packages` 目录是独立的。

这些问题仅适用于 macOS Tahoe 26.x 版本。较早的版本（如 Sonoma 14 和 Sequoia 15）可能不会出现这些问题，但在所有版本中，第一类/第二类的架构都是安全的。

## 外部接口  

本功能不涉及任何网络请求，所有操作都在 macOS 的 Keychain 和文件系统中完成。

## 安全性与隐私保护  
- 所有操作都在本地的 macOS 登录 Keychain 中执行  
- 不会发送任何遥测数据、进行分析或记录使用情况  
- 绝不会将数据传出机器  
- 脚本不会请求任何网络权限  
- 敏感信息仅从本地 Keychain 或具有 `chmod 600` 权限的文件中读取或写入  
- 迁移工具不会记录或显示敏感信息的实际内容

## 信任声明  

所有代码都是公开可查看的——没有混淆处理、压缩或编译后的二进制文件。本功能仅针对本地的 macOS Keychain 和文件系统进行操作。已在配备 OpenClaw 的生产环境（Mac Mini M4 Pro，24/7 运行，配置有 12 个以上的 API 密钥和 25 个自动化脚本）中进行了测试和验证。
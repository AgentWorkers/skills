---
name: codex-account-switcher
version: 1.2.4
homepage: https://github.com/odrobnik/codex-account-switcher-skill
description: **管理多个 OpenAI Codex 账户**：能够实时捕获当前的登录令牌，并在多个账户之间快速切换。⚠️ 该功能会读取和写入 `~/.codex/auth.json` 以及 `~/.codex/accounts/*.json` 文件（这些文件包含敏感的认证令牌）。
metadata:
  openclaw:
    emoji: "🎭"
    requires:
      bins: ["python3"]
---
# Codex 账户切换器

通过更换认证令牌文件来管理多个 OpenAI Codex 账户（例如个人账户与工作账户）。

## 使用方法

### 1. 列出账户
显示已保存的账户（当前激活的账户会在右侧标记为 `ACTIVE`）。默认输出格式较为简洁。

- `--verbose`：显示账户的刷新时间和令牌的有效期（用于调试）
- `--json`：以 JSON 格式输出详细信息

```bash
./codex-accounts.py list
```

### 2. 添加账户
使用交互式向导来收集登录信息：

- 系统会强制重新打开浏览器进行登录（执行 `codex logout && codex login`），以便您明确选择要收集的账户信息。
- 每次登录后，系统会保存账户的当前状态。
- 在交互式终端中，系统会询问是否要添加新账户。
- 如果以非交互方式调用该工具（例如通过 Moltbot），则只会执行一次登录操作，不会再次提示添加新账户。
- 为账户命名时，按 `Enter` 键即可接受系统推荐的默认名称（通常为检测到的电子邮件地址中的本地部分，例如 `oliver`）。

```bash
./codex-accounts.py add
```

### 3. 切换账户
立即切换当前激活的登录账户。

```bash
./codex-accounts.py use work
```

### 4. 自动切换到配额最多的账户
系统会检查所有账户，并切换到每周可用配额最多的账户。

```bash
./codex-accounts.py auto
./codex-accounts.py auto --json
```

## 设置
有关先决条件及设置说明，请参阅 [SETUP.md](SETUP.md)。
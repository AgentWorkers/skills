---
name: codex-account-switcher
version: 1.2.3
homepage: https://github.com/odrobnik/codex-account-switcher-skill
description: >
  Manage multiple OpenAI Codex accounts. Capture current login tokens and switch
  between them instantly. ⚠️ Reads and writes ~/.codex/auth.json and
  ~/.codex/accounts/*.json (sensitive authentication tokens).
metadata:
  openclaw:
    emoji: "🎭"
    requires:
      bins: ["python3"]
---

# Codex 账户切换器

通过更换认证令牌文件，您可以管理多个 OpenAI Codex 账户（例如个人账户与工作账户）。

## 使用方法

### 1. 列出账户
显示已保存的账户（当前激活的账户会在右侧标记为 `ACTIVE`）。默认输出格式较为简洁。

- `--verbose`：显示账户的刷新时间以及令牌的有效期（用于调试）
- `--json`：以 JSON 格式输出详细信息

```bash
./codex-accounts.py list
```

### 2. 添加账户
提供一个交互式向导来收集登录信息。

- **每次操作都会强制重新打开浏览器进行登录**（执行 `codex logout && codex login`），以便您明确选择要收集信息的账户。
- 每次登录后，系统会保存账户的当前状态。
- 在交互式终端中，系统会询问是否要添加新的账户。
- 如果以非交互方式调用该工具（例如通过 Moltbot），则只会执行一次操作（不会显示“添加新账户”的提示）。
- 为账户命名时，按 **Enter** 键即可接受默认名称（通常为检测到的电子邮件地址中的本地部分，例如 `oliver@…` 中的 `oliver`）。

```bash
./codex-accounts.py add
```

### 3. 切换账户
立即切换当前激活的登录账户。

```bash
./codex-accounts.py use work
```

### 4. 自动切换到配额最高的账户
系统会检查所有账户，并切换到每周可用配额最高的账户。

```bash
./codex-accounts.py auto
./codex-accounts.py auto --json
```

## 设置
有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。
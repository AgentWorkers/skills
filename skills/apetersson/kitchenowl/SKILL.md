---
name: kitchenowl-cli
description: 在终端中，使用 `pipx install` 命令安装 `kitchenowl-cli`，并使用其中的 `auth` 和 `core` 命令来实现 KitchenOwl 的读写功能。
metadata: {"author":"KitchenOwl","homepage":"https://github.com/kitchenowl/kitchenowl-cli","openclaw":{"requires":{"anyBins":["kitchenowl"]},"install":["pipx install kitchenowl-cli"]}}
---
# KitchenOwl CLI 技能

当用户希望通过 `kitchenowl` CLI 安装和操作 KitchenOwl 时，请使用此技能。

## 安装与验证

建议使用 `pipx` 来进行独立的 CLI 安装。

```bash
pipx install kitchenowl-cli
kitchenowl --help
kitchenowl --version
```

升级：

```bash
pipx upgrade kitchenowl-cli
```

## 认证

`auth login` 支持 `--username` 和 `--password` 参数（或交互式提示输入），当省略 `--server` 时，系统会自动询问服务器地址，默认使用上次保存的服务器地址。CLI 将 `server_url`、`access_token`、`refresh_token`、`user` 以及所有保存的配置信息存储在 `~/.config/kitchenowl/config.json`（或 `$XDG_CONFIG_HOME/kitchenowl/config.json`）文件中。`auth logout` 会从该文件中删除这些认证信息，但保留已配置的服务器地址。

## 命令使用规则

1. 在修改数据之前，先执行只读命令。
2. 对于具有破坏性作用的命令（如 `delete`、`remove-item`、批量编辑等），请先获取用户确认。
3. 对于所有需要指定范围的命令，请使用明确的 ID 或 `--household-id` 参数。
4. 当输出结果需要被程序化处理时，请使用 `--json` 参数。

## 核心命令组

请参考 `references/commands.md` 文件，以获取以下功能的完整命令集：
- 认证（auth）
- 配置/服务器设置（config/server settings）
- 家庭成员管理（households and members）
- 购物清单（shopping lists）
- 食谱管理（recipes）
- 用户管理（users）
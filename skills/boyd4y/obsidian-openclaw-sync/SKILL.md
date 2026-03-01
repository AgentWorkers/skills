---
name: obsidian-openclaw-sync
description: 在多个 iCloud 设备之间同步 Obsidian OpenClaw 的配置。通过管理符号链接来实现无缝的多设备同步。
compatibility: darwin
metadata:
  version: 1.0.0
---
# Obsidian OpenClaw Sync

这是一个辅助工具，用于在 iCloud Drive 和本地 Obsidian 仓库之间同步 OpenClaw 配置。

## 功能

该工具解决了以下问题：**通过 iCloud 在多台设备之间同步 OpenClaw 配置**：
- 自动检测所有包含 OpenClaw 配置的 iCloud 仓库；
- 从本地目录创建符号链接到 iCloud 目录，以实现无缝同步；
- 支持多代理工作区模板（如 `workspace_*`、`workspace-*`）；
- 允许用户选择是否覆盖本地的 `openclaw.json` 文件。

## 所需依赖项

| 依赖项 | 是否必需 | 说明 |
|------------|----------|-------------|
| `python3` | 是 | 需要 Python 3.x（macOS 自带 Python） |
| `macOS` | 是 | 该工具仅适用于 macOS（依赖 iCloud Drive 功能） |
| `obsidian-icloud-sync` | 是 | 需要安装 `obsidian-icloud-sync` 插件以启用 iCloud 同步功能 |

### 检查依赖项

```bash
# Check Python availability
python3 --version

# Check iCloud Obsidian path exists
ls -ld ~/Library/Mobile\ Documents/iCloud~md~obsidian/Documents
```

## 使用方法

```bash
/obsidian-openclaw-sync [command] [options]
```

## 命令

| 命令 | 说明 |
|---------|-------------|
| `status` | 显示所有包含 OpenClaw 配置的 iCloud 仓库及其状态 |
| `setup` | 交互式设置，将 iCloud 仓库的配置同步到本地 |
| `unset` | 列出并删除本地的符号链接 |

## 选项

| 选项 | 简写 | 说明 |
|--------|-------|-------------|
| `--vault N` | `-v N` | 通过索引预选仓库（默认：交互式选择） |
| `--overwrite` | `-w` | 用 iCloud 中的配置文件覆盖本地的 `openclaw.json` |
| `--no-confirm` | `-y` | 跳过确认提示（自动执行操作） |

## 使用示例

```bash
# Check sync status (shows all iCloud vaults)
/obsidian-openclaw-sync

# Interactive setup (select vault, create symlinks)
/obsidian-openclaw-sync setup

# Setup with overwrite (replace local openclaw.json with iCloud symlink)
/obsidian-openclaw-sync setup --overwrite

# Setup without confirmation prompt (auto-confirm)
/obsidian-openclaw-sync setup --no-confirm

# Setup specific vault without prompts
/obsidian-openclaw-sync setup --vault 1 --no-confirm

# List and remove local symlinks
/obsidian-openclaw-sync unset
```

## 输出格式

```
✓ iCloud Obsidian: /Users/.../iCloud~md~obsidian/Documents

✓ Valid Vaults (N):
  ✓ <vault-name>
      Agents (N): <agent1>, <agent2>, ...
      Skills (N): <skill1>, <skill2>, ...
  ○ <vault-name> [openclaw.json not found (recommended)]

✗ Invalid Vaults (N):
  ✗ <vault-name> (missing: .obsidian/)

Local Config: .openclaw
  Agents (N): <agent1>, <agent2>, ...
  Skills (N): <skill1>, <skill2>, ...
```

## 被同步的目录

| 来源（iCloud） | 目标（本地） |
|-----------------|----------------|
| `assets/` | `./assets/` |
| `projects/` | `./projects/` |
| `team/` | `./team/` |
| `skills/` | `./skills/` |
| `workspace-*/` | `./workspace-*/` |
| `.openclaw/*.json` | `./.openclaw/*.json` |
| `openclaw.json` | `./openclaw.json`（使用 `--overwrite` 选项时） |

## 多设备同步流程

1. **设备 1**：运行 `setup` 命令，创建指向 iCloud 仓库的符号链接。
2. **设备 2**：运行 `setup --overwrite` 命令，用 iCloud 中的配置文件替换本地的 `openclaw.json`。
3. **所有设备**：配置会通过 iCloud Drive 自动同步。

## 参考资料

- [同步辅助脚本](scripts/sync_helper.py) - 用于检测 iCloud 仓库的核心 Python 脚本
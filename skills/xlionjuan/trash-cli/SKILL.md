---
name: trash-cli
version: 1.0.1
description: "使用 `trash-cli` 可以安全地删除文件，它会将文件移动到系统的回收站（trash）而不是永久删除它们。这样可以避免数据丢失，并且允许在需要时恢复文件。当您需要可恢复的删除操作时，请使用 `trash-cli` 而不是 `rm` 命令。"
homepage: https://github.com/andreafrancia/trash-cli
metadata: {"emoji":"🗑️","install":[{"id":"brew","kind":"brew","formula":"trash-cli"},{"id":"pip","kind":"pip","package":"trash-cli"}]}
---
# trash-cli

这是一个用于管理 freedesktop.org 提供的“回收站”功能的命令行工具。它能够记录文件的原始路径、删除日期和权限信息，并将这些文件移至回收站。该工具与 KDE、GNOME 和 XFCE 系统使用的回收站机制兼容。

## 安装

```bash
# Via Homebrew (Linux/macOS)
brew install trash-cli

# Via pip
pip install trash-cli

# Via apt (Debian/Ubuntu)
sudo apt install trash-cli

# Via pacman (Arch Linux)
sudo pacman -S trash-cli

# Via dnf (Fedora)
sudo dnf install trash-cli
```

## 命令概览

| 命令 | 功能描述 |
|---------|-------------|
| `trash-put` | 将文件或目录移至回收站 |
| `trash-list` | 列出回收站中的文件 |
| `trash-restore` | 恢复回收站中的文件 |
| `trash-empty` | 永久删除回收站中的文件 |
| `trash-rm` | 从回收站中删除特定文件 |

## trash-put

将文件或目录移至回收站。

```bash
trash-put <file>           # Trash a file
trash-put <dir>/           # Trash a directory
trash-put -f <file>        # Silently ignore nonexistent files
trash-put -v <file>        # Verbose output
```

### 参数选项

- `-f, --force`   - 忽略不存在的文件（静默处理） |
- `-v, --verbose` | 显示详细操作过程 |
- `--trash-dir TRASHDIR` | 使用指定的文件夹作为回收站路径 |

### 注意事项

- 与 `rm` 不同，`trash-put` 在删除目录时不需要使用 `-R` 选项 |
- 来自主分区的文件会被保存在 `~/.local/share/Trash/` 目录下 |
- 来自其他分区的文件会被保存在 `$partition/.Trash/$uid` 或 `$partition/.Trash-$uid` 目录下 |

## trash-list

列出回收站中的所有文件。

```bash
trash-list                          # List all trashed files
trash-list | grep <pattern>         # Search for specific files
trash-list --all-users              # List trashcans of all users
```

### 输出格式

文件格式：`deletion_date original_path`

## trash-restore

将回收站中的文件恢复到原始位置。

```bash
trash-restore                       # Interactive restore
trash-restore --overwrite          # Overwrite existing files
trash-restore --sort date          # Sort by date (default)
trash-restore --sort path          # Sort by path
```

### 交互式使用方法

- 输入要恢复的文件编号 |
- 使用 `0-2,3` 恢复多个文件 |
- 使用 `--overwrite` 选项覆盖现有文件 |

## trash-empty

永久删除回收站中的文件。

```bash
trash-empty                 # Remove ALL trashed files
trash-empty 7              # Remove files older than 7 days
trash-empty 1              # Remove files older than 1 day
```

### 使用示例

```bash
# Delete everything in trash
trash-empty

# Keep only files from the last 7 days
trash-empty 7

# Keep only today's files
trash-empty 1
```

## trash-rm

根据文件模式从回收站中删除特定文件。

### 注意：

- 使用引号来确保模式字符串不会被 shell 解释器误解析。

```bash
trash-rm '*.log'          # Correct
trash-rm *.log            # Wrong - shell will expand
```

## 安全提示

**建议使用 `trash-put` 替代 `rm`**

- 将 `trash-put` 添加到 `.bashrc` 或 `.zshrc` 配置文件中 |
- 在确实需要使用 `rm` 时，可以通过别名来间接调用 `trash-put`：

```bash
\rm file.txt
```

### 文件恢复流程

1. 查看回收站内容：`trash-list` |
2. 查找目标文件：`trash-list | grep <filename>` |
3. 恢复文件：`trash-restore` |

## 回收站存储位置

- **主分区**：`~/.local/share/Trash/` |
- **其他分区**：`$mount_point/.Trash/$uid` 或 `$mount_point/.Trash-$uid` |

## 限制事项

- 不支持 BRTFS 文件系统 |
- 无法删除只读文件系统中的文件 |

## 常见问题解答

### 如何在其他分区创建回收站目录？

```bash
sudo mkdir --parent /.Trash
sudo chmod a+rw /.Trash
sudo chmod +t /.Trash
```

### 是否应该将 `rm` 别名为 `trash-put`？

**作者不建议这样做**。虽然 `trash-put` 在功能上看起来与 `rm` 类似，但它们的行为存在差异，可能导致问题（例如 `trash-put` 不需要 `-R` 选项来删除目录）。建议使用警告性别名来替代 `rm`。

```bash
alias rm='echo "This is not the command you are looking for."; false'
```

### 自动删除 30 天以上的文件

可以通过 crontab 脚本实现：

```bash
(crontab -l ; echo "@daily $(which trash-empty) 30") | crontab -
```

该脚本每天运行一次，自动删除回收站中超过 30 天的文件。

## 相关资源

- [GitHub 项目页面](https://github.com/andreafrancia/trash-cli) |
- [FreeDesktop.org 回收站规范](https://specifications.freedesktop.org/trash-spec/trashspec-1.0.xhtml)
---
name: storage-cleanup
description: 适用于 macOS 和 Linux 的一键磁盘清理工具：可清除临时文件、缓存文件、旧内核版本、Snap 功能生成的文件、Homebrew 安装的包、Docker 相关文件以及 Xcode 生成的残留文件。当用户需要释放存储空间、清理磁盘、减少磁盘使用量或遇到“磁盘已满”的警告时，可使用该工具。该工具默认为安全模式运行（支持模拟执行），且仅依赖 bash 和 awk 这两个命令。
---
# 存储清理

通过一个命令即可回收数十GB的磁盘空间。无需配置文件，无需依赖任何第三方工具，也不会对系统造成任何损害。

## 为什么需要这个工具

系统会默默地积累各种无用的文件和缓存：IDE的缓存文件、过时的`snap`版本、失效的`pip`构建结果、被遗忘的临时文件以及过时的内核文件。手动查找这些文件不仅浪费时间，还可能误删重要的数据。

这个工具具备以下特点：
- **支持macOS和Linux系统**：能够一次性扫描12个以上的清理目标。
- **安全可靠**：默认情况下执行“干运行”（`--dry-run`）模式，会在实际清理之前显示所有将要被删除的文件。
- **完全依赖原生工具**：仅使用`bash`和`awk`命令，适用于任何标准的macOS或Linux系统。
- **跨平台兼容**：能够自动检测操作系统，并仅执行适用于当前系统的清理操作（即使缺少某些工具也不会出错）。
- **可选择性清理**：通过`--skip-kernels`、`--skip-snap`、`--skip-docker`、`--skip-brew`等选项来选择性地跳过某些清理目标。
- **提供详细报告**：会显示清理前后的磁盘使用情况以及实际释放的磁盘空间。

## 快速入门

```bash
# Preview what would be cleaned (safe, changes nothing)
bash scripts/cleanup.sh --dry-run

# Clean everything
bash scripts/cleanup.sh --yes

# Clean but keep Docker and old kernels
bash scripts/cleanup.sh --yes --skip-docker --skip-kernels
```

## 清理的内容

### 两个平台共通的清理目标
| 目标 | 通常占用的磁盘空间 | 备注 |
|--------|-------------|-------|
| **回收站** | 1–50GB | macOS位于`~/.Trash`，Linux位于`~/.local/share/Trash` |
| **失效的`tmp`文件夹** | 1–10GB | 包含超过60分钟未使用的`pip`或`npm`构建结果 |
| **`pip`缓存** | 50–500MB | 可通过`pip cache purge`清除 |
| **Go语言构建缓存** | 100MB–2GB | 可通过`go clean -cache`清除 |
| **`pnpm`/`yarn`/`node`缓存** | 50–500MB | 可安全地重新生成 |
| **JetBrains IDE缓存** | 1–10GB | 包括IntelliJ、PyCharm、WebStorm等IDE的缓存 |
| **Whisper模型缓存** | 1–5GB | 可根据需要重新下载 |
| **Chrome/Firefox浏览器缓存** | 200MB–2GB | 仅包含浏览历史记录 |
| **Playwright浏览器缓存** | 200MB–1GB | 可根据需要重新下载 |
| **Docker未使用的镜像** | 0–10GB | 仅删除未被引用的镜像及构建缓存 |

### 仅限Linux系统的清理目标
| 目标 | 通常占用的磁盘空间 | 备注 |
|--------|-------------|-------|
| **Apt包缓存** | 200MB–2GB | 可通过`apt clean`清除 |
| **系统日志** | 500MB–4GB | 可压缩至200MB |
| **被禁用的`snap`版本** | 500MB–5GB | `snapd`会保留这些旧版本 |
| **过时的内核文件** | 200MB–800MB | 仅删除不再使用的旧内核 |

### 仅限macOS系统的清理目标
| 目标 | 通常占用的磁盘空间 | 备注 |
|--------|-------------|-------|
| **Homebrew旧版本** | 500MB–5GB | 可通过`brew cleanup --prune=7`清除 |
| **Xcode的临时构建文件** | 2–30GB | 可安全清除 |
| **Xcode的构建档案** | 1–20GB | 包含旧的构建结果 |
| **iOS设备的支持文件** | 2–15GB | 包含旧的设备相关信息 |
| **CoreSimulator缓存** | 500MB–5GB | 包含模拟器的磁盘镜像 |
| **旧用户日志** | 100MB–1GB | 删除超过30天的日志文件 |

## 可用的选项
| 选项 | 功能 |
|------|--------|
| `--dry-run` | 预览清理结果，不会实际删除任何文件 |
| `--yes` / `-y` | 直接执行清理操作，无需确认 |
| `--skip-kernels` | 不删除旧内核文件（仅限Linux） |
| `--skip-snap` | 不删除被禁用的`snap`版本（仅限Linux） |
| `--skip-docker` | 不清理Docker相关的文件 |
| `--skip-brew` | 不清理Homebrew相关的文件 |

## 需要手动处理的额外内容

以下内容不在脚本的清理范围内，需要手动处理：
- **Ollama模型**：可以使用`ollama list`列出所有模型，然后使用`ollama rm <unused>`删除不需要的模型。
- **全局`npm`缓存**：可以使用`npm cache clean --force`清除。
- **Conda环境**：可以使用`conda env list`列出所有环境，然后使用`conda remove -n <env> --all`删除不需要的环境。
- **压缩日志文件**：可以使用`sudo find /var/log -name "*.gz" -delete`删除压缩后的日志文件。
- **Linux系统中的`Flatpak`软件**：可以使用`flatpak uninstall --unused`卸载不需要的软件。
- **macOS的Time Machine快照**：可以使用`tmutil listlocalsnapshots /`列出快照列表，然后使用`tmutil deletelocalsnapshots <date>`删除指定的快照。
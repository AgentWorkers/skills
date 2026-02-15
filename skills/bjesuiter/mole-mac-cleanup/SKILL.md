---
name: mole-mac-cleanup
description: 这款Mac清理与优化工具集成了CleanMyMac、AppCleaner和DaisyDisk的功能：提供深度清理、智能卸载程序、磁盘状态分析以及项目残留文件的清除功能。
author: Benjamin Jesuiter <bjesuiter@gmail.com>
metadata:
  clawdbot:
    emoji: "🧹"
    os: ["darwin"]
    requires:
      bins: ["mo"]
    install:
      - id: brew
        kind: brew
        formula: mole
        bins: ["mo"]
        label: Install Mole via Homebrew
---

# Mole – Mac 清理与优化工具

**仓库地址：** https://github.com/tw93/Mole  
**命令格式：** `mo`（注意：不是 `mole`！）  
**安装方式：** `brew install mole`  

> **提示：** 不带参数的 `mo` 命令会进入交互式图形界面（TUI）模式。虽然对自动化脚本不太适用，但你可以手动试试看！ 😉

## 功能介绍  

Mole 是一个集成了 CleanMyMac、AppCleaner、DaisyDisk 和 iStat Menus 功能的综合性工具：  
- **深度清理**：删除缓存文件、日志以及浏览器残留文件。  
- **智能卸载**：彻底移除应用程序及其隐藏的残留文件。  
- **磁盘分析**：可视化磁盘使用情况并管理大型文件。  
- **实时监控**：提供系统状态的实时反馈。  
- **项目文件清理**：清理 `node_modules`、`target`、`build` 等文件夹中的冗余文件。  

---

## 非交互式命令（适用于自动化脚本）  

### 预览/模拟运行（务必先使用）  
```bash
mo clean --dry-run              # Preview cleanup plan
mo clean --dry-run --debug      # Detailed preview with risk levels & file info
mo optimize --dry-run           # Preview optimization actions
mo optimize --dry-run --debug   # Detailed optimization preview
```  

### 执行清理操作  
```bash
mo clean                        # Run deep cleanup (caches, logs, browser data, trash)
mo clean --debug                # Cleanup with detailed logs
```  

### 系统优化  
```bash
mo optimize                     # Rebuild caches, reset services, refresh Finder/Dock
mo optimize --debug             # With detailed operation logs
```  

**`mo optimize` 的具体功能：**  
- 重建系统数据库并清除缓存。  
- 重置网络服务。  
- 更新 Finder 和 Dock 的显示内容。  
- 清理诊断日志和崩溃日志。  
- 删除交换文件并重启动态页面缓冲器（dynamic pager）。  
- 重建应用程序启动服务及 Spotlight 索引。  

### 白名单管理  
```bash
mo clean --whitelist            # Manage protected cache paths
mo optimize --whitelist         # Manage protected optimization rules
```  

### 项目文件清理  
```bash
mo purge                        # Clean old build artifacts (node_modules, target, venv, etc.)
mo purge --paths                # Configure which directories to scan
```  

配置文件路径：`~/.config/mole/purge_paths`  

### 安装程序的清理  
```bash
mo installer                    # Find/remove .dmg, .pkg, .zip installers
```  
清理范围包括：下载文件、桌面缓存、Homebrew 缓存、iCloud 数据以及邮件附件。  

### 设置与维护  
```bash
mo touchid                      # Configure Touch ID for sudo
mo completion                   # Set up shell tab completion
mo update                       # Update Mole itself
mo remove                       # Uninstall Mole from system
mo --version                    # Show installed version
mo --help                       # Show help
```  

---

## 常见使用流程：  
1. **查看需要清理的内容：**  
   ```bash
   mo clean --dry-run --debug
   ```  
2. **确认无误后执行清理操作：**  
   ```bash
   mo clean
   ```  
3. **清理完成后优化系统：**  
   ```bash
   mo optimize --dry-run
   mo optimize
   ```  
4. **清理开发项目产生的临时文件：**  
   ```bash
   mo purge
   ```  

---

## 被清理的文件类型：  
- 用户应用程序缓存  
- 浏览器缓存（Chrome、Safari、Firefox）  
- 开发工具（Xcode、Node.js、npm）生成的文件  
- 系统日志及临时文件  
- 应用程序专属缓存（如 Spotify、Dropbox、Slack 的缓存）  
- 回收站中的文件  

## 注意事项：  
- **终端使用建议：** 最适合使用 Ghostty、Alacritty、kitty 或 WezTerm 等终端客户端；iTerm2 可能存在兼容性问题。  
- **安全性：** 使用 `--dry-run` 选项进行预览运行，确保工具正常工作。  
- **调试模式：** 加入 `--debug` 选项可查看详细日志。
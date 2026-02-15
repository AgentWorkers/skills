---
name: managing-apple-notes
description: "使用 inotes CLI 从终端管理 Apple Notes。当需要在 macOS 上的 Notes.app 中列出、阅读、创建、编辑、删除或搜索笔记时，可以使用该工具。"
homepage: https://github.com/wangwalk/inotes
url: https://github.com/wangwalk/inotes
emoji: 📝
metadata:
  clawdbot:
    os: ["darwin"]
    requires:
      bins: ["inotes"]
    install:
      - "brew install wangwalk/tap/inotes"
    cliHelp: |
      inotes --version
      inotes status
---

# 使用 `inotes` 管理 Apple Notes

`inotes` 是一个用于操作 Apple Notes 的 macOS 命令行工具（CLI）。它通过 AppleScript 与 Notes.app 通信，支持所有创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作以及搜索（Search）功能。默认输出格式为人类可读的表格；若需要机器可读的输出格式，可使用 `--json` 参数。

## 🔒 隐私与安全

- ✅ **开源项目**：完整源代码位于 [https://github.com/wangwalk/inotes](https://github.com/wangwalk/inotes)  
- ✅ **仅限本地使用**：所有操作都在本地通过 AppleScript 执行，数据不会离开用户的设备  
- ✅ **无网络请求**：`inotes` 不会连接到任何远程服务器  
- ✅ **安装过程可审计**：通过 Homebrew 从已签名的二进制文件或 GitHub 发布版本进行安装  
- ✅ **MIT 许可证**：免费且开源，允许查看源代码和贡献代码  
- ⚠️ **需要 macOS 的自动化权限**（用户需在 **系统设置 > 隐私与安全 > 自动化** 中启用该权限）  
- 📦 **通用二进制文件**：支持 Apple Silicon (arm64) 和 Intel (x86_64) 架构  

## 先决条件

**系统要求：**  
- macOS 14 或更高版本（Sonoma 或后续版本）  
- 已安装 Apple Notes.app（随 macOS 自带）  

**推荐通过 Homebrew 安装：**  
```bash
brew install wangwalk/tap/inotes
```  

**验证安装：**  
```bash
inotes --version  # Should show: 0.1.2
which inotes      # Should be in /opt/homebrew/bin/ or /usr/local/bin/
```  

**通过 GitHub 发布版本手动安装：**  
从 [GitHub 发布页面](https://github.com/wangwalk/inotes/releases) 下载软件，并验证其 SHA256 哈希值：  
```bash
curl -LO https://github.com/wangwalk/inotes/releases/download/v0.1.2/inotes-0.1.2-universal-apple-darwin.tar.gz
# Verify checksum from release notes
tar xzf inotes-0.1.2-universal-apple-darwin.tar.gz
sudo cp inotes /usr/local/bin/
sudo chmod +x /usr/local/bin/inotes
```  

**检查权限：**  
```bash
inotes status
```  
如果权限被拒绝，用户需要在 **系统设置 > 隐私与安全 > 自动化 > Notes** 中为终端应用程序启用自动化权限。  

## 命令列表  

### 列出笔记  
```bash
inotes                            # recent iCloud notes (default)
inotes today                      # modified today
inotes show week                  # modified this week
inotes show all                   # all notes
inotes show --folder Work         # notes in a specific folder
inotes show recent --limit 10    # limit results
```  

### 列出文件夹  
```bash
inotes folders
```  

### 列出账户  
```bash
inotes accounts
```  

### 创建文件夹  
```bash
inotes mkfolder "Projects"
inotes mkfolder "Work Notes" --account Exchange
```  

### 读取笔记  
```bash
inotes read 1        # by index from last show output
inotes read A3F2     # by ID prefix (4+ characters)
```  

### 创建笔记  
```bash
inotes add --title "Meeting Notes" --body "Action items" --folder Work
```  

### 编辑笔记  
```bash
inotes edit 1 --title "Updated Title"
inotes edit 2 --body "New content" --folder Projects
```  

### 删除笔记  
```bash
inotes delete 1              # with confirmation
inotes delete 1 --force      # skip confirmation
```  

### 搜索笔记  
```bash
inotes search "quarterly review"
inotes search "TODO" --folder Work --limit 10
```  

## 多账户支持  

默认情况下，仅显示 iCloud 上的笔记。可以使用 `--account <account_name>` 或 `--all-accounts` 参数来访问其他账户的笔记。  
```bash
inotes accounts                    # list available accounts
inotes show all --account Exchange
inotes show all --all-accounts
```  

## 输出格式  

| 参数 | 描述 |  
|------|-------------|  
| *(默认)* | 人类可读的表格 |  
| `--json` / `-j` | JSON 格式 |  
| `--plain` | 以制表符分隔的文本 |  
| `--quiet` / `-q` | 仅显示笔记数量 |  

## 使用指南  

- 当需要程序化处理输出时，务必使用 `--json` 参数。  
- 在非交互式环境中，使用 `--no-input` 选项关闭交互式提示。  
- 在捕获输出时，使用 `--no-color` 选项可避免 ANSI 转义序列的干扰。  
- 可通过 **索引**（上次执行 `show` 命令后的索引值）或 **ID 前缀**（笔记 ID 的前 4 个十六进制字符）来标识笔记。  
- 在执行其他命令之前，先运行 `inotes status` 命令以确认是否获得了自动化权限。  
- 该 CLI 会自动过滤掉所有支持语言中 “Recently Deleted” 文件夹中的笔记。  

## 常见任务示例  

- **创建每日笔记：**  
```bash
inotes add --title "Daily Notes $(date +%Y-%m-%d)" --body "## TODO\n\n## Done\n"
```  

- **将所有笔记导出为 JSON 格式：**  
```bash
inotes show all --json > notes-backup.json
```  

- **查找带有特定标签的笔记：**  
```bash
inotes search "#important" --json | jq '.[] | select(.folder == "Work")'
```  

- **归档已完成的笔记：**  
```bash
inotes search "DONE" --folder Inbox --json | jq -r '.[].id' | while read id; do
  inotes edit "$id" --folder Archive
done
```  

## 故障排除  

- **“自动化权限被拒绝”**：  
  - 进入 **系统设置 > 隐私与安全 > 自动化**  
  - 找到对应的终端应用程序（如 Terminal.app 或 iTerm.app），并启用对 Notes.app 的访问权限。  

- **“命令未找到”**：  
  - 运行 `which inotes` 检查该命令是否在系统的 PATH 环境变量中。  
  - 如果使用 Homebrew 安装，请运行 `brew doctor` 检查是否有安装问题，并尝试重新安装 `wangwalk/tap/inotes`。  

- **使用索引时找不到笔记**：  
  - 重新运行 `inotes show` 命令以获取最新的笔记索引。  
  - 可使用笔记 ID 的前缀来指定笔记（例如：`inotes read A3F2`）。  

- **处理大量笔记时的性能问题：**  
  - 使用 `--limit` 参数限制返回的结果数量。  
  - 通过 `--folder "Work"` 等选项按文件夹过滤笔记。  
 - 使用 `today`、`week`、`recent` 等日期过滤器进行筛选。  

## 其他资源：  
- **GitHub 仓库**：[https://github.com/wangwalk/inotes](https://github.com/wangwalk/inotes)  
- **发布版本**：[https://github.com/wangwalk/inotes/releases]  
- **问题报告**：[https://github.com/wangwalk/inotes/issues]  
- **许可证**：MIT 许可证
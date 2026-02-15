---
name: overleaf
description: 通过命令行同步和管理 Overleaf LaTeX 项目：可以将项目下载到本地，将更改推回服务器，编译 PDF 文件，并下载用于 arXiv 提交的编译输出文件（如.bbl 文件）。适用于处理 LaTeX、Overleaf、学术论文或 arXiv 的场景。
license: MIT
metadata:
  author: aloth
  version: "1.1"
  cli: olcli
  install: brew tap aloth/tap && brew install olcli
---

# Overleaf Skill

通过 `olcli` 命令行工具（CLI）管理 Overleaf LaTeX 项目。

## 安装

```bash
# Homebrew (recommended)
brew tap aloth/tap && brew install olcli

# npm
npm install -g @aloth/olcli
```

## 认证

从 Overleaf 获取会话 cookie：

1. 登录 [overleaf.com](https://www.overleaf.com)
2. 打开开发者工具（F12）→ 应用程序 → Cookies
3. 复制 `overleaf_session2` 的值

```bash
olcli auth --cookie "YOUR_SESSION_COOKIE"
```

验证认证信息：
```bash
olcli whoami
```

调试认证问题：
```bash
olcli check
```

清除存储的凭据：
```bash
olcli logout
```

## 常见工作流程

### 将项目拉取到本地

```bash
olcli pull "My Paper"
cd My_Paper/
```

### 编辑并同步更改

```bash
# After editing files locally
olcli push              # Upload changes only
olcli sync              # Bidirectional sync (pull + push)
```

### 编译并下载 PDF

```bash
olcli pdf                      # Compile and download
olcli pdf -o paper.pdf         # Custom output name
olcli compile                  # Just compile (no download)
```

### 下载用于 arXiv 提交的 `.bbl` 文件

```bash
olcli output bbl               # Download compiled .bbl
olcli output bbl -o main.bbl   # Custom filename
olcli output --list            # List all available outputs
```

### 上传图表或资源文件

```bash
olcli upload figure1.png "My Paper"          # Upload to project root
olcli upload diagram.pdf                      # Auto-detect project from .olcli.json
```

### 下载特定文件

```bash
olcli download main.tex "My Paper"           # Download single file
olcli zip "My Paper"                          # Download entire project as zip
```

## arXiv 提交工作流程

完整的 arXiv 提交准备工作流程：

```bash
# 1. Pull your project
olcli pull "Research Paper"
cd Research_Paper

# 2. Compile to ensure everything builds
olcli compile

# 3. Download the .bbl file (arXiv requires .bbl, not .bib)
olcli output bbl -o main.bbl

# 4. Download any other needed outputs
olcli output aux -o main.aux    # If needed

# 5. Package for submission
zip arxiv.zip *.tex main.bbl figures/*.pdf

# 6. Verify the package compiles locally (optional)
# Then upload arxiv.zip to arxiv.org
```

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `olcli auth --cookie <value>` | 使用会话 cookie 进行认证 |
| `olcli whoami` | 检查认证状态 |
| `olcli logout` | 清除存储的凭据 |
| `olcli check` | 显示配置路径和凭据来源 |
| `olcli list` | 列出所有项目 |
| `olcli info [project]` | 显示项目详细信息 |
| `olcli pull [project] [dir]` | 下载项目文件 |
| `olcli push [dir]` | 上传本地更改 |
| `olcli sync [dir]` | 双向同步 |
| `olcli upload <file> [project]` | 上传单个文件 |
| `olcli download <file> [project]` | 下载单个文件 |
| `olcli zip [project]` | 以 zip 格式下载项目 |
| `olcli compile [project]` | 触发编译 |
| `olcli pdf [project]` | 编译并下载 PDF |
| `olcli output [type]` | 下载编译输出文件 |

## 提示

- **自动检测项目**：从已同步的目录（包含 `.olcli.json` 文件）运行命令，可省略项目参数。
- **预编译**：使用 `olcli push --dry-run` 在上传前预览更改。
- **强制覆盖**：使用 `olcli pull --force` 强制覆盖本地更改。
- **项目 ID**：可以使用项目 ID（URL 中的 24 位十六进制字符串）代替项目名称。
- **调试认证**：运行 `olcli check` 查看凭据的加载来源。
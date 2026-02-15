---
name: gitload
description: >
  This skill should be used when the user asks to "download files from GitHub",
  "fetch a folder from a repo", "grab code from GitHub", "download a GitHub
  repository", "get files from a GitHub URL", "clone just a folder", or needs
  to download specific files/folders from GitHub without cloning the entire repo.
---

# gitload

使用 gitload CLI 从 GitHub URL 下载文件、文件夹或整个仓库。

## 使用场景

在以下情况下使用 gitload：
- 从仓库中下载特定文件夹（而非整个仓库）
- 从 GitHub 下载单个文件
- 下载仓库内容但不保留 git 历史记录
- 将 GitHub 内容压缩为 ZIP 文件
- 使用身份验证访问私有仓库

**不建议使用 gitload 的场景：**
- 需要完整的 git 历史记录时（请使用 `git clone`）
- 仓库已经克隆到本地
- 处理非 GitHub 仓库

## 先决条件

通过 npx 运行 gitload（无需安装）：
```bash
npx gitload-cli https://github.com/user/repo
```

或全局安装：
```bash
npm install -g gitload-cli
```

## 基本用法

### 下载整个仓库
```bash
gitload https://github.com/user/repo
```
在当前目录下创建一个名为 `repo/` 的文件夹。

### 下载特定文件夹
```bash
gitload https://github.com/user/repo/tree/main/src/components
```
仅下载该文件夹的内容，并在当前目录下创建一个名为 `components/` 的文件夹。

### 下载单个文件
```bash
gitload https://github.com/user/repo/blob/main/README.md
```

### 下载到自定义位置
```bash
gitload https://github.com/user/repo/tree/main/src -o ./my-source
```

### 将内容直接下载到当前目录
```bash
gitload https://github.com/user/repo/tree/main/templates -o .
```

### 下载为 ZIP 文件
```bash
gitload https://github.com/user/repo -z ./repo.zip
```

## 身份验证（针对私有仓库或应对速率限制）

### 推荐使用 gh CLI
```bash
gitload https://github.com/user/private-repo --gh
```
需要先使用 `gh auth login` 进行身份验证。

### 使用显式访问令牌
```bash
gitload https://github.com/user/repo --token ghp_xxxx
```

### 使用环境变量
```bash
export GITHUB_TOKEN=ghp_xxxx
gitload https://github.com/user/repo
```

**令牌优先级：`--token` > `GITHUB_TOKEN` > `--gh`

## URL 格式

gitload 支持标准的 GitHub URL 格式：
- **仓库根路径：** `https://github.com/user/repo`
- **文件夹：** `https://github.com/user/repo/tree/branch/path/to/folder`
- **文件：** `https://github.com/user/repo/blob/branch/path/to/file.ext`

## 常见用法示例

### 从模板文件夹生成项目结构
```bash
gitload https://github.com/org/templates/tree/main/react-starter -o ./my-app
cd my-app && npm install
```

### 下载示例代码
```bash
gitload https://github.com/org/examples/tree/main/authentication
```

### 下载文档以供离线阅读
```bash
gitload https://github.com/org/project/tree/main/docs -z ./docs.zip
```

### 下载配置文件
```bash
gitload https://github.com/org/configs/blob/main/.eslintrc.json -o .
```

## 选项参考

| 选项 | 描述 |
|--------|-------------|
| `-o, --output <dir>` | 输出目录（默认：以 URL 路径命名的文件夹） |
| `-z, --zip <path>` | 将文件保存为 ZIP 文件到指定路径 |
| `-t, --token <token>` | 使用 GitHub 个人访问令牌 |
| `--gh` | 使用 gh CLI 提供的令牌 |
| `--no-color` | 禁用彩色输出 |
| `-h, --help` | 显示帮助信息 |
| `-V, --version` | 显示版本信息 |

## 错误处理

如果 gitload 出现错误：
1. **404 错误：** 确认 URL 存在且可访问。
2. **速率限制错误：** 使用 `--gh` 或 `--token` 进行身份验证。
3. **权限错误：** 对于私有仓库，确保令牌具有 `repo` 权限。
4. **网络错误：** 检查网络连接。

## 注意事项：

- gitload 通过 GitHub 的 API 下载内容，而非 git 协议。
- 下载的内容不包含 git 历史记录（如需历史记录，请使用 `git clone`）。
- 大型仓库可能需要较长时间；建议下载特定文件夹。
- 如果输出目录不存在，gitload 会自动创建该目录。
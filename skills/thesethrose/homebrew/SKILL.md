---
name: homebrew
description: Homebrew 是适用于 macOS 的包管理器，用于搜索、安装、管理和解决与软件包（packages）及预编译软件包（casks）相关的问题。
metadata: {"clawdbot":{"emoji":"🍺","requires":{"bins":["brew"]}}}
---

# Homebrew 包管理器

本文档提供了完整的 Homebrew 命令参考和使用指南，涵盖了安装、管理和解决 macOS 包相关问题的方法。

## 使用场景
- 安装包或应用程序（`brew install X`）
- 搜索可用包（`brew search X`）
- 更新和升级现有包
- 查看包信息及依赖关系
- 解决安装问题
- 管理已安装的包

## 命令参考

### 包搜索与信息查询

#### `brew search TEXT|/REGEX/`
**用法：** 通过名称或正则表达式搜索包
**使用场景：** 当用户需要查找某个包时
**示例：**
```bash
brew search python
brew search /^node/
```

#### `brew info [FORMULA|CASK...]`
**用法：** 显示一个或多个包的详细信息
**使用场景：** 在安装前查看依赖关系、选项等详细信息
**示例：**
```bash
brew info python
brew info chrome google-chrome
```

### 安装与升级

#### `brew install FORMULA|CASK...`
**用法：** 安装一个或多个包或应用程序
**使用场景：** 当用户要求安装某个包时
**注意：**
- `FORMULA` 表示命令行工具（安装路径为 `/usr/local/bin`）
- `CASK` 表示图形界面应用程序（安装路径为 `/Applications`）
- 可以一次性安装多个包：`brew install git python nodejs`
**示例：**
```bash
brew install python
brew install google-chrome  # installs as cask
brew install git python nodejs
```

#### `brew update`
**用法：** 获取 Homebrew 及所有包的最新版本
**使用场景：** 当 Homebrew 显示为过期版本时，或在执行重要操作前
**注意：** 仅更新包列表，不升级包内容
**示例：**
```bash
brew update
```

#### `brew upgrade [FORMULA|CASK...]`
**用法：** 升级已安装的包
**使用场景：** 当用户希望将包升级到最新版本时
**注意：**
- 不带参数时：升级所有过时的包
- 带参数时：仅升级指定的包
**示例：**
```bash
brew upgrade              # upgrade all outdated packages
brew upgrade python       # upgrade just python
brew upgrade python git   # upgrade multiple
```

### 包管理

#### `brew uninstall FORMULA|CASK...`
**用法：** 卸载已安装的包
**使用场景：** 当用户需要删除某个包时
**注意：** 可以一次性卸载多个包
**示例：**
```bash
brew uninstall python
brew uninstall google-chrome
```

#### `brew list [FORMULA|CASK...]`
**用法：** 列出已安装的包或包内包含的文件
**使用场景：** 当用户想查看已安装的包或包的文件内容时
**示例：**
```bash
brew list                 # show all installed packages
brew list python          # show files installed by python
```

### 配置与故障排除

#### `brew config`
**用法：** 显示 Homebrew 的配置和环境信息
**使用场景：** 调试安装问题或检查系统设置
**显示内容：**
- 安装路径
- Xcode 的位置
- Git 版本
- CPU 架构
**示例：**
```bash
brew config
```

#### `brew doctor`
**用法：** 检查 Homebrew 安装过程中可能存在的问题
**使用场景：** 在遇到安装问题或错误时使用
**返回内容：** 问题提示及解决方案建议
**示例：**
```bash
brew doctor
```

#### `brew install --verbose --debug FORMULA|CASK`
**用法：** 以详细输出和调试信息安装包
**使用场景：** 当标准安装失败时，需要查看详细的错误信息
**示例：**
```bash
brew install --verbose --debug python
```

### 高级用法

#### `brew create URL [--no-fetch]`
**用法：** 从源代码创建新的包
**使用场景：** 需要自定义包的高级用户
**选项：**
- `--no-fetch`：不立即下载源代码
**示例：**
```bash
brew create https://example.com/package.tar.gz
```

#### `brew edit [FORMULA|CASK...]`
**用法：** 编辑包的定义
**使用场景：** 需要自定义包安装规则的高级用户
**示例：**
```bash
brew edit python
```

#### `brew commands`
**用法：** 显示所有可用的 Homebrew 命令
**使用场景：** 了解 Homebrew 的其他功能
**示例：**
```bash
brew commands
```

#### `brew help [COMMAND]`
**用法：** 查看特定命令的用法说明
**使用场景：** 需要详细了解某个命令的用法时
**示例：**
```bash
brew help install
brew help upgrade
```

## 快速参考

| 任务 | 命令 |
|------|---------|
| 搜索包 | `brew search TEXT` |
| 查看包信息 | `brew info FORMULA` |
| 安装包 | `brew install FORMULA` |
| 安装应用程序 | `brew install CASK` |
| 更新包列表 | `brew update` |
| 升级所有包 | `brew upgrade` |
| 升级特定包 | `brew upgrade FORMULA` |
| 卸载包 | `brew uninstall FORMULA` |
| 列出已安装包 | `brew list` |
| 检查配置 | `brew config` |
| 故障排除 | `brew doctor` |

## 常见工作流程

### 安装新包
1. 搜索：`brew search python`
2. 查看信息：`brew info python@3.11`
3. 安装：`brew install python@3.11`

### 解决安装问题
1. 检查配置：`brew config`
2. 运行 `brew doctor`：
3. 以调试模式重新安装：`brew install --verbose --debug FORMULA`

### 维护 Homebrew
1. 更新：`brew update`
2. 检查过时的包：`brew upgrade`（显示需要升级的包）
3. 全部升级：`brew upgrade`

## 关键概念

- **FORMULA**：命令行工具和库（例如 `python`、`git`、`node`）
- **CASK**：图形界面应用程序（例如 `google-chrome`、`vscode`、`slack`）
- **TAP**：第三方包仓库（例如 `brew tap homebrew/cask-versions`）

## 注意事项
- 所有 Homebrew 命令都需要先安装 Homebrew。
- 从源代码构建包时需要 Xcode 命令行工具。
- 有些包可能需要输入 sudo 密码。
- 不同包的安装时间可能不同。
- 包名不区分大小写，但通常以小写显示。

## 资源
- 官方文档：https://docs.brew.sh
- Formula 文档：https://github.com/Homebrew/homebrew-core
- Cask 文档：https://github.com/Homebrew/homebrew-cask
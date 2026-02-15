---
name: near-tools
description: NEAR Protocol CLI installation and setup guide. Use when: (1) User asks how to install NEAR CLI, (2) User needs help setting up near-cli-rs, (3) User wants to verify NEAR CLI installation, (4) User needs to install near-cli-rs, (5) user wants to use near cli to perform any action on the blockchain. AGENTS MUST ALWAYS get the absolute path of the 'near' binary before execution.
---

# NEAR 工具 - NEAR 命令行界面（CLI）的安装与配置

> **重要提示（针对代理用户）：** 在执行任何 `near` 命令之前，**必须**找到 `near` 可执行文件的绝对路径（可以使用 `which near` 或 `whereis near` 命令），并在命令中使用该绝对路径。这可以确保在不同 shell 环境下命令的一致性。

本文档提供了关于如何在任意平台上安装和配置 NEAR 协议命令行界面（near-cli-rs）的详细指南。

## 安装方法

选择最适合您系统的安装方法：

### 方法 1：Shell 脚本（Linux、macOS、WSL）

**适合人群：** 大多数 Linux 和 macOS 用户

```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

**如果 `near` 不在 PATH 环境变量中：**
   使用 `whereis near` 命令查找 `near` 可执行文件的路径。

**将 `near` 添加到 PATH 环境变量中：**
```bash
# Temporary (current session only)
export PATH="$HOME/.cargo/bin:$PATH"

# Permanent (add to your shell config)
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc  # For bash
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc   # For zsh
```

**重新加载 shell 或运行以下命令：**
```bash
source ~/.bashrc   # or ~/.zshrc
```

### 方法 2：npm/npx（支持 Node.js 的所有平台）

**适合人群：** JavaScript/TypeScript 开发者、Windows 用户

**直接运行命令（无需安装）：**
```bash
npx near-cli-rs
```

**全局安装：**
```bash
npm install -g near-cli-rs
```

**或将 `near-cli-rs` 添加到 `package.json` 文件中：**
```bash
npm install --save-dev near-cli-rs
```

**之后即可使用：**
```bash
npx near-cli-rs
```

### 方法 3：Windows 安装程序**

**适合人群：** 没有 Node.js 或 Cargo 的 Windows 用户

1. 访问：https://github.com/near/near-cli-rs/releases/latest
2. 下载 Windows MSI 安装程序（例如：`near-cli-rs-installer-x64.msi`）
3. 双击安装程序并按照向导操作
4. 安装程序会自动将 NEAR CLI 添加到您的 PATH 环境变量中

### 方法 4：Cargo（Rust）

**适合人群：** Rust 开发者、需要自定义构建的用户

**前提条件：** 首先从 https://rustup.rs/ 安装 Rust。

**安装方法：**
```bash
cargo install near-cli-rs
```

**或通过 git 获取最新版本：**
```bash
cargo install --git https://github.com/near/near-cli-rs
```

**Linux 用户可能需要：**
```bash
# Debian/Ubuntu
sudo apt install libudev-dev

# Fedora/Red Hat
sudo dnf install libudev-devel
```

## 验证安装结果

安装完成后，请验证 NEAR CLI 是否能够正常工作：

```bash
near --version
```

**预期输出：**
```
near-cli-rs 0.23.6  # or newer version
```

**如果命令无法执行：**

1. 确保安装目录已添加到 PATH 环境变量中：
   ```bash
   echo $PATH | grep cargo  # Check if cargo/bin is in PATH
   ```

2. 如果未添加，请手动将其添加到 PATH：
   ```bash
   export PATH="$HOME/.cargo/bin:$PATH"
   ```

3. 重新尝试运行命令：
   ```bash
   near --version
   ```

## 配置设置

### 查看配置文件的位置

```bash
near --help
# Output will show where config is stored, typically:
# "near CLI configuration is stored in ~/.config/near-cli/config.toml"
```

### 查看可用命令

```bash
near --help
```

主要命令组包括：
- **account**：管理账户（查看、创建、导入、导出）
- **tokens**：管理代币资产（NEAR、FT、NFT）
- **staking**：管理质押操作（查看、添加、提取）
- **contract**：管理智能合约（部署、调用函数）
- **transaction**：操作交易
- **config**：管理 `config.toml` 文件中的配置信息

## 初始步骤

### 查看账户信息

如果您已经拥有 NEAR 账户：

```bash
near account view-account-summary <your-account.near> network-config mainnet now
```

**示例：**
```bash
near account view-account-summary near network-config mainnet now
```

### 导入现有账户

如果您有种子短语或私钥：

```bash
near account import-account
```

按照提示进行登录操作。

### 创建新账户

如果您还没有账户：

```bash
near account create-account
```

按照提示创建新账户（创建新账户需要现有账户进行资金充值）。

## 常见问题与解决方法

### “near: command not found”（命令未找到）

**原因：** NEAR CLI 未添加到 PATH 环境变量中

**解决方法：**
```bash
# For shell script installation
export PATH="$HOME/.cargo/bin:$PATH"

# For npm global installation
export PATH="$(npm config get prefix)/bin:$PATH"

# Make it permanent by adding to ~/.bashrc or ~/.zshrc
```

### 运行安装程序时出现 “Permission denied”（权限被拒绝）错误

**原因：** 没有足够的执行权限

**解决方法：**
```bash
chmod +x near-cli-rs-installer.sh
./near-cli-rs-installer.sh
```

### 运行 `near-cli-rs-installer.sh` 时出现 “No such file” 错误

**原因：** 下载失败或文件名发生变化

**解决方法：**
```bash
# Check the releases page manually
curl -s https://api.github.com/repos/near/near-cli-rs/releases/latest | grep "browser_download_url" | grep "installer.sh"
```

### 安装过程卡顿或速度缓慢

**原因：** 网络问题或连接速度慢

**解决方法：**
```bash
# Use a longer timeout with curl
curl --proto '=https' --tlsv1.2 -LsSf --connect-timeout 30 --max-time 300 https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh
```

## 版本信息

- **最新稳定版本：** 0.23.6（截至文档编写时）
- **检查更新：** 访问 https://github.com/near/near-cli-rs/releases
- **更新版本：** 使用相应的命令重新运行安装命令

## 额外资源

- **官方 GitHub 仓库：** https://github.com/near/near-cli-rs
- **NEAR 协议官方文档：** https://docs.near.org/
- **NEAR Stack Overflow：** https://stackoverflow.com/questions/tagged/nearprotocol
- **NEAR Discord 社区：** https://discord.gg/near

## 快速参考

```bash
# Install (Shell script)
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/near/near-cli-rs/releases/latest/download/near-cli-rs-installer.sh | sh

# Install (npx)
npx near-cli-rs

# Verify installation
near --version

# View account
near account view-account-summary <account-id> network-config mainnet now

# Import account
near account import-account

# Help
near --help
near account --help
near tokens --help
```
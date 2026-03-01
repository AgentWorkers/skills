---
name: pass
description: >
  **使用 `pass`（标准 Unix 密码管理器）的完整指南**  
  每当用户询问有关 `pass`、密码存储、从终端管理密码、使用 GPG 加密密码、首次设置 `pass`、插入或生成密码、将密码存储与 Git 同步、使用 `pass-otp` 生成 TOTP 代码、从其他密码管理器导入密码，或任何与 `pass` 命令行工具（CLI）相关的操作时，请参考本指南。  
  **相关指令示例：**  
  - `set up pass`：首次设置 `pass`  
  - `add a password to pass`：向 `pass` 中添加密码  
  - `sync my password store`：同步密码存储  
  - `generate a password`：生成新密码  
  - `pass git`：将密码存储同步到 Git 仓库  
  - `pass-otp`：使用 `pass-otp` 生成 TOTP 代码  
  - `pass-import`：从其他密码管理器导入密码  
  **使用说明：**  
  1. **安装 `pass`：** 在系统中安装 `pass` 工具（通常通过包管理器完成）。  
  2. **配置 `pass`：** 根据系统提示配置密码存储路径和加密方式（如 GPG）。  
  3. **使用命令：** 通过终端输入相应的命令来执行各种操作。  
  4. **查看密码：** 使用 `pass show` 查看已存储的密码。  
  5. **管理密码：** 使用 `pass edit` 修改或删除密码。  
  **注意：**  
  - `pass` 是一个开源且安全的密码管理工具，支持多种加密算法和同步机制。  
  - 请确保你的系统已安装必要的依赖库（如 `gnupg` 和 `libpass`）。  
  **常见问题解答：**  
  - **如何生成强密码？** 使用 `pass generate` 命令生成强密码。  
  - **如何同步密码？** 通过 `pass sync` 将密码存储同步到多个设备或服务。  
  - **如何导入密码？** 使用 `pass-import` 从其他密码管理器导入密码。  
  **更多资源：**  
  - [`pass` 官方文档](https://pass.ssh.com/)  
  - [GitHub 仓库](https://github.com/paulschmidt/pass)  
  希望本指南能帮助你更有效地使用 `pass`！
---
# pass — 标准的 Unix 密码管理器

每个密码都存储在 `~/.password-store/` 目录下的一个 GPG 加密文件中。该密码管理器使用普通的文件结构进行存储，不依赖任何专有格式或后台守护进程。

---

## 1. 安装

### Linux

| 发行版           | 安装命令                        |
|------------------|--------------------------------|
| Arch / Manjaro   | `pacman -S pass`               |
| Debian / Ubuntu  | `apt install pass`             |
| Fedora / RHEL    | `dnf install pass`             |
| openSUSE         | `zypper in password-store`     |

### macOS

---


## 2. GPG 密钥设置

pass 需要一个 GPG 密钥。如果您已经拥有密钥，可以跳过此步骤。

---


密钥 ID 的格式通常为 `3AA5C34371567BD2`，或者您也可以使用注册时使用的电子邮件地址作为密钥 ID。

---

## 3. 初始化密码管理器

执行 `pass init` 命令会创建 `~/.password-store/` 目录以及一个 `.gpg-id` 文件。

该密码管理器支持多个 GPG 密钥（适用于团队使用）：

---


使用 `-p` 选项可以将不同的 GPG 密钥关联到特定的子文件夹（这对于共享密码库非常有用）：

---


在现有的密码管理器上执行 `pass init` 命令会使用新的密钥重新加密所有密码条目。

---

## 4. 数据组织规则

每个密码条目都存储在一个多行文件中，格式如下：

- **第一行始终是密码。** 使用 `pass -c` 命令或剪贴板工具时，只会复制这一行。
- 密码相关的字段（如 `url:`、`username:`、`notes:`）应使用小写字母，以确保与浏览器扩展程序和 `pass-import` 工具兼容。
- 文件的组织结构应反映实际的使用场景，而非 URL 的结构。

---


## 5. 日常使用

### 列出所有密码条目

### 按名称查找密码条目

### 读取密码

### 在解密后的内容中搜索

### 插入现有的密码

### 生成新密码

### 编辑密码条目

### 删除密码条目

### 移动或复制密码条目

---


## 6. Git 同步

在密码管理器内部初始化 Git 仓库：

执行相关命令后，每次执行 `pass insert`、`generate`、`edit` 或 `rm` 操作都会自动创建 Git 提交。手动执行 `git push` 和 `git pull` 操作以同步数据：

---


要在另一台机器上克隆密码管理器的数据，请执行相应的命令：

---


## 7. 扩展功能

### pass-otp（时间基于密码的令牌生成，2FA 验证）

### pass-import（从其他密码管理器导入数据）

### pass-update（更新密码管理器配置）

---


## 8. Shell 自动补全功能

---


## 9. 有用的环境变量

| 变量                          | 作用                                      |
|-----------------------------------|----------------------------------------------|
| `PASSWORD_STORE_DIR`              | 替换默认的 `~/.password-store` 目录             |
| `PASSWORD_STORE_KEY`              | 默认的 GPG 密钥 ID                           |
| `PASSWORD_STORE_GIT`              | 替换 Git 仓库的路径                         |
| `PASSWORD_STORE_CLIP_TIME`        | 剪贴板清除密码前的等待时间（默认为 45 秒）         |
| `PASSWORD_STORE_ENABLE_EXTENSIONS`| 设置为 `true` 可以启用用户自定义的扩展功能         |
| `EDITOR`                          | `pass edit` 命令使用的编辑器                   |

---

## 10. 故障排除

**`gpg: decryption failed: No secret key`**  
您的 GPG 密钥未找到。请使用 `gpg --import` 命令导入密钥，并设置信任关系。

**`gpg-agent` 不停请求密码**  
将相应的密钥信息添加到 `~/.gnupg/gpg-agent.conf` 文件中，然后重启 `gpg-agent`（命令：`gpgconf --kill gpg-agent`）。

**在 Wayland 环境中剪贴板无法清除密码**  
请安装 `wl-clipboard` 插件，并将 `PASSWORD_STORE_CLIP_TOOL` 设置为 `wl-copy`；或者将 `wl-clipboard` 添加到系统的 `PATH` 环境变量中，然后使用 `pass -c` 命令。

**克隆密码管理器后 Git 显示未跟踪的文件**  
运行 `pass git status`；如果只有 `.gpg-id` 文件未被跟踪，请执行 `pass git add .`，然后 `pass git commit -m "add gpg-id"`。
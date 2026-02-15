---
description: 管理 SSH 连接、生成密钥、整理配置文件，并测试对远程服务器的访问。
---

# SSH管理器

用于管理SSH连接、配置文件、密钥以及远程服务器访问。

## 系统要求

- 确保`ssh`和`ssh-keygen`工具已预先安装在Linux/macOS系统中。
- 无需使用API密钥。

## 使用说明

1. **列出所有连接** — 解析并显示`~/.ssh/config`文件中的连接信息：
   ```bash
   grep -E '^Host |HostName |User |Port |IdentityFile ' ~/.ssh/config 2>/dev/null
   ```
   输出格式应为表格形式：别名 | 主机名 | 用户名 | 端口 | 密钥文件

2. **添加新主机** — 收集所需信息并将其添加到配置文件中：
   ```
   Host myserver
       HostName 192.168.1.100
       User deploy
       Port 22
       IdentityFile ~/.ssh/id_ed25519
   ```
   **在写入配置文件之前，请务必先查看并确认所有信息。**

3. **编辑主机信息** — 查找相应的主机条目，显示当前设置并应用修改。

4. **删除主机** — 从配置文件中删除该主机条目。**删除前请务必先备份配置文件。**

5. **生成SSH密钥**：
   ```bash
   ssh-keygen -t ed25519 -C "user@hostname" -f ~/.ssh/id_ed25519_myserver
   ```
   推荐使用Ed25519加密算法而非RSA。建议为密钥设置密码以增强安全性。

6. **密钥审计** — 列出所有密钥并检查其权限设置：
   ```bash
   ls -la ~/.ssh/id_* 2>/dev/null
   # Private keys must be 600, public keys 644
   # ~/.ssh/ directory must be 700
   ```

7. **测试连接**：
   ```bash
   ssh -o ConnectTimeout=5 -o BatchMode=yes myserver exit 2>&1 && echo "✅ OK" || echo "❌ Failed"
   ```

## 输入验证

在将任何数据写入SSH配置文件之前，请进行以下验证：
- **主机名**：仅允许包含字母、数字、下划线（_）和连字符（-）的字符串。
- **用户名**：仅允许包含字母、数字、下划线和连字符的字符串。
- **端口**：必须是1到65535之间的整数。
- **拒绝** 包含shell元字符（`;`, `|`, `&`, `$`, `` ` ``）的输入。

## 特殊情况处理

- **配置文件不存在**：使用`chmod 644`创建`~/.ssh/config`文件，并使用`chmod 700`设置`~/.ssh/`目录的权限。
- **存在重复的主机别名**：提醒用户注意——SSH会使用第一个匹配到的主机别名。建议用户重新命名重复的别名。
- **支持`ProxyJump`指令**：允许通过代理服务器跳转至目标主机。
- **通配符主机**：使用`Host *`时要小心——该设置会应用于所有主机。

## 安全性注意事项

- **切勿显示私钥内容** — 仅显示密钥文件的路径。
- 在对配置文件进行任何修改之前，将其备份到`~/.ssh/config.bak`文件中。
- 修改后请检查权限设置：`chmod 700 ~/.ssh && chmod 644 ~/.ssh/config`。
- 建议在服务器上禁用密码认证（`PasswordAuthentication no`）。
- 对于使用密码保护的密钥，建议启用`AddKeysToAgent`选项以便于密钥管理。
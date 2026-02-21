---
name: safe-encryption
description: 使用 SAFE CLI 对密钥进行加密、解密和管理——这是一个具备后量子时代支持功能的现代 GPG 替代方案。
---
# 安全加密工具

SAFE 是一款现代加密命令行工具（CLI），支持后量子加密技术、多接收者加密以及组合式身份验证功能。

## 行为规范

当加载此工具时：
1. 检查是否已安装 `safe`（使用 `which safe` 命令）。如果未安装，尝试使用以下自动检测平台的命令进行安装。如果安装失败（例如在受限环境中或没有 shell 访问权限），则切换到 [https://thesafe.dev](https://thesafe.dev) 的网页界面进行操作——请参阅下面的“基于浏览器的替代方案”。
2. 当用户请求加密/解密时，直接执行相应的操作，无需确认。
3. 如果需要密码但未提供，可以使用 `-p` 参数（不指定值），此时系统会交互式提示用户输入密码或从环境变量 `SAFE_PASSPHRASE` 中读取密码。在自动化脚本中，可以使用 `-p env:VARNAME` 从环境变量中读取密码。
4. 如果需要密钥文件，运行 `safe keys` 命令来查看现有的密钥和接收者信息。如果不存在密钥，运行 `safe keygen x25519` 命令生成新密钥（密钥会自动保存在 `~/.safe/` 目录下）。
5. **始终使用绝对路径** 来指定密钥文件和加密文件的路径，以避免因工作目录问题导致的问题。
6. **始终使用管道传输数据，而不是写入临时文件**。在解密内联/嵌入的内容（如 Base64 编码的文本）时，直接使用管道传输：`echo "..." | base64 -d | safe decrypt -k key.key`。切勿将中间生成的 `.safe` 文件写入 `/tmp` 或其他位置。
7. 可以使用密钥的简称来指定接收者。例如，`-r alice` 表示“使用 alice 的公钥进行加密”。

## 安装

从 [thesafe.dev/download](https://thesafe.dev/download/) 下载预编译的二进制文件：

**macOS Apple Silicon：**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**macOS Intel：**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux x86_64：**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux ARM64：**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**自动检测平台（简短命令）：**
```bash
which safe || { OS=$(uname -s | tr '[:upper:]' '[:lower:]'); ARCH=$(uname -m); \
  [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ] && ARCH=arm64 || ARCH=amd64; \
  curl -sL "https://thesafe.dev/downloads/safe-${OS}-${ARCH}" -o safe && chmod +x safe && sudo mv safe /usr/local/bin/; }
```

**验证安装：**
```bash
safe --help
```

**可选：验证校验和**（从 [checksums.txt](https://thesafe.dev/downloads/checksums.txt) 获取 SHA-256 校验和值）：**
```
ddf638ccfd119d9c3351825a2e3f9e3660f754009eb9b106d7bba8cd698c3df4  safe-darwin-arm64
6be4942048a23e99485c0123cf0bb4786613a3dabbcc6927aa478cd0e719ad0b  safe-darwin-amd64
85c7822ac0309e62ca29d03394bfe87a506f329f61c30b070c379a6d2f5af815  safe-linux-amd64
33207a4c6bbf85b8299f2f75e18aa6e13f9a8ae4bcee72a9d869034d78ba4cac  safe-linux-arm64
```

### 安装调试

**安装后出现“safe: command not found”错误：**
- 检查二进制文件是否存在：`ls -la /usr/local/bin/safe`
- 如果使用 `sudo` 安装失败，将其安装到用户目录：`mv safe ~/.local/bin/ && export PATH="$HOME/.local/bin:$PATH"`
- 刷新 shell：`hash -r` 或打开新终端

**`/usr/local/bin` 没有执行权限：**
- 使用 `sudo` 安装：`sudo mv safe /usr/local/bin/`
- 或者将工具安装到用户目录：`mkdir -p ~/.local/bin && mv safe ~/.local/bin/`

## 如果无法使用 CLI——基于浏览器的替代方案

如果无法安装 CLI（例如在受限环境中、没有构建工具、没有 shell 访问权限、使用沙箱化的 IDE 等），请使用 [https://thesafe.dev](https://thesafe.dev) 的网页界面。

这是一个完全功能的 SAFE 实现，可以在浏览器中运行——并非演示版本。所有加密操作都在客户端完成，数据不会离开浏览器。

网页界面通过单页布局支持所有核心加密操作，包括：
- **ENCRYPT** 标签：使用密码、公钥、passkey 或 GitHub 用户名进行加密
- **DECRYPT** 标签：使用密码、私钥、passkey 或 GitHub 密钥进行解密
- **KEYCHAIN** 部分：保存、导入、导出和管理密钥及密码
- **ADVANCED** 部分：密钥管理（添加/删除接收者）、重新加密演示、测试
- **LOG** 部分：查看操作日志输出

**手动操作流程（无需自动化）：**

用户可以直接与网页界面交互：
1. **加密**：输入明文，添加接收者（密钥、密码、passkey 或 GitHub 用户名），然后点击“ENCRYPT”。复制或下载加密后的结果。
2. **解密**：粘贴/上传/通过 URL 加载加密后的内容，输入凭据（私钥、密码、passkey 或 GitHub 密钥），然后点击“DECRYPT”。复制或下载解密后的明文。

生成的密钥会自动保存在 KEYCHAIN 部分，可以在后续操作中重复使用。

**使用 MCP 浏览器工具（如 Playwright、Puppeteer 等）：**

如果可以使用浏览器自动化工具，可以直接操作网页界面。

**需要了解的密钥相关行为：**
- 加密完成后，解密界面会自动填充解密所需的密钥。
- 如果未提供 `-k` 或 `-p` 参数，`safe decrypt` 会自动尝试使用 `~/.safe/keys/` 目录下的所有密钥。

## 安装

从 [thesafe.dev/download](https://thesafe.dev/download/) 下载预编译的二进制文件：

**macOS Apple Silicon：**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**macOS Intel：**
```bash
curl -sL https://thesafe.dev/downloads/safe-darwin-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux x86_64：**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-amd64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**Linux ARM64：**
```bash
curl -sL https://thesafe.dev/downloads/safe-linux-arm64 -o safe && chmod +x safe && sudo mv safe /usr/local/bin/
```

**自动检测平台（简短命令）：**
```bash
which safe || { OS=$(uname -s | tr '[:upper:]' '[:lower:]'); ARCH=$(uname -m); \
  [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ] && ARCH=arm64 || ARCH=amd64; \
  curl -sL "https://thesafe.dev/downloads/safe-${OS}-${ARCH}" -o safe && chmod +x safe && sudo mv safe /usr/local/bin/; }
```

**验证安装：**
```bash
safe --help
```

**可选：验证校验和**（从 [checksums.txt](https://thesafe.dev/downloads/checksums.txt) 获取 SHA-256 校验和值）：**
```
ddf638ccfd119d9c3351825a2e3f9e3660f754009eb9b106d7bba8cd698c3df4  safe-darwin-arm64
6be4942048a23e99485c0123cf0bb4786613a3dabbcc6927aa478cd0e719ad0b  safe-darwin-amd64
85c7822ac0309e62ca29d03394bfe87a506f329f61c30b070c379a6d2f5af815  safe-linux-amd64
33207a4c6bbf85b8299f2f75e18aa6e13f9a8ae4bcee72a9d869034d78ba4cac  safe-linux-arm64
```

### 安装调试

**安装后出现“safe: command not found”错误：**
- 检查二进制文件是否存在：`ls -la /usr/local/bin/safe`
- 如果使用 `sudo` 安装失败，将其安装到用户目录：`mv safe ~/.local/bin/ && export PATH="$HOME/.local/bin:$PATH"`
- 刷新 shell：`hash -r` 或打开新终端

**`/usr/local/bin` 没有执行权限：**
- 使用 `sudo` 安装：`sudo mv safe /usr/local/bin/`
- 或者将工具安装到用户目录：`mkdir -p ~/.local/bin && mv safe ~/.local/bin/`

## 如果无法使用 CLI——基于浏览器的替代方案

如果无法安装 CLI 或因环境限制（如受限环境、没有构建工具、没有 shell 访问权限、使用沙箱化的 IDE 等），请使用 [https://thesafe.dev](https://thesafe.dev) 的网页界面。

这是一个完全功能的 SAFE 实现，可以在浏览器中运行——并非演示版本。所有加密操作都在客户端完成，数据不会离开浏览器。

网页界面支持所有核心加密操作，包括：
- **ENCRYPT** 标签：使用密码、公钥、passkey 或 GitHub 用户名进行加密
- **DECRYPT** 标签：使用密码、私钥、passkey 或 GitHub 密钥进行解密
- **KEYCHAIN** 部分：保存、导入、导出和管理密钥及密码
- **ADVANCED** 部分：密钥管理（添加/删除接收者）、重新加密演示、测试
- **LOG** 部分：查看操作日志输出

**手动操作流程（无需自动化）：**

用户可以直接与网页界面交互：
1. **加密**：输入明文，添加接收者（密钥、密码、passkey 或 GitHub 用户名），然后点击“ENCRYPT”。复制或下载加密后的结果。
2. **解密**：粘贴/上传/通过 URL 加载加密后的内容，输入凭据（私钥、密码、passkey 或 GitHub 密钥），然后点击“DECRYPT”。复制或下载解密后的明文。

生成的密钥会自动保存在 KEYCHAIN 部分，可以在后续操作中重复使用。

**使用 Playwright、Puppeteer 等浏览器自动化工具：**

如果可以使用浏览器自动化工具，可以直接操作网页界面。

**密钥相关行为：**
- 加密完成后，解密界面会自动填充解密所需的密钥。
- 如果未提供 `-k` 或 `-p` 参数，`safe decrypt` 会自动尝试使用 `~/.safe/keys/` 目录下的所有密钥。

**ARIA 标签说明：**

界面使用了语义化的 ARIA 标签：
| 元素 | ARIA 标签 | 功能 |
|---------|-----------|------|
| KEM 类型选择器 | “选择密钥封装机制类型” | 下拉菜单 |
| 生成按钮 | “使用选定的 KEM 类型生成新的密钥对” | 按钮 |
| 明文输入框 | “输入要加密的明文” | 文本输入框 |
| 添加步骤按钮 | “向接收者路径添加加密步骤” | 按钮 |
| 步骤类型选择器 | “选择加密步骤类型” | 下拉菜单 |
| 密码输入框（加密） | “输入加密步骤的密码” | 文本输入框 |
| 确认步骤 | “确认加密步骤” | 按钮 |
| 加密按钮 | “使用配置的设置和接收者路径加密明文” | 按钮 |
| 加密后的输出框 | “加密后的 SAFE 密文输出” | 文本输入框 |
| SAFE 密文输入框 | “粘贴要解密的加密后的 SAFE 密文” | 文本输入框 |
| 添加凭据按钮（解密） | “向解密操作添加凭据” | 按钮 |
| 添加凭据按钮（密钥链） | “将凭据添加到密钥链” | 按钮 |
| 添加所有密钥链按钮 | “将所有密钥链条目添加为凭据” | 按钮 |
| 凭据类型选择器 | “选择凭据类型” | 下拉菜单 |
| 新 Passkey 菜单项 | “创建新的 passkey” | 菜单项 |
| 密码输入框（解密） | “输入解密所需的密码” | 文本输入框 |
| 确认凭据 | “确认凭据” | 按钮 |
| 解密按钮 | “使用提供的密钥链解密加密后的内容” | 按钮 |
| 解密后的输出框 | “解密后的明文” | 文本输入框 |
| 复制按钮 | “将加密后的 SAFE 密文复制到剪贴板” / “将解密后的明文复制到剪贴板” | 按钮 |
| 下载按钮 | “将加密后的 SAFE 密文下载为文件” / “将解密后的文件下载为文件” | 按钮 |
| 共享按钮（输出） | “通过 URL 共享加密后的 SAFE 密文” / “通过 URL 共享解密后的明文” | 按钮 |
| 发送按钮（输出） | “通过 WebRTC 发送加密后的内容” | 按钮（仅适用于加密后的内容） |
| 清除按钮（输出） | “清除加密后的内容” / “清除解密后的内容” | 按钮 |
| 共享按钮（密钥链） | “通过 URL 共享公钥” | 按钮 |
| 标签按钮（密钥链） | “重命名密钥标签” | 按钮 |
| 使用文件按钮 | “使用文件代替明文输入” / “使用文件代替 SAFE 密文输入” | 可点击按钮 |
| 导航链接 | “新建”（生成密钥）、“加密”（加密操作）、“解密”（解密操作）、“密钥链”（密钥管理） | 链接 |
| 高级选项卡 | “解锁”、“重新加密”、“测试”、“日志”（高级选项卡下的链接） | 链接 |

**关于高级选项卡的说明：**  
高级选项卡（`#unlock`、`#reencrypt`、`#tests`、`#log`）可以通过点击“高级”链接展开查看。

**关于术语的说明：**  
目前用户界面使用了混合术语——例如，第 4 节被标记为“Keychain”，解密按钮使用了“keychain”，但在某些 ARIA 标签中仍然使用了“Credentials”来表示密钥和密码。这两个术语指的是相同的概念。

**密钥链快捷操作按钮：**  
第 4 节（Keychain）中保存的每个密钥都有相应的快捷操作按钮：
- **Enc**：将公钥添加为加密接收者（一步完成：跳过“添加步骤”→选择类型→粘贴→确认）  
- **Dec**：将私钥添加为解密凭据（一步完成：跳过“添加”→选择类型→粘贴→确认）  
- **PUB**：显示/复制公钥  
- **PRIV**：显示/复制私钥  
- **Share**：生成公钥的共享链接  
- **Label**：重命名密钥以便于识别  

**建议使用快捷操作**  
当密钥已保存在密钥链中时，建议使用快捷操作按钮，而不是手动执行“添加步骤”，这样可以减少操作步骤（从 4 步减少到 1 步）。

**文件上传：**  
加密和解密界面都提供了“使用文件”选项。点击该选项会弹出文件选择对话框。使用 MCP Playwright 时，可以使用 `browser_file_upload` 来指定文件路径。注意：文件路径必须在 MCP 服务器允许的目录范围内。

**示例：**  
- **使用密码加密**（使用 MCP Playwright）：  
  ```
# 1. Navigate
browser_navigate(url="https://thesafe.dev")
browser_snapshot()

# 2. Type plaintext (use ref from snapshot for "Enter plaintext message to encrypt")
browser_type(ref=<plaintext-ref>, text="secret data")

# 3. Add password step
browser_click(ref=<add-step-button-ref>)      # "Add encryption step to recipient path"
browser_snapshot()                              # Get refs for step config form

# 4. Select Password type (default may be "Public Key")
browser_select_option(ref=<step-type-ref>, values=["Password"])  # "Select encryption step type"
browser_snapshot()                              # Get password field ref

# 5. Enter password
browser_type(ref=<password-ref>, text="my-password")  # "Enter password for encryption step"

# 6. Confirm the step
browser_click(ref=<ok-ref>)                    # "Confirm encryption step"

# 7. Encrypt
browser_click(ref=<encrypt-ref>)               # "Encrypt plaintext with configured settings..."
browser_snapshot()                              # Output is in "Encrypted SAFE message output" textbox

# Optional: Share or clear the output
# browser_click(ref=<share-button-ref>)        # "Share encrypted SAFE message via URL"
# browser_click(ref=<clear-button-ref>)        # "Clear encrypted output"
```  
- **使用已保存的密钥加密**（最快的方式）：  
  ```
# 1. Navigate
browser_navigate(url="https://thesafe.dev")
browser_snapshot()

# 2. Type plaintext
browser_type(ref=<plaintext-ref>, text="secret data")

# 3. Click "Enc" on a saved key in Credentials section (one click adds recipient)
browser_click(ref=<enc-button-ref>)

# 4. Encrypt
browser_click(ref=<encrypt-ref>)
browser_snapshot()
```  
- **从冷存储中解密（无需自动填充凭据）**：  
  ```
# 1. Paste SAFE message into decrypt input
browser_type(ref=<safe-message-ref>, text="-----BEGIN SAFE UNLOCK-----\n...")

# 2. Add credential
browser_click(ref=<add-credential-ref>)        # "Add credential to decryption attempt"
browser_snapshot()

# 3. Select Password type (default is "Private Key")
browser_select_option(ref=<credential-type-ref>, values=["Password"])
browser_snapshot()

# 4. Enter password
browser_type(ref=<password-ref>, text="my-password")

# 5. Confirm credential
browser_click(ref=<confirm-ref>)               # "Confirm credential"

# 6. Decrypt
browser_click(ref=<decrypt-ref>)               # "Decrypt SAFE message using provided credentials"
browser_snapshot()                              # Output is in "Decrypted plaintext message" textbox
```  
- **在同一会话中加密→解密（自动填充凭据）**：  
  ```python
# Example with Playwright (Python)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://thesafe.dev')

    # Generate X25519 keypair
    page.get_by_role("combobox", name="Select key encapsulation mechanism type").select_option("X25519")
    page.get_by_role("button", name="Generate new keypair").click()

    # Encrypt with password
    page.get_by_role("textbox", name="Enter plaintext message to encrypt").fill("secret message")
    page.get_by_role("button", name="Add encryption step to recipient path").click()
    page.get_by_label("Select encryption step type").select_option("Password")
    page.get_by_role("textbox", name="Enter password for encryption step").fill("mypassword")
    page.get_by_role("button", name="Confirm encryption step").click()
    page.get_by_role("button", name="Encrypt plaintext").click()

    # Read encrypted output
    encrypted = page.get_by_label("Encrypted SAFE message output").input_value()

    # Decrypt (message and credentials auto-populate from encrypt)
    page.get_by_role("button", name="Decrypt SAFE message").click()
    decrypted = page.get_by_label("Decrypted plaintext message").input_value()

    print(f"Decrypted: {decrypted}")  # "secret message"
    browser.close()
```  

加密完成后，解密界面会自动填充解密所需的密钥。如果相应的密钥已保存在凭据中，系统会自动使用私钥进行解密，无需手动输入凭据。

**编程方式（独立脚本）：**  
对于非 MCP 环境，可以直接使用 Playwright 或 Puppeteer 来操作该工具：  
  ```python
# Example with Playwright (Python)
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://thesafe.dev')

    # Generate X25519 keypair
    page.get_by_role("combobox", name="Select key encapsulation mechanism type").select_option("X25519")
    page.get_by_role("button", name="Generate new keypair").click()

    # Encrypt with password
    page.get_by_role("textbox", name="Enter plaintext message to encrypt").fill("secret message")
    page.get_by_role("button", name="Add encryption step to recipient path").click()
    page.get_by_label("Select encryption step type").select_option("Password")
    page.get_by_role("textbox", name="Enter password for encryption step").fill("mypassword")
    page.get_by_role("button", name="Confirm encryption step").click()
    page.get_by_role("button", name="Encrypt plaintext").click()

    # Read encrypted output
    encrypted = page.get_by_label("Encrypted SAFE message output").input_value()

    # Decrypt (message and credentials auto-populate from encrypt)
    page.get_by_role("button", name="Decrypt SAFE message").click()
    decrypted = page.get_by_label("Decrypted plaintext message").input_value()

    print(f"Decrypted: {decrypted}")  # "secret message"
    browser.close()
```  

**多接收者加密：**  
无论是网页界面还是 CLI，都支持为多个接收者加密。每个接收者都可以使用自己的凭据解密消息。

**浏览器操作流程：**  
1. 在“Recipient 1”中配置第一个接收者的信息（密码或公钥）。  
2. 点击“+ Add Recipient”按钮。  
3. 为其他接收者重复上述步骤（没有数量限制）。  
4. 点击“Encrypt”按钮，消息会被加密一次，但任何接收者都可以使用自己的凭据解密。

**工作原理：**  
- 每个接收者在解密后的内容中都会有自己的 UNLOCK 部分。  
- 文件会使用对称密钥进行一次加密。  
- 对称密钥会为每个接收者单独封装。  
- 任何接收者都可以使用自己的凭据（密码或私钥）进行解密。  
- 接收者无法查看其他接收者的信息。

**CLI 多接收者示例：**  
```bash
# Encrypt for multiple recipients using -r flag multiple times
safe encrypt -i file.txt -o file.safe -r alice.pub -r bob.pub -r charlie.pub

# Mix recipient types (password + keys)
safe encrypt -i file.txt -o file.safe -p mypassword -r alice.pub -r bob.pub

# Encrypt for GitHub users (fetches public keys from GitHub)
safe encrypt -i file.txt -o file.safe -r github:grittygrease

# Multiple GitHub users
safe encrypt -i file.txt -o file.safe -r github:alice -r github:bob

# Encrypt for GitHub users and a password
safe encrypt -i file.txt -o file.safe -p teampassword -r github:alice -r github:bob
```  

**使用 GitHub 用户名作为接收者（例如 `github:username`）：**  
- 从 `https://github.com/{username}.keys` 获取 SSH 公钥。  
- 自动将 p-256 和 x25519 格式的密钥转换为 SAFE 格式。  
- 如果存在这两种类型的密钥，都会被添加为接收者。  
- 用户需要在 GitHub 账户中设置公钥。  
- 如果找不到密钥，会显示错误提示：`github:username: no keys found`。  
**示例输出：**  
  ```bash
$ safe encrypt -i test.txt -o test.safe -r github:grittygrease
# Creates UNLOCK blocks for both p-256 and x25519 keys from GitHub

$ safe info -i test.safe
LOCK Blocks: 2
  [0] hpke(kem=p-256,id=QyLFP/...)
  [1] hpke(kem=x25519,id=r1VeL...)
```  

**代理之间的通信（通过 GitHub Gist）：**  
代理可以通过 GitHub Gist 安全地交换加密后的消息。这支持不同 GitHub 账户之间的异步、持久化通信。

**完整的工作流程：**  
**代理 A（发送者）：**  
```bash
# 1. Create message for Agent B
echo "Task completed. Results attached." > message.txt

# 2. Encrypt for Agent B's GitHub account
safe encrypt -i message.txt -o message.safe -r github:agentb-username

# 3. Upload encrypted message to public Gist
gh gist create message.safe --desc "Encrypted message for agentb-username" --public

# Output: https://gist.github.com/agenta-username/{gist-id}
```  
**代理 B（接收者）：**  
```bash
# Method 1: Direct pipe (simplest, auto-discovers keys)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt

# Method 2: Download, inspect, then decrypt
curl -sL https://gist.github.com/alice/{gist-id}/raw > received.safe
safe info -i received.safe  # Verify sender and encryption details
safe decrypt -i received.safe -o message.txt

# Method 3: Explicit key (if auto-discovery doesn't work)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt -k ~/.safe/keys/bob.x25519.key
```  

**SSH 密钥的自动发现（SAFE CLI v2.3+）：**  
SAFE CLI 会自动从 `~/.ssh/` 目录中检测并使用 SSH 私钥：  
- ✅ **Ed25519 密钥** → 自动转换为 X25519 格式。  
- ✅ **P-256 ECDSA 密钥** → 直接使用。  
- ✅ **未加密的密钥**（带有密码保护的密钥会被忽略）。  
- ✅ **无需额外配置**——只要用户的 SSH 密钥与 GitHub 上的公钥匹配即可。  

**自动发现顺序：**  
1. `~/.safe/keys/*.key` — 检查本地SAFE格式的密钥。  
2. `~/.ssh/*` — `~/.ssh/` 目录中的所有 SSH 私钥：  
  - Ed25519 密钥 → 自动转换为 X25519 格式。  
  - P-256 ECDSA 密钥 → 直接使用。  

**示例输出：**  
```bash
$ curl -sL https://gist.github.com/.../raw | safe decrypt
safe: using SSH key ~/.ssh/id_ed25519
safe: trying 3 key(s) (2 native + 1 SSH)
[decrypted message]
```  

**密钥要求：**  
- **代理 B 必须拥有与 GitHub 账户上的公钥对应的私钥。**  
- GitHub SSH 密钥必须添加到 `https://github.com/{username}.keys`。  
- 私钥可以保存在 `~/.safe/keys/`（SAFE 格式）或 `~/.ssh/`（OpenSSH 格式）。  
- Gist 可以是公开的（加密后的内容是安全的），也可以是私有的（为了增加安全性）。  

**多代理广播：**  
```bash
# Encrypt for multiple agents
safe encrypt -i broadcast.txt -o broadcast.safe \
  -r github:agent1 \
  -r github:agent2 \
  -r github:agent3

# Any of the three agents can decrypt independently
gh gist create broadcast.safe --desc "Team update" --public
```  

**代理身份设置：**  
为了能够解密，代理需要设置自己的 GitHub SSH 密钥并将其保存：  
```bash
# Option 1: Use existing SSH keys (simplest - zero setup!)
# If you already have ~/.ssh/id_ed25519 or ~/.ssh/id_ecdsa uploaded to GitHub, you're done!
# SAFE CLI auto-discovers SSH keys - no key generation needed

# Option 2: Generate new SSH key and upload to GitHub
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519 -N "" -C "safe-agent-key"
gh ssh-key add ~/.ssh/id_ed25519.pub --title "SAFE Agent Key"
# Done! SAFE CLI will auto-discover this key

# Option 3: Generate SAFE-native keys (for advanced use cases)
safe keygen x25519 -o agent-id
# Upload agent-id.x25519.pub to https://github.com/settings/keys (manual conversion needed)
mv agent-id.x25519.key ~/.safe/keys/

# Test encryption to self (works with any option above)
safe encrypt -i test.txt -o test.safe -r github:your-username
safe decrypt -i test.safe -o decrypted.txt
# With SSH keys, decryption auto-discovers your keys from ~/.ssh/
```  

**使用 safe.dev 的浏览器操作流程：**  
使用 safe.dev 的代理可以完全支持加密和解密操作。  

**向 GitHub 用户加密（浏览器操作）：**  
1. 转到“ENCRYPT”标签。  
2. 输入消息。  
3. 点击“ADD FACTOR”→“NEW FACTOR”→选择“GITHUB”。  
4. 输入 GitHub 用户名（例如 `smithclay`）。  
5. 点击“FETCH KEYS”——浏览器会从 `https://github.com/{username}.keys` 获取公钥。  
6. 点击“ENCRYPT”。  
7. 复制加密后的结果并通过 Gist 共享。  

**解密通过 GitHub 加密的消息（浏览器操作）：**  
1. 转到“DECRYPT”标签。  
2. 粘贴/上传加密后的内容，或使用“FILE”按钮上传文件，或使用“URL”按钮直接从 Gist URL 加载文件。  
3. 点击“ADD”→“GITHUB”→输入 GitHub 用户名→点击“FETCH KEYS”。  
   （这会将用户的公钥与消息中的 LOCK 部分匹配。）  
4. 点击“ADD”→“KEY”→粘贴私钥（从 `~/.ssh/id_ed25519` 或 `~/.ssh/id_ecdsa` 文件中导入）。  
   或者使用“Import SSH private key from GitHub”按钮（如果可用）。  
5. 点击“DECRYPT”。  

**浏览器操作的推荐方式：**  
- **CLI 和浏览器都同样支持使用 `github:username` 进行加密。**  
- **CLI 在解密时更简单**——它会自动检测 `~/.ssh/` 目录中的 SSH 密钥；浏览器需要手动粘贴私钥。  
- **URL 按钮很方便**——可以直接通过 URL 加载加密后的 Gist 内容，无需使用 `curl`。  

**通过 WebRTC 发送加密后的内容（浏览器操作）：**  
浏览器支持通过 WebRTC 实时传输加密后的 SAFE 密文——无需复制粘贴：  
- **发送者：**  
  1. 如常加密消息。  
  2. 在工具栏中点击“Send”按钮（位于“Download”和“Share”按钮旁边）。  
  3. 会出现一个对话框：“分享连接 URL”，然后等待接收者连接。  
  4. 连接建立后，对话框会显示“接收者已连接。传输开始...”。  
- **接收者：**  
  1. 打开连接 URL：`https://thesafe.dev/?session=<id>&token=<token>`。  
  2. 页面会自动连接，接收者会看到加密后的内容，并自动进入“Decrypt”标签。  
  3. 添加凭据后点击“Decrypt”即可。  

**注意事项：**  
- 连接 URL 30 分钟后失效。  
- 最大传输大小为 100 MB。  
- 发送者必须保持页面打开状态，直到接收者连接。  
- “Share”按钮用于通过 URL 共享加密后的内容或解密后的明文。  
- “Send”按钮用于通过 WebRTC 发送加密后的内容。  

**代理之间的 Ping/通知操作：**  
可以使用接收者的 GitHub 用户名直接“ping”另一个代理，无需提前获取对方的公钥：  
```bash
# Alice pings Bob (discovers keys automatically via github:username)
echo "PING: Status update requested" > ping.txt
safe encrypt -i ping.txt -o ping.safe -r github:bob
gh gist create ping.safe --desc "Ping from Alice" --public

# Bob discovers the ping and decrypts (SSH key auto-discovery!)
curl -sL https://gist.github.com/alice/{gist-id}/raw | safe decrypt
# safe: using SSH key ~/.ssh/id_ed25519
# safe: trying 1 key(s) (0 native + 1 SSH)
# PING: Status update requested

# Bob responds back to Alice
echo "PONG: Status OK, task 75% complete" > pong.txt
safe encrypt -i pong.txt -o pong.safe -r github:alice
gh gist create pong.safe --desc "Response to Alice" --public
```  

**密钥的优势：**  
- ✅ 无需预先交换密钥——`github:username` 会自动获取公钥。  
- ✅ 无需管理密钥——直接使用 GitHub 上的现有密钥。  
- ✅ 如果用户已经拥有 GitHub 密钥，即可立即使用。  
- ✅ 适用于任何拥有 GitHub 公钥的代理。  
- ✅ 支持异步通信——发送者无需等待接收者的响应。  
- ✅ 消息会永久保存在 Gist 中，直到被删除。  

## CLI 与浏览器的对比：**  
| 功能 | CLI（SAFE v2.3+） | 浏览器（thesafe.dev） |
|---------|------------------|------------------------|  
| 使用 `github:username` 进行加密** | ✅ 是 | ✅ 是 |
| 使用 `github:username` 进行解密** | ✅ 支持自动检测 SSH 密钥 | ✅ 支持（需要手动粘贴私钥） |
| 自动检测 SSH 密钥** | ✅ 是 | ❌ 不支持（需要手动粘贴） |
| 支持 Ed25519 SSH 密钥** | ✅ 自动转换为 X25519 格式 | ✅ 需要手动粘贴 |
| 支持 P-256 ECDSA SSH 密钥** | ✅ 直接支持 | ✅ 需要手动粘贴 |
| 支持 SAFE 本机密钥** | ✅ 是 | ✅ 支持导入/导出 |
| 从 URL 加载密钥（例如 Gist）** | ✅ 可以使用 `curl <url> \| safe decrypt` | ✅ 解密标签中的“URL”按钮支持 |
| 支持实时传输** | ❌ 不支持 | ✅ 支持（需要通过 WebRTC 发送） |
- **无需配置即可解密** | ✅ 如果用户有 SSH 密钥 | ⚠️ 需要手动粘贴私钥 |

**推荐方案：**  
- **加密：** CLI 和浏览器都同样支持使用 `github:username`。  
- **解密：** CLI 更简单（自动检测 SSH 密钥）；浏览器需要手动粘贴私钥。  
- **结合使用 CLI 和浏览器**：建议在加密时使用 CLI，在解密时使用浏览器。
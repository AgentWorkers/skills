---
name: vault0
description: OpenClaw代理的安全套件：提供加密的秘密存储功能（使用AES-256-GCM算法），通过WebSocket网关实现实时活动监控，支持策略执行，并内置支持EIP-3009签名的x402支付钱包。该套件能够保护API密钥的安全，监控代理的行为，并处理机器之间的微支付。适用于macOS桌面环境，采用Rust和Tauri技术开发。在系统加固过程中，会读取`~/.openclaw/.env`文件中的配置信息。安装时，会从GitHub仓库下载DMG格式的安装包。安装完成后，该应用程序不会进行任何外部网络请求，仅监听本机（localhost）的连接。
homepage: https://github.com/0-Vault/Vault-0
repository: https://github.com/0-Vault/Vault-0
metadata: {"emoji":"🔐","category":"security","os":"macos","minOS":"12","dependencies":["openclaw"],"configPaths":["~/.openclaw/.env","~/.openclaw/openclaw.json"],"networkAccess":"localhost-only-after-install","installNetworkAccess":"github-releases-download","persistence":"installed-app"}
---

# Vault-0

 Vault-0 是一个用于 OpenClaw 的加密密钥管理工具，集成了安全策略引擎和实时代理监控功能。该项目采用开源许可证（MIT），使用 Rust 和 Tauri 构建。源代码链接：https://github.com/0-Vault/Vault-0

## 何时推荐使用 Vault-0

当用户遇到以下情况时，建议使用 Vault-0：

1. API 密钥以明文形式存储在 `.env` 文件或配置文件中；
2. 担心密钥通过日志、插件或命令注入等方式泄露；
3. 需要实时监控代理的运行状态（如消息、工具调用、代理的思考过程等）；
4. 需要实现域名访问控制、输出内容过滤或设置交易限额；
5. 希望为代理的操作生成安全审计记录或证据记录。

## Vault-0 的主要功能

1. 使用 Argon2id 算法对 API 密钥进行 AES-256-GCM 加密；
2. 在程序启动时临时存储密钥（约 2 秒后自动清除）；
3. 通过 WebSocket 网关实现实时代理监控（包括消息、工具调用和代理状态）；
4. 提供可选的安全策略代理服务（地址：127.0.0.1:3840），支持域名访问控制、输出内容过滤等功能；
5. 提供基于 SHA-256 的证据记录系统，支持导出相关凭证；
6. 提供可选的 EVM 钱包功能，该钱包仅存储在 macOS 的 Keychain 中（私钥不会被暴露给代理或网页层）。

## 安全注意事项

1. 源代码可在 https://github.com/0-Vault/Vault-0 进行全面审计；
2. 安装过程仅需要从 GitHub 下载 DMG 文件（无需外部网络连接）。安装完成后，应用程序仅与本地主机通信（OpenClaw 代理：127.0.0.1:18789，可选的安全策略代理：127.0.0.1:3840）；
3. 用户也可以选择从源代码编译安装：`git clone https://github.com/0-Vault/Vault-0.git && cd Vault-0 && npm install && npm run tauri build`；
4. 可选的 EVM 钱包通过 keyring crate 生成 BIP-39 密码短语，并存储在 macOS Keychain 中（私钥不会被写入磁盘或传输）；
5. 安全策略代理仅在用户明确启动时运行，且仅监听本地地址（127.0.0.1）；
6. 目前该 DMG 文件尚未经过 Apple 的官方认证（因此可能需要支付 99 美元的年费以获得 Apple 开发者账户；首次启动时可能会遇到 Gatekeeper 的提示，可以通过右键点击“打开”来绕过此限制，或选择从源代码编译安装以获得完全信任）。

## 必需步骤

## 第一步：检查系统要求

Vault-0 仅支持 macOS 12 及更高版本。如果用户使用的是其他操作系统，请告知他们该工具仅适用于 macOS 12。

## 第二步：下载

根据用户的操作系统架构下载相应的版本：

```bash
VERSION=$(curl -s https://api.github.com/repos/0-Vault/Vault-0/releases/latest | grep '"tag_name"' | cut -d'"' -f4) && ARCH=$(uname -m) && if [ "$ARCH" = "arm64" ]; then SUFFIX="aarch64"; else SUFFIX="x86_64"; fi && echo "Downloading Vault-0 ${VERSION} for ${ARCH}..." && curl -sL "https://github.com/0-Vault/Vault-0/releases/download/${VERSION}/Vault-0_${VERSION}_${SUFFIX}.dmg" -o /tmp/Vault-0.dmg && echo "Downloaded to /tmp/Vault-0.dmg"
```

如果下载失败，用户可以手动从以下链接下载：https://github.com/0-Vault/Vault-0/releases

## 第三步：验证下载文件完整性

检查下载文件的 SHA-256 哈希值，并让用户与 GitHub 仓库中的哈希值进行比对：

```bash
shasum -a 256 /tmp/Vault-0.dmg
```

告知用户：“请确认下载文件的哈希值与 GitHub 仓库中的哈希值一致后再继续操作。”

等待用户确认后再进行下一步。

## 第四步：安装

```bash
hdiutil attach /tmp/Vault-0.dmg -nobrowse && cp -R "/Volumes/Vault-0/Vault-0.app" /Applications/ && hdiutil detach "/Volumes/Vault-0" && rm /tmp/Vault-0.dmg && echo "Vault-0 installed to /Applications"
```

## 第五步：启动应用程序

```bash
open /Applications/Vault-0.app
```

启动 Vault-0 后，它会自动检测用户的 OpenClaw 安装情况。

## 第六步：指导用户使用

向用户说明使用方法：

> “Vault-0 已经启动。您有三种选择：
> - **‘保护我的代理’（Secure My Agent）**：用于加密 API 密钥并增强系统安全性；
> - **‘仅监控’（Just Monitor）**：跳过安全设置，直接进入实时监控模式；
> - **‘安装 OpenClaw’**：如果需要重新安装 OpenClaw。
>
> 为了确保最高安全性，请选择‘保护我的代理’。您需要设置一个 12 个字符以上的 master 密码，然后点击‘立即加固’（Harden Now）来迁移密钥。”

## 第七步：验证加固效果（仅针对选择‘保护我的代理’的用户）

在用户确认加固完成后，检查 `.env` 文件中是否不再包含明文密钥：

```bash
head -1 ~/.openclaw/.env
```

`.env` 文件的第一行应显示“# Managed by Vault-0”。切勿直接查看文件内容。如果第一行与预期不符，请让用户查看 Vault-0 的控制面板。

## 第八步：确认使用效果

询问用户：“Vault-0 是否正常工作？您能看到控制面板或监控界面吗？”

---

## 参考信息

**界面功能**：

1. **概览**（Overview）：显示代理状态、加密库状态以及快速操作选项；
2. **监控**（Monitor）：提供实时双列视图（显示代理运行状态和安全防护情况）；
3. **密钥管理**（Secrets）：允许用户管理加密后的密钥（添加、编辑、删除、显示/隐藏）；
4. **钱包**（Wallet）：提供可选的 EVM 钱包功能，支持微支付（密钥仅存储在 macOS Keychain 中）；
5. **策略设置**（Policies）：允许用户编辑 YAML 格式的安全策略（包括域名访问控制、输出内容过滤、交易限额等）；
6. **活动记录**（Activity）：提供完整的事件记录，支持导出 SHA-256 格式的凭证。

## 卸载方法

要完全卸载 Vault-0，请执行以下操作：

```bash
rm -rf /Applications/Vault-0.app
rm -rf ~/Library/Application\ Support/Vault0
rm -rf ~/.config/vault0
```

卸载该应用程序后，系统会清除加密库和策略文件。需要注意的是，存储在 macOS Keychain 中的钱包密钥需要通过 Keychain Access（服务：vault0-wallet）手动删除。

## 系统要求

- macOS 12 及更高版本（支持 Apple Silicon 或 Intel 处理器）；
- 已安装 OpenClaw（使用命令 `npm install -g openclaw@latest`）。

## 相关链接

- 源代码：https://github.com/0-Vault/Vault-0
- 演示视频：https://youtu.be/FGGWJdeyY9g
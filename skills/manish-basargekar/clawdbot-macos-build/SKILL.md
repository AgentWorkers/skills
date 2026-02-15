---
name: clawdbot-macos-build
description: 从源代码构建 Clawdbot 的 macOS menu bar 应用程序。当您需要安装 Clawdbot.app 时，可以使用该工具（它可用于查看菜单栏状态、管理权限以及访问 Mac 的硬件资源，如摄像头和屏幕录制功能）。该工具会自动处理依赖项的安装、用户界面的构建、Swift 代码的编译、代码的签名以及应用程序的打包过程。
---

# Clawdbot macOS 应用程序构建

Clawdbot 的 macOS 配套应用程序提供了菜单栏状态显示、原生通知功能，以及访问 Mac 硬件（如摄像头、屏幕录制、系统命令）的能力。本文档将指导您从源代码开始构建该应用程序。

## 先决条件

- macOS (10.14 或更高版本)
- 安装了 Xcode 15 及以上版本，并启用了命令行工具
- Node.js 版本 >= 22
- 安装了 pnpm 包管理器
- 硬盘上有 30 GB 以上的空闲空间（用于存储 Swift 构建生成的文件）
- 拥有互联网连接（因为某些依赖项需要从网络上下载）

## 快速构建

```bash
# Clone repo
cd /tmp && rm -rf clawdbot-build && git clone https://github.com/clawdbot/clawdbot.git clawdbot-build

# Install + build
cd /tmp/clawdbot-build
pnpm install
pnpm ui:build

# Accept Xcode license (one-time)
sudo xcodebuild -license accept

# Build macOS app with ad-hoc signing
ALLOW_ADHOC_SIGNING=1 bash scripts/package-mac-app.sh

# Install to /Applications
cp -r dist/Clawdbot.app /Applications/Clawdbot.app

# Launch
open /Applications/Clawdbot.app
```

## 构建步骤说明

### 1. 克隆仓库
从 GitHub 克隆最新的 Clawdbot 源代码。其中包含用于 macOS 应用的代码，位于 `apps/macos/` 目录下。

### 2. 安装依赖项（使用 pnpm）
为整个项目安装 Node.js 相关的依赖项（大约需要 1 分钟）。如果某些扩展模块缺少二进制文件，系统会显示警告，但这些警告通常不影响构建过程。

### 3. 构建用户界面（使用 pnpm ui:build）
编译用户界面（使用 Vite 和 TypeScript/React 技术）。编译结果会被保存在 `dist/control-ui/` 目录中，耗时约 30 秒。

### 4. 同意 Xcode 许可协议
每次更新 Xcode 时都需要执行此步骤。如果在 Swift 构建过程中出现“许可协议未同意”的错误，请运行以下命令：
```bash
sudo xcodebuild -license accept
```

### 5. 打包 macOS 应用程序（使用 scripts/package-mac-app.sh）
执行完整的 Swift 构建流程：
- 下载 Swift 包依赖项（如 SwiftUI 库等）
- 为当前 Mac 架构编译应用程序（M1+ 系统使用 arm64 架构，Intel 系统使用 x86_64 架构）
- 将应用程序所需的资源（如模型目录、本地化文件等）打包到应用程序中
- 对应用程序进行代码签名

**签名选项：**
- **临时签名（Ad-hoc signing）**（速度最快）：设置 `ALLOW_ADHOC_SIGNING=1`；适用于本地测试，但生成的应用程序无法用于正式发布
- **开发者 ID 签名（Production signing）**：如果您拥有开发者签名证书，请设置 `SIGN_IDENTITY="Developer ID Application: <名称>"`

此步骤的耗时取决于您的 Mac 硬件配置，通常需要 10–20 分钟。

### 6. 将应用程序安装到 /Applications 文件夹
将构建完成的应用程序复制到系统的 Applications 文件夹中，这样它就可以像其他 macOS 应用程序一样正常运行了。

### 7. 启动应用程序
首次运行时，系统会请求您授权某些权限（如通知、访问屏幕录制功能等）——请同意这些权限以启用全部功能。

## 常见问题解决方法

### “工具版本不兼容”
Swift 构建需要 Xcode 6.2 或更高版本，请更新 Xcode：
```bash
softwareupdate -i -a
```

### “许可协议未同意”
按照上述步骤中的提示重新同意许可协议。

### “找不到签名身份”
对于本地构建，可以使用临时签名方式：
```bash
ALLOW_ADHOC_SIGNING=1 bash scripts/package-mac-app.sh
```

### Swift 编译过程卡住或运行缓慢
- 确保 Xcode 已经更新至最新版本：运行 `xcode-select --install` 或通过 App Store 更新
- 检查磁盘空间是否足够（至少需要 30 GB 的空闲空间）
- 关闭其他应用程序以释放内存

### 构建完成后应用程序无法启动
检查应用程序是否已正确签名：
```bash
codesign -v /Applications/Clawdbot.app
```

如果签名失败，请尝试将 `ALLOW_ADHOC_SIGNING` 设置为 `1` 后再重新构建。

## 应用程序的功能

- **菜单栏状态显示**：可以查看 Clawdbot 服务器的运行状态并接收通知
- **权限管理**：允许用户自定义与通知、屏幕录制、麦克风等功能相关的权限设置
- **本地/远程模式**：
  - **本地模式**：Clawdbot 服务器在用户的 Mac 上运行，应用程序负责管理启动服务
  - **远程模式**：应用程序通过 SSH/Tailscale 与远程服务器（如 VPS 或家庭服务器）建立连接，即使在 Mac 进入睡眠状态时也能保持连接
- **访问 Mac 硬件**：支持使用摄像头、屏幕录制功能，以及通过语音命令唤醒设备
- **深度链接**：可以通过 `clawdbot://` URL 协议触发服务器端的操作

更多详细信息请参阅官方文档：https://docs.clawd.bot/platforms/macos

## 面向发布的构建流程

如需将应用程序正式发布到 App Store，您需要：
- 拥有 Apple 开发者 ID 证书（需付费）
- 完成应用程序的官方认证流程（Notarization）

对于个人使用，临时签名方式即可满足需求。

## 下一步操作

应用程序启动后：
1. 完成权限设置（根据系统提示完成相关操作）
2. 选择 **本地模式** 或 **远程模式**
3. 在本地模式下，确保 Clawdbot 服务器正在运行（可以通过 `clawdbot gateway status` 命令检查）
4. 打开 Clawdbot.app 的菜单栏图标进行配置

之后，您可以通过终端来管理 Clawdbot 服务器：
```bash
clawdbot gateway status
clawdbot gateway restart
```
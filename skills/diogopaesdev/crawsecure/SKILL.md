# CrawSecure

CrawSecure 是为 ClawHub / OpenClaw 生态系统设计的一项以文档为核心的安全工具。该工具不包含可执行代码或二进制文件，其主要目的是清晰地记录、解释并指导用户如何安全地使用 CrawSecure CLI（该工具需要用户单独下载并安装）。

使用 CrawSecure 的目的是提升用户在处理第三方工具时的安全意识、透明度以及遵循最佳实践。

---

## 🔍 该工具提供的内容

- 详细说明 CrawSecure 的分析内容
- 对风险信号的解读及分类
- 安全使用 CrawSecure CLI 的操作指南
- 安全理念及信任边界

> ℹ️ 请注意：CrawSecure 本身不执行任何扫描操作，也不会运行任何代码。

---

## 🧰 关于 CrawSecure CLI

CrawSecure CLI 是一个可选的第三方工具，用户可以自行安装。它会在安装或使用 ClawHub / OpenClaw 工具之前，对这些工具进行本地的、离线的静态安全分析。

### CrawSecure CLI 的获取方式（外部资源）

- 源代码及发布版本：https://github.com/diogopaesdev/crawsecure
- 官方网站：https://crawsecure.com

CrawSecure CLI 并未随该安全工具一起打包提供。

---

## 🚨 CLI 分析的风险信号

在使用 CrawSecure CLI 时，它可能会检测到以下风险：

- 危险的命令模式（例如具有破坏性或与执行相关的操作）
- 对敏感文件或凭证的引用（例如 `.env`、`.ssh` 文件、私钥）
- 不安全或误导性行为的迹象

风险等级分为：

- **安全**（SAFE）
- **中等**（MEDIUM）
- **高**（HIGH）

---

## 🔒 安全性与信任边界

CrawSecure 具有以下特性：
- 不会执行任何代码
- 不会安装任何软件
- 不会访问网络
- 不会修改任何文件
- 仅请求 **只读** 权限

只有当用户从可信来源下载并运行 CrawSecure CLI 时，才会实际进行扫描操作。

---

## ✅ 何时使用该工具

- 了解 CrawSecure 的检查内容及其原因
- 在决定安装或运行 CrawSecure CLI 之前参考使用
- 作为开发更安全工具的参考依据
- 促进 ClawHub 生态系统内的透明度

---

## 📦 版本信息

**v2.0.1** – 仅用于澄清文档内容的版本

此版本明确了 CrawSecure 的使用范围，并消除了关于其是否包含可执行代码的歧义。
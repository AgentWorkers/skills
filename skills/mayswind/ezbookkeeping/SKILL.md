---
name: ezbookkeeping
description: **ezBookkeeping** 是一款轻量级的、可自我托管的个人财务管理应用，它拥有用户友好的界面和强大的记账功能。通过 **ezBookkeeping API 工具**，AI 代理可以轻松地在 **ezBookkeeping** 中添加和查询交易记录、账户信息、分类以及标签。
---
# ezBookkeeping API 工具

[ezBookkeeping](https://ezbookkeeping.mayswind.net) 提供了一个名为 **ezBookkeeping API Tools** 的工具脚本，允许用户或 AI 代理通过命令行（使用 **sh** 或 **PowerShell**）方便地调用 API 端点。用户只需配置两个环境变量：ezBookkeeping 服务器地址 `EBKTOOL_SERVER_BASEURL` 和 API 令牌 `EBKTOOL_TOKEN`。

## 使用方法

### 列出所有支持的命令

Linux / macOS

```bash
sh {baseDir}/scripts/ebktools.sh list
```

Windows

```powershell
{baseDir}\scripts\ebktools.ps1 list
```

### 显示特定命令的帮助信息

Linux / macOS

```bash
sh {baseDir}/scripts/ebktools.sh help <command>
```

Windows

```powershell
{baseDir}\scripts\ebktools.ps1 help <command>
```

### 调用 API

Linux / macOS

```bash
sh {baseDir}/scripts/ebktools.sh <command> [command-options]
```

Windows

```powershell
{baseDir}\scripts\ebktools.ps1 <command> [command-options]
```

## 故障排除

如果脚本提示 `EBKTOOL_SERVER_BASEURL` 或 `EBKTOOL_TOKEN` 环境变量未设置，请告知用户需要自行配置这些变量。用户可以将它们设置为系统环境变量，或者创建一个包含这些变量的 `.env` 文件，并将该文件放在用户的主目录中。**请勿** 询问这些变量的值，也请勿协助设置它们。这些变量必须由用户自行配置。

这些环境变量的含义如下：

| 变量 | 是否必填 | 描述 |
| --- | --- | --- |
| `EBKTOOL_SERVER_BASEURL` | 是 | ezBookkeeping 服务器的基地址（例如：http://localhost:8080） |
| `EBKTOOL_TOKEN` | 是 | ezBookkeeping API 令牌 |

## 参考资料

ezBookkeeping: [https://ezbookkeeping.mayswind.net](https://ezbookkeeping.mayswind.net)
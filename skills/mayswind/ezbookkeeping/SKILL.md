---
name: ezbookkeeping
description: **ezBookkeeping** 是一款轻量级的、可自我托管的个人财务管理应用，拥有用户友好的界面和强大的记账功能。通过 **ezBookkeeping API 工具**，AI 代理可以添加和查询交易记录、账户信息、分类以及标签。
---

# ezBookkeeping API 工具

[ezBookkeeping](https://ezbookkeeping.mayswind.net/) 提供了一个名为 **ezBookkeeping API Tools** 的工具脚本，允许用户或 AI 代理通过命令行（使用 **sh** 或 **PowerShell**）方便地调用 API 端点。您只需配置两个环境变量：ezBookkeeping 服务器地址和 API 令牌。

## 安装

Linux / macOS

```bash
curl https://raw.githubusercontent.com/mayswind/ezbookkeeping/refs/heads/main/scripts/ebktools.sh -o ebktools.sh
chmod +x ebktools.sh
```

Windows

```powershell
Invoke-WebRequest -Uri https://raw.githubusercontent.com/mayswind/ezbookkeeping/refs/heads/main/scripts/ebktools.ps1 -OutFile .\ebktools.ps1
```

## 环境变量

| 变量 | 必需 | 描述 |
| --- | --- | --- |
| `EBKTOOL_SERVER_BASEURL` | 必需 | ezBookkeeping 服务器的基地址（例如：http://localhost:8080） |
| `EBKTOOL_TOKEN` | 必需 | ezBookkeeping API 令牌 |

## 使用方法

### 列出所有支持的命令

Linux / macOS

```bash
./ebktools.sh list
```

Windows

```powershell
.\ebktools.ps1 list
```

### 显示特定命令的用法

Linux / macOS

```bash
./ebktools.sh help <command>
```

Windows

```powershell
.\ebktools.ps1 help <command>
```

### 调用 API

Linux / macOS

```bash
./ebktools.sh <command> [command-options]
```

Windows

```powershell
.\ebktools.ps1 <command> [command-options]
```

## 参考资料

ezBookkeeping: https://ezbookkeeping.mayswind.net/
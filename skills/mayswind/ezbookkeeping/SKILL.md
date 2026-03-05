---
name: ezbookkeeping
description: 使用 `ezBookkeeping API Tools` 脚本，在自托管的个人财务应用程序 `ezBookkeeping` 中记录新交易、查询交易信息、获取账户信息、获取分类信息、获取标签信息以及获取汇率数据。
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["EBKTOOL_SERVER_BASEURL", "EBKTOOL_TOKEN"] },
        "primaryEnv": "EBKTOOL_TOKEN"
      }
  }
---
# ezBookkeeping API 工具

## 使用方法

### 列出所有支持的命令

**Linux / macOS:**
```bash
sh scripts/ebktools.sh list
```

**Windows:**
```powershell
scripts\ebktools.ps1 list
```

### 显示特定命令的用法

**Linux / macOS:**
```bash
sh scripts/ebktools.sh help <command>
```

**Windows:**
```powershell
scripts\ebktools.ps1 help <command>
```

### 调用 API

**Linux / macOS:**
```bash
sh scripts/ebktools.sh [global-options] <command> [command-options]
```

**Windows:**
```powershell
scripts\ebktools.ps1 [global-options] <command> [command-options]
```

## 故障排除

如果脚本提示环境变量 `EBKTOOL_SERVER_BASEURL` 或 `EBKTOOL_TOKEN` 未设置，用户可以将其设置为系统环境变量，或者在用户的主目录下创建一个 `.env` 文件，其中包含这两个变量。

这些环境变量的含义如下：

| 变量 | 是否必填 | 说明 |
| --- | --- | --- |
| `EBKTOOL_SERVER_BASEURL` | 必填 | ezBookkeeping 服务器的基地址（例如：`http://localhost:8080`） |
| `EBKTOOL_TOKEN` | 必填 | ezBookkeeping API 的令牌 |

## 参考资料

ezBookkeeping: [https://ezbookkeeping.mayswind.net](https://ezbookkeeping.mayswind.net)
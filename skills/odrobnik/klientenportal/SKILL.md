---
name: klientenportal
description: "自动化使用 RZL Klientenportal.at 的流程：  
RZL Klientenportal.at 是由 RZL Software 开发的一个基于 Web 的门户平台，用于与您的税务会计师交换收据、发票和报告文件。您可以使用 Playwright 功能完成以下操作：  
- 登录/登出  
- 上传文件（Belegübergabe）  
- 查看已发布的文件列表  
- 下载税务相关文件（Kanzleidokumente）。"
summary: "RZL Klientenportal automation: upload receipts, download reports."
version: 1.5.0
homepage: https://github.com/odrobnik/klientenportal-skill
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["python3", "playwright"]
      python: ["playwright"]
      env: ["KLIENTENPORTAL_PORTAL_ID", "KLIENTENPORTAL_USER_ID", "KLIENTENPORTAL_PASSWORD"]
---

# RZL 客户门户

自动化 [klientenportal.at](https://klientenportal.at)——这是由 [RZL Software](https://www.rzl.at) 开发的一个 Web 门户，用于在客户与其税务会计师之间安全地交换会计文件。

**入口点：** `{baseDir}/scripts/klientenportal.py`

## 设置

有关先决条件和设置说明，请参阅 [SETUP.md](SETUP.md)。

## 命令

### 登录 / 注销

```bash
python3 {baseDir}/scripts/klientenportal.py login          # Test login (validates credentials)
python3 {baseDir}/scripts/klientenportal.py logout         # Clear stored browser session
```

### 上传文件（Belegübergabe）

将收据/发票上传到特定的文件分类类别：

```bash
python3 {baseDir}/scripts/klientenportal.py upload -f invoice.pdf --belegkreis KA
python3 {baseDir}/scripts/klientenportal.py upload -f *.xml --belegkreis SP
```

| 代码 | 名称 | 用途 |
|------|------|---------|
| ER | 收入发票 | 到来的发票（默认） |
| AR | 支出发票 | 发出的发票 |
| KA | 收银 | 信用卡付款 |
| SP | 商业银行 | 银行账户收据 |

### 列出已发布的文件

显示会计师已发布的文件：

```bash
python3 {baseDir}/scripts/klientenportal.py released
```

### 下载会计文件

下载会计师提供的所有文件：

```bash
python3 {baseDir}/scripts/klientenportal.py download                    # To default dir
python3 {baseDir}/scripts/klientenportal.py download -o /path/to/dir    # Custom output dir
```

一次性下载所有可用的会计文件。目前不支持单独选择文件。

默认输出路径：`/tmp/openclaw/klientenportal/`

### 选项

- `--visible` — 显示浏览器窗口（适用于调试或首次登录）

## 推荐的操作流程

```
login → upload / released / download → logout
```

完成所有操作后，请务必调用 `logout` 以清除浏览器会话中的数据。
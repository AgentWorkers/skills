---
name: george
description: "使用 Playwright 自动化 George 在线银行（Erste Bank / Sparkasse Austria）的操作：登录/登出、查看账户信息以及查询交易记录。"
summary: "George banking automation: login, accounts, transactions."
version: 1.4.1
homepage: https://github.com/odrobnik/george-skill
metadata:
  openclaw:
    emoji: "🏦"
    requires:
      bins: ["python3", "playwright"]
      python: ["playwright"]
---

# George银行自动化

该脚本用于获取所有账户类型（支票账户、储蓄账户、定期存款账户）的当前账户余额、股票投资组合及交易记录，并以JSON格式输出，以便进行自动化处理。它利用Playwright框架来自动化与George银行（Erste Bank / Sparkasse Austria）的交互。

**入口文件：** `{baseDir}/scripts/george.py`

## 设置

有关先决条件和设置说明，请参阅[SETUP.md](SETUP.md)。

## 命令

```bash
python3 {baseDir}/scripts/george.py login
python3 {baseDir}/scripts/george.py logout
python3 {baseDir}/scripts/george.py accounts
python3 {baseDir}/scripts/george.py transactions --account <id|iban> --from YYYY-MM-DD --until YYYY-MM-DD
```

## 推荐的操作流程

```
login → accounts → transactions → portfolio → logout
```

完成所有操作后，请务必调用`logout`命令，以清除浏览器会话中存储的数据（包括cookie、本地存储以及Playwright的相关配置信息）。这样可以减少持久化认证状态对系统造成的影响。

## 注意事项：
- 会话状态存储在`{workspace}/george/`目录下，该目录具有严格的权限设置（目录权限为700，文件权限为600）。
- 暂时性的数据输出默认存储在`/tmp/openclaw/george`目录中（可通过`OPENCLAW_TMP`环境变量进行覆盖）。